# ARP v4 — Hyper-Agent Research Pipeline

> Multi-LLM research team with Knowledge Graph CoT + Drug Discovery + Multimodal Embedding + Social Trend Intelligence

## Overview

ARP v4 is an autonomous research pipeline that combines:

- **HyperAgents (ICLR 2026)** — Self-evolving meta-agent
- **AgentScope (Alibaba)** — Fault tolerance and pipeline abstraction
- **Morrissette's KG-CoT** — Knowledge Graph for real-time correction in chain-of-thought
- **ACP-ConditionalDiffusion** — Diffusion-based peptide generation for drug discovery
- **Chandra OCR** — Document intelligence for PDF extraction
- **Gemini Embedding 2** — Unified multimodal embedding (text/image/video/audio/PDF)
- **last30days** — Social trend intelligence (Reddit, HN, Polymarket, Bluesky, X)

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
│  • Pattern matching against historical mistakes             │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  SOCIAL INTELLIGENCE (last30days)                         │
│  • Reddit, X, HN, Polymarket, Bluesky, YouTube           │
│  • Real-time community trends and sentiment               │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  BASE AGENT LAYER                                         │
│  Lead + Researcher + Analyst + Reviewer + Debater         │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  MULTIMODAL MODULES                                      │
│  • Gemini Embedding 2 (text/image/video/audio/PDF)       │
│  • Chandra OCR (document extraction)                       │
│  • Drug Discovery (peptide generation)                     │
└────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Social trend research (last30days)
cd ~/.openclaw/workspace/skills/last30days
python3 scripts/last30days.py "SIRT3 longevity research"

# Research mode (ARP agents)
python3 orchestrator.py "Urolithin A for sarcopenia"

# Drug discovery mode
python3 discovery_pipeline.py "SIRT3 mitophagy activators"
```

## Three Core Modes

### Research Mode
Multi-agent LLM team for literature review, analysis, and synthesis.

### Drug Discovery Mode
Complete peptide drug discovery workflow with:
- Target identification from research topic
- Peptide generation (diffusion model concept)
- Sequence validation
- Modification suggestions
- Candidate ranking

### Social Intelligence Mode (last30days)
Discover what communities are actually discussing:
- Reddit threads and comments
- Hacker News discussions
- Polymarket prediction markets
- Bluesky/X trends

## Installation

```bash
# Clone the repo
git clone https://github.com/ohbryt/arp-v3.git
cd arp-v3

# Install last30days (optional but recommended)
git clone https://github.com/mvanhorn/last30days-skill.git \
  ~/.openclaw/workspace/skills/last30days

# Optional dependencies
pip install google-genai  # Gemini Embedding 2
pip install chandra-ocr   # Document extraction
```

## Key Innovation: KG-CoT

Based on J Morrissette's insight: *"Chain-of-thought reasoning is powerful but blind to its own history."*

KG-CoT integrates a Knowledge Graph into the CoT loop:
- **Before** each reasoning step: Query KG for known failure patterns
- **After** each step: Learn from result to update KG
- **Intervene** mid-chain to prevent known mistakes

## Model Team (Free Tier)

| Agent | Model | Cost |
|-------|-------|------|
| Lead | minimax/m2.7 | Your API |
| Researcher | nvidia/nemotron-3-super-120b-a12b:free | Free |
| Analyst | nvidia/nemotron-3-super-120b-a12b:free | Free |
| Reviewer | stepfun/step-3.5-flash:free | Free |
| Debater | openrouter/free | Free |

## License

MIT
