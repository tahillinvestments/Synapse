"""
Hierarchical Graph Memory & Modularity Clustering (HiGram / LightRAG / GAM).
Partitions code graph into coarse-to-fine structures:
- Level 0: Macro Communities (Subsystems / Modules)
- Level 1: Micrographs (Files / Classes)
- Level 2: Atomic Symbol Units (Methods / Signatures)
Pure-Python zero-dependency implementation with optional NetworkX acceleration.
"""

from typing import Dict, List, Set, Any
from synapse_graph.models import SymbolNode, MemoryEdge


class HierarchicalCompressor:
    """Computes coarse-to-fine community partitioning for token-efficient hierarchical zoom."""

    def __init__(self):
        pass

    def compute_communities(self, nodes: Dict[str, SymbolNode], edges: List[MemoryEdge]) -> Dict[str, int]:
        """Runs community detection on active graph."""
        active_nodes = [nid for nid, n in nodes.items() if n.is_active]
        if not active_nodes:
            return {}

        try:
            import networkx as nx
            G = nx.Graph()
            for nid in active_nodes:
                G.add_node(nid)
            for edge in edges:
                if edge.is_active and edge.source_id in nodes and edge.target_id in nodes:
                    G.add_edge(edge.source_id, edge.target_id, weight=edge.weight)
            try:
                communities = list(nx.community.greedy_modularity_communities(G))
            except Exception:
                communities = list(nx.connected_components(G))
        except ImportError:
            adj: Dict[str, Set[str]] = {nid: set() for nid in active_nodes}
            for edge in edges:
                if edge.is_active and edge.source_id in adj and edge.target_id in adj:
                    adj[edge.source_id].add(edge.target_id)
                    adj[edge.target_id].add(edge.source_id)

            visited = set()
            communities = []
            for nid in active_nodes:
                if nid not in visited:
                    comp = set()
                    queue = [nid]
                    visited.add(nid)
                    while queue:
                        curr = queue.pop(0)
                        comp.add(curr)
                        for neighbor in adj.get(curr, []):
                            if neighbor not in visited:
                                visited.add(neighbor)
                                queue.append(neighbor)
                    communities.append(comp)

        node_community_map: Dict[str, int] = {}
        for comm_id, comm_set in enumerate(communities):
            for nid in comm_set:
                node_community_map[nid] = comm_id
                if nid in nodes:
                    nodes[nid].community_id = comm_id

        return node_community_map

    def get_cluster_summaries(self, nodes: Dict[str, SymbolNode], node_community_map: Dict[str, int]) -> Dict[int, Dict[str, Any]]:
        """Synthesizes high-level macro cluster summaries."""
        clusters: Dict[int, List[SymbolNode]] = {}
        for nid, comm_id in node_community_map.items():
            if nid in nodes:
                clusters.setdefault(comm_id, []).append(nodes[nid])

        summaries = {}
        for comm_id, c_nodes in clusters.items():
            symbols_count = len(c_nodes)
            files = list({n.file_path for n in c_nodes})
            dominant_lobe = max(set(n.lobe for n in c_nodes), key=lambda l: sum(1 for n in c_nodes if n.lobe == l))
            full_toks = sum(n.full_tokens for n in c_nodes)
            surr_toks = sum(n.surrogate_tokens for n in c_nodes)

            summaries[comm_id] = {
                "community_id": comm_id,
                "symbol_count": symbols_count,
                "files": files,
                "dominant_lobe": dominant_lobe.value,
                "full_tokens": full_toks,
                "surrogate_tokens": surr_toks,
                "compression_ratio": round(full_toks / max(1, surr_toks), 1),
                "top_symbols": [n.name for n in c_nodes[:5]]
            }

        return summaries
