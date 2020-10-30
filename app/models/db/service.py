from app.models.db.db import db
from datetime import datetime


class Service(db.Model):
    __tablename__ = "service"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    holds_data = db.Column(db.Boolean())
    critical = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now)
    # policy = db.relationship("Permission", back_populates="service")

    def __repr__(self):
        return self.name


    @staticmethod
    def find_or_create(name):
        service = Service.query.filter_by(name=name).first()
        if service:
            return service
        service = Service(name=name)
        db.session.add(service)
        return service
