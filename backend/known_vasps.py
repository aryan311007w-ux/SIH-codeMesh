"""
Reference list of wallet addresses believed/labeled to belong to
Virtual Asset Service Providers (VASPs) and other named on-chain entities.

Loads curated authoritative VASPs from vasp_registry.py, plus any
supplementary addresses from data/accounts.csv or data/demo_vasps.csv.
"""

from __future__ import annotations
import csv
import os
from typing import Optional
from vasp_registry import VASP_REGISTRY, get_known_vasps_dict

# ---------------------------------------------------------------------------
# Primary VASP / labelled-address dictionary
# ---------------------------------------------------------------------------
KNOWN_VASPS: dict[str, str] = get_known_vasps_dict()


def _load_accounts_csv(path: str) -> None:
    """Load Ethereum mainnet labelled addresses from accounts.csv if present."""
    if not os.path.isfile(path):
        return

    loaded = 0
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("chainId", "").strip() != "1":
                continue
            addr = row.get("address", "").strip().lower()
            if not (addr.startswith("0x") and len(addr) == 42):
                continue
            name_tag = row.get("nameTag", "").strip()
            label = row.get("label", "").strip()
            display = name_tag if name_tag else label
            if display:
                KNOWN_VASPS[addr] = display
                loaded += 1

    if loaded > 0:
        print(f"[known_vasps] Loaded {loaded:,} addresses from {os.path.basename(path)}.")


_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")
_load_accounts_csv(_CSV_PATH)


def get_vasp_label(address: str) -> Optional[str]:
    """Case-insensitive lookup helper."""
    return KNOWN_VASPS.get(address.lower())


def load_from_csv(path: str) -> dict:
    """Bulk-load an additional CSV of labelled addresses into KNOWN_VASPS."""
    if not os.path.isfile(path):
        return KNOWN_VASPS

    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            addr = row.get("address", "").strip().lower()
            if not (addr.startswith("0x") and len(addr) == 42):
                continue
            name = row.get("name", "").strip() or row.get("nameTag", "").strip() or row.get("label", "").strip()
            if name:
                KNOWN_VASPS[addr] = name

    return KNOWN_VASPS
