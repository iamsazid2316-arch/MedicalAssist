from fastapi import FastAPI

from app import models
from app.api import router
from app.database import init_db
from app.database import SessionLocal
from app.demo import seed_demo_accounts


app = FastAPI(
    title="Medical Assistance System",
    description="AI-assisted medical triage and doctor communication system",
    version="0.1.0",
)


@app.on_event("startup")
def startup():
    init_db()
    db = SessionLocal()
    try:
        seed_demo_accounts(db)
    finally:
        db.close()


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Medical Assistance System API is running"
    }
