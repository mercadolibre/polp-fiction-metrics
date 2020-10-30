from flask import Blueprint


ping = Blueprint("ping", __name__)

@ping.route("/ping")
def main():
    # newrelic.agent.ignore_transaction(flag=True)
    return "pong"
