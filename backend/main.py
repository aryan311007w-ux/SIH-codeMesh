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

import os
import warnings
from datetime import datetime, timezone
from typing import Optional, Callable

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse, JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from dotenv import load_dotenv

from blockchain_client import BlockchainClient, BlockchainClientError
from known_vasps        import KNOWN_VASPS
from tracer             import WalletTracer
from models             import TraceResponse, HealthResponse, ChainInfo
from report             import build_pdf_report
from chains             import SUPPORTED_CHAINS, validate_address
from demo_fixture       import demo_trace_result, demo_health_status

warnings.filterwarnings("ignore", category=Warning, module="requests")
load_dotenv()

ETHERSCAN_API_KEY  = os.getenv("ETHERSCAN_API_KEY",  "")
TRONGRID_API_KEY   = os.getenv("TRONGRID_API_KEY",   "")
MAX_HOPS           = int(os.getenv("MAX_HOPS",           "3"))
MAX_TX_PER_WALLET  = int(os.getenv("MAX_TX_PER_WALLET",  "200"))

# ---------------------------------------------------------------------------
# Silent Probe Middleware
# Intercepts automated tool/extension probe requests at the ASGI level
# BEFORE uvicorn logs them, returning HTTP 204 No Content silently.
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

class SilentProbeMiddleware(BaseHTTPMiddleware):
    """Returns HTTP 204 No Content for known automated probe paths."""
    async def dispatch(self, request: Request, call_next: Callable):
        path = request.url.path
        if path in _SILENT_PROBE_PATHS or (
            path.startswith("/api/v1/") and path not in ("/api/v1/",)
        ):
            return Response(status_code=204)
        return await call_next(request)

# ---------------------------------------------------------------------------
# Startup health report
# ---------------------------------------------------------------------------
_DEMO_MODE = not bool(ETHERSCAN_API_KEY)

_ACCOUNTS_CSV = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")
_HAS_PRIMARY  = os.path.isfile(_ACCOUNTS_CSV)

_VASP_SOURCE = (
    "primary (accounts.csv)"
    if _HAS_PRIMARY and len(KNOWN_VASPS) > 0
    else "demo fallback"
)

print("=" * 60)
print("  SIH-26182  Wallet-to-VASP Attribution System")
print("=" * 60)
print("  Mode            :", "DEMO (no API key)" if _DEMO_MODE else "LIVE")
print("  VASP data       :", _VASP_SOURCE)
print("  VASP count      :", f"{len(KNOWN_VASPS):,}")
print("  Etherscan key   :", "configured" if not _DEMO_MODE else "MISSING")
print("  TronGrid key    :", "configured" if TRONGRID_API_KEY else "not configured")
print("  Supported chains:", ", ".join(SUPPORTED_CHAINS.keys()))
print("  Max hops        :", MAX_HOPS)
print("=" * 60)

app = FastAPI(
    title       = "Wallet-to-VASP Attribution System",
    description = (
        "SIH-26182 — Automated Attribution of Unknown Cryptocurrency Wallets "
        "to nearest VASPs through Blockchain Intelligence APIs. "
        "Integrated with SAHYOG Portal for I4C / Ministry of Home Affairs."
    ),
    version = "2.0.0",
)

app.add_middleware(SilentProbeMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
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

CASE_HISTORY:      list = []
HIGH_RISK_ALERTS:  list = []

# ---------------------------------------------------------------------------
# Health & Config
# ---------------------------------------------------------------------------

@app.get("/api/health", response_model=HealthResponse)
def health():
    """Health check — returns API config and data source status."""
    return HealthResponse(
        status             = "ok",
        api_key_configured = bool(ETHERSCAN_API_KEY),
        known_vasp_count   = len(KNOWN_VASPS),
        max_hops           = MAX_HOPS,
        supported_chains   = list(SUPPORTED_CHAINS.keys()),
    )


@app.get("/api/health/detail")
def health_detail():
    """Detailed health check — includes data source diagnostics."""
    accounts_path = os.path.join(os.path.dirname(__file__), "data", "accounts.csv")
    has_primary = os.path.isfile(accounts_path) and len(KNOWN_VASPS) > 0

    return {
        **demo_health_status(),
        "has_primary_vasp_data": has_primary,
        "accounts_csv_present":  os.path.isfile(accounts_path),
    }


# ---------------------------------------------------------------------------
# Demo trace endpoint (offline / no-API-key mode)
# ---------------------------------------------------------------------------

@app.get("/api/demo/trace")
def demo_trace(
    wallet: str = Query(..., description="Wallet address to trace (demo data)"),
    chain:  str = Query("ethereum", description="Blockchain: ethereum|bsc|polygon|tron|bitcoin"),
):
    """Return a deterministic demo trace result. No live API calls are made."""
    wallet = wallet.strip().lower()
    chain  = chain.strip().lower()

    if chain not in SUPPORTED_CHAINS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported chain '{chain}'. Supported: {list(SUPPORTED_CHAINS.keys())}"
        )

    if SUPPORTED_CHAINS[chain]["type"] == "evm" and not validate_address(wallet, chain):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {SUPPORTED_CHAINS[chain]['name']} address format."
        )

    return demo_trace_result(wallet=wallet, chain=chain)


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
    wallet:     str           = Query(..., description="Wallet address to trace"),
    chain:      str           = Query("ethereum", description="Blockchain: ethereum|bsc|polygon|tron|bitcoin"),
    max_hops:   Optional[int] = Query(None, description="Override hop depth (1-6)"),
    demo_mode:  bool          = Query(False, description="Force demo/synthetic data (bypasses live API)"),
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

    if SUPPORTED_CHAINS[chain]["type"] == "evm":
        wallet = wallet.lower()

    if not validate_address(wallet, chain):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {SUPPORTED_CHAINS[chain]['name']} address format."
        )

    # Explicit demo mode toggle from frontend
    if demo_mode:
        demo_result = demo_trace_result(wallet=wallet, chain=chain)
        demo_result["timestamp"] = datetime.now(timezone.utc).isoformat()
        demo_result["_demo_mode"] = True
        CASE_HISTORY.append(demo_result)
        return JSONResponse(status_code=200, content=demo_result)

    # Auto-fallback to demo mode when the required API key is missing
    chain_type = SUPPORTED_CHAINS[chain]["type"]
    needs_key  = chain_type in ("evm", "tron")
    has_key    = (ETHERSCAN_API_KEY if chain_type == "evm"
                  else TRONGRID_API_KEY if chain_type == "tron"
                  else True)
    if needs_key and not has_key:
        # Auto-fallback to demo mode so the UI is never blank
        demo_result = demo_trace_result(wallet=wallet, chain=chain)
        demo_result["timestamp"] = datetime.now(timezone.utc).isoformat()
        demo_result["_demo_mode"] = True
        demo_result["_warning"] = (
            "Live blockchain API not configured. "
            "Returning synthetic demo data. Add the API key to .env for live tracing."
        )
        CASE_HISTORY.append(demo_result)
        return JSONResponse(status_code=200, content=demo_result)

    try:
        result = tracer.trace(wallet, chain=chain, max_hops=max_hops or MAX_HOPS)
    except BlockchainClientError as e:
        raise HTTPException(status_code=502, detail=f"Blockchain data source error: {e}")

    result["timestamp"] = datetime.now(timezone.utc).isoformat()
    CASE_HISTORY.append(result)

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
    """Return the risk report for a previously traced wallet (from session cache)."""
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
    """Stub: simulate submitting a disclosure/freeze request to SAHYOG."""
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

class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        resp = await super().get_response(path, scope)
        if hasattr(resp, "headers"):
            resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            resp.headers["Pragma"] = "no-cache"
            resp.headers["Expires"] = "0"
        return resp

app.mount("/static", NoCacheStaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


# ---------------------------------------------------------------------------
# Catch-all: return clean JSON 404 for any unknown route
# ---------------------------------------------------------------------------

@app.exception_handler(404)
async def not_found_handler(request: Request, _exc: Exception):
    """Serve index.html for SPA routes, JSON for unknown API routes."""
    path = request.url.path
    if not path.startswith("/api/") and not path.startswith("/static/"):
        return FileResponse("static/index.html")
    return JSONResponse(
        status_code=404,
        content={"detail": f"Endpoint '{path}' not found.",
                 "hint": "See /docs for available API endpoints."},
    )
