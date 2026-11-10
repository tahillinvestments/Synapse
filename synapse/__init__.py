"""
SynapseGraph: Neuro-inspired Hierarchical & Temporal Code Memory Engine.
"""

from synapse.models import SymbolNode, MemoryEdge, LobeType, EdgeType, RetrievalResult
from synapse.engine import SynapseMemoryEngine
from synapse.parser import CodebaseParser
from synapse.hippocampus import HippocampalEngine
from synapse.temporal import TemporalTracker
from synapse.hierarchical import HierarchicalCompressor

__version__ = "2.6.0"
__all__ = [
    "SynapseMemoryEngine",
    "SymbolNode",
    "MemoryEdge",
    "LobeType",
    "EdgeType",
    "RetrievalResult",
    "CodebaseParser",
    "HippocampalEngine",
    "TemporalTracker",
    "HierarchicalCompressor",
]
