import os
import json

with open("app/config.json") as json_data_file:
        data = json.load(json_data_file)

SCOPE = os.environ.get('SCOPE','local')
BLACK_LIST = data[SCOPE].get("blacklist").split(",")
POLP_FICTION_ROLE = data[SCOPE]["iam"].get("polp-role")
POLP_FICTION_ORGANIZATIONS_ROLE = data[SCOPE]["iam"].get("polp-organization-role")
POLP_FICTION_MASTER_ACCOUNT = data[SCOPE]["iam"].get("polp-master-account")
AWS_ACCESS_KEY_ID = data[SCOPE]["iam"].get("aws_access_key_id", os.environ.get("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = data[SCOPE]["iam"].get("aws_secret_access_key", os.environ.get("AWS_SECRET_ACCESS_KEY"))
DB_USER = data[SCOPE]["mysql"].get("user")
DB_PASS = data[SCOPE]["mysql"].get("passwd")
DB_HOST = data[SCOPE]["mysql"].get("host")
DB_NAME = data[SCOPE]["mysql"].get("db")
DB_PORT = data[SCOPE]["mysql"].get("port")
DB_URI = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
