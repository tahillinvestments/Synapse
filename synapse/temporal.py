"""
Graphiti-inspired Temporal Epistemic Graph Tracker.
Maintains temporal validity windows [valid_from, valid_to], historical commit checkpoints,
and handles edge invalidation during code evolution.
"""

from typing import Dict, List, Optional, Tuple
import time
from synapse_graph.models import SymbolNode, MemoryEdge, EdgeType, LobeType


class TemporalTracker:
    """
    Tracks code graph evolution over time. Prevents LLM hallucinations caused by stale
    code representations by invalidating obsolete edges and tracking evolutionary lineage.
    """

    def __init__(self):
        self.commit_history: List[str] = []

    def record_commit(self, commit_sha: str):
        if commit_sha not in self.commit_history:
            self.commit_history.append(commit_sha)

    def invalidate_symbol(self, nodes: Dict[str, SymbolNode], edges: List[MemoryEdge], symbol_id: str, commit_sha: str):
        """Marks a symbol and its connected edges as invalidated at the given commit."""
        now = time.time()
        if symbol_id in nodes:
            nodes[symbol_id].valid_to = now
            nodes[symbol_id].lobe = LobeType.TEMPORAL # Moves to temporal memory archives
            nodes[symbol_id].metadata["invalidated_in_commit"] = commit_sha

        for edge in edges:
            if edge.is_active and (edge.source_id == symbol_id or edge.target_id == symbol_id):
                edge.valid_to = now
                edge.metadata["invalidated_in_commit"] = commit_sha

    def evolve_symbol(
        self,
        nodes: Dict[str, SymbolNode],
        edges: List[MemoryEdge],
        old_symbol_id: str,
        new_node: SymbolNode,
        commit_sha: str
    ):
        """Replaces an obsolete symbol with an evolved version, recording the evolutionary edge."""
        self.invalidate_symbol(nodes, edges, old_symbol_id, commit_sha)
        nodes[new_node.id] = new_node
        
        # Add evolutionary edge
        edge = MemoryEdge(
            source_id=new_node.id,
            target_id=old_symbol_id,
            edge_type=EdgeType.EVOLVED_FROM,
            valid_from=time.time(),
            commit_sha=commit_sha,
            metadata={"evolution": "refactored"}
        )
        edges.append(edge)

    def get_temporal_snapshot(
        self,
        nodes: Dict[str, SymbolNode],
        edges: List[MemoryEdge],
        target_timestamp: Optional[float] = None
    ) -> Tuple[List[SymbolNode], List[MemoryEdge]]:
        """Returns the active nodes and edges at a specific point in time."""
        t = target_timestamp or time.time()
        
        snapshot_nodes = [
            n for n in nodes.values()
            if n.valid_from <= t and (n.valid_to is None or n.valid_to > t)
        ]
        snapshot_edges = [
            e for e in edges
            if e.valid_from <= t and (e.valid_to is None or e.valid_to > t)
        ]
        return snapshot_nodes, snapshot_edges
