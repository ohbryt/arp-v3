# ARP v4 — Hyper-Agent Research Pipeline

> Multi-LLM team with Knowledge Graph CoT + AI Scientist + Multi-Model SubAgents

## Overview

ARP v4 is an autonomous research pipeline that combines:

- **HyperAgents (ICLR 2026)** — Self-evolving meta-agent
- **AgentScope (Alibaba)** — Fault tolerance and pipeline abstraction
- **Morrissette's KG-CoT** — Knowledge Graph for real-time correction in chain-of-thought
- **AI Scientist (Nature 2026)** — Fully automated paper generation with peer review
- **Multi-Model SubAgents** — Dynamic model routing with cost optimization
- **Gemini 3.1 Flash Lite** — Fast, cheap primary subagent
- **RunPod GPU** — Cloud GPU for AI Scientist execution
- **last30days** — Social trend intelligence (Reddit, HN, Polymarket)
- **Gemini Embedding 2** — Unified multimodal embedding
- **System 2 Reasoning** — Slow, deliberate reasoning with self-verification

## Multi-Model Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  MODEL ROUTER (Cost Optimizer)                            │
│  Task → Best model based on: cost, speed, capability      │
└─────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  SUBAGENT TEAM                                           │
│  ┌──────────────┬──────────────┬──────────────┐          │
│  │ Researcher   │ Analyst      │ Reviewer     │          │
│  │ (Nemotron)  │ (Gemini)     │ (Stepfun)    │          │
│  ├──────────────┼──────────────┼──────────────┤          │
│  │ Debater     │ Synthesizer  │ Generator    │          │
│  │ (Free)      │ (Gemini)     │ (Gemini)     │          │
│  └──────────────┴──────────────┴──────────────┘          │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  GEMINI 3.1 FLASH LITE (Primary SubAgent)                │
│  Fast: 1M tokens/min • Cheap: $0.075/1M tokens            │
│  1M context window • Multimodal • Function calling          │
└────────────────────────────────────────────────────────────┘
```

## Model Roster

| Model | Role | Cost | Speed | Strength |
|-------|------|------|-------|----------|
| **Gemini 3.1 Flash Lite** | Primary subagent | $0.075/1M | ⚡⚡⚡ | Fast, cheap, good reasoning |
| **Gemini 3.1 Pro** | Deep reasoning | $1.00/1M | ⚡⚡ | Large context, deep analysis |
| **GLM-5 (ZhipuAI)** | Bulk tasks | $0.72/1M | ⚡⚡⚡ | Very cheap, good quality |
| **GLM-4.5 Free** | Free tasks | FREE | ⚡⚡ | Free, ZhipuAI quality |
| **Nemotron 120B** | Research | FREE | ⚡⚡ | Good reasoning, no cost |
| **Stepfun 3.5** | Review | FREE | ⚡⚡⚡ | Fast, free |
| **OpenRouter Free** | Fallback | FREE | ⚡⚡ | Always available |

## Run Modes

### 1. CPU Mode (Free Tier)
```bash
python3 subagent.py                    # Multi-model pipeline
python3 orchestrator.py "topic"       # Original ARP agents
python3 reasoning.py                   # System 2 reasoning
```

### 2. GPU Mode (RunPod)
```bash
export RUNPOD_API_KEY=your_key
python3 run_aiscientist.py --gpu "AI Scientist experiment"
```

## Pipeline Flow

```
User Input → Model Router (cost optimizer)
                    ↓
    ┌───────────────┼───────────────┐
    ↓               ↓               ↓
Researcher     Analyst          Reviewer
(Nemotron)    (Gemini)         (Stepfun)
    │               │               │
    └───────────────┼───────────────┘
                    ↓
              Debater (GLM-5)
                    ↓
              Synthesizer (Gemini)
                    ↓
            Knowledge Graph (KG-CoT)
                    ↓
               Final Output
```

## AI Scientist Pipeline (RunPod GPU)

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

## Usage Examples

```bash
# Multi-model subagent pipeline
python3 subagent.py

# Run specific subagent
from subagent import SubAgentRunner
runner = SubAgentRunner()
runner.run_full_pipeline("SIRT3 mitophagy research")

# Use specific model
runner.run("Analyze this", model="gemini-flash")
runner.run("Research topic", model="nemotron")
```

## Cost Optimization

| Task | Recommended Model | Reason |
|------|-----------------|--------|
| Quick analysis | Gemini Flash | Fast + cheap |
| Deep research | Nemotron | Free + capable |
| Simple review | Stepfun | Free + fast |
| Complex synthesis | Gemini Pro | Deep reasoning |
| Fallback | OpenRouter Free | Always available |

**Estimated costs:**
- Gemini Flash: $0.001 per research query
- Full pipeline: ~$0.01 (mostly free models)

## Inspired By

- [J Morrissette - KG-CoT](https://substack.com)
- [AI Scientist (Nature 2026)](https://www.nature.com/articles/s41586-026-10265-5)
- [SakanaAI/AI-Scientist](https://github.com/SakanaAI/AI-Scientist)
- [Gemini 3.1 Flash Lite (Google)](https://ai.google.dev)
- [ARC-AGI-3 (Symbolica)](https://github.com/symbolica-ai/ARC-AGI-3-Agents)
- [last30days (mvanhorn)](https://github.com/mvanhorn/last30days-skill)
- [RunPod](https://runpod.io)
