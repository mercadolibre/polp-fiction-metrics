from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autoflush": False, 'expire_on_commit': False})
# db = SQLAlchemy(session_options={"autoflush": False, "autocommit": True})
