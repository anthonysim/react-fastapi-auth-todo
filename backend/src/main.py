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
    return read_all_tasks(db)

@app.post("/task", response_model=Todo)
def add_task(todo: TodoCreate, db: Session = Depends(get_session)):
    return create_task(todo, db)

# erase this later
@app.get("/api/hello")
def say_hello():
    return {"message": "Hello from FastAPI"}
