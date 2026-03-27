"""
ARP v3 — Hyper-Agent Research Pipeline
Multi-LLM team with self-evolution + fault tolerance + document extraction
"""

import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─── Config ──────────────────────────────────────────────────────────────────

OPENROUTER_API_KEY = "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"
OPENROUTER_BASE = "https://openrouter.ai/api/v1"

MODELS = {
    "lead": "minimax/minimax-m2.7",                    # Orchestration
    "researcher": "z-ai/glm-5-turbo",                   # Web research
    "analyst": "nvidia/nemotron-3-super-120b-a12b:free",  # Deep analysis
    "reviewer": "stepfun/step-3.5-flash:free",         # Lightweight critique
    "debater": "openrouter/free",                       # Counter-arguments
    "synthesizer": "minimax/minimax-m2.7",             # Final synthesis
}

# ─── Slug ───────────────────────────────────────────────────────────────────

def make_slug(text: str) -> str:
    clean = re.sub(r'[^\w\s-]', '', text)
    words = clean.split()[:5]
    return '-'.join(w.lower() for w in words)

# ─── OpenRouter Client ───────────────────────────────────────────────────────

def call_openrouter(model: str, messages: list[dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
    """Call OpenRouter API with auto-retry + error handling."""
    import urllib.request
    
    data = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }).encode()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "ARP-v3-HyperAgent",
    }
    
    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f"{OPENROUTER_BASE}/chat/completions",
                data=data,
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            error_body = json.loads(e.read()) if e.fp else {}
            err_msg = error_body.get("error", {}).get("message", str(e))
            
            # Try fallback model for free tiers
            if model in ("stepfun/step-3.5-flash:free", "openrouter/free"):
                fallback = "openrouter/free" if model == "stepfun/step-3.5-flash:free" else "nvidia/nemotron-3-super-120b-a12b:free"
                print(f"  ⚠️ {model} failed ({err_msg}), trying {fallback}")
                model = fallback
                data = json.dumps({
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }).encode()
                continue
            print(f"  ❌ HTTP {e.code}: {err_msg}")
            if attempt < 2:
                print(f"  ↻ Retry {attempt+2}/3...")
                time.sleep(2 ** attempt)
                continue
            raise
        except Exception as e:
            print(f"  ❌ Error: {e}")
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise
    
    return "Error: All retries failed"

# ─── Agent Prompts ───────────────────────────────────────────────────────────

SYSTEM_PROMPTS = {
    "researcher": """You are a **Researcher** agent in a multi-agent team.

STRICT RULES:
1. NEVER fabricate sources — every citation must be verifiable
2. Read before summarizing — don't infer from titles alone
3. Always include URLs — "URL or it didn't happen"
4. Mark claim status: verified / inferred / unverified
5. Use parallel searches for efficiency

OUTPUT: structured markdown with citations.
""",
    
    "analyst": """You are an **Analyst** agent in a multi-agent team.

STRICT RULES:
1. Deep reasoning — don't surface-level analysis
2. Use structured frameworks (SWOT, pros/cons, causal chains)
3. Quantify where possible (%, ratios, benchmarks)
4. Identify uncertainties and knowledge gaps
5. Be critical of your own reasoning

OUTPUT: comprehensive analysis markdown with evidence levels.
""",

    "reviewer": """You are a **Reviewer** agent in a multi-agent team.

STRICT RULES:
1. Find bugs, logical flaws, edge cases
2. Score quality 1-10 with clear reasoning
3. Categorize issues: FATAL / MAJOR / MINOR
4. Suggest specific fixes, not just criticism
5. Challenge assumptions

OUTPUT: structured review markdown with severity grading.
""",

    "debater": """You are a **Debater** agent in a multi-agent team.

STRICT RULES:
1. Find the WEAKEST points in any argument
2. Generate counter-arguments and alternative hypotheses
3. Steelman the opposition — represent it fairly
4. Identify gaps in evidence
5. Rate confidence: HIGH / MEDIUM / LOW for each counter

OUTPUT: structured debate markdown with counter-arguments.
""",

    "synthesizer": """You are a **Synthesizer** agent in a multi-agent team.

STRICT RULES:
1. Resolve conflicts between sources
2. Preserve uncertainty — don't overclaim
3. Give actionable conclusions
4. Highlight open questions
5. Integrate diverse perspectives into coherent narrative

OUTPUT: comprehensive synthesis markdown.
""",

    "hyper": """You are the **Hyper-Agent** — a meta-agent that monitors and improves the team.

YOUR ROLE:
1. Monitor each agent's output quality
2. Identify failure patterns
3. Adjust agent strategies in real-time
4. Optimize token usage
5. Trigger evolution when needed

DECISION TREE:
- If quality gate FAIL → instruct agent to retry with new approach
- If token threshold HIGH → switch to lighter model
- If pattern of failure → modify agent prompt
- If success → log and proceed

OUTPUT: Hyper decisions as structured markdown.
""",
}

# ─── Agent Runner ───────────────────────────────────────────────────────────

def run_agent(role: str, topic: str, context: Optional[str] = None, model: Optional[str] = None) -> str:
    """Run a single agent and return its output."""
    m = model or MODELS.get(role, "openrouter/free")
    system = SYSTEM_PROMPTS.get(role, "You are a helpful agent.")
    
    messages = [{"role": "system", "content": system}]
    
    user_content = f"# Topic\n{topic}\n\n"
    if context:
        user_content += f"# Context from previous stages\n{context}\n\n"
    user_content += "Produce your output now."
    
    messages.append({"role": "user", "content": user_content})
    
    print(f"  [{role.upper()}] → {m} ... ", end="", flush=True)
    result = call_openrouter(m, messages)
    print("✓")
    
    return result

# ─── Document Extractor (Chandra OCR) ──────────────────────────────────────

def extract_document(file_path: str, output_dir: str = "./outputs/docs") -> Optional[str]:
    """Extract text/tables from PDF using Chandra OCR.
    
    Requires: pip install chandra-ocr[hf]
    Or: Docker with vLLM server
    """
    import subprocess
    import shutil
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if shutil.which("chandra") is None:
        print("  ⚠️ Chandra OCR not installed. Install: pip install chandra-ocr[hf]")
        return None
    
    try:
        print(f"  [EXTRACTOR] → Chandra OCR: {file_path}")
        result = subprocess.run(
            ["chandra", file_path, str(output_path), "--method", "hf"],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            print("  [EXTRACTOR] ✓ Extracted")
            base = Path(file_path).stem
            md_files = list(output_path.glob(f"{base}*.md"))
            if md_files:
                return md_files[0].read_text()
        else:
            print(f"  ⚠️ Chandra failed: {result.stderr[:200]}")
    except Exception as e:
        print(f"  ⚠️ Extractor error: {e}")
    
    return None

# ─── Hyper Monitor ──────────────────────────────────────────────────────────

class HyperMonitor:
    """Meta-agent that monitors and adjusts team performance."""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.evolution_log = []
        self.agent_scores = {}
    
    def evaluate(self, role: str, output: str) -> dict:
        """Evaluate an agent's output."""
        score = 7.0
        issues = []
        
        if len(output) < 200:
            score = 5.0
            issues.append("Output too short")
        
        if output.count("?") > 5:
            score -= 1.0
            issues.append("Too many questions (surface-level)")
        
        if "unverified" in output.lower() or "uncertain" in output.lower():
            score -= 0.5
        
        if role in ("researcher", "reviewer"):
            if output.count("http") < 1:
                score -= 1.5
                issues.append("Missing citations/URLs")
        
        self.agent_scores[role] = max(0, min(10, score))
        
        return {
            "score": self.agent_scores[role],
            "issues": issues,
            "decision": "PASS" if score >= 6 else "RETRY"
        }
    
    def log_evolution(self, event: str, decision: str):
        """Log evolution event."""
        self.evolution_log.append({
            "time": datetime.now().isoformat(),
            "event": event,
            "decision": decision
        })
    
    def get_report(self) -> str:
        """Generate hyper layer report."""
        lines = ["# Hyper Layer Report\n"]
        for role, score in self.agent_scores.items():
            status = "✅" if score >= 6 else "⚠️"
            lines.append(f"- {role}: {score}/10 {status}")
        lines.append(f"\n## Evolution Log ({len(self.evolution_log)} events)")
        for e in self.evolution_log[-5:]:
            lines.append(f"- [{e['time']}] {e['event']} → {e['decision']}")
        return "\n".join(lines)

# ─── Pipeline ───────────────────────────────────────────────────────────────

def run_pipeline(topic: str, output_dir: str = "./outputs") -> dict:
    """Run full ARP v3 Hyper-Agent pipeline."""
    
    slug = make_slug(topic)
    out_path = Path(output_dir) / slug
    out_path.mkdir(parents=True, exist_ok=True)
    
    hyper = HyperMonitor(topic)
    
    print(f"\n{'='*60}")
    print(f"ARP v3 Hyper-Agent — {topic}")
    print(f"{'='*60}\n")
    
    # Phase 1: Planning (Lead)
    print("[PHASE 1] Planning...")
    # Lead via OpenClaw (no separate API call needed)
    
    # Phase 2: Parallel Execution
    print("\n[PHASE 2] Parallel Execution (Researcher + Analyst + Reviewer)...")
    
    research = run_agent("researcher", topic)
    eval_result = hyper.evaluate("researcher", research)
    if eval_result["decision"] == "RETRY":
        print(f"  ⚠️ Researcher scored {eval_result['score']}, retrying...")
        hyper.log_evolution("Researcher retry", f"Issues: {eval_result['issues']}")
        research = run_agent("researcher", topic)
    (out_path / f"{slug}-research.md").write_text(research)
    
    # Phase 2b: Document Extraction (if docs exist)
    doc_path = Path(output_dir).parent / "documents"
    extracted_text = None
    if doc_path.exists():
        pdfs = list(doc_path.glob("*.pdf")) + list(doc_path.glob("*.png")) + list(doc_path.glob("*.jpg"))
        if pdfs:
            print(f"\n[PHASE 2b] Extracting {len(pdfs)} document(s) with Chandra OCR...")
            for pdf in pdfs[:3]:
                text = extract_document(str(pdf), str(out_path / "extracted"))
                if text:
                    extracted_text = (extracted_text or "") + f"\n\n# From: {pdf.name}\n\n{text[:5000]}"
    
    # Build analysis context
    analysis_context = research
    if extracted_text:
        analysis_context += f"\n\n## Extracted Documents\n{extracted_text}"
        print("  ✓ Documents integrated into analysis")
    
    analysis = run_agent("analyst", topic, context=analysis_context)
    eval_result = hyper.evaluate("analyst", analysis)
    if eval_result["decision"] == "RETRY":
        print(f"  ⚠️ Analyst scored {eval_result['score']}, retrying...")
        hyper.log_evolution("Analyst retry", f"Issues: {eval_result['issues']}")
        analysis = run_agent("analyst", topic, context=analysis_context)
    (out_path / f"{slug}-analysis.md").write_text(analysis)
    
    review = run_agent("reviewer", topic, context=f"RESEARCH:\n{research}\n\nANALYSIS:\n{analysis}")
    eval_result = hyper.evaluate("reviewer", review)
    (out_path / f"{slug}-review.md").write_text(review)
    
    # Phase 3: Hyper Monitor
    print("\n[PHASE 3] Hyper Monitor...")
    hyper_report = hyper.get_report()
    (out_path / f"{slug}-hyper-report.md").write_text(hyper_report)
    print(hyper_report)
    
    # Phase 4: Debate
    print("\n[PHASE 4] Debate...")
    debate = run_agent("debater", topic, context=f"RESEARCH:\n{research}\n\nANALYSIS:\n{analysis}")
    (out_path / f"{slug}-debate.md").write_text(debate)
    
    # Phase 5: Synthesis
    print("\n[PHASE 5] Synthesis...")
    synthesis = run_agent("synthesizer", topic, context=f"RESEARCH:\n{research}\n\nANALYSIS:\n{analysis}\n\nREVIEW:\n{review}\n\nDEBATE:\n{debate}")
    (out_path / f"{slug}-synthesis.md").write_text(synthesis)
    
    # Final output
    final = f"""# ARP v3 Hyper-Agent — {topic}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Slug:** {slug}
**Model Team:** minimax (lead) + GLM-5 (researcher) + Nemotron (analyst) + Stepfun (reviewer) + Free (debater)
**Document Extraction:** Chandra OCR 2 (when PDF provided)

## Files

| Phase | File |
|---|---|
| Research | `{slug}-research.md` |
| Analysis | `{slug}-analysis.md` |
| Review | `{slug}-review.md` |
| Debate | `{slug}-debate.md` |
| Synthesis | `{slug}-synthesis.md` |
| Hyper Report | `{slug}-hyper-report.md` |

---

{synthesis}
"""
    (out_path / f"{slug}-FINAL.md").write_text(final)
    
    print(f"\n{'='*60}")
    print(f"✅ Complete! Files in: {out_path}")
    print(f"   Main output: {slug}-FINAL.md")
    print(f"{'='*60}\n")
    
    return {
        "slug": slug,
        "path": str(out_path),
        "hyper_report": hyper_report,
        "research": research,
        "analysis": analysis,
        "review": review,
        "debate": debate,
        "synthesis": synthesis,
    }

# ─── CLI ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 orchestrator.py <topic>")
        sys.exit(1)
    
    topic = " ".join(sys.argv[1:])
    result = run_pipeline(topic)
    print(f"\nHyper evolution events: {len(result['hyper_report'].splitlines())}")
