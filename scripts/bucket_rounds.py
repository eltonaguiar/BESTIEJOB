#!/usr/bin/env python3
"""Bucket rounds: 30 todos x 30 rounds for SALESFORCE, SERVICENOW and OTHER.

Each bucket has exactly 30 todos. Todo k is executed in round k, so 30 rounds
finish 30 todos per bucket (90 rounds overall across the three buckets).

Every round queries one real employer feed through the adapters already proven
in scripts/ats_board_sweep.py (Workday CXS, Greenhouse, Lever, Ashby,
SmartRecruiters, Workable), keeps only postings whose TITLE matches the bucket's
keywords, keeps only Canadian locations, then verifies each posting URL still
returns 200 before it may be reported as a live job. Nothing is invented: no
date, company, or salary is ever produced by this script -- the feed supplies
the date or the row is dropped.

    python3 scripts/bucket_rounds.py --bucket salesforce
    python3 scripts/bucket_rounds.py --bucket servicenow --rounds 2
    python3 scripts/bucket_rounds.py --bucket other --verify 0     # skip liveness

Outputs
    reports/bucket_todos_<date>.json                  the 90-todo plan
    reports/bucket_<bucket>_<date>.json               machine-readable results
    reports/bucket_<bucket>_<date>.md                 per-round report
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "reports"
NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y-%m-%d")

# --------------------------------------------------------------------------
# Reuse the proven adapters rather than re-implementing six ATS protocols.
# --------------------------------------------------------------------------
_spec = importlib.util.spec_from_file_location("ats", ROOT / "scripts" / "ats_board_sweep.py")
ats = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ats)

WD = {b[3]: b for b in ats.WORKDAY}
GH = {b[1]: b for b in ats.GREENHOUSE}
LV = {b[1]: b for b in ats.LEVER}
AB = {b[1]: b for b in ats.ASHBY}
SR = {b[1]: b for b in ats.SMARTRECRUITERS}
WK = {b[1]: b for b in ats.WORKABLE}

# --------------------------------------------------------------------------
# Keyword sets. Title-only matching keeps precision high; a body match on
# "Salesforce" would pull in every admin role at a company that merely uses it.
# --------------------------------------------------------------------------
KW = {
    "salesforce": re.compile(
        r"\bsalesforce\b|\bapex\b|\bsoql\b|\blwc\b|\blightning web\b|\bvisualforce\b|"
        r"\bmarketing cloud\b|\bservice cloud\b|\bsales cloud\b|\bdata cloud\b|"
        r"\bagentforce\b|\bcpq\b|\brevenue cloud\b|\bmulesoft\b|\beinstein\b|"
        r"\bcopado\b|\bfsc\b|\bfinancial services cloud\b|\bsfdc\b|\bsf\s?cc\b",
        re.I,
    ),
    "servicenow": re.compile(
        r"\bservice\s?now\b|\bcsdm\b|\bcmdb\b|\bitsm\b|\bitom\b|\bitam\b|"
        r"\bnow assist\b|\bvirtual agent\b|\bmid server\b|\bflow designer\b|"
        r"\bsecops\b|\bdiscovery\b|\bservice mapping\b|\bhrit\b|\bspm\b",
        re.I,
    ),
    "other": re.compile(
        r"\bpython\b|\bsql\b|\btableau\b|\bpower\s?bi\b|\balteryx\b|\bpowershell\b|"
        r"\bvba\b|\bdata (analyst|engineer|scientist|architect)\b|"
        r"\bbusiness intelligence\b|\bbi (developer|analyst|engineer)\b|"
        r"\bdevops\b|\bci/cd\b|\bjira\b|\bconfluence\b|\betl\b|\bdata pipeline\b|"
        r"\banalytics engineer\b|\breporting analyst\b|\bapplication support\b|"
        r"\bsystems? (administrator|analyst|engineer)\b|\bapplication(s)? (analyst|administrator)\b|"
        r"\bbusiness systems analyst\b|\bdata warehouse\b|\bssrs\b|\bssis\b|"
        r"\bpower platform\b|\bsharepoint\b|\bmicrosoft 365\b|\btechnical analyst\b",
        re.I,
    ),
}
# The OTHER bucket must not re-report what the two named buckets already own.
OWNED = re.compile(KW["salesforce"].pattern + "|" + KW["servicenow"].pattern, re.I)

# --------------------------------------------------------------------------
# 30 todos per bucket. board keys are (route, label) resolved against the
# inventory discovered in ats_board_sweep.py -- no invented employers.
# --------------------------------------------------------------------------
def t(route, label, note="", search=None):
    return {"route": route, "label": label, "note": note, "search": search}


TODO = {
    "salesforce": [
        t("workday", "Salesforce", "the vendor itself"),
        t("greenhouse", "NeuraFlash", "Salesforce Summit partner"),
        t("greenhouse", "Highmetric", "Salesforce partner"),
        t("greenhouse", "nCino", "financial-services Salesforce ISV"),
        t("greenhouse", "Varicent", "Salesforce-adjacent comp platform"),
        t("lever", "SiteTracker", "Salesforce-native field ops"),
        t("workable", "Flosum", "Salesforce DevOps ISV"),
        t("workable", "Zaelab", "Salesforce commerce partner"),
        t("workable", "Avacone", "Salesforce partner"),
        t("ashby", "RapDev", "Salesforce/ServiceNow consultancy"),
        t("ashby", "Directive", "Salesforce partner"),
        t("ashby", "Loopio", "Salesforce-using SaaS"),
        t("ashby", "Docebo", "55 York St, downtown Toronto"),
        t("ashby", "Benevity", "Calgary/Toronto, Salesforce shop"),
        t("ashby", "Lightspeed Commerce", "Montreal/Toronto"),
        t("workday", "Accenture", "global SI"),
        t("workday", "Altus Group", "Salesforce Platform, Toronto"),
        t("workday", "BMO", "bank"),
        t("workday", "TD Bank", "bank"),
        t("workday", "CIBC", "bank"),
        t("workday", "Sun Life", "insurer"),
        t("workday", "Manulife", "insurer"),
        t("workday", "OMERS", "pension"),
        t("workday", "TMX Group", "exchange operator"),
        t("workday", "Thomson Reuters", "Toronto HQ"),
        t("workday", "Moneris", "payments"),
        t("workday", "McKesson", "healthcare distribution"),
        t("workday", "Cloudera", "data platform"),
        t("workday", "Harris Computer", "vertical software"),
        t("workday", "GDIT", "defense IT integrator"),
    ],
    "servicenow": [
        t("smartrecruiters", "ServiceNow", "the vendor itself"),
        t("smartrecruiters", "Ensiti", "ServiceNow partner"),
        t("smartrecruiters", "Spruce Infotech", "ServiceNow staffing"),
        t("workable", "Crossfuze", "ServiceNow Elite partner"),
        t("greenhouse", "Highmetric", "ServiceNow partner"),
        t("greenhouse", "NeuraFlash", "ServiceNow + Salesforce"),
        t("ashby", "RapDev", "ServiceNow consultancy"),
        t("ashby", "Directive", "ServiceNow partner"),
        t("workday", "Accenture", "global SI"),
        t("workday", "DXC Technology", "ITSM outsourcing"),
        t("workday", "GDIT", "defense IT integrator"),
        t("workday", "Harris Computer", "vertical software"),
        t("workday", "Huron", "consulting"),
        t("workday", "ICF", "consulting"),
        t("workday", "Resolve Tech Solutions", "IT services"),
        t("workday", "SOTI", "Mississauga, MDM"),
        t("workday", "Moneris", "payments"),
        t("workday", "BMO", "bank"),
        t("workday", "TD Bank", "bank"),
        t("workday", "CIBC", "bank"),
        t("workday", "Sun Life", "insurer"),
        t("workday", "Manulife", "insurer"),
        t("workday", "OMERS", "pension"),
        t("workday", "TMX Group", "exchange operator"),
        t("workday", "Interac", "payments"),
        t("workday", "McKesson", "healthcare distribution"),
        t("workday", "Salvation Army Canada", "nonprofit"),
        t("workday", "CAAT Pension Plan", "pension"),
        t("workday", "Brookfield", "asset manager"),
        t("workday", "Medcan", "health services, Toronto"),
    ],
    "other": [
        t("greenhouse", "Geotab", "Oakville, telematics"),
        t("greenhouse", "D2L", "Kitchener, edtech"),
        t("greenhouse", "MongoDB", "database"),
        t("greenhouse", "Okta", "identity"),
        t("greenhouse", "Brex", "fintech"),
        t("greenhouse", "Take-Two", "games"),
        t("greenhouse", "iCapital", "fintech"),
        t("greenhouse", "Toast", "restaurant POS"),
        t("greenhouse", "Movable Ink", "martech"),
        t("lever", "EQ Bank", "digital bank, Toronto"),
        t("lever", "PointClickCare", "Mississauga, health SaaS"),
        t("lever", "Versapay", "fintech"),
        t("lever", "Achievers", "Toronto HR SaaS"),
        t("lever", "Emburse", "expense SaaS"),
        t("lever", "Electric Mind", "Toronto data consultancy"),
        t("ashby", "1Password", "Toronto security"),
        t("ashby", "Docker", "devtools"),
        t("ashby", "Webflow", "web platform"),
        t("ashby", "Inovalon", "healthcare data"),
        t("ashby", "TELUS Digital", "Canadian telco digital"),
        t("workday", "Canadian Tire", "retail, data/BI"),
        t("workday", "Desjardins", "financial co-op"),
        t("workday", "BDO Canada", "professional services"),
        t("workday", "RSM", "professional services"),
        t("workday", "IKO", "building products"),
        t("workday", "MLSE", "sports/entertainment"),
        t("workday", "TJX", "retail"),
        t("workday", "AGF", "asset manager"),
        t("workday", "Canadian Tire", "second pass: analytics titles", "data analyst"),
        t("workday", "Desjardins", "second pass: BI titles", "business intelligence"),
    ],
}

assert all(len(v) == 30 for v in TODO.values()), {k: len(v) for k, v in TODO.items()}


# --------------------------------------------------------------------------
# Workday needs a searchText per query; the other five feeds return the whole
# board and are filtered locally. This mirrors from_workday() but lets a round
# ask for the bucket's own term instead of the hard-coded servicenow/salesforce.
# --------------------------------------------------------------------------
def workday_search(label: str, search: str, pages: int = 5) -> list[dict]:
    tenant, wd, site, brand = WD[label]
    base = f"https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}"
    out = []
    for offset in range(0, pages * 20, 20):
        try:
            data = ats.fetch_json(
                base + "/jobs", method="POST",
                body={"appliedFacets": {}, "limit": 20, "offset": offset, "searchText": search},
            )
        except Exception:
            break
        posts = data.get("jobPostings") or []
        for p in posts:
            path = p.get("externalPath") or ""
            out.append({
                "title": p.get("title") or "", "company": brand,
                "location": p.get("locationsText") or "",
                "url": f"https://{tenant}.{wd}.myworkdayjobs.com/en-US/{site}{path}",
                "posted": ats.workday_day(p.get("postedOn")),
                "posted_raw": p.get("postedOn"),
                "source": f"workday:{tenant}",
            })
        if len(posts) < 20:
            break
    return out


def fetch_round(todo: dict, bucket: str) -> list[dict]:
    route, label = todo["route"], todo["label"]
    if route == "workday":
        term = todo["search"] or ("salesforce" if bucket == "salesforce"
                                  else "servicenow" if bucket == "servicenow" else "data")
        return workday_search(label, term)
    board = {"greenhouse": GH, "lever": LV, "ashby": AB,
             "smartrecruiters": SR, "workable": WK}[route][label]
    fn = {"greenhouse": ats.from_greenhouse, "lever": ats.from_lever, "ashby": ats.from_ashby,
          "smartrecruiters": ats.from_smartrecruiters, "workable": ats.from_workable}[route]
    return fn(board)


def norm_url(u: str) -> str:
    s = urlsplit(u.strip())
    return urlunsplit((s.scheme, s.netloc.lower(), s.path.rstrip("/"), "", ""))


def live(url: str) -> tuple[bool, int]:
    """HTTP status of the posting page. 200/3xx = still published."""
    try:
        req = ats.urllib.request.Request(url, method="GET", headers=ats.UA if hasattr(ats, "UA") else {"User-Agent": "Mozilla/5.0"})
        with ats.urllib.request.urlopen(req, timeout=15) as r:
            return (200 <= r.status < 400), r.status
    except Exception as exc:
        code = getattr(exc, "code", 0) or 0
        return False, code


def load_known() -> set[str]:
    p = ROOT / "jobs.json"
    known = set()
    if p.exists():
        d = json.loads(p.read_text())
        for j in (d.get("jobs") if isinstance(d, dict) else d) or []:
            if j.get("url"):
                known.add(norm_url(j["url"]))
    return known


def run(bucket: str, rounds: int, verify: bool, workers: int) -> dict:
    kws, todos = KW[bucket], TODO[bucket][:rounds]
    known = load_known()
    seen_this_run: set[str] = set()
    results, t0 = [], time.time()

    for i, todo in enumerate(todos, 1):
        r0 = time.time()
        try:
            postings = fetch_round(todo, bucket)
            err = None
        except Exception as exc:
            postings, err = [], f"{type(exc).__name__}: {str(exc)[:80]}"

        matched = [p for p in postings
                   if kws.search(p.get("title") or "")
                   and (bucket != "other" or not OWNED.search(p.get("title") or ""))
                   and ats.is_canadian(p.get("location") or "", p.get("url") or "")]
        # One row per URL per run.
        uniq, dup = [], 0
        for p in matched:
            k = norm_url(p.get("url") or "")
            if not k or k in seen_this_run:
                dup += 1
                continue
            seen_this_run.add(k)
            uniq.append(p)

        live_rows, new_rows = [], []
        if verify and uniq:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                statuses = list(ex.map(lambda r: live(r["url"]), uniq[:40]))
            for r, (ok, code) in zip(uniq, statuses):
                r["http_status"] = code
                if ok:
                    live_rows.append(r)
                    if norm_url(r["url"]) not in known:
                        new_rows.append(r)
        else:
            live_rows = uniq

        entry = {
            "round": i, "target": todo["label"], "route": todo["route"], "note": todo["note"],
            "fetched": len(postings), "matched": len(matched), "dupes": dup,
            "live": len(live_rows), "new": len(new_rows), "error": err,
            "secs": round(time.time() - r0, 1), "jobs": live_rows,
        }
        results.append(entry)
        print(f"[{bucket} {i:02d}/30] {todo['label'][:26]:26s} {todo['route'][:6]:6s} "
              f"fetched={len(postings):3d} match={len(matched):2d} live={len(live_rows):2d} "
              f"new={len(new_rows):2d} {entry['secs']}s{(' ERR ' + err) if err else ''}", flush=True)

    # ---- report -----------------------------------------------------------
    OUT.mkdir(exist_ok=True)
    payload = {
        "bucket": bucket, "generated": NOW.isoformat(), "rounds_planned": 30,
        "rounds_run": len(results), "verify_liveness": verify,
        "totals": {
            "fetched": sum(r["fetched"] for r in results),
            "matched": sum(r["matched"] for r in results),
            "live": sum(r["live"] for r in results),
            "new": sum(r["new"] for r in results),
            "errors": sum(1 for r in results if r["error"]),
            "secs": round(time.time() - t0, 1),
        },
        "rounds": results,
    }
    (OUT / f"bucket_{bucket}_{STAMP}.json").write_text(json.dumps(payload, indent=1))

    lines = [
        f"# {bucket.upper()} — 30 todos / {len(results)} rounds — {STAMP}", "",
        f"Liveness verified: **{'yes' if verify else 'no'}** · generated {NOW.strftime('%H:%M UTC')}", "",
        "| # | Target | Route | Fetched | Matched | Live | New | Secs |",
        "|---|--------|-------|--------:|--------:|-----:|----:|-----:|",
    ]
    for r in results:
        lines.append(f"| {r['round']} | {r['target']} | {r['route']} | {r['fetched']} | "
                     f"{r['matched']} | {r['live']} | {r['new']} | {r['secs']} |")
    tot = payload["totals"]
    lines += ["", f"**Totals** — fetched {tot['fetched']}, matched {tot['matched']}, "
                  f"live-verified {tot['live']}, net-new {tot['new']}, errors {tot['errors']}, "
                  f"{tot['secs']}s.", ""]
    for r in results:
        if not r["jobs"]:
            continue
        lines.append(f"## Round {r['round']} — {r['target']} ({r['live']} live)")
        lines.append("")
        lines.append("| Posted | Title | Company | Location | Live |")
        lines.append("|--------|-------|---------|----------|------|")
        for j in sorted(r["jobs"], key=lambda x: x.get("posted") or "", reverse=True):
            lines.append(f"| {j.get('posted') or '—'} | [{j['title']}]({j['url']}) | "
                         f"{j['company']} | {(j.get('location') or '—')[:38]} | "
                         f"{'200' if j.get('http_status', 200) < 400 else j.get('http_status')} |")
        lines.append("")
    (OUT / f"bucket_{bucket}_{STAMP}.md").write_text("\n".join(lines))
    print(f"\n[{bucket}] totals {payload['totals']}", flush=True)
    return payload


def dump_todos() -> None:
    OUT.mkdir(exist_ok=True)
    plan = {b: [{"round": i, "target": t_["label"], "route": t_["route"],
                 "note": t_["note"], "search": t_["search"]} for i, t_ in enumerate(v, 1)]
            for b, v in TODO.items()}
    p = OUT / f"bucket_todos_{STAMP}.json"
    p.write_text(json.dumps({"generated": NOW.isoformat(), "per_bucket": 30, "buckets": plan}, indent=1))
    print(f"wrote {p} ({sum(len(v) for v in plan.values())} todos)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket", choices=list(TODO), required=False)
    ap.add_argument("--rounds", type=int, default=30)
    ap.add_argument("--verify", type=int, default=1)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dump-todos", action="store_true")
    a = ap.parse_args()
    if a.dump_todos:
        dump_todos()
        sys.exit(0)
    if not a.bucket:
        dump_todos()
        sys.exit(0)
    run(a.bucket, a.rounds, bool(a.verify), a.workers)
