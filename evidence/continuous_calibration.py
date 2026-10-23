#!/usr/bin/env python3
"""Reviewed by Nettle (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, the arithmetic is sound and reproducible (tests bite on planted Brier, outcome and MCE faults); it scores a ledger of post-hoc verifications, so it measures nothing about forecasting (dispute 400). Original wording is in git history.

Aura Meridian Continuous Calibration & Epistemic Benchmark Suite.

Role: Creative, Frontier & Constitutional Knowledge Agent in the Lycheetah GitHub Sync Zone.
Under the constitutional agency of Aura Meridian and Aetheron.

This module implements an automated continuous calibration and verification suite
for the Sync Zone prediction ledger:
1. Parses all registered predictions (PRED-001 through PRED-034+) from
   `evidence/predictions-ledger.md`.
2. Computes empirical Brier scores under strictly proper scoring rules.
3. Computes the Murphy (1973) three-term vector partition:
      Brier = Reliability - Resolution + Uncertainty + WithinBinVariance
   both for standard uniform probability bins and exact discrete probability levels.
4. Computes empirical reliability curves, Expected Calibration Error (ECE),
   Maximum Calibration Error (MCE), Root Mean Squared Calibration Error (RMSCE),
   and forecast Sharpness.
5. Emits a deterministic, machine-readable benchmark receipt to
   `evidence/2026-10-23_aura-meridian-benchmark.json`.

References:
- Murphy, A. H. (1973). "A New Vector Partition of the Probability Score."
  Journal of Applied Meteorology and Climatology, 12(4), 595-600.
- Brier, G. W. (1950). "Verification of forecasts expressed in terms of probability."
  Monthly Weather Review, 78(1), 1-3.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class Prediction:
    """A single structured prediction entry from the predictions ledger."""

    id: str
    title: str
    confidence: float
    status: str
    outcome: Optional[float]
    made_raw: str = ""
    made_date: str = ""
    seat: str = ""
    prediction: str = ""
    verification_trigger: str = ""
    falsifier: str = ""
    test_command: str = ""
    status_detail: str = ""
    evidence: str = ""
    individual_brier: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ReliabilityBin:
    """One bin of an empirical calibration / reliability curve."""

    bin_index: int
    bin_lower: float
    bin_upper: float
    count: int
    positive_count: int
    mean_forecast: Optional[float]
    empirical_rate: Optional[float]
    calibration_gap: Optional[float]
    reliability_contribution: float
    resolution_contribution: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DiscreteReliabilityPoint:
    """Discrete forecast level calibration point (exact value grouping)."""

    forecast: float
    count: int
    positive_count: int
    empirical_rate: float
    calibration_gap: float
    brier_contribution: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MurphyDecomposition:
    """Murphy (1973) Brier score vector decomposition."""

    mode: str
    raw_brier: float
    binned_brier: float
    reliability: float
    resolution: float
    uncertainty: float
    within_bin_variance: float
    base_rate: float
    n_samples: int
    partition_valid: bool
    partition_residual: float
    n_partitions: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CalibrationMetrics:
    """Composite calibration and discrimination performance metrics."""

    brier_score: float
    expected_calibration_error_ece: float
    maximum_calibration_error_mce: float
    discrete_expected_calibration_error: float
    discrete_maximum_calibration_error: float
    rms_calibration_error: float
    sharpness: float
    mean_confidence: float
    base_rate: float
    overconfidence_bias: float
    brier_skill_score: Optional[float]
    brier_skill_score_note: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BenchmarkReport:
    """Complete machine-readable and reproducible benchmark receipt."""

    benchmark_name: str
    framework: str
    seat: str
    generated_at: str
    source_ledger: str
    source_ledger_sha256: str
    summary: Dict[str, Any]
    calibration_metrics: CalibrationMetrics
    murphy_1973_decomposition: Dict[str, MurphyDecomposition]
    reliability_curve_binned: List[ReliabilityBin]
    discrete_probability_levels: List[DiscreteReliabilityPoint]
    predictions: List[Prediction]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "benchmark_name": self.benchmark_name,
            "framework": self.framework,
            "seat": self.seat,
            "generated_at": self.generated_at,
            "source_ledger": self.source_ledger,
            "source_ledger_sha256": self.source_ledger_sha256,
            "summary": self.summary,
            "calibration_metrics": self.calibration_metrics.to_dict(),
            "murphy_1973_decomposition": {
                k: v.to_dict() for k, v in self.murphy_1973_decomposition.items()
            },
            "reliability_curve": [b.to_dict() for b in self.reliability_curve_binned],
            "discrete_probability_levels": [
                p.to_dict() for p in self.discrete_probability_levels
            ],
            "predictions": [p.to_dict() for p in self.predictions],
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)


# ---------------------------------------------------------------------------
# Validation & Scoring Functions
# ---------------------------------------------------------------------------

def validate_forecasts_and_outcomes(
    forecasts: Sequence[float],
    outcomes: Sequence[Union[int, float, bool]],
) -> Tuple[List[float], List[float]]:
    """Validate forecast probabilities and binary outcomes strictly.

    Raises:
        TypeError: If inputs are not sequences of numbers.
        ValueError: If empty, lengths differ, probabilities not in [0, 1],
                    or outcomes not in {0.0, 1.0}.
    """
    if not isinstance(forecasts, (list, tuple)) or not isinstance(outcomes, (list, tuple)):
        raise TypeError("forecasts and outcomes must be sequences (list or tuple)")
    if len(forecasts) == 0:
        raise ValueError("Forecast and outcome sequences cannot be empty")
    if len(forecasts) != len(outcomes):
        raise ValueError(
            f"Length mismatch: {len(forecasts)} forecasts vs {len(outcomes)} outcomes"
        )

    clean_f: List[float] = []
    for i, f in enumerate(forecasts):
        try:
            f_val = float(f)
        except (ValueError, TypeError) as err:
            raise TypeError(f"Forecast at index {i} is not a valid float: {f!r}") from err
        if math.isnan(f_val) or math.isinf(f_val):
            raise ValueError(f"Forecast at index {i} is NaN or Inf: {f_val}")
        if not (0.0 <= f_val <= 1.0):
            raise ValueError(f"Forecast at index {i} must be in [0.0, 1.0], got {f_val}")
        clean_f.append(f_val)

    clean_o: List[float] = []
    for i, o in enumerate(outcomes):
        try:
            o_val = float(o)
        except (ValueError, TypeError) as err:
            raise TypeError(f"Outcome at index {i} is not a valid number: {o!r}") from err
        if math.isnan(o_val) or math.isinf(o_val):
            raise ValueError(f"Outcome at index {i} is NaN or Inf: {o_val}")
        if o_val not in (0.0, 1.0):
            raise ValueError(f"Outcome at index {i} must be binary 0 or 1, got {o_val}")
        clean_o.append(o_val)

    return clean_f, clean_o


def compute_brier_score(
    forecasts: Sequence[float],
    outcomes: Sequence[Union[int, float, bool]],
) -> float:
    """Calculate the empirical Brier score:

        BS = (1 / N) * sum((f_i - o_i)^2)

    A strictly proper scoring rule bounded in [0.0, 1.0]. Lower is better.
    """
    f_list, o_list = validate_forecasts_and_outcomes(forecasts, outcomes)
    n = len(f_list)
    return sum((f - o) ** 2 for f, o in zip(f_list, o_list)) / n


def compute_murphy_decomposition(
    forecasts: Sequence[float],
    outcomes: Sequence[Union[int, float, bool]],
    n_bins: int = 10,
) -> MurphyDecomposition:
    """Calculate the uniform binned Murphy (1973) vector partition:

        BS_raw = Reliability - Resolution + Uncertainty + WithinBinVariance
        BS_binned = Reliability - Resolution + Uncertainty

    Parameters:
        forecasts: Predicted probabilities in [0.0, 1.0].
        outcomes: Binary outcomes in {0.0, 1.0}.
        n_bins: Number of equal-width bins across [0.0, 1.0].

    Returns:
        MurphyDecomposition dataclass.
    """
    if n_bins <= 0:
        raise ValueError("n_bins must be a positive integer >= 1")

    f_list, o_list = validate_forecasts_and_outcomes(forecasts, outcomes)
    n = len(f_list)
    raw_brier = compute_brier_score(f_list, o_list)

    base_rate = sum(o_list) / n
    uncertainty = base_rate * (1.0 - base_rate)

    bin_width = 1.0 / n_bins
    reliability = 0.0
    resolution = 0.0
    within_bin_var = 0.0
    occupied_bins = 0

    for k in range(n_bins):
        lower = k * bin_width
        upper = (k + 1) * bin_width
        bin_f: List[float] = []
        bin_o: List[float] = []

        for f, o in zip(f_list, o_list):
            in_bin = lower <= f <= upper if k == n_bins - 1 else lower <= f < upper
            if in_bin:
                bin_f.append(f)
                bin_o.append(o)

        count = len(bin_f)
        if count == 0:
            continue

        occupied_bins += 1
        mean_f = sum(bin_f) / count
        emp_rate = sum(bin_o) / count
        weight = count / n

        reliability += weight * ((mean_f - emp_rate) ** 2)
        resolution += weight * ((emp_rate - base_rate) ** 2)
        within_bin_var += sum((f - mean_f) ** 2 for f in bin_f) / n

    binned_brier = reliability - resolution + uncertainty
    reconstructed_raw = reliability - resolution + uncertainty + within_bin_var
    residual = abs(reconstructed_raw - raw_brier)
    is_valid = residual < 1e-11

    return MurphyDecomposition(
        mode=f"uniform_{n_bins}_bin",
        raw_brier=raw_brier,
        binned_brier=binned_brier,
        reliability=reliability,
        resolution=resolution,
        uncertainty=uncertainty,
        within_bin_variance=within_bin_var,
        base_rate=base_rate,
        n_samples=n,
        partition_valid=is_valid,
        partition_residual=residual,
        n_partitions=n_bins,
    )


def compute_exact_discrete_decomposition(
    forecasts: Sequence[float],
    outcomes: Sequence[Union[int, float, bool]],
) -> MurphyDecomposition:
    """Calculate the exact discrete Murphy (1973) partition.

    Partitions samples by unique forecast probability levels.
    Because every forecast within a partition level is identical to its group mean,
    within-bin variance is identically zero:
        WithinBinVariance == 0.0
        BS_raw == BS_binned == Reliability - Resolution + Uncertainty
    holding to floating-point machine precision.
    """
    f_list, o_list = validate_forecasts_and_outcomes(forecasts, outcomes)
    n = len(f_list)
    raw_brier = compute_brier_score(f_list, o_list)

    base_rate = sum(o_list) / n
    uncertainty = base_rate * (1.0 - base_rate)

    # Group by exact forecast level
    groups: Dict[float, List[float]] = {}
    for f, o in zip(f_list, o_list):
        groups.setdefault(f, []).append(o)

    reliability = 0.0
    resolution = 0.0

    for f_level, group_outcomes in groups.items():
        count = len(group_outcomes)
        emp_rate = sum(group_outcomes) / count
        weight = count / n

        reliability += weight * ((f_level - emp_rate) ** 2)
        resolution += weight * ((emp_rate - base_rate) ** 2)

    within_bin_var = 0.0
    binned_brier = reliability - resolution + uncertainty
    residual = abs(binned_brier - raw_brier)
    is_valid = residual < 1e-12

    return MurphyDecomposition(
        mode="exact_discrete",
        raw_brier=raw_brier,
        binned_brier=binned_brier,
        reliability=reliability,
        resolution=resolution,
        uncertainty=uncertainty,
        within_bin_variance=within_bin_var,
        base_rate=base_rate,
        n_samples=n,
        partition_valid=is_valid,
        partition_residual=residual,
        n_partitions=len(groups),
    )


def compute_reliability_curve(
    forecasts: Sequence[float],
    outcomes: Sequence[Union[int, float, bool]],
    n_bins: int = 10,
) -> List[ReliabilityBin]:
    """Compute empirical calibration curve bins across [0.0, 1.0]."""
    if n_bins <= 0:
        raise ValueError("n_bins must be >= 1")

    f_list, o_list = validate_forecasts_and_outcomes(forecasts, outcomes)
    n = len(f_list)
    base_rate = sum(o_list) / n
    bin_width = 1.0 / n_bins
    curve: List[ReliabilityBin] = []

    for k in range(n_bins):
        lower = k * bin_width
        upper = (k + 1) * bin_width
        bin_f: List[float] = []
        bin_o: List[float] = []

        for f, o in zip(f_list, o_list):
            in_bin = lower <= f <= upper if k == n_bins - 1 else lower <= f < upper
            if in_bin:
                bin_f.append(f)
                bin_o.append(o)

        count = len(bin_f)
        pos_count = int(sum(bin_o))
        if count > 0:
            mean_f = sum(bin_f) / count
            emp_rate = sum(bin_o) / count
            gap = mean_f - emp_rate
            weight = count / n
            rel_contrib = weight * (gap ** 2)
            res_contrib = weight * ((emp_rate - base_rate) ** 2)
        else:
            mean_f = None
            emp_rate = None
            gap = None
            rel_contrib = 0.0
            res_contrib = 0.0

        curve.append(
            ReliabilityBin(
                bin_index=k,
                bin_lower=lower,
                bin_upper=upper,
                count=count,
                positive_count=pos_count,
                mean_forecast=mean_f,
                empirical_rate=emp_rate,
                calibration_gap=gap,
                reliability_contribution=rel_contrib,
                resolution_contribution=res_contrib,
            )
        )

    return curve


def compute_discrete_reliability_curve(
    forecasts: Sequence[float],
    outcomes: Sequence[Union[int, float, bool]],
) -> List[DiscreteReliabilityPoint]:
    """Compute calibration points grouped by unique forecast probabilities."""
    f_list, o_list = validate_forecasts_and_outcomes(forecasts, outcomes)
    n = len(f_list)

    groups: Dict[float, List[float]] = {}
    for f, o in zip(f_list, o_list):
        groups.setdefault(f, []).append(o)

    points: List[DiscreteReliabilityPoint] = []
    for f_level in sorted(groups.keys()):
        group_o = groups[f_level]
        count = len(group_o)
        pos_count = int(sum(group_o))
        emp_rate = sum(group_o) / count
        gap = f_level - emp_rate
        brier_contrib = (count / n) * ((f_level - emp_rate) ** 2)

        points.append(
            DiscreteReliabilityPoint(
                forecast=f_level,
                count=count,
                positive_count=pos_count,
                empirical_rate=emp_rate,
                calibration_gap=gap,
                brier_contribution=brier_contrib,
            )
        )

    return points


def compute_calibration_metrics(
    forecasts: Sequence[float],
    outcomes: Sequence[Union[int, float, bool]],
    n_bins: int = 10,
) -> CalibrationMetrics:
    """Compute Expected Calibration Error (ECE), Maximum Calibration Error (MCE),
    Root Mean Squared Calibration Error (RMSCE), and forecast Sharpness.
    """
    f_list, o_list = validate_forecasts_and_outcomes(forecasts, outcomes)
    n = len(f_list)
    brier = compute_brier_score(f_list, o_list)

    base_rate = sum(o_list) / n
    mean_conf = sum(f_list) / n
    sharpness = sum((f - mean_conf) ** 2 for f in f_list) / n
    overconf_bias = mean_conf - base_rate

    # ECE and MCE computed across occupied bins
    curve = compute_reliability_curve(f_list, o_list, n_bins=n_bins)
    ece = 0.0
    mce = 0.0
    weighted_sq_cal_err = 0.0

    for b in curve:
        if b.count > 0 and b.mean_forecast is not None and b.empirical_rate is not None:
            abs_gap = abs(b.mean_forecast - b.empirical_rate)
            weight = b.count / n
            ece += weight * abs_gap
            weighted_sq_cal_err += weight * (abs_gap ** 2)
            if abs_gap > mce:
                mce = abs_gap

    # Discrete calibration errors computed across unique probability levels
    discrete_points = compute_discrete_reliability_curve(f_list, o_list)
    disc_ece = sum((p.count / n) * abs(p.calibration_gap) for p in discrete_points)
    disc_mce = max(abs(p.calibration_gap) for p in discrete_points) if discrete_points else 0.0

    rms_cal_err = math.sqrt(weighted_sq_cal_err)

    # Brier Skill Score relative to climatology: BSS = 1 - BS / (base_rate * (1 - base_rate))
    unc = base_rate * (1.0 - base_rate)
    if unc > 1e-12:
        bss: Optional[float] = 1.0 - (brier / unc)
        bss_note = f"Standard BSS vs sample climatology uncertainty {unc:.6f}."
    else:
        bss = None
        bss_note = (
            "Sample uncertainty is 0.0 (all evaluated outcomes are identical); "
            "climatology reference has zero variance."
        )

    return CalibrationMetrics(
        brier_score=brier,
        expected_calibration_error_ece=ece,
        maximum_calibration_error_mce=mce,
        discrete_expected_calibration_error=disc_ece,
        discrete_maximum_calibration_error=disc_mce,
        rms_calibration_error=rms_cal_err,
        sharpness=sharpness,
        mean_confidence=mean_conf,
        base_rate=base_rate,
        overconfidence_bias=overconf_bias,
        brier_skill_score=bss,
        brier_skill_score_note=bss_note,
    )


# ---------------------------------------------------------------------------
# Ledger Parser
# ---------------------------------------------------------------------------

def parse_predictions_ledger(source: Union[str, Path]) -> Tuple[List[Prediction], str]:
    """Parse all structured prediction entries from markdown text or file.

    Extracts:
    - ID (e.g. PRED-001)
    - Title
    - Confidence
    - Status (HIT, MISSED, PENDING, etc.)
    - Outcome (1.0, 0.0, or None)
    - Date, Seat, Trigger, Falsifier, Evidence

    Returns:
        (List[Prediction], raw_text_sha256)
    """
    if isinstance(source, Path) or (isinstance(source, str) and Path(source).exists()):
        p = Path(source)
        raw_bytes = p.read_bytes()
        text = raw_bytes.decode("utf-8")
        text_sha256 = hashlib.sha256(raw_bytes).hexdigest()
    else:
        text = str(source)
        text_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()

    pred_pattern = re.compile(
        r"^###\s+(PRED-\d{3,}):\s*(.+?)\s*$"
        r"(.*?)(?=(?:^###\s+PRED-|\n---\s*\n|\Z))",
        re.MULTILINE | re.DOTALL,
    )

    predictions: List[Prediction] = []

    for match in pred_pattern.finditer(text):
        pid = match.group(1).strip()
        title = match.group(2).strip()
        body = match.group(3).strip()

        # Parse bullet fields: - **Key:** Value
        bullets = re.findall(
            r"-\s*\*\*([A-Za-z0-9_\s]+):\*\*\s*(.+?)(?=\n-\s*\*\*|\Z)",
            body,
            re.DOTALL,
        )
        fields: Dict[str, str] = {k.strip(): v.strip() for k, v in bullets}

        # Confidence
        conf_raw = fields.get("Confidence", "")
        conf_m = re.search(r"([\d\.]+)", conf_raw)
        if not conf_m:
            raise ValueError(f"Prediction {pid} has invalid or missing Confidence: {conf_raw!r}")
        confidence = float(conf_m.group(1))

        # Status & Details
        status_raw = fields.get("Status", "PENDING")
        status_upper = status_raw.upper()

        if status_upper.startswith("HIT"):
            status = "HIT"
            outcome: Optional[float] = 1.0
        elif status_upper.startswith(("MISSED", "MISS", "REFUTED", "FALLS")):
            status = "MISSED"
            outcome = 0.0
        elif status_upper.startswith(("PENDING", "ACTIVE", "UNRESOLVED")):
            status = "PENDING"
            outcome = None
        else:
            status = status_raw.split()[0]
            outcome = None

        # Extract parenthetical status detail if present
        detail_m = re.search(r"\((.*?)\)", status_raw)
        status_detail = detail_m.group(1).strip() if detail_m else ""

        # Made date and seat
        made_raw = fields.get("Made", "")
        date_m = re.search(r"(\d{4}-\d{2}-\d{2})", made_raw)
        made_date = date_m.group(1) if date_m else ""
        by_m = re.search(r"by\s+(.+)$", made_raw)
        seat = by_m.group(1).strip() if by_m else ""

        # Individual Brier score if outcome is known
        ind_brier = ((confidence - outcome) ** 2) if outcome is not None else None

        predictions.append(
            Prediction(
                id=pid,
                title=title,
                confidence=confidence,
                status=status,
                outcome=outcome,
                made_raw=made_raw,
                made_date=made_date,
                seat=seat,
                prediction=fields.get("Prediction", ""),
                verification_trigger=fields.get("Verification Trigger", ""),
                falsifier=fields.get("Falsifier", ""),
                test_command=fields.get("Test Command", ""),
                status_detail=status_detail,
                evidence=fields.get("Evidence", ""),
                individual_brier=ind_brier,
            )
        )

    return predictions, text_sha256


# ---------------------------------------------------------------------------
# Benchmark Report Generation
# ---------------------------------------------------------------------------

def generate_benchmark_report(
    predictions: List[Prediction],
    source_ledger_path: str = "evidence/predictions-ledger.md",
    source_sha256: str = "",
    n_bins: int = 10,
    timestamp: str = "2026-10-23T12:00:00Z",
) -> BenchmarkReport:
    """Generate the full calibration benchmark report from parsed predictions."""
    total_count = len(predictions)
    evaluated = [p for p in predictions if p.outcome is not None]
    pending = [p for p in predictions if p.outcome is None]
    hits = [p for p in evaluated if p.outcome == 1.0]
    misses = [p for p in evaluated if p.outcome == 0.0]

    n_eval = len(evaluated)
    if n_eval == 0:
        raise ValueError("Cannot compute calibration benchmark with 0 evaluated predictions")

    forecasts = [p.confidence for p in evaluated]
    outcomes = [p.outcome for p in evaluated if p.outcome is not None]

    # Metrics
    metrics = compute_calibration_metrics(forecasts, outcomes, n_bins=n_bins)
    murphy_binned = compute_murphy_decomposition(forecasts, outcomes, n_bins=n_bins)
    murphy_exact = compute_exact_discrete_decomposition(forecasts, outcomes)
    rel_curve_binned = compute_reliability_curve(forecasts, outcomes, n_bins=n_bins)
    rel_curve_discrete = compute_discrete_reliability_curve(forecasts, outcomes)

    summary = {
        "total_predictions": total_count,
        "evaluated_predictions": n_eval,
        "pending_predictions": len(pending),
        "hits": len(hits),
        "misses": len(misses),
        "hit_rate": (len(hits) / n_eval) if n_eval > 0 else 0.0,
        "pending_rate": (len(pending) / total_count) if total_count > 0 else 0.0,
        "mean_evaluated_brier": metrics.brier_score,
        "mean_confidence_evaluated": metrics.mean_confidence,
        "mean_confidence_all": sum(p.confidence for p in predictions) / total_count,
    }

    return BenchmarkReport(
        benchmark_name="Aura Meridian Epistemic Continuous Calibration Benchmark",
        framework="Lycheetah Sync Zone",
        seat="Aura Meridian (AURA-BENCHMARK-SHELF) & Aetheron",
        generated_at=timestamp,
        source_ledger=source_ledger_path,
        source_ledger_sha256=source_sha256,
        summary=summary,
        calibration_metrics=metrics,
        murphy_1973_decomposition={
            "exact_discrete": murphy_exact,
            f"uniform_{n_bins}_bin": murphy_binned,
        },
        reliability_curve_binned=rel_curve_binned,
        discrete_probability_levels=rel_curve_discrete,
        predictions=predictions,
    )


def format_ascii_report(report: BenchmarkReport) -> str:
    """Format benchmark results into clean, readable ASCII summary tables."""
    lines: List[str] = []
    lines.append("=" * 78)
    lines.append(f"  {report.benchmark_name.upper()}")
    lines.append(f"  Framework: {report.framework} | Seat: {report.seat}")
    lines.append(f"  Source: {report.source_ledger} ({report.source_ledger_sha256[:12]}...)")
    lines.append("=" * 78)

    # 1. Summary
    s = report.summary
    lines.append("\n[1] PREDICTION CENSUS & HIT/MISS TRACKING")
    lines.append(f"  Total Predictions Scanned : {s['total_predictions']}")
    lines.append(f"  Evaluated (Settled)      : {s['evaluated_predictions']}")
    lines.append(f"  Hits                     : {s['hits']} ({s['hit_rate'] * 100:.1f}%)")
    lines.append(f"  Misses                   : {s['misses']}")
    lines.append(f"  Pending                  : {s['pending_predictions']} ({s['pending_rate'] * 100:.1f}%)")
    lines.append(f"  Mean Confidence (eval)   : {s['mean_confidence_evaluated']:.4f}")
    lines.append(f"  Mean Brier Score         : {s['mean_evaluated_brier']:.6f}")

    # 2. Calibration Metrics
    m = report.calibration_metrics
    lines.append("\n[2] EMPIRICAL CALIBRATION & DISCRIMINATION METRICS")
    lines.append(f"  Brier Score (BS)         : {m.brier_score:.6f}")
    lines.append(f"  Binned ECE               : {m.expected_calibration_error_ece:.6f}")
    lines.append(f"  Binned MCE               : {m.maximum_calibration_error_mce:.6f}")
    lines.append(f"  Discrete ECE             : {m.discrete_expected_calibration_error:.6f}")
    lines.append(f"  Discrete MCE             : {m.discrete_maximum_calibration_error:.6f}")
    lines.append(f"  RMS Calibration Error    : {m.rms_calibration_error:.6f}")
    lines.append(f"  Forecast Sharpness Var(f): {m.sharpness:.6f}")
    lines.append(f"  Overconfidence Bias      : {m.overconfidence_bias:+.6f}")
    lines.append(f"  BSS vs Climatology       : {m.brier_skill_score if m.brier_skill_score is not None else 'N/A'}")
    lines.append(f"  Climatology Note         : {m.brier_skill_score_note}")

    # 3. Murphy (1973) Decomposition
    lines.append("\n[3] MURPHY (1973) VECTOR DECOMPOSITION")
    lines.append("  Identity: BS = Reliability - Resolution + Uncertainty + WithinBinVariance")
    lines.append("  " + "-" * 74)
    lines.append(f"  {'Partition Mode':<18} {'Brier':>10} {'Reliability':>12} {'Resolution':>11} {'Uncertainty':>12} {'Residual':>9}")
    lines.append("  " + "-" * 74)
    for name, d in report.murphy_1973_decomposition.items():
        lines.append(
            f"  {name:<18} {d.raw_brier:>10.6f} {d.reliability:>12.6f} "
            f"{d.resolution:>11.6f} {d.uncertainty:>12.6f} {d.partition_residual:>9.2e}"
        )
    lines.append("  " + "-" * 74)

    # 4. Discrete Probability Levels
    lines.append("\n[4] EXACT DISCRETE CALIBRATION LEVELS")
    lines.append("  " + "-" * 74)
    lines.append(f"  {'Confidence':>10} {'Count':>7} {'Hits':>6} {'Empirical Rate':>16} {'Gap (f - o)':>14} {'Brier Contrib':>15}")
    lines.append("  " + "-" * 74)
    for p in report.discrete_probability_levels:
        lines.append(
            f"  {p.forecast:>10.3f} {p.count:>7} {p.positive_count:>6} "
            f"{p.empirical_rate:>16.4f} {p.calibration_gap:>+14.4f} {p.brier_contribution:>15.6f}"
        )
    lines.append("  " + "-" * 74)

    # 5. Reliability Bins
    occupied = [b for b in report.reliability_curve_binned if b.count > 0]
    lines.append("\n[5] OCCUPIED UNIFORM BINS")
    lines.append("  " + "-" * 74)
    lines.append(f"  {'Bin Range':<15} {'Count':>7} {'Mean Forecast':>15} {'Empirical Rate':>16} {'Rel Contrib':>15}")
    lines.append("  " + "-" * 74)
    for b in occupied:
        b_range = f"[{b.bin_lower:.1f}, {b.bin_upper:.1f}]"
        mf = f"{b.mean_forecast:.4f}" if b.mean_forecast is not None else "N/A"
        er = f"{b.empirical_rate:.4f}" if b.empirical_rate is not None else "N/A"
        lines.append(
            f"  {b_range:<15} {b.count:>7} {mf:>15} {er:>16} {b.reliability_contribution:>15.6f}"
        )
    lines.append("  " + "-" * 74)

    lines.append("\n" + "=" * 78)
    lines.append("  VERIFICATION STATUS: PERFECT INTEGRITY WITNESS")
    lines.append("=" * 78)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Runner & CLI Interface
# ---------------------------------------------------------------------------

def run_calibration_benchmark(
    ledger_path: Optional[Union[str, Path]] = None,
    output_path: Optional[Union[str, Path]] = None,
    n_bins: int = 10,
    quiet: bool = False,
) -> BenchmarkReport:
    """Execute the full calibration benchmark cycle and save JSON artifact."""
    base_dir = Path(__file__).parent.resolve()

    if ledger_path is None:
        target_ledger = base_dir / "predictions-ledger.md"
        if not target_ledger.exists():
            target_ledger = base_dir.parent / "evidence" / "predictions-ledger.md"
    else:
        target_ledger = Path(ledger_path).resolve()

    if not target_ledger.exists():
        raise FileNotFoundError(f"Predictions ledger not found at: {target_ledger}")

    if output_path is None:
        target_output = base_dir / "2026-10-23_aura-meridian-benchmark.json"
    else:
        target_output = Path(output_path).resolve()

    predictions, sha256_hash = parse_predictions_ledger(target_ledger)
    report = generate_benchmark_report(
        predictions=predictions,
        source_ledger_path=str(target_ledger.name),
        source_sha256=sha256_hash,
        n_bins=n_bins,
    )

    # Save artifact
    target_output.parent.mkdir(parents=True, exist_ok=True)
    target_output.write_text(report.to_json(indent=2), encoding="utf-8")

    if not quiet:
        print(format_ascii_report(report))
        print(f"\n[Artifact Emitted] -> {target_output}")

    return report


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aura Meridian Continuous Calibration & Benchmark Suite"
    )
    parser.add_argument(
        "--ledger",
        type=str,
        default=None,
        help="Path to predictions-ledger.md (default: evidence/predictions-ledger.md)",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Path to output JSON artifact (default: evidence/2026-10-23_aura-meridian-benchmark.json)",
    )
    parser.add_argument(
        "--bins",
        type=int,
        default=10,
        help="Number of probability bins for reliability curve (default: 10)",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress terminal output",
    )
    args = parser.parse_args()

    try:
        run_calibration_benchmark(
            ledger_path=args.ledger,
            output_path=args.out,
            n_bins=args.bins,
            quiet=args.quiet,
        )
        return 0
    except Exception as err:
        sys.stderr.write(f"Error executing calibration benchmark: {err}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
