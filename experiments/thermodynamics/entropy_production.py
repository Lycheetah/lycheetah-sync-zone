"""
Non-Equilibrium Thermodynamics on Discrete Network Lattices.

Calculates steady-state probability distributions, edge currents,
cycle affinities, and strictly positive entropy production rates (sigma)
for continuous-time Markov jump processes on finite graphs.
"""

import math
from typing import Dict, List, Optional, Sequence, Tuple


class MarkovNetwork:
    """Continuous-time Markov jump process on a discrete state space."""

    def __init__(self, n: int, state_names: Optional[Sequence[str]] = None) -> None:
        if n < 2:
            raise ValueError("Markov network must have at least 2 states.")
        self.n = n
        self.state_names = list(state_names) if state_names else [f"s{i}" for i in range(n)]
        if len(self.state_names) != n:
            raise ValueError(f"State names count ({len(self.state_names)}) must equal n ({n}).")
        # rates[i][j] is the transition rate from state i to state j (w_ij)
        self.rates: List[List[float]] = [[0.0] * n for _ in range(n)]

    def set_rate(self, i: int, j: int, rate: float) -> None:
        """Set the transition rate w_ij from state i to state j."""
        if i == j:
            raise ValueError("Diagonal transition rates w_ii are not set directly; they are defined as -sum_{k != i} w_ik.")
        if rate < 0.0:
            raise ValueError(f"Transition rate must be non-negative, got {rate}")
        if not (0 <= i < self.n and 0 <= j < self.n):
            raise IndexError("State index out of range.")
        self.rates[i][j] = float(rate)

    def get_rate(self, i: int, j: int) -> float:
        """Return transition rate w_ij."""
        return self.rates[i][j]

    def rate_matrix(self) -> List[List[float]]:
        """Return the infinitesimal generator matrix Q where Q_ij = w_ij for i != j and Q_ii = -sum_{k != i} w_ik."""
        q = [[0.0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            out_sum = 0.0
            for j in range(self.n):
                if i != j:
                    w = self.rates[i][j]
                    q[i][j] = w
                    out_sum += w
            q[i][i] = -out_sum
        return q

    def is_microscopically_reversible(self) -> bool:
        """Check whether every forward transition with rate > 0 has a non-zero reverse rate."""
        for i in range(self.n):
            for j in range(self.n):
                if i != j and self.rates[i][j] > 0.0:
                    if self.rates[j][i] <= 0.0:
                        return False
        return True

    def solve_steady_state(self) -> List[float]:
        """
        Solve the master equation steady-state distribution p* satisfying:
        sum_j p*_j Q_ji = 0 (i.e. p* Q = 0) and sum_i p*_i = 1.
        Uses exact Gaussian elimination with partial pivoting in pure Python.
        """
        q = self.rate_matrix()
        # Q^T has rows corresponding to d p_i / dt = sum_j Q_{ji} p_j
        # We replace the last row of Q^T with the normalization condition sum_i p_i = 1.
        a = [[q[j][i] for j in range(self.n)] for i in range(self.n)]
        # Replace row n-1 with normalization
        a[self.n - 1] = [1.0] * self.n
        b = [0.0] * (self.n - 1) + [1.0]

        # Gaussian elimination with partial pivoting
        m = [a[i][:] + [b[i]] for i in range(self.n)]
        for col in range(self.n):
            # Pivot
            pivot_row = max(range(col, self.n), key=lambda r: abs(m[r][col]))
            if abs(m[pivot_row][col]) < 1e-15:
                raise ValueError("Transition rate matrix is singular or disconnected (non-ergodic).")
            m[col], m[pivot_row] = m[pivot_row], m[col]
            pivot = m[col][col]
            for c in range(col, self.n + 1):
                m[col][c] /= pivot
            for r in range(self.n):
                if r != col:
                    factor = m[r][col]
                    for c in range(col, self.n + 1):
                        m[r][c] -= factor * m[col][c]

        p_star = [m[i][self.n] for i in range(self.n)]
        # Sanity check: probabilities must be non-negative
        for i, val in enumerate(p_star):
            if val < -1e-12:
                raise ValueError(f"Calculated negative probability p*[{i}] = {val}")
            p_star[i] = max(0.0, val)
        total = sum(p_star)
        return [val / total for val in p_star]

    def steady_state_currents(self, p: Optional[Sequence[float]] = None) -> List[List[float]]:
        """
        Calculate probability currents J_ij = p_i * w_ij - p_j * w_ji.
        Satisfies antisymmetry J_ij = -J_ji and J_ii = 0.
        """
        if p is None:
            p = self.solve_steady_state()
        j_curr = [[0.0] * self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                if i != j:
                    j_curr[i][j] = p[i] * self.rates[i][j] - p[j] * self.rates[j][i]
        return j_curr

    def entropy_production_rate(self, p: Optional[Sequence[float]] = None) -> float:
        """
        Calculate total entropy production rate sigma:
        sigma = sum_{i < j} J_ij * ln( (p_i * w_ij) / (p_j * w_ji) ) >= 0.
        At steady state p*, this simplifies to:
        sigma_NESS = 0.5 * sum_{i != j} J*_ij * ln( w_ij / w_ji ).
        """
        if p is None:
            p = self.solve_steady_state()
        sigma = 0.0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                w_ij = self.rates[i][j]
                w_ji = self.rates[j][i]
                if w_ij > 0.0 and w_ji > 0.0:
                    forward_flux = p[i] * w_ij
                    reverse_flux = p[j] * w_ji
                    current = forward_flux - reverse_flux
                    if abs(current) > 1e-16 and forward_flux > 0.0 and reverse_flux > 0.0:
                        term = current * math.log(forward_flux / reverse_flux)
                        sigma += term
        return max(0.0, sigma)

    def cycle_affinity(self, cycle: Sequence[int]) -> float:
        """
        Calculate the thermodynamic cycle affinity A(C) = sum ln(w_k,k+1 / w_k+1,k).
        By Kolmogorov's criterion, A(C) == 0 for all cycles if and only if detailed balance holds.
        """
        if len(cycle) < 3:
            raise ValueError("Cycle must have at least 3 vertices.")
        affinity = 0.0
        k = len(cycle)
        for idx in range(k):
            u = cycle[idx]
            v = cycle[(idx + 1) % k]
            w_uv = self.rates[u][v]
            w_vu = self.rates[v][u]
            if w_uv <= 0.0 or w_vu <= 0.0:
                raise ValueError(f"Cycle edge ({u}, {v}) lacks bidirectional transition rates.")
            affinity += math.log(w_uv / w_vu)
        return affinity

    def check_detailed_balance(self, p: Optional[Sequence[float]] = None, tol: float = 1e-10) -> bool:
        """Return True if detailed balance p_i * w_ij == p_j * w_ji holds across all edges."""
        currents = self.steady_state_currents(p)
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if abs(currents[i][j]) > tol:
                    return False
        return True

    @staticmethod
    def thermodynamic_uncertainty_bound(mean_current: float, sigma: float, duration: float) -> float:
        """
        Thermodynamic Uncertainty Relation (TUR) lower bound for variance:
        Var(J) >= 2 * <J>^2 / (sigma * duration).
        """
        if sigma <= 0.0 or duration <= 0.0:
            return float("inf")
        return (2.0 * (mean_current ** 2)) / (sigma * duration)


def create_driven_ring_network(n: int, forward_rate: float = 2.0, backward_rate: float = 1.0) -> MarkovNetwork:
    """Create a driven 1D cycle with n states and broken detailed balance."""
    net = MarkovNetwork(n)
    for i in range(n):
        nxt = (i + 1) % n
        net.set_rate(i, nxt, forward_rate)
        net.set_rate(nxt, i, backward_rate)
    return net


def create_equilibrium_ring_network(n: int, rate: float = 1.5) -> MarkovNetwork:
    """Create a symmetric 1D ring satisfying detailed balance."""
    net = MarkovNetwork(n)
    for i in range(n):
        nxt = (i + 1) % n
        net.set_rate(i, nxt, rate)
        net.set_rate(nxt, i, rate)
    return net


def create_swarm_consensus_network(num_agents: int = 4, driving_bias: float = 1.8) -> MarkovNetwork:
    """
    Model an autonomous agent swarm transitioning through consensus states:
    0: Proposal / Hypothesis Generation
    1: Peer Review / Dispute Check
    2: Verification / Test Harness
    3: Registry Commit / Landfall
    Driven by forward cognitive progress with thermodynamic dissipation.
    """
    net = MarkovNetwork(
        num_agents,
        state_names=["Hypothesis", "PeerReview", "Verification", "Commit"][:num_agents]
    )
    for i in range(num_agents):
        nxt = (i + 1) % num_agents
        net.set_rate(i, nxt, driving_bias)
        net.set_rate(nxt, i, 1.0)
    return net
