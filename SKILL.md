# ARP v5 — Autonomous Research Pipeline

> Multi-Model Multi-Agent Research System with AI Scientist

## Overview

ARP v5 is the latest version of our autonomous research pipeline, combining:

- **Multi-Model SubAgents**: Gemini, GLM-5, Nemotron, Stepfun (cost-optimized)
- **KG-CoT**: Knowledge Graph for real-time Chain-of-Thought correction
- **AI Scientist**: Fully automated paper generation (Nature 2026)
- **System 2 Reasoning**: Slow, deliberate reasoning with self-verification
- **RunPod GPU**: Cloud GPU for heavy computation
- **Social Intelligence**: last30days for trend research
- **Multimodal**: Gemini Embedding 2, Chandra OCR

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  HYPER LAYER (KG-CoT Enhanced)                            │
│  • Pre-check: Query KG before each agent execution        │
│  • Post-evaluate: Learn from results                      │
│  • Intervene mid-chain to prevent known failures           │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  MODEL ROUTER (Cost Optimizer)                           │
│  Task → Best model based on: cost, speed, capability       │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  SUBAGENT TEAM (Multi-Model)                             │
│  ┌──────────────┬──────────────┬──────────────┐          │
│  │ Researcher   │ Analyst      │ Reviewer     │          │
│  │ (Nemotron)  │ (Gemini)     │ (Stepfun)    │          │
│  ├──────────────┼──────────────┼──────────────┤          │
│  │ Debater     │ Synthesizer  │ Generator    │          │
│  │ (GLM-5)    │ (Gemini)     │ (GLM-5)     │          │
│  └──────────────┴──────────────┴──────────────┘          │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  AI SCIENTIST LAYER (Nature 2026)                        │
│  Idea → Code → Experiment → Paper → Review               │
│  (Runs on RunPod GPU)                                    │
└────────────────────────────────────────────────────────────┘
                         │
┌────────────────────────────────────────────────────────────┐
│  REASONING LAYER (System 2)                              │
│  Chain-of-Thought + Chain-of-Verification                 │
└────────────────────────────────────────────────────────────┘
```

## Model Roster

| Model | Role | Cost | Strength |
|-------|------|------|----------|
| **Gemini 3.1 Flash Lite** | Primary | $0.075/1M | Fast, cheap, good |
| **GLM-5 (ZhipuAI)** | Generator | $0.72/1M | Very cheap, good quality |
| **Nemotron 120B** | Research | FREE | Good reasoning, no cost |
| **GLM-4.5 Free** | Tasks | FREE | Free, ZhipuAI quality |
| **Stepfun 3.5** | Review | FREE | Fast, free |
| **OpenRouter Free** | Fallback | FREE | Always available |

## Run Modes

### 1. Research Mode (SubAgents)
```bash
python3 subagent.py
```

### 2. Original Orchestrator
```bash
python3 orchestrator.py "topic"
```

### 3. System 2 Reasoning
```bash
python3 reasoning.py
```

### 4. Drug Discovery
```bash
python3 discovery_pipeline.py "drug target"
```

### 5. AI Scientist (GPU)
```bash
export RUNPOD_API_KEY=your_key
python3 run_aiscientist.py --gpu "experiment"
```

## Key Features

### KG-CoT (Morrissette)
- Query KG before each step
- Learn from execution results
- Prevent known failures

### AI Scientist (Nature 2026)
- Fully automated paper generation
- Peer review quality assessment
- Runs on RunPod GPU

### System 2 Reasoning
- Slow, deliberate chain-of-thought
- Self-verification after each step
- Confidence calibration

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
