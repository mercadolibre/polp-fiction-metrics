from app.models.db.db import db
from app.models.db.permission import Permission
from datetime import datetime


# service_policies = db.Table(
#     'service_policy',
#     db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True),
#     db.Column('policy_id', db.Integer, db.ForeignKey('policy.id'), primary_key=True))

class Policy(db.Model):
    __tablename__ = "policy"
    id = db.Column(db.Integer, primary_key=True)
    arn = db.Column(db.String(500))
    scope = db.Column(db.String(500))
    name = db.Column(db.String(500))
    attachment_count = db.Column(db.Integer)
    description = db.Column(db.Text())
    is_attachable = db.Column(db.Boolean)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    job_uuid = db.Column(db.String(500), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    update_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    services = db.relationship("Policy", secondary="permission")
    permissions = db.relationship("Permission",cascade="all,delete")

    def __repr__(self):
        return self.arn

    @staticmethod
    def find_or_create(arn, account_id):
        policy = Policy.query.filter_by(arn=arn,account_id=account_id).first()
        if policy:
            return policy
        policy = Policy(arn=arn)
        db.session.add(policy)
        return policy
