from app.models.db.db import db
from datetime import datetime
from sqlalchemy.orm import validates



role_policies = db.Table(
    'role_policy',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('policy_id', db.Integer, db.ForeignKey('policy.id'), primary_key=True)
)

trusted_role_users = db.Table(
    'trusted_role_user',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

trusted_role_roles = db.Table(
    'trusted_role_role',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('assuming_role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)

trusted_role_accounts = db.Table(
    'trusted_role_account',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('account_id', db.Integer, db.ForeignKey('account.id'), primary_key=True)
)

trusted_role_services = db.Table(
    'trusted_role_service',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('service.id'), primary_key=True)
)


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    arn = db.Column(db.String(500))
    name = db.Column(db.String(500))
    ext_entity_compliance = db.Column(db.Boolean(), nullable=False)
    last_used = db.Column(db.DateTime)
    last_used_region = db.Column(db.String(500))
    inline_count = db.Column(db.Integer)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    policies = db.relationship("Policy", secondary=role_policies, lazy='subquery', backref='roles')
    trusted_users = db.relationship("User", secondary=trusted_role_users, lazy='subquery')
    trusted_accounts = db.relationship("Account", secondary=trusted_role_accounts, lazy='subquery')
    trusted_services = db.relationship("Service", secondary=trusted_role_services, lazy='subquery')
    foreign = db.Column(db.Boolean(), nullable=False)
    job_uuid = db.Column(db.String(500), nullable=False)
    create_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)

    trusted_roles = db.relationship("Role",
            secondary=trusted_role_roles,
            primaryjoin=id == trusted_role_roles.c.role_id,
            secondaryjoin=id == trusted_role_roles.c.assuming_role_id,
            lazy='subquery')

    def __repr__(self):
        return self.arn

    def __eq__(self, other):
        return isinstance(other, Role) and self.arn == other.arn

    @staticmethod
    def find_or_create(arn, foreign=False):
        role = Role(arn=arn, foreign=foreign)
        for o in db.session:
            if role == o:
                return o
        role_in_db = db.session.query(Role).filter_by(arn=arn).first()
        if role_in_db:
            db.session.add(role_in_db)
            return role_in_db
        db.session.add(role)
        return role

