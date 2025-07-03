from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas import TodoCreate, Todo, UserCreate, UserOut
from src.models import User
from src.operations import (
    create_task,
    read_all_tasks,
    get_task,
    remove_task,
    modify_task
    )
from src.auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
    )
from dependencies import get_current_user
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

# todo api routes
@app.post("/task", response_model=Todo)
def add_task(todo: TodoCreate, db: Session = Depends(get_session)):
    """
    Add a new task to the database.

    - **todo**: The task details in the request body.
    - **Returns**: The created Todo item.
    """
    return create_task(todo, db)


@app.get("/tasks", response_model=list[Todo])
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


@app.get("/task/{task_id}", response_model=Todo)
def read_task(task_id: str, db: Session = Depends(get_session)):
    """
    Retrieve a task by its ID.

    - **task_id**: The ID of the task to retrieve.
    - **Returns**: The Todo item if found.
    """
    return get_task(task_id, db)


@app.patch("/task/{task_id}", response_model=Todo)
def update_task(task_id: str, updated_todo: TodoCreate, db: Session = Depends(get_session)):
    """
    Update an existing task by its ID.

    - **task_id**: The ID of the task to update.
    - **updated_todo**: The new task data in the request body.
    - **Returns**: The updated Todo item.
    """
    return modify_task(task_id, updated_todo, db)


@app.delete("/task/{task_id}", response_model=Todo)
def delete_task(task_id: str, db: Session = Depends(get_session)):
    """
    Delete a task by its ID.

    - **task_id**: The ID of the task to delete.
    - **Returns**: The deleted Todo item.
    """
    return remove_task(task_id, db)

# user registration, login, logout api routes
@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_session)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": str(new_user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserOut.model_validate(new_user)
    }


@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user)  # ✅ Cleanly returns user info
    }


# @app.post("/login")
# def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
#     user = db.query(User).filter(User.email == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     access_token = create_access_token({"sub": str(user.id)})
#     refresh_token = create_refresh_token({"sub": str(user.id)})

#     response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
#     response.set_cookie(
#         key="refresh_token",
#         value=refresh_token,
#         httponly=True,
#         secure=True,
#         samesite="strict",
#         max_age=7 * 24 * 60 * 60
#     )
#     return response


@app.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# @app.post("/refresh")
# def refresh_token(request: Request):
#     refresh_token = request.cookies.get("refresh_token")
#     if not refresh_token:
#         raise HTTPException(status_code=403, detail="Refresh token missing")

#     try:
#         payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
#         user_id = payload.get("sub")
#         if user_id is None:
#             raise HTTPException(status_code=403, detail="Invalid token")

#         new_access_token = create_access_token({"sub": user_id})
#         return {"access_token": new_access_token}
#     except JWTError:
#         raise HTTPException(status_code=403, detail="Invalid or expired refresh token")


