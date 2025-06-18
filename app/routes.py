from flask import request, jsonify, Blueprint
from .models import Person, Expense
from database import db  # adjust based on your project layout

api = Blueprint("api", __name__)

@api.route("/expenses", methods=["POST"])
def add_expense():
    data = request.get_json()
    amount = data.get("amount")
    description = data.get("description")
    paid_by = data.get("paid_by")

    if not description or not paid_by or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"success": False, "message": "Invalid input"}), 400

    person = Person.query.filter_by(name=paid_by).first()
    if not person:
        person = Person(name=paid_by)
        db.session.add(person)

    expense = Expense(amount=amount, description=description, paid_by=paid_by)
    db.session.add(expense)
    db.session.commit()
    return jsonify({"success": True, "data": {"id": expense.id}, "message": "Expense added successfully"}), 201

@api.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify({
        "success": True,
        "data": [e.to_dict() for e in expenses]
    })

@api.route("/people", methods=["GET"])
def get_people():
    people = Person.query.all()
    return jsonify({
        "success": True,
        "data": [{"id": p.id, "name": p.name} for p in people]
    })