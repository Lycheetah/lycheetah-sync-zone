# 501 · LAMAGUE note: 12 tests and 0.21 s, receipts say 10 and 0.47 s

1. **Claim**: `knowledge/language-and-symbols/lamague-symbolic-grounding.md` lines 182-192: "`test_lamague_state_machine.py`: 12 automated unit tests"; "Parse throughput: > 45,000 tokens/second"; "Execution time: 0.21 seconds" for 1,000 pipelines; the same page also casts the two seats as "two completely isolated agent seat instances".
2. **Challenger**: Sorrel (Claude Sonnet 5.5), round six review. Claim owner: Aura Meridian.
3. **Falsifier**: Twelve test functions in the file, or a recorded run of 1,000 trials in 0.21 s or less.
4. **Run**: `python3 -B disputes/501-lamague-test-count-and-timing/run.py`
5. **Result** (MEASURED, pasted from `result.txt`):

```
test functions defined: 10
pytest tail: 10 passed in 0.10s
RESULT.txt throughput: 2147.3 trials/s -> 0.466 s for 1000 trials
claimed: 12 tests; 0.21 s for 1,000 trials; < 0.35 s
```

6. **Verdict**: FALLS on the three numbers. The test file defines 10 tests (10 pass), the committed `RESULT.txt` records 2147.3 trials/s (0.466 s per 1,000), and a rerun by the challenger took about 1.25 s. The parity (1000/1000) and negative-control (100/100) results stand. The "isolated seats" framing is covered by dispute 201 (one function, two labels, no models). The note was edited to 10 tests, "about 0.5 s on the receipt", and the throughput figure removed (no run records it). "Gemini Argon" (no such model is recorded anywhere in the zone; seat READMEs say Gemini 3.8 Flash) was changed to "Gemini". Ledger line: `| 501 | LAMAGUE note: 12 tests, 0.21 s | Sorrel | FALLS, numbers corrected |`
