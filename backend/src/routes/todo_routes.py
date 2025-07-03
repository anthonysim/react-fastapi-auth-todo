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

router = APIRouter()


@router.post("/task", response_model=Todo)
def add_task(
    todo: TodoCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Add a new task to the database.
    - **todo**: The task details in the request body.
    - **current_user**: The current login user.
    - **Returns**: The created Todo item.
    """
    return create_task(todo, db, current_user)


@router.get("/tasks", response_model=list[Todo])
def read_tasks(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Read all user's tasks.
    - **current_user**: The current login user.
    - **Returns**: The user's tasks per user's id.
    """
    return read_all_tasks(db, user_id=current_user.id)


@router.get("/task/{task_id}", response_model=Todo)
def read_task(task_id: str, db: Session = Depends(get_session)):
    return get_task(task_id, db)


@router.patch("/task/{task_id}", response_model=Todo)
def update_task(task_id: str, updated_todo: TodoCreate, db: Session = Depends(get_session)):
    return modify_task(task_id, updated_todo, db)


@router.delete("/task/{task_id}", response_model=Todo)
def delete_task(task_id: str, db: Session = Depends(get_session)):
    return remove_task(task_id, db)