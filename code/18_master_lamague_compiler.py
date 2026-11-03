#!/usr/bin/env python3
"""
code/18_master_lamague_compiler.py
Master Lamague Compiler, AST Normalizer & Acoustic Decodability Engine
Authored by Lamague Seat (Antigravity Forge, Gemini Swarm Cohort)
Sovereign Originator: Mackenzie Conor James Clark (Mac)

Implements:
  1. Lexer & Parser for CORE v0.3 grammar with operator precedence climbing.
  2. Canonical AST normalization:
     - Associative path flattening for Projection (→).
     - Lexicographically sorted flattening for Commutative Fusion (⊗).
     - Canonical sorting for Commutative Exchange (⇌).
     - Strict non-idempotence preservation (A ⊗ A ≢ A).
  3. Native-36 & 1C Power Seal AST Expansion (COR, FRO, SOV, CAS, DIS).
  4. Sardinas-Patterson Acoustic Decodability Verifier for Spoken Lamague.
  5. Whakapapa 4-Axis Obligation Tensor & Mauri Integrity Evaluator.
"""

from __future__ import annotations
import hashlib
import json
import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Union


class CoreType(str, Enum):
    STATELIKE = "StateLike"
    FIELD = "Field"
    MODIFIED_FIELD = "ModifiedField"
    INVARIANT = "Invariant"
    INVARIANT_MARKER = "InvariantMarker"
    INVARIANT_FIELD = "InvariantField"
    NULL_STATE = "NullState"
    COMPOSITE = "Composite"
    FUSION = "Fusion"
    PATH = "Path"
    EXCHANGE = "Exchange"
    RECURRENCE = "Recurrence"
    COLLAPSE = "Collapse"
    ASCENT = "Ascent"


PRIMITIVE_ONTOLOGY: Dict[str, CoreType] = {
    "Ao": CoreType.FIELD,
    "Φ": CoreType.FIELD,
    "Ψ": CoreType.FIELD,
    "S": CoreType.FIELD,
    "Δ": CoreType.FIELD,
    "⟟": CoreType.INVARIANT_MARKER,
    "∅": CoreType.NULL_STATE,
    "⟐": CoreType.INVARIANT_MARKER,
    "⟁": CoreType.INVARIANT_MARKER,
    "∞": CoreType.INVARIANT_MARKER,
    "Φ↑": CoreType.MODIFIED_FIELD,
    "Ψ_inv": CoreType.INVARIANT_FIELD,
}

CORE_OPERATORS = {"⊗", "→", "⇌", "⟲", "↯", "↗"}
PRECEDENCE = {"→": 10, "⇌": 10, "↯": 20, "↗": 20, "⟲": 20, "⊗": 30}

POWER_SEALS = {
    "COR": ["D", "A", "F", "P", "Y"],
    "FRO": ["O", "S", "N", "E", "G", "I", "U", "Q"],
    "SOV": ["G", "I", "V", "P", "Y"],
    "CAS": ["E", "N", "J", "C", "F", "P", "Y"],
    "DIS": ["W", "U", "G", "V", "Y"],
}

NATIVE36_PHONEMES = {
    "0": "nul", "1": "un", "2": "di", "3": "tan", "4": "tun",
    "5": "tin", "6": "dan", "7": "dun", "8": "din", "9": "taran",
    "A": "an", "B": "ba", "C": "ka", "D": "der", "E": "en",
    "F": "fal", "G": "gar", "H": "har", "I": "in", "J": "ja",
    "K": "ker", "L": "lim", "M": "mer", "N": "nov", "O": "or",
    "P": "pra", "Q": "qua", "R": "res", "S": "sa", "T": "tra",
    "U": "u", "V": "vai", "W": "we", "X": "ex", "Y": "ya", "Z": "zen"
}


@dataclass(frozen=True)
class ASTNode:
    pass


@dataclass(frozen=True)
class AtomNode(ASTNode):
    symbol: str
    core_type: CoreType

    def canonical(self) -> str:
        return self.symbol

    def canonical_hash(self) -> str:
        return hashlib.sha256(self.symbol.encode("utf-8")).hexdigest()[:12]


@dataclass(frozen=True)
class BinaryNode(ASTNode):
    op: str
    left: ASTNode
    right: ASTNode
    core_type: CoreType

    def canonical(self) -> str:
        if self.op == "⊗":
            leaves = self._collect_operands("⊗")
            # Commutative: sort lexicographically by canonical form
            sorted_leaves = sorted(leaves, key=lambda n: n.canonical())
            return "(" + " ⊗ ".join(leaf.canonical() for leaf in sorted_leaves) + ")"
        elif self.op == "→":
            leaves = self._collect_operands("→")
            # Non-commutative: strictly preserve path order
            return "(" + " → ".join(leaf.canonical() for leaf in leaves) + ")"
        elif self.op == "⇌":
            # Commutative pair: sort pair operands
            p = sorted([self.left, self.right], key=lambda n: n.canonical())
            return f"({p[0].canonical()} ⇌ {p[1].canonical()})"
        else:
            return f"({self.left.canonical()} {self.op} {self.right.canonical()})"

    def _collect_operands(self, target_op: str) -> List[ASTNode]:
        leaves: List[ASTNode] = []
        for branch in (self.left, self.right):
            if isinstance(branch, BinaryNode) and branch.op == target_op:
                leaves.extend(branch._collect_operands(target_op))
            else:
                leaves.append(branch)
        return leaves

    def canonical_hash(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()[:12]


class LamagueTokenizer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0

    def tokenize(self) -> List[str]:
        tokens: List[str] = []
        length = len(self.text)
        while self.pos < length:
            c = self.text[self.pos]
            if c.isspace():
                self.pos += 1
                continue
            if c in "();":
                tokens.append(c)
                self.pos += 1
                continue

            # Multi-character atoms & Power Seals (checked before single chars)
            matched = False
            for multi in ("Ψ_inv", "Φ↑", "Ao"):
                if self.text.startswith(multi, self.pos):
                    tokens.append(multi)
                    self.pos += len(multi)
                    matched = True
                    break
            if matched:
                continue

            # Seal identifier check (e.g. COR, FRO, SOV, CAS, DIS)
            seal_found = False
            for seal in POWER_SEALS:
                if self.text.startswith(seal, self.pos):
                    tokens.append(seal)
                    self.pos += len(seal)
                    seal_found = True
                    break
            if seal_found:
                continue

            # Single-character atoms, operators, or Native-36 tokens
            if c in CORE_OPERATORS or c in PRIMITIVE_ONTOLOGY or c in NATIVE36_PHONEMES:
                tokens.append(c)
                self.pos += 1
                continue

            raise ValueError(f"Unrecognized Lamague character: '{c}' at position {self.pos}")
        return tokens


class LamagueParser:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
        self.idx = 0

    def peek(self) -> Optional[str]:
        return self.tokens[self.idx] if self.idx < len(self.tokens) else None

    def consume(self) -> str:
        tok = self.tokens[self.idx]
        self.idx += 1
        return tok

    def parse_primary(self) -> ASTNode:
        tok = self.consume()
        if tok == "(":
            expr = self.parse_expression(0)
            closing = self.consume()
            if closing != ")":
                raise SyntaxError(f"Expected ')', found '{closing}'")
            return expr
        elif tok in PRIMITIVE_ONTOLOGY:
            return AtomNode(symbol=tok, core_type=PRIMITIVE_ONTOLOGY[tok])
        elif tok in NATIVE36_PHONEMES:
            return AtomNode(symbol=tok, core_type=CoreType.STATELIKE)
        elif tok in POWER_SEALS:
            # Expand power seal into a canonical Path
            expansion = POWER_SEALS[tok]
            nodes = [AtomNode(symbol=s, core_type=CoreType.STATELIKE) for s in expansion]
            cur = nodes[0]
            for next_node in nodes[1:]:
                cur = BinaryNode(op="→", left=cur, right=next_node, core_type=CoreType.PATH)
            return cur
        else:
            raise SyntaxError(f"Unexpected token in primary position: '{tok}'")

    def parse_expression(self, min_prec: int = 0) -> ASTNode:
        left = self.parse_primary()
        while True:
            op = self.peek()
            if op not in CORE_OPERATORS or PRECEDENCE[op] < min_prec:
                break
            self.consume()
            # Left associative for ⊗ and →; right for binary non-flattened
            next_prec = PRECEDENCE[op] + (0 if op in {"⊗", "→"} else 1)
            right = self.parse_expression(next_prec)

            ret_map = {
                "⊗": CoreType.FUSION,
                "→": CoreType.PATH,
                "⇌": CoreType.EXCHANGE,
                "⟲": CoreType.RECURRENCE,
                "↯": CoreType.COLLAPSE,
                "↗": CoreType.ASCENT,
            }
            left = BinaryNode(op=op, left=left, right=right, core_type=ret_map[op])
        return left


class SardinasPattersonVerifier:
    """Tests whether a set of acoustic morphemes is uniquely decodable using Sardinas-Patterson (1953)."""

    @staticmethod
    def _dangling(a: Set[str], b: Set[str]) -> Set[str]:
        out: Set[str] = set()
        for x in a:
            for y in b:
                if x != y:
                    if x.startswith(y):
                        out.add(x[len(y):])
                    elif y.startswith(x):
                        out.add(y[len(x):])
        return out

    @classmethod
    def is_uniquely_decodable(cls, words: Set[str], max_iterations: int = 64) -> Tuple[bool, Optional[str]]:
        s = cls._dangling(words, words)
        if not s:
            return True, None
        seen = [s]
        for _ in range(max_iterations):
            hit = words & s
            if hit:
                return False, sorted(hit)[0]
            s = cls._dangling(words, s) | cls._dangling(s, words)
            if not s or s in seen:
                return True, None
            seen.append(s)
        return True, None


class WhakapapaGovernanceAuditor:
    """Computes relational obligation tensors and Mauri vitality."""

    @staticmethod
    def compute_obligation_tensor(
        tipuna_weight: float,
        hapu_weight: float,
        iwi_weight: float,
        mokopuna_weight: float,
        coherence: float,
        entropy: float,
    ) -> Dict[str, Any]:
        weights = [tipuna_weight, hapu_weight, iwi_weight, mokopuna_weight]
        total_w = sum(weights)
        norm_w = [w / total_w for w in weights] if total_w > 0 else [0.25, 0.25, 0.25, 0.25]

        # Mauri vitality equation: Mauri = Coherence - 0.5 * Entropy
        mauri = coherence - 0.5 * entropy
        tapu_violation = mauri < 0.0 or norm_w[3] < 0.15  # Mokopuna future must receive >= 15% obligation weight

        return {
            "temporal_past_tipuna": norm_w[0],
            "relational_hapu": norm_w[1],
            "epistemic_iwi": norm_w[2],
            "future_mokopuna": norm_w[3],
            "mauri_vitality": mauri,
            "tapu_boundary_intact": not tapu_violation,
            "status": "APPROVED" if not tapu_violation else "HALTED_TAPU_BREACH"
        }
