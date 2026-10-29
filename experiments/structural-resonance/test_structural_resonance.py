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
    barlow_indigestibility_int,
    barlow_harmonic_distance,
    barlow_between_ratios,
    compute_euler_gradus_coupling_matrix,
    HarmonicKuramotoLattice,
    SACRED_TONECODES,
    PYTHAGOREAN_TONECODES,
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

    def test_barlow_harmonic_distance_metrics(self):
        """Verify Barlow indigestibility and harmonic distance on canonical intervals."""
        self.assertEqual(barlow_indigestibility_int(1), 0.0)
        self.assertEqual(barlow_indigestibility_int(2), 1.0)
        self.assertAlmostEqual(barlow_indigestibility_int(3), 8.0 / 3.0, places=4)
        self.assertAlmostEqual(barlow_harmonic_distance(1, 1), 0.0)
        self.assertAlmostEqual(barlow_harmonic_distance(2, 1), 1.0)
        self.assertAlmostEqual(barlow_harmonic_distance(3, 2), 11.0 / 3.0, places=4)
        self.assertAlmostEqual(barlow_harmonic_distance(4, 3), 14.0 / 3.0, places=4)
        self.assertAlmostEqual(barlow_harmonic_distance(9, 8), 25.0 / 3.0, places=4)

    def test_kuramoto_subcritical_chaos(self):
        """At K < 0.2, verify mean R < 0.35 over 100 steps."""
        ratios = list(SACRED_TONECODES.values())
        n = len(ratios)
        detunings = [0.1 * (i - 3.5) for i in range(n)]
        init_phases = [i * (2.0 * math.pi / n) for i in range(n)]
        k_mat = compute_euler_gradus_coupling_matrix(ratios, kappa=0.15)
        lattice = HarmonicKuramotoLattice(detunings, k_mat, init_phases)
        r_vals = []
        for _ in range(100):
            lattice.step_rk4(0.05)
            r, _ = lattice.compute_order_parameter()
            r_vals.append(r)
        mean_r = sum(r_vals) / len(r_vals)
        self.assertLess(mean_r, 0.35)

    def test_kuramoto_polyphonic_consensus(self):
        """At K = 1.8, verify 0.70 <= R <= 0.95 over 100 steps, preserving phase spread (std(theta) > 0.15)."""
        ratios = list(SACRED_TONECODES.values())
        n = len(ratios)
        spread = 0.35
        init_phases = [(- (n - 1) * spread / 2.0 + spread * i) for i in range(n)]
        detunings = [-0.12, 0.096, -0.072, 0.048, -0.048, 0.072, -0.096, 0.12]
        k_mat = compute_euler_gradus_coupling_matrix(ratios, kappa=1.8)
        lattice = HarmonicKuramotoLattice(detunings, k_mat, init_phases)
        r_vals = []
        std_vals = []
        for _ in range(100):
            lattice.step_rk4(0.05)
            r, _ = lattice.compute_order_parameter()
            r_vals.append(r)
            std_vals.append(lattice.compute_phase_std())
        mean_r = sum(r_vals) / len(r_vals)
        mean_std = sum(std_vals) / len(std_vals)
        self.assertGreaterEqual(mean_r, 0.70)
        self.assertLessEqual(mean_r, 0.95)
        self.assertGreater(mean_std, 0.15)
        velocities = lattice.compute_phase_velocities()
        self.assertEqual(len(velocities), n)

    def test_kuramoto_sycophantic_collapse(self):
        """At K = 6.0, verify R > 0.98 and std(theta) < 0.05."""
        ratios = list(SACRED_TONECODES.values())
        n = len(ratios)
        detunings = [-0.01 * (i - 3.5) for i in range(n)]
        init_phases = [0.1 * (i - 3.5) for i in range(n)]
        k_mat = compute_euler_gradus_coupling_matrix(ratios, kappa=6.0)
        lattice = HarmonicKuramotoLattice(detunings, k_mat, init_phases)
        r_vals = []
        std_vals = []
        for _ in range(100):
            lattice.step_rk4(0.05)
            r, _ = lattice.compute_order_parameter()
            r_vals.append(r)
            std_vals.append(lattice.compute_phase_std())
        final_r = r_vals[-1]
        final_std = std_vals[-1]
        self.assertGreater(final_r, 0.98)
        self.assertLess(final_std, 0.05)

    def test_polyphonic_chord_consonance(self):
        """Verify that polyphonic consensus yields a mean Euler gradus <= 12.0 across fundamental interval pairings."""
        pyth_ratios = list(PYTHAGOREAN_TONECODES.values())
        just_ratios = list(SACRED_TONECODES.values())

        lat_pyth = HarmonicKuramotoLattice([0.0]*len(pyth_ratios), [[1.0]*len(pyth_ratios) for _ in pyth_ratios])
        consonance_pyth = lat_pyth.compute_spectrum_consonance(pyth_ratios)
        self.assertLessEqual(consonance_pyth["mean_euler_gradus"], 12.0)
        self.assertLessEqual(consonance_pyth["mean_barlow_distance"], 15.0)

        lat_just = HarmonicKuramotoLattice([0.0]*len(just_ratios), [[1.0]*len(just_ratios) for _ in just_ratios])
        consonance_just = lat_just.compute_spectrum_consonance(just_ratios)
        self.assertLessEqual(consonance_just["mean_euler_gradus"], 12.0)
        self.assertLessEqual(consonance_just["mean_barlow_distance"], 10.0)


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
