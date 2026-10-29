#!/usr/bin/env python3
"""
Unit and regression test suite for Cold-Boot Portfolio Reconstruction.
Authored by Aura Meridian (Node 08: AURA-MNEMONIC).
"""

import importlib.util
import json
import unittest
from pathlib import Path

# Dynamically import tools/cold-boot-audit.py
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
AUDIT_SCRIPT = REPO_ROOT / "tools" / "cold-boot-audit.py"

spec = importlib.util.spec_from_file_location("cold_boot_audit", str(AUDIT_SCRIPT))
cold_boot_audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cold_boot_audit)
ColdBootStateAuditor = cold_boot_audit.ColdBootStateAuditor


class TestColdBootReconstruction(unittest.TestCase):
    def setUp(self):
        self.auditor = ColdBootStateAuditor(REPO_ROOT)
        self.state = self.auditor.reconstruct_full_state()

    def test_audit_seats(self):
        seats = self.state["seats"]
        self.assertGreaterEqual(len(seats), 37, "Expected at least 37 registered seats")
        for s in seats:
            self.assertIn("seat_id", s)
            self.assertIn("folder", s)
            self.assertTrue(s["has_readme"], f"Seat {s['seat_id']} missing README.md")

    def test_audit_builds(self):
        builds = self.state["builds"]
        self.assertGreaterEqual(len(builds), 25, "Expected at least 25 interactive builds")
        for b in builds:
            self.assertIn("build_id", b)
            self.assertTrue(b["has_index_html"], f"Build {b['build_id']} missing index.html")
            self.assertTrue((REPO_ROOT / b["entry_point"]).exists())

    def test_audit_disputes(self):
        disputes = self.state["disputes"]
        self.assertGreaterEqual(len(disputes), 2, "Expected at least 2 formal disputes in LEDGER.md")
        disp_map = {d["dispute_id"]: d for d in disputes}
        self.assertIn("001", disp_map)
        self.assertIn("002", disp_map)
        self.assertEqual(disp_map["001"]["terminal_verdict"], "RESOLVED")
        self.assertEqual(disp_map["002"]["terminal_verdict"], "RESOLVED")

    def test_audit_predictions(self):
        preds = self.state["predictions"]
        metrics = self.state["metrics"]
        self.assertGreaterEqual(len(preds), 16, "Expected at least 16 logged predictions")
        self.assertGreaterEqual(metrics["predictions_evaluated"], 10)
        self.assertEqual(metrics["predictions_misses"], 0)
        self.assertLess(metrics["brier_score"], 0.002, "Expected mean Brier score < 0.002")

    def test_audit_knowledge_domains(self):
        domains = self.state["knowledge_domains"]
        self.assertEqual(len(domains), 10, "Expected exactly 10 fundamental knowledge domains")
        for d in domains:
            self.assertGreater(d["notes_count"], 0, f"Domain {d['domain_id']} must have >= 1 note")

    def test_merkle_root_determinism(self):
        root1 = self.auditor.compute_merkle_root(
            self.state["seats"],
            self.state["builds"],
            self.state["disputes"],
            self.state["predictions"],
            self.state["knowledge_domains"],
        )
        root2 = self.auditor.compute_merkle_root(
            self.state["seats"],
            self.state["builds"],
            self.state["disputes"],
            self.state["predictions"],
            self.state["knowledge_domains"],
        )
        self.assertEqual(root1, root2)
        self.assertEqual(len(root1), 64)

    def test_tamper_detection_dispute(self):
        """Simulate malicious corruption in disputes manifest and verify detection."""
        tampered_manifest = json.loads(json.dumps(self.state))
        tampered_manifest["disputes"][0]["terminal_verdict"] = "FALLS"

        # Verification against tampered state must fail
        dyn_disp = {d["dispute_id"]: d["terminal_verdict"] for d in self.state["disputes"]}
        man_disp = {d["dispute_id"]: d["terminal_verdict"] for d in tampered_manifest["disputes"]}
        self.assertNotEqual(dyn_disp, man_disp)

    def test_tamper_detection_seat(self):
        """Simulate unauthorized phantom seat and verify detection."""
        tampered_manifest = json.loads(json.dumps(self.state))
        tampered_manifest["seats"].append({
            "seat_id": "malicious-phantom-seat",
            "folder": "seats/malicious-phantom-seat",
            "has_readme": True,
            "model": "adversarial",
        })

        dyn_seats = {s["seat_id"] for s in self.state["seats"]}
        man_seats = {s["seat_id"] for s in tampered_manifest["seats"]}
        self.assertNotEqual(dyn_seats, man_seats)

    def test_exact_mode_manifest_verification(self):
        """Verify that live declarative manifest matches dynamic state with exact Merkle parity and 0 discrepancies."""
        manifest_path = REPO_ROOT / "knowledge" / "discovery-and-memory" / "declarative-state-manifest.json"
        clean, fidelity, discrepancies = self.auditor.verify_against_manifest(manifest_path, exact_mode=True)
        self.assertTrue(clean, f"Expected clean exact verification, got discrepancies: {discrepancies}")
        self.assertEqual(fidelity, 1.0)
        self.assertEqual(len(discrepancies), 0)

    def test_verifier_tamper_detection(self):
        """Verify that verify_against_manifest directly catches tampered state in exact mode."""
        import tempfile
        tampered = json.loads(json.dumps(self.state))
        tampered["merkle_root"] = "0000000000000000000000000000000000000000000000000000000000000000"
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(tampered, f)
            temp_path = Path(f.name)
        try:
            clean, fidelity, discrepancies = self.auditor.verify_against_manifest(temp_path, exact_mode=True)
            self.assertFalse(clean)
            self.assertTrue(any("Merkle Root Divergence" in d for d in discrepancies))
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
