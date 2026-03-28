# ARP v3 — Hyper-Agent Research Pipeline

> Multi-LLM team with Knowledge Graph CoT + Drug Discovery + Multimodal Embedding

## Concept

Based on J Morrissette's insight: *"Chain-of-thought reasoning is powerful but blind to its own history."*

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  HYPER LAYER (KG-CoT Enhanced)                            │
│  • Pre-check: Query KG before each agent execution        │
│  • Post-evaluate: Learn from results                      │
│  • Intervene mid-chain to prevent known failures          │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  KNOWLEDGE GRAPH                                          │
│  • Stores observed outcomes (success/failure)              │
│  • Pattern matching against historical mistakes            │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  BASE AGENT LAYER                                         │
│  Lead + Researcher + Analyst + Reviewer + Debater          │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  DRUG DISCOVERY MODULE                                    │
│  • Target identification • Peptide generation               │
│  • Validation • Ranking                                    │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  MULTIMODAL EMBEDDING (Gemini Embedding 2)                │
│  • Text • Image • Video • Audio • PDF                     │
│  • MRL dimensions: 3072/1536/768                          │
│  • RAG: Unified semantic search                            │
└────────────────────────────────────────────────────────────┘
```

## Three Modes

### 1. Research Mode (ARP Agents)
```bash
python3 orchestrator.py "<research topic>"
```

### 2. Drug Discovery Mode
```bash
python3 discovery_pipeline.py "<drug target>"
```

### 3. Multimodal RAG Mode
```python
from data.multimodal import MultimodalEmbedder, SimpleVectorStore

embedder = MultimodalEmbedder()  # Needs GOOGLE_API_KEY
store = SimpleVectorStore(embedder)

# Add research materials
store.add_text("SIRT3 mitophagy mechanism...")
store.add_pdf("paper.pdf")

# Search across all modalities
results = store.search("What activates mitophagy?")
```

## Drug Discovery Targets

| Target | Pathway | Priority |
|--------|---------|----------|
| SIRT3 | Mitophagy activation | High |
| PGC-1α | Mitochondrial biogenesis | Medium |
| FOXO3 | Cellular longevity | Medium |
| PD-L1 | Cancer immunotherapy | High |
| TNF-α | Inflammation | High |

## Multimodal Embedding (Gemini Embedding 2)

| Format | Capability |
|--------|------------|
| Text | 8,192 tokens, 100+ languages |
| Image | Up to 6 per request |
| Video | Up to 120 seconds |
| Audio | Direct processing (no transcription) |
| PDF | Direct processing |

**MRL Dimensions:** 3072 (precise) / 1536 (balanced) / 768 (fast)

## Inspired By

- [J Morrissette - KG-CoT](https://substack.com)
- [ACP-ConditionalDiffusion](https://github.com/yidingneng/ACP-ConditionalDiffusion)
- [HyperAgents (ICLR 2026)](https://arxiv.org/abs/2502.hyperagents)
- [AgentScope (Alibaba)](https://arxiv.org/html/2402.14034v2)
- [Chandra OCR](https://github.com/datalab-to/chandra)
- [Gemini Embedding 2 (Google)](https://ai.google.dev)
