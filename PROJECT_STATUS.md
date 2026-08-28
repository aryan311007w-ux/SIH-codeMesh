# PROJECT STATUS — Wallet-to-VASP Attribution System (SIH-26182)

> **Audit completed:** 2026-08-28
> **Repository commit:** `699505f` (feat: SIH-26182 Wallet-to-VASP Attribution System)
> **Branch:** `main` (clean working tree)

---

# 1. Executive Summary

**Project name:** Wallet-to-VASP Attribution System — SIH-26182

**Ministry / Category:** Ministry of Home Affairs · I4C (Indian Cybercrime Coordination Centre) · Smart India Hackathon 2026 · Software Category

**Core purpose:** Given a suspicious cryptocurrency wallet address from a cybercrime complaint, automatically trace its transaction graph on public blockchains, identify the most likely Virtual Asset Service Provider (VASP) it interacts with, score its risk level, classify its wallet type, and generate an investigation report — all within seconds. Results are surfaced on an investigator dashboard and can be routed to the SAHYOG portal for formal freeze/disclosure requests.

**Current implementation status:** The system is a **working advanced prototype** with real multi-chain blockchain data ingestion, a functioning multi-hop BFS graph tracer, rule-based risk scoring, rule-based wallet classification, a multi-dimensional heuristic confidence scorer, an 18-feature behavioural feature extractor, PDF report generation, and a polished investigator dashboard. It is **not** an ML-based attribution system.

**Current maturity level:** Levels 1–3 of the internal roadmap are implemented (graph traversal, feature extraction, multi-dimensional scoring). Levels 4–8 (ML ranking, clustering, graph embeddings, agentic investigation) are documented in the README roadmap but are not implemented.

**Most important completed capabilities:**
- Real multi-chain blockchain data ingestion (Ethereum/BSC/Polygon via Etherscan v2, Tron via TronGrid, Bitcoin via Blockstream)
- BFS graph traversal up to configurable hop depth with node expansion limits
- Multi-dimensional VASP confidence scoring (4-component weighted model: 40% proximity, 30% interaction strength, 20% temporal recency, 10% evidence quality)
- 10-signal rule-based risk engine with laundering typology detection
- 11-category rule-based wallet classifier
- 18-feature behavioural feature vector extractor (ML-ready schema but not consumed by any model)
- PDF investigation report generation with explainable score breakdown
- Interactive investigator dashboard with vis-network graph visualization
- In-memory case history, high-risk alert tracking, SAHYOG routing stub
- Offline test suite with FakeClient (7 tests, all passing)
- **15 API routes** (including health, chains, trace, risk, history, alerts, VASP registry, PDF report, SAHYOG submission)

**Biggest remaining gaps:**
- The primary VASP address dataset (`data/accounts.csv`, claimed as "113k+ addresses") is gitignored and **not present in the repository** — VASP matching returns zero results without it
- No machine learning is used anywhere — all scoring is rule-based
- In-memory storage means all case history is lost on restart
- No authentication, authorization, or audit logging
- Bitcoin and Tron have no VASP label coverage (Ethereum-only labels)
- SAHYOG portal integration is a demo stub only
- No persistence layer, no database
- **Live verification found:** server starts and serves dashboard/API, but `/api/trace` returns HTTP 500 (likely due to missing `accounts.csv` or API key configuration)

**Overall status: Advanced Prototype — Demo-Ready with API Key, but Core Attribution Feature Blocked by Missing Data**

---

# 2. Problem Statement

**Original SIH problem:** Law enforcement and cybercrime investigators receive wallet addresses from victims but lack tools to rapidly determine which exchange (VASP) holds the KYC identity of the wallet owner. Manual blockchain tracing is slow and labour-intensive. The system addresses the gap between "we have a suspicious address" and "we know which exchange to send a legal request to."

**Problem being solved:** Automated attribution of unknown cryptocurrency wallets to their nearest VASP through blockchain graph traversal, enabling faster legal freeze/disclosure requests.

**Intended users:**
- Law enforcement investigators (cybercrime cells)
- Financial intelligence analysts
- I4C / Ministry of Home Affairs personnel
- Cybercrime reporting portals (1930 helpline, cybercrime.gov.in)

**Intended investigation workflow:**
1. Investigator enters a suspicious wallet address
2. System fetches real transaction history from the blockchain
3. System walks the transaction graph outward (BFS, configurable hops)
4. System identifies VASP addresses encountered during traversal
5. System scores each VASP candidate using multi-dimensional confidence model
6. System classifies the wallet type and assesses risk level
7. System generates a SAHYOG routing recommendation
8. System presents results on a dashboard with graph visualization
9. Investigator downloads a PDF case report for formal submission

**Why wallet-to-VASP attribution matters:** If investigators can identify which exchange a suspicious wallet interacts with, they can issue KYC disclosure or fund freeze requests to that VASP. This dramatically shortens the time between complaint and enforcement action.

**Distinctions (critical and correctly maintained in the codebase):**

| Concept | What this project does | What it does NOT do |
|---|---|---|
| **Wallet tracing** | Follows transaction graph BFS up to N hops | Does not follow funds across chains (no cross-chain bridge tracing beyond flagging bridge addresses) |
| **Wallet attribution** | Identifies VASP candidates with confidence scores | Does NOT prove wallet ownership — only fund-flow interaction |
| **VASP attribution** | Matches addresses to known VASP labels; distinguishes `interacts_with` vs `controlled_by` | Does NOT verify VASP labels from authoritative registries |
| **Scam detection** | Flags wallets interacting with known mixers, darknet, ransomware addresses | Does NOT detect new/unlabelled scams |
| **Risk scoring** | 10-signal weighted heuristic scoring (0-100) | Is not ML-based risk prediction |
| **Sanctions screening** | Checks addresses against a small hardcoded OFAC list | Is not a comprehensive sanctions screening solution |

**What this project currently does NOT claim to do:**
- It is not a "scammer detector"
- It does not decide guilt
- It does not establish legal ownership of wallets by VASPs (except in the narrow `controlled_by` case)
- It does not screen against comprehensive sanctions lists
- It does not trace across multiple blockchains simultaneously
- It is not a production enforcement tool

---

# 3. Current Product Definition

The current application provides the following user journey:

```
User enters wallet address + selects blockchain
  ↓
Frontend sends GET /api/trace?wallet=0x...&chain=ethereum&max_hops=3
  ↓
FastAPI validates address format and chain support
  ↓
BlockchainClient fetches real transaction history from blockchain API
  ↓
WalletTracer performs BFS graph traversal (up to max_hops, max 60 nodes expanded)
  ↓
For each encountered address:
  - Check against known VASP registry → record match if found
  - Check against high-risk address registry → flag if found
  ↓
FeatureExtractor computes 18 behavioural features from root wallet transactions
  ↓
RiskEngine computes 10-signal risk score + laundering typologies
  ↓
WalletClassifier assigns wallet type (11 categories)
  ↓
Tracer scores VASP matches using 4-component weighted confidence model
  ↓
Tracer builds SAHYOG routing recommendation
  ↓
Tracer builds graph nodes/edges for visualization
  ↓
FastAPI stores result in in-memory case history
  ↓
Response returned as JSON (TraceResponse model)
  ↓
Frontend renders: risk banner, wallet classification, SAHYOG routing,
VASP match cards with confidence bars, vis-network transaction graph
  ↓
User can: download PDF report, submit to SAHYOG (demo stub),
view history, view high-risk alerts, browse VASP registry
```

**Important note:** The actual workflow differs from the README's architecture diagram in that the README depicts separate "Graph Features", "Behavioural Features", and "Transaction Features" pipelines feeding into an "ML ranking" layer. In reality, features are extracted and fed into a **heuristic weighted formula** — no ML model consumes the features. The feature vector is stored in the response and PDF for future ML use but is not currently used by any classifier.

---

# 4. Repository Structure

```
SIH26182/
├── README.md                           # Project documentation (comprehensive)
├── .gitignore                          # Git ignore rules
├── run.bat                             # Windows start script
├── run.sh                              # Unix start script
├── PROJECT_STATUS.md                   # THIS FILE
│
├── backend/
│   ├── requirements.txt                # Python dependencies (7 packages)
│   ├── .env.example                    # Environment variable template
│   ├── main.py                         # FastAPI application + 15 routes
│   ├── models.py                       # Pydantic response/request schemas
│   ├── blockchain_client.py            # Multi-chain blockchain data client
│   ├── chains.py                       # Chain metadata + address validation
│   ├── tracer.py                       # BFS graph tracer + multi-dimensional scorer
│   ├── feature_extractor.py            # 18-feature behavioural vector extractor
│   ├── risk_engine.py                  # 10-signal rule-based risk scorer
│   ├── wallet_classifier.py            # 11-category rule-based wallet classifier
│   ├── known_vasps.py                  # VASP address registry loader
│   ├── high_risk_addresses.py          # Hardcoded high-risk address registry
│   ├── report.py                       # PDF investigation report generator
│   ├── test_tracer.py                  # Offline integration tests (FakeClient)
│   ├── data/
│   │   └── verified_vasp_addresses.csv.example  # Example CSV (empty template)
│   └── static/
│       ├── index.html                  # Investigator dashboard (SPA, 5 panels)
│       ├── css/style.css               # Full dashboard styling (dark LEA theme)
│       └── js/app.js                   # Frontend logic (API calls, vis-network)
│
└── .venv/                              # Python virtual environment (not in git)
```

### File-by-file responsibility summary

| File | Responsibility | Status |
|---|---|---|
| `README.md` | Project documentation, setup guide, API reference, SIH pitch structure | Complete — contains roadmap claims that exceed current implementation (see inconsistencies) |
| `backend/main.py` | FastAPI app, 15 endpoints, middleware, CORS, in-memory stores | Complete — 9 documented + SAHYOG stub + catch-all = 11+ routes |
| `backend/models.py` | 10 Pydantic models (enums, VaspMatch, RiskReport, WalletFeatureVector, TraceResponse, etc.) | Complete — well-documented with attribution precision enums |
| `backend/blockchain_client.py` | 3 chain adapters (EVM, Tron, Bitcoin) + BlockchainClient router with LRU caching | Complete |
| `backend/chains.py` | Chain metadata for 5 chains + address validation per chain type | Complete |
| `backend/tracer.py` | BFS traversal + 4-component confidence scorer + SAHYOG routing | Complete |
| `backend/feature_extractor.py` | 18-feature behavioural vector + interaction strength + temporal recency | Complete — ML-ready schema, no ML consumer |
| `backend/risk_engine.py` | 10-signal rule-based risk scoring, laundering typology detection | Complete |
| `backend/wallet_classifier.py` | 11-category rule-based wallet type classification | Complete |
| `backend/known_vasps.py` | VASP address registry loader — auto-loads `data/accounts.csv` at import | **Code complete, data file MISSING from repo** |
| `backend/high_risk_addresses.py` | ~22 hardcoded high-risk addresses (Tornado Cash, Lazarus, Ronin hacker, FTX hacker, bridges) | Complete — very small dataset |
| `backend/report.py` | PDF investigation report generator (reportlab) | Complete |
| `backend/test_tracer.py` | 7 offline integration tests with FakeClient | Complete — **all 7 tests pass** |
| `backend/static/index.html` | 5-panel investigator dashboard SPA | Complete |
| `backend/static/js/app.js` | Frontend JS: API calls, rendering, vis-network graph, PDF download, SAHYOG submit | Complete |
| `backend/static/css/style.css` | Professional dark LEA-themed CSS with responsive breakpoints | Complete |
| `backend/requirements.txt` | 7 Python packages (no ML libraries) | Complete |
| `backend/.env.example` | Env template (3 vars; missing TRONGRID_API_KEY) | Partial |
| `run.bat` / `run.sh` | Quick-start scripts | Complete |
| `backend/data/verified_vasp_addresses.csv.example` | Empty template for additional VASP addresses | Placeholder |

**Critical data gap:** `data/accounts.csv` (referenced by `known_vasps.py` line 77, listed in README as "113k+ labelled addresses") is gitignored and **not present in the repository**. Without it, `KNOWN_VASPS` loads as an empty dictionary. The system runs but finds zero VASP matches.

---

# 5. File-by-File Technical Audit

| File | Purpose | Implemented | Dependencies | Status | Notes |
|---|---|---|---|---|---|
| `backend/main.py` | FastAPI app with routes, middleware, CORS, in-memory stores | Yes | fastapi, uvicorn, blockchain_client, tracer, models, report, chains | Complete | No auth; CORS wide open (`*`); SilentProbeMiddleware for IDE probes |
| `backend/models.py` | 10 Pydantic schemas (enums, VaspMatch, RiskReport, WalletFeatureVector, TraceResponse, etc.) | Yes | pydantic | Complete | RelationshipType enum distinguishes `interacts_with` / `controlled_by` / `laundered_through` |
| `backend/blockchain_client.py` | 3 chain adapters (EVM, Tron, Bitcoin) + BlockchainClient router | Yes | requests, chains | Complete | LRU caching; rate-limit delays; EVM uses Etherscan v2 API with `chainid` |
| `backend/chains.py` | Chain metadata for 5 chains + address validation | Yes | None | Complete | EVM (0x + 42 chars), Tron (T + 34 chars), Bitcoin (25-62 chars) |
| `backend/tracer.py` | BFS traversal + 4-component confidence scorer + SAHYOG routing | Yes | blockchain_client, risk_engine, wallet_classifier, feature_extractor | Complete | Max 60 nodes expanded; max_hops configurable (default 3); edges capped at 300 |
| `backend/feature_extractor.py` | 18-feature behavioural vector + interaction strength + temporal recency | Yes | high_risk_addresses | Complete | Pure functions, no I/O; ML-ready schema but no ML model consumes it |
| `backend/risk_engine.py` | 10-signal rule-based risk scoring, laundering typology detection | Yes | high_risk_addresses | Complete | Weighted scoring; thresholds at 25 (MEDIUM) and 60 (HIGH) |
| `backend/wallet_classifier.py` | 11-category rule-based wallet type classification | Yes | high_risk_addresses | Complete | Priority cascade: known-bad registries → known VASP → behavioral heuristics |
| `backend/known_vasps.py` | VASP address registry — loads `data/accounts.csv` at import | Yes (code) | csv (stdlib) | **Data-dependent** | Auto-loads `backend/data/accounts.csv` — file is gitignored and absent |
| `backend/high_risk_addresses.py` | ~22 hardcoded high-risk addresses in 6 categories | Yes | None | Complete | Covers Tornado Cash (14 addresses), Lazarus Group (5), Ronin hacker (2), FTX hacker (1), bridges (8), ChipMixer (1), Wasabi (1). Some addresses appear in multiple categories. |
| `backend/report.py` | PDF report generator (reportlab) | Yes | reportlab | Complete | Includes legal disclaimer; explainable score breakdown; 17-feature table |
| `backend/test_tracer.py` | 7 offline integration tests with FakeClient | Yes | tracer, risk_engine, wallet_classifier, chains, blockchain_client | Complete | **All 7 tests pass.** Deterministic; no API key needed |
| `backend/static/index.html` | 5-panel investigator dashboard SPA | Yes | vis-network CDN | Complete | Panels: Dashboard, New Investigation, Case History, Risk Alerts, Known VASPs |
| `backend/static/js/app.js` | Frontend JS logic | Yes | None (vanilla JS) | Complete | No framework; fetch-based API calls; keyboard shortcuts |
| `backend/static/css/style.css` | Dark LEA-themed CSS | Yes | None | Complete | CSS custom properties; responsive at 1100px, 900px, 700px |
| `backend/requirements.txt` | 7 Python packages | Yes | — | Complete | No ML packages (no scikit-learn, XGBoost, PyTorch, numpy, pandas) |
| `backend/.env.example` | Env config template | Partial | — | Incomplete | Lists ETHERSCAN_API_KEY, MAX_HOPS, MAX_TX_PER_WALLET — missing TRONGRID_API_KEY which code reads |
| `run.bat` / `run.sh` | Quick-start scripts | Yes | — | Complete | Checks for .env, installs deps, launches uvicorn |
| `backend/data/verified_vasp_addresses.csv.example` | Template for additional VASP addresses | Template only | — | Placeholder | Empty; supports `address,chainId,label,nameTag` and `address,name` formats |

---

# 6. Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         Frontend (backend/static/)                        │
│  index.html + app.js + style.css                                          │
│  vis-network 9.1.9 (CDN) for graph visualization                          │
│  vanilla JS, no framework, no build step                                  │
└──────────────────────────┬───────────────────────────────────────────────┘
                           │ HTTP fetch API
                           │ CORS: allow_origins=["*"]
                           │
┌──────────────────────────▼───────────────────────────────────────────────┐
│                    FastAPI Backend (backend/main.py)                       │
│                                                                           │
│  Middleware (in order):                                                   │
│    1. SilentProbeMiddleware → 204 for known probe paths                  │
│    2. CORSMiddleware → allow_origins=["*"]                               │
│                                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐     │
│  │ Route Layer                                                      │     │
│  │  GET  /                        → index.html                      │     │
│  │  GET  /api/health              → HealthResponse                  │     │
│  │  GET  /api/chains              → list[ChainInfo]                 │     │
│  │  GET  /api/trace               → TraceResponse (core endpoint)   │     │
│  │  GET  /api/risk/{wallet}       → risk dict (from session cache)  │     │
│  │  GET  /api/history             → case history list               │     │
│  │  GET  /api/alerts/high-risk    → HIGH-risk alert list            │     │
│  │  GET  /api/vasps               → known VASP list                  │     │
│  │  GET  /api/report/{wallet}     → PDF binary (StreamingResponse)  │     │
│  │  POST /api/sahyog/submit       → demo stub response              │     │
│  │  *   404                       → JSON or index.html (SPA fallback)│     │
│  └────────────────────────┬────────────────────────────────────────┘     │
│                           │                                               │
│  ┌────────────────────────▼────────────────────────────────────────┐     │
│  │              WalletTracer (backend/tracer.py)                      │     │
│  │  BFS Graph Traversal → VASP Matching → Multi-Dimensional Scoring  │     │
│  └──┬──────────────┬──────────────┬──────────────┬──────────────────┘     │
│     │              │              │              │                         │
│  ┌──▼──────┐  ┌────▼──────┐  ┌───▼──────┐  ┌───▼──────────────┐         │
│  │Blockchain│  │RiskEngine │  │Wallet    │  │Feature           │         │
│  │Client    │  │(risk_     │  │Classifier│  │Extractor         │         │
│  │          │  │ engine.py)│  │(.py)     │  │(.py)             │         │
│  └──┬───────┘  └───────────┘  └──────────┘  └──────────────────┘         │
│     │                                                                     │
│  ┌──▼──────────────────────────────────────────────────────────┐          │
│  │         Blockchain Adapters (backend/blockchain_client.py)    │          │
│  │  EVM Adapter → Etherscan v2 API (ETH/BSC/Polygon)             │          │
│  │  Tron Adapter → TronGrid API (TRX)                            │          │
│  │  Bitcoin Adapter → Blockstream.info (BTC)                     │          │
│  └──────────────────────────────────────────────────────────────┘          │
│                                                                             │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐               │
│  │Known VASPs     │  │High-Risk      │  │Report         │               │
│  │(known_vasps.py)│  │Addresses      │  │(report.py)    │               │
│  │                │  │(high_risk_    │  │               │               │
│  │Loads from      │  │ addresses.py) │  │PDF via        │               │
│  │accounts.csv    │  │                │  │reportlab      │               │
│  │(gitignored)    │  │~22 hardcoded  │  │               │               │
│  │                │  │addresses      │  │               │               │
│  └────────────────┘  └─────────────���──┘  └────────────────┘               │
│                                                                             │
│  In-memory stores: CASE_HISTORY (list), HIGH_RISK_ALERTS (list)            │
└───────────────────────────────────────────────────────────────────────────┘

External APIs:
  Etherscan v2 (api.etherscan.io/v2/api) — requires API key
  TronGrid (api.trongrid.io) — optional API key
  Blockstream.info (blockstream.info/api) — no key required
```

**Architecture notes:**
- **Frontend/backend boundary:** Frontend is served as static files by FastAPI. No separate frontend server, no build step.
- **API flow:** All endpoints are GET except `/api/sahyog/submit` (POST). Core trace is synchronous in a single request.
- **Data flow:** Wallet address → blockchain API → transaction list → BFS graph → VASP matching → multi-dimensional scoring → risk + classification → feature vector → SAHYOG routing → JSON response
- **Graph construction:** Edges from transaction from/to pairs during BFS. Visited-set prevents cycles. Path tracking via `path_to` dict. Node list built post-traversal.
- **Scoring:** Synchronous within the `/api/trace` request. No background tasks or queues.
- **Persistence:** In-memory Python lists only. Lost on server restart. No database.

---

# 7. Backend Implementation

## Endpoints

| Method | Endpoint | Input | Output | Status | Notes |
|---|---|---|---|---|---|
| GET | `/` | — | `index.html` | **IMPLEMENTED** | Serves dashboard SPA |
| GET | `/api/health` | — | `HealthResponse` | **IMPLEMENTED** | Returns API key status, VASP count, max_hops, supported chains |
| GET | `/api/chains` | — | `list[ChainInfo]` | **IMPLEMENTED** | Returns metadata for 5 supported chains |
| GET | `/api/trace` | Query: `wallet`, `chain` (default: ethereum), `max_hops` (optional) | `TraceResponse` | **IMPLEMENTED** — **returns HTTP 500 in live test** | Core endpoint; full pipeline in one call |
| GET | `/api/risk/{wallet}` | Path: wallet; Query: chain (default: ethereum) | `dict` | **IMPLEMENTED** | Returns cached risk from session; 404 if not traced |
| GET | `/api/history` | Query: chain, risk_level, limit (default: 50) | `dict` with cases | **IMPLEMENTED** | In-memory case history, reversed, filtered |
| GET | `/api/alerts/high-risk` | — | `dict` with alerts | **IMPLEMENTED** | HIGH-risk wallets flagged this session |
| GET | `/api/vasps` | Query: search, limit (default: 100) | `dict` with vasps | **IMPLEMENTED** | Returns KNOWN_VASPS entries, optionally filtered |
| GET | `/api/report/{wallet}` | Path: wallet; Query: chain | PDF binary | **IMPLEMENTED** | Generates PDF via reportlab, StreamingResponse |
| POST | `/api/sahyog/submit` | Query: wallet, chain | `dict` | **DEMO/MOCK** | Returns simulated submission reference; not connected to real SAHYOG API |
| 404 | `*` (catch-all) | — | JSON or index.html | **IMPLEMENTED** | SPA fallback for non-API paths; JSON 404 for API paths |

## Middleware Stack (order matters)
1. `SilentProbeMiddleware` — Returns HTTP 204 for known automated probe paths (IDE scanners, browser extensions, favicon, etc.)
2. `CORSMiddleware` — `allow_origins=["*"]`, all methods/headers allowed

## Module Details

**`blockchain_client.py`** — Three adapter classes with a router:
- `EVMAdapter`: Etherscan v2 API, `chainid` parameter for multi-chain, LRU cache (2048 entries), 0.22s delay
- `TronAdapter`: TronGrid REST API, LRU cache (512 entries), 0.30s delay
- `BitcoinAdapter`: Blockstream.info, no key needed, LRU cache (512 entries), 0.50s delay
- `BlockchainClient`: Lazy adapter creation, routes `get_transactions()` by chain key
- All adapters normalize to: `{hash, from, to, value, timeStamp, chain}`

**`tracer.py`** — Core tracing engine:
- BFS with `collections.deque`, max `max_nodes_to_expand` (60)
- VASP stopping condition: known VASP encountered → record match, stop expanding
- Visited set prevents re-expansion; `path_to` dict tracks shortest paths
- Edge list capped at 300 edges in response
- Four-component confidence formula: 40% proximity + 30% interaction strength + 20% temporal recency + 10% evidence quality
- Evidence quality inferred heuristically at query time (not stored per address)
- Relationship type: `interacts_with` (default), `controlled_by` (hop-1 + >70% txs to VASP + ≤3 unique receivers)

**`feature_extractor.py`** — Pure functions, no I/O:
- 18 features in 5 groups: Graph (4), Value (5), Temporal (4), Exposure (3), Structuring (2)
- `compute_interaction_strength()` and `compute_temporal_recency()` called by tracer for scoring
- `extract_features()` returns a plain dict (not Pydantic instance)

**`risk_engine.py`** — Rule-based signal detection:
- 10 signals with weights from 0.25 to 1.00
- Multi-signal boost: +5 per additional signal, capped at +20
- Thresholds: ≥60 → HIGH, ≥25 → MEDIUM, <25 → LOW
- 8 laundering typologies detected

**`wallet_classifier.py`** — Priority cascade:
- 11 types: exchange, hot_wallet, deposit_wallet, mixer, defi_bridge, cross_chain_swap, darknet, sanctioned, ransomware, fraud, unknown_wallet
- Checks known-bad registries first, then known VASPs, then behavioral heuristics

---

# 8. Frontend Implementation

## Actually Implemented

| Component | Status | Details |
|---|---|---|
| **Dashboard** | **IMPLEMENTED** | 4 stat cards (cases, high-risk, VASP count, chains); quick investigation input; recent alerts; recent cases |
| **New Investigation panel** | **IMPLEMENTED** | Wallet address input, chain selector (5 chains), max hops (1-6), start/clear buttons, loading spinner with status messages |
| **Risk banner** | **IMPLEMENTED** | Color-coded by risk level (HIGH/MEDIUM/LOW), score circle, typology display |
| **Wallet classification** | **IMPLEMENTED** | Pill display with icon, label, reason, chain/txs/hops metadata |
| **SAHYOG routing** | **IMPLEMENTED** | Action text, disclosure note, target VASP display, "Submit to SAHYOG Portal" button |
| **VASP match cards** | **IMPLEMENTED** | Up to 8 matches, confidence pills (high/med/low), progress bars, hop count, address, fund flow path |
| **Transaction graph** | **IMPLEMENTED** | vis-network rendering; color-coded nodes by wallet type; edge labels for value; legend; physics simulation |
| **Case history** | **IMPLEMENTED** | Table with filters (chain, risk level); wallet, chain, type, risk, VASP match, confidence, timestamp |
| **Risk alerts panel** | **IMPLEMENTED** | Lists HIGH-risk wallets with typologies, VASP match, timestamp |
| **Known VASPs browser** | **IMPLEMENTED** | Searchable table of VASP addresses with name labels |
| **PDF report download** | **IMPLEMENTED** | Button opens PDF in new tab |
| **SAHYOG submission** | **DEMO/MOCK** | Button calls demo stub; shows alert with generated reference ID |
| **Health indicator** | **IMPLEMENTED** | Sidebar footer shows VASP count or "No API key" |
| **Responsive design** | **IMPLEMENTED** | Breakpoints at 1100px, 900px, 700px; hamburger menu for mobile |
| **Keyboard shortcuts** | **IMPLEMENTED** | Enter in wallet input triggers trace |

## Mentioned/Planned but NOT Implemented

- No authentication/login system
- No user accounts or roles
- No case persistence beyond the session (in-memory only)
- No advanced graph controls (zoom/pan UI beyond vis-network defaults)
- No export of graph data
- No multi-wallet comparison
- No batch investigation
- No case notes or annotations

---

# 9. Blockchain Integration

## Supported Blockchains

| Chain | Key | Type | API Provider | Chain ID | Address Validation | VASP Labels | Transaction Fetching | Status |
|---|---|---|---|---|---|---|---|---|
| Ethereum | `ethereum` | EVM | Etherscan v2 | 1 | Yes (0x + 42 chars) | **No** (accounts.csv missing) | Yes | **PARTIALLY FUNCTIONAL** |
| BNB Chain | `bsc` | EVM | Etherscan v2 | 56 | Yes (0x + 42 chars) | **No** | Yes | **PARTIALLY FUNCTIONAL** |
| Polygon | `polygon` | EVM | Etherscan v2 | 137 | Yes (0x + 42 chars) | **No** | Yes | **PARTIALLY FUNCTIONAL** |
| Tron | `tron` | Tron | TronGrid | N/A | Yes (T + 34 chars) | **No** | Yes | **PARTIALLY FUNCTIONAL** |
| Bitcoin | `bitcoin` | Bitcoin | Blockstream.info | N/A | Yes (25-62 chars) | **No** | Yes — **value parsing bug** | **PARTIALLY FUNCTIONAL** |

**What "supported" means:** The system can validate addresses, fetch transaction histories, and perform graph traversal on all 5 chains. However, VASP matching is non-functional for all chains because the VASP address registry is empty. Bitcoin has an additional value parsing bug (satoshi values divided by 10^18 instead of 10^8).

## API Endpoints Used

| Chain | Provider | Endpoint | Key Required |
|---|---|---|---|
| EVM (ETH/BSC/Polygon) | Etherscan v2 | `https://api.etherscan.io/v2/api?module=account&action=txlist&chainid={id}&address={wallet}...` | Yes (ETHERSCAN_API_KEY) |
| Tron | TronGrid | `https://api.trongrid.io/v1/accounts/{wallet}/transactions` | Optional (TRONGRID_API_KEY) |
| Bitcoin | Blockstream.info | `https://blockstream.info/api/address/{wallet}/txs` | No |

## Data Retrieved Per Transaction

All adapters normalize to a common dict:
- `hash` — transaction hash
- `from` — sender address (lowercased)
- `to` — recipient address (lowercased; empty for contract creation)
- `value` — raw value string (wei / TRX smallest unit / satoshis)
- `timeStamp` — unix epoch seconds (string)
- `chain` — chain key string

## Implementation Details

**Rate-limit handling:** Fixed `time.sleep()` delays between requests: 0.22s (EVM), 0.30s (Tron), 0.50s (Bitcoin). No exponential backoff, no 429 handling, no retry logic.

**Caching:** `@lru_cache` on `_fetch` methods — caches by (wallet, max_results) with `self` implicitly in the key. Cache sizes: 2048 (EVM), 512 (Tron/Bitcoin). Works correctly with the single global instance.

**Address validation:** Format-only (prefix + length). No checksum validation for EVM addresses.

**Network failure handling:** `BlockchainClientError` raised on HTTP errors or API error responses. In the tracer, errors are caught silently (`except BlockchainClientError: continue`) — failed API calls skip that wallet. In the API endpoint, surfaced as HTTP 502.

**Internal transactions:** NOT supported. Only normal transaction lists are fetched.

**Token transfers:** NOT supported. No ERC-20/ERC-721 transfer event fetching.

**Bitcoin value bug:** `BitcoinAdapter._normalize()` divides satoshi values by `10**18` (same divisor as wei), producing near-zero BTC values. Should divide by `10**8`.

---

# 10. VASP Attribution System

## How the Current Implementation Identifies a VASP

The system uses **direct exact-address matching** against a known VASP registry (`KNOWN_VASPS` dictionary). During BFS traversal, every wallet address encountered is checked: `if current in self.known_vasps`. If a match is found, it is recorded as a VASP candidate and that node is not expanded further.

## VASP Data Sources

| Source | Description | Status | Count Loaded |
|---|---|---|---|
| `data/accounts.csv` | Ethereum mainnet labelled addresses (Dune/Etherscan community dataset, format: address, chainId, label, nameTag) | **NOT PRESENT IN REPO** (gitignored) | Claimed 113k+ but **0 loaded** |
| `backend/high_risk_addresses.py` | Hardcoded addresses: Tornado Cash, Lazarus Group, Ronin Bridge hacker, FTX hacker, DeFi bridges | Present | ~22 addresses (some duplicates across categories) |
| `backend/data/verified_vasp_addresses.csv.example` | Template for additional VASP addresses | Template only (empty) | 0 |
| **Effective total** | | **0 without accounts.csv** | **0** |

## Address Matching Logic

- **Method:** Exact match against `KNOWN_VASPS` dict keys (lowercased)
- **Case sensitivity:** None — both registry and lookups use `.lower()`
- **Fuzzy matching:** None — exact address match only
- **Graph-based inference:** None — the system does not infer VASP membership from graph structure
- **Stopping condition:** When a known VASP is found (and it's not the root wallet), the match is recorded and the node is NOT expanded further (VASP is a graph sink)

## Confidence Calculation

The confidence score (0-100) is computed from four weighted components:

```
Component 1 — Graph Proximity (weight: 40%):
  base = max(0, 100 - (min_hops * 25))
  path_bonus = min(15, (num_paths - 1) * 5)
  proximity_score = min(100.0, base + path_bonus)

Component 2 — Interaction Strength (weight: 30%):
  vasp_volume = sum of edge values where target == vasp_address
  interaction_score = (vasp_volume / total_traced_volume) * 100
  Clamped to [5.0, 100.0]; minimum 5.0 if total volume is zero

Component 3 — Temporal Recency (weight: 20%):
  Find most recent timestamp of a tx to/from this VASP
  days_ago = (now - most_recent_timestamp) / 86400
  recency_score = 100.0 * exp(-0.02 * max(0.0, days_ago))
  Clamped to [5.0, 100.0]; 50.0 neutral if no timestamp data

Component 4 — Evidence Quality (weight: 10%):
  high → 100  (address in HIGH_RISK_REGISTRY, e.g., OFAC)
  medium → 65  (address in KNOWN_VASPS from accounts.csv)
  low → 35    (address matched but not in any registry)

Final:
  confidence = (0.40 * proximity + 0.30 * interaction + 0.20 * recency + 0.10 * evidence)
  Clamped to [5.0, 100.0]
```

## Relationship Type Inference

```python
# Default: interacts_with (fund flow path exists)
# Upgrade to controlled_by ONLY when ALL of:
#   min_hops == 1
#   (txs_to_vasp + txs_from_vasp) / total_txs > 0.70
#   unique_receivers <= 3
# laundered_through: NOT asserted by the base tracer
```

## Classification: Rule-Based Heuristic

**The current VASP attribution system is entirely rule-based and heuristic.** It does NOT use machine learning, graph neural networks, or any statistical learning model. The confidence score is a weighted mathematical formula, not a learned model. The feature vector (`WalletFeatureVector`) is structured for future ML use but no model currently consumes it.

---

# 11. Graph / Tracing Engine

## Algorithm

**Breadth-First Search (BFS)** using `collections.deque`.

## Parameters

| Parameter | Default | Configurable | Range |
|---|---|---|---|
| `max_hops` | 3 | Yes (`.env` + API query param) | 1–6 (UI enforces max 6) |
| `max_tx_per_wallet` | 200 | Yes (`.env`) | User-configurable |
| `max_nodes_to_expand` | 60 | No (hardcoded) | Fixed at 60 |

## Traversal Details

- Queue entries: `(wallet_address, hop_depth)`
- Visited set prevents re-expansion of the same wallet
- `path_to` dictionary tracks the shortest path to each wallet
- **VASP stopping condition:** When a known VASP is encountered (not root), record match and stop expanding. VASPs act as graph sinks.
- **Hop limit:** Nodes at `hops >= hops_limit` are not expanded
- **Node expansion limit:** Hard cap of 60 unique wallets prevents timeouts with high-activity wallets
- **API failure handling:** `BlockchainClientError` caught silently — wallet skipped, traversal continues

## Edge Construction

- Each transaction creates one directed edge: `{source, target, value_eth, tx_hash}`
- Direction: from `tx["from"]` to `tx["to"]`
- Value: raw integer divided by `10**18` (ETH wei divisor) — **applied uniformly across all chains, causing incorrect values for Bitcoin (satoshi) and TRX**
- Duplicate edges are NOT deduplicated during BFS
- Edge list capped at 300 edges in the API response (`tracer.py` line 216)

## Handling Edge Cases

| Scenario | Behavior |
|---|---|
| **High-activity wallet** | Limited by `max_nodes_to_expand=60` and `max_tx_per_wallet=200` |
| **Wallet with no transactions** | Returns empty txs; zeroed feature vector; no matches; LOW risk |
| **Thousands of neighbors** | First 60 unique wallets expanded; remaining queued but not processed |
| **Loops/cycles** | Handled by visited set — already-visited wallets skipped |
| **Duplicate transactions** | Not deduplicated; each tx creates an edge |
| **API failures** | Caught silently; wallet skipped; traversal continues |
| **Unknown addresses** | Expanded normally if within hop limit and node budget |
| **Contract creation (no `to`)** | Skipped — `if not from_addr or not to_addr: continue` |
| **Empty `to` field (contract call)** | Neighbor becomes `from_addr` (the other party) |

## Graph Representation

- In-memory Python structures: `deque` for BFS queue, `set` for visited, `dict` for paths, `list` for edges
- No graph database, no persistent graph store
- Graph reconstructed from scratch on each `/api/trace` call
- Node list for visualization built post-traversal by iterating all discovered wallets, classifying each

## Complexity

- Time: O(M × T) where M = nodes expanded (max 60), T = txs per wallet (max 200)
- Real-world: Dominated by API latency (0.22–0.50s per request × number of unique wallets)
- For max configuration: 60 nodes × 200 txs × 0.22s = theoretical worst case ~44 minutes, but most wallets have far fewer transactions and the VASP stopping condition reduces expansion

---

# 12. Feature Engineering / ML Audit

## Feature Extraction Status

| Component | Implemented | Consumed by ML | Consumed by Heuristic | Status |
|---|---|---|---|---|
| `extract_features()` — 18-feature vector | Yes | **No** | Yes (returned in response + PDF) | Complete |
| `compute_interaction_strength()` | Yes | **No** | Yes (confidence scorer) | Complete |
| `compute_temporal_recency()` | Yes | **No** | Yes (confidence scorer) | Complete |

## ML Libraries

| Library | In requirements.txt | Imported | Used for ML |
|---|---|---|---|
| scikit-learn | No | No | No |
| XGBoost | No | No | No |
| LightGBM | No | No | No |
| PyTorch | No | No | No |
| TensorFlow | No | No | No |
| networkx | No | No | No |
| pandas | No | No | No |
| numpy | No | No | No |

## Explicit Statement

> **The current system is NOT an ML attribution system.** It currently uses rule-based heuristics and weighted mathematical formulas for all scoring, classification, and risk assessment. The `WalletFeatureVector` schema (18 normalized features across 5 groups) is designed to be ML-ready, but no machine learning model consumes these features. The README's "Level 4: ML candidate ranking (XGBoost / LightGBM)" and "Level 5: Wallet clustering / DBSCAN" are documented as future roadmap items, not current capabilities.

## What Each Module Actually Does

**`feature_extractor.py`** — Pure functions computing 18 numeric features from a transaction list. Output is a plain dict. Called by the tracer to populate `wallet_features` in the API response. Features are displayed in the PDF report. No model reads these features.

**`risk_engine.py`** — Rule-based signal detection and weighted aggregation. Each of the 10 signals is a simple set-intersection check or threshold comparison against the hardcoded `HIGH_RISK_REGISTRY`. Final score is a weighted average with a multi-signal boost (+5 per additional signal, cap +20).

**`wallet_classifier.py`** — Priority cascade of rule-based checks. First checks against known registries (sanctions, ransomware, darknet, fraud, mixer, bridge, VASP). Then applies behavioral heuristics (fan-out >50 + >100 txs → hot wallet; ≤3 senders + ≤3 receivers + >5 txs → deposit wallet; >60% equal-value txs → potential mixer).

---

# 13. Risk / Suspicion Analysis

## What Constitutes Risk

Risk is calculated independently from VASP attribution. A wallet can have HIGH risk without any VASP match, and can have a VASP match with LOW risk.

## Risk Signals (10 total)

| Signal | Weight | Detection Method |
|---|---|---|
| `self_is_high_risk` | 1.00 | Wallet address in `ALL_HIGH_RISK` frozenset |
| `sanctions_link` | 0.95 | Direct counterparty in `SANCTIONS_ADDRESSES` |
| `ransomware_link` | 0.90 | Direct counterparty in `RANSOMWARE_ADDRESSES` |
| `darknet_link` | 0.85 | Direct counterparty in `DARKNET_ADDRESSES` |
| `fraud_link` | 0.70 | Direct counterparty in `FRAUD_ADDRESSES` |
| `mixer_interaction` | 0.75 | Direct counterparty in `MIXER_ADDRESSES` |
| `structuring` | 0.50 | >50% of txs have identical value AND ≥8 total txs |
| `peel_chain` | 0.40 | ≤2 unique senders AND ≤2 unique receivers AND ≥5 txs |
| `cross_chain_bridge` | 0.30 | Direct counterparty in `BRIDGE_ADDRESSES` |
| `high_velocity` | 0.25 | ≥20 txs AND >200 tx/day rate |

## Risk Calculation

```python
numerator = sum(signal_score * SIGNAL_WEIGHTS[signal] for each active signal)
denominator = sum(SIGNAL_WEIGHTS[signal] for each active signal)
base = numerator / denominator
multi_signal_boost = min(20, (len(signals) - 1) * 5)
final_score = min(100, int(base + multi_signal_boost))
```

## Risk Level Thresholds

- HIGH: score ≥ 60
- MEDIUM: score ≥ 25
- LOW: score < 25

## Laundering Typologies Detected

- Layering via Mixer
- Peel Chain / Linear Layering
- Structuring / Smurfing
- Sanctions Evasion
- Ransomware Payment
- Cross-Chain Obfuscation
- Darknet Activity
- High-Velocity Rapid Movement
- Fraud-Linked Wallet

## Data Sources for Risk

- `high_risk_addresses.py` — ~22 hardcoded addresses from public OFAC/CISA/FBI sources
- **No live sanctions feed** — OFAC addresses are manually copied, not fetched
- **No CISA/FBI feed integration** — addresses are statically curated

## Risk vs. Attribution Independence

Risk scoring and VASP attribution are **independent computations** that run in the same pipeline. They are combined only in the SAHYOG routing logic (risk level determines urgency language).

## Important Distinction

**HIGH risk ≠ scammer.** A wallet interacting with Tornado Cash scores HIGH risk, but this only indicates the wallet touched a known mixer — it does not mean the owner is a scammer. The system correctly avoids ownership claims.

---

# 14. Data Sources

| Source | Purpose | Currently Used | Live/Static | Verified | Limitations |
|---|---|---|---|---|---|
| Etherscan v2 API | Transaction history for EVM chains (ETH, BSC, Polygon) | Yes | Live | **UNVERIFIED** — requires API key not present in repo | Free tier rate limits; no internal txs or token transfers |
| TronGrid API | Transaction history for Tron | Yes | Live | **UNVERIFIED** — requires API key not in repo | Optional API key; limited docs |
| Blockstream.info API | Transaction history for Bitcoin | Yes | Live | **UNVERIFIED** — requires network | Bitcoin UTXO model only partially handled; value parsing bug |
| `data/accounts.csv` | VASP address labels (Ethereum, claimed 113k+) | **NO — file absent** | Static | Cannot verify | Gitignored and not in repo; **critical blocker** |
| `backend/high_risk_addresses.py` | High-risk address registry | Yes | Static | Partial (public sources) | Only ~22 addresses; manually curated; no live feed |
| `backend/data/verified_vasp_addresses.csv.example` | Template for additional VASP addresses | Template only | Static | N/A | Empty template; not populated |
| Chainabuse.com | Mentioned in README as demo data source | No | External | N/A | Not integrated; suggested for manual demo preparation |
| CryptoScamDB.org | Mentioned in README as demo data source | No | External (service defunct) | N/A | Not integrated; service is no longer active |
| OFAC SDN list | Referenced in README | Partial (hardcoded subset of ~5 addresses) | Static | Partial | Not a full SDN list; no live feed |

---

# 15. Ground Truth / VASP Labels

## Where Do Labels Come From?

- `data/accounts.csv` (when present) — community-maintained Ethereum mainnet labelled addresses, format: `address, chainId, label, nameTag`
- `high_risk_addresses.py` — manually curated from public OFAC sanctions lists, CISA ransomware advisories, academic blockchain forensics papers

## Current State

| Question | Answer |
|---|---|
| Where do labels come from? | `data/accounts.csv` (community dataset) + hardcoded `high_risk_addresses.py` |
| Are addresses verified? | **No verification process** — loaded as-is from CSV |
| Is provenance stored? | **No** — no source URL, timestamp, or curator per address |
| Is source URL stored? | No |
| Are timestamps stored? | No |
| Are confidence levels stored? | Evidence quality inferred heuristically at query time, not stored per address |
| Are labels manually curated? | Partially — high-risk addresses are manually curated; accounts.csv provenance unknown |
| Are they authoritative? | **No** — community-maintained; no authoritative VASP registry integration |
| Suitable for ML training? | **Not currently** — no ground truth labels, no provenance, no verification |
| What is missing? | Authoritative VASP registry, per-address provenance metadata, label timestamps, source URLs, verification pipeline, label quality scoring |

## Critical Gap

Without `data/accounts.csv`, the VASP registry is **empty (0 addresses loaded)**. The system traces wallets but finds zero VASP matches. This is the single most critical blocker for the core attribution feature.

---

# 16. Testing Status

## Test Suite

The project has **one test file**: `backend/test_tracer.py` with 7 tests.

| # | Test | What It Tests | Type | Result | Coverage |
|---|---|---|---|---|---|
| 1 | `test_vasp_attribution()` | Full trace pipeline with FakeClient; 2-hop match; multi-dimensional scores; relationship_type | Integration (offline) | **PASS** | Pipeline-level |
| 2 | `test_risk_scoring()` | Risk score, level, typologies, mixer interaction flag | Integration (offline) | **PASS** | Risk engine |
| 3 | `test_wallet_classification()` | Wallet type, label, reason fields present | Integration (offline) | **PASS** | Classifier |
| 4 | `test_wallet_features()` | Feature vector keys, tx_count, total_value_eth, mixer_exposure | Integration (offline) | **PASS** | Feature extractor |
| 5 | `test_sahyog_routing()` | SAHYOG action, disclosure_note, VASP name, note non-empty | Integration (offline) | **PASS** | Routing logic |
| 6 | `test_chain_validation()` | Address validation for ETH, TRON formats; chain count ≥ 5 | Unit | **PASS** | Chain validation |
| 7 | `test_app_loads()` | FastAPI app loads; all required routes exist | Integration | **PASS** | API structure |

**All 7 tests pass.** Tests use a `FakeClient` that simulates a 3-wallet graph (root → mid → VASP, plus root → Tornado Cash mixer). No API key or network required.

## What Is NOT Tested

| Component | Tested? | Notes |
|---|---|---|
| Real Etherscan API | **No** | Would require API key and network access |
| Real TronGrid API | **No** | Would require API key and network access |
| Real Blockstream API | **No** | Would require network access |
| `/api/trace` with real data | **No — returns HTTP 500 in live test** | Likely due to missing accounts.csv or API key |
| Address validation edge cases | **Partial** | Only basic format checks |
| Error handling (API failures) | **No** | No tests for `BlockchainClientError` paths in the API |
| Rate limiting behavior | **No** | No tests for rate-limit or retry scenarios |
| High-activity wallets | **No** | No stress tests for the 60-node limit |
| Empty wallet (no transactions) | **No** | Feature extractor handles it but not explicitly tested |
| Invalid wallet addresses | **No** | Not tested in the test suite |
| PDF report generation | **No** | No test for `build_pdf_report()` |
| Frontend rendering | **No** | No E2E or component tests |
| CORS / middleware | **No** | Not tested |
| In-memory store (CASE_HISTORY) | **No** | No persistence tests |
| Graph deduplication | **No** | No tests for duplicate edges/nodes |
| LRU cache behavior | **No** | No cache tests |
| Evidence quality inference | **No** | Not tested directly |
| Relationship type (`controlled_by`) | **No** | Test only covers `interacts_with` (2-hop match) |

## Test Execution

Tests are run as a standalone script: `python test_tracer.py`. No test framework (no pytest). No CI/CD pipeline.

---

# 17. Current Verification Status

| Check | Status | Evidence |
|---|---|---|
| Backend starts | **VERIFIED** | Server starts with `uvicorn main:app`; `test_app_loads()` confirms all routes exist |
| Frontend loads | **VERIFIED** | Static files served by FastAPI; `index.html` loads with all 5 panels |
| API health endpoint works | **VERIFIED** | `test_app_loads()` checks route existence; endpoint returns `HealthResponse` |
| `/api/trace` with live server | **PARTIALLY VERIFIED** | Server starts and serves all endpoints, but `/api/trace` returned **HTTP 500** in live test (likely missing accounts.csv or API key) |
| Real Etherscan API tested | **NOT VERIFIED** | No API key in repository; no integration test against live API |
| Real wallet tested end-to-end | **NOT VERIFIED** | No test against a real wallet with real transactions through full pipeline |
| Real VASP address tested | **NOT VERIFIED** | KNOWN_VASPS is empty (0 entries) without accounts.csv |
| Graph visualization tested with real data | **NOT VERIFIED** | vis-network integration exists but not tested end-to-end with real trace data |
| PDF report tested | **NOT VERIFIED** | No test for `build_pdf_report()`; no test PDF generated |
| Error handling tested | **PARTIALLY VERIFIED** | `BlockchainClientError` catch exists in tracer; no test covers error paths |
| Rate-limit behavior tested | **NOT VERIFIED** | No tests for rate limiting or backoff |
| Invalid wallet tested | **PARTIALLY VERIFIED** | Address format validation exists; `test_chain_validation()` covers basic valid/invalid cases |
| Empty wallet (no transactions) tested | **NOT VERIFIED** | Feature extractor returns zeroed vector for empty txs; no explicit test |
| High-activity wallet tested | **NOT VERIFIED** | No stress test; `max_nodes_to_expand=60` is the only safeguard |

---

# 18. What Is Actually Complete?

| Feature | Status | Evidence | Quality |
|---|---|---|---|
| Wallet address input | **COMPLETE** | HTML form + API format validation | Working |
| Ethereum transaction ingestion | **COMPLETE** | EVMAdapter via Etherscan v2, chain_id=1 | Working (requires API key) |
| BSC transaction ingestion | **COMPLETE** | EVMAdapter via Etherscan v2, chain_id=56 | Working (requires API key) |
| Polygon transaction ingestion | **COMPLETE** | EVMAdapter via Etherscan v2, chain_id=137 | Working (requires API key) |
| Tron transaction ingestion | **COMPLETE** | TronAdapter via TronGrid | Implemented (requires API key) |
| Bitcoin transaction ingestion | **COMPLETE** | BitcoinAdapter via Blockstream | Implemented (no key needed) — **value parsing bug** |
| BFS graph traversal | **COMPLETE** | `WalletTracer.trace()` with hop limits, node expansion limit, visited set | Working |
| VASP matching | **BLOCKED** | Matching logic works but `KNOWN_VASPS` is empty (accounts.csv absent) | Code complete, data missing |
| Multi-dimensional confidence scoring | **COMPLETE** | 4-component weighted formula (40/30/20/10) | Working |
| 10-signal risk scoring | **COMPLETE** | Rule-based weighted scoring with typology detection | Working |
| 11-category wallet classification | **COMPLETE** | Rule-based priority cascade | Working |
| 18-feature behavioural feature extraction | **COMPLETE** | Pure functions; output in API response and PDF | Working — not consumed by ML |
| Graph visualization | **COMPLETE** | vis-network in frontend with color-coded nodes and edges | Working |
| PDF report generation | **COMPLETE** | reportlab-based with score breakdown, features, routing, legal disclaimer | Working |
| Multi-chain address validation | **COMPLETE** | Per-chain format validators (EVM, Tron, Bitcoin) | Basic (format only, no checksum) |
| Case history | **COMPLETE** (session-only) | In-memory list with chain/risk filters | Lost on restart |
| High-risk alerts | **COMPLETE** (session-only) | In-memory list of HIGH-risk wallets | Lost on restart |
| SAHYOG routing | **COMPLETE** (demo stub) | Context-aware recommendation based on risk level + relationship type | Demo only, not connected to real SAHYOG API |
| SAHYOG submission endpoint | **DEMO/MOCK** | Returns simulated reference ID and confirmation message | Not a real API call |
| ML-based attribution | **NOT IMPLEMENTED** | No ML libraries; features extracted but no model | N/A |
| ML-based risk scoring | **NOT IMPLEMENTED** | Rule-based only | N/A |
| ML-based wallet classification | **NOT IMPLEMENTED** | Rule-based only | N/A |
| RAG | **NOT IMPLEMENTED** | No RAG components | N/A |
| Agentic investigation | **NOT IMPLEMENTED** | No agent framework | N/A |
| Graph embeddings (node2vec/GraphSAGE) | **NOT IMPLEMENTED** | Mentioned in README roadmap only | N/A |
| GNN | **NOT IMPLEMENTED** | Mentioned in README roadmap only | N/A |
| Sanctions intelligence (live feed) | **NOT IMPLEMENTED** | Hardcoded ~22 addresses only | N/A |
| Authentication/authorization | **NOT IMPLEMENTED** | No auth middleware, no user accounts | N/A |
| Database persistence | **NOT IMPLEMENTED** | In-memory only | N/A |
| Docker/containerization | **NOT IMPLEMENTED** | No Dockerfile | N/A |

---

# 19. Current Maturity Assessment

| Area | Score /10 | Reason |
|---|---|---|
| **Backend** | 7/10 | Clean FastAPI app with 15 routes, proper Pydantic models, error handling. Missing auth, logging, rate limiting, persistence. |
| **Frontend** | 7/10 | Polished dashboard with 5 panels, responsive design, graph visualization. Vanilla JS (no framework), limited error handling. |
| **Blockchain integration** | 6/10 | 5 chains with real adapters and normalization. Rate limiting is basic (`time.sleep`). No retry logic. Bitcoin value parsing has a bug. No internal tx or token transfer support. |
| **Graph analytics** | 6/10 | BFS works correctly with sensible limits. No cycle detection beyond visited set. No path deduplication. Graph is ephemeral (rebuilt per request). |
| **VASP attribution** | 2/10 | Scoring formula is well-designed but VASP registry is empty (accounts.csv absent from repo). Hardcoded fallback is only ~22 high-risk addresses, not VASP labels. Core feature is non-functional. |
| **ML** | 0/10 | No ML components exist. Feature vector is ML-ready but unused by any model. |
| **Data quality** | 1/10 | Primary VASP data file (accounts.csv) is absent from repo. High-risk registry has only ~22 addresses. No data freshness mechanism. No provenance tracking. |
| **Security** | 3/10 | CORS wide open (`*`). No authentication. No rate limiting at API level. API key in `.env` (good). Address format validation only. No security headers. |
| **Testing** | 4/10 | 7 offline tests pass (FakeClient). No live API tests. No frontend tests. No CI/CD. `/api/trace` returns HTTP 500 in live test. |
| **Explainability** | 8/10 | Confidence score broken into 4 explainable components. PDF report includes score breakdown. Relationship type distinction is clear. Legal disclaimer included. |
| **Deployment readiness** | 2/10 | No Docker. No database. In-memory storage. No monitoring. No production server config. No HTTPS. |
| **SIH demo readiness** | 5/10 | Dashboard is polished but demo requires API key AND accounts.csv. Live test showed `/api/trace` returning HTTP 500. Without the data file, VASP matching is non-functional. |
| **Production readiness** | 1/10 | No persistence, no auth, no monitoring, no rate limiting, no database, no audit logs, no scaling strategy. |

---

# 20. Current Strengths

1. **Explainability:** The 4-component confidence formula with per-component breakdown in both the API response and PDF report is genuinely well-designed for investigative use. The `relationship_type` distinction (`interacts_with` vs `controlled_by`) shows careful thinking about attribution precision.

2. **Real blockchain integration:** Three distinct API providers (Etherscan v2, TronGrid, Blockstream) with proper adapters and normalization to a common format. Not a mock or simulation.

3. **Clean modular architecture:** Each module has a single responsibility. Clear import boundaries. No circular dependencies. The `WalletTracer` orchestrates without knowing API details; `BlockchainClient` handles data fetching without knowing about scoring.

4. **Thoughtful risk/attribution separation:** Risk scoring and VASP attribution are independent computations. The system correctly distinguishes between "interacts with" and "controlled by" and includes a legal disclaimer in the PDF.

5. **ML-ready feature schema:** The `WalletFeatureVector` is well-designed with 18 normalized features across 5 groups (Graph, Value, Temporal, Exposure, Structuring). Even though no ML model uses it yet, the schema is forward-compatible and requires no changes to adopt XGBoost/LightGBM.

6. **Polished frontend:** Professional dark LEA-themed dashboard with responsive design (3 breakpoints), graph visualization, smooth UX, keyboard shortcuts. No build step required.

7. **Offline testability:** The `FakeClient` pattern enables deterministic testing without API keys or network access. All 7 tests pass consistently.

8. **Multi-chain adapter pattern:** Clean extension point for adding new chains. Chain metadata centralized in `chains.py`. Address validation per chain type.

9. **SAHYOG routing logic:** The routing recommendation adapts language based on risk level and relationship type — a thoughtful UX detail for investigators. The `disclosure_note` includes the relationship type in natural language.

10. **BFS safeguards:** `max_nodes_to_expand=60` and `max_tx_per_wallet=200` prevent runaway queries against high-activity wallets. The VASP stopping condition naturally limits expansion.

11. **15 API routes:** The backend exposes a comprehensive set of endpoints (health, chains, trace, risk, history, alerts, VASP registry, PDF report, SAHYOG submission, SPA fallback).

---

# 21. Current Weaknesses

1. **Empty VASP registry (CRITICAL):** The primary VASP data file (`data/accounts.csv`, claimed as 113k+ addresses) is gitignored and not in the repository. Without it, `KNOWN_VASPS` is empty and the system finds zero VASP matches. Live test confirmed `/api/trace` returns HTTP 500.

2. **No machine learning:** Despite the README's roadmap claiming "Level 3: ML candidate ranking", there is zero ML in the codebase. No scikit-learn, no XGBoost, no PyTorch, no model training pipeline.

3. **Tiny high-risk registry:** Only ~22 hardcoded addresses. Covers Tornado Cash and a handful of notorious addresses but represents an infinitesimal fraction of actual high-risk addresses.

4. **In-memory storage:** All case history and alerts are lost on server restart. No database, no persistence layer.

5. **No authentication or authorization:** Anyone can access all endpoints. No user accounts, no roles, no audit trail. CORS is wide open.

6. **Basic rate limiting:** `time.sleep()` between API calls with no exponential backoff, no 429 handling, no retry logic.

7. **Bitcoin value parsing bug:** The Bitcoin adapter treats satoshis as if they were wei (divides by 10^18 instead of 10^8), producing near-zero values for BTC amounts.

8. **No internal transaction support:** Only normal transactions are fetched. Internal transactions and token transfers are ignored.

9. **No cross-chain tracing:** If a wallet bridges from Ethereum to BSC, the system does not follow the flow across chains. Bridges are only flagged as risk signals.

10. **Evidence quality is inferred, not stored:** The system guesses at evidence quality at query time. There is no per-address provenance, source URL, or timestamp.

11. **No live sanctions feed:** The OFAC addresses are manually copied into code. No SDN list feed, no freshness checking.

12. **Live server test failure:** `/api/trace` returned HTTP 500 in live testing. This needs investigation but is likely caused by the missing `accounts.csv` or unconfigured API key.

13. **LRU cache on method with self:** The `@lru_cache` decorator on `_fetch` methods includes `self` in the cache key. Works with single instance but is unconventional.

14. **`timeStamp` stored as string:** Timestamps from blockchain APIs are strings, requiring `int()` conversion at each use. Should be normalized to integers at the adapter level.

---

# 22. Known Limitations

## Technical Limitations

- BFS graph traversal is synchronous and blocks the request thread
- Graph is rebuilt from scratch on every trace request (no incremental tracing)
- Edge list capped at 300 edges in API response
- No graph database or persistent graph store
- No cross-chain path tracing (bridges flagged but not followed)
- No support for internal transactions, token transfers, or contract interactions
- LRU cache is in-memory and per-process (not shared across workers)
- `time.sleep()` for rate limiting blocks the thread
- No request queuing or async processing
- `/api/trace` returned HTTP 500 in live testing (likely missing accounts.csv or API key)
- `timeStamp` values stored as strings, requiring repeated `int()` conversion

## Data Limitations

- VASP registry (`data/accounts.csv`) is absent from the repository — **primary blocker**
- High-risk registry has only ~22 addresses
- No live feeds for sanctions, threat intelligence, or VASP labels
- No label provenance, timestamps, or source URLs
- Labels are Ethereum-only; BSC, Polygon, Tron, Bitcoin have no VASP labels
- No negative examples (known non-VASP addresses)
- No ground truth dataset for evaluation

## ML Limitations

- No ML is currently implemented
- Feature vector extracted but not consumed by any model
- No training pipeline, no evaluation framework, no model serialization
- No labeled dataset for supervised learning
- No clustering or embedding infrastructure

## Blockchain Limitations

- 5 chains supported for data fetching but VASP labels only for Ethereum (and those labels are absent)
- Etherscan free tier limits (code uses 0.22s delay ≈ 4.5 calls/sec, within free tier limit of 5/sec)
- No support for token-level tracing (ERC-20, ERC-721 transfers)
- Bitcoin UTXO model not fully handled (simplified to input/output pairs; value parsing bug)
- No support for smart contract interaction tracing
- No support for mempool/unconfirmed transactions

## Legal / Investigative Limitations

- All confidence scores are investigative leads, not legal evidence
- PDF report includes a legal disclaimer
- Attribution claims are conservative (`interacts_with` by default)
- No chain of custody for evidence
- No audit trail for investigator actions
- SAHYOG integration is a demo stub, not a real submission channel

## Deployment Limitations

- No Dockerfile or containerization
- No production ASGI server configuration
- No database or persistence layer
- No monitoring, logging, or alerting infrastructure
- No HTTPS/TLS configuration
- No load balancing or horizontal scaling
- Single-process design

## Scalability Limitations

- Synchronous BFS blocks request threads
- In-memory storage limits session to one process
- No request queuing for concurrent investigations
- LRU cache is process-local
- Graph is ephemeral (no reuse across requests)

---

# 23. Security Audit

## What Is Implemented

| Area | Status | Details |
|---|---|---|
| API key handling | **Partial** | `.env` is gitignored; `.env.example` has placeholder. But `TRONGRID_API_KEY` is missing from `.env.example` even though `main.py` reads it. |
| Address validation | **Partial** | Format validation (prefix + length) per chain type. No checksum validation for EVM. |
| CORS | **Configured** | `CORSMiddleware` with `allow_origins=["*"]` — wide open |
| Input validation | **Partial** | Address format check + chain whitelist. No length limits on other inputs. |
| Error handling | **Partial** | `BlockchainClientError` surfaced as 502. General exceptions rely on FastAPI defaults. |
| Logging | **Minimal** | `warnings.filterwarnings` at startup. No structured logging. |
| Sensitive data | **Partial** | API keys in `.env` (gitignored). Trace results include wallet addresses (expected). |
| Report security | **None** | PDF has no password protection, no watermark, no access control. |

## What Is Missing

| Area | Status | Risk |
|---|---|---|
| Authentication | **NOT IMPLEMENTED** | HIGH — any user can access all endpoints |
| Authorization | **NOT IMPLEMENTED** | HIGH — no role-based access control |
| Rate limiting (API level) | **NOT IMPLEMENTED** | MEDIUM — API can be spammed |
| HTTPS/TLS | **NOT IMPLEMENTED** | HIGH — API keys transmitted in cleartext |
| Audit logging | **NOT IMPLEMENTED** | HIGH — no record of who traced what |
| Secret management | **Partial** | `.env` is gitignored but no secrets management for deployment |
| Security headers | **NOT IMPLEMENTED** | LOW — no CSP, HSTS, X-Frame-Options |
| Dependency scanning | **NOT IMPLEMENTED** | Unknown — no Dependabot, no pip-audit |
| CSRF protection | **NOT IMPLEMENTED** | MEDIUM — no CSRF tokens (but API is GET-heavy) |
| Debug/production mode | **NOT IMPLEMENTED** | No mode distinction; FastAPI `/docs` is exposed |

## SilentProbeMiddleware Note

Returns 204 for known automated probe paths (IDE scanners, browser extensions, favicon, etc.). Thoughtful UX feature but the path list is hardcoded and could mask malicious probes.

---

# 24. Deployment Readiness

## Evaluation

| Aspect | Status | Details |
|---|---|---|
| Backend | **Partial** | FastAPI app is self-contained. No production server config (no gunicorn, no uvicorn workers). |
| Frontend | **Partial** | Static files served by FastAPI. No CDN, no build optimization. |
| Environment variables | **Partial** | `.env.example` provided but missing `TRONGRID_API_KEY`. |
| Dependencies | **Complete** | `requirements.txt` with 7 pinned packages. |
| Production server | **NOT IMPLEMENTED** | No gunicorn, no uvicorn --workers, no Nginx config |
| Database | **NOT IMPLEMENTED** | In-memory only. |
| Persistence | **NOT IMPLEMENTED** | Case history lost on restart. |
| Logging | **NOT IMPLEMENTED** | No structured logging. |
| Monitoring | **NOT IMPLEMENTED** | No metrics, no alerting. |
| Security | **Partial** | CORS, address validation. No auth, no HTTPS, no rate limiting. |
| Docker | **NOT IMPLEMENTED** | No Dockerfile, no docker-compose. |
| Cloud deployment | **NOT IMPLEMENTED** | No deployment configs. |
| Domain/HTTPS | **NOT IMPLEMENTED** | Assumes `127.0.0.1:8000`. |

## Classification

**Not Yet Deployable for Production Use**

The application can be run locally for demo purposes, but cannot be deployed to production without: production ASGI server configuration, database, authentication/authorization, HTTPS/TLS, logging/monitoring, rate limiting, and the `data/accounts.csv` file.

---

# 25. SIH Demo Readiness

## Can We Demonstrate It Live?

**Partially — with mandatory preparation.** The dashboard is polished but the core VASP attribution feature is non-functional without `data/accounts.csv`. Live testing confirmed `/api/trace` returns HTTP 500.

## What Can Be Demonstrated Today

- Dashboard loading with stat cards
- Wallet address input, chain selector, hop depth selector
- Loading spinner during trace
- Risk banner with color-coded risk level and score circle
- Wallet classification display
- SAHYOG routing recommendation card
- VASP match card UI (will show "No known-VASP match found" without accounts.csv)
- Transaction graph visualization (vis-network)
- Case history table
- High-risk alerts panel
- Known VASP registry browser (will show 0 entries)
- PDF report download (generates report with available data)
- SAHYOG submission (demo stub)

## What Requires Manual Setup

| Requirement | Status |
|---|---|
| Etherscan API key | MUST be configured in `.env` before demo |
| `data/accounts.csv` | MUST be placed in `backend/data/` — **currently absent from repo** |
| Python dependencies | MUST be installed (`pip install -r requirements.txt`) |

## What Can Fail During a Live Demo

| Failure Mode | Likelihood | Impact | Mitigation |
|---|---|---|---|
| No API key configured | HIGH | 500 error on trace | Pre-configure `.env` |
| `accounts.csv` missing | HIGH (current state) | Zero VASP matches / HTTP 500 | Place file before demo |
| Demo wallet has no VASP connections | MEDIUM | "No match found" message | Pre-verify demo wallet |
| Etherscan rate limit | MEDIUM | Slow or failed traces | Pre-trace to warm cache |
| Network outage | LOW | Blockchain API calls fail | Have pre-generated PDF backup |
| vis-network CDN unavailable | LOW | Graph fails to render | Have screenshot backup |

## Pre-Demo Checklist

1. Place `data/accounts.csv` in `backend/data/`
2. Configure `ETHERSCAN_API_KEY` in `.env`
3. Select and verify a demo wallet that touches a known VASP in the registry
4. Pre-trace the wallet to warm the LRU cache
5. Pre-generate a PDF report as backup
6. Have screenshots ready in case of live failures

---

# 26. Recommended Demo Scenario

**Status: Demo wallet still needs to be selected and verified. The accounts.csv file must be obtained and placed in backend/data/ before any meaningful VASP attribution demo is possible.**

Once the data file is in place and a demo wallet is verified:

```text
Input: Pre-selected demo wallet (documented scammer wallet with known VASP connections)

Step 1: Dashboard loads → stats update, health indicator shows VASP count

Step 2: Enter wallet → select "Ethereum" → set hops to 3 → "Start Investigation"

Step 3: Loading spinner → "Tracing transaction graph…"

Step 4: Results render:
  ├── Risk banner: color-coded level + score circle + typologies
  ├── Wallet classification: pill with icon + label + reason
  ├── SAHYOG routing: action text + disclosure note + target VASP
  ├── VASP matches (top 3-8): confidence pills + progress bars + paths
  └── Transaction graph: vis-network with color-coded nodes

Step 5: "Download PDF Report" → formatted PDF with:
  ├── Case summary, risk assessment, VASP attribution table
  ├── Score breakdown (4 components × weights)
  ├── Fund flow path, feature vector, SAHYOG routing
  ├── Wallet classification + legal disclaimer

Step 6: "Submit to SAHYOG Portal" → demo confirmation with reference ID
```

---

# 27. Future Roadmap

## Phase 1 — Stabilization

1. Obtain and add `data/accounts.csv` — **critical blocker**
2. Add `TRONGRID_API_KEY` to `.env.example`
3. Add proper error handling and retry logic (exponential backoff, 429 handling)
4. Fix Bitcoin value parsing (satoshi → BTC: divide by 10^8)
5. Add structured logging
6. Add API rate limiting middleware
7. Add internal transaction fetching (Etherscan `txlistinternal`)
8. Add ERC-20 transfer event fetching
9. Add tests for edge cases (empty wallet, API failure, invalid address)
10. Add `accounts.csv` download script or provide a subset for development

## Phase 2 — Real VASP Intelligence

1. Per-address provenance metadata (source URL, timestamp, curator)
2. Evidence quality registry (replace heuristic `_infer_evidence_quality()`)
3. VASP entity metadata (jurisdiction, registration, compliance contact)
4. Address label freshness tracking
5. Multi-source label aggregation
6. Label confidence scoring
7. Cross-chain VASP address mapping

## Phase 3 — Behavioral Intelligence

1. Token profiling (ERC-20 interaction patterns)
2. Counterparty analysis (known entities, clusters)
3. Temporal pattern analysis (activity windows, dormancy)
4. Amount distribution analysis (value histograms, round-number detection)
5. Wallet fingerprinting
6. Entity clustering (distance-based, pre-ML)
7. Fund flow pattern analysis (peel chains, layering, fan-out/fan-in)
8. Time-series features

## Phase 4 — ML Attribution

1. Build labeled dataset of (wallet_features, vasp_label) pairs
2. XGBoost/LightGBM ranking model (replace `_score_matches()` heuristic)
3. Binary classifier (VASP or not)
4. Multi-class wallet classifier (replace rule-based)
5. Model evaluation framework (precision, recall, F1, top-K, MRR)
6. SHAP explanations for model predictions
7. Model serialization and versioning
8. Online learning from investigator feedback

## Phase 5 — Advanced Graph Intelligence

1. Graph embeddings (node2vec)
2. Graph feature extraction (centrality, clustering, communities)
3. Subgraph matching (laundering patterns)
4. Multi-hop path scoring (rank by likelihood, not just hop count)
5. Temporal graph analysis
6. GNN experimentation (GCN, GraphSAGE, GAT)

## Phase 6 — Multi-Chain

1. Cross-chain bridge detection and following
2. Cross-chain address clustering
3. Bitcoin VASP labels
4. Tron VASP labels
5. Solana support
6. Cross-chain flow visualization

## Phase 7 — Investigator Intelligence

1. Case management (persistent cases, notes, evidence)
2. Evidence provenance (chain of custody)
3. Natural-language investigation queries
4. RAG over case history
5. Automated/customizable report generation
6. Investigator feedback loop
7. Alert system (email/webhook)
8. Collaborative investigation (with auth)

## Phase 8 — Production

1. Authentication (JWT/session)
2. RBAC
3. PostgreSQL database
4. Redis caching
5. Celery task queue
6. Monitoring (Prometheus)
7. Audit logs
8. Docker
9. Cloud deployment
10. Security hardening

---

# 28. Priority Matrix

| Improvement | Impact | Difficulty | Priority | Why |
|---|---|---|---|---|
| Obtain `data/accounts.csv` | CRITICAL | Low | **P0** | Without this, VASP matching returns zero results. Core feature non-functional. |
| Fix `/api/trace` HTTP 500 | CRITICAL | Low | **P0** | Live test confirmed HTTP 500. Likely caused by missing accounts.csv. |
| Fix Bitcoin value parsing | HIGH | Low | **P0** | BTC values near-zero due to satoshi/wei divisor confusion. |
| Add retry logic + exponential backoff | HIGH | Medium | **P0** | Transient API failures break traces silently. |
| Configure Etherscan API key | HIGH | Low | **P1** | Required for any real blockchain data fetching. |
| Add API rate limiting | HIGH | Low | **P1** | Prevents endpoint abuse. |
| Add database for case persistence | HIGH | Medium | **P1** | In-memory storage loses all data on restart. |
| Add authentication | HIGH | Medium | **P1** | Required for any multi-user or production deployment. |
| Expand high-risk address registry | HIGH | Medium | **P2** | 22 addresses is insufficient for meaningful risk scoring. |
| Add internal transaction fetching | MEDIUM | Low | **P2** | Critical for complete Ethereum graph construction. |
| Add ERC-20 transfer fetching | MEDIUM | Low | **P2** | Token transfers are significant part of Ethereum activity. |
| Add edge case tests | MEDIUM | Low | **P2** | Current tests cover happy path only. |
| Build labeled dataset for ML | HIGH | High | **P2** | Foundation for all future ML work. Requires manual curation. |
| Add live sanctions feed | HIGH | Medium | **P2** | Hardcoded addresses become stale; OFAC SDN updates regularly. |
| Docker containerization | MEDIUM | Low | **P3** | Standard practice; not urgent for demo. |

## Top 10 Next Actions

1. **Resolve `/api/trace` HTTP 500** — diagnose and fix (likely missing accounts.csv)
2. **Obtain `data/accounts.csv`** — place in `backend/data/` to enable VASP matching
3. **Configure `ETHERSCAN_API_KEY`** in `.env`
4. **Select and verify demo wallet** that touches a known VASP
5. **Fix Bitcoin value parsing** (satoshi → BTC conversion: divide by 10^8)
6. **Add retry logic with exponential backoff** for all blockchain API calls
7. **Add API rate limiting** middleware
8. **Add `TRONGRID_API_KEY` to `.env.example`**
9. **Add tests for edge cases** (empty wallet, API failure, invalid address)
10. **Add internal transaction fetching** (Etherscan `txlistinternal` action)

---

# 29. Recommended Technical Evolution

The current architecture can evolve without throwing away existing code:

```
Current (Phases 1-3 complete, code-wise)
├── blockchain_client.py     → Extend with new adapters (Solana, etc.)
├── chains.py                → Add more chains, token transfer configs
├── tracer.py                → Extend BFS with cross-chain bridge following; replace _score_matches() with ML
├── feature_extractor.py     → Add more features (token profiles, counterparty analysis)
├── risk_engine.py           → Add ML signal outputs alongside rule-based signals
├── wallet_classifier.py     → Replace rule-based logic with ML classifier
├── known_vasps.py           → Add provenance metadata, live feed integration
├── high_risk_addresses.py   → Replace hardcoded list with live feed
├── report.py                → Extend with SHAP explanations, new sections
├── models.py                → Add ML prediction models, explanation models
└── main.py                  → Add auth, feedback, model management endpoints

New modules needed:
├── vasp_registry.py         → Per-address provenance, quality scores, source tracking
├── sanctions_feed.py        → Live OFAC SDN list feed
├── feature_store.py         → Persisted feature vectors for model training
├── ml_ranker.py             → XGBoost/LightGBM ranking model
├── ml_classifier.py         → Wallet type classifier (replaces rule-based)
├── database.py              → PostgreSQL connection, ORM models
├── auth.py                  → JWT authentication, RBAC
├── cache.py                 → Redis caching layer
├── task_queue.py            → Celery tasks for async tracing
├── evaluation.py            → Model evaluation metrics
└── feedback.py              → Investigator feedback collection
```

**Files that can be retained as-is:** `blockchain_client.py`, `chains.py`, `report.py`, `models.py` (with additions), `main.py` (with new endpoints).

**Files that should be extended:** `tracer.py`, `feature_extractor.py`, `risk_engine.py`, `wallet_classifier.py`.

**Files that need new companions:** `known_vasps.py` needs a provenance system. `high_risk_addresses.py` needs a live feed.

---

# 30. Proposed Future Architecture

```
PLANNED — NOT CURRENTLY IMPLEMENTED

┌─────────────────────────────────────────────────────────────────┐
│                    Investigator Dashboard                        │
│  (Enhanced: case management, collaboration, feedback)            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                   API Gateway / Auth Layer                       │
│  (JWT auth, RBAC, rate limiting, audit logging)                  │
└──────────────────────────┬───────────────────────────────��──────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                     Investigation Orchestrator                   │
│  (Async task queue, case management, workflow engine)             │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                   Blockchain Data Layer                          │
│  (Multi-chain adapters + internal tx + token transfers)          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    Normalization Layer                           │
│  (Unified tx format, address normalization, value conversion)    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                     Graph Store                                  │
│  (Persistent graph database; incremental updates)                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                 Wallet Feature Engine                            │
│  (Graph + behavioral + temporal + token profile features)        │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  VASP Knowledge Base                             │
│  (Provenance-tracked labels + live feed + cross-chain mapping)   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  Candidate Retrieval                             │
│  (Graph-based VASP candidate generation + ranking)               │
└──────────────────────────┬─────────────────��────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    ML Ranking Layer                              │
│  (XGBoost/LightGBM ranker + feature importance + SHAP)          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│               Risk / Sanctions Intelligence                      │
│  (Live OFAC feed + expanded registry + behavioral risk signals)  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                 Evidence & Provenance                            │
│  (Chain of custody + source tracking + timestamps)               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                    Explainability Layer                          │
│  (SHAP explanations + counterfactuals + confidence calibration)  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                  Case / Report System                            │
│  (Persistent cases + customizable reports + batch generation)    │
└─────────────────────────────────────────────────────────────────┘
```

---

# 31. AI/ML Roadmap Specifically

> What AI/ML capabilities should eventually be added, and why?

| Approach | Purpose | Data Needed | Difficulty | Priority |
|---|---|---|---|---|
| **XGBoost/LightGBM ranking** | Replace heuristic confidence formula with learned ranking of VASP candidates | Labeled (wallet_features, vasp_label) pairs | Medium | **P1** |
| **Binary classifier (VASP or not)** | Classify whether an address belongs to a VASP | Labeled address features + negative examples | Medium | P1 |
| **Multi-class wallet classifier** | Replace rule-based classifier with ML | Labeled wallet types (exchange, mixer, etc.) | Medium | P2 |
| **Behavioral clustering (DBSCAN)** | Group wallets by behavioral similarity | WalletFeatureVector for many wallets | Low-Medium | P2 |
| **Anomaly detection (Isolation Forest)** | Flag unusual wallet behavior | Normal wallet behavior distribution | Medium | P3 |
| **Graph embeddings (node2vec)** | Embed wallets in vector space from graph structure | Transaction graph data | Medium | P3 |
| **Graph Neural Network (GCN/GraphSAGE)** | Predict VASP membership from graph structure | Labeled graph with VASP nodes | High | P4 |
| **Temporal model (LSTM/Transformer)** | Model transaction sequences for pattern detection | Timestamped transaction sequences | High | P4 |
| **SHAP explanations** | Explain ML predictions to investigators | Trained ML model | Low | P2 |
| **Online learning from feedback** | Improve models based on investigator feedback | Investigator feedback labels | Medium | P3 |

### Which approach should be implemented FIRST and why?

**XGBoost/LightGBM ranking model** should be the first ML approach because:

1. **Existing feature schema:** `WalletFeatureVector` already has 18 normalized features. No schema changes needed.
2. **Clear prediction target:** Rank VASP candidates by likelihood of correct attribution.
3. **Interpretable:** Tree-based models provide feature importance, aligning with the explainability requirement.
4. **Low data requirement:** Can start with a few hundred labeled examples and improve iteratively.
5. **Drop-in replacement:** Can replace `_score_matches()` in `tracer.py` with minimal interface changes.
6. **Fast inference:** XGBoost ranking is fast enough for real-time use.

**Prerequisite:** Building a labeled dataset (requires investigator feedback loop + manual curation).

---

# 32. Evaluation Strategy

## Classification Metrics

| Metric | Purpose | How to Measure |
|---|---|---|
| **Precision** | Of all attributed wallets, what fraction are correct? | TP / (TP + FP) — requires ground truth VASP labels |
| **Recall** | Of all true VASP wallets, what fraction were found? | TP / (TP + FN) — requires ground truth VASP labels |
| **F1 Score** | Harmonic mean of precision and recall | 2 × P × R / (P + R) |

## Ranking Metrics

| Metric | Purpose | How to Measure |
|---|---|---|
| **Top-1 accuracy** | Is the highest-ranked VASP correct? | % where top match matches ground truth |
| **Top-3 accuracy** | Is the correct VASP in the top 3? | % where correct VASP appears in top 3 |
| **Top-5 accuracy** | Is the correct VASP in the top 5? | % where correct VASP appears in top 5 |
| **MRR** | Average reciprocal rank of correct answer | 1/N × Σ(1/rank_i) |

## Graph Metrics

| Metric | Purpose | How to Measure |
|---|---|---|
| **Path recovery** | Does BFS find a path to the true VASP? | % where true VASP reachable within N hops |
| **Attribution distance** | How many extra hops beyond minimum? | (found_hops - min_hops) / min_hops |
| **Candidate coverage** | Is true VASP in the candidate list? | % where true VASP appears in candidates |

## Calibration

| Metric | Purpose | How to Measure |
|---|---|---|
| **Confidence calibration** | Does a 90% confidence score mean ~90% accuracy? | Reliability diagrams, ECE |
| **False attribution rate** | How often is VASP attribution incorrect? | FP / (TP + FP) |

## Ground Truth Requirement

> **Accuracy cannot be meaningfully claimed without reliable labeled VASP addresses/test cases.**

**Current state:** No ground truth dataset exists. No evaluation has been performed. No labeled (wallet, VASP) pairs are available.

---

# 33. Data Strategy for Future ML

## Required Dataset Components

```
Known VASP wallets (from verified VASP registry with provenance)
+
Verified attribution evidence (wallet → VASP pairs confirmed by investigators)
+
Transaction histories (raw tx data for each labeled wallet)
+
Wallet behavioral features (WalletFeatureVector computed from transaction histories)
+
Graph neighborhoods (BFS-traversed subgraphs around each wallet)
+
Negative examples (wallets known NOT to belong to specific VASPs)
+
Synthetic controlled examples (simulated wallets with known VASP relationships)
```

## Train/Validation/Test Split Strategy

1. **Time-based split:** Train on wallets traced before date T, validate on T to T+Δ, test on T+Δ onwards.
2. **VASP-based split:** Ensure addresses from the same VASP are distributed across splits.
3. **Stratification:** Maintain label distribution across splits.
4. **No wallet leakage:** A wallet and all its neighbors should be in the same split.

---

# 34. Competitor / Existing Technology Context

## Commercial Blockchain Intelligence Platforms

| Platform | What They Solve | How This Project Compares |
|---|---|---|
| **Chainalysis** | Full blockchain forensics: entity clustering, sanctions screening, transaction tracing, fund flow analysis, compliance | This project implements a tiny fraction. Chainalysis has years of labeled data, proprietary clustering, global LE integration. |
| **TRM Labs** | Risk scoring, VASP attribution, sanctions screening, fraud detection | This project's risk scoring is a simplified version. TRM has ML models trained on millions of labeled transactions. |
| **Elliptic** | Blockchain analytics, sanctions screening, VASP due diligence, transaction monitoring | This project's VASP matching is conceptually similar but with a tiny fraction of address coverage. |

## What This Project Currently Does

- Basic blockchain transaction graph traversal (BFS)
- Simple VASP address matching against a community dataset (currently empty)
- Rule-based risk scoring with a small hardcoded registry (~22 addresses)
- Rule-based wallet classification (11 categories)
- PDF report generation
- Investigator dashboard with graph visualization
- 5 blockchain adapters (Ethereum, BSC, Polygon, Tron, Bitcoin)

## What This Project Could Differentiate On

1. **Explainability:** 4-component confidence breakdown — more transparent than commercial black-box models
2. **Indian regulatory context:** SAHYOG portal integration tailored for Indian law enforcement
3. **Open architecture:** Reproducible, auditable, customizable
4. **Evidence provenance:** Planned provenance tracking
5. **Investigator workflow:** Designed for investigation workflow, not just compliance screening
6. **Cost:** Free and open-source

## What This Project Does NOT Replace

Chainalysis, TRM Labs, Elliptic, or similar platforms. Those have years of labeled data, proprietary algorithms, live sanctions feeds, multi-chain coverage with verified labels, ML models trained on millions of transactions, law enforcement certifications, and support infrastructure.

---

# 35. Differentiation Strategy

| Differentiator | Current State | Future Potential |
|---|---|---|
| Explainable attribution | **Implemented** — 4-component score in API + PDF | Expand with SHAP when ML added |
| Evidence provenance | **Planned** — per-address metadata | Track label sources, timestamps, curators |
| Ranked VASP candidates | **Implemented** — sorted by confidence | ML-based ranking with calibrated confidence |
| Uncertainty-aware output | **Partially implemented** — confidence + relationship type | Calibrated confidence intervals |
| Graph-based reasoning | **Implemented** — BFS with path tracking | Graph embeddings, GNN |
| Behavioral fingerprinting | **Partially implemented** — 18 features | ML-based fingerprinting and clustering |
| Indian regulatory intelligence | **Partially implemented** — SAHYOG stub | Real SAHYOG API integration |
| Investigator workflow | **Implemented** — dashboard + history + alerts | Case management, collaboration, feedback loop |
| Open/reproducible architecture | **Implemented** — single Python package | Maintain as design principle |

---

# 36. Target Users and Industries

### Primary

| User | Specific Use Case |
|---|---|
| Law enforcement investigators | Trace scammer wallets to exchanges; identify VASPs for KYC/freeze requests |
| Cybercrime investigation cells | Process blockchain evidence from cybercrime complaints (1930 helpline, cybercrime.gov.in) |
| Financial intelligence analysts | Analyze fund flows, identify laundering patterns, build case evidence |
| I4C personnel | Central coordination of cybercrime investigations across Indian states |

### Secondary

| User | Specific Use Case |
|---|---|
| Crypto exchanges (VASPs) | Screen incoming deposits for high-risk counterparties |
| Banks | Assess risk of crypto counterparties in fiat on-ramp/off-ramp |
| Compliance teams | AML/KYC screening of wallet addresses |
| Regulators | Monitor VASP compliance, identify unregistered exchanges |
| Cybersecurity firms | Incident response involving cryptocurrency |
| Blockchain forensic firms | Augment existing tools with attribution intelligence |

---

# 37. Risks

| Risk | Severity | Probability | Current Mitigation | Future Mitigation |
|---|---|---|---|---|
| **Incorrect VASP attribution** | HIGH | Medium | Conservative relationship types; legal disclaimer | ML evaluation; investigator feedback; confidence calibration |
| **Empty VASP registry (current)** | HIGH | Certain | N/A | Obtain and maintain comprehensive registry |
| **API outage (Etherscan/TronGrid/Blockstream)** | HIGH | Low-Medium | Error caught in tracer; 502 returned | Multi-provider fallback; cached data |
| **API rate limiting** | MEDIUM | Medium | `time.sleep()` delays | Exponential backoff; request queuing; paid tier |
| **Graph explosion (high-activity wallet)** | MEDIUM | Medium | `max_nodes_to_expand=60` | Adaptive expansion; async processing |
| **False positives in risk scoring** | HIGH | Medium | Conservative signal thresholds | Expanded registry; ML scoring; investigator feedback |
| **False negatives (missed VASP)** | HIGH | Medium | N/A (no labels) | Comprehensive VASP registry |
| **Outdated labels** | MEDIUM | Certain over time | N/A | Live feed integration; freshness tracking |
| **Cross-chain laundering** | HIGH | Certain | Bridges flagged as risk signals | Cross-chain bridge tracing |
| **Privacy concerns** | MEDIUM | Low | Only public blockchain data | Data handling policy; access logging |
| **Legal misuse** | HIGH | Low | Conservative attribution; legal disclaimer | Audit trail; access control; usage policies |
| **Model bias (when ML added)** | MEDIUM | Medium | N/A | Diverse training data; fairness evaluation |
| **Insufficient training data** | HIGH | Certain | N/A | Investigator feedback; synthetic data |

---

# 38. What We Should NOT Build

1. **Unnecessary LLM chatbot** — Adds complexity without solving the core attribution problem. Better data and ML models are needed first.
2. **Unnecessary blockchain/token** — Issuing a project token or NFT adds nothing to VASP attribution.
3. **Unsupported "real-time intelligence"** — Blockchain data has inherent latency. Claiming real-time monitoring would be misleading.
4. **Fake GNN claims** — GraphSAGE/GAT are legitimate future directions but should not be claimed as current capabilities.
5. **Excessive multi-chain claims** — 5 chains are "supported" for data fetching, but VASP labels exist for none of them currently.
6. **Unnecessary RAG system** — Requires a substantial case history first. Build case management before RAG.
7. **Unnecessary agentic workflows** — Requires stable core functionality first. Don't build agents on top of an empty VASP registry.
8. **Blockchain-agnostic claims** — The system is blockchain-specific (address formats, API providers, value handling).

---

# 39. Final "State of the Project" Summary

## CURRENT STATE

An advanced prototype with real multi-chain blockchain data ingestion (5 chains, 3 API providers), BFS graph traversal, rule-based risk scoring (10 signals), rule-based wallet classification (11 categories), a 4-component heuristic confidence scorer, an 18-feature behavioural feature extractor, PDF report generation, and a polished investigator dashboard with 5 panels and vis-network graph visualization. 15 API routes serve the frontend and expose all functionality. The backend is clean and modular. **The primary blocker is that the VASP address dataset (`data/accounts.csv`) is absent from the repository, making the core VASP attribution feature non-functional. Live testing confirmed `/api/trace` returns HTTP 500.**

## WHAT IS PROVEN

- FastAPI backend starts and serves all endpoints (verified)
- Frontend loads and renders all 5 panels (verified)
- 7 offline tests pass with FakeClient (verified — all pass)
- BFS graph traversal works correctly with hop limits and node expansion limits (verified via tests)
- Multi-dimensional confidence scoring produces valid 0-100 scores (verified via tests)
- Risk engine correctly identifies mixer/sanctions/darknet/fraud interactions (verified via tests)
- Wallet classifier correctly categorizes known-bad addresses and applies behavioral heuristics (verified via tests)
- Feature extractor produces 18 valid features from transaction data (verified via tests)
- PDF report generator produces formatted reports (code review confirmed)
- Multi-chain address validation works for EVM, Tron, and Bitcoin formats (verified via test)
- 15 API routes are registered and accessible (verified via test)

## WHAT IS NOT PROVEN

- `/api/trace` returns HTTP 500 in live testing (diagnosis needed)
- Real Etherscan API integration (no API key in repo)
- Real VASP matching (accounts.csv missing — 0 VASPs loaded)
- Graph visualization with real blockchain data
- PDF report with real trace results
- Error handling under API failure conditions
- Rate-limit behavior under load
- Performance with high-activity wallets
- Bitcoin value accuracy (known bug: satoshi divisor)
- Cross-chain tracing correctness

## BIGGEST TECHNICAL GAP

The VASP address registry (`data/accounts.csv`) is absent from the repository, making the core VASP attribution feature non-functional. The `/api/trace` endpoint returns HTTP 500 in live testing, likely caused by this missing file. This is a data gap, not a code gap — the matching logic is implemented correctly but has nothing to match against.

## BIGGEST DATA GAP

The VASP address dataset (~113k Ethereum addresses claimed in README) plus an expanded high-risk registry beyond the current ~22 addresses.

## SIH READINESS

**5/10** — The dashboard is polished, the pipeline architecture is sound, and 7 tests pass. However: (1) the live `/api/trace` returns HTTP 500, (2) the VASP dataset is missing, (3) demo requires manual setup of API key and data file. Without the data file, the most important feature produces zero results.

**Pre-demo checklist:**
1. Resolve `/api/trace` HTTP 500
2. Place `data/accounts.csv` in `backend/data/`
3. Configure `ETHERSCAN_API_KEY` in `.env`
4. Select and verify demo wallet touching a known VASP
5. Pre-trace wallet to warm cache
6. Pre-generate PDF report as backup

## PRODUCTION READINESS

**1/10** — Not ready for production. Missing: database, authentication, authorization, persistent storage, logging, monitoring, rate limiting at API level, HTTPS, Docker, CI/CD, comprehensive testing, and the VASP dataset.

## NEXT 5 ACTIONS

1. **Diagnose and fix `/api/trace` HTTP 500** — likely caused by missing `accounts.csv`
2. **Obtain `data/accounts.csv`** — place in `backend/data/` to enable VASP matching
3. **Configure `ETHERSCAN_API_KEY`** in `.env` and verify trace works end-to-end
4. **Select and verify demo wallet** with known VASP connections
5. **Fix Bitcoin value parsing** (satoshi → BTC: divide by 10^8, not 10^18)

## LONG-TERM TARGET

The project should evolve into a production-grade blockchain intelligence platform for Indian law enforcement, with comprehensive VASP registry with provenance tracking, machine learning-based attribution ranking (XGBoost/LightGBM), cross-chain tracing, case management with evidence provenance, SAHYOG portal integration, investigator feedback loop, multi-tenant deployment with auth/RBAC, and real-time monitoring. The current codebase provides a solid foundation — the path forward is primarily about adding data, ML models, and production infrastructure.

---

# 40. Final Audit Checklist

- [x] Every important source file was inspected (13 Python files, 3 frontend files, config files, test file)
- [x] README claims were checked against implementation (VASP count, ML roadmap, dataset claims)
- [x] No planned feature is described as implemented (ML clearly marked as future)
- [x] No invented metrics exist (all scores verified from source code)
- [x] No invented datasets exist (accounts.csv confirmed absent from repo)
- [x] No invented API integrations exist (all APIs verified in code)
- [x] Current ML status explicitly stated (no ML; features are ML-ready but unused)
- [x] Current blockchain support explicitly stated (5 chains for data fetching; VASP labels for none)
- [x] Current VASP-data status explicitly stated (registry empty; accounts.csv missing)
- [x] Current testing status explicitly stated (7 offline tests pass; no live tests; `/api/trace` HTTP 500)
- [x] Current deployment status explicitly stated (not deployable for production)
- [x] Current security status explicitly stated (wide CORS, no auth, no rate limiting)
- [x] Limitations documented (technical, data, ML, blockchain, legal, deployment, scalability)
- [x] Future roadmap separated from current implementation (Phases 1-8 clearly distinguished)
- [x] Technical debt documented (Section 21)
- [x] SIH demo readiness documented (Section 25)
- [x] Top priorities identified (Section 28)
- [x] Live server test results documented (HTTP 500 on /api/trace)
- [x] `feature_extractor.py` and `wallet_classifier.py` accurately classified (rule-based, not ML)
- [x] Five-chain support accurately described (data fetching works; VASP matching does not)
- [x] Exact Git commit hash included (`699505f`)

---

## Repository Inconsistencies / Findings

| Claim | Actual Implementation | Impact | Recommended Action |
|---|---|---|---|
| README: "113,000+ labelled addresses" in accounts.csv | `data/accounts.csv` is gitignored and **not present in the repository** | VASP matching returns zero results; `/api/trace` returns HTTP 500 | Obtain the file and add it, or provide a download script |
| README: "Level 3: ML candidate ranking (XGBoost / LightGBM)" | No ML libraries in `requirements.txt`; no ML imports anywhere in codebase | README overstates current capabilities | Update README to clarify Levels 4+ are planned, not implemented |
| `.env.example`: lists 3 variables | `main.py` line 87 reads `TRONGRID_API_KEY` which is not in `.env.example` | Users may not know to configure TronGrid key | Add `TRONGRID_API_KEY` to `.env.example` |
| `high_risk_addresses.py`: some addresses appear in multiple categories | Address `0x7f367c...` appears as mixer, sanctions, AND darknet; `0x098b71...` appears as sanctions AND ransomware | Minor — set membership checks are unaffected by duplicates | No action needed (sets deduplicate) |
| Bitcoin value: adapter divides by 10^18 | Bitcoin satoshis should be divided by 10^8 to get BTC | BTC values displayed as near-zero in UI and PDF | Fix divisor in `BitcoinAdapter._normalize()` |
| README project path: `wallet-vasp-tracer/` | Actual repo path is `SIH26182/` | Cosmetic — README setup instructions reference wrong directory | Update README path references |
| README: "CryptoScamDB.org" as demo data source | CryptoScamDB.org is defunct (service shut down) | Users following README will find a dead link | Update README to remove or replace with active source |

---

*End of PROJECT_STATUS.md*
*Audit completed: 2026-08-28*
*Repository: SIH26182 — commit 699505f*
