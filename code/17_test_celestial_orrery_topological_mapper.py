#!/usr/bin/env python3
"""
Unit Test Suite for Celestial Orrery Topological Mapper & Ergodic Engine
Author: Aetheron & Orrery
Date: 2026-11-03
Status: 7 Automated Tests
"""

import unittest
import json
import math
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

from importlib import import_module
engine_module = import_module("16_celestial_orrery_topological_mapper")
CelestialOrreryMapper = engine_module.CelestialOrreryMapper
STANDARD_DOMAINS = engine_module.STANDARD_DOMAINS
DOMAIN_FREQUENCIES = engine_module.DOMAIN_FREQUENCIES

class TestCelestialOrreryTopologicalMapper(unittest.TestCase):

    def setUp(self):
        # Resolve sync zone root
        self.root_path = Path(__file__).resolve().parent.parent
        self.mapper = CelestialOrreryMapper(str(self.root_path))
        self.seats = self.mapper.discover_seats()

    def test_01_seat_discovery(self):
        self.assertGreaterEqual(len(self.seats), 80, "Expected at least 80 active seats on disk")
        self.assertIn("aetheron", self.seats)
        self.assertIn("kaitiaki", self.seats)
        self.assertIn("tiriti", self.seats)
        self.assertIn("matauranga", self.seats)

    def test_02_domain_mapping_exhaustion(self):
        for seat in self.seats:
            domain = self.mapper.map_seat_to_domain(seat)
            self.assertIn(domain, STANDARD_DOMAINS, f"Seat {seat} mapped to invalid domain: {domain}")

    def test_03_celestial_coordinates_geometry(self):
        coords = self.mapper.compute_celestial_coordinates(self.seats, center=(500.0, 500.0))
        self.assertEqual(len(coords["domain_hubs"]), 10)
        self.assertEqual(len(coords["seat_nodes"]), len(self.seats))

        for dom, hub in coords["domain_hubs"].items():
            self.assertTrue(math.isfinite(hub["x"]))
            self.assertTrue(math.isfinite(hub["y"]))
            self.assertGreater(hub["frequency"], 100.0)

        for seat_id, node in coords["seat_nodes"].items():
            self.assertTrue(math.isfinite(node["x"]))
            self.assertTrue(math.isfinite(node["y"]))
            self.assertGreater(node["base_frequency"], 100.0)

    def test_04_domain_frequencies_modal_scale(self):
        freqs = list(DOMAIN_FREQUENCIES.values())
        self.assertEqual(len(freqs), 10)
        # Verify strictly monotonically ascending frequencies
        for i in range(len(freqs) - 1):
            self.assertLess(freqs[i], freqs[i+1], f"Domain frequency inversion at index {i}")

    def test_05_embedding_stress_bound(self):
        coords = self.mapper.compute_celestial_coordinates(self.seats)
        stress = self.mapper.compute_embedding_stress(coords["seat_nodes"])
        self.assertTrue(math.isfinite(stress))
        self.assertLess(stress, 2.0, f"Embedding stress {stress} exceeds tolerance")

    def test_06_ergodic_drift_gap_detection(self):
        res = self.mapper.evaluate_ergodic_drift(ensemble_size=300, timesteps=100)
        self.assertTrue(res["is_non_ergodic"])
        self.assertEqual(res["conclusion"], "NON_ERGODIC_SYSTEM")
        self.assertGreater(res["theoretical_ensemble_growth"], res["theoretical_time_growth"])
        self.assertGreater(res["empirical_ensemble_mean"], res["empirical_time_mean"])

    def test_07_full_serialization_json(self):
        coords = self.mapper.compute_celestial_coordinates(self.seats)
        serialized = json.dumps(coords, indent=2)
        parsed = json.loads(serialized)
        self.assertEqual(parsed["total_seats"], len(self.seats))
        self.assertEqual(parsed["total_domains"], 10)

if __name__ == "__main__":
    unittest.main()
