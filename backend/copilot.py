"""
CryptoGuard AI - Investigation Copilot
Answers investigative questions using exclusively the active investigation's data.

Operates in two modes:
1. LLM-Assisted (when OPENAI_API_KEY or GEMINI_API_KEY is configured in .env)
2. Deterministic Rule-Based Intelligence Engine (default offline fallback for SIH evaluation)
"""

from __future__ import annotations
import os
import json
from typing import Dict, Any, List


def answer_investigation_query(trace_data: Dict[str, Any], query: str) -> Dict[str, Any]:
    """Processes a user question about the active investigation."""
    query_clean = query.strip().lower()

    # Check for LLM API Key
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip()

    if openai_key:
        try:
            return _query_openai(trace_data, query, openai_key)
        except Exception as e:
            # Fall back to deterministic rule engine if API call fails
            rule_res = _rule_based_engine(trace_data, query_clean)
            rule_res["note"] = f"(LLM error: {e}. Reverted to Deterministic Engine)"
            return rule_res

    # Use Deterministic Rule-Based Engine
    return _rule_based_engine(trace_data, query_clean)


def _rule_based_engine(trace_data: Dict[str, Any], q: str) -> Dict[str, Any]:
    """Deterministic NLP and graph analysis engine."""
    wallet = trace_data.get("wallet", "Unknown")
    matches = trace_data.get("matches", [])
    top_match = trace_data.get("top_match") or (matches[0] if matches else {})
    risk = trace_data.get("risk", {})
    edges = trace_data.get("edges", [])
    nodes = trace_data.get("nodes", [])
    timeline = trace_data.get("timeline", [])
    classification = trace_data.get("wallet_classification", {})

    # 1. Why was VASP attributed?
    if any(k in q for k in ["why", "attribute", "attribution", "vasp", "coindcx", "binance", "kraken"]):
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
                f"**Attribution Summary for {name}:**\n\n"
                f"- **Attribution Confidence:** {conf}% ({top_match.get('confidence_label', 'Evaluated')})\n"
                f"- **Hop Distance:** {hops} hop(s)\n"
                f"- **Observed Flow Volume:** {vol} ETH\n"
                f"- **Transaction Path:** `{path}`\n\n"
                f"**Forensic Rationale:** {expl or 'Funds from the suspect wallet moved sequentially through intermediary counterparties before reaching the VASP deposit infrastructure.'}"
            )
        return {
            "answer": ans,
            "engine": "Deterministic Intelligence Engine",
            "confidence": "High",
            "category": "VASP Attribution"
        }

    # 2. Shortest transaction path
    if any(k in q for k in ["shortest", "path", "route", "hops", "how many"]):
        if not matches:
            ans = "No transaction paths connecting to known VASPs were discovered within the maximum hop search radius."
        else:
            sorted_matches = sorted(matches, key=lambda m: m.get("hops", 99))
            shortest = sorted_matches[0]
            path_str = " -> ".join(shortest.get("path", []))
            ans = (
                f"The shortest path terminates at **{shortest.get('vasp_name')}** in **{shortest.get('hops')} hop(s)**.\n\n"
                f"**Route:** `{path_str}`\n"
                f"**Confidence:** {shortest.get('confidence')}% | **Volume:** {shortest.get('volume_eth')} ETH"
            )
        return {
            "answer": ans,
            "engine": "Deterministic Intelligence Engine",
            "confidence": "High",
            "category": "Path Analysis"
        }

    # 3. Strongest risk indicators
    if any(k in q for k in ["risk", "indicator", "suspicious", "flag", "score", "level"]):
        score = risk.get("risk_score", 0)
        level = risk.get("risk_level", "LOW")
        flags = risk.get("flags", [])
        typos = risk.get("typologies", [])
        details = risk.get("details", {})

        flag_lines = "\n".join([f"- **{f.replace('_', ' ').title()}:** Weight/Subscore: {details.get(f, 'Active')}" for f in flags])
        typo_lines = "\n".join([f"- {t}" for t in typos])

        ans = (
            f"**Risk Evaluation Assessment:**\n\n"
            f"- **Overall Risk Score:** **{score}/100** ({level} RISK)\n\n"
            f"**Detected Laundering Typologies:**\n{typo_lines or 'None'}\n\n"
            f"**Active Forensic Signals:**\n{flag_lines or 'No suspicious flags detected.'}"
        )
        return {
            "answer": ans,
            "engine": "Deterministic Intelligence Engine",
            "confidence": "High",
            "category": "Risk Intelligence"
        }

    # 4. Largest transaction
    if any(k in q for k in ["largest", "biggest", "maximum", "max transaction", "highest volume"]):
        if not edges:
            ans = "No transactions recorded in the graph."
        else:
            sorted_edges = sorted(edges, key=lambda e: float(e.get("value_eth", 0)), reverse=True)
            max_edge = sorted_edges[0]
            val = max_edge.get("value_eth", 0)
            src = max_edge.get("source", "")
            tgt = max_edge.get("target", "")
            txh = max_edge.get("tx_hash", "N/A")
            ans = (
                f"**Largest Observed Transaction:**\n\n"
                f"- **Value:** **{val:.4f} ETH**\n"
                f"- **Source:** `{src}`\n"
                f"- **Destination:** `{tgt}`\n"
                f"- **Transaction Hash:** `{txh}`"
            )
        return {
            "answer": ans,
            "engine": "Deterministic Intelligence Engine",
            "confidence": "High",
            "category": "Transaction Profiling"
        }

    # 5. Timeline / What happened after funds received
    if any(k in q for k in ["happened", "after", "received", "sequence", "timeline", "order", "history"]):
        if not timeline:
            ans = "No chronological timeline events are available for this wallet."
        else:
            steps = []
            for idx, te in enumerate(timeline):
                t = te.get("time", "").replace("T", " ").replace("Z", " UTC")
                steps.append(f"{idx+1}. **{t}** — *{te.get('title')}*: {te.get('desc')}")
            ans = "**Chronological Dispersal Flow:**\n\n" + "\n".join(steps)
        return {
            "answer": ans,
            "engine": "Deterministic Intelligence Engine",
            "confidence": "High",
            "category": "Timeline Reconstruction"
        }

    # 6. Investigation Summary
    if any(k in q for k in ["summarize", "summary", "overview", "report", "case"]):
        top_name = top_match.get("vasp_name", "Unattributed")
        score = risk.get("risk_score", 0)
        level = risk.get("risk_level", "LOW")
        ans = (
            f"### Case Investigation Summary\n\n"
            f"- **Target Wallet:** `{wallet}`\n"
            f"- **Classification:** **{classification.get('label', 'Unknown')}**\n"
            f"- **Risk Assessment:** **{score}/100 ({level})**\n"
            f"- **Primary Attributed VASP:** **{top_name}** ({top_match.get('confidence', 0)}% confidence)\n"
            f"- **Identified Counterparties:** {len(nodes)} distinct nodes across {len(edges)} transaction hops\n"
            f"- **Next Recommended Action:** Issue Section 91 CrPC notice to {top_name} for KYC disclosure and asset preservation."
        )
        return {
            "answer": ans,
            "engine": "Deterministic Intelligence Engine",
            "confidence": "High",
            "category": "Executive Summary"
        }

    # Default / General Query response
    return {
        "answer": (
            f"Based on the investigation of wallet `{wallet}`:\n\n"
            f"- **Attributed VASP:** {top_match.get('vasp_name', 'None')} ({top_match.get('confidence', 0)}% confidence)\n"
            f"- **Risk Score:** {risk.get('risk_score', 0)}/100 ({risk.get('risk_level', 'LOW')})\n"
            f"- **Counterparty Count:** {len(nodes)} entities identified\n\n"
            f"You can ask me specific questions such as: *'Why was this VASP attributed?'*, *'What is the shortest transaction path?'*, "
            f"*'What are the strongest risk indicators?'*, *'Show the largest transaction'*, or *'What happened after the suspect wallet received funds?'*."
        ),
        "engine": "Deterministic Intelligence Engine",
        "confidence": "Moderate",
        "category": "General Assistance"
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
        f"You are CryptoGuard AI, an expert blockchain forensics assistant for law enforcement.\n"
        f"Answer the investigator's question based strictly on this case context:\n{json.dumps(context)}\n\n"
        f"Question: {query}\n"
        f"Keep the answer concise, professional, factual, and legally cautious."
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
            "engine": "AI Copilot (GPT-4o-mini)",
            "confidence": "High",
            "category": "LLM Intelligence"
        }
    raise Exception(f"OpenAI API status {resp.status_code}: {resp.text}")
