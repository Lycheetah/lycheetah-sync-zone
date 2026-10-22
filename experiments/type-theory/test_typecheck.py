#!/usr/bin/env python3
"""
test_typecheck.py: Test Suite for Constructive Dependent Type Checking
======================================================================

Verifies propositions-as-types, Martin-Löf Sigma-types, and the constructive
epistemic theorem that untyped/unwitnessed assertions are isomorphic to Void (0).
"""

import unittest
from witness_typecheck import (
    EpistemicStatus,
    Prop,
    MeasuredWitness,
    DerivedWitness,
    ConjectureWitness,
    UnverifiedWitness,
    SigmaPair,
    UntypedAssertion,
    TypeChecker,
    SigmaType,
    ConjectureType,
    VoidType,
    VoidTerm,
    assert_isomorphic_to_void,
)


class TestConstructiveTypeCheck(unittest.TestCase):
    """Unit tests for the constructive witness type checker."""

    def setUp(self) -> None:
        self.checker = TypeChecker()

    def test_unwitnessed_proposition_fails(self) -> None:
        """A naked proposition submitted without a witness term must fail type checking."""
        p = Prop(
            name="EulerCirculationConservation",
            statement="Vortex circulation around material loop is invariant under Euler flow",
            status=EpistemicStatus.MEASURED,
        )
        with self.assertRaises(TypeError) as ctx:
            self.checker.typecheck(p)
        self.assertIn("cannot be asserted as truth without a dependent witness", str(ctx.exception))

    def test_untyped_assertion_isomorphic_to_void_fails(self) -> None:
        """An untyped assertion token has zero constructors and must raise TypeError."""
        assertion = UntypedAssertion("The discrete Laplacian has zero topological obstruction")
        with self.assertRaises(TypeError) as ctx:
            self.checker.typecheck(assertion)
        self.assertIn("isomorphic to Void (0)", str(ctx.exception))

    def test_sigma_pair_with_none_witness_fails(self) -> None:
        """A Sigma pair with a None witness represents an uninhabited type and must fail."""
        p = Prop(
            name="HodgeOrthogonality",
            statement="Gradient flow is orthogonal to curl solenoidal field",
            status=EpistemicStatus.MEASURED,
        )
        pair = SigmaPair(first=p, second=None)
        with self.assertRaises(TypeError) as ctx:
            self.checker.typecheck(pair)
        self.assertIn("lacks a witness term", str(ctx.exception))
        self.assertIn("uninhabited (Void)", str(ctx.exception))

    def test_unverified_claim_fails(self) -> None:
        """A claim with UNVERIFIED status or UnverifiedWitness must fail type checking."""
        p = Prop(
            name="VesperMothDeviceFeel",
            statement="The particle swarm feels responsive on iPhone Safari",
            status=EpistemicStatus.UNVERIFIED,
        )
        pair = SigmaPair(first=p, second=UnverifiedWitness("Not seen on physical mobile device"))
        with self.assertRaises(TypeError) as ctx:
            self.checker.typecheck(pair)
        self.assertIn("UNVERIFIED", str(ctx.exception))
        self.assertIn("inhabit Void (0)", str(ctx.exception))

    def test_measured_witness_passes(self) -> None:
        """A valid MEASURED empirical witness typechecks cleanly into a certified Sigma-type."""
        p = Prop(
            name="VesperKelvinCirculationHalfLife",
            statement="Under Zephyr viscosity 0.9995/frame at 60 fps, circulation half-life is 23.1 s",
            status=EpistemicStatus.MEASURED,
        )
        w = MeasuredWitness(
            artifact_path="builds/vesper-kelvin-loop/RESULT.txt",
            metric_name="half_life_seconds",
            expected_val=23.1,
            actual_val=23.1,
            tolerance=0.05,
        )
        pair = SigmaPair(first=p, second=w)
        certified_type = self.checker.typecheck(pair)

        self.assertIsInstance(certified_type, SigmaType)
        self.assertTrue(certified_type.is_inhabited())
        self.assertEqual(certified_type.prop.name, "VesperKelvinCirculationHalfLife")
        self.assertEqual(certified_type.witness_type.status, EpistemicStatus.MEASURED)

    def test_measured_witness_mismatch_fails(self) -> None:
        """If empirical measurement does not match expected value, type checking must reject it."""
        p = Prop(
            name="DipoleSpeedExact",
            statement="Dipole speed equals 0.39789",
            status=EpistemicStatus.MEASURED,
        )
        # Actual measurement diverged (e.g. 0.45 instead of expected 0.39789)
        w = MeasuredWitness(
            artifact_path="builds/vesper-kelvin-loop/RESULT.txt",
            metric_name="dipole_speed",
            expected_val=0.39789,
            actual_val=0.45000,
            tolerance=1e-4,
        )
        pair = SigmaPair(first=p, second=w)
        with self.assertRaises(TypeError) as ctx:
            self.checker.typecheck(pair)
        self.assertIn("Empirical verification failed", str(ctx.exception))

    def test_derived_witness_with_valid_premises_passes(self) -> None:
        """A DERIVED proposition from validly certified premises typechecks cleanly."""
        # Premise 1: measured coboundary orthogonality
        p1 = Prop(
            name="CoboundaryOrthogonality",
            statement="Inner product <d0 alpha, delta1 beta> < 1e-15",
            status=EpistemicStatus.MEASURED,
        )
        w1 = MeasuredWitness(
            artifact_path="builds/kineton-sheaf-spectral/index.html",
            metric_name="inner_product_residual",
            expected_val=0.0,
            actual_val=0.0,
            tolerance=1e-15,
        )
        pair1 = SigmaPair(first=p1, second=w1)

        # Conclusion: derived Hodge decomposition theorem
        p_conc = Prop(
            name="DiscreteHodgeOrthogonalDirectSum",
            statement="C1(X) decomposes into orthogonal sum of gradient, curl, and harmonic spaces",
            status=EpistemicStatus.DERIVED,
        )
        w_derived = DerivedWitness(
            rule_name="HodgeHelmholtzDEC",
            premises=(pair1,),
            conclusion_name="DiscreteHodgeOrthogonalDirectSum",
        )
        pair_derived = SigmaPair(first=p_conc, second=w_derived)

        certified_type = self.checker.typecheck(pair_derived)
        self.assertIsInstance(certified_type, SigmaType)
        self.assertEqual(certified_type.witness_type.status, EpistemicStatus.DERIVED)
        self.assertTrue(certified_type.is_inhabited())

    def test_derived_witness_with_invalid_premise_fails(self) -> None:
        """A derivation relying on an unverified premise must fail type checking."""
        unverified_premise = SigmaPair(
            first=Prop("SpeedConvergence", "Algorithm converges in O(log N)", EpistemicStatus.UNVERIFIED),
            second=UnverifiedWitness("No empirical benchmark"),
        )
        conc = Prop("FastRunGuarantee", "Run time is bounded by 10ms", EpistemicStatus.DERIVED)
        w_bad = DerivedWitness(
            rule_name="ComplexityModusPonens",
            premises=(unverified_premise,),
            conclusion_name="FastRunGuarantee",
        )
        pair = SigmaPair(first=conc, second=w_bad)

        with self.assertRaises(TypeError) as ctx:
            self.checker.typecheck(pair)
        self.assertIn("UNVERIFIED", str(ctx.exception))

    def test_conjecture_produces_modal_conjecture_type(self) -> None:
        """A CONJECTURE typechecks to ConjectureType, maintaining modal separation from theorems."""
        p = Prop(
            name="HexagonalSheafPhaseTransition",
            statement="At holonomy theta = pi/3, vortex soliton exhibits chaotic bifurcation",
            status=EpistemicStatus.CONJECTURE,
        )
        w = ConjectureWitness(
            hypothesis="Phase transition at theta = pi/3",
            falsification_protocol="Sweep theta in [0, pi] on builds/kineton-sheaf-automata and compute Lyapunov exponent",
            significance_threshold=0.01,
        )
        pair = SigmaPair(first=p, second=w)
        result_type = self.checker.typecheck(pair)

        self.assertIsInstance(result_type, ConjectureType)
        self.assertNotIsInstance(result_type, SigmaType)

    def test_sigma_pair_projections(self) -> None:
        """Martin-Löf first and second projections (pi_1, pi_2) correctly unpack the pair."""
        p = Prop("A", "Statement A", EpistemicStatus.MEASURED)
        w = MeasuredWitness("path/to/receipt", "metric", 1, 1)
        pair = SigmaPair(first=p, second=w)

        self.assertEqual(pair.pi_1, p)
        self.assertEqual(pair.pi_2, w)

    def test_void_type_is_uninhabited(self) -> None:
        """The empty type 0 cannot be instantiated and reports is_inhabited() == False."""
        void = VoidType()
        self.assertFalse(void.is_inhabited())
        with self.assertRaises(ValueError):
            VoidTerm()

    def test_isomorphism_to_void(self) -> None:
        """Untyped assertions map directly to VoidType under the constructive morphism g."""
        untyped = UntypedAssertion("Unchecked assertion without proof")
        mapped_void = assert_isomorphic_to_void(untyped)
        self.assertIsInstance(mapped_void, VoidType)
        self.assertFalse(mapped_void.is_inhabited())


if __name__ == "__main__":
    unittest.main()
