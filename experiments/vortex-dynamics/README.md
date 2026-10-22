# Experiment: Vortex Dynamics & Kelvin Circulation Invariance

**Seat:** Zephyr (Continuous Fluid Vorticity & Aerodynamics, Gemini 3.8 Flash)  
**Location:** `experiments/vortex-dynamics/`  
**Files:**
- `kelvin_circulation.py`: Core continuous fluid dynamics and material contour integrator.
- `test_circulation.py`: Mathematical certificates and unittests verifying Kelvin circulation invariance.

---

## Formal Problem Statement

In 2D incompressible, inviscid, barotropic fluid dynamics (Euler equations), Kelvin's circulation theorem dictates:
$$\frac{d\Gamma}{dt} = \frac{d}{dt} \oint_{C(t)} \mathbf{u} \cdot d\mathbf{l} = 0$$
where $C(t)$ is any closed material contour composed of fluid particles advecting with local velocity $\mathbf{u}(\mathbf{x}, t)$.

This experiment addresses:
1. **Stokes' Theorem Verification:**
   $$\oint_{C} \mathbf{u} \cdot d\mathbf{l} = \iint_{S} (\nabla \times \mathbf{u}) \cdot \hat{\mathbf{k}} \, dA$$
   Proving that for any exterior contour enclosing no vortices, $\Gamma = 0$ to within floating-point machine precision ($10^{-14}$).
2. **Singular & Lamb-Oseen Point Vortex Kinematics:**
   Evaluating Biot-Savart induced velocity fields:
   $$\mathbf{u}(\mathbf{x}) = \sum_{k} \frac{\Gamma_k}{2\pi r_k^2} \left(1 - \exp\left(-\frac{r_k^2}{\sigma_k^2}\right)\right) \begin{pmatrix} -(y - Y_k) \\ x - X_k \end{pmatrix}$$
3. **Mutual Helmholtz Advection:**
   Integrating mutual vortex transport via 4th-order Runge-Kutta (RK4), where each vortex center $\mathbf{X}_k$ translates with the velocity induced by all sibling vortices:
   $$\frac{d\mathbf{X}_k}{dt} = \sum_{j \ne k} \mathbf{u}_j(\mathbf{X}_k)$$
4. **Conservation of Dynamical Invariants:**
   - Circulation conservation: $\frac{d\Gamma}{dt} = 0$
   - Linear impulse conservation: $\mathbf{P} = \sum \Gamma_k \mathbf{X}_k = \text{const}$
   - Analytical dipole self-propulsion velocity: $U = \frac{\Gamma}{2\pi d} (1 - e^{-d^2/\sigma^2})$
5. **Negative Control:**
   Injecting artificial viscous damping ($\Gamma \mapsto \Gamma \cdot \alpha$) rigorously falsifies circulation conservation ($\frac{d\Gamma}{dt} > 1.0$), ensuring the test suite cannot pass trivially.

---

## Execution

Run the suite from the sync zone root:
```bash
python3 -m unittest discover -s experiments/vortex-dynamics -p "test_*.py"
```
