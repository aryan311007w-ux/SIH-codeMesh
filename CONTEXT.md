# SIH-26182 — Context for New Claude Session
## Copy-paste this entire file into a new Claude Chat session in VS Code

---

## Project Overview

**SAHYOG Wallet-to-VASP Attribution System (SIH-26182)**
A blockchain intelligence tool that traces Ethereum wallet transactions to identify connections to known VASPs and flag high-risk activity (mixers, sanctioned addresses, darknet markets).

**Location:** C:\Wallet-to-VASP Attribution System (SIH-26182)\SIH26182
**Backend:** FastAPI (backend/main.py)
**Frontend:** HTML/CSS/JS (backend/static/)
**Key files:**
- backend/tracer.py — Core BFS wallet tracing engine
- backend/blockchain_client.py — Blockchain API client (Etherscan, etc.)
- backend/demo_fixture.py — Deterministic offline demo data
- backend/risk_engine.py — Multi-dimensional risk scoring
- backend/known_vasps.py — Known VASP address registry
- backend/app.py — Flask frontend server (serves static UI, proxies API)
- backend/static/js/app.js — Frontend JavaScript (all UI logic)
- backend/static/css/style.css — All styles
- backend/static/index.html — Single-page app HTML
- backend/data/demo_vasps.csv — VASP database (33 addresses)
- backend/data/TEST_WALLETS.md — Test wallet reference with addresses
- backend/test_tracer.py — Test suite (12 tests, run: cd backend && python test_tracer.py)

---

## How to Run

Terminal 1 — Backend API:
  cd "C:\Wallet-to-VASP Attribution System (SIH-26182)\SIH26182\backend"
  uvicorn main:app --reload --port 8080

Terminal 2 — Frontend:
  python app.py
  (serves at http://127.0.0.1:8080 or check console for port)

---

## What Was Already Fixed (DO NOT redo)

1. Evidence HTML Bug — app.js renderEvidence() now uses innerHTML for direction badges. Labels in .ev-label with ellipsis + tooltip.
2. Graph Height — #graphContainer from 380px to 520px.
3. Graph Legend — Dynamic JS-generated 12 pill badges with colored dots (Target, VASP, Hot Wallet, Deposit Wallet, Mixer, Sanctioned, Darknet, DeFi Bridge, Cross-Chain Swap, Fraud, Unknown).
4. Graph Tooltips — Show: bold label name, Type, VASP name, full address, risk level.
5. Graph Node Shapes — target=star, exchange/sanctioned/darknet/mixer/ransomware=hexagon, hot_wallet/fraud/defi_bridge=triangle, deposit_wallet=database, unknown=dot.
6. Graph Colors — target=blue, exchange=green, hot_wallet=amber, mixer/sanctioned=red, darknet=purple, defi_bridge/fraud=orange, unknown=gray.
7. Graph Arrows — Edges have directional arrows. High-value edges (>0.001 ETH) thicker and blue.
8. Graph Interactivity — Click node highlights it + connected nodes/edges, dims rest to 15%. Click empty space restores. Hover tooltips at 80ms delay.
9. Hamburger Button — Always visible, toggles sidebar. Mobile (<700px): sidebar starts hidden. Desktop: sidebar visible, hamburger collapses.
10. VASP Database — Expanded from 10 to 33 addresses (Binance x5, Coinbase x2, Kraken x2, OKEx, KuCoin, Bybit, Huobi, Bitfinex, BitMEX, Gate.io, Liquid, Luno, FalconX, Uniswap, Aave, 1inch, Zerion, WETH, USDT, USDC, LINK, DAI).
11. Demo Risk Level — wallet 0xd8da6bf... now returns risk=HIGH, score=85, typologies=["Layering via Mixer", "Proximity to Sanctioned Entity"]. SAHYOG says "URGENT: Freeze request".
12. Tracer Early-Stop — BFS stops expanding nodes beyond shortest hop to any VASP match (added in tracer.py).
13. Test Wallet Reference — backend/data/TEST_WALLETS.md with 10+ verified addresses by risk category.

---

## Current Known Issues (the real work left)

### Issue 1: Trace Takes Too Long
Symptom: Tracing the demo wallet takes 2-5 minutes.
Root cause: Even with early-stop, each BFS level makes sequential API calls with retry delays.
What to check:
- tracer.py: verify early-stop condition exists after "if hops >= hops_limit:"
- blockchain_client.py: check _call_with_retry() timeout and retry settings
- Consider reducing max_nodes_to_expand from 60 to 20
- Check if demo mode is active (no API key = uses demo_fixture.py which is instant)

### Issue 2: Risk Banner Shows LOW Instead of HIGH
Symptom: User reports wallet still showing LOW risk despite Tornado Cash link.
Possible causes:
- Server in LIVE mode hitting real Etherscan API, returning different data than demo fixture
- risk_engine.py overriding the demo fixture's risk calculation
- app.js frontend has a risk_level mapping bug
What to check:
- app.js: search for "risk_level" — frontend might map/converts it
- risk_engine.py: see if it overrides risk from the API response
- Check the actual /api/trace JSON response in browser DevTools Network tab

### Issue 3: Evidence Section Still Shows Raw HTML
Symptom: User sees raw <span> tags as visible text.
What to check:
- app.js: find renderEvidence() function
- Verify it uses innerHTML for direction badge
- Check if there are TWO render paths (demo vs live) that render differently

---

## How to Diagnose

1. Check server mode: ETHERSCAN_API_KEY env var. If set = LIVE mode. If not = demo_fixture.py (instant).
2. Browser DevTools (F12) → Network tab → find /api/trace → check response JSON for risk_level value.
3. app.js: search for "risk_level" — frontend may have mapping/threshold logic that converts it.
4. Check if frontend overwrites risk data from API response with its own calculation.

---

## Git Status

Branch: main
Recent commits:
  ac73d69 fix: demo fixture risk=HIGH for mixer wallet, tracer early-stop optimization
  7f566fa feat: UI overhaul — bigger graph, fixed evidence HTML, dynamic legend
  ad1725e feat: add evidence section to trace results UI and backend

---

## Test Wallet for Debugging

Address: 0xd8da6bf26964af9d7eed9e03e53415d37aa96045
Chain: Ethereum
Expected: risk=HIGH, typologies=["Layering via Mixer", "Proximity to Sanctioned Entity"],
          SAHYOG action = "URGENT: Freeze request",
          Binance match at ~65% confidence, 3 nodes in graph, 3 edges

---

## When User Pastes Screenshots

Look for:
1. Risk banner — what color/level does it show?
2. Evidence section — rendered HTML or raw tags visible?
3. Graph — correct size, colors, shapes, legend pills?
4. Console errors (F12 Console tab)
5. Network tab — /api/trace response body

For each, identify the file that controls it, make the fix, explain what changed.
