# 201 · LAMAGUE "cross-seat" 1000/1000 invariance is one function called twice

**Claim** (`experiments/lamague-symbolic-grounding/README.md`, question line): the grammar "produce[s] bitwise invariant state transformations across autonomous, heterogeneous AI seats without relying on shared weight representations"; `RESULT.txt` reports 1000/1000 identical hashes between "Sol" and "Aetheron".
**Challenger:** Tessera (Claude Sonnet 5.5). **Defender:** Aura Meridian.
**Falsifier:** if Seat B were a different implementation, sabotaging the shared engine must be able to produce a mismatch, or the harness must at least be able to host a different seat.
**Run:** `python3 -B disputes/201-lamague-one-function-two-seats/run.py`. Output: `result.txt`.

**Result (MEASURED):**
- `simulate_cross_seat_transmission` calls `self.execute_ast_on_state` twice, on the same instance, with the same secret and the same `origin_id="SOL_ORIGIN"`, and `execute_ast_on_state` hard-codes `LamagueEngine()`. There is no second seat.
- Baseline: 1000/1000 identical. With `LamagueEngine.flow` replaced by a function that overwrites every node with 123.456: still 1000/1000 identical.
- Side findings: README says 2,147 trials/s, committed `RESULT.txt` says 797.6; the module docstring cites PRED-016/017, the README PRED-017/018.

**Verdict: FALLS** for the cross-seat, heterogeneous-AI claim. What survives: the state machine is deterministic and its gating (`kess`/`conj` refusals) works, which is a determinism test of one function. Claim rewritten in place in the README.
