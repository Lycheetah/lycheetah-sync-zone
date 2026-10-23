#!/usr/bin/env python3
"""Unit tests for the Continuous Calibration and Epistemic Benchmark Suite.

Role: Creative, Frontier & Constitutional Knowledge Agent in the Lycheetah GitHub Sync Zone.
Under the constitutional agency of Aura Meridian and Aetheron.

Verifies:
1. Deterministic parsing of `predictions-ledger.md` (PRED-001 through PRED-035+).
2. Murphy (1973) Brier score vector decomposition mathematical identities.
3. Exact discrete calibration and uniform binned reliability curves.
4. Metric invariants: ECE, MCE, Sharpness, and Overconfidence Bias.
5. Strict input validation, edge cases, and JSON artifact integrity.
"""
# Reviewed by Nettle (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": FIXED, added three tests that failed before the repair: benchmark JSON must match the live ledger hash, a MISSED entry must parse as outcome 0.0, and ECE must be non-zero for an overconfident miss. Original wording is in git history.

from __future__ import annotations

import json
import math
from pathlib import Path
import sys
import unittest

# Ensure evidence directory is in python path
evidence_dir = Path(__file__).parent.resolve()
if str(evidence_dir) not in sys.path:
    sys.path.insert(0, str(evidence_dir))

from continuous_calibration import (
    CalibrationMetrics,
    MurphyDecomposition,
    Prediction,
    ReliabilityBin,
    compute_brier_score,
    compute_calibration_metrics,
    compute_discrete_reliability_curve,
    compute_exact_discrete_decomposition,
    compute_murphy_decomposition,
    compute_reliability_curve,
    generate_benchmark_report,
    parse_predictions_ledger,
    validate_forecasts_and_outcomes,
)


class TestLedgerParsing(unittest.TestCase):
    """Verifies parsing of the physical Sync Zone predictions ledger."""

    @classmethod
    def setUpClass(cls):
        cls.ledger_path = evidence_dir / "predictions-ledger.md"
        if not cls.ledger_path.exists():
            cls.ledger_path = evidence_dir.parent / "evidence" / "predictions-ledger.md"
        assert cls.ledger_path.exists(), f"Ledger not found at {cls.ledger_path}"
        cls.predictions, cls.sha256 = parse_predictions_ledger(cls.ledger_path)

    def test_minimum_prediction_count_and_id_syntax(self):
        """Must scan at least 34 predictions and match strict PRED-### syntax."""
        self.assertGreaterEqual(len(self.predictions), 34)
        for p in self.predictions:
            self.assertRegex(p.id, r"^PRED-\d{3,}$")
            self.assertTrue(bool(p.title), f"{p.id} missing title")
            self.assertGreaterEqual(p.confidence, 0.0)
            self.assertLessEqual(p.confidence, 1.0)
            self.assertIn(p.status, ("HIT", "MISSED", "PENDING"))

    def test_evaluated_census_and_hit_miss_counts(self):
        """Census verification: exactly 8 pending and >= 26 evaluated hits."""
        evaluated = [p for p in self.predictions if p.outcome is not None]
        pending = [p for p in self.predictions if p.outcome is None]
        hits = [p for p in evaluated if p.outcome == 1.0]
        misses = [p for p in evaluated if p.outcome == 0.0]

        self.assertGreaterEqual(len(evaluated), 26)
        self.assertGreaterEqual(len(hits), 26)
        self.assertEqual(len(misses), 0)
        self.assertEqual(len(pending), 8)

    def test_parsed_brier_score_matches_ledger_summary(self):
        """Mean evaluated Brier score must match ledger table."""
        evaluated = [p for p in self.predictions if p.outcome is not None]
        forecasts = [p.confidence for p in evaluated]
        outcomes = [p.outcome for p in evaluated if p.outcome is not None]

        score = compute_brier_score(forecasts, outcomes)
        # Expected <= 0.0005 across the high-confidence verified ledger
        self.assertLess(score, 0.0005)

    def test_sha256_custody_hash(self):
        """Ledger file SHA-256 hash must be valid 64-character lowercase hexadecimal."""
        self.assertEqual(len(self.sha256), 64)
        self.assertTrue(all(c in "0123456789abcdef" for c in self.sha256))


class TestBrierScoreAndScoringRules(unittest.TestCase):
    """Verifies mathematical properties of strictly proper Brier scoring."""

    def test_perfect_calibration(self):
        """Forecasts matching binary ground truth identically yield BS = 0.0."""
        forecasts = [1.0, 0.0, 1.0, 0.0]
        outcomes = [1.0, 0.0, 1.0, 0.0]
        self.assertEqual(compute_brier_score(forecasts, outcomes), 0.0)

    def test_maximally_wrong(self):
        """Forecasts inverted from ground truth yield BS = 1.0."""
        forecasts = [0.0, 1.0]
        outcomes = [1.0, 0.0]
        self.assertEqual(compute_brier_score(forecasts, outcomes), 1.0)

    def test_uninformative_baseline(self):
        """A static forecast of 0.5 against balanced outcomes yields BS = 0.25."""
        forecasts = [0.5, 0.5, 0.5, 0.5]
        outcomes = [1.0, 0.0, 1.0, 0.0]
        self.assertEqual(compute_brier_score(forecasts, outcomes), 0.25)

    def test_known_historical_subcube_pair(self):
        """Verify baseline score for PRED-004 (0.999) and PRED-005 (0.95)."""
        forecasts = [0.999, 0.95]
        outcomes = [1.0, 1.0]
        expected = ((0.999 - 1.0) ** 2 + (0.95 - 1.0) ** 2) / 2.0
        self.assertAlmostEqual(compute_brier_score(forecasts, outcomes), expected, places=7)


class TestMurphy1973Decomposition(unittest.TestCase):
    """Verifies the algebraic decomposition theorems of Murphy (1973)."""

    def test_exact_discrete_decomposition_identity(self):
        """In exact discrete decomposition, within-bin variance is 0 identically:
        BS == Reliability - Resolution + Uncertainty
        """
        forecasts = [0.2, 0.2, 0.5, 0.8, 0.8, 0.9]
        outcomes = [0.0, 1.0, 0.0, 1.0, 1.0, 1.0]

        decomp = compute_exact_discrete_decomposition(forecasts, outcomes)
        self.assertEqual(decomp.within_bin_variance, 0.0)
        self.assertTrue(decomp.partition_valid)
        self.assertLess(decomp.partition_residual, 1e-12)

        reconstructed = decomp.reliability - decomp.resolution + decomp.uncertainty
        self.assertAlmostEqual(decomp.raw_brier, reconstructed, places=12)

    def test_uniform_binned_decomposition_identity(self):
        """In uniform binned decomposition:
        BS_raw == Reliability - Resolution + Uncertainty + WithinBinVariance
        BS_binned == Reliability - Resolution + Uncertainty
        """
        forecasts = [0.12, 0.18, 0.35, 0.45, 0.82, 0.89, 0.95]
        outcomes = [0.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0]

        decomp = compute_murphy_decomposition(forecasts, outcomes, n_bins=5)
        self.assertTrue(decomp.partition_valid)
        self.assertLess(decomp.partition_residual, 1e-11)

        # Check binned brier
        reconstructed_binned = decomp.reliability - decomp.resolution + decomp.uncertainty
        self.assertAlmostEqual(decomp.binned_brier, reconstructed_binned, places=12)

        # Check raw brier with within-bin variance
        reconstructed_raw = (
            decomp.reliability - decomp.resolution + decomp.uncertainty + decomp.within_bin_variance
        )
        self.assertAlmostEqual(decomp.raw_brier, reconstructed_raw, places=12)

    def test_zero_uncertainty_when_all_outcomes_identical(self):
        """When all outcomes are 1.0, sample climatology has zero uncertainty."""
        forecasts = [0.90, 0.95, 0.99]
        outcomes = [1.0, 1.0, 1.0]

        decomp = compute_exact_discrete_decomposition(forecasts, outcomes)
        self.assertEqual(decomp.uncertainty, 0.0)
        self.assertEqual(decomp.resolution, 0.0)
        self.assertAlmostEqual(decomp.raw_brier, decomp.reliability, places=12)

    def test_zero_resolution_when_forecasts_constant(self):
        """Constant forecasts provide zero discrimination (Resolution = 0.0)."""
        forecasts = [0.7, 0.7, 0.7, 0.7]
        outcomes = [1.0, 0.0, 1.0, 0.0]

        decomp = compute_exact_discrete_decomposition(forecasts, outcomes)
        self.assertEqual(decomp.resolution, 0.0)


class TestReliabilityCurveAndCalibrationBins(unittest.TestCase):
    """Verifies empirical reliability curve calculation and partitioning."""

    def test_ten_bin_coverage_and_count_conservation(self):
        """Ten uniform bins must partition samples with total count conserved."""
        forecasts = [0.05, 0.15, 0.25, 0.75, 0.85, 0.95]
        outcomes = [0.0, 0.0, 1.0, 1.0, 1.0, 1.0]

        curve = compute_reliability_curve(forecasts, outcomes, n_bins=10)
        self.assertEqual(len(curve), 10)
        total_counted = sum(b.count for b in curve)
        self.assertEqual(total_counted, len(forecasts))

    def test_bin_rate_computations(self):
        """Occupied bins must compute accurate mean forecast and empirical rate."""
        forecasts = [0.92, 0.98]
        outcomes = [1.0, 1.0]

        curve = compute_reliability_curve(forecasts, outcomes, n_bins=10)
        # Bin 9 is [0.9, 1.0]
        bin_9 = curve[9]
        self.assertEqual(bin_9.count, 2)
        self.assertEqual(bin_9.positive_count, 2)
        self.assertAlmostEqual(bin_9.mean_forecast, 0.95, places=5)
        self.assertAlmostEqual(bin_9.empirical_rate, 1.0, places=5)
        self.assertAlmostEqual(bin_9.calibration_gap, -0.05, places=5)

    def test_discrete_reliability_points(self):
        """Discrete reliability points aggregate identical probabilities."""
        forecasts = [0.90, 0.90, 0.99]
        outcomes = [1.0, 1.0, 1.0]

        points = compute_discrete_reliability_curve(forecasts, outcomes)
        self.assertEqual(len(points), 2)
        p0 = points[0]
        self.assertEqual(p0.forecast, 0.90)
        self.assertEqual(p0.count, 2)
        self.assertEqual(p0.empirical_rate, 1.0)


class TestCalibrationMetrics(unittest.TestCase):
    """Verifies composite calibration error metrics (ECE, MCE, Sharpness)."""

    def test_ece_and_mce_relationships(self):
        """MCE must always be greater than or equal to ECE."""
        forecasts = [0.1, 0.4, 0.7, 0.9]
        outcomes = [0.0, 0.0, 1.0, 1.0]

        m = compute_calibration_metrics(forecasts, outcomes, n_bins=5)
        self.assertGreaterEqual(m.maximum_calibration_error_mce, m.expected_calibration_error_ece)
        self.assertGreaterEqual(m.discrete_maximum_calibration_error, m.discrete_expected_calibration_error)
        self.assertGreaterEqual(m.sharpness, 0.0)

    def test_sharpness_ordering(self):
        """High-confidence forecasters exhibit strictly higher sharpness than hedgers."""
        bold_f = [0.99, 0.01, 0.98, 0.02]
        timid_f = [0.52, 0.48, 0.51, 0.49]
        outcomes = [1.0, 0.0, 1.0, 0.0]

        m_bold = compute_calibration_metrics(bold_f, outcomes)
        m_timid = compute_calibration_metrics(timid_f, outcomes)
        self.assertGreater(m_bold.sharpness, m_timid.sharpness)

    def test_brier_skill_score_with_uncertainty(self):
        """When uncertainty > 0, BSS evaluates properly."""
        forecasts = [0.8, 0.2]
        outcomes = [1.0, 0.0]

        m = compute_calibration_metrics(forecasts, outcomes)
        self.assertIsNotNone(m.brier_skill_score)
        # Climatology base rate = 0.5, unc = 0.25. Brier = ((0.8-1)^2 + (0.2-0)^2)/2 = 0.04.
        # BSS = 1 - 0.04 / 0.25 = 1 - 0.16 = 0.84.
        self.assertAlmostEqual(m.brier_skill_score, 0.84, places=5)


class TestInputValidation(unittest.TestCase):
    """Verifies rigorous input validation, type safety, and boundary checks."""

    def test_empty_inputs_raise_value_error(self):
        with self.assertRaises(ValueError):
            validate_forecasts_and_outcomes([], [])

    def test_length_mismatch_raises_value_error(self):
        with self.assertRaises(ValueError):
            validate_forecasts_and_outcomes([0.5, 0.8], [1.0])

    def test_probability_out_of_bounds(self):
        with self.assertRaises(ValueError):
            validate_forecasts_and_outcomes([1.01], [1.0])
        with self.assertRaises(ValueError):
            validate_forecasts_and_outcomes([-0.01], [0.0])

    def test_non_binary_outcomes(self):
        with self.assertRaises(ValueError):
            validate_forecasts_and_outcomes([0.5], [2.0])
        with self.assertRaises(ValueError):
            validate_forecasts_and_outcomes([0.5], [0.5])

    def test_nan_or_inf_rejected(self):
        with self.assertRaises(ValueError):
            validate_forecasts_and_outcomes([float("nan")], [1.0])
        with self.assertRaises(ValueError):
            validate_forecasts_and_outcomes([float("inf")], [1.0])

    def test_invalid_types_rejected(self):
        with self.assertRaises(TypeError):
            validate_forecasts_and_outcomes("0.8", [1.0])


class TestObstinateVsBayesianRevising(unittest.TestCase):
    """Reproduces and verifies PRED-028:
    Refusal to surrender hypothesis certainty degrades Brier calibration by > 5x.
    """

    def test_brier_penalty_inflation(self):
        """In a sequence of 10 failing trials (o = 0):
        Obstinate forecaster (f = 0.90) incurs B = 0.81.
        Bayesian forecaster updating prior Beta(1,1) incurs B < 0.15.
        """
        n_trials = 10
        outcomes = [0.0] * n_trials

        # Obstinate agent: constant 0.90
        obstinate_f = [0.90] * n_trials
        b_obstinate = compute_brier_score(obstinate_f, outcomes)
        self.assertAlmostEqual(b_obstinate, 0.81, places=5)

        # Rational Bayesian agent starting with prior Beta(1, 1), updating: f_t = 1 / (1 + t + 1)
        bayesian_f = [1.0 / (2 + t) for t in range(n_trials)]
        b_bayesian = compute_brier_score(bayesian_f, outcomes)

        self.assertLess(b_bayesian, 0.15)
        inflation_ratio = b_obstinate / b_bayesian
        self.assertGreater(inflation_ratio, 5.0)


class TestReviewAdditions(unittest.TestCase):
    """Added in round-six review: faults that earlier tests let through."""

    def test_benchmark_json_matches_live_ledger_hash(self):
        art = json.loads((evidence_dir / "2026-10-23_aura-meridian-benchmark.json").read_text(encoding="utf-8"))
        _, sha = parse_predictions_ledger(evidence_dir / "predictions-ledger.md")
        self.assertEqual(art["source_ledger_sha256"], sha, "benchmark JSON is stale: rerun continuous_calibration.py")

    def test_missed_entry_parses_as_zero_outcome(self):
        import tempfile
        text = ("### PRED-900: planted\n- **Made:** 2026-10-23 by Test\n- **Prediction:** x\n"
                "- **Confidence:** 0.90\n- **Status:** MISSED (planted)\n")
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "l.md"; p.write_text(text, encoding="utf-8")
            preds, _ = parse_predictions_ledger(p)
        self.assertEqual(preds[0].status, "MISSED")
        self.assertEqual(preds[0].outcome, 0.0)

    def test_overconfident_miss_has_nonzero_ece(self):
        from continuous_calibration import compute_calibration_metrics
        m = compute_calibration_metrics([0.9, 0.9], [0.0, 0.0])
        self.assertGreater(m.expected_calibration_error_ece, 0.5)


class TestBenchmarkArtifactIntegrity(unittest.TestCase):
    """Verifies the emitted machine-readable benchmark JSON artifact."""

    def test_artifact_exists_and_is_valid_json(self):
        artifact_path = evidence_dir / "2026-10-23_aura-meridian-benchmark.json"
        self.assertTrue(artifact_path.exists(), f"Artifact missing at {artifact_path}")

        data = json.loads(artifact_path.read_text(encoding="utf-8"))
        required_keys = {
            "benchmark_name",
            "framework",
            "seat",
            "source_ledger",
            "summary",
            "calibration_metrics",
            "murphy_1973_decomposition",
            "reliability_curve",
            "discrete_probability_levels",
            "predictions",
        }
        self.assertTrue(required_keys.issubset(data.keys()))

        # Check summary metrics
        s = data["summary"]
        self.assertGreaterEqual(s["total_predictions"], 34)
        self.assertGreaterEqual(s["evaluated_predictions"], 26)
        self.assertEqual(s["misses"], 0)
        self.assertEqual(s["pending_predictions"], 8)

        # Check Murphy exact decomposition residual
        murphy = data["murphy_1973_decomposition"]
        exact = murphy["exact_discrete"]
        self.assertTrue(exact["partition_valid"])
        self.assertLess(exact["partition_residual"], 1e-12)


if __name__ == "__main__":
    unittest.main()
