import os

os.environ.setdefault(
    "SECRET_KEY",
    "automated-test-secret-that-is-longer-than-thirty-two-bytes",
)
os.environ["MEDICALASSIST_DEMO_ACCOUNTS"] = "false"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api import get_db
from app.auth import create_user
from app.database import Base
from app.main import app


@pytest.fixture()
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    test_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = test_session()
    create_user(db, name="TestCadet", role="cadet", password="test123")
    create_user(db, name="TestDoctor", role="doctor", password="doctor123")
    db.close()

    def override_get_db():
        session = test_session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    test_client.close()
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture()
def cadet_token(client):
    response = client.post(
        "/login", data={"username": "TestCadet", "password": "test123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture()
def doctor_token(client):
    response = client.post(
        "/login", data={"username": "TestDoctor", "password": "doctor123"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth_header(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
