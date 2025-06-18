# app/models.py
from .extensions import db

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    paid_by = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    split_between = db.Column(db.ARRAY(db.String), nullable=True)  # PostgreSQL specific

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "paid_by": self.paid_by,
            "group_id": self.group_id,
            "split_between": self.split_between
        }

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "group_id": self.group_id
        }

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    people = db.relationship("Person", backref="group", lazy=True)
