#!/usr/bin/env python3
"""keyless_ddg_scan.py — DuckDuckGo HTML dorker for ServiceNow/Salesforce roles.

The paid search APIs (Tavily 432, Firecrawl 402) are exhausted. This route
uses the public DuckDuckGo HTML endpoint with site: and inurl: dorks to reach
ATS families that have no public JSON API (iCIMS, Njoyn, Dayforce, Ultipro,
Taleo, SuccessFactors, Jobvite, BambooHR, Pinpoint, etc.).

It is deliberately keyless and respects the user's "improve our breadth of
search" directive.

Output: inbox/keyless-ddg--YYYY-MM-DD--vN.md
"""

from __future__ import annotations

import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Dorks that reach the families the existing scanners do not cover.
DORKS = [
    # iCIMS (no public API; slug discovery is the blocker)
    'site:icims.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
    # Njoyn / CareerBeacon (Ontario public sector / hospitals / universities)
    'site:njoyn.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario)',
    'site:careerbeacon.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario)',
    # Dayforce / Ceridian
    'site:dayforce.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
    # Ultipro / UKG
    'site:ultipro.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
    # Taleo / Oracle Recruiting Cloud (non-REST path)
    'site:taleo.net ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
    # SuccessFactors
    'site:successfactors.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
    # Jobvite
    'site:jobvite.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
    # BambooHR / Pinpoint (no public API; only reachable via dork)
    'site:bamboohr.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
    'site:pinpointhq.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
    # Phenom (RBC, Bell, BMO use it; sitemap route exists but dork catches more)
    'site:phenom.com ("ServiceNow" OR "Salesforce") (Toronto OR Ontario OR Canada)',
]

TITLE_RE = re.compile(r'<a[^>]+class="result__a"[^>]*>([^<]+)</a>', re.I)
URL_RE = re.compile(r'class="result__a"[^>]*href="([^"]+)"', re.I)
LOC_RE = re.compile(r'class="result__loc"[^>]*>([^<]+)</a>', re.I)


def fetch(q: str, timeout: int = 30) -> str:
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "en-CA,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:                                  # noqa: BLE001
        print(f"[ddg] ERR {type(e).__name__}: {e}")
        return ""


def parse(html: str, base_q: str) -> list[dict]:
    out = []
    titles = TITLE_RE.findall(html)
    urls = URL_RE.findall(html)
    locs = LOC_RE.findall(html)
    n = min(len(titles), len(urls))
    for i in range(n):
        title = titles[i].strip()
        url = urllib.parse.unquote(urls[i])
        loc = locs[i].strip() if i < len(locs) else ""
        if not title or not url:
            continue
        out.append({
            "posted": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "title": title,
            "company": "",          # DDG HTML does not expose employer reliably
            "location": loc,
            "url": url,
            "query": base_q[:80],
        })
    return out


def is_canadian(row: dict) -> bool:
    loc = (row.get("location") or "").lower()
    url = (row.get("url") or "").lower()
    return any(x in loc for x in ("toronto", "ontario", "canada", "ottawa",
                                   "mississauga", "brampton", "hamilton")) or \
           "/ca/" in url or "/canada/" in url


def write_inbox(rows: list[dict], day: str) -> Path:
    INBOX.mkdir(exist_ok=True)
    n = 1
    while (INBOX / f"keyless-ddg--{day}--v{n}.md").exists():
        n += 1
    path = INBOX / f"keyless-ddg--{day}--v{n}.md"
    lines = [
        "---",
        "model: keyless-ddg",
        f"scanned_at: {datetime.now(timezone.utc).isoformat()}",
        "task: ddg-html-dork-breadth",
        f"rows: {len(rows)}",
        "---",
        "",
        f"# Keyless DDG sweep — {day}",
        "",
        "| Posted | Role | Company | Location | URL |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r.get('posted')} "
            f"| [{r.get('title','')}]({r.get('url','')}) "
            f"| {r.get('company','')} | {r.get('location','')} "
            f"| {r.get('url','')} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    all_rows: list[dict] = []
    for dork in DORKS:
        print(f"[ddg] {dork[:70]}...")
        html = fetch(dork)
        if not html:
            time.sleep(2)
            continue
        rows = parse(html, dork)
        can = [r for r in rows if is_canadian(r)]
        print(f"       -> {len(rows)} raw, {len(can)} Canadian")
        all_rows.extend(can)
        time.sleep(3)  # be polite to DDG
    # Dedupe by URL
    seen, uniq = set(), []
    for r in all_rows:
        u = r.get("url")
        if u and u not in seen:
            seen.add(u)
            uniq.append(r)
    print(f"unique Canadian: {len(uniq)}")
    if uniq:
        path = write_inbox(uniq, day)
        print(f"wrote {path}")
    else:
        print("nothing to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())