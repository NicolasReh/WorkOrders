
# models.py

from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Workorder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_required = db.Column(db.DateTime)
    user = db.Column(db.String(1000), default='ADMIN')
    client = db.Column(db.String(1000))
    title = db.Column(db.String(1000))
    parts = db.relationship('Part', backref='workorder', lazy=True, cascade="all, delete-orphan")

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.String(1000), default='ADMIN')
    name = db.Column(db.String(1000), nullable=False)
    code = db.Column(db.String(1000), nullable=False)
    qty = db.Column(db.Integer, nullable=False, default=1)
    finished = db.Column(db.Boolean, default=False)
    wo_id = db.Column(db.Integer, db.ForeignKey('workorder.id'), nullable=False)