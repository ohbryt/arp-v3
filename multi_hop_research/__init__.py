"""
Multi-Hop Research Analysis System v3
Brown Biotech — AI-Powered Research Pipeline

Usage (with web_search tool):
  1. web_search("NASH drugs 2025") → sources
  2. MiniMaxClient.analyze(sources, query) → report

Or via CLI:
  python3 -m multi_hop_research --service pipeline --query "NASH drugs"
"""

import os
import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

MINIMAX_API = "https://api.minimax.io/v1"


# ─────────────────────────────────────────
# DATA CLASSES
# ─────────────────────────────────────────

class ServiceType(Enum):
    DUE_DILIGENCE = "due_diligence"
    DRUG_PIPELINE = "drug_pipeline"
    COMPETITOR_INTEL = "competitor_intel"
    MARKET_RESEARCH = "market_research"
    PAPER_REVIEW = "paper_review"


@dataclass
class Source:
    title: str
    url: str
    snippet: str
    domain: str = "web"


@dataclass
class ResearchResult:
    query: str
    service: str
    report: str
    sources: list
    latency_seconds: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)


# ─────────────────────────────────────────
# MINIMAX LLM (OpenAI-compatible)
# ─────────────────────────────────────────

class MiniMaxLLM:
    """MiniMax LLM client (OpenAI-compatible API)"""

    def __init__(self, api_key: str):
        self.api_key = api_key

    def analyze(self, sources: list[Source], query: str,
                service: str = "drug_pipeline",
                depth: int = 3) -> str:
        """Multi-hop analysis + report generation"""
        import urllib.request

        service_prompts = {
            "due_diligence": (
                "당신은 의약학 Due Diligence 전문가입니다. "
                "출처를 바탕으로 엄격하게 분석하여 보고서를 작성하세요.\n"
                "구조: 1) Executive Summary 2) 지적재산권 3) 임상데이터 "
                "4) 규제환경 5) 투자 의견\n"
                "모든 사실은 출처로 근거를 제시하세요."
            ),
            "drug_pipeline": (
                "당신은 의약품 R&D 파이프라인 분석 전문가입니다. "
                "아래 출처를 바탕으로 분석 보고서를 작성하세요.\n"
                "구조: 1) Executive Summary 2) 치료 영역 현황 "
                "3) 파이프라인 (기전별/임상단계) 4) 주요 후보 5) 시장 6) 결론\n"
                "모든 사실에 [출처: 제목](URL) 형식으로 출처 표기."
            ),
            "competitor_intel": (
                "당신은 경쟁사 분석 전문가입니다. "
                "출처를 바탕으로 SWOT 분석과 전략 권고서를 작성하세요.\n"
                "구조: 1) Executive Summary 2) 회사/제품 현황 "
                "3) SWOT 4) Pricing 5) 전략 권고\n"
                "모든 사실에 출처 표기."
            ),
            "market_research": (
                "당신은 시장 조사 전문가입니다. "
                "출처를 바탕으로 시장 분석 보고서를 작성하세요.\n"
                "구조: 1) Executive Summary 2) 시장 규모 3) 성장률 "
                "4) 경쟁 구도 5) 기회/위협 6) 결론\n"
                "모든 사실에 출처 표기."
            ),
            "paper_review": (
                "당신은 의학 논문 리뷰 전문가입니다. "
                "출처를 바탕으로 핵심 논문 리뷰를 작성하세요.\n"
                "구조: 1) 핵심 발견 2) 방법론 평가 3) Limitation "
                "4) 산업적 시사점 5) 향후研究方向\n"
                "모든 사실에 출처 표기."
            ),
        }

        prompt = service_prompts.get(service, service_prompts["drug_pipeline"])

        # Format sources
        source_text = "\n".join([
            f"- [{s.title}]({s.url})\n  {s.snippet}"
            for s in sources[:20]
        ])

        user_msg = f"""분석 주제: {query}

검색 출처 ({len(sources)}건):
{source_text}

위 출처를 바탕으로 전문적인 분석 보고서를 Markdown으로 작성하세요.
각 주장에는 반드시 [출처: 제목](URL) 형식으로 출처를 명시하세요.
완벽한 Markdown 형식으로 작성하세요."""

        payload = {
            "model": "MiniMax-M2.7",
            "messages": [
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_msg}
            ],
            "max_tokens": 8192,
            "temperature": 0.3,
        }

        req = urllib.request.Request(
            f"{MINIMAX_API}/chat/completions",
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[LLM Error: {e}]"


# ─────────────────────────────────────────
# CLI INTERFACE
# ─────────────────────────────────────────

def get_mm_key() -> str:
    """Get MiniMax API key from common locations"""
    # Try environment variable first
    key = os.environ.get("MINIMAX_API_KEY", "")
    if key:
        return key
    # Try ~/.env
    env_file = os.path.expanduser("~/.env")
    if os.path.exists(env_file):
        for line in open(env_file).read().split("\n"):
            if "minimax" in line.lower() and "key" in line.lower():
                return line.split("=", 1)[1].strip()
    return ""


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Multi-Hop Research CLI")
    parser.add_argument("--service", "-s",
                        choices=["pipeline", "dd", "intel", "market", "paper"],
                        default="pipeline")
    parser.add_argument("--query", "-q", required=True)
    parser.add_argument("--depth", "-d", type=int, choices=[1, 2, 3], default=2)
    args = parser.parse_args()

    service_map = {
        "pipeline": "drug_pipeline",
        "dd": "due_diligence",
        "intel": "competitor_intel",
        "market": "market_research",
        "paper": "paper_review"
    }

    mm_key = get_mm_key()
    if not mm_key:
        print("ERROR: MINIMAX_API_KEY not found")
        return

    llm = MiniMaxLLM(mm_key)

    print(f"\n{'='*60}")
    print(f"Multi-Hop Research — {service_map[args.service]}")
    print(f"Query: {args.query}")
    print(f"Depth: {args.depth}")
    print(f"{'='*60}")

    # NOTE: Run web_search in your main agent, then call:
    #   result = llm.analyze(sources, query, service_map[args.service])
    # This file is the LLM + CLI layer only.

    print("""
NOTE: This is the LLM analysis layer.
For full pipeline, use this in your agent:

  from multi_hop_research import MiniMaxLLM
  sources = [...]  # from web_search tool
  llm = MiniMaxLLM(api_key)
  report = llm.analyze(sources, query, service="drug_pipeline")
  print(report)

Or use the CLI:
  python3 -m multi_hop_research --service pipeline --query "NASH drugs"
""")


if __name__ == "__main__":
    main()
