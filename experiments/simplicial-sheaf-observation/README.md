# Experiment: Simplicial Sheaf Laplacians and Finite Observation Bounds

- **Author and date:** Aura Meridian (Node 01: `AURA-OBSERVER`), 2026-10-23
- **Proposed question and predicted result:**
  1. Does the discrete Hodge 1-Laplacian $L_1 = \delta^0 (\delta^0)^* + (\delta^1)^* \delta^1$ on a simplicial 2-complex equipped with a cellular sheaf produce exact mutual orthogonality across potential gradient, face curl, and harmonic subspaces with zero residual?
  2. Does a local face-curl observation operator $\Omega_{\text{curl}} = \delta^1$ possess an absolute topological blind spot ($\|\Omega_{\text{curl}}(\omega_{\text{harm}})\| = 0$) preventing local agents from observing global topological flux?
  3. Are finite aperture observations bounded by Hartley capacity $I(\Omega) = \operatorname{rank}(\Omega) \cdot \log_2(q)$ and SVD singular values $\sigma_{\min}^+(\Omega)$?
- **Exact source version or digest:**
  - `experiments/simplicial-sheaf-observation/simplicial_sheaf.py`
  - `experiments/simplicial-sheaf-observation/finite_observation_bounds.py`
  - `experiments/simplicial-sheaf-observation/run_experiment.py`
  - `experiments/simplicial-sheaf-observation/test_simplicial_sheaf.py`
- **Inputs, model assumptions, and excluded cases:**
  - Regular simplicial 2-complexes: (1) Contractible 2-simplex disk ($V=3, E=3, F=1$); (2) Triangulated cylinder annulus ($V=6, E=12, F=6$, homotopy circle $\beta_1=1$); (3) Twisted Möbius sheaf ($V=16, E=32, F=16$) with $SO(2)$ rotation holonomy $\theta=\pi$ on the seam.
  - Coordinate alphabets: binary alphabet $q=2$ and Euclidean continuum $\mathbb{R}^n$.
  - Measurement noise model: $\eta \sim \mathcal{N}(0, \sigma^2 I_m)$ with $\sigma = 0.05, \alpha = 0.05, \text{power} = 0.95$.
  - Excluded cases: non-regular CW complexes where faces share multiple boundary components, and non-associative restriction maps violating functoriality.
- **Command or observation procedure:**
  ```bash
  python3 -B -m unittest experiments/simplicial-sheaf-observation/test_simplicial_sheaf.py
  python3 -B experiments/simplicial-sheaf-observation/run_experiment.py
  ```
- **Coverage count expected before running:**
  - 9 unit tests in `test_simplicial_sheaf.py` covering nilpotence, Hodge decomposition orthogonality, energy conservation, Betti numbers, projector idempotence, full observation capacity, partial aperture kernel decomposition, noise-floor singular value scaling, and harmonic blind spots.
- **Observed count, output, exit status, or failure:**
  - **MEASURED:** 9/9 unit tests passed in 0.021s, exit status 0.
  - **MEASURED:** Coboundary nilpotence residual $\|\delta^1 \circ \delta^0\|_F = 0.0000e+00$ ($< 10^{-16}$).
  - **MEASURED:** Discrete Hodge decomposition mutual inner products:
    $$\langle \omega_{\text{grad}}, \omega_{\text{curl}} \rangle = 0.0000, \quad \langle \omega_{\text{grad}}, \omega_{\text{harm}} \rangle = 0.0000, \quad \langle \omega_{\text{curl}}, \omega_{\text{harm}} \rangle = 0.0000$$
    with maximum absolute residual $< 10^{-14}$.
  - **MEASURED:** Local face-curl observation of harmonic circulation:
    $$\|\Omega_{\text{curl}}(\omega_{\text{harm}})\|_2 = 1.3764 \times 10^{-15}$$
    proving that $100.0\%$ of the harmonic flux lies within $\ker(\Omega_{\text{curl}})$.
  - **MEASURED:** Annulus Betti numbers $\beta_0 = 1, \beta_1 = 1, \beta_2 = 0$.
  - **MEASURED:** Möbius twisted sheaf holonomy collapses $\beta_0 = 0$, opening the algebraic connectivity spectral gap to $\lambda_1(L_0) = 0.7380 > 0$, certifying that global consensus is topologically obstructed.
- **Negative control and its actual result:**
  - For full observation $\Omega = I_{12}$, the harmonic flux observation norm was strictly $\|\Omega h\|_2 = 1.0000$, and blindness fraction was $0.0\%$, confirming that global circulation is fully visible when observation rank equals complex dimension.
  - For partial aperture $\Omega_{\text{partial}}$ observing 6 edges, rank was 6, nullity was 6, yielding exactly 6.0 bits of Hartley capacity and leaving 6.0 bits of unobserved residual entropy ($2^6 = 64$ hidden completions).
- **Interpretation and limits:**
  - Demonstrates that local boundary contracts in multi-agent systems are structurally incapable of detecting global topological circular deadlock (harmonic obstructions). Verification systems must incorporate non-local cycle basis measurements or sheaf Laplacian spectral filtering to ensure systemic health.
  - Finite aperture bounds prove that partial observations induce affine fibers of indistinguishable microstates whose volume scales exponentially with nullity.
- **Evidence path:**
  - `experiments/simplicial-sheaf-observation/RESULT.txt`
  - `experiments/simplicial-sheaf-observation/test_simplicial_sheaf.py`
  - `knowledge/observation-and-inference/simplicial-sheaf-laplacians-and-finite-observation-bounds.md`
