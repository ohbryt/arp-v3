#!/usr/bin/env python3
"""
TinyFish Web Agent로 웹调研 자동화 스크립트

Usage:
  python3 run_tinyfish_research.py --topic "지방간 치료제 개발 동향 2025"

Environment:
  export TINYFISH_API_KEY="sk-tinyfish-..."
"""

import os
import sys
import json
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# TinyFish API endpoint
TINYFISH_API = "https://agent.tinyfish.ai/v1/automation/run-sse"

def get_api_key():
    key = os.environ.get("TINYFISH_API_KEY", "")
    if not key:
        # Try .env file
        env_path = Path.home() / ".openclaw" / "workspace" / ".env"
        if env_path.exists():
            for line in env_path.read_text().split("\n"):
                if line.startswith("TINYFISH_API_KEY="):
                    key = line.split("=", 1)[1].strip()
    return key

def run_tinyfish_research(topic: str, search_engine: str = "duckduckgo", 
                          output_dir: str = "01_raw_sources") -> dict:
    """TinyFish API로 웹调研 실행"""
    
    api_key = get_api_key()
    if not api_key:
        print("❌ TINYFISH_API_KEY not found!")
        print("   Set it with: export TINYFISH_API_KEY='sk-tinyfish-...'")
        return {"status": "error", "error": "No API key"}
    
    print(f"🔍 Topic: {topic}")
    print(f"🔍 Search engine: {search_engine}")
    
    # Build search queries
    queries = [
        f"{topic} -latest research and clinical trials",
        f"{topic} drug pipeline and mechanism of action",
        f"{topic} companies and market analysis",
    ]
    
    results = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    for i, query in enumerate(queries):
        print(f"\n[{i+1}/{len(queries)}] Searching: {query}")
        
        # Prepare SSE request
        import urllib.request
        import urllib.parse
        
        data = {
            "url": f"https://{search_engine}.com",
            "goal": f"Search for: {query}. Extract the titles, sources, and brief summaries of the top 10 results. Include URLs.",
            "browser_profile": "lite"
        }
        
        req = urllib.request.Request(
            f"{TINYFISH_API}",
            data=json.dumps(data).encode(),
            headers={
                "Authorization": f"Bearer {api_key}",
                "X-API-Key": api_key,
                "Content-Type": "application/json"
            },
            method="POST"
        )
        
        try:
            # Execute request and stream response
            process = subprocess.Popen(
                ["curl", "-s", "-N", "-X", "POST", f"{TINYFISH_API}",
                "-H", f"X-API-Key: {api_key}",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(data)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            full_response = ""
            for line in process.stdout:
                if line.startswith("data: "):
                    line = line[6:].strip()
                    if line.startswith("{") and line.endswith("}"):
                        try:
                            event = json.loads(line)
                            etype = event.get("type", "")
                            
                            if etype == "STARTED":
                                run_id = event.get("run_id", "")
                                print(f"   Started: {run_id}")
                            elif etype == "PROGRESS":
                                purpose = event.get("purpose", "")
                                print(f"   Progress: {purpose[:60]}...")
                            elif etype == "COMPLETED":
                                result = event.get("result", {})
                                print(f"   ✅ Completed!")
                                results.append({
                                    "query": query,
                                    "run_id": event.get("run_id", ""),
                                    "result": result
                                })
                                
                                # Save to file
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = output_path / f"research_{i+1}_{timestamp}.md"
                                
                                with open(filename, "w") as f:
                                    f.write(f"# Research: {query}\n\n")
                                    f.write(f"**Timestamp:** {datetime.now().isoformat()}\n")
                                    f.write(f"**Topic:** {topic}\n\n")
                                    f.write("---\n\n")
                                    
                                    # Extract results
                                    for key, value in result.items():
                                        f.write(f"## {key.replace('_', ' ').title()}\n\n")
                                        if isinstance(value, list):
                                            for item in value[:10]:
                                                if isinstance(item, dict):
                                                    f.write(f"### {item.get('title', 'N/A')}\n")
                                                    f.write(f"- Source: {item.get('source', 'N/A')}\n")
                                                    if 'url' in item:
                                                        f.write(f"- URL: {item.get('url', 'N/A')}\n")
                                                    if 'snippet' in item:
                                                        f.write(f"- {item.get('snippet', 'N/A')}\n")
                                                    f.write("\n")
                                        else:
                                            f.write(f"{value}\n\n")
                                
                                print(f"   Saved: {filename}")
                                
                            elif etype == "FAILED":
                                print(f"   ❌ Failed: {event.get('error', 'Unknown')}")
                                
                        except json.JSONDecodeError:
                            pass
            
            process.wait()
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue
    
    # Summary
    print(f"\n{'='*60}")
    print(f"✅ Research Complete!")
    print(f"   Queries processed: {len(results)}")
    print(f"   Output: {output_path.absolute()}")
    
    return {"status": "ok", "results": results, "output_dir": str(output_path)}


def main():
    parser = argparse.ArgumentParser(description="TinyFish-powered web research")
    parser.add_argument("--topic", "-t", required=True, help="Research topic")
    parser.add_argument("--search-engine", "-s", default="duckduckgo", 
                       choices=["duckduckgo", "google", "bing"],
                       help="Search engine to use")
    parser.add_argument("--output", "-o", default="01_raw_sources",
                       help="Output directory")
    
    args = parser.parse_args()
    
    # Set API key from env
    if not os.environ.get("TINYFISH_API_KEY"):
        # Try to find it
        print("⚠️  TINYFISH_API_KEY not set in environment")
        print("   Will use .env file if available")
    
    result = run_tinyfish_research(args.topic, args.search_engine, args.output)
    
    if result.get("status") == "ok":
        print(f"\n📁 Results saved to: {result['output_dir']}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
