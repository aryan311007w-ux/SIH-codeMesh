# CryptoGuard AI — 3-Minute SIH Hackathon Demo Guide

**Target Audience:** Smart India Hackathon Jury / Ministry of Home Affairs / I4C Evaluators  
**Goal:** Deliver a compelling, flawless, zero-failure demonstration in under 3 minutes.  
**Platform URL:** `http://127.0.0.1:8000`  

---

## Pre-Demo Checklist
- [x] Run `run.bat` or `python -m uvicorn main:app --reload`
- [x] Open `http://127.0.0.1:8000` in your browser (press `F11` for clean full-screen presentation)
- [x] Verify the yellow **`DEMO MODE`** pill is active in the top-right header

---

## 3-Minute Demonstration Script

### Minute 0:00 – 0:30 | The Platform & Problem Context
**What to show:**
- Start on the **Dashboard** (`http://127.0.0.1:8000`).
- Point to the **Workflow Ribbon** showing the 7-stage pipeline:
  $$\text{Target} \to \text{Trace Graph} \to \text{Behaviour} \to \text{Intermediaries} \to \text{VASP Attribution} \to \text{Risk} \to \text{Section 91 Requisition}$$
- Point to the KPI counters: Active investigations, high-risk targets, and FIU-IND registered entities.

**What to say:**
> *"Respected jury members, in crypto-financial crimes, money rarely sits in the initial scam wallet. Criminals rapidly layer funds through intermediary mules and peel chains before cashing out at Virtual Asset Service Providers (VASPs). Existing tools are either opaque black boxes or unaware of the Indian regulatory framework. We present **CryptoGuard AI**, an AI-powered blockchain forensics and VASP attribution platform designed specifically for law enforcement agencies."*

---

### Minute 0:30 – 1:00 | Launching the Investigation
**What to show:**
- Click **"⚡ Load Demo Case (NCRP-2026-849102)"** on the quick bar (or click **"+ New Investigation"** and select demo target).
- The platform instantly traverses the multi-hop graph and opens the **Investigation Workspace**.
- Highlight the target banner: Target wallet `0x742d...f44e`, Ethereum Mainnet, Risk: `82/100 HIGH RISK`, FIU-IND Target Hit.

**What to say:**
> *"Let's investigate an active cyber fraud complaint reported on the NCRP portal under FIR-2026/89. In one click, CryptoGuard AI ingests the transaction graph, computes multi-hop counterparty paths, and isolates 3 VASP cashout destinations. Notice that our deterministic demo mode guarantees 100% offline reproducibility without external API quota issues."*

---

### Minute 1:00 – 1:40 | Interactive Transaction Graph & Node Inspector
**What to show:**
- Click the **"🕸️ Transaction Graph"** tab.
- Show the visual layout: Target (blue star), Mule accounts (amber dots), Tornado Cash Mixer (red hexagon), and Exchange deposit hubs (green diamonds).
- Click on **Mule Account Alpha** (`0x11112222...`):
  - The **Node Inspector Drawer** slides open on the right.
  - Show direct transfers: `3.50 ETH IN` from suspect, `3.45 ETH OUT` to CoinDCX.
- Use the toolbar filter: change dropdown from **Show All Nodes** to **VASPs Only**, then back to **All**.

**What to say:**
> *"Our interactive graph engine isn't just decorative. When I click on this intermediary node, the Inspector Drawer reveals its role: a pass-through mule account that received 3.50 ETH and forwarded 3.45 ETH directly to CoinDCX within 14 minutes. We can filter nodes by archetypes to instantly separate mixers from exchanges."*

---

### Minute 1:40 – 2:15 | Core SIH Innovation: Explainable VASP Attribution
**What to show:**
- Click the **"🏦 VASP Attribution"** tab.
- Point to the multi-dimensional attribution formula:
  $$\text{Score} = 40\% \text{ Proximity} + 30\% \text{ Volume} + 20\% \text{ Recency} + 10\% \text{ Provenance}$$
- Show the top match: **CoinDCX (Neblio Technologies)** — `84.5% Confidence (Strong Evidence)`, `FIU-IND Registered`.
- Scroll down to the **"Explain Attribution: Hop-by-Hop Forensic Walk"**:
  - Show the visual card sequence: $\text{Suspect} \xrightarrow{\text{Hop 1}} \text{Mule Alpha} \xrightarrow{\text{Hop 2}} \text{CoinDCX}$.
  - Point out transaction hashes, block numbers, and the automated explanation.
- Click on **Binance Hot Wallet 6** to show the 3-hop peel chain path.

**What to say:**
> *"Here is our core innovation: **Explainable VASP Attribution**. Unlike commercial tools that offer opaque labels, CryptoGuard AI breaks down confidence into graph proximity, flow volume, and verified provenance. Furthermore, the 'Explain Attribution' engine generates an auditable, hop-by-hop factual explanation that an investigating officer can defend in court without mathematical ambiguity."*

---

### Minute 2:15 – 2:40 | Indian Cybercrime Response (Section 91 CrPC Notice) & AI Copilot
**What to show:**
- Click the **"🏛️ Cybercrime Response"** tab.
- Click **"Generate Section 91 CrPC Notice"**.
- Show the formal legal requisition compiled in real time for **CoinDCX Nodal Compliance**.
- Click the **"🤖 Copilot"** button on the top right.
- In the slide-out drawer, click the chip: **"Why CoinDCX?"** or **"What are the strongest risk indicators?"**.
- Show the instant, factual response generated by the Deterministic Intelligence Engine.

**What to say:**
> *"To ensure immediate real-world utility for Indian LEAs, we built the Cybercrime Response workflow. With one click, the system compiles a formal notice under Section 91 of the Code of Criminal Procedure (or Section 94 BNSS 2023), requesting KYC documents, bank account links, IP logs, and an immediate asset freeze under Section 102 CrPC. Our built-in AI Copilot assists the investigator with natural language queries without fabricating unverified claims."*

---

### Minute 2:40 – 3:00 | PDF Report & Conclusion
**What to show:**
- Click **"📄 PDF Report"** in the workspace header.
- The browser opens/downloads the formal, publication-ready investigation report.
- Briefly show the headers: Executive Summary, Observed vs Derived Evidence, Timeline Table, and Statutory Notice Attachment.

**What to say:**
> *"Finally, CryptoGuard AI generates a court-admissible forensic PDF report distinguishing observed ledger evidence from derived analysis. The platform is lightweight, persists cases in a local SQLite database, and runs 100% offline in demo mode or live across 5 blockchains. Thank you, and we welcome your questions."*
