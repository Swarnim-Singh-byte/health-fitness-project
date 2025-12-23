from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    goal = Column(String(100))


class Calorie(Base):
    __tablename__ = "calories"

    calorie_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    food_name = Column(String(100))
    calories = Column(Integer)
    date = Column(Date)


class Sleep(Base):
    __tablename__ = "sleep"

    sleep_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    sleep_hours = Column(Float)
    sleep_quality = Column(String(20))
    date = Column(Date)
