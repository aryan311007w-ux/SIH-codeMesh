"""
CryptoGuard AI - Pydantic Request/Response Models
Comprehensive schemas for investigations, VASP attribution, risk scoring,
evidence ledger, timeline, copilot intelligence, and legal notices.
"""

from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


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
    LAYERING_LIKE   = "layering_like"
    UNKNOWN         = "unknown_wallet"


class RelationshipType(str, Enum):
    INTERACTS_WITH    = "interacts_with"
    CONTROLLED_BY     = "controlled_by"
    LAUNDERED_THROUGH = "laundered_through"


class EvidenceQuality(str, Enum):
    HIGH   = "high"
    MEDIUM = "medium"
    LOW    = "low"


class HopDetail(BaseModel):
    hop:          int
    from_addr:    str
    to_addr:      str
    from_label:   str = ""
    to_label:     str = ""
    tx_hash:      str = ""
    value_eth:    float = 0.0
    block_number: Optional[int] = None
    timestamp:    Optional[str] = None


class VaspMatch(BaseModel):
    address:                    str
    vasp_name:                  str
    hops:                       int
    confidence:                 float
    confidence_label:           Optional[str] = "Evaluated"
    path:                       List[str]
    volume_eth:                 float = 0.0
    tx_count:                   int = 1
    first_seen:                 Optional[str] = None
    last_seen:                  Optional[str] = None
    relationship_type:          RelationshipType = RelationshipType.INTERACTS_WITH
    evidence_quality:           EvidenceQuality = EvidenceQuality.MEDIUM
    graph_proximity_score:      float = 0.0
    interaction_strength_score: float = 0.0
    temporal_recency_score:     float = 0.0
    fiu_registered:             bool = False
    compliance_email:           Optional[str] = None
    reporting_id:               Optional[str] = None
    country:                    Optional[str] = None
    explanation:                Optional[str] = None
    hop_details:                Optional[List[HopDetail]] = None


class RiskReport(BaseModel):
    risk_score:  int
    risk_level:  RiskLevel
    flags:       List[str]
    typologies:  List[str]
    details:     Dict[str, int]


class WalletClassification(BaseModel):
    type:   WalletTypeEnum
    label:  str
    reason: str


class WalletFeatureVector(BaseModel):
    unique_counterparties: int   = 0
    unique_senders:        int   = 0
    unique_receivers:      int   = 0
    tx_count:              int   = 0
    total_value_eth:       float = 0.0
    avg_value_eth:         float = 0.0
    max_value_eth:         float = 0.0
    in_out_ratio:          float = 0.0
    value_concentration:   float = 0.0
    tx_per_day:            float = 0.0
    burst_score:           float = 0.0
    recency_days:          float = 0.0
    activity_span_days:    float = 0.0
    mixer_exposure:        float = 0.0
    bridge_exposure:       float = 0.0
    vasp_exposure:         float = 0.0
    structuring_ratio:     float = 0.0
    peel_chain_score:      float = 0.0


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
    vasp_name:                  Optional[str] = None
    vasp_address:               Optional[str] = None
    action:                     str           = "No match found"
    disclosure_note:            str           = ""
    primary_vasp:               Optional[str] = None
    primary_fiu_id:             Optional[str] = None
    primary_email:              Optional[str] = None
    secondary_vasp:             Optional[str] = None
    secondary_fiu_id:           Optional[str] = None
    secondary_email:            Optional[str] = None
    frozen_amount_recommended:  Optional[str] = None
    case_ref:                   Optional[str] = None


class EvidenceItem(BaseModel):
    id:                 Optional[str] = None
    tx_hash:            Optional[str] = None
    direction:          Optional[str] = "outbound"
    counterparty:       Optional[str] = None
    counterparty_label: Optional[str] = None
    value_eth:          Optional[float] = 0.0
    timestamp:          Optional[str] = None
    source:             Optional[str] = "Trace Engine"
    status:             Optional[str] = "Relevant"
    note:               Optional[str] = None


class TimelineEvent(BaseModel):
    time:     str
    title:    str
    desc:     str
    type:     str = "transfer"
    wallet:   Optional[str] = None
    tx_hash:  Optional[str] = None
    amount:   float = 0.0


class TraceResponse(BaseModel):
    wallet:                     str
    chain:                      str
    case_ref:                   Optional[str] = None
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
    timeline:                   Optional[List[TimelineEvent]] = None
    evidence:                   Optional[List[EvidenceItem]] = None
    note:                       Optional[str] = None
    timestamp:                  Optional[str] = None
    _demo_mode:                 Optional[bool] = False
    _warning:                   Optional[str] = None


class HealthResponse(BaseModel):
    status:             str
    product:            str = "CryptoGuard AI"
    tagline:            str = "AI-Powered Blockchain Investigation & VASP Attribution Platform"
    version:            str = "2.0.0-SIH26182"
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


class CopilotQueryRequest(BaseModel):
    query:            str
    investigation_id: Optional[str] = None
    trace_data:       Optional[Dict[str, Any]] = None


class CopilotQueryResponse(BaseModel):
    answer:     str
    engine:     str
    confidence: str
    category:   str
    chips:      Optional[List[str]] = []


class EvidenceUpdateRequest(BaseModel):
    status: str
    notes:  Optional[str] = ""


class InvestigationCreateRequest(BaseModel):
    wallet:        str
    chain:         str = "ethereum"
    case_ref:      Optional[str] = None
    complaint_no:  Optional[str] = None
    max_hops:      Optional[int] = 3
    demo_mode:     bool = False


class Section91NoticeRequest(BaseModel):
    investigation_id:   str
    police_station:     str = "Cyber Crime Police Station, Central"
    fir_number:         str = "FIR-2026/89-CYBER"
    investigator_name:  str = "Inspector R. Verma"
    vasp_name:          Optional[str] = None

