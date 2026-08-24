"""
Wallet Behavioural Feature Extractor.

Extracts a standardised WalletFeatureVector from a list of raw transaction
dicts (the format returned by BlockchainClient.get_transactions).

This module is the foundation for Level 3 ML ranking (XGBoost / LightGBM)
and Level 4 behavioural clustering.  The feature vector is also used by the
multi-dimensional VASP confidence scorer in tracer.py to compute
interaction_strength and temporal_recency sub-scores.

Design principles
-----------------
- Pure functions, no I/O, no side effects.
- All inputs are native Python types — no pandas dependency.
- Every feature is documented so a judge/investigator can understand it.
- Graceful: returns a zeroed vector rather than raising on empty/missing data.
"""

from __future__ import annotations

import time
from collections import Counter
from typing import List, Dict, Optional

from high_risk_addresses import (
    MIXER_ADDRESSES, BRIDGE_ADDRESSES,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_WEI_PER_ETH = 10 ** 18
_SECS_PER_DAY = 86_400


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_features(
    wallet: str,
    txs: List[dict],
    known_vasps: Dict[str, str],
    edges: Optional[List[dict]] = None,
) -> dict:
    """
    Extract a WalletFeatureVector-compatible dict for `wallet`.

    Parameters
    ----------
    wallet      : The address being profiled (used to determine directionality).
    txs         : Transaction list from BlockchainClient (normalized format).
    known_vasps : KNOWN_VASPS dict for VASP exposure calculation.
    edges       : Full edge list from the BFS trace (used only for graph
                  neighbourhood enrichment; optional).

    Returns
    -------
    A plain dict matching the WalletFeatureVector schema.
    All values default to 0 / 0.0 if there are no transactions.
    """
    addr = wallet.lower()

    if not txs:
        return _zeroed_vector()

    # ── Counterparty sets ──────────────────────────────────────────────────
    senders   = Counter(tx.get("from", "").lower() for tx in txs if tx.get("from"))
    receivers = Counter(tx.get("to",   "").lower() for tx in txs if tx.get("to"))

    # Remove self from both sets (contract calls, etc.)
    senders.pop(addr, None)
    receivers.pop(addr, None)

    all_counterparties = set(senders.keys()) | set(receivers.keys())
    n_counterparties   = len(all_counterparties)
    n_senders          = len(senders)
    n_receivers        = len(receivers)

    # ── Value features ─────────────────────────────────────────────────────
    raw_values: List[int] = []
    for tx in txs:
        try:
            raw_values.append(int(tx.get("value", 0)))
        except (ValueError, TypeError):
            raw_values.append(0)

    eth_values = [v / _WEI_PER_ETH for v in raw_values]
    total_eth  = sum(eth_values)
    avg_eth    = total_eth / len(eth_values) if eth_values else 0.0
    max_eth    = max(eth_values) if eth_values else 0.0
    value_concentration = (max_eth / total_eth) if total_eth > 0 else 0.0

    # In/out ratio — fraction that is inbound
    inbound_eth  = sum(
        v / _WEI_PER_ETH
        for tx, v in zip(txs, raw_values)
        if tx.get("to", "").lower() == addr
    )
    outbound_eth = total_eth - inbound_eth
    total_flow   = inbound_eth + outbound_eth
    in_out_ratio = (inbound_eth / total_flow) if total_flow > 0 else 0.5

    # ── Temporal features ──────────────────────────────────────────────────
    timestamps: List[int] = []
    for tx in txs:
        try:
            ts = int(tx.get("timeStamp", 0))
            if ts > 0:
                timestamps.append(ts)
        except (ValueError, TypeError):
            pass

    now_ts = int(time.time())

    if timestamps:
        ts_min  = min(timestamps)
        ts_max  = max(timestamps)
        span    = ts_max - ts_min   # seconds
        span_days = span / _SECS_PER_DAY if span > 0 else 1.0
        tx_per_day = len(timestamps) / span_days if span_days > 0 else float(len(timestamps))

        recency_days = (now_ts - ts_max) / _SECS_PER_DAY

        # Burst score: compare peak 24h activity to average 24h activity
        burst_score = _compute_burst_score(timestamps)
    else:
        span_days  = 0.0
        tx_per_day = 0.0
        recency_days = 0.0
        burst_score  = 1.0

    # ── Exposure features ──────────────────────────────────────────────────
    mixer_count = len(all_counterparties & MIXER_ADDRESSES)
    bridge_count = len(all_counterparties & BRIDGE_ADDRESSES)
    vasp_count  = len(all_counterparties & set(known_vasps.keys()))

    denom = n_counterparties if n_counterparties > 0 else 1
    mixer_exposure  = mixer_count  / denom
    bridge_exposure = bridge_count / denom
    vasp_exposure   = vasp_count   / denom

    # ── Structuring signals ────────────────────────────────────────────────
    structuring_ratio = _structuring_ratio(raw_values)
    peel_chain_score  = _peel_chain_score(n_senders, n_receivers, len(txs))

    return {
        # Graph
        "unique_counterparties": n_counterparties,
        "unique_senders":        n_senders,
        "unique_receivers":      n_receivers,
        "tx_count":              len(txs),
        # Value
        "total_value_eth":       round(total_eth,    6),
        "avg_value_eth":         round(avg_eth,      6),
        "max_value_eth":         round(max_eth,      6),
        "in_out_ratio":          round(in_out_ratio, 4),
        "value_concentration":   round(value_concentration, 4),
        # Temporal
        "tx_per_day":            round(tx_per_day,   4),
        "burst_score":           round(burst_score,  4),
        "recency_days":          round(recency_days, 2),
        "activity_span_days":    round(span_days,    2),
        # Exposure
        "mixer_exposure":        round(mixer_exposure,  4),
        "bridge_exposure":       round(bridge_exposure, 4),
        "vasp_exposure":         round(vasp_exposure,   4),
        # Structuring
        "structuring_ratio":     round(structuring_ratio, 4),
        "peel_chain_score":      round(peel_chain_score,  4),
    }


# ---------------------------------------------------------------------------
# VASP-interaction feature helpers (used by the confidence scorer)
# ---------------------------------------------------------------------------

def compute_interaction_strength(
    vasp_addr: str,
    edges: List[dict],
    total_volume_eth: float,
) -> float:
    """
    Compute how strongly this wallet interacted with a specific VASP,
    measured as the fraction of total traced volume that flowed toward it.

    Returns a 0-100 score.

    A wallet that sent 80 % of its total ETH to Binance scores ~80,
    while one that sent a single 0.01 ETH transaction to a 10 ETH wallet
    scores nearly 0.  This is a key differentiator between "touched the VASP"
    and "primarily used the VASP."
    """
    if total_volume_eth <= 0:
        return 5.0   # minimum evidence — path exists but volume unknown

    vasp_lower = vasp_addr.lower()
    vasp_volume = sum(
        e.get("value_eth", 0.0)
        for e in edges
        if e.get("target", "").lower() == vasp_lower
    )

    ratio = vasp_volume / total_volume_eth
    # Scale: ratio 0→1 maps to score 5→100
    return round(max(5.0, min(100.0, ratio * 100)), 2)


def compute_temporal_recency(
    vasp_addr: str,
    txs: List[dict],
    known_vasps: Dict[str, str],
) -> float:
    """
    Compute a recency score (0-100) for transactions toward this VASP.

    More-recent interactions score higher.  The decay function is:
        score = 100 * exp(-lambda * days_since_last_tx_to_vasp)
    with lambda = 0.02 (half-life ≈ 35 days).

    A wallet that transacted with this VASP yesterday scores ~98.
    A wallet whose last interaction was 180 days ago scores ~27.
    A wallet with no timestamped data scores 50 (neutral).
    """
    import math

    vasp_lower = vasp_addr.lower()
    now_ts = int(time.time())

    # Find the most recent timestamp of a tx to/from this specific VASP
    # We don't have per-edge timestamps in the current edge list, so we
    # fall back to the most recent tx of the root wallet as a proxy.
    # TODO (V2): store per-edge timestamps in the BFS loop for precision.
    timestamps: List[int] = []
    for tx in txs:
        if tx.get("to", "").lower() == vasp_lower or \
           tx.get("from", "").lower() == vasp_lower:
            try:
                ts = int(tx.get("timeStamp", 0))
                if ts > 0:
                    timestamps.append(ts)
            except (ValueError, TypeError):
                pass

    if not timestamps:
        # Fallback: use the wallet's most recent tx of any kind
        all_ts: List[int] = []
        for tx in txs:
            try:
                ts = int(tx.get("timeStamp", 0))
                if ts > 0:
                    all_ts.append(ts)
            except (ValueError, TypeError):
                pass
        if not all_ts:
            return 50.0  # neutral — no temporal data
        most_recent = max(all_ts)
    else:
        most_recent = max(timestamps)

    days_ago = (now_ts - most_recent) / _SECS_PER_DAY
    score = 100.0 * math.exp(-0.02 * max(0.0, days_ago))
    return round(max(5.0, min(100.0, score)), 2)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _zeroed_vector() -> dict:
    return {
        "unique_counterparties": 0,
        "unique_senders":        0,
        "unique_receivers":      0,
        "tx_count":              0,
        "total_value_eth":       0.0,
        "avg_value_eth":         0.0,
        "max_value_eth":         0.0,
        "in_out_ratio":          0.0,
        "value_concentration":   0.0,
        "tx_per_day":            0.0,
        "burst_score":           1.0,
        "recency_days":          0.0,
        "activity_span_days":    0.0,
        "mixer_exposure":        0.0,
        "bridge_exposure":       0.0,
        "vasp_exposure":         0.0,
        "structuring_ratio":     0.0,
        "peel_chain_score":      0.0,
    }


def _structuring_ratio(raw_values: List[int]) -> float:
    """
    Fraction of transactions that share the single most-common value.
    High ratio (> 0.5) with sufficient transaction count = structuring signal.
    """
    if not raw_values:
        return 0.0
    counts = Counter(raw_values)
    top_count = counts.most_common(1)[0][1]
    return top_count / len(raw_values)


def _peel_chain_score(n_senders: int, n_receivers: int, total_txs: int) -> float:
    """
    Returns 1.0 if the wallet looks like a peel-chain node:
    very few unique senders AND receivers, but multiple transactions.
    Classic layering pattern: A → B → C → D each with one sender/receiver.
    """
    if total_txs >= 5 and n_senders <= 2 and n_receivers <= 2:
        return 1.0
    return 0.0


def _compute_burst_score(timestamps: List[int]) -> float:
    """
    Burst score = (peak 24h tx count) / (average 24h tx count).

    A value of 1.0 means perfectly uniform activity.
    High values (> 5) indicate concentrated bursts — a layering signal.
    Capped at 20.0 to avoid extreme outliers dominating the score.
    """
    if len(timestamps) < 3:
        return 1.0

    ts_sorted = sorted(timestamps)
    window    = _SECS_PER_DAY  # 24-hour window

    # Count transactions in a sliding 24h window
    peak = 0
    j    = 0
    for i, ts in enumerate(ts_sorted):
        while ts_sorted[j] < ts - window:
            j += 1
        window_count = i - j + 1
        if window_count > peak:
            peak = window_count

    span_days = (ts_sorted[-1] - ts_sorted[0]) / _SECS_PER_DAY or 1.0
    avg_per_day = len(timestamps) / span_days

    if avg_per_day == 0:
        return 1.0

    burst = peak / avg_per_day
    return round(min(20.0, burst), 2)
