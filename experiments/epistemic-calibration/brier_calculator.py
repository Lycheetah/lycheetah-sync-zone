"""Epistemic Calibration & Brier Score Calculator for Lycheetah Sync Zone.

Calculates the Brier score, Murphy (1973) reliability-resolution-uncertainty decomposition,
sharpness, and empirical calibration bins for probabilistic predictions.
"""

from __future__ import annotations

import math
import re
from typing import Any, Sequence


def brier_score(
    forecasts: Sequence[float],
    outcomes: Sequence[int | float | bool],
) -> float:
    """Calculate the empirical Brier score: B = (1/N) * sum((f_t - o_t)^2).

    Parameters:
        forecasts: Sequence of predicted probabilities in [0.0, 1.0].
        outcomes: Sequence of binary ground truth outcomes in {0, 1}.

    Returns:
        float in [0.0, 1.0]. 0.0 is perfect calibration and sharpness.
    """
    _validate_inputs(forecasts, outcomes)
    n = len(forecasts)
    total_sq_err = sum((float(f) - float(o)) ** 2 for f, o in zip(forecasts, outcomes))
    return total_sq_err / n


def calibration_bins(
    forecasts: Sequence[float],
    outcomes: Sequence[int | float | bool],
    n_bins: int = 10,
) -> list[dict[str, Any]]:
    """Partition predictions into bins to compute empirical calibration curves.

    Parameters:
        forecasts: Sequence of predicted probabilities in [0.0, 1.0].
        outcomes: Sequence of binary ground truth outcomes in {0, 1}.
        n_bins: Number of equal-width bins spanning [0.0, 1.0].

    Returns:
        List of dicts per bin containing:
            - bin_index (int)
            - bin_lower (float)
            - bin_upper (float)
            - count (int)
            - mean_forecast (float | None)
            - empirical_rate (float | None)
    """
    _validate_inputs(forecasts, outcomes)
    if n_bins <= 0:
        raise ValueError("n_bins must be a positive integer")

    bin_width = 1.0 / n_bins
    bins: list[dict[str, Any]] = []

    for k in range(n_bins):
        lower = k * bin_width
        upper = (k + 1) * bin_width
        bin_forecasts: list[float] = []
        bin_outcomes: list[float] = []

        for f, o in zip(forecasts, outcomes):
            f_val = float(f)
            o_val = float(o)
            # Include upper edge in the last bin
            if k == n_bins - 1:
                in_bin = lower <= f_val <= upper
            else:
                in_bin = lower <= f_val < upper

            if in_bin:
                bin_forecasts.append(f_val)
                bin_outcomes.append(o_val)

        count = len(bin_forecasts)
        mean_f = sum(bin_forecasts) / count if count > 0 else None
        emp_rate = sum(bin_outcomes) / count if count > 0 else None

        bins.append({
            "bin_index": k,
            "bin_lower": lower,
            "bin_upper": upper,
            "count": count,
            "mean_forecast": mean_f,
            "empirical_rate": emp_rate,
        })

    return bins


def brier_decomposition(
    forecasts: Sequence[float],
    outcomes: Sequence[int | float | bool],
    n_bins: int = 10,
) -> dict[str, float | int]:
    """Calculate the Murphy (1973) Brier score decomposition:
    BinnedBrier = Reliability - Resolution + Uncertainty

    For discrete forecast categories where all forecasts within a bin share the
    bin forecast probability, Brier == BinnedBrier identically.

    Also calculates forecast Sharpness: Var(f) = (1/N) * sum((f_t - mean(f))^2).

    Parameters:
        forecasts: Sequence of predicted probabilities in [0.0, 1.0].
        outcomes: Sequence of binary ground truth outcomes in {0, 1}.
        n_bins: Number of bins for partition.

    Returns:
        Dict with keys:
            - brier_score (raw sample Brier score)
            - binned_brier_score (evaluating forecasts at bin means)
            - reliability (calibration error, >= 0, lower is better)
            - resolution (discriminative power, >= 0, higher is better)
            - uncertainty (inherent outcome entropy, base_rate * (1 - base_rate))
            - sharpness (sample variance of raw forecasts)
            - base_rate (overall event frequency)
            - n_samples (total count)
    """
    _validate_inputs(forecasts, outcomes)
    n = len(forecasts)
    raw_brier = brier_score(forecasts, outcomes)
    bins = calibration_bins(forecasts, outcomes, n_bins=n_bins)

    base_rate = sum(float(o) for o in outcomes) / n
    uncertainty = base_rate * (1.0 - base_rate)

    reliability = 0.0
    resolution = 0.0
    binned_sq_err = 0.0

    for b in bins:
        count = b["count"]
        if count == 0:
            continue
        mean_f = b["mean_forecast"]
        emp_rate = b["empirical_rate"]
        k = b["bin_index"]
        lower = b["bin_lower"]
        upper = b["bin_upper"]

        # Reliability: (count / N) * (mean_f - emp_rate)^2
        reliability += (count / n) * ((mean_f - emp_rate) ** 2)

        # Resolution: (count / N) * (emp_rate - base_rate)^2
        resolution += (count / n) * ((emp_rate - base_rate) ** 2)

        # Binned square error: sum over bin of (mean_f - o_t)^2
        for f, o in zip(forecasts, outcomes):
            f_val = float(f)
            in_bin = lower <= f_val <= upper if k == n_bins - 1 else lower <= f_val < upper
            if in_bin:
                binned_sq_err += (float(mean_f) - float(o)) ** 2

    binned_brier = binned_sq_err / n

    # Sharpness: sample variance of raw forecasts
    mean_raw_f = sum(float(f) for f in forecasts) / n
    sharpness = sum((float(f) - mean_raw_f) ** 2 for f in forecasts) / n

    return {
        "brier_score": raw_brier,
        "binned_brier_score": binned_brier,
        "reliability": reliability,
        "resolution": resolution,
        "uncertainty": uncertainty,
        "sharpness": sharpness,
        "base_rate": base_rate,
        "n_samples": n,
    }


def parse_prediction_ledger(ledger_text: str) -> list[dict[str, Any]]:
    """Parse prediction entries from markdown ledger text.

    Extracts prediction ID, confidence, and status ('HIT', 'MISSED', 'PENDING').
    """
    pred_regex = re.compile(
        r"###\s+(PRED-\d{3}):\s*(.+?)\n"
        r"(?:.*?\n)*?"
        r"-\s*\*\*Confidence:\*\*\s*([\d\.]+)\n"
        r"-\s*\*\*Status:\*\*\s*(HIT|MISSED|PENDING)",
        re.MULTILINE,
    )
    results = []
    for match in pred_regex.finditer(ledger_text):
        pid, title, conf_str, status = match.groups()
        conf = float(conf_str)
        outcome = 1 if status == "HIT" else 0 if status == "MISSED" else None
        results.append({
            "id": pid,
            "title": title.strip(),
            "confidence": conf,
            "status": status,
            "outcome": outcome,
        })
    return results


def _validate_inputs(
    forecasts: Sequence[float],
    outcomes: Sequence[int | float | bool],
) -> None:
    if not isinstance(forecasts, (list, tuple)) or not isinstance(outcomes, (list, tuple)):
        raise TypeError("forecasts and outcomes must be lists or tuples")
    if len(forecasts) == 0:
        raise ValueError("forecasts list cannot be empty")
    if len(forecasts) != len(outcomes):
        raise ValueError(f"Length mismatch: {len(forecasts)} forecasts vs {len(outcomes)} outcomes")

    for i, f in enumerate(forecasts):
        try:
            f_val = float(f)
        except (ValueError, TypeError) as err:
            raise TypeError(f"Forecast at index {i} is not a valid float: {f}") from err
        if math.isnan(f_val) or math.isinf(f_val):
            raise ValueError(f"Forecast at index {i} is NaN or Inf")
        if not (0.0 <= f_val <= 1.0):
            raise ValueError(f"Forecast at index {i} must be in [0.0, 1.0], got {f_val}")

    for i, o in enumerate(outcomes):
        try:
            o_val = float(o)
        except (ValueError, TypeError) as err:
            raise TypeError(f"Outcome at index {i} is not a valid number: {o}") from err
        if o_val not in (0.0, 1.0):
            raise ValueError(f"Outcome at index {i} must be binary 0 or 1, got {o_val}")
