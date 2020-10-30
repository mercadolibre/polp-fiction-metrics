#!/bin/python      
from __future__ import absolute_import

import os
from sys import argv

import docker
import py

NAME_GRAFANA = "polp_grafana"
NETWORK_NAME = "polpnet"

MYSQL_PORT = 3308
NAME_MYSQL = "polp_mysql"
MYSQL_DATABASE = "polpdb"
MYSQL_USER = "polpuser"
MYSQL_PASSWORD = "polpsecret"
MYSQL_ROOT_PASSWORD = "toor"

top_options = 4
[argv.append("0") for n in range(top_options)]


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


cli_help = f"""
{bcolors.BOLD}{bcolors.OKBLUE}Usage:{bcolors.ENDC}
  command [arguments] [options]

{bcolors.BOLD}{bcolors.OKBLUE}Global Options:{bcolors.ENDC}

  -v, --verbose      Verbosity for all commands

{bcolors.BOLD}{bcolors.OKBLUE}Available Commands:{bcolors.ENDC}
 {bcolors.BOLD}{bcolors.OKGREEN}serve{bcolors.ENDC}                 Starts the API server
 {bcolors.BOLD}{bcolors.OKGREEN}test{bcolors.ENDC}                  Run tests inside "./tests" server
 {bcolors.BOLD}{bcolors.OKGREEN}clean{bcolors.ENDC}                 Cleans Database and Grafana containers
 {bcolors.OKGREEN}populate{bcolors.ENDC}              Populates the database (SOON)

 {bcolors.BOLD}{bcolors.OKGREEN}db, database{bcolors.ENDC}
  {bcolors.BOLD}  up{bcolors.ENDC}                 Starts mysql docker container with the database
  {bcolors.BOLD}  info{bcolors.ENDC}               Get database connection info

{bcolors.BOLD}{bcolors.OKGREEN} migrations{bcolors.ENDC}
  {bcolors.BOLD}  refresh{bcolors.ENDC}            Refreshes Database state by running migrations back and forward
  {bcolors.BOLD}  run{bcolors.ENDC}                Run alembic migrations
  {bcolors.BOLD}  create{bcolors.ENDC}             Creates a new Alembic Revision (Migration) file

{bcolors.BOLD}{bcolors.OKBLUE}Miscellaneous:{bcolors.ENDC}
 {bcolors.BOLD}{bcolors.OKGREEN}fiction{bcolors.ENDC}               Say what one more time !
 {bcolors.BOLD}{bcolors.FAIL}grafana{bcolors.ENDC}               Start grafana server on port 3000 to monitor Polp's Database
"""

db_info = f"""
Host:       localhost
Port:       {MYSQL_PORT}
Database:   polpdb
User:       polpuser
Password:   polsecret
"""

PWD = os.getcwd()
CLI_ROOT = os.path.realpath(os.path.join(os.path.dirname(__file__)))
REPO_ROOT = CLI_ROOT[:-len("scripts")]

DESC = "Polp cli helps you move arround inside the Polp fiction project"

dclient = docker.from_env()


def migrations(command):
    output = dclient.containers.run("contre95/alembic", command,
                                    auto_remove=True,
                                    stderr=True,
                                    stream=True,
                                    stdout=True,
                                    network_mode="host",
                                    volumes={REPO_ROOT + 'db/migrations': {'bind': '/srv'}},
                                    )
    return output


def check_container(container_name):
    for c in dclient.containers.list():
        if c.attrs.get('Name')[1:] == container_name:
            return True
    return False


def clean_containers():
    msg = "Everything is already cleaned"
    for c in dclient.containers.list():
        if c.attrs.get('Name')[1:] in [NAME_MYSQL, NAME_GRAFANA]:
            c.stop()
            msg = "Container and Networks cleaned"
    for n in dclient.networks.list():
        if n.attrs.get('Name') in [NETWORK_NAME]:
            n.remove()
            msg = "Container and Networks cleaned"
    print(msg)


def mysql_up():
    dclient.networks.create(name=NETWORK_NAME, driver="bridge")
    mysql_db_container = dclient.containers.run("mysql:latest",
                                                command="--default-authentication-plugin=mysql_native_password",
                                                auto_remove=True,
                                                detach=True,
                                                name=NAME_MYSQL,
                                                network=NETWORK_NAME,
                                                # restart_policy = {"Name": "always"},
                                                volumes={REPO_ROOT + 'db/mysql_data': {'bind': '/var/lib/mysql'}},
                                                ports={'3306': MYSQL_PORT},
                                                # working_dir = "./db",
                                                environment=[
                                                    f"MYSQL_DATABASE={MYSQL_DATABASE}",
                                                    f"MYSQL_USER={MYSQL_USER}",
                                                    f"MYSQL_PASSWORD={MYSQL_PASSWORD}",
                                                    f"MYSQL_ROOT_PASSWORD={MYSQL_ROOT_PASSWORD}",
                                                ]
                                                )
    print(mysql_db_container.logs())
    print(db_info)


def grafana():
    if not os.path.exists(REPO_ROOT + "db/grafana/data"):
        os.mkdir(REPO_ROOT + "db/grafana/data")
    grafana_container = dclient.containers.run("grafana/grafana:latest-ubuntu",
                                               auto_remove=True,
                                               name=NAME_GRAFANA,
                                               network=NETWORK_NAME,
                                               detach=True,
                                               volumes={
                                                   REPO_ROOT + 'db/grafana/data': {'bind': '/var/lib/grafana/data'},
                                                   REPO_ROOT + 'db/grafana/provisioning': {
                                                       'bind': '/etc/grafana/provisioning'}
                                               },
                                               environment=[
                                                   "GF_INSTALL_PLUGINS=grafana-piechart-panel,snuids-radar-panel,marcusolsson-treemap-panel",
                                               ],
                                               ports={'3000': 8080})
    print(f"Done! Just give it a minute \n {grafana_container.logs()}")
    print("http://localhost:8080 \n Default pass is admin:admin")
    print("Remember this grafana is not production ready. Remember to change your password on the you first login.")


def run_tests(cov=False):
    os.environ['SCOPE'] = 'test'
    if cov:
        py.test.cmdline.main(["--cov=./app", REPO_ROOT + "tests"])
    else:
        py.test.main([REPO_ROOT + "tests"])


def main():
    command = argv[1]
    choice_2nd = argv[2]
    choice_3rd = argv[3]

    if command in {"-h", "--help", "help"}:
        print(cli_help)

    elif command in ['run', 'serve'] and choice_2nd == "0":
        os.system("flask run --reload")

    elif command in ['test', 'pytest']:
        if choice_2nd in ['--cov', '-s']:
            run_tests(cov=True)
            return
        run_tests()

    elif command in ['db', 'database']:
        if choice_2nd == 'info':
            print(db_info)
        elif choice_2nd == 'up':
            if check_container(NAME_MYSQL):
                print(f"Are you sure the Database isn't already running ? \n")
                print(f"Please run 'polp clean' to refresh containers state")
                return
            try:
                mysql_up()
            except docker.errors.ContainerError as e:
                print(f"Something went wrong with the db :( \n\n {e}")
            except docker.errors.APIError as e:
                print(f"Are you sure the Database isn't already running ? \n\n {e}")
        else:
            print(f"Hmm.. {bcolors.BOLD}{bcolors.FAIL}{choice_2nd}{bcolors.ENDC} is not a valid command for {command}")

    elif command in ['grafana']:
        if check_container(NAME_GRAFANA):
            print(f"Are you sure Grafana isn't already running ? 'http://localhost:8080'\n")
            print(f"You can also run 'polp clean' to refresh containers state")
            return
        if not check_container(NAME_MYSQL):
            print(f"Please try running the database first ('polp db up')\n")
            print(f"You can also run 'polp clean' to refresh containers state")
            return

        grafana()
    elif command in ['clean']:
        clean_containers()
    elif command in ['migrations']:
        if choice_2nd == "run":
            output_run = migrations("upgrade head")
            if choice_3rd in ["-v", "--verbose"]:
                for o in list(output_run):
                    print(o.decode('utf-8').strip('\n'))
            print(f"{bcolors.BOLD}{bcolors.OKGREEN}Migrations are up to date.{bcolors.ENDC}")
        elif choice_2nd == "create":
            output_run = migrations("revision")
            if choice_3rd in ["-v", "--verbose"]:
                for o in list(output_run):
                    print(o.decode('utf-8').strip('\n'))
            print(f"Go check db/migrations/versions :)")
            print(f"{bcolors.BOLD}{bcolors.OKGREEN}New migration file template created successfully.{bcolors.ENDC}")

        elif choice_2nd == "refresh":
            print("Refreshing db")
            output_base = migrations("downgrade base")
            output_run = migrations("upgrade head")
            if choice_3rd in ["-v", "--verbose"]:
                for o in list(output_base) + list(output_run):
                    print(o.decode('utf-8').strip('\n'))
            print(f"{bcolors.BOLD}{bcolors.OKGREEN}Migrations are up to date.{bcolors.ENDC}")
        else:
            print(f"Hmm.. {bcolors.BOLD}{bcolors.FAIL}{choice_2nd}{bcolors.ENDC} is not a valid command for {command}")

    elif command in ['fiction']:
        with open('scripts/motd.txt', 'r') as file:
            data = file.read()
        print(data)
    else:
        print('Hmm... not sure what you meant. :(')
