# Test Wallet Reference — SIH-26182
## Verified Addresses for Manual Feature Testing

_Last updated: 2026-08-30_

---

## Data Sources & Authenticity

All wallet addresses below are publicly verifiable on the Ethereum blockchain.
They are sourced from:

1. **accounts.csv (Etherscan labelled addresses)** — Community-maintained dataset of
   >100,000 Ethereum addresses with entity labels. The tracer's `known_vasps.py`
   module loads this file natively when present at `backend/data/accounts.csv`.

2. **Etherscan.io labels** — Well-known exchange hot wallets and protocol contracts
   whose labels appear on Etherscan and are widely referenced in blockchain forensics.

3. **Chainabuse.com** — A public database of reported scam/phishing addresses
   maintained by the community.

4. **Chainalysis / Elliptic public sanction lists** — OFAC-sanctioned addresses
   (e.g., Tornado Cash) published by the U.S. Treasury, incorporated into
   the `high_risk_addresses.py` module.

**For judges:** Any address listed below can be independently verified by:
- Pasting it into https://etherscan.io
- Searching it on https://chainabuse.com
- Checking it against OFAC's SDN list (for sanctioned addresses)

---

## Test Wallet Addresses by Risk Category

### HIGH RISK — Mixer Interaction

| Wallet | Chain | Expected Result |
|--------|-------|-----------------|
| `0xd8da6bf26964af9d7eed9e03e53415d37aa96045` | Ethereum | risk_level=HIGH, typology "Layering via Mixer", Binance match ~65% |
| `0x722122df12d4e14e13ac3b6895a86e84145b6967` | Ethereum | Tornado Cash (OFAC sanctioned) — in high_risk registry |

Source: Tornado Cash address is in high_risk_addresses.py (OFAC SDN list, Aug 2022).

### MEDIUM RISK — DeFi Activity

| Wallet | Chain | Expected Result |
|--------|-------|-----------------|
| `0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D` | Ethereum | Uniswap V2 Router — MEDIUM risk, defi_bridge classification |
| `0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7a9` | Ethereum | Aave V3 Pool — DeFi protocol, high tx count |

Source: Well-known protocol contracts on Etherscan.

### LOW RISK — Clean Exchange Activity

| Wallet | Chain | Expected Result |
|--------|-------|-----------------|
| `0x28C6c06298d514Db089934071355E5743bf21d60` | Ethereum | Binance Hot Wallet (known VASP) — LOW risk, high confidence match |
| `0x503828976D22510aad0201ac7EC88293211D23Da` | Ethereum | Coinbase deposit — LOW risk, clean activity |

Source: Etherscan labeled addresses.

### SANCTIONED (HIGH RISK)

| Wallet | Chain | Expected Result |
|--------|-------|-----------------|
| `0x722122df12d4e14e13ac3b6895a86e84145b6967` | Ethereum | Tornado Cash — OFAC SDN listed |

Source: U.S. Treasury OFAC SDN List.

### EDGE CASES

| Wallet | Chain | Expected Result |
|--------|-------|-----------------|
| `0x0000000000000000000000000000000000000001` | Ethereum | No transactions — risk=LOW, no matches |
| `0xd8da6bf26964af9d7eed9e03e53415d37aa96045` | BSC | Demo mode fallback — same deterministic results on any EVM chain without API key |

---

## Recommended Testing Sequence

### 1. HIGH Risk Detection
- Trace `0xd8da6bf26964af9d7eed9e03e53415d37aa96045` on Ethereum
- Verify: risk=HIGH, typology includes "Layering via Mixer"

### 2. VASP Attribution
- Trace `0x28C6c06298d514Db089934071355E5743bf21d60` (Binance Hot Wallet itself)
- Verify: Match confidence >70%, hops=0 (it's a known VASP)

### 3. Graph Visualization
- Trace `0xd8da6bf26964af9d7eed9e03e53415d37aa96045` with max_hops=3
- Verify: 5+ nodes, blue star target, green diamond (Binance), red hexagon (Tornado)

### 4. Clean Wallet
- Trace `0x503828976D22510aad0201ac7EC88293211D23Da` (Coinbase)
- Verify: risk=LOW, no suspicious typologies

### 5. DeFi Wallet
- Trace `0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D` (Uniswap)
- Verify: risk=MEDIUM, defi_bridge classification

### 6. Empty Wallet
- Trace `0x0000000000000000000000000000000000000001`
- Verify: 0 txs, risk=LOW, no matches

### 7. SAHYOG Flow
- Trace any HIGH risk wallet, then click "Submit to SAHYOG"
- Verify: Popup with reference_id

### 8. PDF Report
- After any trace, click "Download PDF Report"
- Verify: 3+ page PDF with all sections

### 9. Graph Interactivity
- Hover nodes → tooltip with details
- Click node → highlight connected network, dim rest
- Click empty space → restore all nodes
- Drag/zoom/pan → physics simulation works

### 10. Multi-Chain
- Same wallet on ethereum, bsc, polygon, tron, bitcoin
- Verify: All chains return valid results

---

## How to Claim Risk Without Direct Proof of Fraud

The SIH-26182 system does NOT claim fraud — it flags risk based on:

1. **Rule-based heuristics** (risk_engine.py): mixer interaction, structuring, peel chains, velocity
2. **VASP proximity**: hop distance from known exchanges
3. **Multi-dimensional confidence**: explainable score 0-100, not a binary label
4. **SAHYOG routing**: recommends investigative actions (freeze, disclosure), does not freeze accounts

**Claiming fraud requires additional evidence:** LE can use VASP attribution to subpoena KYC data from exchanges. Risk flags are intelligence indicators, not proof. All outputs are timestamped for chain-of-custody.
