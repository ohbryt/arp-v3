"""
ARP v3 — Hyper-Agent Research Pipeline v2
Integrating Knowledge Graph CoT (Morrissette-style) with Self-Evolution

Key Enhancement: KG-Guided Chain-of-Thought
- KG queries at each reasoning step
- Pattern matching against historical failures
- Mid-chain intervention to prevent mistake propagation
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
    "lead": "minimax/minimax-m2.7",
    "researcher": "nvidia/nemotron-3-super-120b-a12b:free",
    "analyst": "nvidia/nemotron-3-super-120b-a12b:free",
    "reviewer": "stepfun/step-3.5-flash:free",
    "debater": "openrouter/free",
    "synthesizer": "minimax/minimax-m2.7",
}

# ─── Knowledge Graph ─────────────────────────────────────────────────────────

class KnowledgeGraph:
    """KG stores operational history for KG-CoT intervention.
    
    Based on J Morrissette's concept: use KG to catch known failure patterns
    mid-chain, not just at prompt time.
    """
    
    def __init__(self, domain: str = "general"):
        self.domain = domain
        self.nodes = {}  # pattern_id -> Node
        self.edges = []   # (pattern_id, related_pattern_id, relation)
        
    def add_pattern(self, pattern_id: str, pattern: str, outcome: str, 
                    context: str = "", evidence: str = ""):
        """Record a pattern with its outcome."""
        self.nodes[pattern_id] = {
            "pattern": pattern,
            "outcome": outcome,  # "success" or "failure"
            "context": context,
            "evidence": evidence,
            "timestamp": datetime.now().isoformat(),
            "hits": 0
        }
        
    def link_patterns(self, from_id: str, to_id: str, relation: str):
        """Link related patterns."""
        self.edges.append((from_id, to_id, relation))
        
    def query(self, current_step: str, context: str = "") -> Optional[dict]:
        """Query KG for matching patterns that should trigger intervention.
        
        Returns intervention dict if bad pattern found, None otherwise.
        Based on Morrissette: catch mid-chain before mistake propagates.
        """
        current_lower = current_step.lower() + context.lower()
        
        for pattern_id, node in self.nodes.items():
            if node["outcome"] == "failure":
                # Check if current step matches failure pattern
                pattern_words = node["pattern"].lower().split()
                matches = sum(1 for w in pattern_words if w in current_lower)
                
                if matches >= 2:  # threshold for pattern match
                    node["hits"] += 1
                    return {
                        "action": "INTERVENE",
                        "pattern_id": pattern_id,
                        "why": node["pattern"],
                        "evidence": node["evidence"],
                        "context": node["context"],
                        "counter": f"This approach was tried at {node['timestamp']} and led to failure. Consider alternative."
                    }
        
        return None
    
    def learn_from_result(self, step_name: str, result: str, success: bool):
        """Learn from execution result (Morrissette's knowledge acquisition)."""
        pattern_id = f"{step_name}_{datetime.now().strftime('%Y%m%d%H%M')}"
        
        if not success:
            # Extract failure reasons
            issues = []
            if len(result) < 200:
                issues.append("Output too short")
            if "error" in result.lower():
                issues.append("Execution error")
            if "http 4" in result.lower():
                issues.append("API/authentication error")
            if "not found" in result.lower():
                issues.append("Resource not found")
                
            self.add_pattern(
                pattern_id=pattern_id,
                pattern=step_name,
                outcome="failure",
                context="; ".join(issues),
                evidence=result[:500]  # First 500 chars as evidence
            )
        else:
            self.add_pattern(
                pattern_id=pattern_id,
                pattern=step_name,
                outcome="success",
                context="",
                evidence=result[:500]
            )
    
    def get_report(self) -> str:
        """Generate KG status report."""
        successes = sum(1 for n in self.nodes.values() if n["outcome"] == "success")
        failures = sum(1 for n in self.nodes.values() if n["outcome"] == "failure")
        
        lines = [
            f"# Knowledge Graph Report ({self.domain})",
            f"- Total patterns: {len(self.nodes)}",
            f"- Successes: {successes}",
            f"- Failures: {failures}",
            f"- Patterns:",
        ]
        
        for pid, node in list(self.nodes.items())[-10:]:  # Last 10
            status = "✅" if node["outcome"] == "success" else "❌"
            lines.append(f"  {status} {pid}: {node['pattern'][:50]}")
            
        return "\n".join(lines)

# ─── Enhanced Hyper Layer with KG-CoT ─────────────────────────────────────────

class HyperLayerKG:
    """
    Enhanced Hyper Layer integrating Morrissette's KG-CoT concept.
    
    Key difference from standard Hyper Layer:
    - Queries KG at each step BEFORE execution
    - Intervenes mid-chain to prevent known failures
    - Learns from results to update KG
    - Deterministic corrections based on observed outcomes
    """
    
    def __init__(self, topic: str, kg_domain: str = "research"):
        self.topic = topic
        self.kg = KnowledgeGraph(domain=kg_domain)
        self.evolution_log = []
        self.agent_scores = {}
        self.interventions = []
        
    def pre_check(self, role: str, proposed_action: str, context: str = "") -> Optional[str]:
        """
        KG-CoT: Check proposed action against KG before execution.
        Morrissette-style: catch the model mid-chain before mistake propagates.
        """
        # Query KG for known failure patterns
        intervention = self.kg.query(proposed_action, context)
        
        if intervention:
            self.interventions.append({
                "role": role,
                "intervention": intervention,
                "timestamp": datetime.now().isoformat()
            })
            
            msg = f"\n⚠️ KG-CO.T INTERVENTION [{role}]:\n"
            msg += f"  Pattern detected: {intervention['why']}\n"
            msg += f"  Evidence: {intervention['evidence'][:100]}...\n"
            msg += f"  → {intervention['counter']}\n"
            
            self.log_evolution(f"KG intervention for {role}", intervention['why'])
            return msg
        
        return None
    
    def post_evaluate(self, role: str, output: str) -> dict:
        """Evaluate output and learn from result."""
        score = 7.0
        issues = []
        
        if output is None or len(output) < 200:
            score = 4.0
            issues.append("Output too short")
            
        if output and output.count("?") > 5:
            score -= 1.0
            issues.append("Too many questions")
            
        if output and ("unverified" in output.lower() or "uncertain" in output.lower()):
            score -= 0.5
            
        if role in ("researcher", "reviewer") and output:
            if output.count("http") < 1:
                score -= 1.5
                issues.append("Missing citations")
        
        self.agent_scores[role] = max(0, min(10, score))
        
        # Learn from result for KG
        success = score >= 6
        self.kg.learn_from_result(role, output or "", success)
        
        return {
            "score": self.agent_scores[role],
            "issues": issues,
            "decision": "PASS" if score >= 6 else "RETRY"
        }
    
    def log_evolution(self, event: str, decision: str):
        self.evolution_log.append({
            "time": datetime.now().isoformat(),
            "event": event,
            "decision": decision
        })
    
    def get_report(self) -> str:
        lines = [
            f"# Hyper Layer Report (KG-CoT Enhanced)",
            f"",
            f"## Knowledge Graph",
            f"- Domain: {self.kg.domain}",
            f"- Total patterns: {len(self.kg.nodes)}",
            f"- Successes: {sum(1 for n in self.kg.nodes.values() if n['outcome'] == 'success')}",
            f"- Failures: {sum(1 for n in self.kg.nodes.values() if n['outcome'] == 'failure')}",
            f"",
            f"## Agent Scores",
        ]
        
        for role, score in self.agent_scores.items():
            status = "✅" if score >= 6 else "⚠️"
            lines.append(f"- {role}: {score}/10 {status}")
            
        lines.append(f"\n## KG Interventions ({len(self.interventions)})")
        for i in self.interventions[-5:]:
            lines.append(f"- [{i['timestamp']}] {i['role']}: {i['intervention']['why'][:50]}")
            
        lines.append(f"\n## Evolution Log ({len(self.evolution_log)} events)")
        for e in self.evolution_log[-5:]:
            lines.append(f"- [{e['time']}] {e['event']} → {e['decision']}")
            
        return "\n".join(lines)

# ─── Slug ───────────────────────────────────────────────────────────────────

def make_slug(text: str) -> str:
    clean = re.sub(r'[^\w\s-]', '', text)
    words = clean.split()[:5]
    return '-'.join(w.lower() for w in words)

# ─── OpenRouter Client ───────────────────────────────────────────────────────

def call_openrouter(model: str, messages: list[dict], temperature: float = 0.7, max_tokens: int = 2048) -> str:
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
        "X-Title": "ARP-v3-HyperAgent-KG",
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
}

# ─── KG-Enhanced Agent Runner ────────────────────────────────────────────────

def run_agent_with_kg(role: str, topic: str, hyper: HyperLayerKG, context: Optional[str] = None, model: Optional[str] = None) -> str:
    """Run agent with KG-CoT pre-check and post-evaluation."""
    m = model or MODELS.get(role, "openrouter/free")
    system = SYSTEM_PROMPTS.get(role, "You are a helpful agent.")
    
    # KG-CoT Pre-check: Query KG before execution
    proposed_action = f"{role} analyzing: {topic[:50]}"
    intervention = hyper.pre_check(role, proposed_action, context or "")
    
    messages = [{"role": "system", "content": system}]
    
    user_content = f"# Topic\n{topic}\n\n"
    if context:
        user_content += f"# Context from previous stages\n{context}\n\n"
    if intervention:
        user_content += f"# KG-COT INTERVENTION (Morrissette-style)\n{intervention}\n\n"
        print(f"  📖 KG-CoT: {intervention[:100]}...")
    
    user_content += "Produce your output now."
    messages.append({"role": "user", "content": user_content})
    
    print(f"  [{role.upper()}] → {m} ... ", end="", flush=True)
    result = call_openrouter(m, messages)
    print("✓")
    
    # Post-evaluation: Learn from result
    hyper.post_evaluate(role, result)
    
    return result

# ─── Document Extractor ─────────────────────────────────────────────────────

def extract_document(file_path: str, output_dir: str = "./outputs/docs") -> Optional[str]:
    import subprocess
    import shutil
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    if shutil.which("chandra") is None:
        return None
    
    try:
        result = subprocess.run(
            ["chandra", file_path, str(output_path), "--method", "hf"],
            capture_output=True, text=True, timeout=300
        )
        if result.returncode == 0:
            base = Path(file_path).stem
            md_files = list(output_path.glob(f"{base}*.md"))
            if md_files:
                return md_files[0].read_text()
    except Exception:
        pass
    
    return None

# ─── KG-Enhanced Pipeline ────────────────────────────────────────────────────

def run_pipeline(topic: str, output_dir: str = "./outputs") -> dict:
    """Run full ARP v3 pipeline with KG-CoT integration."""
    
    slug = make_slug(topic)
    out_path = Path(output_dir) / slug
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize KG-enhanced Hyper Layer
    hyper = HyperLayerKG(topic, kg_domain="arp_v3_research")
    
    print(f"\n{'='*60}")
    print(f"ARP v3 KG-CoT — {topic}")
    print(f"{'='*60}\n")
    
    # Pre-seed KG with known failure patterns
    hyper.kg.add_pattern(
        "http_401_auth",
        "API authentication error 401",
        "failure",
        context="OpenRouter API",
        evidence="User not found"
    )
    hyper.kg.add_pattern(
        "short_output",
        "output length less than 200 chars",
        "failure",
        context="Quality issue",
        evidence="Model produced minimal output"
    )
    
    # Phase 2: Research
    print("[PHASE 2] Research with KG-CoT...")
    research = run_agent_with_kg("researcher", topic, hyper) or "No research output."
    (out_path / f"{slug}-research.md").write_text(research)
    
    # Phase 2b: Document Extraction
    doc_path = Path(output_dir).parent / "documents"
    extracted_text = None
    if doc_path.exists():
        pdfs = list(doc_path.glob("*.pdf")) + list(doc_path.glob("*.png"))
        if pdfs:
            print(f"\n[PHASE 2b] Extracting {len(pdfs)} document(s)...")
            for pdf in pdfs[:3]:
                text = extract_document(str(pdf), str(out_path / "extracted"))
                if text:
                    extracted_text = (extracted_text or "") + f"\n\n# From: {pdf.name}\n\n{text[:5000]}"
    
    analysis_context = research
    if extracted_text:
        analysis_context += f"\n\n## Extracted Documents\n{extracted_text}"
    
    # Phase 2c: Analysis with KG-CoT
    print("\n[PHASE 2c] Analysis with KG-CoT...")
    analysis = run_agent_with_kg("analyst", topic, hyper, context=analysis_context) or "No analysis output."
    (out_path / f"{slug}-analysis.md").write_text(analysis)
    
    # Phase 2d: Review with KG-CoT
    print("\n[PHASE 2d] Review with KG-CoT...")
    review = run_agent_with_kg("reviewer", topic, hyper, context=f"RESEARCH:\n{research}\n\nANALYSIS:\n{analysis}") or "No review output."
    (out_path / f"{slug}-review.md").write_text(review)
    
    # Phase 3: Hyper Report
    print("\n[PHASE 3] Hyper Layer Report...")
    hyper_report = hyper.get_report()
    (out_path / f"{slug}-hyper-report.md").write_text(hyper_report)
    print(hyper_report)
    
    # Phase 4: Debate
    print("\n[PHASE 4] Debate...")
    debate = run_agent_with_kg("debater", topic, hyper, context=f"RESEARCH:\n{research}\n\nANALYSIS:\n{analysis}") or "No debate output."
    (out_path / f"{slug}-debate.md").write_text(debate)
    
    # Phase 5: Synthesis
    print("\n[PHASE 5] Synthesis...")
    synthesis = run_agent_with_kg("synthesizer", topic, hyper, context=f"RESEARCH:\n{research}\n\nANALYSIS:\n{analysis}\n\nREVIEW:\n{review}\n\nDEBATE:\n{debate}") or "No synthesis output."
    (out_path / f"{slug}-synthesis.md").write_text(synthesis)
    
    # Final output
    final = f"""# ARP v3 KG-CoT — {topic}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Slug:** {slug}
**Model Team:** minimax (lead) + Nemotron (researcher/analyst) + Stepfun (reviewer) + Free (debater)
**KG-CoT:** Morrissette-style Knowledge Graph integration

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
    
    # Knowledge Graph Dump
    kg_dump = f"# Knowledge Graph Dump for {slug}\n\n{hyper.kg.get_report()}\n\n"
    for pid, node in hyper.kg.nodes.items():
        kg_dump += f"\n## {pid}\n"
        kg_dump += f"- Outcome: {node['outcome']}\n"
        kg_dump += f"- Context: {node['context']}\n"
        kg_dump += f"- Evidence: {node['evidence'][:200]}\n"
        kg_dump += f"- Timestamp: {node['timestamp']}\n"
        kg_dump += f"- Hits: {node['hits']}\n"
    (out_path / f"{slug}-knowledge-graph.md").write_text(kg_dump)
    
    print(f"\n{'='*60}")
    print(f"✅ Complete! Files in: {out_path}")
    print(f"   Main output: {slug}-FINAL.md")
    print(f"   KG dump: {slug}-knowledge-graph.md")
    print(f"   KG interventions: {len(hyper.interventions)}")
    print(f"{'='*60}\n")
    
    return {
        "slug": slug,
        "path": str(out_path),
        "hyper_report": hyper_report,
        "kg_interventions": hyper.interventions,
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
    print(f"\nKG interventions triggered: {len(result['kg_interventions'])}")
