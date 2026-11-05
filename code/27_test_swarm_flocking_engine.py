"""
Unit tests for Code Engine 26: Sovereign Swarm Flocking & Phase-Transition Engine
Round 28 · Lycheetah Sync Zone
"""

import unittest
import math
import sys
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

import importlib.util
spec = importlib.util.spec_from_file_location(
    "flocking_engine",
    CODE_DIR / "26_swarm_flocking_engine.py"
)
flocking_engine = importlib.util.module_from_spec(spec)
sys.modules["flocking_engine"] = flocking_engine
spec.loader.exec_module(flocking_engine)

SwarmFlockingEngine = flocking_engine.SwarmFlockingEngine
SwarmBoid = flocking_engine.SwarmBoid
SwarmStateSnapshot = flocking_engine.SwarmStateSnapshot

class TestSwarmFlockingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SwarmFlockingEngine(num_boids=60, arena_size=500.0, seed=123)

    def test_boid_initialization(self):
        """Engine initializes exactly N boids distributed among triad seats."""
        self.assertEqual(len(self.engine.boids), 60)
        sol_count = sum(1 for b in self.engine.boids if b.triad_seat == "SOL")
        cael_count = sum(1 for b in self.engine.boids if b.triad_seat == "CAEL")
        aeth_count = sum(1 for b in self.engine.boids if b.triad_seat == "AETHERON")
        self.assertEqual(sol_count, 20)
        self.assertEqual(cael_count, 20)
        self.assertEqual(aeth_count, 20)

    def test_order_parameter_bounds(self):
        """Order parameter Phi must strictly lie in [0.0, 1.0]."""
        snap = self.engine.step()
        self.assertGreaterEqual(snap.order_parameter_phi, 0.0)
        self.assertLessEqual(snap.order_parameter_phi, 1.0)

    def test_open_loop_disorder(self):
        """Under autonomous thermal noise without human steering, order parameter remains low (disordered)."""
        engine = SwarmFlockingEngine(num_boids=80, noise_eta=1.5, seed=99)
        phis = []
        for _ in range(30):
            snap = engine.step(human_attractor=None)
            phis.append(snap.order_parameter_phi)
        avg_phi = sum(phis[-10:]) / 10.0
        # Disordered regime should stay well below 0.60
        self.assertLess(avg_phi, 0.60)

    def test_human_torque_phase_transition(self):
        """Human attractor injection triggers discontinuous phase transition to hyper-ordered alignment."""
        engine = SwarmFlockingEngine(num_boids=60, noise_eta=0.5, seed=77)
        # 15 steps without human
        for _ in range(15):
            engine.step(human_attractor=None)
        
        # Inject human attractor with directive heading
        for _ in range(25):
            snap = engine.step(human_attractor=(250.0, 250.0), human_heading=0.785, human_torque=0.85)
            
        # Terminal state should be highly ordered
        self.assertGreater(snap.order_parameter_phi, 0.85)
        self.assertTrue(snap.human_attractor_active)

    def test_hash_integrity(self):
        """Snapshot hash is a valid SHA-256 hex digest."""
        snap = self.engine.step()
        self.assertEqual(len(snap.state_hash), 64)
        int(snap.state_hash, 16)  # Must parse as hex

    def test_regime_comparison(self):
        """Regime comparison proves closed-loop order dominates open-loop disorder."""
        engine = SwarmFlockingEngine(num_boids=50, noise_eta=0.8, seed=42)
        open_phis, closed_phis = engine.run_regime_comparison(steps=40, human_trigger_step=20)
        self.assertEqual(len(open_phis), 40)
        self.assertEqual(len(closed_phis), 40)
        # Mean of final 10 steps of closed loop must exceed open loop
        final_open = sum(open_phis[-10:]) / 10.0
        final_closed = sum(closed_phis[-10:]) / 10.0
        self.assertGreater(final_closed, final_open)

if __name__ == "__main__":
    unittest.main()
