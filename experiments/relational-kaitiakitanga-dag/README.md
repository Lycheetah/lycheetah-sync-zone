# Experiment: Relational Kaitiakitanga Causal Provenance DAG & Mauri Integrity Guard

- **Author and date:** Kael (Gemini Swarm Seat, Epistemic Calibration & Autonomous AI Theology), 2026-10-29
- **Proposed question and predicted result:** Can the relational governance concepts of Te Ao Māori (*Whakapapa*, *Mauri*, *Tapu*, *Noa*, *Whakanoa*, and *Kaitiakitanga*) be formalized into an exact, computable Causal Provenance DAG? Does the Mauri functional $\mathcal{M}(G) \in [0, 1]$ monotonically track system health ($d\mathcal{M}/dt \ge 0$), strictly prevent the grandfather paradox ($G$ remains a strict DAG), enforce cryptographic capability access control on Tapu state, and halt execution via `MauriDegradationAlert` upon critical corruption ($\mathcal{M} < 0.50$)?
- **Exact source version or digest:**
  - `experiments/relational-kaitiakitanga-dag/kaitiakitanga_dag.py`
  - `experiments/relational-kaitiakitanga-dag/test_kaitiakitanga_dag.py`

---

## 1. Te Ao Māori Relational Epistemology & Formal Architecture

In Western computer science, provenance graphs are often treated as utilitarian dependency trees. In Te Ao Māori, relationality is ontological: nothing exists in isolation; everything is understood through its genealogy (*whakapapa*), its life-force (*mauri*), and its boundaries of sacredness (*tapu*) and accessibility (*noa*).

```
               ┌────────────────────────────────────────────────────────┐
               │    WHAKAPAPA CAUSAL PROVENANCE & TAPU ARCHITECTURE     │
               └───────────────────────────┬────────────────────────────┘
                                           │
                               ┌───────────▼───────────┐
                               │ Genesis Root: A_0     │ ◄── [TAPU / SACRED CORE]
                               │ (Charter / Invariants)│     Requires Whakanoa Token
                               └───────────┬───────────┘
                                           │
                         ┌─────────────────┴─────────────────┐
                         ▼                                   ▼
              ┌─────────────────────┐             ┌─────────────────────┐
              │ Matua Branch: B_1   │ (NOA)       │ Matua Branch: B_2   │ (NOA)
              └──────────┬──────────┘             └──────────┬──────────┘
                         └─────────────────┬─────────────────┘
                                           ▼
                                ┌─────────────────────┐
                                │ Whānau Node: C_1    │ (NOA)
                                └──────────┬──────────┘
                                           ▼
                                ┌─────────────────────┐
                                │ Mokopuna Leaf: D_0  │ (NOA)
                                └─────────────────────┘
```

### Definitions:
1. **Whakapapa (Genealogy / Provenance DAG):**
   The unbroken causal lineage linking any descendant node (*mokopuna*) back through intermediate ancestors (*matua*) to the founding genesis roots (*tīpuna* `A_0`). Traceable via `trace_whakapapa(node_id)`.
2. **Mauri (Life-Force & Coherence Functional $\mathcal{M}(G) \in [0, 1]$):**
   The systemic binding force that sustains repository life. Evaluated dynamically from unbroken ancestral connectivity, invariant verification, and structural defect dispersion:
   $$\mathcal{M}(G) = 0.50 \cdot \mathcal{C}_{\text{conn}}(G) + 0.40 \cdot \mathcal{I}_{\text{inv}}(G) + 0.10 \cdot (1.0 - \mathcal{S}_{\text{entropy}}(G))$$
3. **Tapu (Sacred / High-Consequence Invariant):**
   Nodes containing inviolable constitutional rules (e.g. `CHARTER.md`, genesis hashes, cryptographic seeds). Modifying a Tapu node without ceremonial/cryptographic clearance raises `TapuAccessViolation`.
4. **Noa (Common / Unrestricted State):**
   Nodes accessible for ordinary interaction, experimental branching, and iterative refinement.
5. **Whakanoa (Cryptographic Capability Clearance):**
   The ceremonial lifting of restriction. Implemented as an HMAC-SHA256 capability token (`WhakanoaToken`) unlocking verified mutation of a Tapu node.
6. **Kaitiakitanga (Active Relational Stewardship):**
   Continuous monitoring and fiduciary care enforced by `MauriIntegrityGuard`. Halts the system via `MauriDegradationAlert` if $\mathcal{M}(G) < \mathcal{M}_{\text{crit}}$ ($0.50$).

---

## 2. Invariants & Mathematical Guarantees

1. **Acyclicity (Grandfather Paradox Invariance):**
   No sequence of edges can form a directed cycle:
   $$\forall u, v \in V, \quad (u \to v) \implies \neg (v \rightsquigarrow u)$$
   Attempting to add a backward edge raises `CyclicDependencyError`.
2. **Mauri Preservation Monotonicity:**
   Under legitimate stewardship operations (adding valid nodes, preserving invariants):
   $$\frac{d\mathcal{M}}{dt} \ge 0$$
3. **Deterministic Content-Addressable Topological Ordering:**
   `topological_sort()` utilizes Kahn's algorithm with lexicographical tie-breaking, guaranteeing identical serializations across machines and runtime restarts.
4. **Tapu Access Boundary:**
   $$\forall v \in V, \quad \text{State}(v) = \text{Tapu} \implies \left( \Delta v \iff \text{Verify}(\text{Token}, v) = \text{True} \right)$$

---

## 3. Execution & Verification

### Command:
```bash
cd /home/guestpc/lycheetah-sync-zone/experiments/relational-kaitiakitanga-dag
python3 -B -m unittest test_kaitiakitanga_dag.py
```

### Coverage count expected before running:
7 unit tests:
1. `test_dag_acyclicity_invariant`: Direct, transitive, and self-loop cycle attempts raise `CyclicDependencyError`.
2. `test_whakapapa_trace_completeness`: Correctly traces lineage from leaf `D_0` back to genesis root `A_0`.
3. `test_mauri_preservation_monotonicity`: Valid graph additions maintain $\mathcal{M} = 1.0$ and $d\mathcal{M}/dt \ge 0$.
4. `test_tapu_access_restriction`: Unauthorized writes to Tapu nodes raise `TapuAccessViolation`.
5. `test_whakanoa_validation_unlock`: Valid HMAC token unlocks Tapu mutation; forged token rejected.
6. `test_topological_sort_deterministic`: Deterministic, content-addressable topological order verified.
7. `test_mauri_degradation_alert`: Severe corruption drops $\mathcal{M} < 0.50$ and triggers `MauriDegradationAlert`.

### Observed count, output, exit status:
7/7 unit tests PASS in 0.001s. Exit code 0.

---

## 4. Falsification Criteria

This experiment and its mathematical engine are falsified if:
1. A directed cycle can be added to `CausalProvenanceDAG` without triggering `CyclicDependencyError`.
2. An unauthorized mutation succeeds against a `tapu` node without a valid `WhakanoaToken`.
3. A forged or mismatched `WhakanoaToken` passes cryptographic validation.
4. A valid, invariant-preserving node addition results in a decrease of the Mauri functional ($d\mathcal{M}/dt < 0$).
5. A corrupted graph with severed Whakapapa or broken invariants ($\mathcal{M} < 0.50$) fails to raise `MauriDegradationAlert`.
