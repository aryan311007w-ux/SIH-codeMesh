"""
Demo Fixture — SIH-26182
========================
Provides fully deterministic, offline trace results for frontend demos
and integration tests that do NOT need live blockchain API calls.

Usage:
    from demo_fixture import demo_trace_result, demo_health_status
    result = demo_trace_result(wallet="0xd8dA...06045", chain="ethereum")

All values are synthetic. No real blockchain data is embedded.
"""

from __future__ import annotations

import os as _os
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Synthetic wallet addresses used in the demo trace graph
# ---------------------------------------------------------------------------

_ROOT  = "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
_MID   = "0xbbbb000000000000000000000000000000000002"
_VASP  = "0x28c6c06298d514db089934071355e5743bf21d60"   # Binance Hot Wallet
_MIXER = "0x722122df12d4e14e13ac3b6895a86e84145b6967"   # Tornado Cash


# ---------------------------------------------------------------------------
# Demo trace result — deterministic for any wallet address
# ---------------------------------------------------------------------------

def demo_trace_result(wallet: str = _ROOT, chain: str = "ethereum") -> dict:
    """Return a realistic, deterministic trace result for demo/testing."""
    now_iso = datetime.now(timezone.utc).isoformat()
    w = wallet.lower()

    # ── Compute confidence using the documented 4-component formula ─────────
    # graph_proximity_score      = 50.0  (hop-2 path)
    # interaction_strength_score = 72.3  (deterministic for this demo graph)
    # temporal_recency_score     = 88.1  (deterministic for this demo graph)
    # evidence_quality           = "medium" → 65
    # confidence = 0.40×50 + 0.30×72.3 + 0.20×88.1 + 0.10×65 = 65.85 → 65.9
    _graph_proximity      = 50.0
    _interaction_strength = 72.3
    _temporal_recency     = 88.1
    _evidence_quality     = "medium"   # community-labelled dataset
    _evidence_score       = 65
    _confidence = round(
        0.40 * _graph_proximity
      + 0.30 * _interaction_strength
      + 0.20 * _temporal_recency
      + 0.10 * _evidence_score,
        1,
    )

    top_match = {
        "address":                   _VASP,
        "vasp_name":                 "Binance Hot Wallet",
        "hops":                      2,
        "confidence":                _confidence,
        "path":                      [w, _MID, _VASP],
        "volume_eth":                0.45,
        "relationship_type":         "interacts_with",
        "evidence_quality":          _evidence_quality,
        "graph_proximity_score":     _graph_proximity,
        "interaction_strength_score":_interaction_strength,
        "temporal_recency_score":    _temporal_recency,
        # DEMO / SYNTHETIC — no real blockchain transactions
        "evidence":                  _build_demo_evidence(w),
    }

    sahyog = {
        "vasp_name":       "Binance Hot Wallet",
        "vasp_address":    _VASP,
        "action":          "Voluntary disclosure inquiry to Binance Hot Wallet",
        "disclosure_note": (
            "Low-risk wallet. Traced wallet interacts with Binance Hot Wallet "
            f"(confidence: {_confidence}%, relationship: interacts_with). "
            "Standard disclosure inquiry via SAHYOG may be appropriate."
        ),
    }

    evidence = _build_demo_evidence(w)

    return {
        "wallet":                     w,
        "chain":                      chain,
        "total_transactions_scanned": 6,
        "hops_searched":              3,
        "matches":                    [{**top_match}],
        "top_match":                  top_match,
        "risk": {
            "risk_score":  35,
            "risk_level":  "MEDIUM",
            "flags":       ["mixer_proximity"],
            "typologies":  ["Proximity to mixer (Tornado Cash)"],
            "details":     {"mixer_proximity": 25},
        },
        "wallet_classification": {
            "type":   "hot_wallet",
            "label":  "Hot Wallet",
            "reason": "Regular outbound transactions, narrow counterparty set (<=5 unique).",
        },
        "wallet_features": {
            "unique_counterparties": 4,
            "unique_senders":       2,
            "unique_receivers":     3,
            "tx_count":             6,
            "total_value_eth":      1.25,
            "avg_value_eth":        0.208333,
            "max_value_eth":        0.5,
            "in_out_ratio":         0.55,
            "value_concentration":  0.4,
            "tx_per_day":           3.2,
            "burst_score":          2.1,
            "recency_days":         2.0,
            "activity_span_days":   1.8,
            "mixer_exposure":       0.25,
            "bridge_exposure":      0.0,
            "vasp_exposure":        0.25,
            "structuring_ratio":    0.17,
            "peel_chain_score":     0.0,
        },
        "sahyog_routing":             sahyog,
        "nodes": [
            {
                "id":            w,
                "label":         f"{w[:8]}...",
                "is_known_vasp": False,
                "vasp_name":     None,
                "is_root":       True,
                "wallet_type":   "hot_wallet",
                "risk_level":    "MEDIUM",
            },
            {
                "id":            _MID,
                "label":         f"{_MID[:8]}...",
                "is_known_vasp": False,
                "vasp_name":     None,
                "is_root":       False,
                "wallet_type":   "hot_wallet",
                "risk_level":    "LOW",
            },
            {
                "id":            _VASP,
                "label":         "Binance Hot Wallet",
                "is_known_vasp": True,
                "vasp_name":     "Binance Hot Wallet",
                "is_root":       False,
                "wallet_type":   "exchange",
                "risk_level":    "LOW",
            },
            {
                "id":            _MIXER,
                "label":         "Tornado Cash",
                "is_known_vasp": False,
                "vasp_name":     None,
                "is_root":       False,
                "wallet_type":   "mixer",
                "risk_level":    "HIGH",
            },
        ],
        "edges": [
            {
                "source":    w,
                "target":    _MID,
                "value_eth": 0.5,
                "tx_hash":   "0xdemo_tx_001",
            },
            {
                "source":    w,
                "target":    _MIXER,
                "value_eth": 0.1,
                "tx_hash":   "0xdemo_tx_002",
            },
            {
                "source":    _MID,
                "target":    _VASP,
                "value_eth": 0.4,
                "tx_hash":   "0xdemo_tx_003",
            },
        ],
        "note": None,
        "timestamp": now_iso,
        "evidence": evidence,
    }


def demo_health_status() -> dict:
    """Return a health status response reflecting the actual runtime configuration."""
    _ek = _os.getenv("ETHERSCAN_API_KEY", "")
    _tk = _os.getenv("TRONGRID_API_KEY", "")
    _demo = not bool(_ek)
    return {
        "status":             "ok",
        "api_key_configured": bool(_ek),
        "known_vasp_count":   10,
        "max_hops":           3,
        "supported_chains":   ["ethereum", "bsc", "polygon", "tron", "bitcoin"],
        "demo_mode":          _demo,
        "vasp_data_source":   "demo_vasps.csv (10 addresses - fallback loaded)",
        "api_sources": {
            "etherscan": ("configured" if _ek else "not configured (demo mode)"),
            "trongrid":  ("configured" if _tk else "not configured (demo mode)"),
            "bitcoin":   "blockstream.info (no key required)",
        },
    }


def _build_demo_evidence(wallet: str) -> list[dict]:
    """
    Return deterministic synthetic transaction evidence for the demo.

    All entries are synthetic. No real blockchain transaction data is embedded.
    The `tx_hash` values are prefixed with ``0xdemo_`` to make this visible.
    """
    return [
        {
            "tx_hash":         "0xdemo_tx_001",
            "direction":       "outbound",
            "counterparty":    _MID,
            "counterparty_label": f"{_MID[:8]}... (intermediate)",
            "value_eth":       0.5,
            "timestamp":       "2026-01-15T10:30:00Z",
            "note":            "DEMO — Synthetic transaction",
        },
        {
            "tx_hash":         "0xdemo_tx_002",
            "direction":       "outbound",
            "counterparty":    _MIXER,
            "counterparty_label": "Tornado Cash (Mixer — High Risk)",
            "value_eth":       0.1,
            "timestamp":       "2026-01-15T10:35:00Z",
            "note":            "DEMO — Synthetic transaction; proximity to mixer flagged by risk engine",
        },
        {
            "tx_hash":         "0xdemo_tx_003",
            "direction":       "outbound",
            "counterparty":    _VASP,
            "counterparty_label": "Binance Hot Wallet",
            "value_eth":       0.4,
            "timestamp":       "2026-01-15T10:40:00Z",
            "note":            "DEMO — Synthetic transaction; primary VASP attribution path",
        },
    ]
