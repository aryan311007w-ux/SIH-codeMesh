# Test Wallet Addresses for Demo

Copy these addresses into the investigation form at http://localhost:8080

---

## Known VASPs (Expected: LOW risk, VASP match)

| # | Wallet Address | Name | Expected Risk | Expected VASP |
|---|---------------|------|--------------|---------------|
| 1 | 0x28C6c06298d514Db089934071355E5743bf21d60 | Binance Hot Wallet | LOW | Binance |
| 2 | 0x503828976D22510aad0201ac7EC88293211D23Da | Coinbase | LOW | Coinbase |
| 3 | 0x2910543af39aba0cd09dbb2d50200b3e800a63d2 | Kraken Exchange | LOW | Kraken |

---

## Mixers (Expected: HIGH risk, score 100, no VASP match)

| # | Wallet Address | Name | Classification |
|---|---------------|------|---------------|
| 4 | 0x722122df12d4e14e13ac3b6895a86e84145b6967 | Tornado Cash Proxy | Mixer / Tumbler |
| 5 | 0xa160cdab225685da1d56aa342ad8841c3b53f291 | Tornado Cash 10 ETH Pool | Mixer / Tumbler |
| 6 | 0x910cbd523d972eb0a6f4cae4618ad62622b39dbf | Tornado Cash 1 ETH Pool | Mixer / Tumbler |

---

## Sanctioned / Ransomware (Expected: HIGH risk, score 100)

| # | Wallet Address | Name | Classification |
|---|---------------|------|---------------|
| 7 | 0x098b716b8aaf21512996dc57eb0615e2383e2f96 | Ronin Bridge Hacker | Ransomware Wallet |
| 8 | 0xd882cfc523d972eb0a6f4cae4618ad62622b39dbf | Blender.io | Mixer / Tumbler |
| 9 | 0x901bb9583b24d97e995513c6778dc6888ab6870e | DPRK Lazarus Group | Sanctioned Address |

---

## Suspicious Behavior (Expected: MEDIUM risk, score ~54)

| # | Wallet Address | Expected Risk | Active Signals |
|---|---------------|--------------|----------------|
| 10 | 0xd8da6bf26964af9d7eed9e03e53415d37aa96045 | MEDIUM | Structuring / Smurfing |

---

## Other Known VASPs to Try

| Wallet Address | Name |
|---------------|------|
| 0x7a250d5630B4cF539739dF2C5dAcB4c659F2488D | Uniswap V2 Router |
| 0xdAC17F958D2ee523a2206206994597C13D831ec7 | Tether USD (USDT) |
| 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 | USD Coin (USDC) |
| 0x514910771AF9Ca656af840dff83E8264EcF986CA | Chainlink (LINK) |
| 0x6b175474E89094C44Da98b954EedeAC495271d0F | DAI Maker Vault |
| 0x7d2768de32b0b80b7a3454c06bdac94a69ddc7a9 | Aave V3 Pool |
| 0x28C6C06298d514DB089934071355E5743bf21D60 | Binance Hot Wallet |
