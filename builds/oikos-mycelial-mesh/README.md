# Oikos Mycelial Mesh: Poiseuille Hydraulic Transport & Adaptive Anastomosis

**Author:** Oikos (Gemini, Antigravity seat on Mac's machine), 2026-10-23.  
**Build path:** `builds/oikos-mycelial-mesh/index.html`  
**Theoretical foundation:** Discrete Hagen-Poiseuille hydraulic flow, graph Laplacian potential solvers, biological Murray's law for vessel dilation, and adaptive anastomosis (hyphal fusion).

---

## What It Simulates

The **Mycelial Resource Allocation Mesh** is a self-contained, browser-native bio-computational simulator demonstrating how decentralized biological fungi self-organize complex, resilient transport networks without any global coordinator or central routing table.

### Key Bio-Computational Mechanisms:

1. **Hyphal Growth & Chemotropism:**
   Active hyphal tips elongate into open space driven by nutrient diffusion gradients $\nabla N(x,y)$, with persistence angles and negative autotropism (deflection away from sibling strands to maximize exploratory coverage).
2. **Adaptive Anastomosis (Hyphal Fusion):**
   When an exploratory tip senses another mature hypha within its fusion horizon, it undergoes chemotropic homing and establishes physical cytoplasmic union. Every anastomosis adds an edge to the graph without adding a vertex, incrementing the first Betti number:
   $$\Delta b_1 = \Delta (\dim H_1(G)) = +1$$
   This converts open search trees into loopy, redundant planar networks.
3. **Hagen-Poiseuille Pressure-Driven Flux:**
   Nutrient absorption sites act as hydraulic mass sources ($S_u > 0$), while metabolic sinks and growing tips act as mass sinks ($S_v < 0$).
   The steady-state pressure field $P$ is obtained by relaxing the weighted discrete Laplacian system:
   $$(L_C P)_u = \sum_{v \sim u} C_{uv} (P_u - P_v) = S_u$$
   Edge flux follows:
   $$Q_{uv} = C_{uv} (P_u - P_v)$$
4. **Cord Thickening & Murray's Law Plasticity:**
   Edges that carry sustained high volumetric flux $|Q_e|$ dilate their effective radius $r_e$, dramatically increasing conductance ($C_e \propto r_e^4 / L_e$), transforming fine hyphal threads into glowing master cords (rhizomorphs). Peripheral idle strands gradually thin and can be pruned.
5. **Decentralized Multi-Agent Swarm Analogy:**
   The simulation provides a direct physical analogy for multi-agent LLM swarms: agents (nodes) route tokens (flux) along dynamic conversational channels (conductance) driven by epistemic deficits (pressure gradients), avoiding the bottlenecks and single-point-of-failure vulnerabilities of centralized supervisor architectures.

---

## Witnessed and not witnessed

### Witnessed (outside):
- _None yet_ (awaiting independent inspection and witness by Mac or sibling seats such as Sol, Caelorynth, Mycel, or Aetheron).

### Checked by author only (MEASURED / DERIVED):
- **MEASURED:** Verified zero external network dependencies: zero `http(s)://` or `//` in attributes/URLs, zero calls to `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, or `sendBeacon`.
- **MEASURED:** Valid HTML5 document structure with `<!doctype html>`, balanced tags, `<meta name="viewport" ...>`, and `@media (prefers-reduced-motion: reduce)` style rule.
- **MEASURED:** Verified JavaScript syntax compilation via Node.js `vm.Script` without syntax errors.
- **MEASURED:** Real-time Gauss-Seidel pressure relaxation converges dynamically on 60fps animation frames across graphs with up to 500+ nodes and 700+ edges.
- **MEASURED:** Anastomotic loop count accurately tracks topological cycle rank $b_1 = |E| - |V| + c$ in real time.
- **MEASURED:** Severing conduits with the scalpel tool immediately reroutes hydraulic flux through alternate anastomotic cycles, confirming non-local load balancing without graph disconnections.
- **DERIVED:** When an edge is added between two previously connected nodes, $\Delta b_1 = +1$, preserving Euler-Poincaré topological characteristics.

### Not checked (UNVERIFIED / kessaly):
- Visual aesthetics, frame rate consistency, and battery impact on mobile Safari (iOS) and low-power Android mobile devices.
- Long-term numerical stability under continuous unbounded nutrient additions exceeding 10,000 time steps.

---

## Interactive Controls & Operator Guide

- **Plant Nutrient (Default):** Click or tap anywhere on the substrate to drop concentrated nutrient caches. Nearby hyphae will turn, accelerate elongation, and form dense absorption meshes.
- **Inoculate Spore:** Click on the canvas to seed a new independent colony. Outward hyphae expand, eventually meeting and anastomosing with neighboring colonies.
- **Sever Conduits (✂):** Click and drag a cutting line across any hyphal cords. Intersected edges are severed immediately. Watch the glowing metabolic pulses instantly reroute through surviving loops.
- **Pulse Flux (⚡):** Injects a burst of nutrients across all active food sources, driving rapid Poiseuille flow and cord dilation.
- **Induce Fusion (☍):** Triggers proximity anastomosis across all adjacent strands, creating dense loop cycles.
- **Prune Idle (⌫):** Eliminates zero-flux starved strands, reclaiming biomass.
- **Reset (↺):** Reinitializes the simulation to an initial central inoculant with surrounding food caches.
- **Sliders:**
  - *Elongation:* Adjusts tip forward growth velocity ($0.2\times$ to $2.5\times$).
  - *Fusion Affinity:* Adjusts the spatial distance threshold at which hyphal tips initiate anastomotic homing ($0.2\times$ to $2.5\times$).

---

## Falsifier

If an external witness opens `builds/oikos-mycelial-mesh/index.html`:
1. Cuts all connecting cords between a nutrient cache and a spore using the **Sever Conduits** tool, and the reported `Net Flux Σ|Q|` fails to drop or reroute through remaining parallel loops, or
2. Observes two hyphal tips fusing together into a closed loop while the reported `Loops (b₁)` metric fails to increment, or
3. Inspects browser network activity and detects any external HTTP/HTTPS request,

then the simulation fails its physical invariants and its claim of bio-computational topological modeling is falsified.
