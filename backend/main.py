"""
Main FastAPI application — SIH-26182
Wallet-to-VASP Attribution System

Endpoints:
  GET /                           — Frontend dashboard
  GET /api/health                 — Health check + config
  GET /api/chains                 — List supported blockchains
  GET /api/trace                  — Core tracing endpoint (multi-chain)
  GET /api/risk/{wallet}          — Standalone risk check (uses cached trace)
  GET /api/history                — In-memory case history
  GET /api/vasps                  — List known VASPs
  GET /api/alerts/high-risk       — High-risk wallets from session
  GET /api/report/{wallet}        — Download PDF investigation report
  POST /api/sahyog/submit         — SAHYOG portal integration stub
"""

# Suppress urllib3 / requests version mismatch warning at startup
import warnings
warnings.filterwarnings("ignore", category=Warning, module="requests")

import os
import logging
from datetime import datetime, timezone
from typing import Optional, Callable

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Silent Probe Middleware
# Intercepts automated tool/extension probe requests at the ASGI level
# BEFORE uvicorn logs them, returning HTTP 204 No Content silently.
# This is needed because:
#   - Antigravity IDE PII scanner probes /api/v1/pii/scan on every keystroke
#   - Browser extensions probe /api/v1/site/check, /favicon.ico, etc.
# ---------------------------------------------------------------------------

_SILENT_PROBE_PATHS: set = {
    # Antigravity IDE PII scanner
    "/api/v1/pii/scan",
    # Browser extension probes
    "/api/v1/site/check",
    "/api/v1/health",
    "/api/v1/ping",
    # Standard browser/crawler probes
    "/favicon.ico",
    "/robots.txt",
    "/.well-known/security.txt",
    "/.well-known/assetlinks.json",
    "/apple-app-site-association",
    "/.well-known/apple-app-site-association",
    "/sitemap.xml",
}

class SilentProbeMiddleware(BaseHTTPMiddleware):
    """
    Returns HTTP 204 No Content immediately for known automated probe
    paths, without invoking the router or triggering access log entries.
    """
    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path
        # Suppress any /api/v1/* path that is NOT one of our real endpoints
        if path in _SILENT_PROBE_PATHS or (
            path.startswith("/api/v1/") and path not in ("/api/v1/",)
        ):
            return Response(status_code=204)  # No Content — silent drop
        return await call_next(request)

from blockchain_client import BlockchainClient, BlockchainClientError
from known_vasps        import KNOWN_VASPS
from tracer             import WalletTracer
from models             import (
    TraceResponse, HealthResponse, ChainInfo, RiskAlertItem, RiskLevel
)
from report             import build_pdf_report
from chains             import SUPPORTED_CHAINS, validate_address

load_dotenv()

ETHERSCAN_API_KEY  = os.getenv("ETHERSCAN_API_KEY",  "")
TRONGRID_API_KEY   = os.getenv("TRONGRID_API_KEY",   "")
MAX_HOPS           = int(os.getenv("MAX_HOPS",           "3"))
MAX_TX_PER_WALLET  = int(os.getenv("MAX_TX_PER_WALLET",  "200"))

app = FastAPI(
    title       = "Wallet-to-VASP Attribution System",
    description = (
        "SIH-26182 — Automated Attribution of Unknown Cryptocurrency Wallets "
        "to nearest VASPs through Blockchain Intelligence APIs. "
        "Integrated with SAHYOG Portal for I4C / Ministry of Home Affairs."
    ),
    version = "2.0.0",
)

# SilentProbeMiddleware must be added FIRST (outermost layer) so it
# intercepts probe paths before CORS processing and before access logging.
app.add_middleware(SilentProbeMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = BlockchainClient(api_keys={
    "etherscan": ETHERSCAN_API_KEY,
    "trongrid":  TRONGRID_API_KEY,
})

tracer = WalletTracer(
    client            = client,
    known_vasps       = KNOWN_VASPS,
    max_hops          = MAX_HOPS,
    max_tx_per_wallet = MAX_TX_PER_WALLET,
)

# In-memory case store (swap for DB in production)
CASE_HISTORY:      list = []
HIGH_RISK_ALERTS:  list = []


# ---------------------------------------------------------------------------
# Health & Config
# ---------------------------------------------------------------------------

@app.get("/api/health", response_model=HealthResponse)
def health():
    """Health check — returns API config status."""
    return HealthResponse(
        status             = "ok",
        api_key_configured = bool(ETHERSCAN_API_KEY),
        known_vasp_count   = len(KNOWN_VASPS),
        max_hops           = MAX_HOPS,
        supported_chains   = list(SUPPORTED_CHAINS.keys()),
    )


# ---------------------------------------------------------------------------
# Chain information
# ---------------------------------------------------------------------------

@app.get("/api/chains", response_model=list[ChainInfo])
def list_chains():
    """Return metadata for all supported blockchains."""
    return [
        ChainInfo(
            key          = key,
            name         = meta["name"],
            symbol       = meta["symbol"],
            native_token = meta["native_token"],
            explorer_url = meta["explorer_url"],
            color        = meta["color"],
        )
        for key, meta in SUPPORTED_CHAINS.items()
    ]


# ---------------------------------------------------------------------------
# Core trace endpoint
# ---------------------------------------------------------------------------

@app.get("/api/trace", response_model=TraceResponse)
def trace_wallet(
    wallet:   str           = Query(..., description="Wallet address to trace"),
    chain:    str           = Query("ethereum", description="Blockchain: ethereum|bsc|polygon|tron|bitcoin"),
    max_hops: Optional[int] = Query(None, description="Override hop depth (1-6)"),
):
    """
    Core investigation endpoint. Traces the wallet's transaction graph
    outward, attributes it to the nearest VASP, and scores its risk level.
    """
    wallet = wallet.strip()
    chain  = chain.strip().lower()

    if chain not in SUPPORTED_CHAINS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported chain '{chain}'. Supported: {list(SUPPORTED_CHAINS.keys())}"
        )

    # Normalize EVM addresses to lowercase
    if SUPPORTED_CHAINS[chain]["type"] == "evm":
        wallet = wallet.lower()

    if not validate_address(wallet, chain):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {SUPPORTED_CHAINS[chain]['name']} address format."
        )

    if SUPPORTED_CHAINS[chain]["type"] == "evm" and not ETHERSCAN_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Server is missing ETHERSCAN_API_KEY. Set it in your .env file.",
        )

    try:
        result = tracer.trace(wallet, chain=chain, max_hops=max_hops or MAX_HOPS)
    except BlockchainClientError as e:
        raise HTTPException(status_code=502, detail=f"Blockchain data source error: {e}")

    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    CASE_HISTORY.append(result)

    # Track high-risk wallets separately for the alerts panel
    risk_level = result.get("risk", {}).get("risk_level", "LOW")
    if risk_level == "HIGH":
        HIGH_RISK_ALERTS.append({
            "wallet":     result["wallet"],
            "chain":      result["chain"],
            "risk_level": risk_level,
            "typologies": result.get("risk", {}).get("typologies", []),
            "vasp_match": result.get("top_match", {}).get("vasp_name") if result.get("top_match") else None,
            "timestamp":  result["timestamp"],
        })

    return result


# ---------------------------------------------------------------------------
# Standalone risk endpoint
# ---------------------------------------------------------------------------

@app.get("/api/risk/{wallet}")
def get_risk(wallet: str, chain: str = Query("ethereum")):
    """
    Return the risk report for a previously traced wallet (from session cache).
    If not cached, returns 404 — run /api/trace first.
    """
    wallet = wallet.strip().lower()
    match  = next((c for c in CASE_HISTORY if c.get("wallet") == wallet
                   and c.get("chain") == chain), None)
    if not match:
        raise HTTPException(
            status_code=404,
            detail="No trace found for this wallet/chain. Run /api/trace first.",
        )
    return {"wallet": wallet, "chain": chain, "risk": match.get("risk")}


# ---------------------------------------------------------------------------
# History & Alerts
# ---------------------------------------------------------------------------

@app.get("/api/history")
def get_history(
    chain:      Optional[str] = Query(None, description="Filter by chain"),
    risk_level: Optional[str] = Query(None, description="Filter by risk level: HIGH|MEDIUM|LOW"),
    limit:      int           = Query(50,   description="Max results"),
):
    """Return case investigation history with optional filters."""
    cases = list(reversed(CASE_HISTORY))
    if chain:
        cases = [c for c in cases if c.get("chain") == chain.lower()]
    if risk_level:
        cases = [c for c in cases if c.get("risk", {}).get("risk_level") == risk_level.upper()]
    return {
        "count": len(cases),
        "cases": cases[:limit],
    }


@app.get("/api/alerts/high-risk")
def high_risk_alerts():
    """Return all HIGH-risk wallets flagged during this session."""
    return {
        "count":  len(HIGH_RISK_ALERTS),
        "alerts": list(reversed(HIGH_RISK_ALERTS)),
    }


# ---------------------------------------------------------------------------
# VASP Reference
# ---------------------------------------------------------------------------

@app.get("/api/vasps")
def list_known_vasps(
    search: Optional[str] = Query(None, description="Filter by name fragment"),
    limit:  int           = Query(100,  description="Max results"),
):
    """Return known-VASP reference list (optionally filtered)."""
    items = list(KNOWN_VASPS.items())
    if search:
        s = search.lower()
        items = [(a, n) for a, n in items if s in n.lower() or s in a]
    return {
        "count": len(items),
        "vasps": [{"address": a, "name": n} for a, n in items[:limit]],
    }


# ---------------------------------------------------------------------------
# PDF Report
# ---------------------------------------------------------------------------

@app.get("/api/report/{wallet}")
def download_report(wallet: str, chain: str = Query("ethereum")):
    """Generate and download a PDF investigation report."""
    wallet = wallet.strip().lower()
    match  = next(
        (c for c in CASE_HISTORY if c.get("wallet") == wallet
         and c.get("chain", "ethereum") == chain),
        None,
    )
    if not match:
        raise HTTPException(
            status_code=404,
            detail="No trace found for this wallet/chain. Run /api/trace first.",
        )
    pdf_buffer = build_pdf_report(match)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=SIH26182_report_{wallet[:10]}.pdf"},
    )


# ---------------------------------------------------------------------------
# SAHYOG Portal Integration Stub
# ---------------------------------------------------------------------------

@app.post("/api/sahyog/submit")
def sahyog_submit(wallet: str = Query(...), chain: str = Query("ethereum")):
    """
    Stub endpoint: simulate submitting a disclosure/freeze request to SAHYOG.
    In production, this would call the SAHYOG Portal API with the routing info.
    """
    wallet = wallet.strip().lower()
    match  = next(
        (c for c in CASE_HISTORY if c.get("wallet") == wallet
         and c.get("chain", "ethereum") == chain),
        None,
    )
    if not match:
        raise HTTPException(
            status_code=404,
            detail="Trace this wallet first via /api/trace before submitting to SAHYOG.",
        )
    routing = match.get("sahyog_routing", {})
    return {
        "status":  "submitted",
        "message": "Request successfully routed to SAHYOG Portal (demo mode).",
        "routing": routing,
        "reference_id": f"SIH-{wallet[:8].upper()}-{datetime.now().strftime('%Y%m%d%H%M%S')}",
    }


# ---------------------------------------------------------------------------
# Static frontend
# ---------------------------------------------------------------------------

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


# ---------------------------------------------------------------------------
# Catch-all: return clean JSON 404 for any unknown route
# (prevents browser-extension probes or scanners from getting HTML error pages)
# ---------------------------------------------------------------------------

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    # Serve index.html for root-level non-API paths (SPA fallback)
    path = request.url.path
    if not path.startswith("/api/") and not path.startswith("/static/"):
        return FileResponse("static/index.html")
    return JSONResponse(
        status_code=404,
        content={"detail": f"Endpoint '{path}' not found.",
                 "hint": "See /docs for available API endpoints."},
    )
