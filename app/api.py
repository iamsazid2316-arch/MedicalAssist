from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.auth import authenticate_user
from app.database import SessionLocal
from app.models import Case, DoctorResponse, Message, Notification, User
from app.security import create_access_token, get_current_user, require_role
from app.services.ai import generate_ai_response
from app.services.triage import triage_case


router = APIRouter()


class CaseCreate(BaseModel):
    symptoms: str = Field(min_length=1, max_length=5000)


class MessageCreate(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class CaseStatusUpdate(BaseModel):
    status: Literal["pending", "reviewing", "approved", "rejected", "emergency"]


class DoctorDecisionCreate(BaseModel):
    decision: Literal["approve", "modify", "reject", "emergency"]
    response: str = Field(min_length=1, max_length=10000)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _case_or_404(db: Session, case_id: int) -> Case:
    case = db.query(Case).filter(Case.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


def _owned_case(db: Session, case_id: int, user_id: int) -> Case:
    case = (
        db.query(Case)
        .filter(Case.id == case_id, Case.cadet_id == user_id)
        .first()
    )
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


def _serialize_case(case: Case) -> dict:
    return {
        "case_id": case.id,
        "cadet_id": case.cadet_id,
        "cadet_name": case.cadet.name if case.cadet else "Unknown",
        "symptoms": case.symptoms,
        "summary": case.symptoms,
        "urgency": case.urgency or "routine",
        "status": case.status,
        "created_at": case.created_at,
    }


def _serialize_message(message: Message) -> dict:
    return {
        "message_id": message.id,
        "case_id": message.case_id,
        "sender": message.sender,
        "message": message.message,
        "timestamp": message.timestamp,
    }


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid name or password",
        )
    return {
        "success": True,
        "message": "Login successful",
        "access_token": create_access_token(user_id=user.id, role=user.role),
        "token_type": "bearer",
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
        raise HTTPException(status_code=403, detail="You can only access your own profile")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user.id, "name": user.name, "role": user.role}


@router.post("/cases")
def create_case(
    case_data: CaseCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    urgency = triage_case(case_data.symptoms)
    case = Case(
        cadet_id=int(current_user["sub"]),
        symptoms=case_data.symptoms.strip(),
        urgency=urgency,
        status="emergency" if urgency == "emergency" else "pending",
    )
    db.add(case)
    db.flush()

    notification_type = "emergency" if urgency == "emergency" else "new_case"
    for doctor in db.query(User).filter(User.role == "doctor").all():
        db.add(
            Notification(
                user_id=doctor.id,
                case_id=case.id,
                type=notification_type,
                message=(
                    f"Emergency case #{case.id} requires immediate review."
                    if urgency == "emergency"
                    else f"New medical case #{case.id} is available for review."
                ),
            )
        )
    db.commit()
    db.refresh(case)
    return {
        "success": True,
        "message": "Case created successfully",
        "case_id": case.id,
        "status": case.status,
        "urgency": case.urgency,
    }


@router.get("/cases")
def get_my_cases(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    cases = (
        db.query(Case)
        .filter(Case.cadet_id == int(current_user["sub"]))
        .order_by(Case.created_at.desc())
        .all()
    )
    return [_serialize_case(case) for case in cases]


@router.get("/cases/{case_id}")
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    return _serialize_case(_owned_case(db, case_id, int(current_user["sub"])))


@router.get("/cases/{case_id}/status")
def get_case_status(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    case = _owned_case(db, case_id, int(current_user["sub"]))
    return {"case_id": case.id, "status": case.status, "urgency": case.urgency}


@router.get("/cases/{case_id}/response")
def get_approved_response(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    case = _owned_case(db, case_id, int(current_user["sub"]))
    if case.status not in {"approved", "emergency"}:
        raise HTTPException(status_code=403, detail="Doctor response is not approved yet")
    response = (
        db.query(DoctorResponse)
        .filter(
            DoctorResponse.case_id == case.id,
            DoctorResponse.decision.in_(["approve", "modify", "emergency"]),
        )
        .order_by(DoctorResponse.timestamp.desc())
        .first()
    )
    if response is None:
        raise HTTPException(status_code=404, detail="Approved doctor response not found")
    return {
        "case_id": case.id,
        "response_id": response.id,
        "decision": response.decision,
        "response": response.response,
        "timestamp": response.timestamp,
    }


@router.post("/cases/{case_id}/messages")
def create_message(
    case_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    case = _case_or_404(db, case_id)
    user_id = int(current_user["sub"])
    role = current_user.get("role")
    if role == "cadet" and case.cadet_id != user_id:
        raise HTTPException(status_code=403, detail="You can only message your own case")
    if role not in {"cadet", "doctor"}:
        raise HTTPException(status_code=403, detail="Invalid user role")
    message = Message(case_id=case.id, sender=role, message=message_data.message.strip())
    db.add(message)
    db.commit()
    db.refresh(message)
    return {"success": True, **_serialize_message(message)}


@router.get("/cases/{case_id}/messages")
def get_case_messages(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    case = _case_or_404(db, case_id)
    role = current_user.get("role")
    if role == "cadet" and case.cadet_id != int(current_user["sub"]):
        raise HTTPException(status_code=403, detail="You can only access your own case")
    if role not in {"cadet", "doctor"}:
        raise HTTPException(status_code=403, detail="Invalid user role")
    messages = (
        db.query(Message)
        .filter(Message.case_id == case.id)
        .order_by(Message.timestamp.asc())
        .all()
    )
    return [_serialize_message(message) for message in messages]


@router.post("/cases/{case_id}/assistant")
def assistant_response(
    case_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("cadet")),
):
    case = _owned_case(db, case_id, int(current_user["sub"]))
    user_message = Message(
        case_id=case.id, sender="cadet", message=message_data.message.strip()
    )
    db.add(user_message)
    db.flush()
    history = (
        db.query(Message)
        .filter(Message.case_id == case.id)
        .order_by(Message.timestamp.asc())
        .all()
    )
    conversation = [
        {
            "role": "assistant" if item.sender == "assistant" else "user",
            "content": item.message,
        }
        for item in history
        if item.sender in {"cadet", "assistant"}
    ]
    reply = generate_ai_response(conversation)
    assistant_message = Message(case_id=case.id, sender="assistant", message=reply)
    combined = f"{case.symptoms} {message_data.message}"
    case.urgency = triage_case(combined)
    if case.urgency == "emergency":
        case.status = "emergency"
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    return {
        "case_id": case.id,
        "message": reply,
        "urgency": case.urgency,
        "status": case.status,
        "message_id": assistant_message.id,
    }


@router.get("/doctor/cases")
def get_doctor_cases(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("doctor")),
):
    cases = (
        db.query(Case)
        .filter(Case.status.in_(["pending", "reviewing", "emergency"]))
        .order_by(Case.created_at.desc())
        .all()
    )
    return [_serialize_case(case) for case in cases]


@router.get("/doctor/cases/{case_id}")
def get_doctor_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("doctor")),
):
    case = _case_or_404(db, case_id)
    result = _serialize_case(case)
    result["messages"] = [_serialize_message(message) for message in case.messages]
    return result


@router.patch("/doctor/cases/{case_id}/status")
def update_case_status(
    case_id: int,
    status_data: CaseStatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("doctor")),
):
    case = _case_or_404(db, case_id)
    case.status = status_data.status
    db.commit()
    return {"success": True, "case_id": case.id, "status": case.status}


@router.post("/doctor/cases/{case_id}/decision")
def create_doctor_decision(
    case_id: int,
    decision_data: DoctorDecisionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("doctor")),
):
    case = _case_or_404(db, case_id)
    resulting_status = {
        "approve": "approved",
        "modify": "approved",
        "reject": "rejected",
        "emergency": "emergency",
    }[decision_data.decision]
    response = DoctorResponse(
        case_id=case.id,
        doctor_id=int(current_user["sub"]),
        response=decision_data.response.strip(),
        decision=decision_data.decision,
    )
    case.status = resulting_status
    if decision_data.decision != "reject":
        db.add(
            Notification(
                user_id=case.cadet_id,
                case_id=case.id,
                type=(
                    "emergency"
                    if decision_data.decision == "emergency"
                    else "doctor_response"
                ),
                message=(
                    f"Emergency response is available for case #{case.id}."
                    if decision_data.decision == "emergency"
                    else f"Doctor response is available for case #{case.id}."
                ),
            )
        )
    db.add(response)
    db.commit()
    db.refresh(response)
    return {
        "success": True,
        "message": "Doctor response stored successfully",
        "response_id": response.id,
        "case_id": case.id,
        "doctor_id": response.doctor_id,
        "decision": response.decision,
        "response": response.response,
        "status": case.status,
        "timestamp": response.timestamp,
    }


@router.get("/notifications")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == int(current_user["sub"]))
        .order_by(Notification.created_at.desc())
        .all()
    )
    return [
        {
            "notification_id": item.id,
            "case_id": item.case_id,
            "type": item.type,
            "message": item.message,
            "is_read": item.is_read,
            "created_at": item.created_at,
        }
        for item in notifications
    ]
