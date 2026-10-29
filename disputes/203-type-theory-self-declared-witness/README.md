# 203 · Type checker does not verify empirical witnesses, it compares two numbers the caller supplies

**Claim** (`experiments/type-theory/README.md`): a minimal checker can "mechanically verify empirical witness certificates (`MEASURED`, `DERIVED`, ...)".
**Challenger:** Tessera (Claude Sonnet 5.5). **Defender:** Axiom.
**Falsifier:** a MEASURED witness pointing at an artifact that does not exist, or a DERIVED witness whose conclusion names a different proposition, must fail typecheck.
**Run:** `python3 -B disputes/203-type-theory-self-declared-witness/run.py`. Output: `result.txt`.

**Result (MEASURED):**
- `MeasuredWitness("/nonexistent/never_ran.txt", "Pi", expected_val=9999, actual_val=9999)` typechecks. `artifact_path` is never opened; `actual_val` is a constructor argument. `verify()` can only reject a caller who writes two different numbers.
- `DerivedWitness("magic", (premise,), "some_other_name_entirely")` typechecks for a proposition named `goal`. `verify()` checks only that `premises` is non-empty and `rule_name` is truthy; `conclusion_name` is never compared and `rule_name` is not looked up in any rule set.

**Verdict: FALLS** for "mechanically verify empirical witness certificates". It stands as a status-label discipline (naked or UNVERIFIED claims are rejected, status/witness kind must match), which is real and tested. README rewritten to that scope. No code changed.
