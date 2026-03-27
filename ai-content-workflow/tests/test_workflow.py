#!/usr/bin/env python3
"""
pytest tests for AI Content Pipeline evals
Run with: pytest tests/ -v

Based on Deep Agents' eval framework principles:
- Targeted evals that measure real production behaviors
- Trace every run to shared LangSmith-like history
- Dogfood: every failure → new eval
"""

import pytest
import json
from pathlib import Path

# Add parent to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from run_workflow import (
    EvalResult, run_evals, EVALS,
    load_previous_evals, WorkflowRun
)

# ─────────────────────────────────────────
# UNIT TESTS
# ─────────────────────────────────────────

class TestTinyFishEvals:
    """TinyFish stage evals"""
    
    def test_web_page_loaded(self):
        """웹페이지 로드 성공했는지"""
        result = {"status": "ok", "results": []}
        evals = run_evals("tinyfish", result)
        names = [e.name for e in evals]
        assert "web_page_loaded" in names
        passed = next(e for e in evals if e.name == "web_page_loaded")
        assert passed.passed
    
    def test_content_extracted(self):
        """최소 5개 결과 추출"""
        result = {
            "status": "ok",
            "results": [{"title": f"Item {i}"} for i in range(7)]
        }
        evals = run_evals("tinyfish", result)
        content_eval = next(e for e in evals if e.name == "content_extracted")
        assert content_eval.passed
    
    def test_valid_sources(self):
        """모든 결과에 출처 명시"""
        result = {
            "status": "ok",
            "results": [
                {"title": "A", "source": "PubMed", "url": "https://..."},
                {"title": "B", "source": "Nature", "url": "https://..."},
            ]
        }
        evals = run_evals("tinyfish", result)
        source_eval = next(e for e in evals if e.name == "valid_sources")
        assert source_eval.passed
    
    def test_fail_on_no_results(self):
        """결과 없으면 실패"""
        result = {"status": "ok", "results": []}
        evals = run_evals("tinyfish", result)
        content_eval = next(e for e in evals if e.name == "content_extracted")
        assert not content_eval.passed


class TestClaudeCodeEvals:
    """Claude Code analysis stage evals"""
    
    def test_questions_generated(self):
        """최소 10개 질문 생성"""
        result = {"questions": [f"Q{i}" for i in range(15)]}
        evals = run_evals("claude_code", result)
        q_eval = next(e for e in evals if e.name == "questions_generated")
        assert q_eval.passed
    
    def test_answers_have_sources(self):
        """모든 답변에 출처 표기"""
        result = {
            "questions": ["Q1", "Q2"],
            "answers": [
                {"answer": "A1", "source": "PubMed"},
                {"answer": "A2", "source": ""},
            ]
        }
        evals = run_evals("claude_code", result)
        source_eval = next(e for e in evals if e.name == "answers_based_on_sources")
        assert not source_eval.passed  # One answer has no source


class TestContentEvals:
    """Content generation stage evals"""
    
    def test_format_correct(self):
        """콘텐츠 생성됨"""
        result = {"content": "# Title\n\nContent here"}
        evals = run_evals("content", result)
        format_eval = next(e for e in evals if e.name == "format_correct")
        assert format_eval.passed
    
    def test_min_length(self):
        """최소 500자"""
        result = {"content": "A" * 600}
        evals = run_evals("content", result)
        len_eval = next(e for e in evals if e.name == "min_length")
        assert len_eval.passed
    
    def test_no_hallucination(self):
        """출처 표기로 hallucination 방지"""
        result = {"content": "Some claim [출처: Nature](https://...)"}
        evals = run_evals("content", result)
        halluc_eval = next(e for e in evals if e.name == "no_hallucination")
        assert halluc_eval.passed


# ─────────────────────────────────────────
# INTEGRATION TESTS
# ─────────────────────────────────────────

class TestWorkflowRun:
    """Workflow run tracking"""
    
    def test_workflow_run_solve_rate(self):
        """Workflow 전체 solve rate 계산"""
        evals = [
            EvalResult(name="test1", passed=True, solve_rate=1.0),
            EvalResult(name="test2", passed=True, solve_rate=0.8),
            EvalResult(name="test3", passed=False, solve_rate=0.0),
        ]
        wr = WorkflowRun(
            run_id="test123",
            timestamp="2026-03-27",
            topic="test",
            format="blog",
            evals=evals
        )
        assert wr.solve_rate == pytest.approx((1.0 + 0.8 + 0.0) / 3)
        assert not wr.passed  # test3 failed
    
    def test_workflow_run_to_dict(self):
        """JSON serialize"""
        wr = WorkflowRun(
            run_id="test456",
            timestamp="2026-03-27",
            topic="NASH drugs",
            format="seminar"
        )
        d = wr.to_dict()
        assert d["run_id"] == "test456"
        assert d["topic"] == "NASH drugs"
        assert "evals" in d


# ─────────────────────────────────────────
# CI RUN COMMAND
# ─────────────────────────────────────────

def test_ci_command():
    """CI에서 eval 실행하는 방법 안내"""
    print("""
    
    # Run all evals in CI:
    cd ai-content-workflow
    pytest tests/ -v --tb=short
    
    # Run specific category:
    pytest tests/ -v -k "tinyfish"
    pytest tests/ -v -k "claude_code"
    pytest tests/ -v -k "content"
    
    # With coverage:
    pytest tests/ --cov=scripts --cov-report=html
    
    # GitHub Actions example:
    # See: .github/workflows/evals.yml
    """)

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
