#!/usr/bin/env python3
"""
AI Content Pipeline — v2 (Evals-Inspired)
Based on Deep Agents' eval framework

매번 실행할 때:
1. TinyFish调研 → 결과 검증 (eval)
2. Claude Code 분석 → 정확성 + 효율성 측정
3. 실패하면 → eval 추가
4. 모든 결과를 추적

Usage:
  python3 run_workflow.py --topic "당뇨병 치료제" --format seminar
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional

TINYFISH_API = "https://agent.tinyfish.ai/v1/automation/run-sse"
OUTPUT_DIR = Path(__file__).parent.parent

@dataclass
class EvalResult:
    """단일 eval 결과"""
    name: str
    passed: bool
    correct: bool = True
    efficiency: float = 1.0  # 0-1, 1이最高
    solve_rate: float = 1.0  # 0-1
    latency_seconds: float = 0.0
    cost_tokens: int = 0
    error: Optional[str] = None
    description: str = ""
    notes: str = ""

@dataclass
class WorkflowRun:
    """전체 workflow 실행 결과"""
    run_id: str
    timestamp: str
    topic: str
    format: str
    evals: list = field(default_factory=list)
    total_cost: float = 0.0
    total_latency: float = 0.0
    
    @property
    def solve_rate(self) -> float:
        if not self.evals:
            return 0.0
        return sum(e.solve_rate for e in self.evals) / len(self.evals)
    
    @property
    def passed(self) -> bool:
        return all(e.passed for e in self.evals)
    
    def to_dict(self):
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "topic": self.topic,
            "format": self.format,
            "passed": self.passed,
            "solve_rate": self.solve_rate,
            "total_latency": self.total_latency,
            "total_cost": self.total_cost,
            "evals": [asdict(e) for e in self.evals]
        }


# ─────────────────────────────────────────
# EVAL DEFINITIONS (우리 workflow 평가기준)
# ─────────────────────────────────────────
EVALS = {
    "tinyfish": [
        {
            "name": "web_page_loaded",
            "check": lambda r: r.get("status") == "ok",
            "description": "웹페이지 로드 성공"
        },
        {
            "name": "content_extracted",
            "check": lambda r: len(r.get("results", [])) >= 5,
            "description": "최소 5개 결과 추출"
        },
        {
            "name": "valid_sources",
            "check": lambda r: all(
                bool(item.get("source")) 
                for item in r.get("results", [])[:5]
            ),
            "description": "모든 결과에 출처 명시"
        },
    ],
    "claude_code": [
        {
            "name": "questions_generated",
            "check": lambda r: len(r.get("questions", [])) >= 10,
            "description": "최소 10개 질문 생성"
        },
        {
            "name": "answers_based_on_sources",
            "check": lambda r: all(
                bool(ans.get("source")) 
                for ans in r.get("answers", [])
            ),
            "description": "모든 답변에 출처 표기"
        },
    ],
    "content": [
        {
            "name": "format_correct",
            "check": lambda r: bool(r.get("content")),
            "description": "콘텐츠 생성됨"
        },
        {
            "name": "min_length",
            "check": lambda r: len(r.get("content", "")) >= 500,
            "description": "최소 500자"
        },
        {
            "name": "no_hallucination",
            "check": lambda r: "[출처:" in r.get("content", ""),
            "description": "출처 표기 있음 (hallucination 방지)"
        },
    ]
}

def run_evals(stage: str, result: dict) -> list[EvalResult]:
    """stage별 eval 실행"""
    evals = []
    for eval_def in EVALS.get(stage, []):
        try:
            passed = eval_def["check"](result)
            evals.append(EvalResult(
                name=eval_def["name"],
                passed=passed,
                correct=passed,
                solve_rate=1.0 if passed else 0.0,
                efficiency=1.0 if passed else 0.5,
                description=eval_def.get("description", ""),
            ))
        except Exception as e:
            evals.append(EvalResult(
                name=eval_def["name"],
                passed=False,
                correct=False,
                solve_rate=0.0,
                error=str(e),
                description=eval_def.get("description", ""),
            ))
    return evals

def load_previous_evals() -> list:
    """이전 evals 결과 로드 (추적용)"""
    history_file = OUTPUT_DIR / ".eval_history.json"
    if history_file.exists():
        return json.loads(history_file.read_text())
    return []

def save_eval_history(history: list):
    """eval history 저장"""
    history_file = OUTPUT_DIR / ".eval_history.json"
    history_file.write_text(json.dumps(history, ensure_ascii=False, indent=2))

# ─────────────────────────────────────────
# TINYFISH调研
# ─────────────────────────────────────────
def run_tinyfish(topic: str, search_queries: list[str]) -> dict:
    """TinyFish로 웹调研 + eval 실행"""
    import urllib.request
    import subprocess
    
    api_key = os.environ.get("TINYFISH_API_KEY", "")
    if not api_key:
        # Try .env
        for line in (Path.home() / ".openclaw" / "workspace" / ".env").read_text().split("\n"):
            if "TINYFISH_API_KEY" in line:
                api_key = line.split("=", 1)[1].strip()
    
    results = []
    all_results = []
    
    for query in search_queries:
        print(f"\n🔍 [{query[:50]}...]")
        
        data = {
            "url": "https://duckduckgo.com",
            "goal": f"Search for: {query}. Extract titles, sources, and summaries of top 10 results.",
            "browser_profile": "lite"
        }
        
        process = subprocess.Popen(
            ["curl", "-s", "-N", "-X", "POST", TINYFISH_API,
             "-H", f"X-API-Key: {api_key}",
             "-H", "Content-Type: application/json",
             "-d", json.dumps(data)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        
        for line in process.stdout:
            if line.startswith("data: "):
                try:
                    event = json.loads(line[6:].strip())
                    if event.get("type") == "PROGRESS":
                        print(f"   {event.get('purpose', '')[:50]}...")
                    elif event.get("type") == "COMPLETED":
                        result_data = event.get("result", {})
                        results.append(result_data)
                        print(f"   ✅ Done")
                except json.JSONDecodeError:
                    pass
        
        process.wait()
    
    # Combine results
    combined = {"results": results, "status": "ok" if results else "error"}
    evals = run_evals("tinyfish", combined)
    
    return {
        "raw_results": results,
        "evals": evals,
        "status": combined["status"]
    }

# ─────────────────────────────────────────
# CONTENT GENERATION (Claude Code용 프롬프트)
# ─────────────────────────────────────────
def generate_claude_prompt(topic: str, tinyfish_results: dict) -> str:
    """Claude Code용 분석 프롬프트 생성"""
    
    # Extract key info from TinyFish results
    sources_text = ""
    for r in tinyfish_results.get("raw_results", []):
        for item in r.get("results", [])[:10]:
            title = item.get("title", "")
            source = item.get("source", "")
            url = item.get("url", "")
            snippet = item.get("snippet", "")
            sources_text += f"- [{title}]({url}) ({source})\n  {snippet}\n\n"
    
    prompt = f"""# 분석 요청: {topic}

## 웹调研 결과

{sources_text}

## 질문 생성

위의调研 결과를 바탕으로 {topic}에 대해 좋은 질문 20개를 생성해줘.

형식:
1. [질문]
2. [질문]
...

## 답변 작성

각 질문에 대해上面的调研 결과를 바탕으로 답변을 작성해줘.

형식:
### [질문]
[답변]
[출처: 제목](URL)

단, hallucination 없이 오직调研 결과에서 찾은 내용만 바탕으로 작성해줘.
"""
    return prompt

# ─────────────────────────────────────────
# MAIN WORKFLOW
# ─────────────────────────────────────────
def run_workflow(topic: str, content_format: str = "seminar") -> WorkflowRun:
    """전체 workflow 실행"""
    import uuid
    
    run_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().isoformat()
    
    print(f"\n{'='*60}")
    print(f"🚀 Workflow Started: {run_id}")
    print(f"   Topic: {topic}")
    print(f"   Format: {content_format}")
    print(f"{'='*60}")
    
    workflow_run = WorkflowRun(
        run_id=run_id,
        timestamp=timestamp,
        topic=topic,
        format=content_format
    )
    
    # Stage 1: TinyFish调研
    print(f"\n[STAGE 1] TinyFish调研")
    print("-" * 40)
    
    queries = [
        f"{topic} latest research and clinical trials",
        f"{topic} drug pipeline mechanism companies",
        f"{topic} market analysis trends",
    ]
    
    tinyfish_results = run_tinyfish(topic, queries)
    workflow_run.evals.extend(tinyfish_results["evals"])
    
    # Stage 2: Claude Code 분석용 프롬프트
    print(f"\n[STAGE 2] Claude Code 분석")
    print("-" * 40)
    
    prompt = generate_claude_prompt(topic, tinyfish_results)
    
    # Save prompt for Claude Code
    prompt_file = OUTPUT_DIR / f"03_knowledge_base/{run_id}_prompt.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text(prompt)
    print(f"✅ Prompt saved: {prompt_file}")
    
    # Next steps
    print(f"\n[STAGE 3] Claude Code 실행 (Manual)")
    print("-" * 40)
    print(f"""
다음 명령으로 Claude Code에서 분석하세요:

  cd {OUTPUT_DIR}
  claude

프롬프트 파일:
  {prompt_file}

질문/답변을 저장할 디렉토리:
  04_qa_results/{run_id}_qa.md

모든 evals 결과는 .eval_history.json에 저장됩니다.
    """)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Workflow Summary: {run_id}")
    print(f"{'='*60}")
    print(f"Topic: {topic}")
    print(f"TinyFish results: {len(tinyfish_results.get('raw_results', []))}")
    print(f"Evals passed: {sum(1 for e in workflow_run.evals if e.passed)}/{len(workflow_run.evals)}")
    print(f"Solve rate: {workflow_run.solve_rate:.1%}")
    
    # Save run history
    history = load_previous_evals()
    history.append(workflow_run.to_dict())
    save_eval_history(history)
    
    return workflow_run

def show_dashboard():
    """eval dashboard 표시"""
    history = load_previous_evals()
    
    print(f"\n{'='*60}")
    print(f"📊 Eval Dashboard — {len(history)} runs")
    print(f"{'='*60}")
    
    if not history:
        print("No runs yet. Run with: python3 run_workflow.py --topic '주제'")
        return
    
    for run in history[-10:]:  # Last 10
        solve_rate = run.get("solve_rate", 0)
        status = "✅" if run.get("passed") else "⚠️"
        print(f"\n{status} [{run['run_id']}] {run['topic']}")
        print(f"   Format: {run['format']}")
        print(f"   Solve rate: {solve_rate:.0%}")
        print(f"   Date: {run['timestamp'][:10]}")
        
        # Eval breakdown
        for e in run.get("evals", []):
            icon = "✅" if e["passed"] else "❌"
            print(f"   {icon} {e['name']}: {e.get('solve_rate', 0):.0%}")

def main():
    parser = argparse.ArgumentParser(description="AI Content Pipeline v2")
    parser.add_argument("--topic", "-t", required=True, help="연구 주제")
    parser.add_argument("--format", "-f", default="seminar",
                       choices=["blog", "seminar", "thread"],
                       help="콘텐츠 포맷")
    parser.add_argument("--dashboard", "-d", action="store_true",
                       help="eval dashboard 표시")
    
    args = parser.parse_args()
    
    if args.dashboard:
        show_dashboard()
    else:
        result = run_workflow(args.topic, args.format)
        print(f"\n✅ Run ID: {result.run_id}")
        print(f"   Use --dashboard to see history")

if __name__ == "__main__":
    main()
