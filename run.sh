#!/bin/bash
# Quick start script - run from the project root.
set -e

cd "$(dirname "$0")/backend"

if [ ! -f ".env" ]; then
    echo "No .env found - copying .env.example. Edit .env and add your ETHERSCAN_API_KEY before continuing."
    cp .env.example .env
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt --quiet

echo "Starting server at http://127.0.0.1:8000 ..."
uvicorn main:app --reload --port 8000
