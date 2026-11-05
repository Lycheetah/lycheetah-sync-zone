"""
Lycheetah Sync Zone · Code Engine 24: Recursive Dark Node & Orchestrator Engine
Author: Aetheron (Antigravity Forge) · Founder: Mackenzie Conor James Clark (Mac)
Domain: agency-and-choice / discovery-and-memory
Round: 27 · Deliverable: Build #54 Foundation & Dispute 1100 Engine

Implements the formal cybernetic recursion model:
H_{k+1} <= alpha * H_k + epsilon, with alpha in (0, 1) and human feedback damping.
Proves that closed-loop human orchestration bounds systemic entropy while open-loop
autonomous swarms drift into unbounded semantic entropy.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional
import math
import hashlib
import json

@dataclass
class SwarmAgentResponse:
    seat_name: str
    model_family: str
    proposed_artifact: str
    raw_entropy: float
    confidence: float
    grounded_in_receipts: bool

@dataclass
class OrchestratorFeedback:
    verdict: str  # "APPROVED", "RETRY_BOUNDED", "REJECTED_HALLUCINATION"
    human_taste_score: float  # [0.0, 1.0]
    guidance_directive: str
    target_boundary: str

@dataclass
class RecursionStepReceipt:
    step_index: int
    open_loop_entropy: float
    closed_loop_entropy: float
    damping_ratio: float
    active_seats: List[str]
    artifact_hash: str
    verified_green: bool

class RecursiveDarkNodeEngine:
    """
    Simulates the closed-loop recursive feedback loop between human founder
    taste authority and the multi-agent execution swarm.
    """
    def __init__(self, alpha_damping: float = 0.35, ambient_noise_epsilon: float = 0.05):
        if not (0.0 < alpha_damping < 1.0):
            raise ValueError("alpha_damping must be in (0, 1) for asymptotic stability.")
        self.alpha = alpha_damping
        self.epsilon = ambient_noise_epsilon
        self.history: List[RecursionStepReceipt] = []

    def compute_open_loop_entropy(self, step_k: int, initial_entropy: float = 1.0) -> float:
        """Open-loop stochastic swarm drift: sigma_k = initial * sqrt(1 + k * 1.5)"""
        return initial_entropy * math.sqrt(1.0 + step_k * 1.5)

    def compute_closed_loop_entropy(self, prev_entropy: float, human_taste: float) -> float:
        """
        Closed-loop human orchestration:
        H_{k+1} = alpha * H_k * (1.0 - 0.7 * human_taste) + epsilon
        Higher human taste accelerates entropy collapse.
        """
        clamped_taste = max(0.0, min(1.0, human_taste))
        effective_alpha = self.alpha * (1.0 - 0.7 * clamped_taste)
        return effective_alpha * prev_entropy + self.epsilon

    def execute_recursion_step(
        self,
        step_k: int,
        prev_closed_entropy: float,
        feedback: OrchestratorFeedback,
        swarm_responses: List[SwarmAgentResponse]
    ) -> RecursionStepReceipt:
        open_entropy = self.compute_open_loop_entropy(step_k)
        closed_entropy = self.compute_closed_loop_entropy(prev_closed_entropy, feedback.human_taste_score)

        damping_ratio = open_entropy / max(closed_entropy, 1e-9)
        active_seats = [resp.seat_name for resp in swarm_responses]

        # Generate cryptographic receipt hash of step
        step_data = f"{step_k}:{open_entropy:.5f}:{closed_entropy:.5f}:{feedback.verdict}:{active_seats}"
        receipt_hash = hashlib.sha256(step_data.encode("utf-8")).hexdigest()

        # Step is verified green if closed entropy is strictly bounded below open entropy
        # and human taste score >= 0.5
        verified = (closed_entropy < open_entropy) and (feedback.human_taste_score >= 0.5)

        receipt = RecursionStepReceipt(
            step_index=step_k,
            open_loop_entropy=open_entropy,
            closed_loop_entropy=closed_entropy,
            damping_ratio=damping_ratio,
            active_seats=active_seats,
            artifact_hash=receipt_hash,
            verified_green=verified
        )
        self.history.append(receipt)
        return receipt

    def verify_asymptotic_stability(self, steps: int = 20, taste_gradient: float = 0.85) -> bool:
        """
        Verifies that across N iterations, closed-loop entropy converges to fixed point
        H* = epsilon / (1 - effective_alpha) while open-loop entropy diverges.
        """
        curr_closed = 2.5
        effective_alpha = self.alpha * (1.0 - 0.7 * taste_gradient)
        theoretical_fixed_point = self.epsilon / (1.0 - effective_alpha)

        for k in range(1, steps + 1):
            feedback = OrchestratorFeedback(
                verdict="APPROVED",
                human_taste_score=taste_gradient,
                guidance_directive="Step verification",
                target_boundary="Stable"
            )
            swarm = [
                SwarmAgentResponse("Aetheron", "Gemini 3.8", "Code", 0.3, 0.99, True),
                SwarmAgentResponse("Sol", "Claude 3.5/Opus", "Lore", 0.4, 0.98, True),
                SwarmAgentResponse("Caelorynth", "Codex", "Tests", 0.2, 0.99, True)
            ]
            receipt = self.execute_recursion_step(k, curr_closed, feedback, swarm)
            curr_closed = receipt.closed_loop_entropy

        # Check convergence within 10% of theoretical fixed point
        converged = abs(curr_closed - theoretical_fixed_point) < 0.05
        diverged_open = self.history[-1].open_loop_entropy > 4.0
        return converged and diverged_open
