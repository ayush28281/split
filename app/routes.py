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
    group_name = data.get("group")
    split_between = data.get("split_between", [])

    if not description or not paid_by or not isinstance(amount, (int, float)) or amount <= 0:
        return jsonify({"success": False, "message": "Invalid input"}), 400

    # Handle group
    group = None
    if group_name:
        group = Group.query.filter_by(name=group_name).first()
        if not group:
            group = Group(name=group_name)
            db.session.add(group)
            db.session.commit()

    # Ensure payer exists
    person = Person.query.filter_by(name=paid_by).first()
    if not person:
        person = Person(name=paid_by, group_id=group.id if group else None)
        db.session.add(person)

    # Ensure all people in split_between exist
    for name in split_between:
        p = Person.query.filter_by(name=name).first()
        if not p:
            p = Person(name=name, group_id=group.id if group else None)
            db.session.add(p)

    db.session.commit()

    # Record expense
    expense = Expense(
        amount=amount,
        description=description,
        paid_by=paid_by,
        group_id=group.id if group else None,
        split_between=split_between
    )
    db.session.add(expense)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": {
            "id": expense.id,
            "group": group.name if group else None,
            "paid_by": paid_by,
            "split_between": split_between,
            "description": description,
            "amount": amount
        },
        "message": "Group expense added successfully"
    }), 201

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
    groups = Group.query.all()
    people = Person.query.all()
    expenses = Expense.query.all()

    if not groups or not people or not expenses:
        return jsonify({"success": True, "data": [], "message": "No data to calculate settlements."})

    settlements_data = []

    for group in groups:
        group_expenses = [e for e in expenses if e.group_id == group.id]
        group_people = [p.name for p in people if p.group_id == group.id]

        if not group_expenses or not group_people:
            continue

        balances = {name: 0.0 for name in group_people}

        for expense in group_expenses:
            amount = expense.amount
            paid_by = expense.paid_by
            split_between = expense.split_between if expense.split_between else group_people

            split_count = len(split_between)
            if split_count == 0:
                continue

            share = amount / split_count
            for name in split_between:
                balances[name] -= share
            balances[paid_by] += amount

        group_settlements = []
        for person, balance in balances.items():
            group_settlements.append({
                "name": person,
                "balance": round(balance, 2)
            })

        settlements_data.append({
            "group": group.name,
            "settlements": group_settlements
        })

    return jsonify({"success": True, "data": settlements_data})
