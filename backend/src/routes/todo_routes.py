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
from src.schemas import TodoCreate, Todo

router = APIRouter()


@router.post("/task", response_model=Todo)
def add_task(todo: TodoCreate, db: Session = Depends(get_session)):
    """
    Add a new task to the database.

    - **todo**: The task details in the request body.
    - **Returns**: The created Todo item.
    """
    return create_task(todo, db)


@router.get("/tasks", response_model=list[Todo])
def read_tasks(db: Session = Depends(get_session)):
    """
    Retrieve all tasks from the database.

    - **Returns**: A list of Todo items.
    """
    return read_all_tasks(db)

# @app.get("/tasks", response_model=list[Todo])
# def read_tasks(
#     db: Session = Depends(get_session),
#     current_user: User = Depends(get_current_user)
# ):
#     return read_all_tasks(db, user_id=current_user.id)

@router.get("/task/{task_id}", response_model=Todo)
def read_task(task_id: str, db: Session = Depends(get_session)):
    """
    Retrieve a task by its ID.

    - **task_id**: The ID of the task to retrieve.
    - **Returns**: The Todo item if found.
    """
    return get_task(task_id, db)


@router.patch("/task/{task_id}", response_model=Todo)
def update_task(task_id: str, updated_todo: TodoCreate, db: Session = Depends(get_session)):
    """
    Update an existing task by its ID.

    - **task_id**: The ID of the task to update.
    - **updated_todo**: The new task data in the request body.
    - **Returns**: The updated Todo item.
    """
    return modify_task(task_id, updated_todo, db)


@router.delete("/task/{task_id}", response_model=Todo)
def delete_task(task_id: str, db: Session = Depends(get_session)):
    """
    Delete a task by its ID.

    - **task_id**: The ID of the task to delete.
    - **Returns**: The deleted Todo item.
    """
    return remove_task(task_id, db)