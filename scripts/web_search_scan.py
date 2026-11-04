#!/usr/bin/env python3
"""web_search_scan.py — real web search (Exa / Tavily / Firecrawl) -> inbox/.

The Adzuna/LinkedIn passes only see what those aggregators index. The search
APIs we already hold keys for reach employer pages, partner career sites, and
regional boards directly, so this pass closes the gap the aggregators leave.

Hard rule, same as gap_scan.mjs: a posting date comes from the page or the row
stays undated. Search snippets often contain no date at all, and a "2 days ago"
is never converted into a date. Undated rows go into inbox/ with an em dash and
the merger skips them — they are review candidates, not live listings.

Usage:
    python3 scripts/web_search_scan.py                 # all providers with a key
    python3 scripts/web_search_scan.py --provider tavily
    python3 scripts/web_search_scan.py --dry-run       # print, write nothing
    python3 scripts/web_search_scan.py --max-queries 4 --max-fetch 10
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
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
sys.path.insert(0, str(ROOT / "tools"))

from ai_panel import get_key  # noqa: E402  (reuses the one key-parsing implementation)

INBOX = ROOT / "inbox"
RAW = ROOT / "raw"
README = ROOT / "README.md"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
MAX_AGE_DAYS = 31

# Queries the aggregator keyword lists do not ask. Kept short on purpose: each
# one costs a search-API credit and a handful of page fetches.
#
# These queries MUST be scoped with `site:` to an ATS domain.  A bare keyword
# query ("ServiceNow developer jobs Toronto") describes a *listing page*, and a
# search engine answers it with listing pages: measured 2026-11-04, 16 of 20
# raw results were index/category pages that INDEX_URL and INDEX_TITLE correctly
# discarded, so the run returned 0 rows while spending 100 search credits.
# Scoping to an ATS host can only surface that host's individual postings.
QUERIES = [
    "site:myworkdayjobs.com ServiceNow Toronto",
    "site:myworkdayjobs.com Salesforce Toronto",
    "site:myworkdayjobs.com ServiceNow Ontario",
    "site:myworkdayjobs.com Salesforce Canada",
    "site:boards.greenhouse.io ServiceNow Canada",
    "site:boards.greenhouse.io Salesforce Toronto",
    "site:jobs.lever.co ServiceNow Toronto",
    "site:jobs.lever.co Salesforce Canada",
    "site:jobs.ashbyhq.com ServiceNow",
    "site:jobs.ashbyhq.com Salesforce Toronto",
    "site:jobs.smartrecruiters.com ServiceNow Canada",
    "site:jobs.smartrecruiters.com Salesforce Toronto",
    # Non-mainstream / Canadian-specific boards
    "site:jobbank.gc.ca ServiceNow Toronto",
    "site:jobbank.gc.ca Salesforce Toronto",
    "site:torontojobs.ca ServiceNow",
    "site:torontojobs.ca Salesforce",
    "site:charityvillage.com ServiceNow",
    "site:charityvillage.com Salesforce",
    "site:civicjobs.ca ServiceNow",
    "site:civicjobs.ca Salesforce",
    "site:techjobs.ca ServiceNow",
    "site:techjobs.ca Salesforce",
]

KW = re.compile(
    r"\bservice\s?now\b|\bsalesforce\b|\bapex\b|\blwc\b|\bsoql\b|\bomnistudio\b|"
    r"\bagentforce\b|\brevenue cloud\b|\bdata cloud\b|\bmarketing cloud\b|\bitsm\b|"
    r"\bitam\b|\bcmdb\b|\bitom\b|\bhrsd\b|now platform", re.I)

GEO = re.compile(
    r"toronto|\bgta\b|ontario|canada|montreal|montr[ée]al|quebec|qu[ée]bec|vancouver|"
    r"calgary|ottawa|mississauga|brampton|markham|waterloo|kitchener|hamilton|remote|"
    r"anywhere|t[ée]l[ée]travail", re.I)

EXCLUDE = re.compile(
    r"\b(account executive|account manager|sales representative|sales manager|"
    r"business development|recruiter|talent acquisition|pre-?sales)\b", re.I)

# Pages that are job boards / ATS rather than an employer marketing page.
JOBISH = re.compile(
    r"linkedin\.com/jobs|indeed\.|jobbank\.gc\.ca|adzuna\.|workopolis|jooble|"
    r"greenhouse\.io|lever\.co|ashbyhq\.com|myworkdayjobs\.com|smartrecruiters\.com|"
    r"recruitee\.com|workable\.com|bamboohr\.com|pinpointhq\.com|builtin\.com|"
    r"careerbeacon|eluta\.ca|glassdoor|torontojobs\.ca|charityvillage\.com|civicjobs\.ca|"
    r"techjobs\.ca|startupjobs\.ca|jobillico\.com|neuvoo\.com|talent\.com|ziprecruiter\.ca|"
    r"monster\.ca|simplyhired\.ca|hired\.ca|/jobs?/|job[-_]?(detail|posting|opening)", re.I)

NON_JOB = re.compile(
    r"\.(pdf|png|jpe?g|zip)$|/(blog|news|insights?|events?|webinars?|press|"
    r"products?|solutions?|about|contact|pricing)/?$", re.I)

# Search APIs return board *category* pages far more often than individual
# postings ("ServiceNow Developer Jobs in Toronto (500 Open Roles)"). Those are
# not job postings and carry no datePosted, so they are rejected here rather
# than spending a page fetch each.
INDEX_URL = re.compile(
    r"[?&](q|query|k|keyword|keywords|search|what|jobtitle)="          # search parameters
    # pagination / page-identity params: every hit is a listing view, never a
    # posting. Measured 2026-11-04 on the new non-mainstream boards — all 8
    # charityvillage hits carrying `page=`/`jobId=`/`sorting=`/`geo_location=`
    # were listing pages, while `/job/<slug>-<id>` (no query) was the posting.
    r"|[?&](page|jobid|job_id|sorting|geo_location|gclid|gad_source|sfin\d*|pg)="
    r"|/q-[^/]*jobs|/jobs-in-|/-jobs\.html"
    r"|/(jobs?|jobsearch|job-search|search|careers?|opportunities)/?$"  # listing root
    r"|linkedin\.com/jobs/(search|collections)|indeed\.[a-z.]+/(q|jobs)\b"
    r"|jooble\.org/(job|jobs)/?$|glassdoor\.[a-z.]+/Job/"
    # board-internal index/company/content pages that are not postings. A
    # posting on these boards always lives at `/job/` or `/jobposting/`
    # (singular); anything else on the host is navigation.
    r"|/company(?:ies)?/\d|/employers?(?:-list)?/?$|/author/|/blog/"
    r"|jobbank\.gc\.ca/(findajob|jobsearch/jobsearch)"
    r"|charityvillage\.com/jobs\b(?!\?)", re.I)

INDEX_TITLE = re.compile(
    r"\bjobs? in\b|\bopen roles?\b|\bnow hiring\b|\bhiring now\b|\bexplore jobs\b"
    r"|\bjob search\b|\d[\d,]*\+?\s+(open\s+)?(jobs|roles|openings|vacanc)"
    r"|^jobs?\b|\bcareers? (opportunities|openings|page)\b", re.I)

# ATS detail URLs usually carry the location as the first path segment after
# /job/ — Workday writes `/job/Toronto-ON/ServiceNow-Developer_JR100181/` and
# `/job/toronto-ontario/servicenow-developer...`. The search snippet almost never
# repeats it, so a GEO test on title+snippet alone silently drops real Toronto
# postings. Measured 2026-11-04: 5 of 5 genuinely-new ServiceNow/Toronto rows
# were rejected with "no-GEO" while their own URLs said Toronto-ON.
# Only the FIRST segment after the marker is used, and it must itself match GEO,
# so a company slug ("toronto-hydro") cannot leak a false location.
URL_LOC = re.compile(r"/(?:job|jobs|positions?|postings?|opening|openings)/([^/?#]+)", re.I)


def location_segment(url: str) -> str:
    m = URL_LOC.search(url)
    if not m:
        return ""
    return m.group(1).replace("-", " ").replace("_", " ").strip()

DATE_PATTERNS = [
    re.compile(r'"datePosted"\s*:\s*"([^"]{8,40})"'),
    re.compile(r'property=["\']article:published_time["\']\s+content=["\']([^"\']+)'),
    re.compile(r'itemprop=["\']datePosted["\']\s+content=["\']([^"\']+)'),
]

# ---------------------------------------------------------------------------
# search providers — each returns [{title, url, snippet}]


def _post(url: str, body: dict, headers: dict, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": UA, **headers})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def search_tavily(query: str, limit: int) -> list[dict]:
    keys = [k for k in (get_key("TAVILY_API_KEY"), get_key("TAVILY_API_KEY_ALT")) if k]
    for key in keys:
        try:
            data = _post("https://api.tavily.com/search",
                         {"api_key": key, "query": query, "max_results": limit,
                          "search_depth": "basic", "include_answer": False}, {})
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 402, 403, 429) and key != keys[-1]:
                continue                     # rotate to the alt key
            raise
        return [{"title": r.get("title") or "", "url": r.get("url") or "",
                 "snippet": r.get("content") or "", "source": "tavily"}
                for r in data.get("results", [])]
    return []


def search_exa(query: str, limit: int) -> list[dict]:
    key = get_key("EXA_API_KEY")
    if not key:
        return []
    data = _post("https://api.exa.ai/search",
                 {"query": query, "numResults": limit, "type": "auto"},
                 {"x-api-key": key})
    return [{"title": r.get("title") or "", "url": r.get("url") or "",
             "snippet": r.get("text") or r.get("summary") or "", "source": "exa"}
            for r in data.get("results", [])]


def search_firecrawl(query: str, limit: int) -> list[dict]:
    key = get_key("FIRECRAWL_API_KEY")
    if not key:
        return []
    data = _post("https://api.firecrawl.dev/v2/search", {"query": query, "limit": limit},
                 {"Authorization": f"Bearer {key}"})
    items = data.get("data") or []
    if isinstance(items, dict):
        items = items.get("web") or []
    return [{"title": r.get("title") or "", "url": r.get("url") or "",
             "snippet": r.get("description") or r.get("markdown") or "", "source": "firecrawl"}
            for r in items]


def search_brave(query: str, limit: int) -> list[dict]:
    key = get_key("BRAVE_SEARCH_API_KEY")
    if not key:
        return []
    req = urllib.request.Request(
        f"https://api.search.brave.com/res/v1/web/search?q={urllib.parse.quote(query)}&count={limit}",
        headers={"X-Subscription-Token": key, "Accept": "application/json", "User-Agent": UA}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return [{"title": r.get("title") or "", "url": r.get("url") or "",
             "snippet": r.get("description") or "", "source": "brave"}
            for r in data.get("web", {}).get("results", [])]


# Ordered by observed availability, not preference.  On 2026-11-04 Tavily was
# HTTP 432 (plan set-usage limit) and Exa HTTP 402 (credits exhausted), so
# trying them first would burn a run before reaching the provider that answers.
SEARCHERS = {"firecrawl": search_firecrawl, "tavily": search_tavily, "exa": search_exa, "brave": search_brave}


# ---------------------------------------------------------------------------
# page date — only what the page itself publishes


def posted_date(url: str) -> str | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                   "Accept": "text/html,*/*;q=0.8"})
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read(400_000).decode("utf-8", "replace")
    except Exception:
        return None
    for pattern in DATE_PATTERNS:
        m = pattern.search(html)
        if not m:
            continue
        raw = m.group(1).strip()
        for parse in (lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")),
                      lambda s: datetime.strptime(s[:10], "%Y-%m-%d")):
            try:
                d = parse(raw).date()
            except Exception:
                continue
            now = datetime.now(timezone.utc).date()
            if d > now + timedelta(days=1) or d < now - timedelta(days=MAX_AGE_DAYS):
                return None
            return d.isoformat()
    return None


# ---------------------------------------------------------------------------
# dedupe


def url_key(raw: str) -> str:
    try:
        u = urllib.parse.urlsplit(raw)
        host = u.netloc.lower().replace("www.", "")
        return f"{host}{u.path.rstrip('/')}".lower()
    except Exception:
        return raw.lower()


def known_urls() -> set[str]:
    known: set[str] = set()
    for path in [README, *sorted(ROOT.glob("README.BAK_*.md"))[:3], ROOT / "APPLIED.md"]:
        try:
            known.update(url_key(u) for u in re.findall(r"https?://[^\s)|]+", path.read_text(errors="replace")))
        except OSError:
            continue
    for path in INBOX.glob("*.md"):
        try:
            known.update(url_key(u) for u in re.findall(r"https?://[^\s)|]+", path.read_text(errors="replace")))
        except OSError:
            continue
    try:
        payload = json.loads((ROOT / "jobs.json").read_text())
        jobs = payload.get("jobs", payload) if isinstance(payload, (dict, list)) else []
        for j in jobs:
            if isinstance(j, dict) and j.get("url"):
                known.add(url_key(j["url"]))
    except (OSError, json.JSONDecodeError):
        pass
    return known


def split_company(title: str) -> tuple[str, str]:
    """'ServiceNow Developer at Acme' -> ('ServiceNow Developer', 'Acme')."""
    m = re.split(r"\s+(?:at|@|[-–|])\s+", title, maxsplit=1)
    if len(m) == 2 and 2 < len(m[1]) < 60:
        return m[0].strip(), m[1].strip()
    return title.strip(), "Unknown"


# ---------------------------------------------------------------------------
# inbox submission


def next_version(iso: str) -> int:
    ver = 1
    while (INBOX / f"websearch--{iso}--v{ver}.md").exists():
        ver += 1
    return ver


def build_rows(results: list[dict], known: set[str], max_fetch: int) -> tuple[list[dict], list[dict]]:
    """Split candidates into dated rows (for the feed) and undated (review only)."""
    candidates: list[dict] = []
    seen: set[str] = set()
    for item in results:
        url = (item.get("url") or "").strip()
        title = re.sub(r"\s+", " ", item.get("title") or "").strip()
        snippet = re.sub(r"\s+", " ", item.get("snippet") or "").strip()
        if not url or not title or NON_JOB.search(url):
            continue
        if not JOBISH.search(url):
            continue
        if INDEX_URL.search(url) or INDEX_TITLE.search(title):
            continue                                    # board category page, not a posting
        hay = f"{title} {snippet}"
        if EXCLUDE.search(title) or not KW.search(hay):
            continue
        # GEO: title/snippet first, then the ATS URL's own location segment.
        loc = location_segment(url)
        if not GEO.search(hay) and not (loc and GEO.search(loc)):
            continue
        key = url_key(url)
        if key in known or key in seen:
            continue
        seen.add(key)
        role, company = split_company(title)
        candidates.append({"title": role, "company": company, "url": url,
                           "snippet": snippet[:200], "source": item.get("source", "")})

    dated: list[dict] = []
    undated: list[dict] = []
    with futures.ThreadPoolExecutor(max_workers=4) as ex:
        dates = list(ex.map(lambda c: posted_date(c["url"]), candidates[:max_fetch]))
    for cand, date in zip(candidates, dates):
        cand["posted"] = date
        (dated if date else undated).append(cand)
    for cand in candidates[max_fetch:]:
        cand["posted"] = None
        undated.append(cand)
    return dated, undated


def write_submission(dated: list[dict], undated: list[dict], iso: str) -> Path | None:
    rows = dated + undated
    if not rows:
        return None
    INBOX.mkdir(parents=True, exist_ok=True)
    target = INBOX / f"websearch--{iso}--v{next_version(iso)}.md"
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "---",
        "model: websearch",
        f"scanned_at: {stamp}",
        "task: exa-tavily-firecrawl-search",
        "---",
        "",
        f"# Web-search scan — {iso}",
        "",
        "Dated rows come from a `datePosted` / `article:published_time` the page itself",
        "publishes. Everything else keeps an em dash: the merger skips undated rows, so",
        "no row here can invent a posting date.",
        "",
        "| Posted | Role | Company | Location | Source |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        title = r["title"].replace("|", "/")
        lines.append(
            f"| {r['posted'] or '—'} | [{title}]({r['url']}) | {r['company'].replace('|', '/')} "
            f"| Not specified | via {r['source']} web search |"
        )
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return target


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--provider", choices=sorted(SEARCHERS), help="single search provider")
    ap.add_argument("--max-queries", type=int, default=len(QUERIES))
    ap.add_argument("--max-fetch", type=int, default=24, help="cap page fetches for dates")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    providers = [args.provider] if args.provider else list(SEARCHERS)
    live = [p for p in providers if get_key({"tavily": "TAVILY_API_KEY",
                                             "exa": "EXA_API_KEY",
                                             "firecrawl": "FIRECRAWL_API_KEY",
                                             "brave": "BRAVE_SEARCH_API_KEY"}[p])]
    if not live:
        print("no search API key found (TAVILY_API_KEY / EXA_API_KEY / FIRECRAWL_API_KEY) "
              "— web search skipped")
        return 0

    queries = QUERIES[: args.max_queries]
    results: list[dict] = []
    for provider in live:
        dead = False
        for query in queries:
            if dead:
                break
            try:
                found = SEARCHERS[provider](query, 10)
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", "replace")[:120].replace("\n", " ")
                print(f"[websearch:{provider}] HTTP {exc.code} {detail}")
                # 429 is a *rate* limit, not a plan limit: the provider is still
                # usable next run and the query list is worth finishing on a
                # slower path, but mid-run it carries no recovery. Stop, keep
                # what this provider already returned.
                dead = True
                break
            except Exception as exc:                       # noqa: BLE001
                print(f"[websearch:{provider}] {type(exc).__name__}: {str(exc)[:100]}")
                dead = True
                break
            results.extend(found)
            print(f"[websearch:{provider}] '{query}' -> {len(found)} results")
            if provider == "firecrawl" and len(found):
                time.sleep(6)      # free/entry plan caps at 11 req/min

    known = known_urls()
    dated, undated = build_rows(results, known, args.max_fetch)
    print(f"[websearch] {len(results)} raw results -> {len(dated)} dated, {len(undated)} undated "
          f"after keyword/geo/dedupe filters")

    if args.dry_run:
        for r in (dated + undated)[:15]:
            print(f"  {'DATED ' + r['posted'] if r['posted'] else 'undated':<18} {r['title'][:58]}")
        return 0

    target = write_submission(dated, undated, datetime.now(timezone.utc).date().isoformat())
    if target:
        print(f"[websearch] wrote {target.relative_to(ROOT)} "
              f"(+{len(dated)} dated, {len(undated)} undated)")
        RAW.mkdir(parents=True, exist_ok=True)
        (RAW / "websearch_last.json").write_text(
            json.dumps({"dated": dated, "undated": undated}, indent=2), encoding="utf-8")
    else:
        print("[websearch] nothing new")
    return 0


if __name__ == "__main__":
    sys.exit(main())
