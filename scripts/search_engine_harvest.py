#!/usr/bin/env python3
"""search_engine_harvest.py — turn working search engines into inbox rows.

`search_engines.py probe` answers *which* engines this box can read. Measured on
2026-11-11 with the query "servicenow developer toronto jobs":

    duckduckgo   200, usable (10 hits, 2 postings, 8 listing hubs)
    bing         200, usable (redirect-decode required)
    openrouter   200, usable (perplexity/sonar, grounded, returns dates)
    mojeek       captcha shell
    marginalia   redirects, no results for this query
    searx.be     antibot captcha
    startpage 200 but zero results
    ecosia/qwant 403
    brave        token rejected (422/0)
    perplexity / kagi   no key

This stage spends those engines on `site:`-scoped ATS queries, because a bare
keyword query describes a listing page and engines answer it with listing pages.
Every candidate is then fetched once and must supply, from its own markup:

  * `datePosted` (or article:published_time / microdata) — an absolute date in the
    window, never a relative age and never the scan clock;
  * a location naming Canada — a posting whose page does not say Canada is not
    added, however Canadian the query was;
  * a hiring organisation, for the Company column.

Anything missing is dropped and counted, not guessed. Output is an inbox table
plus a JSON report; nothing is written to the README here.

Usage
    python3 scripts/search_engine_harvest.py
    python3 scripts/search_engine_harvest.py --engines duckduckgo,bing,openrouter --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
from search_engines import ENGINES, JOBISH, LISTING, _get, _text      # noqa: E402
from ats_date_resolve import resolve as ats_date                       # noqa: E402
from board_invariants import normalise_url, parse_readme               # noqa: E402
from locscope import is_canadian                                       # noqa: E402

MAX_AGE = 31
TODAY = datetime.now(timezone.utc).date()

QUERIES = [
    "site:myworkdayjobs.com ServiceNow Toronto",
    "site:myworkdayjobs.com Salesforce Toronto",
    "site:jobs.lever.co ServiceNow Toronto",
    "site:jobs.lever.co Salesforce Canada",
    "site:boards.greenhouse.io Salesforce Toronto",
    "site:jobs.ashbyhq.com ServiceNow Canada",
    "site:jobs.smartrecruiters.com ServiceNow Canada",
    "site:careers.servicenow.com Canada",
]

DATE_PATTERNS = [
    re.compile(r'"datePosted"\s*:\s*"([^"]{8,40})"'),
    re.compile(r'property=["\']article:published_time["\']\s*content=["\']([^"\']+)'),
    re.compile(r'itemprop=["\']datePosted["\']\s*content=["\']([^"\']+)'),
    re.compile(r'content=["\']([^"\']+)["\']\s*property=["\']article:published_time["\']'),
]
COUNTRY = re.compile(r'"addressCountry"\s*:\s*"([^"]+)"')
LOCALITY = re.compile(r'"addressLocality"\s*:\s*"([^"]+)"')
REGION = re.compile(r'"addressRegion"\s*:\s*"([^"]+)"')
ORG = re.compile(r'"hiringOrganization"\s*:\s*\{[^}]*?"name"\s*:\s*"([^"]+)"', re.S)
TITLE = re.compile(r'<title[^>]*>(.*?)</title>', re.S | re.I)
CLOSED = re.compile(r"(no longer accepting|position (has been )?(filled|closed)|"
                    r"job (is )?(no longer|not) available|application period has closed)", re.I)


def facts(url: str) -> dict:
    """Everything this script is allowed to believe, read from one page fetch."""
    status, html = _get(url)
    out = {"status": status, "posted": None, "location": "", "company": "",
           "title": "", "closed": bool(CLOSED.search(html)) if html else False}
    if status != 200 or not html:
        return out
    if CLOSED.search(html):
        return out
    for pattern in DATE_PATTERNS:
        m = pattern.search(html)
        if not m:
            continue
        raw = m.group(1).strip()
        for parse in (lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")).date(),
                      lambda s: datetime.strptime(s[:10], "%Y-%m-%d").date(),
                      lambda s: datetime.strptime(s, "%m/%d/%Y").date(),
                      lambda s: datetime.strptime(s, "%B %d, %Y").date()):
            try:
                d = parse(raw)
            except (ValueError, TypeError):
                continue
            if TODAY - timedelta(days=MAX_AGE) <= d <= TODAY + timedelta(days=1):
                out["posted"] = d.isoformat()
            break
        if out["posted"]:
            break
    parts = [m.group(1).strip() for m in (LOCALITY.search(html), REGION.search(html),
                                          COUNTRY.search(html)) if m]
    if parts:
        out["location"] = ", ".join(dict.fromkeys(parts))
    else:
        # Fall back to the location segment of the URL, which the ATS writes
        # itself ("/job/Toronto-ON/..."): still the posting's own data, never the
        # search scope.
        seg = re.search(r"/(?:job|jobs|positions|postings)/([^/?#]+)", url, re.I)
        if seg:
            out["location"] = seg.group(1).replace("-", " ").replace("_", " ").strip()
    m = ORG.search(html)
    out["company"] = _text(m.group(1)) if m else ""
    m = TITLE.search(html)
    out["title"] = _text(m.group(1)) if m else ""
    return out


def known_urls() -> set[str]:
    rows, _ = parse_readme(ROOT / "README.md")
    keys = {normalise_url(r["url"]) for r in rows}
    feed = ROOT / "jobs.json"
    if feed.exists():
        for j in json.loads(feed.read_text(encoding="utf-8")).get("jobs", []):
            keys.add(normalise_url(j.get("url", "")))
    return keys


def harvest(engines: list[str], queries: list[str], limit: int) -> dict:
    known = known_urls()
    seen: set[str] = set()
    candidates: list[dict] = []
    per_engine: dict[str, int] = {}
    for name in engines:
        for query in queries:
            try:
                status, rows = ENGINES[name](query, limit)
            except Exception:                              # noqa: BLE001
                continue
            per_engine[name] = per_engine.get(name, 0) + (len(rows) if status == 200 else 0)
            for r in rows:
                url = (r.get("url") or "").strip()
                if not url.startswith("http") or LISTING.search(url):
                    continue
                key = normalise_url(url)
                if key in known or key in seen:
                    continue
                if not JOBISH.search(f"{r.get('title','')} {r.get('snippet','')} {url}"):
                    continue
                seen.add(key)
                candidates.append({**r, "query": query})

    kept, dropped = [], {}
    for cand in candidates:
        info = facts(cand["url"])
        reason = None
        if info["status"] != 200:
            reason = f"http-{info['status'] or 'error'}"
        elif info["closed"]:
            reason = "posting-closed"
        elif not info["posted"]:
            reason = "no-absolute-date"
        elif not info["location"]:
            reason = "no-location-on-posting"
        elif not is_canadian(info["location"]):
            reason = "posting-not-canadian"
        elif not info["company"]:
            reason = "no-employer-named"
        if reason:
            dropped[reason] = dropped.get(reason, 0) + 1
            continue
        kept.append({"posted": info["posted"], "title": (info["title"] or cand["title"]).replace("|", "/"),
                     "company": info["company"].replace("|", "/"), "location": info["location"],
                     "url": cand["url"], "engine": cand["engine"], "query": cand["query"]})
    ats = sum(1 for k in kept if ats_date(k["url"]))
    return {"engines": engines, "queries": queries, "perEngineResults": per_engine,
            "candidates": len(candidates), "kept": kept, "dropped": dropped,
            "resolvedByAtsJson": ats}


def write_inbox(rows: list[dict], path: Path) -> None:
    rows = sorted(rows, key=lambda r: (r["posted"], r["company"]), reverse=True)
    lines = ["# Search-engine harvest — " + TODAY.isoformat(), "",
             f"notes: {len(rows)} rows from "
             + ", ".join(sorted({r['engine'] for r in rows}))
             + ". Posted date and location read from each posting's own markup.",
             "", "| Posted | Role | Company | Location | Source |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['posted']} | [{r['title']}]({r['url']}) | {r['company']} | "
                     f"{r['location']} | via {r['engine']} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--engines", default="duckduckgo,bing,openrouter")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    engines = [e.strip() for e in args.engines.split(",") if e.strip()]
    unknown = [e for e in engines if e not in ENGINES]
    if unknown:
        sys.exit(f"unknown engines {unknown}; have {sorted(ENGINES)}")

    result = harvest(engines, QUERIES, args.limit)
    print(f"engines: {result['engines']}")
    print(f"engine results: {result['perEngineResults']}")
    print(f"candidates after listing/keyword filter: {result['candidates']}")
    print(f"kept (date + Canadian location + employer, all from the posting): {len(result['kept'])}")
    print(f"dropped: {result['dropped']}")
    for r in result["kept"][:12]:
        print(f"  {r['posted']} | {r['company'][:24]:24} | {r['location'][:26]:26} | "
              f"{r['title'][:40]:40} | {r['engine']}")
    if args.dry_run:
        return 0

    stamp = "v1"
    inbox = Path(args.out) if args.out else ROOT / "inbox" / f"search-engines--{TODAY}--{stamp}.md"
    write_inbox(result["kept"], inbox)
    report = ROOT / "reports" / f"search_engines_{TODAY}.json"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps({"generatedAt": datetime.now(timezone.utc).isoformat(), **result},
                                 indent=1), encoding="utf-8")
    print(f"\ninbox: {inbox}\nreport: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
