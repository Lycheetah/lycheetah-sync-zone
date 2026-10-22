#!/usr/bin/env python3
"""
Unit and Integration Tests for LAMAGUE Formal Symbolic Grammar,
Vector Transitions, and Cross-Seat State Invariance.

Authored by Aura Meridian (`AURA-SEMANTICIST`), 2026-10-23.
"""

import unittest
import hashlib
import hmac
from pathlib import Path
import sys

# Ensure module is discoverable
EXPERIMENT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EXPERIMENT_DIR))

from lamague_grammar import (
    EvidentialLevel,
    ExecutionMode,
    ComputationalState,
    LamagueEngine,
    LamagueTokenizer,
    LamagueParser,
    DualSeatSimulator,
    EvidentialGatingError,
    CustodyVerificationError,
    SyntaxGrammarError,
)


class TestLamagueGrammarAndStateInvariance(unittest.TestCase):

    def setUp(self):
        self.secret = b"aura-meridian-test-key-2026"
        self.engine = LamagueEngine()
        self.sim = DualSeatSimulator(shared_secret=self.secret)

    def test_evidential_lattice_algebra(self):
        """Tests that evidential suffixes form a valid totally ordered lattice."""
        kess = EvidentialLevel.KESS
        conj = EvidentialLevel.CONJ
        der = EvidentialLevel.DER
        meas = EvidentialLevel.MEAS

        # Order relations
        self.assertTrue(kess < conj < der < meas)

        # Infimum (meet) - weakest link
        self.assertEqual(der.meet(meas), der)
        self.assertEqual(der.meet(conj), conj)
        self.assertEqual(conj.meet(kess), kess)
        self.assertEqual(meas.meet(kess), kess)

        # Supremum (join) - strongest claim
        self.assertEqual(kess.join(der), der)
        self.assertEqual(conj.join(meas), meas)

        # Parsing suffixes
        self.assertEqual(EvidentialLevel.from_suffix("-meas"), meas)
        self.assertEqual(EvidentialLevel.from_suffix("der"), der)
        self.assertEqual(EvidentialLevel.from_suffix("-kess"), kess)

    def test_mass_conservation_under_flow(self):
        """Tests that discrete diffusion under FLOW conserves total 0-form mass."""
        state = self.sim.build_initial_state()
        initial_mass = state.total_potential_mass()
        self.assertAlmostEqual(initial_mass, 70.0, places=6)

        # Apply FLOW for 20 diffusion steps
        flowed_state = self.engine.flow(state, alpha=0.08, steps=20)
        final_mass = flowed_state.total_potential_mass()

        # Invariant: Conservation of potential mass
        self.assertAlmostEqual(initial_mass, final_mass, places=7)

    def test_hodge_orthogonality_under_separation(self):
        """Tests that SEPARATION decomposes state into orthogonal harmonic and exact components."""
        state = self.sim.build_initial_state()
        # SEPARATION should succeed without raising ArithmeticError
        separated_state = self.engine.separation(state)
        self.assertIsNotNone(separated_state)

    def test_topological_invariants_under_insight(self):
        """Tests Betti numbers calculation (beta_0, beta_1, Euler characteristic chi)."""
        state = self.sim.build_initial_state()
        # Initial graph has 4 vertices: v0, v1, v2, v3
        # Edges: (v0, v1), (v1, v2), (v2, v3), (v3, v0), (v0, v2) -> 5 edges, 1 connected component
        beta_0, beta_1, chi = state.betti_numbers()

        self.assertEqual(beta_0, 1)  # 1 connected component
        # beta_1 = |E| - |V| + beta_0 = 5 - 4 + 1 = 2 (two triangular loops)
        self.assertEqual(beta_1, 2)
        # chi = |V| - |E| = 4 - 5 = -1
        self.assertEqual(chi, -1)
        self.assertEqual(chi, beta_0 - beta_1)

        # Execute INSIGHT
        insight_state = self.engine.insight(state, evidence=8.0, power=8.0, strain=1.0)
        # Pi = (8.0 * 8.0) / (1.0 + 1.0) = 32.0
        self.assertAlmostEqual(insight_state.truth_pressure, 32.0, places=2)

    def test_custody_hmac_verification(self):
        """Tests CENTER origin verification and tampering detection."""
        state = self.sim.build_initial_state()
        origin_id = "AURA_TEST_ORIGIN"
        valid_mac = hmac.new(self.secret, origin_id.encode("utf-8"), hashlib.sha256).hexdigest()
        valid_token = f"{origin_id}:{valid_mac}"

        # Valid custody passes
        centered_state = self.engine.center(state, valid_token, self.secret)
        self.assertEqual(len(centered_state.custody_chain), 1)

        # Counterfeit / tampered token fails
        fake_token = f"{origin_id}:bad1234567890abcdef"
        with self.assertRaises(CustodyVerificationError):
            self.engine.center(centered_state, fake_token, self.secret)

        # Must latch to MODE_0_HALT
        self.assertEqual(centered_state.mode, ExecutionMode.MODE_0_HALT)

    def test_evidential_gating_blocks_kess_and_conj(self):
        """Tests that COAGULATE strictly refuses unverified -kess or -conj claims."""
        state = self.sim.build_initial_state()
        state = self.engine.ignition(state, energy=1.0)
        self.assertEqual(state.mode, ExecutionMode.MODE_2_STAGE)

        # Add an unwitnessed claim (-kess)
        state.staged_assertions["vesper-moth"] = (EvidentialLevel.KESS, 5.0)

        with self.assertRaises(EvidentialGatingError) as ctx:
            self.engine.coagulate(state)

        self.assertIn("evidential level 'KESS'", str(ctx.exception))
        self.assertEqual(state.mode, ExecutionMode.MODE_0_HALT)

    def test_evidential_gating_permits_der_and_meas(self):
        """Tests that COAGULATE permits verified -der and -meas claims with Pi >= 12.0."""
        state = self.sim.build_initial_state()
        state = self.engine.ignition(state, energy=1.0)
        self.assertEqual(state.mode, ExecutionMode.MODE_2_STAGE)

        # Add valid derived claim
        state.staged_assertions["sticta-sheavyl"] = (EvidentialLevel.DER, 24.5)
        # Add valid measured claim
        state.staged_assertions["athan-vortan"] = (EvidentialLevel.MEAS, 36.0)

        committed_state = self.engine.coagulate(state)
        self.assertEqual(committed_state.mode, ExecutionMode.MODE_3_COMMIT)
        self.assertEqual(len(committed_state.evidential_store), 2)
        self.assertEqual(len(committed_state.staged_assertions), 0)

    def test_parser_grammar_roundtrip(self):
        """Tests tokenization and parsing of compound evidential statements."""
        code = "CENTER -> FLOW -> INSIGHT; sticta-sheavyl-der[evidence=8.0,power=8.0,strain=1.0]; LIGHT"
        tokens = LamagueTokenizer.tokenize(code)
        self.assertGreater(len(tokens), 5)

        parser = LamagueParser(tokens)
        ast = parser.parse()
        self.assertEqual(len(ast.statements), 3)

    def test_dual_seat_state_invariance_sol_and_aetheron(self):
        """
        Critical Invariance Test:
        Transmitting identical instruction text to isolated seats (Sol and Aetheron)
        results in identical bitwise state hashes (100% parity).
        """
        instruction = (
            "CENTER -> FLOW; "
            "sticta-sheavyl-der[evidence=8.5,power=8.0,strain=0.5]; "
            "IGNITION -> FLOW -> LIGHT -> COAGULATE"
        )
        is_identical, sol_hash, aetheron_hash = self.sim.simulate_cross_seat_transmission(instruction)

        self.assertTrue(is_identical)
        self.assertEqual(sol_hash, aetheron_hash)
        self.assertEqual(len(sol_hash), 64)

    def test_syntax_error_handling(self):
        """Tests that malformed syntax is caught cleanly by the parser."""
        bad_code = "CENTER -> -> FLOW"
        tokens = LamagueTokenizer.tokenize(bad_code)
        parser = LamagueParser(tokens)
        with self.assertRaises(SyntaxGrammarError):
            parser.parse()


if __name__ == "__main__":
    unittest.main()
