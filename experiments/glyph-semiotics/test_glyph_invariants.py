"""Unit tests for glyph semiotics and contour topological invariants.

Verifies:
- Simple loops: chi = 0, beta_0 = 1, beta_1 = 1.
- Figure-eight loops: chi = -1, beta_0 = 1, beta_1 = 2.
- Concentric contours: chi = 0, beta_0 = 2, beta_1 = 2, with winding number grading.
"""

from __future__ import annotations

import unittest

from contour_topology import (
    calculate_path_winding_number,
    calculate_total_winding_number,
    calculate_winding_number,
    compute_contour_topology,
    discretize_svg_path,
)


class TestGlyphTopologicalInvariants(unittest.TestCase):
    """Test topological invariants (Euler characteristic and winding numbers) of glyph contours."""

    def test_simple_loop_square(self):
        """A simple closed square contour has chi = 0, beta_0 = 1, beta_1 = 1."""
        svg = "M 0 0 L 10 0 L 10 10 L 0 10 Z"
        result = compute_contour_topology(svg)

        self.assertEqual(result.chi, 0, f"Expected chi=0 for simple loop, got {result.chi}")
        self.assertEqual(result.beta_0, 1, "Expected 1 connected component")
        self.assertEqual(result.beta_1, 1, "Expected 1 cycle (first Betti number = 1)")
        self.assertEqual(result.V, result.E, "For a simple cycle, V must equal E")

        # Winding numbers: inside = 1, outside = 0
        w_inside = calculate_path_winding_number((5.0, 5.0), svg)
        w_outside = calculate_path_winding_number((15.0, 15.0), svg)
        self.assertEqual(w_inside, 1, "Winding number inside CCW square must be 1")
        self.assertEqual(w_outside, 0, "Winding number outside square must be 0")

    def test_simple_loop_bezier_circle(self):
        """A smooth circle approximated by cubic Bezier curves has chi = 0 and beta_1 = 1."""
        # 4-quadrant cubic Bezier circle of radius 10
        svg = (
            "M 10 0 "
            "C 10 5.5228 5.5228 10 0 10 "
            "C -5.5228 10 -10 5.5228 -10 0 "
            "C -10 -5.5228 -5.5228 -10 0 -10 "
            "C 5.5228 -10 10 -5.5228 10 0 Z"
        )
        result = compute_contour_topology(svg, bezier_samples=8)

        self.assertEqual(result.chi, 0, f"Expected chi=0 for Bezier circle, got {result.chi}")
        self.assertEqual(result.beta_0, 1)
        self.assertEqual(result.beta_1, 1)

        w_center = calculate_path_winding_number((0.0, 0.0), svg, bezier_samples=8)
        w_exterior = calculate_path_winding_number((25.0, 0.0), svg, bezier_samples=8)
        self.assertEqual(w_center, 1)
        self.assertEqual(w_exterior, 0)

    def test_figure_eight_shared_vertex(self):
        """A figure-eight loop with two lobes meeting at a shared central vertex has chi = -1."""
        # Two triangular lobes sharing (0, 0)
        svg = "M 0 0 L 10 5 L 10 -5 L 0 0 L -10 -5 L -10 5 Z"
        result = compute_contour_topology(svg)

        self.assertEqual(result.chi, -1, f"Expected chi=-1 for figure-eight, got {result.chi}")
        self.assertEqual(result.beta_0, 1, "Figure-eight is a single connected component")
        self.assertEqual(result.beta_1, 2, "Figure-eight has two independent 1-cycles (beta_1 = 2)")
        self.assertEqual(result.E, result.V + 1, "E = V + 1 for figure-eight graph")

        # Winding numbers in each lobe
        contours = discretize_svg_path(svg)
        # Right lobe interior: (5.0, 0.0)
        w_right = abs(calculate_total_winding_number((5.0, 0.0), contours))
        # Left lobe interior: (-5.0, 0.0)
        w_left = abs(calculate_total_winding_number((-5.0, 0.0), contours))
        # Exterior
        w_ext = calculate_total_winding_number((0.0, 10.0), contours)

        self.assertEqual(w_right, 1, "Right lobe must enclose query point")
        self.assertEqual(w_left, 1, "Left lobe must enclose query point")
        self.assertEqual(w_ext, 0, "Exterior point must have zero winding number")

    def test_figure_eight_crossing_intersection(self):
        """A self-intersecting lemniscate path crossing at (0, 0) splits into chi = -1."""
        # Crossing hourglass contour
        svg = "M -10 -10 L 10 10 L 10 -10 L -10 10 Z"
        result = compute_contour_topology(svg)

        self.assertEqual(result.chi, -1, f"Expected chi=-1 for crossing lines, got {result.chi}")
        self.assertEqual(result.beta_0, 1)
        self.assertEqual(result.beta_1, 2)

    def test_concentric_contours(self):
        """Two disjoint concentric contours have chi = 0, beta_0 = 2, beta_1 = 2."""
        # Outer square: [-10, 10]^2; Inner square: [-4, 4]^2
        svg = "M -10 -10 L 10 -10 L 10 10 L -10 10 Z M -4 -4 L 4 -4 L 4 4 L -4 4 Z"
        result = compute_contour_topology(svg)

        self.assertEqual(result.chi, 0, f"Expected chi=0 for concentric loops, got {result.chi}")
        self.assertEqual(result.beta_0, 2, "Concentric loops have 2 disjoint connected components")
        self.assertEqual(result.beta_1, 2, "Concentric loops have 2 independent cycles")

        # Winding number gradient:
        # Center is inside both -> W = 2
        w_center = calculate_path_winding_number((0.0, 0.0), svg)
        self.assertEqual(w_center, 2, "Center point enclosed by both loops must have W=2")

        # Annulus between inner and outer -> W = 1
        w_annulus = calculate_path_winding_number((7.0, 0.0), svg)
        self.assertEqual(w_annulus, 1, "Annulus point must have W=1")

        # Exterior -> W = 0
        w_exterior = calculate_path_winding_number((15.0, 0.0), svg)
        self.assertEqual(w_exterior, 0, "Exterior point must have W=0")

    def test_concentric_contours_opposite_orientation(self):
        """Opposite orientations in concentric contours create winding cancellation (even-odd mode)."""
        # Outer CCW, inner CW
        svg = "M -10 -10 L 10 -10 L 10 10 L -10 10 Z M -4 -4 L -4 4 L 4 4 L 4 -4 Z"
        result = compute_contour_topology(svg)

        self.assertEqual(result.chi, 0)
        self.assertEqual(result.beta_0, 2)
        self.assertEqual(result.beta_1, 2)

        # Center: (+1) + (-1) = 0
        w_center = calculate_path_winding_number((0.0, 0.0), svg)
        self.assertEqual(w_center, 0, "Counter-oriented inner loop cancels outer winding number at center")

        # Annulus: (+1) + 0 = 1
        w_annulus = calculate_path_winding_number((7.0, 0.0), svg)
        self.assertEqual(w_annulus, 1)

    def test_evidential_morphemes(self):
        """Topological signatures of evidential morphemes."""
        # -meas (open ray vector): chi = 1 (V=2, E=1, beta_0=1, beta_1=0)
        ray_svg = "M 0 0 L 10 0"
        res_meas = compute_contour_topology(ray_svg)
        self.assertEqual(res_meas.chi, 1)
        self.assertEqual(res_meas.beta_1, 0)

        # -der (closed Jordan cycle): chi = 0 (V=E, beta_0=1, beta_1=1)
        loop_svg = "M 0 0 L 10 0 L 10 10 L 0 10 Z"
        res_der = compute_contour_topology(loop_svg)
        self.assertEqual(res_der.chi, 0)
        self.assertEqual(res_der.beta_1, 1)

        # -conj (broken open whisker arc): chi = 1 (V=4, E=3, beta_1=0)
        arc_svg = "M 0 0 L 10 0 L 10 10 L 0 10"  # unclosed
        res_conj = compute_contour_topology(arc_svg)
        self.assertEqual(res_conj.chi, 1)
        self.assertEqual(res_conj.beta_1, 0)

        # -kess (closed ring + isolated interior puncture dot):
        # beta_0 = 2, beta_1 = 1 -> chi = V - E = 2 - 1 = 1
        puncture_svg = "M -10 -10 L 10 -10 L 10 10 L -10 10 Z M -0.5 0 L 0.5 0"
        res_kess = compute_contour_topology(puncture_svg)
        self.assertEqual(res_kess.beta_0, 2)
        self.assertEqual(res_kess.beta_1, 1)
        self.assertEqual(res_kess.chi, 1)


if __name__ == "__main__":
    unittest.main()
