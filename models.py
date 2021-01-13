from datetime import datetime
from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    publish_date = db.Column(db.DateTime, default=datetime.now())
    changed_date = db.Column(db.DateTime, default=datetime.now())
    title = db.Column(db.String(140))
    description = db.Column(db.Text, default=None)
    status = db.Column(db.Boolean, default=False, server_default="false")
    desk_id = db.Column(db.Integer, db.ForeignKey('desk.id'), nullable=False)
        


class Desk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    publish_date = db.Column(db.DateTime)
    changed_date= db.Column(db.DateTime)
    tasks = db.relationship('Task', cascade="all, delete-orphan", backref='desk', lazy=True)