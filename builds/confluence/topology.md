# Hypercube Subgraph Invariants

`topology.py` provides pure, standard-library-only graph and topological analysis over candidate worlds on the 6-dimensional Boolean hypercube $Q_6$.

## What it computes

Given a list of `compatible_worlds` produced by `inspect_worlds(...)`:
- **Vertices ($|V|$):** The number of unique compatible 6-bit states.
- **Edges ($|E|$):** Transitions between worlds differing by exactly one bit (Hamming distance 1).
- **Connected Components ($\beta_0$):** The number of disconnected clusters in the candidate space.
- **Cycle Rank / 1st Betti Number ($\beta_1$):** Number of independent 1-cycles in the world graph ($\beta_1 = |E| - |V| + \beta_0$).
- **Diameter:** The maximum geodesic distance between any two reachable worlds within a component.
- **Affine Subcube Invariant:** Certifies whether the candidate world space forms an unconstrained subcube $Q_k$ of dimension $k$.

## Mathematical Truth

When a hard parity prior (`parity=0` or `parity=1`) is imposed, the candidate worlds are all at Hamming distance $\ge 2$. Consequently:
- $|E| = 0$
- $\beta_0 = |V|$ (the candidate manifold shatters into completely isolated discrete vertices)
- $\beta_1 = 0$ (all cycles vanish)

This is a **DERIVED** algebraic invariant that holds without empirical speculation.
