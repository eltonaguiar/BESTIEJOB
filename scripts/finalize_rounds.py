#!/usr/bin/env python3
"""
Convert raw search results from 36 focused rounds to inbox markdown.
Uses keyword-based relevance scoring (fast) instead of per-job AI scoring.
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from ai_scan_pipeline import normalize_job, TODAY

SCAN_DIR = ROOT / "scan_results"
INBOX_DIR = ROOT / "inbox"
INBOX_DIR.mkdir(exist_ok=True)

# Keywords that boost relevance for Elton's profile
HIGH_KEYWORDS = [
    "servicenow", "salesforce", "csa", "cad", "platform developer",
    "platform admin", "itsm", "itam", "cmdb", "csdm", "javascript developer",
]
MED_KEYWORDS = [
    "developer", "administrator", "architect", "consultant", "specialist",
    "toronto", "canada", "remote", "ontario", "mississauga", "markham",
    "ottawa", "vancouver", "calgary",
]
LOW_KEYWORDS = [
    "sales", "retail", "warehouse", "driver", "nurse", "teacher",
    "cashier", "barista", "representative",
]


def keyword_score(title: str, company: str, location: str, excerpt: str) -> int:
    """Fast keyword-based relevance score 0-10."""
    text = f"{title} {company} {location} {excerpt}".lower()
    score = 3  # base score for being a job posting

    # Platform match
    if any(k in text for k in ["servicenow", "salesforce"]):
        score += 2
    # Cert keywords
    if any(k in text for k in ["csa", "cad", "platform developer i", "platform admin i", "javascript developer i"]):
        score += 2
    # Location
    if any(k in text for k in ["toronto", "canada", "ontario", "remote"]):
        score += 1
    # Seniority
    if any(k in text for k in ["developer", "administrator", "architect", "consultant", "senior", "lead"]):
        score += 1
    # Penalty for low-relevance
    if any(k in text for k in LOW_KEYWORDS):
        score -= 2

    return min(max(score, 0), 10)


def main() -> int:
    raw_files = sorted(SCAN_DIR.glob(f"{TODAY}_*_round*_raw_*.json"))
    if not raw_files:
        print(f"No raw files found for {TODAY}")
        return 1

    print(f"Found {len(raw_files)} raw result files")

    # Collect all jobs
    all_jobs = []
    for f in raw_files:
        data = json.loads(f.read_text(encoding="utf-8"))
        platform = data.get("platform", "?")
        round_num = data.get("round", 0)
        for res in data.get("results", []):
            j = normalize_job(res, 0)
            if j:
                j["platform"] = platform
                j["round"] = round_num
                j["source_file"] = f.name
                # Keyword-based relevance score
                j["ai_score"] = keyword_score(
                    j.get("title", ""), j.get("company", ""),
                    j.get("location", ""), j.get("excerpt", "")
                )
                j["ai_reason"] = "keyword relevance"
                all_jobs.append(j)

    print(f"Normalized: {len(all_jobs)}")

    # Dedupe by URL
    seen_urls: set[str] = set()
    unique_jobs = []
    for j in all_jobs:
        u = j.get("url", "")
        if u and u not in seen_urls:
            seen_urls.add(u)
            unique_jobs.append(j)
    print(f"Unique after URL dedupe: {len(unique_jobs)}")

    # Split: today's jobs vs older
    today_jobs = [j for j in unique_jobs if j.get("postedDate", "").startswith("2026-11-04")]
    older_jobs = [j for j in unique_jobs if not j.get("postedDate", "").startswith("2026-11-04")]
    print(f"Posted today: {len(today_jobs)} | Older: {len(older_jobs)}")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # Save combined scored results
    scored_file = SCAN_DIR / f"{TODAY}_all_scored_{stamp}.json"
    out = {
        "generated_at": stamp,
        "total_jobs": len(unique_jobs),
        "today_jobs": len(today_jobs),
        "jobs": unique_jobs,
    }
    scored_file.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"Saved: {scored_file.name}")

    # Save to inbox markdown per platform (today's jobs, score >= 5)
    for platform in ["sn", "sf", "other"]:
        pjobs = [j for j in today_jobs if j.get("platform") == platform and j.get("ai_score", 0) >= 5]
        if not pjobs:
            print(f"  {platform.upper()}: 0 jobs score>=5 today, skipping inbox")
            continue
        inbox_file = INBOX_DIR / f"focused-{platform}-all--{stamp}.md"
        lines = [
            "---",
            f"model: focused-platform-{platform}",
            f"scanned_at: {stamp}",
            f"task: {platform}-36-focused-rounds",
            "---",
            "",
            f"# {platform.upper()} Focused Search — 36 Rounds (12 per platform)",
            "",
            f"Date: {TODAY} | Score >= 5: {len(pjobs)} jobs",
            "",
            "| Score | Round | Role | Company | Location | Source |",
            "|---|---|---|---|---|---|",
        ]
        for j in sorted(pjobs, key=lambda x: x.get("ai_score", 0), reverse=True):
            title = (j.get("title", "") or "").replace("|", "/")
            company = (j.get("company", "") or "").replace("|", "/")
            loc = (j.get("location", "") or "").replace("|", "/")
            score = j.get("ai_score", 0)
            rnd = j.get("round", 0)
            src = j.get("source_file", "search")
            lines.append(f"| {score} | R{rnd} | [{title}]({j.get('url','')}) | {company} | {loc} | {src} |")
        inbox_file.write_text("\n".join(lines) + "\n")
        print(f"Inbox: {inbox_file.name} ({len(pjobs)} jobs)")

    # Also save older jobs for reference
    older_good = [j for j in older_jobs if j.get("ai_score", 0) >= 6]
    if older_good:
        inbox_file = INBOX_DIR / f"focused-older-good--{stamp}.md"
        lines = [
            "---",
            "model: focused-older-jobs",
            f"scanned_at: {stamp}",
            "task: older-jobs-reference",
            "---",
            "",
            "# Older Jobs (Score >= 6)",
            "",
            f"Count: {len(older_good)}",
            "",
            "| Score | Platform | Role | Company | Location |",
            "|---|---|---|---|---|---|",
        ]
        for j in sorted(older_good, key=lambda x: x.get("ai_score", 0), reverse=True)[:100]:
            title = (j.get("title", "") or "").replace("|", "/")
            company = (j.get("company", "") or "").replace("|", "/")
            loc = (j.get("location", "") or "").replace("|", "/")
            score = j.get("ai_score", 0)
            plat = j.get("platform", "?")
            lines.append(f"| {score} | {plat.upper()} | [{title}]({j.get('url','')}) | {company} | {loc} |")
        inbox_file.write_text("\n".join(lines) + "\n")
        print(f"Inbox: {inbox_file.name} ({len(older_good)} older jobs)")

    # Summary
    good_today = [j for j in today_jobs if j.get("ai_score", 0) >= 5]
    print(f"\n=== SUMMARY ===")
    print(f"36 rounds complete: {len(raw_files)} files")
    print(f"Total unique jobs: {len(unique_jobs)}")
    print(f"Today's jobs: {len(today_jobs)}")
    print(f"Today score>=5: {len(good_today)}")
    by_platform = {}
    for j in good_today:
        p = j.get("platform", "?")
        by_platform[p] = by_platform.get(p, 0) + 1
    for p in ["sn", "sf", "other"]:
        print(f"  {p.upper()}: {by_platform.get(p, 0)} jobs")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
