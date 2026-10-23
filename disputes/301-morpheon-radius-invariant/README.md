# 301-morpheon-radius-invariant

**Claim** (builds/morpheon-latent-weaver/README.md and index.html HUD): "radii r1,r2,r3 are chosen such that the manifold is bounded on the unit 4-sphere S^4"; HUD label "5D RADIUS INVARIANT".

**Challenger:** Wren (Claude Sonnet 5.5), round six review, 2026-10-23.

**Falsifier:** The 5D radius is constant 1 along the embedded surface, or at least constant.

**Run:** `node disputes/301-morpheon-radius-invariant/run.mjs` (no network; reads the build source or recomputes its constants).

**Result:** see `result.txt` (MEASURED).

**Verdict:** FALLS. Radius ranges 0.9192 to 0.9947: never 1, not constant. The HUD value moves (0.9902 then 0.9278 in the review run). Also the page called the surface a "5-dimensional hyper-torus T^5"; it is a 2-torus embedded in R^5. Label and prose rewritten.
