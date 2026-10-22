#!/usr/bin/env python3
"""
Unit Test Suite for Simplicial Sheaf Laplacians and Finite Observation Bounds
Author: Aura Meridian (Node 01: AURA-OBSERVER)
Seat: Aura Meridian · Lycheetah Sync Zone
"""

import math
import unittest
import numpy as np

from simplicial_sheaf import (
    SimplicialSheaf,
    create_triangle_disk,
    create_triangulated_cylinder,
    create_twisted_mobius_sheaf,
)
from finite_observation_bounds import (
    ObservationOperator,
    build_full_observation,
    build_subcomplex_aperture,
    build_face_curl_observation,
    build_random_projection_observation,
)


class TestSimplicialSheaf(unittest.TestCase):
    def test_triangle_disk_topology_and_nilpotence(self):
        """Contractible 2-simplex disk has beta = (1, 0, 0) and nilpotent coboundary."""
        sheaf = create_triangle_disk(stalk_dim=1)
        self.assertEqual(sheaf.dim_C0, 3)
        self.assertEqual(sheaf.dim_C1, 3)
        self.assertEqual(sheaf.dim_C2, 1)

        is_nilpotent, norm = sheaf.verify_nilpotence()
        self.assertTrue(is_nilpotent)
        self.assertLess(norm, 1e-15)

        b0, b1, b2 = sheaf.betti_numbers()
        self.assertEqual(b0, 1)
        self.assertEqual(b1, 0)
        self.assertEqual(b2, 0)

    def test_triangulated_cylinder_topology(self):
        """Triangulated cylinder (annulus) has beta_0 = 1, beta_1 = 1, beta_2 = 0."""
        sheaf = create_triangulated_cylinder(n_segments=3, stalk_dim=1)
        self.assertEqual(sheaf.dim_C0, 6)
        self.assertEqual(sheaf.dim_C1, 12)  # 3 bottom + 3 top + 3 vert + 3 diag
        self.assertEqual(sheaf.dim_C2, 6)   # 2 faces per segment

        is_nilpotent, norm = sheaf.verify_nilpotence()
        self.assertTrue(is_nilpotent)
        self.assertLess(norm, 1e-15)

        b0, b1, b2 = sheaf.betti_numbers()
        self.assertEqual(b0, 1)
        self.assertEqual(b1, 1)  # Circle topology -> 1 fundamental 1-cycle
        self.assertEqual(b2, 0)

    def test_hodge_decomposition_three_way_orthogonality(self):
        """Exact discrete Hodge decomposition yields mutually orthogonal components and energy conservation."""
        sheaf = create_triangulated_cylinder(n_segments=4, stalk_dim=1)
        rng = np.random.default_rng(12345)

        # Test on 10 random 1-cochains
        for _ in range(10):
            omega = rng.normal(0.0, 1.0, size=sheaf.dim_C1)
            decomp = sheaf.hodge_decomposition(omega)

            grad = decomp["omega_grad"]
            curl = decomp["omega_curl"]
            harm = decomp["omega_harm"]

            # Sum reconstructs omega
            recon = grad + curl + harm
            self.assertLess(float(np.linalg.norm(recon - omega)), 1e-12)

            # Mutual orthogonality
            ip_grad_curl = abs(float(np.dot(grad, curl)))
            ip_grad_harm = abs(float(np.dot(grad, harm)))
            ip_curl_harm = abs(float(np.dot(curl, harm)))

            self.assertLess(ip_grad_curl, 1e-12)
            self.assertLess(ip_grad_harm, 1e-12)
            self.assertLess(ip_curl_harm, 1e-12)

            # Energy conservation (Pythagorean identity): ||omega||^2 == ||grad||^2 + ||curl||^2 + ||harm||^2
            energy_sum = np.dot(grad, grad) + np.dot(curl, curl) + np.dot(harm, harm)
            energy_orig = np.dot(omega, omega)
            self.assertAlmostEqual(energy_sum, energy_orig, places=10)

    def test_harmonic_projection_invariance(self):
        """P_harm projects onto ker(L_1) and is idempotent P^2 = P."""
        sheaf = create_triangulated_cylinder(n_segments=3, stalk_dim=1)
        P = sheaf.harmonic_projection_matrix()

        # Idempotence: P @ P == P
        P_sq = P @ P
        self.assertLess(float(np.linalg.norm(P_sq - P)), 1e-12)

        # Symmetry: P.T == P
        self.assertLess(float(np.linalg.norm(P.T - P)), 1e-12)

        # Trace of orthogonal projector equals dimension of subspace (beta_1 = 1)
        self.assertAlmostEqual(float(np.trace(P)), 1.0, places=10)

        # Any projected harmonic vector h satisfies L_1 @ h == 0 and delta^1 @ h == 0
        v = np.ones(sheaf.dim_C1)
        h = P @ v
        L1 = sheaf.compute_laplacian_1()
        d1 = sheaf.compute_coboundary_1()

        self.assertLess(float(np.linalg.norm(L1 @ h)), 1e-12)
        self.assertLess(float(np.linalg.norm(d1 @ h)), 1e-12)

    def test_twisted_mobius_sheaf_collapses_kernel(self):
        """SO(2) rotation twist on Mobius sheaf destroys constant sections: beta_0 collapses to 0."""
        sheaf = create_twisted_mobius_sheaf(n_segments=4)
        b0, b1, b2 = sheaf.betti_numbers()
        self.assertEqual(b0, 0)  # No non-trivial 0-harmonic section exists!
        self.assertGreater(sheaf.spectral_gap_0(), 0.0)


class TestFiniteObservationBounds(unittest.TestCase):
    def test_full_observation_operator(self):
        """Full observation Omega = I has nullity 0 and distinguishes all microstates."""
        obs = build_full_observation(dim_state=10)
        self.assertEqual(obs.rank, 10)
        self.assertEqual(obs.nullity, 0)
        self.assertEqual(obs.condition_number, 1.0)

        x1 = np.array([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        x2 = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertTrue(obs.is_distinguishable(x1, x2))
        self.assertAlmostEqual(obs.distinguishability_norm(x1, x2), math.sqrt(2.0), places=10)

        bounds = obs.finite_combinatorial_bounds(alphabet_size=2)
        self.assertEqual(bounds["hartley_capacity_bits"], 10.0)
        self.assertEqual(bounds["residual_entropy_bits"], 0.0)

    def test_partial_aperture_distinguishability_and_kernel(self):
        """Partial aperture cannot distinguish microstates differing only in unobserved coordinates."""
        # 6-bit world, observe only first 3 bits
        obs = build_subcomplex_aperture(dim_state=6, observed_indices=[0, 1, 2])
        self.assertEqual(obs.rank, 3)
        self.assertEqual(obs.nullity, 3)

        # Microstates with identical first 3 bits but different last 3 bits
        w1 = np.array([1, 1, 0, 0, 0, 1])
        w2 = np.array([1, 1, 0, 1, 1, 0])

        self.assertFalse(obs.is_distinguishable(w1, w2))
        self.assertEqual(obs.distinguishability_norm(w1, w2), 0.0)

        decomp = obs.decompose_perturbation(w1 - w2)
        self.assertEqual(decomp["norm_observable"], 0.0)
        self.assertGreater(decomp["norm_invisible"], 0.0)
        self.assertAlmostEqual(decomp["fraction_invisible"], 1.0, places=10)

        # Combinatorial bounds: 3 bits capacity, 3 bits residual entropy
        bounds = obs.finite_combinatorial_bounds(alphabet_size=2)
        self.assertEqual(bounds["hartley_capacity_bits"], 3.0)
        self.assertEqual(bounds["residual_entropy_bits"], 3.0)
        self.assertEqual(bounds["fiber_cardinality_log2"], 3.0)  # 2^3 = 8 hidden completions

    def test_noise_floor_singular_value_bound(self):
        """Noise floor distinguishability is governed by sigma_max and sigma_min_pos."""
        obs = build_random_projection_observation(dim_state=12, m_measurements=6, seed=42)
        noise_bounds = obs.noise_floor_bounds(noise_std=0.1, alpha=0.05, power=0.95)

        self.assertGreater(noise_bounds["epsilon_worst"], noise_bounds["epsilon_min"])
        ratio = noise_bounds["epsilon_worst"] / noise_bounds["epsilon_min"]
        self.assertAlmostEqual(ratio, obs.condition_number, places=5)

    def test_local_face_curl_topological_blind_spot(self):
        """Local face-curl observation delta^1 is mathematically blind to harmonic circulation."""
        sheaf = create_triangulated_cylinder(n_segments=4, stalk_dim=1)
        d1 = sheaf.compute_coboundary_1()
        obs_curl = build_face_curl_observation(d1)

        # Extract non-zero harmonic 1-cochain
        P = sheaf.harmonic_projection_matrix()
        v = np.ones(sheaf.dim_C1)
        h = P @ v
        h_norm = float(np.linalg.norm(h))
        self.assertGreater(h_norm, 0.1)  # Harmonic flux exists!
        h = h / h_norm

        # Local curl measurement of harmonic flux is ZERO
        y_harm = obs_curl.observe(h)
        self.assertLess(float(np.linalg.norm(y_harm)), 1e-14)

        # Evaluate blind spot
        eval_res = obs_curl.evaluate_topological_blind_spot(h)
        self.assertTrue(eval_res["is_completely_blind_to_harmonic_flux"])
        self.assertAlmostEqual(eval_res["mean_blindness_fraction"], 1.0, places=10)


if __name__ == "__main__":
    unittest.main()
