"""
Relational Kaitiakitanga Causal Provenance DAG & Mauri Integrity Guard
======================================================================
Synthesizes Te Ao Māori relational epistemology with causal provenance graphs,
formalizing Whakapapa (genealogical provenance tracing), Mauri (systemic life-force
and integrity functional M(G) in [0, 1]), Tapu vs Noa access control enforcements,
Whakanoa cryptographic capability clearances, and strict DAG acyclicity invariants.

Concepts:
    - Whakapapa: Genealogical ancestry DAG tracking causal provenance to genesis roots.
    - Mauri M(G): Life-force integrity functional bounded in [0, 1] derived from
      connectivity, structural invariant preservation, and defect dispersion.
    - Tapu: Sacred, restricted high-consequence core state (e.g. genesis invariants).
    - Noa: Unrestricted, common state open for standard reads and mutations.
    - Whakanoa: Cryptographic clearance ceremony unlocking access to Tapu nodes.
    - Kaitiakitanga: Active, ongoing relational stewardship preventing corruption.
"""

from collections import deque
from dataclasses import dataclass, field
import hashlib
import hmac
import json
import time
from typing import Any, Dict, List, Optional, Set, Tuple


class CyclicDependencyError(Exception):
    """Raised when an edge would introduce a circular dependency (temporal grandfather paradox)."""
    pass


class TapuAccessViolation(Exception):
    """Raised when an unauthorized mutation is attempted on a TAPU protected node without Whakanoa clearance."""
    pass


class MauriDegradationAlert(Exception):
    """Raised when the systemic Mauri M(G) drops below the critical threshold, halting execution."""
    pass


@dataclass
class WhakanoaToken:
    """
    Cryptographic capability token permitting state transition on a Tapu node.
    """
    issuer: str
    target_node_id: str
    signature: str
    timestamp: float
    permissions: List[str] = field(default_factory=lambda: ["modify", "audit"])

    def to_dict(self) -> Dict[str, Any]:
        return {
            "issuer": self.issuer,
            "target_node_id": self.target_node_id,
            "signature": self.signature,
            "timestamp": self.timestamp,
            "permissions": self.permissions,
        }


@dataclass
class DAGNode:
    """
    Node in the Causal Provenance DAG.
    """
    id: str
    name: str
    parents: List[str] = field(default_factory=list)   # Matua / Tipuna (ancestors)
    children: List[str] = field(default_factory=list)  # Mokopuna (descendants)
    data: Dict[str, Any] = field(default_factory=dict)
    state: str = "noa"                                 # "tapu" or "noa"
    content_hash: str = ""
    timestamp: float = field(default_factory=time.time)
    invariant_valid: bool = True

    def compute_hash(self) -> str:
        serialized = json.dumps(
            {
                "id": self.id,
                "name": self.name,
                "parents": sorted(self.parents),
                "data": self.data,
                "state": self.state,
                "invariant_valid": self.invariant_valid,
            },
            sort_keys=True
        )
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


class CausalProvenanceDAG:
    """
    Directed Acyclic Graph ensuring Whakapapa lineage, acyclicity, and Tapu protection.
    """

    def __init__(self):
        self.nodes: Dict[str, DAGNode] = {}
        self.genesis_roots: Set[str] = set()

    def add_node(
        self,
        node_id: str,
        name: str = "",
        parents: Optional[List[str]] = None,
        state: str = "noa",
        data: Optional[Dict[str, Any]] = None,
        invariant_valid: bool = True
    ) -> DAGNode:
        """
        Adds a new node to the DAG. If no parents are specified, node is registered as a genesis root.
        """
        if node_id in self.nodes:
            raise ValueError(f"Node {node_id} already exists in DAG.")

        parents = parents or []
        for p in parents:
            if p not in self.nodes:
                raise ValueError(f"Parent {p} does not exist in DAG.")

        node = DAGNode(
            id=node_id,
            name=name or node_id,
            parents=list(parents),
            children=[],
            data=data or {},
            state=state,
            invariant_valid=invariant_valid,
        )
        node.content_hash = node.compute_hash()
        self.nodes[node_id] = node

        if not parents:
            self.genesis_roots.add(node_id)
        else:
            for p in parents:
                self.nodes[p].children.append(node_id)

        return node

    def has_path(self, start: str, target: str, visited: Optional[Set[str]] = None) -> bool:
        """
        Checks whether target is reachable from start along directed edges (children).
        """
        if start == target:
            return True
        if visited is None:
            visited = set()
        visited.add(start)

        for child in self.nodes[start].children:
            if child not in visited:
                if self.has_path(child, target, visited):
                    return True
        return False

    def add_edge(self, parent_id: str, child_id: str):
        """
        Adds a directed edge parent_id -> child_id.
        Verifies the DAG acyclicity invariant: if child_id can reach parent_id,
        adding this edge would create a cycle (grandfather paradox).
        """
        if parent_id not in self.nodes or child_id not in self.nodes:
            raise ValueError(f"Both nodes must exist: {parent_id}, {child_id}")

        if parent_id == child_id:
            raise CyclicDependencyError(f"Self-loop cycle detected on node {parent_id}.")

        # Check if child_id can reach parent_id
        if self.has_path(child_id, parent_id):
            raise CyclicDependencyError(
                f"Cyclic dependency detected: {child_id} is already an ancestor of {parent_id}."
            )

        if child_id not in self.nodes[parent_id].children:
            self.nodes[parent_id].children.append(child_id)
        if parent_id not in self.nodes[child_id].parents:
            self.nodes[child_id].parents.append(parent_id)

        if child_id in self.genesis_roots:
            self.genesis_roots.remove(child_id)

        # Recompute hash
        self.nodes[child_id].content_hash = self.nodes[child_id].compute_hash()

    def trace_whakapapa(self, node_id: str) -> List[str]:
        """
        Traces the complete ancestral lineage (Whakapapa) of node_id back to genesis roots,
        returning the nodes in topological order from ancestors to node_id.
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist.")

        ancestors: Set[str] = set()

        def dfs_ancestors(curr: str):
            for p in self.nodes[curr].parents:
                if p not in ancestors:
                    ancestors.add(p)
                    dfs_ancestors(p)

        dfs_ancestors(node_id)
        all_lineage = ancestors.union({node_id})

        # Topologically sort the lineage subset
        in_degrees: Dict[str, int] = {nid: 0 for nid in all_lineage}
        for nid in all_lineage:
            for child in self.nodes[nid].children:
                if child in all_lineage:
                    in_degrees[child] += 1

        queue = deque(sorted([nid for nid, deg in in_degrees.items() if deg == 0]))
        topo_order: List[str] = []

        while queue:
            curr = queue.popleft()
            topo_order.append(curr)
            for child in sorted(self.nodes[curr].children):
                if child in all_lineage:
                    in_degrees[child] -= 1
                    if in_degrees[child] == 0:
                        queue.append(child)

        return topo_order

    def topological_sort(self) -> List[str]:
        """
        Returns a deterministic, content-addressable topological ordering of all DAG nodes.
        Uses Kahn's algorithm with lexicographical tie-breaking for perfect reproducibility.
        """
        in_degrees: Dict[str, int] = {nid: len(node.parents) for nid, node in self.nodes.items()}
        queue = deque(sorted([nid for nid, deg in in_degrees.items() if deg == 0]))
        ordered: List[str] = []

        while queue:
            curr = queue.popleft()
            ordered.append(curr)
            for child in sorted(self.nodes[curr].children):
                in_degrees[child] -= 1
                if in_degrees[child] == 0:
                    queue.append(child)

        if len(ordered) != len(self.nodes):
            raise CyclicDependencyError("Graph contains an undetected cycle; topological sort impossible.")

        return ordered

    def modify_node(
        self,
        node_id: str,
        new_data: Dict[str, Any],
        whakanoa_token: Optional[WhakanoaToken] = None,
        secret_key: Optional[bytes] = None
    ) -> DAGNode:
        """
        Modifies node data. If node is TAPU, requires a valid WhakanoaToken with valid signature.
        """
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} does not exist.")

        node = self.nodes[node_id]

        if node.state == "tapu":
            if whakanoa_token is None:
                raise TapuAccessViolation(
                    f"Access Denied: Node {node_id} is TAPU. Mutation forbidden without Whakanoa clearance."
                )
            # Verify token
            if not MauriIntegrityGuard.verify_token(whakanoa_token, node_id, secret_key):
                raise TapuAccessViolation(
                    f"Access Denied: Whakanoa token for node {node_id} failed cryptographic validation."
                )

        node.data.update(new_data)
        node.content_hash = node.compute_hash()
        return node


class MauriIntegrityGuard:
    """
    Evaluates the Mauri life-force integrity functional M(G) in [0, 1]
    and guards against state corruption, severing of whakapapa, and entropy collapse.
    """

    DEFAULT_SECRET = b"lycheetah-kaitiaki-whakanoa-secret-key-2026"

    def __init__(self, dag: CausalProvenanceDAG, secret_key: Optional[bytes] = None):
        self.dag = dag
        self.secret_key = secret_key or self.DEFAULT_SECRET
        self.mauri_history: List[float] = [self.compute_mauri()]

    def compute_mauri(self) -> float:
        """
        Computes the Mauri life-force functional M(G) in [0, 1]:
        M(G) = 0.50 * C_conn(G) + 0.40 * I_inv(G) + 0.10 * (1.0 - S_entropy(G))
        Where:
            C_conn    : Ratio of nodes with unbroken Whakapapa connectivity to genesis roots
            I_inv     : Ratio of nodes with verified, intact structural invariants
            S_entropy : Normalized defect dispersion ratio
        """
        n = len(self.dag.nodes)
        if n == 0:
            return 1.0

        # 1. Connectivity to genesis roots
        connected_count = 0
        for nid, node in self.dag.nodes.items():
            if nid in self.dag.genesis_roots:
                connected_count += 1
            else:
                # Check if reachable from any genesis root
                has_root_lineage = any(
                    self.dag.has_path(root, nid) for root in self.dag.genesis_roots
                )
                if has_root_lineage:
                    connected_count += 1
        c_conn = connected_count / float(n)

        # 2. Invariant preservation
        valid_invariants = sum(1 for node in self.dag.nodes.values() if node.invariant_valid)
        i_inv = valid_invariants / float(n)

        # 3. Defect entropy
        unverified_or_broken = sum(1 for node in self.dag.nodes.values() if not node.invariant_valid)
        s_entropy = unverified_or_broken / float(n)

        mauri = 0.50 * c_conn + 0.40 * i_inv + 0.10 * (1.0 - s_entropy)
        return max(0.0, min(1.0, mauri))

    def update_and_check_monotonicity(self) -> Tuple[float, bool]:
        """
        Recalculates M(G), appends to history, and checks dM/dt >= 0 (monotonic preservation).
        """
        new_mauri = self.compute_mauri()
        prev_mauri = self.mauri_history[-1]
        self.mauri_history.append(new_mauri)
        is_monotonic = (new_mauri >= prev_mauri - 1e-12)
        return new_mauri, is_monotonic

    def check_mauri_threshold(self, threshold: float = 0.50) -> float:
        """
        Enforces that Mauri remains above critical threshold; halts if degraded.
        """
        curr_mauri = self.compute_mauri()
        if curr_mauri < threshold:
            raise MauriDegradationAlert(
                f"CRITICAL HALT: Mauri life-force collapsed to {curr_mauri:.4f} < {threshold:.4f}. "
                "Lineage severed or systemic invariants corrupted."
            )
        return curr_mauri

    def issue_whakanoa_token(self, target_node_id: str) -> WhakanoaToken:
        """
        Issues a cryptographically signed Whakanoa clearance token for a Tapu node.
        """
        ts = time.time()
        message = f"WHAKANOA:{target_node_id}:{ts}".encode("utf-8")
        sig = hmac.new(self.secret_key, message, hashlib.sha256).hexdigest()
        return WhakanoaToken(
            issuer="MauriIntegrityGuard",
            target_node_id=target_node_id,
            signature=sig,
            timestamp=ts,
            permissions=["modify", "audit"],
        )

    @staticmethod
    def verify_token(
        token: WhakanoaToken,
        target_node_id: str,
        secret_key: Optional[bytes] = None
    ) -> bool:
        """
        Verifies cryptographic integrity and validity of a Whakanoa token.
        """
        if token.target_node_id != target_node_id:
            return False
        key = secret_key or MauriIntegrityGuard.DEFAULT_SECRET
        message = f"WHAKANOA:{token.target_node_id}:{token.timestamp}".encode("utf-8")
        expected_sig = hmac.new(key, message, hashlib.sha256).hexdigest()
        return hmac.compare_digest(token.signature, expected_sig)
