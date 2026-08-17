# MedicalAssist

Medical assistance desktop application with a PySide6 frontend and FastAPI backend.

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
