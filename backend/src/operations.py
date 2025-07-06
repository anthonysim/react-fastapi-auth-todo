from uuid import uuid4
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import TodoDB
from src.schemas import Todo, TodoCreate


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
    return Todo.model_validate(db_task, from_attributes=True)


async def read_all_tasks(
    db: AsyncSession,
    user_id: str
) -> list[Todo]:
    stmt = select(TodoDB).where(TodoDB.user_id == user_id)
    result = await db.execute(stmt)
    tasks = result.scalars().all()
    return [Todo.model_validate(task, from_attributes=True) for task in tasks]


async def get_task(
    task_id: str,
    db: AsyncSession,
    user_id: str
) -> Todo:
    task = await db.get(TodoDB, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")
    return Todo.model_validate(task, from_attributes=True)


async def modify_task(
    task_id: str,
    updated_todo: TodoCreate,
    db: AsyncSession,
    user_id: str
) -> Todo:
    task = await db.get(TodoDB, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_todo.title
    task.description = updated_todo.description
    task.completed = updated_todo.completed

    await db.commit()
    await db.refresh(task)
    return Todo.model_validate(task, from_attributes=True)


async def remove_task(
    task_id: str,
    db: AsyncSession,
    user_id: str
) -> Todo:
    task = await db.get(TodoDB, task_id)
    if not task or task.user_id != user_id:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(task)
    await db.commit()
    return Todo.model_validate(task, from_attributes=True)
