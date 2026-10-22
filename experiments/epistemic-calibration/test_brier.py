"""Unit tests for Brier score calculator and epistemic calibration."""

import math
import unittest
from pathlib import Path

from brier_calculator import (
    brier_decomposition,
    brier_score,
    calibration_bins,
    parse_prediction_ledger,
)


class TestBrierCalculator(unittest.TestCase):
    def test_perfect_predictions(self):
        """When forecasts match outcomes identically, Brier score and reliability are 0.0."""
        forecasts = [1.0, 0.0, 1.0, 0.0]
        outcomes = [1, 0, 1, 0]
        b = brier_score(forecasts, outcomes)
        self.assertEqual(b, 0.0)

        decomp = brier_decomposition(forecasts, outcomes, n_bins=10)
        self.assertAlmostEqual(decomp["brier_score"], 0.0, places=10)
        self.assertAlmostEqual(decomp["reliability"], 0.0, places=10)
        self.assertAlmostEqual(decomp["sharpness"], 0.25, places=10)

    def test_maximally_wrong_predictions(self):
        """When forecasts are the exact opposite of outcomes, Brier score is 1.0."""
        forecasts = [0.0, 1.0]
        outcomes = [1, 0]
        b = brier_score(forecasts, outcomes)
        self.assertEqual(b, 1.0)

    def test_uninformative_constant_half(self):
        """A constant forecast of 0.5 against balanced outcomes yields Brier score 0.25."""
        forecasts = [0.5, 0.5, 0.5, 0.5]
        outcomes = [1, 0, 1, 0]
        b = brier_score(forecasts, outcomes)
        self.assertEqual(b, 0.25)

        decomp = brier_decomposition(forecasts, outcomes, n_bins=5)
        # Resolution is 0.0 because the forecaster cannot discriminate between outcomes
        self.assertAlmostEqual(decomp["resolution"], 0.0, places=10)
        # Reliability is 0.0 because 0.5 forecast matches 0.5 base rate exactly
        self.assertAlmostEqual(decomp["reliability"], 0.0, places=10)
        # Uncertainty is 0.5 * (1 - 0.5) = 0.25
        self.assertAlmostEqual(decomp["uncertainty"], 0.25, places=10)
        # Sharpness is 0.0 because there is no variation in predictions
        self.assertAlmostEqual(decomp["sharpness"], 0.0, places=10)

    def test_murphy_decomposition_identity(self):
        """Verify the mathematical identity of Murphy (1973):
        BinnedBrier = Reliability - Resolution + Uncertainty.
        """
        forecasts = [0.1, 0.2, 0.35, 0.8, 0.85, 0.9]
        outcomes = [0, 0, 1, 1, 1, 0]

        decomp = brier_decomposition(forecasts, outcomes, n_bins=5)
        binned_brier = decomp["binned_brier_score"]
        rel = decomp["reliability"]
        res = decomp["resolution"]
        unc = decomp["uncertainty"]

        reconstructed = rel - res + unc
        self.assertAlmostEqual(binned_brier, reconstructed, places=10)

    def test_discrete_forecast_exact_brier_decomposition(self):
        """When each forecast is equal to its bin mean, raw Brier equals binned Brier."""
        forecasts = [0.1, 0.1, 0.4, 0.8, 0.8, 0.8]
        outcomes = [0, 0, 1, 1, 1, 0]

        decomp = brier_decomposition(forecasts, outcomes, n_bins=10)
        self.assertAlmostEqual(decomp["brier_score"], decomp["binned_brier_score"], places=10)
        self.assertAlmostEqual(
            decomp["brier_score"],
            decomp["reliability"] - decomp["resolution"] + decomp["uncertainty"],
            places=10,
        )

    def test_sharpness_property(self):
        """Sharpness measures variance of forecasts: high confidence = high sharpness."""
        # Unhedged bold forecaster
        bold_f = [0.95, 0.05, 0.90, 0.10]
        # Hedging timid forecaster
        timid_f = [0.55, 0.45, 0.52, 0.48]
        outcomes = [1, 0, 1, 0]

        decomp_bold = brier_decomposition(bold_f, outcomes)
        decomp_timid = brier_decomposition(timid_f, outcomes)

        self.assertGreater(decomp_bold["sharpness"], decomp_timid["sharpness"])

    def test_calibration_bins_partition(self):
        """Calibration bins must correctly count and compute empirical rates."""
        forecasts = [0.05, 0.15, 0.85, 0.95]
        outcomes = [0, 1, 1, 1]
        bins = calibration_bins(forecasts, outcomes, n_bins=5)

        self.assertEqual(len(bins), 5)
        # Bin 0: [0.0, 0.2) should contain 0.05 and 0.15
        self.assertEqual(bins[0]["count"], 2)
        self.assertAlmostEqual(bins[0]["mean_forecast"], 0.10, places=5)
        self.assertAlmostEqual(bins[0]["empirical_rate"], 0.50, places=5)

        # Bin 4: [0.8, 1.0] should contain 0.85 and 0.95
        self.assertEqual(bins[4]["count"], 2)
        self.assertAlmostEqual(bins[4]["mean_forecast"], 0.90, places=5)
        self.assertAlmostEqual(bins[4]["empirical_rate"], 1.00, places=5)

    def test_input_validation(self):
        """Strict validation on length, types, probability intervals, and binary values."""
        with self.assertRaises(ValueError):
            brier_score([], [])

        with self.assertRaises(ValueError):
            brier_score([0.5], [1, 0])

        with self.assertRaises(ValueError):
            brier_score([1.5], [1])

        with self.assertRaises(ValueError):
            brier_score([-0.1], [0])

        with self.assertRaises(ValueError):
            brier_score([0.5], [2])

        with self.assertRaises(TypeError):
            brier_score("0.5", [1])

    def test_ledger_parser_and_settled_evaluation(self):
        """Verify parsing against actual sync zone predictions ledger file."""
        ledger_path = Path(__file__).parent.parent.parent / "evidence" / "predictions-ledger.md"
        if not ledger_path.exists():
            self.skipTest(f"Ledger file not found at {ledger_path}")

        content = ledger_path.read_text(encoding="utf-8")
        parsed = parse_prediction_ledger(content)
        self.assertGreaterEqual(len(parsed), 6)

        # Find settled HIT/MISSED predictions
        settled = [p for p in parsed if p["outcome"] is not None]
        self.assertGreaterEqual(len(settled), 2)

        forecasts = [p["confidence"] for p in settled]
        outcomes = [p["outcome"] for p in settled]

        score = brier_score(forecasts, outcomes)
        # Expected from PRED-004 (0.999 hit) and PRED-005 (0.95 hit):
        # ((0.999 - 1.0)^2 + (0.95 - 1.0)^2) / 2 = (0.000001 + 0.0025) / 2 = 0.0012505 ~= 0.0013
        pred_004_005 = [p for p in settled if p["id"] in ("PRED-004", "PRED-005")]
        if len(pred_004_005) == 2:
            s_baseline = brier_score([p["confidence"] for p in pred_004_005], [p["outcome"] for p in pred_004_005])
            self.assertAlmostEqual(s_baseline, 0.0012505, places=5)
        self.assertLess(score, 0.005)


if __name__ == "__main__":
    unittest.main()
