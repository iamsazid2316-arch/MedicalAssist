from fastapi import FastAPI

from app import models
from app.api import router
from app.database import init_db


app = FastAPI(
    title="Medical Assistance System",
    description="AI-assisted medical triage and doctor communication system",
    version="0.1.0",
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Medical Assistance System API is running"
    }