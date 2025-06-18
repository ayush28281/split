import os
from flask import Flask
from database import db, init_db
from routes import api

app = Flask(__name__)

# Ensure DATABASE_URL is set
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in environment variables.")

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and routes
init_db(app)
app.register_blueprint(api)

@app.route("/")
def index():
    return {"message": "Split App API is running!"}

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
