from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import api  # Make sure routes/__init__.py has a Blueprint named 'api'

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configure your PostgreSQL connection
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql://splituser:PyJSCF7xUkzGJv3BI2fYtOVXzkVlvUDP@dpg-d18jn0ggjchc73972ar0-a/splitdb_4v6a'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize DB and register routes
    db.init_app(app)
    app.register_blueprint(api)

    return app
