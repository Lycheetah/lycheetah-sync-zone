#!/usr/bin/env python3
"""
Unit tests for Mathesis Philologica Engine [INVENTED: EXECUTABLE-VERIFICATION]
Verifies all algebraic, topological, ultrametric, hyperreal, and spectral invariants.
"""

import math
import sys
import unittest
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from importlib.machinery import SourceFileLoader
engine_module = SourceFileLoader("mathesis_engine", str(Path(__file__).resolve().parent / "01_mathesis_philologica_engine.py")).load_module()

LambekPregroupParser = engine_module.LambekPregroupParser
PregroupType = engine_module.PregroupType
PAdicConceptTree = engine_module.PAdicConceptTree
HyperrealNumber = engine_module.HyperrealNumber
SurrealEpistemicValuator = engine_module.SurrealEpistemicValuator
SpectralPrimeResonance = engine_module.SpectralPrimeResonance
MathesisPhilologicaEngine = engine_module.MathesisPhilologicaEngine


class TestMathesisPhilologica(unittest.TestCase):

    def setUp(self):
        self.parser = LambekPregroupParser()
        self.tree = PAdicConceptTree(p=5)
        self.engine = MathesisPhilologicaEngine(p=5)

    def test_01_pregroup_adjoint_cancellations(self):
        """Verifies x^l * x -> 1 and x * x^r -> 1 pregroup reductions."""
        n = PregroupType("n")
        n_l = n.left_adjoint
        n_r = n.right_adjoint

        self.assertTrue(n_l.cancels_with(n))
        self.assertTrue(n.cancels_with(n_r))
        self.assertFalse(n.cancels_with(n))
        self.assertFalse(n_r.cancels_with(n_l))

    def test_02_grammatical_sentence_reduction(self):
        """Verifies parsing of transitive and intransitive sentences reduces to 's'."""
        sentence = "The sovereign proves the truth"
        valid, reduced, trace = self.parser.parse_sentence(sentence)
        self.assertTrue(valid, f"Expected valid sentence, got reduced types: {trace}")
        self.assertEqual(len(reduced), 1)
        self.assertEqual(reduced[0].name, "s")
        self.assertEqual(reduced[0].adjoint_order, 0)

    def test_03_padic_valuation_and_norm(self):
        """Verifies p-adic valuation and norm calculations in Q_5."""
        # 25 = 5^2, so v_5(25) = 2, |25|_5 = 5^(-2) = 0.04
        self.assertEqual(self.tree.valuation(25), 2.0)
        self.assertAlmostEqual(self.tree.p_adic_norm(25), 0.04, places=6)

        # 125 = 5^3, v_5(125) = 3, |125|_5 = 0.008
        self.assertEqual(self.tree.valuation(125), 3.0)
        self.assertAlmostEqual(self.tree.p_adic_norm(125), 0.008, places=6)

        # 7 is coprime to 5, so v_5(7) = 0, |7|_5 = 1.0
        self.assertEqual(self.tree.valuation(7), 0.0)
        self.assertAlmostEqual(self.tree.p_adic_norm(7), 1.0, places=6)

    def test_04_strong_triangle_inequality_and_isosceles_theorems(self):
        """Verifies the Strong Triangle Inequality: d(x, z) <= max(d(x, y), d(y, z))
        and that all triangles in p-adic space are isosceles.
        """
        x, y, z = 5, 25, 125
        self.assertTrue(self.tree.verify_strong_triangle_inequality(x, y, z))
        self.assertTrue(self.tree.verify_isosceles_triangle(x, y, z))

        # Test across 10 distinct integer triples
        for i in range(1, 10):
            a, b, c = i * 5, i * 25, (i + 1) * 125
            self.assertTrue(self.tree.verify_strong_triangle_inequality(a, b, c))
            self.assertTrue(self.tree.verify_isosceles_triangle(a, b, c))

    def test_05_hyperreal_infinitesimal_bayesian_update(self):
        """Verifies non-standard Bayesian update: eps * omega = 1 lifts infinitesimal doubt."""
        # Prior is an infinitesimal eps (0 + 1*eps)
        prior = HyperrealNumber(standard_part=0.0, infinitesimal_coeff=1.0)
        self.assertTrue(prior.is_infinitesimal())
        self.assertFalse(prior.is_infinite())

        # Likelihood is infinite omega (0 + 0*eps + 1*omega)
        likelihood = HyperrealNumber(standard_part=0.0, infinite_coeff=1.0)
        self.assertTrue(likelihood.is_infinite())

        # Posterior = eps * omega = 1
        posterior = SurrealEpistemicValuator.bayesian_non_archimedean_update(prior, likelihood)
        self.assertAlmostEqual(posterior.standard_part, 1.0, places=6)

    def test_06_montgomery_odlyzko_level_repulsion(self):
        """Verifies GUE pair correlation level repulsion R_2(0) = 0 for Riemann zeros."""
        # At s = 0, level repulsion forces R_2(0) = 0
        r_zero = SpectralPrimeResonance.montgomery_odlyzko_pair_correlation(0.0)
        self.assertAlmostEqual(r_zero, 0.0, places=6)

        # At large s, R_2(s) approaches 1.0
        r_large = SpectralPrimeResonance.montgomery_odlyzko_pair_correlation(10.0)
        self.assertAlmostEqual(r_large, 1.0, places=2)

    def test_07_full_mathesis_philologica_synthesis(self):
        """Verifies the complete end-to-end synthesis report."""
        report = self.engine.synthesize("The sovereign proves the truth")
        self.assertTrue(report.is_grammatically_sound)
        self.assertTrue(report.is_ultrametric_triangle)
        self.assertAlmostEqual(report.hyperreal_truth_value.standard_part, 1.0, places=6)
        self.assertGreater(report.prime_spectral_freq, 100.0)
        self.assertGreater(report.thematic_consonance, 0.0)


if __name__ == "__main__":
    unittest.main()
