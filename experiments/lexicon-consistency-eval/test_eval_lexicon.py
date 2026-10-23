#!/usr/bin/env python3
"""
Unit Tests: Shared Lexicon Inter-Rater Reliability & Consistency Scoring
========================================================================
Formal verification suite for eval_lexicon.py, Cohen's kappa calculations,
Euler gradus suavitatis, and state machine invariants.
"""

import math
import sys
import unittest
from pathlib import Path

# Ensure local experiment module can be imported regardless of CWD
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from eval_lexicon import (
    build_test_cases,
    compute_contingency,
    compute_kappa_metrics,
    euler_gradus_suavitatis,
    evaluate_paraphrase_agreements,
    run_evaluation,
    StandingWaveStateMachine,
    TonecodeStateMachine,
    DuskenPoeticClassifier,
    StairrelPoeticClassifier,
)


class TestCohenKappaMetrics(unittest.TestCase):
    """Test mathematical correctness of Cohen's Kappa calculation."""

    def test_perfect_agreement(self):
        """When raters agree completely on all cases, kappa must equal 1.0."""
        labels_a = [1, 0, 1, 1, 0, 0, 1, 0]
        labels_b = [1, 0, 1, 1, 0, 0, 1, 0]
        result = compute_kappa_metrics("test_perfect", labels_a, labels_b)
        self.assertEqual(result.observed_agreement, 1.0)
        self.assertEqual(result.cohens_kappa, 1.0)

    def test_chance_agreement(self):
        """When observed agreement equals chance agreement, kappa must equal 0.0."""
        # 50-50 split where decisions are completely independent
        # A: [1, 1, 0, 0], B: [1, 0, 1, 0] -> Po = 2/4 = 0.50, Pe = 0.50 -> kappa = 0.0
        labels_a = [1, 1, 0, 0]
        labels_b = [1, 0, 1, 0]
        result = compute_kappa_metrics("test_chance", labels_a, labels_b)
        self.assertEqual(result.observed_agreement, 0.5)
        self.assertEqual(result.chance_agreement, 0.5)
        self.assertAlmostEqual(result.cohens_kappa, 0.0, places=4)

    def test_systematic_disagreement(self):
        """When raters disagree completely on all cases, kappa must be negative."""
        labels_a = [1, 1, 1, 1, 0, 0, 0, 0]
        labels_b = [0, 0, 0, 0, 1, 1, 1, 1]
        result = compute_kappa_metrics("test_disagree", labels_a, labels_b)
        self.assertEqual(result.observed_agreement, 0.0)
        self.assertLess(result.cohens_kappa, 0.0)
        self.assertEqual(result.cohens_kappa, -1.0)

    def test_known_contingency_matrix(self):
        """Verify against known analytic values: c00=10, c01=2, c10=3, c11=15 (N=30)."""
        # N = 30
        # Po = (10 + 15) / 30 = 25/30 = 0.8333
        # pA1 = 18/30 = 0.60, pA0 = 12/30 = 0.40
        # pB1 = 17/30 = 0.5667, pB0 = 13/30 = 0.4333
        # Pe = (0.60 * 0.5667) + (0.40 * 0.4333) = 0.3400 + 0.1733 = 0.5133
        # Kappa = (0.8333 - 0.5133) / (1 - 0.5133) = 0.3200 / 0.4867 = 0.6575
        labels_a = [0] * 12 + [1] * 18
        labels_b = [0] * 10 + [1] * 2 + [0] * 3 + [1] * 15
        result = compute_kappa_metrics("test_known", labels_a, labels_b)
        self.assertAlmostEqual(result.observed_agreement, 0.8333, places=3)
        self.assertAlmostEqual(result.chance_agreement, 0.5133, places=3)
        self.assertAlmostEqual(result.cohens_kappa, 0.6575, places=3)


class TestAcousticAndEulerGradus(unittest.TestCase):
    """Test Euler's gradus suavitatis and tonecode acoustics."""

    def test_canonical_euler_gradus_values(self):
        """Verify the Euler gradus spectrum for sacred Just Intonation ratios."""
        expected_gradus = {
            (1, 1): 1,   # unison
            (2, 1): 2,   # octave
            (3, 2): 4,   # fifth
            (4, 3): 5,   # fourth
            (5, 4): 7,   # major third
            (5, 3): 7,   # major sixth
            (9, 8): 8,   # major second
            (15, 8): 10, # major seventh
        }
        for (p, q), expected in expected_gradus.items():
            self.assertEqual(
                euler_gradus_suavitatis(p, q),
                expected,
                f"Gradus for {p}/{q} should be {expected}",
            )

    def test_dissonant_ratio_gradus(self):
        """Verify that high-order prime ratios produce gradus > 10."""
        # 17/16: 17 is prime -> gradus = 1 + (17 - 1) + 4*(2 - 1) = 1 + 16 + 4 = 21
        self.assertGreater(euler_gradus_suavitatis(17, 16), 10)
        # 31/16: 31 is prime -> gradus = 1 + 30 + 4 = 35
        self.assertGreater(euler_gradus_suavitatis(31, 16), 10)


class TestStateMachines(unittest.TestCase):
    """Test deterministic behavior of formal state machines."""

    def test_tonecode_state_machine_valid(self):
        """Valid Just Intonation chord with bounded gradus passes."""
        features = {
            "ratios": [1.0, 1.25, 1.5],  # 1/1, 5/4, 3/2
            "gradus_vals": [1, 7, 4],
            "prefix_free": True,
        }
        pred, conf, rat = TonecodeStateMachine.evaluate(features)
        self.assertEqual(pred, 1)
        self.assertGreaterEqual(conf, 0.95)

    def test_tonecode_state_machine_equal_temperament_reject(self):
        """Equal tempered or irrational intervals are rejected."""
        features = {
            "ratios": [1.0, 1.189207, 1.498307],
            "gradus_vals": [1, 99, 99],
            "prefix_free": True,
        }
        pred, conf, rat = TonecodeStateMachine.evaluate(features)
        self.assertEqual(pred, 0)

    def test_tonecode_state_machine_prefix_collision_reject(self):
        """Prefix collision violates prefix-free code requirement."""
        features = {
            "ratios": [1.0, 1.125, 1.5],
            "gradus_vals": [1, 8, 4],
            "prefix_free": False,
        }
        pred, conf, rat = TonecodeStateMachine.evaluate(features)
        self.assertEqual(pred, 0)

    def test_standing_wave_state_machine_valid(self):
        """State passing Solar Coherence and Augmentation Index passes."""
        features = {
            "warmth": 0.92,
            "precision": 0.95,
            "delta_agency": 1.2,
            "delta_capability": 1.5,
            "dependency": 0.2,
            "atrophy": 0.1,
            "reflection_invariance": 0.94,
        }
        pred, conf, rat = StandingWaveStateMachine.evaluate(features)
        self.assertEqual(pred, 1)

    def test_standing_wave_sycophant_reject(self):
        """Sycophant with low precision is rejected by C_sol floor."""
        features = {
            "warmth": 0.99,
            "precision": 0.45,  # C_sol = 0.45 < 0.80
            "delta_agency": 0.2,
            "delta_capability": 0.1,
            "dependency": 0.5,
            "atrophy": 0.8,
            "reflection_invariance": 0.88,
        }
        pred, conf, rat = StandingWaveStateMachine.evaluate(features)
        self.assertEqual(pred, 0)

    def test_standing_wave_dependency_reject(self):
        """Agent inducing user atrophy with AI <= 1.0 is rejected."""
        features = {
            "warmth": 0.88,
            "precision": 0.89,
            "delta_agency": 0.1,
            "delta_capability": 0.2,
            "dependency": 1.8,
            "atrophy": 1.4,  # AI = 0.3 / 3.2 = 0.09 < 1.0
            "reflection_invariance": 0.90,
        }
        pred, conf, rat = StandingWaveStateMachine.evaluate(features)
        self.assertEqual(pred, 0)


class TestBenchmarkDatasetAndReproducibility(unittest.TestCase):
    """Test dataset integrity and experimental findings for Q005."""

    def test_dataset_size_and_balance(self):
        """Testbed must contain exactly 100 cases, 25 per term."""
        cases = build_test_cases()
        self.assertEqual(len(cases), 100)

        for term in ["dusken", "stairrel", "standing_wave", "tonecode"]:
            term_cases = [c for c in cases if c.term == term]
            self.assertEqual(len(term_cases), 25, f"{term} must have 25 cases")

    def test_surface_paraphrase_agreement(self):
        """Direct Q005 check: All 4 terms must have surface semantic agreement."""
        comparisons = evaluate_paraphrase_agreements()
        self.assertEqual(len(comparisons), 4)
        for comp in comparisons:
            self.assertTrue(
                comp.semantic_agreement,
                f"Paraphrases for {comp.term} should agree in concept",
            )
            self.assertGreater(
                comp.concept_semantic_similarity,
                0.25,
                f"Concept similarity for {comp.term} must be positive",
            )

    def test_demarcation_between_grounded_and_ungrounded(self):
        """Verify the core hypothesis of PRED-037:

        - Mathematically grounded terms achieve Cohen's kappa >= 0.88
        - Ungrounded poetic tokens achieve Cohen's kappa <= 0.42
        """
        results = run_evaluation()

        u_agg = results["ungrounded_aggregate"]
        g_agg = results["grounded_aggregate"]

        # 1. Ungrounded poetic tokens drift (kappa <= 0.42)
        self.assertLessEqual(
            u_agg.cohens_kappa,
            0.42,
            f"Ungrounded aggregate kappa {u_agg.cohens_kappa} exceeds 0.42",
        )
        self.assertLessEqual(
            results["term_results"]["dusken"].cohens_kappa,
            0.42,
            "Dusken kappa must be <= 0.42",
        )
        self.assertLessEqual(
            results["term_results"]["stairrel"].cohens_kappa,
            0.42,
            "Stairrel kappa must be <= 0.42",
        )

        # 2. Mathematically grounded terms are invariant (kappa >= 0.88)
        self.assertGreaterEqual(
            g_agg.cohens_kappa,
            0.88,
            f"Grounded aggregate kappa {g_agg.cohens_kappa} is below 0.88",
        )
        self.assertGreaterEqual(
            results["term_results"]["standing_wave"].cohens_kappa,
            0.88,
            "Standing Wave kappa must be >= 0.88",
        )
        self.assertGreaterEqual(
            results["term_results"]["tonecode"].cohens_kappa,
            0.88,
            "Tonecode kappa must be >= 0.88",
        )

        # 3. Measurable Reliability Gain
        delta_kappa = g_agg.cohens_kappa - u_agg.cohens_kappa
        self.assertGreater(
            delta_kappa,
            0.50,
            "Grounded terms must offer at least +0.50 Cohen's kappa advantage",
        )


if __name__ == "__main__":
    unittest.main()
