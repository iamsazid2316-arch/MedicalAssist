from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from app.models import User


password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_user(
    db: Session,
    name: str,
    role: str,
    password: str,
):
    user = User(
        name=name,
        role=role,
        password_hash=hash_password(password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def authenticate_user(
    db: Session,
    name: str,
    password: str,
):
    user = db.query(User).filter(User.name == name).first()

    if user is None:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return user