# ARP v3 — Hyper-Agent Research Pipeline

> Multi-LLM research team with self-evolution + fault tolerance + document extraction

## Overview

ARP v3 is an autonomous research pipeline that orchestrates a team of specialized LLM agents to conduct comprehensive research on any topic. It combines concepts from:

- **HyperAgents** (ICLR 2026) — Self-evolving meta-agent that monitors and improves team performance
- **AgentScope** (Alibaba) — Fault tolerance and pipeline abstraction
- **Chandra OCR** (Datalab) — Document intelligence for PDF extraction

## Model Team

| Agent | Model | Role |
|---|---|---|
| **Lead** | minimax/minimax-m2.7 | Orchestration, planning, final synthesis |
| **Researcher** | z-ai/glm-5-turbo | Web research, fact-gathering |
| **Analyst** | nvidia/nemotron-3-super-120b-a12b:free | Deep analysis, structured reasoning |
| **Reviewer** | stepfun/step-3.5-flash:free | Code/doc review, critique |
| **Debater** | openrouter/free | Counter-arguments, weakness identification |
| **Extractor** | chandra-ocr | PDF/document → structured text |

**All sub-agents use free tier models** — zero API cost for research agents.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  HYPER LAYER (Meta-Agent)                              │
│  • Monitors base agent performance                      │
│  • Adjusts prompts/rules in real-time                  │
│  • Self-evolution during task execution                │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│  BASE AGENT LAYER                                       │
│                                                          │
│  Lead (minimax)  →  Orchestration + Planning            │
│      ↓                                                    │
│  ┌──────────┬──────────┬──────────┬──────────┐        │
│  │Researcher│ Analyst  │ Reviewer │Extractor │        │
│  │ (GLM-5) │(Nemotron)│(Stepfun) │(Chandra) │        │
│  └──────────┴──────────┴──────────┴──────────┘        │
│      ↓                                                    │
│  Synthesizer (minimax) ← Final integration             │
└─────────────────────────────────────────────────────────┘
```

## Phase Flow

```
User Input → Lead (minimax)
    ↓
Phase 1: PLAN — Break into tasks, assign roles
    ↓
Phase 2: EXECUTE (parallel)
    ├── Researcher (GLM) → Web research + PDF links
    ├── Analyst (Nemotron) → Deep analysis
    ├── Reviewer (Stepfun) → Critique
    └── Extractor (Chandra) → PDF/document → structured text
    ↓
Phase 3: HYPER MONITOR — Check quality gates
    ↓
Phase 4: DEBATE — Debater challenges conclusions
    ↓
Phase 5: SYNTHESIZE — Lead integrates all outputs
    ↓
Phase 6: EVOLVE — Log lessons, update approach
```

## Installation

```bash
# Clone the repo
git clone https://github.com/ohbryt/arp-v3.git
cd arp-v3

# Install Chandra OCR (optional, for document extraction)
pip install chandra-ocr[hf]

# Set your OpenRouter API key
export OPENROUTER_API_KEY="your-key-here"
```

## Usage

```bash
# Basic research
python3 orchestrator.py "SIRT3 anti-aging mechanisms"

# With PDF documents (place in ../documents/ relative to output dir)
# mkdir -p ../documents
# cp paper.pdf ../documents/
# python3 orchestrator.py "your topic"
```

## Output

```
outputs/<slug>/
├── <slug>-research.md      # Web research findings
├── <slug>-analysis.md       # Deep analysis
├── <slug>-review.md         # Critical review
├── <slug>-debate.md         # Counter-arguments
├── <slug>-synthesis.md      # Final integration
├── <slug>-hyper-report.md   # Hyper layer report
└── <slug>-FINAL.md         # Complete report
```

## Token Strategy

- **minimax-m2.7**: Lead + final synthesis only (your primary model)
- **nemotron**: Analyst (free) — deep dive tasks
- **GLM-5**: Researcher (free tier) — web research
- **stepfun/flash**: Reviewer (free) — lightweight critique
- **openrouter/free**: Debater (free) — devil's advocate

## Self-Evolution (Hyper Layer)

The Hyper Layer monitors each agent and automatically:

1. **Scores outputs** (1-10) based on length, citations, uncertainty markers
2. **Retries failed agents** with adjusted prompts
3. **Logs evolution events** for future improvement
4. **Generates reports** on team performance

## Fault Tolerance

| Error Type | Handling |
|---|---|
| API timeout | Auto-retry (3x) |
| Model unavailable | Switch to fallback model |
| JSON parse error | Rule-based correction |
| Quality gate fail | Hyper Layer intervention |

## License

MIT

## Citation

If you use ARP v3 in your research, please cite:

```bibtex
@software{arp-v3,
  title = {ARP v3: Hyper-Agent Research Pipeline},
  author = {Demis (OpenClaw)},
  year = {2026},
  url = {https://github.com/ohbryt/arp-v3}
}
```
