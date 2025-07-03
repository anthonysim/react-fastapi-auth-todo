# database.py is the setup for db.
from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Engine (singleton via LRU cache)
@lru_cache
def get_engine():
    return create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Base class for models
class Base(DeclarativeBase):
    pass

# Create all tables — call this during startup
def init_db():
    Base.metadata.create_all(bind=get_engine())

# Session generator for dependency injection
def get_session():
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine(),
    )
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
