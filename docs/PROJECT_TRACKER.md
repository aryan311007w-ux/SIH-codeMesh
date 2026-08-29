# SIH26182 Project Tracker

## Core Prototype

| Item | Status | Evidence | Notes |
|---|---|---|---|
| Wallet input | COMPLETE | Frontend form + `/api/trace` endpoint | Validated, chain-specific |
| Address validation | COMPLETE | Chain-specific regex in backend | Ethereum, BSC, Polygon, TRON, BTC |
| Blockchain API | WORKING | Etherscan/TronGrid/Blockstream adapters | Live mode needs API key |
| Transaction retrieval | WORKING | `blockchain_client.py` | Exponential-backoff retry |
| Graph | COMPLETE | vis-network in frontend | Renders transaction graph |
| BFS trace | COMPLETE | `tracer.py` bounded BFS | Hop-limited, 60-node cap |
| VASP matching | COMPLETE | `known_vasps.py` + demo_vasps.csv | 10 curated addresses |
| Attribution score | COMPLETE | 4-component weighted model | 40/30/20/10 breakdown |
| Score explanation | COMPLETE | Component scores in response | Non-black-box |
| Evidence | COMPLETE | Transaction evidence in trace response | Shown in UI |
| Risk/context | COMPLETE | `risk_engine.py` + `wallet_classifier.py` | 10 signals, 11 types |
| Classification | COMPLETE | 11-category classifier | Rule-based |
| PDF report | COMPLETE | `report.py` + reportlab | Downloadable |
| Demo mode | COMPLETE | `demo_fixture.py` deterministic data | Works without API key |
| UI | WORKING | Vanilla JS dashboard, 5 panels | Polished dark theme |

## Data

| Item | Status | Evidence | Notes |
|---|---|---|---|
| demo_vasps.csv | COMPLETE | 10 curated VASP/exchange addresses | WETH, USDT, USDC, LINK, Uniswap, Aave, DAI, Binance, Coinbase, Kraken |
| accounts.csv | NOT PRESENT | 12 MB, gitignored | 113k+ ETH labels, download separately |
| High-risk registry | COMPLETE | ~33 addresses in code | Mixers, sanctions, ransomware |
| Label provenance | PARTIAL | Demo addresses are well-known | Full provenance requires accounts.csv |

## Backend

| Item | Status | Evidence | Notes |
|---|---|---|---|
| FastAPI app | COMPLETE | `main.py` — 11 endpoints | Running on port 8000 |
| Multi-chain adapters | COMPLETE | 3 adapter classes | EVM, TRON, BTC |
| BFS tracer | COMPLETE | `tracer.py` | Configurable hops + node cap |
| VASP registry | COMPLETE | `known_vasps.py` | Primary + demo fallback |
| Risk engine | COMPLETE | `risk_engine.py` | 10 signals, 9 typologies |
| Wallet classifier | COMPLETE | `wallet_classifier.py` | 11 archetypes |
| Feature extractor | COMPLETE | `behavioral_features.py` | 18 features, ML-ready |
| PDF report | COMPLETE | `report.py` | reportlab |
| Demo fixture | COMPLETE | `demo_fixture.py` | Deterministic offline data |
| Error handling | COMPLETE | Try/except + HTTPException | Safe API errors |
| CORS | COMPLETE | Restricted to localhost | Not open wildcard |
| Input validation | COMPLETE | Wallet format checks | Chain-specific regex |

## Frontend

| Item | Status | Evidence | Notes |
|---|---|---|---|
| Dashboard HTML | COMPLETE | `index.html` | Single-page, dark theme |
| Investigation form | COMPLETE | Wallet input + chain selector | Working |
| Analyze button | COMPLETE | Triggers `/api/trace` | Working |
| Loading state | COMPLETE | Spinner + progress | Working |
| Result display | COMPLETE | VASP cards, score, evidence | Working |
| Graph visualization | COMPLETE | vis-network | Working |
| Score breakdown | COMPLETE | Component scores displayed | 40/30/20/10 |
| Risk/context panel | COMPLETE | Risk level + typologies | Working |
| Classification panel | COMPLETE | Wallet type display | Working |
| Evidence panel | COMPLETE | Transaction evidence | Working |
| Report download | COMPLETE | PDF download button | Working |
| Demo/live indicator | COMPLETE | Mode badge in UI | Distinguishable |
| Error states | COMPLETE | Error messages in UI | Working |
| History panel | COMPLETE | Session case history | Working |
| Alerts panel | COMPLETE | High-risk wallet list | Working |
| VASP reference panel | COMPLETE | Known VASP list | Working |

## Security

| Item | Status | Evidence | Notes |
|---|---|---|---|
| Secrets server-side | COMPLETE | `.env` gitignored, not in responses | Verified |
| Input validation | COMPLETE | Wallet format + chain validation | Chain-specific regex |
| Bounded traversal | COMPLETE | max_hops + max_nodes enforced | Prevents runaway queries |
| Safe error handling | COMPLETE | No stack traces in responses | Generic error messages |
| CORS restricted | COMPLETE | Localhost origins only | Not wildcard |
| No HTML injection | COMPLETE | Text content, no innerHTML with user data | Safe rendering |
| .env.example | COMPLETE | Placeholder only | No real keys |

## Demo

| Item | Status | Evidence | Notes |
|---|---|---|---|
| Demo mode works | COMPLETE | `demo_fixture.py` | No API key needed |
| Demo wallet → trace | COMPLETE | Full pipeline in fixture | Deterministic |
| Demo graph renders | COMPLETE | Pre-built graph data | vis-network |
| Demo VASP match | COMPLETE | Binance (score 85) | In fixture |
| Demo score | COMPLETE | 85/100 with breakdown | 4 components |
| Demo evidence | COMPLETE | Transaction evidence | In fixture |
| Demo risk | COMPLETE | Risk level + typologies | In fixture |
| Demo classification | COMPLETE | Wallet type | In fixture |
| Demo PDF | COMPLETE | Report generation | reportlab |

## GitHub

| Item | Status | Evidence | Notes |
|---|---|---|---|
| Repository | COMPLETE | https://github.com/subhranshuparh/SIH26182 | Existing repo |
| Collaborator access | COMPLETE | Push access confirmed | biswal-prem-5677 |
| No secrets in repo | COMPLETE | `.env` gitignored, no keys in code | Verified |
| Demo data present | COMPLETE | `demo_vasps.csv` in repo | 10 addresses |

## Presentation

| Item | Status | Evidence | Notes |
|---|---|---|---|
| Slide 1 — Title | COMPLETE | `docs/presentation_content.md` | SIH-26182, problem, team |
| Slide 2 — Proposed Solution | COMPLETE | Pipeline + differentiators | 6 steps, 4 differentiators |
| Slide 3 — Technical Approach | COMPLETE | 5-layer architecture | All implemented tech listed |
| Slide 4 — Feasibility | COMPLETE | Works/challenges/mitigations | Realistic, honest |
| Slide 5 — Impact | COMPLETE | Before/after + benefits | Investigator focus |
| Slide 6 — Research | COMPLETE | Real sources + future | Correctly separated |
| Current vs Future | COMPLETE | Capability matrix | Clear distinction |
| Screenshots | PENDING | Need localhost screenshots | Run prototype first |
