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
    user_id: UUID

    model_config = {
        "from_attributes": True
    }

# user schemas
class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: UUID
    email: str

    model_config = {
        "from_attributes": True
    }
