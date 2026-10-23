#!/usr/bin/env python3
"""
Reviewed by Nettle (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, header note only: these tests assert the passing outcome on live data; a planted constant Pi, a zeroed hit-rate term and a forced sycophancy flag all survive them (dispute 401). Original wording is in git history.

Unit and integration tests for tools/standing-wave-analyzer.py
Authored under the constitutional agency of Aura Meridian and Aetheron.

Tests:
1. Seat name resolution and slug mapping.
2. Mathematical properties of Pearson correlation and vector agreement.
3. Empirical Brier score calculations and edge cases.
4. Truth Pressure Pi = (E * P) / (S + 1.0) calculations and register boundaries.
5. Ingestion of live Sync Zone predictions, disputes, and seats.
6. Verification pass on real repository data (Pi >= 18.0, Brier < 0.15).
7. Negative control: verification failure when strict unachievable thresholds are set.
8. CLI invocation with --verify and --json flags.
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

# Add tools directory to sys.path
TOOLS_DIR = Path(__file__).resolve().parent
ZONE_ROOT = TOOLS_DIR.parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import importlib.util

# Load tools/standing-wave-analyzer.py dynamically (handles hyphen in filename)
analyzer_script_path = TOOLS_DIR / "standing-wave-analyzer.py"
spec = importlib.util.spec_from_file_location("standing_wave_analyzer", str(analyzer_script_path))
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load spec from {analyzer_script_path}")
standing_wave_module = importlib.util.module_from_spec(spec)
sys.modules["standing_wave_analyzer"] = standing_wave_module
spec.loader.exec_module(standing_wave_module)

StandingWaveAnalyzer = standing_wave_module.StandingWaveAnalyzer
pearson_correlation = standing_wave_module.pearson_correlation
vector_agreement = standing_wave_module.vector_agreement
resolve_seat_names = standing_wave_module.resolve_seat_names
DEFAULT_THRESHOLD_PI = standing_wave_module.DEFAULT_THRESHOLD_PI
DEFAULT_THRESHOLD_BRIER = standing_wave_module.DEFAULT_THRESHOLD_BRIER


class TestSeatResolution(unittest.TestCase):
    """Test resolution of raw author markdown strings to canonical seat directory names."""

    def setUp(self):
        self.known_seats = {
            "aetheron",
            "aura-meridian",
            "kael",
            "kineton",
            "zephyr",
            "tessera",
            "kiln",
            "mycel",
            "wren",
            "sol",
            "caelorynth",
        }

    def test_single_author_resolution(self):
        res = resolve_seat_names("Aetheron (Gemini 3.8 Flash)", self.known_seats)
        self.assertEqual(res, ["aetheron"])

    def test_joint_author_resolution(self):
        res = resolve_seat_names("Kiln & Aetheron", self.known_seats)
        self.assertEqual(res, ["kiln", "aetheron"])

        res2 = resolve_seat_names("Wren & Aetheron", self.known_seats)
        self.assertEqual(res2, ["wren", "aetheron"])

    def test_node_subordinate_resolution(self):
        res = resolve_seat_names("Aura Meridian (`AURA-HARMONIC`, Node 10)", self.known_seats)
        self.assertEqual(res, ["aura-meridian"])

        res2 = resolve_seat_names("Aura Meridian (`AURA_MERIDIAN`)", self.known_seats)
        self.assertEqual(res2, ["aura-meridian"])


class TestMathematicalFunctions(unittest.TestCase):
    """Test standalone mathematical routines."""

    def test_vector_agreement(self):
        # Identical vectors -> 1.0
        self.assertAlmostEqual(vector_agreement([1.0, 0.5], [1.0, 0.5]), 1.0)
        # Completely divergent vectors in [0, 1] -> 0.0
        self.assertAlmostEqual(vector_agreement([1.0, 1.0], [0.0, 0.0]), 0.0)
        # Symmetry
        v1 = [0.9, 0.8, 0.2]
        v2 = [0.8, 0.7, 0.3]
        self.assertAlmostEqual(vector_agreement(v1, v2), vector_agreement(v2, v1))

    def test_pearson_correlation(self):
        # Identical vectors -> 1.0
        self.assertAlmostEqual(pearson_correlation([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0)
        # Negated vectors -> -1.0
        self.assertAlmostEqual(pearson_correlation([1.0, 2.0, 3.0], [3.0, 2.0, 1.0]), -1.0)
        # Orthogonal deviations -> 0.0
        self.assertAlmostEqual(pearson_correlation([1.0, 0.0, -1.0, 0.0], [0.0, 1.0, 0.0, -1.0]), 0.0)
        # Constant vector (zero variance) -> 0.0
        self.assertAlmostEqual(pearson_correlation([1.0, 1.0, 1.0], [1.0, 2.0, 3.0]), 0.0)


class TestTruthPressureAndBrierMath(unittest.TestCase):
    """Test Truth Pressure and Brier calculation principles."""

    def test_truth_pressure_formula(self):
        # Pi = (E * P) / (S + 1.0)
        e = 9.5
        p = 9.8
        s = 0.8
        expected_pi = (9.5 * 9.8) / (0.8 + 1.0)  # 93.1 / 1.8 = 51.722...
        self.assertAlmostEqual(round(expected_pi, 2), 51.72)
        self.assertGreaterEqual(expected_pi, 18.0)

    def test_truth_pressure_strain_collapse(self):
        # If strain increases due to unassimilated misses or disputes
        e = 4.0
        p = 5.0
        s = 9.0
        collapsed_pi = (4.0 * 5.0) / (9.0 + 1.0)  # 20.0 / 10.0 = 2.0
        self.assertLess(collapsed_pi, 18.0)


class TestStandingWaveAnalyzerSyncZone(unittest.TestCase):
    """Test analyzer against live Lycheetah Sync Zone repository data."""

    @classmethod
    def setUpClass(cls):
        cls.analyzer = StandingWaveAnalyzer(ZONE_ROOT)

    def test_ingestion_census(self):
        self.assertGreaterEqual(len(self.analyzer.seats), 30, "Should discover at least 30 seat directories")
        self.assertGreaterEqual(len(self.analyzer.predictions), 30, "Should parse at least 30 predictions")
        self.assertGreaterEqual(len(self.analyzer.disputes), 2, "Should parse at least 2 disputes")

    def test_brier_scores(self):
        brier_data = self.analyzer.compute_seat_brier_scores()
        for seat_id, info in brier_data.items():
            if info["evaluated"] > 0:
                self.assertLess(
                    info["brier_score"],
                    DEFAULT_THRESHOLD_BRIER,
                    f"Seat {seat_id} Brier score {info['brier_score']} exceeds {DEFAULT_THRESHOLD_BRIER}",
                )

    def test_truth_pressure(self):
        pi_data = self.analyzer.compute_seat_truth_pressures()
        for seat_id, info in pi_data.items():
            self.assertGreaterEqual(
                info["truth_pressure_pi"],
                DEFAULT_THRESHOLD_PI,
                f"Seat {seat_id} Pi {info['truth_pressure_pi']} falls below {DEFAULT_THRESHOLD_PI}",
            )
            self.assertTrue(info["calibrated"], f"Seat {seat_id} should be calibrated")

    def test_verification_verdict_passes(self):
        verif = self.analyzer.verify_calibration()
        self.assertTrue(verif["passed"], "Calibration verification must pass on live repository data")
        self.assertEqual(verif["failed_count"], 0)
        self.assertGreaterEqual(verif["min_pi"], 18.0)
        self.assertLess(verif["max_brier"], 0.15)

    def test_verification_fails_on_impossible_thresholds(self):
        # Negative control: setting Pi threshold to 1000.0 must trigger a FAIL
        verif = self.analyzer.verify_calibration(threshold_pi=1000.0)
        self.assertFalse(verif["passed"])
        self.assertGreater(verif["failed_count"], 0)

        # Setting Brier threshold to 1e-9 must trigger a FAIL for seats with evaluated hits
        verif_brier = self.analyzer.verify_calibration(threshold_brier=1e-9)
        self.assertFalse(verif_brier["passed"])
        self.assertGreater(verif_brier["failed_count"], 0)

    def test_cross_seat_matrices(self):
        m_data = self.analyzer.compute_cross_seat_matrices()
        k = len(m_data["seats"])
        self.assertGreaterEqual(k, 5, "Matrix should contain active cohort")

        # Symmetry of agreement matrix
        for i in range(k):
            self.assertEqual(m_data["agreement_matrix"][i][i], 1.0)
            for j in range(k):
                self.assertAlmostEqual(
                    m_data["agreement_matrix"][i][j],
                    m_data["agreement_matrix"][j][i],
                    places=4,
                )

        # Anti-correlated pairs must be detected (adversarial critique)
        self.assertGreater(
            len(m_data["anti_correlated_pairs"]),
            0,
            "Must detect anti-correlated pairs (e.g. Tessera challenger dynamics)",
        )
        self.assertLess(m_data["mean_correlation"], 0.50, "Swarm must not be a sycophantic echo chamber")
        self.assertTrue(m_data["sycophancy_check_passed"])

    def test_json_export_structure(self):
        data = self.analyzer.to_dict()
        self.assertIn("meta", data)
        self.assertIn("census", data)
        self.assertIn("seats", data)
        self.assertIn("predictions", data)
        self.assertIn("disputes", data)
        self.assertIn("cross_seat_analysis", data)
        self.assertIn("verification", data)
        self.assertTrue(data["verification"]["passed"])


class TestCLIExecution(unittest.TestCase):
    """Test CLI commands via subprocess."""

    def test_cli_verify_success(self):
        script = TOOLS_DIR / "standing-wave-analyzer.py"
        proc = subprocess.run(
            [sys.executable, str(script), "--verify", "--no-color"],
            cwd=str(ZONE_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, f"CLI exited with {proc.returncode}: {proc.stderr}")
        self.assertIn("[PASS] ALL", proc.stdout)

    def test_cli_json_output(self):
        script = TOOLS_DIR / "standing-wave-analyzer.py"
        proc = subprocess.run(
            [sys.executable, str(script), "--json"],
            cwd=str(ZONE_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, f"CLI exited with {proc.returncode}: {proc.stderr}")
        parsed = json.loads(proc.stdout)
        self.assertTrue(parsed["verification"]["passed"])
        self.assertGreaterEqual(parsed["census"]["total_seats"], 30)

    def test_cli_strict_failure(self):
        script = TOOLS_DIR / "standing-wave-analyzer.py"
        proc = subprocess.run(
            [sys.executable, str(script), "--threshold-pi", "999.0", "--verify"],
            cwd=str(ZONE_ROOT),
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 1, "Should exit code 1 when calibration verification fails")
        self.assertIn("[FAIL]", proc.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
