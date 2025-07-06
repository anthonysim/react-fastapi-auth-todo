from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.databases.sqlite_database import get_session
from src.services.operations import (
    create_task,
    read_all_tasks,
    get_task,
    remove_task,
    modify_task
)
from src.auth.dependencies import get_current_user
from src.models.sqlite_models import User
from src.schemas.schemas import TodoCreate, Todo

router = APIRouter()


@router.post("/task", response_model=Todo)
async def add_task(
    todo: TodoCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await create_task(todo, db, current_user.id)


@router.get("/tasks", response_model=list[Todo])
async def read_tasks(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await read_all_tasks(db, user_id=current_user.id)


@router.get("/task/{task_id}", response_model=Todo)
async def read_task(
    task_id: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await get_task(task_id, db, current_user.id)


@router.patch("/task/{task_id}", response_model=Todo)
async def update_task(
    task_id: str,
    updated_todo: TodoCreate,  # ⚠️ all fields required
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await modify_task(task_id, updated_todo, db, current_user.id)


@router.delete("/task/{task_id}", response_model=Todo)
async def delete_task(
    task_id: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return await remove_task(task_id, db, current_user.id)
