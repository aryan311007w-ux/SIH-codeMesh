# Real Test Wallets — SIH-26182

## LIVE MODE (with Etherscan API key configured)

These wallets have known on-chain activity that will show up in live traces.

### HIGH RISK — Mixer Proximity
| Wallet | Chain | What you'll see |
|--------|-------|-----------------|
| 0x722122df12d4e14e13ac3b6895a86e84145b6967 | Ethereum | **Tornado Cash Proxy** — this IS the mixer. Risk will be HIGH. Not in VASP registry but in high-risk list. |
| 0x47ce0c6ed5b0ce3d3a51fdb1c52dc66a7c3f2936 | Ethereum | **Tornado Cash 0.1 ETH Pool** — direct mixer address. |
| 0xa160cdab225685da1d56aa342ad8841c3b53f291 | Ethereum | **Tornado Cash 10 ETH Pool** — larger denomination mixer. |

### HIGH RISK — Sanctions (OFAC)
| Wallet | Chain | What you'll see |
|--------|-------|-----------------|
| 0x098b716b8aaf21512996dc57eb0615e2383e2f96 | Ethereum | **Lazarus Group / Ronin Bridge Hacker** — OFAC sanctioned. |
| 0x901bb9583b24d97e995513c6778dc6888ab6870e | Ethereum | **DPRK Lazarus Group** — sanctions-linked. |

### MEDIUM RISK — Known Exchange Wallets (will match VASPs)
| Wallet | Chain | What you'll see |
|--------|-------|-----------------|
| 0x28C6c06298d514Db089934071355E5743bf21d60 | Ethereum | **Binance Hot Wallet** — in VASP registry. Should show HIGH confidence match. |
| 0x503828976D22510aad0201ac7EC88293211D23Da | Ethereum | **Coinbase** — in VASP registry. |
| 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D | Ethereum | **Uniswap Router** — in VASP registry as DeFi. |
| 0x7d2768dE32b0b80b7a3454c06BdAc94A69DDc7a9 | Ethereum | **Aave V3 Pool** — in VASP registry. |

### LOW RISK — Random Active Wallet
| Wallet | Chain | What you'll see |
|--------|-------|-----------------|
| 0xBe3d0f9D90bb36b2932230A39D54aec085dBa2DF | Ethereum | Active wallet, likely no VASP match, LOW risk. |
| 0xAbCdEf0123456789AbCdEf0123456789AbCdEf01 | Ethereum | Random address — probably no transactions, LOW risk. |

---

## DEMO MODE (no API key OR toggle "Demo mode" checkbox)

Use the demo toggle in the UI, or unset ETHERSCAN_API_KEY.

### Test Wallet: 0xd8da6bf26964af9d7eed9e03e53415d37aa96045
**Expected result in demo mode:**
- Risk: **HIGH** (score 85)
- Typologies: Layering via Mixer, Proximity to Sanctioned Entity
- SAHYOG: "URGENT: Freeze request recommended to Binance Hot Wallet"
- VASP Match: Binance Hot Wallet at ~65% confidence
- Graph: 3 nodes (Target, Binance, Tornado Cash), 3 edges
- Evidence: 6 transactions showing mixer interaction

---

## Quick Test Checklist

1. Start backend: `cd backend && uvicorn main:app --reload --port 8080`
2. Start frontend: `python app.py`
3. Open browser to the URL shown in console
4. **Test demo mode:** Check "Demo mode" checkbox → trace `0xd8da6bf26964af9d7eed9e03e53415d37aa96045`
   - Should show: HIGH risk, red banner, URGENT SAHYOG
5. **Test live mode:** Uncheck "Demo mode" → trace `0x28C6c06298d514Db089934071355E5743bf21d60`
   - Should show: Binance VASP match, depends on real transaction data
6. **Test high-risk:** Trace `0x722122df12d4e14e13ac3b6895a86e84145b6967`
   - Should show: Tornado Cash detected in high-risk registry
