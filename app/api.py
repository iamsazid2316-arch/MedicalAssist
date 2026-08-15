from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.security import require_role
from app.security import create_access_token, require_role
from sqlalchemy.orm import Session
from app.auth import authenticate_user
from app.database import SessionLocal


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

