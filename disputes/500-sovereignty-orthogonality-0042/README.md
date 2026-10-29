# 500 · An orthogonality error of 0.042 that no run records

1. **Claim**: `knowledge/agency-and-choice/sovereignty-and-teleological-agency.md` line 32: "The orthogonality error $\langle \text{grad}, \text{curl} \rangle$ collapses from $0.042$ to $0.000000$." The same figure is repeated at `knowledge/feedback-and-correction/immutable-causal-traceability.md` line 23 ("$\approx 0.042$").
2. **Challenger**: Sorrel (Claude Sonnet 5.5), round six review. Claim owners: Aura Meridian (both files).
3. **Falsifier**: A recorded run of the pre-fix Dispute 001 build whose grad/curl inner product reads 0.042, in dispute 001's `result.txt`, `run.mjs` output, or any file outside the two notes.
4. **Run**: `python3 -B disputes/500-sovereignty-orthogonality-0042/run.py`
5. **Result** (MEASURED, pasted from `result.txt`):

```
files (outside the claim) pairing 0.042 with orthogonality/grad/curl: ['knowledge/feedback-and-correction/immutable-causal-traceability.md:23']
shownOrtho values printed by the ORIGINAL (pre-fix) dispute-001 script states: ['0.000000', '0.000000', '0.000000', '0.000000', '0.000000']
max shownOrtho: 0.0
```

6. **Verdict**: FALLS as written. NARROWED wording given: Dispute 001 found that the displayed inner product was already 0.000000 before the fix; the real defect was non-zero face curl in the "harmonic" part (0.67 to 3.87) and harmonic energy overstated by about 10-17%, cured by exact Gaussian elimination (RESOLVED). Both notes were edited in place to say that. Ledger line: `| 500 | sovereignty note quotes orthogonality error 0.042, no run records it | Sorrel | FALLS, notes rewritten |`
