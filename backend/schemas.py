from pydantic import BaseModel
from datetime import date

class CalorieCreate(BaseModel):
    name: str
    food: str
    calories: int
    entry_date: date


class SleepCreate(BaseModel):
    name: str
    sleep_hours: float
    sleep_quality: str
    entry_date: date

class SleepByName(BaseModel):
    name: str
    sleep_hours: float
    sleep_quality: str
    entry_date: date

class WorkoutByName(BaseModel):
    name: str
    workout: str
    duration: int
    entry_date: date
    