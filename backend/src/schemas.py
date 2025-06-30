from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class Todo(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    completed: bool
    created_at: datetime

    model_config = {
        "from_attributes": True  # ✅ replaces orm_mode = True in Pydantic v2
    }
