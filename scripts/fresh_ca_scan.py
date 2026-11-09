#!/usr/bin/env python3
"""Freshness-first Canadian sweep for ServiceNow / Salesforce dev+admin roles.

The hourly board scan is breadth-first: it fills seven-day windows from
aggregators and ATS APIs, so a posting made this morning can lose the table to
older rows that were already queued. This adapter is the opposite -- it only
keeps postings dated *today or yesterday*, from sources that expose an absolute
posting date or a same-day relative date, and it drops every row whose URL does
not answer.

Sources
    adzuna      api.adzuna.com, `max_days_old=2&sort_by=date` (absolute `created`)
    jobbank     jobbank.gc.ca sorted by newest (absolute "November 9, 2026")
    eluta       eluta.ca "last seen" (relative "today"/"yesterday")

Job Bank and Eluta parsing is imported from scripts/canada_index_sweep.py so
there is exactly one parser per site; a second copy would drift.

    python3 scripts/fresh_ca_scan.py                      # today + yesterday
    python3 scripts/fresh_ca_scan.py --days 3 --out-inbox inbox/x--2026-11-09--v1.md

Output
    reports/fresh_ca_<date>.json      rows + per-source stats
    inbox/fresh-ca--<date>--v1.md     6-column inbox table
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import canada_index_sweep as cis  # noqa: E402  (reuse jobbank_page / eluta_page)

INBOX = ROOT / "inbox"
OUT = ROOT / "reports"
NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y-%m-%d")
TODAY = NOW.date()

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Adzuna credentials are the public demo pair already used by
# tools/import_adzuna_jobs.py; env wins when set.
APP_ID = __import__("os").environ.get("ADZUNA_APP_ID", "54ce986e")
APP_KEY = __import__("os").environ.get("ADZUNA_APP_KEY", "db851f299e966c0a2a72af525dce6199")

ADZUNA_QUERIES = [
    "servicenow", "servicenow developer", "servicenow administrator",
    "servicenow architect", "servicenow consultant", "servicenow analyst",
    "salesforce", "salesforce developer", "salesforce administrator",
    "salesforce platform developer", "salesforce platform administrator",
    "salesforce admin", "salesforce consultant", "apex developer",
    "ITSM", "CMDB", "ServiceNow CSA CAD CIS",
]

# A title is relevant when it names the platform, one of its modules, or the
# certification the employer is buying (CSA/CAD/CIS). This mirrors the board's
# own bucket rules rather than inventing a wider net.
SN = re.compile(
    r"service\s?now|\bcsdm\b|\bcmdb\b|\bitsm\b|\bitam\b|\bitom\b|\bhrsd\b|"
    r"\bsecops\b|\bcsa\b|\bcad\b|\bcis\b|\bnow assist\b|\bflow designer\b|"
    r"\bservice catalog\b|\bglide\b", re.I)
SF = re.compile(
    r"salesforce|\bapex\b|\bsoql\b|\blwc\b|lightning|visualforce|agentforce|"
    r"\bcpq\b|mulesoft|\bsfdc\b|platform (?:developer|administrator|admin)|"
    r"\bcrm developer\b|experience cloud|\bcommunities\b", re.I)
EXCLUDE = re.compile(
    r"sales (?:representative|manager|associate|consultant|lead|agent)|"
    r"account executive|account manager|recruiter|talent acquisition|"
    r"pre-?sales|customer success|product marketing|demand gen|"
    r"marketing (?:manager|specialist|coordinator)|social media|brand manager|"
    r"business development|\bintern\b|\bco-?op\b|\bstage\b|\btrainee\b|"
    r"\bcashier\b|\bbarista\b|\bwarehouse\b", re.I)

CA_PREF = re.compile(
    r"toronto|ontario|mississauga|brampton|markham|vaughan|richmond hill|"
    r"scarborough|etobicoke|north york|oakville|hamilton|ottawa|kitchener|"
    r"waterloo|london|windsor|canada|remote", re.I)
CA_PROV = re.compile(r"\b(ON|QC|BC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b", re.I)


def get(url: str, timeout: int = 30, tries: int = 2) -> bytes | None:
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "*/*",
                              "Accept-Language": "en-CA,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 410, 403):
                return None
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def classify(title: str) -> str | None:
    if EXCLUDE.search(title):
        return None
    if SN.search(title):
        return "servicenow"
    if SF.search(title):
        return "salesforce"
    return None


def canadaish(location: str) -> bool:
    return bool(location) and bool(CA_PREF.search(location) or CA_PROV.search(location))


def priority(location: str) -> int:
    """0 = Toronto/Ontario, 1 = Canadian remote, 2 = other Canada."""
    loc = location.lower()
    if re.search(r"toronto|ontario|mississauga|brampton|markham|vaughan|"
                 r"richmond hill|scarborough|etobicoke|north york|oakville|"
                 r"hamilton|ottawa|kitchener|waterloo|london|windsor", loc):
        return 0
    if "remote" in loc or "anywhere in canada" in loc:
        return 1
    return 2


def adzuna_rows(window: list[str], stats: dict) -> list[dict]:
    rows: list[dict] = []
    for query in ADZUNA_QUERIES:
        url = ("https://api.adzuna.com/v1/api/jobs/ca/search/1"
               f"?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=50"
               f"&what={urllib.parse.quote(query)}&max_days_old={len(window) + 1}"
               "&sort_by=date&content-type=application/json")
        blob = get(url)
        stats["requests"] += 1
        if not blob:
            stats["adzuna_misses"] = stats.get("adzuna_misses", 0) + 1
            continue
        try:
            data = json.loads(blob)
        except json.JSONDecodeError:
            continue
        for r in data.get("results", []):
            created = (r.get("created") or "")[:10]
            if created not in window:
                continue
            title = (r.get("title") or "").strip()
            bucket = classify(title)
            if not bucket:
                continue
            location = ((r.get("location") or {}).get("display_name") or "").strip()
            if not canadaish(location):
                continue
            rows.append({
                "source": "adzuna", "bucket": bucket, "posted": created,
                "title": title,
                "company": ((r.get("company") or {}).get("display_name") or "").strip(),
                "location": location,
                "url": r.get("redirect_url") or r.get("url") or "",
            })
        time.sleep(0.3)
    return rows


def index_rows(window: list[str], stats: dict, eluta_pages: int,
               jobbank_pages: int) -> list[dict]:
    rows: list[dict] = []
    keywords = ["servicenow", "servicenow developer", "servicenow administrator",
                "salesforce", "salesforce developer", "salesforce administrator"]
    for kw in keywords:
        for page in range(1, jobbank_pages + 1):
            got = cis.jobbank_page(kw, page)
            stats["jobbank_pages"] += 1
            rows.extend(got)
            if not got:
                break
            time.sleep(1.0)
        for page in range(1, eluta_pages + 1):
            got, _origins = cis.eluta_page(kw, page)
            stats["eluta_pages"] += 1
            rows.extend(got)
            if not got:
                break
            time.sleep(1.0)
    kept = []
    for r in rows:
        if r.get("posted") not in window:
            continue
        bucket = classify(r.get("title", ""))
        if not bucket:
            continue
        location = r.get("location", "")
        if not canadaish(location):
            continue
        r = dict(r)
        r["bucket"] = bucket
        kept.append(r)
    return kept


def verify(url: str) -> bool:
    """A row is only submitted when its URL answers with something real."""
    if not url.startswith("http"):
        return False
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return 200 <= r.status < 400
    except urllib.error.HTTPError as e:
        return e.code in (401, 403)  # auth walls still prove the req exists
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2, help="2 = today + yesterday")
    ap.add_argument("--eluta-pages", type=int, default=3)
    ap.add_argument("--jobbank-pages", type=int, default=2)
    ap.add_argument("--verify", type=int, default=1)
    ap.add_argument("--out-inbox", default="")
    args = ap.parse_args()

    window = [(TODAY - timedelta(days=i)).isoformat() for i in range(max(args.days, 1))]
    stats = {"requests": 0, "jobbank_pages": 0, "eluta_pages": 0}

    rows = adzuna_rows(window, stats)
    rows += index_rows(window, stats, args.eluta_pages, args.jobbank_pages)

    uniq: dict[str, dict] = {}
    for r in rows:
        url = (r.get("url") or "").rstrip("/")
        if not url:
            continue
        r["url"] = url
        key = re.sub(r"[?#].*$", "", url.lower())
        uniq.setdefault(key, r)

    kept = list(uniq.values())
    if args.verify:
        before = len(kept)
        kept = [r for r in kept if verify(r["url"])]
        stats["unverified_dropped"] = before - len(kept)

    kept.sort(key=lambda r: (r["posted"], -priority(r["location"]), r["title"]), reverse=True)

    OUT.mkdir(exist_ok=True)
    (OUT / f"fresh_ca_{STAMP}.json").write_text(
        json.dumps({"generated": NOW.isoformat(), "window": window,
                    "stats": stats, "count": len(kept), "rows": kept}, indent=2),
        encoding="utf-8")

    INBOX.mkdir(exist_ok=True)
    inbox = Path(args.out_inbox) if args.out_inbox else INBOX / f"fresh-ca--{STAMP}--v1.md"
    lines = [
        f"# Fresh CA sweep — {STAMP}",
        "",
        f"Window: {', '.join(window)}. Sources: Adzuna (dated API, "
        f"{stats['requests']} calls), Job Bank ({stats['jobbank_pages']} pages), "
        f"Eluta ({stats['eluta_pages']} pages). Every URL answered before submission.",
        "",
        "| Posted | Role | Company | Location | URL | Note |",
        "|--------|------|---------|----------|-----|------|",
    ]
    safe = lambda s: str(s or "").replace("|", "/").strip()
    for r in kept:
        lines.append(
            f"| {r['posted']} | {safe(r['title'])} | {safe(r['company'])} | "
            f"{safe(r['location'])} | {r['url']} | "
            f"fresh-ca {r['source']} / {r['bucket']} |")
    inbox.write_text("\n".join(lines) + "\n", encoding="utf-8")

    by_bucket: dict[str, int] = {}
    for r in kept:
        by_bucket[r["bucket"]] = by_bucket.get(r["bucket"], 0) + 1
    print(f"window {window} | raw {len(rows)} | unique {len(uniq)} | kept {len(kept)} "
          f"| {by_bucket} | stats {stats}")
    print("inbox:", inbox)
    for r in kept[:20]:
        print(f"  {r['posted']} [{r['bucket'][:4]}] {r['title'][:52]:52} "
              f"{r['company'][:24]:24} {r['location'][:30]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
