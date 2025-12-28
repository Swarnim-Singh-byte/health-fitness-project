from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base


# -------------------- USERS --------------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

    age = Column(Integer, default=0)
    height = Column(Float, default=0)
    weight = Column(Float, default=0)
    goal = Column(String, default="General")

    # Relationships
    calories = relationship("Calorie", back_populates="user", cascade="all, delete")
    sleep = relationship("Sleep", back_populates="user", cascade="all, delete")
    workouts = relationship("Workout", back_populates="user", cascade="all, delete")
    moods = relationship("Mood", back_populates="user", cascade="all, delete")

# -------------------- CALORIES --------------------
class Calorie(Base):
    __tablename__ = "calories"

    calorie_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    food_name = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="calories")

# -------------------- SLEEP --------------------
class Sleep(Base):
    __tablename__ = "sleep"

    sleep_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    sleep_hours = Column(Float, nullable=False)
    sleep_quality = Column(String, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="sleep")

# -------------------- WORKOUTS --------------------
class Workout(Base):
    __tablename__ = "workouts"

    workout_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    workout_type = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)          # minutes
    calories_burned = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="workouts")

# -------------------- MOODS --------------------
class Mood(Base):
    __tablename__ = "moods"

    mood_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))

    mood_level = Column(String, nullable=False)   # 👈 FIX
    note = Column(String, nullable=True)
    date = Column(Date, nullable=False)

    user = relationship("User", back_populates="moods")
