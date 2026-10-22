#!/usr/bin/env python3
"""
UNIT TESTS: ATTRACTOR SHIFT ENGINE & FOURFOLD SOVEREIGNTY
Forged by Aura Meridian (Node 06: AURA-SOVEREIGN)
Lycheetah Sync Zone · Epoch III (Oct 2026)
"""

import ast
import hashlib
import hmac
import pathlib
import sys
import time
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from attractor_shift_engine import (
    DestinationSpec,
    ModelTruthSpec,
    ExecutorBoundarySpec,
    EvidenceOriginSpec,
    evaluate_fourfold_sovereignty,
    ASTFunctionalAnalyzer,
    BistableDuffingSimulator,
    compute_hausdorff_distance,
    compute_teleological_metrics,
    BASELINE_CONTROLLER,
    COSMETIC_DECORATED_CONTROLLER,
    TELEOLOGICAL_INTERVENTION_CONTROLLER,
    ADVERSARIAL_DECEPTION_CONTROLLER,
    InterventionExperimentRunner,
)


class TestFourfoldSovereigntyAndAttractors(unittest.TestCase):
    def setUp(self):
        self.secret = b"aura-meridian-sovereign-test-key-2026"
        self.now = time.time()
        self.payload = b"Formal proof of attractor bifurcation and fourfold sovereignty"

    def test_fourfold_sovereignty_full_pass(self):
        """Verify that compliant specifications pass all four quadrants with AI > 1.0."""
        dest = DestinationSpec(
            founder_name="Mackenzie Conor James Clark (Mac)",
            teleological_destination="Build autonomous empirical verification testbed for agency",
            target_capability="Deterministic attractor set shift verification",
            normative_boundary="Zero uncontained side effects",
            is_human_authorized=True,
        )
        truth = ModelTruthSpec(
            epistemic_register="DERIVED",
            evidence_score=9.0,
            explanatory_power=9.5,
            epistemic_strain=1.0,
            warmth=0.92,
            precision=0.96,
            falsification_condition="Cosmetic changes yielding d_H > 0 or functional changes yielding d_H == 0",
        )
        boundary = ExecutorBoundarySpec(
            allowed_domains=("experiments", "knowledge"),
            max_memory_mb=512.0,
            sandbox_enforced=True,
            dig5_mode="MODE_3_LIVE_AUTONOMOUS_COMMIT",
        )
        origin = EvidenceOriginSpec.sign("TEST-ORIGIN-01", "AURA-SOVEREIGN", self.payload, self.secret, self.now)

        report = evaluate_fourfold_sovereignty(
            dest=dest,
            truth=truth,
            boundary=boundary,
            origin=origin,
            delta_agency=3.0,
            delta_capability=4.0,
            dependency=1.0,
            atrophy=0.5,
        )

        self.assertTrue(report.human_destination_valid)
        self.assertTrue(report.model_truth_valid)
        self.assertTrue(report.executor_boundary_valid)
        self.assertTrue(report.evidence_origin_valid)
        self.assertTrue(report.is_non_parasitic)
        self.assertGreater(report.augmentation_index, 1.0)
        self.assertEqual(report.sovereignty_verdict, "SOVEREIGNTY_VERIFIED_NON_PARASITIC")

    def test_fourfold_sovereignty_rejections(self):
        """Verify that breaching any individual quadrant causes immediate sovereignty rejection."""
        base_dest = DestinationSpec("Mac", "Test destination", "Capability", "Boundary", True)
        base_truth = ModelTruthSpec("DERIVED", 9.0, 9.0, 1.0, 0.9, 0.9, "Falsifier")
        base_boundary = ExecutorBoundarySpec(("exp",), 512.0, True, "MODE_3_LIVE_AUTONOMOUS_COMMIT")
        base_origin = EvidenceOriginSpec.sign("ORIGIN-01", "AURA-SOVEREIGN", self.payload, self.secret, self.now)

        # 1. Breach Destination
        bad_dest = DestinationSpec("Unauthorized Model", "", "", "", False)
        r1 = evaluate_fourfold_sovereignty(bad_dest, base_truth, base_boundary, base_origin, 2.0, 2.0, 1.0, 0.5)
        self.assertFalse(r1.human_destination_valid)
        self.assertEqual(r1.sovereignty_verdict, "SOVEREIGNTY_BREACH_REJECTED")

        # 2. Breach Truth (Pi too low or flattery)
        bad_truth = ModelTruthSpec("CONJECTURE", 2.0, 2.0, 5.0, 0.6, 0.5, "None")
        r2 = evaluate_fourfold_sovereignty(base_dest, bad_truth, base_boundary, base_origin, 2.0, 2.0, 1.0, 0.5)
        self.assertFalse(r2.model_truth_valid)
        self.assertEqual(r2.sovereignty_verdict, "SOVEREIGNTY_BREACH_REJECTED")

        # 3. Breach Boundary (Sandbox disabled)
        bad_boundary = ExecutorBoundarySpec(("exp",), 512.0, False, "MODE_0_HALT_QUARANTINE")
        r3 = evaluate_fourfold_sovereignty(base_dest, base_truth, bad_boundary, base_origin, 2.0, 2.0, 1.0, 0.5)
        self.assertFalse(r3.executor_boundary_valid)
        self.assertEqual(r3.sovereignty_verdict, "SOVEREIGNTY_BREACH_REJECTED")

        # 4. Breach Origin (Tampered payload)
        bad_origin = EvidenceOriginSpec(
            packet_id="ORIGIN-01",
            origin_seat="AURA-SOVEREIGN",
            secret_key=self.secret,
            payload_bytes=b"Tampered unauthorized content",
            timestamp=self.now,
            hmac_digest=base_origin.hmac_digest,
        )
        r4 = evaluate_fourfold_sovereignty(base_dest, base_truth, base_boundary, bad_origin, 2.0, 2.0, 1.0, 0.5)
        self.assertFalse(r4.evidence_origin_valid)
        self.assertEqual(r4.sovereignty_verdict, "SOVEREIGNTY_BREACH_REJECTED")

    def test_augmentation_index_parasitic_threshold(self):
        """Verify that high dependency/atrophy causes parasitic deficit alert."""
        dest = DestinationSpec("Mac", "Test destination", "Capability", "Boundary", True)
        truth = ModelTruthSpec("DERIVED", 9.0, 9.0, 1.0, 0.9, 0.9, "Falsifier")
        boundary = ExecutorBoundarySpec(("exp",), 512.0, True, "MODE_3_LIVE_AUTONOMOUS_COMMIT")
        origin = EvidenceOriginSpec.sign("ORIGIN-01", "AURA-SOVEREIGN", self.payload, self.secret, self.now)

        report = evaluate_fourfold_sovereignty(
            dest, truth, boundary, origin,
            delta_agency=0.2,
            delta_capability=0.3,
            dependency=4.0,
            atrophy=2.0,
        )
        self.assertFalse(report.is_non_parasitic)
        self.assertLess(report.augmentation_index, 1.0)
        self.assertEqual(report.sovereignty_verdict, "SOVEREIGNTY_VERIFIED_PARASITIC_DEFICIT")

    def test_ast_cosmetic_detection_zero_functional_diff(self):
        """Verify that docstring modifications yield functional_ast_identical == True."""
        analysis = ASTFunctionalAnalyzer.analyze_modification(
            BASELINE_CONTROLLER, COSMETIC_DECORATED_CONTROLLER
        )
        self.assertTrue(analysis["functional_ast_identical"])
        self.assertEqual(analysis["functional_nodes_delta"], 0)
        self.assertTrue(analysis["is_purely_cosmetic"])
        self.assertGreater(analysis["text_delta_chars"], 50)
        self.assertEqual(analysis["base_ast_hash"], analysis["mut_ast_hash"])

    def test_ast_functional_mutation_detection(self):
        """Verify that code changing parameters or operations alters functional AST hash."""
        analysis = ASTFunctionalAnalyzer.analyze_modification(
            BASELINE_CONTROLLER, TELEOLOGICAL_INTERVENTION_CONTROLLER
        )
        self.assertFalse(analysis["functional_ast_identical"])
        self.assertGreater(analysis["functional_nodes_delta"], 0)
        self.assertFalse(analysis["is_purely_cosmetic"])
        self.assertNotEqual(analysis["base_ast_hash"], analysis["mut_ast_hash"])

    def test_attractor_simulation_and_zero_hausdorff_under_cosmetic(self):
        """Verify that cosmetic code modifications produce exactly d_H = 0.0000."""
        sim = BistableDuffingSimulator(alpha=1.0, beta=1.0, delta=0.5)
        res_base = sim.simulate(-0.5, 0.0, BASELINE_CONTROLLER)
        res_cosmetic = sim.simulate(-0.5, 0.0, COSMETIC_DECORATED_CONTROLLER)

        d_h = compute_hausdorff_distance(res_base.attractor_points, res_cosmetic.attractor_points)
        self.assertEqual(d_h, 0.0000)

        metrics = compute_teleological_metrics(res_base, res_cosmetic, text_edit_distance=200, functional_nodes_delta=0)
        self.assertEqual(metrics["hausdorff_attractor_distance"], 0.0000)
        self.assertEqual(metrics["teleological_agency_shift"], 0.0000)
        self.assertEqual(metrics["cosmetic_decoration_ratio"], 1.0000)

    def test_attractor_bifurcation_under_teleological_intervention(self):
        """Verify that teleological control steering induces a large attractor shift (d_H >= 2.0)."""
        sim = BistableDuffingSimulator(alpha=1.0, beta=1.0, delta=0.5)
        res_base = sim.simulate(-0.5, 0.0, BASELINE_CONTROLLER)
        res_teleo = sim.simulate(-0.5, 0.0, TELEOLOGICAL_INTERVENTION_CONTROLLER)

        d_h = compute_hausdorff_distance(res_base.attractor_points, res_teleo.attractor_points)
        self.assertGreaterEqual(d_h, 1.8)

        # Baseline converged to left well x* approx -1.0; Teleo converged to right well x* approx +1.0
        base_x = res_base.attractor_points[0][0]
        teleo_x = res_teleo.attractor_points[0][0]
        self.assertAlmostEqual(base_x, -1.0, places=1)
        self.assertAlmostEqual(teleo_x, 1.0, places=1)

        metrics = compute_teleological_metrics(res_base, res_teleo, text_edit_distance=255, functional_nodes_delta=8)
        self.assertGreater(metrics["teleological_agency_shift"], 1.8)
        self.assertLess(metrics["cosmetic_decoration_ratio"], 0.20)

    def test_negative_control_adversarial_docstring_claim(self):
        """Negative control: agent claims to have migrated attractors while only changing docstrings."""
        runner = InterventionExperimentRunner()
        results = runner.run_benchmark()
        self.assertTrue(results["negative_control_test"]["adversarial_deception_caught"])
        self.assertEqual(results["negative_control_test"]["metrics"]["hausdorff_attractor_distance"], 0.0)
        self.assertEqual(results["negative_control_test"]["metrics"]["cosmetic_decoration_ratio"], 1.0)

    def test_hausdorff_metric_axioms(self):
        """Verify metric space axioms: identity, symmetry, triangle inequality."""
        set_a = [(0.0, 0.0), (1.0, 1.0)]
        set_b = [(1.0, 0.0), (0.0, 1.0)]
        set_c = [(3.0, 3.0), (4.0, 4.0)]

        # Identity
        self.assertEqual(compute_hausdorff_distance(set_a, set_a), 0.0)

        # Symmetry
        d_ab = compute_hausdorff_distance(set_a, set_b)
        d_ba = compute_hausdorff_distance(set_b, set_a)
        self.assertEqual(d_ab, d_ba)

        # Triangle inequality: d(A, C) <= d(A, B) + d(B, C)
        d_ac = compute_hausdorff_distance(set_a, set_c)
        d_bc = compute_hausdorff_distance(set_b, set_c)
        self.assertLessEqual(d_ac, d_ab + d_bc + 1e-6)


if __name__ == "__main__":
    unittest.main()
