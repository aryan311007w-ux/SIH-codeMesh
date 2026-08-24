@echo off
cd /d "%~dp0backend"

if not exist ".env" (
    echo No .env found - copying .env.example. Edit .env and add your ETHERSCAN_API_KEY, then run this again.
    copy .env.example .env
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo Starting server at http://127.0.0.1:8000 ...
uvicorn main:app --reload --port 8000
