"""
ARP v3 Drug Discovery Package

Modules:
- peptgene: Peptide generation with ACP-ConditionalDiffusion concept
"""

from .peptgene import (
    PeptideCandidate,
    PeptideGenerator,
    TARGET_DATABASE,
    get_targets_for_research,
)

__all__ = [
    "PeptideCandidate",
    "PeptideGenerator", 
    "TARGET_DATABASE",
    "get_targets_for_research",
]
