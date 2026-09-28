# CryptoGuard AI — SIH 2026 Presentation Content

**Problem Statement Code:** SIH26182  
**Problem Statement Title:** Automated Attribution of Unknown Cryptocurrency Wallets to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs  
**Product Name:** CryptoGuard AI  
**Tagline:** AI-Powered Blockchain Investigation & VASP Attribution Platform  

---

### Slide 1: Problem Statement + Team/Product
- **Title:** CryptoGuard AI: Automated Blockchain Forensics & VASP Attribution Platform
- **Key Points:**
  - **Problem Statement (SIH26182):** Automated attribution of unhosted cryptocurrency wallets to nearest Virtual Asset Service Providers (VASPs).
  - **Core Mission:** Empower Indian Law Enforcement Agencies (LEAs) and compliance officers to trace illicit fund flows and requisition KYC records.
  - **Product Identity:** CryptoGuard AI — an explainable, auditable, and regulatory-aligned investigation console.
  - **Target Stakeholders:** Indian Cybercrime Coordination Centre (I4C), Financial Intelligence Unit (FIU-IND), State Cyber Cells.
- **Recommended Screenshot / Diagram:**
  - Platform brand banner with shield/radar emblem, followed by the 7-stage workflow pipeline from suspect wallet to Section 91 CrPC requisition notice.
- **Presenter Script:**
  > *"Good morning respected jury members. We are presenting **CryptoGuard AI**, an AI-powered blockchain forensics and VASP attribution platform built for Smart India Hackathon problem statement SIH26182. Our platform addresses the critical challenge faced by law enforcement: automatically identifying which crypto exchanges hold the proceeds of crime, while maintaining full forensic explainability and alignment with Indian legal frameworks."*

---

### Slide 2: Problem & Existing Gap
- **Title:** The Forensic Gap in Crypto Financial Crime Investigation
- **Key Points:**
  - **Rapid Fund Dissipation:** Illicit crypto assets rarely remain in the initial target wallet; funds are structured across multiple hops within minutes.
  - **Opaque Black-Box Tools:** Commercial analytics tools provide proprietary risk scores without explainable evidence or mathematical transparency.
  - **Regulatory Disconnect:** Existing tools do not map to domestic Indian regulations (PMLA, FIU-IND reporting entities, Section 91 CrPC).
  - **High Operational Barrier:** Forensic investigators require actionable legal requisitions, not just abstract cluster graphs.
- **Recommended Screenshot / Diagram:**
  - Flow diagram illustrating a victim deposit being split into peel chains and mules, showing the time gap before an investigator can identify the cashout exchange.
- **Presenter Script:**
  > *"When cyber criminals defraud victims, they don't leave funds stationary. They use peel chains, mule accounts, and mixers to obfuscate origin before exiting into fiat currency through exchanges. Existing commercial solutions present two fatal flaws: they are expensive black boxes that defense attorneys can challenge in court, and they have zero native integration with Indian statutory requisition procedures under the PMLA and CrPC."*

---

### Slide 3: Proposed Solution
- **Title:** Proposed Solution: Automated Multi-Hop VASP Attribution Engine
- **Key Points:**
  - **Multi-Chain Graph Traversal:** Directed Breadth-First Search (BFS) tracking fund flows across EVM chains, Tron, and Bitcoin.
  - **Auditable 4-Factor Scoring:** Attribution confidence derived from graph proximity, interaction volume, temporal recency, and registry provenance.
  - **Forensic Separation:** Strict distinction between verifiable *on-chain evidence* and *derived heuristic analysis* (`interacts_with` vs `controlled_by`).
  - **End-to-End Case Management:** Integrated evidence locker, chronological timeline reconstruction, and court-admissible PDF reporting.
- **Recommended Screenshot / Diagram:**
  - Investigation Workspace Overview showing target wallet metadata, behavioural classification badge, and top VASP candidate summary.
- **Presenter Script:**
  > *"CryptoGuard AI bridges this gap. Given an unknown target wallet, our engine automatically maps the transaction graph up to 6 hops outward. It detects intermediary mules, measures velocity and structuring, and matches endpoints against verified VASP registries. Most importantly, it produces an auditable attribution score that investigators can explain and defend."*

---

### Slide 4: System Architecture
- **Title:** System Architecture: 4-Tier Forensic Processing Pipeline
- **Key Points:**
  - **Ingestion Layer:** Multi-chain REST adapters for EVM (Etherscan v2), Tron (TronGrid), and Bitcoin (Blockstream), with deterministic demo fallback.
  - **Graph Engine:** Bounded Breadth-First Search with degree pruning and counterparty filtering.
  - **Intelligence Engines:** Behavioral feature extractor (velocity, burst score, peel chain linearity) + 10-signal risk engine.
  - **Persistence & Presentation:** Embedded SQLite database (`cryptoguard.db`) coupled with a zero-dependency, desktop-first dark console.
- **Recommended Screenshot / Diagram:**
  - Architecture diagram from `ARCHITECTURE.md` showing the flow from blockchain data sources to FastAPI backend, forensic scoring, SQLite, and investigator UI.
- **Presenter Script:**
  > *"Our architecture is lightweight, resilient, and enterprise-grade. The FastAPI backend coordinates multi-chain data ingestion, runs our graph traversal algorithms, and persists all case data into a local SQLite database. We built the platform with zero external UI CDN dependencies, ensuring that it operates securely within air-gapped or restricted LEA network environments."*

---

### Slide 5: Core Innovation / Differentiation
- **Title:** Core Innovation: Explainable Attribution & Regulatory Alignment
- **Key Points:**
  - **Explain Attribution (Hop-by-Hop Walk):** Step-by-step visual and natural language walkthrough of exact transaction hashes, block numbers, and ETH amounts.
  - **India-Focused Cybercrime Workflow:** Native Section 91 CrPC / Section 94 BNSS legal notice generation targeting FIU-IND registered VASPs.
  - **AI Investigation Copilot:** Context-bounded assistant answering natural language case queries via deterministic rule engine or optional LLM.
  - **Interactive Node Inspector:** Clickable graph interface with instant counterparty debit/credit flow inspection.
- **Recommended Screenshot / Diagram:**
  - Side-by-side screenshot of the 'Explain Attribution' hop cards and the compiled Section 91 CrPC legal notice for CoinDCX.
- **Presenter Script:**
  > *"What sets CryptoGuard AI apart is explainability and statutory readiness. When our platform attributes a wallet to CoinDCX or Binance, it doesn't just display a number. It generates an 'Explain Attribution' hop walk showing the exact path, amounts, and block heights. Furthermore, it automatically compiles a Section 91 CrPC notice with designated FIU-IND compliance contacts, transforming raw blockchain data into immediate legal action."*

---

### Slide 6: Workflow + Demo
- **Title:** Demonstration: Real-World NCRP Cybercrime Investigation
- **Key Points:**
  - **Case Study:** NCRP Complaint `NCRP-2026-849102` involving 7.70 ETH fraud proceeds.
  - **Step 1:** Ingest target wallet & detect rapid dispersal into Mule Account Alpha and Peel Chain Node 1.
  - **Step 2:** Flag high-risk interaction with Tornado Cash mixer pool and peel chain structuring.
  - **Step 3:** Attribute primary cashout to CoinDCX (2 hops, 84.5% confidence) and Binance (3 hops, 73.8% confidence).
  - **Step 4:** Compile Section 91 CrPC disclosure notice and export forensic PDF report.
- **Recommended Screenshot / Diagram:**
  - Interactive Vis.js transaction graph highlighting the suspect target, intermediaries, and VASP deposit clusters with the Node Inspector open.
- **Presenter Script:**
  > *"In our live demo, we investigate a real-world cyber fraud complaint. Within seconds, CryptoGuard AI maps the 14-transaction flow, identifies the mixer obfuscation attempt, isolates two distinct VASP exit points, and produces an exportable formal requisition notice. All of this runs deterministically without latency or external API failure risks."*

---

### Slide 7: Technology Stack + Feasibility
- **Title:** Technology Stack, Modularity & Operational Feasibility
- **Key Points:**
  - **Backend:** Python 3.10+, FastAPI (ASGI), Pydantic v2 schemas, ReportLab PDF builder.
  - **Frontend:** Vanilla HTML5, responsive CSS3 cyber-intelligence design system, Vis.js graph network.
  - **Database:** Embedded SQLite with optimized indexes on wallets, transactions, evidence, and audit logs.
  - **Cost & Resource Footprint:** Minimal hardware requirements; runs on standard police workstation without GPU or expensive cloud licenses.
- **Recommended Screenshot / Diagram:**
  - Clean table showing the technology stack components and their open-source, cost-free licensing.
- **Presenter Script:**
  > *"CryptoGuard AI is built entirely on proven, open-source technologies with zero software licensing costs. It runs natively on standard police hardware without specialized GPU infrastructure. Its modular architecture allows seamless future integration with central LEA systems like the I4C SAHYOG portal or state police CCTNS databases."*

---

### Slide 8: Impact + Future Scope
- **Title:** Societal Impact, Legal Compliance & Future Roadmap
- **Key Points:**
  - **Accelerated Asset Recovery:** Reduces preliminary crypto tracing time from days to under 3 minutes, enabling rapid asset freezing before cashout.
  - **Court-Admissible Evidence:** Adheres to Section 63 of Bharatiya Sakshya Adhiniyam (BSA 2023) by maintaining immutable chain-of-custody logs.
  - **Future Scope (Phase II):**
    - Direct API integration with I4C SAHYOG Nodal Gateway.
    - Graph neural network (GNN) clustering for unknown deposit address heuristic expansion.
    - Automated cross-chain bridge tracking (Ethereum to Tron/Solana).
- **Recommended Screenshot / Diagram:**
  - Roadmap diagram depicting Phase 1 (MVP Delivered), Phase 2 (I4C SAHYOG Gateway API), and Phase 3 (Cross-Chain Liquidity Tracking).
- **Presenter Script:**
  > *"The impact of CryptoGuard AI is tangible: empowering cybercrime investigating officers across India to freeze proceeds of crime before they are liquidated into cash. By combining mathematical transparency with Indian procedural law, we deliver a solution that is practical, compliant, and ready for deployment. Thank you."*
