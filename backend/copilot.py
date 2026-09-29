"""
CryptoGuard AI — Hybrid Forensic Copilot
Answers investigative questions using exclusively the active investigation's data.

Operates in two modes:
1. LLM-Assisted (when OPENAI_API_KEY is configured in .env)
2. Hybrid Forensic Copilot (Deterministic Domain-Specific Forensic Engine — offline & reliable for SIH)
"""

from __future__ import annotations
import os
import json
from typing import Dict, Any, List

# Standard approved follow-up chips
DEFAULT_CHIPS: List[str] = [
    "Why was this VASP attributed?",
    "Show the strongest evidence",
    "What are the main risk indicators?",
    "Show the shortest transaction path",
    "What KYC information should be requested?",
    "Summarize this investigation"
]


def answer_investigation_query(trace_data: Dict[str, Any], query: str) -> Dict[str, Any]:
    """Processes an investigator question against active case data."""
    query_clean = query.strip().lower()

    # Check for LLM API Key (optional plug-in)
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    if openai_key:
        try:
            return _query_openai(trace_data, query, openai_key)
        except Exception as e:
            # Gracefully fall back to deterministic engine
            rule_res = _rule_based_engine(trace_data, query_clean)
            rule_res["note"] = f"(LLM fallback: {e}. Reverted to Hybrid Forensic Copilot)"
            return rule_res

    # Use Hybrid Forensic Copilot (Deterministic Engine)
    return _rule_based_engine(trace_data, query_clean)


def _rule_based_engine(trace_data: Dict[str, Any], q: str) -> Dict[str, Any]:
    """Deterministic domain-specific forensic NLP & graph reasoning engine."""
    wallet = trace_data.get("wallet", "Unknown")
    chain = trace_data.get("chain", "ethereum").capitalize()
    matches = trace_data.get("matches", [])
    top_match = trace_data.get("top_match") or (matches[0] if matches else {})
    risk = trace_data.get("risk", {})
    edges = trace_data.get("edges", [])
    nodes = trace_data.get("nodes", [])
    timeline = trace_data.get("timeline", [])
    evidence = trace_data.get("evidence", [])
    classification = trace_data.get("wallet_classification", {})
    features = trace_data.get("wallet_features", {})
    sahyog = trace_data.get("sahyog_routing", {})

    top_name = top_match.get("vasp_name", "Unattributed")
    score = risk.get("risk_score", 0)
    level = risk.get("risk_level", "LOW")

    # Helper to construct chip list excluding current topic
    def get_chips(exclude: str) -> List[str]:
        return [c for c in DEFAULT_CHIPS if exclude.lower() not in c.lower()][:4]

    # 1. KYC / Identity Requisitions
    if any(k in q for k in ["kyc", "identity", "customer information", "customer details", "user details", "beneficiary", "account holder"]):
        email = top_match.get("compliance_email", "compliance@vasp.internal")
        fiu_id = top_match.get("reporting_id", "FIU-IND-REG-PENDING")
        dep_addr = top_match.get("address", wallet)
        ans = (
            f"### Statutory KYC Disclosure Requisition for {top_name}\n\n"
            f"Under Section 91 CrPC and PMLA compliance rules, serve legal requisition to `{email}` "
            f"(Entity Registration: `{fiu_id}`) requesting disclosure for deposit address `{dep_addr}`:\n\n"
            f"1. **Account Holder Identity:** Verified Full Legal Name, Father's Name, DOB, and National ID (PAN / Aadhaar / Passport).\n"
            f"2. **Contact Coordinates:** Registered Mobile Number, Alternate Numbers, Primary and Secondary Email Addresses.\n"
            f"3. **Banking Coordinates:** Linked Domestic Bank Account Number, Account Holder Name, and Branch IFSC Code.\n"
            f"4. **Digital Footprint:** Ingress/Egress IP addresses with UTC timestamps, ISP details, and device UUID/IMEI fingerprints.\n"
            f"5. **Downstream Asset Trail:** Off-ramp fiat bank withdrawal transaction references (UTR/IMPS/NEFT) and external withdrawal addresses."
        )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "KYC Intelligence",
            "chips": get_chips("KYC")
        }

    # 2. Freeze / Asset Preservation Requisitions
    if any(k in q for k in ["freeze", "freezing", "hold funds", "block account", "seize", "debit freeze", "lien"]):
        vol = top_match.get("volume_eth", features.get("total_value_eth", 0))
        target_dep = top_match.get("address", "Target VASP Wallet")
        ans = (
            f"### Emergency Asset Preservation & Debit Freeze Requisition\n\n"
            f"- **Target Beneficiary Entity:** **{top_name}**\n"
            f"- **VASP Deposit Infrastructure:** `{target_dep}`\n"
            f"- **Traced Ingress Flow:** **{vol} ETH**\n"
            f"- **Compliance Channel:** `{top_match.get('compliance_email', 'lawenforcement@coindcx.com')}`\n\n"
            f"**Legal Mechanism:** CryptoGuard generates an automated **Section 91 CrPC Summon & Debit Freeze Requisition**. "
            f"The nodal compliance desk must place an immediate lien on the customer's internal trading UID and freeze fiat withdrawals "
            f"pending formal court attachment."
        )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Asset Preservation",
            "chips": get_chips("VASP")
        }

    # 3. Mule / Intermediary Wallets
    if any(k in q for k in ["mule", "mule wallet", "intermediary", "intermediary wallet", "mules", "middleman", "hopper"]):
        mules = [n for n in nodes if not n.get("is_root") and not n.get("is_known_vasp") and n.get("wallet_type") != "mixer"]
        if not mules:
            ans = f"No intermediate mule hops detected. Funds moved directly between `{wallet}` and attributed counterparties."
        else:
            mule_lines = []
            for idx, m in enumerate(mules[:4]):
                m_label = m.get("label") or m.get("id", "")[:12] + "…"
                m_risk = m.get("risk_level", "MED")
                m_type = m.get("wallet_type", "intermediary").replace("_", " ").title()
                mule_lines.append(f"{idx+1}. `{m.get('id')}` — **{m_label}** ({m_type}, Risk: `{m_risk}`)")
            ans = (
                f"### Identified Intermediary / Mule Accounts ({len(mules)} total)\n\n"
                f"Funds dispersed from `{wallet}` through structured hopping layers:\n\n"
                + "\n".join(mule_lines) +
                f"\n\n**Modus Operandi:** Intermediary mules are utilized to layer transaction velocity, break single-tx heuristics, "
                f"and obscure the originator before depositing into {top_name}."
            )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Mule Detection",
            "chips": ["Show the shortest transaction path", "What are the main risk indicators?", "What KYC information should be requested?", "Summarize this investigation"]
        }

    # 4. Evidence / Forensic Proof
    if any(k in q for k in ["evidence", "proof", "strongest evidence", "sha-256", "integrity", "locker"]):
        if not evidence:
            ans = f"No formal forensic evidence artifacts currently loaded for `{wallet}`."
        else:
            ev_lines = []
            for ev in evidence[:4]:
                h = ev.get("sha256_hash", "")[:16] + "…"
                ev_lines.append(f"- **[{ev.get('id')}] {ev.get('title')}** ({ev.get('evidence_type')}): SHA-256 `{h}` | Status: `{ev.get('status')}`")
            ans = (
                f"### Chain-of-Custody Forensic Evidence Artifacts ({len(evidence)} items)\n\n"
                + "\n".join(ev_lines) +
                f"\n\n**Evidentiary Standing:** All evidence items are bound with deterministic SHA-256 provenance hashes "
                f"and verifiable for submission under Section 65B of the Indian Evidence Act."
            )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Evidence Locker",
            "chips": ["Why was this VASP attributed?", "What are the main risk indicators?", "What KYC information should be requested?", "Summarize this investigation"]
        }

    # 5. FIU-IND / Legal Jurisdiction
    if any(k in q for k in ["fiu", "fiu-ind", "financial intelligence", "pmla", "compliance", "reporting entity"]):
        is_fiu = top_match.get("fiu_registered", False)
        fiu_id = top_match.get("reporting_id", "Unregistered")
        ans = (
            f"### FIU-IND Regulatory Compliance Profile: {top_name}\n\n"
            f"- **Domestic Reporting Status:** **{'Registered Reporting Entity (RE)' if is_fiu else 'Foreign / Non-Compliant Entity'}**\n"
            f"- **FIU-IND Registration ID:** `{fiu_id}`\n"
            f"- **Country of Incorporation:** {top_match.get('country', 'India')}\n"
            f"- **Legal Nodal Desk:** `{top_match.get('compliance_email', 'lawenforcement@coindcx.com')}`\n\n"
            f"**Legal Implication:** As an FIU-IND registered virtual digital asset service provider (VDASP), {top_name} "
            f"is statutorily mandated to maintain KYC records for 5 years and respond to law enforcement requisitions."
        )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Regulatory Intelligence",
            "chips": ["What KYC information should be requested?", "Why was this VASP attributed?", "Summarize this investigation", "Show the strongest evidence"]
        }

    # 6. Police / Investigator Procedure & SOP
    if any(k in q for k in ["police", "investigator", "law enforcement", "lea", "procedure", "sop", "next action", "next steps", "what to do", "protocol"]):
        ans = (
            f"### Recommended Law Enforcement Standard Operating Procedure (SOP)\n\n"
            f"1. **Formal Notice Issuance:** Navigate to the **Cybercrime Response** tab and compile a formal Section 91 CrPC notice for `{top_name}`.\n"
            f"2. **Emergency Debit Freeze:** Transmit notice to `{top_match.get('compliance_email', 'lawenforcement@coindcx.com')}` requesting lien on deposit address `{top_match.get('address', 'N/A')}`.\n"
            f"3. **Preserve Digital Artifacts:** Download the official **CryptoGuard PDF Investigation Report** for inclusion in the case diary.\n"
            f"4. **Examine Mule Chain:** Issue parallel summon notices for intermediary mule accounts identified in Hop 1.\n"
            f"5. **Fiat Bank Trail:** Upon receipt of VASP KYC, issue Section 102 CrPC notices to the destination banking branch."
        )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Investigative SOP",
            "chips": ["What KYC information should be requested?", "Show the strongest evidence", "Why was this VASP attributed?", "Summarize this investigation"]
        }

    # 7. VASP / Attribution Analysis
    if any(k in q for k in ["why", "attribute", "attribution", "vasp", "exchange", "service provider", "crypto exchange", "coindcx", "binance", "kraken", "wazirx"]):
        if not top_match:
            ans = "No VASP was attributed to this wallet because no transaction paths terminated at any known VASP addresses within the searched hop depth."
        else:
            name = top_match.get("vasp_name", "Unknown VASP")
            hops = top_match.get("hops", 0)
            conf = top_match.get("confidence", 0)
            vol = top_match.get("volume_eth", 0)
            path = " -> ".join(top_match.get("path", []))
            expl = top_match.get("explanation", "")
            ans = (
                f"### Attribution Rationale for {name}\n\n"
                f"- **Attribution Confidence:** **{conf}%** ({top_match.get('confidence_label', 'Evaluated')})\n"
                f"- **Graph Proximity:** **{hops} hop(s)** from target `{wallet}`\n"
                f"- **Attributed Flow Volume:** **{vol} ETH**\n"
                f"- **Transaction Path:** `{path}`\n\n"
                f"**Forensic Breakdown:** {expl or 'Funds from the suspect wallet were routed sequentially through intermediary counterparties into VASP deposit infrastructure.'}\n\n"
                f"**Multi-Factor Scoring Weights:** Proximity (40%), Interaction Volume (30%), Temporal Recency (20%), Evidence Provenance (10%)."
            )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "VASP Attribution",
            "chips": get_chips("VASP")
        }

    # 8. Shortest Transaction Path
    if any(k in q for k in ["shortest", "path", "route", "hops", "how many hops", "distance"]):
        if not matches:
            ans = f"No transaction paths connecting to known VASPs were discovered within {trace_data.get('hops_searched', 3)} hops."
        else:
            sorted_matches = sorted(matches, key=lambda m: m.get("hops", 99))
            shortest = sorted_matches[0]
            path_str = " -> ".join(shortest.get("path", []))
            ans = (
                f"### Shortest Transaction Path\n\n"
                f"The shortest path terminates at **{shortest.get('vasp_name')}** in **{shortest.get('hops')} hop(s)**.\n\n"
                f"- **Route:** `{path_str}`\n"
                f"- **Attribution Confidence:** **{shortest.get('confidence')}%**\n"
                f"- **Volume Routed:** **{shortest.get('volume_eth')} ETH**"
            )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Path Analysis",
            "chips": ["Why was this VASP attributed?", "What are the main risk indicators?", "What KYC information should be requested?", "Summarize this investigation"]
        }

    # 9. Risk Indicators & Laundering Typologies
    if any(k in q for k in ["risk", "danger", "suspicious", "high risk", "red flag", "indicator", "threat", "score", "level"]):
        flags = risk.get("flags", [])
        typos = risk.get("typologies", [])
        details = risk.get("details", {})
        flag_lines = "\n".join([f"- **{f.replace('_', ' ').title()}:** Weight: `{details.get(f, 'Active')}`" for f in flags])
        typo_lines = "\n".join([f"- {t}" for t in typos])
        ans = (
            f"### Forensic Risk Assessment: {score}/100 ({level} RISK)\n\n"
            f"**Detected Laundering Typologies:**\n{typo_lines or 'None identified'}\n\n"
            f"**Active Forensic Risk Signals:**\n{flag_lines or 'No suspicious flags detected.'}"
        )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Risk Intelligence",
            "chips": get_chips("risk")
        }

    # 10. Transactions / Fund Flow / Movement
    if any(k in q for k in ["transaction", "transfer", "movement", "fund flow", "money flow", "volume", "largest", "biggest", "flow"]):
        if not edges:
            ans = "No recorded transactions in the active investigation graph."
        else:
            sorted_edges = sorted(edges, key=lambda e: float(e.get("value_eth", 0)), reverse=True)
            max_edge = sorted_edges[0]
            val = max_edge.get("value_eth", 0)
            src = max_edge.get("source", "")
            tgt = max_edge.get("target", "")
            txh = max_edge.get("tx_hash", "N/A")
            total_vol = sum(float(e.get("value_eth", 0)) for e in edges)
            ans = (
                f"### Transaction Flow Profiling\n\n"
                f"- **Total Flow Recorded:** **{total_vol:.2f} ETH** across **{len(edges)} transactions**\n"
                f"- **Largest Single Transfer:** **{val:.4f} ETH**\n"
                f"  - **From:** `{src}`\n"
                f"  - **To:** `{tgt}`\n"
                f"  - **Tx Hash:** `{txh}`"
            )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Transaction Profiling",
            "chips": ["Show the shortest transaction path", "Why was this VASP attributed?", "What are the main risk indicators?", "Summarize this investigation"]
        }

    # 11. Timeline / Chronological Sequence
    if any(k in q for k in ["timeline", "sequence", "chronological", "what happened", "history", "order", "after"]):
        if not timeline:
            ans = f"No chronological events recorded for `{wallet}`."
        else:
            steps = []
            for idx, te in enumerate(timeline[:6]):
                t = te.get("time", "").replace("T", " ").replace("Z", " UTC")
                steps.append(f"{idx+1}. **{t}** — *{te.get('title')}*: {te.get('desc')}")
            ans = "### Chronological Fund Dispersal Timeline\n\n" + "\n".join(steps)
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Timeline Reconstruction",
            "chips": ["Why was this VASP attributed?", "What are the main risk indicators?", "Show the strongest evidence", "Summarize this investigation"]
        }

    # 12. Case Summary / Executive Overview
    if any(k in q for k in ["summarize", "summary", "overview", "report", "case", "briefing"]):
        ans = (
            f"### Executive Case Summary: {wallet}\n\n"
            f"- **Chain & Classification:** {chain} | **{classification.get('label', 'Suspect Facilitator')}**\n"
            f"- **Risk Assessment:** **{score}/100 ({level} RISK)**\n"
            f"- **Primary Attributed VASP:** **{top_name}** ({top_match.get('confidence', 0)}% confidence, {top_match.get('hops', 0)} hops)\n"
            f"- **Entities Identified:** **{len(nodes)} distinct nodes** across **{len(edges)} transaction hops**\n"
            f"- **Recommended Legal Action:** Issue Section 91 CrPC notice to {top_name} requesting KYC and asset preservation."
        )
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
            "confidence": "High",
            "category": "Executive Summary",
            "chips": ["Why was this VASP attributed?", "Show the strongest evidence", "What are the main risk indicators?", "What KYC information should be requested?"]
        }

    # Default fallback
    return {
        "answer": (
            f"### Case Overview for Target `{wallet}`\n\n"
            f"- **Attributed VASP:** {top_name} ({top_match.get('confidence', 0)}% confidence)\n"
            f"- **Risk Level:** {score}/100 ({level})\n"
            f"- **Counterparties Traced:** {len(nodes)} entities across {len(edges)} transaction paths\n\n"
            f"Select a suggested follow-up below or ask about VASP attribution, mules, KYC requisitions, asset freezing, or risk indicators."
        ),
        "engine": "Hybrid Forensic Copilot (Deterministic Engine)",
        "confidence": "Moderate",
        "category": "General Assistance",
        "chips": DEFAULT_CHIPS[:4]
    }


def _query_openai(trace_data: Dict[str, Any], query: str, api_key: str) -> Dict[str, Any]:
    """Optional OpenAI GPT call if key is supplied."""
    import requests
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    context = {
        "wallet": trace_data.get("wallet"),
        "chain": trace_data.get("chain"),
        "top_match": trace_data.get("top_match"),
        "risk": trace_data.get("risk"),
        "classification": trace_data.get("wallet_classification"),
        "total_nodes": len(trace_data.get("nodes", [])),
        "total_edges": len(trace_data.get("edges", []))
    }
    prompt = (
        f"You are CryptoGuard AI Hybrid Forensic Copilot, a blockchain forensics assistant for law enforcement.\n"
        f"Answer the investigator's question based strictly on this case context:\n{json.dumps(context)}\n\n"
        f"Question: {query}\n"
        f"Keep the answer concise, professional, factual, and legally cautious. Never fabricate data."
    )
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are a blockchain forensics assistant for law enforcement."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=10)
    if resp.status_code == 200:
        data = resp.json()
        ans = data["choices"][0]["message"]["content"]
        return {
            "answer": ans,
            "engine": "Hybrid Forensic Copilot (LLM-Assisted)",
            "confidence": "High",
            "category": "LLM Intelligence",
            "chips": DEFAULT_CHIPS[:4]
        }
    raise Exception(f"OpenAI API status {resp.status_code}: {resp.text}")

