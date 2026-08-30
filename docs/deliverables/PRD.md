# Product Requirements Document
## Wallet-to-VASP Attribution System (SIH-26182)

**Version:** 2.0  |  **Date:** 2026-08-30

---

## 1. Problem Statement

Law enforcement agencies investigating cryptocurrency-related crimes need tools to:

1. Trace the flow of funds across blockchain addresses
2. Identify which Virtual Asset Service Providers (VASPs) are involved
3. Assess the risk level of suspect wallets with explainable scores
4. Generate court-admissible investigation reports
5. Route cases to appropriate enforcement portals (SAHYOG)

Current tools are either expensive commercial products, require deep technical
expertise, or lack transparency in scoring methodology.

SIH-26182 addresses this gap with a transparent, explainable, open-source
blockchain analytics prototype built for the Smart India Hackathon.

---

## 2. Target Users

| User | Role | Primary Need |
|------|------|-------------|
| Investigator | Law enforcement analyst | Trace wallets, assess risk, find VASP links |
| Judge | Judicial officer | Review evidence, understand scoring methodology |
| Technical Reviewer | System evaluator | Verify formula correctness, data sources |
| Developer | Maintainer | Extend blockchains, add signals, improve scoring |

---

## 3. User Stories

### US-1: As an Investigator, I want to trace a wallet address

So that I can see all addresses it transacts with and identify potential VASPs.

### US-2: As an Investigator, I want to see a risk score with breakdown

So that I can prioritize which wallets to investigate first and justify the score.

### US-3: As a Judge, I want to see the scoring formula

So that I can understand and verify how the risk score was calculated.

### US-4: As an Investigator, I want to generate a PDF report

So that I can include it in case documentation and court submissions.

### US-5: As an Investigator, I want SAHYOG routing recommendations

So that I know which enforcement action to take for each risk level.

### US-6: As a Reviewer, I want to see data sources cited

So that I can verify the intelligence datasets used for attribution.

---

## 4. Feature Prioritization

### P0 -- Must Have (Core)

- Multi-chain wallet trace (Ethereum, BSC, Polygon, Tron, Bitcoin)
- Risk scoring with transparent formula and visible weights
- Score breakdown cards in UI
- VASP attribution with multi-dimensional confidence scoring
- Wallet classification (9 types)
- SAHYOG routing recommendations
- PDF report generation
- Transaction graph visualization

### P1 -- Should Have

- Scoring methodology visible in UI (permanent formula card)
- Scoring methodology in PDF report
- Case history sidebar
- Health check endpoint
- 12 unit tests covering core functions

### P2 -- Nice to Have (Future)

- Multi-language support
- Batch investigation (multiple wallets)
- Export to CSV/JSON
- Dark mode
- User authentication
- PostgreSQL database for case persistence
- ML-based ranking (Level 3 roadmap)

---

## 5. Design Decisions

### Decision 1: No black-box ML in risk scoring

**Rationale:** Judges and investigators must be able to understand and verify
every score. A transparent formula with auditable weights is more defensible
in court than a neural network or random forest.

### Decision 2: All intelligence data embedded in code

**Rationale:** No external data files, no CSV dependencies, no database.
The system is self-contained and portable. Any Python developer can run it.

### Decision 3: Vanilla frontend (no build step)

**Rationale:** Investigators should be able to run the system without npm,
webpack, or any JavaScript build tooling.

### Decision 4: Scoring formula visible everywhere

**Rationale:** The formula is displayed in the UI card, the PDF report,
and the source code. Maximum transparency for all stakeholders.

---

## 6. Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Trace success rate | > 95% | API calls returning valid graph data |
| VASP detection rate | > 80% | Known VASPs correctly identified |
| Score consistency | 100% | Same wallet produces identical score across runs |
| PDF generation time | < 5s | Time from click to download start |
| UI load time | < 2s | Time to interactive on localhost |
| Unit test pass rate | 100% | All 12 tests passing |

---

## 7. Demo Test Wallets

Copy-paste these addresses into the investigation form at http://localhost:8080

### Known VASPs (Expected: LOW risk, VASP match)

1. `0x28C6c06298d514Db089934071355E5743bf21d60` -- Binance Hot Wallet
2. `0x503828976D22510aad0201ac7EC88293211D23Da` -- Coinbase
3. `0x2910543af39aba0cd09dbb2d50200b3e800a63d2` -- Kraken Exchange

### Mixers (Expected: HIGH risk, score 100, no VASP match)

4. `0x722122df12d4e14e13ac3b6895a86e84145b6967` -- Tornado Cash Proxy
5. `0xa160cdab225685da1d56aa342ad8841c3b53f291` -- Tornado Cash 10 ETH Pool
6. `0x910cbd523d972eb0a6f4cae4618ad62622b39dbf` -- Tornado Cash 1 ETH Pool

### Sanctioned / Ransomware (Expected: HIGH risk, score 100, no VASP match)

7. `0x098b716b8aaf21512996dc57eb0615e2383e2f96` -- Ronin Bridge Hacker (Lazarus)
8. `0xd882cfc523d972eb0a6f4cae4618ad62622b39dbf` -- Blender.io (OFAC sanctioned mixer)
9. `0x901bb9583b24d97e995513c6778dc6888ab6870e` -- DPRK Lazarus Group

### Suspicious Behavior (Expected: MEDIUM risk, score ~54)

10. `0xd8da6bf26964af9d7eed9e03e53415d37aa96045` -- Structuring/Smurfing wallet

---

## 8. How to Run

```bash
# 1. Clone the repo
git clone https://github.com/subhranshuparh/SIH26182.git
cd SIH26182

# 2. Install dependencies
pip install -r backend/requirements.txt

# 3. Set API key
export ETHERSCAN_API_KEY=your_key_here

# 4. Start server
cd backend
uvicorn main:app --reload --port 8080

# 5. Open browser
# http://localhost:8080
```