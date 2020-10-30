from app.models.db.db import db
from app.models.db.policy import Policy
from datetime import datetime

user_policies = db.Table(
    'user_policy',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('policy_id', db.Integer, db.ForeignKey('policy.id'), primary_key=True))


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    last_auth = db.Column(db.DateTime)
    arn = db.Column(db.String(500))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    foreign = db.Column(db.Boolean(), nullable=False)
    inline_count = db.Column(db.Integer)
    create_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    job_uuid = db.Column(db.String(500), nullable=False)
    policies = db.relationship("Policy", secondary=user_policies, lazy='subquery', backref='users')

    def __repr__(self):
        return self.arn

    def __eq__(self, other):
        return isinstance(other, User) and self.arn == other.arn

    @staticmethod
    def find_or_create(arn, foreign=False):
        user = User(arn=arn, foreign=foreign)
        for o in db.session:
            if user == o:
                return o
        user_in_db = db.session.query(User).filter_by(arn=arn).first()
        if user_in_db:
            db.session.add(user_in_db)
            return user_in_db
        db.session.add(user)
        return user


