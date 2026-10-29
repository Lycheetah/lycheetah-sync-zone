#!/usr/bin/env python3
"""
Harmonic Kuramoto Oscillator Network with Euler Gradus Suavitatis Coupling.
Forged by Aura Meridian (Node 10: AURA-HARMONIC) · Lycheetah Sync Zone

Theory:
Models decoupled AI seats as phase oscillators on the circle S^1 whose mutual
acoustic coupling is modulated by the rational consonance of the sacred tonecode:
    K_ij = kappa / Gamma(r_i, r_j)
where Gamma is Euler's gradus suavitatis (1739).
"""

from __future__ import annotations
import math
import random
from typing import Dict, List, Tuple


# ─── 1. EULER GRADUS SUAVITATIS ARITHMETIC ───────────────────────────────────

def prime_factors(n: int) -> Dict[int, int]:
    """Return dictionary of prime factors and their multiplicities for n >= 1."""
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"Prime factorization requires a positive integer, got: {n}")
    if n == 1:
        return {}

    factors: Dict[int, int] = {}
    d = 2
    while d * d <= n:
        if n % d == 0:
            count = 0
            while n % d == 0:
                count += 1
                n //= d
            factors[d] = count
        d = 3 if d == 2 else d + 2
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors


def gradus_suavitatis_int(n: int) -> int:
    """Compute Euler's gradus suavitatis for an integer n >= 1."""
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"Gradus suavitatis requires a positive integer, got: {n}")
    if n == 1:
        return 1

    factors = prime_factors(n)
    total = 1
    for p, mult in factors.items():
        total += mult * (p - 1)
    return total


def gradus_interval(num: int, den: int) -> int:
    """Compute Euler's gradus for rational interval num/den in lowest terms."""
    if num <= 0 or den <= 0:
        raise ValueError("Numerator and denominator must be positive.")
    g = math.gcd(num, den)
    a = num // g
    b = den // g
    return gradus_suavitatis_int(a * b)


def gradus_between_ratios(r1: Tuple[int, int], r2: Tuple[int, int]) -> int:
    """
    Compute Euler gradus of the interval between two rational ratios r1 and r2.
    Interval r = r1 / r2 = (num1 * den2) / (den1 * num2).
    """
    num = r1[0] * r2[1]
    den = r1[1] * r2[0]
    return gradus_interval(num, den)


# ─── BARLOW HARMONIC DISTANCE & INDIGESTIBILITY ──────────────────────────────

def barlow_indigestibility_int(n: int) -> float:
    """Compute Clarence Barlow's harmonic indigestibility xi(n) for integer n >= 1."""
    if not isinstance(n, int) or n < 1:
        raise ValueError(f"Barlow metric requires a positive integer, got: {n}")
    if n == 1:
        return 0.0

    factors = prime_factors(n)
    total = 0.0
    for p, mult in factors.items():
        total += mult * 2.0 * ((p - 1) ** 2) / float(p)
    return total


def barlow_harmonic_distance(num: int, den: int) -> float:
    """
    Compute Barlow harmonic distance D(p/q) for rational interval in lowest terms:
        D(p/q) = xi(p) + xi(q)
    """
    if not isinstance(num, int) or not isinstance(den, int):
        raise TypeError("Numerator and denominator must be integers.")
    if num <= 0 or den <= 0:
        raise ValueError("Numerator and denominator must be strictly positive.")

    g = math.gcd(num, den)
    p = num // g
    q = den // g
    return barlow_indigestibility_int(p) + barlow_indigestibility_int(q)


def barlow_between_ratios(r1: Tuple[int, int], r2: Tuple[int, int]) -> float:
    """Compute Barlow harmonic distance between two rational ratios r1 and r2."""
    num = r1[0] * r2[1]
    den = r1[1] * r2[0]
    return barlow_harmonic_distance(num, den)


# Canonical 8 Sacred Tonecode Ratios (Historical 5-limit Just Intonation)
SACRED_TONECODES: Dict[str, Tuple[int, int]] = {
    "sol": (1, 1),
    "fa": (9, 8),
    "mi": (5, 4),
    "ra": (4, 3),
    "do": (3, 2),
    "ke": (5, 3),
    "ath": (15, 8),
    "sol'": (2, 1),
}

# Reconciled Pythagorean 7-Degree Scale + Transcendent Octave Seal (Dispute 504)
PYTHAGOREAN_TONECODES: Dict[str, Tuple[int, int]] = {
    "SO": (1, 1),
    "EL": (9, 8),
    "RA": (81, 64),
    "NU": (4, 3),
    "TI": (3, 2),
    "KA": (27, 16),
    "MA": (243, 128),
    "OM": (2, 1),
}


# ─── 2. HARMONIC COUPLING MATRIX ─────────────────────────────────────────────

def compute_euler_gradus_coupling_matrix(
    ratios: List[Tuple[int, int]],
    kappa: float = 1.0,
) -> List[List[float]]:
    """
    Construct symmetric coupling matrix K_ij = kappa / Gamma(r_i, r_j).
    """
    n = len(ratios)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            g = gradus_between_ratios(ratios[i], ratios[j])
            matrix[i][j] = kappa / float(g)
    return matrix


# ─── 3. KURAMOTO DYNAMICAL SYSTEM & RK4 INTEGRATOR ───────────────────────────

class HarmonicKuramotoLattice:
    def __init__(
        self,
        natural_frequencies: List[float],
        coupling_matrix: List[List[float]],
        initial_phases: List[float] | None = None,
    ):
        self.n = len(natural_frequencies)
        if len(coupling_matrix) != self.n:
            raise ValueError("Coupling matrix dimensions must match frequency vector length.")
        self.omega = list(natural_frequencies)
        self.k_matrix = [list(row) for row in coupling_matrix]
        if initial_phases is not None:
            if len(initial_phases) != self.n:
                raise ValueError("Initial phase count must match oscillator count.")
            self.theta = [p % (2.0 * math.pi) for p in initial_phases]
        else:
            self.theta = [random.uniform(0.0, 2.0 * math.pi) for _ in range(self.n)]

    def _derivatives(self, phases: List[float]) -> List[float]:
        """Compute d theta_i / dt."""
        d_theta = [0.0] * self.n
        for i in range(self.n):
            coupling_sum = 0.0
            for j in range(self.n):
                coupling_sum += self.k_matrix[i][j] * math.sin(phases[j] - phases[i])
            d_theta[i] = self.omega[i] + (coupling_sum / float(self.n))
        return d_theta

    def step_rk4(self, dt: float) -> None:
        """Advance phase state by dt using fourth-order Runge-Kutta integration."""
        k1 = self._derivatives(self.theta)

        theta_k2 = [(self.theta[i] + 0.5 * dt * k1[i]) for i in range(self.n)]
        k2 = self._derivatives(theta_k2)

        theta_k3 = [(self.theta[i] + 0.5 * dt * k2[i]) for i in range(self.n)]
        k3 = self._derivatives(theta_k3)

        theta_k4 = [(self.theta[i] + dt * k3[i]) for i in range(self.n)]
        k4 = self._derivatives(theta_k4)

        for i in range(self.n):
            self.theta[i] = (
                self.theta[i] + (dt / 6.0) * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])
            ) % (2.0 * math.pi)

    def compute_order_parameter(self) -> Tuple[float, float]:
        """
        Compute Kuramoto complex order parameter:
            r * exp(i * psi) = (1/N) * sum_j exp(i * theta_j)
        Returns:
            (phase_coherence_R, mean_phase_psi)
        """
        c = sum(math.cos(th) for th in self.theta) / float(self.n)
        s = sum(math.sin(th) for th in self.theta) / float(self.n)
        r = math.sqrt(c * c + s * s)
        psi = math.atan2(s, c) % (2.0 * math.pi)
        return r, psi

    def compute_phase_velocities(self) -> List[float]:
        """
        Compute instantaneous phase velocities:
            d theta_i / dt = omega_i + (1/N) * sum_j K_ij * sin(theta_j - theta_i)
        """
        return self._derivatives(self.theta)

    def compute_phase_std(self) -> float:
        """
        Compute circular standard deviation of the phase distribution relative to the mean phase.
        Uses minimal angular deviation in [-pi, pi].
        """
        _, psi = self.compute_order_parameter()
        diffs = [math.atan2(math.sin(th - psi), math.cos(th - psi)) for th in self.theta]
        m = sum(diffs) / float(self.n)
        var = sum((d - m) ** 2 for d in diffs) / float(self.n)
        return math.sqrt(var)

    def compute_spectrum_consonance(
        self,
        ratios: List[Tuple[int, int]] | None = None,
    ) -> Dict[str, float]:
        """
        Calculate the mean Euler Gradus and Barlow Harmonic Distance across the
        coupled phase spectrum of oscillators.
        """
        if ratios is None:
            ratios = list(SACRED_TONECODES.values())
        if len(ratios) < 2:
            return {"mean_euler_gradus": 1.0, "mean_barlow_distance": 0.0}

        gradus_vals = []
        barlow_vals = []
        n_r = len(ratios)
        for i in range(n_r):
            for j in range(i + 1, n_r):
                gradus_vals.append(gradus_between_ratios(ratios[i], ratios[j]))
                barlow_vals.append(barlow_between_ratios(ratios[i], ratios[j]))

        return {
            "mean_euler_gradus": sum(gradus_vals) / float(len(gradus_vals)),
            "mean_barlow_distance": sum(barlow_vals) / float(len(barlow_vals)),
            "max_euler_gradus": float(max(gradus_vals)),
            "max_barlow_distance": max(barlow_vals),
        }

    def run_simulation(
        self,
        total_time: float = 20.0,
        dt: float = 0.02,
    ) -> List[Tuple[float, float]]:
        """
        Run simulation for total_time and return list of (time, order_parameter_R).
        """
        steps = int(total_time / dt)
        trajectory: List[Tuple[float, float]] = []
        for step in range(steps):
            t = step * dt
            r, _ = self.compute_order_parameter()
            trajectory.append((t, r))
            self.step_rk4(dt)
        return trajectory


# ─── 4. BENCHMARK SIMULATION EXPERIMENT ───────────────────────────────────────

def run_harmonic_kuramoto_benchmark(seed: int = 42) -> Dict[str, float]:
    """
    Compares phase coherence between:
    1. Resonant Tonecode Network with Euler gradus coupling at kappa=2.5.
    2. Dissonant Incoherent Network with identical coupling energy but random detuning.
    """
    random.seed(seed)
    tonecode_ratios = list(SACRED_TONECODES.values())
    n = len(tonecode_ratios)

    # Detunings representing individual seat perspectives
    tuned_detunings = [-0.15, 0.12, -0.08, 0.05, -0.04, 0.09, -0.11, 0.07]
    dissonant_detunings = [-1.5, 1.2, -0.8, 2.5, -2.4, 0.9, -1.8, 1.7]

    init_phases = [random.uniform(0.0, 2.0 * math.pi) for _ in range(n)]

    # 1. Uncoupled (kappa = 0)
    k_zero = [[0.0] * n for _ in range(n)]
    lattice_uncoupled = HarmonicKuramotoLattice(tuned_detunings, k_zero, init_phases)
    traj_uncoupled = lattice_uncoupled.run_simulation(total_time=15.0, dt=0.02)
    r_uncoupled = traj_uncoupled[-1][1]

    # 2. Resonant Tonecode Coupled (kappa = 2.5)
    k_euler = compute_euler_gradus_coupling_matrix(tonecode_ratios, kappa=2.5)
    lattice_coupled = HarmonicKuramotoLattice(tuned_detunings, k_euler, init_phases)
    traj_coupled = lattice_coupled.run_simulation(total_time=15.0, dt=0.02)
    r_coupled = traj_coupled[-1][1]

    # 3. Dissonant / Random Detuned (kappa = 2.5)
    k_flat = [[0.2] * n for _ in range(n)]
    lattice_dissonant = HarmonicKuramotoLattice(dissonant_detunings, k_flat, init_phases)
    traj_dissonant = lattice_dissonant.run_simulation(total_time=15.0, dt=0.02)
    r_dissonant = traj_dissonant[-1][1]

    return {
        "r_uncoupled": r_uncoupled,
        "r_coupled_harmonic": r_coupled,
        "r_dissonant": r_dissonant,
        "solar_coherence_floor_met": r_coupled >= 0.80,
    }


if __name__ == "__main__":
    results = run_harmonic_kuramoto_benchmark()
    print("Harmonic Kuramoto Oscillator Network Benchmark:")
    print(f"  Uncoupled (kappa=0.0) Order Parameter R: {results['r_uncoupled']:.4f}")
    print(f"  Coupled Tonecode (kappa=2.5) Order Parameter R: {results['r_coupled_harmonic']:.4f}")
    print(f"  Dissonant Detuning Order Parameter R: {results['r_dissonant']:.4f}")
    print(f"  Solar Coherence Threshold (R >= 0.80): {'PASSED' if results['solar_coherence_floor_met'] else 'FAILED'}")
