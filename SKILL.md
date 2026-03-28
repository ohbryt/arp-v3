# ARP v4 — Hyper-Agent Research Pipeline

> Multi-LLM team with Knowledge Graph CoT + Drug Discovery + Multimodal Embedding + Social Trend Intelligence + Advanced Reasoning + AI Scientist

## Overview

ARP v4 is an autonomous research pipeline that combines:

- **HyperAgents (ICLR 2026)** — Self-evolving meta-agent
- **AgentScope (Alibaba)** — Fault tolerance and pipeline abstraction
- **Morrissette's KG-CoT** — Knowledge Graph for real-time correction in chain-of-thought
- **AI Scientist (Nature 2026)** — Fully automated paper generation with peer review
- **ARC-AGI-3** — Abstraction and reasoning benchmark
- **ACP-ConditionalDiffusion** — Diffusion-based peptide generation for drug discovery
- **Chandra OCR** — Document intelligence for PDF extraction
- **Gemini Embedding 2** — Unified multimodal embedding (text/image/video/audio/PDF)
- **last30days** — Social trend intelligence (Reddit, HN, Polymarket, Bluesky, X)
- **System 2 Reasoning** — Slow, deliberate reasoning with self-verification
- **RunPod GPU** — Cloud GPU for AI Scientist execution

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  HYPER LAYER (KG-CoT Enhanced)                            │
│  • Pre-check: Query KG before each agent execution         │
│  • Post-evaluate: Learn from results                      │
│  • Intervene mid-chain to prevent known failures           │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  REASONING LAYER (System 2)                              │
│  • Chain-of-Thought reasoning                              │
│  • Chain-of-Verification (reduce hallucinations)           │
│  • Abstraction & pattern recognition (ARC-AGI style)        │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  AI SCIENTIST LAYER (Nature 2026)                        │
│  • Idea generation → Code → Experiment → Paper → Review   │
│  • Runs on RunPod GPU (cloud)                             │
│  • Peer review quality assessment                          │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  KNOWLEDGE GRAPH                                          │
│  • Stores observed outcomes (success/failure)              │
│  • Pattern matching against historical mistakes             │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  SOCIAL INTELLIGENCE (last30days)                         │
│  • Reddit, X, HN, Polymarket, Bluesky, YouTube           │
│  • Real-time community trends and sentiment                │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  BASE AGENT LAYER                                         │
│  Lead + Researcher + Analyst + Reviewer + Debater        │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  MULTIMODAL MODULES                                       │
│  • Gemini Embedding 2 (text/image/video/audio/PDF)         │
│  • Chandra OCR (document extraction)                      │
│  • Drug Discovery (peptide generation)                     │
└────────────────────────────────────────────────────────────┘
```

## Run Modes

### 1. CPU Mode (Free)
```bash
python3 run.py "SIRT3 research"                    # Reasoning
python3 orchestrator.py "topic"                  # Research agents
python3 discovery_pipeline.py "drug target"       # Drug discovery
```

### 2. GPU Mode (RunPod)
```bash
# Requires RUNPOD_API_KEY
export RUNPOD_API_KEY=your_key
python3 run_aiscientist.py --gpu "AI Scientist experiment"
```

## GPU Options (RunPod)

| GPU | Price/hr | Use Case |
|-----|----------|----------|
| RTX 3090 | $0.40 | Standard AI Scientist |
| RTX 4090 | $0.50 | Faster experiments |
| A100 | $1.50 | Large experiments |
| H100 | $3.00 | Production runs |

## AI Scientist Pipeline

```
Idea Generation (LLM)
        ↓
Code Writing (LLM)
        ↓
Experiment Execution (RunPod GPU)
        ↓
Paper Writing (LaTeX)
        ↓
Peer Review (AI Scientist)
        ↓
Quality Assessment
```

## Drug Discovery Targets

| Target | Pathway | Priority |
|--------|---------|----------|
| SIRT3 | Mitophagy activation | High |
| PGC-1α | Mitochondrial biogenesis | Medium |
| FOXO3 | Cellular longevity | Medium |
| PD-L1 | Cancer immunotherapy | High |
| TNF-α | Inflammation | High |

## Reasoning Capabilities

### System 2 Reasoning
- Slow, deliberate chain-of-thought
- Self-verification after each step
- Confidence calibration

### Chain-of-Verification
- Extract claims from output
- Verify each claim independently
- Identify contradictions and uncertainties

### ARC-AGI Style Abstraction
- Surface pattern vs deep structure
- Invariant properties
- Transformation rules
- Analogical reasoning

## Inspired By

- [J Morrissette - KG-CoT](https://substack.com)
- [AI Scientist (Nature 2026)](https://www.nature.com/articles/s41586-026-10265-5)
- [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist)
- [ARC-AGI-3 (Symbolica)](https://github.com/symbolica-ai/ARC-AGI-3-Agents)
- [ACP-ConditionalDiffusion](https://github.com/yidingneng/ACP-ConditionalDiffusion)
- [HyperAgents (ICLR 2026)](https://arxiv.org/abs/2502.hyperagents)
- [AgentScope (Alibaba)](https://arxiv.org/html/2402.14034v2)
- [Chandra OCR](https://github.com/datalab-to/chandra)
- [Gemini Embedding 2 (Google)](https://ai.google.dev)
- [last30days (mvanhorn)](https://github.com/mvanhorn/last30days-skill)
- [RunPod](https://runpod.io)
