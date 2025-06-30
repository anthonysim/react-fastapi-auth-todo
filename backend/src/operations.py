# the business logic for the API calls
from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models import TodoDB
from src.schemas import Todo, TodoCreate


def read_all_tasks(db: Session) -> list[Todo]:
    tasks = db.query(TodoDB).all()
    return [Todo.model_validate(task) for task in tasks]

def create_task(todo: TodoCreate, db: Session) -> Todo:
    db_task = TodoDB(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        **todo.model_dump()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return Todo.model_validate(db_task)
