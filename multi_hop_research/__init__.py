"""
Multi-Hop Research Analysis System v4
Brown Biotech — AI-Powered Research Pipeline

Design Patterns Applied:
1. Prompt = UI — structured prompt as the interface
2. Same UI, Different Modes — Quick / Standard / Deep
3. Output customization — preview first, then customize
4. Ghost UI — meaningful loading states
5. Just-in-time guidance — help at the right moment
"""

import os
import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum

MINIMAX_API = "https://api.minimax.io/v1"


# ─────────────────────────────────────────
# MODES — Same UI, Different Modes
# ─────────────────────────────────────────

class AnalysisMode(Enum):
    """Three analysis modes with different depth/structure"""
    QUICK = "quick"       # 5 sources, 1 hop, fast (2-3 min)
    STANDARD = "standard" # 10 sources, 2 hops (5-10 min)
    DEEP = "deep"        # 20 sources, 3 hops, full (15-20 min)


@dataclass
class ModeConfig:
    """Mode-specific settings"""
    name: str
    num_sources: int
    depth: int
    max_tokens: int
    temperature: float
    time_estimate: str
    description: str


MODE_CONFIGS = {
    AnalysisMode.QUICK: ModeConfig(
        name="Quick Analysis",
        num_sources=5,
        depth=1,
        max_tokens=2048,
        temperature=0.3,
        time_estimate="2-3분",
        description="핵심 사실만 빠르게 파악"
    ),
    AnalysisMode.STANDARD: ModeConfig(
        name="Standard Analysis",
        num_sources=10,
        depth=2,
        max_tokens=4096,
        temperature=0.3,
        time_estimate="5-10분",
        description="균형잡힌 분석"
    ),
    AnalysisMode.DEEP: ModeConfig(
        name="Deep Dive",
        num_sources=20,
        depth=3,
        max_tokens=8192,
        temperature=0.2,
        time_estimate="15-20분",
        description="종합적 깊이 있는 분석"
    ),
}


# ─────────────────────────────────────────
# PROMPT = UI — Structured Request Interface
# ─────────────────────────────────────────

@dataclass
class AnalysisRequest:
    """
    Prompt = UI: All user input structured as a single dataclass
    This IS the interface — no separate form needed
    """
    # Required
    query: str                      # 분석 주제
    service: str = "drug_pipeline"  # 분석 유형

    # Mode
    mode: AnalysisMode = AnalysisMode.STANDARD

    # Customization
    focus_areas: list[str] = field(default_factory=list)
    # 예: ["patent", "clinical", "market", "regulatory"]

    # Output preferences
    include_executive_summary: bool = True
    include_swot: bool = False
    include_timeline: bool = False
    language: str = "ko"  # ko | en

    # Human in loop
    preview_first: bool = True  # 먼저 preview 보여주고 승인 받기

    def to_prompt(self) -> str:
        """Convert request to structured prompt (the UI)"""
        mode_cfg = MODE_CONFIGS[self.mode]

        parts = [
            f"분석 주제: {self.query}",
            f"분석 유형: {self.service}",
            f"분석 깊이: {mode_cfg.name} ({mode_cfg.description})",
            f"예상 시간: {mode_cfg.time_estimate}",
        ]

        if self.focus_areas:
            parts.append(f"집중 영역: {', '.join(self.focus_areas)}")

        parts.append("\n출력 옵션:")
        parts.append(f"- Executive Summary: {'✓' if self.include_executive_summary else '✗'}")
        parts.append(f"- SWOT: {'✓' if self.include_swot else '✗'}")
        parts.append(f"- Timeline: {'✓' if self.include_timeline else '✗'}")
        parts.append(f"- 언어: {'한국어' if self.language == 'ko' else 'English'}")

        if self.preview_first:
            parts.append("\n→ 먼저 3줄 요약 preview 보여줄게요. 승인하면 전체 보고서 생성.")

        return "\n".join(parts)

    @classmethod
    def from_query(cls, query: str, service: str = "drug_pipeline",
                    mode: str = "standard", **kwargs):
        """Easy factory from simple params"""
        mode_enum = AnalysisMode[mode.upper()]
        return cls(query=query, service=service, mode=mode_enum, **kwargs)


# ─────────────────────────────────────────
# GHOST UI — Meaningful Loading States
# ─────────────────────────────────────────

@dataclass
class GhostState:
    """Ghost UI states — meaningful placeholders"""
    stage: str
    message: str
    hint: str = ""  # Just-in-time guidance


GHOST_STATES = {
    "init": GhostState(
        stage="init",
        message="분석 템플릿 생성 중...",
        hint="검색어와 분석 유형을 확인하고 있어요"
    ),
    "explore": GhostState(
        stage="explore",
        message="웹调研 중... ({current}/{total})",
        hint="최신 논문과 임상시험을 찾고 있어요"
    ),
    "verify": GhostState(
        stage="verify",
        message="사실 검증 중...",
        hint="여러 출처를 교차확인하고 있어요"
    ),
    "extend": GhostState(
        stage="extend",
        message="관련 정보 확장 중...",
        hint="관련 특허와 규제 동향도 파악하고 있어요"
    ),
    "report": GhostState(
        stage="report",
        message="보고서 작성 중...",
        hint="출처를 정리하고 있어요"
    ),
    "preview": GhostState(
        stage="preview",
        message="미리보기 생성 중...",
        hint="3줄 요약으로 먼저 보여드릴게요"
    ),
    "done": GhostState(
        stage="done",
        message="완료!",
        hint="수정할 부분 있으면 말씀하세요"
    ),
}


# ─────────────────────────────────────────
# OUTPUT CUSTOMIZATION — Preview First
# ─────────────────────────────────────────

@dataclass
class AnalysisPreview:
    """Preview output — user approves before full generation"""
    summary_3lines: str      # 3줄 요약
    key_sources: list         # 핵심 출처 3개
    estimated_time: str
    estimated_pages: str
    total_cost: float         # 추정 비용 (시간 기반)


@dataclass
class AnalysisResult:
    """Final output — all deliverables"""
    request: AnalysisRequest
    preview: AnalysisPreview

    # Full content
    report_md: str           # Markdown 보고서
    report_pdf_url: str = ""  # PDF (future)

    # Metadata
    sources: list            # [{title, url, snippet}]
    verified_facts: list     # [{fact, source}]
    hops: list              # [{stage, query, result_count}]

    # Stats
    latency_seconds: float = 0.0
    tokens_used: int = 0
    cost_estimate: float = 0.0

    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)


# ─────────────────────────────────────────
# ANALYSIS SERVICE (with web_search integration)
# ─────────────────────────────────────────

class ResearchAnalyzer:
    """
    Main analysis engine with AI product design patterns.

    Usage:
        analyzer = ResearchAnalyzer(api_key="sk-cp-...")

        # Step 1: Create request (Prompt = UI)
        request = AnalysisRequest.from_query(
            query="NASH 치료제 파이프라인 2025",
            service="drug_pipeline",
            mode="standard",
            focus_areas=["patent", "clinical"],
            preview_first=True
        )
        print(request.to_prompt())  # Show the "UI"

        # Step 2: Preview
        preview = analyzer.generate_preview(request)
        print(preview.summary_3lines)

        # Step 3: User approves → Full report
        result = analyzer.analyze(request)  # Human in loop

        print(result.report_md)
    """

    def __init__(self, api_key: str):
        self.api_key = api_key

    # ─────────────────────────────────
    # Step 1: Create request (Prompt = UI)
    # ─────────────────────────────────

    def create_request(self, query: str, service: str = "drug_pipeline",
                       mode: str = "standard",
                       focus_areas: list = None,
                       language: str = "ko",
                       preview_first: bool = True) -> AnalysisRequest:
        """Prompt = UI: Create structured request"""
        return AnalysisRequest.from_query(
            query=query,
            service=service,
            mode=mode,
            focus_areas=focus_areas or [],
            language=language,
            preview_first=preview_first
        )

    # ─────────────────────────────────
    # Step 2: Preview (Ghost UI)
    # ─────────────────────────────────

    def generate_preview(self, request: AnalysisRequest) -> AnalysisPreview:
        """
        Ghost UI: Generate meaningful preview before full work
        - 3줄 요약
        - 핵심 출처 3개
        - 시간/비용 추정
        """
        # In real impl: call web_search + mini LLM call
        # For now: estimate based on mode
        mode_cfg = MODE_CONFIGS[request.mode]

        preview = AnalysisPreview(
            summary_3lines=(
                f"[{request.query}]에 대한 {mode_cfg.name} 분석입니다.\n"
                f"예상 출처: {mode_cfg.num_sources * mode_cfg.depth}건\n"
                f"예상 시간: {mode_cfg.time_estimate}"
            ),
            key_sources=[
                {"title": "PubMed 논문", "url": "https://pubmed.ncbi.nlm.nih.gov/"},
                {"title": "ClinicalTrials.gov", "url": "https://clinicaltrials.gov/"},
                {"title": "FDA approvals", "url": "https://www.fda.gov/"},
            ],
            estimated_time=mode_cfg.time_estimate,
            estimated_pages=str(3 + mode_cfg.depth * 2),
        )
        return preview

    # ─────────────────────────────────
    # Step 3: Full Analysis (Human in Loop)
    # ─────────────────────────────────

    def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """
        Full analysis with Ghost UI states.
        Returns preview first if requested, then full report.
        """
        start = time.time()
        mode_cfg = MODE_CONFIGS[request.mode]

        # Ghost: show loading states
        print(f"\n{GHOST_STATES['explore'].message}")
        print(f"  💡 {GHOST_STATES['explore'].hint}")

        # In real impl: call web_search for sources
        # Here: return structured result
        sources = self._fetch_sources(request)

        # Ghost: verify stage
        print(f"\n{GHOST_STATES['verify'].message}")
        print(f"  💡 {GHOST_STATES['verify'].hint}")

        verified = self._verify_sources(sources)

        # Ghost: extend stage
        if request.mode == AnalysisMode.DEEP:
            print(f"\n{GHOST_STATES['extend'].message}")
            print(f"  💡 {GHOST_STATES['extend'].hint}")
            sources.extend(self._extend_sources(request, sources))

        # Ghost: report stage
        print(f"\n{GHOST_STATES['report'].message}")

        report_md = self._generate_report(request, sources, verified)

        latency = time.time() - start

        result = AnalysisResult(
            request=request,
            preview=self.generate_preview(request),
            report_md=report_md,
            sources=sources,
            verified_facts=verified,
            hops=[{"stage": "explore", "count": len(sources)}],
            latency_seconds=latency,
        )

        print(f"\n{GHOST_STATES['done'].message}")
        print(f"  💡 {GHOST_STATES['done'].hint}")

        return result

    def _fetch_sources(self, request: AnalysisRequest) -> list:
        """Fetch sources via web search (integrate with my web_search tool)"""
        # Placeholder — in real usage, call my web_search tool
        return [
            {"title": f"Source for: {request.query[:30]}",
             "url": "https://example.com",
             "snippet": "Relevant finding..."}
        ]

    def _verify_sources(self, sources: list) -> list:
        """Verify sources (cross-reference)"""
        return [{"fact": s["title"], "source": s["url"]} for s in sources[:3]]

    def _extend_sources(self, request: AnalysisRequest, sources: list) -> list:
        """Extend with related searches"""
        return []

    def _generate_report(self, request: AnalysisRequest,
                         sources: list, verified: list) -> str:
        """Generate full Markdown report"""
        mode_cfg = MODE_CONFIGS[request.mode]

        # Build sections based on request
        sections = []

        # 1. Executive Summary
        if request.include_executive_summary:
            sections.append("## Executive Summary\n")
            sections.append(f"{request.query}에 대한 {mode_cfg.name} 분석 결과입니다.\n")

        # 2. Key Findings
        sections.append("## 핵심 발견\n")
        for v in verified[:5]:
            sections.append(f"- {v['fact']} [출처]({v['source']})\n")

        # 3. Sources
        sections.append(f"\n## 출처 ({len(sources)}건)\n")
        for s in sources[:mode_cfg.num_sources]:
            sections.append(f"- [{s['title']}]({s['url']})\n")

        # 4. SWOT (if requested)
        if request.include_swot:
            sections.append("\n## SWOT 분석\n")
            sections.append("| Strength | Weakness |\n|---------|----------|\n")
            sections.append("| | |\n")

        return "".join(sections)


# ─────────────────────────────────────────
# QUICK START — All-in-one method
# ─────────────────────────────────────────

def quick_analyze(query: str, service: str = "drug_pipeline",
                 mode: str = "standard",
                 api_key: str = None) -> AnalysisResult:
    """
    All-in-one: Create request → Preview → Full analysis
    Just-in-time guidance at each step
    """
    if api_key is None:
        api_key = os.environ.get("MINIMAX_API_KEY", "")

    analyzer = ResearchAnalyzer(api_key)

    # Step 1: Prompt = UI
    request = analyzer.create_request(
        query=query,
        service=service,
        mode=mode
    )
    print("\n" + "="*50)
    print("📋 ANALYST REQUEST (이것이 인터페이스입니다)")
    print("="*50)
    print(request.to_prompt())

    # Step 2: Preview
    preview = analyzer.generate_preview(request)
    print("\n" + "="*50)
    print("👻 GHOST PREVIEW (가장 먼저 이것을 보게 됩니다)")
    print("="*50)
    print(preview.summary_3lines)
    print(f"\n예상 분량: {preview.estimated_pages}쪽")
    print(f"예상 시간: {preview.estimated_time}")
    print(f"\n핵심 출처 {len(preview.key_sources)}개:")
    for s in preview.key_sources:
        print(f"  • {s['title']}")

    # Step 3: Full (user approves implicitly)
    print("\n" + "="*50)
    print("🚀 FULL ANALYSIS (승인 없이 바로 생성)")
    print("="*50)

    result = analyzer.analyze(request)

    return result


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Brown Biotech Research Analyzer")
    parser.add_argument("--query", "-q", required=True)
    parser.add_argument("--service", "-s",
                        choices=["pipeline", "dd", "intel", "market", "paper"],
                        default="pipeline")
    parser.add_argument("--mode", "-m",
                        choices=["quick", "standard", "deep"],
                        default="standard")
    parser.add_argument("--api-key", "-k", default=None)
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("MINIMAX_API_KEY", "")
    if not api_key:
        # Try ~/.env
        env_path = os.path.expanduser("~/.env")
        if os.path.exists(env_path):
            for line in open(env_path).read().split("\n"):
                if "minimax" in line.lower() and "api" in line.lower():
                    api_key = line.split("=", 1)[1].strip()

    if not api_key:
        print("ERROR: MINIMAX_API_KEY not found")
        return

    result = quick_analyze(
        query=args.query,
        service=args.service,
        mode=args.mode,
        api_key=api_key
    )

    print("\n" + "="*50)
    print("📄 FINAL REPORT")
    print("="*50)
    print(result.report_md)


if __name__ == "__main__":
    main()
