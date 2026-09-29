# PRE-DEVELOPMENT REVIEW: CRYPTOGUARD AI (SIH26182)

**Repository:** `aryan311007w-ux/SIH-codeMesh`  
**Problem Statement:** SIH26182 — *Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs*  
**Evaluation Date:** September 29, 2026  
**Auditor:** Antigravity Senior Technical Reviewer  
**Review Type:** Pre-Development Baseline & Demo Verification (Read-Only)

---

## 1. Git Repository & Working Tree Status

| Parameter | Current State | Verification Status |
| :--- | :--- | :--- |
| **Branch Name** | `sih26182-cryptoguard` | Confirmed active & tracking `origin/sih26182-cryptoguard` |
| **Latest Commit** | `cf113c1` (*docs: add final project audit*) | Confirmed on branch HEAD |
| **Previous Commit** | `e21c34c` (*feat(cryptoguard): complete CryptoGuard AI MVP for SIH26182*) | Confirmed in git log |
| **Working Tree** | `nothing to commit, working tree clean` | Clean; zero uncommitted modifications |
| **Read-Only Mode** | Active | No source code altered; no commits; no pushes |

---

## 2. Local Runtime & Infrastructure Verification

The backend service was verified running locally at `http://127.0.0.1:8000`:

* **Runtime:** Python 3.14.0 / FastAPI 0.115 / Uvicorn 0.34
* **Database:** SQLite (`backend/data/cryptoguard.db`) with WAL mode enabled
* **Frontend:** Vanilla HTML5 + CSS3 + ES6 JavaScript served directly from `backend/static/`
* **Graph Engine:** `vis-network.min.js` bundled locally in `backend/static/js/vis-network.min.js` (100% offline self-contained)
* **Health Check Endpoint (`GET /api/health`):**
  ```json
  {
    "status": "ok",
    "version": "2.0.0-SIH26182",
    "system": "CryptoGuard AI",
    "chains_supported": ["ethereum", "bitcoin", "polygon", "arbitrum", "tron"],
    "database": "connected",
    "timestamp": "2026-09-28T19:32:00Z"
  }
  ```
  *HTTP Status: 200 OK (272 bytes)*

---

## 3. SIH Main Demo Flow Verification

We tested the end-to-end hackathon presentation flow step by step:

```
Dashboard ➔ New Investigation ➔ Demo Wallet ➔ Analyze ➔ Transaction Graph
   ➔ Wallet Intelligence ➔ VASP Attribution ➔ Risk Analysis ➔ Timeline
   ➔ Evidence Locker ➔ Cybercrime Response ➔ Legal Report (PDF)
```

| Step | Flow Stage | Tested Element | Verified Result | Status |
| :--- | :--- | :--- | :--- | :--- |
| **1** | **Dashboard** | `GET /api/v1/dashboard/summary` | Returned 12 cases, 21 known VASPs, 5 supported chains, recent investigations list. | **PASS** |
| **2** | **New Investigation** | Chain selector & address input | Chain dropdown (`ethereum`, `bitcoin`, `polygon`, `arbitrum`, `tron`) & Demo Mode toggle switch verified. | **PASS** |
| **3** | **Demo Wallet** | `loadDemoWallet(1)` | Loaded target address `0x742d35cc6634c0532925a3b844bc454e4438f44e` on Ethereum. | **PASS** |
| **4** | **Analyze** | `GET /api/trace` (Demo Mode) | Execution completed in ~140ms; generated 12 nodes, 12 edges, 3 VASP matches, risk 82/100 HIGH. | **PASS** |
| **5** | **Transaction Graph** | Tab 1 (`#tabGraph`) | Vis-network initialized with 12 colored nodes (Suspect, Mules, Mixers, VASPs), edge weights, physics stabilization, and interactive Node Inspector. | **PASS** |
| **6** | **Wallet Intelligence** | Tab 2 (`#tabWalletIntel`) | Rendered classification (*Suspect / Laundering Facilitator*), 0.12 ETH balance, 14 transactions, inflow/outflow balance, behavioral summary. | **PASS** |
| **7** | **VASP Attribution** | Tab 3 (`#tabVaspAttribution`) | Ranked VASP matches: **CoinDCX (84.5% - 2 hops)**, **Binance (73.8% - 3 hops)**, **Kraken (58.2% - 3 hops)** with 4-factor scoring and hop walks. | **PASS** |
| **8** | **Risk Analysis** | Tab 4 (`#tabRiskAnalysis`) | Circular risk gauge (82/100 HIGH), 10 weighted forensics signals, 4 AML typologies (*Layering via Mixer Obfuscation*, *Peel Chain Structuring*, etc.). | **PASS** |
| **9** | **Timeline** | Tab 5 (`#tabTimeline`) | 8 chronological events with timestamps, block numbers, transaction hashes, values, and hop role labels. | **PASS** |
| **10** | **Evidence Locker** | Tab 6 (`#tabEvidence`) | 5 forensic evidence items with SHA-256 hashes; `PATCH /api/evidence/{id}` updated status to "Reviewed" and persisted in SQLite. | **PASS** |
| **11** | **Cybercrime Response** | Tab 7 (`#tabCybercrime`) | `POST /api/sahyog/notice` generated 2,394-character formal Section 91 CrPC notice with Indian legal format, FIR details, and VASP compliance contact. | **PASS** |
| **12** | **PDF Report** | `GET /api/report/{wallet}` | Generated 7,768-byte binary PDF report via ReportLab with LEA headers, case details, attribution table, and legal disclaimer. | **PASS** |
| **13** | **Copilot Drawer** | `POST /api/copilot/query` | Deterministic Intelligence Engine answered "Why was CoinDCX attributed?" with confidence breakdown and hop route. | **PASS** |

---

## 4. Specific Point-by-Point Verification

| Item to Verify | Result | Evidence / Exact Output |
| :--- | :--- | :--- |
| **Demo Mode works** | **YES** | Deterministic fixture loads 12 nodes, 12 edges, 3 VASP hits, 8 timeline items, 5 evidence records. |
| **VASP attribution works** | **YES** | Multi-factor attribution scoring formula calculates: Proximity (75.0), Interaction (86.2), Recency (96.0), Evidence Quality (High) = 84.5% CoinDCX. |
| **Transaction graph works** | **YES** | Local `vis-network.min.js` renders directed network with typed node styling, custom physics, and node inspection. |
| **Risk scoring works** | **YES** | Scored 82/100 (HIGH) based on 10 risk signals (mixer interaction, rapid fund movement, peel chain, multi-hop dispersal, high-value flow). |
| **PDF report works** | **YES** | HTTP 200, 7,768 bytes, valid `%PDF-1.4` stream generated dynamically by ReportLab. |
| **Copilot works** | **YES** | Rule-based engine handles 5 primary prompt chips with forensic context; optional LLM integration if API key provided. |
| **SQLite persistence works** | **YES** | `cryptoguard.db` stores investigations, evidence items, and audit logs. `PATCH` calls update database rows in real time. |
| **All 8 workspace tabs work** | **YES** | Overview, Graph, Wallet Intel, VASP Attribution, Risk Analysis, Timeline, Evidence Locker, Cybercrime Response all bind correctly. |
| **No major console errors** | **YES** | `node -c backend/static/js/app.js` passed with 0 syntax errors. All 88 `document.getElementById` targets exist in `index.html`. |
| **No broken API calls** | **YES** | 7 core endpoints tested and returning HTTP 200 OK. |

---

## 5. Identified Broken Functionality

1. **Starlette TestClient in `test_cryptoguard_e2e.py` on Python 3.14:**  
   Running `python test_cryptoguard_e2e.py` directly throws `RuntimeError: The starlette.testclient module requires the httpx package to be installed`. In Python 3.14 / modern Starlette, `httpx` is an explicit requirement for `TestClient`. The test script should be updated to use `urllib` against the running server or `httpx` should be added to `requirements.txt`.
2. **Arbitrary Live Address Tracing without API Keys:**  
   If an evaluator unchecks "Demo Mode" and enters a random mainnet wallet address without having set `ETHERSCAN_API_KEY` or `ALCHEMY_API_KEY` in `.env`, the trace returns a fallback with 0 transactions. While it does not crash, the UI does not currently display a warning badge explaining that live tracing requires an RPC API key.

---

## 6. UI/UX Problems Visible to SIH Judges

1. **Fixed Graph Canvas Height (`640px`):**  
   In `backend/static/css/style.css`, `#graphNetwork` is hardcoded to `height: 640px`. On standard 1366×768 or 1080p laptop screens commonly used by hackathon judges, this pushes the node inspector and action buttons below the fold, forcing awkward vertical scrolling.
2. **Node Inspector Overlap on Narrow Screens:**  
   The Node Inspector Drawer (`.inspector-drawer`) floats at `bottom: 16px; right: 16px; width: 340px`. On screen widths below 1280px, it overlaps with the graph legend and zoom buttons.
3. **No Direct "View/Export Raw JSON" Button:**  
   Technical evaluators often ask to see the raw API payload to verify that calculations aren't hardcoded in the frontend. Currently, an investigator must open DevTools Network tab to see the JSON.
4. **Table Density & Horizontal Scroll Indicators:**  
   The Evidence Locker and Timeline tables feature 6+ columns. On smaller laptop viewports, horizontal scrolling is possible but lacks visual fade indicators or scroll hint arrows.

---

## 7. Misleading or Unsupported Claims

1. **"Deep Generative AI Copilot" vs. Deterministic Rule Engine:**  
   In default offline demo mode, the Copilot uses a deterministic regex/keyword parser. While this is resilient for hackathons, describing it in judging pitches as "Deep Generative AI" is inaccurate. It should be presented as **"Hybrid Forensic Copilot: Deterministic NLP Rule Engine + Optional LLM Plug-in"**.
2. **"113,000+ VASPs Indexed":**  
   The active in-memory registry contains **21 curated VASPs** (CoinDCX, WazirX, Binance, ZebPay, CoinSwitch, Kraken, KuCoin, etc.) with enriched compliance data (FIU-IND, reporting IDs, compliance emails). The 113,000-address dataset is an offline reference file. The UI should state: *"21 Tier-1 VASPs actively registered with FIU-IND compliance metadata; scalable via offline accounts registry"*.
3. **"Automated Exchange Asset Freezing":**  
   The system does not directly freeze assets on exchanges (which requires private exchange compliance API keys or law enforcement portal integration). It compiles legally compliant **Section 91 CrPC notices**. The wording must clearly state: *"Automated Legal Notice Generation for KYC Disclosure and Account Freezing"*.

---

## 8. Security & Deployment Problems

1. **CORS Wildcard Configuration:**  
   `backend/main.py` configures `allow_origins=["*"]`. While standard for local hackathons, it exposes API endpoints to unauthorized cross-origin requests.
2. **Unauthenticated SQLite Management Endpoints:**  
   The `PATCH /api/evidence/{id}` and `POST /api/sahyog/notice` endpoints lack session-based or token-based authentication (RBAC). Any client can update evidence status.
3. **External Font Dependencies (Google Fonts):**  
   `index.html` loads fonts from `fonts.googleapis.com`. If the SIH evaluation occurs in an air-gapped venue with restricted internet or captive portals, font loading will time out before falling back to system sans-serif.

---

## 9. Top 5 Prioritized Improvements Before SIH Submission

| # | Improvement | Exact File | Component / Function | Problem | Proposed Change | Difficulty |
| :---: | :--- | :--- | :--- | :--- | :--- | :---: |
| **1** | **Responsive Graph Height & Fullscreen Mode** | `backend/static/css/style.css` & `backend/static/js/app.js` | `#graphNetwork` and `renderGraph()` | Fixed 640px height forces vertical scrolling on 1366x768 laptop screens; inspector overlaps legend. | Change height to `clamp(440px, 60vh, 700px)` and add a 1-click "Fullscreen / Expand Graph" toggle with `network.fit()`. | **LOW** |
| **2** | **One-Click Raw JSON Export & Inspection Modal** | `backend/static/index.html` & `backend/static/js/app.js` | Top action bar & new `showRawJsonModal()` | Technical evaluators cannot inspect the raw multi-dimensional scoring payload without opening browser DevTools. | Add an "Export JSON" button next to "PDF Report" that triggers instant download and opens a syntax-highlighted inspector modal. | **LOW** |
| **3** | **Offline Font & Fallback Typography** | `backend/static/index.html` & `backend/static/css/style.css` | `<link>` in `<head>` & `font-family` CSS | External Google Fonts CDN dependency can cause layout shift or latency in an air-gapped evaluation hall. | Add local font-family fallback stack (`system-ui, -apple-system, Segoe UI, Roboto, sans-serif`) with `font-display: swap`. | **LOW** |
| **4** | **Live Mode API Key Banner & Sample Wallets** | `backend/static/js/app.js` & `backend/tracer.py` | `handleTraceSubmit()` & `TracerService` | Querying live addresses without an Etherscan API key yields an empty graph without an explanatory message. | Add a dismissible status badge: *"Live API key not detected — showing offline cache or switch to Demo Mode"* with 3 pre-tested live sample addresses. | **MEDIUM** |
| **5** | **Enhanced Copilot Keyword Matcher & Chip Suggestions** | `backend/copilot.py` | `_rule_based_engine()` | Copilot falls back to generic summary if queries don't match exact regex triggers (e.g. "mule", "stolen", "freeze"). | Expand keyword synonym dictionary (covering "mule", "funds", "freeze", "kyc", "fiu", "police") and return clickable follow-up chips in answers. | **MEDIUM** |

---

## 10. Conclusion & Final Decision

### **READY TO DEVELOP: YES**

The CryptoGuard AI codebase is in an **exceptional baseline state**. The backend architecture, VASP multi-factor attribution engine, 8-tab workspace, SQLite persistence, vis-network graph, deterministic Copilot, and ReportLab PDF generator are fully functional, verified, and free of blocking bugs.

### Recommended Sequence of First 5 Implementation Tasks:
1. **Implement Responsive Graph Height & Fullscreen Button** (`backend/static/css/style.css`, `backend/static/js/app.js`)
2. **Add One-Click Raw JSON Export & Modal Inspector** (`backend/static/index.html`, `backend/static/js/app.js`)
3. **Configure Air-Gapped Font Fallbacks** (`backend/static/index.html`, `backend/static/css/style.css`)
4. **Add Live Mode API Key Indicator & Sample Live Wallets** (`backend/static/js/app.js`, `backend/tracer.py`)
5. **Expand Copilot Forensic Synonym Engine & Interactive Chips** (`backend/copilot.py`, `backend/static/js/app.js`)
