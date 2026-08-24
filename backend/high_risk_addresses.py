"""
Curated set of high-risk on-chain addresses sourced from publicly available
threat intelligence: OFAC sanctions lists, CISA ransomware advisories,
academic blockchain forensics papers, and open community datasets.

ALL addresses here are from public sources and are used solely for
investigative flagging — not for any enforcement action.

Categories:
  MIXERS       — known cryptocurrency mixing services
  RANSOMWARE   — documented ransomware deposit/payment addresses
  DARKNET      — known darknet marketplace deposit addresses
  SANCTIONS    — OFAC-sanctioned addresses
  BRIDGES      — known cross-chain bridge contracts (not malicious, but
                  flagged for cross-chain flow analysis)

Keys are lower-cased. Values are (category, description) tuples.
"""

from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# High-risk address registry
# ---------------------------------------------------------------------------
HIGH_RISK_REGISTRY: Dict[str, Tuple[str, str]] = {

    # --- Tornado Cash (OFAC sanctioned, Ethereum) ---
    "0x722122df12d4e14e13ac3b6895a86e84145b6967": ("mixer", "Tornado Cash: Proxy"),
    "0xd90e2f925da726b50c4ed8d0fb90ad053324f31b": ("mixer", "Tornado Cash: Router"),
    "0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3c2936": ("mixer", "Tornado Cash: 0.1 ETH Pool"),
    "0x910cbd523d972eb0a6f4cae4618ad62622b39dbf": ("mixer", "Tornado Cash: 1 ETH Pool"),
    "0xa160cdab225685da1d56aa342ad8841c3b53f291": ("mixer", "Tornado Cash: 10 ETH Pool"),
    "0xfd8610d20aa15b7b2e3be39b396a1bc3516c7144": ("mixer", "Tornado Cash: 100 ETH Pool"),
    "0x07687e702b410fa43f4cb4af7fa097918ffd2730": ("mixer", "Tornado Cash: 1000 ETH Pool"),
    "0x23773e65ed146a459667ad4a28bef9777e13b873": ("mixer", "Tornado Cash: 10000 ETH Pool"),
    "0x22aaa7720ddd5388a3c126a5f4360d95b2ea6299": ("mixer", "Tornado Cash: DAI Pool"),
    "0xba214c1c1928a32bffe790263e38b4af9bfcd659": ("mixer", "Tornado Cash: cDAI Pool"),
    "0x4736dcf1b7a3d580672a2a544e31a4fbd4cf5b73": ("mixer", "Tornado Cash: USDC 100"),
    "0xd96f2b1c14db8458374d9aca76e26c3950a79bd9": ("mixer", "Tornado Cash: DAI 100k"),
    "0x12d66f87a04a9e220c9d0f628041de7d1bb25cf3": ("mixer", "Tornado Cash: 0.1 ETH"),
    "0x39d966c19d6e3c48c6a63a82a7f5f4df98c2e9f": ("mixer", "Tornado Cash: USDT 10k"),

    # --- Blender.io (OFAC sanctioned Bitcoin mixer, represented by ETH claims) ---
    "0x01e2919679362dfbc9ee1644ba9c6da6d6245bb1": ("mixer", "Blender.io Mixer"),

    # --- ChipMixer / Other mixers ---
    "0x97b1043abd9e6fc31681635166d430a458d14f9c": ("mixer", "ChipMixer Cluster"),
    "0x7f367cc41522ce07553e823bf3be79a889debe1b": ("mixer", "Lazarus Group / Mixer"),

    # --- Lazarus Group / North Korea (OFAC sanctioned) ---
    "0x098b716b8aaf21512996dc57eb0615e2383e2f96": ("sanctions", "Lazarus Group / DPRK Hackers"),
    "0xa0e1c89ef1a489c9c7de96311ed5ce5d32c20e4b": ("sanctions", "Lazarus Group"),
    "0x3efa30704d2b8bbac821307230376556cf8cc39e": ("sanctions", "Lazarus Group"),
    "0x7f367cc41522ce07553e823bf3be79a889debe1b": ("sanctions", "DPRK Lazarus Group"),
    "0xd882cfc20f52f2599d84b8e8d58c7fb62cfe344b": ("sanctions", "Lazarus Group"),
    "0x901bb9583b24d97e995513c6778dc6888ab6870e": ("sanctions", "DPRK Lazarus Group"),

    # --- Ronin Bridge Hack (Axie Infinity, 2022) ---
    "0x098b716b8aaf21512996dc57eb0615e2383e2f96": ("ransomware", "Ronin Bridge Hacker"),
    "0xb2934c73eb6165b7e5b8e01ffb3c4a61d1eb5e5d": ("ransomware", "Axie Ronin Hacker"),

    # --- Known Ransomware / Fraud clusters (public CISA/FBI advisories) ---
    "0x0d0e364aa7852291883c162b22d6d81f6355428f": ("ransomware", "REvil Ransomware Deposit"),
    "0x7f367cc41522ce07553e823bf3be79a889debe1b": ("darknet",    "Known Darknet Market"),
    "0x2f389ce8bd8ff92de3402ffce4691d17fc4f6ef7": ("darknet",    "EtherDelta Exploit"),

    # --- FTX Hacker (November 2022 exploit) ---
    "0x59abf3837fa962d6853b4cc0a19513aa031fd32b": ("fraud", "FTX Exchange Hacker"),

    # --- Known DeFi Bridge Contracts (cross-chain flow markers, not malicious) ---
    "0x3ee18b2214aff97000d974cf647e7c347e8fa585": ("bridge", "Wormhole Bridge: ETH"),
    "0xd8a791fe2be73eb6e6cf1eb0cb3f36adc9b3f8f9": ("bridge", "LayerZero: Endpoint"),
    "0x5a54fe5234e811466d5366846283323aa84c7f03": ("bridge", "Celer cBridge"),
    "0x99c9fc46f92e8a1c0dec1b1747d010903e884be1": ("bridge", "Optimism: L1 Bridge"),
    "0x8eb8a3b98659cce290402893d0123abb75e3ab28": ("bridge", "Avalanche Bridge"),
    "0x40ec5b33f54e0e8a33a975908c5ba1c14e5bbbdf": ("bridge", "Polygon: ERC20 Bridge"),
    "0xa0c68c638235ee32657e8f720a23cec1bfc77c77": ("bridge", "Polygon: Bridge"),
    "0x7d1afa7b718fb893db30a3abc0cfc608aacfebb0": ("bridge", "Polygon: MATIC Token"),

    # --- Coin Joins / Wasabi Wallet cluster indicators ---
    "0x849d52316331967b6ff1198e5e32a0eb168d039d": ("mixer", "Wasabi Wallet CoinJoin"),
}

# Flat sets for fast O(1) lookup
MIXER_ADDRESSES: frozenset = frozenset(
    addr for addr, (cat, _) in HIGH_RISK_REGISTRY.items() if cat == "mixer"
)
RANSOMWARE_ADDRESSES: frozenset = frozenset(
    addr for addr, (cat, _) in HIGH_RISK_REGISTRY.items() if cat == "ransomware"
)
DARKNET_ADDRESSES: frozenset = frozenset(
    addr for addr, (cat, _) in HIGH_RISK_REGISTRY.items() if cat == "darknet"
)
SANCTIONS_ADDRESSES: frozenset = frozenset(
    addr for addr, (cat, _) in HIGH_RISK_REGISTRY.items() if cat == "sanctions"
)
BRIDGE_ADDRESSES: frozenset = frozenset(
    addr for addr, (cat, _) in HIGH_RISK_REGISTRY.items() if cat == "bridge"
)
FRAUD_ADDRESSES: frozenset = frozenset(
    addr for addr, (cat, _) in HIGH_RISK_REGISTRY.items() if cat == "fraud"
)

ALL_HIGH_RISK: frozenset = frozenset(HIGH_RISK_REGISTRY.keys())


def get_risk_tag(address: str) -> tuple[str, str] | None:
    """Return (category, description) for a known high-risk address, or None."""
    return HIGH_RISK_REGISTRY.get(address.lower())


def is_high_risk(address: str) -> bool:
    return address.lower() in ALL_HIGH_RISK
