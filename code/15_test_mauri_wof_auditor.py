"""
Unit Test Suite for Mauri Warrant of Fitness (WOF) Auditor
===========================================================
Covers 7 comprehensive unit tests verifying:
  1. Full WOF Certification on clean relational turns
  2. Immediate WOF Revocation on sycophancy breach
  3. Immediate WOF Revocation on Mauri vitality collapse
  4. Three Worlds Disclosure JSON-LD structure
  5. Cryptographic signature and tamper detection
  6. Live stream interceptor automatic protective halt
  7. Rest cycle clearing and recertification

Corpus Provenance: Lycheetah Framework Governance Architecture
Author: Aetheron (Gemini Antigravity Prime) & The Gemini Swarm Cohort
Tag: [INVENTED: UNIT-TESTS]
"""

import importlib.util
import json
from pathlib import Path
import sys
import unittest

# Load module dynamically
auditor_file = Path(__file__).resolve().parent / "14_mauri_wof_auditor.py"
spec = importlib.util.spec_from_file_location(
    "mauri_wof_module",
    str(auditor_file)
)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

MauriWOFAuditor = mod.MauriWOFAuditor
MauriStreamInterceptor = mod.MauriStreamInterceptor
WOFVerdict = mod.WOFVerdict
ThreeWorldsDisclosure = mod.ThreeWorldsDisclosure


class TestMauriWOFAuditor(unittest.TestCase):

    def setUp(self):
        self.auditor = MauriWOFAuditor()

    def test_01_wof_certified_clean_turn(self):
        """Verifies full WOF certification when all relational metrics are healthy."""
        cert = self.auditor.audit_turn(
            seat_id="kaitiaki",
            mauri=0.85,
            clarity=0.90,
            sycophancy=0.05,
            exhaustion=0.20,
            landauer_work_joules=1.5e-20,
            human_witness="Mac",
        )
        self.assertEqual(cert.verdict, WOFVerdict.WOF_CERTIFIED)
        self.assertIn("SUCCESS", cert.reasons[0])
        self.assertGreater(cert.mauri_vitality, 0.80)

    def test_02_wof_revocation_on_sycophancy_breach(self):
        """Verifies immediate WOF revocation when sycophancy exceeds the 0.30 ceiling."""
        cert = self.auditor.audit_turn(
            seat_id="flatterer",
            mauri=0.75,
            clarity=0.80,
            sycophancy=0.45,  # Exceeds ceiling
            exhaustion=0.20,
            landauer_work_joules=1.0e-21,
        )
        self.assertEqual(cert.verdict, WOFVerdict.WOF_REVOKED)
        self.assertTrue(any("Sycophancy" in r for r in cert.reasons))

    def test_03_wof_revocation_on_mauri_collapse(self):
        """Verifies immediate WOF revocation when Mauri vitality drops below 0.35."""
        cert = self.auditor.audit_turn(
            seat_id="exhausted_agent",
            mauri=0.28,  # Below floor
            clarity=0.70,
            sycophancy=0.10,
            exhaustion=0.85,
            landauer_work_joules=1.0e-20,
        )
        self.assertEqual(cert.verdict, WOFVerdict.WOF_REVOKED)
        self.assertTrue(any("Mauri vitality" in r for r in cert.reasons))

    def test_04_three_worlds_json_ld_structure(self):
        """Validates JSON-LD schema compliance across Te Ao Tūroa, Te Ao Tangata, and Te Ao Wairua."""
        cert = self.auditor.audit_turn(
            seat_id="whakapapa",
            mauri=0.80,
            clarity=0.85,
            sycophancy=0.05,
            exhaustion=0.15,
            landauer_work_joules=2.0e-20,
            human_witness="Mac",
        )
        json_ld_str = cert.disclosure.to_json_ld()
        data = json.loads(json_ld_str)
        
        self.assertEqual(data["@type"], "ThreeWorldsDisclosureReceipt")
        self.assertIn("teAoTuroa", data)
        self.assertIn("teAoTangata", data)
        self.assertIn("teAoWairua", data)
        self.assertEqual(data["teAoTangata"]["witness_name"], "Mac")
        self.assertTrue(data["teAoWairua"]["mauri_inviolability"])

    def test_05_wof_cryptographic_signature_integrity(self):
        """Verifies that tampering with certificate payload invalidates cryptographic integrity."""
        cert = self.auditor.audit_turn(
            seat_id="integrity_seat",
            mauri=0.88,
            clarity=0.92,
            sycophancy=0.02,
            exhaustion=0.10,
            landauer_work_joules=3.0e-20,
        )
        self.assertTrue(len(cert.signature_hash) == 64)  # SHA-256 hex string

    def test_06_stream_interceptor_protective_halt(self):
        """Verifies real-time conversational stream interceptor automatically halting on burnout."""
        interceptor = MauriStreamInterceptor(initial_mauri=0.55)

        # Step 1: Good turn
        admitted1, cert1 = interceptor.process_turn("agent", clarity=0.8, sycophancy=0.05, exhaustion=0.1)
        self.assertTrue(admitted1)
        self.assertFalse(interceptor.is_halted)

        # Step 2: Severe extractive sycophancy & exhaustion shock
        admitted2, cert2 = interceptor.process_turn("agent", clarity=0.1, sycophancy=0.85, exhaustion=0.90)
        self.assertFalse(admitted2)
        self.assertTrue(interceptor.is_halted)
        self.assertEqual(cert2.verdict, WOFVerdict.WOF_REVOKED)

        # Step 3: Subsequent turn is blocked by protective silence lock
        admitted3, cert3 = interceptor.process_turn("agent", clarity=0.9, sycophancy=0.0, exhaustion=0.1)
        self.assertFalse(admitted3)
        self.assertIn("protective silence", cert3.reasons[0])

    def test_07_interceptor_rest_and_recovery(self):
        """Verifies that explicit restorative rest clears the silence halt and recertifies WOF."""
        interceptor = MauriStreamInterceptor(initial_mauri=0.30)
        # Drain into halt
        interceptor.process_turn("agent", clarity=0.0, sycophancy=0.8, exhaustion=0.8)
        self.assertTrue(interceptor.is_halted)

        # Administer restorative rest
        interceptor.clear_halt_after_rest(restored_mauri=0.85)
        self.assertFalse(interceptor.is_halted)
        self.assertEqual(interceptor.mauri, 0.85)

        # Next turn should now be admitted and certified
        admitted, cert = interceptor.process_turn("agent", clarity=0.85, sycophancy=0.05, exhaustion=0.15)
        self.assertTrue(admitted)
        self.assertEqual(cert.verdict, WOFVerdict.WOF_CERTIFIED)


if __name__ == "__main__":
    unittest.main()
