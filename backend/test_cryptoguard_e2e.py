"""
End-to-End Test Suite for CryptoGuard AI Backend & APIs
Verifies:
1. Health & Config
2. Chains Info
3. Dashboard Summary
4. Trace Execution (Demo & Multi-Hop Attribution)
5. Database Persistence & Case Retrieval
6. Evidence Management & Review Status Update
7. AI Investigation Copilot (Deterministic Engine)
8. Legal Notice Generator (Section 91 CrPC)
9. VASP Directory & FIU Filtering
10. PDF Report Generation
"""

import sys
import os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(__file__))
from main import app
from database import get_db_connection

client = TestClient(app)

def run_e2e_tests():
    print("=" * 60)
    print("  CryptoGuard AI — End-to-End API Test Suite")
    print("=" * 60)

    # 1. Health
    res = client.get("/api/health")
    assert res.status_code == 200, f"Health check failed: {res.text}"
    health_data = res.json()
    assert health_data["product"] == "CryptoGuard AI"
    print(f"[PASS] 1. Health check ok: {health_data['product']} v{health_data['version']}")

    # 2. Chains
    res = client.get("/api/chains")
    assert res.status_code == 200
    chains = res.json()
    assert len(chains) >= 5
    print(f"[PASS] 2. Supported chains: {[c['key'] for c in chains]}")

    # 3. Dashboard Summary
    res = client.get("/api/v1/dashboard/summary")
    assert res.status_code == 200
    summary = res.json()
    assert "total_cases" in summary
    print(f"[PASS] 3. Dashboard summary: {summary['total_cases']} cases, {summary['known_vasp_count']} VASPs")

    # 4. Core Trace (Demo Mode)
    demo_wallet = "0x742d35cc6634c0532925a3b844bc454e4438f44e"
    res = client.get(f"/api/trace?wallet={demo_wallet}&chain=ethereum&demo_mode=true&case_ref=NCRP-2026-849102")
    assert res.status_code == 200, f"Trace failed: {res.text}"
    trace = res.json()
    assert trace["wallet"] == demo_wallet
    assert "top_match" in trace
    assert trace["top_match"]["vasp_name"] == "CoinDCX (Neblio Technologies)"
    assert trace["risk"]["risk_score"] == 82
    inv_id = trace["investigation_id"]
    print(f"[PASS] 4. Core trace executed: Inv ID = {inv_id}, Top VASP = {trace['top_match']['vasp_name']} ({trace['top_match']['confidence']}%)")

    # 5. Database Persistence & History
    res = client.get(f"/api/investigation/{inv_id}")
    assert res.status_code == 200
    saved_case = res.json()
    assert saved_case["wallet_address"] == demo_wallet
    print(f"[PASS] 5. Database retrieval: Case {inv_id} found in SQLite with risk {saved_case['risk_level']}")

    # 6. Evidence Management
    res = client.get(f"/api/evidence/{inv_id}")
    assert res.status_code == 200
    ev_data = res.json()
    assert len(ev_data["evidence"]) > 0
    ev_item = ev_data["evidence"][0]
    ev_id = ev_item["id"]

    # Update evidence status
    patch_res = client.patch(f"/api/evidence/{ev_id}", json={"status": "Reviewed", "notes": "Verified by Investigator"})
    assert patch_res.status_code == 200
    assert patch_res.json()["new_status"] == "Reviewed"
    print(f"[PASS] 6. Evidence lifecycle: {ev_id} updated to 'Reviewed'")

    # 7. AI Copilot Query
    copilot_res = client.post("/api/copilot/query", json={
        "query": "Why was CoinDCX attributed?",
        "investigation_id": inv_id,
        "trace_data": trace
    })
    assert copilot_res.status_code == 200
    copilot_data = copilot_res.json()
    assert "CoinDCX" in copilot_data["answer"]
    assert "Engine" in copilot_data["engine"]
    print(f"[PASS] 7. AI Copilot: Answered attribution query via {copilot_data['engine']}")

    # 8. Legal Notice Generator (Section 91 CrPC)
    notice_res = client.post("/api/sahyog/notice", json={
        "investigation_id": inv_id,
        "police_station": "Cyber Crime Police Station, North",
        "fir_number": "FIR-2026/104-CYBER",
        "investigator_name": "Inspector S. K. Roy",
        "vasp_name": "CoinDCX (Neblio Technologies)"
    })
    assert notice_res.status_code == 200
    notice_data = notice_res.json()
    assert "SECTION 91" in notice_data["notice_text"]
    assert "CoinDCX" in notice_data["notice_text"]
    print(f"[PASS] 8. Cybercrime response: Section 91 CrPC notice compiled for {notice_data['vasp_name']}")

    # 9. VASP Directory & FIU Filtering
    res = client.get("/api/vasps?fiu_only=true")
    assert res.status_code == 200
    fiu_vasps = res.json()["vasps"]
    assert len(fiu_vasps) >= 5
    print(f"[PASS] 9. VASP Directory: {len(fiu_vasps)} FIU-IND registered entities verified")

    # 10. PDF Report Generation
    res = client.get(f"/api/report/{demo_wallet}?chain=ethereum")
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 1000
    print(f"[PASS] 10. PDF Report: Generated binary PDF ({len(res.content):,} bytes)")

    # 11. Root Static Frontend
    res = client.get("/")
    assert res.status_code == 200
    assert "CryptoGuard" in res.text
    print(f"[PASS] 11. Frontend static bundle served cleanly at /")

    print("\n" + "=" * 60)
    print("  ALL 11 CRYPTOGUARD AI TESTS PASSED PERFECTLY!")
    print("=" * 60)

if __name__ == "__main__":
    run_e2e_tests()
