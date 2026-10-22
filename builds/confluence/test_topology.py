"""Test suite for topology.py contract and hypercube subgraph invariants."""

from pathlib import Path
import sys
import unittest

ZONE_ROOT = Path(__file__).resolve().parents[2]
if str(ZONE_ROOT) not in sys.path:
    sys.path.insert(0, str(ZONE_ROOT))

from builds.confluence.worlds import inspect_worlds
from builds.confluence.topology import analyze_world_topology


class TestWorldTopology(unittest.TestCase):
    def test_empty_worlds(self):
        res = analyze_world_topology([])
        self.assertEqual(res["vertex_count"], 0)
        self.assertEqual(res["beta_0"], 0)
        self.assertEqual(res["beta_1"], 0)
        self.assertFalse(res["is_subcube"])

    def test_full_hypercube_q6(self):
        # Inspect worlds with zero observations -> all 64 worlds
        w_data = inspect_worlds({})
        res = analyze_world_topology(w_data["compatible_worlds"])
        self.assertEqual(res["vertex_count"], 64)
        # In Q_6: |E| = d * 2^(d-1) = 6 * 32 = 192
        self.assertEqual(res["edge_count"], 192)
        self.assertEqual(res["beta_0"], 1)
        # beta_1 = 192 - 64 + 1 = 129
        self.assertEqual(res["beta_1"], 129)
        self.assertEqual(res["diameter"], 6)
        self.assertTrue(res["is_subcube"])
        self.assertEqual(res["dimension"], 6)

    def test_single_fixed_coordinate_q5(self):
        # 1 observation fixed -> 32 worlds, dimension 5 subcube
        w_data = inspect_worlds({0: 1})
        res = analyze_world_topology(w_data["compatible_worlds"])
        self.assertEqual(res["vertex_count"], 32)
        # In Q_5: |E| = 5 * 16 = 80
        self.assertEqual(res["edge_count"], 80)
        self.assertEqual(res["beta_0"], 1)
        self.assertEqual(res["beta_1"], 80 - 32 + 1)
        self.assertEqual(res["diameter"], 5)
        self.assertTrue(res["is_subcube"])
        self.assertEqual(res["dimension"], 5)

    def test_parity_constraint_breaks_connectivity(self):
        # Parity constraint keeps only even or odd worlds
        # Any two even worlds have Hamming distance >= 2.
        # Thus edge count must be 0, and beta_0 == vertex_count!
        w_data = inspect_worlds({}, parity=0)
        res = analyze_world_topology(w_data["compatible_worlds"])
        self.assertEqual(res["vertex_count"], 32)
        self.assertEqual(res["edge_count"], 0)
        self.assertEqual(res["beta_0"], 32)
        self.assertEqual(res["beta_1"], 0)
        self.assertFalse(res["is_subcube"])


if __name__ == "__main__":
    unittest.main()
