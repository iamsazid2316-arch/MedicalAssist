import os

from sqlalchemy.orm import Session

from app.auth import create_user, get_user_by_name


DEMO_ACCOUNTS = (
    ("TestCadet", "cadet", "test123"),
    ("TestDoctor", "doctor", "doctor123"),
)


def seed_demo_accounts(db: Session) -> None:
    enabled = os.getenv("MEDICALASSIST_DEMO_ACCOUNTS", "true").lower()
    if enabled not in {"1", "true", "yes", "on"}:
        return
    for name, role, password in DEMO_ACCOUNTS:
        if get_user_by_name(db, name) is None:
            create_user(db, name=name, role=role, password=password)
