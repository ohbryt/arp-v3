# Multi-Hop Research Analysis System v3
## Brown Biotech — AI-Powered Research Pipeline

**Architecture:**
```
web_search tool (browser) → sources → LLM.analyze() → 보고서
```

---

## Quick Start

### 1. Run web search (in agent)
```
web_search("NASH drugs resmetirom 2025", num=10)
web_fetch("https://...")
```

### 2. Pass results to LLM
```python
from multi_hop_research import MiniMaxLLM, Source

sources = [
    Source(title="Resmetirom FDA", url="https://...", snippet="Approved March 2024"),
    Source(title="Lanifibranor Phase 3", url="https://...", snippet="NATiV3 trial..."),
]

llm = MiniMaxLLM("sk-cp-mQNc3y...")
report = llm.analyze(sources, query="NASH drug pipeline 2025", service="drug_pipeline")
print(report)
```

### 3. CLI
```bash
python3 -m multi_hop_research --service pipeline --query "NASH drugs"
```

---

## Services

| Service | Description | Depth |
|---------|-------------|-------|
| `pipeline` | Drug pipeline analysis | 3-hop |
| `dd` | Technical Due Diligence | 3-hop |
| `intel` | Competitor intelligence | 2-hop |
| `market` | Market research | 2-hop |
| `paper` | Paper review | 2-hop |

---

## Multi-Hop Process

```
1. Explore: Initial web search (broad)
2. Verify: LLM extracts verified facts
3. Extend: Related searches (patents, trials, news)
```

---

## API Keys

- MiniMax: `sk-cp-mQNc3yEQSkm-...` (in ~/.env)
