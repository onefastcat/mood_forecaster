from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    data_points = db.relationship('DataPoint', backref='users')


class DataPoint(db.Model):
    __tablename__ = 'datapoints'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    mood_value = db.Column(db.Integer, nullable=False)
    energy_value = db.Column(db.Integer, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    pressure = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.Date, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
