# ARP v3 KG-CoT — Hyper-Agent Research Pipeline

> Multi-LLM team with Knowledge Graph CoT (Morrissette-style) + self-evolution

## Concept

Based on J Morrissette's insight: *"Chain-of-thought reasoning is powerful but blind to its own history."*

This pipeline integrates a **Knowledge Graph** into the Chain-of-Thought reasoning loop:
- **NOT** input to the chain
- **BUT** corrective/guiding mechanism **between steps**

```
[CoT Step N] → KG Query → Pattern Match? 
                              ↓
              ┌─ YES → INTERVENE (prevent mistake)
              └─ NO  → Proceed
```

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
│  Researcher (Nemotron) → Research                         │
│  Analyst (Nemotron) → Deep Analysis                      │
│  Reviewer (Stepfun) → Critique                           │
│  Debater (openrouter/free) → Counter-arguments           │
│  Synthesizer (minimax) → Final Integration              │
└───────────────────────────────────────────────────────────┘
```

## Morrissette's KG Acquisition Modes

| Domain | Signal Source | Example |
|---|---|---|
| **Technical** | Logs, tests, observable failures | API errors, build failures |
| **Documented** | Policies, architecture, rules | Encoded constraints |
| **Conversational** | User feedback → secondary LLM | Pattern extraction |

## How KG-CoT Works

```
1. Agent proposes next step
2. Hyper Layer queries KG for matching failure patterns
3. If match found:
   - INTERVENE with warning
   - Redirect before mistake propagates
4. Execute with awareness of history
5. Post-evaluate: Learn from result
6. Update KG with new pattern
```

## Token Strategy

- **minimax-m2.7**: Lead + synthesis (your model)
- **nemotron**: Researcher + Analyst (free)
- **stepfun/flash**: Reviewer (free)
- **openrouter/free**: Debater (free)

## Usage

```bash
python3 orchestrator.py "<research topic>"
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
└── knowledge-graph.md  ← KG dump with all patterns
```

## Inspired By

- [J Morrissette - Knowledge Graphs as Real-Time Correction in CoT](https://substack.com)
- [HyperAgents (ICLR 2026)](https://arxiv.org/abs/2502.hyperagents)
- [AgentScope (Alibaba)](https://arxiv.org/html/2402.14034v2)
- [Chandra OCR](https://github.com/datalab-to/chandra)
