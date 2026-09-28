"""
CryptoGuard AI - Deterministic High-Fidelity Demo Fixture
Provides comprehensive, repeatable, realistic forensic datasets for demonstration
and offline evaluation without external blockchain API dependencies.

Guarantees 100% deterministic behaviour for SIH evaluation.
Features:
- 1 Suspect Cybercrime Target Wallet
- 7 Intermediary Wallets (Mule accounts, Peel Chains, Rapid Forwarders)
- 1 Sanctioned Mixer (Tornado Cash)
- 3 Distinct VASP Attribution Candidates (CoinDCX FIU-IND, Binance, Kraken)
- 14 Structured Transactions with timestamps, block numbers, and hashes
- Full Timeline, Evidence Ledger, and SAHYOG-Ready Legal Requisitions
"""

from __future__ import annotations
from typing import Dict, List, Any

# Target wallets
_SUSPECT = "0x742d35cc6634c0532925a3b844bc454e4438f44e"
_MULE_ALPHA = "0x111122223333444455556666777788889999aaaa"
_LAYERING_BETA = "0x22223333444455556666777788889999aaaa1111"
_PEEL_1 = "0x3333444455556666777788889999aaaa11112222"
_PEEL_2 = "0x444455556666777788889999aaaa111122223333"
_PEEL_3 = "0x55556666777788889999aaaa1111222233334444"
_OTC_BROKER = "0x6666777788889999aaaa11112222333344445555"
_FORWARDER = "0x777788889999aaaa111122223333444455556666"
_MIXER = "0x722122df12d4e14e13ac3b6895a86e84145b6967"   # Tornado Cash Router

# VASPs
_VASP_COINDCX = "0x503828976d22510aad0201ac7ec88293211d23da"
_VASP_BINANCE = "0x28c6c06298d514db089934071355e5743bf21d60"
_VASP_KRAKEN  = "0x2910543af39aba0cd09dbb2d50200b3e800a63d2"


def demo_trace_result(wallet: str = _SUSPECT, chain: str = "ethereum", case_ref: str = "NCRP-2026-849102") -> Dict[str, Any]:
    """Generates a complete forensic intelligence package for the demo wallet."""
    target_wallet = wallet.lower()

    # VASP Candidates
    vasp_matches = [
        {
            "address": _VASP_COINDCX,
            "vasp_name": "CoinDCX (Neblio Technologies)",
            "hops": 2,
            "confidence": 84.5,
            "confidence_label": "Strong Evidence",
            "relationship_type": "interacts_with",
            "evidence_quality": "high",
            "volume_eth": 3.45,
            "tx_count": 3,
            "first_seen": "2026-09-28T04:15:00Z",
            "last_seen": "2026-09-28T05:32:00Z",
            "path": [target_wallet, _MULE_ALPHA, _VASP_COINDCX],
            "graph_proximity_score": 75.0,
            "interaction_strength_score": 86.2,
            "temporal_recency_score": 96.0,
            "fiu_registered": True,
            "compliance_email": "lawenforcement@coindcx.com",
            "reporting_id": "FIU-IND-REG-2023-0192",
            "country": "India",
            "explanation": (
                "The suspect wallet transferred 3.50 ETH to Mule Account Alpha within 14 minutes of fund ingress. "
                "Mule Account Alpha subsequently routed 3.45 ETH directly into CoinDCX deposit infrastructure. "
                "This creates a direct 2-hop attribution path to a domestic FIU-IND reporting entity with KYC availability."
            ),
            "hop_details": [
                {
                    "hop": 1,
                    "from_addr": target_wallet,
                    "to_addr": _MULE_ALPHA,
                    "from_label": "Suspect Target",
                    "to_label": "Mule Account Alpha",
                    "tx_hash": "0xdemo_tx_001_suspect_to_mule",
                    "value_eth": 3.50,
                    "block_number": 21894010,
                    "timestamp": "2026-09-28T04:15:00Z"
                },
                {
                    "hop": 2,
                    "from_addr": _MULE_ALPHA,
                    "to_addr": _VASP_COINDCX,
                    "from_label": "Mule Account Alpha",
                    "to_label": "CoinDCX Deposit Aggregator",
                    "tx_hash": "0xdemo_tx_004_mule_to_coindcx",
                    "value_eth": 3.45,
                    "block_number": 21894042,
                    "timestamp": "2026-09-28T05:32:00Z"
                }
            ]
        },
        {
            "address": _VASP_BINANCE,
            "vasp_name": "Binance Hot Wallet 6",
            "hops": 3,
            "confidence": 73.8,
            "confidence_label": "Strong Evidence",
            "relationship_type": "interacts_with",
            "evidence_quality": "high",
            "volume_eth": 2.10,
            "tx_count": 2,
            "first_seen": "2026-09-28T04:22:00Z",
            "last_seen": "2026-09-28T06:10:00Z",
            "path": [target_wallet, _PEEL_1, _LAYERING_BETA, _VASP_BINANCE],
            "graph_proximity_score": 55.0,
            "interaction_strength_score": 79.5,
            "temporal_recency_score": 94.0,
            "fiu_registered": True,
            "compliance_email": "case-response@binance.com",
            "reporting_id": "FIU-IND-OFFSHORE-001",
            "country": "Global / FIU-Registered Offshore",
            "explanation": (
                "Suspect wallet engaged in peeling chain layering by sending 2.40 ETH to Peel Node 1. "
                "Peel Node 1 stripped off 0.30 ETH and routed 2.10 ETH to Layering Node Beta, which forwarded "
                "the net funds to Binance Hot Wallet 6. This establishes a 3-hop layering path terminating in a registered offshore exchange."
            ),
            "hop_details": [
                {
                    "hop": 1,
                    "from_addr": target_wallet,
                    "to_addr": _PEEL_1,
                    "from_label": "Suspect Target",
                    "to_label": "Peel Node 1",
                    "tx_hash": "0xdemo_tx_002_suspect_to_peel1",
                    "value_eth": 2.40,
                    "block_number": 21894015,
                    "timestamp": "2026-09-28T04:22:00Z"
                },
                {
                    "hop": 2,
                    "from_addr": _PEEL_1,
                    "to_addr": _LAYERING_BETA,
                    "from_label": "Peel Node 1",
                    "to_label": "Layering Node Beta",
                    "tx_hash": "0xdemo_tx_006_peel1_to_layering",
                    "value_eth": 2.10,
                    "block_number": 21894050,
                    "timestamp": "2026-09-28T05:45:00Z"
                },
                {
                    "hop": 3,
                    "from_addr": _LAYERING_BETA,
                    "to_addr": _VASP_BINANCE,
                    "from_label": "Layering Node Beta",
                    "to_label": "Binance Hot Wallet 6",
                    "tx_hash": "0xdemo_tx_008_layering_to_binance",
                    "value_eth": 2.10,
                    "block_number": 21894065,
                    "timestamp": "2026-09-28T06:10:00Z"
                }
            ]
        },
        {
            "address": _VASP_KRAKEN,
            "vasp_name": "Kraken Exchange Hot Wallet",
            "hops": 3,
            "confidence": 58.2,
            "confidence_label": "Moderate Evidence",
            "relationship_type": "interacts_with",
            "evidence_quality": "medium",
            "volume_eth": 0.28,
            "tx_count": 1,
            "first_seen": "2026-09-28T04:22:00Z",
            "last_seen": "2026-09-28T06:45:00Z",
            "path": [target_wallet, _PEEL_1, _PEEL_2, _VASP_KRAKEN],
            "graph_proximity_score": 50.0,
            "interaction_strength_score": 54.0,
            "temporal_recency_score": 88.0,
            "fiu_registered": False,
            "compliance_email": "subpoena@kraken.com",
            "reporting_id": "FINCEN-MSB-31000136371738",
            "country": "United States",
            "explanation": (
                "Secondary residue funds of 0.30 ETH from Peel Node 1 were split to Peel Node 2, "
                "which transferred 0.28 ETH to Kraken Exchange. Represents low-volume exit path."
            ),
            "hop_details": [
                {
                    "hop": 1,
                    "from_addr": target_wallet,
                    "to_addr": _PEEL_1,
                    "from_label": "Suspect Target",
                    "to_label": "Peel Node 1",
                    "tx_hash": "0xdemo_tx_002_suspect_to_peel1",
                    "value_eth": 2.40,
                    "block_number": 21894015,
                    "timestamp": "2026-09-28T04:22:00Z"
                },
                {
                    "hop": 2,
                    "from_addr": _PEEL_1,
                    "to_addr": _PEEL_2,
                    "from_label": "Peel Node 1",
                    "to_label": "Peel Node 2",
                    "tx_hash": "0xdemo_tx_007_peel1_to_peel2",
                    "value_eth": 0.30,
                    "block_number": 21894052,
                    "timestamp": "2026-09-28T05:48:00Z"
                },
                {
                    "hop": 3,
                    "from_addr": _PEEL_2,
                    "to_addr": _VASP_KRAKEN,
                    "from_label": "Peel Node 2",
                    "to_label": "Kraken Exchange",
                    "tx_hash": "0xdemo_tx_009_peel2_to_kraken",
                    "value_eth": 0.28,
                    "block_number": 21894080,
                    "timestamp": "2026-09-28T06:45:00Z"
                }
            ]
        }
    ]

    top_match = vasp_matches[0]

    # Graph Nodes
    nodes = [
        {"id": target_wallet, "label": "TARGET: Suspect Wallet", "is_root": True, "is_known_vasp": False, "wallet_type": "high_risk_interaction", "risk_level": "HIGH"},
        {"id": _MULE_ALPHA, "label": "Mule Account Alpha", "is_root": False, "is_known_vasp": False, "wallet_type": "deposit_wallet", "risk_level": "MEDIUM"},
        {"id": _LAYERING_BETA, "label": "Layering Node Beta", "is_root": False, "is_known_vasp": False, "wallet_type": "hot_wallet", "risk_level": "MEDIUM"},
        {"id": _PEEL_1, "label": "Peel Chain Node 1", "is_root": False, "is_known_vasp": False, "wallet_type": "hot_wallet", "risk_level": "MEDIUM"},
        {"id": _PEEL_2, "label": "Peel Chain Node 2", "is_root": False, "is_known_vasp": False, "wallet_type": "hot_wallet", "risk_level": "LOW"},
        {"id": _PEEL_3, "label": "Peel Chain Node 3", "is_root": False, "is_known_vasp": False, "wallet_type": "hot_wallet", "risk_level": "LOW"},
        {"id": _OTC_BROKER, "label": "OTC Broker Intermediary", "is_root": False, "is_known_vasp": False, "wallet_type": "hot_wallet", "risk_level": "MEDIUM"},
        {"id": _FORWARDER, "label": "Rapid Forwarder Node", "is_root": False, "is_known_vasp": False, "wallet_type": "hot_wallet", "risk_level": "MEDIUM"},
        {"id": _MIXER, "label": "Tornado Cash (Mixer)", "is_root": False, "is_known_vasp": False, "wallet_type": "mixer", "risk_level": "HIGH"},
        {"id": _VASP_COINDCX, "label": "CoinDCX (FIU-IND)", "is_root": False, "is_known_vasp": True, "vasp_name": "CoinDCX (Neblio Technologies)", "wallet_type": "exchange", "risk_level": "LOW"},
        {"id": _VASP_BINANCE, "label": "Binance Hot Wallet 6", "is_root": False, "is_known_vasp": True, "vasp_name": "Binance Hot Wallet 6", "wallet_type": "exchange", "risk_level": "LOW"},
        {"id": _VASP_KRAKEN, "label": "Kraken Hot Wallet", "is_root": False, "is_known_vasp": True, "vasp_name": "Kraken Exchange Hot Wallet", "wallet_type": "exchange", "risk_level": "LOW"}
    ]

    # Graph Edges
    edges = [
        {"source": target_wallet, "target": _MULE_ALPHA, "value_eth": 3.50, "tx_hash": "0xdemo_tx_001_suspect_to_mule"},
        {"source": target_wallet, "target": _PEEL_1, "value_eth": 2.40, "tx_hash": "0xdemo_tx_002_suspect_to_peel1"},
        {"source": target_wallet, "target": _MIXER, "value_eth": 1.00, "tx_hash": "0xdemo_tx_003_suspect_to_mixer"},
        {"source": _MULE_ALPHA, "target": _VASP_COINDCX, "value_eth": 3.45, "tx_hash": "0xdemo_tx_004_mule_to_coindcx"},
        {"source": target_wallet, "target": _FORWARDER, "value_eth": 0.80, "tx_hash": "0xdemo_tx_005_suspect_to_forwarder"},
        {"source": _PEEL_1, "target": _LAYERING_BETA, "value_eth": 2.10, "tx_hash": "0xdemo_tx_006_peel1_to_layering"},
        {"source": _PEEL_1, "target": _PEEL_2, "value_eth": 0.30, "tx_hash": "0xdemo_tx_007_peel1_to_peel2"},
        {"source": _LAYERING_BETA, "target": _VASP_BINANCE, "value_eth": 2.10, "tx_hash": "0xdemo_tx_008_layering_to_binance"},
        {"source": _PEEL_2, "target": _VASP_KRAKEN, "value_eth": 0.28, "tx_hash": "0xdemo_tx_009_peel2_to_kraken"},
        {"source": _PEEL_2, "target": _PEEL_3, "value_eth": 0.02, "tx_hash": "0xdemo_tx_010_peel2_to_peel3"},
        {"source": _FORWARDER, "target": _OTC_BROKER, "value_eth": 0.78, "tx_hash": "0xdemo_tx_011_forwarder_to_otc"},
        {"source": _OTC_BROKER, "target": _VASP_BINANCE, "value_eth": 0.76, "tx_hash": "0xdemo_tx_012_otc_to_binance"}
    ]

    # Chronological Timeline
    timeline = [
        {
            "time": "2026-09-28T04:00:00Z",
            "title": "Suspect Wallet Inflow (Victim Funds)",
            "desc": "Victim reporting NCRP fraud deposited 7.70 ETH into suspect wallet.",
            "type": "inflow",
            "wallet": target_wallet,
            "tx_hash": "0xdemo_tx_000_victim_deposit",
            "amount": 7.70
        },
        {
            "time": "2026-09-28T04:15:00Z",
            "title": "Hop 1: Rapid Mule Dispersal",
            "desc": "3.50 ETH routed to Mule Account Alpha within 15 minutes.",
            "type": "layering",
            "wallet": _MULE_ALPHA,
            "tx_hash": "0xdemo_tx_001_suspect_to_mule",
            "amount": 3.50
        },
        {
            "time": "2026-09-28T04:22:00Z",
            "title": "Hop 1: Peel Chain Initiated",
            "desc": "2.40 ETH routed to Peel Node 1 for structured peeling.",
            "type": "layering",
            "wallet": _PEEL_1,
            "tx_hash": "0xdemo_tx_002_suspect_to_peel1",
            "amount": 2.40
        },
        {
            "time": "2026-09-28T04:30:00Z",
            "title": "Mixer Obfuscation Attempt",
            "desc": "1.00 ETH deposited into Tornado Cash Mixer contract.",
            "type": "mixer_interaction",
            "wallet": _MIXER,
            "tx_hash": "0xdemo_tx_003_suspect_to_mixer",
            "amount": 1.00
        },
        {
            "time": "2026-09-28T05:32:00Z",
            "title": "Hop 2: CoinDCX Ingress (Primary Cashout)",
            "desc": "3.45 ETH deposited into CoinDCX exchange deposit address.",
            "type": "vasp_interaction",
            "wallet": _VASP_COINDCX,
            "tx_hash": "0xdemo_tx_004_mule_to_coindcx",
            "amount": 3.45
        },
        {
            "time": "2026-09-28T05:45:00Z",
            "title": "Hop 2: Peel Node 1 Split",
            "desc": "2.10 ETH sent to Layering Beta; 0.30 ETH peeled to Peel Node 2.",
            "type": "layering",
            "wallet": _LAYERING_BETA,
            "tx_hash": "0xdemo_tx_006_peel1_to_layering",
            "amount": 2.10
        },
        {
            "time": "2026-09-28T06:10:00Z",
            "title": "Hop 3: Binance Dispersal (Secondary Cashout)",
            "desc": "2.10 ETH received by Binance Hot Wallet 6.",
            "type": "vasp_interaction",
            "wallet": _VASP_BINANCE,
            "tx_hash": "0xdemo_tx_008_layering_to_binance",
            "amount": 2.10
        },
        {
            "time": "2026-09-28T06:45:00Z",
            "title": "Hop 3: Kraken Deposit (Residue Cashout)",
            "desc": "0.28 ETH deposited into Kraken Hot Wallet.",
            "type": "vasp_interaction",
            "wallet": _VASP_KRAKEN,
            "tx_hash": "0xdemo_tx_009_peel2_to_kraken",
            "amount": 0.28
        }
    ]

    # Evidence Ledger
    evidence = [
        {
            "id": "EV-849102-01",
            "tx_hash": "0xdemo_tx_004_mule_to_coindcx",
            "direction": "outbound",
            "counterparty": _VASP_COINDCX,
            "counterparty_label": "CoinDCX (Neblio Technologies) [FIU-IND Registered]",
            "value_eth": 3.45,
            "timestamp": "2026-09-28T05:32:00Z",
            "source": "Deterministic Demo Fixture",
            "status": "Relevant",
            "note": "Primary VASP attribution path (2 hops). 3.45 ETH deposited into FIU-registered exchange."
        },
        {
            "id": "EV-849102-02",
            "tx_hash": "0xdemo_tx_008_layering_to_binance",
            "direction": "outbound",
            "counterparty": _VASP_BINANCE,
            "counterparty_label": "Binance Hot Wallet 6 [FIU Registered Offshore]",
            "value_eth": 2.10,
            "timestamp": "2026-09-28T06:10:00Z",
            "source": "Deterministic Demo Fixture",
            "status": "Relevant",
            "note": "Secondary VASP attribution path (3 hops). 2.10 ETH layered through peel chain into Binance."
        },
        {
            "id": "EV-849102-03",
            "tx_hash": "0xdemo_tx_003_suspect_to_mixer",
            "direction": "outbound",
            "counterparty": _MIXER,
            "counterparty_label": "Tornado Cash (Mixer - OFAC Sanctioned)",
            "value_eth": 1.00,
            "timestamp": "2026-09-28T04:30:00Z",
            "source": "Deterministic Demo Fixture",
            "status": "Relevant",
            "note": "Mixer interaction flagged by Risk Engine. Direct deposit to obfuscation pool."
        },
        {
            "id": "EV-849102-04",
            "tx_hash": "0xdemo_tx_001_suspect_to_mule",
            "direction": "outbound",
            "counterparty": _MULE_ALPHA,
            "counterparty_label": "Mule Account Alpha",
            "value_eth": 3.50,
            "timestamp": "2026-09-28T04:15:00Z",
            "source": "Deterministic Demo Fixture",
            "status": "Reviewed",
            "note": "Hop 1 transfer executed within 15 mins of victim fund ingress."
        },
        {
            "id": "EV-849102-05",
            "tx_hash": "0xdemo_tx_009_peel2_to_kraken",
            "direction": "outbound",
            "counterparty": _VASP_KRAKEN,
            "counterparty_label": "Kraken Hot Wallet",
            "value_eth": 0.28,
            "timestamp": "2026-09-28T06:45:00Z",
            "source": "Deterministic Demo Fixture",
            "status": "Needs Verification",
            "note": "Residue transfer after 3 hops."
        }
    ]

    # SAHYOG / Cybercrime Legal Request Package
    sahyog = {
        "status": "ready",
        "action": "ACTION REQUIRED: Issue Section 91 CrPC / Section 94 BNSS KYC Disclosure to CoinDCX & Binance",
        "primary_vasp": "CoinDCX (Neblio Technologies)",
        "primary_fiu_id": "FIU-IND-REG-2023-0192",
        "primary_email": "lawenforcement@coindcx.com",
        "secondary_vasp": "Binance Hot Wallet 6",
        "secondary_fiu_id": "FIU-IND-OFFSHORE-001",
        "secondary_email": "case-response@binance.com",
        "frozen_amount_recommended": "5.55 ETH (~$14,400 USD)",
        "case_ref": case_ref,
        "disclosure_note": (
            "Suspect wallet demonstrated immediate layering and cash-out flow of 3.45 ETH to CoinDCX "
            "and 2.10 ETH to Binance Hot Wallet within 2 hours of complaint ingress. "
            "Pursuant to PMLA (2002) and Section 91 CrPC, serve urgent account freezing and KYC requisition notices."
        )
    }

    return {
        "wallet": target_wallet,
        "chain": chain,
        "case_ref": case_ref,
        "total_transactions_scanned": 14,
        "hops_searched": 3,
        "matches": vasp_matches,
        "top_match": top_match,
        "risk": {
            "risk_score": 82,
            "risk_level": "HIGH",
            "flags": [
                "rapid_fund_movement",
                "mixer_interaction",
                "peel_chain",
                "multiple_intermediary_hops",
                "high_value_flow"
            ],
            "typologies": [
                "Layering via Mixer Obfuscation",
                "Peel Chain Structuring",
                "Multi-Hop VASP Dispersal",
                "High-Velocity Rapid Exit"
            ],
            "details": {
                "mixer_interaction": 45,
                "rapid_fund_movement": 30,
                "peel_chain": 25,
                "multiple_intermediary_hops": 20,
                "high_value_flow": 15
            }
        },
        "wallet_classification": {
            "type": "layering_like",
            "label": "Layering / Mule Dispersal Hub",
            "reason": "Rapid fund ingress followed by immediate fan-out to peel chains, mixer, and VASP deposit accounts within 120 minutes."
        },
        "wallet_features": {
            "unique_counterparties": 7,
            "unique_senders": 1,
            "unique_receivers": 6,
            "tx_count": 14,
            "total_value_eth": 7.70,
            "avg_value_eth": 0.55,
            "max_value_eth": 3.50,
            "in_out_ratio": 0.95,
            "value_concentration": 0.45,
            "tx_per_day": 8.5,
            "burst_score": 3.4,
            "recency_days": 0.1,
            "activity_span_days": 0.2,
            "mixer_exposure": 0.14,
            "bridge_exposure": 0.0,
            "vasp_exposure": 0.42,
            "structuring_ratio": 0.35,
            "peel_chain_score": 0.85
        },
        "sahyog_routing": sahyog,
        "nodes": nodes,
        "edges": edges,
        "timeline": timeline,
        "evidence": evidence,
        "note": "Deterministic Law-Enforcement Demo Case (NCRP-2026-849102)",
        "timestamp": "2026-09-28T07:00:00Z",
        "_demo_mode": True
    }


def demo_health_status() -> Dict[str, Any]:
    """Health check response showing full operational status."""
    return {
        "status": "ok",
        "product": "CryptoGuard AI",
        "tagline": "AI-Powered Blockchain Investigation & VASP Attribution Platform",
        "version": "2.0.0-SIH26182",
        "api_key_configured": False,
        "demo_mode": True,
        "supported_chains": ["ethereum", "bsc", "polygon", "tron", "bitcoin"],
        "known_vasp_count": 22,
        "fiu_registered_count": 8,
        "database": "SQLite (cryptoguard.db)",
        "max_hops": 3
    }
