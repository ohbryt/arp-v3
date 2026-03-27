# ARP v3 — Hyper-Agent Research Pipeline

> Multi-LLM team with self-evolution (HyperAgents concept) + fault tolerance (AgentScope) + role-based routing

---

## Model Team

| Model | Provider | Role | Strength |
|---|---|---|---|
| `minimax/minimax-m2.7` | MiniMax | **Team Lead** | Orchestration, planning, final synthesis |
| `z-ai/glm-5-turbo` | ZhipuAI | **Researcher** | Web research, fact-gathering |
| `nvidia/nemotron-3-super-120b-a12b:free` | OpenRouter | **Analyst** | Deep analysis, structured reasoning |
| `stepfun/step-3.5-flash:free` | OpenRouter | **Reviewer** | Code/doc review, critique |
| `openrouter/free` | OpenRouter | **Debater** | Counter-arguments, weakness identification |
| `chandra-ocr` | Datalab | **Extractor** | PDF/document → structured text/tables |

**Free tier only** — zero API cost for sub-agents.

---

## Hyper-Agent Architecture

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
│  │ (GLM)    │(Nemotron)│(Stepfun) │(Chandra) │        │
│  └──────────┴──────────┴──────────┴──────────┘        │
│      ↓                                                    │
│  Synthesizer (minimax) ← Final integration             │
└─────────────────────────────────────────────────────────┘
```

---

## Self-Evolution Loop (HyperAgents-inspired)

```
LOOP until task complete:
  1. Base agents execute their roles
  2. Hyper Layer monitors:
     - Success/failure patterns
     - Token efficiency
     - Output quality
  3. If improvement detected → update agent prompt/strategy
  4. If failure detected → retry with adjusted approach
  5. Log evolution in ARP_CHANGELOG.md
```

**Evolution triggers:**
- Task success → refine approach
- Task failure → modify strategy
- Token threshold → switch model
- Quality gate fail → enhance prompt

---

## Fault Tolerance (AgentScope-inspired)

| Error Type | Handling |
|---|---|
| API timeout | Auto-retry (3x) |
| Model unavailable | Switch to fallback model |
| JSON parse error | Rule-based correction |
| Quality gate fail | Hyper Layer intervention |
| Unresolvable | Log + escalate to Lead |

---

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
    └── Extractor (Chandra) → PDF/document → structured text  ← NEW
    ↓
Phase 3: HYPER MONITOR — Check quality gates
    ↓
Phase 4: DEBATE — Debater challenges conclusions
    ↓
Phase 5: SYNTHESIZE — Lead integrates all outputs
    ↓
Phase 6: EVOLVE — Log lessons, update approach
```

---

## Token Strategy

- **minimax-m2.7**: Lead + final synthesis only
- **nemotron**: Analyst (free) — deep dive tasks
- **GLM-5**: Researcher (free tier) — web research
- **stepfun/flash**: Reviewer (free) — lightweight critique
- **openrouter/free**: Debater (free) — devil's advocate

---

## Invocation

```
/arp-v3 <topic or project description>
```

---

## Inspired By

- [HyperAgents (ICLR 2026)](https://arxiv.org/abs/2502.hyperagents) — Self-evolving meta-agent
- [AgentScope (Alibaba)](https://arxiv.org/html/2402.14034v2) — Fault tolerance, pipeline abstraction
- [Chandra OCR (Datalab)](https://github.com/datalab-to/chandra) — Document intelligence, PDF extraction
- [auto-research-pipeline](https://github.com/ohbryt/auto-research-pipeline) — Base architecture
