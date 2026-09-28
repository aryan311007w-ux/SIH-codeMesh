# CryptoGuard AI — System Architecture & Forensic Design

**Product:** CryptoGuard AI  
**Tagline:** AI-Powered Blockchain Investigation & VASP Attribution Platform  
**Target Domain:** Law Enforcement Agencies (LEAs), I4C (Indian Cybercrime Coordination Centre), FIU-IND  
**Problem Statement:** SIH26182  

---

## 1. High-Level Architectural Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             INVESTIGATOR UI                                 │
│  [ Dashboard ]  [ Workspace (8 Tabs) ]  [ Graph Inspector ]  [ Copilot ]    │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │ HTTP / REST / JSON
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    FASTAPI ASGI APPLICATION ENGINE                          │
│                                                                             │
│  ├── /api/trace                ├── /api/copilot/query                       │
│  ├── /api/investigation/{id}   ├── /api/sahyog/notice                       │
│  ├── /api/evidence/{id}        ├── /api/report/{wallet}                     │
│  └── /api/v1/dashboard/summary └── /api/vasps                               │
└───────┬──────────────────────────────┬──────────────────────────────┬───────┘
        │                              │                              │
┌───────▼──────────────┐   ┌───────────▼──────────────┐   ┌───────────▼──────────────┐
│  GRAPH TRAVERSAL     │   │   FORENSIC ENGINES       │   │  PERSISTENCE & DATA      │
│  & INGESTION         │   │                          │   │                          │
│                      │   │  ├── VASP Attribution    │   │  ├── SQLite Database     │
│  ├── Multi-Hop BFS   │   │      (4-Factor Model)    │   │      (cryptoguard.db)    │
│  ├── Blockchain      │   │  ├── 10-Signal Risk      │   │  ├── VASP Registry       │
│      Adapters        │   │      Scoring Engine      │   │      (FIU-IND + Global)  │
│      (EVM/Tron/BTC)  │   │  ├── Behaviour Classifier│   │  ├── Evidence Locker     │
│  └── Deterministic   │   │  └── AI Copilot Engine   │   │  └── Audit Logging       │
│      Demo Fixture    │   │      (Rule/LLM Hybrid)   │   │                          │
└──────────────────────┘   └──────────────────────────┘   └──────────────────────────┘
```

---

## 2. Multi-Hop Graph Traversal Engine (BFS Walk)

The traversal engine (`backend/tracer.py`) performs an outward Breadth-First Search (BFS) starting from the investigated target wallet $W_0$:

1. **Queue Initialization:** $\mathcal{Q} \leftarrow [(W_0, \text{hop}=0, \text{path}=[W_0])]$.
2. **Expansion Bound:** Traversal is bounded by $\text{max\_hops}$ (default 3, max 6) and $\text{max\_nodes\_to\_expand} = 20$ to prevent denial-of-service on ultra-high-degree contracts (e.g. exchange hot wallets).
3. **Transaction Extraction:** For each node $u$, transaction history is extracted and directionally parsed:
   - Outbound flow: $u \to v$
   - Inbound flow: $v \to u$
4. **Pruning & Counterparty Filtering:** Zero-value spam transactions, ERC-20 approvals, and repeated self-loops are filtered out.
5. **VASP & High-Risk Interception:** Every encountered counterparty $v$ is checked against:
   - Verified VASP Registry (`backend/vasp_registry.py`)
   - Sanctioned / Mixer / Ransomware Registry (`backend/high_risk_addresses.py`)
6. **Path Construction:** When a VASP address is reached, the complete path $[W_0, v_1, v_2, \dots, VASP]$ is recorded along with transaction hashes, timestamps, and transfer volumes.

---

## 3. Multi-Dimensional VASP Attribution Algorithm

Attribution is not a black-box machine learning claim. CryptoGuard AI uses a transparent, explainable 4-factor scoring model normalized to $0 - 100$:

$$\text{Confidence Score} = w_1 S_{\text{proximity}} + w_2 S_{\text{interaction}} + w_3 S_{\text{recency}} + w_4 S_{\text{provenance}}$$

Where:
- $w_1 = 0.40$ (Graph Proximity Weight)
- $w_2 = 0.30$ (Interaction Flow Volume Weight)
- $w_3 = 0.20$ (Temporal Recency Weight)
- $w_4 = 0.10$ (Registry Provenance Weight)

### Sub-Score Formulations:
1. **Graph Proximity Score ($S_{\text{proximity}}$):**
   $$S_{\text{proximity}} = \max\left(0, 100 - (\text{hops} \times 25)\right) + \min\left(15, (\text{paths} - 1) \times 5\right)$$
   Direct 1-hop interactions score up to 90; 2-hop paths score 50–65; 3-hop paths score 25–40.
2. **Interaction Volume Score ($S_{\text{interaction}}$):**
   $$S_{\text{interaction}} = \left(\frac{\text{Volume routed toward VASP candidate}}{\text{Total observed target outflow}}\right) \times 100$$
3. **Temporal Recency Score ($S_{\text{recency}}$):**
   $$S_{\text{recency}} = 100 \times \exp\left(-0.02 \times \Delta t_{\text{days}}\right)$$
   Decays smoothly as the time elapsed since the most recent interaction increases.
4. **Registry Provenance Weight ($S_{\text{provenance}}$):**
   - **High ($100$):** Authoritative FIU-IND registered reporting entities, official exchange cold/hot wallets, or OFAC listings.
   - **Medium ($65$):** Community-corroborated exchange deposit clusters.
   - **Low ($35$):** Uncorroborated single-source public tag.

### Confidence Labels:
- $\ge 75\%$: **Strong Evidence**
- $50\% - 74\%$: **Moderate Evidence**
- $25\% - 49\%$: **Weak Evidence**
- $< 25\%$: **Insufficient Evidence**

---

## 4. Transparent Forensic Risk Engine

The risk engine (`backend/risk_engine.py`) scores target wallets on a $0 - 100$ scale using 10 weighted forensic signals:

| Signal Name | Severity Weight | Trigger Condition |
|---|---|---|
| `self_is_high_risk` | 1.00 | Wallet itself appears on OFAC/sanctions or verified fraud list |
| `sanctions_link` | 0.95 | Direct counterparty to OFAC-sanctioned address |
| `ransomware_link` | 0.90 | Transaction with known ransomware deposit address |
| `darknet_link` | 0.85 | Transaction with darknet marketplace address |
| `mixer_interaction` | 0.75 | Inbound or outbound flow from Tornado Cash or tumblers |
| `fraud_link` | 0.70 | Interaction with verified scam/phishing report |
| `rapid_fund_movement` | 0.50 | Capital forwarded within 15 minutes of deposit |
| `structuring` | 0.50 | Near-identical repetitive values just below reporting thresholds |
| `peel_chain` | 0.40 | Linear single-hop peeling pattern (score $> 0.5$) |
| `cross_chain_bridge` | 0.30 | Funds routed through non-custodial cross-chain bridges |

$$\text{Final Risk Score} = \min\left(100, \sum (\text{signal\_score} \times \text{weight}) + \min(20, (N_{\text{signals}} - 1) \times 5)\right)$$

- **Risk Levels:**
  - $\ge 60$: **HIGH RISK** (Mandatory statutory requisition recommended)
  - $25 - 59$: **MEDIUM RISK** (Enhanced monitoring)
  - $< 25$: **LOW RISK** (Standard operational pattern)

---

## 5. Database Schema (`cryptoguard.db`)

CryptoGuard AI uses an ACID-compliant embedded SQLite database:

1. **`investigations`**: Case reference, target wallet, chain, status, risk level, risk score, top VASP, confidence, serialized result JSON, timestamps.
2. **`wallets`**: Address, chain, classification, risk score, VASP status, first/last seen.
3. **`transactions`**: Investigation ID, transaction hash, chain, from address, to address, amount, block number, timestamp.
4. **`vasps`**: Name, category, FIU registration status, country, compliance email, reporting ID, deposit addresses.
5. **`evidence`**: Evidence ID (`EV-xxxx-xx`), investigation ID, type, transaction hash, counterparty, timestamp, verification status (`Relevant`, `Reviewed`, `Needs Verification`), investigator notes.
6. **`timeline_events`**: Chronological events, timestamps, titles, descriptions, transaction hashes, amounts.
7. **`audit_logs`**: Timestamp, action, investigator ID, details.

---

## 6. Indian Cybercrime (NCRP / I4C) & Legal Framework

CryptoGuard AI is architected specifically to bridge blockchain evidence with Indian statutory law enforcement procedures:

- **Section 91 CrPC (or Section 94 Bharatiya Nagarik Suraksha Sanhita, 2023):**  
  Power of Police Officer / Investigating Officer to summon documents or production of electronic records from entities.
- **Section 102 CrPC (or Section 106 BNSS 2023):**  
  Seizure and temporary freezing of property suspected to be stolen or linked to proceeds of crime.
- **Prevention of Money Laundering Act (PMLA, 2002):**  
  Mandates all registered Virtual Asset Service Providers (VASPs) operating in India to register with FIU-IND and maintain 24/7 Nodal Compliance Desks for LEA coordination.
- **Bharatiya Sakshya Adhiniyam (BSA, 2023) Section 63:**  
  Admissibility of electronic records and chain of custody documentation.
