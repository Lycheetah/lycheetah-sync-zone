"""
test_d_separation.py
Unit tests verifying DAG d-separation, active trail search, and Pearl's
causal criteria across forks, chains, colliders, and M-bias structures.

Author: Aeon (Gemini Cohort, Lycheetah Sync Zone)
Date: 2026-10-23
"""

import unittest
from d_separation import CausalDAG


class TestDSeparationPrimitives(unittest.TestCase):
    """
    Tests for the three elementary causal junctions:
    1. Fork (Common Cause)
    2. Chain (Mediated Cause)
    3. Collider (Common Effect / Inverted Fork)
    """

    def test_fork(self):
        """
        Fork: X <- Z -> Y (Z is a common cause / confounder).
        - Unconditioned (Z = empty): active trail exists (d-connected).
        - Conditioned on Z: trail is blocked (d-separated).
        """
        dag = CausalDAG()
        dag.add_edge("Z", "X")
        dag.add_edge("Z", "Y")

        # Unconditioned: d-connected
        self.assertFalse(dag.is_d_separated("X", "Y", set()))
        trail = dag.find_active_trail("X", "Y", set())
        self.assertIsNotNone(trail)
        self.assertEqual(trail, ["X", "Z", "Y"])
        self.assertTrue(dag.is_trail_active(trail, set()))

        # Conditioned on common cause Z: d-separated
        self.assertTrue(dag.is_d_separated("X", "Y", {"Z"}))
        self.assertIsNone(dag.find_active_trail("X", "Y", {"Z"}))

    def test_chain(self):
        """
        Chain: X -> Z -> Y (Z is a mediator).
        - Unconditioned (Z = empty): active trail exists (d-connected).
        - Conditioned on Z: trail is blocked (d-separated).
        """
        dag = CausalDAG()
        dag.add_edge("X", "Z")
        dag.add_edge("Z", "Y")

        # Unconditioned: d-connected
        self.assertFalse(dag.is_d_separated("X", "Y", set()))
        trail = dag.find_active_trail("X", "Y", set())
        self.assertIsNotNone(trail)
        self.assertEqual(trail, ["X", "Z", "Y"])
        self.assertTrue(dag.is_trail_active(trail, set()))

        # Conditioned on mediator Z: d-separated
        self.assertTrue(dag.is_d_separated("X", "Y", {"Z"}))
        self.assertIsNone(dag.find_active_trail("X", "Y", {"Z"}))

    def test_collider(self):
        """
        Collider: X -> Z <- Y (Z is a common effect).
        - Unconditioned (Z = empty): collider blocks the trail (d-separated).
        - Conditioned on collider Z: conditioning opens the trail (d-connected).
        """
        dag = CausalDAG()
        dag.add_edge("X", "Z")
        dag.add_edge("Y", "Z")

        # Unconditioned: collider naturally blocks, d-separated
        self.assertTrue(dag.is_d_separated("X", "Y", set()))
        self.assertIsNone(dag.find_active_trail("X", "Y", set()))

        # Conditioned on collider Z: opens trail, d-connected
        self.assertFalse(dag.is_d_separated("X", "Y", {"Z"}))
        trail = dag.find_active_trail("X", "Y", {"Z"})
        self.assertIsNotNone(trail)
        self.assertEqual(trail, ["X", "Z", "Y"])
        self.assertTrue(dag.is_trail_active(trail, {"Z"}))

    def test_collider_descendant_conditioning(self):
        """
        Collider with Descendant: X -> Z <- Y, with Z -> W.
        Conditioning on descendant W unblocks the collider Z!
        - Unconditioned: d-separated.
        - Conditioned on W (descendant of Z): d-connected.
        """
        dag = CausalDAG()
        dag.add_edge("X", "Z")
        dag.add_edge("Y", "Z")
        dag.add_edge("Z", "W")

        # Unconditioned: d-separated
        self.assertTrue(dag.is_d_separated("X", "Y", set()))

        # Conditioned on descendant W: collider Z is activated, d-connected!
        self.assertFalse(dag.is_d_separated("X", "Y", {"W"}))
        trail = dag.find_active_trail("X", "Y", {"W"})
        self.assertIsNotNone(trail)
        self.assertEqual(trail, ["X", "Z", "Y"])
        self.assertTrue(dag.is_trail_active(trail, {"W"}))

        # Conditioned on descendant of descendant: Z -> W -> V
        dag.add_edge("W", "V")
        self.assertFalse(dag.is_d_separated("X", "Y", {"V"}))
        trail_v = dag.find_active_trail("X", "Y", {"V"})
        self.assertIsNotNone(trail_v)
        self.assertEqual(trail_v, ["X", "Z", "Y"])
        self.assertTrue(dag.is_trail_active(trail_v, {"V"}))


class TestComplexCausalTopologies(unittest.TestCase):
    """
    Tests on realistic multi-node DAGs: M-bias, Front-door, and Diamond graphs.
    """

    def test_m_bias(self):
        r"""
        M-Bias DAG:
            U1       U2
           /  \     /  \
          v    v   v    v
          X      M      Y

        - Unconditioned (Z = empty): M is a collider; trail X <- U1 -> M <- U2 -> Y is blocked.
          Therefore X and Y are d-separated!
        - Conditioning on M: activates collider M, inducing spurious correlation (d-connected)!
        - Conditioning on {M, U1}: U1 is a non-collider (fork), so conditioning on U1 re-blocks the trail!
        """
        dag = CausalDAG()
        dag.add_edge("U1", "X")
        dag.add_edge("U1", "M")
        dag.add_edge("U2", "M")
        dag.add_edge("U2", "Y")

        # Unconditioned: d-separated
        self.assertTrue(dag.is_d_separated("X", "Y", set()))
        self.assertIsNone(dag.find_active_trail("X", "Y", set()))

        # Conditioned on M (collider): spurious connection opened!
        self.assertFalse(dag.is_d_separated("X", "Y", {"M"}))
        trail = dag.find_active_trail("X", "Y", {"M"})
        self.assertIsNotNone(trail)
        self.assertEqual(trail, ["X", "U1", "M", "U2", "Y"])
        self.assertTrue(dag.is_trail_active(trail, {"M"}))

        # Conditioned on {M, U1}: U1 is blocked, so d-separated again
        self.assertTrue(dag.is_d_separated("X", "Y", {"M", "U1"}))

        # Conditioned on {M, U2}: U2 is blocked, so d-separated again
        self.assertTrue(dag.is_d_separated("X", "Y", {"M", "U2"}))

    def test_diamond_and_multiple_paths(self):
        """
        Diamond Network:
            X -> A -> Y
            X -> B -> Y
        Two parallel chains.
        - Z = empty: d-connected.
        - Z = {A}: d-connected (via path through B).
        - Z = {B}: d-connected (via path through A).
        - Z = {A, B}: d-separated (both paths blocked).
        """
        dag = CausalDAG()
        dag.add_edge("X", "A")
        dag.add_edge("A", "Y")
        dag.add_edge("X", "B")
        dag.add_edge("B", "Y")

        self.assertFalse(dag.is_d_separated("X", "Y", set()))
        self.assertFalse(dag.is_d_separated("X", "Y", {"A"}))
        self.assertFalse(dag.is_d_separated("X", "Y", {"B"}))
        self.assertTrue(dag.is_d_separated("X", "Y", {"A", "B"}))

    def test_direct_edge_always_connected(self):
        """
        If there is a direct edge X -> Y, no conditioning set can d-separate them.
        """
        dag = CausalDAG()
        dag.add_edge("X", "Y")
        dag.add_edge("X", "Z")
        dag.add_edge("Z", "Y")

        self.assertFalse(dag.is_d_separated("X", "Y", set()))
        self.assertFalse(dag.is_d_separated("X", "Y", {"Z"}))


class TestCausalCriteriaAndInvariants(unittest.TestCase):
    """
    Tests for structural properties: Markov blanket, back-door criterion,
    cycle detection, and consistency with exhaustive trail search.
    """

    def test_markov_blanket(self):
        """
        Verify Markov blanket: MB(V) = Parents(V) U Children(V) U Parents(Children(V)) \\ {V}.
        Conditioned on MB(V), V is d-separated from every other node in the graph.
        """
        dag = CausalDAG()
        # Graph:
        # P1 -> V -> C1
        # P2 -> V -> C2
        # C1 <- O1 (other parent of C1)
        # S (separate isolated component / ancestor of P1)
        # S -> P1
        dag.add_edge("S", "P1")
        dag.add_edge("P1", "V")
        dag.add_edge("P2", "V")
        dag.add_edge("V", "C1")
        dag.add_edge("V", "C2")
        dag.add_edge("O1", "C1")

        mb = dag.markov_blanket("V")
        expected_mb = {"P1", "P2", "C1", "C2", "O1"}
        self.assertEqual(mb, expected_mb)

        # Conditioned on MB(V), V must be d-separated from S
        self.assertTrue(dag.is_d_separated("V", "S", mb))

    def test_backdoor_criterion(self):
        """
        Test Pearl's Back-Door Criterion on a classic confounding graph:
        X <- U -> Y, and X -> Y.
        - Backdoor path: X <- U -> Y
        - Frontdoor causal path: X -> Y
        Adjustment set {U} is admissible.
        Adjustment set {Y} is inadmissible (contains descendant of X, or outcome itself).
        """
        dag = CausalDAG()
        dag.add_edge("U", "X")
        dag.add_edge("U", "Y")
        dag.add_edge("X", "Y")

        # Empty set does NOT satisfy back-door (back-door path X <- U -> Y is open)
        self.assertFalse(dag.is_backdoor_admissible("X", "Y", set()))

        # S = {U} blocks the back-door path without conditioning on descendants of X
        self.assertTrue(dag.is_backdoor_admissible("X", "Y", {"U"}))

        # Adding a descendant of X: X -> D
        dag.add_edge("X", "D")
        # {U, D} is inadmissible because D is a descendant of X
        self.assertFalse(dag.is_backdoor_admissible("X", "Y", {"U", "D"}))

    def test_cycle_detection(self):
        """
        Adding an edge that would create a cycle must raise ValueError.
        """
        dag = CausalDAG()
        dag.add_edge("A", "B")
        dag.add_edge("B", "C")
        dag.add_edge("C", "D")

        # Adding D -> A introduces a 4-cycle: A -> B -> C -> D -> A
        with self.assertRaises(ValueError):
            dag.add_edge("D", "A")

        # Adding self-loop must raise ValueError
        with self.assertRaises(ValueError):
            dag.add_edge("A", "A")

        self.assertTrue(dag.is_dag())
        top_order = dag.topological_sort()
        self.assertEqual(top_order, ["A", "B", "C", "D"])

    def test_cross_validation_with_all_simple_trails(self):
        """
        Cross-validate active trail BFS against exhaustive enumeration
        and is_trail_active on all simple trails in a non-trivial DAG.
        """
        dag = CausalDAG()
        dag.add_edge("A", "B")
        dag.add_edge("A", "C")
        dag.add_edge("B", "D")
        dag.add_edge("C", "D")
        dag.add_edge("D", "E")
        dag.add_edge("F", "C")
        dag.add_edge("F", "E")

        all_nodes = list(dag.nodes)
        conditioning_sets = [
            set(),
            {"C"},
            {"D"},
            {"C", "D"},
            {"E"},
            {"B", "F"},
        ]

        # For every pair of nodes and conditioning set, verify that BFS d-separation
        # matches the definition: d-connected iff at least one simple trail is active.
        for u in all_nodes:
            for v in all_nodes:
                if u >= v:
                    continue
                for z in conditioning_sets:
                    bfs_d_sep = dag.is_d_separated(u, v, z)
                    simple_trails = dag.all_simple_trails(u, v)
                    any_active = any(dag.is_trail_active(t, z) for t in simple_trails)
                    # d-separated means NO trail is active
                    self.assertEqual(
                        bfs_d_sep,
                        not any_active,
                        f"Mismatch for ({u}, {v}) given {z}: BFS says d_sep={bfs_d_sep}, simple_trails active={any_active}",
                    )


if __name__ == "__main__":
    unittest.main()
