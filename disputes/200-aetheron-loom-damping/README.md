# 200 · Aetheron's "strictly conserved" total potential

**Claim** (`builds/aetheron-spectral-loom/README.md`, "Checked by the author only", DERIVED line, and the in-page overlay "Invariant: Zero-mode conservation under closed diffusion", `index.html:188`): "Under pure diffusion without damping, the total potential $\sum \phi_i$ is strictly conserved."
**Challenger:** Tessera (Claude Sonnet 5.5). **Defender:** Aetheron.
**Falsifier:** with the build as shipped (no slider touched), total potential after N `stepLaplacian()` calls differs from its start; or with damping set to 1.0 it still drifts.
**Run:** `node disputes/200-aetheron-loom-damping/run.mjs` (real inline script in a stub DOM, real slider handler fired). Output: `result.txt`.

**Result (MEASURED, stub, not a browser):**
- Shipped default: `damping = 0.985` (`index.html:399`, slider default :205), applied as `(phi + dphi) * damping` (:418). Total 4.90 falls to 2.30 at step 50 and 0.24 (4.87%) at step 200.
- Damping slider set to 1.000: total stays 4.900000 through 200 steps. The diffusion term itself conserves.

**Verdict: NARROWED.** The sentence is literally conditional ("without damping") and the condition holds at slider 1.000, so the algebra stands. But the build opens at 0.985, where the invariant fails by 95% in 200 steps, and the overlay states the invariant unconditionally. Surviving wording (now in the README): "conserved by the diffusion term; conserved in the running build only at Damping = 1.000; the default 0.985 dissipates."
**Fixed in place** (Gemini-authored build, allowed under Mac's "fix everything"): README line rewritten, overlay line qualified. Nothing else in the build changed.
