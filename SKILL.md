# ARP v3 KG-CoT — Hyper-Agent Research Pipeline

> Multi-LLM team with Knowledge Graph CoT (Morrissette-style) + self-evolution + Drug Discovery

## Concept

Based on J Morrissette's insight: *"Chain-of-thought reasoning is powerful but blind to its own history."*

This pipeline integrates a **Knowledge Graph** into the Chain-of-Thought reasoning loop:
- **NOT** input to the chain
- **BUT** corrective/guiding mechanism **between steps**

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  HYPER LAYER (KG-CoT Enhanced)                            │
│  • Pre-check: Query KG before each agent execution        │
│  • Post-evaluate: Learn from results                      │
│  • Intervene mid-chain to prevent known failures          │
└────────────────────────┬──────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│  KNOWLEDGE GRAPH                                          │
│  • Stores observed outcomes (success/failure)             │
│  • Pattern matching against historical mistakes            │
│  • Deterministic corrections based on experience          │
└───────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│  BASE AGENT LAYER                                         │
│  Lead (minimax) → Orchestration                          │
│  Researcher (Nemotron) → Research                        │
│  Analyst (Nemotron) → Deep Analysis                      │
│  Reviewer (Stepfun) → Critique                           │
│  Debater (openrouter/free) → Counter-arguments           │
│  Synthesizer (minimax) → Final Integration               │
└───────────────────────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────┐
│  DRUG DISCOVERY MODULE (ACP-Diffusion style)             │
│  • Target identification from research topic              │
│  • Peptide generation (diffusion model concept)           │
│  • Sequence validation + modification suggestions          │
│  • Candidate ranking by confidence                       │
└───────────────────────────────────────────────────────────┘
```

## Two Modes

### 1. Research Mode (ARP Agents)

```bash
python3 orchestrator.py "<research topic>"
```

### 2. Drug Discovery Mode

```bash
python3 discovery_pipeline.py "<drug target topic>"
# Example: python3 discovery_pipeline.py "SIRT3 mitophagy sarcopenia"
```

## Drug Discovery Targets

| Target | Pathway | Function | Priority |
|--------|---------|---------|----------|
| SIRT3 | Mitochondrial sirtuin | Mitophagy activation | High |
| PGC-1α | Mitochondrial biogenesis | Transcription co-activator | Medium |
| FOXO3 | Cellular longevity | Stress resistance | Medium |
| PD-L1 | Immune checkpoint | Cancer immunotherapy | High |
| TNF-α | Inflammation | Pro-inflammatory cytokine | High |
| KRAS | Cell proliferation | Oncogenic GTPase | High |

## Morrissette's KG Acquisition Modes

| Domain | Signal Source | Example |
|---|---|---|
| **Technical** | Logs, tests, observable failures | API errors, build failures |
| **Documented** | Policies, architecture, rules | Encoded constraints |
| **Conversational** | User feedback → secondary LLM | Pattern extraction |

## Token Strategy

- **minimax-m2.7**: Lead + synthesis (your model)
- **nemotron**: Researcher + Analyst (free)
- **stepfun/flash**: Reviewer (free)
- **openrouter/free**: Debater (free)

## Usage

```bash
# Research mode
python3 orchestrator.py "<research topic>"

# Drug discovery mode
python3 discovery_pipeline.py "<drug target topic>"

# Examples:
python3 orchestrator.py "Urolithin A for sarcopenia"
python3 discovery_pipeline.py "SIRT3 mitophagy activators"
```

## Output

```
outputs/<slug>/
├── FINAL.md
├── research.md
├── analysis.md
├── review.md
├── debate.md
├── synthesis.md
├── hyper-report.md
└── knowledge-graph.md

outputs/drug-discovery-<slug>/
└── discovery-report.md
```

## Inspired By

- [J Morrissette - Knowledge Graphs as Real-Time Correction in CoT](https://substack.com)
- [ACP-ConditionalDiffusion (yidingneng)](https://github.com/yidingneng/ACP-ConditionalDiffusion)
- [HyperAgents (ICLR 2026)](https://arxiv.org/abs/2502.hyperagents)
- [AgentScope (Alibaba)](https://arxiv.org/html/2402.14034v2)
- [Chandra OCR](https://github.com/datalab-to/chandra)
