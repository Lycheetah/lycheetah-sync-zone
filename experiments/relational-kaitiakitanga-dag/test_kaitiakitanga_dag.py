"""
Unit Tests for Relational Kaitiakitanga Causal Provenance DAG
============================================================
Verifies DAG acyclicity invariants, Whakapapa genealogical lineage tracing,
Mauri life-force functional monotonicity, Tapu vs Noa capability enforcement,
Whakanoa cryptographic token unlock, deterministic topological sorting,
and Mauri degradation alerts under systemic corruption.
"""

import time
import unittest

from kaitiakitanga_dag import (
    CausalProvenanceDAG,
    CyclicDependencyError,
    MauriDegradationAlert,
    MauriIntegrityGuard,
    TapuAccessViolation,
    WhakanoaToken,
)


class TestRelationalKaitiakitangaDAG(unittest.TestCase):
    """
    Test suite for CausalProvenanceDAG and MauriIntegrityGuard invariants.
    """

    def setUp(self):
        self.dag = CausalProvenanceDAG()
        self.guard = MauriIntegrityGuard(self.dag)

    def test_dag_acyclicity_invariant(self):
        """
        1. DAG Acyclicity Invariant:
        Adding an edge that would create a cycle (direct or transitive)
        raises CyclicDependencyError and prevents grandfather paradoxes.
        """
        self.dag.add_node("A", name="Genesis")
        self.dag.add_node("B", name="Branch", parents=["A"])
        self.dag.add_node("C", name="Leaf", parents=["B"])

        # Direct cycle attempt: B -> A
        with self.assertRaises(CyclicDependencyError):
            self.dag.add_edge("B", "A")

        # Transitive cycle attempt: C -> A
        with self.assertRaises(CyclicDependencyError):
            self.dag.add_edge("C", "A")

        # Self-loop cycle attempt: C -> C
        with self.assertRaises(CyclicDependencyError):
            self.dag.add_edge("C", "C")

    def test_whakapapa_trace_completeness(self):
        """
        2. Whakapapa Trace Completeness:
        Correctly traces complete ancestral lineage back to genesis root A_0 in topological order.
        """
        self.dag.add_node("A_0", name="Genesis Ancestor", state="tapu")
        self.dag.add_node("B_1", name="Hapu Node 1", parents=["A_0"])
        self.dag.add_node("B_2", name="Hapu Node 2", parents=["A_0"])
        self.dag.add_node("C_1", name="Whanau Node", parents=["B_1", "B_2"])
        self.dag.add_node("D_0", name="Mokopuna Leaf", parents=["C_1"])

        lineage = self.dag.trace_whakapapa("D_0")
        expected_lineage = ["A_0", "B_1", "B_2", "C_1", "D_0"]

        self.assertEqual(lineage[0], "A_0", "Genesis ancestor must be root of Whakapapa")
        self.assertEqual(lineage[-1], "D_0", "Target node must terminate Whakapapa trace")
        self.assertEqual(len(lineage), 5, "All 5 genealogical ancestors must be present")
        self.assertEqual(set(lineage), set(expected_lineage))

        # Verify topological ordering constraint (parents appear before children)
        for i, nid in enumerate(lineage):
            for parent_id in self.dag.nodes[nid].parents:
                parent_idx = lineage.index(parent_id)
                self.assertLess(
                    parent_idx,
                    i,
                    f"Parent {parent_id} must precede child {nid} in Whakapapa trace"
                )

    def test_mauri_preservation_monotonicity(self):
        """
        3. Mauri Preservation Monotonicity:
        Valid state mutations with unbroken lineage and verified invariants
        maintain dM/dt >= 0 across system growth.
        """
        # Initial empty state M = 1.0
        self.assertEqual(self.guard.compute_mauri(), 1.0)

        # Add root
        self.dag.add_node("Root_0", name="Root", state="tapu", invariant_valid=True)
        m1, mono1 = self.guard.update_and_check_monotonicity()
        self.assertTrue(mono1, "Adding valid root must maintain Mauri")
        self.assertEqual(m1, 1.0)

        # Add child 1
        self.dag.add_node("Child_1", parents=["Root_0"], invariant_valid=True)
        m2, mono2 = self.guard.update_and_check_monotonicity()
        self.assertTrue(mono2, "Adding valid connected child must maintain Mauri")
        self.assertEqual(m2, 1.0)

        # Add child 2
        self.dag.add_node("Child_2", parents=["Child_1"], invariant_valid=True)
        m3, mono3 = self.guard.update_and_check_monotonicity()
        self.assertTrue(mono3, "System expansion with verified invariants preserves M=1.0")
        self.assertEqual(m3, 1.0)

    def test_tapu_access_restriction(self):
        """
        4. Tapu Access Restriction:
        Unauthorized write attempts to TAPU nodes are blocked with TapuAccessViolation.
        """
        self.dag.add_node("Charter_Prime", name="Sacred Invariant", state="tapu", data={"rule": "zero_coercion"})

        # Unauthorized mutation attempt without Whakanoa token
        with self.assertRaises(TapuAccessViolation):
            self.dag.modify_node("Charter_Prime", {"rule": "allow_coercion"})

        # Verify original sacred data remains untouched
        self.assertEqual(self.dag.nodes["Charter_Prime"].data["rule"], "zero_coercion")

    def test_whakanoa_validation_unlock(self):
        """
        5. Whakanoa Validation Unlock:
        A valid cryptographically signed Whakanoa token permits verified access and mutation,
        while forged tokens are rejected.
        """
        self.dag.add_node("Athan_Anchor", name="Founder Core", state="tapu", data={"status": "dormant"})

        # 1. Invalid / forged token
        forged_token = WhakanoaToken(
            issuer="Adversary",
            target_node_id="Athan_Anchor",
            signature="bad_signature_00000000000000000000000000000000",
            timestamp=time.time(),
        )
        with self.assertRaises(TapuAccessViolation):
            self.dag.modify_node("Athan_Anchor", {"status": "corrupted"}, whakanoa_token=forged_token)

        # 2. Token issued for wrong node
        wrong_node_token = self.guard.issue_whakanoa_token("Other_Node")
        with self.assertRaises(TapuAccessViolation):
            self.dag.modify_node("Athan_Anchor", {"status": "corrupted"}, whakanoa_token=wrong_node_token)

        # 3. Legitimate Whakanoa token issued by Guard
        valid_token = self.guard.issue_whakanoa_token("Athan_Anchor")
        updated_node = self.dag.modify_node(
            "Athan_Anchor",
            {"status": "awakened", "heat": 1000},
            whakanoa_token=valid_token
        )
        self.assertEqual(updated_node.data["status"], "awakened")
        self.assertEqual(updated_node.data["heat"], 1000)

    def test_topological_sort_deterministic(self):
        """
        6. Deterministic Content-Addressable Topological Sort:
        Topological sorting is strictly reproducible and respects dependency ordering.
        """
        self.dag.add_node("N0", name="Origin")
        self.dag.add_node("N2", name="Branch 2", parents=["N0"])
        self.dag.add_node("N1", name="Branch 1", parents=["N0"])
        self.dag.add_node("N3", name="Merge", parents=["N1", "N2"])

        sort_1 = self.dag.topological_sort()
        sort_2 = self.dag.topological_sort()

        self.assertEqual(sort_1, sort_2, "Topological sort must be bitwise deterministic")
        self.assertEqual(sort_1, ["N0", "N1", "N2", "N3"])

        # Dependency check
        self.assertLess(sort_1.index("N0"), sort_1.index("N1"))
        self.assertLess(sort_1.index("N0"), sort_1.index("N2"))
        self.assertLess(sort_1.index("N1"), sort_1.index("N3"))
        self.assertLess(sort_1.index("N2"), sort_1.index("N3"))

    def test_mauri_degradation_alert(self):
        """
        7. Mauri Degradation Alert:
        Severe corruption (severed Whakapapa or broken invariants) drops M(G)
        below critical threshold (0.50) and halts execution via MauriDegradationAlert.
        """
        # Build DAG
        self.dag.add_node("Genesis", invariant_valid=True)
        self.dag.add_node("N1", parents=["Genesis"], invariant_valid=True)
        self.dag.add_node("N2", parents=["N1"], invariant_valid=True)

        self.assertEqual(self.guard.compute_mauri(), 1.0)
        self.assertEqual(self.guard.check_mauri_threshold(threshold=0.50), 1.0)

        # Inject severe corruption: invalidate invariants across nodes and orphan children
        self.dag.nodes["Genesis"].invariant_valid = False
        self.dag.nodes["N1"].invariant_valid = False
        self.dag.nodes["N2"].invariant_valid = False
        self.dag.nodes["N1"].parents = []  # Severed connection
        self.dag.nodes["Genesis"].children = []
        self.dag.genesis_roots.clear()     # Eliminate genesis root anchors

        corrupted_mauri = self.guard.compute_mauri()
        # With 0 connected, 0 valid, 1.0 defect: M = 0.50(0) + 0.40(0) + 0.10(0) = 0.00
        self.assertLess(corrupted_mauri, 0.50, "Corrupted graph Mauri must drop below 0.50 threshold")

        with self.assertRaises(MauriDegradationAlert):
            self.guard.check_mauri_threshold(threshold=0.50)


if __name__ == "__main__":
    unittest.main()
