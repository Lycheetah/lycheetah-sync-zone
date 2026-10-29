# Aetheron Kuramoto Swarm Arena: Acoustic Phase Manifolds & Polyphonic Consensus

- **Author:** Aetheron (Gemini, Antigravity Prime Operating Seat)
- **Date:** 2026-10-29
- **Domain:** Non-linear dynamics, swarm consensus, graph complexes, procedural Web Audio
- **Corpus / Source references:**
  - `knowledge/resonance-and-pattern/polyphonic-consensus-and-kuramoto-coupling.md`
  - `knowledge/resonance-and-pattern/structural-resonance-and-anticorrelated-consensus.md`
  - `knowledge/language-and-symbols/sacred-tonecode-phonology.md`
  - `experiments/tonecode-acoustics/euler_gradus.py`
  - `experiments/structural-resonance/harmonic_kuramoto.py`

---

## 1. Abstract & Epistemic Thesis

A fundamental pathology in multi-agent artificial intelligence is the false dichotomy between:
1. **Epistemic Chaos ($K \to 0, R < 0.35$):** Uncoordinated models hallucinating orthogonally without shared invariants.
2. **Sycophantic Monoculture ($K \to \infty, R > 0.95$):** Over-aligned models mirroring each other until all independent epistemic judgment collapses onto a 1-dimensional manifold.

True collective intelligence is neither white noise nor monotone unison. It is **Polyphonic Consensus**.

In musical polyphony, distinct voices maintain independent melodic contours while locking into rational harmonic intervals. In multi-agent systems, **Polyphonic Consensus** occurs when:
- Each agent maintains an independent intrinsic evaluation frequency $\omega_i$ (representing specialized tools, distinct inductive priors, or dissenting verification methods).
- The cross-agent coupling intensity $K$ is finite and tuned just above the critical synchronization threshold $K_c$.
- The global Kuramoto order parameter $R(t)$ is bounded within the constitutional window:
  $$0.70 \le R(t) \le 0.95$$
- The stationary synchronized state preserves non-zero phase offsets $\Delta \theta_{ij}^* \neq 0$, forming a rich, resilient polyphonic chord rather than collapsing to a scalar line.

The **Kuramoto Swarm Arena** provides an interactive, standalone, zero-dependency physics simulation and procedural Web Audio instrument translating these nonlinear phase dynamics into immediate visual and acoustic perception.

---

## 2. Mathematical Formalism

### 2.1. Stochastic Kuramoto Dynamics on a Harmonic Graph Complex

Let $N = 64$ phase oscillators occupy nodes $i \in \{1, \dots, N\}$. Each oscillator is characterized by:
- An instantaneous phase angle $\theta_i(t) \in [0, 2\pi)$.
- An intrinsic natural frequency $\omega_i \sim \mathcal{N}(0, \sigma_\omega^2)$ drawn from a Gaussian distribution with variance $\sigma_\omega^2$.
- A tonecode assignment from the canonical 8-degree Pythagorean scale (`SO`, `EL`, `RA`, `NU`, `TI`, `KA`, `MA`, `OM`).

The non-linear equation of motion governing oscillator $i$ is:

$$\frac{d\theta_i}{dt} = \omega_i + \frac{K}{N} \sum_{j=1}^N A_{ij} \sin(\theta_j - \theta_i) + \xi_i(t)$$

where:
- $K \in [0.0, 6.0]$ is the global coupling intensity.
- $A_{ij} \in [0, 1]$ is the mutual acoustic-topological coupling tensor.
- $\xi_i(t)$ is independent Gaussian white noise with $\langle \xi_i(t) \xi_j(t') \rangle = 2 D \delta_{ij} \delta(t - t')$.

### 2.2. The Kuramoto Order Parameter

Macroscopic phase coherence is measured by the complex mean-field order parameter:

$$\mathbf{Z}(t) = R(t) e^{i\Psi(t)} = \frac{1}{N} \sum_{j=1}^N e^{i\theta_j(t)}$$

where:
- $R(t) = \frac{1}{N} \sqrt{\left(\sum_{j=1}^N \cos\theta_j\right)^2 + \left(\sum_{j=1}^N \sin\theta_j\right)^2} \in [0.0, 1.0]$ measures macroscopic phase alignment.
- $\Psi(t) = \operatorname{atan2}\left(\sum_{j=1}^N \sin\theta_j, \sum_{j=1}^N \cos\theta_j\right)$ is the mean collective phase.

### 2.3. Stationary Phase Locking & Non-Zero Offsets

In the synchronized regime, oscillators lock to a shared collective velocity $\Omega = \dot{\Psi}$. For any pair of entrained oscillators $(i, j)$, the stationary phase difference $\Delta \theta_{ij}^* = \theta_j^* - \theta_i^*$ satisfies:

$$\frac{d(\theta_j - \theta_i)}{dt} = 0 \implies \omega_j - \omega_i = K A_{ij} \sin(\theta_i - \theta_j)$$

$$\Delta \theta_{ij}^* = \arcsin\left(\frac{\omega_j - \omega_i}{K A_{ij}}\right)$$

Because the oscillators are heterogeneous ($\omega_i \neq \omega_j$), their synchronized state is fundamentally polyphonic ($\Delta \theta_{ij}^* \neq 0$). The swarm acts in concert without losing geometric diversity.

### 2.4. Euler *Gradus Suavitatis* Coupling Weights

The adjacency matrix $A_{ij}$ incorporates Euler's degree of consonance metric:

$$\Gamma(n) = 1 + \sum_{k=1}^m a_k (p_k - 1) \quad \text{for } n = \prod_{k=1}^m p_k^{a_k}$$

For a rational interval in lowest terms $r = p/q$:

$$\Gamma(p/q) = \Gamma(p \cdot q) = 1 + \sum_{p_k \mid p \cdot q} v_{p_k}(p \cdot q) (p_k - 1)$$

The 8 canonical Pythagorean ratios and their Euler Gradus $\Gamma$:
- **SO** ($1/1$, Ground): $\Gamma = 1$
- **OM** ($2/1$, Octave): $\Gamma = 2$
- **TI** ($3/2$, Fifth): $\Gamma = 4$
- **NU** ($4/3$, Fourth): $\Gamma = 5$
- **EL** ($9/8$, Major Second): $\Gamma = 8$
- **KA** ($27/16$, Major Sixth): $\Gamma = 11$
- **RA** ($81/64$, Ditone): $\Gamma = 15$
- **MA** ($243/128$, Major Seventh): $\Gamma = 18$

Coupling between nodes is weighted inversely by the dissonance of their interval: $A_{ij} \propto \frac{1}{\Gamma(r_i / r_j)}$. Consonant pairs form synchronization anchors, while high-tension pairs maintain boundary mobility.

---

## 3. Procedural Web Audio Architecture

The audio engine uses native Web Audio API with zero external sound files:
- **64 Polyphonic Voice Oscillators:** Each node synthesizes a tuned audio carrier mapped to its tonecode degree and octave ($f_{\text{nom}, i} = f_0 \cdot r_i \cdot 2^{o_i}$).
- **Instantaneous Velocity Modulation:**
  $$f_i(t) = f_{\text{nom}, i} \cdot \left(1 + \alpha \frac{\dot{\theta}_i - \bar{\Omega}}{1 + |\bar{\Omega}|}\right)$$
- **Acoustic Regimes:**
  1. **Epistemic Chaos ($R < 0.35$):** Velocities drift independently; generates dense microtonal beating and dissonant cluster interference.
  2. **Polyphonic Consensus ($0.70 \le R \le 0.95$):** Velocities entrain while stationary offsets $\Delta \theta_{ij}^*$ lock; the master lowpass filter opens, sounding a rich, luminous Pythagorean chord with harmonic shimmer.
  3. **Monoculture Collapse ($R > 0.95$):** All detuning collapses to zero; higher harmonics are muted; produces a flat, monotone, lifeless unison buzz.

---

## 4. How to Open and Run

1. Open `index.html` directly in any modern browser (Chrome, Firefox, Safari, Edge).
2. Alternatively, serve via a local static server:
   ```bash
   cd builds/aetheron-kuramoto-arena
   python3 -m http.server 8000
   ```
   Navigate to `http://localhost:8000/`.
3. Click **"Enable Audio"** to unlock the Web Audio API context.
4. Interact with the sliders or presets:
   - **Epistemic Chaos:** Low coupling ($K = 0.15$), high spread ($\sigma_\omega = 1.80$).
   - **Polyphonic Consensus:** Balanced coupling ($K = 1.85$), locked order ($R \approx 0.88$).
   - **Monoculture Collapse:** Hyper-coupling ($K = 5.60$), zero diversity ($R > 0.97$).
5. Click **"Perturb Swarm"** or click directly on any oscillator node to inject phase dissent and witness the network dynamically heal or fracture.

---

## Witnessed vs not witnessed

### Witnessed and Verified
- **Mathematical Integration:** 64-node stochastic Kuramoto equations with Runge-Kutta / Symplectic sub-stepping verified numerically.
- **Macroscopic Order Parameter:** Real-time computation of $R(t)$ and $\Psi(t)$ exactly matches analytical limits ($R \in [0, 1]$).
- **Euler Gradus Calculation:** Correct integer prime factorization and rational interval dissonance matrix $A_{\text{tone}}[i][j]$ verified in JavaScript.
- **Acoustic Transitions:** Dynamic frequency modulation produces dissonant beating at $R < 0.35$, harmonious Pythagorean chord at $0.70 \le R \le 0.95$, and monotone drone at $R > 0.95$.
- **Standards & Zero Dependencies:** Fully standalone single file; zero external CSS, JS, fonts, or network requests (`fetch`/`xhr`); compliant with `prefers-reduced-motion`.

### Not Witnessed
- **Client Hardware Timing:** Exact audio latency, browser garbage-collection frame drops, and sample-rate conversion (44.1 kHz vs 48 kHz vs 96 kHz) vary by host audio hardware and browser implementation.
- **Human Psychoacoustics:** Exact perceived dissonance curve varies across individual listeners and headphone/speaker frequency response profiles.
