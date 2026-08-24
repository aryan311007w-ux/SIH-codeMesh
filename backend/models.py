"""Pydantic models used for API request/response schemas."""

from __future__ import annotations
from typing import List, Optional, Dict
from pydantic import BaseModel
from enum import Enum


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RiskLevel(str, Enum):
    HIGH   = "HIGH"
    MEDIUM = "MEDIUM"
    LOW    = "LOW"


class WalletTypeEnum(str, Enum):
    EXCHANGE        = "exchange"
    HOT_WALLET      = "hot_wallet"
    DEPOSIT_WALLET  = "deposit_wallet"
    MIXER           = "mixer"
    DEFI_BRIDGE     = "defi_bridge"
    CROSS_CHAIN     = "cross_chain_swap"
    DARKNET         = "darknet"
    SANCTIONS       = "sanctioned"
    RANSOMWARE      = "ransomware"
    FRAUD           = "fraud"
    UNKNOWN         = "unknown_wallet"


class RelationshipType(str, Enum):
    """
    Precisely describes how the traced wallet relates to the matched VASP.

    interacts_with
        A transaction path exists between the traced wallet and the VASP
        address. The VASP may or may not *own* the wallet — this is the
        correct default claim for any BFS-discovered path. It means:
        "funds from this wallet were observed flowing toward this VASP."

    controlled_by
        Strong evidence that the VASP directly controls the traced wallet
        (e.g. the address is a labelled deposit wallet in the VASP's own
        registry, or it shows deposit-wallet behavioural patterns sending
        exclusively to one exchange). Requires substantially stronger
        evidence than graph proximity alone. Do NOT assert this from BFS
        alone.

    laundered_through
        Funds demonstrably moved INTO the VASP and were subsequently
        withdrawn to a different destination address — a classic layering
        pattern. Requires directional flow evidence beyond the basic trace.
    """
    INTERACTS_WITH    = "interacts_with"
    CONTROLLED_BY     = "controlled_by"
    LAUNDERED_THROUGH = "laundered_through"


class EvidenceQuality(str, Enum):
    """
    Provenance confidence of the VASP address label itself.

    high    — Verified authoritative source: OFAC list, official VASP
              disclosure, Etherscan verified contract tag, or government
              intelligence dataset.
    medium  — Community-maintained with multiple corroborating sources:
              accounts.csv labelled dataset, Etherscan name tag, public
              scam-report database.
    low     — Single unverified source; treat attribution as a lead only.
              Must be corroborated before any enforcement action.
    """
    HIGH   = "high"
    MEDIUM = "medium"
    LOW    = "low"


# ---------------------------------------------------------------------------
# Sub-models
# ---------------------------------------------------------------------------

class VaspMatch(BaseModel):
    """
    A single VASP attribution candidate returned by the tracer.

    The `confidence` score (0-100) is multi-dimensional:
        graph_proximity_score      — inverse hop distance (closer = higher)
        interaction_strength_score — volume to this VASP / total traced volume
        temporal_recency_score     — how recently funds moved toward this VASP
        evidence_quality_weight    — provenance of the VASP label (high/med/low)

    IMPORTANT — `relationship_type` disambiguates *interaction* from *ownership*.
    The default is `interacts_with` — do NOT claim the VASP owns the wallet
    unless `relationship_type == controlled_by` AND `evidence_quality == high`.
    """
    address:    str
    vasp_name:  str
    hops:       int
    confidence: float    # 0-100, multi-dimensional weighted score
    path:       List[str]
    volume_eth: float = 0.0

    # Attribution precision
    relationship_type: RelationshipType = RelationshipType.INTERACTS_WITH
    evidence_quality:  EvidenceQuality  = EvidenceQuality.MEDIUM

    # Explainable sub-scores (each 0-100)
    graph_proximity_score:      float = 0.0
    interaction_strength_score: float = 0.0
    temporal_recency_score:     float = 0.0


class RiskReport(BaseModel):
    risk_score:  int            # 0-100
    risk_level:  RiskLevel
    flags:       List[str]      # active signal names
    typologies:  List[str]      # human-readable laundering typologies
    details:     Dict[str, int] # signal_name -> sub-score


class WalletClassification(BaseModel):
    type:   WalletTypeEnum
    label:  str
    reason: str


class WalletFeatureVector(BaseModel):
    """
    Standardized feature vector extracted per wallet.

    This is the foundation for Level 3 ML ranking (XGBoost / LightGBM)
    and Level 4 behavioural clustering. All values are normalised floats
    except raw counts, so they can be fed directly into a classifier
    without further preprocessing.

    Graph features
        How many distinct entities the wallet has interacted with, and
        the directionality of those interactions.

    Transaction value features
        The economic profile of the wallet — volume, average size, and
        whether the wallet is primarily a sender or receiver.

    Temporal features
        Velocity and recency signals. High burst_score = lots of activity
        compressed into short windows (structuring / rapid layering).

    Exposure features
        What fraction of the wallet's counterparties are known high-risk
        entities (mixers, bridges, VASPs). High VASP exposure is a strong
        signal for exchange attribution.

    Structuring signals
        Indicators of deliberate obfuscation: repeated equal values,
        narrow counterparty sets (peel chains).
    """
    # Graph features
    unique_counterparties: int   = 0
    unique_senders:        int   = 0
    unique_receivers:      int   = 0
    tx_count:              int   = 0

    # Transaction value features
    total_value_eth:       float = 0.0
    avg_value_eth:         float = 0.0
    max_value_eth:         float = 0.0
    in_out_ratio:          float = 0.0  # inbound_eth / (inbound + outbound_eth)
    value_concentration:   float = 0.0  # top-tx value / total value

    # Temporal features
    tx_per_day:            float = 0.0  # transaction velocity
    burst_score:           float = 0.0  # peak_rate / mean_rate (1.0 = uniform)
    recency_days:          float = 0.0  # days since most recent tx
    activity_span_days:    float = 0.0  # first tx to last tx

    # Exposure features (0.0-1.0, fraction of counterparties)
    mixer_exposure:        float = 0.0
    bridge_exposure:       float = 0.0
    vasp_exposure:         float = 0.0

    # Structuring signals
    structuring_ratio:     float = 0.0  # most-common-value count / tx_count
    peel_chain_score:      float = 0.0  # 1.0 if linear peel chain detected


class GraphNode(BaseModel):
    id:            str
    label:         str
    is_known_vasp: bool           = False
    vasp_name:     Optional[str]  = None
    is_root:       bool           = False
    wallet_type:   Optional[str]  = None
    risk_level:    Optional[str]  = None


class GraphEdge(BaseModel):
    source:    str
    target:    str
    value_eth: float
    tx_hash:   Optional[str] = None


class SahyogRouting(BaseModel):
    """Recommendation for SAHYOG portal routing."""
    vasp_name:       Optional[str] = None
    vasp_address:    Optional[str] = None
    action:          str           = "No match found"
    disclosure_note: str           = ""


# ---------------------------------------------------------------------------
# API Response Models
# ---------------------------------------------------------------------------

class TraceResponse(BaseModel):
    wallet:                     str
    chain:                      str
    total_transactions_scanned: int
    hops_searched:              int
    matches:                    List[VaspMatch]
    top_match:                  Optional[VaspMatch]
    risk:                       RiskReport
    wallet_classification:      WalletClassification
    wallet_features:            Optional[WalletFeatureVector] = None
    sahyog_routing:             SahyogRouting
    nodes:                      List[GraphNode]
    edges:                      List[GraphEdge]
    note:                       Optional[str] = None


class HealthResponse(BaseModel):
    status:             str
    api_key_configured: bool
    known_vasp_count:   int
    max_hops:           int
    supported_chains:   List[str]


class ChainInfo(BaseModel):
    key:          str
    name:         str
    symbol:       str
    native_token: str
    explorer_url: str
    color:        str


class RiskAlertItem(BaseModel):
    wallet:     str
    chain:      str
    risk_level: RiskLevel
    typologies: List[str]
    vasp_match: Optional[str] = None
    timestamp:  str
