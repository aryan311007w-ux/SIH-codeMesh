---
name: project-context
description: Canonical project context for SIH26182 — Wallet-to-VASP Attribution System
---

# SIH26182 — Project Context

## Why This Project Exists

Smart India Hackathon 2026 problem (SIH-26182) for the Ministry of Home Affairs.

**Problem:** When a cybercrime investigator receives a suspicious cryptocurrency wallet address, the current workflow is manual, slow, and inconsistent — open Etherscan, trace hops, cross-reference spreadsheets, build a report.

**Solution:** Automate the repetitive part. Given an unknown wallet address, the system traces its transaction graph, identifies known VASPs, scores attribution confidence, and produces an investigator-ready report.

## What SIH26182 Solves

| Manual Process | Automated |
|---|---|
| Open blockchain explorer | Wallet input + validation |
| Manually trace hops | BFS graph traversal |
| Cross-reference addresses | VASP registry matching |
| Spreadsheet scoring | Four-dimensional confidence score |
| Assemble report fragments | PDF report generation |
| SAHYOG routing (manual) | SAHYOG routing recommendation stub |

## Architecture

```
SIH26182
│
├── PROBLEM
│   └── Unknown/Suspicious Wallet → VASP Attribution
│
├── INPUT
│   ├── Wallet Address
│   └── Blockchain / Chain
│
├── DATA
│   ├── Blockchain APIs
│   │   ├── Etherscan v2 (Ethereum, BSC, Polygon)
│   │   ├── TronGrid (TRON)
│   │   └── Blockstream.info (Bitcoin)
│   └── Address / Entity Labels
│       └── demo_vasps.csv (10 curated VASP/exchange addresses)
│
├── CORE ENGINE
│   ├── Transaction Normalization
│   ├── Graph Construction
│   ├── Bounded BFS
│   ├── VASP Matching
│   └── Attribution Scoring
│
├── SUPPORTING INTELLIGENCE
│   ├── Risk Engine (10 signals, 9 typologies)
│   ├── Wallet Classification (11 archetypes)
│   ├── High-Risk Registry (~33 addresses)
│   └── Behavioral Feature Extraction (18 features)
│
├── OUTPUT
│   ├── Dashboard (5 panels)
│   ├── Transaction Graph (vis-network)
│   ├── Evidence + Score Breakdown
│   └── PDF Report
│
├── CURRENT STATUS
│   ├── Working (core pipeline)
│   ├── Demo (deterministic fixture)
│   ├── Configuration Required (Etherscan API key)
│   ├── Known Limitation (10 VASP dataset, in-memory storage)
│   └── Future (ML, SAHYOG, multi-chain correlation)
│
└── ROADMAP
    ├── ML ranking (XGBoost/LightGBM)
    ├── Cross-chain correlation
    └── Production deployment
```

## Core Workflow

```
UNKNOWN WALLET
     ↓
BLOCKCHAIN TRANSACTIONS (Etherscan / TronGrid / Blockstream)
     ↓
TRANSACTION GRAPH (nodes = wallets, edges = transactions)
     ↓
BOUNDED BFS TRAVERSAL (multi-hop, hop-limited, node-capped at 60)
     ↓
VASP REGISTRY MATCHING (known address labels)
     ↓
ATTRIBUTION SCORE (4-component: proximity 40%, strength 30%, recency 20%, quality 10%)
     ↓
RISK + CLASSIFICATION (10-signal risk, 11 archetype classifier)
     ↓
INVESTIGATOR DASHBOARD + PDF REPORT
```

## Data Sources

### Blockchain APIs

| Chain | Adapter | API | Key Required |
|---|---|---|---|
| Ethereum | `EVMAdapter` | Etherscan v2 | Yes (free tier) |
| BSC | `EVMAdapter` | Etherscan v2 | Yes (free tier) |
| Polygon | `EVMAdapter` | Etherscan v2 | Yes (free tier) |
| TRON | `TronAdapter` | TronGrid REST | No (optional) |
| Bitcoin | `BTCAdapter` | Blockstream.info | No |

### VASP/Address Labels

| Source | File | Count | Status |
|---|---|---|---|
| Primary | `backend/data/accounts.csv` | 113k+ | Not in repo (gitignored, 12 MB) |
| Demo | `backend/data/demo_vasps.csv` | 10 | **Active** — curated exchanges/VASPs |

The system loads `accounts.csv` when available (provides 113k+ Ethereum address labels). Falls back to `demo_vasps.csv` (10 curated VASP addresses). The architecture accepts any CSV drop-in without code changes.

### High-Risk Registry

Hardcoded set of ~33 addresses: mixer contracts, sanctions-linked addresses, ransomware wallets, darknet market addresses, bridge contracts. Sourced from public OFAC lists and documented threat intelligence.

## Current Implementation

### Backend (Python / FastAPI)

- `backend/main.py` — FastAPI app, 11 endpoints, CORS, security middleware
- `backend/blockchain_client.py` — Multi-chain API adapters with exponential-backoff retry
- `backend/tracer.py` — BFS graph traversal, bounded by hop depth (default 3) and node cap (60)
- `backend/known_vasps.py` — VASP registry loader (primary + demo fallback)
- `backend/models.py` — Pydantic response models
- `backend/demo_fixture.py` — Deterministic demo data for offline demonstration
- `backend/risk_engine.py` — 10-signal risk scorer with 9 laundering typologies
- `backend/wallet_classifier.py` — 11-category wallet type classifier
- `backend/behavioral_features.py` — 18-feature behavioral vector extraction
- `backend/report.py` — PDF generation with reportlab

### Frontend (Vanilla JS / vis-network)

- `backend/static/index.html` — Single-page dashboard
- `backend/static/js/app.js` — Investigation workflow, graph, results rendering
- `backend/static/js/lib/` — Third-party libraries (vis-network, etc.)

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Frontend dashboard |
| GET | `/api/health` | Health check + config status |
| GET | `/api/chains` | Supported chains |
| GET | `/api/vasps` | Known VASP list (searchable) |
| GET | `/api/trace` | **Core** — wallet investigation |
| GET | `/api/risk/{wallet}` | Risk assessment |
| GET | `/api/history` | Session case history |
| GET | `/api/alerts/high-risk` | High-risk wallets |
| GET | `/api/report/{wallet}` | PDF report download |
| POST | `/api/sahyog/submit` | SAHYOG routing stub |

## Demo Mode

The system operates in two modes:

### LIVE MODE
- Requires `ETHERSCAN_API_KEY` in `backend/.env`
- Fetches real blockchain transactions
- Uses live VASP matching against the loaded registry
- Mode indicator: **LIVE ANALYSIS**

### DEMO MODE
- No API key required
- Uses deterministic fixture data from `demo_fixture.py`
- Guaranteed reliable demonstration
- Mode indicator: **DEMO MODE — DETERMINISTIC FIXTURE**

## Security

- Secrets stored server-side only (`backend/.env`, gitignored)
- CORS restricted to localhost origins
- Input validation on all user-facing endpoints
- Wallet address format validation (chain-specific)
- Bounded traversal (`max_hops`, `max_nodes`) preventing runaway queries
- No arbitrary HTML execution from user input
- No API keys in responses or logs
- `.env.example` contains only placeholders

## Attribution Language

Default relationship: **INTERACTS_WITH** (transactional evidence only)

Escalated to **CONTROLLED_BY** only when structural evidence supports it (hop-1 + deposit wallet pattern).

Score range: **X/100** (heuristic investigative score, not probability)

## Known Limitations

1. **VASP coverage** — 10-address demo dataset; full 113k dataset requires separate download
2. **In-memory storage** — Case history lost on server restart
3. **API rate limits** — Free-tier limits; mitigated by request delays and retry logic
4. **Single-chain tracing** — No cross-chain bridge detection (future)
5. **Rule-based scoring** — No trained ML model (future: XGBoost/LightGBM)
6. **SAHYOG** — Routing stub only, no live government portal integration

## Future (Not Implemented)

- XGBoost / LightGBM attribution ranking
- DBSCAN clustering, node2vec / GraphSAGE embeddings
- Graph Neural Networks (GNN)
- RAG investigation agents
- Cross-chain correlation (bridge tracing)
- PostgreSQL persistence
- JWT / RBAC authentication
- Production deployment (Kubernetes, cloud)
- Real SAHYOG government portal integration
- Live sanctions feed (OFAC SDN automated)

## How to Run

```bash
# 1. Clone repository
git clone https://github.com/subhranshuparh/SIH26182.git
cd SIH26182

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Configure (optional — for live mode)
cp backend/.env.example backend/.env
# Edit backend/.env with your Etherscan API key

# 5. Run
cd backend
python main.py
# → http://localhost:8000
```

## How to Demonstrate

### Demo Mode (no API key needed):
1. Start the server: `python backend/main.py`
2. Open `http://localhost:8000`
3. Verify "DEMO MODE" indicator appears
4. Enter wallet: `0x742d35Cc6634C0532925a3b844Bc9e7595f2bD38`
5. Select chain: Ethereum
6. Click **Analyze**
7. Verify: graph renders, VASP candidates appear, score displays, evidence shows, risk/classification visible
8. Download PDF report

### Live Mode (with API key):
1. Add `ETHERSCAN_API_KEY` to `backend/.env`
2. Restart server — indicator changes to "LIVE ANALYSIS"
3. Same workflow as demo mode

## Project Structure

```
SIH26182/
├── backend/
│   ├── main.py                 # FastAPI app + endpoints
│   ├── blockchain_client.py    # Multi-chain API adapters
│   ├── tracer.py               # BFS graph traversal
│   ├── known_vasps.py          # VASP registry
│   ├── risk_engine.py          # Risk scoring
│   ├── wallet_classifier.py    # Wallet classification
│   ├── behavioral_features.py  # Feature extraction
│   ├── demo_fixture.py         # Deterministic demo data
│   ├── models.py               # Pydantic models
│   ├── report.py               # PDF generation
│   ├── .env.example            # Environment template
│   ├── data/
│   │   ├── demo_vasps.csv      # 10 curated VASP addresses
│   │   └── accounts.csv        # 113k+ addresses (gitignored)
│   └── static/
│       ├── index.html          # Dashboard HTML
│       ├── css/                # Stylesheets
│       └── js/
│           ├── app.js          # Main application logic
│           └── lib/            # Third-party libraries
├── docs/
│   ├── presentation_content.md # SIH PPT content
│   ├── PROJECT_CONTEXT.md      # This file
│   ├── PROJECT_TRACKER.md      # Operational tracker
│   └── PROTOTYPE_STATUS.md     # Verification status
├── TASK_TRACKER.md
├── README.md
└── requirements.txt
```
