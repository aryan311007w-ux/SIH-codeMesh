# Data Sources and Dataset Registry

## Blockchain APIs (Live Data)

| Source | URL | Purpose |
|--------|-----|---------|
| Etherscan API | https://docs.etherscan.io | Ethereum/BSC/Polygon transactions and address labels |
| TronGrid API | https://developers.tron.network | Tron transactions |
| Blockchair API | https://blockchair.com/api | Bitcoin transactions |

## Intelligence Datasets (Embedded in Code)

All datasets are hardcoded in Python files. No external data files required.

| Dataset | File Location | Count | Data Format | Source Reference |
|---------|--------------|-------|-------------|-----------------|
| Known VASPs | backend/known_vasps.py | 33 addresses | dict: address -> name | Community labels, Etherscan address tags |
| Mixer Addresses | backend/high_risk_addresses.py | 17 addresses | set of strings | Tornado Cash official addresses, Blender.io (OFAC) |
| Sanctions Addresses | backend/high_risk_addresses.py | 4 addresses | set of strings | OFAC SDN List (Treasury.gov/public) |
| Ransomware Addresses | backend/high_risk_addresses.py | 3 addresses | set of strings | Public ransomware tracker databases |
| Darknet Addresses | backend/high_risk_addresses.py | 2 addresses | set of strings | Community darknet market address lists |
| Fraud Addresses | backend/high_risk_addresses.py | 1 address | set of strings | Public fraud tracking databases |
| Bridge Addresses | backend/high_risk_addresses.py | 8 addresses | set of strings | Official bridge contract addresses |

## Data Flow

1. User enters wallet address in UI
2. Frontend calls POST /api/trace with wallet, chain, max_hops
3. Backend fetches transactions from blockchain API (Etherscan/TronGrid/Blockchair)
4. Tracer performs BFS to build transaction graph
5. Risk engine scores wallet using intelligence registries
6. VASP attribution finds nearest VASP in graph
7. Wallet classifier identifies wallet type
8. Results returned to frontend for display
9. User can download PDF report or submit to SAHYOG

## Data Retention

- Transaction data: Not stored (fetched at runtime, discarded after trace)
- Case history: In-memory only, cleared on server restart
- No database, no persistent storage
- No user data collected or transmitted externally

---

## How to Add More Addresses to Registries

Edit `backend/high_risk_addresses.py` to add addresses to the respective sets:

```python
MIXER_ADDRESSES = {
    "0x...",  # existing
    "0xNEW_ADDRESS",  # add new
}
```

Edit `backend/known_vasps.py` to add VASP entries:

```python
KNOWN_VASPS = {
    "0x...": "Exchange Name",
    "0xNEW_ADDRESS": "New Exchange Name",
}
```

For bulk imports, replace the `KNOWN_VASPS` dict with a load from
`data/accounts.csv` (format: address,name,chain).