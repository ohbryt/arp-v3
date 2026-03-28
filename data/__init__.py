"""
ARP v3 Data Modules

Modules:
- peptgene: Peptide generation with ACP-ConditionalDiffusion concept
- multimodal: Gemini Embedding 2 for text/image/video/audio/PDF embedding
"""

from .peptgene import (
    PeptideCandidate,
    PeptideGenerator,
    TARGET_DATABASE,
    get_targets_for_research,
)

from .multimodal import (
    MultimodalEmbedder,
    EmbeddingResult,
    SimpleVectorStore,
)

__all__ = [
    # Peptide generation
    "PeptideCandidate",
    "PeptideGenerator", 
    "TARGET_DATABASE",
    "get_targets_for_research",
    # Multimodal embedding
    "MultimodalEmbedder",
    "EmbeddingResult",
    "SimpleVectorStore",
]
