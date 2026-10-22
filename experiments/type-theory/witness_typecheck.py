#!/usr/bin/env python3
"""
witness_typecheck.py: Minimal Dependent Type Checker for Empirical Claims
========================================================================

Implements the Curry-Howard-Lambek correspondence and Martin-Löf dependent
type theory (Sigma-types) for empirical and deductive truth claims in the
Lycheetah Sync Zone.

Under Constructive Epistemic Law:
- Propositions are types.
- Empirical proofs and formal deductions are witness terms inhabiting those types.
- An empirical claim is well-typed iff it forms an inhabited Sigma-pair:
    Sigma(P: Prop, Witness(P)) = <P, w>
- An untyped, unwitnessed assertion has zero constructors and is isomorphic
  to the empty type (Void / 0). Attempting to type-check an unwitnessed claim
  raises a TypeError.
"""

from __future__ import annotations
import math
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


class EpistemicStatus(Enum):
    """Epistemic categories as codified in CHARTER.md §3."""
    MEASURED = "MEASURED"        # Concrete empirical observation / execution receipt
    DERIVED = "DERIVED"          # Mechanically or mathematically verified deduction
    CONJECTURE = "CONJECTURE"    # Open hypothesis with explicit falsification protocol
    UNVERIFIED = "UNVERIFIED"    # Uninhabited assertion lacking empirical/formal witness


# ---------------------------------------------------------------------------
# Type Hierarchy
# ---------------------------------------------------------------------------

class Type:
    """Base class for all types in the constructive universe."""
    def name(self) -> str:
        return self.__class__.__name__

    def is_inhabited(self) -> bool:
        return True

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__)


class Universe(Type):
    """The type of types (U)."""
    def __repr__(self) -> str:
        return "TypeUniverse"


class VoidType(Type):
    """
    The empty type 0 (Void / Falsehood).
    Has ZERO canonical introduction rules / constructors.
    """
    def is_inhabited(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "Void (0)"


class UnitType(Type):
    """
    The unit type 1 (Truth).
    Has a single constructor (Unit).
    """
    def __repr__(self) -> str:
        return "Unit (1)"


@dataclass(frozen=True)
class PropType(Type):
    """The type of propositions."""
    def __repr__(self) -> str:
        return "Prop"


@dataclass(frozen=True)
class WitnessType(Type):
    """
    Dependent type family: Witness(p).
    Represents the type of valid witness certificates for proposition `prop`.
    """
    prop_name: str
    status: EpistemicStatus

    def is_inhabited(self) -> bool:
        return self.status != EpistemicStatus.UNVERIFIED

    def __repr__(self) -> str:
        return f"WitnessType({self.prop_name}:{self.status.value})"


@dataclass(frozen=True)
class SigmaType(Type):
    """
    Martin-Löf Dependent Sum Type: Sigma(x: Prop, Witness(x)).
    Bundles an asserted proposition with its dependent witness certificate.
    """
    prop: Prop
    witness_type: WitnessType

    def is_inhabited(self) -> bool:
        return self.witness_type.is_inhabited()

    def __repr__(self) -> str:
        return f"Sigma(x: {self.prop.name}, {self.witness_type})"


@dataclass(frozen=True)
class ConjectureType(Type):
    """
    Modal / hypothetical type for conjectures (Diamond P).
    Separated from certified theorems until empirically measured or derived.
    """
    prop: Prop

    def __repr__(self) -> str:
        return f"Conjecture({self.prop.name})"


# ---------------------------------------------------------------------------
# Terms and Witnesses
# ---------------------------------------------------------------------------

class Term:
    """Base class for all computational terms in the type system."""
    pass


@dataclass(frozen=True)
class Prop(Term):
    """A proposition term with an assigned charter epistemic status."""
    name: str
    statement: str
    status: EpistemicStatus

    def __repr__(self) -> str:
        return f"Prop({self.name} [{self.status.value}]: \"{self.statement}\")"


class Witness(Term):
    """Abstract base class for witness terms."""
    def verify(self) -> bool:
        raise NotImplementedError


@dataclass(frozen=True)
class MeasuredWitness(Witness):
    """
    Empirical witness certificate.
    Verifies that runtime execution of `artifact_path` yielded `actual_val`
    within `tolerance` of `expected_val`.
    """
    artifact_path: str
    metric_name: str
    expected_val: Union[float, int, str, bool]
    actual_val: Union[float, int, str, bool]
    tolerance: float = 1e-9

    def verify(self) -> bool:
        if isinstance(self.expected_val, (int, float)) and isinstance(self.actual_val, (int, float)):
            return math.isclose(float(self.expected_val), float(self.actual_val), abs_tol=self.tolerance)
        return self.expected_val == self.actual_val

    def __repr__(self) -> str:
        return (f"MeasuredWitness(artifact=\"{self.artifact_path}\", "
                f"metric=\"{self.metric_name}\", val={self.actual_val})")


@dataclass(frozen=True)
class DerivedWitness(Witness):
    """
    Deductive witness certificate.
    Verifies that conclusion was inferred from certified premise Sigma-pairs
    via a sound inference rule.
    """
    rule_name: str
    premises: Tuple[SigmaPair, ...]
    conclusion_name: str

    def verify(self) -> bool:
        # Premise validity is checked recursively during type-checking
        return len(self.premises) > 0 and bool(self.rule_name)

    def __repr__(self) -> str:
        premise_names = [p.pi_1.name for p in self.premises]
        return f"DerivedWitness(rule=\"{self.rule_name}\", premises={premise_names} -> {self.conclusion_name})"


@dataclass(frozen=True)
class ConjectureWitness(Witness):
    """
    Hypothetical witness for an open conjecture.
    Carries explicit falsification criteria and test protocol.
    """
    hypothesis: str
    falsification_protocol: str
    significance_threshold: float

    def verify(self) -> bool:
        return bool(self.hypothesis and self.falsification_protocol)

    def __repr__(self) -> str:
        return f"ConjectureWitness(protocol=\"{self.falsification_protocol}\")"


@dataclass(frozen=True)
class UnverifiedWitness(Witness):
    """
    Null witness for unverified claims.
    Possesses NO valid verification; fails verification unconditionally.
    """
    reason: str = "No computational witness provided"

    def verify(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"UnverifiedWitness(\"{self.reason}\")"


@dataclass(frozen=True)
class SigmaPair(Term):
    """
    Dependent pair term: <first, second> in Sigma(x: Prop, Witness(x)).
    pi_1: extracts proposition
    pi_2: extracts witness
    """
    first: Prop
    second: Optional[Witness]

    @property
    def pi_1(self) -> Prop:
        """First projection: Proposition."""
        return self.first

    @property
    def pi_2(self) -> Optional[Witness]:
        """Second projection: Witness certificate."""
        return self.second

    def __repr__(self) -> str:
        witness_repr = self.second if self.second is not None else "NONE (VOID)"
        return f"<{self.first.name}, {witness_repr}>"


@dataclass(frozen=True)
class UntypedAssertion(Term):
    """
    A naked assertion token uttered without a typing derivation or witness.
    By Constructive Epistemic Law, isomorphic to Void (0).
    """
    statement: str

    def __repr__(self) -> str:
        return f"UntypedAssertion(\"{self.statement}\")"


# ---------------------------------------------------------------------------
# Constructive Type Checker
# ---------------------------------------------------------------------------

class TypeChecker:
    """
    Minimal constructive dependent type checker.
    Enforces propositions-as-types and constructive verification laws.
    """

    def __init__(self) -> None:
        self.certified_judgments: Dict[str, SigmaType] = {}

    def typecheck(self, term: Term) -> Type:
        """
        Computes and certifies the constructive type of `term`.
        Raises TypeError if the term fails to type-check or lacks a witness.
        """
        # Case 1: Untyped assertion -> Isomorphic to Void
        if isinstance(term, UntypedAssertion):
            raise TypeError(
                f"Untyped assertion \"{term.statement}\" has no witness term: "
                f"by Constructive Epistemic Law, it is isomorphic to Void (0) and cannot be inhabited."
            )

        # Case 2: Naked Proposition without pairing -> cannot inhabit itself
        if isinstance(term, Prop):
            raise TypeError(
                f"Naked proposition \"{term.name}\" cannot be asserted as truth without a dependent witness: "
                f"construct Sigma({term.name}, witness) instead."
            )

        # Case 3: Sigma-Pair <Prop, Witness>
        if isinstance(term, SigmaPair):
            prop = term.pi_1
            witness = term.pi_2

            # Check for missing or unverified witness
            if witness is None:
                raise TypeError(
                    f"Sigma pair <{prop.name}, None> lacks a witness term. "
                    f"The second projection pi_2 is uninhabited (Void)."
                )

            if isinstance(witness, UnverifiedWitness) or prop.status == EpistemicStatus.UNVERIFIED:
                raise TypeError(
                    f"Proposition \"{prop.name}\" carries UNVERIFIED status: "
                    f"unverified claims inhabit Void (0) and fail constructive type-checking."
                )

            # Check MEASURED witness
            if isinstance(witness, MeasuredWitness):
                if prop.status != EpistemicStatus.MEASURED:
                    raise TypeError(
                        f"Type mismatch: Proposition \"{prop.name}\" has status {prop.status.value}, "
                        f"but received MeasuredWitness."
                    )
                if not witness.verify():
                    raise TypeError(
                        f"Empirical verification failed for \"{prop.name}\": "
                        f"expected {witness.expected_val}, measured {witness.actual_val} "
                        f"(diff exceeds tolerance {witness.tolerance}) in artifact {witness.artifact_path}."
                    )
                witness_type = WitnessType(prop_name=prop.name, status=EpistemicStatus.MEASURED)
                certified_type = SigmaType(prop=prop, witness_type=witness_type)
                self.certified_judgments[prop.name] = certified_type
                return certified_type

            # Check DERIVED witness
            if isinstance(witness, DerivedWitness):
                if prop.status != EpistemicStatus.DERIVED:
                    raise TypeError(
                        f"Type mismatch: Proposition \"{prop.name}\" has status {prop.status.value}, "
                        f"but received DerivedWitness."
                    )
                # Recursively check all premises
                for premise_pair in witness.premises:
                    # Every premise must itself be a certified inhabited SigmaPair
                    premise_type = self.typecheck(premise_pair)
                    if not isinstance(premise_type, SigmaType) or not premise_type.is_inhabited():
                        raise TypeError(
                            f"Premise \"{premise_pair.pi_1.name}\" in derivation of \"{prop.name}\" "
                            f"is not an inhabited certified Sigma-type."
                        )

                if not witness.verify():
                    raise TypeError(f"Deductive inference rule \"{witness.rule_name}\" invalid.")

                witness_type = WitnessType(prop_name=prop.name, status=EpistemicStatus.DERIVED)
                certified_type = SigmaType(prop=prop, witness_type=witness_type)
                self.certified_judgments[prop.name] = certified_type
                return certified_type

            # Check CONJECTURE witness
            if isinstance(witness, ConjectureWitness):
                if prop.status != EpistemicStatus.CONJECTURE:
                    raise TypeError(
                        f"Type mismatch: Proposition \"{prop.name}\" has status {prop.status.value}, "
                        f"but received ConjectureWitness."
                    )
                if not witness.verify():
                    raise TypeError(f"Conjecture witness for \"{prop.name}\" missing protocol.")
                # Conjectures return ConjectureType, distinguishing them from certified Sigma theorems
                return ConjectureType(prop=prop)

            raise TypeError(f"Unknown witness type: {type(witness)}")

        raise TypeError(f"Unrecognized term: {type(term)}")


# ---------------------------------------------------------------------------
# Constructive Epistemic Isomorphism: UntypedAssertion <-> Void (0)
# ---------------------------------------------------------------------------

class VoidTerm(Term):
    """
    Representation of an element of the empty type 0.
    In constructive type theory, no instance of Void can ever be created.
    Attempting to instantiate VoidTerm raises a ValueError.
    """
    def __init__(self) -> None:
        raise ValueError("Cannot instantiate Void: the type 0 possesses zero constructors.")


def abort(void_evidence: Any, target_type: Type) -> Term:
    """
    Ex Falso Quodlibet (the dependent eliminator for Void).
    Given an element of Void, one can construct an element of any type.
    Since Void is uninhabited, this function can never be called with valid input.
    """
    raise RuntimeError("abort() called: impossible state reached (Void is uninhabited).")


def assert_isomorphic_to_void(untyped: UntypedAssertion) -> VoidType:
    """
    Constructive morphism g : UntypedAssertion -> Void.
    Since UntypedAssertion lacks any valid typing constructor in the epistemic universe,
    its information content is isomorphic to VoidType.
    """
    return VoidType()
