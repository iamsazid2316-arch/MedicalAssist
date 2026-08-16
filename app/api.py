from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import authenticate_user, create_user, get_user_by_name
from app.database import SessionLocal
from app.models import User, Case, Message, DoctorResponse
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
class DoctorDecisionCreate(BaseModel):
    decision: Literal[
        "approve",
        "modify",
        "reject",
        "emergency",
    ]
    response: str = Field(min_length=1, max_length=10000)

class MessageCreate(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


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
@router.get("/cases/{case_id}/status")
def get_case_status(
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
        "status": case.status,
        "urgency": case.urgency,
    }
@router.get("/cases/{case_id}/response")
def get_approved_response(
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

    if case.status not in ["approved", "emergency"]:
        raise HTTPException(
            status_code=403,
            detail="Doctor response is not approved yet",
        )

    doctor_response = (
        db.query(DoctorResponse)
        .filter(
            DoctorResponse.case_id == case.id,
            DoctorResponse.decision.in_(["approve", "modify", "emergency"]),
        )
        .order_by(DoctorResponse.timestamp.desc())
        .first()
    )

    if doctor_response is None:
        raise HTTPException(
            status_code=404,
            detail="Approved doctor response not found",
        )

    return {
        "case_id": case.id,
        "response_id": doctor_response.id,
        "decision": doctor_response.decision,
        "response": doctor_response.response,
        "timestamp": doctor_response.timestamp,
    }
@router.get("/doctor/cases")
def get_doctor_cases(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("doctor")),
):
    cases = (
        db.query(Case)
        .filter(
            Case.status.in_(
                ["pending", "reviewing", "emergency"]
            )
        )
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
        "messages": [
            {
                "message_id": message.id,
                "sender": message.sender,
                "message": message.message,
                "timestamp": message.timestamp,
            }
            for message in case.messages
        ],
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
@router.post("/cases/{case_id}/messages")
def create_message(
    case_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
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

    user_id = int(current_user["sub"])
    role = current_user.get("role")

    if role == "cadet" and case.cadet_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only send messages in your own case",
        )

    if role not in {"cadet", "doctor"}:
        raise HTTPException(
            status_code=403,
            detail="Invalid user role",
        )

    message = Message(
        case_id=case_id,
        sender=role,
        message=message_data.message,
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return {
        "success": True,
        "message_id": message.id,
        "case_id": message.case_id,
        "sender": message.sender,
        "message": message.message,
        "timestamp": message.timestamp,
    }


@router.get("/cases/{case_id}/messages")
def get_case_messages(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
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

    user_id = int(current_user["sub"])
    role = current_user.get("role")

    if role == "cadet" and case.cadet_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access messages from your own case",
        )

    if role not in {"cadet", "doctor"}:
        raise HTTPException(
            status_code=403,
            detail="Invalid user role",
        )

    messages = (
        db.query(Message)
        .filter(Message.case_id == case_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    return [
        {
            "message_id": message.id,
            "case_id": message.case_id,
            "sender": message.sender,
            "message": message.message,
            "timestamp": message.timestamp,
        }
        for message in messages
    ]
@router.get("/cases/{case_id}/messages")
def get_case_messages(
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

    messages = (
        db.query(Message)
        .filter(Message.case_id == case_id)
        .order_by(Message.timestamp.asc())
        .all()
    )

    return [
        {
            "message_id": message.id,
            "case_id": message.case_id,
            "sender": message.sender,
            "message": message.message,
            "timestamp": message.timestamp,
        }
        for message in messages
    ]
@router.post("/doctor/cases/{case_id}/decision")
def create_doctor_decision(
    case_id: int,
    decision_data: DoctorDecisionCreate,
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

    decision_status = {
        "approve": "approved",
        "modify": "approved",
        "reject": "rejected",
        "emergency": "emergency",
    }

    resulting_status = decision_status[decision_data.decision]

    doctor_response = DoctorResponse(
        case_id=case.id,
        doctor_id=int(current_user["sub"]),
        response=decision_data.response,
        decision=decision_data.decision,
    )

    case.status = resulting_status

    db.add(doctor_response)
    db.commit()
    db.refresh(doctor_response)
    db.refresh(case)

    return {
        "success": True,
        "message": "Doctor response stored successfully",
        "response_id": doctor_response.id,
        "case_id": doctor_response.case_id,
        "doctor_id": doctor_response.doctor_id,
        "decision": doctor_response.decision,
        "response": doctor_response.response,
        "status": case.status,
        "timestamp": doctor_response.timestamp,
    }