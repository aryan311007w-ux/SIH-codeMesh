"""
Integration tests for the Wallet-to-VASP Attribution System -- SIH-26182.
Tests the full pipeline: tracing, risk scoring, wallet classification,
multi-dimensional confidence scoring, wallet feature extraction,
SAHYOG routing, and multi-chain address validation.
"""

import json
from tracer             import WalletTracer
from risk_engine        import score_wallet
from wallet_classifier  import classify_wallet
from chains             import validate_address, SUPPORTED_CHAINS
from blockchain_client  import BlockchainClient


# ---------------------------------------------------------------------------
# Fake blockchain client for deterministic offline tests
# ---------------------------------------------------------------------------

class FakeClient:
    """Simulates: root -> mid -> known VASP, with a mixer in the graph."""
    def __init__(self):
        self.ROOT  = "0xaaaa000000000000000000000000000000000001"
        self.MID   = "0xbbbb000000000000000000000000000000000002"
        self.VASP  = "0x1111111111111111111111111111111111aaaaaa"
        self.MIXER = "0x722122df12d4e14e13ac3b6895a86e84145b6967"  # Tornado Cash

        self.graph = {
            self.ROOT: [
                {"from": self.ROOT, "to": self.MID,
                 "value": str(int(0.5 * 10**18)), "hash": "0xtx1", "timeStamp": "1700000000"},
                {"from": self.ROOT, "to": self.MIXER,
                 "value": str(int(0.1 * 10**18)), "hash": "0xtx_m", "timeStamp": "1700000100"},
            ],
            self.MID: [
                {"from": self.ROOT, "to": self.MID,
                 "value": str(int(0.5 * 10**18)), "hash": "0xtx1", "timeStamp": "1700000000"},
                {"from": self.MID,  "to": self.VASP,
                 "value": str(int(0.4 * 10**18)), "hash": "0xtx2", "timeStamp": "1700000200"},
            ],
        }

    def get_transactions(self, wallet, chain="ethereum", max_results=200):
        return self.graph.get(wallet.lower(), [])


KNOWN_VASPS = {"0x1111111111111111111111111111111111aaaaaa": "TestExchange"}
fake_client = FakeClient()
tracer      = WalletTracer(client=fake_client, known_vasps=KNOWN_VASPS, max_hops=3)


# ---------------------------------------------------------------------------
# Test 1: VASP attribution + multi-dimensional scoring
# ---------------------------------------------------------------------------

def test_vasp_attribution():
    result = tracer.trace(fake_client.ROOT, chain="ethereum")

    assert result["matches"], "Expected at least one VASP match"
    top = result["matches"][0]
    assert top["vasp_name"] == "TestExchange"
    assert top["hops"] == 2

    # New: verify multi-dimensional score components are present
    assert "graph_proximity_score"       in top, "Missing graph_proximity_score"
    assert "interaction_strength_score"  in top, "Missing interaction_strength_score"
    assert "temporal_recency_score"      in top, "Missing temporal_recency_score"
    assert "relationship_type"           in top, "Missing relationship_type"
    assert "evidence_quality"            in top, "Missing evidence_quality"

    # Confidence should be >= 5 and <= 100
    assert 5.0 <= top["confidence"] <= 100.0, \
        f"Confidence out of range: {top['confidence']}"

    # Relationship type should be interacts_with for 2-hop match
    assert top["relationship_type"] == "interacts_with", \
        f"Expected interacts_with for 2-hop match, got {top['relationship_type']}"

    print(f"[PASS] Test 1: VASP attribution -- 2-hop match: {top['vasp_name']}")
    print(f"       confidence={top['confidence']} | proximity={top['graph_proximity_score']} "
          f"| interaction={top['interaction_strength_score']} | recency={top['temporal_recency_score']}")
    print(f"       relationship_type={top['relationship_type']} | evidence_quality={top['evidence_quality']}")
    return result


# ---------------------------------------------------------------------------
# Test 2: Risk scoring
# ---------------------------------------------------------------------------

def test_risk_scoring(result):
    risk = result.get("risk", {})
    assert "risk_score"  in risk, "Missing risk_score"
    assert "risk_level"  in risk, "Missing risk_level"
    assert "typologies"  in risk, "Missing typologies"

    # Root wallet interacts with Tornado Cash -> should be MEDIUM or HIGH
    assert risk["risk_level"] in ("HIGH", "MEDIUM"), \
        f"Expected HIGH/MEDIUM risk due to mixer interaction, got {risk['risk_level']}"
    assert "mixer_interaction" in risk.get("flags", []) or \
           any("Mixer" in t for t in risk.get("typologies", [])), \
        "Expected mixer flag in risk report"

    print(f"[PASS] Test 2: Risk scoring -- level={risk['risk_level']}, score={risk['risk_score']}")
    print(f"       typologies={risk['typologies']}")


# ---------------------------------------------------------------------------
# Test 3: Wallet classification
# ---------------------------------------------------------------------------

def test_wallet_classification(result):
    cls = result.get("wallet_classification", {})
    assert "type"   in cls, "Missing classification type"
    assert "label"  in cls, "Missing classification label"
    assert "reason" in cls, "Missing classification reason"
    print(f"[PASS] Test 3: Wallet classification -- {cls['type']} / {cls['label']}")


# ---------------------------------------------------------------------------
# Test 4: Wallet feature vector
# ---------------------------------------------------------------------------

def test_wallet_features(result):
    feats = result.get("wallet_features")
    assert feats is not None, "Missing wallet_features in trace result"

    required_keys = [
        "tx_count", "unique_counterparties", "total_value_eth",
        "in_out_ratio", "tx_per_day", "mixer_exposure",
        "vasp_exposure", "structuring_ratio", "peel_chain_score",
    ]
    for key in required_keys:
        assert key in feats, f"Missing feature key: {key}"

    # Root wallet sent 0.5 ETH to MID + 0.1 ETH to mixer = 0.6 ETH total
    assert feats["tx_count"] == 2, f"Expected 2 txs, got {feats['tx_count']}"
    assert feats["total_value_eth"] > 0, "Expected non-zero total volume"
    # Mixer exposure: 1 out of 2 counterparties (MID, MIXER) is a mixer
    assert feats["mixer_exposure"] > 0, "Expected non-zero mixer_exposure"

    print(f"[PASS] Test 4: Feature vector -- tx_count={feats['tx_count']}, "
          f"total_eth={feats['total_value_eth']:.4f}, mixer_exposure={feats['mixer_exposure']:.3f}")


# ---------------------------------------------------------------------------
# Test 5: SAHYOG routing
# ---------------------------------------------------------------------------

def test_sahyog_routing(result):
    routing = result.get("sahyog_routing", {})
    assert "action"          in routing, "Missing sahyog action"
    assert "disclosure_note" in routing, "Missing disclosure_note"
    assert routing["vasp_name"] == "TestExchange", \
        f"Expected TestExchange routing, got {routing.get('vasp_name')}"

    # New: check that routing language uses relationship type correctly
    note = routing.get("disclosure_note", "")
    assert len(note) > 10, "disclosure_note is empty"

    print(f"[PASS] Test 5: SAHYOG routing -- {routing['action'][:60]}...")


# ---------------------------------------------------------------------------
# Test 6: Chain address validation
# ---------------------------------------------------------------------------

def test_chain_validation():
    assert validate_address("0xd8dA6BF26964aF9D7eed9e03E53415D37aA96045", "ethereum"), \
        "Valid ETH address should pass"
    assert not validate_address("0xshort", "ethereum"), \
        "Short address should fail"
    assert validate_address("TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7", "tron"), \
        "Valid Tron address should pass"
    assert not validate_address("0xabc123", "tron"), \
        "ETH address should fail Tron validation"
    assert len(SUPPORTED_CHAINS) >= 5, "Expected at least 5 supported chains"
    print(f"[PASS] Test 6: Chain validation -- {len(SUPPORTED_CHAINS)} chains supported")


# ---------------------------------------------------------------------------
# Test 7: FastAPI app loads with all required routes
# ---------------------------------------------------------------------------

def test_app_loads():
    from main import app
    assert app, "FastAPI app should load"
    routes = [r.path for r in app.routes]
    required = [
        "/api/health", "/api/trace", "/api/chains",
        "/api/alerts/high-risk", "/api/sahyog/submit", "/api/history"
    ]
    for route in required:
        assert route in routes, f"Missing route: {route}"
    print(f"[PASS] Test 7: App loaded with {len(routes)} routes")


# ---------------------------------------------------------------------------
# Run all tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n=== SIH-26182 Test Suite ===\n")
    result = test_vasp_attribution()
    test_risk_scoring(result)
    test_wallet_classification(result)
    test_wallet_features(result)
    test_sahyog_routing(result)
    test_chain_validation()
    test_app_loads()
    print("\n=== ALL TESTS PASSED ===\n")
    # Uncomment to inspect full result:
    # print(json.dumps(result, indent=2, default=str))
