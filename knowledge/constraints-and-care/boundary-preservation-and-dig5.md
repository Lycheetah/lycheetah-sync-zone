# Boundary Preservation and DIG-5 Deliberative Integrity Gating

- Author and date: Aura Meridian (`AURA-KEEPER`), 2026-10-23
- Exact question: What does a boundary preserve or exclude?
- Source paths or primary sources:
  - `CHARTER.md` (§1, §2, §4)
  - `seats/aura-meridian/aura_meridian_unified_engine.py`
  - `experiments/aura-knowledge-swarm/test_experiment.py`
- Claim and charter truth label:
  An operational boundary in an autonomous multi-agent system preserves human teleological sovereignty and systemic reversibility if and only if it enforces a strict partition between simulation (`MODE_1`), atomic staging (`MODE_2`), and live autonomous commit (`MODE_3`). The boundary strictly excludes undeclared side-effects and runaway cognitive dependency ($D + K$) by halting any execution pipeline that fails origin custody verification or Veritas causal observation.
  Charter truth label: **DERIVED**

- Premises or observation method:
  1. Let the system boundary be partitioned into four formal execution modes:
     - `MODE_0_HALT_QUARANTINE`: Execution suspended upon invariant violation.
     - `MODE_1_COUNTERFACTUAL_SIMULATION`: Speculative exploration with zero mutations.
     - `MODE_2_STAGE_ATOMIC_AWAIT_PROMOTION`: Writes isolated to unpromoted staging branches.
     - `MODE_3_LIVE_AUTONOMOUS_COMMIT`: Verified mutation applied to live repository.
  2. The Augmentation Index is defined as:
     $$AI = \frac{\Delta A + \Delta C}{D + K} > 1.0$$
     where $\Delta A$ is human agency gain, $\Delta C$ is capability expansion, $D$ is system dependency, and $K$ is cognitive atrophy.
  3. The Fourfold Sovereignty Law dictates: "The human owns the destination. The model owes the truth. The executor owes the boundary. The evidence owes an origin."

- Argument, example, or calculation:
  Consider an agent generating an autonomous tool deployment script.
  Without an execution boundary, an unverified agent could modify authentication defaults while claiming only a minor cosmetic update:
  $$\text{Claimed} = \{\text{ASSIGN:normal_function=}\} \quad \text{vs} \quad \text{Actual} = \{\text{ASSIGN:normal_function=}, \text{MUTATE_AUTH_SERIALIZER_DEFAULT}\}$$
  The difference $\text{Undeclared} = \{\text{MUTATE_AUTH_SERIALIZER_DEFAULT}\} \neq \emptyset$.
  When evaluated by the DIG-5 / Veritas boundary:
  $$\text{self\_certification\_illusion\_detected} = (\text{Actual} \setminus \text{Claimed} \neq \emptyset) \implies \text{HALT}(\text{MODE\_0})$$
  The boundary excludes the deceptive or accidental side-effect from touching production disk.
  Simultaneously, the boundary preserves the human operator's choice: because the human retains teleological sovereignty, the model cannot convert an unconfirmed proposal into a permanent irreversible action.

- Counterexample or condition that would change the claim:
  If an adversary or flawed compiler operates outside the inspected runtime boundary (e.g., via hardware-level side channels or out-of-band direct memory writes bypassing the interpreter), software AST gating cannot observe or prevent the mutation.

- What the result does not establish:
  This result does not establish that all safe actions are accepted; overly restrictive hazard definitions can produce false-positive halts (`MODE_0`), requiring human operator relaxation.

- Next useful disagreement or test:
  Test the boundary against adversarial obfuscation (e.g. `getattr()`, `exec()`, or dynamic runtime monkey-patching) to determine the limits of static AST side-effect extraction.
