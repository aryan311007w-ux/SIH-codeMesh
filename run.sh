#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/backend"

echo "============================================================"
echo "  CryptoGuard AI -- Blockchain Investigation & VASP Attribution"
echo "  SIH 2026 Problem Statement SIH26182"
echo "============================================================"

if [ ! -f ".env" ]; then
    echo "[INFO] No .env found. Generating default .env from .env.example ..."
    cp .env.example .env
    echo "[INFO] Running in high-fidelity Deterministic DEMO MODE."
fi

echo "[INFO] Starting CryptoGuard AI on http://127.0.0.1:8000 ..."
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
