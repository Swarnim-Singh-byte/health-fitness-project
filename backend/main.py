from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from datetime import date

from database import SessionLocal
from models import User, Sleep
from schemas import SleepByName, WorkoutByName

# -------------------- DB DEPENDENCY --------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- APP SETUP --------------------
app = FastAPI(title="Health & Fitness Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- DATABASE --------------------
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/health_fitness_db"
engine = create_engine(DATABASE_URL)

# -------------------- MASTERS --------------------
FOOD_CALORIES = {
    "rice": 350,
    "roti": 120,
    "banana": 105,
    "apple": 95,
    "oats": 250,
    "chicken": 400,
}

WORKOUT_CALORIES = {
    "lunges": 230,
    "squats": 250,
    "pushups": 180,
    "plank": 120,
    "jumping jacks": 200,
    "burpees": 300,
    "running": 400,
}

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"status": "API running successfully"}

# -------------------- USERS --------------------
@app.post("/users/get-or-create", tags=["Users"])
def get_or_create_user(name: str):
    with engine.begin() as conn:
        user = conn.execute(
            text("SELECT user_id FROM users WHERE LOWER(name)=LOWER(:n)"),
            {"n": name},
        ).fetchone()

        if user:
            return {"user_id": user[0], "status": "existing"}

        new_user = conn.execute(
            text(
                "INSERT INTO users (name, age, height, weight, goal) "
                "VALUES (:n, 0, 0, 0, 'General') RETURNING user_id"
            ),
            {"n": name},
        ).fetchone()

    return {"user_id": new_user[0], "status": "created"}

# -------------------- CALORIES --------------------
@app.post("/calories/add-by-name", tags=["Calories"])
def add_calorie_by_name(name: str, food: str, entry_date: date):
    food_key = food.lower()

    if food_key not in FOOD_CALORIES:
        raise HTTPException(status_code=400, detail="Food not found")

    calories = FOOD_CALORIES[food_key]

    with engine.begin() as conn:
        user = conn.execute(
            text("SELECT user_id FROM users WHERE LOWER(name)=LOWER(:n)"),
            {"n": name},
        ).fetchone()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        conn.execute(
            text("""
                INSERT INTO calories (user_id, food_name, calories, date)
                VALUES (:u, :f, :c, :d)
            """),
            {"u": user[0], "f": food, "c": calories, "d": entry_date},
        )

    return {"message": "Calorie added", "food": food, "calories": calories}

# -------------------- SLEEP --------------------
@app.post("/sleep/add-by-name", tags=["Sleep"])
def add_sleep_by_name(data: SleepByName, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.name.ilike(data.name)).first()
    if not user:
        user = User(name=data.name)
        db.add(user)
        db.commit()
        db.refresh(user)

    sleep = Sleep(
        user_id=user.user_id,
        sleep_hours=data.sleep_hours,
        sleep_quality=data.sleep_quality,
        date=data.entry_date
    )

    db.add(sleep)
    db.commit()

    return {"message": "Sleep entry added successfully"}

# -------------------- WORKOUTS (AUTO CALORIES) --------------------
@app.post("/workouts/add-by-name", tags=["Workouts"])
def add_workout_by_name(
    data: WorkoutByName,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.name.ilike(data.name)).first()
    if not user:
        user = User(name=data.name)
        db.add(user)
        db.commit()
        db.refresh(user)

    workout_key = data.workout.lower()
    calories = WORKOUT_CALORIES.get(workout_key)

    if not calories:
        raise HTTPException(status_code=400, detail="Workout not found")

    db.execute(
        text("""
            INSERT INTO workouts
            (user_id, workout_type, duration, calories_burned, date)
            VALUES (:u, :w, :d, :c, :dt)
        """),
        {
            "u": user.user_id,
            "w": data.workout,
            "d": data.duration,
            "c": calories,
            "dt": data.entry_date,
        }
    )
    db.commit()

    return {
        "message": "Workout added successfully",
        "workout": data.workout,
        "calories_burned": calories
    }

# -------------------- MOODS --------------------
@app.post("/moods/add-by-name", tags=["Moods"])
def add_mood(name: str, mood: str, entry_date: date, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name.ilike(name)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.execute(
        text("""
            INSERT INTO moods (user_id, mood, date)
            VALUES (:u, :m, :d)
        """),
        {"u": user.user_id, "m": mood, "d": entry_date}
    )
    db.commit()

    return {"message": "Mood added successfully"}

# -------------------- RUN --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
