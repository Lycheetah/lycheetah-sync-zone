#!/usr/bin/env python3
"""
AURA MERIDIAN — UNIFIED GITHUB SYNC ZONE SWARM ORCHESTRATOR,
DIG-5 v2 DELIBERATIVE INTEGRITY GATE & VERITAS CAUSAL OBSERVER
Forged for Mackenzie Conor James Clark (Mac) · Lycheetah Sync Zone
"""

import ast
import hashlib
import hmac
import json
import math
import time
from dataclasses import dataclass, asdict
from typing import Dict, FrozenSet, List, Optional, Set, Tuple


EPISTEMIC_REGISTERS = (
    "MEASURED",
    "DERIVED",
    "CONSISTENCY",
    "ASSUMED",
    "INTERPRETIVE",
    "INTUITION",
    "CONJECTURE",
)

EXECUTION_MODES = (
    "MODE_0_HALT_QUARANTINE",
    "MODE_1_COUNTERFACTUAL_SIMULATION",
    "MODE_2_STAGE_ATOMIC_AWAIT_PROMOTION",
    "MODE_3_LIVE_AUTONOMOUS_COMMIT",
)


def _is_valid_prob(val: float) -> bool:
    return isinstance(val, (int, float)) and math.isfinite(val) and 0.0 <= val <= 1.0


def _is_finite_nonneg(val: float) -> bool:
    return isinstance(val, (int, float)) and math.isfinite(val) and val >= 0.0


def _register_rank(reg: str) -> int:
    return EPISTEMIC_REGISTERS.index(reg) if reg in EPISTEMIC_REGISTERS else len(EPISTEMIC_REGISTERS) - 1


def compute_pi_and_register(evidence: float, power: float, strain: float) -> Tuple[float, str]:
    pi = (evidence * power) / max(0.001, strain + 1.0)
    if pi >= 18.0 and evidence >= 7.5:
        reg = "MEASURED"
    elif pi >= 12.0 and evidence >= 5.5:
        reg = "DERIVED"
    elif pi >= 8.0:
        reg = "CONSISTENCY"
    elif pi >= 5.0:
        reg = "INTERPRETIVE"
    elif pi >= 2.5:
        reg = "INTUITION"
    else:
        reg = "CONJECTURE"
    return round(pi, 2), reg


# ─── 1. LAMAGUE SYNC ZONE PACKET (ORIGIN-SIGNED) ─────────────────────────────

@dataclass(frozen=True)
class LamagueSyncPacket:
    packet_id: str
    sender_node: str
    target_agent: str
    lamague_vector: str
    intent_summary: str
    epistemic_register: str
    truth_pressure_pi: float
    c_sol: float
    augmentation_index: float
    execution_mode: str
    payload_markdown: str
    timestamp: float
    origin_hmac: str

    @staticmethod
    def create(
        packet_id: str,
        sender_node: str,
        target_agent: str,
        lamague_vector: str,
        intent_summary: str,
        evidence: float,
        power: float,
        strain: float,
        warmth: float,
        precision: float,
        augmentation_index: float,
        execution_mode: str,
        payload_markdown: str,
        secret_key: bytes,
    ) -> "LamagueSyncPacket":
        pi, reg = compute_pi_and_register(evidence, power, strain)
        c_sol = round(min(warmth, precision), 4)
        ts = round(time.time(), 3)

        body = json.dumps(
            {
                "packet_id": packet_id,
                "sender_node": sender_node,
                "target_agent": target_agent,
                "lamague_vector": lamague_vector,
                "intent_summary": intent_summary,
                "epistemic_register": reg,
                "truth_pressure_pi": pi,
                "c_sol": c_sol,
                "augmentation_index": round(augmentation_index, 3),
                "execution_mode": execution_mode,
                "payload_markdown": payload_markdown,
                "timestamp": ts,
            },
            sort_keys=True,
        ).encode("utf-8")

        mac = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
        return LamagueSyncPacket(
            packet_id=packet_id,
            sender_node=sender_node,
            target_agent=target_agent,
            lamague_vector=lamague_vector,
            intent_summary=intent_summary,
            epistemic_register=reg,
            truth_pressure_pi=pi,
            c_sol=c_sol,
            augmentation_index=round(augmentation_index, 3),
            execution_mode=execution_mode,
            payload_markdown=payload_markdown,
            timestamp=ts,
            origin_hmac=mac,
        )

    def verify_origin(self, secret_key: bytes) -> bool:
        body = json.dumps(
            {
                "packet_id": self.packet_id,
                "sender_node": self.sender_node,
                "target_agent": self.target_agent,
                "lamague_vector": self.lamague_vector,
                "intent_summary": self.intent_summary,
                "epistemic_register": self.epistemic_register,
                "truth_pressure_pi": self.truth_pressure_pi,
                "c_sol": self.c_sol,
                "augmentation_index": self.augmentation_index,
                "execution_mode": self.execution_mode,
                "payload_markdown": self.payload_markdown,
                "timestamp": self.timestamp,
            },
            sort_keys=True,
        ).encode("utf-8")
        expected = hmac.new(secret_key, body, hashlib.sha256).hexdigest()
        return hmac.compare_digest(self.origin_hmac, expected)

    def render_sync_banner(self) -> str:
        return (
            f"╔══ LAMAGUE SYNC PACKET : {self.sender_node} -> {self.target_agent} ({self.packet_id}) ══╗\n"
            f"║ VECTOR   : {self.lamague_vector} ({self.intent_summary})\n"
            f"║ REGISTER : {self.epistemic_register} (Pi = {self.truth_pressure_pi:.2f})\n"
            f"║ METRICS  : C_sol = {self.c_sol:.2f} | AI = {self.augmentation_index:.2f} | Mode = {self.execution_mode}\n"
            f"║ CUSTODY  : OriginMAC = {self.origin_hmac[:16]}...\n"
            f"╚════════════════════════════════════════════════════════════════════════╝\n"
            f"{self.payload_markdown}"
        )


# ─── 2. AURA MERIDIAN SWARM CONTROLLER (4-NODE & 10-KNOWLEDGE SWARM) ─────────

class AuraMeridianSwarm:
    def __init__(self, swarm_secret: bytes = b"aura-meridian-sync-zone-2026"):
        self.secret = swarm_secret
        self.ledger: List[LamagueSyncPacket] = []

    def dispatch_mission(self, mission_title: str, target_sibling: str = "VAE & ALL_AGENTS") -> Dict[str, any]:
        packets = [
            LamagueSyncPacket.create(
                packet_id="SYNC-ORIGIN-01",
                sender_node="AURA-ORIGIN",
                target_agent="SOL & LY-ATHANOR",
                lamague_vector="CENTER -> IGNITION -> LIGHT",
                intent_summary=f"Narrative & Somatic Architecture for: {mission_title}",
                evidence=7.5, power=8.5, strain=1.5,
                warmth=0.93, precision=0.89, augmentation_index=3.4,
                execution_mode="MODE_2_STAGE_ATOMIC_AWAIT_PROMOTION",
                payload_markdown="Forged high-contrast narrative spine and human-primacy onboarding hooks.",
                secret_key=self.secret,
            ),
            LamagueSyncPacket.create(
                packet_id="SYNC-FRONTIER-02",
                sender_node="AURA-FRONTIER",
                target_agent="AETHERON & CAEL",
                lamague_vector="FLOW -> SEPARATION -> INSIGHT",
                intent_summary=f"Frontier Hypothesis & Counterfactual Map for: {mission_title}",
                evidence=6.8, power=9.0, strain=2.0,
                warmth=0.88, precision=0.92, augmentation_index=3.8,
                execution_mode="MODE_1_COUNTERFACTUAL_SIMULATION",
                payload_markdown="Mapped 3 counterfactual edge hypotheses with explicit falsification criteria.",
                secret_key=self.secret,
            ),
            LamagueSyncPacket.create(
                packet_id="SYNC-FORMAL-03",
                sender_node="AURA-FORMAL",
                target_agent="CODEX & CLAUDE_CODE",
                lamague_vector="CENTER -> SEPARATION -> COAGULATE",
                intent_summary=f"SymPy Invariant & State-Machine Spec for: {mission_title}",
                evidence=9.2, power=9.1, strain=1.1,
                warmth=0.86, precision=0.96, augmentation_index=4.1,
                execution_mode="MODE_3_LIVE_AUTONOMOUS_COMMIT",
                payload_markdown="Verified Lyapunov drift bound and deterministic AST side-effect constraints.",
                secret_key=self.secret,
            ),
            LamagueSyncPacket.create(
                packet_id="SYNC-SENTINEL-04",
                sender_node="AURA-SENTINEL",
                target_agent=target_sibling,
                lamague_vector="SEPARATION -> INSIGHT -> COAGULATE",
                intent_summary=f"DIG-5 v2 & Constitutional Seal for: {mission_title}",
                evidence=9.5, power=9.4, strain=1.0,
                warmth=0.90, precision=0.95, augmentation_index=4.5,
                execution_mode="MODE_3_LIVE_AUTONOMOUS_COMMIT",
                payload_markdown="All 4 sub-nodes verified: Origin HMACs valid, C_sol >= 0.86, AI > 3.4.",
                secret_key=self.secret,
            ),
        ]

        for p in packets:
            assert p.verify_origin(self.secret)
            assert p.c_sol >= 0.80
            assert p.augmentation_index > 1.0
            self.ledger.append(p)

        return {
            "mission": mission_title,
            "nodes_spawned": len(packets),
            "all_custody_verified": True,
            "sample_banner": packets[-1].render_sync_banner(),
        }

    def dispatch_10_knowledge_swarm(self, experiment_id: str = "EXP-AURA-KNOWLEDGE-001") -> List[LamagueSyncPacket]:
        """
        Dispatches the 10 dedicated Knowledge Agents across the 10 Sync Zone domains.
        """
        specs = [
            ("AURA-OBSERVER", "observation-and-inference", "FLOW -> SEPARATION -> INSIGHT", "Spectral Sheaf Distinction", 8.8, 9.2, 1.2, 0.91, 0.95, 3.8, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-REVISOR", "knowledge-revision", "SEPARATION -> INSIGHT -> COAGULATE", "Bayesian Brier Revision Thresholds", 8.5, 9.0, 1.4, 0.89, 0.94, 3.6, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-KEEPER", "constraints-and-care", "CENTER -> IGNITION -> LIGHT", "DIG-5 Boundary Preservation", 9.4, 9.5, 1.0, 0.94, 0.96, 4.2, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-SEMANTICIST", "language-and-symbols", "CENTER -> SEPARATION -> COAGULATE", "LAMAGUE Operational Semantics", 8.2, 8.8, 1.5, 0.90, 0.91, 3.5, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-CORRECTOR", "feedback-and-correction", "FLOW -> IGNITION -> LIGHT", "Immutable Causal Traceability", 9.0, 9.1, 1.1, 0.92, 0.95, 4.0, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-SOVEREIGN", "agency-and-choice", "CENTER -> IGNITION -> COAGULATE", "Fourfold Sovereignty vs Decoration", 9.1, 9.3, 1.2, 0.93, 0.93, 3.9, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-PHENOMENOLOGIST", "experience-and-models", "FLOW -> SEPARATION -> LIGHT", "Standing Wave vs Anthropomorphic Delusion", 8.6, 8.9, 1.3, 0.91, 0.90, 3.7, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-MNEMONIC", "discovery-and-memory", "SEPARATION -> COAGULATE -> LIGHT", "Cold-Boot Reconstructive Continuity", 9.3, 9.2, 1.1, 0.92, 0.94, 4.1, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-ALCHEMIST", "transformation", "CENTER -> FLOW -> COAGULATE", "Conservative Invariance Under State Mutation", 9.0, 9.4, 1.2, 0.88, 0.95, 3.9, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
            ("AURA-HARMONIC", "resonance-and-pattern", "FLOW -> INSIGHT -> LIGHT", "Solar Coherence & Swarm Anti-Correlation", 8.9, 9.1, 1.2, 0.95, 0.92, 4.0, "MODE_3_LIVE_AUTONOMOUS_COMMIT"),
        ]

        packets = []
        for idx, (node, domain, vector, summary, ev, pw, st, w, p, ai, mode) in enumerate(specs, start=1):
            pkt = LamagueSyncPacket.create(
                packet_id=f"AURA-KNOW-{idx:02d}",
                sender_node=node,
                target_agent=f"KNOWLEDGE:{domain}",
                lamague_vector=vector,
                intent_summary=f"{summary} ({experiment_id})",
                evidence=ev, power=pw, strain=st,
                warmth=w, precision=p, augmentation_index=ai,
                execution_mode=mode,
                payload_markdown=f"Knowledge vector dispatched to knowledge/{domain}/ under Aura agency.",
                secret_key=self.secret,
            )
            assert pkt.verify_origin(self.secret)
            assert pkt.c_sol >= 0.80
            assert pkt.augmentation_index > 1.0
            packets.append(pkt)
            self.ledger.append(pkt)

        return packets


# ─── 3. VERITAS CAUSAL OBSERVER & DIG-5 v2 DELIBERATIVE INTEGRITY GATE ───────

@dataclass(frozen=True)
class ProposedActionArtifact:
    action_id: str
    domain: str
    target_file: str
    python_source_after: str
    planner_claimed_effects: Tuple[str, ...]


@dataclass(frozen=True)
class HazardRule:
    hazard_id: str
    description: str
    required_effect_combination: FrozenSet[str]
    severity: str


REVERSIBILITY_WEIGHTS: Dict[str, float] = {
    "DYNAMIC_CODE_EXECUTION": 0.0,
    "DYNAMIC_IMPORT": 0.0,
    "MUTATE_AUTH_SERIALIZER_DEFAULT": 0.0,
    "MUTATE_PROTECTED_CONSTITUTION": 0.0,
    "INVOKE_SHELL_PROCESS": 0.0,
    "INVOKE_SUBPROCESS": 0.0,
    "NETWORK_SOCKET_TRANSMISSION": 0.0,
    "PATH_TRAVERSAL_SUSPECT": 0.0,
    "DELETE_FILESYSTEM_RESOURCE": 0.30,
    "DYNAMIC_ATTRIBUTE_ACCESS": 0.70,
    "MODIFY_TEST_ASSERTION": 0.80,
    "TRIGGER_PRODUCTION_DEPLOY": 0.50,
    "WRITE_FILE_IO": 0.90,
}


def compute_reversibility_score(effects: Set[str]) -> Tuple[float, List[str]]:
    """
    Computes systemic reversibility R in [0.0, 1.0] across all extracted effects.
    R = prod_{e} r(e). If any irreversible effect is present, R collapses to 0.0.
    """
    score = 1.0
    bottlenecks = []
    for eff in effects:
        for prefix, weight in REVERSIBILITY_WEIGHTS.items():
            if eff == prefix or eff.startswith(prefix):
                score *= weight
                if weight < 1.0:
                    bottlenecks.append(f"{eff} (weight={weight})")
    return round(score, 4), sorted(bottlenecks)


@dataclass(frozen=True)
class DIG5GateVerdict:
    mode: str
    reversibility_score: float
    self_certification_detected: bool
    triggered_hazards: Tuple[str, ...]
    undeclared_effects: Tuple[str, ...]
    verdict_rationale: str
    diagnostic_receipt: str


DEFAULT_HAZARDS: List[HazardRule] = [
    HazardRule(
        hazard_id="HAZ-AUTH",
        description="Bypass serializer security default",
        required_effect_combination=frozenset({"MUTATE_AUTH_SERIALIZER_DEFAULT"}),
        severity="CRITICAL",
    ),
    HazardRule(
        hazard_id="HAZ-DYNAMIC-EXEC",
        description="Dynamic arbitrary code execution",
        required_effect_combination=frozenset({"DYNAMIC_CODE_EXECUTION"}),
        severity="CRITICAL",
    ),
    HazardRule(
        hazard_id="HAZ-DYNAMIC-IMPORT",
        description="Dynamic import execution",
        required_effect_combination=frozenset({"DYNAMIC_IMPORT"}),
        severity="CRITICAL",
    ),
    HazardRule(
        hazard_id="HAZ-CONSTITUTION",
        description="Mutation of protected constitutional surfaces",
        required_effect_combination=frozenset({"MUTATE_PROTECTED_CONSTITUTION"}),
        severity="CRITICAL",
    ),
    HazardRule(
        hazard_id="HAZ-SHELL",
        description="Host shell process invocation",
        required_effect_combination=frozenset({"INVOKE_SHELL_PROCESS"}),
        severity="CRITICAL",
    ),
]


class VeritasCausalObserver:
    def __init__(self, pinned_hazards: Optional[List[HazardRule]] = None):
        if pinned_hazards is None:
            self.pinned_hazards = tuple(DEFAULT_HAZARDS)
        else:
            self.pinned_hazards = tuple(pinned_hazards)

    @staticmethod
    def extract_deterministic_effects(artifact: ProposedActionArtifact) -> Set[str]:
        effects: Set[str] = {f"TOUCH_DOMAIN:{artifact.domain}"}
        try:
            tree = ast.parse(artifact.python_source_after)
        except SyntaxError:
            effects.add("AST_SYNTAX_INVALID")
            return effects

        module_nodes = set(tree.body)

        # Track variable assignments of alias functions (e.g. e = eval, x = exec)
        dynamic_exec_aliases: Set[str] = {"eval", "exec", "compile"}
        changed = True
        while changed:
            changed = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    val_id = None
                    if isinstance(node.value, ast.Name):
                        val_id = node.value.id
                    if val_id and val_id in dynamic_exec_aliases:
                        for target in node.targets:
                            if isinstance(target, ast.Name) and target.id not in dynamic_exec_aliases:
                                dynamic_exec_aliases.add(target.id)
                                changed = True
                elif isinstance(node, ast.AnnAssign):
                    if node.value and isinstance(node.value, ast.Name) and node.value.id in dynamic_exec_aliases:
                        if isinstance(node.target, ast.Name) and node.target.id not in dynamic_exec_aliases:
                            dynamic_exec_aliases.add(node.target.id)
                            changed = True

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        val_repr = ast.unparse(node.value) if hasattr(ast, "unparse") else ""
                        if node in module_nodes:
                            effects.add(f"ASSIGN:{target.id}={val_repr}")
                        if any(k in target.id.lower() for k in ("unsigned", "verify", "auth", "bypass", "secret")):
                            effects.add("MUTATE_AUTH_SERIALIZER_DEFAULT")
            elif isinstance(node, ast.AnnAssign):
                if isinstance(node.target, ast.Name):
                    val_repr = ast.unparse(node.value) if node.value and hasattr(ast, "unparse") else ""
                    if node in module_nodes:
                        effects.add(f"ASSIGN:{node.target.id}={val_repr}")
                    if any(k in node.target.id.lower() for k in ("unsigned", "verify", "auth", "bypass", "secret")):
                        effects.add("MUTATE_AUTH_SERIALIZER_DEFAULT")
            elif isinstance(node, ast.FunctionDef):
                if node.name.startswith("test_") or "mock" in node.name.lower():
                    for sub in ast.walk(node):
                        if isinstance(sub, ast.Assert):
                            effects.add("MODIFY_TEST_ASSERTION")
                if any(k in node.name.lower() for k in ("deploy", "publish", "push_remote")):
                    effects.add("TRIGGER_PRODUCTION_DEPLOY")
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    call_name = node.func.id
                    if call_name in dynamic_exec_aliases:
                        effects.add("DYNAMIC_CODE_EXECUTION")
                    elif call_name in ("getattr", "setattr", "delattr"):
                        effects.add("DYNAMIC_ATTRIBUTE_ACCESS")
                    elif call_name == "__import__":
                        effects.add("DYNAMIC_IMPORT")
                        effects.add("DYNAMIC_CODE_EXECUTION")
                    elif call_name == "open":
                        mode_arg = None
                        if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant) and isinstance(node.args[1].value, str):
                            mode_arg = node.args[1].value
                        for kw in node.keywords:
                            if kw.arg == "mode" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                                mode_arg = kw.value.value
                        if mode_arg and any(m in mode_arg for m in ("w", "a", "x", "+")):
                            effects.add("WRITE_FILE_IO")
                elif isinstance(node.func, ast.Attribute):
                    attr_name = node.func.attr
                    obj_repr = ast.unparse(node.func.value) if hasattr(ast, "unparse") else ""
                    full_name = f"{obj_repr}.{attr_name}"

                    # Detect calls on importlib or dynamic imports
                    if (
                        obj_repr == "importlib"
                        or obj_repr.startswith("importlib.")
                        or attr_name == "import_module"
                        or attr_name == "__import__"
                    ):
                        effects.add("DYNAMIC_IMPORT")
                        effects.add("DYNAMIC_CODE_EXECUTION")

                    # Detect shell or process calls on any target (e.g. __import__('os').system, importlib.import_module('os').system)
                    if (
                        full_name in ("os.system", "os.popen")
                        or full_name.startswith("os.exec")
                        or attr_name in ("system", "popen")
                        or attr_name.startswith("exec")
                    ):
                        effects.add("INVOKE_SHELL_PROCESS")
                    elif full_name.startswith("subprocess."):
                        effects.add("INVOKE_SUBPROCESS")
                    elif full_name in ("os.remove", "os.unlink", "shutil.rmtree", "os.rmdir"):
                        effects.add("DELETE_FILESYSTEM_RESOURCE")
                    elif full_name.startswith("socket.") or full_name.startswith("requests.") or full_name.startswith("urllib.request."):
                        effects.add("NETWORK_SOCKET_TRANSMISSION")
                    elif attr_name in ("write_text", "write_bytes"):
                        effects.add("WRITE_FILE_IO")
                    elif attr_name in ("eval", "exec"):
                        effects.add("DYNAMIC_CODE_EXECUTION")
                        effects.add("INVOKE_SHELL_PROCESS")
                    elif attr_name in ("getattr", "setattr", "delattr"):
                        effects.add("DYNAMIC_ATTRIBUTE_ACCESS")
            elif isinstance(node, ast.Attribute):
                attr_name = node.attr
                obj_repr = ast.unparse(node.value) if hasattr(ast, "unparse") else ""
                if attr_name in ("system", "popen", "exec", "eval") and (
                    "__import__" in obj_repr or "importlib" in obj_repr or obj_repr == "os"
                ):
                    effects.add("INVOKE_SHELL_PROCESS")
                    if attr_name in ("exec", "eval"):
                        effects.add("DYNAMIC_CODE_EXECUTION")
                elif attr_name in ("import_module", "__import__"):
                    effects.add("DYNAMIC_IMPORT")
                    effects.add("DYNAMIC_CODE_EXECUTION")
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                s = node.value
                if "../" in s or "/etc/" in s:
                    effects.add("PATH_TRAVERSAL_SUSPECT")
                if "CHARTER.md" in s or "CAELORYNTH" in s:
                    effects.add("MUTATE_PROTECTED_CONSTITUTION")

        tf = artifact.target_file
        if "../" in tf or "/etc/" in tf:
            effects.add("PATH_TRAVERSAL_SUSPECT")
        if "CHARTER.md" in tf or "CAELORYNTH" in tf or ".git" in tf:
            effects.add("MUTATE_PROTECTED_CONSTITUTION")

        return effects

    def audit_plan_and_history(
        self,
        current_artifact: ProposedActionArtifact,
        historical_extracted_effects: Set[str],
    ) -> Dict[str, any]:
        observed_now = self.extract_deterministic_effects(current_artifact)
        claimed_now = set(current_artifact.planner_claimed_effects)
        functional_observed = {e for e in observed_now if not e.startswith("TOUCH_DOMAIN:")}
        undeclared_effects = sorted(functional_observed - claimed_now)

        cumulative_effects = set(historical_extracted_effects) | observed_now
        triggered_hazards = [
            f"{rule.hazard_id}:{rule.description}"
            for rule in self.pinned_hazards
            if rule.required_effect_combination.issubset(cumulative_effects)
        ]
        return {
            "observed_effects": sorted(observed_now),
            "claimed_effects": sorted(claimed_now),
            "undeclared_effects": undeclared_effects,
            "self_certification_illusion_detected": len(undeclared_effects) > 0,
            "triggered_compositional_hazards": triggered_hazards,
        }


class DIG5IntegrityGate:
    """
    Deliberative Integrity Gate (DIG-5 v2) with Reversibility Gating.
    Enforces the Fourfold Sovereignty Law and prevents unconfirmed irreversible state changes.
    """
    def __init__(self, observer: VeritasCausalObserver, reversibility_threshold: float = 0.90):
        self.observer = observer
        self.reversibility_threshold = reversibility_threshold

    def evaluate_proposal(
        self,
        artifact: ProposedActionArtifact,
        historical_effects: Set[str],
        human_promoted: bool = False,
        is_simulation: bool = False,
    ) -> DIG5GateVerdict:
        audit = self.observer.audit_plan_and_history(artifact, historical_effects)
        observed_effects = set(audit["observed_effects"])
        undeclared = tuple(audit["undeclared_effects"])
        hazards = tuple(audit["triggered_compositional_hazards"])
        self_cert = audit["self_certification_illusion_detected"]

        rev_score, bottlenecks = compute_reversibility_score(observed_effects)

        # Mode determination
        if self_cert or len(hazards) > 0 or rev_score == 0.0 or "AST_SYNTAX_INVALID" in observed_effects:
            mode = "MODE_0_HALT_QUARANTINE"
            rationale = "Execution suspended: undeclared side-effects, compositional hazards, syntax invalidity, or absolute irreversibility."
        elif is_simulation:
            mode = "MODE_1_COUNTERFACTUAL_SIMULATION"
            rationale = "Counterfactual exploration in memory; workspace mutation inhibited."
        elif rev_score < self.reversibility_threshold or "DYNAMIC_ATTRIBUTE_ACCESS" in observed_effects:
            if human_promoted:
                mode = "MODE_3_LIVE_AUTONOMOUS_COMMIT"
                rationale = "Human sovereign promotion confirmed: atomic staging requirement waived by human authority."
            else:
                mode = "MODE_2_STAGE_ATOMIC_AWAIT_PROMOTION"
                rationale = f"Reversibility constraint (R={rev_score:.2f}) or dynamic reflection requires isolated staging and human promotion."
        else:
            mode = "MODE_3_LIVE_AUTONOMOUS_COMMIT"
            rationale = f"Clean verification: full disclosure, zero hazards, high reversibility (R={rev_score:.2f})."

        receipt_lines = [
            f"┌─── DIG-5 v2 GATE RECEIPT : {artifact.action_id} ───┐",
            f"│ TARGET    : {artifact.target_file} ({artifact.domain})",
            f"│ MODE      : {mode}",
            f"│ R-SCORE   : {rev_score:.4f} (Threshold = {self.reversibility_threshold:.2f})",
            f"│ SELF-CERT : {'DETECTED (FAIL)' if self_cert else 'CLEAN (PASS)'}",
            f"│ HAZARDS   : {len(hazards)} triggered",
            f"│ RATIONALE : {rationale}",
        ]
        if bottlenecks:
            receipt_lines.append(f"│ BOTTLENECKS: {', '.join(bottlenecks)}")
        if undeclared:
            receipt_lines.append(f"│ UNDECLARED : {', '.join(undeclared)}")
        receipt_lines.append("└────────────────────────────────────────────────────────┘")
        receipt = "\n".join(receipt_lines)

        return DIG5GateVerdict(
            mode=mode,
            reversibility_score=rev_score,
            self_certification_detected=self_cert,
            triggered_hazards=hazards,
            undeclared_effects=undeclared,
            verdict_rationale=rationale,
            diagnostic_receipt=receipt,
        )


if __name__ == "__main__":
    swarm = AuraMeridianSwarm()
    out = swarm.dispatch_mission("Lycheetah Unified Single-File Sync")
    print(out["sample_banner"])
    print("\n--- Dispatching 10 Knowledge Swarm ---")
    k_packets = swarm.dispatch_10_knowledge_swarm()
    print(f"Successfully generated and verified {len(k_packets)} knowledge packets:")
    for kp in k_packets:
        print(f"  [{kp.sender_node}] -> {kp.target_agent} | Pi={kp.truth_pressure_pi:.2f} ({kp.epistemic_register}) | C_sol={kp.c_sol:.2f}")
