"""Verify discrete Laplacian conservation and Lyapunov bounds under perturbation."""

import math
import random
import unittest


class DiscreteLaplacianInvariantTests(unittest.TestCase):
    def setUp(self):
        # 14-node graph corresponding to Spectral Loom
        self.n = 14
        self.edges = []
        for i in range(self.n):
            self.edges.append((i, (i + 1) % self.n, 1.0))
            self.edges.append((i, (i + 3) % self.n, 0.5))

    def test_potential_conservation_under_unforced_diffusion(self):
        """Total potential sum(phi) must be invariant under pure diffusion (kappa * L)."""
        random.seed(42)
        phi = [random.uniform(-1.0, 1.0) for _ in range(self.n)]
        initial_sum = sum(phi)
        kappa = 0.06

        # Step diffusion 100 times without external damping
        for _ in range(100):
            lap = [0.0] * self.n
            for u, v, w in self.edges:
                diff = phi[u] - phi[v]
                lap[u] += w * diff
                lap[v] -= w * diff
            for i in range(self.n):
                phi[i] -= kappa * lap[i]

        final_sum = sum(phi)
        # Numerical error must be less than 1e-12
        self.assertAlmostEqual(initial_sum, final_sum, places=12)

    def test_negative_control_external_sink_violates_conservation(self):
        """Negative control: dissipative external sink breaks total potential conservation."""
        random.seed(42)
        phi = [random.uniform(0.1, 1.0) for _ in range(self.n)]
        initial_sum = sum(phi)

        # Dissipative open sink on node 0
        for _ in range(20):
            lap = [0.0] * self.n
            for u, v, w in self.edges:
                diff = phi[u] - phi[v]
                lap[u] += w * diff
                lap[v] -= w * diff
            # Node 0 has un-reciprocated dissipation to ground
            lap[0] += 0.25 * phi[0]
            for i in range(self.n):
                phi[i] -= 0.05 * lap[i]

        final_sum = sum(phi)
        self.assertNotAlmostEqual(initial_sum, final_sum, places=2)
        self.assertLess(final_sum, initial_sum)

    def test_lamb_oseen_divergence_free_vorticity(self):
        """Biot-Savart velocity field must have zero numerical divergence."""
        def get_vel(x, y, vortex_x=0.0, vortex_y=0.0, gamma=10.0, core=1.0):
            dx = x - vortex_x
            dy = y - vortex_y
            r2 = dx * dx + dy * dy
            r = math.sqrt(r2) + 1e-6
            factor = (gamma / (2 * math.pi * r)) * (1.0 - math.exp(-r2 / (core * core)))
            u = -factor * (dy / r)
            v = factor * (dx / r)
            return u, v

        eps = 1e-5
        max_div = 0.0
        # Sample points away from singular core center
        for px in [0.5, 1.0, 2.0, 3.5]:
            for py in [0.5, 1.0, 2.0, 3.5]:
                u_xp, _ = get_vel(px + eps, py)
                u_xm, _ = get_vel(px - eps, py)
                _, v_yp = get_vel(px, py + eps)
                _, v_ym = get_vel(px, py - eps)
                dudx = (u_xp - u_xm) / (2 * eps)
                dvdy = (v_yp - v_ym) / (2 * eps)
                div = abs(dudx + dvdy)
                if div > max_div:
                    max_div = div

        self.assertLess(max_div, 1e-4)


if __name__ == "__main__":
    unittest.main()
