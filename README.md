# Wallet-to-VASP Attribution System (SIH-26182)

**Multi-Dimensional Blockchain Intelligence for Attribution of Unknown Cryptocurrency
Wallets to Virtual Asset Service Providers (VASPs)**

Ministry of Home Affairs · I4C · SIH 2026 · Software Category

---

## 1. What this system does

Given a suspicious wallet address from a cybercrime complaint, this system:

1. **Fetches real transaction history** from the blockchain (Ethereum, BSC,
   Polygon, Tron, Bitcoin) using public APIs.
2. **Walks outward through the transaction graph** hop by hop (BFS), following
   money flows to neighbouring wallets.
3. **Scores every VASP candidate** found in the graph using a **multi-dimensional
   attribution model** — not a single hop-distance heuristic.
4. **Classifies the root wallet** into one of ten behavioural archetypes
   (exchange, hot wallet, deposit wallet, mixer, darknet, sanctioned, etc.).
5. **Scores risk** using ten independent signals (mixer interaction, sanctions
   links, ransomware links, structuring, peel chains, high velocity, etc.).
6. **Generates a SAHYOG routing recommendation** — which VASP to send a
   freeze or disclosure request to, and with what urgency.
7. **Presents results on an investigator dashboard** with a visual transaction
   graph and a downloadable PDF case report.

### What it is NOT

This is not a "scammer detector." It does not decide guilt. It assumes a human
(a victim, an investigator, or a scam-report database) has already flagged a
wallet. This tool's job is to trace where funds went and **identify the most
likely VASP relationship** — so investigators can direct a formal KYC/freeze
request to the right exchange.

### Attribution vs. Ownership

The system carefully distinguishes two claims:

| Relationship | Meaning | Evidence Required |
|---|---|---|
| **Interacts with** | A fund-flow path exists between the wallet and the VASP | BFS path discovery |
| **Attributed deposit wallet** | Strong evidence the VASP directly controls this wallet | Hop-1 + >70% of txs toward this VASP + narrow counterparty set |

The weaker claim (`interacts with`) is the correct default. The system only
asserts the stronger claim (`controlled_by`) when structural evidence clearly
supports it.

---

## 2. Architecture

```
                    ┌────────────────────┐
                    │  Unknown Wallet    │
                    └─────────┬──────────┘
                              ↓
                 ┌────────────────────────┐
                 │  Blockchain Data Layer  │
                 │  ETH / BSC / Polygon   │
                 │  Tron / Bitcoin        │
                 └───────────┬────────────┘
                             ↓
              ┌──────────────────────────────┐
              │  Transaction Graph Builder    │
              │  BFS · max_hops · max_nodes  │
              └──────────────┬───────────────┘
                             ↓
       ┌─────────────────────┼──────────────────────┐
       ↓                     ↓                      ↓
 Graph Features       Behavioural Features   Transaction Features
 (hop distance,       (velocity, burst,      (volume, in/out ratio,
  path count,          peel chain,            value concentration,
  counterparties)      structuring)           recency)
       │                     │                      │
       └─────────────────────┼──────────────────────┘
                             ↓
                 ┌────────────────────────┐
                 │  Feature Extractor     │  ← feature_extractor.py
                 │  WalletFeatureVector   │
                 └────────────┬───────────┘
                              ↓
                 ┌────────────────────────┐
                 │  Multi-Dimensional     │
                 │  Confidence Scorer     │  ← tracer.py
                 │  (4-component model)   │
                 └────────────┬───────────┘
                              ↓
              ┌───────────────┼────────────────┐
              ↓               ↓                ↓
        VASP Registry     OFAC/Sanctions   Risk Engine
        (113k+ labels)    High-Risk Intel  (10 signals)
              │               │                │
              └───────────────┼────────────────┘
                              ↓
                 ┌────────────────────────┐
                 │  Attribution Result    │
                 │  relationship_type     │
                 │  evidence_quality      │
                 │  confidence (0-100)    │
                 └────────────┬───────────┘
                              ↓
                 ┌────────────────────────┐
                 │  Investigator Dashboard│
                 │  + SAHYOG Routing      │
                 └────────────┬───────────┘
                              ↓
                    PDF Case Report
```

---

## 3. How the confidence score works

The confidence score (0–100) is computed from **four independent components**,
each scored 0–100, then combined with fixed weights:

```
Confidence =
    40% × Graph Proximity Score
  + 30% × Interaction Strength Score
  + 20% × Temporal Recency Score
  + 10% × Evidence Quality Weight
```

### Component definitions

| Component | Formula | Rationale |
|---|---|---|
| **Graph Proximity** | `max(0, 100 − hops × 25) + min(15, (paths−1) × 5)` | Closer hops and multiple independent paths = stronger link |
| **Interaction Strength** | `(volume sent toward VASP / total traced volume) × 100` | A wallet that sent 80% of its ETH to one exchange is much more strongly attributed than one that touched it with a single 0.001 ETH tx |
| **Temporal Recency** | `100 × e^(−0.02 × days_since_last_tx)` | Recent interactions are stronger attribution evidence; 30-day-old txs score ~55, 6-month-old score ~30 |
| **Evidence Quality** | `100 (high) / 65 (medium) / 35 (low)` | Provenance of the VASP label: OFAC/government = high; community dataset = medium; single unverified source = low |

All four sub-scores are returned in the API response and in the PDF report,
so an investigator can see exactly why a match scored as it did.

---

## 4. Intelligence level / development roadmap

The system is designed as a progressive intelligence stack:

```
Level 1  ✅  Graph traversal (BFS, multi-chain)
Level 2  ✅  Behavioral feature extraction (WalletFeatureVector, 18 features)
Level 3  ✅  Multi-dimensional weighted scoring (4-component confidence model)
Level 4  🔧  ML candidate ranking (XGBoost / LightGBM on WalletFeatureVector)
Level 5  🔧  Wallet clustering / DBSCAN behavioral grouping
Level 6  📋  Graph embeddings (node2vec / GraphSAGE)
Level 7  📋  Multi-chain cross-chain flow analysis
Level 8  📋  Agentic investigation + RAG over case history
```

Levels 1–3 are implemented. Levels 4–8 are the post-demo roadmap.
The feature vector from Level 2 feeds directly into Level 4 without
any schema changes — the ML upgrade is additive.

---

## 5. Project structure

```
wallet-vasp-tracer/
└── backend/
    ├── main.py                  FastAPI app + all API routes
    ├── models.py                Pydantic schemas (VaspMatch, WalletFeatureVector, ...)
    ├── blockchain_client.py     Multi-chain data client (EVM, Tron, Bitcoin)
    ├── chains.py                Chain metadata + address validation
    ├── tracer.py                BFS graph traversal + multi-dimensional scorer
    ├── feature_extractor.py     Wallet behavioural feature vector extractor
    ├── risk_engine.py           10-signal risk scorer + laundering typology detection
    ├── wallet_classifier.py     10-category behavioural wallet classifier
    ├── known_vasps.py           VASP registry loader (113k+ labelled addresses)
    ├── high_risk_addresses.py   OFAC / CISA / FBI threat intelligence registry
    ├── report.py                PDF investigation report generator (reportlab)
    ├── test_tracer.py           Offline unit test (no API key needed)
    ├── requirements.txt
    ├── .env.example
    ├── data/
    │   ├── accounts.csv                      113k+ Ethereum mainnet labelled addresses
    │   └── verified_vasp_addresses.csv.example
    └── static/
        ├── index.html           Investigator dashboard
        ├── css/style.css
        └── js/app.js
```

---

## 6. Setup

### Prerequisites
- Python 3.10+
- A free Etherscan API key: https://etherscan.io/myapikey

### Steps

```bash
cd wallet-vasp-tracer/backend

# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure your API key
cp .env.example .env
# Open .env and paste your ETHERSCAN_API_KEY

# 3. Run the server
uvicorn main:app --reload --port 8000

# 4. Open the dashboard
# Visit http://127.0.0.1:8000
```

### Quick offline test (no API key needed)
```bash
python test_tracer.py
```

---

## 7. ⚠️ Before your SIH demo

The system loads `data/accounts.csv` at startup (113,000+ labelled Ethereum
addresses from the Dune / Etherscan community dataset). For a convincing demo:

1. **Use real documented scam wallets** as input — sources:
   - [Chainabuse.com](https://www.chainabuse.com) — crowd-sourced scam reports
   - [CryptoScamDB.org](https://cryptoscamdb.org) — searchable scam database
   - FIR case numbers with associated wallet addresses

2. **Verify your demo wallet touches a known VASP** by checking it on
   [Etherscan](https://etherscan.io) first — look for "Name Tag" labels on
   counterparties within 3 hops.

3. **Optional: add your own verified VASP addresses** via CSV:
   ```python
   from known_vasps import load_from_csv
   load_from_csv("data/verified_vasp_addresses.csv")
   ```
   Format: `address,name` or the full `accounts.csv` format.

---

## 8. API reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Backend + config status |
| GET | `/api/chains` | List supported blockchains |
| GET | `/api/trace?wallet=0x...&chain=ethereum&max_hops=3` | Run trace, get attribution + risk + graph |
| GET | `/api/risk/{wallet}` | Risk report for a previously traced wallet |
| GET | `/api/history` | Session case history (filterable) |
| GET | `/api/vasps` | View / search VASP registry |
| GET | `/api/alerts/high-risk` | HIGH-risk wallets flagged this session |
| GET | `/api/report/{wallet}` | Download PDF investigation report |
| POST | `/api/sahyog/submit` | SAHYOG portal integration (demo stub) |

Interactive docs: `http://127.0.0.1:8000/docs`

---

## 9. Risk signals (risk_engine.py)

| Signal | Weight | Typology |
|---|---|---|
| Wallet itself is flagged | 1.00 | — |
| Sanctions link (OFAC) | 0.95 | Sanctions Evasion |
| Ransomware link | 0.90 | Ransomware Payment |
| Darknet link | 0.85 | Darknet Activity |
| Fraud-linked wallet | 0.70 | Fraud-Linked Wallet |
| Mixer interaction | 0.75 | Layering via Mixer |
| Structuring / smurfing | 0.50 | Structuring / Smurfing |
| Peel chain pattern | 0.40 | Peel Chain / Linear Layering |
| Cross-chain bridge | 0.30 | Cross-Chain Obfuscation |
| High-velocity tx rate | 0.25 | High-Velocity Rapid Movement |

---

## 10. Known limitations

- **Ethereum-primary**: The VASP dataset (`accounts.csv`) covers Ethereum
  mainnet. BSC, Polygon, Tron, and Bitcoin data fetching works, but label
  coverage is lower. Expanding the label dataset per chain is a post-demo step.
- **Rate limits**: Etherscan's free tier limits calls; `max_nodes_to_expand`
  caps graph traversal to prevent timeouts.
- **Attribution confidence ≠ proof**: All confidence scores are heuristic
  investigative leads. The PDF report carries a legal disclaimer. Formal
  enforcement requires corroboration through official process.
- **In-memory case store**: Session history is lost on server restart. A
  production deployment should swap to a database (PostgreSQL / SQLite).

---

## 11. Suggested SIH pitch structure

1. **Problem** — Investigators receive a scammer's wallet address but cannot
   determine which exchange holds KYC data on the owner. Manual tracing is
   slow and labour-intensive.

2. **Live demo** — Enter a real documented scam wallet. Show the system
   trace it across multiple hops, surface the most likely VASP relationship
   with confidence breakdown, flag laundering typologies, and generate a
   PDF case report — in under 30 seconds.

3. **Architecture** — Walk through the 4-component confidence model. Explain
   why `interaction_strength` catches cases hop distance misses (a wallet that
   touched Binance once with 0.001 ETH is very different from one that sent 90%
   of its funds there).

4. **Intelligence stack** — Explain the Level 1→8 roadmap. The current system
   implements Levels 1–3. The `WalletFeatureVector` from Level 2 feeds directly
   into Level 4 ML ranking without any schema changes.

5. **Deployment path** — Integration with SAHYOG Portal (I4C) for one-click
   freeze/disclosure requests to Indian and international exchanges. Expansion
   to India's National Cybercrime Reporting Portal (cybercrime.gov.in / 1930
   helpline) as a backend intelligence service.

6. **Impact** — Faster VASP attribution → faster legal requests → faster fund
   freezes → higher recovery rates for cybercrime victims.
