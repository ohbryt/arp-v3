#!/usr/bin/env python3
"""
Demo: Multi-Hop Research System
Brown Biotech — Research Analysis Pipeline
"""

import os
import sys

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_hop_research import ResearchSystem


def get_api_keys():
    tf_key = os.environ.get("TINYFISH_API_KEY", "")
    mm_key = os.environ.get("MINIMAX_API_KEY", "")

    if not tf_key or not mm_key:
        env_path = os.path.expanduser("~/.env")
        if os.path.exists(env_path):
            for line in open(env_path).read().split("\n"):
                if "TINYFISH" in line:
                    tf_key = line.split("=", 1)[1].strip()
                if "MINIMAX" in line or ("API_KEY" in line and "OPENAI" not in line):
                    mm_key = line.split("=", 1)[1].strip()

    return tf_key, mm_key


def main():
    tf_key, mm_key = get_api_keys()

    if not tf_key:
        print("ERROR: TINYFISH_API_KEY not found")
        sys.exit(1)
    if not mm_key:
        print("ERROR: MINIMAX_API_KEY not found")
        sys.exit(1)

    print(f"API keys loaded: TF={tf_key[:15]}..., MM={mm_key[:15]}...")

    system = ResearchSystem(tinyfish_key=tf_key, mini_max_key=mm_key)

    print("\n=== DEMO: NASH Drug Pipeline Analysis ===")

    result = system.drug_pipeline(
        query="NASH NAFLD treatment drugs pipeline 2025 resmetirom",
        domains=["web", "patents", "news"],
        depth=3
    )

    print(f"\nLatency: {result.latency_seconds:.1f}s")
    print(f"Sources: {len(result.sources)}")
    print(f"\n--- REPORT PREVIEW (first 1500 chars) ---")
    print(result.report[:1500])
    print("...")
    print(f"\n=== DONE ({len(result.report)} chars) ===")


if __name__ == "__main__":
    main()
