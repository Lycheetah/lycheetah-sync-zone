"""Contour Topology and Glyph Semiotics Engine.

Calculates topological invariants (Euler characteristic chi = V - E + F,
Betti numbers beta_0, beta_1, and winding numbers) for discretized SVG path commands
(M, L, C, Z, and related SVG path syntax).
"""

from __future__ import annotations

import math
import re
from collections import deque
from dataclasses import dataclass, field
from typing import List, Optional, Sequence, Set, Tuple

Point = Tuple[float, float]


@dataclass
class TopologyResult:
    """Topological invariants for a discretized glyph contour."""
    V: int
    E: int
    F: int
    chi: int
    beta_0: int
    beta_1: int
    contours: List[List[Point]] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"V={self.V}, E={self.E}, F={self.F} -> chi={self.chi} "
            f"(beta_0={self.beta_0}, beta_1={self.beta_1})"
        )


def parse_svg_path_tokens(path_str: str) -> List[Tuple[str, List[float]]]:
    """Parse an SVG path string into a list of (command, numbers) tuples.

    Supports M, m, L, l, H, h, V, v, C, c, S, s, Q, q, Z, z.
    """
    token_pattern = re.compile(
        r'([MmLlHhVvCcSsQqZz])|([+-]?(?:\d*\.\d+|\d+)(?:[eE][+-]?\d+)?)'
    )
    tokens = token_pattern.findall(path_str)

    commands: List[Tuple[str, List[float]]] = []
    current_cmd: Optional[str] = None
    current_nums: List[float] = []

    for cmd, num in tokens:
        if cmd:
            if current_cmd is not None:
                commands.append((current_cmd, current_nums))
            current_cmd = cmd
            current_nums = []
        elif num:
            current_nums.append(float(num))

    if current_cmd is not None:
        commands.append((current_cmd, current_nums))

    return commands


def evaluate_cubic_bezier(
    p0: Point, p1: Point, p2: Point, p3: Point, t: float
) -> Point:
    """Evaluate cubic Bézier curve at parameter t in [0, 1]."""
    u = 1.0 - t
    u2 = u * u
    u3 = u2 * u
    t2 = t * t
    t3 = t2 * t

    x = u3 * p0[0] + 3.0 * u2 * t * p1[0] + 3.0 * u * t2 * p2[0] + t3 * p3[0]
    y = u3 * p0[1] + 3.0 * u2 * t * p1[1] + 3.0 * u * t2 * p2[1] + t3 * p3[1]
    return (x, y)


def discretize_svg_path(
    path_str: str, bezier_samples: int = 16
) -> List[List[Point]]:
    """Discretize SVG path commands into a list of polyline subpaths (contours).

    Handles M, L, C, Z commands (absolute and relative).
    """
    raw_commands = parse_svg_path_tokens(path_str)
    contours: List[List[Point]] = []
    current_contour: List[Point] = []
    current_pos: Point = (0.0, 0.0)
    subpath_start: Point = (0.0, 0.0)

    for cmd, nums in raw_commands:
        if cmd in ('M', 'm'):
            if current_contour:
                contours.append(current_contour)
                current_contour = []
            it = iter(nums)
            first = True
            for x, y in zip(it, it):
                if cmd == 'm':
                    current_pos = (current_pos[0] + x, current_pos[1] + y)
                else:
                    current_pos = (x, y)
                if first:
                    subpath_start = current_pos
                    current_contour.append(current_pos)
                    first = False
                else:
                    current_contour.append(current_pos)

        elif cmd in ('L', 'l'):
            it = iter(nums)
            for x, y in zip(it, it):
                if cmd == 'l':
                    current_pos = (current_pos[0] + x, current_pos[1] + y)
                else:
                    current_pos = (x, y)
                current_contour.append(current_pos)

        elif cmd in ('H', 'h'):
            for x in nums:
                if cmd == 'h':
                    current_pos = (current_pos[0] + x, current_pos[1])
                else:
                    current_pos = (x, current_pos[1])
                current_contour.append(current_pos)

        elif cmd in ('V', 'v'):
            for y in nums:
                if cmd == 'v':
                    current_pos = (current_pos[0], current_pos[1] + y)
                else:
                    current_pos = (current_pos[0], y)
                current_contour.append(current_pos)

        elif cmd in ('C', 'c'):
            it = iter(nums)
            while True:
                chunk = [next(it, None) for _ in range(6)]
                if None in chunk:
                    break
                x1, y1, x2, y2, x, y = chunk  # type: ignore
                if cmd == 'c':
                    p1 = (current_pos[0] + x1, current_pos[1] + y1)
                    p2 = (current_pos[0] + x2, current_pos[1] + y2)
                    p3 = (current_pos[0] + x, current_pos[1] + y)
                else:
                    p1 = (x1, y1)
                    p2 = (x2, y2)
                    p3 = (x, y)
                p0 = current_pos

                for step in range(1, bezier_samples + 1):
                    t = step / float(bezier_samples)
                    pt = evaluate_cubic_bezier(p0, p1, p2, p3, t)
                    current_contour.append(pt)
                current_pos = p3

        elif cmd in ('Z', 'z'):
            if current_contour and current_contour[-1] != subpath_start:
                current_contour.append(subpath_start)
            current_pos = subpath_start
            if current_contour:
                contours.append(current_contour)
                current_contour = []

    if current_contour:
        contours.append(current_contour)

    # Clean contours: deduplicate consecutive identical points
    cleaned_contours: List[List[Point]] = []
    for c in contours:
        if not c:
            continue
        cleaned: List[Point] = [c[0]]
        for pt in c[1:]:
            dx = pt[0] - cleaned[-1][0]
            dy = pt[1] - cleaned[-1][1]
            if math.hypot(dx, dy) > 1e-6:
                cleaned.append(pt)
        if len(cleaned) >= 2:
            cleaned_contours.append(cleaned)

    return cleaned_contours


def calculate_winding_number(point: Point, contour: Sequence[Point]) -> int:
    """Calculate the integer winding number of a point with respect to a single closed contour.

    Uses continuous angle accumulation: W = (1 / 2pi) * sum(delta_theta_i).
    Counterclockwise contours yield positive winding numbers.
    """
    if len(contour) < 3:
        return 0

    px, py = point
    total_angle = 0.0

    n = len(contour)
    # Check if loop is explicitly closed at endpoints
    closed_contour = list(contour)
    if math.hypot(contour[0][0] - contour[-1][0], contour[0][1] - contour[-1][1]) > 1e-6:
        closed_contour.append(contour[0])

    for i in range(len(closed_contour) - 1):
        x1, y1 = closed_contour[i]
        x2, y2 = closed_contour[i + 1]

        u_x = x1 - px
        u_y = y1 - py
        v_x = x2 - px
        v_y = y2 - py

        # Cross product u x v and dot product u . v
        cross = u_x * v_y - u_y * v_x
        dot = u_x * v_x + u_y * v_y

        angle = math.atan2(cross, dot)
        total_angle += angle

    return int(round(total_angle / (2.0 * math.pi)))


def calculate_total_winding_number(
    point: Point, contours: Sequence[Sequence[Point]]
) -> int:
    """Calculate the total winding number of a point across multiple contours."""
    return sum(calculate_winding_number(point, c) for c in contours)


def calculate_path_winding_number(
    point: Point, path_str: str, bezier_samples: int = 16
) -> int:
    """Discretize an SVG path and calculate its total winding number at point."""
    contours = discretize_svg_path(path_str, bezier_samples=bezier_samples)
    return calculate_total_winding_number(point, contours)


def _segment_intersection(
    p1: Point, p2: Point, p3: Point, p4: Point, tol: float = 1e-7
) -> Optional[Tuple[float, float, Point]]:
    """Check if segments (p1, p2) and (p3, p4) intersect strictly in their relative interiors."""
    rx = p2[0] - p1[0]
    ry = p2[1] - p1[1]
    sx = p4[0] - p3[0]
    sy = p4[1] - p3[1]

    denom = rx * sy - ry * sx
    if abs(denom) < 1e-12:
        return None

    qx_minus_px = p3[0] - p1[0]
    qy_minus_py = p3[1] - p1[1]

    t = (qx_minus_px * sy - qy_minus_py * sx) / denom
    u = (qx_minus_px * ry - qy_minus_py * rx) / denom

    if tol < t < (1.0 - tol) and tol < u < (1.0 - tol):
        ix = p1[0] + t * rx
        iy = p1[1] + t * ry
        return (t, u, (ix, iy))
    return None


def subdivide_intersecting_segments(
    segments: List[Tuple[Point, Point]], tol: float = 1e-5
) -> List[Tuple[Point, Point]]:
    """Subdivide a set of 2D line segments at all mutual interior intersection points."""
    split_points: List[List[float]] = [[] for _ in segments]

    m = len(segments)
    for i in range(m):
        p1, p2 = segments[i]
        for j in range(i + 1, m):
            p3, p4 = segments[j]
            res = _segment_intersection(p1, p2, p3, p4, tol=1e-5)
            if res is not None:
                t, u, _ = res
                split_points[i].append(t)
                split_points[j].append(u)

    subdivided: List[Tuple[Point, Point]] = []
    for i, (p1, p2) in enumerate(segments):
        t_vals = [0.0] + sorted(set(split_points[i])) + [1.0]
        # Filter near duplicates
        filtered_t = [t_vals[0]]
        for t in t_vals[1:]:
            if t - filtered_t[-1] > 1e-5:
                filtered_t.append(t)
        if filtered_t[-1] < 1.0:
            filtered_t.append(1.0)

        for k in range(len(filtered_t) - 1):
            t_a = filtered_t[k]
            t_b = filtered_t[k + 1]
            pt_a = (p1[0] + t_a * (p2[0] - p1[0]), p1[1] + t_a * (p2[1] - p1[1]))
            pt_b = (p1[0] + t_b * (p2[0] - p1[0]), p1[1] + t_b * (p2[1] - p1[1]))
            if math.hypot(pt_b[0] - pt_a[0], pt_b[1] - pt_a[1]) > 1e-5:
                subdivided.append((pt_a, pt_b))

    return subdivided


def build_planar_graph(
    contours: List[List[Point]], tol: float = 1e-4
) -> Tuple[int, int, int, int]:
    """Construct a planar graph from polyline contours with vertex clustering and intersection splitting.

    Returns:
        (V, E, beta_0, beta_1)
    """
    raw_segments: List[Tuple[Point, Point]] = []
    for c in contours:
        for i in range(len(c) - 1):
            p1 = c[i]
            p2 = c[i + 1]
            if math.hypot(p2[0] - p1[0], p2[1] - p1[1]) > tol:
                raw_segments.append((p1, p2))

    if not raw_segments:
        return (0, 0, 0, 0)

    # Subdivide any segments that cross each other
    subdivided = subdivide_intersecting_segments(raw_segments, tol=tol)

    # Cluster unique vertices
    unique_vertices: List[Point] = []

    def get_vertex_id(pt: Point) -> int:
        for idx, v in enumerate(unique_vertices):
            if math.hypot(pt[0] - v[0], pt[1] - v[1]) <= tol:
                return idx
        unique_vertices.append(pt)
        return len(unique_vertices) - 1

    edges: Set[Tuple[int, int]] = set()
    for p1, p2 in subdivided:
        u = get_vertex_id(p1)
        v = get_vertex_id(p2)
        if u != v:
            edge = (min(u, v), max(u, v))
            edges.add(edge)

    V = len(unique_vertices)
    E = len(edges)

    if V == 0:
        return (0, 0, 0, 0)

    # Calculate connected components (beta_0)
    adj: List[List[int]] = [[] for _ in range(V)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = [False] * V
    beta_0 = 0
    for i in range(V):
        if not visited[i]:
            beta_0 += 1
            queue = deque([i])
            visited[i] = True
            while queue:
                curr = queue.popleft()
                for neighbor in adj[curr]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)

    # First Betti number (cycle rank)
    beta_1 = E - V + beta_0

    return (V, E, beta_0, beta_1)


def calculate_euler_characteristic(V: int, E: int, F: int = 0) -> int:
    """Calculate Euler characteristic chi = V - E + F."""
    return V - E + F


def compute_contour_topology(
    path_str: str,
    bezier_samples: int = 16,
    tol: float = 1e-4,
    F: int = 0,
) -> TopologyResult:
    """Compute the topological invariants of an SVG path.

    Calculates:
      - V: number of vertices (after clustering and intersection resolution)
      - E: number of undirected edges
      - F: number of faces (default 0 for 1-dimensional CW complexes)
      - chi = V - E + F
      - beta_0: connected components
      - beta_1: independent 1-cycles (cycle rank)
    """
    contours = discretize_svg_path(path_str, bezier_samples=bezier_samples)
    V, E, beta_0, beta_1 = build_planar_graph(contours, tol=tol)
    chi = calculate_euler_characteristic(V, E, F)

    return TopologyResult(
        V=V,
        E=E,
        F=F,
        chi=chi,
        beta_0=beta_0,
        beta_1=beta_1,
        contours=contours,
    )
