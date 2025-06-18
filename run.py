from app import create_app
from app.extensions import db
from app.models import Person, Expense, Group  # Import all models

app = create_app()

# Run once to create tables
with app.app_context():
    db.create_all()
