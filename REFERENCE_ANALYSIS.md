# Technical Reference Analysis: SIH26182 Reference Project

**Target Platform:** CryptoGuard AI — AI-Powered Blockchain Investigation & VASP Attribution Platform  
**Problem Statement:** SIH26182 (“Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers through Blockchain Intelligence APIs”)  
**Reference Repository:** `https://github.com/subhranshuparh/SIH26182`  
**Date of Analysis:** September 2026  

---

## 1. Existing Architecture Overview

The reference repository is a monolithic Python application combining a FastAPI backend with a static HTML/CSS/JavaScript single-page application (SPA):

```
├── backend/
│   ├── main.py                 # FastAPI application, route definitions, probe middleware
│   ├── tracer.py               # BFS multi-hop graph traversal engine
│   ├── blockchain_client.py    # Multi-chain API adapters (Etherscan v2, TronGrid, Blockstream)
│   ├── feature_extractor.py    # Graph, temporal, and exposure feature extraction
│   ├── wallet_classifier.py    # Heuristic wallet classification (hot wallet, deposit, mixer, etc.)
│   ├── risk_engine.py          # Rule-based 10-signal risk scoring engine
│   ├── known_vasps.py          # In-memory dictionary for VASP addresses (loads accounts.csv or demo)
│   ├── high_risk_addresses.py  # Hardcoded sets of sanctions, mixers, bridges, ransomware
│   ├── demo_fixture.py         # Static synthetic 3-hop trace response for offline testing
│   ├── models.py               # Pydantic v2 schemas for API requests and responses
│   ├── report.py               # PDF investigation report generator using ReportLab
│   ├── chains.py               # Chain configurations (Ethereum, BSC, Polygon, Tron, Bitcoin)
│   └── static/                 # Frontend assets
│       ├── index.html          # Plain HTML structure
│       ├── css/style.css       # Custom dark CSS
│       └── js/
│           ├── app.js          # Monolithic client logic (~880 lines)
│           └── vis-network.min.js # Network visualization library
```

---

## 2. Technical Stack Identification

| Layer | Reference Project Technology | Evaluation |
|---|---|---|
| **Frontend** | Vanilla HTML5, Vanilla CSS, Vanilla JavaScript, Vis-network 9.1.2 | Lightweight, zero build-step requirement, but monolithic `app.js` and lacks modular tabs, side panels, and copilot interaction. |
| **Backend** | Python 3.11+ / FastAPI 0.115 / Starlette | Fast, modern async ASGI framework; excellent for rapid prototyping and REST APIs. |
| **Database** | **None** (In-memory Python lists: `CASE_HISTORY`, `HIGH_RISK_ALERTS`) | **Critical limitation**: Data is lost on server restart. No persistent case management, user auditing, or saved evidence. |
| **Blockchain APIs** | Etherscan v2 multi-chain API, TronGrid REST, Blockstream.info | Good multi-chain coverage (EVM + Tron + BTC), but fragile when API keys are unconfigured. |
| **VASP Matching** | In-memory hash map lookup + BFS traversal | Simple string matching against `KNOWN_VASPS`. Dependent on `accounts.csv`. |
| **Risk Scoring** | Weighted linear combination of 10 signals + multi-signal boost | Transparent, explainable, and non-black-box. Good foundation. |
| **Reporting** | ReportLab 4.x/5.x PDF Builder | Clean PDF output with tabular formatting. |
| **Authentication** | **None** | No auth, no roles, open access. |

---

## 3. What We Will Retain Conceptually

1. **Multi-hop Graph Traversal (BFS Approach):**
   The Breadth-First Search concept to find the shortest and most direct fund paths between a suspect wallet and known VASP deposit clusters is mathematically sound and investigator-friendly.
2. **Multi-Dimensional Attribution Scoring:**
   The 4-factor scoring model:
   $$\text{Attribution Confidence} = 0.40 \times \text{Proximity} + 0.30 \times \text{Interaction} + 0.20 \times \text{Recency} + 0.10 \times \text{Evidence Quality}$$
   is explainable and avoids arbitrary "black box" claims.
3. **Transparent Risk Engine:**
   Scoring risk based on observable typologies (Mixers, Sanctions, Rapid Velocity, Structuring, Peel Chains) with clear signal weights rather than opaque neural predictions.
4. **Distinction Between Interaction and Control:**
   Legally and forensically, asserting that a wallet *interacts with* a VASP is distinct from asserting it is *controlled by* or *owned by* that VASP. We will maintain and strengthen this forensic distinction.
5. **Local Vis.js Transaction Graph Visualization:**
   Retain local bundling of `vis-network` to guarantee full offline execution without external CDN dependencies.

---

## 4. What We Will Redesign

1. **Brand Identity & UI/UX:**
   - **Completely replace** the original presentation and branding ("SAHYOG Intelligence" / SIH26182 placeholder) with **CryptoGuard AI: AI-Powered Blockchain Investigation & VASP Attribution Platform**.
   - Redesign into a desktop-first, professional cybersecurity investigation console featuring clean cards, high-contrast dark mode, and an 8-tab comprehensive Investigation Workspace:
     `Overview` | `Transaction Graph` | `Wallet Intelligence` | `VASP Attribution` | `Risk Analysis` | `Timeline` | `Evidence` | `Report`.
2. **Interactive Transaction Graph & Node Side-Panel:**
   - Instead of static tooltips, clicking any node in the graph opens a dedicated **Inspector Drawer** showing counterparty statistics, incoming/outgoing volume, detected flags, and hop distance.
3. **VASP Dataset & Indian Regulatory Relevance:**
   - The reference repo's `demo_vasps.csv` improperly categorized ERC-20 token contracts (`WETH`, `USDT`, `DAI`) and liquidity pools (`Uniswap V2 Router`, `Aave V3 Pool`) as "VASPs".
   - We will redesign the dataset to only include real Virtual Asset Service Providers, incorporating Indian FIU-IND registered reporting entities (e.g., WazirX/Zanmai Labs, CoinDCX/Neblio Technologies, ZebPay, CoinSwitch Kuber, Mudrex) alongside major international exchanges (Binance, Coinbase, Kraken, OKX, Bybit, KuCoin).
4. **VASP Attribution "Explain Attribution" Path:**
   - Provide a step-by-step visual path:
     $$\text{Suspect Wallet} \xrightarrow{\text{tx}_1} \text{Hop 1 Intermediary} \xrightarrow{\text{tx}_2} \text{VASP Hot Wallet}$$
     with exact transaction hashes, amounts, timestamps, block numbers, and natural language rationale.

---

## 5. What We Will Implement Ourselves (New Capabilities)

1. **Persistent SQLite Database (`cryptoguard.db`):**
   - Implement relational storage for `Investigation`, `Wallet`, `Transaction`, `VASP`, `EvidenceItem`, `TimelineEvent`, and `AuditLog` so cases persist across sessions.
2. **Investigation Copilot (AI Assistant):**
   - An interactive copilot widget that answers investigator questions about the current case using deterministic rule-based analysis (with pluggable LLM support via environment variable).
3. **India-Focused Cybercrime Response Workflow:**
   - Structured NCRP / 1930 Cybercrime complaint integration workflow:
     $$\text{Complaint} \to \text{Suspect Wallet} \to \text{Attributed VASP} \to \text{Section 91 CrPC / BNSS Notice Generator} \to \text{FIU-IND KYC Requisition Form}$$
4. **Interactive Evidence Locker:**
   - Allow investigators to triage evidence items (`Relevant`, `Reviewed`, `Needs Verification`), filter by counterparty, and export chain-of-custody logs.
5. **Interactive Investigation Timeline:**
   - Chronological breakdown of fund movements with rapid velocity detection and layering alert callouts.
6. **High-Fidelity Deterministic Demo Mode:**
   - A multi-hop scenario featuring 1 suspect wallet, 6 intermediary wallets, peel chain layering, mixer interaction, and 2 distinct VASP candidates (Binance & CoinDCX/WazirX).
7. **Comprehensive Exportable PDF Report:**
   - Redesigned with CryptoGuard AI branding, investigator credentials, chain of custody, and legal notice attachments.

---

## 6. Known Limitations of the Reference Project

1. **No Data Persistence:** Server restart wipes all past investigations.
2. **Missing Accounts Dataset:** `accounts.csv` (113k rows) was not included in git; fallback had only 10 items (including non-VASP tokens).
3. **Static Directory Path Bug:** Running `main.py` from project root crashed because `directory="static"` was relative instead of using `os.path.dirname(__file__)`.
4. **No Hop-by-Hop Explanation:** The UI did not explain why an attribution occurred or show transaction-level hop hops.
5. **No Evidence Management:** Evidence was read-only with no review status or triage capability.
6. **No AI Copilot / Case Chat:** No natural-language query capability over case evidence.
7. **Unimplemented SAHYOG Actions:** SAHYOG submission was a stub that generated a fake random ID without legal request templates or actionable forms.

---

*This analysis provides the architectural roadmap for constructing CryptoGuard AI.*
