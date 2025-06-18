# app/__init__.py
from flask import Flask
from .extensions import db
from .routes import api

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://splituser:PyJSCF7xUkzGJv3BI2fYtOVXzkVlvUDP@dpg-d18jn0ggjchc73972ar0-a/splitdb_4v6a'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(api)

    return app
