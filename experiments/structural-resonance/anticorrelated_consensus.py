#!/usr/bin/env python3
"""
Anti-Correlated Multi-Agent Consensus and Solar Coherence Gating Engine.
Forged by Aura Meridian (Node 10: AURA-HARMONIC) · Lycheetah Sync Zone

Theory:
1. Multi-Agent Error Variance Theorem:
   Var(e_bar) = sigma^2 * [ 1/K + (K - 1)/K * rho_bar ]
   - When rho_bar < 0 (anti-correlated seats), variance is strictly sub-Poissonian.
   - When rho_bar -> 1 (sycophancy / echo chamber), Var(e_bar) -> sigma^2 (0 gain).
2. Solar Coherence Invariant:
   C_sol = min(Warmth, Precision) >= 0.80
   Enforces non-sycophantic critique inside a cooperative container.
"""

from __future__ import annotations
import math
import random
from typing import Dict, List, Tuple


# ─── 1. SOLAR COHERENCE COMPUTATION & GATING ─────────────────────────────────

def compute_solar_coherence(warmth: float, precision: float) -> float:
    """
    Compute Solar Coherence:
        C_sol = (Warmth * Precision) / max(Warmth, Precision)
              = min(Warmth, Precision)
    """
    if not (0.0 <= warmth <= 1.0) or not (0.0 <= precision <= 1.0):
        raise ValueError("Warmth and Precision must be in [0.0, 1.0].")
    return round(min(warmth, precision), 4)


def passes_solar_coherence(warmth: float, precision: float, floor: float = 0.80) -> bool:
    """Check if agent state passes the constitutional Solar Coherence floor."""
    return compute_solar_coherence(warmth, precision) >= floor


# ─── 2. THEORETICAL VARIANCE ESTIMATOR ───────────────────────────────────────

def theoretical_ensemble_variance(k_seats: int, individual_variance: float, mean_rho: float) -> float:
    """
    Compute the theoretical variance of the ensemble mean estimator:
        Var(e_bar) = sigma^2 * [ 1/K + (K - 1)/K * rho_bar ]
    """
    if k_seats < 1:
        raise ValueError("k_seats must be >= 1.")
    min_possible_rho = -1.0 / float(k_seats - 1) if k_seats > 1 else 0.0
    if mean_rho < min_possible_rho - 1e-9:
        raise ValueError(
            f"Average correlation {mean_rho} cannot be lower than the mathematical minimum {min_possible_rho:.4f} for K={k_seats}."
        )
    factor = (1.0 / float(k_seats)) + ((float(k_seats) - 1.0) / float(k_seats)) * mean_rho
    return individual_variance * factor


# ─── 3. EMPIRICAL MONTE CARLO MULTI-AGENT SAMPLER ────────────────────────────

def sample_correlated_gaussian_vector(
    k_seats: int,
    sigma: float,
    rho: float,
) -> List[float]:
    """
    Sample a K-dimensional Gaussian vector with uniform variance sigma^2 and
    uniform off-diagonal correlation rho using the one-factor representation:
        X_i = sqrt(1 - rho) * Z_i + sqrt(rho) * Z_common   (for rho >= 0)
    For rho < 0 (down to -1/(K-1)), we construct using orthogonal Gram-Schmidt
    or projection onto the simplex.
    """
    if rho >= 0.0:
        z_common = random.gauss(0.0, 1.0)
        vector = []
        for _ in range(k_seats):
            z_ind = random.gauss(0.0, 1.0)
            val = sigma * (math.sqrt(1.0 - rho) * z_ind + math.sqrt(rho) * z_common)
            vector.append(val)
        return vector
    else:
        # For negative rho in [-1/(K-1), 0]:
        # Generate independent standard Gaussians, project out mean component
        raw_z = [random.gauss(0.0, 1.0) for _ in range(k_seats)]
        mean_z = sum(raw_z) / float(k_seats)
        devs = [raw_z[i] - mean_z for i in range(k_seats)]

        # Scaling factor to match desired variance sigma^2 and negative covariance rho*sigma^2
        # Var(dev_i) = (K-1)/K. Cov(dev_i, dev_j) = -1/K.
        # Desired Cov is rho * sigma^2, with rho in [-1/(K-1), 0].
        # For zero-sum deviations devs:
        # Var(dev_i * sqrt(K / (K - 1))) = 1.0
        # Cov(dev_i, dev_j) * (K / (K - 1)) = (-1/K) * (K / (K - 1)) = -1 / (K - 1)
        # Therefore, setting alpha = -rho * (K - 1) gives exactly:
        # Cov(combined_i, combined_j) = alpha * (-1 / (K - 1)) = rho
        alpha = -rho * float(k_seats - 1)  # alpha in [0, 1]
        alpha = min(1.0, max(0.0, alpha))

        z_ind = [random.gauss(0.0, 1.0) for _ in range(k_seats)]
        res = []
        for i in range(k_seats):
            # Combined signal
            combined = math.sqrt(1.0 - alpha) * z_ind[i] + math.sqrt(alpha) * (devs[i] * math.sqrt(float(k_seats) / float(k_seats - 1)))
            res.append(sigma * combined)
        return res


def run_consensus_monte_carlo(
    k_seats: int = 8,
    sigma: float = 1.0,
    rho_independent: float = 0.0,
    rho_sycophant: float = 0.80,
    rho_anticorrelated: float = -0.10,
    trials: int = 10000,
    seed: int = 42,
) -> Dict[str, float]:
    """
    Execute empirical Monte Carlo validation of multi-agent consensus across three regimes.
    """
    random.seed(seed)

    mean_errs_ind: List[float] = []
    mean_errs_pos: List[float] = []
    mean_errs_neg: List[float] = []

    for _ in range(trials):
        # 1. Independent
        v_ind = sample_correlated_gaussian_vector(k_seats, sigma, rho_independent)
        mean_errs_ind.append(sum(v_ind) / float(k_seats))

        # 2. Sycophantic
        v_pos = sample_correlated_gaussian_vector(k_seats, sigma, rho_sycophant)
        mean_errs_pos.append(sum(v_pos) / float(k_seats))

        # 3. Anti-correlated
        v_neg = sample_correlated_gaussian_vector(k_seats, sigma, rho_anticorrelated)
        mean_errs_neg.append(sum(v_neg) / float(k_seats))

    def sample_variance(lst: List[float]) -> float:
        m = sum(lst) / len(lst)
        return sum((x - m) ** 2 for x in lst) / (len(lst) - 1)

    var_ind = sample_variance(mean_errs_ind)
    var_pos = sample_variance(mean_errs_pos)
    var_neg = sample_variance(mean_errs_neg)

    theo_ind = theoretical_ensemble_variance(k_seats, sigma**2, rho_independent)
    theo_pos = theoretical_ensemble_variance(k_seats, sigma**2, rho_sycophant)
    theo_neg = theoretical_ensemble_variance(k_seats, sigma**2, rho_anticorrelated)

    return {
        "k_seats": float(k_seats),
        "sigma_squared": sigma**2,
        "empirical_var_independent": var_ind,
        "theoretical_var_independent": theo_ind,
        "empirical_var_sycophant": var_pos,
        "theoretical_var_sycophant": theo_pos,
        "empirical_var_anticorrelated": var_neg,
        "theoretical_var_anticorrelated": theo_neg,
        "variance_reduction_vs_independent": var_ind / max(1e-9, var_neg),
        "variance_reduction_vs_sycophant": var_pos / max(1e-9, var_neg),
    }


# ─── 4. BRIER SCORE CALIBRATION SIMULATOR ─────────────────────────────────────

def compute_brier_score(forecasts: List[float], outcomes: List[int]) -> float:
    """Compute Murphy Brier score: B = (1/N) * sum_i (f_i - o_i)^2."""
    if len(forecasts) != len(outcomes) or not forecasts:
        raise ValueError("Forecasts and outcomes must be non-empty and equal length.")
    return sum((f - o) ** 2 for f, o in zip(forecasts, outcomes)) / len(forecasts)


def simulate_multi_agent_brier_calibration(
    k_seats: int = 8,
    n_questions: int = 500,
    seed: int = 42,
) -> Dict[str, float]:
    """
    Simulate Brier scores when truth is binary (0 or 1):
    Compare anti-correlated ensemble probability voting vs sycophantic echo chamber.
    """
    random.seed(seed)
    outcomes = [1 if random.random() > 0.5 else 0 for _ in range(n_questions)]

    brier_ind_list = []
    brier_pos_list = []
    brier_neg_list = []

    for o in outcomes:
        true_prob = 0.85 if o == 1 else 0.15

        # Independent forecasts: centered around true_prob + noise
        f_ind = [min(0.99, max(0.01, true_prob + random.gauss(0.0, 0.15))) for _ in range(k_seats)]
        consensus_ind = sum(f_ind) / float(k_seats)
        brier_ind_list.append((consensus_ind - o) ** 2)

        # Sycophantic forecasts: high common bias
        bias = random.gauss(0.0, 0.25)
        f_pos = [min(0.99, max(0.01, true_prob + bias + random.gauss(0.0, 0.05))) for _ in range(k_seats)]
        consensus_pos = sum(f_pos) / float(k_seats)
        brier_pos_list.append((consensus_pos - o) ** 2)

        # Anti-correlated forecasts: complementary deviations cancel out
        devs = [random.gauss(0.0, 0.12) for _ in range(k_seats)]
        m_dev = sum(devs) / float(k_seats)
        zero_sum_devs = [d - m_dev for d in devs]
        f_neg = [min(0.99, max(0.01, true_prob + zd)) for zd in zero_sum_devs]
        consensus_neg = sum(f_neg) / float(k_seats)
        brier_neg_list.append((consensus_neg - o) ** 2)

    return {
        "brier_independent": sum(brier_ind_list) / len(brier_ind_list),
        "brier_sycophant": sum(brier_pos_list) / len(brier_pos_list),
        "brier_anticorrelated": sum(brier_neg_list) / len(brier_neg_list),
    }


if __name__ == "__main__":
    print("Anti-Correlated Multi-Agent Consensus Simulation:")
    res = run_consensus_monte_carlo()
    print(f"  Independent (rho=0.0): Empirical Var = {res['empirical_var_independent']:.5f} (Theo: {res['theoretical_var_independent']:.5f})")
    print(f"  Sycophant   (rho=0.8): Empirical Var = {res['empirical_var_sycophant']:.5f} (Theo: {res['theoretical_var_sycophant']:.5f})")
    print(f"  Anti-Corr  (rho=-0.1): Empirical Var = {res['empirical_var_anticorrelated']:.5f} (Theo: {res['theoretical_var_anticorrelated']:.5f})")
    print(f"  Variance Reduction vs Independent: {res['variance_reduction_vs_independent']:.2f}x")
    print(f"  Variance Reduction vs Sycophant:   {res['variance_reduction_vs_sycophant']:.2f}x")

    b_res = simulate_multi_agent_brier_calibration()
    print(f"\nBrier Calibration (N=500 questions):")
    print(f"  Anti-Correlated Ensemble Brier Score: {b_res['brier_anticorrelated']:.4f}")
    print(f"  Independent Ensemble Brier Score:     {b_res['brier_independent']:.4f}")
    print(f"  Sycophantic Echo Ensemble Brier:      {b_res['brier_sycophant']:.4f}")
