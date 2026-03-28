# ARP v5 — Autonomous Research Pipeline

> Multi-Model Multi-Agent Research System with AI Scientist

![Version](https://img.shields.io/badge/version-v5-blue)
![License](https://img.shields.io/badge/license-MIT-green)

ARP v5 is our fully autonomous research pipeline that combines cutting-edge AI technologies for scientific discovery.

## Features

- **Novel Discovery Engine**: Beyond literature-known compounds
- **Multi-Model SubAgents**: Dynamically route tasks to optimal models (Gemini, GLM-5, Nemotron, etc.)
- **KG-CoT**: Knowledge Graph-guided Chain-of-Thought for real-time correction
- **AI Scientist**: Automated paper generation (Nature 2026)
- **System 2 Reasoning**: Slow, deliberate reasoning with self-verification
- **RunPod GPU**: Cloud GPU for heavy computation
- **Social Intelligence**: Trend research via last30days
- **Multimodal**: Gemini Embedding 2, Chandra OCR

## Quick Start

```bash
# Research with SubAgents
python3 subagent.py

# Original orchestrator
python3 orchestrator.py "SIRT3 mitophagy research"

# System 2 Reasoning
python3 reasoning.py

# Drug Discovery
python3 discovery_pipeline.py "SIRT3"

# Novel Discovery (beyond literature)
python3 novel_discovery.py

# AI Scientist (requires RunPod GPU)
export RUNPOD_API_KEY=your_key
python3 run_aiscientist.py --gpu "experiment"
```

## Architecture

```
User Input → Hyper Layer (KG-CoT)
                    ↓
         Model Router (Cost Optimizer)
                    ↓
         ┌──────────┼──────────┐
         ↓          ↓          ↓
    Researcher  Analyst   Reviewer
    (Nemotron) (Gemini)  (Stepfun)
         └──────────┼──────────┘
                    ↓
               Debater (GLM-5)
                    ↓
             Synthesizer (Gemini)
                    ↓
         Knowledge Graph (KG-CoT)
                    ↓
               Final Output
```

## Models

| Model | Cost | Use Case |
|-------|------|----------|
| Gemini 3.1 Flash Lite | $0.075/1M | Primary subagent |
| GLM-5 | $0.72/1M | Generator |
| Nemotron | FREE | Research |
| Stepfun | FREE | Review |
| OpenRouter Free | FREE | Fallback |

## Installation

```bash
# Clone the repo
git clone https://github.com/ohbryt/arp-v3.git
cd arp-v3

# Install dependencies
pip install openai anthropic google-generativeai

# Configure API keys in .env
cp .env.example .env
# Edit .env with your keys
```

## .env Configuration

```bash
OPENROUTER_API_KEY=your_key
GOOGLE_API_KEY=your_key
RUNPOD_API_KEY=your_key
```

## License

MIT
