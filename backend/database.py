from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - SQLite file will be created automatically
DATABASE_URL = "sqlite:///./rentaroom.db"

# Create engine
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()

# Dependency - gets a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()