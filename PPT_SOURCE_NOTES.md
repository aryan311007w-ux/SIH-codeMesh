# CRYPTOGUARD AI — PPT SOURCE NOTES & TECHNICAL TRACEABILITY
**Problem Statement ID:** SIH26182  
**Problem Statement:** *Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs*  
**Document Purpose:** Source mapping, technical claim verification, and architecture traceability for `FINAL_SIH26182_CryptoGuard_AI_6_SLIDE.pptx`.  
**Repository Branch:** `sih26182-cryptoguard`  
**Verified Slide Count:** Exactly 6 Slides (PASS)

---

## SLIDE 1 — TITLE PAGE & PROJECT BRIEF

### 1. Slide Objective & Structure
- **Header:** Smart India Hackathon 2026 official branding with Ministry of Education / AICTE logo (left) and SIH 2026 logo (right).
- **Core Identifiers:**
  - Problem Statement ID: `SIH26182`
  - Problem Statement Title: `Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs`
  - Theme: `Blockchain & Cybersecurity`
  - PS Category: `Software`
  - Team ID: `To be finalized on SIH Portal` (Standard SIH placeholder convention)
  - Team Name (Registered): `CodeMesh` (Derived from project origin repository `SIH-codeMesh`)
  - Solution Name: `CryptoGuard AI`
- **Right Showcase Card:** Executive brief highlighting multi-chain tracing, 4-factor attribution, 10-signal AML risk scoring, and statutory Section 91 CrPC notice generation.

### 2. Source Repository Mapping
- [`docs/deliverables/SRS.md`](file:///d:/SIH%202/docs/deliverables/SRS.md) — System Requirements Specification & problem scope definition.
- [`docs/deliverables/PRD.md`](file:///d:/SIH%202/docs/deliverables/PRD.md) — Product Requirements Document for Indian Cybercrime Cells.
- [`backend/main.py`](file:///d:/SIH%202/backend/main.py) — Root API metadata (`product: "CryptoGuard AI"`, `tagline: "AI-Powered Blockchain Investigation & VASP Attribution Platform"`).
- [`README.md`](file:///d:/SIH%202/README.md) — Project summary, mission, and operational stakeholders.

### 3. Verified Technical Claims
- Problem statement text matches the official SIH 2026 portal definition verbatim.
- Target stakeholders correctly identified as Indian Law Enforcement Agencies (LEAs), Indian Cybercrime Coordination Centre (I4C), Financial Intelligence Unit (FIU-IND), and state cyber cells.
- Solution scope restricted to unhosted wallet attribution, transaction graph analysis, risk scoring, and legal notice generation.

### 4. Current vs. Future Functionality
- **Current (Implemented):** Complete software MVP with persistent SQLite store, multi-chain adapters, 4-factor scoring algorithm, and PDF export.
- **Future (Roadmap):** Direct single-sign-on (SSO) integration with police intranet intranets and production HSM-secured keychains.

---

## SLIDE 2 — IDEA / PROPOSED SOLUTION (`CryptoGuard AI`)

### 1. Slide Objective & Structure
- 4 Structured Content Blocks:
  1. `Blockchain Investigation Engine`: Multi-chain support, BFS traversal, Vis.js graph, Node Inspector.
  2. `VASP Attribution Engine`: Curated registry lookup, 4-factor confidence formula, strict legal distinction.
  3. `Risk & Forensic Intelligence`: 10-signal AML risk engine, typologies (peel chains, mixers), Forensic Copilot.
  4. `Investigation & Cybercrime Response`: Evidence Locker, chronological timeline, Section 91 CrPC notice, court-ready PDF.
- 2 Live UI Screenshots:
  - Screenshot 1: Interactive Vis.js Multi-Hop Transaction Graph (`cryptoguard_screenshot_graph.png`).
  - Screenshot 2: VASP Attribution Console (`cryptoguard_screenshot_vasp.png`).
- Linear Flow Banner:
  `UNKNOWN WALLET -> BLOCKCHAIN ADAPTERS -> MULTI-HOP GRAPH -> WALLET INTEL -> VASP ATTRIBUTION -> RISK SCORING -> EVIDENCE + REPORT`

### 2. Source Repository Mapping
- [`backend/tracer.py`](file:///d:/SIH%202/backend/tracer.py) — Directed BFS graph traversal algorithm (`trace_wallet` lines 97–250).
- [`backend/vasp_registry.py`](file:///d:/SIH%202/backend/vasp_registry.py) — Curated directory of FIU-IND reporting entities (CoinDCX, WazirX, ZebPay, CoinSwitch, Mudrex) and global exchanges.
- [`backend/risk_engine.py`](file:///d:/SIH%202/backend/risk_engine.py) — 10-signal weighted risk scoring engine (`compute_risk_score`).
- [`backend/copilot.py`](file:///d:/SIH%202/backend/copilot.py) — Hybrid Forensic Copilot (Deterministic NLP engine + optional LLM integration).
- [`backend/demo_fixture.py`](file:///d:/SIH%202/backend/demo_fixture.py) — Deterministic synthetic dataset for NCRP complaint `NCRP-2026-849102`.
- [`backend/static/js/app.js`](file:///d:/SIH%202/backend/static/js/app.js) — Client-side Vis.js graph physics rendering, Node Inspector drawer, and tab controllers.

### 3. Screenshots & Visual Assets Used
- `cryptoguard_screenshot_graph.png`: Real live capture from the running platform showing the 12-node force-directed transaction graph with mule accounts, mixer nodes, and VASP deposit aggregators.
- `cryptoguard_screenshot_vasp.png`: Real live capture showing CoinDCX (84.5% confidence), Binance (73.8%), Kraken (58.2%), and the 2-hop sequence walk with transaction hashes.

### 4. Verified Technical Claims
- The 4-factor scoring formula matches lines 215–225 of `tracer.py`:
  $$\text{Confidence} = 0.40 \cdot \text{Proximity} + 0.30 \cdot \text{Volume} + 0.20 \cdot \text{Recency} + 0.10 \cdot \text{Trust}$$
- Strict evidentiary separation of `interacts_with` vs `controlled_by` is enforced in code (only 1-hop deposit wallets receive `controlled_by`).
- Copilot is factually designated as an **"Explainable Rule Engine + Optional LLM Integration"** (NO false "deep neural network" claims).
- Demo Mode is prominently labeled as synthetic demonstration data.

### 5. Current vs. Future Functionality
- **Current:** Deterministic 4-factor scoring, 12-node synthetic demo case, real-time node inspector, and rule-based Copilot.
- **Future:** Autonomous continuous mempool monitoring and automated darknet clustering.

---

## SLIDE 3 — TECHNICAL APPROACH & PROTOTYPE

### 1. Slide Objective & Structure
- 8-Phase Architecture Methodology Table:
  1. `Input`: Suspect address, chain selector, max hops (1–6).
  2. `Blockchain Adapters`: Etherscan v2, TronGrid, Blockstream REST clients.
  3. `Normalization`: Standardized address checksum, wei/satoshi conversion, ERC-20 parsing.
  4. `Graph Analysis`: BFS traversal, cycle pruning, Vis.js graph topology.
  5. `VASP Attribution`: Curated registry matching, 4-factor multi-dimensional scoring.
  6. `Risk & AML Engine`: 10-signal explainable risk calculation (0–100 score).
  7. `Forensic Workspace`: Chronological timeline, SHA-256 evidence locker, Node Inspector.
  8. `Response & Export`: Section 91 CrPC notice generator, ReportLab PDF export, SAHYOG-ready stub.
- Right Sidebar: Full-Stack Technology Architecture & Verified Repository Links.

### 2. Source Repository Mapping
- [`backend/chains.py`](file:///d:/SIH%202/backend/chains.py) — Chain configurations and address validators for Ethereum, BSC, Polygon, Tron, and Bitcoin.
- [`backend/blockchain_client.py`](file:///d:/SIH%202/backend/blockchain_client.py) — Multi-chain REST adapters (`EVMAdapter`, `TronAdapter`, `BitcoinAdapter`).
- [`backend/feature_extractor.py`](file:///d:/SIH%202/backend/feature_extractor.py) — Velocity, burstiness, structuring, and fan-out metric extractors.
- [`backend/wallet_classifier.py`](file:///d:/SIH%202/backend/wallet_classifier.py) — Behavioral archetype classification rules.
- [`backend/database.py`](file:///d:/SIH%202/backend/database.py) — SQLite persistent schema with 7 indexed tables (`investigations`, `nodes`, `edges`, `vasp_matches`, `risk_signals`, `evidence_items`, `timeline_events`).
- [`backend/report.py`](file:///d:/SIH%202/backend/report.py) — ReportLab binary PDF generator.
- [`backend/static/js/vis-network.min.js`](file:///d:/SIH%202/backend/static/js/vis-network.min.js) — Locally bundled Vis.js network visualization library.

### 3. Verified Technical Claims
- All 5 stated blockchains (Ethereum, BSC, Polygon, Tron, Bitcoin) have active adapter code in `chains.py` and `blockchain_client.py`.
- Frontend has zero external CDN dependencies (fonts and Vis.js are local).
- Backend executes natively via FastAPI/Uvicorn on Python 3.10+.
- Database is persistent SQLite (`cryptoguard.db`).

### 4. Verified Links
- GitHub: `https://github.com/aryan311007w-ux/SIH-codeMesh` (Matches git remote).
- Website & Demo Video: Clearly marked `To be updated after deployment` (No fabricated URLs).

---

## SLIDE 4 — PROBLEM -> SOLUTION -> FEASIBILITY & VIABILITY

### 1. Slide Objective & Structure
- 3 Structured Columns:
  1. `Operational Challenges`: Rapid fund dissipation, multi-hop obfuscation, cross-chain fragmentation, attribution uncertainty, opaque black-boxes, manual paperwork.
  2. `CryptoGuard AI Solution`: Automated BFS walk, 4-factor scoring, unified multi-chain schema, explainable evidence, 1-click Section 91 notices, tamper-evident PDF reports.
  3. `Feasibility & Scalability Pillars`: Technical Feasibility, Practical Implementability, Sustainable Impact, Scalability by Design.
- Bottom Full-Width Card: `Risk Identification & Mitigation Strategy` (API rate limits, data noise, attribution ambiguity, security hardening).

### 2. Source Repository Mapping
- [`docs/deliverables/PRD.md`](file:///d:/SIH%202/docs/deliverables/PRD.md) — Operational friction analysis of Indian cybercrime police stations.
- [`backend/high_risk_addresses.py`](file:///d:/SIH%202/backend/high_risk_addresses.py) — OFAC sanctions, Tornado Cash, Blender.io, and bridge contracts.
- [`backend/main.py`](file:///d:/SIH%202/backend/main.py) — Notice generation (`/api/sahyog/notice`) and demo fallback mechanisms.

### 3. Verified Technical Claims
- Technical feasibility: Zero GPU/heavy ML requirements allows execution on standard investigator laptops.
- Practical implementability: Deterministic Demo Mode works 100% offline without requiring paid API keys.
- Scalability: SQLite schema is designed for 1-to-1 migration to enterprise PostgreSQL.
- Risk mitigations accurately reflect the code's fallback behaviors.

### 4. Current vs. Future Functionality
- **Current:** Single-tenant investigator dashboard with SQLite storage and Section 91 notice generation.
- **Future:** Multi-tenant police station hierarchy with institutional JWT authentication and role-based access control (RBAC).

---

## SLIDE 5 — IMPACT AND BENEFITS

### 1. Slide Objective & Structure
- 4 Stakeholder Benefit Cards:
  1. `Law Enforcement & Investigators`: Rapid preliminary tracing, unified graph, structured evidence locker.
  2. `Cybercrime Cells & Prosecution`: Automated Section 91 CrPC notices, court-defensible mathematical confidence, verified PDF reports.
  3. `VASPs & Compliance Officers`: Clear hop paths, transaction hashes, timestamps, and reduced nodal turnaround.
  4. `Financial & Legal Ecosystem`: Lowers recovery friction, establishes open attribution benchmark, multi-chain extensibility.
- Bottom 6-Grid Container: `Long-Term Systemic Effects on National Blockchain Forensics`:
  1. Accelerated Asset Freezing
  2. Standardized Digital Requisitions
  3. Cross-Chain Investigative Parity
  4. Institutional Evidentiary Memory
  5. Low-Cost Station Deployment
  6. National Integration-Ready (I4C / SAHYOG)

### 2. Source Repository Mapping
- [`SIH_PPT_CONTENT.md`](file:///d:/SIH%202/SIH_PPT_CONTENT.md) — Stakeholder value propositions and long-term systemic impact.
- [`docs/presentation_content.md`](file:///d:/SIH%202/docs/presentation_content.md) — Operational benefits for LEAs and compliance nodals.
- [`backend/database.py`](file:///d:/SIH%202/backend/database.py) — Data model supporting persistent cold case re-analysis.

### 3. Verified Technical Claims
- No fabricated percentage improvements (e.g., no fake "99.8% precision" or "95% time savings" claims).
- Benefits focus on structural, workflow, and evidentiary standardization.
- Asset freezing is described as an accelerated operational outcome enabled by fast notices, NOT an automated protocol capability.

---

## SLIDE 6 — RESEARCH AND REFERENCES

### 1. Slide Objective & Structure
- 3 Academic & Regulatory Reference Columns:
  1. `Statutory & Regulatory Frameworks`: FATF Guidance (2021/2023), FIU-IND AML/CFT Guidelines (2023), Section 91 CrPC / Section 94 BNSS, PMLA 2002.
  2. `Blockchain APIs & Forensic Protocols`: Etherscan v2 API, TronGrid Protocol, Blockstream Bitcoin REST API, Vis.js Network Engine.
  3. `Forensic Heuristics & Research Papers`: Meiklejohn et al. (ACM IMC 2013), Friedhelm Victor (Springer 2020), OFAC SDN Sanctions, UNODC Typology Manual.
- Bottom Deliverables & Official Repository Access Bar.

### 2. Source Repository Mapping
- [`docs/deliverables/DATASETS.md`](file:///d:/SIH%202/docs/deliverables/DATASETS.md) — Official registry of APIs, OFAC SDN lists, Tornado Cash routers, and VASP data sources.
- [`backend/vasp_registry.py`](file:///d:/SIH%202/backend/vasp_registry.py) — References to FIU-IND registered reporting entities under PMLA.
- [`backend/high_risk_addresses.py`](file:///d:/SIH%202/backend/high_risk_addresses.py) — References to OFAC sanctions and mixer contracts.

### 3. Verified Citations & Absence of Hallucinations
- All cited laws (PMLA 2002, CrPC Section 91, BNSS Section 94) are genuine Indian statutes governing digital evidence requisition.
- All cited papers (Meiklejohn 2013, Victor 2020) are authentic, peer-reviewed computer science literature on blockchain clustering heuristics.
- All cited APIs (Etherscan, TronGrid, Blockstream) match the actual adapter endpoints implemented in `blockchain_client.py`.
- No fake research papers, fabricated author names, or broken links were included.

---

## SUMMARY OF VERIFICATION CHECKS

| Check Item | Target Requirement | Verified Status |
|---|---|---|
| **Slide Count** | EXACTLY 6 slides | **PASS (6 Slides)** |
| **Problem Statement ID** | SIH26182 | **PASS (SIH26182)** |
| **Team Name** | CodeMesh (from project origin) | **PASS (CodeMesh)** |
| **AI Copilot Description** | Rule Engine + Optional LLM | **PASS (Accurate)** |
| **SAHYOG Integration** | Workflow / Integration Point | **PASS (Accurate)** |
| **Asset Freezing** | Not claimed as automatic | **PASS (Accurate)** |
| **Demo Mode Data** | Labeled synthetic demo data | **PASS (Accurate)** |
| **VASP Count** | Curated registry (21 VASPs) | **PASS (Accurate)** |
| **Metrics** | No invented statistics | **PASS (Accurate)** |
| **Live UI Screenshots** | Embedded on Slide 2 | **PASS (Real Captures)** |
| **Template Compliance** | Preserves official SIH logos/footers | **PASS (100% Intact)** |
| **Code Modification** | Application code untouched | **PASS (Untouched)** |
