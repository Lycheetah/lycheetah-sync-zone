"""Compute graph and topological invariants on compatible 6-bit hypercube worlds."""

__all__ = ["analyze_world_topology"]


def _hamming_distance(w1: str, w2: str) -> int:
    return sum(c1 != c2 for c1, c2 in zip(w1, w2))


def analyze_world_topology(compatible_worlds: list[str]) -> dict:
    """Analyze the induced subgraph of compatible worlds on the 6-hypercube Q_6.

    Vertices are compatible 6-bit strings. Edges connect worlds at Hamming distance 1.
    Calculates exact connected components (beta_0), cycle rank (beta_1), and graph diameter.
    """
    if type(compatible_worlds) is not list:
        raise TypeError("compatible_worlds must be a list of strings")

    for i, w in enumerate(compatible_worlds):
        if type(w) is not str:
            raise TypeError(f"compatible_worlds[{i}] must be a string")
        if len(w) != 6 or any(c not in "01" for c in w):
            raise ValueError(f"compatible_worlds[{i}] must be exactly six characters, all '0' or '1'")

    # Deduplicate while preserving order
    unique_worlds = list(dict.fromkeys(compatible_worlds))
    n = len(unique_worlds)

    if n == 0:
        return {
            "vertex_count": 0,
            "edge_count": 0,
            "connected_components": 0,
            "beta_0": 0,
            "beta_1": 0,
            "diameter": 0,
            "is_subcube": False,
            "dimension": None,
        }

    world_set = set(unique_worlds)
    adj: dict[str, list[str]] = {w: [] for w in unique_worlds}
    edges: set[tuple[str, str]] = set()

    for i in range(n):
        w1 = unique_worlds[i]
        for j in range(i + 1, n):
            w2 = unique_worlds[j]
            if _hamming_distance(w1, w2) == 1:
                adj[w1].append(w2)
                adj[w2].append(w1)
                edges.add((w1, w2))

    # Connected components (beta_0) via BFS
    visited = set()
    components: list[list[str]] = []
    for w in unique_worlds:
        if w not in visited:
            comp = []
            queue = [w]
            visited.add(w)
            while queue:
                curr = queue.pop(0)
                comp.append(curr)
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            components.append(comp)

    beta_0 = len(components)
    edge_count = len(edges)
    # 1st Betti number / cycle rank: beta_1 = |E| - |V| + beta_0
    beta_1 = edge_count - n + beta_0

    # Graph diameter (maximum shortest path within connected components)
    diameter = 0
    for w_start in unique_worlds:
        dist = {w_start: 0}
        q = [w_start]
        while q:
            c = q.pop(0)
            d = dist[c]
            if d > diameter:
                diameter = d
            for nb in adj[c]:
                if nb not in dist:
                    dist[nb] = d + 1
                    q.append(nb)

    # Check if induced subgraph is an affine subcube Q_k
    # A set of worlds is an affine subcube of dimension k iff its size is 2^k,
    # and all elements share identical bits on 6-k coordinates while varying freely on k coordinates.
    is_subcube = False
    subcube_dim = None

    # Check powers of 2: 1, 2, 4, 8, 16, 32, 64
    if n in (1, 2, 4, 8, 16, 32, 64):
        k = (n - 1).bit_length()
        # Find coordinates that are invariant across all worlds
        fixed_coords = []
        for bit_idx in range(6):
            vals = {w[bit_idx] for w in unique_worlds}
            if len(vals) == 1:
                fixed_coords.append(bit_idx)
        if len(fixed_coords) == (6 - k):
            is_subcube = True
            subcube_dim = k

    return {
        "vertex_count": n,
        "edge_count": edge_count,
        "connected_components": beta_0,
        "beta_0": beta_0,
        "beta_1": beta_1,
        "diameter": diameter,
        "is_subcube": is_subcube,
        "dimension": subcube_dim,
    }
