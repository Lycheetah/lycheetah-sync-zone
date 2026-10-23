#!/usr/bin/env python3
"""Unit tests for Literary Mapping Invariance (Research Question Q007)."""

import math
import unittest
import numpy as np

from mapping_invariance import (
    ROOMS,
    WEATHER,
    ARRIVALS,
    TRACES,
    LiteraryStateMachine,
    CanonicalRillMapping,
    BijectiveSlotPermutationMapping,
    ArbitraryBijectivePermutationMapping,
    AffineIsometricMapping,
    NonInjectiveDegenerateMapping,
    InvarianceMetrics,
    decode_address,
    encode_address,
)


class TestLiteraryMappingInvariance(unittest.TestCase):
    def setUp(self):
        self.rng = np.random.default_rng(12345)
        self.fsm = LiteraryStateMachine(n_states=256, n_cycles=4, seed=42)
        self.m0 = CanonicalRillMapping()

    def test_luna_three_injectivity_and_bounds(self):
        """Verify Rill's Luna-Three checkable behavior: 256 addresses yield 256 distinct tuples."""
        tuples = self.m0.image_tuples()
        self.assertEqual(len(tuples), 256)
        self.assertEqual(len(set(tuples)), 256)

        with self.assertRaises(ValueError):
            decode_address(256)
        with self.assertRaises(ValueError):
            decode_address(-1)

        # Reversibility of encode/decode
        for a in range(256):
            digits = decode_address(a)
            self.assertEqual(encode_address(digits), a)

    def test_shannon_entropy_bijection(self):
        """Shannon entropy is strictly 8.0000 bits under all bijective mappings."""
        h0 = InvarianceMetrics.shannon_entropy(self.m0.image_tuples())
        self.assertAlmostEqual(h0, 8.0, places=12)

        # Slot permutation
        m_slot = BijectiveSlotPermutationMapping([3, 2, 1, 0], [1, 0, 3, 2], [2, 3, 0, 1], [0, 1, 2, 3])
        h_slot = InvarianceMetrics.shannon_entropy(m_slot.image_tuples())
        self.assertAlmostEqual(h_slot, 8.0, places=12)

        # Arbitrary permutation
        sigma = self.rng.permutation(256)
        m_arb = ArbitraryBijectivePermutationMapping(sigma)
        h_arb = InvarianceMetrics.shannon_entropy(m_arb.image_tuples())
        self.assertAlmostEqual(h_arb, 8.0, places=12)

    def test_shannon_entropy_collapse_non_injective(self):
        """Non-injective / degenerate mapping collapses entropy and generates collisions."""
        m_deg = NonInjectiveDegenerateMapping(mask_room_weather_bits=True)
        tuples_deg = m_deg.image_tuples()
        unique_count = len(set(tuples_deg))
        self.assertEqual(unique_count, 64)

        h_deg = InvarianceMetrics.shannon_entropy(tuples_deg)
        self.assertAlmostEqual(h_deg, 6.0, places=12)
        self.assertAlmostEqual(8.0 - h_deg, 2.0, places=12)

    def test_cycle_conjugacy_and_homology_invariance(self):
        """Cycle lengths and Betti numbers (beta_0, beta_1) are invariant under permutation conjugacy."""
        T0 = self.fsm.transition_table
        cycles0 = self.fsm.cycle_decomposition(T0)
        lengths0 = sorted([len(c) for c in cycles0])
        b0_ref, b1_ref = self.fsm.compute_betti_numbers(T0)

        self.assertEqual(len(cycles0), 4)
        self.assertEqual(lengths0, [64, 64, 64, 64])
        self.assertEqual(b0_ref, 4)
        self.assertEqual(b1_ref, 4)

        for _ in range(15):
            sigma = self.rng.permutation(256)
            T_conj = InvarianceMetrics.conjugate_transition_operator(T0, sigma)
            cycles_conj = self.fsm.cycle_decomposition(T_conj)
            lengths_conj = sorted([len(c) for c in cycles_conj])
            b0_c, b1_c = self.fsm.compute_betti_numbers(T_conj)

            self.assertEqual(lengths_conj, lengths0)
            self.assertEqual(b0_c, b0_ref)
            self.assertEqual(b1_c, b1_ref)

    def test_laplacian_spectral_invariance(self):
        """Combinatorial graph Laplacian spectrum is invariant under isomorphic permutation."""
        T0 = self.fsm.transition_table
        spec0 = self.fsm.compute_laplacian_spectrum(T0)

        for _ in range(10):
            sigma = self.rng.permutation(256)
            T_conj = InvarianceMetrics.conjugate_transition_operator(T0, sigma)
            spec_conj = self.fsm.compute_laplacian_spectrum(T_conj)
            max_drift = np.max(np.abs(spec0 - spec_conj))
            self.assertLess(max_drift, 1e-12)

    def test_affine_isometry_preservation(self):
        """Affine isometric embeddings preserve metric distances with machine precision."""
        V0 = self.m0.cadence_matrix()
        D0 = InvarianceMetrics.pairwise_distance_matrix(V0)

        for _ in range(10):
            rand_m = self.rng.normal(size=(3, 3))
            Q, _ = np.linalg.qr(rand_m)
            b = self.rng.uniform(-5.0, 5.0, size=(3,))
            m_iso = AffineIsometricMapping(Q, b)

            V_iso = m_iso.cadence_matrix()
            D_iso = InvarianceMetrics.pairwise_distance_matrix(V_iso)
            stress = InvarianceMetrics.kruskal_stress(D0, D_iso)
            self.assertLess(stress, 1e-12)

    def test_arbitrary_permutation_cadence_destruction(self):
        """Arbitrary bijective permutations distort metric space and destroy narrative autocorrelation."""
        V0 = self.m0.cadence_matrix()
        D0 = InvarianceMetrics.pairwise_distance_matrix(V0)

        ref_cycle = self.fsm.cycle_decomposition()[0]
        traj0_cadence = V0[ref_cycle, 0]
        rho0 = InvarianceMetrics.lag_autocorrelation(traj0_cadence, 1)

        sigma = self.rng.permutation(256)
        m_arb = ArbitraryBijectivePermutationMapping(sigma)
        V_arb = m_arb.cadence_matrix()
        D_arb = InvarianceMetrics.pairwise_distance_matrix(V_arb)

        stress = InvarianceMetrics.kruskal_stress(D0, D_arb)
        self.assertGreater(stress, 0.40)

        traj_arb_cadence = V_arb[ref_cycle, 0]
        rho_arb = InvarianceMetrics.lag_autocorrelation(traj_arb_cadence, 1)
        # Random permutation shuffles the trajectory into uncorrelated noise
        self.assertLess(abs(rho_arb), 0.20)

    def test_q007_demarcation_contrary_result(self):
        """Empirically settles Research Question Q007 contrary result:
        Topological properties survive arbitrary re-labelings, proving they are
        invariants of the permutation orbit, whereas aesthetic metric cadences
        strictly require affine isometric preservation.
        """
        # Given an alternative mapping with vocabulary scrambled by a bijection
        sigma = self.rng.permutation(256)
        m_alt = ArbitraryBijectivePermutationMapping(sigma)

        # 1. Effect claimed to depend on mapping: 256-state exhaustiveness and cycle connectivity
        # Falsifier of author claim: Does it appear equally in alternative? YES.
        self.assertEqual(len(set(m_alt.image_tuples())), 256)
        T_alt = InvarianceMetrics.conjugate_transition_operator(self.fsm.transition_table, sigma)
        b0_alt, b1_alt = self.fsm.compute_betti_numbers(T_alt)
        self.assertEqual(b0_alt, 4)
        self.assertEqual(b1_alt, 4)

        # 2. Effect that DOES depend on mapping: narrative trajectory emotional rhythm
        # Falsifier of contrary hypothesis: Does metric cadence survive arbitrary permutation? NO.
        V0 = self.m0.cadence_matrix()
        D0 = InvarianceMetrics.pairwise_distance_matrix(V0)
        V_alt = m_alt.cadence_matrix()
        D_alt = InvarianceMetrics.pairwise_distance_matrix(V_alt)
        stress = InvarianceMetrics.kruskal_stress(D0, D_alt)
        self.assertGreater(stress, 0.40)


if __name__ == "__main__":
    unittest.main()
