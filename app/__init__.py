from flask_sqlalchemy import SQLAlchemy
from app.controllers.populate import populates
from app.controllers.accounts import accounts
from app.controllers.ping import ping
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

from app.config import DB_URI, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

ACTIVE_ENDPOINTS = (
    ("/", [], ping),
    ('/v1/job/populate', ['jobs', 'test', 'local', 'single-account'], populates),
    ('/v1/job/account', ['jobs', 'test', 'local'], accounts)
    )

print(f'SCOPE set to: {os.environ.get("SCOPE")}')
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI #Connectar con proxySQL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Setting this paramete due to a SQLAlchemy Warning, can be removed of future versions of the package.
    os.environ['AWS_ACCESS_KEY_ID'] = AWS_ACCESS_KEY_ID
    os.environ['AWS_SECRET_ACCESS_KEY'] = AWS_SECRET_ACCESS_KEY
    db = SQLAlchemy(app)
    db.init_app(app)
    app.url_map.strict_slashes = False
    for url, scopes, blueprint in ACTIVE_ENDPOINTS:
        if os.environ.get('SCOPE') in scopes or not scopes:
            app.register_blueprint(blueprint, url_prefix=url)
    return app

