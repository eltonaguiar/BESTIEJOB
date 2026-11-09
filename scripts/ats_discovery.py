#!/usr/bin/env python3
"""ats_discovery.py — ask employers' own ATS for postings, not an aggregator.

Adzuna/Job Bank/Eluta only carry what they choose to index, and a search engine
answers a job query with listing pages. Workday and SmartRecruiters each expose a
credential-free list endpoint for a single employer, so this pass asks the
employer directly. Workday's list gives a relative label ("Posted Today"), which
is accepted only when it names the day outright; the absolute date always comes
from the posting's own JSON via ats_date_resolve.

Usage:
    python3 scripts/ats_discovery.py --days 2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))

from ats_date_resolve import resolve as ats_date          # noqa: E402
from fresh_ca_scan import (INBOX, canadaish, classify, known_urls,  # noqa: E402
                           norm_url, verify)

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# (tenant, host shard, site). A wrong guess costs one 404 and is skipped.
WORKDAY = [
    ("salesforce", "wd12", "External_Career_Site"),
    ("gdit", "wd5", "External_Career_Site"),
    ("bmo", "wd3", "External"),
    ("rbc", "wd3", "External"),
    ("cibc", "wd3", "External"),
    ("scotiabank", "wd3", "External"),
    ("manulife", "wd3", "External"),
    ("sunlife", "wd3", "External"),
    ("telus", "wd3", "External"),
    ("opg", "wd3", "External"),
]
SMARTRECRUITERS = ["ServiceNow"]
QUERIES = ["ServiceNow", "Salesforce"]
TODAY = datetime.now(timezone.utc)


def get_json(url: str, payload: dict | None = None) -> dict | None:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"User-Agent": UA, "Accept": "application/json"}
    if data:
        headers["Content-Type"] = "application/json"
    try:
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError):
        return None


WD_URL = re.compile(
    r"https://([a-z0-9-]+)\.(wd[0-9]+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/]+)/job/")


def seeds_from_board() -> list[tuple[str, str, str]]:
    """Workday tenants proven live by postings the board already carries.

    The hard-coded list above is guesswork: a wrong shard or site 404s, and 20
    guesses produced 3 rows. Every Workday URL on the board encodes the exact
    (tenant, shard, site) triple that answered, so those are used first.
    """
    seen: list[tuple[str, str, str]] = []
    readme = ROOT / "README.md"
    if not readme.exists():
        return seen
    for m in WD_URL.finditer(readme.read_text(encoding="utf-8", errors="ignore")):
        triple = (m.group(1), m.group(2), m.group(3))
        if triple not in seen:
            seen.append(triple)
    return seen


def workday_rows(query: str, stats: dict, seeds: list) -> list[dict]:
    rows = []
    for tenant, host, site in seeds:
        base = f"https://{tenant}.{host}.myworkdayjobs.com/wday/cxs/{tenant}/{site}"
        data = get_json(base + "/jobs", {"appliedFacets": {}, "limit": 20,
                                         "offset": 0, "searchText": query})
        stats["workday_calls"] += 1
        if not data:
            continue
        for jp in data.get("jobPostings", []):
            title = jp.get("title") or ""
            if not classify(title):
                continue
            # Only the labels that name the day. "Posted 5 Days Ago" needs our
            # clock, not the employer's, and the detail JSON has the real date.
            if not re.search(r"\btoday\b|\byesterday\b", jp.get("postedOn") or "", re.I):
                continue
            rows.append({"title": title, "company": tenant.title(),
                         "location": jp.get("locationsText") or "",
                         "url": f"https://{tenant}.{host}.myworkdayjobs.com/en-US/{site}"
                                f"{jp.get('externalPath', '')}",
                         "source": "workday"})
    return rows


def smartrecruiters_rows(query: str, stats: dict) -> list[dict]:
    rows = []
    for company in SMARTRECRUITERS:
        url = (f"https://api.smartrecruiters.com/v1/companies/{company}/postings"
               f"?limit=100&q={urllib.parse.quote(query)}")
        data = get_json(url)
        stats["smartrecruiters_calls"] += 1
        if not data:
            continue
        for p in data.get("content", []):
            title = p.get("name") or ""
            if not classify(title):
                continue
            loc = p.get("location") or {}
            released = (p.get("releasedDate") or "")[:10]
            rows.append({"title": title, "company": company,
                         "location": ", ".join(str(v) for v in
                                               (loc.get("city"), loc.get("country")) if v),
                         "url": f"https://jobs.smartrecruiters.com/{company}/{p.get('id')}",
                         "source": "smartrecruiters", "date": released})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2)
    args = ap.parse_args()
    window = {(TODAY - timedelta(days=i)).date().isoformat() for i in range(max(args.days, 1))}
    stats = {"workday_calls": 0, "smartrecruiters_calls": 0}

    seeds: list[tuple[str, str, str]] = []
    for triple in seeds_from_board() + WORKDAY:
        if triple not in seeds:
            seeds.append(triple)
    seeds = seeds[:24]
    print(f"workday tenants: {len(seeds)}")

    raw = []
    for q in QUERIES:
        raw += workday_rows(q, stats, seeds)
        raw += smartrecruiters_rows(q, stats)

    uniq: dict[str, dict] = {}
    for r in raw:
        if r["url"]:
            uniq.setdefault(norm_url(r["url"]), r)

    board = known_urls()
    kept, dropped = [], {"old": 0, "non_canada": 0, "undated": 0, "board": 0, "dead": 0}
    for r in uniq.values():
        if norm_url(r["url"]) in board:
            dropped["board"] += 1
            continue
        if r.get("location") and not canadaish(r["location"]):
            dropped["non_canada"] += 1
            continue
        posted = r.get("date") or ats_date(r["url"]) or ""
        if not posted:
            dropped["undated"] += 1
            continue
        if posted[:10] not in window:
            dropped["old"] += 1
            continue
        if not verify(r["url"]):
            dropped["dead"] += 1
            continue
        r["posted"] = posted[:10]
        r["bucket"] = classify(r["title"]) or "other"
        kept.append(r)

    kept.sort(key=lambda r: (r["posted"], r["title"]), reverse=True)
    stamp = TODAY.date().isoformat()
    n = 1
    inbox = INBOX / f"ats--{stamp}--v{n}.md"
    while inbox.exists():
        n += 1
        inbox = INBOX / f"ats--{stamp}--v{n}.md"
    lines = [f"# ATS discovery — {stamp}", "",
             f"Window: {', '.join(sorted(window))}. Employer list endpoints: "
             f"Workday ({stats['workday_calls']} calls), SmartRecruiters "
             f"({stats['smartrecruiters_calls']} calls). Absolute dates from each "
             "posting's own JSON; every URL answered before submission.", "",
             "| Posted | Role | Company | Location | URL | Note |",
             "|--------|------|---------|----------|-----|------|"]
    safe = lambda s: str(s or "").replace("|", "/").strip()
    for r in kept:
        lines.append(f"| {r['posted']} | {safe(r['title'])} | {safe(r['company'])} | "
                     f"{safe(r['location'])} | {r['url']} | ats {r['source']} / {r['bucket']} |")
    inbox.parent.mkdir(exist_ok=True)
    inbox.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"raw {len(raw)} | unique {len(uniq)} | kept {len(kept)} | dropped {dropped}")
    print("inbox:", inbox)
    for r in kept[:15]:
        print(f"  {r['posted']} {r['title'][:50]:50} {r['company'][:18]:18} {r['location'][:28]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
