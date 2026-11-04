#!/usr/bin/env python3
"""
Focused platform-specific search rounds for bestiejob.

Runs N rounds per platform (ServiceNow, Salesforce, Other) using Exa + Parallel AI
(search), scores with Ollama (local, free), saves to inbox/.

Optimized: search and score are separated to avoid long timeouts.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))

from ai_scan_pipeline import (
    exa_search, parallel_ai_search, jina_search,
    normalize_job, score_jobs_with_ai, local_ollama_chat,
    TODAY,
)

INBOX_DIR = ROOT / "inbox"
SCAN_DIR = ROOT / "scan_results"
INBOX_DIR.mkdir(exist_ok=True)
SCAN_DIR.mkdir(exist_ok=True)

PLATFORM_TERMS = {
    "sn": [
        "ServiceNow developer", "ServiceNow administrator", "ServiceNow architect",
        "ServiceNow consultant", "ServiceNow CSA", "ServiceNow CAD",
        "ServiceNow ITSM", "ServiceNow ITAM", "ServiceNow CMDB",
    ],
    "sf": [
        "Salesforce developer", "Salesforce administrator", "Salesforce architect",
        "Salesforce consultant", "Salesforce Platform Developer I",
        "Salesforce JavaScript Developer I", "Salesforce CPQ",
    ],
    "other": [
        "IT service management job Toronto", "ITSM consultant Canada",
        "platform administrator job Canada", "IT operations manager Toronto",
        "business analyst ServiceNow Salesforce Canada", "CRM developer Canada",
        "cloud platform engineer Toronto", "IT service desk manager Canada",
    ],
}

GEO_MODIFIERS = [
    "Toronto GTA Ontario Canada",
    "Canada remote",
    "Mississauga Markham Brampton",
    "Ottawa Ontario",
    "Vancouver BC",
    "Calgary Alberta",
]


def build_queries(platform: str, round_num: int) -> list[tuple[str, str]]:
    terms = PLATFORM_TERMS[platform]
    geo = GEO_MODIFIERS[round_num % len(GEO_MODIFIERS)]
    queries = []
    for term in terms:
        queries.append((f"{term} {geo} job", f"{platform}_r{round_num}"))
    return queries


def search_only(platform: str, round_num: int, apis: list[str]) -> list[dict]:
    """Run search APIs only, return raw results deduped by URL."""
    queries = build_queries(platform, round_num)
    seen: dict[str, dict] = {}
    all_results: list[dict] = []

    for query, geo_label in queries:
        for api in apis:
            try:
                if api == "exa":
                    results = exa_search(query)
                elif api == "parallel":
                    results = parallel_ai_search(query)
                elif api == "jina":
                    results = jina_search(query)
                else:
                    results = []
                for r in results:
                    u = r.get("url", "")
                    if u and u not in seen:
                        seen[u] = r
                        all_results.append(r)
            except Exception as e:
                print(f"    [{api}] {query[:50]} -> error: {e}")
        time.sleep(0.4)

    return all_results


def normalize_and_score(results: list[dict]) -> list[dict]:
    """Normalize results and score with Ollama."""
    jobs = []
    for r in results:
        j = normalize_job(r, 0)
        if j:
            jobs.append(j)

    if not jobs:
        return []

    scored = score_jobs_with_ai(jobs, 0, voters=[
        ("ollama-qwen7b", local_ollama_chat, {"model": "qwen2.5:7b-instruct-q5_K_M"}),
    ])
    return scored


def save_round(platform: str, round_num: int, scored: list[dict], raw_count: int):
    good = [j for j in scored if j.get("ai_score", 0) >= 5]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    out = {
        "platform": platform,
        "round": round_num,
        "raw_results": raw_count,
        "normalized": len(scored),
        "scored_good": len(good),
        "generated_at": stamp,
        "jobs": good,
    }
    raw_file = SCAN_DIR / f"{TODAY}_{platform}_round{round_num}_{stamp}.json"
    raw_file.write_text(json.dumps(out, indent=1, ensure_ascii=False))

    inbox_file = INBOX_DIR / f"focused-{platform}-round{round_num}--{stamp}.md"
    lines = [
        "---",
        f"model: focused-platform-{platform}",
        f"scanned_at: {stamp}",
        f"task: {platform}-focused-search-round-{round_num}",
        "---",
        "",
        f"# {platform.upper()} Focused Search — Round {round_num}",
        "",
        f"Raw results: {raw_count} | Normalized: {len(scored)} | Score >= 5: {len(good)}",
        "",
        "| Posted | Role | Company | Location | Score | Source |",
        "|---|---|---|---|---|---|",
    ]
    for j in good:
        title = (j.get("title", "") or "").replace("|", "/")
        company = (j.get("company", "") or "").replace("|", "/")
        loc = (j.get("location", "") or "").replace("|", "/")
        score = j.get("ai_score", 0)
        src = j.get("source", "search")
        lines.append(f"| {j.get('postedDate','')[:10]} | [{title}]({j.get('url','')}) | {company} | {loc} | {score} | {src} |")
    inbox_file.write_text("\n".join(lines) + "\n")

    return len(good), inbox_file.name


def main() -> int:
    ap = argparse.ArgumentParser(description="Focused platform search rounds")
    ap.add_argument("--platform", choices=["sn", "sf", "other"])
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--rounds", type=int, default=12)
    ap.add_argument("--apis", nargs="+", default=["exa", "parallel"])
    args = ap.parse_args()

    platforms = ["sn", "sf", "other"] if args.all else [args.platform]
    if not platforms:
        ap.error("specify --platform or --all")

    total = len(platforms) * args.rounds
    print(f"=== Focused Platform Search: {total} rounds ===")
    print(f"Platforms: {', '.join(platforms)} | APIs: {args.apis} | Date: {TODAY}")

    grand_raw = 0
    grand_norm = 0
    grand_good = 0

    for platform in platforms:
        print(f"\n--- Platform: {platform.upper()} ---")
        for r in range(1, args.rounds + 1):
            print(f"  Round {r}/{args.rounds} ...", end=" ", flush=True)
            results = search_only(platform, r, args.apis)
            grand_raw += len(results)

            scored = normalize_and_score(results)
            grand_norm += len(scored)

            good_count, inbox_name = save_round(platform, r, scored, len(results))
            grand_good += good_count

            print(f"{len(results)} raw -> {len(scored)} norm -> {good_count} good ({inbox_name})")

    print(f"\n=== COMPLETE ===")
    print(f"Total rounds: {total}")
    print(f"Raw: {grand_raw} | Normalized: {grand_norm} | Score>=5: {grand_good}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
