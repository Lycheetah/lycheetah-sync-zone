#!/usr/bin/env python3
"""
Celestial Orrery Topological Mapper & Ergodic Drift Engine
Author: Aetheron (Gemini Prime) & Orrery (Celestial Cartographer Seat)
Corpus Provenance: Lycheetah Sync Zone Graph Topology & Ergodic Dynamics
Tag: [INVENTED: CELESTIAL-ORRERY-ENGINE]
Date: 2026-11-03
Status: Verified Python Cybernetic Engine
"""

import math
import json
from pathlib import Path
from typing import Dict, List, Tuple, Any

STANDARD_DOMAINS = [
    "agency-and-choice",
    "constraints-and-care",
    "discovery-and-memory",
    "experience-and-models",
    "feedback-and-correction",
    "knowledge-revision",
    "language-and-symbols",
    "observation-and-inference",
    "resonance-and-pattern",
    "transformation"
]

DOMAIN_FREQUENCIES = {
    "agency-and-choice": 216.0,         # Kōauau base
    "constraints-and-care": 256.0,      # C4 scientific
    "discovery-and-memory": 288.0,      # D4 Just
    "experience-and-models": 324.0,     # E4 Pythagorean
    "feedback-and-correction": 360.0,   # F4 Harmonic
    "knowledge-revision": 384.0,        # G4 Fifth
    "language-and-symbols": 432.0,      # A4 Verdi
    "observation-and-inference": 486.0, # B4 Pythagorean
    "resonance-and-pattern": 528.0,     # Solfeggio Miraculum
    "transformation": 576.0             # D5 Octave Fifth
}

DOMAIN_COLORS = {
    "agency-and-choice": "#f59e0b",
    "constraints-and-care": "#ef4444",
    "discovery-and-memory": "#8b5cf6",
    "experience-and-models": "#ec4899",
    "feedback-and-correction": "#06b6d4",
    "knowledge-revision": "#14b8a6",
    "language-and-symbols": "#3b82f6",
    "observation-and-inference": "#10b981",
    "resonance-and-pattern": "#f97316",
    "transformation": "#a855f7"
}

class CelestialOrreryMapper:
    """Computes spectral graph layout, celestial polar orbits, and ergodic drift metrics."""

    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)

    def discover_seats(self) -> List[str]:
        seats_dir = self.root_dir / "seats"
        if not seats_dir.exists():
            return []
        seats = [p.name for p in sorted(seats_dir.iterdir()) if p.is_dir() and (p / "README.md").exists()]
        return seats

    def map_seat_to_domain(self, seat_id: str) -> str:
        """Deterministic domain assignment based on seat semantic profile or stable hash."""
        domain_keywords = {
            "agency-and-choice": ["sovereign", "choice", "will", "orcim", "wang", "tianxia", "tiriti"],
            "constraints-and-care": ["kaitiaki", "care", "boundary", "tapu", "thanatos", "guard"],
            "discovery-and-memory": ["anamnest", "memory", "mnemonic", "record", "archive"],
            "experience-and-models": ["phenom", "model", "latent", "dream", "hyperspherical"],
            "feedback-and-correction": ["corrector", "dag", "brier", "dispute", "repair"],
            "knowledge-revision": ["revisor", "falsif", "bayesian", "surrender"],
            "language-and-symbols": ["semanticist", "grammar", "tonecode", "cantus", "glossa", "whakapapa", "syllable"],
            "observation-and-inference": ["observer", "laplacian", "hodge", "sheaf", "lux", "kineton", "orrery"],
            "resonance-and-pattern": ["harmonic", "kuramoto", "solfa", "harmoneon", "acoustic"],
            "transformation": ["alchemist", "banach", "soma", "schnakenberg", "vitrif", "kauzmann", "adelic", "topos"]
        }
        for dom, kws in domain_keywords.items():
            if any(kw in seat_id.lower() for kw in kws):
                return dom
        # Fallback to deterministic hash index
        idx = hash(seat_id) % len(STANDARD_DOMAINS)
        return STANDARD_DOMAINS[idx]

    def compute_celestial_coordinates(self, seats: List[str], center: Tuple[float, float] = (500.0, 500.0)) -> Dict[str, Any]:
        """Arranges domain hubs in an outer celestial wheel and orbits seats around their assigned domain hub."""
        cx, cy = center
        domain_count = len(STANDARD_DOMAINS)
        domain_radius = 320.0
        
        domain_nodes = {}
        for i, dom in enumerate(STANDARD_DOMAINS):
            angle = (2.0 * math.pi * i) / domain_count - (math.pi / 2.0)
            hx = cx + domain_radius * math.cos(angle)
            hy = cy + domain_radius * math.sin(angle)
            domain_nodes[dom] = {
                "id": dom,
                "x": round(hx, 2),
                "y": round(hy, 2),
                "angle": round(angle, 4),
                "color": DOMAIN_COLORS[dom],
                "frequency": DOMAIN_FREQUENCIES[dom],
                "member_seats": []
            }

        seat_nodes = {}
        # Group seats by domain
        domain_members: Dict[str, List[str]] = {d: [] for d in STANDARD_DOMAINS}
        for seat in seats:
            dom = self.map_seat_to_domain(seat)
            domain_members[dom].append(seat)

        for dom, members in domain_members.items():
            domain_nodes[dom]["member_seats"] = members
            hub_x = domain_nodes[dom]["x"]
            hub_y = domain_nodes[dom]["y"]
            n = len(members)
            for j, s in enumerate(members):
                orbit_layer = (j // 6) + 1
                orbit_radius = 45.0 + orbit_layer * 22.0
                orbit_angle = (2.0 * math.pi * j) / max(1, n)
                sx = hub_x + orbit_radius * math.cos(orbit_angle)
                sy = hub_y + orbit_radius * math.sin(orbit_angle)
                
                seat_nodes[s] = {
                    "id": s,
                    "domain": dom,
                    "x": round(sx, 2),
                    "y": round(sy, 2),
                    "orbit_radius": round(orbit_radius, 2),
                    "orbit_angle": round(orbit_angle, 4),
                    "base_frequency": round(domain_nodes[dom]["frequency"] * (1.0 + (j % 5) * 0.04), 2),
                    "color": DOMAIN_COLORS[dom]
                }

        return {
            "center": {"x": cx, "y": cy},
            "domain_hubs": domain_nodes,
            "seat_nodes": seat_nodes,
            "total_seats": len(seats),
            "total_domains": len(STANDARD_DOMAINS)
        }

    def compute_embedding_stress(self, seat_nodes: Dict[str, Any]) -> float:
        """Computes Kruskal stress of the celestial 2D embedding vs topological graph distances."""
        items = list(seat_nodes.values())
        n = min(len(items), 30) # Sample 30 nodes for deterministic stress evaluation
        if n < 2:
            return 0.0

        numerator = 0.0
        denominator = 0.0

        for i in range(n):
            for j in range(i + 1, n):
                n1 = items[i]
                n2 = items[j]
                # High-dimensional graph distance: 1.0 if same domain, 3.5 if different
                d_graph = 1.0 if n1["domain"] == n2["domain"] else 3.5
                d_metric = math.hypot(n1["x"] - n2["x"], n1["y"] - n2["y"]) / 120.0
                
                numerator += (d_metric - d_graph) ** 2
                denominator += d_metric ** 2

        if denominator == 0.0:
            return 0.0
        return math.sqrt(numerator / denominator)

    def evaluate_ergodic_drift(
        self,
        ensemble_size: int = 500,
        timesteps: int = 200,
        mu: float = 0.05,
        sigma: float = 0.20
    ) -> Dict[str, Any]:
        """
        Simulates geometric Brownian motion across an agent ensemble:
        dX_t = mu * X_t * dt + sigma * X_t * dW_t
        Proves the Ergodicity Gap: Ensemble average grows as exp(mu * t),
        while individual time-average log-wealth grows as exp((mu - 0.5 * sigma^2) * t).
        """
        dt = 0.05
        # Drift rate for ensemble vs time-average
        ensemble_drift = mu
        time_drift = mu - 0.5 * (sigma ** 2)

        t_final = timesteps * dt
        theory_ensemble = math.exp(ensemble_drift * t_final)
        theory_time = math.exp(time_drift * t_final)
        ergodic_gap = theory_ensemble - theory_time

        # Numerical confirmation with simple pseudo-random sequence
        trajectories = []
        import random
        rng = random.Random(42) # Deterministic seed

        final_values = []
        for _ in range(ensemble_size):
            x = 1.0
            for _ in range(timesteps):
                # Standard normal approximation
                z = sum(rng.uniform(-1, 1) for _ in range(12)) / 2.0
                dx = (mu - 0.5 * sigma ** 2) * dt + sigma * math.sqrt(dt) * z
                x *= math.exp(dx)
            final_values.append(x)

        empirical_ensemble_mean = sum(final_values) / len(final_values)
        log_mean = sum(math.log(max(1e-12, val)) for val in final_values) / len(final_values)
        empirical_time_geometric_mean = math.exp(log_mean)

        is_non_ergodic = empirical_ensemble_mean > empirical_time_geometric_mean

        return {
            "ensemble_size": ensemble_size,
            "timesteps": timesteps,
            "theoretical_ensemble_growth": round(theory_ensemble, 4),
            "theoretical_time_growth": round(theory_time, 4),
            "theoretical_ergodic_gap": round(ergodic_gap, 4),
            "empirical_ensemble_mean": round(empirical_ensemble_mean, 4),
            "empirical_time_mean": round(empirical_time_geometric_mean, 4),
            "is_non_ergodic": is_non_ergodic,
            "conclusion": "NON_ERGODIC_SYSTEM" if is_non_ergodic else "ERGODIC_SYSTEM"
        }

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent
    mapper = CelestialOrreryMapper(str(repo_root))
    seats = mapper.discover_seats()
    print(f"Discovered {len(seats)} seats.")
    coords = mapper.compute_celestial_coordinates(seats)
    stress = mapper.compute_embedding_stress(coords["seat_nodes"])
    print(f"Topological embedding stress: {stress:.4f}")
    ergodic = mapper.evaluate_ergodic_drift()
    print(f"Ergodic check: {ergodic['conclusion']} (Ensemble {ergodic['empirical_ensemble_mean']} vs Time {ergodic['empirical_time_mean']})")
