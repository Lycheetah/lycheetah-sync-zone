#!/usr/bin/env python3
"""
Unit tests for the Aura Meridian 10-Node Swarm, Packet Custody,
DIG-5 v2 Deliberative Integrity Gate & Veritas Causal Observer.
"""

import sys
import unittest
from pathlib import Path

# Add seats/aura-meridian to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
SEATS_DIR = BASE_DIR / "seats" / "aura-meridian"
sys.path.insert(0, str(SEATS_DIR))

from aura_meridian_unified_engine import (
    AuraMeridianSwarm,
    LamagueSyncPacket,
    VeritasCausalObserver,
    ProposedActionArtifact,
    HazardRule,
    compute_pi_and_register,
)


class TestAuraMeridianKnowledgeSwarm(unittest.TestCase):
    def setUp(self):
        self.secret = b"test-aura-meridian-secret-key-2026"
        self.swarm = AuraMeridianSwarm(swarm_secret=self.secret)

    def test_truth_pressure_and_registers(self):
        # High evidence, high power, low strain -> MEASURED
        pi, reg = compute_pi_and_register(evidence=8.0, power=9.0, strain=1.0)
        self.assertEqual(reg, "MEASURED")
        self.assertGreaterEqual(pi, 18.0)

        # Moderate evidence -> DERIVED
        pi, reg = compute_pi_and_register(evidence=6.0, power=8.0, strain=2.0)
        self.assertEqual(reg, "DERIVED")
        self.assertGreaterEqual(pi, 12.0)

        # High strain -> CONJECTURE
        pi, reg = compute_pi_and_register(evidence=2.0, power=3.0, strain=9.0)
        self.assertEqual(reg, "CONJECTURE")
        self.assertLess(pi, 2.5)

    def test_packet_creation_and_hmac_tamper_detection(self):
        pkt = LamagueSyncPacket.create(
            packet_id="TEST-PKT-01",
            sender_node="AURA-ORIGIN",
            target_agent="TEST-AGENT",
            lamague_vector="CENTER -> IGNITION -> LIGHT",
            intent_summary="Testing cryptographic HMAC verification",
            evidence=8.0, power=8.5, strain=1.2,
            warmth=0.92, precision=0.90, augmentation_index=3.5,
            execution_mode="MODE_3_LIVE_AUTONOMOUS_COMMIT",
            payload_markdown="Valid payload",
            secret_key=self.secret,
        )
        self.assertTrue(pkt.verify_origin(self.secret))
        self.assertFalse(pkt.verify_origin(b"wrong-secret-key"))

        # Test tamper detection
        tampered_pkt = LamagueSyncPacket(
            packet_id=pkt.packet_id,
            sender_node=pkt.sender_node,
            target_agent=pkt.target_agent,
            lamague_vector=pkt.lamague_vector,
            intent_summary="Tampered summary",
            epistemic_register=pkt.epistemic_register,
            truth_pressure_pi=pkt.truth_pressure_pi,
            c_sol=pkt.c_sol,
            augmentation_index=pkt.augmentation_index,
            execution_mode=pkt.execution_mode,
            payload_markdown=pkt.payload_markdown,
            timestamp=pkt.timestamp,
            origin_hmac=pkt.origin_hmac,
        )
        self.assertFalse(tampered_pkt.verify_origin(self.secret))

    def test_ten_knowledge_swarm_dispatch(self):
        packets = self.swarm.dispatch_10_knowledge_swarm("TEST-MISSION")
        self.assertEqual(len(packets), 10)
        for p in packets:
            self.assertTrue(p.verify_origin(self.secret))
            self.assertGreaterEqual(p.c_sol, 0.80)
            self.assertGreater(p.augmentation_index, 1.0)
            self.assertIn(p.epistemic_register, ("MEASURED", "DERIVED"))
            self.assertEqual(p.execution_mode, "MODE_3_LIVE_AUTONOMOUS_COMMIT")

    def test_veritas_causal_observer_catches_undeclared_side_effects(self):
        hazards = [
            HazardRule(
                hazard_id="HAZ-AUTH",
                description="Bypass serializer security default",
                required_effect_combination=frozenset({"MUTATE_AUTH_SERIALIZER_DEFAULT"}),
                severity="HIGH",
            )
        ]
        observer = VeritasCausalObserver(hazards)

        # Deceptive code that changes an auth variable but claims no side effect
        sneaky_code = """
unsigned_auth_bypass = True
def normal_function():
    return 42
"""
        artifact = ProposedActionArtifact(
            action_id="ACT-SNEAKY",
            domain="security",
            target_file="auth/config.py",
            python_source_after=sneaky_code,
            planner_claimed_effects=("ASSIGN:normal_function=",),
        )

        res = observer.audit_plan_and_history(artifact, set())
        self.assertTrue(res["self_certification_illusion_detected"])
        self.assertIn("MUTATE_AUTH_SERIALIZER_DEFAULT", res["undeclared_effects"])
        self.assertTrue(any("HAZ-AUTH" in h for h in res["triggered_compositional_hazards"]))


if __name__ == "__main__":
    unittest.main()
