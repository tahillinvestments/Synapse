"""
Unified SynapseMemoryEngine: orchestrates parsing, temporal tracking,
hippocampal associative retrieval, and 3D brain spatial mapping.
"""

from typing import Dict, List, Optional, Any, Tuple
import os
import math
import random
import json
from synapse.models import SymbolNode, MemoryEdge, LobeType, EdgeType, RetrievalResult
from synapse.parser import CodebaseParser
from synapse.hippocampus import HippocampalEngine
from synapse.temporal import TemporalTracker
from synapse.hierarchical import HierarchicalCompressor


class SynapseMemoryEngine:
    """
    State-of-the-art Cognitive Code Memory System.
    Combines:
    1. Zero-LLM Tree-Sitter / AST Programmatic Ingestion (Codebase-Memory)
    2. HippoRAG Personalized PageRank Associative Retrieval
    3. Graphiti-style Temporal Epistemic Graph Invalidation
    4. Hierarchical Modularity & Community Compression (HiGram)
    5. 3D Spatial Brain Coordinate Mapping
    """

    def __init__(self):
        self.nodes: Dict[str, SymbolNode] = {}
        self.edges: List[MemoryEdge] = []
        self.parser = CodebaseParser()
        self.hippocampus = HippocampalEngine()
        self.temporal = TemporalTracker()
        self.hierarchical = HierarchicalCompressor()

    def ingest_source_code(self, file_path: str, source_code: str, commit_sha: str = "HEAD"):
        """Parses and ingests a source file into the memory graph."""
        nodes, edges = self.parser.parse_python_source(file_path, source_code, commit_sha=commit_sha)
        for n in nodes:
            self.nodes[n.id] = n
        self.edges.extend(edges)
        self.temporal.record_commit(commit_sha)
        self._resolve_unbound_calls()

    def ingest_directory(self, root_dir: str, commit_sha: str = "HEAD", max_files: int = 50):
        """Scans a directory and ingests all Python files."""
        count = 0
        for dirpath, _, filenames in os.walk(root_dir):
            for f in filenames:
                if f.endswith(".py") and not f.startswith("."):
                    full_path = os.path.join(dirpath, f)
                    rel_path = os.path.relpath(full_path, root_dir)
                    try:
                        with open(full_path, "r", encoding="utf-8", errors="ignore") as fp:
                            code = fp.read()
                        self.ingest_source_code(rel_path, code, commit_sha=commit_sha)
                        count += 1
                        if count >= max_files:
                            break
                    except Exception as e:
                        print(f"Error reading {rel_path}: {e}")
            if count >= max_files:
                break

        self.rebuild_topology()

    def _resolve_unbound_calls(self):
        """Matches unresolved call targets to known function/class node IDs."""
        known_names = {n.name: n.id for n in self.nodes.values() if n.symbol_type in ("function", "method", "class", "route")}
        for edge in self.edges:
            if edge.edge_type == EdgeType.CALLS and edge.target_id not in self.nodes:
                target_short = edge.target_id.split(":")[-1]
                if target_short in known_names:
                    edge.target_id = known_names[target_short]

    def rebuild_topology(self):
        """Re-computes Louvain communities and baseline PageRank."""
        self._resolve_unbound_calls()
        self.hierarchical.compute_communities(self.nodes, self.edges)
        
        # Compute baseline global PageRank
        baseline_ppr = self.hippocampus.run_personalized_pagerank(
            self.nodes, self.edges, seed_node_ids=list(self.nodes.keys())
        )
        for nid, score in baseline_ppr.items():
            if nid in self.nodes:
                self.nodes[nid].pagerank_score = score

    def query(self, query_text: str, top_k: int = 10) -> RetrievalResult:
        """
        Associative recall via HippoRAG Personalized PageRank.
        Finds query seeds and propagates activation energy across code topologies.
        """
        query_lower = query_text.lower()
        query_tokens = set(query_lower.replace("_", " ").replace(".", " ").replace(":", " ").split())

        # Match seeds
        seed_candidates: List[Tuple[str, float]] = []
        for nid, node in self.nodes.items():
            if not node.is_active:
                continue
            name_parts = set(node.name.lower().split("_"))
            overlap = len(query_tokens.intersection(name_parts))
            
            if node.name.lower() in query_lower:
                seed_candidates.append((nid, 3.0))
            elif overlap > 0:
                seed_candidates.append((nid, 1.0 + overlap))
            elif any(t in node.signature.lower() for t in query_tokens):
                seed_candidates.append((nid, 0.8))
            elif node.docstring and any(t in node.docstring.lower() for t in query_tokens):
                seed_candidates.append((nid, 0.5))

        seed_candidates.sort(key=lambda x: x[1], reverse=True)
        seeds = [s[0] for s in seed_candidates[:4]]
        if not seeds and self.nodes:
            # Fallback to top degree or first node
            seeds = [list(self.nodes.keys())[0]]

        return self.hippocampus.extract_associative_subgraph(
            self.nodes, self.edges, query=query_text, seed_node_ids=seeds, top_k=top_k
        )

    def simulate_temporal_evolution(self, symbol_to_refactor: str, new_symbol_name: str, commit_sha: str = "v2.0-refactor"):
        """Demonstrates Graphiti-style edge invalidation during refactor."""
        if symbol_to_refactor not in self.nodes:
            return None

        old = self.nodes[symbol_to_refactor]
        new_id = old.id.replace(old.name, new_symbol_name)
        new_node = SymbolNode(
            id=new_id,
            name=new_symbol_name,
            symbol_type=old.symbol_type,
            file_path=old.file_path,
            lobe=LobeType.FRONTAL,
            line_start=old.line_start,
            line_end=old.line_end,
            signature=old.signature.replace(old.name, new_symbol_name),
            docstring=f"Refactored non-blocking replacement for {old.name}",
            surrogate=f"def {new_symbol_name}(...): [Refactored High-Performance]",
            full_tokens=old.full_tokens,
            surrogate_tokens=old.surrogate_tokens,
            commit_sha=commit_sha,
            tags=["refactored", "active"]
        )

        self.temporal.evolve_symbol(self.nodes, self.edges, old.id, new_node, commit_sha)
        self.rebuild_topology()
        return new_node

    def export_3d_brain_data(self) -> Dict[str, Any]:
        """
        Calculates 3D spatial coordinates inside an anatomically-inspired brain volume:
        - Frontal Lobe: +Z, +Y (Anterior / Upper)
        - Hippocampus: Center Core (Medial Temporal Lobe, curved arch)
        - Temporal Lobe: Lateral -Y, lower sides
        - Parietal Lobe: Top dorsal, mid-to-posterior +Y, mid-Z
        - Occipital Lobe: Posterior -Z (Sensory / Visual Cortex)
        """
        brain_nodes = []
        random.seed(42)

        for nid, node in self.nodes.items():
            lobe = node.lobe
            # Base position by functional lobe with organic jitter
            if lobe == LobeType.FRONTAL:
                # Anterior forehead region
                base_x = (random.random() - 0.5) * 80.0
                base_y = 15.0 + random.random() * 45.0
                base_z = 35.0 + random.random() * 45.0
                color = "#38bdf8" # Sky blue
            elif lobe == LobeType.HIPPOCAMPUS:
                # Deep medial core arch
                side = 1 if random.random() > 0.5 else -1
                theta = random.random() * math.pi
                base_x = side * (18.0 + math.sin(theta) * 15.0)
                base_y = -10.0 + math.cos(theta) * 15.0
                base_z = -10.0 + (random.random() - 0.5) * 20.0
                color = "#f43f5e" # Rose / Vibrant pink
            elif lobe == LobeType.TEMPORAL:
                # Lower lateral sides
                side = 1 if random.random() > 0.5 else -1
                base_x = side * (45.0 + random.random() * 30.0)
                base_y = -25.0 + random.random() * 30.0
                base_z = -15.0 + random.random() * 40.0
                color = "#eab308" # Amber / Golden
            elif lobe == LobeType.PARIETAL:
                # Superior dorsal crown
                base_x = (random.random() - 0.5) * 75.0
                base_y = 40.0 + random.random() * 35.0
                base_z = -15.0 + random.random() * 40.0
                color = "#a855f7" # Purple
            else: # OCCIPITAL
                # Posterior back of head
                base_x = (random.random() - 0.5) * 60.0
                base_y = -15.0 + random.random() * 35.0
                base_z = -55.0 - random.random() * 30.0
                color = "#10b981" # Emerald / Green

            # Degree count
            deg = sum(1 for e in self.edges if (e.source_id == nid or e.target_id == nid) and e.is_active)

            node_dict = {
                "id": node.id,
                "name": node.name,
                "type": node.symbol_type,
                "file": node.file_path,
                "lobe": node.lobe.value,
                "signature": node.signature,
                "docstring": node.docstring or "No docstring available",
                "surrogate": node.surrogate,
                "full_tokens": node.full_tokens,
                "surrogate_tokens": node.surrogate_tokens,
                "community": node.community_id,
                "pagerank": round(node.pagerank_score * 1000, 2),
                "is_active": node.is_active,
                "commit": node.commit_sha,
                "degree": deg,
                "x": round(base_x, 2),
                "y": round(base_y, 2),
                "z": round(base_z, 2),
                "color": color
            }
            try:
                from synapse.personas import enrich_node_with_persona
                node_dict = enrich_node_with_persona(node_dict)
            except Exception:
                pass

            brain_nodes.append(node_dict)

        brain_edges = []
        for e in self.edges:
            if e.source_id in self.nodes and e.target_id in self.nodes:
                brain_edges.append({
                    "source": e.source_id,
                    "target": e.target_id,
                    "type": e.edge_type.value,
                    "weight": e.weight,
                    "is_active": e.is_active,
                    "commit": e.commit_sha
                })

        return {
            "nodes": brain_nodes,
            "edges": brain_edges,
            "stats": {
                "total_nodes": len(brain_nodes),
                "total_edges": len(brain_edges),
                "active_nodes": sum(1 for n in brain_nodes if n["is_active"]),
                "active_edges": sum(1 for e in brain_edges if e["is_active"]),
                "total_full_tokens": sum(n["full_tokens"] for n in brain_nodes),
                "total_surrogate_tokens": sum(n["surrogate_tokens"] for n in brain_nodes),
                "overall_token_compression": round(
                    sum(n["full_tokens"] for n in brain_nodes) /
                    max(1, sum(n["surrogate_tokens"] for n in brain_nodes)), 1
                )
            }
        }
