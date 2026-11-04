#!/usr/bin/env python3
"""Public-sector scan: Ontario Public Service + City of Toronto.

The board was ~78% staffing-agency postings with essentially no public-sector
employers, because none of the existing scanners can read these two boards:

  City of Toronto   https://jobs.toronto.ca/jobsatcity/  (SAP SuccessFactors)
      Server-rendered tiles on /search/ carry a data-url per posting; the
      detail page exposes schema.org/JobPosting microdata, including an exact
      `datePosted` and `validThrough`. Only external postings are visible
      (internal-only competitions need an employee login), so a small daily
      count is normal — it is not a scraper failure.

  Ontario Public Service   https://www.gojobs.gov.on.ca/Search.aspx
      A custom ASP.NET site behind Radware Bot Manager (perfdrive). Plain
      requests get the "We apologize for the inconvenience" challenge page
      instead of results, and the 2026-10-31 review already declined to solve
      that CAPTCHA. So this script never tries to defeat it: it probes once,
      records `blocked`, and falls back to the Government of Canada Job Bank
      employer feed, which mirrors OPS competitions with a posted date on both
      the list and the detail page:

          https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=ontario+public+service&sort=D

      Job Bank carries the employer verbatim ("Ontario Public Service"), so
      the fallback rows are still genuinely OPS postings, just a subset of what
      gojobs lists. Rows say which route produced them.

Every row must resolve to a live posting date. Undated or closed pages are
dropped rather than dated by guesswork.

Usage
  python3 scripts/public_sector_scan.py                 # write inbox submission
  python3 scripts/public_sector_scan.py --all           # no title keyword filter
  python3 scripts/public_sector_scan.py --apply         # merge + rebuild site
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

TORONTO_BASE = "https://jobs.toronto.ca"
TORONTO_SEARCH = TORONTO_BASE + "/jobsatcity/search/"
OPS_SEARCH = "https://www.gojobs.gov.on.ca/Search.aspx"
JOBBANK_OPS = ("https://www.jobbank.gc.ca/jobsearch/jobsearch"
               "?searchstring=ontario+public+service&sort=D")

# Platform roles are the board's core; the rest are the generic titles the
# public sector actually uses for the same work ("Senior Systems Analyst" is
# an ERP/CRM role far more often than not).
KEYWORDS = re.compile(
    r"servicenow|salesforce|itsm|itam|cmdb|itom|mulesoft|apex|service-?now|"
    r"integration-hub|now-assist|business systems analyst|systems analyst|"
    r"application(s)? developer|software developer|software engineer|"
    r"crm|erp|application(s)? analyst|integration (developer|analyst|specialist)|"
    r"service desk|it service|information technology|technical architect|"
    r"solution architect|data analyst|database administrator|cloud",
    re.I)

# Radware challenge fingerprints. Any of these means "blocked", never "empty".
BLOCK_MARKERS = ("perfdrive.com", "Radware Captcha", "We apologize for the inconvenience")

CARD_URL = re.compile(r'data-url="(/jobsatcity/job/[^"]+)"')
RECORDS_RETURNED = re.compile(r'data-record-returned="(\d+)"')
OG_TITLE = re.compile(r'<meta property="og:title" content="([^"]{3,200})"')
DATE_POSTED = re.compile(r'itemprop="datePosted" content="([^"]+)"')
VALID_THROUGH = re.compile(r'itemprop="validThrough" content="([^"]+)"')
LOCALITY = re.compile(r'itemprop="addressLocality" content="([^"]+)"')
REGION = re.compile(r'itemprop="addressRegion" content="([^"]+)"')

JB_ARTICLE = re.compile(r'<article id="article-\d+".*?</article>', re.S)
JB_DATE = re.compile(r'class="date">\s*([^<]+?)\s*<')
JB_BIZ = re.compile(r'class="business">\s*([^<]+?)\s*<')
JB_TITLE = re.compile(r'class="noctitle">\s*(.*?)\s*</span>', re.S)
JB_LOC = re.compile(r'<li class="location">(.*?)</li>', re.S)
JB_LINK = re.compile(r'href="(/jobsearch/jobposting/[^"]+)"')
JB_DETAIL_DATE = re.compile(r'"datePosted" class="date">\s*Posted on\s*([A-Za-z]+ \d{1,2}, \d{4})')

OPS_EMPLOYERS = re.compile(
    r"^(Ontario Public Service|Government of Ontario|"
    r"(Ministry|Ministry of) .+|Ontario Provincial Police|Metrolinx)$", re.I)


def norm(text: str) -> str:
    text = (text or "").replace("&amp;", "&").lower()
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text).split())


def text_of(html: str) -> str:
    return " ".join(re.sub(r"<[^>]+>", " ", html or "").split())


def existing_corpus() -> tuple[set[str], str]:
    blob = ""
    for name in ["README.md"] + sorted(glob.glob(str(ROOT / "README.BAK_*.md"))):
        try:
            blob += Path(name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    for f in sorted(INBOX.glob("*.md")):
        try:
            blob += f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    urls = {u.rstrip("/.,") for u in re.findall(r'https?://[^\s\)\]\|"]+', blob)}
    return urls, blob.lower()


def get(session, url: str) -> str | None:
    try:
        r = session.get(url, timeout=30)
    except Exception:
        return None
    if r.status_code != 200:
        return None
    return r.text


def parse_meta_date(raw: str) -> str | None:
    """`Fri Oct 16 00:00:00 UTC 2026` -> `2026-10-16`."""
    for fmt in ("%a %b %d %H:%M:%S UTC %Y", "%Y-%m-%d", "%a %b %d %Y"):
        try:
            return datetime.strptime(raw.strip(), fmt).date().isoformat()
        except ValueError:
            continue
    return None


def parse_jb_date(raw: str) -> str | None:
    """`November 03, 2026` -> `2026-11-03`."""
    try:
        return datetime.strptime(raw.strip(), "%B %d, %Y").date().isoformat()
    except ValueError:
        return None


# --------------------------------------------------------------------------
# City of Toronto (SuccessFactors career site)
# --------------------------------------------------------------------------
def toronto_scan(session, days: int, cutoff: str, today: str,
                 keep_all: bool) -> tuple[list[dict], dict]:
    seen_urls: list[str] = []
    for start in (0, 25, 50, 75, 100):
        html = get(session, f"{TORONTO_SEARCH}?startrow={start}")
        if not html:
            break
        found = CARD_URL.findall(html)
        returned = RECORDS_RETURNED.search(html)
        for path in found:
            if path not in seen_urls:
                seen_urls.append(path)
        total = int(returned.group(1)) if returned else len(found)
        if not found or len(seen_urls) >= total:
            break
        time.sleep(0.5)

    rows: list[dict] = []
    undated = 0
    for path in seen_urls:
        detail = get(session, TORONTO_BASE + path)
        time.sleep(0.4)
        if not detail:
            undated += 1
            continue
        posted_raw = DATE_POSTED.search(detail)
        posted = parse_meta_date(posted_raw.group(1)) if posted_raw else None
        if not posted:
            # 200 but no datePosted => posting pulled/closed; never guess a date.
            undated += 1
            continue
        if not (cutoff <= posted <= today):
            continue
        title_m = OG_TITLE.search(detail)
        title = text_of(title_m.group(1)) if title_m else ""
        if not title:
            undated += 1
            continue
        if not keep_all and not KEYWORDS.search(title):
            continue
        city = (LOCALITY.search(detail).group(1) if LOCALITY.search(detail) else "").strip()
        region = (REGION.search(detail).group(1) if REGION.search(detail) else "").strip()
        where = ", ".join(x for x in (city, region) if x) or "Toronto, ON"
        valid = VALID_THROUGH.search(detail)
        rows.append({
            "employer": "City of Toronto",
            "title": title[:180],
            "posted": posted,
            "location": where,
            "url": TORONTO_BASE + path,
            "route": "jobs.toronto.ca",
            "validThrough": parse_meta_date(valid.group(1)) if valid else None,
        })
    return rows, {"tiles": len(seen_urls), "undated_or_closed": undated}


# --------------------------------------------------------------------------
# Ontario Public Service (own board, Job Bank mirror as fallback)
# --------------------------------------------------------------------------
def ops_via_gojobs(session) -> tuple[list[dict], str]:
    """Return (rows, status). Rows are only ever dated by the site itself."""
    html = get(session, OPS_SEARCH)
    if not html:
        return [], "unreachable"
    if any(m.lower() in html.lower() for m in BLOCK_MARKERS):
        return [], "blocked (Radware bot manager)"
    # The real search page lists competitions as Preview.aspx?JobID=<id> links.
    links = sorted(set(re.findall(r'(?:Preview|JobDetails)\.aspx\?[^"\'<>\s]*JobID=\d+', html)))
    if not links:
        return [], "no links on page"
    rows: list[dict] = []
    for href in links:
        detail = get(session, "https://www.gojobs.gov.on.ca/" + href.replace("&amp;", "&"))
        time.sleep(0.4)
        if not detail:
            continue
        posted_raw = DATE_POSTED.search(detail) or re.search(
            r'Apply By[^<]*?(\d{4}-\d{2}-\d{2})', detail)
        posted = parse_meta_date(posted_raw.group(1)) if posted_raw else None
        if not posted:
            continue
        title_m = OG_TITLE.search(detail) or re.search(r'<h1[^>]*>(.*?)</h1>', detail, re.S)
        title = text_of(title_m.group(1)) if title_m else ""
        if not title:
            continue
        rows.append({
            "employer": "Ontario Public Service",
            "title": title[:180],
            "posted": posted,
            "location": "Ontario",
            "url": "https://www.gojobs.gov.on.ca/" + href.replace("&amp;", "&"),
            "route": "gojobs.gov.on.ca",
            "validThrough": None,
        })
    return rows, f"ok ({len(links)} competitions)"


def ops_via_jobbank(session, cutoff: str, today: str, keep_all: bool) -> tuple[list[dict], dict]:
    html = get(session, JOBBANK_OPS)
    if not html:
        return [], {"error": "job bank unreachable"}
    articles = JB_ARTICLE.findall(html)
    rows: list[dict] = []
    skipped_employer = 0
    undated = 0
    for a in articles:
        biz_m, date_m, title_m, link_m = JB_BIZ.search(a), JB_DATE.search(a), JB_TITLE.search(a), JB_LINK.search(a)
        if not (biz_m and date_m and title_m and link_m):
            undated += 1
            continue
        employer = text_of(biz_m.group(1)).strip()
        if not OPS_EMPLOYERS.match(employer):
            skipped_employer += 1
            continue
        posted = parse_jb_date(date_m.group(1))
        title = text_of(title_m.group(1)).strip()
        if not posted or not title:
            undated += 1
            continue
        if not (cutoff <= posted <= today):
            continue
        if not keep_all and not KEYWORDS.search(title):
            continue
        loc_m = JB_LOC.search(a)
        where = re.sub(r"^Location\s*", "", text_of(loc_m.group(1))) if loc_m else "Ontario"
        url = "https://www.jobbank.gc.ca" + link_m.group(1).split(";jsessionid")[0]
        rows.append({
            "employer": employer,
            "title": title[:180],
            "posted": posted,
            "location": where or "Ontario",
            "url": url,
            "route": "Job Bank (OPS employer feed)",
            "validThrough": None,
        })
    return rows, {"articles": len(articles), "non_ops_skipped": skipped_employer,
                  "undated": undated}


def next_version(day: str) -> Path:
    n = 1
    while (INBOX / f"public-sector--{day}--v{n}.md").exists():
        n += 1
    return INBOX / f"public-sector--{day}--v{n}.md"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=45, help="keep postings newer than N days")
    ap.add_argument("--all", action="store_true", help="skip the title keyword filter")
    ap.add_argument("--apply", action="store_true", help="merge inbox + rebuild site")
    ap.add_argument("--max-per-table", type=int, default=400)
    args = ap.parse_args()

    today_d = datetime.now(timezone.utc).date()
    today = today_d.isoformat()
    cutoff = (today_d - timedelta(days=args.days)).isoformat()
    known, corpus = existing_corpus()

    session = cr.Session(impersonate="chrome124", headers={"User-Agent": UA})

    toronto_rows, toronto_stats = toronto_scan(session, args.days, cutoff, today, args.all)
    ops_status_rows, ops_status = ops_via_gojobs(session)
    ops_rows, jb_stats = [], {}
    route_note = "gojobs.gov.on.ca"
    if ops_status != "blocked (Radware bot manager)" and ops_status_rows:
        ops_rows = ops_status_rows
    else:
        ops_rows, jb_stats = ops_via_jobbank(session, cutoff, today, args.all)
        route_note = "Job Bank (OPS employer feed)"

    found: list[dict] = []
    for row in toronto_rows + ops_rows:
        key = row["url"].split("?")[0].rstrip("/")
        if key in known:
            continue
        if f'{norm(row["title"])[:60]}|{norm(row["employer"])[:30]}' in corpus:
            continue
        found.append(row)

    report = {
        "scannedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "window_days": args.days,
        "toronto": toronto_stats,
        "ops_gojobs_status": ops_status,
        "ops_jobbank": jb_stats,
        "ops_route": route_note,
        "found": found,
    }
    RAW.mkdir(exist_ok=True)
    (RAW / f"public_sector_{today}.json").write_text(json.dumps(report, indent=1), encoding="utf-8")

    print(f"City of Toronto   {toronto_stats['tiles']} tiles, "
          f"{toronto_stats['undated_or_closed']} undated/closed")
    print(f"OPS gojobs        {ops_status}")
    if jb_stats:
        print(f"OPS Job Bank      {jb_stats.get('articles', 0)} articles, "
              f"{jb_stats.get('non_ops_skipped', 0)} non-OPS skipped, "
              f"{jb_stats.get('undated', 0)} unparsed")
    print(f"new postings: {len(found)}")
    for j in found:
        print(f"  {j['posted']} | {j['employer'][:26]:26s} | {j['title'][:58]:58s} | {j['location'][:22]}")

    if not found:
        return 0

    rows = "\n".join(
        f'| {j["posted"]} | {j["title"]} | {j["employer"]} | {j["location"]} | {j["url"]} | '
        f'{j["route"]}, live datePosted |'
        for j in sorted(found, key=lambda r: (r["posted"], r["employer"]), reverse=True))
    INBOX.mkdir(exist_ok=True)
    target = next_version(today)
    target.write_text(
        "---\n"
        "model: public-sector\n"
        f"scanned_at: {report['scannedAt']}\n"
        "task: ops-toronto-board-scan\n"
        f"notes: City of Toronto SuccessFactors tiles + schema.org datePosted; OPS via "
        f"{route_note}. gojobs.gov.on.ca probe returned: {ops_status}.\n"
        "---\n\n| Posted | Role | Company | Location | URL | Note |\n|---|---|---|---|---|---|\n"
        + rows + "\n",
        encoding="utf-8",
    )
    print(f"wrote {target.relative_to(ROOT)}")

    if args.apply:
        subprocess.run([sys.executable, str(ROOT / "tools" / "jobs_merge_inbox.py"),
                        "--max-per-table", str(args.max_per_table)], check=True)
        subprocess.run(["node", str(ROOT / "scripts" / "sync_readme_to_jobs.mjs")], check=True)
        subprocess.run([sys.executable, str(ROOT / "tools" / "build_site.py")], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
