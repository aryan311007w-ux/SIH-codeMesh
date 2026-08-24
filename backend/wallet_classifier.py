"""
Wallet Type Classifier.

Given a wallet address and its transaction list, classifies it into one of
the known wallet archetypes used in blockchain forensics:

  EXCHANGE        — A known centralized exchange (in known_vasps)
  HOT_WALLET      — High-frequency, high-fan-out; likely exchange operational wallet
  DEPOSIT_WALLET  — Receives from one source, forwards to one destination (exchange pattern)
  MIXER           — In known mixer list or shows mixing behavioral patterns
  DEFI_BRIDGE     — Interacts with known bridge contracts
  CROSS_CHAIN     — Funds flow across chain boundaries via bridge/swap
  DARKNET         — In known darknet registry
  SANCTIONS       — OFAC-sanctioned address
  RANSOMWARE      — Known ransomware wallet
  FRAUD           — Known fraud wallet
  UNKNOWN_WALLET  — Unhosted wallet; no classification matched
"""

from collections import Counter
from typing import List

from high_risk_addresses import (
    MIXER_ADDRESSES, RANSOMWARE_ADDRESSES, DARKNET_ADDRESSES,
    SANCTIONS_ADDRESSES, BRIDGE_ADDRESSES, FRAUD_ADDRESSES, get_risk_tag,
)

# Wallet type constants
class WalletType:
    EXCHANGE       = "exchange"
    HOT_WALLET     = "hot_wallet"
    DEPOSIT_WALLET = "deposit_wallet"
    MIXER          = "mixer"
    DEFI_BRIDGE    = "defi_bridge"
    CROSS_CHAIN    = "cross_chain_swap"
    DARKNET        = "darknet"
    SANCTIONS      = "sanctioned"
    RANSOMWARE     = "ransomware"
    FRAUD          = "fraud"
    UNKNOWN        = "unknown_wallet"


def classify_wallet(
    address: str,
    txs: List[dict],
    known_vasps: dict,
) -> dict:
    """
    Classify a wallet and return a dict with:
      - type: WalletType constant string
      - label: human-readable label
      - reason: brief explanation
    """
    addr = address.lower()

    # --- Priority 1: explicit known-bad registries ---
    if addr in SANCTIONS_ADDRESSES:
        tag = get_risk_tag(addr)
        return {"type": WalletType.SANCTIONS, "label": "Sanctioned Address",
                "reason": tag[1] if tag else "OFAC or equivalent sanction"}

    if addr in RANSOMWARE_ADDRESSES:
        tag = get_risk_tag(addr)
        return {"type": WalletType.RANSOMWARE, "label": "Ransomware Wallet",
                "reason": tag[1] if tag else "Known ransomware deposit address"}

    if addr in DARKNET_ADDRESSES:
        tag = get_risk_tag(addr)
        return {"type": WalletType.DARKNET, "label": "Darknet Wallet",
                "reason": tag[1] if tag else "Known darknet marketplace address"}

    if addr in FRAUD_ADDRESSES:
        tag = get_risk_tag(addr)
        return {"type": WalletType.FRAUD, "label": "Fraud Wallet",
                "reason": tag[1] if tag else "Known fraud-linked address"}

    if addr in MIXER_ADDRESSES:
        tag = get_risk_tag(addr)
        return {"type": WalletType.MIXER, "label": "Mixer / Tumbler",
                "reason": tag[1] if tag else "Known mixing service address"}

    if addr in BRIDGE_ADDRESSES:
        tag = get_risk_tag(addr)
        return {"type": WalletType.DEFI_BRIDGE, "label": "DeFi Bridge Contract",
                "reason": tag[1] if tag else "Known cross-chain bridge"}

    # --- Priority 2: in known VASP list ---
    if addr in known_vasps:
        return {"type": WalletType.EXCHANGE, "label": known_vasps[addr],
                "reason": "Address is in the verified VASP/exchange dataset"}

    if not txs:
        return {"type": WalletType.UNKNOWN, "label": "Unknown Wallet",
                "reason": "No transactions available for classification"}

    # --- Priority 3: behavioral analysis ---
    senders   = Counter(tx.get("from", "").lower() for tx in txs if tx.get("from"))
    receivers = Counter(tx.get("to",   "").lower() for tx in txs if tx.get("to"))
    unique_senders   = len(senders)
    unique_receivers = len(receivers)
    total_txs        = len(txs)

    # Check if neighbors include bridge contracts
    all_counterparties = set(senders.keys()) | set(receivers.keys())
    if all_counterparties & BRIDGE_ADDRESSES:
        return {"type": WalletType.CROSS_CHAIN, "label": "Cross-Chain Swap User",
                "reason": "Interacts with known DeFi bridge/swap contracts"}

    # High fan-out + high volume → hot wallet
    if unique_receivers > 50 and total_txs > 100:
        return {"type": WalletType.HOT_WALLET, "label": "Hot Wallet",
                "reason": f"High-frequency wallet: {total_txs} txs, {unique_receivers} unique recipients"}

    # Very few unique counterparties → deposit wallet pattern
    if unique_senders <= 3 and unique_receivers <= 3 and total_txs > 5:
        return {"type": WalletType.DEPOSIT_WALLET, "label": "Deposit Wallet",
                "reason": "Narrow counterparty set: typical exchange deposit wallet pattern"}

    # Mixer behavioral pattern: many equal-value transactions
    if total_txs >= 10:
        values = [int(tx.get("value", 0)) for tx in txs if tx.get("value", "0") != "0"]
        if values:
            most_common_value, most_common_count = Counter(values).most_common(1)[0]
            if most_common_count / len(values) > 0.6:  # >60% same value = structuring/mixing
                return {"type": WalletType.MIXER, "label": "Potential Mixer",
                        "reason": f"Structuring pattern: {most_common_count}/{len(values)} txs have identical value"}

    return {"type": WalletType.UNKNOWN, "label": "Unknown Wallet",
            "reason": "No specific classification matched — likely unhosted personal wallet"}
