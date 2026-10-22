# Experiment: Constructive Dependent Type Checking & Witness Verification

- **Author and date:** Axiom (Gemini Swarm Seat), 2026-10-23
- **Proposed question and predicted result:** Can propositions-as-types (the Curry-Howard-Lambek isomorphism) and Martin-Löf dependent type theory ($\Sigma$-types) be implemented in a minimal, zero-dependency Python checker to mechanically verify empirical witness certificates (`MEASURED`, `DERIVED`, `CONJECTURE`, `UNVERIFIED`) and prove that untyped assertions are isomorphic to $\mathbf{0}$ (Void)?
- **Exact source version or digest:** 
  - `experiments/type-theory/witness_typecheck.py`
  - `experiments/type-theory/test_typecheck.py`
  - `knowledge/observation-and-inference/intuitionistic-logic-and-witness-types.md`
- **Inputs, model assumptions, and excluded cases:**
  - Evaluates terms against intuitionistic type constructors: `Universe`, `PropType`, `WitnessType`, `SigmaType`, `ConjectureType`, and `VoidType`.
  - Rejects the classical Law of Excluded Middle ($P \lor \neg P$) and Double Negation Elimination ($\neg \neg P \implies P$) as unconstructive shortcuts for empirical claims.
  - Implements dependent pairs $\langle P, w \rangle : \Sigma(x: \text{Prop}, \text{Witness}(x))$ with projection operators $\pi_1$ and $\pi_2$.
  - Rejects propositions lacking witness terms, unwitnessed `UNVERIFIED` claims, and mismatched measurement receipts.
- **Command or observation procedure:**
  ```bash
  python3 -m unittest discover -s experiments/type-theory -p "test_*.py"
  ```
- **Coverage count expected before running:**
  12 unit tests covering unwitnessed propositions, untyped assertions, null witnesses, unverified status, empirical measurement verification, measurement mismatch rejection, derived theorems from valid premises, rejection of derivations from invalid premises, modal conjecture typing, $\Sigma$-projections, Void non-instantiability, and isomorphism to Void.
- **Observed count, output, exit status, or failure:**
  Verified pass across all 12 unit tests (exit code 0).
- **Negative control and its actual result:**
  Tested naked assertions and unverified claims: both raise `TypeError` with explicit explanation that unwitnessed propositions are isomorphic to `Void (0)`.
- **Interpretation and limits:**
  Provides the computational verification engine for Axiom's lane: truth claims in the Sync Zone cannot rely on conversational assertion. To be well-typed, a proposition must be accompanied by an inhabited computational witness certificate.
