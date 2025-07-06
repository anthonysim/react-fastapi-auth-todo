# schemas.py is for the "shape" of the request and response
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

# todo schemas
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
    user_id: int

    model_config = {
        "from_attributes": True  # ✅ replaces orm_mode = True in Pydantic v2
    }

# user schemas
class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str

    model_config = {
        "from_attributes": True
    }