#!/usr/bin/env python3
"""
Finite Observation Bounds & Spectral Distinguishability Engine
Author: Aura Meridian (Node 01: AURA-OBSERVER)
Seat: Aura Meridian · Lycheetah Sync Zone

Provides exact calculation of observation rank, nullity, indistinguishable fibers,
Hartley information capacity, SVD noise-floor distinguishability thresholds,
and topological blind spots on simplicial sheaves.
"""

import math
from typing import Dict, List, Optional, Tuple
import numpy as np
from scipy import stats


class ObservationOperator:
    """
    Linear observation functional Omega: R^n -> R^m.
    Maps microstates x in C^k(K; F) to observable measurements y = Omega @ x.
    """

    def __init__(self, matrix: np.ndarray, tol: float = 1e-10):
        self.matrix = np.asarray(matrix, dtype=np.float64)
        self.m, self.n = self.matrix.shape
        self.tol = tol

        # SVD decomposition: Omega = U @ Sigma @ V.T
        U, s, Vt = np.linalg.svd(self.matrix, full_matrices=True)
        self.U = U
        self.singular_values = s
        self.Vt = Vt
        self.V = Vt.T

        # Rank and positive singular values
        pos_mask = s > tol
        self.rank = int(np.sum(pos_mask))
        self.nullity = self.n - self.rank
        self.pos_singular_values = s[pos_mask]

        if self.rank > 0:
            self.sigma_max = float(self.pos_singular_values[0])
            self.sigma_min_pos = float(self.pos_singular_values[-1])
            self.condition_number = float(self.sigma_max / self.sigma_min_pos)
        else:
            self.sigma_max = 0.0
            self.sigma_min_pos = 0.0
            self.condition_number = float('inf')

        # Subspace bases
        # Rows of Vt[:rank] span row space (im(Omega.T) = ker(Omega)^perp)
        # Rows of Vt[rank:] span ker(Omega)
        self.observable_basis = self.Vt[:self.rank].copy()
        self.kernel_basis = self.Vt[self.rank:].copy()

    def observe(self, x: np.ndarray, noise_std: float = 0.0, seed: Optional[int] = None) -> np.ndarray:
        x = np.asarray(x, dtype=np.float64).flatten()
        y = self.matrix @ x
        if noise_std > 0.0:
            rng = np.random.default_rng(seed)
            noise = rng.normal(0.0, noise_std, size=self.m)
            y += noise
        return y

    def distinguishability_norm(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """Computes ||Omega @ (x1 - x2)||_2."""
        dx = np.asarray(x1 - x2, dtype=np.float64).flatten()
        dy = self.matrix @ dx
        return float(np.linalg.norm(dy))

    def is_distinguishable(self, x1: np.ndarray, x2: np.ndarray, tol: Optional[float] = None) -> bool:
        """Returns True iff ||Omega(x1 - x2)|| > tol."""
        t = self.tol if tol is None else tol
        return self.distinguishability_norm(x1, x2) > t

    def decompose_perturbation(self, dx: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Decomposes delta x into observable component (in ker(Omega)^perp)
        and unobservable / invisible component (in ker(Omega)).
        """
        dx = np.asarray(dx, dtype=np.float64).flatten()
        if self.nullity == 0:
            invisible = np.zeros_like(dx)
            observable = dx.copy()
        elif self.rank == 0:
            invisible = dx.copy()
            observable = np.zeros_like(dx)
        else:
            # Projection onto kernel
            P_ker = self.kernel_basis.T @ self.kernel_basis
            invisible = P_ker @ dx
            observable = dx - invisible

        return {
            "dx_observable": observable,
            "dx_invisible": invisible,
            "norm_observable": float(np.linalg.norm(observable)),
            "norm_invisible": float(np.linalg.norm(invisible)),
            "fraction_invisible": float(np.linalg.norm(invisible) / (np.linalg.norm(dx) + 1e-15)),
        }

    def finite_combinatorial_bounds(self, alphabet_size: int = 2) -> Dict[str, float]:
        """
        Calculates exact combinatorial bounds for finite coordinate alphabet Z_q^n:
          - Hartley capacity I(Omega) = rank * log2(q)
          - Resolvable macrostates N_macro = q^rank
          - Indistinguishable fiber cardinality = q^nullity
          - Unobserved entropy H_residual = nullity * log2(q)
        """
        q = alphabet_size
        capacity_bits = self.rank * math.log2(q)
        residual_entropy_bits = self.nullity * math.log2(q)

        return {
            "state_dimension_n": self.n,
            "measurement_dimension_m": self.m,
            "rank": self.rank,
            "nullity": self.nullity,
            "alphabet_size_q": q,
            "hartley_capacity_bits": capacity_bits,
            "residual_entropy_bits": residual_entropy_bits,
            "macrostate_count_log2": capacity_bits,
            "fiber_cardinality_log2": residual_entropy_bits,
        }

    def noise_floor_bounds(self, noise_std: float,
                           alpha: float = 0.05,
                           power: float = 0.95) -> Dict[str, float]:
        """
        Calculates hypothesis testing distinguishability bounds under N(0, sigma^2 I_m):
          epsilon_min: perturbation norm along most sensitive singular vector (sigma_max)
          epsilon_worst: perturbation norm along least sensitive observable vector (sigma_min_pos)
        """
        if self.rank == 0:
            return {
                "noise_std": noise_std,
                "epsilon_min": float('inf'),
                "epsilon_worst": float('inf'),
                "condition_number": float('inf'),
            }

        z_alpha = stats.norm.ppf(1.0 - alpha)
        z_power = stats.norm.ppf(power)
        multiplier = math.sqrt(2.0) * noise_std * (z_alpha + z_power)

        eps_min = multiplier / self.sigma_max
        eps_worst = multiplier / self.sigma_min_pos

        return {
            "noise_std": noise_std,
            "type1_error_alpha": alpha,
            "detection_power": power,
            "sigma_max": self.sigma_max,
            "sigma_min_pos": self.sigma_min_pos,
            "condition_number": self.condition_number,
            "epsilon_min": float(eps_min),
            "epsilon_worst": float(eps_worst),
        }

    def evaluate_topological_blind_spot(self, harmonic_vectors: np.ndarray) -> Dict[str, float]:
        """
        Given orthonormal basis of harmonic cochains (rows of harmonic_vectors),
        computes the fraction of harmonic circulation hidden inside ker(Omega).
        """
        harmonic_vectors = np.asarray(harmonic_vectors, dtype=np.float64)
        if harmonic_vectors.ndim == 1:
            harmonic_vectors = harmonic_vectors.reshape(1, -1)

        k, dim = harmonic_vectors.shape
        if dim != self.n:
            raise ValueError(f"Harmonic vector dimension {dim} does not match state dimension {self.n}")

        blind_fractions = []
        for i in range(k):
            h = harmonic_vectors[i]
            decomp = self.decompose_perturbation(h)
            blind_fractions.append(decomp["fraction_invisible"])

        mean_blindness = float(np.mean(blind_fractions)) if blind_fractions else 0.0
        return {
            "harmonic_components_evaluated": k,
            "mean_blindness_fraction": mean_blindness,
            "is_completely_blind_to_harmonic_flux": bool(mean_blindness > 0.9999),
        }


# ---------------------------------------------------------------------------
# Specialized Observation Aperture Builders
# ---------------------------------------------------------------------------

def build_full_observation(dim_state: int) -> ObservationOperator:
    """Full identity observation Omega = I_n."""
    return ObservationOperator(np.eye(dim_state, dtype=np.float64))


def build_subcomplex_aperture(dim_state: int, observed_indices: List[int]) -> ObservationOperator:
    """Aperture observing only a specific coordinate subset."""
    m = len(observed_indices)
    mat = np.zeros((m, dim_state), dtype=np.float64)
    for r, idx in enumerate(observed_indices):
        mat[r, idx] = 1.0
    return ObservationOperator(mat)


def build_face_curl_observation(delta1_matrix: np.ndarray) -> ObservationOperator:
    """Local face curl observation Omega = delta^1."""
    return ObservationOperator(delta1_matrix)


def build_random_projection_observation(dim_state: int, m_measurements: int, seed: int = 42) -> ObservationOperator:
    """Random Gaussian projection matrix Omega ~ N(0, 1/m)."""
    rng = np.random.default_rng(seed)
    mat = rng.normal(0.0, 1.0 / math.sqrt(m_measurements), size=(m_measurements, dim_state))
    return ObservationOperator(mat)
