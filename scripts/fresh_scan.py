#!/usr/bin/env python3
"""Freshness-first scan: ServiceNow and Salesforce first, then "Other" jobs
shaped like the ones already in BESTIEJOB's Other tab.

Differences from scripts/bucket_rounds.py (which does fixed 30-todo sets):
  * every board in scripts/ats_board_sweep.py is a round, not just 30 seeds;
  * family is assigned by tools/jobs_consolidate.py:classify() -- the exact
    function the site uses to sort jobs into ServiceNow / Salesforce / Other --
    so a row can never land in two buckets or contradict the page;
  * a posting must be dated within --days to count as fresh, and undated
    postings are reported separately instead of being treated as new;
  * "Other" requires a Business-Analyst / Data-Analyst / project-coordinator
    style title, because classify() sends everything unclassified to Other and
    that would otherwise pull in the whole board.

    python3 scripts/fresh_scan.py --family servicenow --days 21
    python3 scripts/fresh_scan.py --family all --days 7

Writes reports/fresh_<family>_<date>.{json,md}
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Reuse the round driver's loaders, liveness probe and URL normaliser.
_s = importlib.util.spec_from_file_location("br", ROOT / "scripts" / "bucket_rounds.py")
br = importlib.util.module_from_spec(_s)
_s.loader.exec_module(br)

# Same classifier the live page uses -- single source of truth for family.
_s2 = importlib.util.spec_from_file_location("jc", ROOT / "tools" / "jobs_consolidate.py")
jc = importlib.util.module_from_spec(_s2)
_s2.loader.exec_module(jc)

NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y-%m-%d")
OUT = ROOT / "reports"

RELEVANT = {
    "servicenow": br.KW["servicenow"],
    "salesforce": br.KW["salesforce"],
    # Title shapes that dominate the page's current Other tab: business
    # analyst, data analyst, business systems analyst, project coordinator.
    "other": re.compile(
        r"business (systems? )?analyst|\bbusiness process analyst\b|\bsystems? analyst\b|"
        r"\bdata analyst\b|\breporting analyst\b|\banalytics? analyst\b|"
        r"\bbusiness intelligence\b|\bproject coordinator\b|\bit project manager\b|"
        r"\bproject manager\b|\bscrum master\b|\bproduct owner\b|\bqa analyst\b|"
        r"\bdata engineer\b|\bdata scientist\b|\bbi developer\b|\bsql\b|\btableau\b|"
        r"\bpower ?bi\b|\bpython\b|\btechnical analyst\b|\bapplication analyst\b",
        re.I,
    ),
}
SEARCH_TERM = {"servicenow": "servicenow", "salesforce": "salesforce",
               "other": "business analyst"}


def rounds_for(family: str) -> list[tuple[str, str, str]]:
    """(route, label, search) for every board in the inventory."""
    out = []
    for label in br.WD:
        out.append(("workday", label, SEARCH_TERM[family]))
    for route, table in (("greenhouse", br.GH), ("lever", br.LV), ("ashby", br.AB),
                         ("smartrecruiters", br.SR), ("workable", br.WK)):
        for label in table:
            out.append((route, label, None))
    return out


def fetch(route: str, label: str, search: str | None) -> list[dict]:
    if route == "workday":
        return br.workday_search(label, search or "data")
    table = {"greenhouse": br.GH, "lever": br.LV, "ashby": br.AB,
             "smartrecruiters": br.SR, "workable": br.WK}[route]
    fn = {"greenhouse": br.ats.from_greenhouse, "lever": br.ats.from_lever,
          "ashby": br.ats.from_ashby, "smartrecruiters": br.ats.from_smartrecruiters,
          "workable": br.ats.from_workable}[route]
    return fn(table[label])


def parse_day(s: str | None) -> date | None:
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%b %d, %Y", "%d %b %Y"):
        try:
            return datetime.strptime(s.strip()[:11].strip(), fmt).date()
        except ValueError:
            continue
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    return date(int(m[1]), int(m[2]), int(m[3])) if m else None


def run(family: str, days: int, verify: bool, workers: int) -> dict:
    cutoff = NOW.date() - timedelta(days=days)
    known = br.load_known()
    relevant = RELEVANT[family]
    seen: set[str] = set()
    results, t0 = [], time.time()
    todos = rounds_for(family)

    for i, (route, label, search) in enumerate(todos, 1):
        r0 = time.time()
        try:
            postings, err = fetch(route, label, search), None
        except Exception as exc:
            postings, err = [], f"{type(exc).__name__}: {str(exc)[:70]}"

        fresh, undated = [], 0
        for p in postings:
            title = p.get("title") or ""
            loc = p.get("location") or ""
            if not relevant.search(title):
                continue
            if jc.classify(title, p.get("url") or "", loc) != family:
                continue
            if not br.ats.is_canadian(loc, p.get("url") or ""):
                continue
            d = parse_day(p.get("posted"))
            if d is None:
                undated += 1
                continue
            if d < cutoff:
                continue
            fresh.append(p)

        uniq = []
        for p in fresh:
            k = br.norm_url(p.get("url") or "")
            if not k or k in seen:
                continue
            seen.add(k)
            uniq.append(p)

        live_rows, new_rows = [], []
        if verify and uniq:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                for r, (ok, code) in zip(uniq, ex.map(lambda r: br.live(r["url"]), uniq[:40])):
                    r["http_status"] = code
                    if ok:
                        live_rows.append(r)
                        if br.norm_url(r["url"]) not in known:
                            new_rows.append(r)
        else:
            live_rows = uniq

        results.append({
            "round": i, "target": label, "route": route,
            "fetched": len(postings), "fresh": len(fresh), "undated": undated,
            "live": len(live_rows), "new": len(new_rows), "error": err,
            "secs": round(time.time() - r0, 1), "jobs": live_rows,
        })
        print(f"[{family} {i:03d}/{len(todos)}] {label[:24]:24s} {route[:6]:6s} "
              f"got={len(postings):3d} fresh={len(fresh):2d} live={len(live_rows):2d} "
              f"new={len(new_rows):2d} {results[-1]['secs']}s"
              f"{(' ERR ' + err) if err else ''}", flush=True)

    OUT.mkdir(exist_ok=True)
    totals = {
        "boards": len(todos),
        "fetched": sum(r["fetched"] for r in results),
        "fresh": sum(r["fresh"] for r in results),
        "undated": sum(r["undated"] for r in results),
        "live": sum(r["live"] for r in results),
        "new": sum(r["new"] for r in results),
        "errors": sum(1 for r in results if r["error"]),
        "secs": round(time.time() - t0, 1),
    }
    payload = {"family": family, "generated": NOW.isoformat(), "fresh_days": days,
               "cutoff": cutoff.isoformat(), "verify_liveness": verify,
               "totals": totals, "rounds": results}
    (OUT / f"fresh_{family}_{STAMP}.json").write_text(json.dumps(payload, indent=1))

    # Net-new is recomputed against jobs.json; per-round "new" is only a count.
    rows, seen3 = [], set()
    for r in results:
        for j in r["jobs"]:
            k = br.norm_url(j["url"])
            if k and k not in seen3:
                seen3.add(k)
                rows.append(j)
    net_new = [j for j in rows if br.norm_url(j["url"]) not in known]
    net_new.sort(key=lambda j: j.get("posted") or "", reverse=True)

    week = [j for j in net_new if (parse_day(j.get("posted")) or cutoff) > NOW.date() - timedelta(days=7)]
    L = [f"# Fresh {family.upper()} scan — postings ≤ {days} days old — {STAMP}", "",
         f"{len(todos)} board rounds · cutoff {cutoff} · liveness verified: "
         f"**{'yes' if verify else 'no'}** · generated {NOW.strftime('%H:%M UTC')}", "",
         "| Metric | Count |", "|---|---:|",
         f"| Boards queried | {totals['boards']} |",
         f"| Postings fetched | {totals['fetched']} |",
         f"| Relevant title + correct family + Canadian | {totals['fresh']} |",
         f"| Live-verified (HTTP 2xx/3xx) | {totals['live']} |",
         f"| Net-new vs jobs.json | **{len(net_new)}** |",
         f"| Net-new posted in last 7 days | **{len(week)}** |",
         f"| Undated (excluded from freshness) | {totals['undated']} |",
         f"| Board errors | {totals['errors']} |", "",
         f"## {len(net_new)} net-new fresh {family} job(s)", ""]
    if net_new:
        L += ["| Posted | Title | Company | Location | HTTP |", "|---|---|---|---|---|"]
        for j in net_new:
            L.append(f"| {j.get('posted') or '—'} | [{j['title']}]({j['url']}) | {j['company']} | "
                     f"{(j.get('location') or '—')[:38]} | {j.get('http_status','—')} |")
    else:
        L.append("_Nothing net-new inside the freshness window._")
    L += ["", "## Per-board detail", "",
          "| # | Board | Route | Fetched | Fresh | Live | New | Err |", "|---|---|---|---:|---:|---:|---:|---|"]
    for r in results:
        if r["fetched"]:
            L.append(f"| {r['round']} | {r['target']} | {r['route']} | {r['fetched']} | "
                     f"{r['fresh']} | {r['live']} | {r['new']} | {r['error'] or ''} |")
    (OUT / f"fresh_{family}_{STAMP}.md").write_text("\n".join(L))
    print(f"\n[{family}] {totals} net_new={len(net_new)} last7d={len(week)}", flush=True)
    return payload


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True,
                    choices=["servicenow", "salesforce", "other", "all"])
    ap.add_argument("--days", type=int, default=21)
    ap.add_argument("--verify", type=int, default=1)
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()
    fams = ["servicenow", "salesforce", "other"] if a.family == "all" else [a.family]
    for f in fams:
        run(f, a.days, bool(a.verify), a.workers)
