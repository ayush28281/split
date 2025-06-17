from flask import Blueprint, request, jsonify
from models import Expense
from database import db

api = Blueprint("api", __name__)

@api.route("/expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([e.to_dict() for e in expenses])

@api.route("/expenses", methods=["POST"])
def add_expense():
    data = request.json
    if not data.get("amount") or not data.get("description") or not data.get("paid_by"):
        return jsonify({"error": "Invalid input"}), 400
    expense = Expense(
        amount=data["amount"],
        description=data["description"],
        paid_by=data["paid_by"]
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify(expense.to_dict()), 201
