# the business logic for the API calls
from uuid import uuid4
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import TodoDB
from schemas import Todo, TodoCreate


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


def read_all_tasks(db: Session) -> list[Todo]:
    tasks = db.query(TodoDB).all()
    return [Todo.model_validate(task) for task in tasks]


def get_task(task_id: str, db: Session) -> Todo:
    task = db.get(TodoDB, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return Todo.model_validate(task)


def modify_task(task_id: str, updated_todo: TodoCreate, db: Session) -> Todo:
    task = db.get(TodoDB, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_todo.title
    task.description = updated_todo.description
    task.completed = updated_todo.completed

    db.commit()
    db.refresh(task)
    return Todo.model_validate(task)


def remove_task(task_id: str, db: Session) -> Todo:
    task = db.get(TodoDB, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return Todo.model_validate(task)
