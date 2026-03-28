#!/usr/bin/env python3
"""
ARP v4 — Complete Research Pipeline Orchestrator

Combines all modules:
- KG-CoT (Morrissette's Knowledge Graph)
- last30days (Social Intelligence)
- Gemini Embedding 2 (Multimodal)
- AI Scientist (Automated Paper Generation) + RunPod GPU
- System 2 Reasoning
- Drug Discovery

Usage:
    python3 run.py "SIRT3 mitophagy research"
    
With GPU:
    python3 run.py "AI Scientist experiment" --gpu
"""

import argparse
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from reasoning import ReasoningAgent, ChainOfVerification, ReasoningBenchmark
from gpu_runtime import RunPodGPU, AIScientistRunner, check_gpu_availability


def print_banner(text: str):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def run_reasoning_mode(topic: str):
    """Run System 2 reasoning on a topic."""
    print_banner(f"System 2 Reasoning: {topic}")
    
    agent = ReasoningAgent()
    result = agent.think(topic, verify_each=True)
    
    print(result)
    
    # Chain of Verification
    print_banner("Chain of Verification")
    cov = ChainOfVerification()
    results = cov.verify(result)
    
    print(f"Verified claims: {len(results['verified_claims'])}")
    print(f"Uncertainties: {len(results['uncertainties'])}")
    print(f"Contradictions: {len(results['contradictions'])}")
    
    return result


def run_gpu_check():
    """Check GPU availability."""
    print_banner("GPU Availability Check")
    
    gpus = check_gpu_availability()
    for gpu, info in gpus.items():
        status = "✅" if info["available"] else "❌"
        price = f"${info['price_per_hour']}/hr"
        print(f"  {status} {gpu}: {price}")


def run_ai_scientist(
    topic: str,
    api_key: str = None,
    gpu_type: str = "NVIDIA RTX 3090"
):
    """Run AI Scientist on RunPod GPU."""
    print_banner(f"AI Scientist: {topic}")
    
    print("⚠️  AI Scientist requires GPU and significant setup.")
    print("    This would:")
    print("    1. Start RunPod GPU container")
    print("    2. Clone AI Scientist repo")
    print("    3. Run experiments")
    print("    4. Generate papers")
    print()
    
    # Check if API key is configured
    if not api_key:
        import os
        api_key = os.environ.get("RUNPOD_API_KEY", "")
    
    if not api_key:
        print("❌ RUNPOD_API_KEY not set")
        print("   Get one at: https://runpod.io")
        print("   Then run: export RUNPOD_API_KEY=your_key")
        return
    
    print(f"✅ GPU: {gpu_type}")
    print("   Starting container...")
    
    # Initialize GPU
    gpu = RunPodGPU(api_key=api_key)
    
    try:
        # Start container
        instance = gpu.start(name=f"arp-v4-{topic[:20]}")
        
        # Setup AI Scientist
        ai_scientist = AIScientistRunner(gpu)
        ai_scientist.setup()
        
        # Run experiment
        print("\n🧪 Running AI Scientist experiment...")
        result = ai_scientist.run_experiment(
            experiment="nanoGPT_lite",
            model="gpt-4o-2024-05-13",
            num_ideas=2
        )
        
        print("\n📄 Results:")
        print(result["stdout"][-2000:] if result["stdout"] else "No output")
        
    finally:
        gpu.stop()


def main():
    parser = argparse.ArgumentParser(description="ARP v4 Complete Research Pipeline")
    parser.add_argument("topic", nargs="?", default="SIRT3 mitophagy research", help="Research topic")
    parser.add_argument("--mode", choices=["reason", "gpu", "full"], default="reason", help="Run mode")
    parser.add_argument("--gpu", action="store_true", help="Use GPU (requires RUNPOD_API_KEY)")
    parser.add_argument("--runpod-key", help="RunPod API key")
    
    args = parser.parse_args()
    
    print_banner(f"ARP v4 Research Pipeline")
    print(f"Topic: {args.topic}")
    print(f"Mode: {args.mode}")
    print(f"GPU: {'Yes' if args.gpu else 'No (CPU only)'}")
    
    if args.gpu:
        run_ai_scientist(args.topic, args.runpod_key)
    elif args.mode == "reason":
        run_reasoning_mode(args.topic)
    elif args.mode == "full":
        # Run reasoning first
        run_reasoning_mode(args.topic)
        # Then suggest GPU usage
        print_banner("GPU Recommendation")
        print("For full AI Scientist execution, run with --gpu flag:")
        print("  python3 run.py --gpu 'your topic'")
    else:
        print("Unknown mode")


if __name__ == "__main__":
    main()
