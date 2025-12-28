from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import date

from backend.database import get_db
from backend.models import User, Sleep, Mood
from backend.schemas import SleepByName, WorkoutByName, CalorieByName
from sqlalchemy import text


# -------------------- APP SETUP --------------------
app = FastAPI(title="Health & Fitness Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # restrict later in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- MASTER DATA --------------------
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

MOOD_MAP = {
    "Sad": 1,
    "Tired": 2,
    "Neutral": 3,
    "Happy": 4,
    "Energetic": 5
}


# -------------------- HELPERS --------------------
def get_or_create_user(db: Session, name: str) -> User:
    user = db.query(User).filter(User.name.ilike(name)).first()
    if not user:
        user = User(name=name, age=0, height=0, weight=0, goal="General")
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

# -------------------- ROOT --------------------
@app.get("/")
def root():
    return {"status": "API running successfully"}

# -------------------- CALORIES --------------------
@app.post("/calories/add-by-name", tags=["Calories"])
def add_calorie_by_name(
    data: CalorieByName,
    db: Session = Depends(get_db)
):
    food_key = data.food.lower()

    if food_key not in FOOD_CALORIES:
        raise HTTPException(status_code=400, detail="Food not found")

    calories = FOOD_CALORIES[food_key]
    user = get_or_create_user(db, data.name)

    db.execute(
    text("""
        INSERT INTO calories (user_id, food_name, calories, date)
        VALUES (:u, :f, :c, :d)
    """),
    {"u": user.user_id, "f": data.food, "c": calories, "d": data.entry_date}
)

    db.commit()

    return {
        "message": "Calorie added successfully",
        "food": data.food,
        "calories": calories
    }

# -------------------- SLEEP --------------------
@app.post("/sleep/add-by-name", tags=["Sleep"])
def add_sleep_by_name(
    data: SleepByName,
    db: Session = Depends(get_db)
):
    user = get_or_create_user(db, data.name)

    sleep = Sleep(
        user_id=user.user_id,
        sleep_hours=data.sleep_hours,
        sleep_quality=data.sleep_quality,
        date=data.entry_date
    )

    db.add(sleep)
    db.commit()

    return {"message": "Sleep entry added successfully"}

# -------------------- WORKOUTS --------------------
from backend.models import Workout

@app.post("/workouts/add-by-name", tags=["Workouts"])
def add_workout_by_name(
    data: WorkoutByName,
    db: Session = Depends(get_db)
):
    # 1. Get or create user
    user = db.query(User).filter(User.name.ilike(data.name)).first()
    if not user:
        user = User(
            name=data.name,
            age=0,
            height=0,
            weight=0,
            goal="General"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 2. Get calories for workout
    workout_key = data.workout.lower()
    calories = WORKOUT_CALORIES.get(workout_key)

    if calories is None:
        raise HTTPException(status_code=400, detail="Workout not found")

    # 3. Create workout entry (ORM)
    workout_entry = Workout(
        user_id=user.user_id,
        workout_type=data.workout,
        duration=data.duration,
        calories_burned=calories,
        date=data.entry_date
    )

    # 4. Save
    db.add(workout_entry)
    db.commit()

    return {
        "message": "Workout added successfully",
        "workout": data.workout,
        "calories_burned": calories
    }

# -------------------- MOODS --------------------
@app.post("/moods/add-by-name", tags=["Moods"])
def add_mood(
    name: str,
    mood: str,
    entry_date: date,
    db: Session = Depends(get_db)
):
    # get or create user
    user = db.query(User).filter(User.name.ilike(name)).first()
    if not user:
        user = User(name=name, age=0, height=0, weight=0, goal="General")
        db.add(user)
        db.commit()
        db.refresh(user)

    # 🔥 convert mood string → integer
    mood_level = MOOD_MAP.get(mood)
    if mood_level is None:
        raise HTTPException(status_code=400, detail="Invalid mood")

    mood_entry = Mood(
        user_id=user.user_id,
        mood_level=mood_level,  # ✅ INTEGER now
        date=entry_date
    )

    db.add(mood_entry)
    db.commit()

    return {"message": "Mood added successfully"}


# -------------------- RUN --------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
