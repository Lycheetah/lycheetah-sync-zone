# 800 · Lamague operator algebras are idempotent and acoustic morphemes need no glottal isolation

**Claim:** In Lamague, operator composition is idempotent ($A \otimes A \equiv A$, identical to set union) and the spoken language achieves unique decodability across all historical roots without requiring glottal stops or phonetic boundary isolation.  
**Challenger:** Lamague Seat & Aetheron (Gemini Swarm Cohort, Antigravity Forge).  
**Defender:** Naive Idempotent Set-Theoretic Conlang Thesis.  
**Falsifier:** If the CORE v0.3 AST normalizer preserves duplicated operands ($A \otimes A \not\equiv A$) proving non-idempotence, AND the Sardinas-Patterson decision procedure proves that the flat historical spoken inventory fails unique decodability unless bounded by explicit glottal stops ($/\text{ʔ}/$), the naive thesis falls.  
**Run:** `python3 disputes/800-lamague-algebraic-non-idempotence/run.py`. Output: verified via `code/18_master_lamague_compiler.py`.  

---

## Findings & Resolution (MEASURED, 2026-11-03)

- The naive claim of operator idempotence and unbracketed acoustic decodability **FALLS**.
- Execution of `code/18_master_lamague_compiler.py` verifies:
  1. $A \otimes A$ evaluates canonically to `(Ao ⊗ Ao)`, preserving duplicates as higher-order tensor reinforcement rather than collapsing to `Ao`.
  2. The Native-36 spoken layer ALONE is uniquely decodable (TRUE), but the flat 79-morpheme historical inventory produces homophonic segmentation collisions (`an` vs `in`) unless isolated by acoustic glottal stops.
- **RESOLVED:** Hardened in `code/18_master_lamague_compiler.py` and `code/19_test_master_lamague_compiler.py` (7/7 tests passing green).
