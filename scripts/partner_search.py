#!/usr/bin/env python3
"""
Partner-focused ServiceNow job search.
Searches each ServiceNow partner company for ServiceNow job postings
using Parallel AI and Jina search APIs, scores with Ollama, and merges into the pipeline.
"""
import sys
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))

from ai_scan_pipeline import (
    parallel_ai_search, jina_search, exa_search,
    score_jobs_with_ai, normalize_job, local_ollama_chat,
    KEYS, TODAY, STAMP
)

# ServiceNow partner companies from the sponsor list
PARTNERS = [
    # Diamond - top tier partners
    "Ateko", "Deloitte Canada", "Ernst & Young", "KPMG",
    # Platinum
    "Cognizant", "Fujitsu", "IBM", "Tanium",
    # Gold - major Canadian partners
    "BDO Canada", "CDW", "Compugen", "NewRocket", "RapDev",
    "TELUS Business", "Tech Mahindra",
]

# Job terms to combine with each partner
TERMS = ["ServiceNow developer", "ServiceNow administrator", "ServiceNow consultant"]

def run_partner_searches():
    all_results = []
    seen = set()
    
    for partner in PARTNERS:
        for term in TERMS[:3]:  # Limit to 3 terms per partner to manage API calls
            query = f"{term} {partner} Canada job"
            
            # Try Parallel AI first (works well)
            for r in parallel_ai_search(query, num_results=5):
                u = r.get("url", "")
                if u and u not in seen:
                    seen.add(u)
                    all_results.append(r)
            
            time.sleep(0.3)  # rate limiting
    
    print(f"Total unique results from partner searches: {len(all_results)}")
    return all_results

def main():
    results = run_partner_searches()
    
    # Normalize to job format
    jobs = []
    for r in results:
        j = normalize_job(r, tier=4)  # tier 4 = partner/agency
        if j:
            jobs.append(j)
    
    print(f"Normalized jobs: {len(jobs)}")
    
    if not jobs:
        print("No jobs found.")
        return
    
    # Score with Ollama
    voters = [("ollama-qwen7b", local_ollama_chat, {"model": "qwen2.5:7b-instruct-q5_K_M"})]
    scored = score_jobs_with_ai(jobs, 4, voters=voters)
    scored.sort(key=lambda j: j.get("ai_score", 0), reverse=True)
    
    # Print top results
    print(f"\n=== TOP PARTNER JOBS (scored 7+/10) ===")
    high = [j for j in scored if j.get("ai_score", 0) >= 7]
    print(f"High-scoring: {len(high)} / {len(scored)}")
    for j in scored[:20]:
        print(f"  {j.get('ai_score', 0)}/10 | {j.get('title','')[:60]} | {j.get('company','')} | {j.get('location','')} | {j.get('url','')[:80]}")
    
    # Save results
    out_dir = ROOT / "scan_results"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"{TODAY}_partner_jobs.json"
    out_file.write_text(json.dumps(scored, indent=2), encoding="utf-8")
    print(f"\nSaved to {out_file}")
    
    # Also write inbox markdown
    inbox_dir = ROOT / "inbox"
    inbox_dir.mkdir(exist_ok=True)
    existing = list(inbox_dir.glob(f"ai-scan--{TODAY}--v*.md"))
    v = len(existing) + 1
    inbox_file = inbox_dir / f"ai-scan--{TODAY}--v{v}.md"
    
    lines = [f"# AI Scan — {TODAY} (Partner Search v{v})", ""]
    lines.append("| Posted | Role | Company | Location | Score | AI Reason | URL |")
    lines.append("|---|---|---|---|---|---|---|")
    for j in scored:
        posted = j.get("postedDate", TODAY)[:10]
        score = j.get("ai_score", 0)
        reason = j.get("ai_reason", "")[:80].replace("|", "\\|")
        lines.append(f"| {posted} | [{j['title']}]({j['url']}) | {j['company']} | {j['location']} | {score}/10 | {reason} | {j['url']} |")
    lines.append("")
    lines.append(f"_Partner search · {len(scored)} jobs · Generated {STAMP}_")
    inbox_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Inbox written to {inbox_file}")

if __name__ == "__main__":
    main()
