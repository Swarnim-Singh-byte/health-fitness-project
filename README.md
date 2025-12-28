# 🏋️‍♂️ Health & Fitness Tracker

A full-stack Health & Fitness Tracking System built using FastAPI, PostgreSQL,
and Dash, designed to track daily calories, sleep, workouts, and mood with
real-time analytics.

---

## 📌 Features

- User management
- Calorie tracking (food-based)
- Sleep tracking with quality
- Workout tracking with auto calorie calculation
- Mood tracking with analytics
- Interactive dashboard with KPIs and charts
- Secure authentication (password hashing)
- Swagger API documentation

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Pydantic
- Uvicorn

### Dashboard
- Dash
- Plotly
- Dash Bootstrap Components

### Tools
- Git & GitHub
- Python Virtual Environment

---

## 📂 Project Structure

health-fitness-project/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── create_tables.py
│
├── dashboard.py
├── venv/              (ignored in git)
├── .gitignore
└── README.md

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
git clone https://github.com/Swarnim-Singh-byte/health-fitness-project.git
cd health-fitness-project

---

### 2. Create & Activate Virtual Environment
python3 -m venv venv
source venv/bin/activate

---

### 3. Install Dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic
pip install dash plotly dash-bootstrap-components pandas requests

---

### 4. Configure Database

Create the PostgreSQL database:

CREATE DATABASE health_fitness_db;

Update database URL if needed:
postgresql://postgres:postgres123@localhost:5432/health_fitness_db

---

### 5. Create Tables
python backend/create_tables.py

---

## ▶️ Running the Application

### Terminal 1 — Start Backend
source venv/bin/activate
uvicorn backend.main:app --reload

Swagger UI:
http://127.0.0.1:8000/docs

---

### Terminal 2 — Start Dashboard
source venv/bin/activate
python dashboard.py

Dashboard UI:
http://127.0.0.1:8050

---

## 🔐 Authentication

- Passwords are securely hashed
- Login and register APIs available
- No plain-text password storage

---

## 📊 Dashboard Analytics

- Total calories consumed
- Average sleep hours
- Workout frequency
- Mood trends
- Date-wise graphs and summaries

---

## 🧠 Design Decisions

- FastAPI chosen for speed and automatic API documentation
- Dash used for rapid analytics and Python-based visualization
- PostgreSQL for relational integrity and scalability
- ORM used to prevent SQL injection and improve maintainability

---

## 🧪 Testing

All APIs tested using:
- Swagger UI
- Live Dashboard interactions

---

## 📚 Future Enhancements

- JWT-based authentication
- Mobile-friendly frontend
- Advanced analytics (weekly/monthly reports)
- Cloud deployment

---

## 👨‍💻 Author

Swarnim Singh  
B.Tech CSE (AI & Data Engineering)

---

## 📄 License

This project is for educational purposes.

---

## 🏁 Final Note

This project demonstrates backend API design, database modeling,
authentication, and real-time data analytics using modern Python frameworks.

