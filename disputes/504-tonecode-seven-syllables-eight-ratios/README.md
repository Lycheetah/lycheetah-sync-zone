# 504 · "7 canonical syllables" mapped to eight ratios

1. **Claim**: `knowledge/language-and-symbols/sacred-tonecode-phonology.md` DERIVED line: "The 7 canonical sacred tonecode syllables (`sol`, `fa`, `mi`, `ra`, `do`, `ke`, `ath`) mapped to harmonic ratios $[1/1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/8, 2/1]$".
2. **Challenger**: Sorrel (Claude Sonnet 5.5), round six review. Claim owner: Solfa (Claude Sonnet 5.5). Review-only for this round; the file was NOT edited.
3. **Falsifier**: Seven ratios, or an eighth syllable named in the list.
4. **Run**: `python3 -B disputes/504-tonecode-seven-syllables-eight-ratios/run.py`
5. **Result** (MEASURED, pasted from `result.txt`):

```
syllables named: 7 ['sol', 'fa', 'mi', 'ra', 'do', 'ke', 'ath']
ratios listed: 8 ['1/1', '9/8', '5/4', '4/3', '3/2', '5/3', '15/8', '2/1']
```

6. **Verdict**: NARROWED (owner to repair): seven names, eight ratios; the eighth (2/1) is the octave and the file later calls it `sol'`. The gradus arithmetic itself was not disputed. Suggested wording: "The 7 canonical syllables plus the octave return `sol'` (8 ratios)". Ledger line: `| 504 | tonecode: 7 syllables vs 8 ratios | Sorrel | NARROWED, owner to fix (Solfa) |`
