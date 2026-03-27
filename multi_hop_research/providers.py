"""
Z.AI + MiniMax Multi-Provider Analyzer
Brown Biotech — Research Pipeline

Supports:
- Z.AI (z-ai.com) — primary
- MiniMax — fallback/secondary

Usage:
    from providers import MultiProviderAnalyzer
    analyzer = MultiProviderAnalyzer()
    result = analyzer.analyze(query="NASH drugs", provider="zai")
"""

import os
import json
import time
from dataclasses import dataclass, field
from enum import Enum

# ─────────────────────────────────────────
# PROVIDER CONFIGS
# ─────────────────────────────────────────

class Provider(Enum):
    ZAI = "zai"
    MINIMAX = "minimax"
    OLLAMA = "ollama"  # local


@dataclass
class ProviderConfig:
    name: str
    base_url: str
    model: str
    api_key_env: str
    cost_per_1k: float
    speed: str
    accuracy: float  # relative to FP16
    context_window: int
    description: str


PROVIDERS = {
    Provider.ZAI: ProviderConfig(
        name="Z.AI",
        base_url="https://api.z-ai.com/v1",
        model="mixtral-8x22b",
        api_key_env="ZA_API_KEY",
        cost_per_1k=0.001,  # cheap
        speed="fast",
        accuracy=1.0,
        context_window=64000,
        description="빠르고 싸고 정확한 Reasoning 모델"
    ),
    Provider.MINIMAX: ProviderConfig(
        name="MiniMax",
        base_url="https://api.minimax.io/v1",
        model="MiniMax-M2.7",
        api_key_env="MINIMAX_API_KEY",
        cost_per_1k=0.01,
        speed="medium",
        accuracy=1.0,
        context_window=32000,
        description="우리的主力 모델"
    ),
}


def get_api_key(provider: Provider) -> str:
    """Get API key from environment"""
    env_var = PROVIDERS[provider].api_key_env
    key = os.environ.get(env_var, "")

    if not key:
        # Try ~/.env
        env_path = os.path.expanduser("~/.env")
        if os.path.exists(env_path):
            for line in open(env_path).read().split("\n"):
                if env_var.lower() in line.lower() and "key" in line.lower():
                    key = line.split("=", 1)[1].strip()
    if not key:
        # Try /Users/ocm/.env
        for path in ["/Users/ocm/.env", "/Users/ocm/.openclaw/workspace/.env"]:
            if os.path.exists(path):
                for line in open(path).read().split("\n"):
                    if env_var.lower() in line.lower():
                        key = line.split("=", 1)[1].strip()
                        break
    return key


# ─────────────────────────────────────────
# ANALYSIS REQUEST
# ─────────────────────────────────────────

@dataclass
class AnalysisRequest:
    query: str
    service: str = "drug_pipeline"
    provider: Provider = Provider.ZAI
    tier: str = "standard"  # fast | standard | deep
    focus_areas: list = field(default_factory=list)
    language: str = "ko"
    preview_first: bool = True

    def summary(self) -> str:
        pcfg = PROVIDERS[self.provider]
        return f"""
{'='*50}
📊 Analysis Request
{'='*50}
🤖 Provider: {pcfg.name} ({pcfg.description})
📝 Query: {self.query}
🎯 Service: {self.service}
⚡ Tier: {self.tier}
⏱️ Speed: {pcfg.speed} | 💰 ~${pcfg.cost_per_1k:.3f}/1K
🎚️ Accuracy: {pcfg.accuracy:.0%}
{'='*50}
"""


# ─────────────────────────────────────────
# MULTI-PROVIDER LLM CLIENT
# ─────────────────────────────────────────

class LLMClient:
    """Universal LLM client with provider fallback"""

    def __init__(self, primary: Provider = Provider.ZAI):
        self.primary = primary

    def chat(self, prompt: str,
             provider: Provider = None,
             model: str = None,
             max_tokens: int = 4096) -> str:
        """Send chat completion, try primary first, fallback to secondary"""
        provider = provider or self.primary

        # Try primary first
        for try_provider in [provider, Provider.MINIMAX]:
            cfg = PROVIDERS[try_provider]
            key = get_api_key(try_provider)
            if not key:
                continue

            try:
                return self._chat_with_provider(
                    cfg, key, prompt, model or cfg.model, max_tokens
                )
            except Exception as e:
                print(f"[{cfg.name}] Error: {e}, trying fallback...")
                continue

        return "[Error: All providers failed]"

    def _chat_with_provider(self, cfg: ProviderConfig, key: str,
                           prompt: str, model: str, max_tokens: int) -> str:
        import urllib.request

        messages = [
            {"role": "system", "content": "당신은 의약학/바이오 전문 분석가입니다. 간결하고 정확하게 답변하세요."},
            {"role": "user", "content": prompt}
        ]

        # Z.AI and MiniMax use OpenAI-compatible format
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.3,
        }

        url = f"{cfg.base_url}/chat/completions"

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode(),
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read())
            return result["choices"][0]["message"]["content"]


# ─────────────────────────────────────────
# ANALYSIS ENGINES
# ─────────────────────────────────────────

class ResearchAnalyzer:
    """Multi-provider research analyzer"""

    def __init__(self):
        self.llm = LLMClient()

    def analyze(self, request: AnalysisRequest) -> dict:
        """Run full analysis with selected provider"""
        pcfg = PROVIDERS[request.provider]

        print(f"\n{'='*50}")
        print(f"🤖 {pcfg.name} — {pcfg.description}")
        print(f"📝 {request.query[:50]}...")
        print(f"{'='*50}")

        # Build prompt
        service_prompts = {
            "drug_pipeline": (
                "의약품 파이프라인 분석 보고서를 작성하세요.\n"
                "구조: Executive Summary, 치료 영역, 파이프라인, 임상 데이터, 시장, 결론\n"
                "모든 사실에 출처를 표기하세요."
            ),
            "dd": (
                "기술 Due Diligence 보고서를 작성하세요.\n"
                "구조: Executive Summary, 지적재산권, 임상데이터, 규제, 투자 의견\n"
            ),
            "intel": "경쟁사 분석 SWOT 보고서를 작성하세요.",
            "market": "시장 조사 보고서를 작성하세요.",
            "paper": "의학 논문 리뷰를 작성하세요.",
        }

        prompt = service_prompts.get(request.service, service_prompts["drug_pipeline"])
        full_prompt = f"{prompt}\n\n주제: {request.query}"

        # Run
        start = time.time()
        report = self.llm.chat(full_prompt, provider=request.provider)
        latency = time.time() - start

        print(f"\n✅ 완료: {latency:.1f}s ({request.provider.value})")

        return {
            "report": report,
            "provider": request.provider.value,
            "latency_seconds": latency,
            "query": request.query,
            "service": request.service,
        }


# ─────────────────────────────────────────
# QUICK START
# ─────────────────────────────────────────

def analyze(query: str, service: str = "drug_pipeline",
           provider: str = "zai") -> dict:
    """
    One-liner analysis.

    Usage:
        result = analyze("NASH drugs 2025", provider="zai")
        print(result["report"])
    """
    analyzer = ResearchAnalyzer()
    req = AnalysisRequest(
        query=query,
        service=service,
        provider=Provider(provider)
    )
    print(req.summary())
    return analyzer.analyze(req)


# ─────────────────────────────────────────
# CLI
# ─────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Multi-Provider Research Analyzer")
    parser.add_argument("--query", "-q", required=True)
    parser.add_argument("--service", "-s",
                        choices=["pipeline", "dd", "intel", "market", "paper"],
                        default="pipeline")
    parser.add_argument("--provider", "-p",
                        choices=["zai", "minimax"],
                        default="zai")
    args = parser.parse_args()

    service_map = {
        "pipeline": "drug_pipeline", "dd": "dd",
        "intel": "intel", "market": "market", "paper": "paper"
    }

    result = analyze(
        query=args.query,
        service=service_map[args.service],
        provider=args.provider
    )

    print(f"\n{'='*50}")
    print("📄 REPORT")
    print(f"{'='*50}\n")
    print(result["report"])


if __name__ == "__main__":
    main()
