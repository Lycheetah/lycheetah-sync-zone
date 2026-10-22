#!/usr/bin/env python3
"""
Simplicial Sheaf & Hodge Laplacian Engine
Author: Aura Meridian (Node 01: AURA-OBSERVER)
Seat: Aura Meridian · Lycheetah Sync Zone

Provides discrete exterior calculus on simplicial 2-complexes equipped with
cellular sheaves. Computes exact coboundary operators delta^0, delta^1,
Hodge Laplacians L_0, L_1, L_2, Moore-Penrose harmonic projections,
and sheaf Betti numbers.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
import numpy as np


@dataclass(frozen=True)
class Simplex:
    dim: int
    vertices: Tuple[int, ...]

    def __post_init__(self):
        if sorted(self.vertices) != list(self.vertices):
            raise ValueError(f"Vertices must be sorted in canonical order: {self.vertices}")
        if len(self.vertices) != self.dim + 1:
            raise ValueError(f"Dimension {self.dim} requires {self.dim + 1} vertices")


class SimplicialSheaf:
    """
    Finite simplicial 2-complex equipped with a cellular sheaf (F, rho).
    Stalks F(sigma) are finite-dimensional Euclidean spaces R^{d_sigma}.
    """

    def __init__(self):
        self.vertices: List[int] = []
        self.edges: List[Tuple[int, int]] = []
        self.faces: List[Tuple[int, int, int]] = []

        # Stalk dimensions
        self.stalk_dims: Dict[Tuple[int, ...], int] = {}

        # Restriction maps: rho[(face, coface)] = matrix (dim_coface x dim_face)
        self.restrictions: Dict[Tuple[Tuple[int, ...], Tuple[int, ...]], np.ndarray] = {}

        # Cached operators
        self._delta0: Optional[np.ndarray] = None
        self._delta1: Optional[np.ndarray] = None
        self._L0: Optional[np.ndarray] = None
        self._L1: Optional[np.ndarray] = None
        self._L2: Optional[np.ndarray] = None

    def add_vertex(self, v: int, stalk_dim: int = 1):
        if v not in self.vertices:
            self.vertices.append(v)
            self.vertices.sort()
        self.stalk_dims[(v,)] = stalk_dim
        self._invalidate_cache()

    def add_edge(self, u: int, v: int, stalk_dim: int = 1,
                 rho_u: Optional[np.ndarray] = None,
                 rho_v: Optional[np.ndarray] = None):
        u, v = sorted([u, v])
        edge = (u, v)
        if edge not in self.edges:
            self.edges.append(edge)
            self.edges.sort()
        self.stalk_dims[edge] = stalk_dim

        # Ensure vertices exist
        if (u,) not in self.stalk_dims:
            self.add_vertex(u, stalk_dim)
        if (v,) not in self.stalk_dims:
            self.add_vertex(v, stalk_dim)

        dim_u = self.stalk_dims[(u,)]
        dim_v = self.stalk_dims[(v,)]

        if rho_u is None:
            rho_u = np.eye(stalk_dim, dim_u)
        if rho_v is None:
            rho_v = np.eye(stalk_dim, dim_v)

        self.restrictions[((u,), edge)] = np.asarray(rho_u, dtype=np.float64)
        self.restrictions[((v,), edge)] = np.asarray(rho_v, dtype=np.float64)
        self._invalidate_cache()

    def add_face(self, u: int, v: int, w: int, stalk_dim: int = 1,
                 rho_e01: Optional[np.ndarray] = None,
                 rho_e12: Optional[np.ndarray] = None,
                 rho_e02: Optional[np.ndarray] = None):
        u, v, w = sorted([u, v, w])
        face = (u, v, w)
        if face not in self.faces:
            self.faces.append(face)
            self.faces.sort()
        self.stalk_dims[face] = stalk_dim

        e01 = (u, v)
        e12 = (v, w)
        e02 = (u, w)

        # Ensure edges exist
        for e in [e01, e12, e02]:
            if e not in self.edges:
                self.add_edge(e[0], e[1], stalk_dim)

        d_e01 = self.stalk_dims[e01]
        d_e12 = self.stalk_dims[e12]
        d_e02 = self.stalk_dims[e02]

        if rho_e01 is None:
            rho_e01 = np.eye(stalk_dim, d_e01)
        if rho_e12 is None:
            rho_e12 = np.eye(stalk_dim, d_e12)
        if rho_e02 is None:
            rho_e02 = np.eye(stalk_dim, d_e02)

        self.restrictions[(e01, face)] = np.asarray(rho_e01, dtype=np.float64)
        self.restrictions[(e12, face)] = np.asarray(rho_e12, dtype=np.float64)
        self.restrictions[(e02, face)] = np.asarray(rho_e02, dtype=np.float64)
        self._invalidate_cache()

    def _invalidate_cache(self):
        self._delta0 = None
        self._delta1 = None
        self._L0 = None
        self._L1 = None
        self._L2 = None

    @property
    def dim_C0(self) -> int:
        return sum(self.stalk_dims[(v,)] for v in self.vertices)

    @property
    def dim_C1(self) -> int:
        return sum(self.stalk_dims[e] for e in self.edges)

    @property
    def dim_C2(self) -> int:
        return sum(self.stalk_dims[f] for f in self.faces)

    def vertex_offset(self, v: int) -> int:
        offset = 0
        for vert in self.vertices:
            if vert == v:
                return offset
            offset += self.stalk_dims[(vert,)]
        raise KeyError(f"Vertex {v} not found")

    def edge_offset(self, e: Tuple[int, int]) -> int:
        offset = 0
        for edge in self.edges:
            if edge == e:
                return offset
            offset += self.stalk_dims[edge]
        raise KeyError(f"Edge {e} not found")

    def face_offset(self, f: Tuple[int, int, int]) -> int:
        offset = 0
        for face in self.faces:
            if face == f:
                return offset
            offset += self.stalk_dims[face]
        raise KeyError(f"Face {f} not found")

    def compute_coboundary_0(self) -> np.ndarray:
        """
        Builds delta^0: C^0(K; F) -> C^1(K; F).
        For oriented edge e = [u, v]:
          (delta^0 x)_e = rho_{v -> e} x_v - rho_{u -> e} x_u
        """
        if self._delta0 is not None:
            return self._delta0

        D0 = np.zeros((self.dim_C1, self.dim_C0), dtype=np.float64)

        for e in self.edges:
            u, v = e
            row_start = self.edge_offset(e)
            row_end = row_start + self.stalk_dims[e]

            # u block (negative sign)
            col_u_start = self.vertex_offset(u)
            col_u_end = col_u_start + self.stalk_dims[(u,)]
            rho_u = self.restrictions[((u,), e)]
            D0[row_start:row_end, col_u_start:col_u_end] = -rho_u

            # v block (positive sign)
            col_v_start = self.vertex_offset(v)
            col_v_end = col_v_start + self.stalk_dims[(v,)]
            rho_v = self.restrictions[((v,), e)]
            D0[row_start:row_end, col_v_start:col_v_end] = +rho_v

        self._delta0 = D0
        return D0

    def compute_coboundary_1(self) -> np.ndarray:
        """
        Builds delta^1: C^1(K; F) -> C^2(K; F).
        For oriented face f = [u, v, w] with u < v < w:
          boundary edges: e0 = [v, w], e1 = [u, w], e2 = [u, v]
          (delta^1 y)_f = rho_{e0 -> f} y_{e0} - rho_{e1 -> f} y_{e1} + rho_{e2 -> f} y_{e2}
        """
        if self._delta1 is not None:
            return self._delta1

        if self.dim_C2 == 0:
            D1 = np.zeros((0, self.dim_C1), dtype=np.float64)
            self._delta1 = D1
            return D1

        D1 = np.zeros((self.dim_C2, self.dim_C1), dtype=np.float64)

        for f in self.faces:
            u, v, w = f
            row_start = self.face_offset(f)
            row_end = row_start + self.stalk_dims[f]

            e_vw = (v, w)
            e_uw = (u, w)
            e_uv = (u, v)

            # e_vw (+ sign)
            c_vw = self.edge_offset(e_vw)
            d_vw = self.stalk_dims[e_vw]
            rho_vw = self.restrictions[(e_vw, f)]
            D1[row_start:row_end, c_vw:c_vw + d_vw] = +rho_vw

            # e_uw (- sign)
            c_uw = self.edge_offset(e_uw)
            d_uw = self.stalk_dims[e_uw]
            rho_uw = self.restrictions[(e_uw, f)]
            D1[row_start:row_end, c_uw:c_uw + d_uw] = -rho_uw

            # e_uv (+ sign)
            c_uv = self.edge_offset(e_uv)
            d_uv = self.stalk_dims[e_uv]
            rho_uv = self.restrictions[(e_uv, f)]
            D1[row_start:row_end, c_uv:c_uv + d_uv] = +rho_uv

        self._delta1 = D1
        return D1

    def verify_nilpotence(self, tol: float = 1e-12) -> Tuple[bool, float]:
        """
        Verifies delta^1 @ delta^0 == 0.
        Returns (is_nilpotent, frobenius_norm).
        """
        d0 = self.compute_coboundary_0()
        d1 = self.compute_coboundary_1()
        if d1.shape[0] == 0:
            return True, 0.0
        prod = d1 @ d0
        norm = float(np.linalg.norm(prod, ord='fro'))
        return norm < tol, norm

    def compute_laplacian_0(self) -> np.ndarray:
        """0-Laplacian L_0 = (delta^0)^T @ delta^0."""
        if self._L0 is None:
            d0 = self.compute_coboundary_0()
            self._L0 = d0.T @ d0
        return self._L0

    def compute_laplacian_1(self) -> np.ndarray:
        """1-Laplacian L_1 = delta^0 @ (delta^0)^T + (delta^1)^T @ delta^1."""
        if self._L1 is None:
            d0 = self.compute_coboundary_0()
            d1 = self.compute_coboundary_1()
            L1_down = d0 @ d0.T
            if d1.shape[0] > 0:
                L1_up = d1.T @ d1
            else:
                L1_up = np.zeros_like(L1_down)
            self._L1 = L1_down + L1_up
        return self._L1

    def compute_laplacian_2(self) -> np.ndarray:
        """2-Laplacian L_2 = delta^1 @ (delta^1)^T."""
        if self._L2 is None:
            d1 = self.compute_coboundary_1()
            if d1.shape[0] > 0:
                self._L2 = d1 @ d1.T
            else:
                self._L2 = np.zeros((0, 0), dtype=np.float64)
        return self._L2

    def hodge_decomposition(self, omega: np.ndarray, tol: float = 1e-10) -> Dict[str, np.ndarray]:
        """
        Computes exact discrete Hodge decomposition:
          omega = omega_grad + omega_curl + omega_harm
        using Moore-Penrose pseudo-inverses.
        """
        omega = np.asarray(omega, dtype=np.float64).flatten()
        if len(omega) != self.dim_C1:
            raise ValueError(f"1-cochain size mismatch: expected {self.dim_C1}, got {len(omega)}")

        d0 = self.compute_coboundary_0()
        d1 = self.compute_coboundary_1()
        L0 = self.compute_laplacian_0()
        L2 = self.compute_laplacian_2()

        # Gradient component: delta^0 @ pinv(L_0) @ (delta^0)^T @ omega
        L0_pinv = np.linalg.pinv(L0, rcond=tol)
        alpha = L0_pinv @ (d0.T @ omega)
        omega_grad = d0 @ alpha

        # Curl component: (delta^1)^T @ pinv(L_2) @ delta^1 @ omega
        if d1.shape[0] > 0:
            L2_pinv = np.linalg.pinv(L2, rcond=tol)
            beta = L2_pinv @ (d1 @ omega)
            omega_curl = d1.T @ beta
        else:
            omega_curl = np.zeros_like(omega)

        # Harmonic component
        omega_harm = omega - omega_grad - omega_curl

        return {
            "omega_grad": omega_grad,
            "omega_curl": omega_curl,
            "omega_harm": omega_harm,
            "norm_total": float(np.linalg.norm(omega)),
            "norm_grad": float(np.linalg.norm(omega_grad)),
            "norm_curl": float(np.linalg.norm(omega_curl)),
            "norm_harm": float(np.linalg.norm(omega_harm)),
        }

    def harmonic_projection_matrix(self, tol: float = 1e-10) -> np.ndarray:
        """
        Returns orthogonal projector P_harm onto ker(L_1).
        """
        d0 = self.compute_coboundary_0()
        d1 = self.compute_coboundary_1()
        L0 = self.compute_laplacian_0()
        L2 = self.compute_laplacian_2()

        I = np.eye(self.dim_C1, dtype=np.float64)
        L0_pinv = np.linalg.pinv(L0, rcond=tol)
        P_grad = d0 @ L0_pinv @ d0.T

        if d1.shape[0] > 0:
            L2_pinv = np.linalg.pinv(L2, rcond=tol)
            P_curl = d1.T @ L2_pinv @ d1
        else:
            P_curl = np.zeros_like(I)

        return I - P_grad - P_curl

    def betti_numbers(self, tol: float = 1e-10) -> Tuple[int, int, int]:
        """
        Computes sheaf Betti numbers:
          beta_0 = dim ker(L_0)
          beta_1 = dim ker(L_1)
          beta_2 = dim ker(L_2)
        """
        L0 = self.compute_laplacian_0()
        L1 = self.compute_laplacian_1()
        L2 = self.compute_laplacian_2()

        e0 = np.linalg.eigvalsh(L0)
        e1 = np.linalg.eigvalsh(L1)
        b0 = int(np.sum(e0 < tol))
        b1 = int(np.sum(e1 < tol))

        if L2.shape[0] > 0:
            e2 = np.linalg.eigvalsh(L2)
            b2 = int(np.sum(e2 < tol))
        else:
            b2 = 0

        return b0, b1, b2

    def spectral_gap_0(self, tol: float = 1e-10) -> float:
        """
        Returns the smallest positive eigenvalue of L_0 (Fiedler eigenvalue / algebraic connectivity).
        If all eigenvalues < tol, returns 0.0.
        """
        L0 = self.compute_laplacian_0()
        evals = np.sort(np.linalg.eigvalsh(L0))
        pos_evals = evals[evals > tol]
        return float(pos_evals[0]) if len(pos_evals) > 0 else 0.0


# ---------------------------------------------------------------------------
# Benchmark Complex Generators
# ---------------------------------------------------------------------------

def create_triangle_disk(stalk_dim: int = 1) -> SimplicialSheaf:
    """
    Contractible 2-simplex disk: 3 vertices, 3 edges, 1 face.
    Betti numbers: beta_0 = 1, beta_1 = 0, beta_2 = 0.
    """
    sheaf = SimplicialSheaf()
    for v in [0, 1, 2]:
        sheaf.add_vertex(v, stalk_dim)
    sheaf.add_edge(0, 1, stalk_dim)
    sheaf.add_edge(1, 2, stalk_dim)
    sheaf.add_edge(0, 2, stalk_dim)
    sheaf.add_face(0, 1, 2, stalk_dim)
    return sheaf


def create_triangulated_cylinder(n_segments: int = 3, stalk_dim: int = 1) -> SimplicialSheaf:
    """
    Triangulated cylinder (annulus) with n_segments:
    Bottom ring vertices: 0, 1, ..., n_segments-1
    Top ring vertices: n_segments, ..., 2*n_segments-1
    Homotopy circle: beta_0 = 1, beta_1 = 1, beta_2 = 0.
    """
    sheaf = SimplicialSheaf()
    n = n_segments
    for v in range(2 * n):
        sheaf.add_vertex(v, stalk_dim)

    # Bottom ring edges
    for i in range(n):
        sheaf.add_edge(i, (i + 1) % n, stalk_dim)

    # Top ring edges
    for i in range(n):
        sheaf.add_edge(n + i, n + ((i + 1) % n), stalk_dim)

    # Vertical and diagonal edges & faces
    for i in range(n):
        b0 = i
        b1 = (i + 1) % n
        t0 = n + i
        t1 = n + ((i + 1) % n)

        sheaf.add_edge(b0, t0, stalk_dim)
        sheaf.add_edge(b0, t1, stalk_dim)

        # Triangle 1: (b0, b1, t1)
        sheaf.add_face(b0, b1, t1, stalk_dim)
        # Triangle 2: (b0, t0, t1)
        sheaf.add_face(b0, t0, t1, stalk_dim)

    return sheaf


def create_twisted_mobius_sheaf(n_segments: int = 4) -> SimplicialSheaf:
    """
    Triangulated cylinder topology with an SO(2) stalk rotation twist theta = pi
    along the closing seam, creating a topological holonomy obstruction (Möbius sheaf).
    Collapses ker(L_0) to {0}.
    """
    sheaf = SimplicialSheaf()
    n = n_segments
    d = 2  # 2D stalks for SO(2) rotation
    for v in range(2 * n):
        sheaf.add_vertex(v, stalk_dim=d)

    # Reflection / pi-rotation matrix
    R_twist = np.array([[-1.0, 0.0], [0.0, -1.0]])

    for i in range(n):
        b0 = i
        b1 = (i + 1) % n
        t0 = n + i
        t1 = n + ((i + 1) % n)

        is_seam = (i == n - 1)
        rho_b = R_twist if is_seam else np.eye(2)
        rho_t = R_twist if is_seam else np.eye(2)

        sheaf.add_edge(b0, b1, stalk_dim=d, rho_v=rho_b)
        sheaf.add_edge(t0, t1, stalk_dim=d, rho_v=rho_t)
        sheaf.add_edge(b0, t0, stalk_dim=d)
        sheaf.add_edge(b0, t1, stalk_dim=d, rho_v=rho_t if is_seam else np.eye(2))

        sheaf.add_face(b0, b1, t1, stalk_dim=d)
        sheaf.add_face(b0, t0, t1, stalk_dim=d)

    return sheaf
