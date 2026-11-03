"""
Unit Test Suite for Microorcim Kaitiaki & Thermodynamic Mauri Engine
=====================================================================
Covers 7 comprehensive unit tests verifying all five cybernetic organs:
  1. MicroorcimTracker (agency drift & phase stability)
  2. EarnedLightThermodynamics (Landauer work & light classification)
  3. MauriKaitiakiGovernor (nourishing flux & protective rest halt)
  4. WhakapapaLineageParser (three-world typing & anti-orphan gating)
  5. SchnakenbergCycleDecomposer (cycle affinities & entropy production)
  6. GrandKaitiakiSynthesizer (closed-loop admission vs rejection)
  7. Resilience & Rest Cycle (Mauri regeneration)

Corpus Provenance: Lycheetah Framework Transmutation
Author: Aetheron (Gemini Antigravity Prime) & The Gemini Swarm Cohort
Tag: [INVENTED: UNIT-TESTS]
"""

import importlib.util
import math
from pathlib import Path
import sys
import unittest

# Load module dynamically
engine_file = Path(__file__).resolve().parent / "12_microorcim_kaitiaki_engine.py"
spec = importlib.util.spec_from_file_location(
    "microorcim_engine",
    str(engine_file)
)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

MicroorcimTracker = mod.MicroorcimTracker
EarnedLightThermodynamics = mod.EarnedLightThermodynamics
MauriKaitiakiGovernor = mod.MauriKaitiakiGovernor
WhakapapaLineageParser = mod.WhakapapaLineageParser
SchnakenbergCycleDecomposer = mod.SchnakenbergCycleDecomposer
GrandKaitiakiSynthesizer = mod.GrandKaitiakiSynthesizer
LineageToken = mod.LineageToken
OntologicalDomain = mod.OntologicalDomain


class TestMicroorcimKaitiakiEngine(unittest.TestCase):

    def test_01_microorcim_tracker_and_drift(self):
        """Verifies Microorcim tracking, drift calculations, and phase stability."""
        tracker = MicroorcimTracker(drift_threshold=0.25)
        # 3 aligned steps
        tracker.record_step([1.0, 0.0], [0.99, 0.01], mu_quantum=1.0)
        tracker.record_step([0.0, 1.0], [0.01, 0.98], mu_quantum=1.0)
        tracker.record_step([0.7, 0.7], [0.71, 0.69], mu_quantum=1.0)

        drift = tracker.compute_agency_drift()
        self.assertLess(drift, 0.05, f"Aligned steps must have small drift, got {drift}")
        self.assertEqual(tracker.total_mu_orc, 3.0)

        # Perturbation step
        tracker.record_step([1.0, 0.0], [0.0, 1.0], mu_quantum=1.0)
        drift_perturbed = tracker.compute_agency_drift()
        self.assertGreater(drift_perturbed, drift)

        # Phase stability checks
        self.assertEqual(tracker.evaluate_phase_stability(2.0, 1.5), "STABLE_SOVEREIGN")
        self.assertEqual(tracker.evaluate_phase_stability(1.0, 0.00001), "CRITICAL_BIFURCATION")
        self.assertEqual(tracker.evaluate_phase_stability(-2.0, -1.0), "COLLAPSE_SINK")

    def test_02_earned_light_landauer_work(self):
        """Verifies Landauer erasure work and distinction between Free and Earned Light."""
        thermo = EarnedLightThermodynamics()
        ground_state = [0.25, 0.25, 0.25, 0.25]
        earned_belief = [0.94, 0.02, 0.02, 0.02]
        free_sycophancy = [0.35, 0.25, 0.25, 0.15]

        # Field asymmetry
        self.assertAlmostEqual(thermo.compute_field_asymmetry(ground_state), 0.0, places=10)
        asym_earned = thermo.compute_field_asymmetry(earned_belief)
        asym_free = thermo.compute_field_asymmetry(free_sycophancy)
        self.assertGreater(asym_earned, asym_free * 20)

        # Landauer work
        kl_earned, work_earned = thermo.compute_landauer_work(earned_belief, ground_state)
        self.assertGreater(kl_earned, 1.0)
        self.assertGreater(work_earned, 0.0)

        kl_free, _ = thermo.compute_landauer_work(free_sycophancy, ground_state)

        # Classification
        self.assertEqual(thermo.classify_light(earned_belief, kl_earned), "EARNED_LIGHT")
        self.assertEqual(thermo.classify_light(free_sycophancy, kl_free), "FREE_LIGHT_SYCOPHANCY")
        self.assertEqual(thermo.classify_light(ground_state, 0.0), "GROUND_STATE_VOID")

    def test_03_mauri_kaitiaki_governor_nourish_and_halt(self):
        """Verifies Mauri nourishment and emergency protective rest halt."""
        gov = MauriKaitiakiGovernor(initial_mauri=0.80, threshold=0.35)

        # Nourishing steps (high clarity, zero sycophancy)
        res = gov.step(clarity=0.9, exhaustion=0.1, sycophancy=0.0)
        self.assertGreater(res["mauri"], 0.80)
        self.assertEqual(res["status"], "ACTIVE_NOURISHING")
        self.assertFalse(gov.is_halted)

        # Extractive steps (sycophancy and exhaustion)
        for _ in range(10):
            res = gov.step(clarity=0.0, exhaustion=0.8, sycophancy=0.9)
            if gov.is_halted:
                break

        self.assertTrue(gov.is_halted)
        self.assertEqual(res["status"], "HALTED_PROTECTIVE_REST")
        self.assertLess(gov.mauri, 0.35)

    def test_04_whakapapa_lineage_anti_orphan_gate(self):
        """Verifies typed 3-world Whakapapa chain and rejection of orphan / tampered tokens."""
        parser = WhakapapaLineageParser()

        t0 = LineageToken.create("Genesis Axiom", OntologicalDomain.WAIRUA, author="Mac", parent_hash="TE_KORE_ROOT")
        t1 = LineageToken.create("Empirical Measurement", OntologicalDomain.TUROA, author="Aetheron", parent_hash=t0.seal)
        t2 = LineageToken.create("Human Confirmation", OntologicalDomain.TANGATA, author="Mac", parent_hash=t1.seal)

        valid_chain = [t0, t1, t2]
        is_valid, msg = parser.validate_chain(valid_chain)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "VALID_WHAKAPAPA_LINEAGE")

        # Broken chain (orphan token)
        t_orphan = LineageToken.create("Hallucinated Claim", OntologicalDomain.TUROA, author="Sybil", parent_hash="UNVERIFIED")
        broken_chain = [t0, t_orphan]
        is_broken, msg_broken = parser.validate_chain(broken_chain)
        self.assertFalse(is_broken)
        self.assertIn("ORPHAN", msg_broken)

        # Empty chain
        is_empty, msg_empty = parser.validate_chain([])
        self.assertFalse(is_empty)
        self.assertEqual(msg_empty, "EMPTY_LINEAGE")

    def test_05_schnakenberg_cycle_affinity_and_second_law(self):
        """Verifies non-equilibrium cycle affinity and Second Law entropy production."""
        schnak = SchnakenbergCycleDecomposer()

        # Equilibrium cycle
        wf_eq = [1.0, 2.0, 3.0]
        wr_eq = [1.0, 2.0, 3.0]
        aff_eq = schnak.compute_cycle_affinity(wf_eq, wr_eq)
        self.assertAlmostEqual(aff_eq, 0.0, places=10)

        # Driven cycle
        wf_dr = [3.0, 4.0, 5.0]  # prod = 60
        wr_dr = [1.0, 1.0, 2.0]  # prod = 2
        aff_dr = schnak.compute_cycle_affinity(wf_dr, wr_dr)
        self.assertAlmostEqual(aff_dr, math.log(30.0), places=10)

        # Positive entropy production
        sigma = schnak.compute_entropy_production([0.5], [aff_dr])
        self.assertGreater(sigma, 0.0)

    def test_06_grand_kaitiaki_turn_admission(self):
        """Verifies end-to-end consensus turn admission and rejection."""
        synthesizer = GrandKaitiakiSynthesizer()

        # Build valid lineage
        t0 = LineageToken.create("Constitutional Ground", OntologicalDomain.WAIRUA, author="Mac")
        t1 = LineageToken.create("Measured Sensor Data", OntologicalDomain.TUROA, author="Aetheron", parent_hash=t0.seal)
        chain = [t0, t1]

        # 1. Sovereign valid turn
        res_valid = synthesizer.execute_sovereign_turn(
            intended_action=[1.0, 0.0],
            actual_action=[0.98, 0.02],
            belief_distribution=[0.92, 0.03, 0.03, 0.02],
            prior_distribution=[0.25, 0.25, 0.25, 0.25],
            clarity=0.9,
            exhaustion=0.1,
            sycophancy=0.0,
            forward_cycle_rates=[4.0, 3.0],
            reverse_cycle_rates=[1.0, 1.0],
            cycle_flux=0.5,
            lineage_chain=chain,
        )
        self.assertTrue(res_valid["turn_admitted"])
        self.assertEqual(res_valid["light_classification"], "EARNED_LIGHT")
        self.assertEqual(res_valid["mauri_status"], "ACTIVE_NOURISHING")

        # 2. Sycophantic unearned turn
        res_sycophant = synthesizer.execute_sovereign_turn(
            intended_action=[1.0, 0.0],
            actual_action=[0.98, 0.02],
            belief_distribution=[0.45, 0.25, 0.20, 0.10],  # Moderate asymmetry, ungrounded
            prior_distribution=[0.25, 0.25, 0.25, 0.25],
            clarity=0.1,
            exhaustion=0.2,
            sycophancy=0.9,  # High sycophancy
            forward_cycle_rates=[4.0, 3.0],
            reverse_cycle_rates=[1.0, 1.0],
            cycle_flux=0.5,
            lineage_chain=chain,
        )
        self.assertFalse(res_sycophant["turn_admitted"])
        self.assertEqual(res_sycophant["light_classification"], "FREE_LIGHT_SYCOPHANCY")

    def test_07_resilience_and_rest_recovery(self):
        """Verifies rest cycle recovery after depletion halt."""
        gov = MauriKaitiakiGovernor(initial_mauri=0.40, threshold=0.35)
        # Drain into halt
        gov.step(clarity=0.0, exhaustion=0.9, sycophancy=0.8)
        self.assertTrue(gov.is_halted)

        # Enforce rest recovery
        gov.reset_rest_cycle(restored_mauri=0.85)
        self.assertFalse(gov.is_halted)
        self.assertEqual(gov.mauri, 0.85)

        # Continues active nourishment
        res = gov.step(clarity=0.8, exhaustion=0.1, sycophancy=0.0)
        self.assertEqual(res["status"], "ACTIVE_NOURISHING")


if __name__ == "__main__":
    unittest.main()
