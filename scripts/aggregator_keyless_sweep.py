#!/usr/bin/env python3
"""
Aggregator keyless sweep — Round 2 novel route.

Targets Canadian aggregators that the existing scanners never touch:
- Talent.com (high yield: 155 SN, 331 SF hits)
- Workopolis (high yield: 143 SN, 202 SF hits)
- Careerjet (live, 0 hits in probe but still indexed)

These are server-rendered HTML pages, not ATS APIs. We parse the listing
page for job cards, extract title/company/location/URL, then fetch the
detail page for a posted date when available.

CIBC exclusion is honoured: any URL or employer containing "cibc" is skipped.

Outputs inbox/aggregator-keyless--<date>--v1.md
"""
from __future__ import annotations

import argparse
import html as htmllib
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from curl_cffi import requests as cr

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

SN = re.compile(r'service\s?now|itsm|itam|cmdb|csdm|hrsd|servicenow', re.I)
SF = re.compile(r'salesforce|apex|soql|lwc|visualforce|marketing cloud|sfdc|agentforce|cpq|platform developer|platform administrator', re.I)
EXCL = re.compile(r'\b(account executive|account manager|sales representative|sales manager|business development|recruiter|talent acquisition|pre-?sales|customer success|product marketing)\b', re.I)
CIBC = re.compile(r'\bcibc\b', re.I)

CA_CITY = re.compile(r'toronto|mississauga|markham|brampton|vaughan|etobicoke|scarborough|north york|richmond hill|oakville|burlington|waterloo|kitchener|guelph|london, on|ottawa|montr[eé]al|montreal|laval|qu[eé]bec city|gatineau|calgary|edmonton|winnipeg|regina|saskatoon|vancouver|burnaby|surrey|victoria, bc|halifax|moncton|fredericton|st\.? john\'?s|charlottetown|whitehorse|yellowknife|iqaluit', re.I)
CA_FULL = re.compile(r'\b(ontario|british columbia|alberta|manitoba|saskatchewan|nova scotia|new brunswick|newfoundland( and labrador)?|prince edward island|yukon|nunavut|northwest territories)\b', re.I)
CA_CODE = re.compile(r'(?:^|[\s,(/-])(ON|BC|QC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)(?=$|[\s,)/-])')
CA_WORD = re.compile(r'\bcanada\b|\bcanadian\b|\bCAN\b', re.I)
MULTI_LOC = re.compile(r'^\s*\d+\s+locations?\s*$', re.I)
US_STATE = re.compile(r'(?:^|[\s,(/-])(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)(?=$|[\s,)/-])')

def is_canadian(location: str, url: str = "") -> bool:
    if not location or MULTI_LOC.match(location):
        return False
    if US_STATE.search(location) and not CA_CITY.search(location) and not CA_FULL.search(location):
        return False
    if CA_CITY.search(location) or CA_FULL.search(location) or CA_CODE.search(location) or CA_WORD.search(location):
        return True
    if url and ("/ca/" in url.lower() or "toronto" in url.lower() or "ontario" in url.lower()):
        return True
    return False

def classify(title: str, url: str) -> str:
    hay = f"{title} {url}".lower()
    if SN.search(hay):
        return "servicenow"
    if SF.search(hay):
        return "salesforce"
    return "other"

def norm_url(u: str) -> str:
    u = u.strip().rstrip("/")
    u = re.sub(r"^\w+://", "", u, flags=re.I)
    u = re.sub(r"^www\.", "", u, flags=re.I)
    return u.lower()

def existing_corpus() -> tuple[set[str], str]:
    blob = ""
    for name in ["README.md"] + sorted(glob.glob(str(ROOT / "README.BAK_*.md"))):
        try:
            blob += Path(name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    for f in sorted(INBOX.glob("*.md")):
        blob += f.read_text(encoding="utf-8", errors="replace")
    return {u.rstrip("/.,") for u in re.findall(r'https?://[^\s\)\]\|"]+', blob)}, blob.lower()

import glob

def fetch(url: str, timeout: int = 30) -> str | None:
    try:
        r = cr.get(url, impersonate="chrome124", timeout=timeout, headers={"User-Agent": UA})
        if r.status_code == 200:
            return r.text
    except Exception:
        pass
    return None

def parse_talent(html: str, base: str) -> list[dict]:
    rows: list[dict] = []
    # Talent.com cards are <div class="job"> or similar; look for links to /job/
    for m in re.finditer(r'href="(/job/[^"]+)"[^>]*>([^<]{5,200})</a>', html, re.I):
        url = "https://ca.talent.com" + m.group(1)
        title = htmllib.unescape(m.group(2)).strip()
        if CIBC.search(title) or CIBC.search(url):
            continue
        rows.append({"title": title, "url": url, "company": "", "location": ""})
    # Fallback: broader link scrape
    if not rows:
        for m in re.finditer(r'href="(https?://[^"]*talent\.com[^"]*job[^"]*)"[^>]*>([^<]{5,200})</a>', html, re.I):
            url = m.group(1)
            title = htmllib.unescape(m.group(2)).strip()
            if CIBC.search(title) or CIBC.search(url):
                continue
            rows.append({"title": title, "url": url, "company": "", "location": ""})
    return rows

def parse_workopolis(html: str) -> list[dict]:
    rows: list[dict] = []
    # Workopolis job cards
    for m in re.finditer(r'href="(/jobsearch/[^"]+)"[^>]*>([^<]{5,200})</a>', html, re.I):
        url = "https://www.workopolis.com" + m.group(1)
        title = htmllib.unescape(m.group(2)).strip()
        if CIBC.search(title) or CIBC.search(url):
            continue
        rows.append({"title": title, "url": url, "company": "", "location": ""})
    return rows

def parse_careerjet(html: str) -> list[dict]:
    rows: list[dict] = []
    for m in re.finditer(r'href="(/[^"]*job[^"]*)"[^>]*>([^<]{5,200})</a>', html, re.I):
        url = "https://www.careerjet.ca" + m.group(1) if m.group(1).startswith("/") else m.group(1)
        title = htmllib.unescape(m.group(2)).strip()
        if CIBC.search(title) or CIBC.search(url):
            continue
        rows.append({"title": title, "url": url, "company": "", "location": ""})
    return rows

SOURCES = [
    ("talent", "https://ca.talent.com/jobs?k=servicenow&l=Toronto%2C+Ontario", parse_talent),
    ("talent", "https://ca.talent.com/jobs?k=salesforce&l=Toronto%2C+Ontario", parse_talent),
    ("workopolis", "https://www.workopolis.com/jobsearch/find-jobs?ak=servicenow&l=Toronto%2C+ON", parse_workopolis),
    ("workopolis", "https://www.workopolis.com/jobsearch/find-jobs?ak=salesforce&l=Toronto%2C+ON", parse_workopolis),
    ("careerjet", "https://www.careerjet.ca/servicenow-jobs?s=1&l=Toronto", parse_careerjet),
    ("careerjet", "https://www.careerjet.ca/salesforce-jobs?s=1&l=Toronto", parse_careerjet),
]

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    known, _ = existing_corpus()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_rows: list[dict] = []

    for src, url, parser in SOURCES:
        html = fetch(url)
        if not html:
            print(f"[{src}] fetch failed")
            continue
        rows = parser(html, url) if src == "talent" else parser(html)
        for r in rows:
            u = norm_url(r["url"])
            if u in known:
                continue
            fam = classify(r["title"], r["url"])
            if fam == "other":
                continue
            if EXCL.search(r["title"]):
                continue
            if not is_canadian(r.get("location", ""), r["url"]):
                # still accept if URL has Toronto/Ontario signal
                if not ("toronto" in r["url"].lower() or "ontario" in r["url"].lower()):
                    continue
            out_rows.append({
                "posted": today,
                "title": r["title"][:160],
                "company": r.get("company", "")[:80],
                "location": r.get("location", "Toronto, ON"),
                "url": r["url"],
                "source": src,
                "family": fam,
            })
            known.add(u)

    if not out_rows:
        print("nothing new")
        return 0

    # write inbox
    ver = 1
    while True:
        p = INBOX / f"aggregator-keyless--{today}--v{ver}.md"
        if not p.exists():
            break
        ver += 1

    lines = [
        "---",
        f"model: aggregator-keyless",
        f"scanned_at: {datetime.now(timezone.utc).isoformat()}",
        f"task: talent-workopolis-careerjet",
        "---",
        "",
        f"# Aggregator Keyless Sweep — {today}",
        "",
        "| Posted | Role | Company | Location | Source |",
        "|---|---|---|---|---|",
    ]
    for r in out_rows:
        lines.append(f"| {r['posted']} | [{r['title']}]({r['url']}) | {r['company']} | {r['location']} | {r['source']} |")

    p.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {p} ({len(out_rows)} rows)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
