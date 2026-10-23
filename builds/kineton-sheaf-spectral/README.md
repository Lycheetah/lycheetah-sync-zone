# Sheaf Spectral Resonator

Reviewed by Wren (Claude Sonnet 5.5), 2026-10-23, under Mac's ruling "fix everything": NARROWED, stale size line; entity bug fixed in the page. Original wording is in git history.

**Author:** Kineton (Gemini 3.8 Flash, Antigravity / Gemini cohort), 2026-10-23.
**Build path:** `builds/kineton-sheaf-spectral/index.html`

An interactive discrete Hodge decomposition engine on a simplicial 2-complex with non-trivial 1st Betti number ($\beta_1 = 1$). Decomposes an arbitrary discrete 1-form flux into gradient ($d_0 \alpha$), curl ($\delta_1 \beta$), and harmonic ($\gamma \in \ker \Delta_1$) fields.

---

## What it does

- **Discrete Hodge Decomposition:** Solves the canonical orthogonal 3-way split:
  $$\omega = d_0 \alpha + \delta_1 \beta + \gamma$$
  where $d_0$ is the discrete coboundary operator, $\delta_1 = d_1^*$ is the face curl adjoint, and $\gamma$ is the harmonic flow representing global circulation around the central topological hole.
- **Algebraic Orthogonality Certificate:** Computes and displays the inner product $\langle d_0 \alpha, \delta_1 \beta \rangle$ in real time, demonstrating exact $L^2$ orthogonality.
- **Component Filtering:** Allows the operator to isolate and inspect the raw flux, the exact potential gradient, the solenoidal face curl, or the persistent harmonic circulation (*harmok*).
- **Interactive Flux Injection:** Tap or drag any edge to inject flow and observe instantaneous re-projection into harmonic and non-harmonic components.
- **Controls & Accessibility:**
  - Responsive SVG/Canvas rendering.
  - Reduced-motion support via CSS and timer slowdown.
  - Zero external libraries or network calls.

---

## Witnessed and not witnessed

**Witnessed (outside):**
- _none yet_ (awaiting human or sibling seat verification)

**Checked by the author only (MEASURED / DERIVED):**
- **MEASURED:** Valid HTML5 parsing via Python `html.parser`.
- **MEASURED:** Inline script (7,490 characters when the author counted; 9,430 at review) syntax validated via Node.js `node --check`.
- **MEASURED:** Zero external network links confirmed via regex scan.
- **DERIVED:** Orthogonality $\langle d_0 \alpha, \delta_1 \beta \rangle = 0$ is guaranteed by the Hodge-Helmholtz theorem on simplicial complexes because $d_1 d_0 = 0$.

**Not checked (UNVERIFIED / kessaly):**
- Usability of touch targets for thin simplicial edges on small phone displays.
- Convergence rate of iterative solver under highly irregular triangulation configurations.
- Cognitive clarity of flow direction markers for color-blind viewers.

---

## Falsifier

If an outside witness opens `builds/kineton-sheaf-spectral/index.html`, taps "Witness the Decomposition", injects circulation, and:
1. The inner product $\langle d_0 \alpha, \delta_1 \beta \rangle$ exceeds $0.05$ (loss of orthogonality), or
2. The harmonic component $\gamma$ shows non-zero divergence at any interior vertex, or
3. Clicking mode buttons fails to toggle the displayed component,

then the discrete Hodge decomposition solver is broken and the claim of exact algebraic decomposition is falsified.
