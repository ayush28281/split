from flask import request, jsonify, Blueprint
from .models import Person, Expense, Group
from .extensions import db

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def index():
    return {"message": "Split App is Live"}, 200

# ---------------------- EXPENSES ----------------------
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

# ---------------------- PEOPLE ----------------------
@api.route("/people", methods=["GET"])
def get_people():
    people = Person.query.all()
    return jsonify({
        "success": True,
        "data": [{"id": p.id, "name": p.name} for p in people]
    })

# ---------------------- GROUPS ----------------------
@api.route("/groups", methods=["POST"])
def create_group():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"success": False, "message": "Group name is required"}), 400

    if Group.query.filter_by(name=name).first():
        return jsonify({"success": False, "message": "Group already exists"}), 409

    group = Group(name=name)
    db.session.add(group)
    db.session.commit()

    return jsonify({"success": True, "data": {"id": group.id, "name": group.name}}), 201

@api.route("/groups", methods=["GET"])
def list_groups():
    groups = Group.query.all()
    return jsonify({
        "success": True,
        "data": [{"id": g.id, "name": g.name} for g in groups]
    })

# ---------------------- SETTLEMENTS ----------------------
@api.route("/settlements", methods=["GET"])
def get_settlements():
    people = Person.query.all()
    expenses = Expense.query.all()

    if not people or not expenses:
        return jsonify({"success": True, "data": [], "message": "No data to calculate settlements."})

    total_expense = sum(e.amount for e in expenses)
    per_person = total_expense / len(people)
    
    paid = {p.name: 0 for p in people}
    for e in expenses:
        paid[e.paid_by] += e.amount

    settlements = []
    for p in people:
        balance = round(paid[p.name] - per_person, 2)
        settlements.append({
            "name": p.name,
            "paid": round(paid[p.name], 2),
            "should_have_paid": round(per_person, 2),
            "balance": balance
        })

    return jsonify({"success": True, "data": settlements})
