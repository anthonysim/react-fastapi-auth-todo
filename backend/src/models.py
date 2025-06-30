
from sqlalchemy import Column, String, Boolean, DateTime
from datetime import datetime, timezone
from uuid import uuid4
from src.database import Base  # ✅ import the correct Base

class TodoDB(Base):
    __tablename__ = "todos"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
