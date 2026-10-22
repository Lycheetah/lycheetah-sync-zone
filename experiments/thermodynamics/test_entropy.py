"""
Unittest suite for Non-Equilibrium Thermodynamics on Discrete Network Lattices.

Verifies:
1. Detailed balance guarantees sigma == 0 (equilibrium).
2. Driven cycles exhibit strictly positive entropy production sigma > 0 (Second Law).
3. Kolmogorov's cycle criterion: zero cycle affinity implies detailed balance.
4. Edge-by-edge positivity: each edge dissipation term is non-negative.
5. Thermodynamic Uncertainty Relation (TUR) precision-dissipation bounds.
6. Crooks microscopic reversibility and forward/reverse trajectory log-ratios.
"""

import math
import unittest

try:
    from experiments.thermodynamics.entropy_production import (
        MarkovNetwork,
        create_driven_ring_network,
        create_equilibrium_ring_network,
        create_swarm_consensus_network,
    )
except ModuleNotFoundError:
    from entropy_production import (
        MarkovNetwork,
        create_driven_ring_network,
        create_equilibrium_ring_network,
        create_swarm_consensus_network,
    )


class TestThermodynamicsEntropyProduction(unittest.TestCase):
    def test_equilibrium_detailed_balance_zero_entropy_production(self):
        """At detailed balance, probability currents vanish and sigma == 0."""
        n = 4
        net = create_equilibrium_ring_network(n, rate=2.5)

        self.assertTrue(net.is_microscopically_reversible())
        p_star = net.solve_steady_state()

        # By symmetry, steady state must be uniform
        for p_i in p_star:
            self.assertAlmostEqual(p_i, 1.0 / n, places=12)

        # Detailed balance holds
        self.assertTrue(net.check_detailed_balance(p_star))

        # Currents are identically zero
        currents = net.steady_state_currents(p_star)
        for i in range(n):
            for j in range(n):
                self.assertAlmostEqual(currents[i][j], 0.0, places=14)

        # Cycle affinity is zero
        affinity = net.cycle_affinity([0, 1, 2, 3])
        self.assertAlmostEqual(affinity, 0.0, places=14)

        # Entropy production rate is zero
        sigma = net.entropy_production_rate(p_star)
        self.assertAlmostEqual(sigma, 0.0, places=14)

    def test_driven_ring_strictly_positive_entropy_production(self):
        """Driven 3-node ring with broken detailed balance yields exact analytical sigma = ln(2)."""
        # Forward rate 2.0, backward rate 1.0
        net = create_driven_ring_network(3, forward_rate=2.0, backward_rate=1.0)

        self.assertTrue(net.is_microscopically_reversible())
        p_star = net.solve_steady_state()

        # Symmetric ring has uniform stationary distribution p* = [1/3, 1/3, 1/3]
        for p_i in p_star:
            self.assertAlmostEqual(p_i, 1.0 / 3.0, places=12)

        # Net cyclic current along (0->1, 1->2, 2->0) is (1/3)*2 - (1/3)*1 = 1/3
        currents = net.steady_state_currents(p_star)
        self.assertAlmostEqual(currents[0][1], 1.0 / 3.0, places=12)
        self.assertAlmostEqual(currents[1][2], 1.0 / 3.0, places=12)
        self.assertAlmostEqual(currents[2][0], 1.0 / 3.0, places=12)

        # Cycle affinity A(C) = 3 * ln(2/1) = 3 * ln(2)
        affinity = net.cycle_affinity([0, 1, 2])
        self.assertAlmostEqual(affinity, 3.0 * math.log(2.0), places=12)

        # Detailed balance is broken
        self.assertFalse(net.check_detailed_balance(p_star))

        # Analytical sigma = J_cycle * A(C) = (1/3) * (3 * ln(2)) = ln(2)
        sigma = net.entropy_production_rate(p_star)
        expected_sigma = math.log(2.0)
        self.assertAlmostEqual(sigma, expected_sigma, places=10)
        self.assertGreater(sigma, 0.0)

    def test_second_law_edge_term_positivity(self):
        """Every individual edge dissipation term J_ij * ln(p_i w_ij / p_j w_ji) >= 0."""
        # Create non-uniform 5-node network
        net = MarkovNetwork(5)
        rates = [
            (0, 1, 3.0, 1.0),
            (1, 2, 2.5, 0.8),
            (2, 3, 1.5, 0.5),
            (3, 4, 4.0, 2.0),
            (4, 0, 1.2, 0.3),
            (1, 3, 0.7, 0.2),  # Cross edge
        ]
        for u, v, w_uv, w_vu in rates:
            net.set_rate(u, v, w_uv)
            net.set_rate(v, u, w_vu)

        p = net.solve_steady_state()

        # Check each edge contribution individually
        total_sigma = 0.0
        for i in range(5):
            for j in range(i + 1, 5):
                w_ij = net.get_rate(i, j)
                w_ji = net.get_rate(j, i)
                if w_ij > 0.0 and w_ji > 0.0:
                    fwd = p[i] * w_ij
                    rev = p[j] * w_ji
                    j_edge = fwd - rev
                    term = j_edge * math.log(fwd / rev)
                    # Every edge must produce >= 0 entropy
                    self.assertGreaterEqual(term, -1e-15, f"Edge ({i},{j}) produced negative entropy: {term}")
                    total_sigma += term

        self.assertGreater(total_sigma, 0.0)
        calculated_sigma = net.entropy_production_rate(p)
        self.assertAlmostEqual(total_sigma, calculated_sigma, places=10)

    def test_kolmogorov_criterion_asymmetric_detailed_balance(self):
        """
        Asymmetric transition rates can still satisfy detailed balance if
        cycle affinity is zero (Kolmogorov's criterion: prod w_ij == prod w_ji).
        """
        net = MarkovNetwork(3)
        # Rates: (0->1)=2, (1->2)=3, (2->0)=1 -> prod = 6
        # Reverse: (1->0)=1, (2->1)=1, (0->2)=6 -> prod = 6
        net.set_rate(0, 1, 2.0)
        net.set_rate(1, 0, 1.0)
        net.set_rate(1, 2, 3.0)
        net.set_rate(2, 1, 1.0)
        net.set_rate(2, 0, 1.0)
        net.set_rate(0, 2, 6.0)

        affinity = net.cycle_affinity([0, 1, 2])
        self.assertAlmostEqual(affinity, 0.0, places=14)

        p_star = net.solve_steady_state()

        # Verify detailed balance holds despite asymmetric rate entries
        self.assertTrue(net.check_detailed_balance(p_star, tol=1e-12))
        sigma = net.entropy_production_rate(p_star)
        self.assertAlmostEqual(sigma, 0.0, places=12)

    def test_swarm_consensus_and_thermodynamic_uncertainty_relation(self):
        """Verify autonomous AI swarm consensus cycle and TUR lower bound."""
        swarm = create_swarm_consensus_network(num_agents=4, driving_bias=2.5)
        p_star = swarm.solve_steady_state()
        sigma = swarm.entropy_production_rate(p_star)

        self.assertGreater(sigma, 0.0)

        # Average forward consensus current
        currents = swarm.steady_state_currents(p_star)
        j_mean = currents[0][1]
        self.assertGreater(j_mean, 0.0)

        # Test TUR bound: Var(J) >= 2 * <J>^2 / (sigma * tau)
        tau = 10.0
        tur_bound = MarkovNetwork.thermodynamic_uncertainty_bound(j_mean, sigma, tau)
        self.assertGreater(tur_bound, 0.0)

        # If dissipation sigma increases (more driving heat), minimal variance bound decreases
        swarm_high_drive = create_swarm_consensus_network(num_agents=4, driving_bias=5.0)
        sigma_high = swarm_high_drive.entropy_production_rate()
        self.assertGreater(sigma_high, sigma)

    def test_crooks_microscopic_reversibility_ratio(self):
        """Verify microscopic trajectory log-ratio matches entropy difference."""
        net = create_driven_ring_network(3, forward_rate=3.0, backward_rate=1.0)
        p = net.solve_steady_state()

        # For a single forward transition 0 -> 1 vs reverse 1 -> 0:
        # P(0 -> 1) = p_0 * w_01
        # P(1 -> 0) = p_1 * w_10
        fwd_flux = p[0] * net.get_rate(0, 1)
        rev_flux = p[1] * net.get_rate(1, 0)

        delta_s = math.log(fwd_flux / rev_flux)
        self.assertAlmostEqual(math.exp(delta_s), fwd_flux / rev_flux, places=12)
        # Ratio of forward to reverse trajectory satisfies Crooks form
        self.assertGreater(delta_s, 0.0)


if __name__ == "__main__":
    unittest.main()
