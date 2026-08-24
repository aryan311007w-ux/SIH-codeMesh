"""
Core tracing engine — multi-chain, risk-aware, multi-dimensional attribution.

Given a starting wallet and chain, performs a breadth-first walk outward
through its transaction graph, then checks every wallet encountered against:

  1. The VASP registry (for multi-dimensional attribution scoring)
  2. The high-risk registry (mixer / ransomware / darknet / sanctions)
  3. Behavioural heuristics (structuring, peel chains, high velocity)
  4. The wallet feature extractor (for ML-ready feature vectors)

VASP Confidence Formula (multi-dimensional, 0-100)
---------------------------------------------------
The old formula was:
    confidence = 100 - (hops × 25) + path_bonus

The upgraded formula is:

    confidence =
        w_proximity   × graph_proximity_score       (40 % weight)
      + w_interaction × interaction_strength_score  (30 % weight)
      + w_recency     × temporal_recency_score      (20 % weight)
      + w_evidence    × evidence_quality_weight     (10 % weight)

Where:
  graph_proximity_score      = max(0, 100 - hops × 25) + min(15, (paths-1)×5)
  interaction_strength_score = (volume_to_vasp / total_volume) × 100
  temporal_recency_score     = 100 × exp(-0.02 × days_since_last_tx)
  evidence_quality_weight    = 100 | 65 | 35  (high / medium / low provenance)

The component scores are returned alongside the final confidence value so
an investigator can see exactly why a match scored as it did.

Attribution Language
--------------------
The system uses `relationship_type` to distinguish:

  interacts_with   — a fund flow path exists between the wallet and VASP.
                     Default claim for BFS discovery. Does NOT mean ownership.
  controlled_by    — the VASP directly controls this wallet (deposit address).
                     Requires: hops==1 AND wallet_type==deposit_wallet.
  laundered_through — funds moved into VASP and exited to different address.
                     Not asserted by the base tracer; reserved for future flow
                     analysis.

Returns a rich dict including VASP matches, risk report, wallet
classification, wallet feature vector, laundering typologies, and the
graph for visualization.
"""

from __future__ import annotations

from collections import deque, defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Optional

from blockchain_client import BlockchainClient, BlockchainClientError
from risk_engine        import score_wallet
from wallet_classifier  import classify_wallet, WalletType
from feature_extractor  import (
    extract_features,
    compute_interaction_strength,
    compute_temporal_recency,
)

# ---------------------------------------------------------------------------
# VASP Evidence Quality mapping
# ---------------------------------------------------------------------------
# Maps known label sources to evidence quality scores (0-100).
# Future: this should be driven by vasp_registry.py metadata.
# Currently we approximate from the name tag text heuristically.

_EVIDENCE_QUALITY_SCORE = {
    "high":   100,
    "medium":  65,
    "low":     35,
}

# Confidence component weights (must sum to 1.0)
_W_PROXIMITY    = 0.40
_W_INTERACTION  = 0.30
_W_RECENCY      = 0.20
_W_EVIDENCE     = 0.10


class WalletTracer:
    def __init__(
        self,
        client:               BlockchainClient,
        known_vasps:          Dict[str, str],
        max_hops:             int = 3,
        max_tx_per_wallet:    int = 200,
        max_nodes_to_expand:  int = 60,
    ):
        self.client              = client
        self.known_vasps         = known_vasps
        self.max_hops            = max_hops
        self.max_tx_per_wallet   = max_tx_per_wallet
        self.max_nodes_to_expand = max_nodes_to_expand

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def trace(self, root_wallet: str, chain: str = "ethereum",
              max_hops: Optional[int] = None) -> dict:
        root_wallet = root_wallet.lower()
        hops_limit  = max_hops if max_hops is not None else self.max_hops

        visited        = set()
        queue          = deque([(root_wallet, 0)])
        path_to        = {root_wallet: [root_wallet]}
        edges          = []
        all_txs        = {}   # wallet -> List[tx]  (kept for scoring)
        nodes_expanded = 0
        total_tx_scanned = 0

        # raw_matches[vasp_address] = list of {hops, path, volume_eth}
        raw_matches: dict = defaultdict(list)

        while queue and nodes_expanded < self.max_nodes_to_expand:
            current, hops = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            # If this is a known VASP (and not the root), record and stop expanding
            if current in self.known_vasps and current != root_wallet:
                path   = path_to[current]
                volume = self._path_volume(path, edges)
                raw_matches[current].append({"hops": hops, "path": path, "volume_eth": volume})
                continue

            if hops >= hops_limit:
                continue

            try:
                txs = self.client.get_transactions(
                    current, chain=chain, max_results=self.max_tx_per_wallet
                )
            except BlockchainClientError:
                continue

            all_txs[current] = txs
            nodes_expanded  += 1
            total_tx_scanned += len(txs)

            for tx in txs:
                from_addr = tx.get("from", "").lower()
                to_addr   = tx.get("to",   "").lower()
                if not from_addr or not to_addr:
                    continue

                neighbor = to_addr if from_addr == current else from_addr
                if not neighbor or neighbor == current:
                    continue

                try:
                    value_native = int(tx.get("value", 0)) / (10 ** 18)
                except (ValueError, TypeError):
                    value_native = 0.0

                edges.append({
                    "source":    from_addr,
                    "target":    to_addr,
                    "value_eth": value_native,
                    "tx_hash":   tx.get("hash"),
                })

                if neighbor not in visited and neighbor not in path_to:
                    path_to[neighbor] = path_to[current] + [neighbor]
                    queue.append((neighbor, hops + 1))

        # Extract feature vector for root wallet
        root_txs = all_txs.get(root_wallet, [])
        wallet_features = extract_features(
            wallet      = root_wallet,
            txs         = root_txs,
            known_vasps = self.known_vasps,
            edges       = edges,
        )

        # Score VASP matches (multi-dimensional)
        total_volume = wallet_features.get("total_value_eth", 0.0)
        matches = self._score_matches(raw_matches, root_txs, edges, total_volume)

        # Risk score the ROOT wallet
        risk = score_wallet(
            wallet       = root_wallet,
            txs          = root_txs,
            edges        = edges,
            path_wallets = list(path_to.keys()),
        )

        # Classify the ROOT wallet
        classification = classify_wallet(root_wallet, root_txs, self.known_vasps)

        # SAHYOG routing recommendation
        sahyog = self._build_sahyog_routing(matches, risk)

        # Build graph node list
        nodes = self._build_node_list(root_wallet, path_to.keys(), all_txs)

        return {
            "wallet":                     root_wallet,
            "chain":                      chain,
            "total_transactions_scanned": total_tx_scanned,
            "hops_searched":              hops_limit,
            "matches":                    matches,
            "top_match":                  matches[0] if matches else None,
            "risk":                       risk,
            "wallet_classification":      classification,
            "wallet_features":            wallet_features,
            "sahyog_routing":             sahyog,
            "nodes":                      nodes,
            "edges":                      edges[:300],
            "note": (
                "No known-VASP match found within the searched hop depth. "
                "Try increasing max_hops or ensure the VASP registry contains "
                "addresses this wallet's network touches."
                if not matches else None
            ),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ------------------------------------------------------------------
    # Multi-dimensional confidence scorer
    # ------------------------------------------------------------------

    def _score_matches(
        self,
        raw_matches:      dict,
        root_txs:         List[dict],
        edges:            List[dict],
        total_volume_eth: float,
    ) -> List[dict]:
        """
        Score and rank VASP attribution candidates using a multi-dimensional
        weighted formula.

        Components (all 0-100):
            graph_proximity_score      — inverse hop distance + path count bonus
            interaction_strength_score — fraction of traced volume toward this VASP
            temporal_recency_score     — exponential decay on days since last tx
            evidence_quality_weight    — provenance quality of the VASP address label

        Weights: 40 % / 30 % / 20 % / 10 %

        This replaces the legacy single-dimensional formula:
            confidence = 100 - (hops × 25) + path_bonus
        """
        scored = []

        for vasp_addr, observations in raw_matches.items():
            min_hops     = min(o["hops"]       for o in observations)
            num_paths    = len(observations)
            best_path    = min(observations, key=lambda o: o["hops"])["path"]
            total_volume = round(sum(o["volume_eth"] for o in observations), 6)

            # ── Component 1: Graph Proximity (legacy formula, preserved) ──
            base_proximity = max(0, 100 - (min_hops * 25))
            path_bonus     = min(15, (num_paths - 1) * 5)
            proximity_score = min(100.0, base_proximity + path_bonus)

            # ── Component 2: Interaction Strength ────────────────────────
            interaction_score = compute_interaction_strength(
                vasp_addr        = vasp_addr,
                edges            = edges,
                total_volume_eth = total_volume_eth,
            )

            # ── Component 3: Temporal Recency ─────────────────────────────
            recency_score = compute_temporal_recency(
                vasp_addr   = vasp_addr,
                txs         = root_txs,
                known_vasps = self.known_vasps,
            )

            # ── Component 4: Evidence Quality ─────────────────────────────
            evidence_quality  = self._infer_evidence_quality(vasp_addr)
            evidence_score    = _EVIDENCE_QUALITY_SCORE.get(evidence_quality, 65)

            # ── Final Weighted Score ───────────────────────────────────────
            confidence = (
                _W_PROXIMITY   * proximity_score    +
                _W_INTERACTION * interaction_score   +
                _W_RECENCY     * recency_score       +
                _W_EVIDENCE    * evidence_score
            )
            confidence = round(max(5.0, min(100.0, confidence)), 1)

            # ── Relationship Type ─────────────────────────────────────────
            # Upgrade from interacts_with → controlled_by only when there is
            # very strong structural evidence (hop-1 deposit wallet).
            relationship_type = self._infer_relationship_type(
                vasp_addr  = vasp_addr,
                min_hops   = min_hops,
                root_txs   = root_txs,
            )

            scored.append({
                "address":                   vasp_addr,
                "vasp_name":                 self.known_vasps.get(vasp_addr, "Unknown"),
                "hops":                      min_hops,
                "confidence":                confidence,
                "path":                      best_path,
                "volume_eth":                total_volume,

                # Attribution precision
                "relationship_type":         relationship_type,
                "evidence_quality":          evidence_quality,

                # Explainable component scores
                "graph_proximity_score":      round(proximity_score,    1),
                "interaction_strength_score": round(interaction_score,  1),
                "temporal_recency_score":     round(recency_score,      1),
            })

        scored.sort(key=lambda m: m["confidence"], reverse=True)
        return scored

    # ------------------------------------------------------------------
    # Attribution inference helpers
    # ------------------------------------------------------------------

    def _infer_relationship_type(
        self,
        vasp_addr: str,
        min_hops:  int,
        root_txs:  List[dict],
    ) -> str:
        """
        Infer the most defensible relationship_type for this VASP match.

        Rules (conservative — prefer weaker claims):
          - Default: interacts_with
          - Upgrade to controlled_by ONLY when:
              a) min_hops == 1  (direct neighbor)
              b) Root wallet behaves like a deposit wallet (narrow counterparty set,
                 primarily sends to this VASP)
          - laundered_through: NOT asserted here — requires directional flow
            evidence not yet implemented in the base tracer.
        """
        if min_hops != 1 or not root_txs:
            return "interacts_with"

        # Check if the root wallet sends predominantly to this VASP
        to_vasp   = sum(1 for tx in root_txs if tx.get("to",   "").lower() == vasp_addr)
        from_vasp = sum(1 for tx in root_txs if tx.get("from", "").lower() == vasp_addr)
        total     = len(root_txs)

        if total == 0:
            return "interacts_with"

        vasp_fraction = (to_vasp + from_vasp) / total
        unique_receivers = len(set(tx.get("to", "").lower() for tx in root_txs if tx.get("to")))

        # Strong deposit wallet signal: > 70 % of txs to this VASP AND narrow receiver set
        if vasp_fraction > 0.70 and unique_receivers <= 3:
            return "controlled_by"

        return "interacts_with"

    def _infer_evidence_quality(self, vasp_addr: str) -> str:
        """
        Infer evidence quality from available VASP label metadata.

        Future: delegate to vasp_registry.py per-address provenance.
        Current heuristic: all addresses from accounts.csv are treated as
        'medium' (community-maintained, multiple sources). Addresses that
        are also in the high-risk registry (e.g. OFAC sanctioned) are 'high'.
        """
        from high_risk_addresses import is_high_risk
        if is_high_risk(vasp_addr):
            return "high"   # OFAC / government intelligence source
        if vasp_addr in self.known_vasps:
            return "medium"  # Community-labelled dataset
        return "low"

    # ------------------------------------------------------------------
    # Remaining private helpers (unchanged)
    # ------------------------------------------------------------------

    def _path_volume(self, path: List[str], edges: List[dict]) -> float:
        """Sum the native-token value of edges lying along this path."""
        total = 0.0
        for i in range(len(path) - 1):
            a, b = path[i], path[i + 1]
            for e in edges:
                if (e["source"] == a and e["target"] == b) or \
                   (e["source"] == b and e["target"] == a):
                    total += e["value_eth"]
        return round(total, 6)

    def _build_sahyog_routing(self, matches: List[dict], risk: dict) -> dict:
        """Build a SAHYOG portal routing recommendation."""
        if not matches:
            return {
                "vasp_name":       None,
                "vasp_address":    None,
                "action":          "No VASP identified — manual investigation required",
                "disclosure_note": (
                    "No known exchange was reached within the hop limit. "
                    "Consider widening the search depth or checking additional chains."
                ),
            }

        top        = matches[0]
        risk_level = risk.get("risk_level", "LOW")
        typologies = risk.get("typologies", [])

        # Use relationship_type in the action language
        rel = top.get("relationship_type", "interacts_with")
        rel_label = {
            "interacts_with":    "interacts with",
            "controlled_by":     "is attributed to (deposit/operational wallet of)",
            "laundered_through": "laundered funds through",
        }.get(rel, "interacts with")

        if risk_level == "HIGH":
            action = f"URGENT: Freeze request recommended to {top['vasp_name']}"
            note   = (
                f"High-risk wallet with typologies: {', '.join(typologies)}. "
                f"Traced wallet {rel_label} {top['vasp_name']} "
                f"(confidence: {top['confidence']}%, relationship: {rel}). "
                f"Initiate immediate freeze/disclosure request via SAHYOG."
            )
        elif risk_level == "MEDIUM":
            action = f"Disclosure request recommended to {top['vasp_name']}"
            note   = (
                f"Medium-risk wallet. Traced wallet {rel_label} {top['vasp_name']} "
                f"(confidence: {top['confidence']}%, relationship: {rel}). "
                f"Initiate KYC/AML disclosure request via SAHYOG."
            )
        else:
            action = f"Voluntary disclosure inquiry to {top['vasp_name']}"
            note   = (
                f"Low-risk wallet. Traced wallet {rel_label} {top['vasp_name']}. "
                f"Standard disclosure inquiry via SAHYOG may be appropriate "
                f"(confidence: {top['confidence']}%)."
            )

        return {
            "vasp_name":       top["vasp_name"],
            "vasp_address":    top["address"],
            "action":          action,
            "disclosure_note": note,
        }

    def _build_node_list(self, root: str, all_wallets, all_txs: dict) -> List[dict]:
        nodes = []
        for w in all_wallets:
            is_vasp        = w in self.known_vasps
            classification = classify_wallet(w, all_txs.get(w, []), self.known_vasps)
            nodes.append({
                "id":            w,
                "label":         (self.known_vasps.get(w) if is_vasp else f"{w[:6]}…{w[-4:]}"),
                "is_known_vasp": is_vasp,
                "vasp_name":     self.known_vasps.get(w),
                "is_root":       (w == root),
                "wallet_type":   classification["type"],
                "risk_level":    None,  # per-node risk computed for root only (performance)
            })
        return nodes
