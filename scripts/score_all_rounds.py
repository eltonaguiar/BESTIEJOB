#!/usr/bin/env python3
"""
Score phase: normalize all raw search results, score with Ollama,
save to inbox/ markdown for the merger.
Limited to jobs posted today (2026-11-04) for speed.
"""
from __future__ import annotations

import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))

from ai_scan_pipeline import normalize_job, local_ollama_chat, TODAY

SCAN_DIR = ROOT / "scan_results"
INBOX_DIR = ROOT / "inbox"
INBOX_DIR.mkdir(exist_ok=True)

SCORING_PROMPT = """Rate this job 0-10 for fit against Elton Aguiar's profile (ServiceNow Developer, Toronto, CSA/CAD certified). Consider ServiceNow/Salesforce match, Toronto/Canada location, certification relevance, seniority.

Job: {title} at {company}
Location: {location}
Excerpt: {excerpt}

Respond with ONLY: SCORE: <0-10> | REASON: <one sentence>"""


def extract_score(response: str) -> tuple[int, str]:
    m = re.search(r"SCORE:\s*(\d+)", response)
    r = re.search(r"REASON:\s*(.+)", response)
    if m:
        score = int(m.group(1))
        reason = r.group(1).strip() if r else response[:100]
        return min(max(score, 0), 10), reason
    m2 = re.search(r"\b([0-9]|10)\b", response)
    if m2:
        score = int(m2.group(1))
        sentences = re.split(r"[.!?]", response)
        reason = sentences[0].strip()[:120] if sentences else response[:100]
        return min(max(score, 0), 10), reason
    return 0, response[:100]


def main() -> int:
    raw_files = sorted(SCAN_DIR.glob(f"{TODAY}_*_round*_raw_*.json"))
    if not raw_files:
        print(f"No raw files found for {TODAY}")
        return 1

    print(f"Found {len(raw_files)} raw result files")

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

    # Filter to today's jobs only
    today_jobs = [j for j in unique_jobs if j.get("postedDate", "").startswith("2026-11-04")]
    print(f"Posted today (2026-11-04): {len(today_jobs)}")

    # Score with Ollama
    print(f"\nScoring {len(today_jobs)} jobs with Ollama...")
    scored = []
    good = 0
    start = time.time()
    for i, j in enumerate(today_jobs):
        prompt = SCORING_PROMPT.format(
            title=j.get("title", ""),
            company=j.get("company", ""),
            location=j.get("location", ""),
            excerpt=j.get("excerpt", "")[:200],
        )
        try:
            content = local_ollama_chat(
                "qwen2.5:7b-instruct-q5_K_M",
                [{"role": "user", "content": prompt}],
                max_tokens=80,
            )
            if content:
                score, reason = extract_score(content)
            else:
                score, reason = 0, "no response"
        except Exception as e:
            score, reason = 0, f"error: {str(e)[:60]}"

        j["ai_score"] = score
        j["ai_reason"] = reason
        scored.append(j)
        if score >= 5:
            good += 1

        if (i + 1) % 50 == 0:
            elapsed = time.time() - start
            rate = elapsed / (i + 1)
            remaining = len(today_jobs) - (i + 1)
            eta = remaining * rate
            print(f"  {i + 1}/{len(today_jobs)} ... good: {good} ... ETA: {eta/60:.0f}min")
        time.sleep(0.1)

    elapsed = time.time() - start
    print(f"\nScoring complete: {len(scored)} scored, {good} score>=5 in {elapsed/60:.0f}min")

    # Save scored results
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    scored_file = SCAN_DIR / f"{TODAY}_all_scored_{stamp}.json"
    out = {
        "generated_at": stamp,
        "total_jobs": len(scored),
        "good_jobs": good,
        "jobs": scored,
    }
    scored_file.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(f"Saved: {scored_file.name}")

    # Save to inbox markdown grouped by platform
    good_jobs = [j for j in scored if j.get("ai_score", 0) >= 5]
    for platform in ["sn", "sf", "other"]:
        pjobs = [j for j in good_jobs if j.get("platform") == platform]
        if not pjobs:
            continue
        inbox_file = INBOX_DIR / f"scored-{platform}--{stamp}.md"
        lines = [
            "---",
            f"model: scored-platform-{platform}",
            f"scanned_at: {stamp}",
            f"task: {platform}-scored-rounds",
            "---",
            "",
            f"# {platform.upper()} Scored Jobs",
            "",
            f"Score >= 5: {len(pjobs)} jobs (from 36 focused rounds)",
            "",
            "| Score | Role | Company | Location | Source |",
            "|---|---|---|---|---|---|",
        ]
        for j in sorted(pjobs, key=lambda x: x.get("ai_score", 0), reverse=True):
            title = (j.get("title", "") or "").replace("|", "/")
            company = (j.get("company", "") or "").replace("|", "/")
            loc = (j.get("location", "") or "").replace("|", "/")
            score = j.get("ai_score", 0)
            src = j.get("source_file", "search")
            lines.append(f"| {score} | [{title}]({j.get('url','')}) | {company} | {loc} | {src} |")
        inbox_file.write_text("\n".join(lines) + "\n")
        print(f"Inbox: {inbox_file.name} ({len(pjobs)} jobs)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
