# Wallet-to-VASP Attribution System (SIH-26182)

> Blockchain analytics prototype for law enforcement — traces wallets, scores risk, attributes VASPs.

Built for **Smart India Hackathon (SIH) 2025-26** — Problem Statement ID: SIH-26182

---

## What It Does

1. **Trace** — Follows a wallet's transaction graph outward across multiple blockchains
2. **Score** — Computes a transparent risk score (0-100) using 10 weighted signals
3. **Attribute** — Identifies the nearest VASP/exchange with confidence scoring
4. **Route** — Generates SAHYOG portal routing recommendations
5. **Report** — Downloads a PDF investigation report with full methodology

## Quick Start

```bash
pip install -r backend/requirements.txt
export ETHERSCAN_API_KEY=your_key
cd backend && uvicorn main:app --reload --port 8080
# Open http://localhost:8080
```

## Project Structure

```
SIH26182/
  backend/          # FastAPI backend + frontend static files
    main.py         # API server
    tracer.py       # Multi-chain BFS tracer
    risk_engine.py  # 10-signal risk scoring
    report.py       # PDF generation
    static/         # HTML/CSS/JS frontend
  docs/             # Documentation
    deliverables/   # SRS, PRD, test wallets, data sources
```

## Deliverable Documents

- `docs/deliverables/SRS.md` -- Software Requirements Specification
- `docs/deliverables/PRD.md` -- Product Requirements Document
- `docs/deliverables/TEST_WALLETS.md` -- 10 test addresses for demo
- `docs/deliverables/DATASETS.md` -- Data sources and dataset registry

## Key Features

- 5 blockchains: Ethereum, BSC, Polygon, Tron, Bitcoin
- Transparent risk scoring formula (no black-box ML)
- Score breakdown visible in UI and PDF
- VASP attribution with 4-component confidence scoring
- SAHYOG portal integration
- Interactive transaction graph
- PDF investigation reports

## Test Wallets (Copy-Paste for Demo)

See `docs/deliverables/TEST_WALLETS.md` for 10 curated addresses.

## Risk Scoring Formula

```
final_score = sum(signal_score * signal_weight) + boost
boost = min(20, (n_signals - 1) * 5)
# clamped to [0, 100]

# Thresholds: HIGH >= 60, MEDIUM >= 25, LOW < 25
```

## License

MIT License -- see LICENSE file.