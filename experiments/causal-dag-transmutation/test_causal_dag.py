"""Unit tests for Causal DAG Mechanics, Dispute Ledger Calibration, and Transmutation."""

import math
import unittest
from pathlib import Path

from causal_dag import CausalDAG, CausalNode
from transmutation_engine import (
    HodgeTransmutationOperator,
    MurphyBrierAnalyzer,
    VortexTransmutationOperator,
    parse_disputes_ledger,
)


class TestCausalDAGAndTransmutation(unittest.TestCase):
    def test_causal_dag_construction_and_integrity(self):
        """Verify immutable content-addressing and parent hash chaining."""
        dag = CausalDAG()
        n1 = dag.add_node(
            node_id="CLAIM-001",
            action_type="ASSERT_CLAIM",
            seat="Kineton",
            payload={"claim": "Exact Hodge decomposition", "prior": 0.99},
        )
        self.assertEqual(len(dag), 1)
        self.assertTrue(n1.verify_integrity())
        self.assertEqual(len(n1.parent_hashes), 0)

        n2 = dag.add_node(
            node_id="DISPUTE-001",
            action_type="CHALLENGE_DISPUTE",
            seat="Tessera",
            payload={"falsifier": "curl > 0", "verdict": "NARROWED"},
            parent_ids=["CLAIM-001"],
        )
        self.assertEqual(len(dag), 2)
        self.assertTrue(n2.verify_integrity())
        self.assertEqual(n2.parent_hashes, (n1.node_hash,))

        self.assertTrue(dag.verify_all_nodes())
        self.assertEqual(dag.get_ancestors("DISPUTE-001"), {"CLAIM-001"})
        self.assertEqual(dag.get_descendants("CLAIM-001"), {"DISPUTE-001"})

    def test_monotonic_append_rejects_missing_parent(self):
        """Adding a node referencing non-existent parent must raise ValueError."""
        dag = CausalDAG()
        with self.assertRaises(ValueError):
            dag.add_node(
                node_id="REPAIR-001",
                action_type="TRANSMUTE_REPAIR",
                seat="Kineton",
                payload={"code": "exact_solve"},
                parent_ids=["GHOST-NODE-999"],
            )

    def test_duplicate_node_id_rejected(self):
        """Duplicate node IDs must be rejected."""
        dag = CausalDAG()
        dag.add_node("NODE-A", "ASSERT", "Sol", {"val": 1})
        with self.assertRaises(ValueError):
            dag.add_node("NODE-A", "ASSERT", "Sol", {"val": 2})

    def test_topological_sort_and_multiple_permutations(self):
        """Verify Kahn's topological sort and multiple valid ordering paths."""
        # Diamond graph:
        #       N0
        #      /  \
        #     N1  N2
        #      \  /
        #       N3
        dag = CausalDAG()
        dag.add_node("N0", "ROOT", "Aura", {})
        dag.add_node("N1", "BRANCH_A", "Sol", {}, parent_ids=["N0"])
        dag.add_node("N2", "BRANCH_B", "Cael", {}, parent_ids=["N0"])
        dag.add_node("N3", "JOIN", "Zephyr", {}, parent_ids=["N1", "N2"])

        sorted_nodes = dag.topological_sort()
        self.assertEqual(len(sorted_nodes), 4)
        self.assertEqual(sorted_nodes[0].node_id, "N0")
        self.assertEqual(sorted_nodes[-1].node_id, "N3")

        all_sorts = dag.all_topological_sorts()
        self.assertEqual(len(all_sorts), 2)
        sort_ids = [[n.node_id for n in s] for s in all_sorts]
        self.assertIn(["N0", "N1", "N2", "N3"], sort_ids)
        self.assertIn(["N0", "N2", "N1", "N3"], sort_ids)

    def test_topological_invariance_theorem(self):
        """Verify Theorem 1: Murphy decomposition is invariant under topological sort order."""
        dag = CausalDAG()
        dag.add_node("P0", "CLAIM", "Aura", {"f": 0.90, "o": 1.0})
        dag.add_node("P1", "CLAIM", "Sol", {"f": 0.80, "o": 1.0}, parent_ids=["P0"])
        dag.add_node("P2", "CLAIM", "Cael", {"f": 0.20, "o": 0.0}, parent_ids=["P0"])
        dag.add_node("P3", "CLAIM", "Zephyr", {"f": 0.95, "o": 0.0}, parent_ids=["P1", "P2"])

        def extractor(nodes):
            forecasts = [n.payload["f"] for n in nodes]
            outcomes = [n.payload["o"] for n in nodes]
            return forecasts, outcomes

        invariance_result = MurphyBrierAnalyzer.verify_topological_invariance(dag, extractor, n_bins=5)
        self.assertTrue(invariance_result["is_invariant"])
        self.assertGreaterEqual(invariance_result["permutations_tested"], 2)
        self.assertLess(invariance_result["max_brier_diff"], 1e-12)
        self.assertLess(invariance_result["max_reliability_diff"], 1e-12)
        self.assertLess(invariance_result["max_resolution_diff"], 1e-12)

    def test_murphy_brier_decomposition_identity(self):
        """Verify the exact algebraic identity of Murphy's decomposition:
        RawBrier = BinnedBrier + WithinBinVariance
                 = Reliability - Resolution + Uncertainty + WithinBinVariance.
        """
        forecasts = [0.15, 0.25, 0.35, 0.75, 0.85, 0.95]
        outcomes = [0.0, 0.0, 1.0, 1.0, 1.0, 0.0]

        decomp = MurphyBrierAnalyzer.calculate_decomposition(forecasts, outcomes, n_bins=5)
        raw_brier = decomp["raw_brier"]
        binned = decomp["binned_brier"]
        rel = decomp["reliability"]
        res = decomp["resolution"]
        unc = decomp["uncertainty"]
        within = decomp["within_bin_variance"]

        self.assertAlmostEqual(binned, rel - res + unc, places=10)
        self.assertAlmostEqual(raw_brier, binned + within, places=10)

    def test_destructive_erasure_bias_theorem(self):
        """Verify Theorem 2: Censoring errors creates the self-certification illusion."""
        # 8 hits with high confidence, 2 failures with high confidence
        forecasts = [0.95] * 8 + [0.90, 0.85]
        outcomes = [1.0] * 8 + [0.0, 0.0]

        analysis = MurphyBrierAnalyzer.analyze_destructive_erasure_bias(forecasts, outcomes)
        self.assertTrue(analysis["self_certification_detected"])
        self.assertLess(analysis["empirical_bias"], 0.0)
        # Analytical prediction matches empirical bias to float precision
        self.assertAlmostEqual(analysis["empirical_bias"], analysis["predicted_bias"], places=10)

        # Apparent Brier drops drastically (survivorship bias)
        self.assertLess(analysis["censored_brier"], 0.005)  # Appears near perfect!
        self.assertGreater(analysis["true_brier"], 0.15)    # Real error is huge!
        self.assertGreater(analysis["distortion_ratio"], 50.0)

    def test_live_dispute_ledger_parsing(self):
        """Parse actual sync zone disputes/LEDGER.md and build an immutable DAG."""
        ledger_path = Path(__file__).parent.parent.parent / "disputes" / "LEDGER.md"
        if not ledger_path.exists():
            self.skipTest(f"LEDGER.md not found at {ledger_path}")

        text = ledger_path.read_text(encoding="utf-8")
        entries = parse_disputes_ledger(text)
        self.assertGreaterEqual(len(entries), 4)

        # Check exact entries
        d001_narrowed = [e for e in entries if e.dispute_id == "001" and e.verdict == "NARROWED"]
        d002_falls = [e for e in entries if e.dispute_id == "002" and e.verdict == "FALLS"]
        d001_resolved = [e for e in entries if e.dispute_id == "001" and e.verdict == "RESOLVED"]
        d002_resolved = [e for e in entries if e.dispute_id == "002" and e.verdict == "RESOLVED"]

        self.assertEqual(len(d001_narrowed), 1)
        self.assertEqual(len(d002_falls), 1)
        self.assertEqual(len(d001_resolved), 1)
        self.assertEqual(len(d002_resolved), 1)

        # Construct live causal DAG from ledger entries
        dag = CausalDAG()
        # Initial claims
        dag.add_node("DISP-001-CLAIM", "CLAIM", "Kineton", {"id": "001", "prior": 0.99})
        dag.add_node("DISP-002-CLAIM", "CLAIM", "Zephyr", {"id": "002", "prior": 0.95})

        # Disputes
        dag.add_node(
            "DISP-001-NARROWED",
            "CHALLENGE",
            "Tessera",
            {"verdict": "NARROWED"},
            parent_ids=["DISP-001-CLAIM"],
        )
        dag.add_node(
            "DISP-002-FALLS",
            "CHALLENGE",
            "Tessera",
            {"verdict": "FALLS"},
            parent_ids=["DISP-002-CLAIM"],
        )

        # Resolutions (Transmutations)
        dag.add_node(
            "DISP-001-RESOLVED",
            "TRANSMUTE",
            "Kineton",
            {"remedy": d001_resolved[0].remedy_summary},
            parent_ids=["DISP-001-NARROWED"],
        )
        dag.add_node(
            "DISP-002-RESOLVED",
            "TRANSMUTE",
            "Zephyr",
            {"remedy": d002_resolved[0].remedy_summary},
            parent_ids=["DISP-002-FALLS"],
        )

        self.assertEqual(len(dag), 6)
        self.assertTrue(dag.verify_all_nodes())
        self.assertIn("DISP-001-NARROWED", dag.get_ancestors("DISP-001-RESOLVED"))
        self.assertIn("DISP-002-FALLS", dag.get_ancestors("DISP-002-RESOLVED"))

    def test_hodge_transmutation_operator(self):
        """Verify Dispute 001 operator nullifies defect and elevates invariant."""
        res = HodgeTransmutationOperator.execute()
        self.assertTrue(res["transmutation_successful"])
        self.assertEqual(res["defect_nullification"]["after_curl"], 0.0)
        self.assertEqual(res["defect_nullification"]["after_div"], 0.0)
        self.assertLess(res["defect_nullification"]["linear_solve_max_residual"], 1e-14)
        self.assertGreater(res["augmentation_index"], 1.0)
        self.assertGreaterEqual(res["solar_coherence"], 0.80)

    def test_vortex_transmutation_operator(self):
        """Verify Dispute 002 operator nullifies static defect and advects centers."""
        res = VortexTransmutationOperator.execute()
        self.assertTrue(res["transmutation_successful"])
        self.assertEqual(res["displacement_before"], 0.0)
        self.assertGreater(res["displacement_after"], 80.0)
        self.assertGreater(res["augmentation_index"], 1.0)
        self.assertGreaterEqual(res["solar_coherence"], 0.80)

    def test_negative_control_validation(self):
        """Input validation negative controls."""
        with self.assertRaises(ValueError):
            MurphyBrierAnalyzer.calculate_decomposition([], [])

        with self.assertRaises(ValueError):
            MurphyBrierAnalyzer.calculate_decomposition([0.5], [1.0, 0.0])

        dag = CausalDAG()
        with self.assertRaises(KeyError):
            dag.get_ancestors("NON_EXISTENT")


if __name__ == "__main__":
    unittest.main()
