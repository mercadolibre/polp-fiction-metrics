from app.models.db.db import db
from app.models.db.user import User
from app.models.db.role import Role
from datetime import datetime
from app.config import BLACK_LIST


class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(500), nullable=False)
    foreign = db.Column(db.Boolean(), nullable=False)
    blacklisted = db.Column(db.Boolean())
    job_uuid = db.Column(db.String(500), nullable=False)
    name = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    roles = db.relationship('Role', backref='account', lazy=True)
    users = db.relationship('User', backref='account', lazy=True)
    policies = db.relationship('Policy', backref='account', lazy=True)

    def __repr__(self):
        return self.uuid

    def __eq__(self, other):
        return isinstance(other, Account) and self.uuid == other.uuid

    @staticmethod
    def find_or_create(uuid, foreign=False):
        blacklisted = uuid in BLACK_LIST
        account = Account(uuid=uuid, foreign=foreign, blacklisted=blacklisted)
        for o in db.session:
            if account == o:
                return o
        account_in_db = db.session.query(Account).filter_by(uuid=uuid).first()
        if account_in_db:
            db.session.add(account_in_db)
            return account_in_db
        db.session.add(account)
        return account
