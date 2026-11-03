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
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from ai_panel import get_key  # noqa: E402

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
# Platform mentions are not platform roles: a legal-counsel posting can name
# ServiceNow as an internal tool. Description-only matches must also look like an
# IT role.
TECH_TITLE = re.compile(
    r"developer|administrator|analyst|engineer|architect|consultant|specialist|"
    r"programmer|systems?\b|\bIT\b|information technology|integration|"
    r"database|application|software|\bQA\b|devops|platform", re.I)

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

# Boards verified 2026-11-03 to actually carry SN/SF titles (count of matching
# roles in brackets). Dead slugs 404 and are skipped, so this list only grows
# with boards that proved they post this work.
GREENHOUSE = [("neuraflash", "NeuraFlash"),        # 47 SN/SF
              ("brex", "Brex"),                     # 4
              ("mongodb", "MongoDB"),               # 4
              ("icapitalnetwork", "iCapital"),      # 2
              ("toast", "Toast"),                   # 1
              ("bloomerang", "Bloomerang"),         # 1
              ("movableink", "Movable Ink"),        # 1
              ("lightfeatheriollc", "LightFeather"),
              ("9thwayinsignia", "9th Way Insignia"),
              ("accenturefederalservices", "Accenture Federal Services"),
              ("d2l", "D2L")]
LEVER = [("eqbank", "EQ Bank"), ("alimentiv-2", "Alimentiv"), ("versapay", "Versapay")]
ASHBY = [("benevity", "Benevity"), ("loopio", "Loopio"), ("moego", "MoeGo")]

# Quoted phrases matter: an unquoted "servicenow" makes Job Bank match any word
# in the description and returns shipping clerks, while "servicenow consultant"
# returns the actual postings. Verified 2026-11-03.
JOBBANK_QUERIES = [
    ('"servicenow"', "Toronto, ON"), ('"servicenow"', "Ontario"),
    ('"servicenow developer"', "Ontario"), ('"servicenow consultant"', "Ontario"),
    ('"servicenow administrator"', "Ontario"), ('"servicenow"', "Mississauga, ON"),
    ('"salesforce"', "Toronto, ON"), ('"salesforce"', "Ontario"),
    ('"salesforce developer"', "Ontario"), ('"salesforce administrator"', "Ontario"),
    ('"servicenow"', "Canada"), ('"salesforce"', "Canada"),
]


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
    """'Posted Today' / 'Posted 13 Days Ago' -> ISO date; '30+ Days Ago' -> None.

    Workday's "Posted 30+ Days Ago" is an open-ended bucket, not a day: the true
    date is *older* than 30 days, never newer. Back-dating it to exactly 30 days
    would put the freshest possible reading on the stalest postings.
    """
    if not posted_on:
        return None
    s = posted_on.lower()
    if "30+" in s:
        return None
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


# Adzuna is the richest Canadian aggregator and the only source here with a native
# `max_days_old` filter, so "posted in the last N days" is the API's own answer.
# It needs an app id + app key pair. The pair below is the repo's public demo
# credential (also in scripts/scrape_adzuna*.js); its quota is shared and often
# exhausted, and a 429 means *throttled* ("Usage limits exceeded"), never "bad key".
ADZUNA_DEMO = ("54ce986e", "db851f299e966c0a2a72af525dce6199")

ADZUNA_QUERIES = [
    ("servicenow", "Toronto"), ("servicenow", "Ontario"),
    ("servicenow developer", "Canada"), ("servicenow administrator", "Ontario"),
    ("servicenow consultant", "Toronto"),
    ("salesforce", "Toronto"), ("salesforce", "Ontario"),
    ("salesforce developer", "Canada"), ("salesforce administrator", "Ontario"),
    ("apex developer", "Toronto"),
]


def adzuna_credentials() -> tuple[str, str, str]:
    """env -> dbpasses.txt -> the repo's demo pair. Returns (id, key, mode)."""
    app_id = os.environ.get("ADZUNA_APP_ID") or get_key("ADZUNA_APP_ID")
    app_key = (os.environ.get("ADZUNA_API_KEY") or os.environ.get("ADZUNA_APP_KEY")
               or get_key("ADZUNA_APP_KEY"))
    if app_id and app_key:
        return app_id, app_key, "configured"
    return ADZUNA_DEMO[0], ADZUNA_DEMO[1], "demo"


def from_adzuna(days: int) -> list[dict]:
    app_id, app_key, mode = adzuna_credentials()
    out: list[dict] = []
    throttled = False
    for what, where in ADZUNA_QUERIES:
        if throttled:
            break
        for page in (1, 2):
            url = (f"https://api.adzuna.com/v1/api/jobs/ca/search/{page}?"
                   + urllib.parse.urlencode({
                       "app_id": app_id, "app_key": app_key, "results_per_page": 50,
                       "what": what, "where": where, "sort_by": "date",
                       "max_days_old": days, "content-type": "application/json"}))
            try:
                data = json.loads(fetch(url))
            except urllib.error.HTTPError as exc:
                if exc.code == 429:
                    print(f"[adzuna:{mode}] quota exhausted (429) — stopping this source")
                    throttled = True
                else:
                    print(f"[adzuna:{mode}] HTTP {exc.code} on '{what}'")
                break
            except Exception as exc:                      # noqa: BLE001
                print(f"[adzuna:{mode}] {type(exc).__name__} on '{what}'")
                break
            results = data.get("results") or []
            for r in results:
                out.append({"title": r.get("title") or "",
                            "company": (r.get("company") or {}).get("display_name") or "Unknown",
                            "location": (r.get("location") or {}).get("display_name") or where,
                            "url": r.get("redirect_url") or "",
                            "posted": iso_day(r.get("created")), "source": "adzuna"})
            if len(results) < 50:
                break
    print(f"[adzuna:{mode}] {len(out)} postings")
    return out


MONTHS = {name: i + 1 for i, name in enumerate(
    ("january", "february", "march", "april", "may", "june", "july",
     "august", "september", "october", "november", "december"))}

# Job Bank does NOT publish schema.org JSON-LD. Its date is a microdata span with
# human text (verified 2026-11-03):
#   <span property="datePosted" class="date"> Posted on October 29, 2026 </span>
# The old `"datePosted": "..."` JSON regex never matched, so this source silently
# contributed zero rows on every run.
DATE_POSTED = re.compile(r'property="datePosted"[^>]*>(.*?)</span>', re.S)
DATE_TEXT = re.compile(r"posted\s+on\s+([a-z]+)\s+(\d{1,2}),\s*(\d{4})", re.I)
TITLE_TAG = re.compile(r"<title>(.*?)</title>", re.S)
HIRING_ORG = re.compile(r'property="hiringOrganization".*?property="name"[^>]*>(.*?)</span>', re.S)


def jobbank_day(html: str) -> str | None:
    """Microdata 'Posted on October 29, 2026' -> '2026-10-29'. Never guessed."""
    span = DATE_POSTED.search(html)
    if not span:
        return None
    m = DATE_TEXT.search(re.sub(r"\s+", " ", span.group(1)))
    if not m:
        return None
    month = MONTHS.get(m.group(1).lower())
    if not month:
        return None
    return f"{int(m.group(3)):04d}-{month:02d}-{int(m.group(2)):02d}"


# Search-result markup, verified 2026-11-03. Every row carries its own title,
# employer, city and date, so no detail fetch is needed for those fields:
#   <h3 class="noctitle"> title </h3>
#   <li class="date">November 03, 2026</li>
#   <li class="business">Employer</li>
#   <li class="location">... Mississauga (ON)</li>
JOB_ID = re.compile(r"jobposting/(\d+)")
JB_TITLE = re.compile(r'class="noctitle">(.*?)</span>', re.S)
JB_DATE = re.compile(r'class="date">(.*?)</li>', re.S)
JB_BIZ = re.compile(r'class="business">(.*?)</li>', re.S)
JB_LOC = re.compile(r'class="wb-inv">Location</span>\s*(.*?)</li>', re.S)


def jobbank_text_day(text: str) -> str | None:
    """'November 03, 2026' -> '2026-11-03'. Never guessed."""
    m = re.search(r"([A-Za-z]+)\s+(\d{1,2}),\s*(\d{4})", text or "")
    if not m:
        return None
    month = MONTHS.get(m.group(1).lower())
    if not month:
        return None
    return f"{int(m.group(3)):04d}-{month:02d}-{int(m.group(2)):02d}"


def _jobbank_rows(html: str) -> list[dict]:
    """One dict per search-result row."""
    rows: list[dict] = []
    for chunk in html.split('class="noctitle"')[1:]:
        chunk = 'class="noctitle"' + chunk
        jid, title, date = JOB_ID.search(chunk), JB_TITLE.search(chunk), JB_DATE.search(chunk)
        if not (jid and title):
            continue
        biz, loc = JB_BIZ.search(chunk), JB_LOC.search(chunk)
        city = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", loc.group(1))).strip() if loc else ""
        rows.append({
            "jid": jid.group(1),
            "title": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title.group(1))).strip(),
            "company": (re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", biz.group(1))).strip()
                        if biz else "Job Bank employer"),
            # Job Bank writes "Mississauga (ON)"; append the country so the shared
            # geo filter accepts every Canadian city, not only the listed ones.
            "location": f"{city}, Canada" if city else "Canada",
            "posted": jobbank_text_day(re.sub(r"<[^>]+>", "", date.group(1))) if date else None,
        })
    return rows


def from_jobbank(max_detail: int) -> list[dict]:
    """Job Bank, searched the way Job Bank actually works.

    It matches the job *title*, and no employer titles a posting "ServiceNow" —
    the real titles are NOC-style ("computer systems analyst"). So this queries
    the vocabulary Job Bank understands (role titles) and then tests the platform
    keyword against the posting's own description. The old code searched for
    "servicenow", which Job Bank cannot match against a title, so it returned
    shipping clerks and the keyword filter then discarded everything.
    """
    cands: dict[str, dict] = {}
    for keyword, location in JOBBANK_QUERIES:
        url = ("https://www.jobbank.gc.ca/jobsearch/jobsearch?"
               + urllib.parse.urlencode({"searchstring": keyword,
                                         "locationstring": location, "sort": "D"}))
        try:
            html = fetch(url, headers={"Accept": "text/html"}).decode("utf-8", "replace")
        except Exception as exc:                       # noqa: BLE001
            print(f"[jobbank:{keyword}] {type(exc).__name__} {str(exc)[:50]}")
            continue
        for row in _jobbank_rows(html):
            cands.setdefault(row["jid"], row)

    out: list[dict] = []
    checks = 0
    for jid, row in cands.items():
        if not row["posted"]:
            continue                    # no published date -> no row, never a guess
        matched = KW.search(row["title"])
        if not matched:
            if not TECH_TITLE.search(row["title"]):
                continue        # description may name the platform; the role is not IT
            if checks >= max_detail:    # cap detail fetches; each is ~200 KB
                continue
            checks += 1
            try:
                html = fetch(f"https://www.jobbank.gc.ca/jobsearch/jobposting/{jid}",
                             headers={"Accept": "text/html"}).decode("utf-8", "replace")
            except Exception:                          # noqa: BLE001
                continue
            # The detail URL is session-stateful: fetched without a warm session it
            # can return a different posting's page, which made "counsel" and
            # "shipping coordinator" appear to mention ServiceNow. Verify identity
            # against the page's own <title> before believing its description.
            page = TITLE_TAG.search(html)
            page_title = (re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", page.group(1))).lower()
                          if page else "")
            if row["title"][:24].lower() not in page_title:
                continue
            matched = KW.search(re.sub(r"<[^>]+>", " ", html))
        if not matched:
            continue
        out.append({"title": row["title"], "company": row["company"],
                    "location": row["location"],
                    "url": f"https://www.jobbank.gc.ca/jobsearch/jobposting/{jid}",
                    "posted": row["posted"], "source": "jobbank",
                    "match": re.sub(r"\s+", " ", matched.group(0)).strip()})
    print(f"[jobbank] {len(cands)} candidates, {checks} descriptions read, {len(out)} matched")
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
    ap.add_argument("--jobbank-max", type=int, default=120)
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
