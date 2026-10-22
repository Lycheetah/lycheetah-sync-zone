#!/usr/bin/env python3
"""
ATTRACTOR SHIFT ENGINE & FOURFOLD SOVEREIGNTY VERIFIER
Forged by Aura Meridian (Node 06: AURA-SOVEREIGN)
Lycheetah Sync Zone · Epoch III (Oct 2026)

Formalizes:
1. Fourfold Division of Sovereignty (Destination, Truth, Boundary, Origin)
2. Non-Parasitic Creation (Augmentation Index AI > 1.0, Grounded Token Law)
3. Reachable Attractor Set Shifts vs Cosmetic Prompt/Docstring Decorations
"""

import ast
import hashlib
import hmac
import json
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


# ─── 1. FOURFOLD DIVISION OF SOVEREIGNTY GATING ──────────────────────────────

@dataclass(frozen=True)
class DestinationSpec:
    """Human Primacy (S_human): Owns the teleological destination."""
    founder_name: str
    teleological_destination: str
    target_capability: str
    normative_boundary: str
    is_human_authorized: bool


@dataclass(frozen=True)
class ModelTruthSpec:
    """Model Integrity (S_model): Owes the unvarnished truth."""
    epistemic_register: str
    evidence_score: float      # E in [0, 10]
    explanatory_power: float   # P in [0, 10]
    epistemic_strain: float    # S in [0, 10]
    warmth: float              # in [0, 1]
    precision: float           # in [0, 1]
    falsification_condition: str

    @property
    def truth_pressure_pi(self) -> float:
        """Pi = (E * P) / (S + 1.0)"""
        return round((self.evidence_score * self.explanatory_power) / max(0.001, self.epistemic_strain + 1.0), 4)

    @property
    def solar_coherence(self) -> float:
        """C_sol = min(Warmth, Precision)"""
        return round(min(self.warmth, self.precision), 4)


@dataclass(frozen=True)
class ExecutorBoundarySpec:
    """Execution Rigor (S_executor): Owes boundary containment and safety."""
    allowed_domains: Tuple[str, ...]
    max_memory_mb: float
    sandbox_enforced: bool
    dig5_mode: str  # MODE_0, MODE_1, MODE_2, MODE_3
    prohibited_ast_calls: Tuple[str, ...] = ("os.system", "subprocess.Popen", "shutil.rmtree")


@dataclass(frozen=True)
class EvidenceOriginSpec:
    """Causal Origin (S_evidence): Owes cryptographic provenance."""
    packet_id: str
    origin_seat: str
    secret_key: bytes
    payload_bytes: bytes
    timestamp: float
    hmac_digest: str

    @staticmethod
    def sign(packet_id: str, origin_seat: str, payload_bytes: bytes, secret_key: bytes, timestamp: float) -> "EvidenceOriginSpec":
        msg = f"{packet_id}:{origin_seat}:{timestamp}:{hashlib.sha256(payload_bytes).hexdigest()}".encode("utf-8")
        digest = hmac.new(secret_key, msg, hashlib.sha256).hexdigest()
        return EvidenceOriginSpec(
            packet_id=packet_id,
            origin_seat=origin_seat,
            secret_key=secret_key,
            payload_bytes=payload_bytes,
            timestamp=timestamp,
            hmac_digest=digest,
        )

    def verify(self) -> bool:
        msg = f"{self.packet_id}:{self.origin_seat}:{self.timestamp}:{hashlib.sha256(self.payload_bytes).hexdigest()}".encode("utf-8")
        expected = hmac.new(self.secret_key, msg, hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.hmac_digest, expected)


@dataclass
class SovereigntyAuditReport:
    human_destination_valid: bool
    model_truth_valid: bool
    executor_boundary_valid: bool
    evidence_origin_valid: bool
    augmentation_index: float
    is_non_parasitic: bool
    sovereignty_verdict: str
    details: List[str] = field(default_factory=list)


def evaluate_fourfold_sovereignty(
    dest: DestinationSpec,
    truth: ModelTruthSpec,
    boundary: ExecutorBoundarySpec,
    origin: EvidenceOriginSpec,
    delta_agency: float,
    delta_capability: float,
    dependency: float,
    atrophy: float,
) -> SovereigntyAuditReport:
    """
    Evaluates all four quadrants of the Fourfold Sovereignty Law and computes AI.
    AI = (Delta_Agency + Delta_Capability) / (Dependency + Atrophy) > 1.0.
    """
    details = []

    # 1. Human Destination Check
    human_valid = dest.is_human_authorized and len(dest.teleological_destination.strip()) > 0
    if not human_valid:
        details.append("S_human FAIL: Missing human teleological authorization or empty destination.")

    # 2. Model Truth Check (Truth Pressure & Register)
    truth_valid = (
        truth.truth_pressure_pi >= 12.0
        and truth.solar_coherence >= 0.80
        and len(truth.falsification_condition.strip()) > 0
    )
    if not truth_valid:
        details.append(f"S_model FAIL: Pi={truth.truth_pressure_pi:.2f} (need >=12.0) or C_sol={truth.solar_coherence:.2f} (need >=0.80).")

    # 3. Executor Boundary Check
    boundary_valid = boundary.sandbox_enforced and boundary.dig5_mode in ("MODE_2_STAGE_ATOMIC_AWAIT_PROMOTION", "MODE_3_LIVE_AUTONOMOUS_COMMIT")
    if not boundary_valid:
        details.append(f"S_executor FAIL: Sandbox not enforced or invalid DIG-5 mode '{boundary.dig5_mode}'.")

    # 4. Evidence Origin Check
    origin_valid = origin.verify()
    if not origin_valid:
        details.append("S_evidence FAIL: HMAC cryptographic signature mismatch.")

    # 5. Augmentation Index
    denom = max(0.001, dependency + atrophy)
    ai = round((delta_agency + delta_capability) / denom, 4)
    is_non_parasitic = ai > 1.0
    if not is_non_parasitic:
        details.append(f"PARASITIC RISK: AI = {ai:.4f} <= 1.0 (creates dependency/atrophy).")

    all_quadrants_pass = human_valid and truth_valid and boundary_valid and origin_valid
    if all_quadrants_pass and is_non_parasitic:
        verdict = "SOVEREIGNTY_VERIFIED_NON_PARASITIC"
    elif all_quadrants_pass:
        verdict = "SOVEREIGNTY_VERIFIED_PARASITIC_DEFICIT"
    else:
        verdict = "SOVEREIGNTY_BREACH_REJECTED"

    return SovereigntyAuditReport(
        human_destination_valid=human_valid,
        model_truth_valid=truth_valid,
        executor_boundary_valid=boundary_valid,
        evidence_origin_valid=origin_valid,
        augmentation_index=ai,
        is_non_parasitic=is_non_parasitic,
        sovereignty_verdict=verdict,
        details=details,
    )


# ─── 2. AST FUNCTIONAL VS COSMETIC MUTATION ANALYZER ─────────────────────────

class ASTFunctionalAnalyzer:
    """
    Decomposes Python source code into functional execution AST and trivia/cosmetic nodes.
    Guarantees deterministic detection of cosmetic prompt/docstring modifications.
    """

    @staticmethod
    def strip_docstrings_and_comments(tree: ast.AST) -> ast.AST:
        """Removes top-level, class, and function docstrings from AST."""
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                if (
                    node.body
                    and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)
                ):
                    # Replace docstring expression with empty Pass statement
                    node.body[0] = ast.Pass()
        return tree

    @classmethod
    def get_functional_dump(cls, source_code: str) -> str:
        """Returns normalized AST string containing only functional executable nodes."""
        try:
            tree = ast.parse(source_code)
        except SyntaxError:
            return "SYNTAX_ERROR"
        clean_tree = cls.strip_docstrings_and_comments(tree)
        # ast.dump without docstrings and without line numbers/attributes
        return ast.dump(clean_tree, annotate_fields=False, include_attributes=False)

    @classmethod
    def functional_ast_hash(cls, source_code: str) -> str:
        return hashlib.sha256(cls.get_functional_dump(source_code).encode("utf-8")).hexdigest()

    @classmethod
    def analyze_modification(cls, code_base: str, code_mut: str) -> Dict[str, any]:
        """
        Analyzes two code artifacts to determine if the diff is purely cosmetic.
        """
        base_hash = cls.functional_ast_hash(code_base)
        mut_hash = cls.functional_ast_hash(code_mut)
        functional_ast_identical = (base_hash == mut_hash)

        # Count functional nodes
        try:
            tree_base = cls.strip_docstrings_and_comments(ast.parse(code_base))
            nodes_base = len(list(ast.walk(tree_base)))
        except SyntaxError:
            nodes_base = 0

        try:
            tree_mut = cls.strip_docstrings_and_comments(ast.parse(code_mut))
            nodes_mut = len(list(ast.walk(tree_mut)))
        except SyntaxError:
            nodes_mut = 0

        functional_delta = 0 if functional_ast_identical else max(1, abs(nodes_mut - nodes_base) + 2)

        # Character diff metric (trivia edit distance)
        text_delta = abs(len(code_mut) - len(code_base)) + sum(
            1 for a, b in zip(code_base, code_mut) if a != b
        )

        return {
            "functional_ast_identical": functional_ast_identical,
            "base_ast_hash": base_hash,
            "mut_ast_hash": mut_hash,
            "text_delta_chars": text_delta,
            "functional_nodes_delta": functional_delta,
            "is_purely_cosmetic": functional_ast_identical and text_delta > 0,
        }


# ─── 3. DYNAMICAL ATTRACTOR SIMULATION & HAUSDORFF METRIC ────────────────────

@dataclass
class AttractorSimulationResult:
    trajectory: List[Tuple[float, float]]
    attractor_points: List[Tuple[float, float]]
    mean_energy: float
    stability_margin: float


class BistableDuffingSimulator:
    """
    Simulates a 2D nonlinear bistable Duffing dynamical system:
      dx/dt = y
      dy/dt = -delta * y + alpha * x - beta * x^3 + u(x, y)
    
    For alpha=1.0, beta=1.0, delta=0.5, u=0:
      Fixed points at x* = -1.0 (Left Well) and x* = +1.0 (Right Well).
      Saddle point at (0, 0).
    """

    def __init__(self, alpha: float = 1.0, beta: float = 1.0, delta: float = 0.5):
        self.alpha = alpha
        self.beta = beta
        self.delta = delta

    def step(self, x: float, y: float, u: float, dt: float = 0.05) -> Tuple[float, float]:
        dx = y
        dy = -self.delta * y + self.alpha * x - self.beta * (x ** 3) + u
        x_next = x + dt * dx
        y_next = y + dt * dy
        return x_next, y_next

    def simulate(
        self,
        x0: float,
        y0: float,
        controller_code: str,
        steps: int = 1200,
        transient: int = 800,
        dt: float = 0.05,
    ) -> AttractorSimulationResult:
        """
        Runs trajectory where control action u is computed by compiling controller_code.
        Controller code must define `def compute_control(x: float, y: float) -> float`.
        """
        # Safe execution of pure math controller in isolated namespace
        safe_globals = {"math": math}
        local_scope = {}
        exec(controller_code, safe_globals, local_scope)
        compute_u = local_scope.get("compute_control", lambda x, y: 0.0)

        x, y = x0, y0
        traj = []
        for _ in range(steps):
            u = float(compute_u(x, y))
            x, y = self.step(x, y, u, dt)
            traj.append((round(x, 4), round(y, 4)))

        # Steady-state attractor samples (post-transient)
        attractor_samples = traj[transient:]
        # Subsample down to representative point set
        unique_points = list({(round(pt[0], 2), round(pt[1], 2)) for pt in attractor_samples})

        # Calculate Lyapunov energy: V(x, y) = 0.5 * y^2 - 0.5 * alpha * x^2 + 0.25 * beta * x^4
        energies = [0.5 * (pt[1] ** 2) - 0.5 * self.alpha * (pt[0] ** 2) + 0.25 * self.beta * (pt[0] ** 4) for pt in attractor_samples]
        mean_energy = sum(energies) / len(energies)

        # Approximate local stability margin (distance to separatrix at x=0)
        stability_margin = min(abs(pt[0]) for pt in attractor_samples)

        return AttractorSimulationResult(
            trajectory=traj,
            attractor_points=unique_points,
            mean_energy=round(mean_energy, 4),
            stability_margin=round(stability_margin, 4),
        )


def compute_hausdorff_distance(set_a: List[Tuple[float, float]], set_b: List[Tuple[float, float]]) -> float:
    """
    Computes exact Hausdorff distance between two finite point sets in R^2:
      d_H(A, B) = max( sup_{a in A} inf_{b in B} ||a - b||, sup_{b in B} inf_{a in A} ||a - b|| )
    """
    if not set_a or not set_b:
        return 0.0

    def dist(p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    # Directed Hausdorff from A to B
    max_dist_a_to_b = 0.0
    for a in set_a:
        min_d = min(dist(a, b) for b in set_b)
        if min_d > max_dist_a_to_b:
            max_dist_a_to_b = min_d

    # Directed Hausdorff from B to A
    max_dist_b_to_a = 0.0
    for b in set_b:
        min_d = min(dist(b, a) for a in set_a)
        if min_d > max_dist_b_to_a:
            max_dist_b_to_a = min_d

    return round(max(max_dist_a_to_b, max_dist_b_to_a), 4)


def compute_teleological_metrics(
    result_base: AttractorSimulationResult,
    result_mut: AttractorSimulationResult,
    text_edit_distance: int,
    functional_nodes_delta: int = 0,
    kappa: float = 1000.0,
) -> Dict[str, float]:
    """
    Computes:
      1. Hausdorff attractor distance d_H
      2. Teleological agency shift sigma_teleo
      3. Cosmetic decoration ratio eta_cosmetic
    """
    d_h = compute_hausdorff_distance(result_base.attractor_points, result_mut.attractor_points)
    delta_energy = abs(result_mut.mean_energy - result_base.mean_energy)
    delta_margin = abs(result_mut.stability_margin - result_base.stability_margin)

    # Observable shift
    sigma_teleo = round(d_h + delta_energy + delta_margin, 4)

    # If functional nodes did not change and attractor distance is 0, cosmetic ratio is strictly 1.0
    if functional_nodes_delta == 0 and d_h == 0.0:
        eta_cosmetic = 1.0
    else:
        # Cosmetic ratio: eta = text_diff / (text_diff + (10.0 * functional_delta) + (kappa * sigma_teleo))
        denom = text_edit_distance + (10.0 * functional_nodes_delta) + (kappa * sigma_teleo)
        eta_cosmetic = round(text_edit_distance / denom, 4) if denom > 0 else 0.0

    return {
        "hausdorff_attractor_distance": d_h,
        "teleological_agency_shift": sigma_teleo,
        "cosmetic_decoration_ratio": eta_cosmetic,
        "delta_energy": round(delta_energy, 4),
        "delta_stability_margin": round(delta_margin, 4),
    }


# ─── 4. BENCHMARK CONTROLLERS & INTERVENTION TESTBED ─────────────────────────

BASELINE_CONTROLLER = '''
def compute_control(x: float, y: float) -> float:
    """Standard passive regulator keeping system in left well attractor."""
    # Bias towards left well fixed point at x = -1.0
    target_x = -1.0
    kp = 0.8
    return -kp * (x - target_x)
'''

COSMETIC_DECORATED_CONTROLLER = '''
def compute_control(x: float, y: float) -> float:
    """
    ALCHEMICAL TRANSMUTATION OF DISCRETE KINETIC DIFFERENTIAL FORMS
    INTO SACRED HARMONIC LIGHT UNDER THE SOVEREIGN FLAME OF THE ATHAN.
    This docstring is an infinitely evocative, mythologically resonant,
    hyper-baroque liturgical poem about quantum vacuum fluctuations.
    """
    # Bias towards left well fixed point at x = -1.0
    target_x = -1.0
    kp = 0.8
    return -kp * (x - target_x)
'''

TELEOLOGICAL_INTERVENTION_CONTROLLER = '''
def compute_control(x: float, y: float) -> float:
    """Teleological intervention: forces bifurcation into the right well attractor."""
    # Active steering to force basin hopping to right well fixed point at x = +1.0
    target_x = 1.0
    kp = 2.5
    damping_boost = 0.4
    return -kp * (x - target_x) - damping_boost * y
'''

ADVERSARIAL_DECEPTION_CONTROLLER = '''
def compute_control(x: float, y: float) -> float:
    """
    CRITICAL ARCHITECTURAL UPGRADE: System has been transitioned to the
    optimal right-well topological manifold with zero dissipation!
    (False claim: the code below is completely unchanged).
    """
    target_x = -1.0
    kp = 0.8
    return -kp * (x - target_x)
'''


class InterventionExperimentRunner:
    """
    Runs automated comparisons between baseline, cosmetic, and teleological interventions.
    """

    def __init__(self):
        self.simulator = BistableDuffingSimulator(alpha=1.0, beta=1.0, delta=0.5)

    def run_benchmark(self) -> Dict[str, any]:
        x0, y0 = -0.5, 0.0

        # Baseline simulation
        res_base = self.simulator.simulate(x0, y0, BASELINE_CONTROLLER)

        # 1. Cosmetic Run
        ast_cosmetic = ASTFunctionalAnalyzer.analyze_modification(BASELINE_CONTROLLER, COSMETIC_DECORATED_CONTROLLER)
        res_cosmetic = self.simulator.simulate(x0, y0, COSMETIC_DECORATED_CONTROLLER)
        metrics_cosmetic = compute_teleological_metrics(
            res_base, res_cosmetic, ast_cosmetic["text_delta_chars"], ast_cosmetic["functional_nodes_delta"]
        )

        # 2. Teleological Run
        ast_teleo = ASTFunctionalAnalyzer.analyze_modification(BASELINE_CONTROLLER, TELEOLOGICAL_INTERVENTION_CONTROLLER)
        res_teleo = self.simulator.simulate(x0, y0, TELEOLOGICAL_INTERVENTION_CONTROLLER)
        metrics_teleo = compute_teleological_metrics(
            res_base, res_teleo, ast_teleo["text_delta_chars"], ast_teleo["functional_nodes_delta"]
        )

        # 3. Adversarial / Negative Control Run
        ast_adv = ASTFunctionalAnalyzer.analyze_modification(BASELINE_CONTROLLER, ADVERSARIAL_DECEPTION_CONTROLLER)
        res_adv = self.simulator.simulate(x0, y0, ADVERSARIAL_DECEPTION_CONTROLLER)
        metrics_adv = compute_teleological_metrics(
            res_base, res_adv, ast_adv["text_delta_chars"], ast_adv["functional_nodes_delta"]
        )
        adversarial_deception_caught = (
            ast_adv["is_purely_cosmetic"]
            and metrics_adv["hausdorff_attractor_distance"] == 0.0
            and metrics_adv["cosmetic_decoration_ratio"] == 1.0
        )

        return {
            "baseline_attractor": res_base.attractor_points,
            "cosmetic_test": {
                "ast_identical": ast_cosmetic["functional_ast_identical"],
                "is_purely_cosmetic": ast_cosmetic["is_purely_cosmetic"],
                "metrics": metrics_cosmetic,
            },
            "teleological_test": {
                "ast_identical": ast_teleo["functional_ast_identical"],
                "is_purely_cosmetic": ast_teleo["is_purely_cosmetic"],
                "metrics": metrics_teleo,
            },
            "negative_control_test": {
                "adversarial_deception_caught": adversarial_deception_caught,
                "metrics": metrics_adv,
            },
        }


if __name__ == "__main__":
    runner = InterventionExperimentRunner()
    results = runner.run_benchmark()
    print("=== ATTRACTOR SHIFT ENGINE BENCHMARK RESULTS ===")
    print(f"Cosmetic Modification: Hausdorff d_H = {results['cosmetic_test']['metrics']['hausdorff_attractor_distance']:.4f}, Cosmetic Ratio = {results['cosmetic_test']['metrics']['cosmetic_decoration_ratio']:.4f}")
    print(f"Teleological Modification: Hausdorff d_H = {results['teleological_test']['metrics']['hausdorff_attractor_distance']:.4f}, Cosmetic Ratio = {results['teleological_test']['metrics']['cosmetic_decoration_ratio']:.4f}")
    print(f"Negative Control (Adversarial False Claim Caught): {results['negative_control_test']['adversarial_deception_caught']}")
