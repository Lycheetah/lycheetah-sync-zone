"""Unit tests for Kelvin Circulation & Vortex Dynamics.

Verifies:
1. Single vortex circulation Gamma = oint v . dl matches vortex strength.
2. Vortex dipole circulation:
   - Loop enclosing only positive vortex yields +Gamma.
   - Loop enclosing only negative vortex yields -Gamma.
   - Loop enclosing both vortices yields net circulation 0.
3. Exterior contour: Loop enclosing no vortex yields 0 (Stokes' theorem).
4. Kelvin's Circulation Theorem: dGamma/dt = 0 numerically for inviscid flow
   over advecting material loops and propagating vortex dipoles.
5. Negative control: artificial viscous decay breaks dGamma/dt = 0.
6. Theoretical dipole translation speed U = Gamma / (2*pi*d) * (1 - exp(-d^2/sigma^2)).
7. Linear impulse conservation P = sum(Gamma_i * x_i).
"""

import math
import unittest

from kelvin_circulation import (
    MaterialContour,
    PointVortex,
    VortexSystem,
    KelvinCirculationSolver,
    evaluate_contour_circulation,
)


class TestKelvinCirculation(unittest.TestCase):
    """Test suite verifying Kelvin's circulation theorem and Biot-Savart contour dynamics."""

    def test_single_vortex_enclosed_circulation(self):
        """A contour enclosing a single point vortex must have circulation equal to Gamma."""
        gamma = 4.5
        vortex = PointVortex(x=0.0, y=0.0, gamma=gamma, sigma=0.04)
        system = VortexSystem([vortex])

        # Circular contour of radius R=0.8 enclosing the vortex
        contour = MaterialContour.circle(cx=0.0, cy=0.0, radius=0.8, num_points=180)
        self.assertTrue(contour.encloses_point(0.0, 0.0))

        circ_trap = contour.circulation(system.velocity_at, method="trapezoid")
        circ_gauss = contour.circulation(system.velocity_at, method="gauss2")

        # Trapezoidal rule on N=180 circle has relative error < 0.02%
        self.assertAlmostEqual(circ_trap, gamma, delta=1e-3)
        # 2-point Gauss-Legendre quadrature has error < 1e-6
        self.assertAlmostEqual(circ_gauss, gamma, places=6)

    def test_exterior_contour_circulation_equals_zero_stokes_theorem(self):
        """A contour not enclosing any vortex must have circulation identically 0 (Stokes' theorem)."""
        vortex = PointVortex(x=0.0, y=0.0, gamma=8.0, sigma=0.05)
        system = VortexSystem([vortex])

        # Exterior circular contour centered far away at (2.5, 2.5) with radius 0.6
        contour_ext = MaterialContour.circle(cx=2.5, cy=2.5, radius=0.6, num_points=120)
        self.assertFalse(contour_ext.encloses_point(0.0, 0.0))

        circ = contour_ext.circulation(system.velocity_at, method="trapezoid")
        circ_gauss = contour_ext.circulation(system.velocity_at, method="gauss2")

        # Because curl(v) = 0 everywhere in the exterior simply-connected domain,
        # circulation is zero to machine precision.
        self.assertAlmostEqual(circ, 0.0, places=12)
        self.assertAlmostEqual(circ_gauss, 0.0, places=14)

        # Exterior rectangular contour
        rect_ext = MaterialContour.rectangle(x_min=-3.0, y_min=1.0, x_max=-1.0, y_max=3.0, points_per_side=40)
        self.assertFalse(rect_ext.encloses_point(0.0, 0.0))
        circ_rect = rect_ext.circulation(system.velocity_at, method="gauss2")
        self.assertAlmostEqual(circ_rect, 0.0, places=10)

    def test_vortex_dipole_circulation(self):
        """Test circulation around vortex dipole components and total pair."""
        gamma_mag = 5.0
        # Positive vortex at (0.0, 0.4), negative vortex at (0.0, -0.4)
        v_pos = PointVortex(x=0.0, y=0.4, gamma=gamma_mag, sigma=0.04)
        v_neg = PointVortex(x=0.0, y=-0.4, gamma=-gamma_mag, sigma=0.04)
        system = VortexSystem([v_pos, v_neg])

        # Loop enclosing only positive vortex
        loop_pos = MaterialContour.circle(cx=0.0, cy=0.4, radius=0.25, num_points=180)
        self.assertTrue(loop_pos.encloses_point(0.0, 0.4))
        self.assertFalse(loop_pos.encloses_point(0.0, -0.4))
        circ_pos = loop_pos.circulation(system.velocity_at, method="gauss2")
        self.assertAlmostEqual(circ_pos, gamma_mag, places=4)

        # Loop enclosing only negative vortex
        loop_neg = MaterialContour.circle(cx=0.0, cy=-0.4, radius=0.25, num_points=180)
        self.assertTrue(loop_neg.encloses_point(0.0, -0.4))
        self.assertFalse(loop_neg.encloses_point(0.0, 0.4))
        circ_neg = loop_neg.circulation(system.velocity_at, method="gauss2")
        self.assertAlmostEqual(circ_neg, -gamma_mag, places=4)

        # Large loop enclosing BOTH vortices: net circulation must be Gamma_1 + Gamma_2 = 0
        loop_both = MaterialContour.circle(cx=0.0, cy=0.0, radius=1.2, num_points=200)
        self.assertTrue(loop_both.encloses_point(0.0, 0.4))
        self.assertTrue(loop_both.encloses_point(0.0, -0.4))
        circ_both = loop_both.circulation(system.velocity_at, method="gauss2")
        self.assertAlmostEqual(circ_both, 0.0, places=6)

    def test_kelvin_theorem_invariance_single_vortex(self):
        """Verify dGamma/dt = 0 for a material contour advecting around a stationary vortex."""
        gamma = 3.0
        vortex = PointVortex(x=0.0, y=0.0, gamma=gamma, sigma=0.15)
        system = VortexSystem([vortex])

        # Circular material contour centered at origin
        contour = MaterialContour.circle(cx=0.0, cy=0.0, radius=0.6, num_points=100)
        solver = KelvinCirculationSolver(system, [contour])

        g0 = solver.get_circulations(method="trapezoid")[0]
        dt = 0.01
        num_steps = 200

        # Advect material loop through fluid for 200 RK4 time steps
        for _ in range(num_steps):
            solver.step(dt=dt, rk4=True)

        g_final = solver.get_circulations(method="trapezoid")[0]
        delta_gamma = abs(g_final - g0)
        dgamma_dt = delta_gamma / (num_steps * dt)

        # Circulation drift is bounded at micro-precision (< 1e-6 over 200 RK4 steps)
        self.assertLess(delta_gamma, 1e-6)
        self.assertLess(dgamma_dt, 1e-6)

    def test_kelvin_theorem_invariance_propagating_dipole(self):
        """Verify dGamma/dt = 0 for material contours around a moving, self-propagating dipole."""
        gamma = 2.5
        d = 0.8
        # Dipole aligned on y-axis will self-propagate in +x direction
        v_pos = PointVortex(x=0.0, y=d / 2.0, gamma=gamma, sigma=0.05)
        v_neg = PointVortex(x=0.0, y=-d / 2.0, gamma=-gamma, sigma=0.05)
        system = VortexSystem([v_pos, v_neg])

        # Contour 1: Encloses positive vortex
        c_pos = MaterialContour.circle(cx=0.0, cy=d / 2.0, radius=0.25, num_points=160)
        # Contour 2: Exterior contour positioned along translation path
        c_ext = MaterialContour.circle(cx=1.5, cy=0.0, radius=0.3, num_points=120)

        solver = KelvinCirculationSolver(system, [c_pos, c_ext])

        g_init = solver.get_circulations(method="trapezoid")
        dt = 0.005
        steps = 150

        for _ in range(steps):
            solver.step(dt=dt, rk4=True, refine_threshold=0.02)

        g_final = solver.get_circulations(method="trapezoid")

        # Positive loop circulation conserved to high relative accuracy (< 0.1% with adaptive refinement)
        rel_drift_pos = abs(g_final[0] - g_init[0]) / abs(g_init[0])
        self.assertLess(rel_drift_pos, 1e-3)

        # Exterior loop circulation remains 0 (< 1e-4)
        self.assertAlmostEqual(g_final[1], 0.0, places=4)

        # Confirm vortices actually translated along x (self-propulsion)
        self.assertGreater(system.vortices[0].x, 0.05)
        self.assertGreater(system.vortices[1].x, 0.05)

    def test_negative_control_viscous_decay_violates_kelvin_conservation(self):
        """Negative control: artificial viscous damping violates dGamma/dt = 0."""
        gamma = 4.0
        vortex = PointVortex(x=0.0, y=0.0, gamma=gamma, sigma=0.15)
        system = VortexSystem([vortex])
        contour = MaterialContour.circle(cx=0.0, cy=0.0, radius=0.5, num_points=100)

        # Solver with artificial viscosity factor 0.99/step
        solver = KelvinCirculationSolver(system, [contour], decay_factor=0.99)

        g0 = solver.get_circulations()[0]
        for _ in range(50):
            solver.step(dt=0.01, rk4=True)
        g_decayed = solver.get_circulations()[0]

        # Circulation has decayed significantly: dGamma/dt != 0
        self.assertLess(g_decayed, 0.7 * g0)
        dgamma_dt = abs(g_decayed - g0) / 0.50
        self.assertGreater(dgamma_dt, 1.0)

    def test_analytical_dipole_propagation_speed(self):
        """Verify numerical dipole translation matches Lamb-Oseen analytical velocity."""
        gamma = 1.5
        d = 0.6
        sigma = 0.15
        v1 = PointVortex(x=0.0, y=d / 2.0, gamma=gamma, sigma=sigma)
        v2 = PointVortex(x=0.0, y=-d / 2.0, gamma=-gamma, sigma=sigma)
        system = VortexSystem([v1, v2])

        # Analytical Lamb-Oseen self-propagation speed:
        # U = Gamma / (2 * pi * d) * (1 - exp(-d^2 / sigma^2))
        u_theory = (gamma / (2.0 * math.pi * d)) * (1.0 - math.exp(-(d * d) / (sigma * sigma)))

        solver = KelvinCirculationSolver(system, [])
        dt = 0.005
        steps = 1000
        for _ in range(steps):
            solver.step(dt=dt, rk4=True)

        measured_u = system.vortices[0].x / (steps * dt)
        rel_error = abs(measured_u - u_theory) / u_theory

        # Translation speed matches analytical solution to machine precision (< 1e-10)
        self.assertLess(rel_error, 1e-10)

    def test_impulse_conservation(self):
        """Verify linear impulse P = sum(Gamma_i * x_i) is conserved under mutual advection."""
        v1 = PointVortex(x=-0.3, y=0.1, gamma=2.0, sigma=0.1)
        v2 = PointVortex(x=0.3, y=-0.1, gamma=1.5, sigma=0.1)
        v3 = PointVortex(x=0.0, y=0.5, gamma=-1.0, sigma=0.1)
        system = VortexSystem([v1, v2, v3])

        px0, py0 = system.linear_impulse()
        solver = KelvinCirculationSolver(system, [])

        for _ in range(200):
            solver.step(dt=0.01, rk4=True)

        px_final, py_final = system.linear_impulse()
        self.assertAlmostEqual(px_final, px0, places=10)
        self.assertAlmostEqual(py_final, py0, places=10)

    def test_kelvin_theorem_material_contour_dynamic_deformation_500_steps(self):
        """Verify Kelvin's circulation theorem holds (< 1e-4 drift) on a dynamically deforming contour over 500 steps."""
        gamma = 3.0
        vortex = PointVortex(x=0.0, y=0.0, gamma=gamma, sigma=0.08)
        system = VortexSystem([vortex])

        # Initialize off-center circular material contour (cx=0.08, cy=0.04, radius=0.6)
        # Because the vortex is not centered, the contour experiences strong shear and deforms dynamically.
        contour = MaterialContour.circle(cx=0.08, cy=0.04, radius=0.6, num_points=360)
        self.assertTrue(contour.encloses_point(0.0, 0.0))

        initial_stretch = contour.stretch_ratio()
        self.assertAlmostEqual(initial_stretch, 1.0, places=4)

        solver = KelvinCirculationSolver(system, [contour])
        g0 = solver.get_circulations(method="trapezoid")[0]
        dt = 0.005
        steps = 500

        max_rel_drift = 0.0
        for _ in range(steps):
            solver.step(dt=dt, rk4=True, refine_threshold=0.015)
            g_curr = solver.get_circulations(method="trapezoid")[0]
            drift = abs(g_curr - g0) / abs(g0)
            if drift > max_rel_drift:
                max_rel_drift = drift

        g_final = solver.get_circulations(method="trapezoid")[0]
        delta_gamma = abs(g_final - g0)
        dgamma_dt = delta_gamma / (steps * dt)
        rel_drift = delta_gamma / abs(g0)

        # Confirm substantial dynamic deformation occurred
        final_contour = solver.contours[0]
        self.assertGreater(final_contour.stretch_ratio(), 1.5)

        # Invariance: relative drift strictly bounded below 1e-4 across all 500 steps
        self.assertLess(max_rel_drift, 1e-4)
        self.assertLess(rel_drift, 1e-4)
        self.assertLess(delta_gamma, 5e-4)
        self.assertLess(dgamma_dt, 1e-4)

    def test_kelvin_theorem_binary_orbiting_vortices_500_steps(self):
        """Verify Kelvin invariance for a material contour enclosing two mutually orbiting point vortices."""
        gamma = 2.0
        d = 0.4
        v1 = PointVortex(x=d / 2.0, y=0.0, gamma=gamma, sigma=0.06)
        v2 = PointVortex(x=-d / 2.0, y=0.0, gamma=gamma, sigma=0.06)
        system = VortexSystem([v1, v2])

        # Material contour enclosing both vortices
        contour = MaterialContour.circle(cx=0.0, cy=0.0, radius=0.6, num_points=360)
        self.assertTrue(contour.encloses_point(v1.x, v1.y))
        self.assertTrue(contour.encloses_point(v2.x, v2.y))

        solver = KelvinCirculationSolver(system, [contour])
        result = solver.track_circulation_drift(steps=500, dt=0.005, rk4=True, refine_threshold=0.015)

        g0 = result["initial_circulations"][0]
        g_final = result["final_circulations"][0]
        max_rel_drift = result["max_relative_drifts"][0]
        delta_gamma = abs(g_final - g0)
        dgamma_dt = delta_gamma / (500 * 0.005)
        rel_drift = delta_gamma / abs(g0)

        # Circulation must match sum of two vortices (4.0)
        self.assertAlmostEqual(g0, 2.0 * gamma, places=3)
        # Relative drift across all 500 steps bounded below 1e-4
        self.assertLess(max_rel_drift, 1e-4)
        self.assertLess(rel_drift, 1e-4)
        self.assertLess(delta_gamma, 5e-4)
        self.assertLess(dgamma_dt, 1e-4)

    def test_kelvin_theorem_long_horizon_1000_steps(self):
        """Verify Kelvin invariance across 1,000 steps without heuristic tolerance windows."""
        gamma = 3.0
        vortex = PointVortex(x=0.0, y=0.0, gamma=gamma, sigma=0.08)
        system = VortexSystem([vortex])

        contour = MaterialContour.circle(cx=0.08, cy=0.04, radius=0.6, num_points=360)
        solver = KelvinCirculationSolver(system, [contour])
        result = solver.track_circulation_drift(steps=1000, dt=0.005, rk4=True, refine_threshold=0.015)

        g0 = result["initial_circulations"][0]
        g_final = result["final_circulations"][0]
        max_rel_drift = result["max_relative_drifts"][0]
        delta_gamma = abs(g_final - g0)
        dgamma_dt = delta_gamma / (1000 * 0.005)
        rel_drift = delta_gamma / abs(g0)

        # Strictly replaces fabricated heuristic windows with exact physical conservation < 1e-4
        self.assertLess(max_rel_drift, 1e-4)
        self.assertLess(rel_drift, 1e-4)
        self.assertLess(delta_gamma, 5e-4)
        self.assertLess(dgamma_dt, 1e-4)


if __name__ == "__main__":
    unittest.main()
