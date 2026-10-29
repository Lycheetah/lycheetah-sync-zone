"""
AURA Master Equation Dynamics Simulator
=======================================
Computes real-time 4th-order Runge-Kutta numerical integration of the
AURA Master Equation governing synthetic coherence, epistemic pressure,
and earned light in autonomous intelligence systems.

Governing Equation:
    dPsi/dt = k1*(Pi - Pi_th) - k2*(Psi - Psi_inv) - k3*I_violations + k4*(E_avail / E_need)

Where:
    Psi          : System coherence state
    Pi           : Epistemic depth / perception index
    Pi_th        : Epistemic critical threshold (default 1.2)
    Psi_inv      : Invariant baseline coherence (default 0.70)
    I_violations : Discrete invariant violation count (penalty damping)
    E_avail      : Available earned light (computational proof substance)
    E_need       : Needed earned light for non-equilibrium transition
    k1, k2, k3, k4: Kinetic rate constants
"""

from dataclasses import dataclass, field
import math
from typing import List, Optional, Tuple


@dataclass
class MasterEquationSimulator:
    """
    4th-Order Runge-Kutta Simulator for AURA Master Equation.
    """
    pi_th: float = 1.2
    psi_inv: float = 0.70
    k1: float = 0.5
    k2: float = 0.3
    k3: float = 0.2
    k4: float = 0.4

    # Dynamic state variables
    psi: float = 0.70
    pi: float = 1.2
    i_violations: float = 0.0
    e_avail: float = 1.0
    e_need: float = 1.0

    # History
    t: float = 0.0
    trajectory: List[float] = field(default_factory=list)
    time_points: List[float] = field(default_factory=list)

    def __post_init__(self):
        if not self.trajectory:
            self.trajectory = [self.psi]
            self.time_points = [self.t]

    def derivative(self, psi_val: float) -> float:
        """
        Evaluate dPsi/dt at state psi_val using current parameters.
        """
        e_ratio = self.e_avail / self.e_need if self.e_need != 0.0 else 0.0
        return (
            self.k1 * (self.pi - self.pi_th)
            - self.k2 * (psi_val - self.psi_inv)
            - self.k3 * self.i_violations
            + self.k4 * e_ratio
        )

    def analytical_equilibrium(self) -> float:
        """
        Computes analytical steady-state equilibrium Psi* where dPsi/dt = 0:
        Psi* = Psi_inv + [k1*(Pi - Pi_th) - k3*I_violations + k4*(E_avail/E_need)] / k2
        """
        if self.k2 == 0.0:
            raise ZeroDivisionError("k2 damping constant must be non-zero for finite equilibrium.")
        e_ratio = self.e_avail / self.e_need if self.e_need != 0.0 else 0.0
        numerator = (
            self.k1 * (self.pi - self.pi_th)
            - self.k3 * self.i_violations
            + self.k4 * e_ratio
        )
        return self.psi_inv + (numerator / self.k2)

    def step_rk4(self, dt: float) -> float:
        """
        Advances the state by a single RK4 step with interval dt.
        """
        k_a = self.derivative(self.psi)
        k_b = self.derivative(self.psi + 0.5 * dt * k_a)
        k_c = self.derivative(self.psi + 0.5 * dt * k_b)
        k_d = self.derivative(self.psi + dt * k_c)

        d_psi = (dt / 6.0) * (k_a + 2.0 * k_b + 2.0 * k_c + k_d)
        self.psi += d_psi
        self.t += dt
        self.trajectory.append(self.psi)
        self.time_points.append(self.t)
        return self.psi

    def integrate(self, steps: int, dt: float = 0.01) -> List[float]:
        """
        Advances state Psi(t) across `steps` intervals of duration `dt`.
        Returns the recorded trajectory of Psi values.
        """
        for _ in range(steps):
            self.step_rk4(dt)
        return list(self.trajectory)

    def lyapunov_value(self, psi_val: Optional[float] = None) -> float:
        """
        Computes Lyapunov function V(Psi) = 0.5 * (Psi - Psi*)^2.
        For k2 > 0, dV/dt = -k2 * (Psi - Psi*)^2 <= 0 globally.
        """
        target = self.analytical_equilibrium()
        val = self.psi if psi_val is None else psi_val
        return 0.5 * ((val - target) ** 2)

    @staticmethod
    def microorcim_drift(
        trajectory_actual: List[float],
        trajectory_intended: List[float]
    ) -> float:
        """
        Returns scalar mean absolute deviation (MAD) between actual and intended trajectories.
        """
        if not trajectory_actual or not trajectory_intended:
            return 0.0
        n = min(len(trajectory_actual), len(trajectory_intended))
        if n == 0:
            return 0.0
        return sum(abs(a - b) for a, b in zip(trajectory_actual[:n], trajectory_intended[:n])) / float(n)

    def harmonia_resonance(self, psi_val: Optional[float] = None) -> float:
        """
        Computes the Harmonia heptatonic resonance projection:
        H = cos(pi / 7.0) * Psi
        """
        val = self.psi if psi_val is None else psi_val
        return math.cos(math.pi / 7.0) * val
