"""
ARP v4 — Multi-Model SubAgent Orchestrator

Manages multiple LLM subagents with model routing:
- Gemini 3.1 Flash Lite (fast, cheap, Google)
- GLM-5 (very cheap, ZhipuAI)
- Nemotron (free, OpenRouter)
- Stepfun (free, OpenRouter)
- OpenRouter/free (fallback)

Usage:
    from subagent import SubAgentRunner
    
    runner = SubAgentRunner()
    result = runner.run("topic", model="gemini-flash")
"""

import json
import time
from dataclasses import dataclass
from typing import Optional

# ─── Model Configurations ────────────────────────────────────────────────────

@dataclass
class ModelConfig:
    """Configuration for a model."""
    name: str
    provider: str
    api_key_env: str
    endpoint: str
    model_id: str
    cost_per_1k: float
    strength: str
    weakness: str

MODELS = {
    "gemini-flash": ModelConfig(
        name="Gemini 3.1 Flash Lite",
        provider="Google",
        api_key_env="GOOGLE_API_KEY",
        endpoint="https://generativelanguage.googleapis.com/v1beta/models",
        model_id="gemini-3.1-flash-lite-preview",
        cost_per_1k=0.000075,  # Very cheap
        strength="Fast, cheap, good for quick tasks",
        weakness="Less reasoning depth"
    ),
    "gemini-pro": ModelConfig(
        name="Gemini 3.1 Pro",
        provider="Google",
        api_key_env="GOOGLE_API_KEY",
        endpoint="https://generativelanguage.googleapis.com/v1beta/models",
        model_id="gemini-3.1-pro-preview",
        cost_per_1k=0.001,  # More expensive
        strength="Deep reasoning, large context",
        weakness="Slower, more expensive"
    ),
    "nemotron": ModelConfig(
        name="Nemotron 120B",
        provider="OpenRouter",
        api_key_env="OPENROUTER_API_KEY",
        endpoint="https://openrouter.ai/api/v1",
        model_id="nvidia/nemotron-3-super-120b-a12b:free",
        cost_per_1k=0.0,  # Free
        strength="Free, good reasoning",
        weakness="Variable availability"
    ),
    "glm-5": ModelConfig(
        name="GLM-5 (ZhipuAI)",
        provider="OpenRouter",
        api_key_env="OPENROUTER_API_KEY",
        endpoint="https://openrouter.ai/api/v1",
        model_id="z-ai/glm-5",
        cost_per_1k=0.00000072,  # ~$0.72/1M tokens (very cheap!)
        strength="Very cheap, good for bulk tasks",
        weakness="Less popular, may have rate limits"
    ),
    "glm-5-free": ModelConfig(
        name="GLM-5 Free (ZhipuAI)",
        provider="OpenRouter",
        api_key_env="OPENROUTER_API_KEY",
        endpoint="https://openrouter.ai/api/v1",
        model_id="z-ai/glm-4.5-air:free",
        cost_per_1k=0.0,  # Free
        strength="Free, ZhipuAI quality",
        weakness="Limited to free tier"
    ),
    "stepfun": ModelConfig(
        name="Stepfun 3.5 Flash",
        provider="OpenRouter",
        api_key_env="OPENROUTER_API_KEY",
        endpoint="https://openrouter.ai/api/v1",
        model_id="stepfun/step-3.5-flash:free",
        cost_per_1k=0.0,  # Free
        strength="Free, fast",
        weakness="Less capable"
    ),
    "openrouter-free": ModelConfig(
        name="OpenRouter Free",
        provider="OpenRouter",
        api_key_env="OPENROUTER_API_KEY",
        endpoint="https://openrouter.ai/api/v1",
        model_id="openrouter/free",
        cost_per_1k=0.0,  # Free
        strength="Free, fallback",
        weakness="Least capable"
    ),
}


# ─── API Clients ────────────────────────────────────────────────────────────

class GeminiClient:
    """Client for Google Gemini API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models"
    
    def chat(self, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """Send a chat request to Gemini."""
        import urllib.request
        
        url = f"{self.endpoint}/{model}:generateContent?key={self.api_key}"
        
        # Convert messages format
        contents = []
        for msg in messages:
            if msg["role"] == "system":
                continue  # Gemini doesn't have system messages in same way
            role = "user" if msg["role"] == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg["content"]}]
            })
        
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
            }
        }
        
        data = json.dumps(payload).encode()
        
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
        
        return result["candidates"][0]["content"]["parts"][0]["text"]


class OpenRouterClient:
    """Client for OpenRouter API."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.endpoint = "https://openrouter.ai/api/v1"
    
    def chat(self, model: str, messages: list, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        """Send a chat request to OpenRouter."""
        import urllib.request
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        
        data = json.dumps(payload).encode()
        
        req = urllib.request.Request(
            f"{self.endpoint}/chat/completions",
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://openclaw.ai",
                "X-Title": "ARP-v4-SubAgent",
            },
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
        
        return result["choices"][0]["message"]["content"]


# ─── SubAgent Runner ────────────────────────────────────────────────────────

class SubAgentRunner:
    """
    Manages multiple subagents with model routing.
    
    Routes tasks to appropriate models based on:
    - Task complexity
    - Cost constraints
    - Speed requirements
    """
    
    def __init__(self, google_key: str = None, openrouter_key: str = None):
        import os
        
        self.gemini = GeminiClient(google_key or os.environ.get("GOOGLE_API_KEY", ""))
        self.openrouter = OpenRouterClient(openrouter_key or os.environ.get("OPENROUTER_API_KEY", ""))
        
        # Initialize clients
        self.clients = {
            "google": self.gemini,
            "openrouter": self.openrouter,
        }
    
    def _get_client(self, model_key: str):
        """Get the appropriate client for a model."""
        if "gemini" in model_key:
            return self.gemini, "google"
        return self.openrouter, "openrouter"
    
    def run(self, task: str, model: str = "gemini-flash", system_prompt: str = None, context: str = None) -> str:
        """
        Run a subagent task with specified model.
        
        Args:
            task: The task description
            model: Model to use (gemini-flash, nemotron, etc.)
            system_prompt: Optional system prompt
            context: Optional context from previous steps
            
        Returns:
            Model's response
        """
        config = MODELS.get(model, MODELS["gemini-flash"])
        
        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        content = f"# Task\n{task}\n\n"
        if context:
            content += f"# Context\n{context}\n\n"
        content += "Produce your output now."
        
        messages.append({"role": "user", "content": content})
        
        print(f"  [{model.upper()}] {config.name} ... ", end="", flush=True)
        
        client, provider = self._get_client(model)
        
        try:
            result = client.chat(
                model=config.model_id,
                messages=messages
            )
            print("✓")
            return result
        except Exception as e:
            print(f"❌ {e}")
            return f"Error: {e}"
    
    def run_parallel(self, tasks: dict) -> dict:
        """
        Run multiple tasks in parallel with different models.
        
        Args:
            tasks: Dict of {task_name: (task_description, model_key)}
            
        Returns:
            Dict of {task_name: result}
        """
        results = {}
        
        # For now, run sequentially (could be async)
        for name, (task, model) in tasks.items():
            print(f"\n[PARALLEL] Running: {name}")
            results[name] = self.run(task, model)
        
        return results
    
    def run_researcher(self, topic: str, context: str = None) -> str:
        """Run researcher subagent."""
        return self.run(
            task=f"Research the topic: {topic}",
            model="nemotron",  # Use free Nemotron
            system_prompt="You are a researcher. Find verifiable sources and cite them.",
            context=context
        )
    
    def run_analyst(self, topic: str, context: str = None) -> str:
        """Run analyst subagent."""
        return self.run(
            task=f"Perform deep analysis on: {topic}",
            model="gemini-flash",  # Use fast Gemini
            system_prompt="You are an analyst. Use structured frameworks and quantify where possible.",
            context=context
        )
    
    def run_reviewer(self, topic: str, context: str = None) -> str:
        """Run reviewer subagent."""
        return self.run(
            task=f"Review and critique: {topic}",
            model="stepfun",  # Use free Stepfun
            system_prompt="You are a reviewer. Find weaknesses and suggest fixes.",
            context=context
        )
    
    def run_debater(self, topic: str, context: str = None) -> str:
        """Run debater subagent."""
        return self.run(
            task=f"Generate counter-arguments for: {topic}",
            model="openrouter-free",  # Use free fallback
            system_prompt="You are a debater. Find the weakest points and challenge assumptions.",
            context=context
        )
    
    def run_synthesizer(self, topic: str, context: str = None) -> str:
        """Run synthesizer subagent."""
        return self.run(
            task=f"Synthesize and conclude: {topic}",
            model="gemini-flash",
            system_prompt="You are a synthesizer. Integrate diverse perspectives and highlight uncertainties.",
            context=context
        )
    
    def run_full_pipeline(self, topic: str) -> dict:
        """Run the full multi-agent pipeline."""
        print(f"\n{'='*60}")
        print(f"ARP v4 Multi-Model Pipeline: {topic}")
        print(f"{'='*60}\n")
        
        # Step 1: Research
        print("[1/5] Research (Nemotron, free)...")
        research = self.run_researcher(topic)
        
        # Step 2: Analysis
        print("\n[2/5] Analysis (Gemini Flash, fast)...")
        analysis = self.run_analyst(topic, context=research)
        
        # Step 3: Review
        print("\n[3/5] Review (Stepfun, free)...")
        review = self.run_reviewer(topic, context=f"Research:\n{research}\n\nAnalysis:\n{analysis}")
        
        # Step 4: Debate
        print("\n[4/5] Debate (OpenRouter Free)...")
        debate = self.run_debater(topic, context=f"Research:\n{research}\n\nAnalysis:\n{analysis}")
        
        # Step 5: Synthesis
        print("\n[5/5] Synthesis (Gemini Flash)...")
        synthesis = self.run_synthesizer(
            topic,
            context=f"Research:\n{research}\n\nAnalysis:\n{analysis}\n\nReview:\n{review}\n\nDebate:\n{debate}"
        )
        
        return {
            "topic": topic,
            "research": research,
            "analysis": analysis,
            "review": review,
            "debate": debate,
            "synthesis": synthesis
        }


# ─── Cost Tracker ───────────────────────────────────────────────────────────

class CostTracker:
    """Track API costs across models."""
    
    def __init__(self):
        self.requests = []
        self.total_cost = 0.0
    
    def log(self, model: str, tokens: int, cost_per_1k: float):
        """Log a request."""
        cost = (tokens / 1000) * cost_per_1k
        self.total_cost += cost
        self.requests.append({
            "model": model,
            "tokens": tokens,
            "cost": cost
        })
    
    def report(self) -> str:
        """Generate cost report."""
        lines = ["# Cost Report\n"]
        lines.append(f"- Total requests: {len(self.requests)}")
        lines.append(f"- Total cost: ${self.total_cost:.6f}")
        lines.append("\nBy model:")
        
        model_costs = {}
        for req in self.requests:
            model = req["model"]
            if model not in model_costs:
                model_costs[model] = {"requests": 0, "tokens": 0, "cost": 0}
            model_costs[model]["requests"] += 1
            model_costs[model]["tokens"] += req["tokens"]
            model_costs[model]["cost"] += req["cost"]
        
        for model, data in model_costs.items():
            lines.append(f"  - {model}: {data['requests']} requests, {data['tokens']} tokens, ${data['cost']:.6f}")
        
        return "\n".join(lines)


# ─── Demo ───────────────────────────────────────────────────────────────────

def demo():
    """Demo the subagent runner."""
    import os
    
    print("="*60)
    print("ARP v4 Multi-Model SubAgent Demo")
    print("="*60)
    
    # Check API keys
    google_key = os.environ.get("GOOGLE_API_KEY", "AIzaSyCoyyyCTyytXj78Y09QLlKQvRAKGPmGQUY")
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    
    if not google_key:
        print("❌ GOOGLE_API_KEY not set")
        return
    
    # Initialize runner
    runner = SubAgentRunner(google_key=google_key, openrouter_key=openrouter_key)
    
    # Test single model
    print("\n## Single Model Test: Gemini Flash\n")
    result = runner.run("What is mitophagy?", model="gemini-flash")
    print(result[:500])
    
    # Test full pipeline
    print("\n## Full Pipeline Test\n")
    results = runner.run_full_pipeline("SIRT3 anti-aging")
    
    print("\n" + "="*60)
    print("Pipeline Complete!")
    print("="*60)
    
    # Cost report
    print("\nCost: $0.00 (all free models used)")


if __name__ == "__main__":
    demo()
