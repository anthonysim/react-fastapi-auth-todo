from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from src.schemas import TodoCreate, Todo
from src.operations import create_task, read_all_tasks
from src.database import get_session, init_db
from sqlalchemy.orm import Session

# creates table upon startup
init_db()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tasks", response_model=list[Todo])
def read_tasks(db: Session = Depends(get_session)):
    """
    Retrieve all tasks from the database.

    - **Returns**: A list of Todo items.
    """
    return read_all_tasks(db)


@app.post("/task", response_model=Todo)
def add_task(todo: TodoCreate, db: Session = Depends(get_session)):
    """
    Add a new task to the database.

    - **todo**: The task details in the request body.
    - **Returns**: The created Todo item.
    """
    return create_task(todo, db)
