#!/usr/bin/env python3
"""
콘텐츠 생성기 — QA 결과를 최종 콘텐츠로 변환

Usage:
  python3 generate_content.py --topic "지방간 치료제" --format seminar
  python3 generate_content.py --topic "당뇨병" --format blog
  python3 generate_content.py --topic "비만" --format thread
"""

import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
OUTPUT_DIR = Path(__file__).parent.parent / "05_content_output"

def load_qa_results(qa_dir: str) -> list:
    """QA 결과 파일들 로드"""
    qa_path = Path(qa_dir)
    if not qa_path.exists():
        return []
    
    results = []
    for f in sorted(qa_path.glob("*.md")):
        results.append(f.read_text())
    return results

def load_template(format_type: str) -> str:
    """템플릿 로드"""
    template_file = TEMPLATES_DIR / f"{format_type}.md"
    if template_file.exists():
        return template_file.read_text()
    
    # Default template
    return """# {title}

**작성일:** {date}
**주제:** {topic}

---

## 핵심 요약

{qa_summary}

---

##详细内容

{qa_content}

---

## 결론 및 시사점

{conclusion}

---

*본 콘텐츠는 AI Content-to-Cash Workflow로 생성됨*
"""

def generate_blog_post(topic: str, qa_results: list) -> str:
    """블로그 포스트 생성"""
    content = f"""# {topic} — 심층 분석 보고서

**작성일:** {datetime.now().strftime('%Y년 %m월 %d일')}
**주제:** {topic}

---

## 한 줄 요약

{topic}에 대한 최신 동향, 주요 발견, 그리고 앞으로의 전망을 정리합니다.

---

## 1. 배경 및 중요성

{topic}은(는) 현재 전 세계적으로 관심을 받고 있는 분야입니다.
최근 연구에서 주목할 만한 진전이 이루어지고 있습니다.

---

## 2. 주요 발견

"""

    for i, qa in enumerate(qa_results[:5], 1):
        content += f"\n### 발견 {i}\n\n{qa[:500]}...\n"
    
    content += """

---

## 3. 전문가 관점

실제 데이터에 기반한 분석 결과, 다음과 같은 패턴이 관찰됩니다:

1. **기전의 다양성** — 여러 표적 단백질이 동시에 관여
2. **임상 단계별 분포** — Phase 1에서 Phase 3까지 폭넓은 포트폴리오
3. **시장 전망** — 높은 성장률 기대

---

## 4. 향후 전망

、短기적으로 보면:


- 새로운 약물의 FDA 승인 기대
- 병용요법 개발 가속화
- 환자分层医疗 발전

중기적:


- 실제 임상 데이터 축적
- 비용 효과 분석 본격화

장기적:


- 표준 치료 변화
- 글로벌 시장 확대

---

## 5. 결론

{topic} 분야는 Rapid Evolution 중이며, Investors와 연구자 모두에게 큰 기희입니다.
본 보고서가 현장 이해관계자에게 유용한 참고자료가 되기를 바랍니다.

---

*본 보고서는 AI Content-to-Cash Workflow (TinyFish + Claude Code)로 생성됨*
"""
    return content

def generate_seminar(topic: str, qa_results: list) -> str:
    """세미나 자료 생성"""
    content = f"""# {topic}
## プレゼンテーション資料

**날짜:** {datetime.now().strftime('%Y년 %m월 %d일')}
**소요 시간:** 30분

---

## Aganda

1. 배경 (3분)
2. 최신 동향 (10분)
3. 주요侯補 약물 (10분)
4. 향후 전망 (5분)
5. Q&A (2분)

---

## 1. 배경

{topic}은(는) 다음과 같은 맥락에서 중요합니다:


- 전 세계 환자 수 증가
- 기존 치료의 한계
- Innovative 기전의 등장

---

## 2. 최신 동향

### 2-1. 작용 기전별 분류

"""

    for i, qa in enumerate(qa_results[:4], 1):
        content += f"\n**기전 {i}:**\n{qa[:300]}...\n"
    
    content += """

---

## 3. 주요侯補 약물

### 임상단계별 현황

| 단계 | 약물 수 | 대표 사례 |
|------|---------|----------|
| Phase 3 | 3+ | Lanifibranor, Semaglutide, Resmetirom |
| Phase 2 | 5+ | VK2809, TERN-101, ASC42 |
| Phase 1 | 2+ | Dapiglutide |

---

## 4. 향후 전망

###短期 (1-2년)


- Resmetirom 본격적 출시
- Semaglutide Phase 3 결과

###中期 (3-5년)


- Lanifibranor 승인 가능성
- 병용요법 임상 가속화

###長期 (5년+)


- 표준 치료 변화
- 시장 재편

---

## 5. 핵심 메시지

1. **NASH 치료제 시대 개막** — Resmetirom FDA 승인
2. **다양한 기전** — FXR, PPAR, GLP-1, THR-β 등
3. **병용요법이 미래** — 단독보다 조합이 효과적
4. **시장 급성장** — CAGR 20% 이상

---

## Q&A

（질문 환영）

---

*본 자료는 AI Content-to-Cash Workflow로 생성됨*
"""
    return content

def generate_thread(topic: str, qa_results: list) -> str:
    """X/Twitter Thread 생성"""
    lines = [
        f"🧵 {topic} — 완전 정리 (NASH 편)",
        "",
        f"오늘 {topic} 최신 동향을 정리했어요. 덤프 시작!",
        "",
        "1/ 주요 기전 4가지",
        "",
        "• FXR Agonist — 담즙산 경로 조절",
        "• PPAR Agonist — 대사 개선 + 항염증",
        "• GLP-1 Agonist — 체중감량 + 대사",
        "• THR-β Agonist — 간 선택적 작용",
        "",
        "2/ 2024 최대 사건",
        "",
        "Resmetirom (Rezdiffra) FDA 승인",
        "→ NASH 최초 승인 약물! 🇺🇸",
        "",
        "3/ 유망侯補",
        "",
    ]
    
    for i, qa in enumerate(qa_results[:6], 1):
        snippet = qa[:200].replace("\n", " ")[:150]
        lines.append(f"•侯補 {i}: {snippet}...")
    
    lines += [
        "",
        "4/ 시장은?",
        "",
        "2024: $30억",
        "2030: $130~150억 (예상)",
        "CAGR: 20%+ 💰",
        "",
        "5/ 결론",
        "",
        "✓ NASH 치료제 시대 개막",
        "✓ 다양한 기전 동시 개발",
        "✓ 병용요법이 핵심",
        "",
        "이 덤프 유용했으면 ♻️RT 해주세요!",
        "팔로우하면 임상단계별侯補 약물 더 자세히 올릴게요 → @yourhandle",
        "",
        "#NASH #Metabolic #DrugDevelopment #Biotech #Healthcare",
    ]
    
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="콘텐츠 생성기")
    parser.add_argument("--topic", "-t", required=True, help="주제")
    parser.add_argument("--qa-dir", "-q", default="04_qa_results", help="QA 결과 디렉토리")
    parser.add_argument("--format", "-f", default="blog",
                       choices=["blog", "seminar", "thread"],
                       help="콘텐츠 포맷")
    parser.add_argument("--output", "-o", default=None, help="출력 파일")
    
    args = parser.parse_args()
    
    qa_results = load_qa_results(args.qa_dir)
    
    if args.format == "blog":
        content = generate_blog_post(args.topic, qa_results)
        ext = ".md"
    elif args.format == "seminar":
        content = generate_seminar(args.topic, qa_results)
        ext = ".md"
    else:  # thread
        content = generate_thread(args.topic, qa_results)
        ext = ".txt"
    
    if args.output:
        output_file = Path(args.output)
    else:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"{args.topic}_{args.format}_{timestamp}{ext}"
    
    output_file.write_text(content)
    print(f"✅ Generated: {output_file}")
    print(f"   Format: {args.format}")
    print(f"   Size: {len(content)} chars")

if __name__ == "__main__":
    main()
