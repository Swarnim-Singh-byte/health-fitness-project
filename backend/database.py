
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# CHANGE these values only if your credentials are different
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/health_fitness_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# database.py

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
