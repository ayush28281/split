from app import create_app
from app.extensions import db
from app.models import Person, Expense, Group  # Ensure all your models are imported

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # This will create all tables if they don't exist
    app.run(host="0.0.0.0", port=5000)
