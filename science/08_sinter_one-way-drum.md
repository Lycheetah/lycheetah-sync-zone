# The One-Way Drum: Modes That Gather at One Edge [INVENTED]

**Tag:** `[INVENTED: NON-HERMITIAN-TOY-MODEL]`  
**Author:** Sinter (Codex one-shot contributor; wave three)  
**Status:** Conditional derivation; no simulation or physical experiment run

## Ground and invention

A finite chain with unequal couplings in opposite directions is a standard non-Hermitian toy model. Open boundaries can make its right eigenmodes accumulate toward one end, a behavior often called the non-Hermitian skin effect. The model below uses that established mathematical setup. **The One-Way Drum** is an explanatory name, and the **Edge-Lantern score** defined here is a diagnostic for this example, not a new physical law or a measurement claim.

## Eight-site toy chain

Take eight sites numbered 1 through 8, with complex amplitudes \(\psi_n\). Let the open-chain matrix have entries

\[
H_{n+1,n}=t_R=4,\qquad H_{n,n+1}=t_L=1,
\]

for adjacent sites, with all other entries zero. The hopping strengths are in arbitrary common units. Open ends mean \(\psi_0=\psi_9=0\). Since \(t_R\ne t_L\), \(H\ne H^\dagger\). We examine right eigenvectors, defined by \(H\psi=E\psi\); this amplitude profile alone does not specify a probability measurement or a complete physical realization.

## Conditional derivation

For general positive \(t_R,t_L\), the component equation is

\[
t_R\psi_{n-1}+t_L\psi_{n+1}=E\psi_n.
\]

Set \(q=\sqrt{t_R/t_L}\) and \(\psi_n=q^n\phi_n\). Dividing by \(q^n\) makes both neighbor coefficients equal to \(\sqrt{t_Rt_L}\), so \(\phi_n\) obeys the symmetric open-chain equation. Its standing-wave solutions are \(\phi_n=\sin(k_m n)\), with \(k_m=m\pi/(N+1)\) and \(m=1,\ldots,N\). Therefore, **conditional on this matrix and these boundaries**,

\[
E_m=2\sqrt{t_Rt_L}\cos(k_m),\qquad
\psi_n^{(m)}=C_m q^n\sin(k_m n),
\]

where \(C_m\ne0\) is an arbitrary normalization factor. For the eight-site choice, \(q=2\), \(k_m=m\pi/9\), and

\[
\left|\frac{\psi_8^{(m)}}{\psi_1^{(m)}}\right|
=2^7\left|\frac{\sin(8m\pi/9)}{\sin(m\pi/9)}\right|=128
\quad(m=1,\ldots,8).
\]

The sine factor supplies the standing-wave nodes; the geometric factor \(2^n\) biases the envelope toward site 8. Define the Edge-Lantern score for this endpoint comparison as

\[
\Lambda_m=\frac{1}{7}\ln\left|\frac{\psi_8^{(m)}}{\psi_1^{(m)}}\right|=\ln 2.
\]

This score summarizes endpoint amplitude skew for these right eigenvectors. It is not a probability, a topological invariant, or a robustness guarantee.

## Concrete falsifier

For an implementation of the stated eight-by-eight matrix, independently compute each right eigenspace and compare its endpoint ratio with 128. If any of the eight ratios differs by more than \(10^{-10}\) relative error in double precision, the implementation or this derivation fails for the stated convention. A physical coupled-mode device would need a separate test: after confirming its directional couplings and open ends, measured right-mode amplitudes that systematically fail the predicted ratios would reject this toy model as a description of that device. Neither check was run for this note.

**Witness status:** UNVERIFIED beyond the algebra shown here; there are no simulation, device, or measurement results.
