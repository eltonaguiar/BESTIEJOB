#!/usr/bin/env python3
"""Discover *new* employer ATS boards, so the sweep isn't limited to boards we
already stumbled onto.

The aggregators only index what they index. The way around that is to search the
ATS hosts themselves: an `jobs.ashbyhq.com/<board>` or `boards.greenhouse.io/
<token>` URL names the employer's board token directly, and that token is the
key to the dated public feed.

Queries are host-scoped and platform-scoped, so every hit is a real requisition
on a real employer board rather than a job-board listing page. Slugs are written
to `raw/ats_boards_extra.json`, which `ats_board_sweep.py` merges into its
registry. Nothing here invents a date -- this step only finds boards.

Usage
    python3 scripts/ats_discover.py                # all queries
    python3 scripts/ats_discover.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from ai_panel import get_key  # noqa: E402

RAW = ROOT / "raw"
OUT = RAW / "ats_boards_extra.json"

# One query per host family. "servicenow" + "salesforce" is the whole board
# remit, and the geography terms keep results Canadian-relevant without
# excluding remote-Canada postings.
PLATFORM = '("servicenow" OR "salesforce")'
GEO = '(canada OR toronto OR ontario OR vancouver OR montreal OR calgary OR "remote, canada")'

QUERIES: list[tuple[str, str]] = [
    ("ashby", f'site:jobs.ashbyhq.com {PLATFORM} {GEO}'),
    ("greenhouse", f'site:boards.greenhouse.io {PLATFORM} {GEO}'),
    ("lever", f'site:jobs.lever.co {PLATFORM} {GEO}'),
    ("workable", f'site:apply.workable.com {PLATFORM} {GEO}'),
    ("recruitee", f'site:recruitee.com {PLATFORM} {GEO}'),
    ("teamtailor", f'site:teamtailor.com {PLATFORM} {GEO}'),
    ("breezy", f'site:breezy.hr {PLATFORM} {GEO}'),
    ("pinpoint", f'site:pinpointhq.com {PLATFORM} {GEO}'),
    ("gem", f'site:jobs.gem.com {PLATFORM} {GEO}'),
    ("polymer", f'site:jobs.polymer.co {PLATFORM} {GEO}'),
    ("smartrecruiters", f'site:jobs.smartrecruiters.com {PLATFORM} {GEO}'),
    ("workday", f'site:myworkdayjobs.com {PLATFORM} "Toronto" OR "Canada"'),
    ("bamboohr", f'site:bamboohr.com/careers {PLATFORM} {GEO}'),
    ("jobvite", f'site:jobs.jobvite.com {PLATFORM} {GEO}'),
]

# A platform keyword plus a continent-wide geography term returns whichever
# boards rank best globally, not the Canadian ones. Anchoring on a single city
# makes the search engine answer the question that matters: which employers in
# THIS city run THIS ATS. These are appended to the query set.
CITY_ANCHOR = [
    ("ashby", 'site:jobs.ashbyhq.com "Toronto" (servicenow OR salesforce OR ITSM)'),
    ("ashby", 'site:jobs.ashbyhq.com "Vancouver" OR "Calgary" OR "Montreal" (servicenow OR salesforce)'),
    ("greenhouse", 'site:boards.greenhouse.io "Toronto" OR "Vancouver" (servicenow OR salesforce)'),
    ("lever", 'site:jobs.lever.co "Toronto" OR "Vancouver" (servicenow OR salesforce)'),
    ("workable", 'site:apply.workable.com "Toronto" OR "Vancouver" OR "Montreal" (servicenow OR salesforce)'),
    ("recruitee", 'site:recruitee.com "Toronto" OR "Vancouver" OR "Montreal" (servicenow OR salesforce)'),
    ("teamtailor", 'site:teamtailor.com "Toronto" OR "Vancouver" (servicenow OR salesforce)'),
    ("breezy", 'site:breezy.hr "Toronto" OR "Vancouver" (servicenow OR salesforce)'),
    ("gem", 'site:jobs.gem.com "Toronto" OR "Canada" (servicenow OR salesforce)'),
    ("workday", 'site:myworkdayjobs.com "Toronto, ON" (servicenow OR salesforce)'),
]

EXTRACT = {
    "ashby": re.compile(r"jobs\.ashbyhq\.com/([a-z0-9][a-z0-9-]{1,40})", re.I),
    "greenhouse": re.compile(r"boards\.greenhouse\.io/([a-z0-9][a-z0-9_-]{1,40})", re.I),
    "lever": re.compile(r"jobs\.lever\.co/([a-z0-9][a-z0-9-]{1,40})", re.I),
    "workable": re.compile(r"apply\.workable\.com/([a-z0-9][a-z0-9-]{1,40})", re.I),
    "recruitee": re.compile(r"([a-z0-9][a-z0-9-]{1,40})\.recruitee\.com", re.I),
    "teamtailor": re.compile(r"([a-z0-9][a-z0-9-]{1,40})\.teamtailor\.com", re.I),
    "breezy": re.compile(r"([a-z0-9][a-z0-9-]{1,40})\.breezy\.hr", re.I),
    "pinpoint": re.compile(r"([a-z0-9][a-z0-9-]{1,40})\.pinpointhq\.com", re.I),
    "gem": re.compile(r"jobs\.gem\.com/([a-z0-9][a-z0-9-]{1,40})", re.I),
    "polymer": re.compile(r"jobs\.polymer\.co/([a-z0-9][a-z0-9-]{1,40})", re.I),
    "smartrecruiters": re.compile(r"(?:jobs|careers)\.smartrecruiters\.com/([a-z0-9][a-z0-9-]{1,40})", re.I),
    "workday": re.compile(r"([a-z0-9-]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([A-Za-z0-9_-]+)", re.I),
    "bamboohr": re.compile(r"([a-z0-9][a-z0-9-]{1,40})\.bamboohr\.com", re.I),
    "jobvite": re.compile(r"jobs\.jobvite\.com/([a-z0-9][a-z0-9-]{1,40})", re.I),
}

# Host subdomains that are the platform, not an employer.
NOT_AN_EMPLOYER = {
    "www", "api", "app", "jobs", "boards", "careers", "apply", "help", "support",
    "static", "cdn", "assets", "blog", "docs", "status", "login", "signup",
    "resources", "hire", "en", "fr", "go", "my", "secure", "portal",
}


def _post(url: str, body: dict, headers: dict | None = None, timeout: int = 45) -> dict:
    req = urllib.request.Request(
        url, data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def tavily(query: str, key: str, max_results: int = 40) -> list[str]:
    data = _post("https://api.tavily.com/search",
                 {"api_key": key, "query": query, "max_results": max_results,
                  "search_depth": "advanced", "include_answer": False})
    return [x.get("url") for x in (data.get("results") or []) if x.get("url")]


def exa(query: str, key: str, max_results: int = 40) -> list[str]:
    data = _post("https://api.exa.ai/search",
                 {"query": query, "numResults": min(max_results, 100), "type": "auto"},
                 {"x-api-key": key})
    return [x.get("url") for x in (data.get("results") or []) if x.get("url")]


def firecrawl(query: str, key: str, max_results: int = 40) -> list[str]:
    data = _post("https://api.firecrawl.dev/v2/search",
                 {"query": query, "limit": min(max_results, 100)},
                 {"Authorization": f"Bearer {key}"})
    items = data.get("data") or []
    if isinstance(items, dict):
        items = items.get("web") or []
    return [x.get("url") for x in items if isinstance(x, dict) and x.get("url")]


# Provider pool. Tavily's 432 is "plan limit reached" (both keys carry separate
# quotas and both hit it), so discovery used to stop dead and report it as a
# transient throttle. Rotating across three providers means one exhausted plan
# no longer ends the pass -- which is what "205 of the tokens" actually was.
POOL = (("tavily", "TAVILY_API_KEY", tavily),
        ("tavily-alt", "TAVILY_API_KEY_ALT", tavily),
        ("exa", "EXA_API_KEY", exa),
        ("firecrawl", "FIRECRAWL_API_KEY", firecrawl))

# A 401/402/403/429/432 means this credential is not usable right now; further
# calls only burn time. Anything else (timeout, malformed body) is worth
# retrying on the next query.
FATAL = {401, 402, 403, 429, 432}


def search(query: str, dead: set[str], max_results: int = 40) -> tuple[list[str], str]:
    last = "no provider"
    for name, env, fn in POOL:
        if name in dead:
            continue
        key = get_key(env)
        if not key:
            dead.add(name)
            continue
        try:
            return fn(query, key, max_results), name
        except Exception as exc:                            # noqa: BLE001
            code = getattr(exc, "code", None)
            last = f"{name}:{type(exc).__name__}{code or ''}"
            if code in FATAL:
                dead.add(name)
    return [], last


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--max-queries", type=int, default=len(QUERIES) + len(CITY_ANCHOR))
    args = ap.parse_args()

    known = json.loads(OUT.read_text()) if OUT.exists() else {}
    found: dict[str, set[str]] = {k: set(v) for k, v in known.items()}
    dead: set[str] = set()

    for route, query in (QUERIES + CITY_ANCHOR)[:args.max_queries]:
        urls, provider = search(query, dead)
        if not urls:
            print(f"[{route:16}] no results ({provider})")
            continue
        pat = EXTRACT[route]
        before = len(found.get(route, set()))
        for url in urls:
            for m in pat.finditer(url):
                slug = (".".join(m.groups()) if len(m.groups()) > 1 else m.group(1)).lower()
                head = slug.split(".")[0]
                if head in NOT_AN_EMPLOYER or len(head) < 2:
                    continue
                found.setdefault(route, set()).add(slug)
        gained = len(found.get(route, set())) - before
        print(f"[{route:16}] {provider:10} {len(urls):3} urls -> +{gained} new "
              f"(total {len(found.get(route, set()))})")
    if dead:
        print(f"providers exhausted: {', '.join(sorted(dead))}")

    payload = {k: sorted(v) for k, v in found.items() if v}
    if args.dry_run:
        print(json.dumps(payload, indent=1))
        return 0
    RAW.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")
    total = sum(len(v) for v in payload.values())
    print(f"\nwrote {OUT.relative_to(ROOT)}: {total} board tokens")
    return 0


if __name__ == "__main__":
    sys.exit(main())
