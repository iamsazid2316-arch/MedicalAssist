from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import authenticate_user, create_user, get_user_by_name
from app.database import SessionLocal
from app.models import User, Case
from app.security import create_access_token, get_current_user, require_role


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    role: Literal["cadet", "doctor"]
    password: str = Field(min_length=6, max_length=100)
class CaseCreate(BaseModel):
    symptoms: str = Field(min_length=1, max_length=5000)
class CaseStatusUpdate(BaseModel):
    status: Literal[
        "pending",
        "reviewing",
        "approved",
        "rejected",
        "emergency",
    ]


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
@router.post("/cases")
def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    case = Case(
        cadet_id=int(current_user["sub"]),
        symptoms=case_data.symptoms,
        status="pending",
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return {
        "success": True,
        "message": "Case created successfully",
        "case_id": case.id,
        "status": case.status,
    }
@router.get("/cases")
def get_my_cases(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    cadet_id = int(current_user["sub"])

    cases = (
        db.query(Case)
        .filter(Case.cadet_id == cadet_id)
        .order_by(Case.created_at.desc())
        .all()
    )

    return [
        {
            "case_id": case.id,
            "symptoms": case.symptoms,
            "urgency": case.urgency,
            "status": case.status,
            "created_at": case.created_at,
        }
        for case in cases
    ]
@router.get("/cases/{case_id}")
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    case = (
        db.query(Case)
        .filter(
            Case.id == case_id,
            Case.cadet_id == int(current_user["sub"]),
        )
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )

    return {
        "case_id": case.id,
        "symptoms": case.symptoms,
        "urgency": case.urgency,
        "status": case.status,
        "created_at": case.created_at,
    }
@router.get("/doctor/cases")
def get_doctor_cases(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("doctor")),
):
    cases = (
        db.query(Case)
        .order_by(Case.created_at.desc())
        .all()
    )

    return [
        {
            "case_id": case.id,
            "cadet_id": case.cadet_id,
            "symptoms": case.symptoms,
            "urgency": case.urgency,
            "status": case.status,
            "created_at": case.created_at,
        }
        for case in cases
    ]
@router.get("/doctor/cases/{case_id}")
def get_doctor_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("doctor")),
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )

    return {
        "case_id": case.id,
        "cadet_id": case.cadet_id,
        "symptoms": case.symptoms,
        "urgency": case.urgency,
        "status": case.status,
        "created_at": case.created_at,
    }
@router.patch("/doctor/cases/{case_id}/status")
def update_case_status(
    case_id: int,
    status_data: CaseStatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("doctor")),
):
    case = (
        db.query(Case)
        .filter(Case.id == case_id)
        .first()
    )

    if case is None:
        raise HTTPException(
            status_code=404,
            detail="Case not found",
        )

    case.status = status_data.status

    db.commit()
    db.refresh(case)

    return {
        "success": True,
        "message": "Case status updated",
        "case_id": case.id,
        "status": case.status,
    }