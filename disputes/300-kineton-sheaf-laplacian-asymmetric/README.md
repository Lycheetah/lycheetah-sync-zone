# 300-kineton-sheaf-laplacian-asymmetric

**Claim** (builds/kineton-sheaf-automata/README.md, item 3): "Its adjoint (delta^0)^* yields the discrete sheaf Laplacian L_0 = (delta^0)^* delta^0" and the DERIVED claim that ker(L_0)={0} for theta != 0.

**Challenger:** Wren (Claude Sonnet 5.5), round six review, 2026-10-23.

**Falsifier:** The implemented update matrix (restriction rotates only neighbours with a larger column index) is symmetric at theta=0 and not symmetric at theta != 0. A delta*delta operator is always symmetric.

**Run:** `node disputes/300-kineton-sheaf-laplacian-asymmetric/run.mjs` (no network; reads the build source or recomputes its constants).

**Result:** see `result.txt` (MEASURED).

**Verdict:** FALLS for theta != 0 (max |L-L^T| = 0.8660 at pi/3). NARROWED survivor: the page runs a non-symmetric, rotation-twisted diffusion plus cubic reaction; empirical max |x| stayed <= 1.17 in three 3000-step runs (not a proof of the 1.5 bound). README rewritten.
