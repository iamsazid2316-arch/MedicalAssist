import os


API_BASE_URL = os.getenv("MEDICALASSIST_API_URL", "http://127.0.0.1:8000").rstrip("/")
API_TIMEOUT_SECONDS = float(os.getenv("MEDICALASSIST_API_TIMEOUT", "12"))
