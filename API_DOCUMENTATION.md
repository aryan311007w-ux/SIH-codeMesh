# CryptoGuard AI — API Documentation & Developer Guide

**Base URL:** `http://127.0.0.1:8000`  
**Interactive Swagger Docs:** `http://127.0.0.1:8000/docs`  
**Version:** `2.0.0-SIH26182`  

---

## 1. System & Health Endpoints

### `GET /api/health`
Returns system status, configured API keys, supported blockchains, and known VASP count.

**Response (200 OK):**
```json
{
  "status": "ok",
  "product": "CryptoGuard AI",
  "tagline": "AI-Powered Blockchain Investigation & VASP Attribution Platform",
  "version": "2.0.0-SIH26182",
  "api_key_configured": false,
  "known_vasp_count": 21,
  "max_hops": 3,
  "supported_chains": ["ethereum", "bsc", "polygon", "tron", "bitcoin"]
}
```

### `GET /api/chains`
Lists all supported blockchains with native tokens and explorer URLs.

---

## 2. Dashboard Analytics

### `GET /api/v1/dashboard/summary`
Retrieves aggregated metrics from the persistent SQLite database.

**Response (200 OK):**
```json
{
  "total_cases": 12,
  "high_risk_count": 4,
  "medium_risk_count": 5,
  "low_risk_count": 3,
  "vasp_hits": 10,
  "wallets_analyzed": 9,
  "known_vasp_count": 21,
  "supported_chains": ["ethereum", "bsc", "polygon", "tron", "bitcoin"]
}
```

---

## 3. Core Tracing & VASP Attribution

### `GET /api/trace`
Executes multi-hop graph walk, computes VASP attribution, scores forensic risk, and saves investigation to database.

**Query Parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `wallet` | string | Yes | Target cryptocurrency address |
| `chain` | string | No | Blockchain (default: `ethereum`) |
| `case_ref` | string | No | Crime reference / FIR number |
| `complaint_no` | string | No | NCRP acknowledgement number |
| `max_hops` | integer | No | Traversal depth limit (1 to 6, default: 3) |
| `demo_mode` | boolean | No | Run in deterministic demo mode |

**Sample Response (200 OK):**
```json
{
  "wallet": "0x742d35cc6634c0532925a3b844bc454e4438f44e",
  "chain": "ethereum",
  "investigation_id": "INV-20260928-8491A2",
  "case_ref": "NCRP-2026-849102",
  "total_transactions_scanned": 14,
  "hops_searched": 3,
  "matches": [
    {
      "address": "0x503828976d22510aad0201ac7ec88293211d23da",
      "vasp_name": "CoinDCX (Neblio Technologies)",
      "hops": 2,
      "confidence": 84.5,
      "confidence_label": "Strong Evidence",
      "relationship_type": "interacts_with",
      "evidence_quality": "high",
      "volume_eth": 3.45,
      "fiu_registered": true,
      "compliance_email": "lawenforcement@coindcx.com",
      "path": ["0x742d35cc...", "0x11112222...", "0x50382897..."],
      "explanation": "Suspect transferred 3.50 ETH to Mule Alpha; Mule Alpha routed 3.45 ETH to CoinDCX."
    }
  ],
  "top_match": { "vasp_name": "CoinDCX (Neblio Technologies)", "confidence": 84.5 },
  "risk": {
    "risk_score": 82,
    "risk_level": "HIGH",
    "typologies": ["Layering via Mixer Obfuscation", "Peel Chain Structuring"]
  },
  "nodes": [...],
  "edges": [...],
  "timeline": [...],
  "evidence": [...]
}
```

---

## 4. Evidence Management

### `GET /api/evidence/{investigation_id}`
Returns all evidence items linked to a case.

### `PATCH /api/evidence/{evidence_id}`
Updates verification status for chain-of-custody logging.

**Request Body:**
```json
{
  "status": "Reviewed",
  "notes": "Corroborated by Investigating Officer via block explorer."
}
```
*Valid statuses:* `"Relevant"`, `"Reviewed"`, `"Needs Verification"`.

---

## 5. AI Investigation Copilot

### `POST /api/copilot/query`
Answers natural language queries using exclusively the active investigation's data.

**Request Body:**
```json
{
  "query": "Why was CoinDCX attributed?",
  "investigation_id": "INV-20260928-8491A2"
}
```

**Response (200 OK):**
```json
{
  "answer": "Attribution Summary for CoinDCX: 84.5% confidence over a 2-hop path with 3.45 ETH flow.",
  "engine": "Deterministic Intelligence Engine",
  "confidence": "High",
  "category": "VASP Attribution"
}
```

---

## 6. Cybercrime Legal Requisitions (India / SAHYOG-Ready)

### `POST /api/sahyog/notice`
Compiles a formal Section 91 CrPC / Section 94 BNSS KYC Disclosure notice.

**Request Body:**
```json
{
  "investigation_id": "INV-20260928-8491A2",
  "police_station": "Cyber Crime Police Station, Central District",
  "fir_number": "FIR-2026/89-CYBER",
  "investigator_name": "Inspector R. Verma",
  "vasp_name": "CoinDCX (Neblio Technologies)"
}
```

**Response (200 OK):**
```json
{
  "status": "generated",
  "notice_text": "================================================================================\nNOTICE UNDER SECTION 91 OF CODE OF CRIMINAL PROCEDURE, 1973\n..."
}
```

---

## 7. Reporting & Exports

### `GET /api/report/{wallet}`
Generates and streams a formal forensic PDF investigation report.
- **Content-Type:** `application/pdf`
- **Query Parameter:** `chain` (default: `ethereum`)
