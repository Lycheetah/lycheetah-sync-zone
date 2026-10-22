"""
Executable Unittest Suite for Discrete Noether Invariants & Non-Equilibrium Thermodynamics.

Forged by Aura Meridian (Node 09: AURA-ALCHEMIST) for the Lycheetah Sync Zone.
Human Architect: Mackenzie Conor James Clark (Mac).
"""

import math
import random
import sys
import unittest
from pathlib import Path

# Enable direct import of siblings in hyphenated directory
_CURR_DIR = str(Path(__file__).resolve().parent)
if _CURR_DIR not in sys.path:
    sys.path.insert(0, _CURR_DIR)

from discrete_noether_engine import (
    CentralForce2DLagrangian,
    ContinuousMutationLattice,
    DiscreteVariationalIntegrator,
    SchnakenbergCycleEngine,
    TwoBodyTranslationLagrangian,
    runge_kutta_4_step,
)


class TestDiscreteNoetherInvariants(unittest.TestCase):
    def setUp(self):
        random.seed(42)

    def test_discrete_noether_angular_momentum_conservation(self):
        """
        Discrete Noether's Theorem: Under SO(2) rotational symmetry of a central force field,
        the discrete angular momentum map J(q_k, p_k) = q_k x p_k is conserved
        across 10,000 continuous DEL iterations with machine precision drift (< 1e-12).
        """
        lagrangian = CentralForce2DLagrangian(mass=1.0, k=1.0, power=2.0)
        h = 0.02
        q_prev = [1.0, 0.0]
        v0 = [0.0, 1.2]
        f0 = lagrangian.force(q_prev)
        q_curr = [q_prev[i] + h * v0[i] + 0.5 * (h ** 2) * f0[i] for i in range(2)]

        # Initial angular momentum
        p_init = [lagrangian.mass * v0[0], lagrangian.mass * v0[1]]
        j_initial = lagrangian.angular_momentum(q_prev, p_init)

        max_deviation = 0.0
        for _ in range(10000):
            q_next, p_curr = DiscreteVariationalIntegrator.step_central_force(q_prev, q_curr, h, lagrangian)
            j_curr = lagrangian.angular_momentum(q_curr, p_curr)
            dev = abs(j_curr - j_initial)
            if dev > max_deviation:
                max_deviation = dev
            q_prev, q_curr = q_curr, q_next

        # Machine precision preservation guaranteed by Discrete Noether theorem
        self.assertLess(max_deviation, 1e-12, f"Discrete angular momentum drifted by {max_deviation}")

    def test_discrete_noether_vs_rk4_angular_momentum_drift(self):
        """
        Contrast test: Standard Runge-Kutta 4 (non-symplectic) exhibits measurable drift,
        whereas Discrete Noether maintains strict machine precision invariant conservation.
        """
        lagrangian = CentralForce2DLagrangian(mass=1.0, k=1.0, power=2.0)
        h = 0.02
        steps = 10000

        # RK4
        q_rk = [1.0, 0.0]
        v_rk = [0.0, 1.2]
        j_init_rk = lagrangian.angular_momentum(q_rk, [lagrangian.mass * v_rk[0], lagrangian.mass * v_rk[1]])
        for _ in range(steps):
            q_rk, v_rk = runge_kutta_4_step(q_rk, v_rk, h, lagrangian.force, mass=1.0)
        j_final_rk = lagrangian.angular_momentum(q_rk, [lagrangian.mass * v_rk[0], lagrangian.mass * v_rk[1]])
        rk_drift = abs(j_final_rk - j_init_rk)

        # DEL
        q_prev = [1.0, 0.0]
        v0 = [0.0, 1.2]
        f0 = lagrangian.force(q_prev)
        q_curr = [q_prev[i] + h * v0[i] + 0.5 * (h ** 2) * f0[i] for i in range(2)]
        q_next, p_curr = DiscreteVariationalIntegrator.step_central_force(q_prev, q_curr, h, lagrangian)
        j_init_del = lagrangian.angular_momentum(q_curr, p_curr)
        q_prev, q_curr = q_curr, q_next

        for _ in range(steps - 1):
            q_next, p_curr = DiscreteVariationalIntegrator.step_central_force(q_prev, q_curr, h, lagrangian)
            j_final_del = lagrangian.angular_momentum(q_curr, p_curr)
            q_prev, q_curr = q_curr, q_next
        del_drift = abs(j_final_del - j_init_del)

        # Discrete Noether drift is orders of magnitude smaller than RK4 drift
        self.assertLess(del_drift, 1e-12)
        self.assertGreater(rk_drift, del_drift * 1000)

    def test_discrete_noether_linear_momentum_conservation(self):
        """
        Under spatial translation symmetry, total discrete momentum P = p1 + p2 is conserved to < 1e-12.
        """
        lagrangian = TwoBodyTranslationLagrangian(m1=1.5, m2=2.5, k=3.0)
        h = 0.02
        q_prev = [-0.5, 0.2, 0.5, -0.2]
        v0 = [0.8, -0.4, -0.48, 0.24]
        p_init = (
            lagrangian.m1 * v0[0] + lagrangian.m2 * v0[2],
            lagrangian.m1 * v0[1] + lagrangian.m2 * v0[3],
        )

        f0 = lagrangian.forces(q_prev)
        a0 = [
            f0[0] / lagrangian.m1,
            f0[1] / lagrangian.m1,
            f0[2] / lagrangian.m2,
            f0[3] / lagrangian.m2,
        ]
        q_curr = [q_prev[i] + h * v0[i] + 0.5 * (h ** 2) * a0[i] for i in range(4)]

        max_dev = 0.0
        for _ in range(5000):
            q_next, p_curr = DiscreteVariationalIntegrator.step_two_body(q_prev, q_curr, h, lagrangian)
            px, py = lagrangian.total_momentum(p_curr)
            dev = math.sqrt((px - p_init[0]) ** 2 + (py - p_init[1]) ** 2)
            if dev > max_dev:
                max_dev = dev
            q_prev, q_curr = q_curr, q_next

        self.assertLess(max_dev, 1e-12)

    def test_shadow_hamiltonian_bounded_energy_oscillations(self):
        """
        Symplectic integrators bound energy fluctuations within a tight O(h^2) envelope
        without secular drift over thousands of steps.
        """
        lagrangian = CentralForce2DLagrangian(mass=1.0, k=1.0, power=2.0)
        h = 0.03
        q_prev = [1.0, 0.0]
        v0 = [0.0, 1.0]
        f0 = lagrangian.force(q_prev)
        q_curr = [q_prev[i] + h * v0[i] + 0.5 * (h ** 2) * f0[i] for i in range(2)]

        e_initial = lagrangian.kinetic_energy(v0) + lagrangian.potential_energy(q_prev)
        energies = []

        for _ in range(5000):
            q_next, p_curr = DiscreteVariationalIntegrator.step_central_force(q_prev, q_curr, h, lagrangian)
            v_curr = [p_curr[i] / lagrangian.mass for i in range(2)]
            e_step = lagrangian.kinetic_energy(v_curr) + lagrangian.potential_energy(q_curr)
            energies.append(e_step)
            q_prev, q_curr = q_curr, q_next

        min_e = min(energies)
        max_e = max(energies)
        delta_envelope = max_e - min_e

        self.assertLess(delta_envelope, 0.005)
        self.assertLess(abs(energies[-1] - e_initial), 0.005)

    def test_network_potential_mass_conservation_under_chaotic_conductance_mutation(self):
        """
        Total potential mass sum_i phi_i is strictly conserved to machine precision (< 1e-13)
        across 500 continuous diffusion iterations even as edge conductances W_ij(t) fluctuate chaotically.
        """
        lattice = ContinuousMutationLattice(num_nodes=16)
        initial_mass = lattice.initial_mass
        dt = 0.01

        mass_records = []
        for step in range(500):
            t = step * dt
            mass = lattice.step_continuous_mutation(dt=dt, t=t)
            mass_records.append(mass)

        final_mass = mass_records[-1]
        max_mass_drift = max(abs(m - initial_mass) for m in mass_records)

        self.assertAlmostEqual(initial_mass, final_mass, places=13)
        self.assertLess(max_mass_drift, 1e-13)

    def test_negative_control_asymmetric_leakage_breaks_mass_conservation(self):
        """
        Negative control: Introducing an asymmetric boundary leak immediately breaks mass conservation.
        """
        lattice = ContinuousMutationLattice(num_nodes=16)
        initial_mass = lattice.initial_mass
        dt = 0.01

        for step in range(100):
            t = step * dt
            lattice.step_continuous_mutation(dt=dt, t=t, leak_node=0, leak_rate=0.5)

        final_mass = sum(lattice.phi)
        self.assertNotAlmostEqual(initial_mass, final_mass, places=3)
        self.assertLess(final_mass, initial_mass)

    def test_schnakenberg_cycle_affinity_gauge_invariance(self):
        """
        Schnakenberg cycle affinity A(C) is strictly invariant under arbitrary continuous
        node gauge potential shifts psi in R^N.
        """
        engine = SchnakenbergCycleEngine(n=4)
        engine.set_rate(0, 1, 3.0)
        engine.set_rate(1, 0, 1.0)
        engine.set_rate(1, 2, 2.5)
        engine.set_rate(2, 1, 0.8)
        engine.set_rate(2, 3, 4.0)
        engine.set_rate(3, 2, 1.5)
        engine.set_rate(3, 0, 2.0)
        engine.set_rate(0, 3, 0.5)
        engine.set_rate(1, 3, 1.2)
        engine.set_rate(3, 1, 0.6)

        c1 = [0, 1, 2, 3]
        c2 = [1, 2, 3]

        orig_a1 = engine.cycle_affinity(c1)
        orig_a2 = engine.cycle_affinity(c2)

        for _ in range(50):
            psi = [random.uniform(-10.0, 10.0) for _ in range(4)]
            transformed_rates = engine.apply_gauge_transformation(psi)

            trans_a1 = engine.cycle_affinity(c1, rates=transformed_rates)
            trans_a2 = engine.cycle_affinity(c2, rates=transformed_rates)

            self.assertAlmostEqual(orig_a1, trans_a1, places=13)
            self.assertAlmostEqual(orig_a2, trans_a2, places=13)

    def test_schnakenberg_entropy_production_cycle_decomposition(self):
        """
        In a stationary non-equilibrium network, total entropy production rate sigma_NESS
        decomposes into fundamental cycle fluxes and affinities: sigma = sum_alpha J_alpha * A_alpha.
        """
        engine = SchnakenbergCycleEngine(n=3)
        engine.set_rate(0, 1, 4.0)
        engine.set_rate(1, 0, 1.0)
        engine.set_rate(1, 2, 3.0)
        engine.set_rate(2, 1, 1.0)
        engine.set_rate(2, 0, 2.0)
        engine.set_rate(0, 2, 0.5)

        p = engine.solve_steady_state()
        sigma_total = engine.entropy_production_rate(p)

        j_cycle = p[0] * engine.get_rate(0, 1) - p[1] * engine.get_rate(1, 0)
        affinity = engine.cycle_affinity([0, 1, 2])

        sigma_cycle_decomp = j_cycle * affinity

        self.assertAlmostEqual(sigma_total, sigma_cycle_decomp, places=12)
        self.assertGreater(sigma_total, 0.0)

    def test_thermodynamic_uncertainty_relation_dimensionless_bound(self):
        """
        Thermodynamic Uncertainty Relation (TUR): Q_TUR = Var(J) / <J>^2 * sigma * tau >= 2.0.
        """
        engine = SchnakenbergCycleEngine(n=3)
        engine.set_rate(0, 1, 2.0)
        engine.set_rate(1, 0, 1.0)
        engine.set_rate(1, 2, 2.0)
        engine.set_rate(2, 1, 1.0)
        engine.set_rate(2, 0, 2.0)
        engine.set_rate(0, 2, 1.0)

        p = engine.solve_steady_state()
        sigma = engine.entropy_production_rate(p)

        j_mean = p[0] * engine.get_rate(0, 1) - p[1] * engine.get_rate(1, 0)
        tau = 5.0
        diffusion = (p[0] * engine.get_rate(0, 1) + p[1] * engine.get_rate(1, 0)) / tau
        q_tur = (diffusion / (j_mean ** 2)) * sigma * tau

        self.assertGreaterEqual(q_tur, 2.0 - 1e-12)

    def test_jarzynski_fluctuation_trajectory_expectation(self):
        """
        Microscopic Jarzynski/Crooks equality: <exp(-Delta s_tot)> converges to 1.0.
        """
        engine = SchnakenbergCycleEngine(n=3)
        engine.set_rate(0, 1, 2.0)
        engine.set_rate(1, 0, 1.0)
        engine.set_rate(1, 2, 2.0)
        engine.set_rate(2, 1, 1.0)
        engine.set_rate(2, 0, 2.0)
        engine.set_rate(0, 2, 1.0)

        num_trajectories = 1000
        duration = 1.0
        exp_sum = 0.0

        for seed in range(num_trajectories):
            _, delta_s = engine.simulate_stochastic_trajectory(duration=duration, seed=seed + 1000, max_jumps=30)
            clipped_s = max(-20.0, min(20.0, delta_s))
            exp_sum += math.exp(-clipped_s)

        mean_exp = exp_sum / num_trajectories
        self.assertAlmostEqual(mean_exp, 1.0, delta=0.25)


if __name__ == "__main__":
    unittest.main()
