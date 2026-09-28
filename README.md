# CryptoGuard AI: AI-Powered Blockchain Investigation & VASP Attribution Platform

**Smart India Hackathon (SIH) 2026 — Problem Statement SIH26182**  
*“Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs”*

---

## 1. Executive Summary

**CryptoGuard AI** is a specialized cyber-forensics platform engineered for Law Enforcement Agencies (LEAs), compliance officers, and regulatory bodies (such as I4C and FIU-IND). It automates the extraction and multi-hop graph traversal of illicit cryptocurrency flows, isolates intermediary mule accounts and peel chains, attributes target wallets to Virtual Asset Service Providers (VASPs), and compiles court-admissible statutory requisition notices (Section 91 CrPC / Section 94 BNSS).

```
INVESTIGATION WORKFLOW:
Target Wallet ──> Multi-Hop BFS ──> Behaviour Profiling ──> Intermediary Discovery ──> VASP Attribution ──> Forensic Risk ──> Section 91 Requisition
```

---

## 2. Key Capabilities & Innovations

1. **Explainable VASP Attribution Engine:**
   - Evaluates attribution candidates via an auditable 4-factor scoring model:
     $$\text{Confidence Score} = 0.40 \times \text{Proximity} + 0.30 \times \text{Volume} + 0.20 \times \text{Recency} + 0.10 \times \text{Provenance}$$
   - Generates an interactive **"Explain Attribution"** hop walk detailing exact transaction hashes, block numbers, and factual explanations.
2. **Indian Cybercrime Response Workflow:**
   - Tailored specifically to Indian law enforcement procedures under the Prevention of Money Laundering Act (PMLA 2002), Section 91 of Code of Criminal Procedure (or Section 94 Bharatiya Nagarik Suraksha Sanhita 2023), and Section 102 CrPC (Asset Freeze).
   - Generates ready-to-dispatch formal legal notices populated with verified FIU-IND compliance contacts (CoinDCX, WazirX, ZebPay, Binance, etc.).
3. **Interactive Investigation Workspace (8 Tabs):**
   - **Overview:** High-level case metrics, behavioural archetype, top VASP candidate, next recommended action.
   - **Transaction Graph:** Interactive Vis.js network with visual node archetypes (Target, Mule, VASP, Mixer) and a dedicated **Node Inspector Drawer**.
   - **Wallet Intelligence:** Quantifies velocity (tx/day), burst score, peel chain linearity, in/out ratio, and exposure meters.
   - **VASP Attribution:** Multi-candidate scoring breakdown with confidence badges (Strong, Moderate, Weak, Insufficient).
   - **Risk Analysis:** Transparent 10-signal risk engine with active laundering typologies.
   - **Timeline:** Chronological event sequence tracking victim ingress, layering, and VASP cashouts.
   - **Evidence Locker:** Chain-of-custody ledger allowing investigators to triage items as *Relevant*, *Reviewed*, or *Needs Verification*.
   - **Cybercrime Response:** Section 91 CrPC notice generator and FIU-IND compliance directory.
4. **AI Investigation Copilot:**
   - Embedded forensic assistant answering questions about the active case using a deterministic rule engine (or optional OpenAI/Gemini LLM).
5. **ACID-Compliant Local Database:**
   - Embedded SQLite database (`cryptoguard.db`) persisting investigations, transactions, evidence, and audit logs across reboots.
6. **High-Fidelity Deterministic Demo Mode:**
   - Comprehensive offline demo case (`NCRP-2026-849102`) featuring 1 suspect target, 7 intermediaries, 1 mixer, 3 VASPs, and 14 transactions, guaranteeing a 100% zero-failure demo for SIH evaluation.

---

## 3. Quick Start Guide

### 1-Click Launch (Windows)
```cmd
run.bat
```

### Linux / macOS
```bash
chmod +x run.sh
./run.sh
```

### Manual Launch
```bash
# 1. Install dependencies
python -m pip install -r backend/requirements.txt

# 2. Launch FastAPI ASGI server
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Open **`http://127.0.0.1:8000`** in any modern web browser.

---

## 4. Multi-Chain Support

| Blockchain | Adapter | Required Key | Status |
|---|---|---|---|
| **Ethereum (ETH)** | Etherscan v2 API | `ETHERSCAN_API_KEY` (or Demo Mode) | Supported |
| **BNB Smart Chain (BSC)** | Etherscan v2 Multi-chain | `ETHERSCAN_API_KEY` (or Demo Mode) | Supported |
| **Polygon (MATIC)** | Etherscan v2 Multi-chain | `ETHERSCAN_API_KEY` (or Demo Mode) | Supported |
| **Tron (TRX)** | TronGrid REST API | `TRONGRID_API_KEY` (optional) | Supported |
| **Bitcoin (BTC)** | Blockstream.info REST | None (Public) | Supported |

*Note: If no API key is configured, CryptoGuard AI automatically and gracefully executes in Deterministic Demo Mode with synthetic forensic data.*

---

## 5. Comprehensive Documentation Index

- 📘 [PROJECT_SETUP.md](file:///d:/SIH%202/PROJECT_SETUP.md) — Detailed installation, environment variables, and troubleshooting.
- 📐 [ARCHITECTURE.md](file:///d:/SIH%202/ARCHITECTURE.md) — Technical specifications, mathematical scoring models, and database schema.
- 🔌 [API_DOCUMENTATION.md](file:///d:/SIH%202/API_DOCUMENTATION.md) — Complete REST endpoint reference and JSON schemas.
- ⏱️ [DEMO_GUIDE.md](file:///d:/SIH%202/DEMO_GUIDE.md) — Step-by-step 3-minute hackathon jury demonstration script.
- 📊 [SIH_PPT_CONTENT.md](file:///d:/SIH%202/SIH_PPT_CONTENT.md) — Complete 8-slide presentation content and talking points.
- 🔬 [REFERENCE_ANALYSIS.md](file:///d:/SIH%202/REFERENCE_ANALYSIS.md) — Technical audit of the reference project and our architectural evolution.

---

## 6. Verification & Automated Testing

To run the complete automated end-to-end verification suite:
```bash
cd backend
python test_cryptoguard_e2e.py
```

All 11 verification tests validate health checks, multi-hop BFS tracing, SQLite persistence, evidence updates, AI copilot responses, Section 91 notice generation, FIU VASP directory filtering, and binary PDF report generation.
