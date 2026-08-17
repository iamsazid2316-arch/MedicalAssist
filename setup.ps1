$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Creating the virtual environment..."
    py -m venv .venv
}

$Python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

Write-Host "Installing MedicalAssist dependencies..."
& $Python -m pip install --upgrade pip
& $Python -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    $Secret = & $Python -c "import secrets; print(secrets.token_urlsafe(48))"
    @(
        "SECRET_KEY=$Secret"
        "MEDICALASSIST_DEMO_ACCOUNTS=true"
        "MEDICALASSIST_API_URL=http://127.0.0.1:8000"
        "MEDICALASSIST_API_TIMEOUT=12"
        "OLLAMA_BASE_URL=http://localhost:11434/v1"
        "OLLAMA_API_KEY=ollama"
        "MEDICALASSIST_AI_MODEL=llama3.2:3b"
        "MEDICALASSIST_AI_TIMEOUT=5"
    ) | Set-Content -Encoding UTF8 ".env"
    Write-Host "Created .env with a secure random secret."
} else {
    Write-Host "Keeping the existing .env file."
}

New-Item -ItemType Directory -Path "data" -Force | Out-Null

Write-Host ""
Write-Host "Setup complete."
Write-Host "Backend: .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload"
Write-Host "Frontend: .\.venv\Scripts\python.exe app\ui_app.py"
Write-Host "Tests:   .\.venv\Scripts\python.exe -m pytest"
