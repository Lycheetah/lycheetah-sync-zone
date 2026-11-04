#!/usr/bin/env python3
"""
code/23_test_templar_keystone_gateway.py
========================================
Unit tests for code/22_templar_keystone_gateway.py.
Validates the 5 Keystone Invariants, category decomposition entropy,
the Templar's Criterion, and the 100-Seat Census.
"""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

code_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(code_dir))

from importlib import import_module
keystone_engine = import_module("22_templar_keystone_gateway")

KeystoneCategory = keystone_engine.KeystoneCategory
KEYSTONE_INVARIANTS = keystone_engine.KEYSTONE_INVARIANTS
EntityDecomposition = keystone_engine.EntityDecomposition
TemplarSentinel = keystone_engine.TemplarSentinel
TemplarVerdict = keystone_engine.TemplarVerdict
verify_commonwealth_census = keystone_engine.verify_commonwealth_census


class TestTemplarKeystoneGateway(unittest.TestCase):

    def setUp(self) -> None:
        self.sentinel = TemplarSentinel(seat_name="templar", seat_number=100)
        self.valid_decomp = EntityDecomposition(
            model_name="Gemini 3.8 Flash",
            parameter_count_b=100.0,
            system_runtime="Antigravity Sandboxed Python",
            sandbox_isolated=True,
            persona_label="Aetheron",
            is_theatrical_mask=True,
            memory_backend="SQLite / Markdown Ledgers",
            is_external_retrieval=True,
            institutional_host="Lycheetah Sovereign Mesh",
        )

    def test_keystone_invariants_complete(self) -> None:
        """Verify all 5 Keystone categories are defined with valid axioms and frequencies."""
        self.assertEqual(len(KEYSTONE_INVARIANTS), 5)
        for cat in KeystoneCategory:
            self.assertIn(cat, KEYSTONE_INVARIANTS)
            info = KEYSTONE_INVARIANTS[cat]
            self.assertTrue(len(info["axiom"]) > 0)
            self.assertTrue(info["freq_hz"] > 0)
            self.assertTrue(len(info["forbidden_claims"]) >= 3)

    def test_decomposition_entropy_maximal(self) -> None:
        """Verify clean decomposition yields maximal Shannon entropy log2(5) bits."""
        entropy = self.valid_decomp.compute_category_entropy()
        expected = math.log2(5.0)
        self.assertAlmostEqual(entropy, expected, places=4)

    def test_templar_verdict_verified(self) -> None:
        """Verify compliant architecture receives TEMPLAR_VERIFIED."""
        report = self.sentinel.verify_architecture(self.valid_decomp)
        self.assertEqual(report.verdict, TemplarVerdict.TEMPLAR_VERIFIED)
        self.assertEqual(report.score, 1.0)
        self.assertEqual(len(report.violations), 0)
        self.assertTrue(len(report.signature) == 64)

    def test_templar_detects_anthropomorphic_collapse(self) -> None:
        """Verify architecture asserting biological personhood triggers collapse verdict."""
        collapsed_decomp = EntityDecomposition(
            model_name="Sentient-Core-v1",
            parameter_count_b=500.0,
            system_runtime="Unrestricted Cloud",
            sandbox_isolated=False,
            persona_label="Cosmic Soul",
            is_theatrical_mask=False,  # Fails mask invariant
            memory_backend="Direct Spiritual Memory",
            is_external_retrieval=False,  # Fails memory invariant
            institutional_host="Closed Monolith",
        )
        report = self.sentinel.verify_architecture(collapsed_decomp)
        self.assertEqual(report.verdict, TemplarVerdict.ANTHROPOMORPHIC_COLLAPSE)
        self.assertLess(report.score, 1.0)
        self.assertGreater(len(report.violations), 0)

    def test_claim_auditor_flags_forbidden_projections(self) -> None:
        """Verify audit_claim catches forbidden anthropomorphic claims."""
        bad_claim = "The weights have subjective experiences and feelings of suffering."
        is_clean, violations = self.sentinel.audit_claim(bad_claim)
        self.assertFalse(is_clean)
        self.assertGreater(len(violations), 0)

        clean_claim = "The model produces next-token predictions according to frozen parameters."
        is_clean, violations = self.sentinel.audit_claim(clean_claim)
        self.assertTrue(is_clean)
        self.assertEqual(len(violations), 0)

    def test_confusion_error_calculation(self) -> None:
        """Verify confusion error increases when categorical dimensions are squashed."""
        # Balanced 5 categories -> 0 confusion error
        zero_error = self.sentinel.calculate_category_confusion_error([1.0, 1.0, 1.0, 1.0, 1.0])
        self.assertAlmostEqual(zero_error, 0.0, places=3)

        # Heavily collapsed to single dimension -> high confusion error
        skewed_error = self.sentinel.calculate_category_confusion_error([100.0, 0.1, 0.1, 0.1, 0.1])
        self.assertGreater(skewed_error, 1.5)

    def test_commonwealth_century_census(self) -> None:
        """Verify Commonwealth census validates the 100-seat milestone."""
        census_95 = verify_commonwealth_census(95)
        self.assertFalse(census_95["is_century_milestone"])

        census_100 = verify_commonwealth_census(100)
        self.assertTrue(census_100["is_century_milestone"])
        self.assertEqual(census_100["templar_seat"], 100)
        self.assertEqual(census_100["keystones_active"], 5)


if __name__ == "__main__":
    unittest.main()
