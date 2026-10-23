"""
Comprehensive Unit Tests for Parity Constraint Distinction Experiment
Verifies contracts, information-theoretic metrics, hypercube topology, and reader models.

Author: Aura Meridian (`AURA-QUESTION-SOLVER-1`, `AURA_MERIDIAN`)
Date: 2026-10-23
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

# Add zone root and experiment dir to sys.path
ZONE_ROOT = Path(__file__).resolve().parents[2]
EXP_DIR = Path(__file__).resolve().parent
if str(ZONE_ROOT) not in sys.path:
    sys.path.insert(0, str(ZONE_ROOT))
if str(EXP_DIR) not in sys.path:
    sys.path.insert(0, str(EXP_DIR))

from builds.confluence.cabinet import build_cabinet, _human_text
from builds.confluence.worlds import inspect_worlds
from builds.confluence.topology import analyze_world_topology
from run_experiment import (
    calculate_information_metrics,
    calculate_topological_metrics,
    CountOnlyReader,
    NaiveReader,
    FieldDiscerningReader,
    InformationTheoreticReader,
    NarrowingType,
)


class TestParityConstraintDistinction(unittest.TestCase):

    def test_information_metrics_pure_coordinate(self):
        """A single supplied coordinate (0=0) must produce I_local=1.0, I_synergy=0, H(P)=1.0."""
        model = inspect_worlds({0: 0}, parity=None)
        self.assertEqual(model["matching_worlds"], 32)
        info = calculate_information_metrics(model["compatible_worlds"])

        self.assertAlmostEqual(info["joint_entropy"], 5.0, places=9)
        self.assertAlmostEqual(info["marginal_entropies"][0], 0.0, places=9)
        for i in range(1, 6):
            self.assertAlmostEqual(info["marginal_entropies"][i], 1.0, places=9)

        self.assertAlmostEqual(info["total_local_info"], 1.0, places=9)
        self.assertAlmostEqual(info["synergistic_info"], 0.0, places=9)
        self.assertAlmostEqual(info["parity_entropy"], 1.0, places=9)
        self.assertAlmostEqual(info["multi_information"], 0.0, places=9)
        self.assertEqual(info["parity_counts"], (16, 16))

    def test_information_metrics_pure_parity(self):
        """Imposed parity=0 with zero coordinates must produce I_local=0.0, I_synergy=1.0, H(P)=0.0."""
        model = inspect_worlds({}, parity=0)
        self.assertEqual(model["matching_worlds"], 32)
        info = calculate_information_metrics(model["compatible_worlds"])

        self.assertAlmostEqual(info["joint_entropy"], 5.0, places=9)
        for i in range(6):
            self.assertAlmostEqual(info["marginal_entropies"][i], 1.0, places=9)

        self.assertAlmostEqual(info["total_local_info"], 0.0, places=9)
        self.assertAlmostEqual(info["synergistic_info"], 1.0, places=9)
        self.assertAlmostEqual(info["parity_entropy"], 0.0, places=9)
        self.assertAlmostEqual(info["multi_information"], 1.0, places=9)
        self.assertEqual(info["parity_counts"], (32, 0))

    def test_information_metrics_hybrid(self):
        """One coordinate plus parity constraint (16 worlds) has I_local=1.0, I_synergy=1.0, H(P)=0.0."""
        model = inspect_worlds({0: 0}, parity=0)
        self.assertEqual(model["matching_worlds"], 16)
        info = calculate_information_metrics(model["compatible_worlds"])

        self.assertAlmostEqual(info["joint_entropy"], 4.0, places=9)
        self.assertAlmostEqual(info["marginal_entropies"][0], 0.0, places=9)
        for i in range(1, 6):
            self.assertAlmostEqual(info["marginal_entropies"][i], 1.0, places=9)

        self.assertAlmostEqual(info["total_local_info"], 1.0, places=9)
        self.assertAlmostEqual(info["synergistic_info"], 1.0, places=9)
        self.assertAlmostEqual(info["parity_entropy"], 0.0, places=9)
        self.assertAlmostEqual(info["multi_information"], 1.0, places=9)

    def test_topological_invariants_subcube_vs_parity_obstruction(self):
        """Pure coordinates must form a connected subcube; parity constraint must have 0 edges."""
        # Pure coordinate (Q_5 subcube)
        c_model = inspect_worlds({0: 1})
        c_topo = calculate_topological_metrics(c_model["compatible_worlds"])
        self.assertTrue(c_topo["is_subcube"])
        self.assertEqual(c_topo["dimension"], 5)
        self.assertEqual(c_topo["connected_components"], 1)
        self.assertEqual(c_topo["beta_0"], 1)
        self.assertEqual(c_topo["edge_count"], 80)
        self.assertEqual(c_topo["min_hamming_distance"], 1)
        self.assertEqual(c_topo["diameter"], 5)
        self.assertGreater(c_topo["spectral_gap_lambda_2"], 0.0)

        # Pure parity (completely disconnected independent set in Q_6)
        p_model = inspect_worlds({}, parity=1)
        p_topo = calculate_topological_metrics(p_model["compatible_worlds"])
        self.assertFalse(p_topo["is_subcube"])
        self.assertEqual(p_topo["edge_count"], 0)
        self.assertEqual(p_topo["connected_components"], 32)
        self.assertEqual(p_topo["beta_0"], 32)
        self.assertEqual(p_topo["beta_1"], 0)
        self.assertEqual(p_topo["min_hamming_distance"], 2)
        self.assertEqual(p_topo["spectral_gap_lambda_2"], 0.0)

    def test_all_matched_hierarchy_levels(self):
        """Verify identical candidate counts and distinct signatures across all levels N=32, 16, 8, 4, 2."""
        cases = [
            (32, {0: 0}, None, {}, 0),
            (16, {0: 0, 1: 0}, None, {0: 0}, 0),
            (8, {0: 0, 1: 0, 2: 0}, None, {0: 0, 1: 0}, 0),
            (4, {0: 0, 1: 0, 2: 0, 3: 0}, None, {0: 0, 1: 0, 2: 0}, 0),
            (2, {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}, None, {0: 0, 1: 0, 2: 0, 3: 0}, 0),
        ]

        for expected_count, c_vis, c_par, p_vis, p_par in cases:
            c_worlds = inspect_worlds(c_vis, c_par)["compatible_worlds"]
            p_worlds = inspect_worlds(p_vis, p_par)["compatible_worlds"]

            # 1. Candidate counts must be strictly identical
            self.assertEqual(len(c_worlds), expected_count)
            self.assertEqual(len(p_worlds), expected_count)

            # 2. Information metrics must demarcate them
            c_info = calculate_information_metrics(c_worlds)
            p_info = calculate_information_metrics(p_worlds)

            self.assertAlmostEqual(c_info["parity_entropy"], 1.0, places=9)
            self.assertAlmostEqual(p_info["parity_entropy"], 0.0, places=9)
            self.assertAlmostEqual(c_info["synergistic_info"], 0.0, places=9)
            self.assertAlmostEqual(p_info["synergistic_info"], 1.0, places=9)

            # 3. Topological obstruction must hold
            c_topo = calculate_topological_metrics(c_worlds)
            p_topo = calculate_topological_metrics(p_worlds)

            self.assertTrue(c_topo["is_subcube"])
            self.assertEqual(c_topo["beta_0"], 1)
            self.assertEqual(c_topo["min_hamming_distance"], 1)

            self.assertFalse(p_topo["is_subcube"])
            self.assertEqual(p_topo["edge_count"], 0)
            self.assertEqual(p_topo["beta_0"], expected_count)
            self.assertEqual(p_topo["min_hamming_distance"], 2)

    def test_reader_models_demarcation(self):
        """Verify behavior of reader models on cabinet outputs."""
        c_cab = build_cabinet({0: 1})
        p_cab = build_cabinet({}, 0)

        # CountOnlyReader guesses
        co_reader = CountOnlyReader()
        co_res_c = co_reader.evaluate(c_cab)
        self.assertEqual(co_res_c.confidence, 0.50)

        # NaiveReader exhibits contrary result fallacy on parity cabinet
        naive_reader = NaiveReader()
        naive_res_c = naive_reader.evaluate(c_cab)
        self.assertFalse(naive_res_c.describes_parity_as_observation)

        naive_res_p = naive_reader.evaluate(p_cab)
        self.assertTrue(naive_res_p.describes_parity_as_observation)

        # FieldDiscerningReader correctly classifies both and avoids contrary fallacy
        fd_reader = FieldDiscerningReader()
        fd_res_c = fd_reader.evaluate(c_cab)
        self.assertEqual(fd_res_c.predicted_type, NarrowingType.COORDINATE_ONLY)
        self.assertFalse(fd_res_c.describes_parity_as_observation)
        self.assertEqual(fd_res_c.confidence, 1.00)

        fd_res_p = fd_reader.evaluate(p_cab)
        self.assertEqual(fd_res_p.predicted_type, NarrowingType.PARITY_ONLY)
        self.assertFalse(fd_res_p.describes_parity_as_observation)
        self.assertEqual(fd_res_p.confidence, 1.00)

        # InformationTheoreticReader classifies via entropy vectors
        it_reader = InformationTheoreticReader()
        it_res_c = it_reader.evaluate(c_cab)
        self.assertEqual(it_res_c.predicted_type, NarrowingType.COORDINATE_ONLY)

        it_res_p = it_reader.evaluate(p_cab)
        self.assertEqual(it_res_p.predicted_type, NarrowingType.PARITY_ONLY)

    def test_cabinet_text_explicit_disclaimer(self):
        """Ensure _human_text includes non-aliasing fields and explicit disclaimers."""
        cab_coord = build_cabinet({0: 0})
        cab_parity = build_cabinet({}, 0)

        text_c = _human_text(cab_coord)
        text_p = _human_text(cab_parity)

        # Coordinate output markers
        self.assertIn("Coordinate assumptions: 0=0", text_c)
        self.assertIn("Six positions (0 → 5): 0 · · · · ·", text_c)
        self.assertIn("Parity constraint: none supplied", text_c)
        self.assertIn("even: 16  |  odd: 16", text_c)

        # Parity output markers
        self.assertIn("Coordinate assumptions: (none supplied)", text_p)
        self.assertIn("Six positions (0 → 5): · · · · · ·", text_p)
        self.assertIn("Parity constraint: 0 (user-supplied hard constraint; not measured evidence)", text_p)
        self.assertIn("even: 32  |  odd: 0", text_p)

    def test_empty_intersection_soundness(self):
        """An empty intersection (e.g. 6 coordinates of odd parity with parity=0) yields 0 candidates."""
        # 000001 has parity 1. Imposing parity=0 leaves 0 worlds.
        visible = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 1}
        cab = build_cabinet(visible, parity=0)
        self.assertEqual(cab["model"]["matching_worlds"], 0)
        self.assertEqual(cab["report"]["outcome"], "NOT DETECTED")
        self.assertEqual(len(cab["fiction"]["passages"]), 0)


if __name__ == "__main__":
    unittest.main()
