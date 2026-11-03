#!/usr/bin/env python3
"""today_feeds_scan.py — postings published *today* from employer ATS feeds.

Every other source in this repo sorts by an aggregator's idea of "recent", and
Adzuna's newest record is routinely yesterday. This pass reads the employer's
own ATS instead, where the publish timestamp is minutes old:

  SmartRecruiters  api.smartrecruiters.com/v1/companies/<co>/postings  (releasedDate)
  Workday CXS      <tenant>.wdN.myworkdayjobs.com/wday/cxs/.../jobs    (postedOn)
  Greenhouse       boards-api.greenhouse.io/v1/boards/<token>/jobs     (first_published)
  Lever            api.lever.co/v0/postings/<token>?mode=json          (createdAt)
  Ashby            api.ashbyhq.com/posting-api/job-board/<token>       (publishedAt)
  Job Bank Canada  jobbank.gc.ca search (sort=D) -> jobposting JSON-LD (datePosted)

Workday reports a *relative* stamp ("Posted Today", "Posted 13 Days Ago"); it is
converted to an absolute date by subtracting the stated number of days. Nothing
else is inferred: a source that publishes no date contributes no dated row.

Usage:
    python3 scripts/today_feeds_scan.py                # today only
    python3 scripts/today_feeds_scan.py --days 2       # today + yesterday
    python3 scripts/today_feeds_scan.py --dry-run
    python3 scripts/today_feeds_scan.py --source workday,smartrecruiters
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
RAW = ROOT / "raw"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
NOW = datetime.now(timezone.utc)

KW = re.compile(r"\bservice\s?now\b|\bsalesforce\b|\bapex\b|\bsoql\b|\blwc\b|\bitsm\b|"
                r"\bitam\b|\bcmdb\b|\bitom\b|\bnow platform\b|platform developer|"
                r"agentforce|omnistudio|revenue cloud|service cloud|sales cloud|"
                r"field service|experience cloud|commerce cloud|mulesoft", re.I)
GEO = re.compile(r"toronto|ontario|canada|mississauga|markham|brampton|vaughan|etobicoke|"
                 r"scarborough|north york|richmond hill|oakville|burlington|waterloo|"
                 r"kitchener|ottawa|montreal|montr[ée]al|quebec|calgary|vancouver|remote", re.I)
EXCL = re.compile(r"\b(account executive|account manager|sales representative|sales manager|"
                  r"business development|recruiter|talent acquisition|pre-?sales|"
                  r"customer success|marketing|growth|product marketing)\b", re.I)

SMARTRECRUITERS = ["ServiceNow"]

WORKDAY_BOARDS = [
    ("td", "wd3", "TD_Bank_Careers", "TD Bank"),
    ("bmo", "wd3", "External", "BMO"),
    ("salesforce", "wd12", "External_Career_Site", "Salesforce"),
    ("moneris", "wd3", "Moneris", "Moneris"),
    ("bdo", "wd3", "BDO", "BDO Canada"),
    ("caatpension", "wd10", "Careers", "CAAT Pension Plan"),
    ("altusgroup", "wd3", "AltusGroup", "Altus Group"),
    ("brookfield", "wd5", "brookfield", "Brookfield"),
    ("gdit", "wd5", "External_Career_Site", "GDIT"),
    ("resolvetech", "wd1", "RTS", "Resolve Tech Solutions"),
]

GREENHOUSE = [("lightfeatheriollc", "LightFeather"), ("9thwayinsignia", "9th Way Insignia"),
              ("accenturefederalservices", "Accenture Federal Services"), ("d2l", "D2L"),
              ("icapitalnetwork", "iCapital"), ("bloomerang", "Bloomerang"),
              ("neuraflash", "NeuraFlash"), ("movableink", "Movable Ink")]
LEVER = [("eqbank", "EQ Bank"), ("alimentiv-2", "Alimentiv"), ("versapay", "Versapay")]
ASHBY = [("benevity", "Benevity"), ("loopio", "Loopio"), ("moego", "MoeGo")]

JOBBANK_QUERIES = [("servicenow", "Toronto, ON"), ("salesforce", "Toronto, ON"),
                   ("servicenow", "Ontario"), ("salesforce administrator", "Ontario")]


def fetch(url: str, *, method="GET", body: bytes | None = None,
          headers: dict | None = None, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, data=body, method=method,
                                 headers={"User-Agent": UA, "Accept": "application/json,text/html",
                                          **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_json(url: str, **kw):
    return json.loads(fetch(url, **kw))


def iso_day(value) -> str | None:
    """Absolute date from ISO string / epoch ms. No guessing."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(value / 1000, timezone.utc).date().isoformat()
    s = str(value).strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).date().isoformat()
    except ValueError:
        pass
    m = re.match(r"(\d{4}-\d{2}-\d{2})", s)
    return m.group(1) if m else None


def workday_day(posted_on: str) -> str | None:
    """'Posted Today' / 'Posted 13 Days Ago' / 'Posted 30+ Days Ago' -> ISO date."""
    if not posted_on:
        return None
    s = posted_on.lower()
    if "today" in s:
        return NOW.date().isoformat()
    if "yesterday" in s:
        return (NOW.date() - timedelta(days=1)).isoformat()
    m = re.search(r"(\d+)\+?\s*days?\s*ago", s)
    if m:
        return (NOW.date() - timedelta(days=int(m.group(1)))).isoformat()
    m = re.search(r"(\d+)\+?\s*hours?\s*ago", s)
    if m:
        return NOW.date().isoformat()
    return None


def norm(u: str) -> str:
    try:
        s = urllib.parse.urlsplit(u)
        return f"{s.netloc.lower().replace('www.', '')}{s.path.rstrip('/')}".lower()
    except Exception:
        return u.lower()


def known_urls() -> set[str]:
    known: set[str] = set()
    for p in [ROOT / "README.md", *sorted(ROOT.glob("README.BAK_*.md"))[:2], ROOT / "APPLIED.md"]:
        try:
            known.update(norm(u) for u in re.findall(r"https?://[^\s)|]+", p.read_text(errors="replace")))
        except OSError:
            pass
    for p in INBOX.glob("*.md"):
        if p.name.startswith(("todayfeeds--", "_ai-triage")):
            continue
        try:
            known.update(norm(u) for u in re.findall(r"https?://[^\s)|]+", p.read_text(errors="replace")))
        except OSError:
            pass
    try:
        data = json.loads((ROOT / "jobs.json").read_text())
        jobs = data.get("jobs", data) if isinstance(data, dict) else data
        for j in jobs:
            if isinstance(j, dict) and j.get("url"):
                known.add(norm(j["url"]))
    except (OSError, json.JSONDecodeError):
        pass
    return known


# ---------------------------------------------------------------------------
# sources: each yields dicts {title, company, location, url, posted, source}


def from_smartrecruiters(_: int) -> list[dict]:
    out = []
    for slug in SMARTRECRUITERS:
        for offset in range(0, 800, 100):
            try:
                data = fetch_json(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings"
                                  f"?limit=100&offset={offset}")
            except Exception as exc:
                print(f"[sr:{slug}] {type(exc).__name__} {str(exc)[:60]}")
                break
            items = data.get("content") or []
            for it in items:
                loc = it.get("location") or {}
                loc_text = ", ".join(x for x in (loc.get("city"), loc.get("region"),
                                                 loc.get("country")) if x)
                out.append({"title": it.get("name") or "", "company": slug,
                            "location": loc_text + (" · Remote" if loc.get("remote") else ""),
                            "url": f"https://jobs.smartrecruiters.com/{slug}/{it.get('id')}",
                            "posted": iso_day(it.get("releasedDate")), "source": "smartrecruiters"})
            if len(items) < 100:
                break
    return out


def from_workday(days: int) -> list[dict]:
    out = []
    for tenant, wd, site, label in WORKDAY_BOARDS:
        api = f"https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
        for query in ("servicenow", "salesforce"):
            try:
                data = fetch_json(api, method="POST",
                                  body=json.dumps({"appliedFacets": {}, "limit": 20,
                                                   "offset": 0, "searchText": query}).encode(),
                                  headers={"content-type": "application/json"})
            except Exception as exc:
                print(f"[workday:{tenant}] {type(exc).__name__} {str(exc)[:50]}")
                continue
            for p in data.get("jobPostings") or []:
                posted = workday_day(p.get("postedOn") or "")
                if posted and (NOW.date() - datetime.fromisoformat(posted).date()).days > days:
                    continue
                out.append({"title": p.get("title") or "", "company": label,
                            "location": p.get("locationsText") or "",
                            "url": f"https://{tenant}.{wd}.myworkdayjobs.com/en-US/{site}{p.get('externalPath')}",
                            "posted": posted, "source": "workday"})
    return out


def from_greenhouse(_: int) -> list[dict]:
    out = []
    for token, label in GREENHOUSE:
        try:
            data = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")
        except Exception as exc:
            print(f"[greenhouse:{token}] {type(exc).__name__} {str(exc)[:50]}")
            continue
        for j in data.get("jobs") or []:
            out.append({"title": j.get("title") or "", "company": label,
                        "location": (j.get("location") or {}).get("name") or "",
                        "url": j.get("absolute_url") or "",
                        "posted": iso_day(j.get("first_published") or j.get("updated_at")),
                        "source": "greenhouse"})
    return out


def from_lever(_: int) -> list[dict]:
    out = []
    for token, label in LEVER:
        try:
            data = fetch_json(f"https://api.lever.co/v0/postings/{token}?mode=json")
        except Exception as exc:
            print(f"[lever:{token}] {type(exc).__name__} {str(exc)[:50]}")
            continue
        for j in data if isinstance(data, list) else []:
            out.append({"title": j.get("text") or "", "company": label,
                        "location": ((j.get("categories") or {}).get("location") or ""),
                        "url": j.get("hostedUrl") or "",
                        "posted": iso_day(j.get("createdAt")), "source": "lever"})
    return out


def from_ashby(_: int) -> list[dict]:
    out = []
    for token, label in ASHBY:
        try:
            data = fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}")
        except Exception as exc:
            print(f"[ashby:{token}] {type(exc).__name__} {str(exc)[:50]}")
            continue
        for j in data.get("jobs") or []:
            out.append({"title": j.get("title") or "", "company": label,
                        "location": j.get("location") or "",
                        "url": j.get("jobUrl") or "",
                        "posted": iso_day(j.get("publishedAt")), "source": "ashby"})
    return out


DATE_LD = re.compile(r'"datePosted"\s*:\s*"([^"]{8,40})"')


def from_jobbank(max_detail: int) -> list[dict]:
    """Job Bank has no working JSON API (500). Search HTML -> detail JSON-LD."""
    ids: list[str] = []
    for keyword, location in JOBBANK_QUERIES:
        url = ("https://www.jobbank.gc.ca/jobsearch/jobsearch?"
               + urllib.parse.urlencode({"searchstring": keyword, "locationstring": location,
                                         "sort": "D"}))
        try:
            html = fetch(url, headers={"Accept": "text/html"}).decode("utf-8", "replace")
        except Exception as exc:
            print(f"[jobbank:{keyword}] {type(exc).__name__} {str(exc)[:50]}")
            continue
        for m in re.findall(r"jobposting/(\d+)", html):
            if m not in ids:
                ids.append(m)
    ids = ids[:max_detail]
    out: list[dict] = []
    for jid in ids:
        purl = f"https://www.jobbank.gc.ca/jobsearch/jobposting/{jid}"
        try:
            html = fetch(purl, headers={"Accept": "text/html"}).decode("utf-8", "replace")
        except Exception:
            continue
        m = DATE_LD.search(html)
        if not m:
            continue                       # no published date -> no row, never a guess
        title = re.search(r"<title>(.*?)</title>", html, re.S)
        t = re.sub(r"\s+", " ", (title.group(1) if title else "")).replace("| Job Bank", "").strip()
        out.append({"title": t, "company": "Job Bank employer", "location": "Canada",
                    "url": purl, "posted": iso_day(m.group(1)), "source": "jobbank"})
    return out


SOURCES = {"smartrecruiters": from_smartrecruiters, "workday": from_workday,
           "greenhouse": from_greenhouse, "lever": from_lever, "ashby": from_ashby,
           "jobbank": from_jobbank}


def keep(row: dict, known: set[str], days: int, seen: set[str]) -> bool:
    url, title = row.get("url") or "", row.get("title") or ""
    if not url or not title or EXCL.search(title):
        return False
    hay = f"{title} {row.get('location') or ''}"
    if not KW.search(hay) or not GEO.search(hay):
        return False
    posted = row.get("posted")
    if posted:
        age = (NOW.date() - datetime.fromisoformat(posted).date()).days
        if age > days or age < 0:
            return False
    key = norm(url)
    if key in known or key in seen:
        return False
    seen.add(key)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=1, help="how many days back counts as fresh")
    ap.add_argument("--source", default=None, help="comma-separated subset")
    ap.add_argument("--jobbank-max", type=int, default=25)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    wanted = [s.strip() for s in args.source.split(",")] if args.source else list(SOURCES)
    known, seen = known_urls(), set()
    rows: list[dict] = []
    per_source: dict[str, tuple[int, int]] = {}

    with futures.ThreadPoolExecutor(max_workers=3) as ex:
        jobs = {}
        for name in wanted:
            fn = SOURCES[name]
            jobs[name] = ex.submit(fn, args.jobbank_max if name == "jobbank" else args.days)

    for name in wanted:
        try:
            raw = jobs[name].result()
        except Exception as exc:                 # noqa: BLE001
            print(f"[{name}] failed: {type(exc).__name__} {str(exc)[:70]}")
            per_source[name] = (0, 0)
            continue
        kept = [r for r in raw if keep(r, known, args.days, seen)]
        rows.extend(kept)
        per_source[name] = (len(raw), len(kept))
        print(f"[{name:<14}] fetched {len(raw):>4}  kept {len(kept):>3}")

    rows.sort(key=lambda r: (r["posted"] or "", r["company"]))
    today = NOW.date().isoformat()
    today_rows = [r for r in rows if r["posted"] == today]
    print(f"\n[{len(rows)} fresh rows · {len(today_rows)} posted today]")

    if args.dry_run or not rows:
        for r in rows[:20]:
            print(f"  {r['posted'] or 'undated':<10} [{r['source'][:12]:<12}] "
                  f"{r['title'][:52]:<52} | {r['company'][:18]:<18} | {r['location'][:24]}")
        return 0 if rows else 0

    INBOX.mkdir(parents=True, exist_ok=True)
    ver = 1
    while (INBOX / f"todayfeeds--{today}--v{ver}.md").exists():
        ver += 1
    target = INBOX / f"todayfeeds--{today}--v{ver}.md"
    lines = ["---", "model: todayfeeds",
             f"scanned_at: {NOW.strftime('%Y-%m-%dT%H:%M:%SZ')}",
             "task: ats-and-jobbank-today", "---", "",
             f"# Today's postings from employer ATS — {today}", "",
             "Publish timestamps come from each ATS. Workday's relative \"Posted Today\" is",
             "converted arithmetically; Job Bank rows carry the page's own `datePosted`.",
             "A posting with no published date is not listed here at all.",
             "", "| Posted | Role | Company | Location | Source |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['posted'] or '—'} | [{r['title'].replace('|', '/')}]({r['url']}) | "
                     f"{r['company'].replace('|', '/')} | {(r['location'] or 'Not specified')[:60].replace('|', '/')} "
                     f"| via {r['source']} |")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    RAW.mkdir(parents=True, exist_ok=True)
    (RAW / "today_feeds_last.json").write_text(json.dumps(
        {"generated_at": NOW.isoformat(), "rows": rows, "per_source": per_source}, indent=2),
        encoding="utf-8")
    print(f"[todayfeeds] wrote {target.relative_to(ROOT)} (+{len(rows)} rows, {len(today_rows)} today)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
