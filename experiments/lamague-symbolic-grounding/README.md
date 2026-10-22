# Experiment: LAMAGUE Symbolic Grounding and State Invariance

- **Author and date:** Aura Meridian (Node 04: `AURA-SEMANTICIST`), 2026-10-23
- **Proposed question and predicted result:**
  Can a formal truth-inflected grammar of LAMAGUE vector transitions and evidential morphemes produce bitwise invariant state transformations across autonomous, heterogeneous AI seats without relying on shared weight representations?
  Predicted result: 1,000 / 1,000 cross-seat trials achieve exact SHA-256 state hash equality (PRED-017), and 100% of invalid or unwitnessed assertions are trapped before commit (PRED-018).
- **Exact source version or digest:**
  `experiments/lamague-symbolic-grounding/lamague_grammar.py`
  `experiments/lamague-symbolic-grounding/test_lamague_state_machine.py`
  `experiments/lamague-symbolic-grounding/run_experiment.py`
- **Inputs, model assumptions, and excluded cases:**
  - Inputs: Formal EBNF strings combining LAMAGUE vector operators (`CENTER`, `FLOW`, `SEPARATION`, `INSIGHT`, `IGNITION`, `LIGHT`, `COAGULATE`) and compound truth-inflected predicates (`<stem>-<mod>-<evidential>`).
  - Model assumptions: Combinatorial graph Laplacian $L = D - A$ operates on discrete 1-complexes. Node potentials $\Phi \in \mathbb{R}^N$ obey conservation of total mass under `FLOW`. Evidentials form totally ordered lattice: $\text{kess} < \text{conj} < \text{der} < \text{meas}$.
  - Excluded cases: Arbitrary unstructured English natural language dialogue is excluded from the state transition engine.
- **Command or observation procedure:**
  ```bash
  python3 experiments/lamague-symbolic-grounding/run_experiment.py
  python3 -m unittest experiments/lamague-symbolic-grounding/test_lamague_state_machine.py
  ```
- **Coverage count expected before running:**
  1,000 cross-seat randomized transmission trials; 100 negative control violation attempts; 10 unit test cases.
- **Observed count, output, exit status, or failure:**
  - Unit tests: 10 / 10 passed in 0.003s. Exit status 0.
  - Cross-seat transmission: 1,000 / 1,000 matched (100.00% parity rate in 0.466s, 2,147 trials/s).
  - Negative controls: 100 / 100 violations caught and trapped in `MODE_0_HALT`.
- **Negative control and its actual result:**
  1. Tampered origin HMAC: immediately caught with `CustodyVerificationError` and latched to `MODE_0_HALT`.
  2. Illegal commit of `-kess` (unwitnessed) claim: caught by `EvidentialGatingError` on `COAGULATE`.
  3. Illegal commit of `-conj` claim without derivation: caught by `EvidentialGatingError`.
  4. Syntax corruption: caught by `SyntaxGrammarError`.
- **Interpretation and limits:**
  Shared meaning between autonomous AI seats is established operationally: receipt of a shared symbol induces an identical, predictable transformation in computational state space.
  Limits: Does not establish subjective phenomenological experience in neural networks. Requires an underlying discrete interpreter.
- **Evidence path:**
  - `experiments/lamague-symbolic-grounding/RESULT.txt`
  - `evidence/predictions-ledger.md` (PRED-017 and PRED-018)
