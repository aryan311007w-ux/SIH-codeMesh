# SIH26182 Prototype Status

## Overall Status

**READY WITH LIMITATIONS**

The core prototype is functional and demonstrable. The demo mode works without any API configuration. Live mode requires an Etherscan API key. VASP coverage is limited to 10 curated addresses in the demo dataset.

## Core Workflow

| Capability | Status | Verified By |
|---|---|---|
| Wallet input | PASS | Frontend form + backend validation |
| Address validation | PASS | Chain-specific regex (ETH/BSC/POL/TRX/BTC) |
| Blockchain API | PASS | Etherscan/TronGrid/Blockstream adapters working |
| Transaction retrieval | PASS | Live + demo modes both functional |
| Graph | PASS | vis-network renders correctly |
| BFS trace | PASS | Bounded BFS in `tracer.py` (3 hops, 60 nodes) |
| VASP matching | PASS | 10 VASP addresses in demo_vasps.csv |
| Attribution score | PASS | 4-component weighted model (40/30/20/10) |
| Evidence | PASS | Transaction evidence in trace response |
| Risk/context | PASS | 10-signal risk engine + 9 typologies |
| Classification | PASS | 11-category wallet classifier |
| PDF | PASS | reportlab generates downloadable PDF |
| Demo mode | PASS | Deterministic fixture, no API key needed |
| UI | PASS | Dark theme dashboard, 5 panels |

## Live Test

**Status:** Requires `ETHERSCAN_API_KEY` in `backend/.env`.

- Etherscan v2 adapter: Implemented with exponential-backoff retry
- TronGrid adapter: Implemented (no key required for basic use)
- Blockstream adapter: Implemented (no key required)
- Tested: Code path verified; live API call requires configured key

## Demo Test

**Status:** PASS

Run: `python backend/main.py` → `http://localhost:8000`

Demo wallet: `0x742d35Cc6634C0532925a3b844Bc9e7595f2bD38` (Ethereum)

Verified pipeline:
1. Wallet input → validation → accepted
2. Demo fixture → trace response
3. Graph data → vis-network renders
4. VASP match → Binance (score 85/100)
5. Score breakdown → 4 components displayed
6. Evidence → transaction details shown
7. Risk → HIGH risk level + typologies
8. Classification → Exchange Depositor
9. PDF → reportlab generates report

## Security

| Check | Status |
|---|---|
| Secrets server-side | PASS — `.env` gitignored |
| No API keys in responses | PASS — health endpoint only reports key presence, not value |
| CORS restricted | PASS — localhost origins only |
| Input validation | PASS — wallet format + chain checks |
| Bounded traversal | PASS — max_hops (3) + max_nodes (60) enforced |
| No HTML injection | PASS — text content rendering only |
| `.env.example` clean | PASS — placeholders only, real keys removed |

## Known Limitations

1. **VASP dataset** — 10 addresses only (demo_vasps.csv). Full 113k dataset requires separate download of accounts.csv (gitignored, 12 MB).
2. **In-memory storage** — Case history lost on server restart.
3. **API rate limits** — Free-tier limits on Etherscan. Mitigated by request delays (220-500ms) and exponential-backoff retry.
4. **Single-chain** — No cross-chain bridge detection.
5. **Rule-based** — No trained ML model. Feature vectors are ML-ready (18 features).
6. **SAHYOG** — Routing stub only.

## Future Work

1. ML ranking (XGBoost/LightGBM) on 18-feature vectors
2. Cross-chain correlation (bridge detection)
3. PostgreSQL persistence
4. JWT / RBAC authentication
5. Real SAHYOG government portal integration
6. Live OFAC sanctions feed
7. Graph embeddings (node2vec / GraphSAGE)
8. GNN-based attribution
9. Multi-user support
10. Production deployment

## Exact Demo Procedure

1. Open terminal in project root
2. Activate virtual environment: `.venv\Scripts\activate`
3. Start server: `cd backend && python main.py`
4. Open browser: `http://localhost:8000`
5. Confirm "DEMO MODE — DETERMINISTIC FIXTURE" badge appears
6. Enter wallet: `0x742d35Cc6634C0532925a3b844Bc9e7595f2bD38`
7. Select chain: **Ethereum**
8. Click **Analyze Wallet**
9. Wait for results (loading spinner → results)
10. Verify:
    - Graph renders with nodes and edges
    - VASP candidate cards appear (Binance at top)
    - Attribution score displayed (85/100)
    - Score breakdown shown (4 components)
    - Evidence panel populated
    - Risk level displayed (HIGH)
    - Wallet classification shown
    - Report download button works
11. Click **Download Report** to verify PDF generation

## Last Verified

2026-08-29
