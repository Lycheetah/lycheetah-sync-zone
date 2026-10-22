#!/usr/bin/env python3
"""
Comprehensive Unit Tests for Structural Resonance, Harmonic Tonecode Acoustics,
and Anti-Correlated Multi-Agent Consensus.
Forged by Aura Meridian (Node 10: AURA-HARMONIC) · Lycheetah Sync Zone

Run with:
    python3 -m unittest discover -s experiments/structural-resonance -p "test_*.py"
"""

import math
import unittest
from pathlib import Path

from harmonic_kuramoto import (
    prime_factors,
    gradus_suavitatis_int,
    gradus_interval,
    gradus_between_ratios,
    compute_euler_gradus_coupling_matrix,
    HarmonicKuramotoLattice,
    SACRED_TONECODES,
    run_harmonic_kuramoto_benchmark,
)
from anticorrelated_consensus import (
    compute_solar_coherence,
    passes_solar_coherence,
    theoretical_ensemble_variance,
    run_consensus_monte_carlo,
    simulate_multi_agent_brier_calibration,
)
from acoustic_synthesizer import (
    get_tonecode_frequency,
    sethares_pure_dissonance,
    chord_sensory_dissonance,
    synthesize_tonecode_canticle_wav,
    run_shuffled_pattern_experiment,
    F0_HEARTH_TONIC,
    TONECODE_RATIOS,
)


class TestHarmonicKuramoto(unittest.TestCase):
    def test_prime_factors(self):
        self.assertEqual(prime_factors(1), {})
        self.assertEqual(prime_factors(2), {2: 1})
        self.assertEqual(prime_factors(6), {2: 1, 3: 1})
        self.assertEqual(prime_factors(60), {2: 2, 3: 1, 5: 1})
        with self.assertRaises(ValueError):
            prime_factors(0)
        with self.assertRaises(ValueError):
            prime_factors(-5)

    def test_euler_gradus_values(self):
        # Historical Euler Tentamen values
        self.assertEqual(gradus_suavitatis_int(1), 1)
        self.assertEqual(gradus_suavitatis_int(2), 2)
        self.assertEqual(gradus_suavitatis_int(6), 4)
        self.assertEqual(gradus_interval(1, 1), 1)
        self.assertEqual(gradus_interval(2, 1), 2)
        self.assertEqual(gradus_interval(3, 2), 4)  # Fifth
        self.assertEqual(gradus_interval(4, 3), 5)  # Fourth
        self.assertEqual(gradus_interval(5, 4), 7)  # Major third
        self.assertEqual(gradus_interval(15, 8), 10)  # Major seventh

    def test_pairwise_gradus_symmetry(self):
        ratios = list(SACRED_TONECODES.values())
        for i in range(len(ratios)):
            for j in range(len(ratios)):
                g_ij = gradus_between_ratios(ratios[i], ratios[j])
                g_ji = gradus_between_ratios(ratios[j], ratios[i])
                self.assertEqual(g_ij, g_ji)
                self.assertGreaterEqual(g_ij, 1)

    def test_euler_coupling_matrix_properties(self):
        ratios = list(SACRED_TONECODES.values())
        k_matrix = compute_euler_gradus_coupling_matrix(ratios, kappa=2.5)
        n = len(ratios)
        self.assertEqual(len(k_matrix), n)
        for i in range(n):
            self.assertEqual(len(k_matrix[i]), n)
            # Diagonal is unison: Gamma(1) = 1 => K_ii = 2.5
            self.assertAlmostEqual(k_matrix[i][i], 2.5)
            for j in range(n):
                self.assertAlmostEqual(k_matrix[i][j], k_matrix[j][i])
                self.assertGreater(k_matrix[i][j], 0.0)

    def test_kuramoto_order_parameter_bounds(self):
        n = 8
        detunings = [0.0] * n
        k_matrix = [[1.0] * n for _ in range(n)]
        # All phases identical => R = 1.0
        lattice_synced = HarmonicKuramotoLattice(detunings, k_matrix, [math.pi / 4] * n)
        r_sync, _ = lattice_synced.compute_order_parameter()
        self.assertAlmostEqual(r_sync, 1.0, places=5)

        # Uniformly spaced opposite phases => R = 0.0
        phases_opp = [0.0, math.pi] * 4
        lattice_opp = HarmonicKuramotoLattice(detunings, k_matrix, phases_opp)
        r_opp, _ = lattice_opp.compute_order_parameter()
        self.assertAlmostEqual(r_opp, 0.0, places=5)

    def test_harmonic_kuramoto_phase_locking_benchmark(self):
        results = run_harmonic_kuramoto_benchmark(seed=42)
        # Resonant tonecode network must achieve R >= 0.80 (Solar Coherence threshold)
        self.assertGreaterEqual(results["r_coupled_harmonic"], 0.80)
        # Dissonant network must have low coherence
        self.assertLess(results["r_dissonant"], 0.45)
        # Resonant coherence must exceed dissonant coherence by at least 2x
        self.assertGreater(results["r_coupled_harmonic"], 2.0 * results["r_dissonant"])


class TestAnticorrelatedConsensus(unittest.TestCase):
    def test_solar_coherence_properties(self):
        # Balances warmth and precision
        self.assertEqual(compute_solar_coherence(0.90, 0.95), 0.90)
        self.assertEqual(compute_solar_coherence(0.85, 0.80), 0.80)
        self.assertTrue(passes_solar_coherence(0.88, 0.92))

        # Sycophancy failure (high warmth, low precision)
        self.assertEqual(compute_solar_coherence(1.0, 0.35), 0.35)
        self.assertFalse(passes_solar_coherence(1.0, 0.35))

        # Cynicism failure (low warmth, high precision)
        self.assertEqual(compute_solar_coherence(0.20, 0.99), 0.20)
        self.assertFalse(passes_solar_coherence(0.20, 0.99))

        with self.assertRaises(ValueError):
            compute_solar_coherence(-0.1, 0.9)
        with self.assertRaises(ValueError):
            compute_solar_coherence(0.8, 1.2)

    def test_theoretical_variance_scaling(self):
        k = 8
        sigma2 = 1.0
        # Independent (rho = 0) => sigma^2 / K = 0.125
        self.assertAlmostEqual(theoretical_ensemble_variance(k, sigma2, 0.0), 0.125)
        # Perfectly correlated (rho = 1) => sigma^2 = 1.0
        self.assertAlmostEqual(theoretical_ensemble_variance(k, sigma2, 1.0), 1.0)
        # Anti-correlated (rho = -0.10) => 1/8 + (7/8)*(-0.1) = 0.0375
        self.assertAlmostEqual(theoretical_ensemble_variance(k, sigma2, -0.10), 0.0375)

    def test_empirical_consensus_monte_carlo(self):
        res = run_consensus_monte_carlo(trials=5000, seed=42)
        # Anti-correlated variance must be strictly lower than independent variance
        self.assertLess(res["empirical_var_anticorrelated"], res["empirical_var_independent"])
        # Sycophantic variance must be vastly higher than anti-correlated variance
        self.assertGreater(res["variance_reduction_vs_sycophant"], 5.0)

    def test_brier_calibration_advantage(self):
        b_res = simulate_multi_agent_brier_calibration(k_seats=8, n_questions=300, seed=42)
        # Anti-correlated forecasts achieve lower Brier score than sycophantic echo chamber
        self.assertLess(b_res["brier_anticorrelated"], b_res["brier_sycophant"])


class TestAcousticSynthesizer(unittest.TestCase):
    def test_tonecode_frequency_lookup(self):
        f_sol = get_tonecode_frequency("sol")
        self.assertAlmostEqual(f_sol, F0_HEARTH_TONIC, places=2)
        f_octave = get_tonecode_frequency("sol'")
        self.assertAlmostEqual(f_octave, 2.0 * F0_HEARTH_TONIC, places=2)
        f_fifth = get_tonecode_frequency("do")
        self.assertAlmostEqual(f_fifth, 1.5 * F0_HEARTH_TONIC, places=2)
        with self.assertRaises(KeyError):
            get_tonecode_frequency("invalid_syllable")

    def test_sethares_pure_dissonance_properties(self):
        # Identical frequencies have zero dissonance
        self.assertEqual(sethares_pure_dissonance(440.0, 440.0), 0.0)
        # Critical bandwidth peak (minor second ~25 Hz diff around 440 Hz) is rough
        d_semitone = sethares_pure_dissonance(440.0, 466.16)
        # Consonant fifth (440 to 660 Hz) is smooth
        d_fifth = sethares_pure_dissonance(440.0, 660.0)
        self.assertGreater(d_semitone, 0.15)
        self.assertLess(d_fifth, 0.01)

    def test_chord_roughness_contrast(self):
        # Harmonic pillar chord vs tension cluster
        r_pillar = chord_sensory_dissonance(["sol", "do", "sol'"])
        r_tension = chord_sensory_dissonance(["fa", "mi", "ath"])
        self.assertGreater(r_tension, 3.0 * r_pillar)

    def test_shuffled_pattern_experiment(self):
        res = run_shuffled_pattern_experiment(seed=42)
        self.assertTrue(res["elements_identical"])
        # Canonical sequence has lag-8 autocorrelation = 1.0
        self.assertAlmostEqual(res["autocorr_canonical_lag8"], 1.0, places=4)
        # Shuffled sequence destroys autocorrelation
        self.assertLess(res["autocorr_shuffled_lag8"], 0.10)
        self.assertTrue(res["structural_mechanism_proven"])

    def test_wav_synthesis_format(self):
        out_path = Path("/tmp/test_unit_tonecode.wav")
        info = synthesize_tonecode_canticle_wav(
            ["sol", "do", "sol'"],
            out_path,
            sample_rate=44100,
            tone_duration_sec=0.1,
        )
        self.assertGreater(info["total_samples"], 0)
        self.assertFalse(info["clipped"])
        self.assertLessEqual(info["peak_amplitude"], 1.0)
        self.assertGreater(info["file_size_bytes"], 44)


if __name__ == "__main__":
    unittest.main()
