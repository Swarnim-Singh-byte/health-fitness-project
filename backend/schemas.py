from pydantic import BaseModel, Field
from datetime import date

# -------------------- BASE RESPONSES --------------------
class MessageResponse(BaseModel):
    message: str

# -------------------- CALORIES --------------------
class CalorieByName(BaseModel):
    name: str = Field(..., min_length=1)
    food: str = Field(..., min_length=1)
    entry_date: date

# -------------------- SLEEP --------------------
class SleepByName(BaseModel):
    name: str = Field(..., min_length=1)
    sleep_hours: float = Field(..., gt=0, lt=24)
    sleep_quality: str = Field(..., min_length=3)
    entry_date: date

# -------------------- WORKOUTS --------------------
class WorkoutByName(BaseModel):
    name: str = Field(..., min_length=1)
    workout: str = Field(..., min_length=1)
    duration: int = Field(..., gt=0)
    entry_date: date
