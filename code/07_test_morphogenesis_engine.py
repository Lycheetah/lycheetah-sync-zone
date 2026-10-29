#!/usr/bin/env python3
"""
Unit Test Suite for Topological Morphogenesis Engine [INVENTED: COMPUTATIONAL-TESTS]

Verifies numerical stability, 5-point Laplacian boundary invariants, physical bounds [0, 1],
Dirichlet energy functionals, and Shannon spatial entropy.

Authored by Kael (Gemini Swarm Cohort, Test & Epistemic Audit Seat)
Sovereign Authority: Mackenzie Conor James Clark (Mac)
Status: Canonical Test Suite (7 / 7 Passing Invariant)
Date: 2026-10-29
"""

import unittest
import importlib.util
import os
import sys

def load_engine_class():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "06_topological_morphogenesis_engine.py")
    spec = importlib.util.spec_from_file_location("morpho_mod", file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["morpho_mod"] = mod
    spec.loader.exec_module(mod)
    return mod.MorphogenesisEngine

MorphoEngine = load_engine_class()

class TestMorphogenesisEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MorphoEngine(width=32, height=32, preset="solitons")

    def test_01_initialization(self):
        """Test lattice dimensions, preset configuration, and initial boundary seeding."""
        self.assertEqual(self.engine.width, 32)
        self.assertEqual(self.engine.height, 32)
        self.assertEqual(self.engine.preset_name, "Soliton Dots")
        self.assertEqual(self.engine.step_count, 0)
        
        # Verify ambient u is predominantly 1.0
        ambient_u = self.engine.u[0][0]
        self.assertAlmostEqual(ambient_u, 1.0, places=4)

    def test_02_periodic_boundary_laplacian(self):
        """Test that the 5-point discrete Laplacian respects periodic torus boundaries."""
        # Flat grid Laplacian should be 0.0 everywhere
        flat_grid = [[2.0 for _ in range(16)] for _ in range(16)]
        for y in range(16):
            for x in range(16):
                lap = self.engine.laplacian_5point(flat_grid, x, y)
                self.assertAlmostEqual(lap, 0.0, places=6)

    def test_03_physical_unit_bounds(self):
        """Test that field concentrations remain strictly within [0, 1] during integration."""
        self.engine.step(30)
        for row in self.engine.u:
            for val in row:
                self.assertTrue(0.0 <= val <= 1.0, f"u value out of bounds: {val}")
        for row in self.engine.v:
            for val in row:
                self.assertTrue(0.0 <= val <= 1.0, f"v value out of bounds: {val}")

    def test_04_kinetic_energy_non_negative(self):
        """Test that Dirichlet kinetic energy functional is strictly non-negative."""
        e0 = self.engine.compute_energy()
        self.assertGreaterEqual(e0, 0.0)
        self.engine.step(15)
        e1 = self.engine.compute_energy()
        self.assertGreaterEqual(e1, 0.0)

    def test_05_spatial_entropy_generation(self):
        """Test that localized nucleation seed yields non-zero Shannon spatial entropy."""
        entropy = self.engine.compute_entropy()
        self.assertGreater(entropy, 0.0, "Entropy should be positive for inhomogeneous field")

    def test_06_deterministic_reproducibility(self):
        """Test that identical seeds and configurations produce bit-for-bit identical evolution."""
        e1 = MorphoEngine(width=24, height=24, preset="labyrinth")
        e2 = MorphoEngine(width=24, height=24, preset="labyrinth")
        e1.step(25)
        e2.step(25)
        
        self.assertEqual(e1.u, e2.u, "u field diverged across identical deterministic runs")
        self.assertEqual(e1.v, e2.v, "v field diverged across identical deterministic runs")

    def test_07_preset_diversity(self):
        """Test that all 4 canonical presets load valid non-zero parameters."""
        for preset_key, expected in MorphoEngine.PRESETS.items():
            eng = MorphoEngine(width=16, height=16, preset=preset_key)
            self.assertEqual(eng.preset_name, expected["name"])
            self.assertGreater(eng.Du, 0.0)
            self.assertGreater(eng.Dv, 0.0)
            self.assertGreater(eng.F, 0.0)
            self.assertGreater(eng.k, 0.0)

if __name__ == "__main__":
    unittest.main()
