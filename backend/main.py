"""
CryptoGuard AI — Backend Server
SIH-26182: Automated Attribution of Unknown Cryptocurrency Wallets
to Nearest Virtual Asset Service Providers (VASPs) through Blockchain Intelligence APIs.

Platform Identity:
Product: CryptoGuard AI
Tagline: AI-Powered Blockchain Investigation & VASP Attribution Platform
Target Users: Law Enforcement Agencies (LEAs), I4C, FIU-IND, Compliance Officers
"""

import os
import sys
import uuid
import warnings
from datetime import datetime, timezone
from typing import Optional, Callable, Dict, Any, List

from fastapi import FastAPI, HTTPException, Query, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

from blockchain_client import BlockchainClient, BlockchainClientError
from known_vasps        import KNOWN_VASPS
from vasp_registry      import VASP_REGISTRY, get_fiu_registered_vasps
from tracer             import WalletTracer
from models             import (
    TraceResponse, HealthResponse, ChainInfo, CopilotQueryRequest,
    CopilotQueryResponse, EvidenceUpdateRequest, Section91NoticeRequest
)
from report             import build_pdf_report
from chains             import SUPPORTED_CHAINS, validate_address
from demo_fixture       import demo_trace_result, demo_health_status
from database           import (
    init_db, seed_vasps_if_empty, save_investigation, get_investigations,
    get_investigation_by_id, update_evidence_status, get_evidence_for_investigation,
    get_timeline_for_investigation, get_dashboard_metrics
)
from copilot            import answer_investigation_query

warnings.filterwarnings("ignore", category=Warning, module="requests")
load_dotenv()

# Initialize Database and Seed VASP Directory
init_db()
seed_vasps_if_empty(VASP_REGISTRY)

ETHERSCAN_API_KEY   = os.getenv("ETHERSCAN_API_KEY", "")
TRONGRID_API_KEY    = os.getenv("TRONGRID_API_KEY", "")
MAX_HOPS            = int(os.getenv("MAX_HOPS", "3"))
MAX_TX_PER_WALLET   = int(os.getenv("MAX_TX_PER_WALLET", "200"))
MAX_NODES_TO_EXPAND = int(os.getenv("MAX_NODES_TO_EXPAND", "20"))
_DEMO_MODE          = not bool(ETHERSCAN_API_KEY)

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# ---------------------------------------------------------------------------
# Silent Probe Middleware
# ---------------------------------------------------------------------------
_SILENT_PROBE_PATHS: set = {
    "/api/v1/pii/scan",
    "/api/v1/site/check",
    "/api/v1/health",
    "/api/v1/ping",
    "/favicon.ico",
    "/robots.txt",
    "/.well-known/security.txt",
    "/.well-known/assetlinks.json",
    "/apple-app-site-association",
    "/.well-known/apple-app-site-association",
    "/sitemap.xml",
}
_REAL_V1_PATHS: set = {
    "/api/v1/dashboard/summary",
}

class SilentProbeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path
        if path in _SILENT_PROBE_PATHS or (
            path.startswith("/api/v1/") and path not in _REAL_V1_PATHS
        ):
            return Response(status_code=204)
        return await call_next(request)

# ---------------------------------------------------------------------------
# FastAPI Initialization
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CryptoGuard AI",
    description=(
        "AI-Powered Blockchain Investigation & VASP Attribution Platform. "
        "SIH-26182: Automated Attribution of Unknown Cryptocurrency Wallets "
        "to Nearest Virtual Asset Service Providers (VASPs). "
        "Designed for LEAs, I4C, and FIU-IND compliance."
    ),
    version="2.0.0",
)

app.add_middleware(SilentProbeMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

client = BlockchainClient(api_keys={
    "etherscan": ETHERSCAN_API_KEY,
    "trongrid":  TRONGRID_API_KEY,
})

tracer = WalletTracer(
    client=client,
    known_vasps=KNOWN_VASPS,
    max_hops=MAX_HOPS,
    max_tx_per_wallet=MAX_TX_PER_WALLET,
    max_nodes_to_expand=MAX_NODES_TO_EXPAND,
)

# ---------------------------------------------------------------------------
# Health & Status Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/health", response_model=HealthResponse)
def health():
    """Returns platform health and config."""
    return HealthResponse(
        status="ok",
        product="CryptoGuard AI",
        tagline="AI-Powered Blockchain Investigation & VASP Attribution Platform",
        version="2.0.0-SIH26182",
        api_key_configured=bool(ETHERSCAN_API_KEY),
        known_vasp_count=len(KNOWN_VASPS),
        max_hops=MAX_HOPS,
        supported_chains=list(SUPPORTED_CHAINS.keys()),
    )


@app.get("/api/health/detail")
def health_detail():
    """Detailed health check including database and API configuration."""
    return {
        **demo_health_status(),
        "database": "SQLite (data/cryptoguard.db)",
        "fiu_registered_count": len(get_fiu_registered_vasps()),
        "known_vasp_count": len(KNOWN_VASPS),
        "api_key_configured": bool(ETHERSCAN_API_KEY),
    }


# ---------------------------------------------------------------------------
# Blockchain Chains Information
# ---------------------------------------------------------------------------
@app.get("/api/chains", response_model=List[ChainInfo])
def list_chains():
    """Returns metadata for all supported blockchains."""
    return [
        ChainInfo(
            key=key,
            name=meta["name"],
            symbol=meta["symbol"],
            native_token=meta["native_token"],
            explorer_url=meta["explorer_url"],
            color=meta["color"],
        )
        for key, meta in SUPPORTED_CHAINS.items()
    ]


# ---------------------------------------------------------------------------
# Dashboard Analytics
# ---------------------------------------------------------------------------
@app.get("/api/v1/dashboard/summary")
def dashboard_summary():
    """Aggregated stats from persistent SQLite database."""
    metrics = get_dashboard_metrics()
    metrics["known_vasp_count"] = max(metrics["known_vasp_count"], len(KNOWN_VASPS))
    metrics["supported_chains"] = list(SUPPORTED_CHAINS.keys())
    return metrics


# ---------------------------------------------------------------------------
# Core Investigation & Tracing Endpoint
# ---------------------------------------------------------------------------
@app.get("/api/trace", response_model=TraceResponse)
def trace_wallet(
    wallet: str = Query(..., description="Wallet address to investigate"),
    chain: str = Query("ethereum", description="Blockchain network"),
    case_ref: Optional[str] = Query(None, description="Case reference / FIR number"),
    complaint_no: Optional[str] = Query(None, description="NCRP Complaint acknowledgement number"),
    max_hops: Optional[int] = Query(None, description="Hop depth (1-6)"),
    demo_mode: bool = Query(False, description="Run in deterministic demo mode"),
):
    """
    Core investigation endpoint. Traces transaction graph, computes VASP attribution,
    evaluates forensic risk, generates timeline, and persists result in database.
    """
    wallet = wallet.strip()
    chain = chain.strip().lower()
    hops = max_hops or MAX_HOPS
    inv_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    if chain not in SUPPORTED_CHAINS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported chain '{chain}'. Supported: {list(SUPPORTED_CHAINS.keys())}"
        )

    if SUPPORTED_CHAINS[chain]["type"] == "evm":
        wallet = wallet.lower()

    if not validate_address(wallet, chain):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {SUPPORTED_CHAINS[chain]['name']} address format."
        )

    # Demo Mode: Explicit toggle or fallback when API key is missing
    is_demo_target = wallet.lower() in ("0x742d35cc6634c0532925a3b844bc454e4438f44e", "0xd8da6bf26964af9d7eed9e03e53415d37aa96045")
    needs_key = SUPPORTED_CHAINS[chain]["type"] in ("evm", "tron")
    has_key = bool(ETHERSCAN_API_KEY) if SUPPORTED_CHAINS[chain]["type"] == "evm" else bool(TRONGRID_API_KEY)

    if demo_mode or is_demo_target or (needs_key and not has_key):
        result = demo_trace_result(wallet=wallet, chain=chain, case_ref=case_ref or "NCRP-2026-849102")
        result["investigation_id"] = inv_id
        result["timestamp"] = datetime.now(timezone.utc).isoformat()
        result["_demo_mode"] = True
        if not demo_mode and needs_key and not has_key:
            result["_warning"] = "Live blockchain API key not configured in .env. Returning deterministic demo data."

        # Persist into database
        save_investigation(
            inv_id=inv_id,
            wallet=wallet,
            chain=chain,
            case_ref=case_ref or "NCRP-2026-849102",
            complaint_no=complaint_no or "",
            trace_data=result,
            is_demo=True
        )
        return JSONResponse(status_code=200, content=result)

    # Live Blockchain Tracing
    try:
        result = tracer.trace(wallet, chain=chain, max_hops=hops)
    except BlockchainClientError as e:
        raise HTTPException(status_code=502, detail=f"Blockchain data source error: {e}")

    result["investigation_id"] = inv_id
    result["case_ref"] = case_ref or f"CASE-{datetime.now().strftime('%Y%m%d%H%M')}"
    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    result["_demo_mode"] = False

    # Persist into database
    save_investigation(
        inv_id=inv_id,
        wallet=wallet,
        chain=chain,
        case_ref=result["case_ref"],
        complaint_no=complaint_no or "",
        trace_data=result,
        is_demo=False
    )
    return result


@app.get("/api/demo/trace")
def demo_trace(
    wallet: str = Query("0x742d35cc6634c0532925a3b844bc454e4438f44e", description="Demo wallet"),
    chain: str = Query("ethereum", description="Blockchain network"),
):
    """Explicit deterministic demo trace endpoint."""
    return demo_trace_result(wallet=wallet, chain=chain)


# ---------------------------------------------------------------------------
# Investigation Cases & History
# ---------------------------------------------------------------------------
@app.get("/api/history")
def get_history(
    chain: Optional[str] = Query(None, description="Filter by chain"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level"),
    limit: int = Query(50, description="Max results"),
):
    """Retrieves case investigation history from SQLite database."""
    cases = get_investigations(limit=limit, chain=chain, risk=risk_level)
    return {
        "count": len(cases),
        "cases": cases,
    }


@app.get("/api/investigation/{inv_id}")
def get_investigation(inv_id: str):
    """Retrieves a single investigation record by ID."""
    case = get_investigation_by_id(inv_id)
    if not case:
        raise HTTPException(status_code=404, detail=f"Investigation '{inv_id}' not found.")
    return case


@app.get("/api/alerts/high-risk")
def high_risk_alerts():
    """Returns all investigations flagged with HIGH risk."""
    high_cases = get_investigations(limit=50, risk="HIGH")
    alerts = []
    for c in high_cases:
        alerts.append({
            "investigation_id": c["id"],
            "wallet": c["wallet_address"],
            "chain": c["chain"],
            "risk_level": "HIGH",
            "risk_score": c["risk_score"],
            "vasp_match": c["top_vasp"],
            "timestamp": c["created_at"],
            "case_ref": c.get("case_ref")
        })
    return {
        "count": len(alerts),
        "alerts": alerts,
    }


# ---------------------------------------------------------------------------
# Evidence Management Endpoints
# ---------------------------------------------------------------------------
@app.get("/api/evidence/{inv_id}")
def get_evidence(inv_id: str):
    """Retrieves evidence items for an investigation."""
    evidence_list = get_evidence_for_investigation(inv_id)
    return {
        "investigation_id": inv_id,
        "count": len(evidence_list),
        "evidence": evidence_list
    }


@app.patch("/api/evidence/{evidence_id}")
def update_evidence(evidence_id: str, payload: EvidenceUpdateRequest):
    """Updates evidence review status (Relevant / Reviewed / Needs Verification)."""
    valid_statuses = {"Relevant", "Reviewed", "Needs Verification"}
    if payload.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Choose from: {valid_statuses}")

    updated = update_evidence_status(evidence_id, payload.status, payload.notes or "")
    if not updated:
        raise HTTPException(status_code=404, detail=f"Evidence item '{evidence_id}' not found.")
    return {
        "status": "success",
        "evidence_id": evidence_id,
        "new_status": payload.status
    }


# ---------------------------------------------------------------------------
# AI Investigation Copilot
# ---------------------------------------------------------------------------
@app.post("/api/copilot/query", response_model=CopilotQueryResponse)
def copilot_query(payload: CopilotQueryRequest):
    """
    Answers investigative questions about the current case using
    deterministic rule-based intelligence or optional LLM.
    """
    trace_data = payload.trace_data
    if not trace_data and payload.investigation_id:
        case = get_investigation_by_id(payload.investigation_id)
        if case and case.get("result"):
            trace_data = case["result"]

    if not trace_data:
        # Fall back to default demo fixture context
        trace_data = demo_trace_result()

    response = answer_investigation_query(trace_data, payload.query)
    return CopilotQueryResponse(
        answer=response["answer"],
        engine=response.get("engine", "Deterministic Intelligence Engine"),
        confidence=response.get("confidence", "High"),
        category=response.get("category", "General Analysis")
    )


# ---------------------------------------------------------------------------
# Cybercrime Response & Legal Requisition (India / SAHYOG-Ready)
# ---------------------------------------------------------------------------
@app.post("/api/sahyog/notice")
def generate_sahyog_notice(payload: Section91NoticeRequest):
    """
    Generates a formal legal requisition notice under Section 91 CrPC /
    Section 94 Bharatiya Nagarik Suraksha Sanhita (BNSS) for VASP KYC disclosure.
    """
    case = get_investigation_by_id(payload.investigation_id)
    trace_data = case.get("result", {}) if case else demo_trace_result()

    top_match = trace_data.get("top_match") or {}
    vasp_name = payload.vasp_name or top_match.get("vasp_name", "Target Virtual Asset Service Provider")
    wallet = trace_data.get("wallet", "Unknown")
    chain = trace_data.get("chain", "ethereum").upper()

    notice_text = f"""
================================================================================
NOTICE UNDER SECTION 91 OF CODE OF CRIMINAL PROCEDURE, 1973
(OR SECTION 94 OF BHARATIYA NAGARIK SURAKSHA SANHITA, 2023)
================================================================================

TO:
The Nodal Officer / Compliance Department
{vasp_name}
Ref: Prevention of Money Laundering Act (PMLA), 2002 & FIU-IND Compliance Guidelines

FROM:
Investigating Officer: {payload.investigator_name}
Police Station: {payload.police_station}
FIR / Crime No: {payload.fir_number}
Date: {datetime.now(timezone.utc).strftime('%d-%B-%Y')}

SUBJECT: URGENT REQUISITION FOR TRANSACTION DISCLOSURE, KYC RECORDS,
         AND INTERIM FREEZING OF BENEFICIARY CRYPTOCURRENCY ASSETS

Sir/Madam,

1. WHEREAS an investigation into a cyber-financial fraud under the Indian Penal Code /
   Bharatiya Nyaya Sanhita and Information Technology Act 2000 is being conducted
   in Crime No. {payload.fir_number} at Police Station {payload.police_station}.

2. AND WHEREAS forensic blockchain analysis by CryptoGuard AI identified fund flows
   originating from the suspect wallet:
   Target Public Key: {wallet}
   Blockchain Network: {chain}
   terminating in deposit/operational infrastructure registered to {vasp_name}.

3. YOU ARE HEREBY REQUIRED under Section 91 CrPC / Section 94 BNSS to furnish the following
   information/documents within 24 hours of receipt of this notice:
   a) Full KYC documents (Government ID, PAN card, Aadhaar, Passport) of the account holder(s)
      associated with the attributed deposit address.
   b) Bank account details linked to the user profile, including registered mobile and email.
   c) Comprehensive login audit logs (IP addresses, timestamps, device fingerprints, MAC addresses).
   d) Complete crypto deposit and withdrawal logs for the period of the incident.

4. YOU ARE FURTHER DIRECTED to place an immediate debit freeze / administrative hold
   on any remaining balances in the beneficiary account under Section 102 CrPC / Section 106 BNSS
   to prevent dissipation of proceed of crime.

Issued under my signature and seal of the Police Station.

_____________________________
{payload.investigator_name}
Investigating Officer
{payload.police_station}
================================================================================
"""

    return {
        "status": "generated",
        "case_id": payload.investigation_id,
        "fir_number": payload.fir_number,
        "vasp_name": vasp_name,
        "notice_text": notice_text.strip(),
        "created_at": datetime.now(timezone.utc).isoformat()
    }


@app.post("/api/sahyog/submit")
def sahyog_submit(wallet: str = Query(...), chain: str = Query("ethereum")):
    """Simulates submitting disclosure/freeze request to SAHYOG-ready portal."""
    wallet_clean = wallet.strip().lower()
    ref_id = f"SAHYOG-SIH-{wallet_clean[:8].upper()}-{datetime.now().strftime('%Y%m%d%H%M')}"
    return {
        "status": "submitted",
        "workflow": "SAHYOG-Ready LEA Portal",
        "reference_id": ref_id,
        "message": "Requisition notice queued for delivery to VASP Nodal Desk.",
        "target_wallet": wallet_clean,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# ---------------------------------------------------------------------------
# VASP Intelligence Directory
# ---------------------------------------------------------------------------
@app.get("/api/vasps")
def list_vasps(
    search: Optional[str] = Query(None, description="Search by name or address"),
    fiu_only: bool = Query(False, description="Filter FIU-IND registered only"),
    limit: int = Query(100, description="Max results"),
):
    """Returns curated VASP reference directory."""
    items = []
    for addr, meta in VASP_REGISTRY.items():
        if fiu_only and not meta.get("fiu_registered"):
            continue
        items.append({
            "address": addr,
            "name": meta.get("name", "Unknown VASP"),
            "category": meta.get("category", "Exchange"),
            "fiu_registered": meta.get("fiu_registered", False),
            "country": meta.get("country", "Global"),
            "compliance_email": meta.get("compliance_email", ""),
            "reporting_id": meta.get("reporting_id", ""),
            "chain": meta.get("chain", "ethereum")
        })

    # Also include any other addresses in KNOWN_VASPS not already in VASP_REGISTRY
    existing_addrs = set(VASP_REGISTRY.keys())
    for addr, name in KNOWN_VASPS.items():
        if addr not in existing_addrs and not fiu_only:
            items.append({
                "address": addr,
                "name": name,
                "category": "Exchange / Labelled",
                "fiu_registered": False,
                "country": "Global",
                "compliance_email": "",
                "reporting_id": "",
                "chain": "ethereum"
            })

    if search:
        s = search.lower()
        items = [v for v in items if s in v["name"].lower() or s in v["address"].lower()]

    return {
        "count": len(items),
        "fiu_registered_count": len(get_fiu_registered_vasps()),
        "vasps": items[:limit]
    }


# ---------------------------------------------------------------------------
# PDF Forensic Report Download
# ---------------------------------------------------------------------------
@app.get("/api/report/{wallet}")
def download_report(wallet: str, chain: str = Query("ethereum")):
    """Generates and downloads a forensic investigation PDF report."""
    wallet_clean = wallet.strip().lower()

    # Look up in database
    cases = get_investigations(limit=10, chain=chain)
    match = next((c for c in cases if c.get("wallet_address") == wallet_clean), None)
    trace_data = None

    if match and match.get("result_json"):
        import json
        try:
            trace_data = json.loads(match["result_json"])
        except Exception:
            pass

    if not trace_data:
        # Generate on-demand demo report
        trace_data = demo_trace_result(wallet=wallet_clean, chain=chain)

    pdf_buffer = build_pdf_report(trace_data)
    filename = f"CryptoGuard_Report_{wallet_clean[:10]}_{datetime.now().strftime('%Y%m%d')}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


# ---------------------------------------------------------------------------
# Static Frontend Serving
# ---------------------------------------------------------------------------
class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        resp = await super().get_response(path, scope)
        if hasattr(resp, "headers"):
            resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            resp.headers["Pragma"] = "no-cache"
            resp.headers["Expires"] = "0"
        return resp

if os.path.isdir(STATIC_DIR):
    app.mount("/static", NoCacheStaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return JSONResponse(content={"status": "running", "product": "CryptoGuard AI"})


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    fav_path = os.path.join(STATIC_DIR, "favicon.ico")
    if os.path.isfile(fav_path):
        return FileResponse(fav_path, media_type="image/x-icon")
    return Response(status_code=204)


@app.exception_handler(404)
async def not_found_handler(request: Request, _exc: Exception):
    path = request.url.path
    if not path.startswith("/api/") and not path.startswith("/static/"):
        index_path = os.path.join(STATIC_DIR, "index.html")
        if os.path.isfile(index_path):
            return FileResponse(index_path)
    return JSONResponse(
        status_code=404,
        content={"detail": f"Endpoint '{path}' not found.", "hint": "See /docs for interactive API specs."},
    )
