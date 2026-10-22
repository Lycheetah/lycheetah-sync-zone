"""
d_separation.py
Pure Python implementation of Directed Acyclic Graphs (DAGs) and
Pearl's d-separation algorithm via active trail search.

Author: Aeon (Gemini Cohort, Lycheetah Sync Zone)
Date: 2026-10-23
"""

from __future__ import annotations
from collections import deque
from typing import Any, Iterable, Sequence


class CausalDAG:
    """
    A Directed Acyclic Graph (DAG) for causal modeling, structural inference,
    and d-separation active trail search.
    """

    def __init__(self, nodes: Iterable[str] | None = None, edges: Iterable[tuple[str, str]] | None = None):
        self._nodes: set[str] = set()
        self._children: dict[str, set[str]] = {}
        self._parents: dict[str, set[str]] = {}

        if nodes:
            for node in nodes:
                self.add_node(node)

        if edges:
            for u, v in edges:
                self.add_edge(u, v)

    @property
    def nodes(self) -> set[str]:
        """Return the set of all node identifiers."""
        return set(self._nodes)

    @property
    def edges(self) -> set[tuple[str, str]]:
        """Return the set of all directed edges (u, v) where u -> v."""
        result = set()
        for u, children in self._children.items():
            for v in children:
                result.add((u, v))
        return result

    def add_node(self, node: str) -> None:
        """Add a node to the DAG."""
        if node not in self._nodes:
            self._nodes.add(node)
            self._children[node] = set()
            self._parents[node] = set()

    def add_nodes_from(self, nodes: Iterable[str]) -> None:
        """Add multiple nodes to the DAG."""
        for n in nodes:
            self.add_node(n)

    def add_edge(self, u: str, v: str) -> None:
        """
        Add a directed edge u -> v (u causes v).
        Raises ValueError if adding the edge would introduce a cycle.
        """
        if u == v:
            raise ValueError(f"Self-loops are not permitted in a causal DAG: {u} -> {v}")

        self.add_node(u)
        self.add_node(v)

        if v in self._children[u]:
            return  # Edge already exists

        # Check if v is an ancestor of u (which would form a cycle v ... -> u -> v)
        if v in self.ancestors(u):
            raise ValueError(f"Adding directed edge {u} -> {v} introduces a cycle; graph must remain acyclic.")

        self._children[u].add(v)
        self._parents[v].add(u)

    def add_edges_from(self, edges: Iterable[tuple[str, str]]) -> None:
        """Add multiple directed edges."""
        for u, v in edges:
            self.add_edge(u, v)

    def has_node(self, node: str) -> bool:
        """Check if node exists in the DAG."""
        return node in self._nodes

    def has_edge(self, u: str, v: str) -> bool:
        """Check if directed edge u -> v exists."""
        return u in self._nodes and v in self._children.get(u, set())

    def parents(self, node: str) -> set[str]:
        """Return immediate causal parents of node (PA_i)."""
        if node not in self._nodes:
            raise KeyError(f"Node '{node}' not found in DAG.")
        return set(self._parents[node])

    def children(self, node: str) -> set[str]:
        """Return immediate causal children of node (CH_i)."""
        if node not in self._nodes:
            raise KeyError(f"Node '{node}' not found in DAG.")
        return set(self._children[node])

    def ancestors(self, nodes: str | Iterable[str]) -> set[str]:
        """
        Return all ancestors of the given node(s), including the nodes themselves.
        """
        targets = {nodes} if isinstance(nodes, str) else set(nodes)
        visited = set()
        queue = deque(t for t in targets if t in self._nodes)

        while queue:
            curr = queue.popleft()
            if curr not in visited:
                visited.add(curr)
                for p in self._parents.get(curr, ()):
                    if p not in visited:
                        queue.append(p)

        return visited

    def descendants(self, nodes: str | Iterable[str]) -> set[str]:
        """
        Return all descendants of the given node(s), including the nodes themselves.
        """
        targets = {nodes} if isinstance(nodes, str) else set(nodes)
        visited = set()
        queue = deque(t for t in targets if t in self._nodes)

        while queue:
            curr = queue.popleft()
            if curr not in visited:
                visited.add(curr)
                for c in self._children.get(curr, ()):
                    if c not in visited:
                        queue.append(c)

        return visited

    def is_dag(self) -> bool:
        """Verify that the graph is acyclic using Kahn's algorithm."""
        in_degrees = {n: len(self._parents[n]) for n in self._nodes}
        zero_in = deque([n for n, d in in_degrees.items() if d == 0])
        count = 0

        while zero_in:
            node = zero_in.popleft()
            count += 1
            for child in self._children[node]:
                in_degrees[child] -= 1
                if in_degrees[child] == 0:
                    zero_in.append(child)

        return count == len(self._nodes)

    def topological_sort(self) -> list[str]:
        """Return a topological ordering of the nodes."""
        in_degrees = {n: len(self._parents[n]) for n in self._nodes}
        zero_in = deque(sorted([n for n, d in in_degrees.items() if d == 0]))
        order = []

        while zero_in:
            node = zero_in.popleft()
            order.append(node)
            for child in sorted(self._children[node]):
                in_degrees[child] -= 1
                if in_degrees[child] == 0:
                    zero_in.append(child)

        if len(order) != len(self._nodes):
            raise ValueError("Graph contains a cycle; cannot produce topological ordering.")
        return order

    def markov_blanket(self, node: str) -> set[str]:
        r"""
        Return the Markov Blanket of a node:
        MB(node) = Parents(node) U Children(node) U Parents(Children(node)) \ {node}.
        Conditioned on its Markov blanket, a node is d-separated from all other nodes.
        """
        if node not in self._nodes:
            raise KeyError(f"Node '{node}' not found in DAG.")

        mb = set(self._parents[node]) | set(self._children[node])
        for child in self._children[node]:
            mb.update(self._parents[child])
        mb.discard(node)
        return mb

    # -------------------------------------------------------------------------
    # d-Separation & Active Trail Search
    # -------------------------------------------------------------------------

    def is_trail_active(self, trail: Sequence[str], conditioning_set: Iterable[str] | None = None) -> bool:
        """
        Directly test if a specific trail (sequence of nodes) is active given Z.
        A trail is active if:
        1. Every collider on the trail has a descendant in Z (including itself).
        2. Every non-collider on the trail is not in Z.
        """
        if len(trail) < 2:
            return True

        z_set = self._normalize_set(conditioning_set)
        z_anc = self.ancestors(z_set)

        # Check validity of steps along the trail
        for i in range(len(trail) - 1):
            u, v = trail[i], trail[i + 1]
            if not (self.has_edge(u, v) or self.has_edge(v, u)):
                raise ValueError(f"Trail step ({u}, {v}) is not an edge in the DAG.")

        # Check intermediate nodes
        for i in range(1, len(trail) - 1):
            prev_node = trail[i - 1]
            curr_node = trail[i]
            next_node = trail[i + 1]

            # Collider: prev -> curr <- next
            is_collider = self.has_edge(prev_node, curr_node) and self.has_edge(next_node, curr_node)

            if is_collider:
                # Collider is active iff curr_node or one of its descendants is in Z
                if curr_node not in z_anc:
                    return False
            else:
                # Non-collider (chain or fork) is active iff curr_node not in Z
                if curr_node in z_set:
                    return False

        return True

    def find_active_trail(
        self,
        start_nodes: str | Iterable[str],
        target_nodes: str | Iterable[str],
        conditioning_set: Iterable[str] | None = None,
    ) -> list[str] | None:
        """
        Search for an active trail between start_nodes (X) and target_nodes (Y)
        given conditioning_set (Z) using active trail BFS (Geiger, Verma, Pearl 1990).

        Returns:
            A list of node IDs representing the active trail if one exists,
            or None if X and Y are d-separated given Z.
        """
        X = self._normalize_set(start_nodes)
        Y = self._normalize_set(target_nodes)
        Z = self._normalize_set(conditioning_set)

        # Check self / intersection
        overlap = X & Y
        if overlap:
            common = sorted(overlap)[0]
            return [common]

        z_anc = self.ancestors(Z)

        # Direction constants for edge traversal
        FROM_PARENT = 1  # Arrived via directed edge: parent -> curr_node
        FROM_CHILD = -1  # Arrived via directed edge: child -> curr_node

        # BFS queue stores: (curr_node, arrival_dir, path)
        queue: deque[tuple[str, int, list[str]]] = deque()
        visited: set[tuple[str, int]] = set()

        # Seed from start nodes X
        for x in X:
            if x not in self._nodes:
                continue
            # Trails can initiate from x along outgoing edges (x -> child)
            for child in sorted(self._children[x]):
                path = [x, child]
                if child in Y:
                    return path
                state = (child, FROM_PARENT)
                if state not in visited:
                    visited.add(state)
                    queue.append((child, FROM_PARENT, path))

            # Trails can initiate from x along incoming edges (x <- parent)
            for parent in sorted(self._parents[x]):
                path = [x, parent]
                if parent in Y:
                    return path
                state = (parent, FROM_CHILD)
                if state not in visited:
                    visited.add(state)
                    queue.append((parent, FROM_CHILD, path))

        while queue:
            curr_node, arrival_dir, path = queue.popleft()

            if curr_node in Y:
                return path

            # Move 1: Traverse to children (curr_node -> next_child)
            # This represents:
            # - Chain: parent -> curr_node -> next_child (if arrival_dir == FROM_PARENT)
            # - Fork:  child  <- curr_node -> next_child (if arrival_dir == FROM_CHILD)
            # Both are non-colliders; active iff curr_node not in Z.
            if curr_node not in Z:
                for child in sorted(self._children[curr_node]):
                    if child in path:
                        continue  # Keep trails simple
                    next_path = path + [child]
                    if child in Y:
                        return next_path
                    state = (child, FROM_PARENT)
                    if state not in visited:
                        visited.add(state)
                        queue.append((child, FROM_PARENT, next_path))

            # Move 2: Traverse to parents (curr_node <- next_parent)
            # This represents:
            # - Collider: parent -> curr_node <- next_parent (if arrival_dir == FROM_PARENT)
            #   Active iff curr_node or a descendant is in Z (i.e. curr_node in z_anc).
            # - Chain:    child  <- curr_node <- next_parent (if arrival_dir == FROM_CHILD)
            #   Active iff curr_node not in Z.
            if arrival_dir == FROM_PARENT:
                if curr_node in z_anc:
                    for parent in sorted(self._parents[curr_node]):
                        if parent in path:
                            continue
                        next_path = path + [parent]
                        if parent in Y:
                            return next_path
                        state = (parent, FROM_CHILD)
                        if state not in visited:
                            visited.add(state)
                            queue.append((parent, FROM_CHILD, next_path))
            else:  # arrival_dir == FROM_CHILD
                if curr_node not in Z:
                    for parent in sorted(self._parents[curr_node]):
                        if parent in path:
                            continue
                        next_path = path + [parent]
                        if parent in Y:
                            return next_path
                        state = (parent, FROM_CHILD)
                        if state not in visited:
                            visited.add(state)
                            queue.append((parent, FROM_CHILD, next_path))

        return None

    def is_d_separated(
        self,
        X: str | Iterable[str],
        Y: str | Iterable[str],
        Z: Iterable[str] | None = None,
    ) -> bool:
        """
        Test whether X and Y are d-separated given conditioning set Z.

        Returns:
            True if X and Y are d-separated given Z (no active trail exists).
            False if X and Y are d-connected given Z (at least one active trail exists).
        """
        trail = self.find_active_trail(X, Y, Z)
        return trail is None

    def all_simple_trails(self, start: str, target: str) -> list[list[str]]:
        """
        Exhaustively find all simple trails (undirected paths) between start and target.
        Used for verification and small-graph pedagogical inspection.
        """
        if start not in self._nodes or target not in self._nodes:
            return []

        trails: list[list[str]] = []

        def dfs(curr: str, path: list[str], visited: set[str]):
            if curr == target:
                trails.append(list(path))
                return
            # Neighbors in undirected skeleton
            neighbors = self._children.get(curr, set()) | self._parents.get(curr, set())
            for nbr in sorted(neighbors):
                if nbr not in visited:
                    visited.add(nbr)
                    path.append(nbr)
                    dfs(nbr, path, visited)
                    path.pop()
                    visited.remove(nbr)

        dfs(start, [start], {start})
        return trails

    def is_backdoor_admissible(self, treatment: str, outcome: str, adjustment_set: Iterable[str]) -> bool:
        """
        Test whether a set S satisfies Pearl's Back-Door Criterion relative to (treatment, outcome):
        1. No node in S is a descendant of treatment.
        2. S blocks every back-door path between treatment and outcome
           (every path starting with an incoming arrow into treatment).
        """
        S = self._normalize_set(adjustment_set)
        desc_x = self.descendants(treatment)

        # Condition 1: S must not contain descendants of treatment
        if any(s in desc_x for s in S):
            return False

        # Build modified graph without outgoing edges from treatment (severing front-door causal paths)
        # In G_under_X (outgoing arrows from treatment removed), S must d-separate treatment and outcome.
        mutilated = CausalDAG(nodes=self.nodes)
        for u, v in self.edges:
            if u == treatment:
                continue  # Sever outgoing arrow
            mutilated.add_edge(u, v)

        return mutilated.is_d_separated(treatment, outcome, S)

    @staticmethod
    def _normalize_set(val: Any) -> set[str]:
        if val is None:
            return set()
        if isinstance(val, str):
            return {val}
        return set(val)
