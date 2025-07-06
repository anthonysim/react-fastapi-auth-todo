# the business logic for the API calls
from uuid import uuid4
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.models import TodoDB
from src.schemas import Todo, TodoCreate
from sqlalchemy.ext.asyncio import AsyncSession


async def create_task(
    todo: TodoCreate,
    db: AsyncSession,
    user_id: str
) -> Todo:
    db_task = TodoDB(
        id=str(uuid4()),
        created_at=datetime.now(timezone.utc),
        user_id=user_id,
        **todo.model_dump()
    )
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return Todo.model_validate(db_task)


async def read_all_tasks(
        db: Session,
        user_id: str
) -> list[Todo]:
    tasks = db.query(TodoDB).filter(TodoDB.user_id == user_id).all()
    return [Todo.model_validate(task) for task in tasks]


def get_task(
        task_id: str,
        db: Session,
        user_id: str
) -> Todo:
    task = db.get(TodoDB, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return Todo.model_validate(task)


async def modify_task(
    task_id: str,
    updated_todo: TodoCreate,
    db: Session,
    user_id: str
) -> Todo:
    task = db.get(TodoDB, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_todo.title
    task.description = updated_todo.description
    task.completed = updated_todo.completed

    db.commit()
    db.refresh(task)
    return Todo.model_validate(task)


async def remove_task(
        task_id: str,
        db: Session,
        user_id: str
) -> Todo:
    task = db.get(TodoDB, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return Todo.model_validate(task)
