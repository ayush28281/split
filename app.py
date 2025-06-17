from flask import Flask
from database import db, init_db
from routes import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)
app.register_blueprint(api)

@app.route("/")
def index():
    return {"message": "Split App API is running!"}

if __name__ == "__main__":
    app.run(debug=True)
