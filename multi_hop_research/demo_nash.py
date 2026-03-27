#!/usr/bin/env python3
"""Demo: Multi-Hop Research System v2 — DuckDuckGo + MiniMax"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_hop_research import ResearchSystem

# API Key (tilde expansion broken — use absolute path)
env_path = "/Users/ocm/.env"
mm_key = None
if os.path.exists(env_path):
    for line in open(env_path).read().split("\n"):
        if "minimax" in line.lower() and "api" in line.lower():
            mm_key = line.split("=", 1)[1].strip()

if not mm_key:
    print("ERROR: MINIMAX_API_KEY not found")
    sys.exit(1)

print(f"Key: {mm_key[:20]}...")
system = ResearchSystem(mm_key)

print("\n=== NASH Drug Pipeline Analysis ===")
result = system.drug_pipeline(
    query="NASH NAFLD treatment drugs resmetirom FDA approved 2025",
    depth=3
)

print(f"\nSources: {len(result.sources)}")
print(f"Latency: {result.latency_seconds:.1f}s")
print(f"\n--- REPORT ---")
print(result.report[:3000])
print("...")
print(f"\nTotal: {len(result.report)} chars")
