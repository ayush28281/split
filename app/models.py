from database import db

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    paid_by = db.Column(db.String(100), nullable=False)  # Ideally use user_id

    def to_dict(self):
        return {
            "id": self.id,
            "amount": self.amount,
            "description": self.description,
            "paid_by": self.paid_by
        }

    def __repr__(self):
        return f"<Expense {self.id}: {self.description}, ₹{self.amount}>"

# Dummy Person class if you need it for imports (you can expand later)
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Person {self.id}: {self.name}>"
