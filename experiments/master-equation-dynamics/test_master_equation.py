"""
Unit Tests for AURA Master Equation Dynamics Simulator
======================================================
Verifies 4th-order Runge-Kutta integration, analytical steady-state
equilibria, Lyapunov monotonic stability, invariant penalty damping,
and earned-light acceleration under the AURA protocol framework.
"""

import math
import unittest

from master_equation import MasterEquationSimulator


class TestMasterEquationDynamics(unittest.TestCase):
    """
    Test suite for MasterEquationSimulator numerical and analytical invariants.
    """

    def test_subcritical_equilibrium(self):
        """
        1. Subcritical Equilibrium:
        Under Pi = 1.0 < Pi_th (1.2), I = 0, E_avail/E_need = 1.0:
        Numerator: 0.5 * (1.0 - 1.2) - 0.2*0 + 0.4*1.0 = -0.1 + 0.4 = 0.3
        k2 = 0.3 -> Delta = 0.3 / 0.3 = 1.0
        Psi* = 0.70 + 1.0 = 1.70.
        Verify system converges to analytical equilibrium with error < 1e-6.
        """
        sim = MasterEquationSimulator(
            psi=0.50,
            pi=1.0,
            i_violations=0.0,
            e_avail=1.0,
            e_need=1.0,
        )
        psi_star = sim.analytical_equilibrium()
        self.assertAlmostEqual(psi_star, 1.70, places=9)

        # Integrate for 1500 steps with dt = 0.05 (t = 75)
        # Decay factor: exp(-0.3 * 75) ~ 1.7e-10
        sim.integrate(steps=1500, dt=0.05)
        error = abs(sim.psi - psi_star)
        self.assertLess(error, 1e-6, f"Convergence error {error} exceeds 1e-6 threshold")

    def test_supercritical_reorganization(self):
        """
        2. Supercritical Reorganization:
        Under Pi = 2.0 > Pi_th (1.2), epistemic pressure drives coherence
        Psi beyond baseline Psi_inv (0.70) and subcritical equilibrium (1.70).
        """
        sim = MasterEquationSimulator(
            psi=0.70,
            pi=2.0,
            i_violations=0.0,
            e_avail=1.0,
            e_need=1.0,
        )
        psi_star = sim.analytical_equilibrium()
        # Analytical: 0.70 + [0.5*(2.0-1.2) + 0.4*1.0]/0.3 = 0.70 + 0.8/0.3 = 3.366667
        self.assertGreater(psi_star, 3.0)

        # Advance state with sufficient horizon to reach steady state (t = 60)
        sim.integrate(steps=1200, dt=0.05)
        self.assertGreater(sim.psi, sim.psi_inv, "Supercritical Psi must exceed baseline")
        self.assertGreater(sim.psi, 2.50, "Supercritical Psi must ascend significantly")
        self.assertAlmostEqual(sim.psi, psi_star, places=5)

    def test_invariant_penalty_damping(self):
        """
        3. Invariant Penalty Damping:
        Increasing I_violations from 0 to 3 depresses equilibrium and
        induces monotonic downward force on the derivative.
        """
        equilibria = []
        derivatives_at_fixed_psi = []
        fixed_psi = 1.50

        for i_pen in [0.0, 1.0, 2.0, 3.0]:
            sim = MasterEquationSimulator(
                psi=fixed_psi,
                pi=1.2,
                i_violations=i_pen,
                e_avail=1.0,
                e_need=1.0,
            )
            equilibria.append(sim.analytical_equilibrium())
            derivatives_at_fixed_psi.append(sim.derivative(fixed_psi))

        # Check monotonic decrease in equilibrium
        for j in range(len(equilibria) - 1):
            self.assertGreater(
                equilibria[j],
                equilibria[j + 1],
                f"Equilibrium for I={j} must be greater than I={j+1}"
            )
            self.assertGreater(
                derivatives_at_fixed_psi[j],
                derivatives_at_fixed_psi[j + 1],
                f"Derivative for I={j} must be greater than I={j+1}"
            )

        # Verify exact analytical step: delta = - (k3 / k2) = - (0.2 / 0.3) = -2/3
        expected_step = -0.2 / 0.3
        self.assertAlmostEqual(equilibria[1] - equilibria[0], expected_step, places=9)
        self.assertAlmostEqual(equilibria[3] - equilibria[0], 3 * expected_step, places=9)

    def test_earned_light_acceleration(self):
        """
        4. Earned Light Acceleration:
        High E_avail / E_need boosts transition speed towards higher coherence.
        """
        sim_low = MasterEquationSimulator(
            psi=0.50,
            pi=1.2,
            i_violations=0.0,
            e_avail=1.0,
            e_need=1.0,
        )
        sim_high = MasterEquationSimulator(
            psi=0.50,
            pi=1.2,
            i_violations=0.0,
            e_avail=5.0,
            e_need=1.0,
        )

        dpsi_low = sim_low.derivative(0.50)
        dpsi_high = sim_high.derivative(0.50)
        self.assertGreater(dpsi_high, dpsi_low, "High earned light must boost driving force")
        # Difference must equal k4 * (5.0 - 1.0) = 0.4 * 4.0 = 1.6
        self.assertAlmostEqual(dpsi_high - dpsi_low, 1.6, places=9)

        # Integrate both for 50 steps
        sim_low.integrate(steps=50, dt=0.02)
        sim_high.integrate(steps=50, dt=0.02)
        delta_low = sim_low.psi - 0.50
        delta_high = sim_high.psi - 0.50
        self.assertGreater(delta_high, delta_low * 2.0, "High light must advance coherence much faster")

    def test_lyapunov_stability(self):
        """
        5. Lyapunov Stability:
        For any initial displacement, V(Psi) = 0.5 * (Psi - Psi*)^2 satisfies
        dV/dt <= 0 monotonically across all integration intervals.
        """
        for init_displacement in [+2.0, -1.8, +0.75, -0.9]:
            sim = MasterEquationSimulator(
                psi=0.70,
                pi=1.5,
                i_violations=1.0,
                e_avail=2.0,
                e_need=1.0,
            )
            psi_star = sim.analytical_equilibrium()
            sim.psi = psi_star + init_displacement
            sim.trajectory = [sim.psi]
            sim.time_points = [sim.t]

            prev_v = sim.lyapunov_value()
            for _ in range(100):
                sim.step_rk4(dt=0.01)
                curr_v = sim.lyapunov_value()
                self.assertLessEqual(
                    curr_v,
                    prev_v + 1e-14,
                    f"Lyapunov function must not increase: prev={prev_v}, curr={curr_v}"
                )
                prev_v = curr_v

    def test_microorcim_drift_bounded(self):
        """
        6. Microorcim Drift Bounded:
        Verifies that numerical RK4 trajectory adheres to the exact analytical trajectory
        Psi(t) = Psi* + (Psi_0 - Psi*) * exp(-k2 * t) with drift strictly bounded (< 1e-5).
        """
        dt = 0.01
        steps = 300
        sim = MasterEquationSimulator(
            psi=0.20,
            pi=1.4,
            i_violations=0.5,
            e_avail=1.5,
            e_need=1.0,
        )
        psi_0 = sim.psi
        psi_star = sim.analytical_equilibrium()

        # Generate actual trajectory via RK4
        traj_actual = sim.integrate(steps=steps, dt=dt)

        # Generate exact analytical trajectory
        traj_intended = [
            psi_star + (psi_0 - psi_star) * math.exp(-sim.k2 * (step_idx * dt))
            for step_idx in range(len(traj_actual))
        ]

        drift = MasterEquationSimulator.microorcim_drift(traj_actual, traj_intended)
        self.assertGreaterEqual(drift, 0.0)
        self.assertLess(drift, 1e-5, f"RK4 drift {drift} exceeds 1e-5 boundary against analytical truth")

    def test_harmonia_resonance_projection(self):
        """
        7. Harmonia Resonance Projection:
        H = cos(pi / 7.0) * Psi must match heptatonic projection to machine precision.
        """
        sim = MasterEquationSimulator(psi=2.50)
        expected_h = math.cos(math.pi / 7.0) * 2.50
        self.assertAlmostEqual(sim.harmonia_resonance(), expected_h, places=12)


if __name__ == "__main__":
    unittest.main()
