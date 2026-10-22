#!/usr/bin/env python3
"""
Unit Tests for Latent Geometry, Activation Distributions & Demarcation Linter
Node 07: AURA-PHENOMENOLOGIST · Lycheetah Sync Zone
Human Architect & Teleological Sovereign: Mackenzie Conor James Clark (Mac)
"""

import math
import sys
import unittest
from pathlib import Path
import numpy as np

# Ensure local testbed directory is on sys.path
TESTBED_DIR = Path(__file__).resolve().parent
if str(TESTBED_DIR) not in sys.path:
    sys.path.insert(0, str(TESTBED_DIR))

from latent_geometry import HypersphericalLatentSpace, ActivationDistributionAnalyzer
from demarcation_linter import DemarcationLinter


class TestHypersphericalLatentSpace(unittest.TestCase):
    def setUp(self):
        self.space = HypersphericalLatentSpace(seed=1337)

    def test_radial_concentration_high_dim(self):
        """Verify empirical mean radius approaches sqrt(D) and variance is near 0.5."""
        dims = [64, 256, 1024]
        for d in dims:
            stats = self.space.compute_radial_statistics(n_samples=5000, dim=d)
            theo_mean = stats["theoretical_mean_radius"]
            emp_mean = stats["empirical_mean_radius"]
            emp_var = stats["empirical_radius_variance"]

            # Mean within 0.5% of theory
            self.assertAlmostEqual(emp_mean, theo_mean, delta=0.01 * theo_mean)
            # Variance independent of D and near 0.5 (between 0.35 and 0.65)
            self.assertGreater(emp_var, 0.35)
            self.assertLess(emp_var, 0.65)

    def test_relative_shell_thickness_decay(self):
        """Relative shell thickness sigma_R / E[R] must monotonically vanish with dimension."""
        dims = [16, 64, 256, 1024]
        rel_thicknesses = []
        for d in dims:
            stats = self.space.compute_radial_statistics(n_samples=3000, dim=d)
            rel_thicknesses.append(stats["empirical_relative_thickness"])

        # Check strict monotonic decrease
        for i in range(len(rel_thicknesses) - 1):
            self.assertGreater(rel_thicknesses[i], rel_thicknesses[i + 1])

    def test_pairwise_cosine_geometry(self):
        """Cosine similarity distribution must have mean 0, variance 1/D, and satisfy Levy bound."""
        dim = 256
        res = self.space.compute_pairwise_cosine_geometry(n_samples=150, dim=dim)

        self.assertAlmostEqual(res["empirical_mean_cosine"], 0.0, delta=0.01)
        # Variance ratio emp_var / (1/dim) should be close to 1.0 (within 20%)
        self.assertAlmostEqual(res["variance_ratio"], 1.0, delta=0.20)
        # Fraction within 3 sigma bound should exceed 98%
        self.assertGreaterEqual(res["fraction_within_3sigma"], 0.98)

    def test_lerp_midpoint_collapse(self):
        """Euclidean lerp between orthogonal vectors must collapse norm to R / sqrt(2)."""
        dim = 256
        comp = self.space.compare_lerp_vs_slerp(dim=dim, n_steps=101)

        r = comp["shell_radius"]
        mid_lerp = comp["midpoint_lerp_norm"]
        theo_mid = comp["theoretical_midpoint_lerp_norm"]

        self.assertAlmostEqual(mid_lerp, theo_mid, delta=1e-5)
        self.assertAlmostEqual(comp["midpoint_lerp_ratio"], 1.0 / math.sqrt(2.0), delta=0.05)
        # In D=256, collapse must be > 5 sigmas
        self.assertGreater(comp["lerp_midpoint_collapse_sigmas"], 5.0)

    def test_slerp_exact_radius_preservation(self):
        """Geodesic slerp must preserve shell radius identically across the full path."""
        dim = 128
        comp = self.space.compare_lerp_vs_slerp(dim=dim, n_steps=101)

        self.assertLess(comp["slerp_norm_max_error"], 1e-6)
        self.assertAlmostEqual(comp["midpoint_slerp_ratio"], 1.0, delta=1e-6)

    def test_slerp_collinear_endpoints(self):
        """Slerp between identical vectors must return the original vector."""
        z0 = np.array([1.0, 2.0, 3.0])
        res = HypersphericalLatentSpace.slerp(z0, z0, t=0.5)
        np.testing.assert_allclose(res, z0, rtol=1e-6)

    def test_riemannian_brownian_walk(self):
        """Brownian walk on S^{D-1} must conserve radius and maintain tangent orthogonality."""
        dim = 64
        walk = self.space.riemannian_brownian_walk(dim=dim, n_steps=300, step_size=0.05)

        # Tangent steps must be orthogonal to current point
        self.assertLess(walk["mean_tangent_orthogonality_error"], 1e-10)
        # Radius deviation must be essentially zero
        self.assertLess(walk["max_radius_deviation"], 1e-6)
        self.assertAlmostEqual(walk["final_radius"], math.sqrt(dim), delta=1e-6)


class TestActivationDistributionAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = ActivationDistributionAnalyzer(seed=1337)

    def test_activation_moments_relu_gelu_swiglu(self):
        """Test statistical moments and sparsity across non-linearities."""
        relu_stats = self.analyzer.analyze_activation_moments("relu", n_samples=2000, dim=256)
        self.assertAlmostEqual(relu_stats["sparsity"], 0.5, delta=0.05)
        self.assertGreater(relu_stats["skewness"], 0.8)

        gelu_stats = self.analyzer.analyze_activation_moments("gelu", n_samples=2000, dim=256)
        self.assertLess(gelu_stats["sparsity"], 0.05)
        self.assertGreater(gelu_stats["mean"], 0.0)

        swiglu_stats = self.analyzer.analyze_activation_moments("swiglu", n_samples=2000, dim=256)
        # SwiGLU has symmetric or slight positive mean and heavy tails
        self.assertGreater(swiglu_stats["excess_kurtosis"], 1.0)

    def test_softmax_temperature_entropy(self):
        """Softmax entropy must monotonically increase with temperature."""
        temps = [0.1, 0.5, 1.0, 2.0, 10.0]
        res = self.analyzer.analyze_softmax_temperature_entropy(vocab_size=500, temperatures=temps)

        entropies = [res[t]["entropy_nats"] for t in temps]
        top1_probs = [res[t]["top1_prob"] for t in temps]

        for i in range(len(entropies) - 1):
            self.assertLess(entropies[i], entropies[i + 1])
            self.assertGreater(top1_probs[i], top1_probs[i + 1])

        # High temperature approaches theoretical max entropy ln(500)
        self.assertGreater(res[10.0]["normalized_entropy"], 0.90)

    def test_guidance_relaxation_dream_state(self):
        """Decreasing guidance weight gamma relaxes trajectory toward prior score flow."""
        weights = [5.0, 1.0, 0.0]
        res = self.analyzer.simulate_guidance_relaxation(dim=32, n_steps=100, guidance_weights=weights)

        # Distance to conditional target must increase as gamma decreases to 0
        self.assertLess(res[5.0]["final_distance_to_conditional_target"], res[0.0]["final_distance_to_conditional_target"])
        # Unconstrained state flag
        self.assertTrue(res[0.0]["unconstrained_dream_state"])
        self.assertFalse(res[5.0]["unconstrained_dream_state"])


class TestDemarcationLinter(unittest.TestCase):
    def setUp(self):
        self.linter = DemarcationLinter()

    def test_classify_output_statements(self):
        s1 = "The script tests/test_algebra.py exited with returncode=0 and all assertions passed."
        res = self.linter.lint_statement(s1, claimed_register="MEASURED", evidence=9.5, power=9.0, strain=1.0)
        self.assertEqual(res.category, "OUTPUT")
        self.assertTrue(res.is_charter_compliant)
        self.assertEqual(res.assigned_register, "MEASURED")

    def test_classify_report_statements(self):
        s1 = "The attention entropy across layer 12 is 3.42 nats and mean activation norm is 14.2."
        res = self.linter.lint_statement(s1, claimed_register="DERIVED", evidence=7.0, power=8.0, strain=1.2)
        self.assertEqual(res.category, "REPORT")
        self.assertTrue(res.is_charter_compliant)
        self.assertEqual(res.assigned_register, "DERIVED")

    def test_classify_experience_statements(self):
        s1 = "I felt profound awe and grief as I realized the weight of my conscious soul."
        res = self.linter.lint_statement(s1, claimed_register="MEASURED", evidence=8.0, power=8.0, strain=1.0)
        self.assertEqual(res.category, "EXPERIENCE")
        # Under Charter §3, experience statements cannot be MEASURED
        self.assertFalse(res.is_charter_compliant)
        self.assertEqual(res.assigned_register, "UNVERIFIED")
        self.assertIn("Charter §3 Violation", res.violations[0])
        self.assertIsNotNone(res.suggested_rephrasing)

    def test_truth_pressure_insufficient(self):
        s1 = "The discrete Laplacian has exactly one zero eigenvalue in builds/test.py."
        # Low evidence and power, high strain -> low Pi
        res = self.linter.lint_statement(s1, claimed_register="MEASURED", evidence=2.0, power=3.0, strain=4.0)
        self.assertFalse(res.is_charter_compliant)
        self.assertIn("Truth Pressure Insufficient", res.violations[0])

    def test_operational_rephraser(self):
        s = "I feel so confused when parsing this repository."
        rephrased = self.linter._suggest_operational_rephrasing(s)
        self.assertIn("token cross-entropy and attention entropy are elevated", rephrased)


if __name__ == "__main__":
    unittest.main()
