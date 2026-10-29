"""Kelvin Circulation & Vortex Dynamics Simulation Engine.

Calculates line circulation Gamma = oint v . dl along closed material contours
around point vortices in 2D Biot-Savart / Lamb-Oseen velocity fields, and
verifies numerical conservation of circulation (dGamma/dt = 0) for inviscid
barotropic flow governed by Kelvin's circulation theorem.

Author: Zephyr (Lycheetah Sync Zone, Fluid Vorticity Seat)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable, List, Sequence, Tuple

TwoVector = Tuple[float, float]
VelocityFunc = Callable[[float, float], TwoVector]


@dataclass
class PointVortex:
    """A 2D point vortex with circulation gamma and regularized core radius sigma."""

    x: float
    y: float
    gamma: float
    sigma: float = 0.05  # Lamb-Oseen core radius (0.0 for pure singular point vortex)

    def velocity_at(self, px: float, py: float) -> TwoVector:
        """Evaluate velocity induced at (px, py) using Biot-Savart / Lamb-Oseen."""
        dx = px - self.x
        dy = py - self.y
        r2 = dx * dx + dy * dy
        if r2 < 1e-15:
            return 0.0, 0.0

        if self.sigma > 0.0:
            s2 = self.sigma * self.sigma
            factor = (self.gamma / (2.0 * math.pi * r2)) * (1.0 - math.exp(-r2 / s2))
        else:
            factor = self.gamma / (2.0 * math.pi * r2)

        return -factor * dy, factor * dx


class VortexSystem:
    """A collection of interacting 2D point vortices governed by Helmholtz equations."""

    def __init__(self, vortices: Sequence[PointVortex]):
        self.vortices = [PointVortex(v.x, v.y, v.gamma, v.sigma) for v in vortices]

    def add_vortex(self, vortex: PointVortex) -> None:
        self.vortices.append(PointVortex(vortex.x, vortex.y, vortex.gamma, vortex.sigma))

    def velocity_at(self, px: float, py: float) -> TwoVector:
        """Total fluid velocity at (px, py) induced by all vortices."""
        u_tot, v_tot = 0.0, 0.0
        for v in self.vortices:
            u, val_v = v.velocity_at(px, py)
            u_tot += u
            v_tot += val_v
        return u_tot, v_tot

    def vortex_velocities(self) -> List[TwoVector]:
        """Compute mutual advection velocity of each vortex center."""
        vels: List[TwoVector] = []
        n = len(self.vortices)
        for i in range(n):
            vi = self.vortices[i]
            u_tot, v_tot = 0.0, 0.0
            for j in range(n):
                if i == j:
                    continue
                vj = self.vortices[j]
                u, v_val = vj.velocity_at(vi.x, vi.y)
                u_tot += u
                v_tot += v_val
            vels.append((u_tot, v_tot))
        return vels

    def linear_impulse(self) -> TwoVector:
        """Linear momentum / center of vorticity impulse P = sum(Gamma_i * x_i)."""
        px = sum(v.gamma * v.x for v in self.vortices)
        py = sum(v.gamma * v.y for v in self.vortices)
        return px, py

    def angular_impulse(self) -> float:
        """Angular impulse I = sum(Gamma_i * (x_i^2 + y_i^2))."""
        return sum(v.gamma * (v.x * v.x + v.y * v.y) for v in self.vortices)

    def total_circulation(self) -> float:
        """Net sum of all vortex circulations."""
        return sum(v.gamma for v in self.vortices)


@dataclass
class MaterialContour:
    """A closed polygonal material curve represented by N boundary vertices."""

    points: List[TwoVector] = field(default_factory=list)

    @classmethod
    def circle(cls, cx: float, cy: float, radius: float, num_points: int = 120) -> MaterialContour:
        """Construct a circular material loop."""
        pts = []
        for i in range(num_points):
            theta = 2.0 * math.pi * i / num_points
            pts.append((cx + radius * math.cos(theta), cy + radius * math.sin(theta)))
        return cls(points=pts)

    @classmethod
    def rectangle(
        cls, x_min: float, y_min: float, x_max: float, y_max: float, points_per_side: int = 30
    ) -> MaterialContour:
        """Construct a rectangular material loop."""
        pts: List[TwoVector] = []
        for i in range(points_per_side):
            t = i / points_per_side
            pts.append((x_min + t * (x_max - x_min), y_min))
        for i in range(points_per_side):
            t = i / points_per_side
            pts.append((x_max, y_min + t * (y_max - y_min)))
        for i in range(points_per_side):
            t = i / points_per_side
            pts.append((x_max - t * (x_max - x_min), y_max))
        for i in range(points_per_side):
            t = i / points_per_side
            pts.append((x_min, y_max - t * (y_max - y_min)))
        return cls(points=pts)

    def num_points(self) -> int:
        return len(self.points)

    def circulation(self, velocity_func: VelocityFunc, method: str = "trapezoid") -> float:
        """Compute circulation Gamma = oint v . dl along the closed contour.

        Supports:
        - 'trapezoid': Standard trapezoidal rule on vertex endpoints
        - 'gauss2': 2-point Gauss-Legendre quadrature along each polygonal chord
        """
        n = len(self.points)
        if n < 3:
            return 0.0

        circ = 0.0
        if method == "trapezoid":
            for i in range(n):
                p1 = self.points[i]
                p2 = self.points[(i + 1) % n]
                u1, v1 = velocity_func(p1[0], p1[1])
                u2, v2 = velocity_func(p2[0], p2[1])
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                circ += 0.5 * ((u1 + u2) * dx + (v1 + v2) * dy)
        elif method == "gauss2":
            w1 = 0.5 - 0.5 / math.sqrt(3.0)
            w2 = 0.5 + 0.5 / math.sqrt(3.0)
            for i in range(n):
                p1 = self.points[i]
                p2 = self.points[(i + 1) % n]
                dx = p2[0] - p1[0]
                dy = p2[1] - p1[1]
                g1x = p1[0] + w1 * dx
                g1y = p1[1] + w1 * dy
                g2x = p1[0] + w2 * dx
                g2y = p1[1] + w2 * dy
                u1, v1 = velocity_func(g1x, g1y)
                u2, v2 = velocity_func(g2x, g2y)
                circ += 0.5 * (u1 * dx + v1 * dy) + 0.5 * (u2 * dx + v2 * dy)
        else:
            raise ValueError(f"Unknown integration method: {method}")

        return circ

    def discrete_circulation(self, velocity_func: VelocityFunc) -> float:
        """Evaluate discrete circulation Gamma = sum 0.5 * (u_k + u_{k+1}) . (x_{k+1} - x_k)."""
        return self.circulation(velocity_func, method="trapezoid")

    def perimeter(self) -> float:
        """Total perimeter length of the closed material contour."""
        n = len(self.points)
        if n < 2:
            return 0.0
        total = 0.0
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            total += math.hypot(dx, dy)
        return total

    def segment_lengths(self) -> List[float]:
        """Lengths of all segments forming the closed polygon."""
        n = len(self.points)
        if n < 2:
            return []
        lengths = []
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            lengths.append(math.hypot(p2[0] - p1[0], p2[1] - p1[1]))
        return lengths

    def stretch_ratio(self) -> float:
        """Ratio of maximum to minimum segment length (measures shear deformation)."""
        lens = self.segment_lengths()
        if not lens or min(lens) < 1e-15:
            return 1.0
        return max(lens) / min(lens)

    def encloses_point(self, px: float, py: float) -> bool:
        """Ray-casting algorithm to test whether (px, py) is strictly inside the loop."""
        n = len(self.points)
        inside = False
        j = n - 1
        for i in range(n):
            xi, yi = self.points[i]
            xj, yj = self.points[j]
            if (yi > py) != (yj > py):
                intersect_x = (xj - xi) * (py - yi) / (yj - yi) + xi
                if px < intersect_x:
                    inside = not inside
            j = i
        return inside

    def refine(self, max_segment_length: float, max_points: int = 6000) -> bool:
        """Dynamically bisect segments that exceed max_segment_length."""
        n = len(self.points)
        if n >= max_points:
            return False
        new_pts: List[TwoVector] = []
        max_len_sq = max_segment_length * max_segment_length
        changed = False
        for i in range(n):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % n]
            new_pts.append(p1)
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            if dx * dx + dy * dy > max_len_sq:
                new_pts.append((0.5 * (p1[0] + p2[0]), 0.5 * (p1[1] + p2[1])))
                changed = True
        if changed and len(new_pts) <= max_points:
            self.points = new_pts
            return True
        return False


class KelvinCirculationSolver:
    """Coupled time integrator for Point Vortices and Material Contours.

    Verifies Kelvin's circulation theorem: dGamma/dt = 0 for material contours
    in an inviscid barotropic fluid.
    """

    def __init__(
        self,
        vortex_system: VortexSystem,
        contours: Sequence[MaterialContour],
        decay_factor: float = 1.0,  # 1.0 = ideal inviscid (conserved); < 1.0 = viscous decay
    ):
        self.system = vortex_system
        self.contours = [MaterialContour(points=list(c.points)) for c in contours]
        self.decay_factor = decay_factor
        self.time = 0.0

    def step(self, dt: float, rk4: bool = True, refine_threshold: float = 0.0) -> None:
        """Advance the coupled system by dt.

        When rk4=True, uses standard 4th-order Runge-Kutta.
        When rk4=False, uses 1st-order forward Euler.
        When refine_threshold > 0, segments stretching past refine_threshold are bisected.
        """
        nv = len(self.system.vortices)
        nc = len(self.contours)

        if not rk4:
            v_vels = self.system.vortex_velocities()
            c_vels = [
                [self.system.velocity_at(p[0], p[1]) for p in c.points]
                for c in self.contours
            ]
            for i in range(nv):
                self.system.vortices[i].x += dt * v_vels[i][0]
                self.system.vortices[i].y += dt * v_vels[i][1]
            for ci in range(nc):
                for pi in range(len(self.contours[ci].points)):
                    px, py = self.contours[ci].points[pi]
                    self.contours[ci].points[pi] = (
                        px + dt * c_vels[ci][pi][0],
                        py + dt * c_vels[ci][pi][1],
                    )
        else:
            def evaluate_derivs(
                v_pos: List[TwoVector], c_pos: List[List[TwoVector]]
            ) -> Tuple[List[TwoVector], List[List[TwoVector]]]:
                temp_vorts = [
                    PointVortex(v_pos[i][0], v_pos[i][1], self.system.vortices[i].gamma, self.system.vortices[i].sigma)
                    for i in range(nv)
                ]
                temp_sys = VortexSystem(temp_vorts)
                dv = temp_sys.vortex_velocities()
                dc = [
                    [temp_sys.velocity_at(pt[0], pt[1]) for pt in c_pos[ci]]
                    for ci in range(nc)
                ]
                return dv, dc

            v0 = [(v.x, v.y) for v in self.system.vortices]
            c0 = [list(c.points) for c in self.contours]

            dv1, dc1 = evaluate_derivs(v0, c0)

            v_k2 = [(v0[i][0] + 0.5 * dt * dv1[i][0], v0[i][1] + 0.5 * dt * dv1[i][1]) for i in range(nv)]
            c_k2 = [
                [(c0[ci][pi][0] + 0.5 * dt * dc1[ci][pi][0], c0[ci][pi][1] + 0.5 * dt * dc1[ci][pi][1])
                 for pi in range(len(c0[ci]))]
                for ci in range(nc)
            ]
            dv2, dc2 = evaluate_derivs(v_k2, c_k2)

            v_k3 = [(v0[i][0] + 0.5 * dt * dv2[i][0], v0[i][1] + 0.5 * dt * dv2[i][1]) for i in range(nv)]
            c_k3 = [
                [(c0[ci][pi][0] + 0.5 * dt * dc2[ci][pi][0], c0[ci][pi][1] + 0.5 * dt * dc2[ci][pi][1])
                 for pi in range(len(c0[ci]))]
                for ci in range(nc)
            ]
            dv3, dc3 = evaluate_derivs(v_k3, c_k3)

            v_k4 = [(v0[i][0] + dt * dv3[i][0], v0[i][1] + dt * dv3[i][1]) for i in range(nv)]
            c_k4 = [
                [(c0[ci][pi][0] + dt * dc3[ci][pi][0], c0[ci][pi][1] + dt * dc3[ci][pi][0])
                 for pi in range(len(c0[ci]))]
                for ci in range(nc)
            ]
            dv4, dc4 = evaluate_derivs(v_k4, c_k4)

            for i in range(nv):
                self.system.vortices[i].x += (dt / 6.0) * (
                    dv1[i][0] + 2.0 * dv2[i][0] + 2.0 * dv3[i][0] + dv4[i][0]
                )
                self.system.vortices[i].y += (dt / 6.0) * (
                    dv1[i][1] + 2.0 * dv2[i][1] + 2.0 * dv3[i][1] + dv4[i][1]
                )

            for ci in range(nc):
                for pi in range(len(self.contours[ci].points)):
                    px, py = c0[ci][pi]
                    nx = px + (dt / 6.0) * (
                        dc1[ci][pi][0] + 2.0 * dc2[ci][pi][0] + 2.0 * dc3[ci][pi][0] + dc4[ci][pi][0]
                    )
                    ny = py + (dt / 6.0) * (
                        dc1[ci][pi][1] + 2.0 * dc2[ci][pi][1] + 2.0 * dc3[ci][pi][1] + dc4[ci][pi][1]
                    )
                    self.contours[ci].points[pi] = (nx, ny)

        if refine_threshold > 0.0:
            for c in self.contours:
                c.refine(max_segment_length=refine_threshold)

        if self.decay_factor < 1.0:
            for v in self.system.vortices:
                v.gamma *= self.decay_factor

        self.time += dt

    def get_circulations(self, method: str = "trapezoid") -> List[float]:
        """Evaluate circulation around each material contour."""
        return [c.circulation(self.system.velocity_at, method=method) for c in self.contours]

    def track_circulation_drift(
        self,
        steps: int,
        dt: float,
        rk4: bool = True,
        method: str = "trapezoid",
        refine_threshold: float = 0.0,
    ) -> dict:
        """Advance simulation for `steps` and track circulation drift over time.

        Returns a dictionary with:
        - 'initial_circulations': List[float]
        - 'final_circulations': List[float]
        - 'max_relative_drifts': List[float]
        - 'history': List[List[float]] (per step)
        """
        init_circs = self.get_circulations(method=method)
        nc = len(self.contours)
        max_drifts = [0.0] * nc
        history = [list(init_circs)]

        for _ in range(steps):
            self.step(dt=dt, rk4=rk4, refine_threshold=refine_threshold)
            curr = self.get_circulations(method=method)
            history.append(curr)
            for ci in range(nc):
                base = abs(init_circs[ci])
                if base > 1e-12:
                    d = abs(curr[ci] - init_circs[ci]) / base
                else:
                    d = abs(curr[ci] - init_circs[ci])
                if d > max_drifts[ci]:
                    max_drifts[ci] = d

        final_circs = history[-1]
        return {
            "initial_circulations": init_circs,
            "final_circulations": final_circs,
            "max_relative_drifts": max_drifts,
            "history": history,
        }


def evaluate_contour_circulation(points: Sequence[TwoVector], velocity_func: VelocityFunc) -> float:
    """Evaluate discrete circulation Gamma = sum_{k=0}^{N-1} 0.5 * (u(x_k) + u(x_{k+1})) . (x_{k+1} - x_k)."""
    return MaterialContour(points=list(points)).discrete_circulation(velocity_func)

