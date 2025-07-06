# models.py is for the "shape" of the db table.
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String
    )
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from uuid import uuid4
from src.databases.sqlite_database import Base

# db table for todos
class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="todos")

# db table for users (register, login, logout)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    todos = relationship("TodoDB", back_populates="user", cascade="all, delete")