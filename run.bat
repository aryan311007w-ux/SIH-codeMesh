@echo off
setlocal
cd /d "%~dp0backend"

echo ============================================================
echo   CryptoGuard AI -- Blockchain Investigation & VASP Attribution
echo   SIH 2026 Problem Statement SIH26182
echo ============================================================

if not exist ".env" (
    echo [INFO] No .env found. Generating default .env from .env.example ...
    copy .env.example .env >nul
    echo [INFO] Running in high-fidelity Deterministic DEMO MODE.
    echo [INFO] (Optional: To enable live mainnet traces, add your ETHERSCAN_API_KEY to backend\.env)
)

echo [INFO] Starting CryptoGuard AI on http://127.0.0.1:8000 ...
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
