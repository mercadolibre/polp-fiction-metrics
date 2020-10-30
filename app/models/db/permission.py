from app.models.db.db import db
from app.models.db.service import Service
from datetime import datetime


class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policy.id'), nullable=False)
    last_used = db.Column(db.DateTime)
    reading = db.Column(db.Boolean(), default=False, nullable=False)
    writing = db.Column(db.Boolean(), default=False, nullable=False)
    job_uuid = db.Column(db.String(500), nullable=False)
    listing = db.Column(db.Boolean(), default=False, nullable=False)
    managing = db.Column(db.Boolean(), default=False, nullable=False)
    tagging = db.Column(db.Boolean(), default=False, nullable=False)
    last_auth_entity = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    # service = db.relationship('Service', lazy=True)
    # policy = db.relationship("Policy", backref="permissions")
    service = db.relationship("Service", backref="permissions")

    def __eq__(self, other):
        return isinstance(other, Permission) and self.policy_id == other.policy_id and self.service_id == other.service_id
