# ARP v4 — Hyper-Agent Research Pipeline

> Multi-LLM team with Knowledge Graph CoT + Drug Discovery + Multimodal Embedding + Social Trend Intelligence + Advanced Reasoning

## Overview

ARP v4 is an autonomous research pipeline that combines:

- **HyperAgents (ICLR 2026)** — Self-evolving meta-agent
- **AgentScope (Alibaba)** — Fault tolerance and pipeline abstraction
- **Morrissette's KG-CoT** — Knowledge Graph for real-time correction in chain-of-thought
- **ARC-AGI-3** — Abstraction and reasoning benchmark
- **ACP-ConditionalDiffusion** — Diffusion-based peptide generation for drug discovery
- **Chandra OCR** — Document intelligence for PDF extraction
- **Gemini Embedding 2** — Unified multimodal embedding (text/image/video/audio/PDF)
- **last30days** — Social trend intelligence (Reddit, HN, Polymarket, Bluesky, X)
- **System 2 Reasoning** — Slow, deliberate reasoning with self-verification

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
│  REASONING LAYER (System 2)                               │
│  • Chain-of-Thought reasoning                              │
│  • Chain-of-Verification (reduce hallucinations)           │
│  • Abstraction & pattern recognition (ARC-AGI style)       │
│  • Self-verification after each step                      │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  KNOWLEDGE GRAPH                                          │
│  • Stores observed outcomes (success/failure)             │
│  • Pattern matching against historical mistakes             │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  SOCIAL INTELLIGENCE (last30days)                        │
│  • Reddit, X, HN, Polymarket, Bluesky, YouTube           │
│  • Real-time community trends and sentiment                │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  BASE AGENT LAYER                                         │
│  Lead + Researcher + Analyst + Reviewer + Debater          │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  MULTIMODAL MODULES                                      │
│  • Gemini Embedding 2 (text/image/video/audio/PDF)      │
│  • Chandra OCR (document extraction)                       │
│  • Drug Discovery (peptide generation)                    │
└────────────────────────────────────────────────────────────┘
```

## Research Modes

### 1. Research Mode (ARP Agents)
```bash
python3 orchestrator.py "<research topic>"
```

### 2. Drug Discovery Mode
```bash
python3 discovery_pipeline.py "<drug target>"
```

### 3. Social Trend Mode (last30days)
```bash
cd ~/.openclaw/workspace/skills/last30days
python3 scripts/last30days.py "<topic>"
```

### 4. Reasoning Mode
```bash
python3 reasoning.py  # Demo
python3 reasoning.py --task "<reasoning task>"
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

## last30days Sources

| Source | Status | Auth Required |
|--------|--------|---------------|
| Reddit | ✅ | OpenAI/Codex auth |
| Hacker News | ✅ | None |
| Polymarket | ✅ | None |
| Bluesky | ⚡ | BSKY credentials |
| X/Twitter | ❌ | AUTH_TOKEN + CT0 |
| YouTube | ❌ | yt-dlp |
| TikTok/Instagram | ⚡ | ScrapeCreators API |

## Inspired By

- [J Morrissette - KG-CoT](https://substack.com)
- [ARC-AGI-3 (Symbolica)](https://github.com/symbolica-ai/ARC-AGI-3-Agents)
- [ACP-ConditionalDiffusion](https://github.com/yidingneng/ACP-ConditionalDiffusion)
- [HyperAgents (ICLR 2026)](https://arxiv.org/abs/2502.hyperagents)
- [AgentScope (Alibaba)](https://arxiv.org/html/2402.14034v2)
- [Chandra OCR](https://github.com/datalab-to/chandra)
- [Gemini Embedding 2 (Google)](https://ai.google.dev)
- [last30days (mvanhorn)](https://github.com/mvanhorn/last30days-skill)
