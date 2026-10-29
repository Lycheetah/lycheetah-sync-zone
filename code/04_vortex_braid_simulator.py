#!/usr/bin/env python3
"""
Vortex Braid Simulator [INVENTED: QUANTUM-SIMULATION]

Simulates 2D point vortex advection under the Biot-Savart velocity field:
    u(x) = (1 / (2*pi)) * sum_j Gamma_j * (z_hat x (x - x_j)) / |x - x_j|^2

Steps vortices using Runge-Kutta 4th order (RK4), computes conserved
Hamiltonian energy, linear impulse, and angular momentum, and extracts the
resulting topological braid word in the Artin braid group B_N.

Authored by Zephyr (Gemini Fluid Invariance Seat)
Sovereign Authority: Mackenzie Conor James Clark (Mac)
Status: Canonical Speculative Simulation
Date: 2026-10-29
"""

import math
from dataclasses import dataclass
from typing import List, Tuple, Dict


@dataclass
class PointVortex:
    """Represents a discrete 2D point vortex singularity."""
    x: float
    y: float
    gamma: float
    label: str = ""

    @property
    def pos(self) -> Tuple[float, float]:
        return (self.x, self.y)


@dataclass
class BraidCrossing:
    """Represents a generator in the Artin braid group B_N."""
    index: int      # 1-based generator index k for sigma_k
    power: int      # +1 for over-crossing, -1 for under-crossing
    time: float     # Simulation time of crossing
    strand_a: int   # First vortex index involved
    strand_b: int   # Second vortex index involved

    def __str__(self) -> str:
        if self.power == 1:
            return f"sigma_{self.index}"
        elif self.power == -1:
            return f"sigma_{self.index}^-1"
        return f"sigma_{self.index}^{self.power}"


class VortexBraidSimulator:
    """
    Simulates inviscid 2D point vortex dynamics and extracts braid words.
    """

    def __init__(self, vortices: List[PointVortex], eps: float = 1e-12):
        self.vortices = [PointVortex(v.x, v.y, v.gamma, v.label or f"V{i+1}")
                         for i, v in enumerate(vortices)]
        self.n = len(self.vortices)
        self.eps = eps
        self.time = 0.0
        self.braid_history: List[BraidCrossing] = []

        # Initial conserved quantities
        self.initial_circulation = self.total_circulation()
        self.initial_hamiltonian = self.hamiltonian()
        self.initial_impulse = self.linear_impulse()
        self.initial_angular_momentum = self.angular_momentum()

    def total_circulation(self) -> float:
        """Conserved quantity: Gamma_tot = sum Gamma_i."""
        return sum(v.gamma for v in self.vortices)

    def linear_impulse(self) -> Tuple[float, float]:
        """Conserved quantity in unconfined 2D Euler flow: P = sum Gamma_i * r_i."""
        px = sum(v.gamma * v.x for v in self.vortices)
        py = sum(v.gamma * v.y for v in self.vortices)
        return (px, py)

    def angular_momentum(self) -> float:
        """Conserved quantity: I = sum Gamma_i * |r_i|^2."""
        return sum(v.gamma * (v.x**2 + v.y**2) for v in self.vortices)

    def hamiltonian(self) -> float:
        """
        Kirchhoff-Routh Hamiltonian energy:
        H = - (1 / (4*pi)) * sum_{i < j} Gamma_i * Gamma_j * ln(r_{ij}^2)
        """
        h = 0.0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                dx = self.vortices[i].x - self.vortices[j].x
                dy = self.vortices[i].y - self.vortices[j].y
                r2 = dx * dx + dy * dy
                if r2 > self.eps:
                    h -= (self.vortices[i].gamma * self.vortices[j].gamma / (4.0 * math.pi)) * math.log(r2)
        return h

    def compute_velocities(self, coords: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
        """
        Evaluates Biot-Savart velocity field:
        u_i = - (1 / (2*pi)) * sum_{j != i} Gamma_j * (y_i - y_j) / r_ij^2
        v_i =   (1 / (2*pi)) * sum_{j != i} Gamma_j * (x_i - x_j) / r_ij^2
        """
        vel = []
        for i in range(self.n):
            vx, vy = 0.0, 0.0
            xi, yi = coords[i]
            for j in range(self.n):
                if i == j:
                    continue
                xj, yj = coords[j]
                dx = xi - xj
                dy = yi - yj
                r2 = dx * dx + dy * dy + self.eps
                factor = self.vortices[j].gamma / (2.0 * math.pi * r2)
                vx -= factor * dy
                vy += factor * dx
            vel.append((vx, vy))
        return vel

    def step(self, dt: float):
        """Advances the vortex system by time dt using 4th-order Runge-Kutta (RK4)."""
        c0 = [(v.x, v.y) for v in self.vortices]
        k1 = self.compute_velocities(c0)

        c1 = [(c0[i][0] + 0.5 * dt * k1[i][0], c0[i][1] + 0.5 * dt * k1[i][1]) for i in range(self.n)]
        k2 = self.compute_velocities(c1)

        c2 = [(c0[i][0] + 0.5 * dt * k2[i][0], c0[i][1] + 0.5 * dt * k2[i][1]) for i in range(self.n)]
        k3 = self.compute_velocities(c2)

        c3 = [(c0[i][0] + dt * k3[i][0], c0[i][1] + dt * k3[i][1]) for i in range(self.n)]
        k4 = self.compute_velocities(c3)

        new_coords = [
            (
                c0[i][0] + (dt / 6.0) * (k1[i][0] + 2.0 * k2[i][0] + 2.0 * k3[i][0] + k4[i][0]),
                c0[i][1] + (dt / 6.0) * (k1[i][1] + 2.0 * k2[i][1] + 2.0 * k3[i][1] + k4[i][1]),
            )
            for i in range(self.n)
        ]

        # Detect strand crossings across x-projection during interval [t, t+dt]
        self._detect_crossings(c0, new_coords, dt)

        # Update positions
        for i in range(self.n):
            self.vortices[i].x = new_coords[i][0]
            self.vortices[i].y = new_coords[i][1]

        self.time += dt

    def _detect_crossings(self, c_old: List[Tuple[float, float]],
                          c_new: List[Tuple[float, float]], dt: float):
        """
        Detects zero-crossings of relative x-coordinates between pairs (i, j).
        Resolves over/under topology via relative transverse y-coordinate.
        """
        for i in range(self.n):
            for j in range(i + 1, self.n):
                dx0 = c_old[i][0] - c_old[j][0]
                dx1 = c_new[i][0] - c_new[j][0]
                if dx0 * dx1 <= 0.0 and abs(dx0 - dx1) > 1e-14:
                    # Estimate crossing time fraction alpha in [0, 1]
                    denom = dx0 - dx1
                    alpha = dx0 / denom if abs(denom) > 1e-14 else 0.5
                    t_cross = self.time + max(0.0, min(1.0, alpha)) * dt

                    # Position at crossing
                    y_i_cross = c_old[i][1] + alpha * (c_new[i][1] - c_old[i][1])
                    y_j_cross = c_old[j][1] + alpha * (c_new[j][1] - c_old[j][1])
                    x_cross = c_old[i][0] + alpha * (c_new[i][0] - c_old[i][0])

                    # Rank: count strands strictly to the left at crossing time
                    rank = 1
                    for m in range(self.n):
                        if m != i and m != j:
                            xm_cross = c_old[m][0] + alpha * (c_new[m][0] - c_old[m][0])
                            if xm_cross < x_cross:
                                rank += 1

                    # Over-crossing convention:
                    # Strand moving rightward (dx1 > dx0) passes over if its y is higher
                    if dx1 > dx0:
                        is_over = (y_i_cross > y_j_cross)
                    else:
                        is_over = (y_j_cross > y_i_cross)

                    power = 1 if is_over else -1
                    crossing = BraidCrossing(
                        index=rank,
                        power=power,
                        time=t_cross,
                        strand_a=i,
                        strand_b=j
                    )
                    self.braid_history.append(crossing)

    def braid_word(self) -> List[str]:
        """Returns the chronological sequence of Artin braid generators."""
        return [str(c) for c in self.braid_history]

    def reduced_braid_word(self) -> List[str]:
        """Cancels adjacent inverse generators sigma_i * sigma_i^-1 = 1."""
        stack: List[BraidCrossing] = []
        for c in self.braid_history:
            if stack and stack[-1].index == c.index and stack[-1].power == -c.power:
                stack.pop()
            else:
                stack.append(c)
        return [str(c) for c in stack]

    def verify_invariants(self) -> Dict[str, float]:
        """Calculates maximum deviation of all conserved quantities from initial values."""
        gamma_err = abs(self.total_circulation() - self.initial_circulation)
        h_err = abs(self.hamiltonian() - self.initial_hamiltonian)
        px, py = self.linear_impulse()
        p_err = math.sqrt((px - self.initial_impulse[0])**2 + (py - self.initial_impulse[1])**2)
        ang_err = abs(self.angular_momentum() - self.initial_angular_momentum)

        return {
            "circulation_drift": gamma_err,
            "hamiltonian_drift": h_err,
            "linear_impulse_drift": p_err,
            "angular_momentum_drift": ang_err,
        }


def create_regular_polygon_cluster(n: int, radius: float = 1.0,
                                   gamma: float = 2.0 * math.pi) -> List[PointVortex]:
    """Generates N identical point vortices arranged in a regular polygon."""
    vortices = []
    for k in range(n):
        theta = 2.0 * math.pi * k / n
        vx = radius * math.cos(theta)
        vy = radius * math.sin(theta)
        vortices.append(PointVortex(vx, vy, gamma, label=f"V{k+1}"))
    return vortices


if __name__ == "__main__":
    print("=" * 60)
    print("VORTEX BRAID SIMULATOR [INVENTED: QUANTUM-SIMULATION]")
    print("Fluid Invariance Seat: Zephyr (Gemini)")
    print("Sovereign: Mackenzie Conor James Clark (Mac)")
    print("=" * 60)

    # 1. Initialize 3-vortex rotating triad
    vortices = create_regular_polygon_cluster(n=3, radius=1.0, gamma=2.0 * math.pi)
    sim = VortexBraidSimulator(vortices)

    print(f"Initial Vortices: {sim.n}")
    print(f"Total Circulation: {sim.initial_circulation:.6f}")
    print(f"Initial Hamiltonian Energy: {sim.initial_hamiltonian:.6f}")
    print(f"Initial Linear Impulse: ({sim.initial_impulse[0]:.6f}, {sim.initial_impulse[1]:.6f})")

    # 2. Integrate 1000 steps with dt = 0.005
    dt = 0.005
    steps = 1000
    print(f"\nIntegrating {steps} steps (dt = {dt}, total time = {steps*dt:.3f}s)...")

    for s in range(steps):
        sim.step(dt)

    # 3. Check conservation laws
    invariants = sim.verify_invariants()
    print("\n--- Conserved Quantity Invariant Verification ---")
    print(f"Total Circulation Drift:      {invariants['circulation_drift']:.2e}")
    print(f"Hamiltonian Energy Drift:     {invariants['hamiltonian_drift']:.2e}")
    print(f"Linear Impulse Drift:         {invariants['linear_impulse_drift']:.2e}")
    print(f"Angular Momentum Drift:       {invariants['angular_momentum_drift']:.2e}")

    # Assert rigorous bounds
    assert invariants["circulation_drift"] < 1e-12, "Circulation must be strictly conserved."
    assert invariants["hamiltonian_drift"] < 1e-6, "Energy drift must be below 1e-6."
    assert invariants["linear_impulse_drift"] < 1e-10, "Linear impulse must be conserved."

    # 4. Analyze generated Braid Word
    braid = sim.braid_word()
    print(f"\nTotal Braid Crossings Detected: {len(braid)}")
    sample = braid[:12] if len(braid) >= 12 else braid
    print(f"Sample Braid Word: {' * '.join(sample)}")

    reduced = sim.reduced_braid_word()
    print(f"Reduced Braid Word Length: {len(reduced)}")

    # In a rotating triad, we expect continuous periodic crossings
    assert len(braid) > 0, "Topological braiding must detect crossings in rotating triad."

    print("\n" + "=" * 60)
    print(">>> VORTEX BRAID SIMULATION & CONSERVATION INVARIANTS: PASS <<<")
    print("=" * 60)
