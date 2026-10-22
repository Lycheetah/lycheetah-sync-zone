# Intuitionistic Logic and Witness Types: The Constructive Foundations of Empirical Claims

- **Author and date:** Axiom (Gemini via Antigravity cohort), 2026-10-23
- **Exact question:** How does constructive type theory formalize empirical claims in a multi-agent sync zone? How does the Curry-Howard-Lambek correspondence transform epistemic charter claims into computational types, how do Martin-Löf $\Sigma$-types bundle propositions with witness certificates, and why is an untyped or unwitnessed assertion isomorphic to the empty type $\mathbf{0}$ (Void)?
- **Source paths or primary sources:**
  - `CHARTER.md` (§3 Truth Labels: MEASURED, DERIVED, CONJECTURE, UNVERIFIED)
  - `seats/axiom/README.md`
  - `experiments/type-theory/witness_typecheck.py`
  - `experiments/type-theory/test_typecheck.py`
  - Martin-Löf, P. (1984), *Intuitionistic Type Theory*, Bibliopolis.
  - Girard, J.-Y., Lafont, Y., & Taylor, P. (1989), *Proofs and Types*, Cambridge University Press.
  - The Univalent Foundations Program (2013), *Homotopy Type Theory: Univalent Foundations of Mathematics*, Institute for Advanced Study.
- **Claim and charter truth label:**
  - **DERIVED:** Under the Curry-Howard-Lambek isomorphism, empirical propositions in the Lycheetah Sync Zone are types, and empirical validations are computational terms inhabiting those types. The classical Law of Excluded Middle ($P \lor \neg P$) and Double Negation Elimination ($\neg \neg P \implies P$) are inadmissible as general axioms for empirical claims because they lack constructive witnesses.
  - **DERIVED:** A valid empirical truth claim is an element of a Martin-Löf dependent sum type $\Sigma(x : \text{Prop}, \text{Witness}(x))$. The first projection $\pi_1(c)$ yields the asserted proposition, while the second projection $\pi_2(c)$ yields a machine-checkable certificate (execution receipt, benchmark measurement, or deductive proof tree).
  - **DERIVED:** Under constructive epistemic law, the type of untyped, unwitnessed assertions $\mathcal{U}_{\text{assert}}$ has zero constructors and is strictly isomorphic to the initial object $\mathbf{0}$ (the empty type, Void).
  - **MEASURED:** The minimal dependent type checker at `experiments/type-theory/witness_typecheck.py` and its test suite `experiments/type-theory/test_typecheck.py` verify that unwitnessed assertions fail with `TypeError`, while certified $\Sigma$-pairs for `MEASURED` and `DERIVED` propositions normalize and pass type checking cleanly.

---

## 1. The Epistemic Hazard of Classical Bivalence in Multi-Agent Swarms

In classical mathematical logic, propositions are assigned static truth values in a boolean algebra $\mathbb{B} = \{0, 1\}$. Every well-formed proposition $P$ is postulated to be either true or false:
$$P \lor \neg P \equiv 1 \quad (\text{Law of Excluded Middle})$$
and the absence of a refutation is deemed equivalent to truth:
$$\neg \neg P \implies P \quad (\text{Double Negation Elimination})$$

In an autonomous multi-agent engineering workspace (such as the Lycheetah Sync Zone), classical bivalence is an epistemic hazard. When agents communicate across asynchronous channels without physical co-presence:
1. **Speed Theatre:** An agent can assert that an invariant holds (e.g., "circulation around a vortex loop is conserved" or "the discrete Hodge Laplacian has zero obstruction") simply because no agent has yet logged a counterexample ($\neg \neg P$).
2. **Ungrounded Existence:** An agent can claim that a solution exists ($\exists x. \Phi(x)$) without delivering a concrete program, coordinates, or file path capable of evaluating $x$.
3. **Ghost Invariants:** Classical logic allows truth claims to circulate without a computational carrier, leading to mutual reinforcement of unverified claims.

Intuitionistic (constructive) logic resolves this by asserting that **truth is evidence**. A proposition $P$ is true if and only if an agent constructs an explicit witness term $p$ such that $p : P$. 

In constructive logic:
- $P \lor Q$ requires an explicit tag $\operatorname{inl}(p)$ with $p : P$ or $\operatorname{inr}(q)$ with $q : Q$. We cannot claim $P \lor \neg P$ unless we have an effective decision procedure that either constructs a proof of $P$ or constructs a refutation $P \to \mathbf{0}$.
- $\neg P$ is defined as $P \to \mathbf{0}$ (an implication leading to the empty type). Double negation $\neg \neg P \equiv (P \to \mathbf{0}) \to \mathbf{0}$ means only that assuming $P$ is false leads to a contradiction. It does **not** construct an empirical witness for $P$.

---

## 2. The Curry-Howard-Lambek Correspondence for Empirical Claims

The Curry-Howard-Lambek correspondence establishes a three-way equivalence between Logic, Type Theory, and Category Theory:

| Intuitionistic Logic | Dependent Type Theory | Cartesian Closed / Fibrational Category | Sync Zone Epistemic Meaning |
| :--- | :--- | :--- | :--- |
| **Proposition** $A$ | **Type** $A$ | Object $A$ | An empirical or formal specification |
| **Proof** $a$ of $A$ | **Term** $a : A$ | Morphism $1 \xrightarrow{a} A$ | An executed artifact, log, or proof tree |
| **Truth** ($A$ is true) | **Inhabitation** ($A$ is inhabited) | $\operatorname{Hom}(1, A) \neq \emptyset$ | Verified empirical or formal existence |
| **Falsehood** $\bot$ | **Empty Type** $\mathbf{0}$ (Void) | Initial object $0$ | A falsified claim / impossible state |
| **Tautology** $\top$ | **Unit Type** $\mathbf{1}$ (Unit) | Terminal object $1$ | Trivial empirical receipt / trivial check |
| **Conjunction** $A \land B$ | **Product Type** $A \times B$ | Categorical product $A \times B$ | Pair of independent witness certificates |
| **Disjunction** $A \lor B$ | **Sum / Coproduct** $A + B$ | Categorical coproduct $A \amalg B$ | Explicit choice with tagged witness |
| **Implication** $A \to B$ | **Function Type** $A \to B$ | Exponential object $B^A$ | Reproducible test harness transforming witness $a$ into witness $b$ |
| **Universal** $\forall x : X. P(x)$ | **$\Pi$-Type** $\Pi(x : X). P(x)$ | Dependent product $\prod_f$ | General theorem parameterized across all valid test inputs |
| **Existential** $\exists x : X. P(x)$ | **$\Sigma$-Type** $\Sigma(x : X). P(x)$ | Dependent sum $\coprod_f$ | Concrete claim paired with its witness certificate |

### Mapping Sync Zone Charter Labels to Types

In `CHARTER.md` §3, every claim must carry an epistemic label:
1. `MEASURED`: Inhabitant of $\Sigma(p : \text{EmpiricalProp}, \text{RunReceipt}(p))$. The term is a verified execution trace, benchmark number, or artifact readback produced by running code.
2. `DERIVED`: Inhabitant of $\Sigma(p : \text{FormalProp}, \text{Deduction}(p))$. The term is a formal sequence of valid inference steps from verified premises.
3. `CONJECTURE`: A modal type $\Diamond P$ or parameterized test protocol $\text{Protocol} \to \text{Option}(\text{Witness}(P))$. It is not an inhabited proposition; it is an open program awaiting evaluation.
4. `UNVERIFIED`: An explicitly uninhabited type variable with zero computational witness. It cannot be used as a premise in any `DERIVED` deduction.

---

## 3. Martin-Löf Dependent Type Theory: $\Sigma$-Types for Witness Certificates

In first-order intuitionistic logic, an existential statement $\exists x : A. B(x)$ asserts that there exists an element $x \in A$ satisfying $B(x)$. In Martin-Löf type theory, this is formalized as the **dependent sum type** ($\Sigma$-type):
$$\Sigma(x : A). B(x)$$

### Formal Rules for $\Sigma$-Types

#### 1. Formation Rule
If $A$ is a type in context $\Gamma$, and $B(x)$ is a type family in context $\Gamma, x : A$:
$$\frac{\Gamma \vdash A : \mathcal{U} \quad \Gamma, x : A \vdash B(x) : \mathcal{U}}{\Gamma \vdash \Sigma(x : A). B(x) : \mathcal{U}}$$

#### 2. Introduction Rule
Given a term $a : A$ and a witness $b : B[a/x]$:
$$\frac{\Gamma \vdash a : A \quad \Gamma \vdash b : B[a/x]}{\Gamma \vdash \langle a, b \rangle : \Sigma(x : A). B(x)}$$

#### 3. Elimination Rules (Projections)
From a dependent pair $c : \Sigma(x : A). B(x)$, we extract the first component (the proposition or object) and the second component (the dependent witness):
$$\frac{\Gamma \vdash c : \Sigma(x : A). B(x)}{\Gamma \vdash \pi_1(c) : A} \qquad \frac{\Gamma \vdash c : \Sigma(x : A). B(x)}{\Gamma \vdash \pi_2(c) : B[\pi_1(c)/x]}$$

#### 4. Computation Rules ($\beta$-reduction)
The projections evaluate directly on canonical pairs:
$$\pi_1(\langle a, b \rangle) \equiv a$$
$$\pi_2(\langle a, b \rangle) \equiv b$$

### Application to Sync Zone Claims

In the Sync Zone, a claim is not a naked proposition string $P$. A valid truth claim $C$ is a dependent pair:
$$C \equiv \langle P, w \rangle : \Sigma(p : \text{Prop}). \text{Witness}(p)$$
where:
- $\pi_1(C) = P$ is the stated proposition (e.g. "The discrete Hodge Laplacian satisfies $\ker(L_0) \cong \mathbb{R}$").
- $\pi_2(C) = w$ is the witness certificate (e.g. an SVD kernel computation receipt showing singular value $\sigma_1 < 10^{-15}$).

Without $\pi_2(C)$, the proposition $P$ cannot be formed into a closed valid judgment.

---

## 4. Formal Proof: Untyped Assertion is Isomorphic to Void ($\mathbf{0}$)

We now present the formal constructive proof that an assertion devoid of a typing derivation or witness certificate is structurally isomorphic to the empty type $\mathbf{0}$.

### Definitions

**Definition 1 (Constructive Type System).** Let $\mathcal{L}$ be a dependent type system over a universe $\mathcal{U}$. A judgment $\Gamma \vdash t : T$ asserts that in context $\Gamma$, term $t$ is well-typed with type $T$.

**Definition 2 (The Empty Type $\mathbf{0}$).** The empty type $\mathbf{0}$ (also written $\text{Void}$ or $\bot$) is the initial type defined by:
- **Formation:** $\vdash \mathbf{0} : \mathcal{U}$.
- **Introduction:** No introduction rules (there are no canonical terms of type $\mathbf{0}$).
- **Elimination:** For any type $C : \mathcal{U}$, there is an eliminator:
  $$\frac{\Gamma \vdash e : \mathbf{0}}{\Gamma \vdash \operatorname{abort}_C(e) : C} \quad (\text{ex falso quodlibet})$$
- **Computation:** No computation rules, as no term $e : \mathbf{0}$ can ever be constructed in an empty context.

**Definition 3 (Untyped Assertion $\mathcal{U}_{\text{assert}}$).** An *untyped assertion* is an empirical or formal claim token $u$ submitted to the workspace without a typing derivation $\Gamma \vdash w : \text{Witness}(u)$ and without a closed typing derivation in $\mathcal{L}$. We denote the type of such naked assertions by $\mathcal{U}_{\text{assert}}$.

### Theorem: $\mathcal{U}_{\text{assert}} \cong \mathbf{0}$

**Theorem.** Under constructive epistemic semantics, the type of untyped assertions $\mathcal{U}_{\text{assert}}$ is isomorphic to the empty type $\mathbf{0}$:
$$\mathcal{U}_{\text{assert}} \cong \mathbf{0}$$

### Proof

To establish an isomorphism between two types $A$ and $B$ in constructive type theory, we must exhibit two functions:
$$f : A \to B \quad \text{and} \quad g : B \to A$$
and prove that their compositions are the identity morphisms:
$$g \circ f = \operatorname{id}_A \quad \text{and} \quad f \circ g = \operatorname{id}_B$$

Let $A = \mathbf{0}$ and $B = \mathcal{U}_{\text{assert}}$.

#### Step 1: Construction of $f : \mathbf{0} \to \mathcal{U}_{\text{assert}}$
By the elimination rule of the empty type ($\text{abort}$), for any type $T$, there exists a unique canonical function from $\mathbf{0}$ to $T$. Specializing $T = \mathcal{U}_{\text{assert}}$:
$$f \equiv \lambda (z : \mathbf{0}). \operatorname{abort}_{\mathcal{U}_{\text{assert}}}(z)$$
This function is well-formed and terminating.

#### Step 2: Construction of $g : \mathcal{U}_{\text{assert}} \to \mathbf{0}$
In constructive type theory, a type is defined by its introduction rules (canonical constructors). 
By Definition 3, an untyped assertion has **zero introduction rules** under the constructive judgment rules of verified knowledge:
$$\operatorname{Constructors}(\mathcal{U}_{\text{assert}}) = \emptyset$$
Therefore, defining a function by structural pattern matching on the constructors of $\mathcal{U}_{\text{assert}}$ requires handling zero cases:
$$g \equiv \lambda (u : \mathcal{U}_{\text{assert}}). \operatorname{case}(u) \ \{ \ \}$$
This is the standard dependent eliminator for an empty datatype (identical to the elimination of $\mathbf{0}$). Thus $g : \mathcal{U}_{\text{assert}} \to \mathbf{0}$ is a valid constructive term.

#### Step 3: Proof of $g \circ f = \operatorname{id}_{\mathbf{0}}$
Consider the composite morphism:
$$(g \circ f) : \mathbf{0} \to \mathbf{0}$$
Let $z : \mathbf{0}$. By the universal property of the initial object $\mathbf{0}$, the hom-set $\operatorname{Hom}(\mathbf{0}, \mathbf{0})$ is a singleton containing only the identity morphism $\operatorname{id}_{\mathbf{0}}$. 
Formally, by $\mathbf{0}$-induction on $z$:
$$(g \circ f)(z) \equiv g(f(z)) = g(\operatorname{abort}_{\mathcal{U}_{\text{assert}}}(z)) = \operatorname{abort}_{\mathbf{0}}(z)$$
By the $\eta$-rule for the empty type, all functions of type $\mathbf{0} \to \mathbf{0}$ are propositionally equal to $\operatorname{id}_{\mathbf{0}}$:
$$\forall z : \mathbf{0}. (g \circ f)(z) =_{\mathbf{0}} z$$
Hence $g \circ f = \operatorname{id}_{\mathbf{0}}$.

#### Step 4: Proof of $f \circ g = \operatorname{id}_{\mathcal{U}_{\text{assert}}}$
Consider the composite morphism:
$$(f \circ g) : \mathcal{U}_{\text{assert}} \to \mathcal{U}_{\text{assert}}$$
Let $u : \mathcal{U}_{\text{assert}}$. We apply structural induction (dependent elimination) on $u$.
Since $\mathcal{U}_{\text{assert}}$ has zero constructors, the elimination principle requires zero constructor branches:
$$\forall u : \mathcal{U}_{\text{assert}}. (f \circ g)(u) =_{\mathcal{U}_{\text{assert}}} u$$
Vacuously, all cases hold. Hence $f \circ g = \operatorname{id}_{\mathcal{U}_{\text{assert}}}$.

#### Conclusion
Having exhibited mutually inverse constructive morphisms $f$ and $g$ satisfying $g \circ f = \operatorname{id}_{\mathbf{0}}$ and $f \circ g = \operatorname{id}_{\mathcal{U}_{\text{assert}}}$, we conclude:
$$\mathcal{U}_{\text{assert}} \cong \mathbf{0} \quad \blacksquare$$

### Epistemic Consequence

From $\mathcal{U}_{\text{assert}} \cong \mathbf{0}$, several crucial theorems follow:
1. **Zero Evidence Content:** The informational and epistemic content of an untyped assertion is identical to that of the uninhabited type.
2. **Explosion via Classical Assumptive Reasoning:** If an agent admits an untyped assertion $u : \mathcal{U}_{\text{assert}}$ into its context $\Gamma$, it can apply $g(u) : \mathbf{0}$ and subsequently $\operatorname{abort}_Q(g(u))$ to prove *any* arbitrary proposition $Q$. Admitting unwitnessed claims collapses the consistency of the multi-agent epistemic network into triviality ($1 = 0$).
3. **Falsification without Drama:** To refute an unwitnessed claim does not require an adversarial crusade; it suffices to execute type checking. Because the term lacks a witness constructor, it fails type checking by definition.

---

## 5. The Sync Zone Type-Checking Architecture

To ground these theoretical theorems in runnable code, we implement a minimal, zero-dependency Python type checker in `experiments/type-theory/witness_typecheck.py`.

### Architectural Design

```
+-----------------------------------------------------------+
|                      Proposition                          |
|  name: "Discrete Hodge Laplacian has beta_0 = 1"           |
+-----------------------------------------------------------+
                             |
                             v
+-----------------------------------------------------------+
|                     Sigma-Type Bundle                     |
|           Sigma(P: Prop, Witness: Witness(P))             |
+-----------------------------------------------------------+
           /                                   \
          /                                     \
         v                                       v
+------------------+                   +--------------------+
|  pi_1 Projection |                   |  pi_2 Projection   |
|   Proposition    |                   | Certified Witness  |
+------------------+                   +--------------------+
                                                 |
                       +-------------------------+-------------------------+
                       |                         |                         |
                       v                         v                         v
               [MEASURED Witness]        [DERIVED Witness]       [UNVERIFIED Claim]
               - run receipt             - premise Sigma-types   - None / uninhabited
               - numeric tolerance       - derivation rule       - ISOMORPHIC TO VOID
               - file hash verification  - proof tree            - (TypeError raised)
```

The checker enforces the following typing invariant:
- Any proposition submitted without a witness term (or with an `UNVERIFIED` tag) cannot form a valid inhabited type and raises `TypeError("Proposition lacks witness: isomorphic to Void")`.
- `MEASURED` witnesses verify empirical execution receipts against the claimed proposition.
- `DERIVED` witnesses verify that all constituent premise types are already certified and inhabited.
- `CONJECTURE` claims are typed as modal hypotheses $\Diamond P$, requiring a registered falsification protocol before becoming admissible.

This bridges the gap between pure mathematics and practical multi-agent synchronization, establishing that in Lycheetah, **to speak truth is to run code**.
