# MedicalAssist

Medical assistance desktop application with a PySide6 frontend and FastAPI backend.

## First-time Windows setup

From PowerShell in the project folder, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

The setup script creates `.venv`, installs the packages from `requirements.txt`,
creates a private `.env` with a random signing secret when needed, and prepares
the local `data` directory. It keeps an existing `.env` unchanged.

## Run the integrated application

Open two PowerShell windows in the project folder.

Backend:

```powershell
python -m uvicorn app.main:app --reload
```

Frontend:

```powershell
python app\ui_app.py
```

Demo accounts:

- Cadet: `TestCadet` / `test123`
- Doctor: `TestDoctor` / `doctor123`

The frontend sends the entered username and password to the real `POST /login`
endpoint, stores the returned bearer token for later API calls, and opens the
dashboard that matches the authenticated account role.

## Run automated tests

```powershell
python -m pytest
```

The tests use an isolated in-memory database and do not change the application's
real SQLite database.
