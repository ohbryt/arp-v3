# AI 内容变现工作流 (AI Content-to-Cash Workflow)

## 概述

```
信息来源
  │
  ├─ TinyFish (웹 자동调研)
  │     ↓
  │   Markdown (.md)
  │     ↓
  └─ 로컬 저장 (01_raw_sources/)
        ↓
    Claude Code (분석 + 질문 생성)
        ↓
    로컬 QA 결과 (04_qa_results/)
        ↓
    콘텐츠創作 (05_content_output/)
        ↓
    배포 (Notion, 블로그, 세미나, X/Twitter)
```

## 구성 요소

| 폴더 | 내용 |
|------|------|
| `01_raw_sources/` | TinyFish가 수집한 원본 웹 내용 |
| `02_markdown/` | 정제된 Markdown 파일 |
| `03_knowledge_base/` | Claude Code 분석용 knowledge base |
| `04_qa_results/` | Claude Code 질문/답변 쌍 |
| `05_content_output/` | 최종 콘텐츠 (글, 세미나 자료, X(thread) 등) |
| `scripts/` | 자동화 스크립트 |
| `templates/` | 프롬프트/템플릿 |

## 도구 연결

| 단계 | 도구 | 용도 |
|------|------|------|
| 정보수집 | **TinyFish API** | 웹 자동调研 (크롤링) |
| 저장 | **로컬 파일** | Markdown 변환 후 저장 |
| 분석 | **Claude Code** | 수백 篇 문서 기반 질문/답변 |
| 임시저장 | **NotebookLM** (선택) | Gemini 기반 긴 문서 요약 |
| 최종创作 | **Claude Code / 수동** | 글, 세미나, thread |

## 사용 방법

### 1단계: TinyFish로 웹调研

```bash
cd scripts
python3 run_tinyfish_research.py \
  --topic "지방간 치료제 개발 동향 2025" \
  --output ../01_raw_sources/
```

### 2단계: Claude Code로 분석

```bash
# Claude Code에서 실행
claude mcp add --transport http tinyfish https://agent.tinyfish.ai/mcp

# Claude Code 프롬프트:
# "이 폴더의 모든 Markdown 파일을 읽고, 좋은 질문을 20개 생성해줘.
# 각 질문에 대한 답변을 文献 바탕으로 작성해줘."
```

### 3단계: 콘텐츠創作

```bash
# 스크립트로 콘텐츠 생성
python3 scripts/generate_content.py \
  --qa_results ../04_qa_results/ \
  --template templates/seminar.md \
  --output ../05_content_output/
```

## 파일 구조

```
ai-content-workflow/
├── 00_README.md              ← 이 파일
├── 01_raw_sources/           ← TinyFish 원본
├── 02_markdown/             ← 정제 Markdown
├── 03_knowledge_base/        ← 분석용
├── 04_qa_results/           ← Q&A 쌍
├── 05_content_output/       ← 최종 산출물
├── scripts/
│   ├── run_tinyfish_research.py
│   ├── convert_to_markdown.py
│   └── generate_content.py
└── templates/
    ├── seminar.md
    ├── blog_post.md
    └── thread.md
```

## 빠른 시작

```bash
# 1. TinyFish API 키 설정
export TINYFISH_API_KEY="sk-tinyfish-..."

# 2. 주제 설정
TOPIC="당뇨병 치료제 개발 동향 2025"

# 3. 자동 실행
cd scripts
python3 run_tinyfish_research.py --topic "$TOPIC" --search-engine duckduckgo
```

## 커스터마이징

- `scripts/run_tinyfish_research.py` — TinyFish 호출 로직
- `templates/` — 콘텐츠 템플릿 커스터마이징
- Claude Code skill로 NotebookLM 연동 가능
