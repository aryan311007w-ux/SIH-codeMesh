"""
Reference list of wallet addresses believed/labeled to belong to
Virtual Asset Service Providers (VASPs) and other named on-chain entities.

Data source: data/accounts.csv  (113,000+ Ethereum mainnet labelled addresses)
  Columns: address, chainId, label, nameTag
  - Only chainId == "1" (Ethereum mainnet) rows are loaded.
  - nameTag is used as the display name when present; falls back to label.

The dictionary is populated automatically when this module is imported.
Keys are lower-cased addresses (the tracer always lower-cases before lookup).
"""

import csv
import os

# ---------------------------------------------------------------------------
# Primary VASP / labelled-address dictionary
# ---------------------------------------------------------------------------
KNOWN_VASPS: dict[str, str] = {}


def _load_accounts_csv(path: str) -> None:
    """
    Load Ethereum mainnet labelled addresses from accounts.csv into KNOWN_VASPS.

    CSV format (accounts.csv):
        address,chainId,label,nameTag
        0xabc...,1,binance,Binance: Hot Wallet
        ...

    Rules applied while loading:
      - Only rows where chainId == "1" (Ethereum mainnet) are kept.
      - Address must be valid: 0x + exactly 40 hex chars (42 total).
      - Display name = nameTag if non-empty, else label.
      - Duplicate addresses are silently overwritten (last row wins).
    """
    if not os.path.isfile(path):
        # Fail gracefully so the server still starts even without the data file.
        print(f"[known_vasps] WARNING: {path!r} not found — KNOWN_VASPS will be empty.")
        return

    loaded = 0
    skipped = 0
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Only Ethereum mainnet
            if row.get("chainId", "").strip() != "1":
                skipped += 1
                continue

            addr = row.get("address", "").strip().lower()
            # Validate address format: 0x + 40 hex chars
            if not (addr.startswith("0x") and len(addr) == 42):
                skipped += 1
                continue

            name_tag = row.get("nameTag", "").strip()
            label    = row.get("label",   "").strip()
            display  = name_tag if name_tag else label
            if not display:
                skipped += 1
                continue

            KNOWN_VASPS[addr] = display
            loaded += 1

    print(f"[known_vasps] Loaded {loaded:,} addresses from {os.path.basename(path)} "
          f"({skipped:,} rows skipped).")


# ---------------------------------------------------------------------------
# Auto-load at import time — path is relative to this file's directory so it
# works regardless of where uvicorn is launched from.
# ---------------------------------------------------------------------------
_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")
_load_accounts_csv(_CSV_PATH)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_vasp_label(address: str) -> str | None:
    """Case-insensitive lookup helper."""
    return KNOWN_VASPS.get(address.lower())


def load_from_csv(path: str) -> dict:
    """
    Bulk-load an additional CSV of labelled addresses into KNOWN_VASPS.

    Supports two CSV formats:
      1. accounts.csv format:  address, chainId, label, nameTag
         (only chainId==1 rows loaded; nameTag preferred over label)
      2. Simple format:        address, name
         (used by the original load_from_csv callers)

    Any rows with malformed addresses are silently skipped.
    Returns the updated KNOWN_VASPS dict.
    """
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []

        if "chainId" in fieldnames:
            # accounts.csv style
            for row in reader:
                if row.get("chainId", "").strip() != "1":
                    continue
                addr = row.get("address", "").strip().lower()
                if not (addr.startswith("0x") and len(addr) == 42):
                    continue
                name_tag = row.get("nameTag", "").strip()
                label    = row.get("label",   "").strip()
                display  = name_tag if name_tag else label
                if display:
                    KNOWN_VASPS[addr] = display
        else:
            # Simple address,name format
            for row in reader:
                addr = row.get("address", "").strip().lower()
                if not (addr.startswith("0x") and len(addr) == 42):
                    continue
                name = row.get("name", "").strip()
                if name:
                    KNOWN_VASPS[addr] = name

    return KNOWN_VASPS
