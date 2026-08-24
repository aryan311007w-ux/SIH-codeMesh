"""
Chain metadata and configuration for all supported blockchains.
Indexed by a short string key used as the `chain` query parameter in the API.
"""

SUPPORTED_CHAINS: dict = {
    "ethereum": {
        "name": "Ethereum",
        "symbol": "ETH",
        "chain_id": 1,                      # Etherscan v2 chainid
        "native_token": "ETH",
        "decimals": 18,
        "explorer_url": "https://etherscan.io",
        "type": "evm",                      # adapter type
        "color": "#627EEA",
    },
    "bsc": {
        "name": "BNB Chain",
        "symbol": "BNB",
        "chain_id": 56,
        "native_token": "BNB",
        "decimals": 18,
        "explorer_url": "https://bscscan.com",
        "type": "evm",
        "color": "#F3BA2F",
    },
    "polygon": {
        "name": "Polygon",
        "symbol": "MATIC",
        "chain_id": 137,
        "native_token": "MATIC",
        "decimals": 18,
        "explorer_url": "https://polygonscan.com",
        "type": "evm",
        "color": "#8247E5",
    },
    "tron": {
        "name": "Tron",
        "symbol": "TRX",
        "chain_id": None,
        "native_token": "TRX",
        "decimals": 6,
        "explorer_url": "https://tronscan.org/#/transaction",
        "type": "tron",
        "color": "#EF0027",
    },
    "bitcoin": {
        "name": "Bitcoin",
        "symbol": "BTC",
        "chain_id": None,
        "native_token": "BTC",
        "decimals": 8,
        "explorer_url": "https://blockstream.info/tx",
        "type": "bitcoin",
        "color": "#F7931A",
    },
}

# Address format validation per chain type
ADDRESS_PATTERNS = {
    "evm":     lambda a: a.startswith("0x") and len(a) == 42,
    "tron":    lambda a: a.startswith("T") and len(a) == 34,
    "bitcoin": lambda a: len(a) >= 25 and len(a) <= 62,
}


def validate_address(address: str, chain: str) -> bool:
    """Return True if address looks valid for the given chain."""
    meta = SUPPORTED_CHAINS.get(chain)
    if not meta:
        return False
    chain_type = meta["type"]
    validator = ADDRESS_PATTERNS.get(chain_type)
    return bool(validator and validator(address))


def get_chain_type(chain: str) -> str:
    return SUPPORTED_CHAINS.get(chain, {}).get("type", "evm")
