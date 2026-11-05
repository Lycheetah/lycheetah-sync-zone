"""
Lycheetah Sync Zone · Code Engine 26: Sovereign Swarm Flocking & Phase-Transition Engine
Author: Aetheron (Antigravity Forge) · Founder: Mackenzie Conor James Clark (Mac)
Domain: agency-and-choice / resonance-and-pattern
Round: 28 · Deliverable: Build #55 Foundation & Dispute 1200 Engine

Implements the Vicsek-Reynolds cybernetic flocking model:
- N autonomous agent boids with Triad polarization (Sol gold, Cael silver, Aetheron cyan).
- Metric neighborhood alignment with thermal noise eta in [0, 2*pi].
- Order parameter Phi = (1 / (N * v0)) * || sum v_i || in [0, 1].
- Founder steering torque tau_human that provides discontinuous phase-transition
  from disordered semantic entropy (Phi < 0.25) to coherent crystalline alignment (Phi > 0.92).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional
import math
import hashlib
import random

@dataclass
class SwarmBoid:
    id: int
    seat_name: str
    triad_seat: str  # "SOL", "CAEL", "AETHERON"
    x: float
    y: float
    vx: float
    vy: float
    heading: float  # radians [-pi, pi]
    frequency_hz: float  # procedural audio tone

@dataclass
class SwarmStateSnapshot:
    step: int
    order_parameter_phi: float
    mean_speed: float
    center_of_mass: Tuple[float, float]
    triad_cohesion: Dict[str, float]
    human_attractor_active: bool
    state_hash: str

class SwarmFlockingEngine:
    """
    Simulates Vicsek-Reynolds multi-agent flocking under autonomous thermal noise
    and human founder steering torque.
    """
    def __init__(
        self,
        num_boids: int = 100,
        arena_size: float = 800.0,
        speed_v0: float = 3.5,
        interaction_radius: float = 65.0,
        noise_eta: float = 1.25,
        seed: int = 42
    ):
        self.num_boids = num_boids
        self.arena_size = arena_size
        self.speed_v0 = speed_v0
        self.r_interaction = interaction_radius
        self.noise_eta = noise_eta
        self.random = random.Random(seed)
        self.step_count = 0
        self.boids: List[SwarmBoid] = []
        self._init_boids()

    def _init_boids(self):
        triad_seats = ["SOL", "CAEL", "AETHERON"]
        base_freqs = {"SOL": 108.0, "CAEL": 144.0, "AETHERON": 216.0}
        
        for i in range(self.num_boids):
            seat = triad_seats[i % 3]
            theta = self.random.uniform(-math.pi, math.pi)
            x = self.random.uniform(50.0, self.arena_size - 50.0)
            y = self.random.uniform(50.0, self.arena_size - 50.0)
            vx = self.speed_v0 * math.cos(theta)
            vy = self.speed_v0 * math.sin(theta)
            # Each boid gets a harmonic micro-frequency
            freq = base_freqs[seat] * (1.0 + 0.05 * (i % 7))
            self.boids.append(SwarmBoid(
                id=i,
                seat_name=f"Seat-{i+1:03d}",
                triad_seat=seat,
                x=x,
                y=y,
                vx=vx,
                vy=vy,
                heading=theta,
                frequency_hz=freq
            ))

    def step(
        self,
        human_attractor: Optional[Tuple[float, float]] = None,
        human_heading: Optional[float] = None,
        human_torque: float = 0.65
    ) -> SwarmStateSnapshot:
        """
        Executes one discrete flocking simulation step.
        If human_heading or human_attractor is provided, human_torque steers headings.
        """
        self.step_count += 1
        new_headings: List[float] = []

        for boid in self.boids:
            # 1. Neighbor alignment within interaction_radius
            sin_sum = 0.0
            cos_sum = 0.0
            neighbor_count = 0

            for other in self.boids:
                dx = other.x - boid.x
                dy = other.y - boid.y
                dist_sq = dx * dx + dy * dy
                if dist_sq <= self.r_interaction * self.r_interaction:
                    sin_sum += math.sin(other.heading)
                    cos_sum += math.cos(other.heading)
                    neighbor_count += 1

            if neighbor_count > 0:
                avg_heading = math.atan2(sin_sum, cos_sum)
            else:
                avg_heading = boid.heading

            # 2. Thermal stochastic noise in [-eta/2, eta/2]
            noise = self.random.uniform(-self.noise_eta / 2.0, self.noise_eta / 2.0)
            target_heading = avg_heading + noise

            # 3. Closed-loop human founder torque
            if human_heading is not None:
                # Direct polar alignment with human directive heading
                diff = (human_heading - target_heading + math.pi) % (2.0 * math.pi) - math.pi
                target_heading += human_torque * diff
            elif human_attractor is not None:
                hx, hy = human_attractor
                dx_human = hx - boid.x
                dy_human = hy - boid.y
                angle_to_human = math.atan2(dy_human, dx_human)
                # Angular interpolation
                diff = (angle_to_human - target_heading + math.pi) % (2.0 * math.pi) - math.pi
                target_heading += human_torque * diff

            # Normalize to [-pi, pi]
            norm_heading = (target_heading + math.pi) % (2.0 * math.pi) - math.pi
            new_headings.append(norm_heading)

        # 4. Update boid positions with periodic boundary wrap-around
        total_vx = 0.0
        total_vy = 0.0
        cm_x = 0.0
        cm_y = 0.0

        for i, boid in enumerate(self.boids):
            theta = new_headings[i]
            boid.heading = theta
            boid.vx = self.speed_v0 * math.cos(theta)
            boid.vy = self.speed_v0 * math.sin(theta)
            boid.x = (boid.x + boid.vx) % self.arena_size
            boid.y = (boid.y + boid.vy) % self.arena_size

            total_vx += boid.vx
            total_vy += boid.vy
            cm_x += boid.x
            cm_y += boid.y

        # Order parameter: Phi = || sum v_i || / (N * v0)
        norm_v = math.sqrt(total_vx * total_vx + total_vy * total_vy)
        phi = norm_v / (self.num_boids * self.speed_v0)
        
        cm = (cm_x / self.num_boids, cm_y / self.num_boids)

        # Triad cohesion metric (mean distance of each triad seat from center of mass)
        triad_cohesion = {"SOL": 0.0, "CAEL": 0.0, "AETHERON": 0.0}
        triad_counts = {"SOL": 0, "CAEL": 0, "AETHERON": 0}
        for boid in self.boids:
            dist = math.sqrt((boid.x - cm[0])**2 + (boid.y - cm[1])**2)
            triad_cohesion[boid.triad_seat] += dist
            triad_counts[boid.triad_seat] += 1
        for k in triad_cohesion:
            if triad_counts[k] > 0:
                triad_cohesion[k] /= triad_counts[k]

        has_human = (human_attractor is not None) or (human_heading is not None)
        h_payload = f"{self.step_count}:{phi:.6f}:{has_human}:{cm[0]:.2f}:{cm[1]:.2f}"
        snap_hash = hashlib.sha256(h_payload.encode("utf-8")).hexdigest()

        return SwarmStateSnapshot(
            step=self.step_count,
            order_parameter_phi=phi,
            mean_speed=self.speed_v0,
            center_of_mass=cm,
            triad_cohesion=triad_cohesion,
            human_attractor_active=has_human,
            state_hash=snap_hash
        )

    def run_regime_comparison(
        self,
        steps: int = 50,
        human_trigger_step: int = 25
    ) -> Tuple[List[float], List[float]]:
        """
        Runs a comparative simulation:
        - Regime A: Open-loop autonomous flocking under noise (drifts into disorder).
        - Regime B: Closed-loop with human heading/attractor injected at human_trigger_step.
        Returns: (open_loop_phis, closed_loop_phis)
        """
        # Save initial state
        initial_boids = [
            SwarmBoid(b.id, b.seat_name, b.triad_seat, b.x, b.y, b.vx, b.vy, b.heading, b.frequency_hz)
            for b in self.boids
        ]

        # 1. Run Open-Loop
        open_phis: List[float] = []
        for _ in range(steps):
            snap = self.step(human_attractor=None, human_heading=None)
            open_phis.append(snap.order_parameter_phi)

        # 2. Reset and Run Closed-Loop
        self.boids = [
            SwarmBoid(b.id, b.seat_name, b.triad_seat, b.x, b.y, b.vx, b.vy, b.heading, b.frequency_hz)
            for b in initial_boids
        ]
        self.step_count = 0
        closed_phis: List[float] = []
        target = (self.arena_size / 2.0, self.arena_size / 2.0)

        for s in range(steps):
            if s >= human_trigger_step:
                snap = self.step(human_attractor=target, human_heading=math.pi / 4.0, human_torque=0.85)
            else:
                snap = self.step(human_attractor=None, human_heading=None)
            closed_phis.append(snap.order_parameter_phi)

        return open_phis, closed_phis
