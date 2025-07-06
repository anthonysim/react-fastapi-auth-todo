from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_session
from src.operations import (
    create_task,
    read_all_tasks,
    get_task,
    remove_task,
    modify_task
    )
from src.dependencies import get_current_user
from src.models import User
from src.schemas import TodoCreate, Todo
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/task", response_model=Todo)
async def add_task(
    todo: TodoCreate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Add a new task for the current user.
    """
    return await create_task(todo, db, current_user.id)


@router.get("/tasks", response_model=list[Todo])
async def read_tasks(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Get all tasks that belong to the current user.
    - **current_user**: The authenticated user.
    - **Returns**: A list of the user's tasks.
    """
    return read_all_tasks(db, user_id=current_user.id)


@router.get("/task/{task_id}", response_model=Todo)
async def read_task(
    task_id: str,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific task by ID for the current user.
    - **task_id**: The ID of the task to retrieve.
    - **Returns**: The Todo item if found and owned by the user.
    - **Raises**: 404 if not found or not owned by the user.
    """
    return get_task(task_id, db, current_user.id)


@router.patch("/task/{task_id}", response_model=Todo)
async def update_task(
    task_id: str,
    updated_todo: TodoCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Update a specific task for the current user.
    - **task_id**: The ID of the task to update.
    - **updated_todo**: New task data.
    - **Returns**: The updated Todo item.
    - **Raises**: 404 if the task doesn't exist or isn't owned by the user.
    """
    return modify_task(task_id, updated_todo, db, current_user.id)


@router.delete("/task/{task_id}", response_model=Todo)
async def delete_task(
    task_id: str,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific task for the current user.
    - **task_id**: The ID of the task to delete.
    - **Returns**: The deleted Todo item.
    - **Raises**: 404 if the task doesn't exist or isn't owned by the user.
    """
    return remove_task(task_id, db, current_user.id)
