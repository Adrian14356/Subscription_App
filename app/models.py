from __future__ import annotations
from app import db, bcrypt
from datetime import datetime



class Users(db.Model):
    __tablename__ = "user"
    _id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(60), nullable=False)
    password = db.Column(db.String(400), nullable=False)
    subscriptions = db.relationship("Subscriptions", backref="Users")

    def __init__(self, user_name, email, password):
        self.user_name = user_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")


class Subscriptions(db.Model):
    __tablename__ = "subscriptions"
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    price = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user._id"), nullable=False)

    def __init__(self, name, start_date, user_id, price):
        self.name = name
        self.start_date = datetime.strptime(start_date, "%d-%m-%Y")
        self.price = price
        self.user_id = user_id
