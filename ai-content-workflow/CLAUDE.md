# AI Content-to-Cash Workflow

이 폴더는 Dr. OCM의 콘텐츠 제작 파이프라인입니다.

## 목표
```
TinyFish (웹调研) → Markdown → Claude Code (분석) → 콘텐츠創作
```

## 핵심 도구
- **TinyFish API**: sk-tinyfish-d85Piw8gdzmnX4w9E5g2_vlJrSfVe7xe
- **Claude Code**: 분석 및 콘텐츠生成
- **NotebookLM**: (선택) Gemini 기반 문서 요약

## 사용 방법

### 1단계: TinyFish调研
```bash
cd scripts
python3 run_tinyfish_research.py --topic "주제" --search-engine duckduckgo
```

### 2단계: Claude Code 분석
Claude Code에서:
```
이 폴더의 모든 md 파일을 읽고, 주제에 대해 좋은 질문을 20개 생성해줘.
각 질문에 답변을 文献 바탕으로 작성해줘.
```

### 3단계: 콘텐츠 생성
```bash
python3 scripts/generate_content.py --topic "주제" --format seminar
```

## 폴더 구조
- `01_raw_sources/` — TinyFish 원본
- `02_markdown/` — 정제 Markdown
- `03_knowledge_base/` — 분석용
- `04_qa_results/` — Q&A 쌍
- `05_content_output/` — 최종 산출물
