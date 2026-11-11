#!/usr/bin/env python3
"""collapse_mirrors.py — one requisition, one row.

`semantic_dedupe.py` already tries this, but its own dry run on 2026-11-11 would
have dropped 1,047 rows, and it merged *Alimentiv, Toronto* with *Alimentiv,
London, Middlesex* and the Accenture federal postings in Virginia into single
rows. Two rules let that happen: an empty city ("Canada") matches any city, and
nothing compares countries. That is the wrong direction for a job board — a lost
requisition is worse than a duplicate.

This pass therefore only removes a row when **all** of the following hold:

  * `tools/crossurl.same_posting()` — same employer alias, same seniority set,
    title token overlap >= 0.75;
  * both rows name a city and the cities are identical (never "unknown matches
    anything");
  * both rows resolve to the same country, so a Canadian row can never absorb a
    foreign namesake.

Then, inside such a cluster:

  * if any row links to the employer's own ATS page, every aggregator copy
    (LinkedIn, Indeed, Adzuna, Jobicy, …) is a mirror and is dropped; the
    employer URL is the one that still works when the resale listing expires;
  * with no employer URL, only repeated same-host, same-date aggregator copies
    collapse (an aggregator minting several IDs for one requisition) — distinct
    LinkedIn/Indeed posting IDs are separate requisitions and are left alone.

Removed rows are archived, and the feed loses the same URLs so the site agrees
with the board.

Usage
    python3 scripts/collapse_mirrors.py            # report
    python3 scripts/collapse_mirrors.py --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
from board_invariants import parse_readme, normalise_url           # noqa: E402
from crossurl import same_posting, company_key, city               # noqa: E402
from enforce_canada_scope import region_of                         # noqa: E402

AGGREGATOR = re.compile(
    r"linkedin\.|indeed\.|adzuna\.|jobbank\.|glassdoor\.|ziprecruiter\.|simplyhired\.|"
    r"talent\.com|jooble\.|careerjet\.|dice\.com|monster\.com|eluta\.|workopolis\.|"
    r"jobillico\.|neuvoo\.|builtin\.com|jobrapido\.|whatjobs\.|jobicy\.|jobs\.ca|"
    r"visasponsor\.|migratemate\.|jobgether\.|trabajo\.", re.I)


# Hosts that mint a fresh ID for every pull of the same requisition. Only these
# collapse on (host, date): two LinkedIn posting IDs are two requisitions (TD
# listed two ServiceNow developers the same day), so LinkedIn and Indeed are
# never merged without an employer URL to anchor them.
MINTING = re.compile(r"adzuna\.|jobicy\.|simplyhired\.|jobrapido\.|careerjet\.|"
                     r"jooble\.|talent\.com|whatjobs\.|neuvoo\.", re.I)


def is_direct(url: str) -> bool:
    return not AGGREGATOR.search(url or "")


def host(url: str) -> str:
    return re.sub(r"^https?://(www\.)?", "", (url or "").lower()).split("/")[0]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=str(ROOT))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    root = Path(args.repo)

    rows, _ = parse_readme(root / "README.md")
    buckets: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(rows):
        buckets[company_key(r["company"])[:5] or "_"].append(i)

    parent = list(range(len(rows)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    pairs = 0
    for members in buckets.values():
        if len(members) < 2:
            continue
        for pos, ia in enumerate(members):
            a = rows[ia]
            for ib in members[pos + 1:]:
                b = rows[ib]
                if a["url"] == b["url"]:
                    continue
                ca_, cb_ = city(a["location"]), city(b["location"])
                if not ca_ or not cb_ or ca_ != cb_:
                    continue                       # unknown city never matches
                if region_of(a["location"]) != region_of(b["location"]):
                    continue                       # never merge across countries
                if same_posting(a, b):
                    union(ia, ib)
                    pairs += 1

    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(len(rows)):
        groups[find(i)].append(i)

    drop: dict[int, str] = {}
    for members in groups.values():
        if len(members) < 2:
            continue
        directs = [i for i in members if is_direct(rows[i]["url"])]
        if directs:
            for i in members:
                if not is_direct(rows[i]["url"]):
                    drop[i] = "aggregator mirror of an employer URL"
            continue
        # No employer anchor: collapse only same-host, same-date re-listings,
        # never distinct Linkedin/Indeed posting IDs.
        seen: dict[tuple, int] = {}
        for i in members:
            if not MINTING.search(rows[i]["url"]):
                continue
            key = (host(rows[i]["url"]), rows[i]["posted"])
            if key in seen:
                drop[i] = "same aggregator, same date, one requisition"
            else:
                seen[key] = i

    print(f"README rows: {len(rows)}  clusters merged: {pairs} pairs")
    print(f"rows to drop: {len(drop)}")
    print("by reason:", dict(Counter(drop.values())))
    for i, reason in list(drop.items())[:10]:
        r = rows[i]
        print(f"  {r['posted']} | {r['title'][:38]:38} | {r['company'][:18]:18} | "
              f"{r['location'][:18]:18} | {reason}")
        print(f"     {r['url'][:96]}")

    if not args.apply or not drop:
        if not args.apply:
            print("\ndry run — pass --apply to write")
        return 0

    dropped = [rows[i] for i in drop]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive = root / f"README.MIRRORS_{stamp}.md"
    archive.write_text(
        "# Rows removed by collapse_mirrors.py\n"
        "# rule: same employer, seniority, title and city — one requisition, one row\n\n"
        + "\n".join(f"| {r['posted']} | [{r['title']}]({r['url']}) | {r['company']} | "
                    f"{r['location']} | {drop[i]} |"
                    for i, r in zip(sorted(drop, key=lambda x: rows[x]["posted"]),
                                    [rows[k] for k in sorted(drop, key=lambda x: rows[x]["posted"])]))
        + "\n", encoding="utf-8")

    urls = {r["url"] for r in dropped}
    keys = {normalise_url(u) for u in urls}
    readme = root / "README.md"
    kept, removed = [], 0
    for line in readme.read_text(encoding="utf-8").splitlines():
        m = re.search(r"\((https?://[^)\s]+)\)", line)
        if line.startswith("| 20") and m and normalise_url(m.group(1)) in keys:
            removed += 1
            continue
        kept.append(line)
    readme.write_text("\n".join(kept) + "\n", encoding="utf-8")

    feed_path = root / "jobs.json"
    payload = json.loads(feed_path.read_text(encoding="utf-8"))
    jobs = payload["jobs"] if isinstance(payload, dict) else payload
    before = len(jobs)
    jobs = [j for j in jobs if normalise_url(j.get("url", "")) not in keys]
    if isinstance(payload, dict):
        payload["jobs"] = jobs
        if "meta" in payload:
            payload["meta"]["total"] = len(jobs)
    feed_path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
                         encoding="utf-8")

    raw = root / "raw"
    raw.mkdir(exist_ok=True)
    (raw / f"mirrors_{datetime.now(timezone.utc).date().isoformat()}.json").write_text(
        json.dumps({"generatedAt": datetime.now(timezone.utc).isoformat(),
                    "dropped": len(drop), "byReason": dict(Counter(drop.values())),
                    "readmeLinesRemoved": removed, "feedRows": [before, len(jobs)],
                    "rows": [{**{k: rows[i][k] for k in
                                 ("posted", "title", "company", "location", "url")},
                              "reason": drop[i]} for i in sorted(drop)]},
                   indent=1), encoding="utf-8")
    print(f"\nremoved: README lines {removed} · feed rows {before} -> {len(jobs)}")
    print(f"archive: {archive.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
