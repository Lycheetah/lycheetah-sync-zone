#!/usr/bin/env python3
"""
UNIT & VERIFICATION TESTS FOR HYPOTHESIS SURRENDER & EPISTEMIC REVISION
Aura Meridian · Node 02: AURA-REVISOR
Lycheetah Multi-Agent Sync Zone

Verifies:
- Decisive single-trial falsification (K <= 0.01).
- Cumulative Bayesian evidence decay.
- Epistemic register phase transitions.
- Truth Pressure collapse (Pi < 2.50).
- Anti-immunization detection (Duhem-Quine complexity penalties).
- Legitimate scope narrowing vs forced surrender.
- Brier calibration penalty theorem for obstinate non-revision.
- Cryptographic surrender certificate integrity & tamper-proofing.
- Deterministic replay invariance.
"""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

# Ensure local module is importable
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from hypothesis_engine import (
    EpistemicRegister,
    Hypothesis,
    HypothesisState,
    Observation,
    SurrenderCertificate,
    calculate_truth_pressure,
    compute_brier_score,
    determine_epistemic_register,
    simulate_obstinate_vs_revising_agent,
)


class TestHypothesisSurrender(unittest.TestCase):
    def setUp(self):
        self.secret = b"test-aura-revisor-secret-2026"

    def test_truth_pressure_and_register_mapping(self):
        # High evidence, high power, low strain -> MEASURED
        pi_high = calculate_truth_pressure(evidence=8.5, power=9.0, strain=1.0)
        self.assertEqual(pi_high, 38.25)
        self.assertEqual(
            determine_epistemic_register(pi_high, evidence=8.5),
            EpistemicRegister.MEASURED,
        )

        # Moderate evidence -> DERIVED
        pi_med = calculate_truth_pressure(evidence=6.0, power=8.0, strain=2.0)
        self.assertEqual(pi_med, 16.0)
        self.assertEqual(
            determine_epistemic_register(pi_med, evidence=6.0),
            EpistemicRegister.DERIVED,
        )

        # Low evidence, low power, high strain -> CONJECTURE
        pi_low = calculate_truth_pressure(evidence=1.5, power=4.0, strain=7.0)
        self.assertLess(pi_low, 2.50)
        self.assertEqual(
            determine_epistemic_register(pi_low, evidence=1.5),
            EpistemicRegister.CONJECTURE,
        )

        # Surrendered hypothesis always yields FALLS
        self.assertEqual(
            determine_epistemic_register(pi_high, evidence=8.5, is_surrendered=True),
            EpistemicRegister.FALLS,
        )

    def test_decisive_single_trial_falsification(self):
        """A single observation with K <= 0.01 immediately forces surrender."""
        h = Hypothesis(
            hypothesis_id="H-UNIVERSAL-001",
            title="Universal Conservation of Static Parity",
            prior_prob=0.95,
            current_prob=0.95,
            evidence_score=8.5,
            explanatory_power=9.0,
            epistemic_strain=1.0,
            state=HypothesisState.CONFIRMED_MEASURED,
            scope_domain="Universal Q6 Worlds",
        )
        self.assertEqual(h.epistemic_register(), EpistemicRegister.MEASURED)

        # Counter-observation: P(D|H) = 0.001, P(D|~H) = 0.80 -> K = 0.00125
        obs = Observation.create(
            datum_id="OBS-COUNTER-01",
            description="Disconnected giant component observed at Hamming distance 1.0",
            outcome=0,
            likelihood_under_h=0.001,
            likelihood_under_alt=0.80,
            secret_key=self.secret,
            timestamp=1761218400.0,
        )

        state, cert = h.process_observation(obs, self.secret)

        self.assertEqual(state, HypothesisState.SURRENDERED)
        self.assertIsNotNone(cert)
        self.assertIsInstance(cert, SurrenderCertificate)
        self.assertTrue(cert.verify_certificate(self.secret))
        self.assertEqual(cert.hypothesis_id, "H-UNIVERSAL-001")
        self.assertEqual(cert.trigger_observation_id, "OBS-COUNTER-01")
        self.assertEqual(h.epistemic_register(), EpistemicRegister.FALLS)
        self.assertLess(h.current_prob, 0.05)

    def test_cumulative_bayesian_evidence_surrender(self):
        """Repeated sub-threshold negative evidence accumulates to force surrender."""
        h = Hypothesis(
            hypothesis_id="H-STOCHASTIC-002",
            title="Persistent Spectral Gap under 50% Random Dropout",
            prior_prob=0.85,
            current_prob=0.85,
            evidence_score=6.0,
            explanatory_power=7.0,
            epistemic_strain=1.5,
            state=HypothesisState.CONFIRMED_DERIVED,
            scope_domain="Affine subcubes",
        )

        # 4 successive trials with Bayes factor 0.25 (P(D|H)=0.1, P(D|~H)=0.4)
        # Cumulative K = 0.25^4 = 0.00390625 <= 0.01
        for i in range(4):
            obs = Observation.create(
                datum_id=f"OBS-BATCH-{i+1}",
                description=f"Trial {i+1}: Spectral gap collapsed to zero",
                outcome=0,
                likelihood_under_h=0.10,
                likelihood_under_alt=0.40,
                secret_key=self.secret,
                timestamp=1761218400.0 + i * 10.0,
            )
            state, cert = h.process_observation(obs, self.secret)
            if i < 3:
                self.assertIn(state, (HypothesisState.CHALLENGED, HypothesisState.CONFIRMED_DERIVED))
            else:
                self.assertEqual(state, HypothesisState.SURRENDERED)
                self.assertIsNotNone(cert)
                self.assertTrue(cert.verify_certificate(self.secret))

        self.assertLessEqual(h.cumulative_bayes_factor, 0.01)
        self.assertEqual(h.state, HypothesisState.SURRENDERED)

    def test_anti_immunization_auxiliary_patch_penalty(self):
        """Ad-hoc auxiliary patches without independent evidence inflate strain and force surrender."""
        h = Hypothesis(
            hypothesis_id="H-RESISTANT-003",
            title="Inflexible Vorticity Claim",
            prior_prob=0.80,
            current_prob=0.80,
            evidence_score=4.0,
            explanatory_power=6.0,
            epistemic_strain=3.0,
            state=HypothesisState.CHALLENGED,
            scope_domain="All Reynolds Numbers",
        )

        # Patch 1: "The sensor was slightly off" (complexity=3.0, independent_evidence=0.0)
        success_1 = h.attempt_auxiliary_patch(
            patch_id="PATCH-01",
            description="Sensor calibration offset excuse",
            complexity_cost=3.0,
            independent_evidence=0.0,
            secret_key=self.secret,
        )
        self.assertTrue(success_1)
        self.assertEqual(h.epistemic_strain, 6.0)

        # Patch 2: "Temperature fluctuation excuse" (complexity=3.5, independent_evidence=0.0)
        # Strain becomes 6.0 + 3.5 = 9.5. Pi = (4.0 * 6.0) / (9.5 + 1.0) = 24.0 / 10.5 = 2.2857 < 2.50
        # Collapses below conjecture threshold -> Surrender forced
        success_2 = h.attempt_auxiliary_patch(
            patch_id="PATCH-02",
            description="Thermal noise excuse",
            complexity_cost=3.5,
            independent_evidence=0.0,
            secret_key=self.secret,
        )
        self.assertFalse(success_2)
        self.assertEqual(h.state, HypothesisState.SURRENDERED)
        self.assertIsNotNone(h.surrender_certificate)
        self.assertTrue(h.surrender_certificate.verify_certificate(self.secret))
        self.assertIn("Anti-immunization rule triggered", h.surrender_certificate.surrender_reason)

    def test_legitimate_scope_narrowing(self):
        """Legitimate narrowing to an unaffected sub-domain resets strain and preserves claim."""
        h = Hypothesis(
            hypothesis_id="H-KELVIN-004",
            title="Kelvin Circulation Invariance",
            prior_prob=0.90,
            current_prob=0.90,
            evidence_score=7.0,
            explanatory_power=8.0,
            epistemic_strain=4.0,
            state=HypothesisState.CHALLENGED,
            scope_domain="All Fluid Flows",
        )

        success = h.narrow_scope(
            new_subdomain="Inviscid Barotropic Fluids (nu = 0)",
            justification="Kelvin theorem mathematically holds in zero viscosity limit",
            residual_strain=1.0,
        )
        self.assertTrue(success)
        self.assertEqual(h.state, HypothesisState.NARROWED)
        self.assertEqual(h.scope_domain, "Inviscid Barotropic Fluids (nu = 0)")
        self.assertEqual(h.epistemic_strain, 1.0)
        # Truth pressure restored: (7.0 * 8.0) / (1.0 + 1.0) = 28.0 (DERIVED)
        self.assertGreaterEqual(h.truth_pressure(), 18.0)

    def test_brier_penalty_simulation_rational_vs_obstinate(self):
        """Obstinate non-revision incurs severe Brier score inflation."""
        # 10 trials of an erroneous hypothesis: actual outcome is always 0
        observations = [
            Observation.create(
                datum_id=f"OBS-TRIAL-{t+1}",
                description=f"Negative trial {t+1}",
                outcome=0,
                likelihood_under_h=0.05,
                likelihood_under_alt=0.95,
                secret_key=self.secret,
                timestamp=1761218400.0 + t,
            )
            for t in range(10)
        ]

        res = simulate_obstinate_vs_revising_agent(
            initial_prior=0.90,
            observations=observations,
            secret_key=self.secret,
        )

        self.assertEqual(res["n_trials"], 10)
        self.assertEqual(res["revising_final_state"], HypothesisState.SURRENDERED.value)
        self.assertLess(res["revising_final_prob"], 0.05)

        # Obstinate agent has Brier = 0.90^2 = 0.81
        self.assertAlmostEqual(res["obstinate_brier"], 0.81, places=4)
        # Revising agent quickly drops to ~0.0, yielding much lower Brier
        self.assertLess(res["revising_brier"], 0.15)
        self.assertGreater(res["brier_penalty"], 0.65)
        self.assertGreater(res["obstinate_brier_inflation_ratio"], 5.0)

    def test_surrender_certificate_tamper_detection(self):
        """Any mutation to a SurrenderCertificate invalidates its HMAC signature."""
        cert = SurrenderCertificate.issue(
            certificate_id="CERT-TAMPER-TEST",
            hypothesis_id="H-TAMPER",
            initial_prior=0.95,
            final_posterior=0.005,
            cumulative_bayes_factor=0.001,
            initial_truth_pressure=32.0,
            terminal_truth_pressure=1.2,
            trigger_observation_id="OBS-CRIT-99",
            surrender_reason="Decisive falsification",
            secret_key=self.secret,
        )
        self.assertTrue(cert.verify_certificate(self.secret))

        # Tamper with wrong key
        wrong_key = b"malicious-attacker-key"
        self.assertFalse(cert.verify_certificate(wrong_key))

        # Tamper with internal data using replacement dataclass
        tampered_cert = SurrenderCertificate(
            certificate_id=cert.certificate_id,
            hypothesis_id=cert.hypothesis_id,
            initial_prior=cert.initial_prior,
            final_posterior=0.99,  # Maliciously altered posterior!
            cumulative_bayes_factor=cert.cumulative_bayes_factor,
            initial_truth_pressure=cert.initial_truth_pressure,
            terminal_truth_pressure=cert.terminal_truth_pressure,
            terminal_register=cert.terminal_register,
            trigger_observation_id=cert.trigger_observation_id,
            surrender_reason=cert.surrender_reason,
            timestamp=cert.timestamp,
            origin_hmac=cert.origin_hmac,
        )
        self.assertFalse(tampered_cert.verify_certificate(self.secret))

    def test_deterministic_replay(self):
        """Identical inputs produce bit-for-bit identical state and Bayes factors."""
        def run_sim():
            h = Hypothesis(
                hypothesis_id="H-DETERMINISM",
                title="Determinism Test",
                prior_prob=0.80,
                current_prob=0.80,
                evidence_score=5.0,
                explanatory_power=6.0,
                epistemic_strain=1.0,
                state=HypothesisState.TENTATIVE,
                scope_domain="Universal",
            )
            for k in range(3):
                obs = Observation.create(
                    datum_id=f"OBS-DET-{k}",
                    description=f"Det obs {k}",
                    outcome=0,
                    likelihood_under_h=0.15,
                    likelihood_under_alt=0.75,
                    secret_key=self.secret,
                    timestamp=1000.0 + k * 10.0,
                )
                h.process_observation(obs, self.secret)
            return h.current_prob, h.cumulative_bayes_factor, h.state

        prob_1, bf_1, state_1 = run_sim()
        prob_2, bf_2, state_2 = run_sim()

        self.assertEqual(prob_1, prob_2)
        self.assertEqual(bf_1, bf_2)
        self.assertEqual(state_1, state_2)


if __name__ == "__main__":
    unittest.main()
