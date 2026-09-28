# CryptoGuard AI — Project Setup Guide

**Product:** CryptoGuard AI  
**Tagline:** AI-Powered Blockchain Investigation & VASP Attribution Platform  
**Hackathon:** Smart India Hackathon (SIH) 2026 — Problem Statement SIH26182  
**Evaluation Ready:** 100% Deterministic Demo Mode & Live Blockchain Mainnet Support  

---

## 1. System Requirements

- **Operating System:** Windows 10/11, Ubuntu 20.04+, or macOS 12+
- **Python:** Python 3.10, 3.11, 3.12, 3.13, or 3.14
- **Dependencies:** FastAPI, Uvicorn, Requests, Python-Dotenv, Pydantic, ReportLab (all listed in `backend/requirements.txt`)
- **Database:** SQLite 3 (built into Python standard library, zero setup required)
- **Browser:** Any modern web browser (Chrome, Edge, Firefox, Brave)
- **External Dependencies:** **None** (Frontend assets, including Vis.js network visualization, are bundled locally for complete offline reliability)

---

## 2. Quick Start (1-Click Launch)

### On Windows
Simply double-click or run:
```cmd
run.bat
```
This script automatically:
1. Navigates to `backend/`.
2. Generates default `.env` from `.env.example` if not present.
3. Launches the Uvicorn ASGI server at `http://127.0.0.1:8000`.

### On Linux / macOS
```bash
chmod +x run.sh
./run.sh
```

---

## 3. Manual Step-by-Step Installation

### Step 1: Clone or Navigate to the Workspace
```bash
cd "d:\SIH 2"
```

### Step 2: Install Python Dependencies
```bash
python -m pip install -r backend/requirements.txt
```

### Step 3: Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
copy backend\.env.example backend\.env   # On Windows
cp backend/.env.example backend/.env    # On Linux/macOS
```

Default configuration in `backend/.env`:
```env
# Etherscan v2 API key (optional — if omitted, runs in Deterministic DEMO MODE)
ETHERSCAN_API_KEY=""

# TronGrid API key (optional)
TRONGRID_API_KEY=""

# Optional LLM API Key for Copilot (if omitted, uses Deterministic Rule Engine)
OPENAI_API_KEY=""

# Maximum hop depth for graph traversal
MAX_HOPS=3

# Max transactions analyzed per counterparty
MAX_TX_PER_WALLET=200
```

### Step 4: Start the Investigation Platform
```bash
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Open your browser and navigate to:  
👉 **`http://127.0.0.1:8000`**

---

## 4. Operational Modes: Demo Mode vs. Live Mode

### Mode 1: Deterministic DEMO MODE (Default & Recommended for Presentations)
- **Trigger:** Checked by default in the UI, or automatically activated when no `ETHERSCAN_API_KEY` is configured in `backend/.env`.
- **Target Case:** `0x742d35cc6634c0532925a3b844bc454e4438f44e` (Flagged Cybercrime Target — Case `NCRP-2026-849102`).
- **Included Dataset:**
  - 1 Suspect Cybercrime Target
  - 7 Intermediary Wallets (Mule Alpha, Layering Beta, Peel Chain Nodes 1-3, OTC Broker, Forwarder)
  - 1 Sanctioned Mixer (Tornado Cash)
  - 3 Distinct VASP Candidates (CoinDCX FIU-IND, Binance, Kraken)
  - 14 Cryptographically structured transactions with block numbers and timestamps
  - Full chronological timeline
  - Evidence locker with review statuses
  - Pre-drafted Section 91 CrPC requisition notice
- **Advantage:** 100% reliable, zero API latency, zero risk of third-party rate limits during jury evaluation.

### Mode 2: Live Blockchain Tracing (Mainnet)
- **Supported Blockchains:** Ethereum, BNB Smart Chain (BSC), Polygon, Tron, Bitcoin.
- **Setup:** Add your free API key to `backend/.env`:
  ```env
  ETHERSCAN_API_KEY="YOUR_KEY_HERE"
  ```
- **Execution:** Enter any valid on-chain address, uncheck Demo Mode, and click **Start Investigation**. The engine fetches live transactions via Etherscan v2 / TronGrid / Blockstream, traverses the graph via BFS, extracts behavioral features, and matches against the known VASP registry.

---

## 5. Running Automated Verification Tests

CryptoGuard AI includes comprehensive test suites. To execute:

```bash
cd backend
python test_cryptoguard_e2e.py
```
Expected output:
```
============================================================
  CryptoGuard AI — End-to-End API Test Suite
============================================================
[PASS] 1. Health check ok: CryptoGuard AI v2.0.0-SIH26182
[PASS] 2. Supported chains: ['ethereum', 'bsc', 'polygon', 'tron', 'bitcoin']
[PASS] 3. Dashboard summary: 1 cases, 21 VASPs
[PASS] 4. Core trace executed: Inv ID = INV-..., Top VASP = CoinDCX (84.5%)
[PASS] 5. Database retrieval: Case found in SQLite with risk HIGH
[PASS] 6. Evidence lifecycle: EV-01 updated to 'Reviewed'
[PASS] 7. AI Copilot: Answered attribution query via Deterministic Engine
[PASS] 8. Cybercrime response: Section 91 CrPC notice compiled
[PASS] 9. VASP Directory: 11 FIU-IND registered entities verified
[PASS] 10. PDF Report: Generated binary PDF (7,787 bytes)
[PASS] 11. Frontend static bundle served cleanly at /
============================================================
  ALL 11 CRYPTOGUARD AI TESTS PASSED PERFECTLY!
============================================================
```

To run the tracer unit tests:
```bash
python test_tracer.py
```

---

## 6. Database Storage & Persistence

Investigations, transactions, evidence, timeline events, and audit logs are stored in:
```
backend/data/cryptoguard.db (SQLite)
```
- Cases persist across server restarts.
- To inspect via CLI: `sqlite3 backend/data/cryptoguard.db`
- To reset database: Simply delete `cryptoguard.db`; it will automatically re-create and re-seed on next server boot.
