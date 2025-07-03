from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session

from src.auth import (
    hash_password,
    create_access_token,
    create_refresh_token,
    verify_password
    )
from src.database import get_session
from src.dependencies import get_current_user
from src.models import User
from src.schemas import UserCreate, UserOut


router = APIRouter()


@router.post("/register")
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


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserOut.model_validate(user).model_dump()
    })
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=7 * 24 * 60 * 60
    )
    return response


@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# @router.post("/refresh")
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