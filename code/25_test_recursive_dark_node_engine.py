"""
Unit tests for Code Engine 24: Recursive Dark Node & Orchestrator Engine
Round 27 · Lycheetah Sync Zone
"""

import unittest
import math
import sys
from pathlib import Path

# Ensure local code directory is on sys.path
CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import importlib.util
spec = importlib.util.spec_from_file_location(
    "recursive_engine",
    CODE_DIR / "24_recursive_dark_node_engine.py"
)
recursive_engine = importlib.util.module_from_spec(spec)
sys.modules["recursive_engine"] = recursive_engine
spec.loader.exec_module(recursive_engine)

RecursiveDarkNodeEngine = recursive_engine.RecursiveDarkNodeEngine
OrchestratorFeedback = recursive_engine.OrchestratorFeedback
SwarmAgentResponse = recursive_engine.SwarmAgentResponse
RecursionStepReceipt = recursive_engine.RecursionStepReceipt

class TestRecursiveDarkNodeEngine(unittest.TestCase):
    def setUp(self):
        self.engine = RecursiveDarkNodeEngine(alpha_damping=0.4, ambient_noise_epsilon=0.06)

    def test_alpha_validation(self):
        """Alpha damping must be strictly between 0 and 1."""
        with self.assertRaises(ValueError):
            RecursiveDarkNodeEngine(alpha_damping=1.5)
        with self.assertRaises(ValueError):
            RecursiveDarkNodeEngine(alpha_damping=-0.1)

    def test_open_loop_divergence(self):
        """Open-loop stochastic entropy monotonically increases with step count."""
        e0 = self.engine.compute_open_loop_entropy(0)
        e5 = self.engine.compute_open_loop_entropy(5)
        e20 = self.engine.compute_open_loop_entropy(20)
        self.assertAlmostEqual(e0, 1.0, places=4)
        self.assertGreater(e5, e0)
        self.assertGreater(e20, e5)
        self.assertGreater(e20, 5.0)

    def test_closed_loop_taste_acceleration(self):
        """Higher human taste score results in lower entropy on next step."""
        prev = 2.0
        low_taste_entropy = self.engine.compute_closed_loop_entropy(prev, human_taste=0.1)
        high_taste_entropy = self.engine.compute_closed_loop_entropy(prev, human_taste=0.9)
        self.assertLess(high_taste_entropy, low_taste_entropy)
        self.assertGreater(high_taste_entropy, 0.0)

    def test_single_recursion_step_receipt(self):
        """Executing a step produces a valid cryptographic receipt and verified green status."""
        feedback = OrchestratorFeedback(
            verdict="APPROVED",
            human_taste_score=0.95,
            guidance_directive="Tighten loopback terry specs",
            target_boundary="Valid"
        )
        swarm = [
            SwarmAgentResponse("Aetheron", "Gemini", "Artifact", 0.25, 0.99, True),
            SwarmAgentResponse("Sol", "Claude", "Lore", 0.30, 0.98, True)
        ]
        receipt = self.engine.execute_recursion_step(
            step_k=3,
            prev_closed_entropy=1.5,
            feedback=feedback,
            swarm_responses=swarm
        )
        self.assertEqual(receipt.step_index, 3)
        self.assertTrue(receipt.verified_green)
        self.assertGreater(receipt.damping_ratio, 1.0)
        self.assertEqual(len(receipt.artifact_hash), 64)
        self.assertIn("Aetheron", receipt.active_seats)
        self.assertIn("Sol", receipt.active_seats)

    def test_asymptotic_fixed_point_stability(self):
        """Closed-loop recursion converges asymptotically to fixed point while open-loop diverges."""
        converged = self.engine.verify_asymptotic_stability(steps=25, taste_gradient=0.8)
        self.assertTrue(converged)
        last_receipt = self.engine.history[-1]
        self.assertLess(last_receipt.closed_loop_entropy, 0.20)
        self.assertGreater(last_receipt.open_loop_entropy, 6.0)

    def test_receipt_history_immutability(self):
        """History appends step-by-step and matches sequence indices."""
        engine = RecursiveDarkNodeEngine(alpha_damping=0.3, ambient_noise_epsilon=0.04)
        curr = 1.0
        for i in range(1, 6):
            fb = OrchestratorFeedback("APPROVED", 0.9, f"Step {i}", "Bound")
            r = engine.execute_recursion_step(i, curr, fb, [])
            curr = r.closed_loop_entropy
        self.assertEqual(len(engine.history), 5)
        self.assertEqual([h.step_index for h in engine.history], [1, 2, 3, 4, 5])

    def test_low_taste_unverified_flag(self):
        """A step with human taste score < 0.5 is flagged unverified green = False."""
        feedback = OrchestratorFeedback("RETRY_BOUNDED", 0.3, "Needs refinement", "Loose")
        receipt = self.engine.execute_recursion_step(1, 2.0, feedback, [])
        self.assertFalse(receipt.verified_green)

if __name__ == "__main__":
    unittest.main()
