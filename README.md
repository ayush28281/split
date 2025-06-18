# Split App Backend – Expense Sharing System

This is a backend API built using Flask that allows users to manage shared expenses within groups. Users can add expenses, group members, and track settlements efficiently. The API is publicly hosted on Render.

---

##  Tech Stack

- Python 3.10+
- Flask
- SQLAlchemy
- PostgreSQL (via Render)
- Gunicorn (for WSGI deployment)
- Render (Free Hosting)

---


### 1. Clone the Repository
```bash
git clone https://github.com/your-username/split-app-backend.git
cd split-app-backend


##Create Virtual Environment & Install Dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt



##Configure Environment (if local)

DATABASE_URL=your_postgres_connection_string


##Deployed API https://split-hvd7.onrender.com

Use this URL for all Postman requests and frontend integration.



##API Endpoints
 Root
GET / → Health check

People
GET /people → List all users

 Groups
POST /groups → Create a new group

GET /groups → List all groups

 Expenses
POST /expenses → Add a new expense

GET /expenses → View all expenses

 Settlements
POST /settlements → Record a settlement between users

GET /settlements → View all settlements