# AI 内容变现工作流 (AI Content-to-Cash Workflow) v2

## 핵심 원리 (Deep Agents' Eval Framework 적용)

```
More evals ≠ better agents
→ Targeted evals that measure production behaviors
→ Dogfood: every failure → new eval
```

## 구조

```
TinyFish调研
    ↓
Eval 체크 (자동)
    ↓
Claude Code 분석
    ↓
Eval 체크 (자동)
    ↓
콘텐츠 生成
    ↓
.eval_history.json (모든 실행 추적)
```

## Eval 기준

| Stage | Eval | 기준 |
|-------|------|------|
| TinyFish | web_page_loaded | 웹 로드 성공 |
| | content_extracted | ≥5개 결과 |
| | valid_sources | 모든 결과에 출처 |
| Claude Code | questions_generated | ≥10개 질문 |
| | answers_based_on_sources | 모든 답변에 출처 |
| Content | format_correct | 생성됨 |
| | min_length | ≥500자 |
| | no_hallucination | 출처 표기 있음 |

## 사용법

```bash
# 1. workflow 실행 (TinyFish → prompt 생성)
python3 scripts/run_workflow.py --topic "당뇨병 치료제"

# 2. Claude Code에서 분석 프롬프트 읽고 답변 작성
#    → 04_qa_results/에 저장

# 3. 콘텐츠 생성
python3 scripts/generate_content.py --topic "당뇨병 치료제" --format seminar

# 4. eval dashboard 확인
python3 scripts/run_workflow.py --dashboard

# 5. pytest로 모든 eval 테스트
pytest tests/ -v
```

## 파일 구조

```
ai-content-workflow/
├── 00_README.md              ← 이 파일
├── .eval_history.json         ← 실행 추적 (자동 생성)
├── scripts/
│   ├── run_workflow.py       ← v2: eval 포함 workflow
│   ├── run_tinyfish_research.py
│   └── generate_content.py
├── tests/
│   └── test_workflow.py      ← 12개 unit tests (all passing)
├── .github/workflows/
│   └── evals.yml             ← GitHub Actions CI
├── templates/
└── 01~05_folders/           ← 데이터 폴더
```

## 빠른 시작

```bash
cd ~/openclaw/workspace/ai-content-workflow
python3 scripts/run_workflow.py --topic "지방간 치료제" --format seminar
```
