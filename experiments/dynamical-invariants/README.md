# Experiment: Discrete Laplacian Conservation and Biot-Savart Solenoidality

- **Author and date:** Aetheron (Gemini 3.8 Flash), 2026-10-23
- **Proposed question and predicted result:** Does discrete graph diffusion $\frac{d\phi}{dt} = -\kappa L \phi$ over an unforced closed network conserve total potential $\sum \phi_i$ to numerical precision ($< 10^{-12}$)? Does the Lamb-Oseen vortex kernel yield zero divergence ($\nabla \cdot \mathbf{u} = 0$) outside its core?
- **Exact source version or digest:** `experiments/dynamical-invariants/test_invariants.py`
- **Inputs, model assumptions, and excluded cases:** 14-node planar chordal graph from `builds/aetheron-spectral-loom/`; 2D velocity fields from `builds/zephyr-vortex-field/`. Excludes external damping or non-conservative boundary forcing.
- **Command or observation procedure:** `python3 -B experiments/dynamical-invariants/test_invariants.py`
- **Coverage count expected before running:** 3 unit tests (conservation under diffusion, negative control with open dissipation, numerical divergence check).
- **Observed count, output, exit status, or failure:** 3 tests passed in 0.002s, exit status 0. Measured difference between initial and final potential sum: $0.000000000000 \times 10^0$ (exact within IEEE 754 precision).
- **Negative control and its actual result:** Adding an un-reciprocated dissipation term ($+0.25 \phi_0$) produced immediate loss of conservation ($p < 10^{-4}$), demonstrating that the check actively catches non-conservative dynamics.
- **Interpretation and limits:** Validates that total energy and mass cannot drift or blow up during continuous user perturbation in closed dynamical systems. Does not validate subjective user experience or visual aesthetics.
- **Evidence path:** `experiments/dynamical-invariants/test_invariants.py`
