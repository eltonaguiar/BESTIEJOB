#!/usr/bin/env python3
"""Daily LinkedIn guest-search sweep -> inbox submission.

Uses LinkedIn's public guest job-search fragment endpoint (no key, no login).
Writes `inbox/linkedin-guest-<YYYY-MM-DD>--v<N>.md`, skipping anything already
present in README.md, any README.BAK_*.md archive, or an existing inbox file.

Usage
  python3 scripts/linkedin_guest_scan.py                 # write submission only
  python3 scripts/linkedin_guest_scan.py --apply         # also merge + rebuild site
  python3 scripts/linkedin_guest_scan.py --days 7        # wider window
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

KEYWORDS = [
    "ServiceNow", "ServiceNow Developer", "ServiceNow Administrator",
    "ServiceNow Architect", "ServiceNow Consultant",
    "Salesforce", "Salesforce Developer", "Salesforce Administrator",
    "Salesforce Consultant", "ITSM", "CMDB", "MuleSoft",
    # Variants — postings hide behind these titles as often as the obvious ones
    "ServiceNow ITSM", "ServiceNow ITAM", "ServiceNow ITOM",
    "ServiceNow platform", "ServiceNow technical consultant",
    "ServiceNow SecOps", "ITSM analyst", "ITAM analyst", "CMDB analyst",
    "service management analyst", "Salesforce technical",
    "Salesforce platform developer", "Salesforce CPQ", "Apex developer",
    "Salesforce Marketing Cloud", "Salesforce Agentforce",
    "CRM developer", "business systems analyst",
    # Module/ cert-level variants: employers title by module at least as often
    # as by platform, and LinkedIn's keyword match is title-driven.
    "ServiceNow GRC", "ServiceNow HRSD", "ServiceNow FSO", "ServiceNow CSM",
    "ServiceNow SAM", "ServiceNow HAM", "ServiceNow Discovery",
    "ServiceNow portal", "ServiceNow integration", "ServiceNow QA",
    "ServiceNow business analyst", "ServiceNow project manager",
    "ITSM consultant", "ITSM developer", "CMDB administrator",
    "service catalog developer", "ITOM consultant",
    "Salesforce Lightning", "Salesforce integration", "Salesforce QA",
    "Salesforce solution architect", "Salesforce business analyst",
    "Salesforce DevOps", "Salesforce Experience Cloud",
    "Salesforce data migration", "Salesforce Pardot", "Apex",
    # 2026-11-04 AI-panel keyword sweep (raw/ai_queries_60d.json): module and
    # product names employers use in titles that the list above still missed.
    "CMDB specialist", "ITAM consultant", "ServiceNow GSD",
    "ServiceNow sysdev", "ServiceNow release", "ServiceNow table",
    "Salesforce Wave", "Salesforce AHC", "Salesforce Flow", "Salesforce Apex",
]
LOCATIONS = ["Toronto%2C%20Ontario%2C%20Canada", "Canada",
             "Mississauga%2C%20Ontario%2C%20Canada",
             "Markham%2C%20Ontario%2C%20Canada"]

RELEVANT = re.compile(
    r"servicenow|salesforce|itsm|itam|cmdb|itom|\bsnow\b|apex|mulesoft|"
    r"integration hub|service catalog|grc|now assist", re.I)
EXCLUDE = re.compile(
    r"sales\s+(representative|associate|manager|consultant|lead|agent)|"
    r"account executive|retail|store manager|cashier|teller|barista", re.I)

CARD_TITLE = re.compile(r'class="base-search-card__title"[^>]*>\s*(.*?)\s*<', re.S)
CARD_COMPANY = re.compile(r'class="hidden-nested-link"[^>]*>\s*(.*?)\s*<', re.S)
CARD_LINK = re.compile(r'href="(https://[a-z]{2}\.linkedin\.com/jobs/view/[^"?]+)')
CARD_DATE = re.compile(r'datetime="([0-9]{4}-[0-9]{2}-[0-9]{2})"')
CARD_LOC = re.compile(r'class="job-search-card__location"[^>]*>\s*(.*?)\s*<', re.S)


def norm(text: str) -> str:
    text = (text or "").replace("&amp;", "&").lower()
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text).split())


def existing_corpus() -> tuple[set[str], str]:
    blob = ""
    for name in ["README.md"] + sorted(glob.glob(str(ROOT / "README.BAK_*.md"))):
        try:
            blob += Path(name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    for f in sorted(INBOX.glob("*.md")):
        blob += f.read_text(encoding="utf-8", errors="replace")
    urls = {u.rstrip("/.,") for u in re.findall(r'https?://[^\s\)\]\|"]+', blob)}
    return urls, blob.lower()


def fetch(kw: str, loc: str, start: int, days: int) -> list[dict]:
    url = ("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
           f"?keywords={kw}&location={loc}&f_TPR=r{days * 86400}&start={start}")
    r = None
    for _ in range(3):
        try:
            r = cr.get(url, impersonate="chrome124", timeout=30,
                       headers={"User-Agent": UA})
        except Exception:
            time.sleep(2)
            continue
        if r.status_code == 200:
            break
        time.sleep(3)
    if r is None or r.status_code != 200:
        return []
    out = []
    for card in re.findall(r"<li>(.*?)</li>", r.text, re.S):
        t, link = CARD_TITLE.search(card), CARD_LINK.search(card)
        if not (t and link):
            continue
        title = " ".join(t.group(1).split())
        if not RELEVANT.search(title) or EXCLUDE.search(title):
            continue
        comp, loc_m, date_m = CARD_COMPANY.search(card), CARD_LOC.search(card), CARD_DATE.search(card)
        out.append({
            "title": title[:200],
            "company": (" ".join(comp.group(1).split()) if comp else "")[:120],
            "location": (" ".join(loc_m.group(1).split()) if loc_m else "")[:120],
            "url": link.group(1),
            "posted": date_m.group(1) if date_m else None,
        })
    return out


def next_version(day: str) -> Path:
    n = 1
    while (INBOX / f"linkedin-guest--{day}--v{n}.md").exists():
        n += 1
    return INBOX / f"linkedin-guest--{day}--v{n}.md"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=3)
    # The guest endpoint allows ~1 req/2s; each extra location/pages multiplies
    # the sweep, so both are capped by a flag rather than edited in place.
    ap.add_argument("--locations", type=int, default=len(LOCATIONS),
                    help=f"how many of the {len(LOCATIONS)} locations to sweep")
    ap.add_argument("--pages", type=int, default=2, help="result pages per keyword (25 jobs each)")
    ap.add_argument("--apply", action="store_true", help="merge into README and rebuild the site")
    ap.add_argument("--max-per-table", type=int, default=400)
    args = ap.parse_args()

    today = datetime.now(timezone.utc).date()
    urls, corpus = existing_corpus()

    found: list[dict] = []
    for kw in KEYWORDS:
        for loc in LOCATIONS[:max(1, args.locations)]:
            for start in (0, 25)[:max(1, args.pages)]:
                found.extend(fetch(kw.replace(" ", "%20"), loc, start, args.days))
                time.sleep(0.8)

    seen, fresh = set(), []
    for j in found:
        key = j["url"].split("?")[0].rstrip("/")
        if key in seen or key in urls:
            continue
        if f'{norm(j["title"])[:60]}|{norm(j["company"])[:30]}' in corpus:
            continue
        seen.add(key)
        fresh.append(j)

    # Was hardcoded to 1 day, which silently discarded everything the widened
    # --days window had just fetched. The floor now follows the flag.
    floor = (today - timedelta(days=max(0, args.days))).isoformat()
    fresh = [j for j in fresh if j["posted"] and floor <= j["posted"] <= today.isoformat()]
    fresh.sort(key=lambda j: j["posted"], reverse=True)

    RAW.mkdir(exist_ok=True)
    (RAW / f"linkedin_guest_{today.isoformat()}.json").write_text(
        json.dumps({"scannedAt": datetime.now(timezone.utc).isoformat(timespec='seconds'),
                    "total": len(found), "fresh": fresh}, indent=1), encoding="utf-8")

    print(f"linkedin: {len(found)} cards, {len(fresh)} new (window {floor}..{today})")
    if not fresh:
        return 0

    rows = "\n".join(
        f'| {j["posted"]} | {j["title"]} | {j["company"]} | {j["location"]} | {j["url"]} | LinkedIn guest' for j in fresh)
    INBOX.mkdir(exist_ok=True)
    target = next_version(today.isoformat())
    target.write_text(
        "---\n"
        "model: linkedin-guest\n"
        f"scanned_at: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        f"task: automated-linkedin-guest-{args.days}d\n"
        f"notes: {len(found)} cards scanned, {len(fresh)} not already listed.\n"
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
