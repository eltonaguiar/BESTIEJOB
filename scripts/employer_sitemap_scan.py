#!/usr/bin/env python3
"""Employer career-site scan for Phenom-hosted banks/telcos.

Phenom tenant ids (discovered 2026-11-02 from each site's
`cdn.phenompeople.com/CareerConnectResources/...` asset paths):

    RBC  -> RBCAA0088      jobs.rbc.com
    Bell -> BECACA         jobs.bell.ca
    BMO  -> BOMOGLOBAL     jobs.bmo.com

Phenom's JSON APIs reject these tenants without a session
(`/api/apply/v2/jobs?domain=<tid>` -> "Tenant not identified",
 `/api/jobs?...` -> HTTP 500/404), and the search pages are client-rendered
(no JobPosting JSON-LD, no cards in the HTML). What *does* work is the public
sitemap: it lists every live requisition URL, and each requisition page carries
JobPosting JSON-LD with an exact `datePosted`.

This script therefore goes sitemap -> keyword filter -> detail page -> date.

Usage
  python3 scripts/employer_sitemap_scan.py              # write inbox submission
  python3 scripts/employer_sitemap_scan.py --apply      # merge + rebuild site
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from curl_cffi import requests as cr
except ImportError:
    sys.exit("FATAL: curl_cffi not installed (pip install curl_cffi)")

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
RAW = ROOT / "raw"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

EMPLOYERS = {
    "RBC": ("https://jobs.rbc.com", "RBCAA0088", ["https://jobs.rbc.com/sitemap.xml"]),
    "Bell": ("https://jobs.bell.ca", "BECACA", ["https://jobs.bell.ca/sitemap.xml"]),
    "BMO": ("https://jobs.bmo.com", "BOMOGLOBAL", ["https://jobs.bmo.com/sitemap.xml"]),
}

KEYWORDS = re.compile(r"servicenow|salesforce|itsm|itam|cmdb|itom|mulesoft|apex|"
                      r"service-?now|integration-hub|now-assist", re.I)

CANADA = re.compile(r"toronto|ontario|mississauga|markham|montreal|montr|quebec|"
                    r"ottawa|calgary|vancouver|edmonton|waterloo|canada|brampton|"
                    r"scarborough|north york|laval|brossard|halifax|winnipeg|victoria", re.I)

LOC = re.compile(r'"addressLocality"\s*:\s*"([^"]+)"')
REGION = re.compile(r'"addressRegion"\s*:\s*"([^"]+)"')
DATE = re.compile(r'"datePosted"\s*:\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})')
TITLE = re.compile(r'"title"\s*:\s*"([^"]{4,160})"')


def sitemap_urls(entry: str, depth: int = 0) -> list[str]:
    """Return <loc> entries, following one level of sitemap index."""
    if depth > 2:
        return []
    try:
        r = cr.get(entry, impersonate="chrome124", timeout=30, headers={"User-Agent": UA})
    except Exception:
        return []
    if r.status_code != 200:
        return []
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
    if "<sitemapindex" in r.text:
        out: list[str] = []
        for loc in locs:
            out.extend(sitemap_urls(loc, depth + 1))
        return out
    return locs


def existing_urls() -> tuple[set[str], str]:
    blob = ""
    for name in ["README.md"] + sorted(glob.glob(str(ROOT / "README.BAK_*.md"))):
        try:
            blob += Path(name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    for f in sorted(INBOX.glob("*.md")):
        blob += f.read_text(encoding="utf-8", errors="replace")
    return {u.rstrip("/.,") for u in re.findall(r'https?://[^\s\)\]\|"]+', blob)}, blob.lower()


def norm(text: str) -> str:
    text = (text or "").replace("&amp;", "&").lower()
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text).split())


def detail(url: str) -> dict | None:
    try:
        r = cr.get(url, impersonate="chrome124", timeout=30, headers={"User-Agent": UA})
    except Exception:
        return None
    if r.status_code != 200:
        return None
    title = TITLE.search(r.text)
    date = DATE.search(r.text)
    if not title or not date:
        return None
    loc = LOC.search(r.text)
    region = REGION.search(r.text)
    where = ", ".join(x for x in [loc.group(1) if loc else "", region.group(1) if region else ""] if x)
    return {"title": title.group(1), "posted": date.group(1), "location": where}


def next_version(day: str) -> Path:
    n = 1
    while (INBOX / f"employer-sitemap--{day}--v{n}.md").exists():
        n += 1
    return INBOX / f"employer-sitemap--{day}--v{n}.md"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=30, help="keep postings newer than N days")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-per-table", type=int, default=150)
    ap.add_argument("--all-locations", action="store_true", help="keep non-Canadian rows too")
    args = ap.parse_args()

    today = datetime.now(timezone.utc).date()
    cutoff = (today - timedelta(days=args.days)).isoformat()
    known, corpus = existing_urls()

    found: list[dict] = []
    report: dict[str, str] = {}
    for employer, (base, tid, sitemaps) in EMPLOYERS.items():
        urls: list[str] = []
        for sm in sitemaps:
            urls.extend(sitemap_urls(sm))
        jobs = [u for u in urls if "/job/" in u]
        hits = [u for u in jobs if KEYWORDS.search(u.split("/job/", 1)[-1])]
        report[employer] = f"{len(jobs)} job urls, {len(hits)} keyword hits"
        for u in hits:
            key = u.split("?")[0].rstrip("/")
            if key in known:
                continue
            info = detail(u)
            time.sleep(0.4)
            if not info:
                continue
            if not (cutoff <= info["posted"] <= today.isoformat()):
                continue
            if not args.all_locations and not CANADA.search(info["location"]):
                continue
            if f'{norm(info["title"])[:60]}|{norm(employer)[:30]}' in corpus:
                continue
            found.append({"employer": employer, "url": u, **info})

    RAW.mkdir(exist_ok=True)
    (RAW / f"employer_sitemap_{today.isoformat()}.json").write_text(
        json.dumps({"scannedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "report": report, "found": found}, indent=1), encoding="utf-8")

    for k, v in report.items():
        print(f"{k:6s} {v}")
    print(f"new postings: {len(found)}")
    for j in found:
        print(f"  {j['posted']} | {j['employer']:4s} | {j['title'][:64]} | {j['location'][:26]}")
    if not found:
        return 0

    rows = "\n".join(
        f'| {j["posted"]} | {j["title"]} | {j["employer"]} | {j["location"]} | {j["url"]} | '
        f'employer sitemap, JSON-LD datePosted |' for j in sorted(found, key=lambda j: j["posted"], reverse=True))
    INBOX.mkdir(exist_ok=True)
    target = next_version(today.isoformat())
    target.write_text(
        "---\n"
        "model: employer-sitemap\n"
        f"scanned_at: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        "task: phenom-sitemap-scan\n"
        "notes: RBC/Bell/BMO Phenom tenants (RBCAA0088/BECACA/BOMOGLOBAL) via sitemap; "
        "JSON APIs reject the tenant, sitemap + JSON-LD is the working route.\n"
        "---\n\n| Posted | Role | Company | Location | URL | Note |\n|---|---|---|---|---|---|\n"
        + rows + "\n",
        encoding="utf-8",
    )
    print(f"wrote {target.relative_to(ROOT)}")

    if args.apply:
        subprocess.run([sys.executable, str(ROOT / "tools" / "jobs_merge_inbox.py"),
                        "--max-per-table", str(args.max_per_table)], check=True)
        subprocess.run([sys.executable, str(ROOT / "tools" / "build_site.py")], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
