"""
Risk Scoring Engine for the Wallet-to-VASP Attribution System.

Computes a holistic risk score (0-100) for a wallet based on multiple
independent signals, assigns a risk level (HIGH / MEDIUM / LOW), and
identifies any laundering typologies detected.

Risk Signals (each scored 0-100, then weighted):
  1. mixer_interaction      — direct link to known mixer/tumbler
  2. sanctions_link         — direct link to OFAC-sanctioned address
  3. ransomware_link        — direct link to known ransomware address
  4. darknet_link           — direct link to known darknet address
  5. structuring            — many transactions just below round thresholds
  6. peel_chain             — linear single-hop chain (classic layering)
  7. high_velocity          — abnormally high transaction rate
  8. cross_chain_bridge     — direct interaction with bridge/swap (risk indicator)
  9. self_is_high_risk      — the wallet itself is in the high-risk registry

Laundering Typologies Detected:
  - "Layering via Mixer"
  - "Peel Chain / Linear Layering"
  - "Structuring / Smurfing"
  - "Sanctions Evasion"
  - "Ransomware Payment"
  - "Cross-Chain Obfuscation"
  - "Darknet Activity"
  - "High-Velocity Rapid Movement"
"""

from __future__ import annotations
from collections import Counter
from typing import List

from high_risk_addresses import (
    MIXER_ADDRESSES, RANSOMWARE_ADDRESSES, DARKNET_ADDRESSES,
    SANCTIONS_ADDRESSES, BRIDGE_ADDRESSES, FRAUD_ADDRESSES, is_high_risk,
)

# Risk level thresholds
RISK_HIGH_THRESHOLD   = 60
RISK_MEDIUM_THRESHOLD = 25

SIGNAL_WEIGHTS = {
    "self_is_high_risk":   1.00,   # most severe — the wallet itself is flagged
    "sanctions_link":      0.95,
    "ransomware_link":     0.90,
    "darknet_link":        0.85,
    "mixer_interaction":   0.75,
    "structuring":         0.50,
    "peel_chain":          0.40,
    "cross_chain_bridge":  0.30,
    "high_velocity":       0.25,
    "fraud_link":          0.70,
}


def score_wallet(
    wallet: str,
    txs: List[dict],
    edges: List[dict],
    path_wallets: list,
) -> dict:
    """
    Compute a risk report for a single wallet.

    Args:
        wallet:        The wallet address being assessed.
        txs:           Its transaction list (dicts with from/to/value/timeStamp).
        edges:         All graph edges collected during the trace.
        path_wallets:  All wallets in the trace graph (for neighbor lookup).

    Returns a dict with:
        risk_score  (0-100, int)
        risk_level  ("HIGH" | "MEDIUM" | "LOW")
        flags       (list of active signal names)
        typologies  (list of human-readable laundering typology strings)
        details     (dict: signal_name -> sub-score)
    """
    addr = wallet.lower()
    signals: dict[str, float] = {}
    typologies: list[str] = []

    # Collect all direct counterparties
    counterparties = set()
    for tx in txs:
        f = tx.get("from", "").lower()
        t = tx.get("to",   "").lower()
        if f and f != addr:
            counterparties.add(f)
        if t and t != addr:
            counterparties.add(t)

    # --- Signal 1: self is in high-risk registry ---
    if is_high_risk(addr):
        signals["self_is_high_risk"] = 100

    # --- Signal 2: sanctions link ---
    sanctioned_neighbors = counterparties & SANCTIONS_ADDRESSES
    if sanctioned_neighbors:
        signals["sanctions_link"] = 100
        typologies.append("Sanctions Evasion")

    # --- Signal 3: ransomware link ---
    ransomware_neighbors = counterparties & RANSOMWARE_ADDRESSES
    if ransomware_neighbors:
        signals["ransomware_link"] = 100
        typologies.append("Ransomware Payment")

    # --- Signal 4: darknet link ---
    darknet_neighbors = counterparties & DARKNET_ADDRESSES
    if darknet_neighbors:
        signals["darknet_link"] = 100
        typologies.append("Darknet Activity")

    # --- Signal 5: fraud link ---
    fraud_neighbors = counterparties & FRAUD_ADDRESSES
    if fraud_neighbors:
        signals["fraud_link"] = 90
        typologies.append("Fraud-Linked Wallet")

    # --- Signal 6: mixer interaction ---
    mixer_neighbors = counterparties & MIXER_ADDRESSES
    if mixer_neighbors:
        signals["mixer_interaction"] = 90
        typologies.append("Layering via Mixer")

    # --- Signal 7: cross-chain bridge interaction ---
    bridge_neighbors = counterparties & BRIDGE_ADDRESSES
    if bridge_neighbors:
        signals["cross_chain_bridge"] = 50
        typologies.append("Cross-Chain Obfuscation")

    # --- Behavioral signals (require txs) ---
    if txs:
        values = []
        for tx in txs:
            raw = tx.get("value", "0")
            try:
                values.append(int(raw))
            except (ValueError, TypeError):
                pass

        total_txs = len(txs)

        # Signal 8: structuring — many txs with identical or near-identical values
        if values:
            value_counts = Counter(values)
            top_val, top_count = value_counts.most_common(1)[0]
            structuring_ratio = top_count / len(values)
            if structuring_ratio > 0.5 and total_txs >= 8:
                score = min(100, int(structuring_ratio * 100))
                signals["structuring"] = score
                typologies.append("Structuring / Smurfing")

        # Signal 9: peel chain — very few unique counterparties, linear flow
        unique_senders   = len(set(tx.get("from","").lower() for tx in txs if tx.get("from")))
        unique_receivers = len(set(tx.get("to","").lower()   for tx in txs if tx.get("to")))
        if unique_senders <= 2 and unique_receivers <= 2 and total_txs >= 5:
            signals["peel_chain"] = 70
            typologies.append("Peel Chain / Linear Layering")

        # Signal 10: high velocity — many txs in a short time window
        timestamps = []
        for tx in txs:
            try:
                timestamps.append(int(tx.get("timeStamp", 0)))
            except (ValueError, TypeError):
                pass
        if len(timestamps) >= 20:
            time_span = max(timestamps) - min(timestamps)
            if time_span > 0:
                tx_per_day = (len(timestamps) / time_span) * 86400
                if tx_per_day > 200:
                    signals["high_velocity"] = min(100, int(tx_per_day / 3))
                    typologies.append("High-Velocity Rapid Movement")

    # --- Compute final weighted score ---
    if not signals:
        final_score = 0
    else:
        numerator   = sum(signals[k] * SIGNAL_WEIGHTS.get(k, 0.5) for k in signals)
        denominator = sum(SIGNAL_WEIGHTS.get(k, 0.5) for k in signals)
        # Boost: more independent signals = more certain
        multi_signal_boost = min(20, (len(signals) - 1) * 5)
        base = (numerator / denominator) if denominator else 0
        final_score = min(100, int(base + multi_signal_boost))

    # --- Determine risk level ---
    if final_score >= RISK_HIGH_THRESHOLD:
        risk_level = "HIGH"
    elif final_score >= RISK_MEDIUM_THRESHOLD:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Deduplicate typologies while preserving order
    seen: set[str] = set()
    unique_typologies = []
    for t in typologies:
        if t not in seen:
            seen.add(t)
            unique_typologies.append(t)

    return {
        "risk_score":  final_score,
        "risk_level":  risk_level,
        "flags":       list(signals.keys()),
        "typologies":  unique_typologies,
        "details":     {k: round(v) for k, v in signals.items()},
    }
