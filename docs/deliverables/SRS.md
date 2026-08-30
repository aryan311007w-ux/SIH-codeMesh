# Software Requirements Specification
## Wallet-to-VASP Attribution System (SIH-26182)

**Version:** 2.0  |  **Date:** 2026-08-30  |  **Team:** I4C / SIH 2025-26

---

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements for
the Wallet-to-VASP Attribution System (SIH-26182), a blockchain analytics
prototype that traces cryptocurrency wallet transaction graphs, assesses risk
levels, and attributes fund flows to Virtual Asset Service Providers (VASPs)
for law enforcement investigative use.

### 1.2 Scope

The system performs: (1) Multi-hop transaction graph tracing across 5
blockchains, (2) Wallet risk scoring (0-100) with transparent weighted signal
aggregation, (3) VASP attribution with multi-dimensional confidence scoring,
(4) SAHYOG portal routing recommendations, (5) PDF investigation report
generation, and (6) Interactive transaction graph visualization.

### 1.3 Audience

Investigators, judges, technical reviewers, and system evaluators.

---

## 2. System Architecture

### Backend (FastAPI, Python)

| Module | Purpose |
|--------|---------|
| main.py | API endpoints, case history, health check |
| tracer.py | Core BFS graph tracer (multi-chain) |
| risk_engine.py | 10-signal risk scoring engine |
| wallet_classifier.py | Wallet type classification |
| feature_extractor.py | ML-ready feature vectors |
| blockchain_client.py | Etherscan / TronGrid API client |
| high_risk_addresses.py | Intelligence registries |
| known_vasps.py | VASP registry (33 addresses) |
| report.py | PDF report generation (ReportLab) |
| models.py | Pydantic response schemas |
| chains.py | Chain configuration |

### Frontend

Vanilla HTML/CSS/JS with interactive graph, score breakdown cards, risk
banner, SAHYOG routing, PDF download, and case history sidebar.

### Supported Blockchains

| Chain | Explorer API |
|-------|-------------|
| Ethereum | Etherscan |
| BSC | Etherscan (BSC) |
| Polygon | Etherscan (Polygon) |
| Tron | TronGrid |
| Bitcoin | Blockchair |

---

## 3. Functional Requirements

### FR-1: Wallet Trace

Accept wallet address, blockchain, and hop depth. Fetch all transactions via
blockchain explorer API. Perform BFS outward through counterparty wallets.
Return complete transaction graph (nodes, edges, total tx count).

### FR-2: VASP Attribution

Identify nearest VASP using 4-component confidence scoring:
- Graph Proximity (40%): max(0, 100 - hops*25) + min(15, (paths-1)*5)
- Interaction Strength (30%): (volume_to_vasp / total_volume) * 100
- Temporal Recency (20%): 100 * exp(-0.02 * days_since_last_tx)
- Evidence Quality (10%): 100/65/35 (high/medium/low)
Relationship types: interacts_with, controlled_by, laundered_through.

### FR-3: Risk Scoring

Formula:

    final_score = sum(signal_score * signal_weight) + boost
    boost = min(20, (n_signals - 1) * 5)
    # clamped to [0, 100]

| Signal | Weight | Trigger Condition |
|--------|--------|-------------------|
| self_is_high_risk | 1.00 | Wallet in known flagged registry |
| sanctions_link | 0.95 | Direct tx with OFAC-sanctioned address |
| ransomware_link | 0.90 | Transaction with known ransomware address |
| darknet_link | 0.85 | Transaction with darknet marketplace |
| fraud_link | 0.70 | Transaction with fraud-linked address |
| mixer_interaction | 0.75 | Funds sent to/received from mixer/tumbler |
| structuring | 0.50 | Many near-identical tx values (layering) |
| peel_chain | 0.40 | Linear single-hop chain pattern |
| cross_chain_bridge | 0.30 | Interaction with bridge/swap contract |
| high_velocity | 0.25 | Abnormally high transaction rate |

Risk Levels: HIGH (score >= 60), MEDIUM (score >= 25), LOW (score < 25)

### FR-4: Wallet Classification

Types: vasp_hot_wallet, vasp_deposit_wallet, mixer, ransomware, sanctioned,
darknet_market, bridge, defi, unknown_wallet.

### FR-5: SAHYOG Routing

HIGH risk + VASP match: URGENT freeze/disclosure request.
HIGH risk + no VASP match: URGENT direct law enforcement escalation.
LOW/MEDIUM: Standard disclosure request with VASP details.

### FR-6: PDF Report

Full investigation report: case summary, risk assessment, score breakdown table,
VASP attribution results, wallet feature vector, SAHYOG routing recommendation,
wallet classification, scoring methodology section, legal disclaimer.

### FR-7: Transaction Graph Visualization

Interactive graph with color-coded nodes by wallet type, directed edges, legend.

### FR-8: Case History

Session history of investigated wallets with timestamps.

---

## 4. Non-Functional Requirements

- Trace completion: < 30 seconds for 3-hop depth on Ethereum
- PDF generation: < 5 seconds
- UI response: < 200ms for interactive elements
- Deterministic scoring (identical input produces identical output)
- All signal weights visible and auditable in code and UI
- No black-box ML components in scoring
- API keys configured via environment variables only
- Graceful degradation if blockchain API is unavailable
- CORS restricted to localhost

---

## 5. Data Sources and Dataset References

### 5.1 Blockchain Data APIs (Live Data at Runtime)

| Source | URL | Data Type |
|--------|-----|-----------|
| Etherscan API | https://docs.etherscan.io | ETH/BSC/Polygon transactions, labels |
| TronGrid API | https://developers.tron.network | TRX transactions |
| Blockchair API | https://blockchair.com/api | BTC transactions |

### 5.2 Intelligence Datasets (Embedded in Python Source Code)

All intelligence data is hardcoded in Python files. No external data files or
databases are required at runtime. The system is fully self-contained.

| Registry | File in Repo | Count | Source / Reference |
|----------|-------------|-------|-------------------|
| Known VASPs | backend/known_vasps.py | 33 | Community labels, Etherscan address tags |
| Mixer Addresses | backend/high_risk_addresses.py | 17 | Tornado Cash official addresses, Blender.io |
| Sanctions Addresses | backend/high_risk_addresses.py | 4 | OFAC SDN List (Treasury.gov/public) |
| Ransomware Addresses | backend/high_risk_addresses.py | 3 | Public ransomware tracker databases |
| Darknet Addresses | backend/high_risk_addresses.py | 2 | Community darknet market address lists |
| Fraud Addresses | backend/high_risk_addresses.py | 1 | Public fraud tracking databases |
| Bridge Addresses | backend/high_risk_addresses.py | 8 | Official bridge contract addresses |

### 5.3 Data Storage Locations

- Intelligence registries: Embedded as Python sets/dicts in source code files
- Transaction data: Fetched at runtime from APIs, not persisted to disk
- Case history: In-memory Python list, cleared on server restart
- No database or persistent storage required or used

---

## 6. API Specification

### POST /api/trace

Query params: wallet (required), chain (required), max_hops (optional, default 3)
Returns: Complete trace result with risk, VASP matches, graph, features

### GET /api/health

Returns: status, vasp_count, supported_chains, api_key_status

### GET /api/history

Returns: Session investigation history array

### POST /api/sahyog/submit

Submits investigation result for SAHYOG portal routing

### GET /api/report/pdf

Query params: wallet, chain. Returns: PDF file (application/pdf)

---

## 7. Constraints

- Python 3.8+ backend with FastAPI
- No database required (in-memory session state)
- Etherscan API key required for live blockchain data
- Vanilla frontend (HTML/CSS/JS), no build step
- Risk scores are investigative leads only, not legal evidence
- VASP attribution identifies fund flow relationships, not legal ownership

---

## 8. Acceptance Criteria

- [ ] All 5 blockchains supported with successful traces
- [ ] Risk score formula matches documented weights exactly
- [ ] Score breakdown visible in UI for every investigation
- [ ] PDF report contains scoring methodology section
- [ ] SAHYOG routing recommends correct action for each risk level
- [ ] VASP attribution identifies Binance, Coinbase, Kraken correctly
- [ ] Wallet classification correct for known addresses
- [ ] All 12 unit tests pass
- [ ] App starts with: uvicorn main:app --reload --port 8080
- [ ] UI accessible at http://localhost:8080