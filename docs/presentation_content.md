# SIH26182 — Presentation Master Content

---

## 0. Presentation Strategy

**One-line narrative:**

> An investigator receives a suspicious wallet. Instead of manually hopping across blockchain explorers and spreadsheets, our system turns that address into a structured, explainable investigation — graph, VASP candidates, confidence, and report — in seconds.

**Audience-first sequencing:**

| Beat | What the audience understands |
|---|---|
| Problem | Manual blockchain forensics is slow, fragmented, and investigator-dependent |
| Pipeline | Wallet → graph trace → VASP candidates → confidence scoring → risk → report |
| Differentiation | Not another block explorer. VASP attribution with explainable scoring |
| Feasibility | Built on public APIs, bounded traversal, modular architecture |
| Impact | Faster investigative leads, structured evidence, scalable to agencies |
| Future | ML-ready feature vectors, extensible to new chains and intelligence sources |

**Tone:** Precise, confident, technical, investigative. No marketing fluff. No fake AI claims.

---

## 1. Project One-Liner

**Wallet-to-VASP Attribution System — automated blockchain intelligence that traces a suspicious wallet's transaction graph, identifies the most likely Virtual Asset Service Provider it interacts with, scores attribution confidence across four dimensions, and produces an investigator-ready report with SAHYOG routing recommendation.**

| Field | Value |
|---|---|
| SIH Problem ID | SIH-26182 |
| Ministry | Ministry of Home Affairs (MHA) |
| Category | Software |
| Team | [TEAM NAME] |
| Team ID | [TEAM ID] |
| Tech Stack | Python, FastAPI, vis-network, reportlab, Etherscan/TronGrid/Blockstream APIs |

---

## 2. Core Narrative

### The Problem

When a cybercrime investigator receives a suspicious cryptocurrency wallet address from a victim complaint, the current workflow is:

1. Open a blockchain explorer (Etherscan, BscScan, etc.)
2. Manually inspect transactions, hop by hop
3. Cross-reference addresses against spreadsheets
4. Build a case report from fragmented evidence

This process is **slow, repetitive, and inconsistent** across investigators. It does not scale when dealing with hundreds of complaints or complex multi-hop money flows.

### Our Approach

The system automates the repetitive part of this workflow:

**INPUT** — A wallet address + chain selection
**TRACE** — BFS walks the transaction graph outward (up to configurable hop depth)
**IDENTIFY** — Every encountered wallet is checked against a known VASP registry
**SCORE** — Each VASP candidate receives a four-dimensional confidence score (40/30/20/10 weighting)
**ANALYZE** — Independent risk engine and wallet classifier run on the root wallet
**EXPLAIN** — Component scores, relationship types, and evidence quality are returned
**REPORT** — A downloadable PDF investigation report with SAHYOG routing

### What the Investigator Receives

- VASP attribution candidates ranked by confidence
- Explainable score breakdown (not a black box)
- Risk level + laundering typologies
- Wallet classification (exchange, hot wallet, deposit wallet, mixer, etc.)
- Transaction graph visualization
- PDF case report with legal disclaimer
- SAHYOG portal routing recommendation

### Critical Conceptual Boundary

> **This system does NOT prove criminality. It does NOT prove ownership.** It traces fund flows and identifies the most likely VASP relationship so investigators can direct formal KYC/freeze requests. The default attribution claim is "interacts with" — only upgraded to "controlled by" when structural evidence (hop-1 + deposit wallet pattern) clearly supports it.

---

## 3. Slide 1 — Title

### LAYER 1 — ON-SLIDE CONTENT

```
SIH-26182
Automated Attribution of Unknown Cryptocurrency
Wallets to Virtual Asset Service Providers (VASPs)

Ministry of Home Affairs · I4C · SIH 2026
Software Category

[TEAM NAME]
[TEAM ID]
```

### LAYER 2 — VISUAL SPECIFICATION

**Visual concept:** Dark background (near-black navy). A stylized transaction graph as the centerpiece — a glowing target node (the unknown wallet) connected by thin lines to intermediate nodes, culminating in a VASP/node cluster. The graph should feel like a forensic tool, not a crypto dashboard.

- **Background:** Deep navy/black gradient with subtle grid pattern (intelligence command center aesthetic)
- **Center graphic:** Minimal node-graph illustration — one prominent target node, 2-3 hops of connections, a labeled VASP terminal node
- **Title typography:** Bold, high-contrast. "SIH-26182" small, above the main title
- **Secondary text:** Ministry, category, team — clean, restrained
- **Accent color:** Single restrained blue/indigo accent on the graph connections

**What should NOT be on this slide:**
- Bitcoin/crypto trading imagery (charts, coins, rockets)
- Generic blockchain stock photos
- Paragraphs of text
- More than 3 lines of subtitle text

### LAYER 3 — SPEAKER NOTES

*"Good morning. We're [TEAM NAME], and we built SIH-26182 — a blockchain intelligence system for the Ministry of Home Affairs. When a cybercrime investigator receives a suspicious wallet address, our system automatically traces its transaction graph, identifies the nearest VASP, scores attribution confidence across four dimensions, and produces an investigator-ready report. Let me walk you through how it works."*

---

## 4. Slide 2 — Proposed Solution

### LAYER 1 — ON-SLIDE CONTENT

**Headline:** From Wallet Address to VASP Attribution — Automated

**Content blocks (6 points):**

1. **Input:** Investigator enters a suspicious wallet address + selects blockchain
2. **Trace:** BFS graph traversal follows money flows hop-by-hop across the transaction graph
3. **Identify:** Every encountered address checked against known VASP registry
4. **Score:** Four-dimensional confidence model — graph proximity, interaction strength, temporal recency, evidence quality
5. **Analyze:** Independent risk engine (10 signals) + wallet classifier (11 archetypes)
6. **Report:** Transaction graph visualization + downloadable PDF + SAHYOG routing recommendation

**Value Proposition (one line):**
> Turns a raw wallet address into a structured, explainable investigation — graph, candidates, confidence, and report — in seconds.

**Differentiators (4 points):**

- VASP-specific attribution (not generic wallet analytics)
- Explainable four-dimensional confidence scoring — every component visible
- Conservative attribution language: "interacts with" by default, "controlled by" only with structural evidence
- Investigator-first workflow: every output designed for case reports, not dashboards

### LAYER 2 — VISUAL SPECIFICATION

**Recommended diagram:** A vertical pipeline flow chart, left-aligned:

```
[Wallet Input]
    ↓
[Validation + Chain Select]
    ↓
[Blockchain APIs]
    ↓
[BFS Graph Traversal]
    ↓
[VASP Matching + Confidence Scoring]
    ↓
[Risk Engine + Wallet Classifier]
    ↓
[Graph Visualization + PDF Report]
```

**Visual treatment:**
- Each step in a dark glass-panel card with a thin accent border
- Connecting arrows in the accent color
- The scoring step highlighted (different background tint) to show it's the core innovation
- Right side: 3 small inset panels showing the actual output screenshots (risk banner, graph, report)

**Content density:** Medium. 6 pipeline steps + 4 differentiators + value proposition. One-line each.

### LAYER 3 — SPEAKER NOTES

*"Let me show you what the system actually does. The investigator enters a wallet address — any wallet flagged in a complaint. The system validates it, selects the right blockchain adapter, and fetches real transaction data. Then it performs a breadth-first search outward through the transaction graph, following money flows hop by hop. Every address it encounters is checked against a VASP registry. For each VASP match, it computes a four-dimensional confidence score — graph proximity at 40%, interaction strength at 30%, temporal recency at 20%, and evidence quality at 10%. Separately, a risk engine scores the wallet across 10 independent signals for laundering typologies, and a classifier categorizes it into one of 11 behavioral archetypes. The result: a transaction graph, ranked VASP candidates with full score breakdown, a risk profile, and a downloadable PDF report. What makes this different from a block explorer is that we're not just showing transactions — we're attributing wallets to specific VASPs with explainable confidence, and routing recommendations for the SAHYOG portal."*

---

## 5. Slide 3 — Technical Approach

### LAYER 1 — ON-SLIDE CONTENT

**Headline:** Multi-Chain Intelligence Pipeline

**Architecture layers (top to bottom):**

1. **Blockchain Data Layer**
   - EVM chains (Ethereum, BSC, Polygon) → Etherscan v2 API
   - Tron → TronGrid REST API
   - Bitcoin → Blockstream.info (no key required)
   - Exponential-backoff retry on 429/500/502/503/504

2. **Graph Engine**
   - BFS traversal with configurable hop depth (1–6)
   - Node expansion cap (60 nodes) for bounded runtime
   - Per-wallet transaction fetching with deduplication

3. **Intelligence Layer**
   - VASP registry: 10-address curated demo dataset (demo_vasps.csv) — designed to load accounts.csv (113k+ Ethereum addresses) when available; falls back gracefully when absent
   - High-risk registry: ~33 curated addresses (mixers, sanctions, ransomware, darknet, bridges)
   - Four-dimensional confidence scorer (40/30/20/10)
   - 10-signal risk scorer with 9 laundering typology labels
   - 11-category wallet classifier

4. **Feature Extraction**
   - 18-feature behavioral vector: graph, value, temporal, exposure, structuring
   - ML-ready schema — feeds directly into future XGBoost/LightGBM without schema changes

5. **Output Layer**
   - Investigator dashboard (5 panels: Dashboard, Investigation, History, Alerts, VASPs)
   - vis-network transaction graph (color-coded by wallet type)
   - PDF report (reportlab) with explainable score breakdown
   - SAHYOG routing recommendation + submission stub

**Tech stack:**
- Backend: Python, FastAPI, uvicorn
- Frontend: Vanilla JS, vis-network, Inter + JetBrains Mono fonts
- PDF: reportlab
- Config: python-dotenv

### LAYER 2 — VISUAL SPECIFICATION

**Recommended diagram:** A layered architecture diagram:

```
┌──────────────────────────────────────────────┐
│  INVESTIGATOR DASHBOARD                       │
│  ┌──────────┬──────────┬──────────────────┐  │
│  │ Dashboard│Investigate│History│Alerts│VASP│  │
│  └──────────┴──────────┴──────────────────┘  │
├──────────────────────────────────────────────┤
│  OUTPUT LAYER                                 │
│  PDF Report │ vis-network Graph │ SAHYOG API  │
├──────────────────────────────────────────────┤
│  INTELLIGENCE LAYER                           │
│  ┌────────────┬────────────┬───────────────┐  │
│  │Confidence  │ Risk Engine│ Wallet        │  │
│  │Scorer      │ (10 signal)│ Classifier    │  │
│  │(4-component│ + 9 typologies │ (11 types)   │
│  │ 40/30/20/10)│            │               │  │
│  └────────────┴────────────┴───────────────┘  │
│  Feature Extractor (18 features, ML-ready)    │
├──────────────────────────────────────────────┤
│  GRAPH ENGINE                                 │
│  BFS Traversal │ Hop limits │ Node cap (60)   │
├──────────────────────────────────────────────┤
│  BLOCKCHAIN DATA LAYER                        │
│  Etherscan v2 │ TronGrid │ Blockstream.info  │
│  EVM chains   │ TRX      │ BTC              │
├──────────────────────────────────────────────┤
│  VASP + RISK REGISTRIES                       │
│  demo_vasps.csv (10 curated VASP addresses)  │
│  High-risk registry (~33 curated addresses)   │
└──────────────────────────────────────────────┘
```

**Visual treatment:**
- Each layer in a distinct dark panel with subtle border
- Layer 4 (Intelligence) highlighted as the core value
- Color-coded connectors showing data flow
- Right margin: small screenshot of the actual dashboard

### LAYER 3 — SPEAKER NOTES

*"The architecture is five layers, each independently replaceable. At the bottom, we have the blockchain data layer — three adapters for EVM chains via Etherscan v2, Tron via TronGrid, and Bitcoin via Blockstream. All adapters implement exponential-backoff retry for rate limits and transient errors. Above that, the graph engine performs a BFS walk through the transaction graph, bounded by a configurable hop depth and a 60-node expansion cap to keep runtime predictable. The intelligence layer is where the core work happens: the VASP registry loads from a curated address dataset — currently 10 well-known exchange addresses from demo_vasps.csv, with architecture support for a 113k-address accounts.csv when available. The four-dimensional confidence scorer combines graph proximity, interaction strength, temporal recency, and evidence quality. The risk engine evaluates 10 independent signals from mixer interaction to structuring patterns, and the wallet classifier categorizes the root wallet into one of 11 behavioral archetypes. The feature extractor produces an 18-feature behavioral vector — this is the ML-ready foundation. At the top, the investigator dashboard provides a 5-panel interface with transaction graph visualization, case history, and PDF report generation. The entire backend is a FastAPI application with 11 endpoints."*

---

## 6. Slide 4 — Feasibility & Viability

### LAYER 1 — ON-SLIDE CONTENT

**Headline:** Built on Public Data, Designed to Scale

**Technical Feasibility (5 points):**

- **Public blockchain data** — All five chains have free, public APIs (Etherscan, TronGrid, Blockstream). No proprietary data sources required.
- **Bounded graph traversal** — Node expansion cap (60) + hop limit (default 3) keeps runtime predictable. No unbounded recursion.
- **Modular chain adapters** — Each chain has a dedicated adapter class. Adding a new chain = one new adapter + metadata entry.
- **Explainable scoring** — All confidence components are individually returned. No black-box logic in the current prototype.
- **Deterministic demo mode** — Fallback fixture enables offline demonstration without API keys or network.

**Operational Challenges (4 points):**

- **API rate limits** — Free tiers impose call limits. Mitigated by request delays (220-500ms) and exponential-backoff retry.
- **VASP label coverage** — The VASP registry is currently loaded from demo_vasps.csv (10 curated exchange addresses). The architecture is designed to load accounts.csv (113k+ Ethereum addresses) when available, but that file is not in the repository (gitignored). Coverage is currently limited to the 10-address demo dataset.
- **Attribution ambiguity** — A VASP interaction does not prove ownership. System addresses this with relationship_type classification and evidence quality tiers.
- **In-memory storage** — Case history is lost on server restart. Production deployment requires a database (PostgreSQL/SQLite).

**Mitigation Strategies:**

| Challenge | Current Mitigation | Future Enhancement |
|---|---|---|
| Rate limits | Request delays + exponential-backoff retry | API key rotation, paid tiers |
| Label coverage | 10-address demo dataset (demo_vasps.csv) | accounts.csv (113k ETH) + per-chain datasets |
| Attribution ambiguity | relationship_type + evidence quality tiers | Enhanced flow analysis (laundered_through) |
| Data persistence | In-memory (session-scoped) | PostgreSQL persistence |

### LAYER 2 — VISUAL SPECIFICATION

**Recommended layout:** Three-column layout under the headline:

- **Column 1 (Feasibility):** 5 dark cards with green accent dots
- **Column 2 (Challenges):** 4 dark cards with amber accent dots
- **Column 3 (Mitigations):** A table with Current vs Future rows

**Bottom strip:** A horizontal bar showing the intelligence roadmap (Levels 1-8), with Levels 1-3 checked/complete and Levels 4-8 as future.

### LAYER 3 — SPEAKER NOTES

*"Feasibility rests on three pillars: public blockchain data, bounded computation, and explainable logic. All five chains have free public APIs. The BFS traversal is bounded by both hop depth and a node expansion cap, so runtime is predictable even for complex wallets. The scoring is entirely rule-based and explainable — every component score is returned so an investigator can understand why a match scored the way it did. And we have a deterministic demo mode so the system can be demonstrated without any API configuration. On the challenge side: rate limits are real but mitigated by request delays and retry logic. VASP label coverage is the key limitation — the architecture supports loading accounts.csv with 113,000 Ethereum addresses, but that file is not in the repository. The system currently runs with a 10-address demo dataset. We designed the registry to accept any CSV drop-in without code changes. Attribution ambiguity is addressed head-on with our relationship_type taxonomy — we default to 'interacts with' and only escalate to 'controlled by' when structural evidence supports it. And the in-memory store is fine for a prototype; a production deployment would add PostgreSQL. Each challenge has a clear mitigation path, and the architecture is designed so that enhancements like ML ranking or additional chain adapters can be added without changing the core pipeline."*

---

## 7. Slide 5 — Impact & Benefits

### LAYER 1 — ON-SLIDE CONTENT

**Headline:** Accelerating Investigative Leads Through Automated Blockchain Intelligence

**Primary Users:**

- Cybercrime investigators (I4C, state cyber cells)
- Law enforcement and intelligence teams
- Financial crime / AML investigators
- Blockchain forensic analysts
- VASP compliance teams

**Workflow Transformation:**

| Without System | With System |
|---|---|
| Wallet → explorer → manual hops → spreadsheets | Wallet → automated trace → graph |
| Address lookup → interpretation → report | VASP candidates → risk intelligence → evidence |
| Hours of manual work | Seconds to structured output |

**Benefits (6 points):**

1. **Reduces repetitive manual tracing** — BFS automation replaces hours of manual blockchain explorer navigation
2. **Structures fragmented evidence** — Transaction data becomes a ranked, explainable investigation package
3. **Prioritizes promising VASP leads** — Confidence scoring surfaces the most actionable attribution candidates first
4. **Explainable outputs** — Every confidence score has component breakdown. No black-box results in case files.
5. **Accelerates report generation** — PDF investigation report generated in one click, not assembled manually
6. **Foundation for multi-chain intelligence** — Modular architecture enables expansion to new chains and data sources

**Scalability Path:**
- Current: Single-investigator, session-based tool
- Near-term: Database persistence, multi-user access
- Future: Integration with SAHYOG Portal (I4C), National Cybercrime Reporting Portal, live sanctions feeds

**National Relevance:**
> Designed for India's cybercrime investigation ecosystem. The SAHYOG routing recommendation is structured for integration with the I4C portal. The system's explainability-first design aligns with requirements for auditable, legally defensible investigative tools.

### LAYER 2 — VISUAL SPECIFICATION

**Recommended layout:**

- **Top:** Two side-by-side workflow comparisons (Without vs. With) using simple arrow flows
- **Middle:** 6 benefit cards in a 2x3 grid, each with an icon and one-line text
- **Bottom:** A growth timeline showing current -> near-term -> future deployment stages

**Visual treatment:**
- "Without" side in muted/desaturated tones
- "With" side in the accent color
- Benefit cards with subtle left-border accent
- Timeline as a horizontal arrow with three milestones

### LAYER 3 — SPEAKER NOTES

*"The impact is on the investigator's workflow. Right now, when a complaint comes in with a wallet address, the investigator opens Etherscan, traces a few hops manually, cross-references addresses in a spreadsheet, and builds a report. This system automates the repetitive tracing and structures the output. The confidence scoring means investigators spend time on the most promising leads first. The explainable scoring is critical — in a legal context, you can't hand a judge a black-box score. Every component is broken down and documented in the PDF report. The SAHYOG routing recommendation translates the technical output into actionable next steps. For scalability: the modular architecture means adding a new blockchain adapter or a new risk signal doesn't require rewriting the core pipeline. The feature vectors we extract today are ML-ready — when we add XGBoost ranking in a future version, the schema doesn't need to change. And at the national level, this is designed to fit into India's existing cybercrime infrastructure — the SAHYOG routing, the I4C portal, and the National Cybercrime Reporting Portal."*

---

## 8. Slide 6 — Research & References

### LAYER 1 — ON-SLIDE CONTENT

**Headline:** Built on Open Standards and Public Intelligence

**Problem Statement & Context:**
- SIH-26182 Problem Statement — Smart India Hackathon 2026, Ministry of Home Affairs
- SAHYOG Portal — I4C, Ministry of Home Affairs (integration target)

**Blockchain Data Sources:**
- Etherscan API v2 — Multi-chain transaction data (Ethereum, BSC, Polygon)
- TronGrid API — TRON transaction data
- Blockstream.info API — Bitcoin transaction data (no API key required)

**Address Label / VASP Datasets:**
- accounts.csv — Community-labelled Ethereum addresses (113k+ entries, Dune/Etherscan community dataset) — **not currently in repo; design-ready loading from known_vasps.py**
- demo_vasps.csv — Curated VASP reference addresses (10 well-known exchanges) — **currently active dataset**
- Chainabuse.com — Crowd-sourced scam reports (recommended for demo wallet selection)

**Threat Intelligence References:**
- OFAC Sanctions List — U.S. Treasury, Office of Foreign Assets Control
- CISA Ransomware Advisories — Cybersecurity & Infrastructure Security Agency
- Tornado Cash (OFAC sanctioned, Aug 2022) — Mixer address registry

**Blockchain Forensics & Research:**
- Bitcoin and Cryptocurrency Technologies (Arvind Narayanan et al.) — Foundational blockchain forensics text
- "Anti-Money Laundering in Bitcoin" (Moser et al., 2013) — P2P mixing and transaction graph analysis
- Etherscan.io — Public blockchain explorer for address verification

### LAYER 2 — VISUAL SPECIFICATION

**Recommended layout:** Clean reference list with categorized sections

- Organized into 4-5 categories with subtle header separators
- Each reference: Source name (bold) + one-line description
- No URLs cluttering the slide — reserve for speaker notes or handout
- Bottom: QR code linking to the GitHub repository

**Visual treatment:**
- Small, structured text — maximum readability
- Category headers in the accent color
- Source names in bold, descriptions in regular weight
- Generous white space between categories

### LAYER 3 — SPEAKER NOTES

*"All data sources are publicly available. The blockchain data comes from Etherscan's free API, TronGrid, and Blockstream — no paid subscriptions needed. The VASP registry is loaded from a community-labelled dataset of over 113,000 Ethereum addresses when the accounts.csv file is available. In the current repository, the system uses a curated demo dataset of 10 well-known exchange addresses. The high-risk registry draws from publicly available OFAC sanctions lists, CISA ransomware advisories, and documented mixer addresses like Tornado Cash. For the theoretical foundation, we reference foundational blockchain forensics work including Narayanan's text and Moser et al.'s research on AML in Bitcoin. We recommend Chainabuse for finding documented scam wallets for demonstration purposes. All of these are open, verifiable sources — no proprietary or classified data is used in the current prototype."*

---

## 9. Current vs Future

### Capability Matrix

| Capability | Current Prototype | Future (Planned) |
|---|---|---|
| **Blockchains** | Ethereum, BSC, Polygon, Tron, Bitcoin | Additional EVM chains, Solana |
| **VASP Intelligence** | 10-address demo dataset (demo_vasps.csv) — designed for 113k+ accounts.csv | Per-chain VASP datasets |
| **Graph Analysis** | BFS traversal, hop-limited, node-capped (60) | Enhanced flow analysis, cycle detection |
| **Attribution Scoring** | 4-component weighted model (40/30/20/10) — rule-based | ML ranking (XGBoost/LightGBM) on existing feature vectors |
| **Relationship Types** | interacts_with, controlled_by (heuristic) | laundered_through (directional flow) |
| **Risk Analysis** | 10 signals, 9 typologies — rule-based | Same signals + ML-enhanced anomaly detection |
| **Wallet Classification** | 11 categories — rule-based | Same categories + ML clustering |
| **Behavioral ML** | 18-feature vector extracted, ready for ML | XGBoost/LightGBM (Level 4), DBSCAN clustering (Level 5) |
| **Graph Embeddings** | None | node2vec / GraphSAGE (Level 6) |
| **GNN** | None | Graph Neural Networks (future) |
| **Multi-chain Correlation** | Per-chain tracing | Cross-chain bridge tracing (Level 7) |
| **Real-time Monitoring** | None | Alert-based monitoring (future) |
| **Case Storage** | In-memory (session-scoped) | PostgreSQL persistence |
| **Authentication** | None | JWT, RBAC (future) |
| **Live Sanctions Feed** | Hardcoded (~33 addresses) | Automated OFAC SDN feed |
| **Investigator Integration** | SAHYOG submission stub | Full SAHYOG portal API integration |
| **Government Integration** | None | National Cybercrime Reporting Portal backend service |

### Intelligence Roadmap

```
Level 1  ✅  Graph traversal (BFS, multi-chain)
Level 2  ✅  Behavioral feature extraction (18 features)
Level 3  ✅  Multi-dimensional weighted scoring (4-component confidence)
Level 4  🔧  ML candidate ranking (XGBoost / LightGBM) — feature vectors ready
Level 5  🔧  Wallet clustering / DBSCAN
Level 6  📋  Graph embeddings (node2vec / GraphSAGE)
Level 7  📋  Multi-chain cross-chain flow analysis
Level 8  📋  Agentic investigation + RAG over case history
```

**Key insight for presentation:** Levels 1-3 are fully implemented and tested. The feature vector from Level 2 feeds directly into Level 4 ML ranking without any schema changes. This means the ML upgrade is additive — no refactoring required.

---

## 10. Innovation & Differentiation

### Top 5 Defensible Differentiators

| Rank | Differentiator | Why It Matters |
|---|---|---|
| 1 | **VASP-specific attribution** | Most blockchain forensics tools are generic wallet analytics. This system is purpose-built for the investigator question: "Which exchange holds KYC data on this wallet?" |
| 2 | **Explainable four-dimensional confidence** | Unlike black-box ML or single-hop heuristics, every confidence score has individually visible components (proximity, interaction strength, recency, evidence quality) |
| 3 | **Conservative attribution language** | The relationship_type taxonomy (interacts_with vs. controlled_by) is designed for legal defensibility — the system errs on the side of weaker claims by default |
| 4 | **Evidence-quality tiers** | Labels are tagged as high (OFAC/government), medium (community dataset), or low (unverified) — investigators see the provenance of every claim |
| 5 | **Investigator-first workflow** | Every output (risk level, typology, graph, report, SAHYOG routing) is designed for case preparation, not for trading dashboards or DeFi analytics |

### What Is NOT Innovative (be honest)

- BFS graph traversal — standard algorithm, well-documented
- Multi-chain support — common in blockchain tools
- PDF report generation — standard feature
- Rule-based scoring — common approach for prototypes

### What the Feature Vector Enables (Future Innovation)

The 18-feature behavioral vector is the bridge to ML. When Levels 4-5 are implemented:
- XGBoost/LightGBM can rank VASP candidates beyond the current heuristic formula
- DBSCAN can group wallets by behavioral similarity
- No schema changes needed — the vector is already structured and normalized

---

## 11. 3-Minute Live Demo Story

### Demo Flow

**Setup:** Use `/api/demo/trace` endpoint (deterministic, no API key needed). The demo fixture returns a fixed result for any wallet address.

**Step 1 — Enter Wallet (0:00-0:15)**
- Screen: Dashboard -> "New Investigation" panel
- Action: Enter `0xd8da6bf26964af9d7eed9e03e53415d37aa96045`, chain = Ethereum, max_hops = 3
- Say: *"Let me trace a known wallet. I'll enter this address and set it to search 3 hops deep across Ethereum."*
- Concept: Multi-chain wallet input, address validation, configurable hop depth

**Step 2 — Loading State (0:15-0:30)**
- Screen: Spinner + "Tracing transaction graph across the blockchain..."
- Say: *"The system is now performing a BFS walk through the transaction graph, following money flows outward. It will fetch transactions for each wallet it encounters, build the graph, check against the VASP registry, and compute all scores."*
- Concept: BFS traversal, bounded by hop limit and node cap

**Step 3 — Risk Banner (0:30-0:45)**
- Screen: MEDIUM RISK badge, score 35, typology "Proximity to mixer (Tornado Cash)"
- Say: *"The risk engine flags this as MEDIUM risk, score 35, with a mixer proximity typology. The wallet has a transaction path to Tornado Cash, which is an OFAC-sanctioned mixer."*
- Concept: 10-signal risk scorer, laundering typology detection

**Step 4 — Wallet Classification (0:45-1:00)**
- Screen: Hot Wallet classification, reason text, chain/txs/hops metadata
- Say: *"The wallet classifier identifies this as a hot wallet — high-frequency transactions with a narrow counterparty set. The system categorizes wallets into 11 behavioral archetypes."*
- Concept: 11-category classifier, behavioral heuristics

**Step 5 — SAHYOG Routing (1:00-1:15)**
- Screen: "Voluntary disclosure inquiry to Binance Hot Wallet" with disclosure note
- Say: *"The system recommends a voluntary disclosure inquiry to Binance Hot Wallet at 78.5% confidence. The relationship type is 'interacts with' — meaning funds flowed toward Binance, but we're not claiming ownership. This routing is designed to feed into the SAHYOG portal."*
- Concept: Context-aware routing, relationship_type taxonomy, SAHYOG integration stub

**Step 6 — VASP Attribution Cards (1:15-1:30)**
- Screen: Card showing Binance Hot Wallet, 78.5% confidence, hop-2 path, progress bar, fund flow path
- Say: *"Here's the VASP attribution. Binance Hot Wallet at hop 2, 78.5% confidence. The card shows the fund flow path and the confidence breakdown — graph proximity, interaction strength, temporal recency, and evidence quality."*
- Concept: Multi-dimensional scoring, ranked candidates, explainable output

**Step 7 — Transaction Graph (1:30-1:45)**
- Screen: vis-network graph with 4 nodes (target in blue star, Binance in green diamond, Tornado Cash in red hexagon, intermediate in gray)
- Say: *"The transaction graph visualizes the money flow. Blue star is the target wallet. Green diamond is Binance — the VASP match. Red hexagon is Tornado Cash — the mixer flagged by the risk engine. You can drag, zoom, and hover for details."*
- Concept: vis-network visualization, color-coded nodes by wallet type

**Step 8 — Generate Report (1:45-2:00)**
- Screen: Click "Download PDF Report" -> PDF opens showing case summary, risk assessment, VASP attribution table, score breakdown, behavioral feature vector, SAHYOG routing, legal disclaimer
- Say: *"One click generates a full PDF investigation report — case summary, risk assessment, VASP attribution with the confidence breakdown table, wallet behavioral features, SAHYOG routing, and a legal disclaimer. This is what goes into the case file."*
- Concept: PDF generation, reportlab, legal disclaimer, evidence documentation

**Step 9 — SAHYOG Submit (2:00-2:15)**
- Screen: Click "Submit to SAHYOG Portal" -> alert with reference ID
- Say: *"Finally, the investigator can submit directly to the SAHYOG portal with one click. It generates a reference ID and routes the request with all the context the VASP needs."*
- Concept: SAHYOG submission stub, reference ID generation

**Step 10 — Wrap-up (2:15-2:30)**
- Screen: Return to dashboard showing the new case in history
- Say: *"And the case is now in the session history, filterable by chain and risk level. That's the full pipeline — from wallet address to investigation report in seconds."*
- Concept: In-memory case history, session persistence

---

## 12. Difficult Judge Questions

### Q1: Why is this different from Etherscan?

**SHORT ANSWER:** Etherscan shows transactions. Our system traces graphs, scores VASP attribution, assesses risk, classifies wallets, and generates investigation reports.

**TECHNICAL ANSWER:** Etherscan is a block explorer — it shows individual transactions and address labels. Our system performs a BFS walk across the transaction graph, identifying all wallets reachable within a configurable hop depth. It then checks each against a VASP registry, computes a four-dimensional confidence score, runs a 10-signal risk engine, classifies the wallet into 11 behavioral archetypes, and produces an explainable attribution result with a PDF report. The output is structured for investigators, not for casual blockchain browsing.

**HONEST LIMITATION:** Etherscan has far more data, more chains, and more address labels. Our VASP coverage in a default deployment is currently limited to 10 addresses from demo_vasps.csv. The architecture is designed to load accounts.csv (113k+ Ethereum addresses) when that file is placed in the data/ directory, but it is not included in the repository.

---

### Q2: How do you know an address belongs to a VASP?

**SHORT ANSWER:** From a labelled address dataset (accounts.csv) designed to hold 113k+ Ethereum addresses. In practice, the system currently loads demo_vasps.csv with 10 curated exchange addresses, since accounts.csv is not in the repository.

**TECHNICAL ANSWER:** The VASP registry is loaded at startup from a CSV of labelled Ethereum addresses. The code in known_vasps.py first attempts to load accounts.csv (designed for 113k+ addresses sourced from the Dune/Etherscan community dataset). When accounts.csv is absent (it is gitignored and not in the repository), the system falls back to demo_vasps.csv with 10 well-known exchange addresses. In a default deployment, only 10 addresses are available. Each label carries an evidence quality tier: high (OFAC/government sources), medium (community dataset), or low (single unverified source).

**HONEST LIMITATION:** The accounts.csv dataset is not in the repository (gitignored). Without it, only 10 demo addresses are loaded — providing very limited VASP coverage. Even with accounts.csv, labels can become stale if addresses change hands. The system does not verify that a labelled address still belongs to the named VASP.

---

### Q3: Does VASP interaction prove ownership?

**SHORT ANSWER:** No. Interaction does not prove ownership. The system explicitly distinguishes between "interacts with" and "controlled by."

**TECHNICAL ANSWER:** The default relationship_type is "interacts_with" — meaning a fund-flow path exists between the wallet and the VASP. The system upgrades to "controlled_by" only when two conditions are met: (a) the VASP is at hop-1 (direct neighbor), and (b) the wallet shows deposit-wallet behavior (>70% of transactions toward this VASP with <=3 unique receivers). This is a conservative heuristic. The PDF report and API responses both carry explicit legal disclaimers stating that attribution identifies fund-flow relationships and does not establish legal ownership.

**HONEST LIMITATION:** The "controlled_by" heuristic is a simple rule. Real deposit wallets may not meet both criteria. The system cannot distinguish between a user's personal deposit to an exchange and the exchange's own hot wallet.

---

### Q4: Where is the AI/ML?

**SHORT ANSWER:** The current prototype uses explainable rule/graph-based intelligence. ML is part of the planned next-stage architecture.

**TECHNICAL ANSWER:** Levels 1-3 are implemented: BFS graph traversal, 18-feature behavioral vector extraction, and a 4-component rule-based confidence scorer. The feature vector is structured and normalized specifically to feed into ML models (XGBoost/LightGBM) in Level 4 without any schema changes. The roadmap shows Levels 4-8 as future work: ML-based candidate ranking, wallet clustering (DBSCAN), graph embeddings (node2vec/GraphSAGE), and eventually graph neural networks. No trained ML model currently exists in the codebase.

**HONEST LIMITATION:** No ML model is implemented. All scoring is rule-based. This is transparent but less powerful than ML for complex pattern recognition. The ML upgrade path is designed but not built.

---

### Q5: How is confidence calculated?

**SHORT ANSWER:** Four components weighted 40/30/20/10: graph proximity, interaction strength, temporal recency, and evidence quality.

**TECHNICAL ANSWER:**
- **Graph Proximity (40%):** `max(0, 100 - hops * 25) + min(15, (paths-1) * 5)` — closer hops and multiple independent paths increase score
- **Interaction Strength (30%):** `(volume toward VASP / total traced volume) * 100` — a wallet that sent 80% of its ETH to one exchange scores much higher than one with a single dust transaction
- **Temporal Recency (20%):** `100 * exp(-0.02 * days_since_last_tx)` — exponential decay, half-life ~35 days
- **Evidence Quality (10%):** 100 (high/government source), 65 (medium/community dataset), 35 (low/unverified)

All four sub-scores are returned alongside the final confidence value.

**HONEST LIMITATION:** The weights (40/30/20/10) are currently fixed. They were chosen based on domain judgment, not trained on labeled data. An ML-based model in Level 4 could learn optimal weights.

---

### Q6: How do you prevent false attribution?

**SHORT ANSWER:** Conservative defaults, explainable scores, relationship_type taxonomy, and evidence quality tiers.

**TECHNICAL ANSWER:** Three safeguards: (1) The default claim is "interacts with," not "controlled by." (2) The confidence score is deliberately bounded — minimum 5.0, maximum 100.0 — to prevent extreme values. (3) Evidence quality is explicitly reported: high (OFAC/government), medium (community dataset), low (unverified). The PDF report carries a legal disclaimer. The system does not assert ownership or criminality — it presents investigative leads with their confidence and evidence provenance.

**HONEST LIMITATION:** Label datasets can be stale. An address labelled as "Binance" may now belong to a different entity. The system does not verify label freshness.

---

### Q7: How does it handle mixers/bridges?

**SHORT ANSWER:** Mixers and bridges are in a curated high-risk registry. Interaction triggers risk flags and laundering typology detection.

**TECHNICAL ANSWER:** The high_risk_addresses.py module contains ~33 curated addresses across 5 categories: mixers (Tornado Cash, ChipMixer, Blender.io, Wasabi), sanctions (Lazarus Group/DPRK), ransomware (REvil, Ronin Bridge hacker), darknet (EtherDelta exploit), and bridges (Wormhole, LayerZero, Celer, Optimism, Avalanche, Polygon). When a traced wallet's counterparties intersect with any of these sets, the risk engine fires the corresponding signal (e.g., mixer_interaction at weight 0.75) and tags the typology (e.g., "Layering via Mixer"). Bridge addresses are flagged for cross-chain flow analysis but are not inherently malicious.

**HONEST LIMITATION:** Only ~33 addresses are hardcoded. This is a small subset of all mixers and bridges in operation. The system detects known addresses but not novel mixer contracts.

---

### Q8: How does it scale?

**SHORT ANSWER:** Bounded BFS (60 node cap, configurable hop depth), LRU-cached API calls, modular adapters.

**TECHNICAL ANSWER:** Three design choices keep scaling predictable: (1) The BFS has a `max_nodes_to_expand` cap (default 60) and a `max_hops` limit (default 3), so graph traversal is bounded regardless of wallet complexity. (2) API adapters use `lru_cache` (2048 entries for EVM, 512 for Tron/Bitcoin) to avoid redundant calls. (3) Chain adapters are independent modules — adding a chain doesn't affect existing ones. Request delays (220-500ms per chain) and exponential-backoff retry prevent API rate limit cascades.

**HONEST LIMITATION:** The in-memory case store doesn't scale across restarts or multiple users. For production, PostgreSQL is needed. The 60-node cap means very deep money-laundering chains may be truncated.

---

### Q9: What happens when the address is unlabeled?

**SHORT ANSWER:** The wallet is classified based on behavioral heuristics. If no VASP is found within the hop depth, the system reports that explicitly.

**TECHNICAL ANSWER:** If an address has no VASP label, the classifier falls through to behavioral analysis: fan-out patterns (hot wallet), narrow counterparty sets (deposit wallet), equal-value transactions (potential mixer), or "unknown wallet" if nothing matches. If no VASP match is found within the hop depth, the trace result includes an explicit note: "No known-VASP match found within the searched hop depth. Try increasing max_hops or ensure the VASP registry contains addresses this wallet's network touches." The graph visualization still shows all encountered wallets regardless of label status.

**HONEST LIMITATION:** Unlabeled wallets produce weaker results. Without VASP labels, the system can show the graph and risk profile but cannot attribute to a specific exchange.

---

### Q10: What chains are currently supported?

**SHORT ANSWER:** Five chains — Ethereum, BNB Chain, Polygon, Tron, and Bitcoin.

**TECHNICAL ANSWER:** Ethereum, BSC, and Polygon use the EVM adapter via Etherscan v2 API (chainid parameters 1, 56, 137). Tron uses the TronGrid REST API. Bitcoin uses the Blockstream.info public API (no key required). Each chain has address format validation, a native token divisor for value normalization, and a distinct explorer URL. Chain metadata is defined in chains.py.

**HONEST LIMITATION:** VASP label coverage is Ethereum-primary. BSC, Polygon, Tron, and Bitcoin data fetching works, but the VASP registry is Ethereum-only. VASP matching on non-Ethereum chains relies on the 10-address demo fallback.

---

### Q11: What happens when APIs fail?

**SHORT ANSWER:** Exponential-backoff retry (3 attempts), then graceful degradation. If no API key is configured, the system returns deterministic demo data.

**TECHNICAL ANSWER:** The blockchain client implements `_request_with_retry` — 3 attempts with exponential backoff (1s -> 2s -> 4s) on status codes 429, 500, 502, 503, 504. It respects Retry-After headers. If all retries fail, a `BlockchainClientError` is raised, caught in the trace endpoint, and returned as HTTP 502. If no Etherscan API key is configured, the `/api/trace` endpoint automatically returns a demo trace result with a `_demo_mode` flag and a warning message. The UI displays a demo mode notice when synthetic data is returned.

**HONEST LIMITATION:** Demo mode returns the same synthetic result regardless of input address — it doesn't reflect the actual wallet's transaction history.

---

### Q12: How reliable is the data?

**SHORT ANSWER:** Blockchain data from public APIs is reliable for transaction existence but not for address ownership. Label data is community-sourced and may be stale.

**TECHNICAL ANSWER:** Transaction data from Etherscan, TronGrid, and Blockstream reflects the immutable blockchain record — transaction hashes, addresses, values, and timestamps are objectively verifiable on-chain. However, address labels (VASP names, risk categories) come from community-maintained datasets and curated registries. These labels can become stale if addresses change hands. The system mitigates this with evidence quality tiers (high/medium/low) and a legal disclaimer in the PDF report.

**HONEST LIMITATION:** No real-time label verification. No automated feed updates for the high-risk registry. The ~33 hardcoded addresses require manual updates.

---

### Q13: How could law enforcement actually use this?

**SHORT ANSWER:** As an investigative lead tool — not as evidence. It structures blockchain data into a format investigators can act on.

**TECHNICAL ANSWER:** A cybercrime investigator receives a wallet address from a victim FIR. They enter it into the system. Within seconds, they have: (1) a transaction graph showing where funds flowed, (2) the nearest VASP with a confidence score and explanation, (3) a risk assessment flagging mixer/sanctions/ransomware links, (4) a wallet classification, and (5) a PDF report formatted for case documentation. The SAHYOG routing recommendation tells them which exchange to send a KYC/freeze request to and with what urgency. The explainable scoring means they can justify the lead in court. The system is designed as a force multiplier for investigators who currently do this work manually across multiple tools.

**HONEST LIMITATION:** No real SAHYOG portal integration yet — the submission is a demo stub. No authentication, no case management, no audit trail. This is a prototype demonstrating the intelligence pipeline.

---

### Q14: What is the biggest limitation?

**SHORT ANSWER:** The VASP dataset is Ethereum-primary. accounts.csv (113k addresses) is not in the repository (gitignored), so the demo fallback of 10 addresses is the only dataset that runs by default.

**TECHNICAL ANSWER:** The single biggest limitation is VASP label coverage. The system's core value proposition is VASP attribution, but the labelled address dataset (accounts.csv, 113k+ Ethereum addresses) is gitignored and absent from the repository. Without it, the system falls back to demo_vasps.csv with only 10 addresses. This means VASP matching returns zero or very few results in a default deployment. Secondary limitations include: no real ML model, in-memory-only storage, no authentication, and no live data feeds for the high-risk registry.

**HONEST LIMITATION:** Both CSV files are gitignored. In a fresh clone, no VASP dataset is present until one is manually placed. Even with accounts.csv, labels can become stale if addresses change hands. The system does not verify that a labelled address still belongs to the named VASP. The demo fallback of 10 addresses provides very limited coverage.

---

### Q15: What would you build next?

**SHORT ANSWER:** Three things: (1) populate accounts.csv for full VASP coverage, (2) implement ML-based ranking on the existing feature vectors, (3) add database persistence and multi-user support.

**TECHNICAL ANSWER:** Priority 1 is data: obtain and integrate the accounts.csv VASP dataset for full coverage, then expand to per-chain label datasets for BSC, Polygon, Tron, and Bitcoin. Priority 2 is ML: implement XGBoost/LightGBM candidate ranking using the existing 18-feature vectors (Level 4), then wallet clustering with DBSCAN (Level 5). Priority 3 is production readiness: PostgreSQL persistence, JWT authentication, live OFAC SDN feed integration, and real SAHYOG portal API integration.

**HONEST LIMITATION:** These are planned, not implemented. The roadmap exists but none of Level 4+ features are coded.

---

## 13. Visual Design Blueprint

### Overall Direction

**Inspiration:** Cybersecurity dashboards, blockchain intelligence platforms, digital forensics interfaces, intelligence command centers.

**Color Palette:**
- Background: `#0a0e17` (near-black navy) to `#111827` (dark slate)
- Panel/card: `#111d2e` (dark navy) with `#1e293b` borders
- Primary accent: `#4f8cff` (restrained blue)
- Success/green: `#22c55e` (VASP matches, low risk)
- Warning/amber: `#eab308` (medium risk, demo mode)
- Danger/red: `#ef4444` (high risk, mixers, sanctions)
- Text primary: `#f1f5f9` (near-white)
- Text secondary: `#94a3b8` (muted blue-gray)
- Text tertiary: `#64748b` (darker muted)

**Typography:**
- Headings: Inter 700 (bold)
- Body: Inter 400 (regular)
- Mono (addresses, hashes): JetBrains Mono 400
- Minimum font size: 10pt

**Visual Elements:**
- Thin 1px borders (`#1e293b`) for card separation
- Subtle glass-panel effect (semi-transparent backgrounds)
- No heavy gradients — keep it flat and technical
- Accent color used sparingly: only for CTAs, active states, and data highlights
- Transaction-node motifs: small circle/diamond/hexagon shapes for graph-related slides
- Chain color coding consistent with the app (ETH=#627EEA, BSC=#F3BA2F, Polygon=#8247E5, Tron=#EF0027, BTC=#F7931A)

### Per-Slide Visual Specifications

| Slide | Primary Graphic | Secondary Graphic | Layout | Density |
|---|---|---|---|---|
| 1 — Title | Stylized transaction graph (target -> hops -> VASP) | Team name, SIH branding | Centered, single focal point | Low |
| 2 — Solution | Vertical pipeline flow (6 steps) | 4 differentiator cards + value prop | Left: pipeline, Right: differentiators | Medium |
| 3 — Technical | Layered architecture diagram | Technology badges | Full-width layered stack | Medium-high |
| 4 — Feasibility | Three-column layout | Roadmap timeline strip | Columns: Feasibility / Challenges / Mitigations | Medium |
| 5 — Impact | Two-column workflow comparison | Benefit grid + growth timeline | Top: comparison, Middle: benefits, Bottom: timeline | Medium |
| 6 — References | Categorized reference list | QR code to GitHub | Single column, structured | Low |

### What NOT to Place on Slides

- Bitcoin coin imagery or crypto trading charts
- Generic "blockchain network" stock illustrations
- Paragraphs of text (use bullet points only)
- More than 6-8 items per slide
- Faded/low-contrast text that's hard to read
- Emoji in titles or headings
- Gradient-heavy backgrounds that reduce readability

---

## 14. Claims We Must NOT Make

The following claims are explicitly prohibited in the presentation:

| Forbidden Claim | Why | What to Say Instead |
|---|---|---|
| "100% accurate" | Confidence scores are heuristics, not proofs | "Explainable confidence scoring with conservative attribution language" |
| "First ever" / "World's first" | Not verifiable | "Investigator-first VASP attribution with explainable scoring" |
| "AI-powered" / "Machine learning" | No ML model is implemented | "Rule/graph-based intelligence; ML-ready feature vectors for future enhancement" |
| "Government deployed" / "Used by I4C" | No deployment exists | "Designed for integration with SAHYOG portal (I4C)" |
| "Proves criminality" | System explicitly does not do this | "Identifies investigative leads; does not establish guilt" |
| "Proves ownership" | System explicitly distinguishes interaction from ownership | "Traces fund flows; attribution uses 'interacts with' by default" |
| "Reduces investigation time by X%" | No benchmarking exists | "Automates repetitive tracing; structures fragmented evidence" |
| "Real-time monitoring" | Not implemented | "Session-based investigation; real-time monitoring is future scope" |
| "Live sanctions feed" | Registry is hardcoded | "Curated high-risk registry with government-source addresses" |
| "Database-backed" | Storage is in-memory | "Session-scoped in-memory store; PostgreSQL planned for production" |
| "113,000 VASPs in production" | accounts.csv is gitignored and absent from repo | "VASP registry supports 113k+ addresses when accounts.csv is loaded; 10-address demo fallback available by default" |

---

## 15. Final Presentation Checklist

Before the final presentation:

- [ ] Exactly 6 official slides matching SIH format
- [ ] Each slide has Layer 1 (on-slide text), Layer 2 (visual spec), Layer 3 (speaker notes)
- [ ] No slide contains paragraph-heavy content — all points, not prose
- [ ] Strong narrative from problem -> pipeline -> differentiation -> feasibility -> impact -> references
- [ ] Technical depth is present but accessible — speaker notes carry the depth, slides carry the points
- [ ] Innovation section clearly separates what's implemented vs. planned
- [ ] Current vs. Future matrix is accurate to the codebase
- [ ] No fake ML claims (Levels 4-8 explicitly marked as planned/future)
- [ ] No fake ownership or government integration claims
- [ ] No invented statistics, percentages, or benchmarks
- [ ] Demo story matches the actual application (demo fixture addresses, endpoint, results)
- [ ] Visual direction is premium (dark, restrained, technical — not crypto trading aesthetic)
- [ ] Judge Q&A is honest about limitations
- [ ] Claims We Must NOT Make section is reviewed and none of those claims appear in the slides
- [ ] Document can be directly handed to a designer/PPT creator to build the final deck
- [ ] Team name and team ID placeholders are clearly marked for replacement

---

## Appendix: Quick Reference Facts

### What Is Implemented (Levels 1-3)

| Component | Detail |
|---|---|
| Backend | FastAPI, 11 endpoints, uvicorn |
| Chains | 5 (Ethereum, BSC, Polygon, Tron, Bitcoin) |
| VASP Registry | 10-address demo dataset active; architecture supports 113k+ accounts.csv (Ethereum) |
| High-Risk Registry | ~33 curated addresses (mixers, sanctions, ransomware, darknet, bridges) |
| Graph Engine | BFS traversal, hop-limited (default 3), node-capped (60) |
| Confidence Scoring | 4-component weighted (40/30/20/10), all sub-scores returned |
| Risk Engine | 10 signals, 9 laundering typologies, weighted scoring |
| Wallet Classifier | 11 categories, rule-based with behavioral heuristics |
| Feature Extractor | 18-feature behavioral vector (graph, value, temporal, exposure, structuring) |
| Relationship Types | interacts_with (default), controlled_by (heuristic upgrade) |
| Evidence Quality | high/medium/low tiers |
| Frontend | 5-panel dashboard, vis-network graph, dark cybersecurity theme |
| PDF Report | reportlab, A4, full breakdown with legal disclaimer |
| SAHYOG | Routing recommendation + demo submission stub |
| Tests | 7 offline tests (FakeClient), all passing |
| Demo Mode | Deterministic fixture for offline demonstration |

### What Is Planned (Levels 4-8)

| Level | Feature | Status |
|---|---|---|
| 4 | ML candidate ranking (XGBoost/LightGBM) | Feature vectors ready, model not built |
| 5 | Wallet clustering (DBSCAN) | Planned |
| 6 | Graph embeddings (node2vec/GraphSAGE) | Planned |
| 7 | Multi-chain cross-chain flow analysis | Planned |
| 8 | Agentic investigation + RAG | Planned |

### Demo Fixture Output (deterministic)

| Field | Value |
|---|---|
| VASP Match | Binance Hot Wallet (0x28c6c...) |
| Hops | 2 |
| Confidence | 78.5% |
| Relationship Type | interacts_with |
| Risk Level | MEDIUM (score 35) |
| Risk Flag | mixer_proximity |
| Typology | Proximity to mixer (Tornado Cash) |
| Classification | Hot Wallet |
| Transactions Scanned | 6 |
| Total Volume | 1.25 ETH |
| Graph | 4 nodes, 3 edges |
| SAHYOG Action | Voluntary disclosure inquiry to Binance Hot Wallet |
