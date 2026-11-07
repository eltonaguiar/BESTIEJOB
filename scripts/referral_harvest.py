#!/usr/bin/env python3
"""
Referral harvester - scrapes job posting pages for referral program information.
Reads jobs.json, fetches each job page, extracts referral info, writes back.
"""
import json
import re
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

REFERRAL_PATTERNS = [
    re.compile(r"employee referral program", re.I),
    re.compile(r"refer a friend", re.I),
    re.compile(r"employee referral", re.I),
    re.compile(r"employee referral bonus", re.I),
    re.compile(r"referral bonus", re.I),
    re.compile(r"referral program", re.I),
]

def fetch_url(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None

def extract_referral_info(html):
    if not html:
        return None
    info = {
        "referral_program_mentioned": False,
        "referral_bonus": None,
        "referral_details": [],
    }
    haystack = html.lower()
    if re.search(r"employee referral program", haystack):
        info["referral_program_mentioned"] = True
    if re.search(r"refer a friend", haystack):
        info["referral_program_mentioned"] = True
    if re.search(r"employee referral", haystack):
        info["referral_program_mentioned"] = True

    bonus_patterns = [
        re.compile(r"referral bonus of \$([\d,]+)", re.I),
        re.compile(r"\$([\d,]+) referral bonus", re.I),
        re.compile(r"referral bonus of up to \$([\d,]+)", re.I),
        re.compile(r"earn up to \$([\d,]+) per referral", re.I),
        re.compile(r"earn \$([\d,]+) per referral", re.I),
    ]
    for pattern in bonus_patterns:
        for m in pattern.finditer(html):
            info["referral_bonus"] = m.group(1)
            break

    for pattern in REFERRAL_PATTERNS:
        for m in pattern.finditer(html):
            start = max(0, m.start() - 100)
            end = min(len(html), m.end() + 100)
            snippet = html[start:end].strip()
            snippet = snippet.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            snippet = re.sub(r"<[^>]+>", " ", snippet)
            snippet = re.sub(r"\s+", " ", snippet).strip()
            if len(snippet) > 20:
                info["referral_details"].append(snippet[:200])

    seen = set()
    unique = []
    for d in info["referral_details"]:
        if d not in seen:
            seen.add(d)
            unique.append(d)
    info["referral_details"] = unique[:5]

    return info if info["referral_program_mentioned"] or info["referral_bonus"] or info["referral_details"] else None

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="jobs_from_gh.json")
    ap.add_argument("--output", default="jobs_with_referral.json")
    ap.add_argument("--limit", type=int, default=50)
    ap.add_argument("--delay", type=float, default=1.0)
    args = ap.parse_args()

    with open(args.input) as f:
        data = json.load(f)
    jobs = d.get("jobs", []) if isinstance(d := json.load(open(args.input)), dict) else d
    # Actually re-load properly
    with open(args.input) as f:
        raw = json.load(f)
    jobs = raw.get("jobs", raw) if isinstance(raw, dict) else raw

    processed = 0
    updated = 0
    found = 0

    for i, job in enumerate(jobs):
        if i >= args.limit:
            break
        url = job.get("url", "")
        if not url:
            continue
        print(f"[{i+1}/{args.limit}] {job.get('title','')} | {job.get('company','')}")
        print(f"  URL: {url}")
        html = fetch_url(url)
        if html:
            info = extract_referral_info(html)
            if info:
                job["referral"] = info
                updated += 1
                found += 1
                print(f"  -> Referral found: bonus={info['referral_bonus']}, details={len(info['referral_details'])}")
            else:
                print(f"  -> No referral info")
        else:
            print(f"  -> Failed to fetch")
        processed += 1
        time.sleep(args.delay)

    raw["jobs"] = jobs if isinstance(raw, dict) else all_new
    with open(args.output, "w") as f:
        json.dump(raw, f, indent=2)
    print(f"\nDone! Processed {processed}, updated {updated}, found referral: {found}")
    print(f"Output: {args.output}")

if __name__ == "__main__":
    main()
