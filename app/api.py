from typing import Literal
from app.models import User
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.security import (
    create_access_token,
    get_current_user,
    require_role,
)
from app.security import create_access_token, require_role
from sqlalchemy.orm import Session
from app.auth import authenticate_user, get_user_by_name, create_user
from app.database import SessionLocal
from typing import Literal
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    role: Literal["cadet", "doctor"]
    password: str = Field(min_length=6, max_length=100)


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(
    db,
    form_data.username,
    form_data.password,
)

    if user is None:
        return {
            "success": False,
            "message": "Invalid name or password",
        }

    access_token = create_access_token(
    user_id=user.id,
    role=user.role,
)

    return {
        "success": True,
        "message": "Login successful",
        "access_token": access_token,
        "user_id": user.id,
        "name": user.name,
        "role": user.role,
    }
@router.post("/register")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):

    existing_user = get_user_by_name(
    db,
    user_data.name,
)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="User already exists",
        )

    user = create_user(
        db=db,
        name=user_data.name,
        role=user_data.role,
        password=user_data.password,
    )

    return {
        "success": True,
        "message": "User created successfully",
        "user_id": user.id,
        "name": user.name,
        "role": user.role,
    }
@router.get("/users/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if user_id != int(current_user["sub"]):
        raise HTTPException(
            status_code=403,
            detail="You can only access your own profile",
        )
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "user_id": user.id,
        "name": user.name,
        "role": user.role,
    }
