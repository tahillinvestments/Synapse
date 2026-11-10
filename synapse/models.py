"""
Data models for SynapseGraph: Modern Hierarchical & Temporal Code Memory.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Any
import time


class LobeType(str, Enum):
    """
    Biological brain functional mapping for AI code memory:
    - FRONTAL: Executive control, core logic, AST symbols (functions, classes).
    - HIPPOCAMPUS: Associative indexing, multi-hop relational bridge nodes.
    - TEMPORAL: Episodic evolution, commit history, invalidation state.
    - PARIETAL: Semantic contracts, types, interfaces, schemas.
    - OCCIPITAL: Sensory/External perception, MCP tool interfaces, API routes.
    """
    FRONTAL = "frontal"          # Core functions, classes, AST logic
    HIPPOCAMPUS = "hippocampus"  # Cross-module associative bridges & PPR index
    TEMPORAL = "temporal"        # Versioning, commit states, temporal diffs
    PARIETAL = "parietal"        # Type systems, data models, schemas
    OCCIPITAL = "occipital"      # External perception, API routes, MCP tools


class EdgeType(str, Enum):
    CALLS = "calls"
    IMPORTS = "imports"
    INHERITS = "inherits"
    USES_TYPE = "uses_type"
    EXPOSES = "exposes"
    EVOLVED_FROM = "evolved_from"
    INVALIDATES = "invalidates"
    ASSOCIATED_WITH = "associated_with"


@dataclass
class SymbolNode:
    id: str                             # Unique symbol identifier e.g. "auth.service:verify_token"
    name: str                           # Short name e.g. "verify_token"
    symbol_type: str                    # "function", "class", "method", "module", "route"
    file_path: str                      # Source file path
    lobe: LobeType                      # Assigned brain lobe
    line_start: int                     # Start line in source
    line_end: int                       # End line in source
    signature: str                      # Def line with params & return type
    docstring: Optional[str] = None     # Docstring summary
    surrogate: str = ""                 # Compressed surrogate interface (tokens ~15-30)
    full_tokens: int = 0                # Original full source token count
    surrogate_tokens: int = 0           # Token count of surrogate interface
    community_id: int = 0               # Louvain / Hierarchical community cluster
    pagerank_score: float = 0.0         # Hippocampal PPR centrality score
    valid_from: float = field(default_factory=time.time)  # Temporal epoch start
    valid_to: Optional[float] = None                      # None means currently active
    commit_sha: str = "HEAD"                              # Commit or revision tag
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.valid_to is None


@dataclass
class MemoryEdge:
    source_id: str
    target_id: str
    edge_type: EdgeType
    weight: float = 1.0
    valid_from: float = field(default_factory=time.time)
    valid_to: Optional[float] = None
    commit_sha: str = "HEAD"
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_active(self) -> bool:
        return self.valid_to is None


@dataclass
class RetrievalResult:
    query: str
    subgraph_nodes: List[SymbolNode]
    subgraph_edges: List[MemoryEdge]
    seed_nodes: List[str]
    ppr_scores: Dict[str, float]
    tokens_original: int
    tokens_retrieved: int
    token_savings_pct: float
    hops_resolved: int
    execution_time_ms: float
