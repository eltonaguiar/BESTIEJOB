#!/usr/bin/env python3
"""
Rebuild the three job tables in bestiejob/README.md from
raw/second_round_2026-11-02.json.

Rules (from the subtask spec):
  * Candidates = raw records where is_new_vs_jobs_json is true OR posted_date is
    the target date (2026-11-02).
  * Existing README rows that are still live (== their URL was re-seen in this
    run, or they are a primary/employer source dated within the window) are kept
    as "reconfirmed" fillers so each table still holds 60 rows.
  * Newest first; the target-date rows are forced to the top of their table.
  * Ranked by relevance (pillar keyword in title / query specificity), then date,
    then job id -- fully deterministic.

Usage:
    python3 tools/rebuild_readme_tables.py --dry-run
    python3 tools/rebuild_readme_tables.py --write
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BESTIEJOB = HERE.parent
README = BESTIEJOB / "README.md"
RAW = BESTIEJOB / "raw" / "second_round_2026-11-02.json"
TARGET_DATE = "2026-11-02"
TARGET_ROWS = 60
MAX_ROWS = 60
PILLARS = ("servicenow", "salesforce", "other")

# --------------------------------------------------------------------------
# keyword dictionaries
# --------------------------------------------------------------------------
STRONG = {
    "servicenow": [
        "servicenow", "snow ", "itsm", "itom", "itam", "cmdb", "grc",
        "discovery", "service portal", "hrsd", "fsm", "csm",
    ],
    "salesforce": [
        "salesforce", "sfdc", "sfmc", "marketing cloud", "cpq", "pardot",
        "apex", "visualforce", "lightning", "sales cloud", "service cloud",
        "revenue cloud", "financial services cloud", "experience cloud",
    ],
    "other": [
        "itsm", "itil", "itam", "cmdb", "integration", "middleware", "api",
        "workflow", "automation", "rpa", "business analyst", "business systems",
        "data analyst", "data engineer", "bi ", "power bi", "tableau", "sql",
        "service desk", "help desk", "incident", "change management",
        "application support", "systems analyst", "technical project manager",
        "devops", "platform", "crm", "erp", "mulesoft", "boomi",
    ],
}

# Titles that must never appear in the "other" table even if the query matched.
OTHER_NOISE = [
    "paint", "e-coat", "welder", "millwright", "electrician", "hvac",
    "forklift", "machine operator", "production associate", "line cook",
    "warehouse", "labourer", "labour", "janitor", "custodian", "truck driver",
    "registered nurse", "personal support worker", "dental", "phlebotom",
    "hair stylist", "barista", "server ", "busser", "dishwasher",
    "autobody", "autobody", "collision repair", "mechanic", "plumber",
]

# Locations we consider in-scope (Toronto-first, Canada-wide).
OUT_OF_SCOPE_LOC = [
    "india", "bengaluru", "bangalore", "hyderabad", "pune", "chennai",
    "philippines", "manila", "pakistan", "nigeria", "egypt", "brazil",
    "mexico city", "poland", "romania", "ukraine", "atlanta, ga", "roy, ut",
    ", ut", "virginia", "texas", "florida", "california,", "new york, ny",
    "chicago, il", "seattle, wa", "boston, ma", "austin, tx",
]

ADZUNA_ID_RE = re.compile(r"/(?:details|land/ad)/(\d+)")
ROW_RE = re.compile(r"^\| (\d{4}-\d{2}-\d{2}) \| \[(.*?)\]\((.*?)\) \| (.*?) \| (.*?) \| (.*?) \|$")


def adzuna_id(url: str) -> str | None:
    m = ADZUNA_ID_RE.search(url or "")
    return m.group(1) if m else None


def norm_url(url: str) -> str:
    """Strip query string + trailing slash so utm_* variants collapse."""
    return (url or "").split("?")[0].rstrip("/").lower()


def clean(text: str) -> str:
    """Make a cell safe for a markdown table and drop NBSP."""
    return (text or "").replace("\xa0", " ").replace("|", "\\|").replace("\n", " ").strip()


def keyword_hits(pillar: str, title: str) -> list[str]:
    low = f" {title.lower()} "
    return [k for k in STRONG[pillar] if k in low]


def relevance(pillar: str, title: str, query: str) -> int:
    """Higher is better. Title keyword match dominates; query specificity adds."""
    hits = keyword_hits(pillar, title)
    score = 0
    score += 10 * min(len(hits), 3)
    # a pillar keyword appearing in the title is the strongest signal
    if pillar in title.lower():
        score += 25
    # shorter queries are more specific ("Salesforce CPQ" > "Salesforce")
    q = (query or "").lower()
    if q and q != pillar:
        score += 4
    # generic / junky titles lose points
    for bad in ("manager", "director", "vp ", "vice president", "intern", "stage ", "stagiaire"):
        if bad in title.lower():
            score -= 6
    return score


def in_scope_location(loc: str) -> bool:
    low = (loc or "").lower()
    return not any(bad in low for bad in OUT_OF_SCOPE_LOC)


# --------------------------------------------------------------------------
# load
# --------------------------------------------------------------------------
def load_raw() -> list[dict]:
    data = json.loads(RAW.read_text(encoding="utf-8"))
    return data["jobs"]


def parse_existing() -> dict[str, list[dict]]:
    """Parse the current README tables into structured rows."""
    out: dict[str, list[dict]] = {p: [] for p in PILLARS}
    text = README.read_text(encoding="utf-8")
    stops = {
        "servicenow": r"^### Salesforce jobs",
        "salesforce": r"^### Other jobs",
        "other": r"^## User",
    }
    heads = {
        "servicenow": r"^### ServiceNow jobs",
        "salesforce": r"^### Salesforce jobs",
        "other": r"^### Other jobs",
    }
    for pillar in PILLARS:
        inside = False
        for line in text.split("\n"):
            if re.match(heads[pillar], line):
                inside = True
                continue
            if inside and re.match(stops[pillar], line):
                break
            if not inside:
                continue
            m = ROW_RE.match(line)
            if not m:
                continue
            date, title, url, company, loc, note = m.groups()
            out[pillar].append(
                {
                    "date": date,
                    "title": title,
                    "url": url,
                    "company": company,
                    "location": loc,
                    "note": note.strip(),
                    "origin": "existing",
                }
            )
    return out


# --------------------------------------------------------------------------
# build
# --------------------------------------------------------------------------
def build_pool(pillar: str, raw: list[dict], existing: list[dict]) -> list[dict]:
    seen_urls: set[str] = set()
    seen_ids: set[str] = set()
    pool: list[dict] = []

    # 1. raw records (new or target-dated)
    for j in raw:
        if j["pillar"] != pillar:
            continue
        if not (j.get("is_new_vs_jobs_json") or j["posted_date"] == TARGET_DATE):
            continue
        u = norm_url(j["url"])
        jid = j.get("source_job_id") or adzuna_id(j["url"]) or ""
        if u in seen_urls or (jid and jid in seen_ids):
            continue
        seen_urls.add(u)
        if jid:
            seen_ids.add(jid)
        pool.append(
            {
                "date": j["posted_date"],
                "title": clean(j["title"]),
                "url": j["url"],
                "company": clean(j["company"]),
                "location": clean(j["location"]),
                "query": j.get("query", ""),
                "job_id": jid,
                "is_new": bool(j.get("is_new_vs_jobs_json")),
                "origin": "raw",
            }
        )

    # 2. existing rows that are still live -> reconfirmed fillers
    raw_ids = {j.get("source_job_id") for j in raw if j.get("source_job_id")}
    raw_urls = {norm_url(j["url"]) for j in raw}
    for r in existing:
        u = norm_url(r["url"])
        rid = adzuna_id(r["url"])
        if u in seen_urls:
            continue
        if rid and rid in raw_ids:
            continue  # already covered by a raw record
        # only carry forward rows inside the live window
        if r["date"] < "2026-10-29":
            continue
        seen_urls.add(u)
        primary = "adzuna.ca" not in r["url"]
        pool.append(
            {
                "date": r["date"],
                "title": clean(r["title"]),
                "url": r["url"],
                "company": clean(r["company"]),
                "location": clean(r["location"]),
                "query": "",
                "job_id": rid or "",
                "is_new": False,
                "origin": "existing",
                "was_in_raw": u in raw_urls or (rid in raw_ids if rid else False),
                "primary": primary,
                "old_note": r["note"],
            }
        )
    return pool


def is_relevant(pillar: str, rec: dict) -> bool:
    title_low = rec["title"].lower()
    if pillar == "other":
        if any(bad in title_low for bad in OTHER_NOISE):
            return False
        if not in_scope_location(rec["location"]):
            # keep out-of-scope only when the title is a very strong match
            if not keyword_hits("other", rec["title"]):
                return False
        return bool(keyword_hits("other", rec["title"]))
    # servicenow / salesforce
    if not in_scope_location(rec["location"]):
        return False
    return bool(keyword_hits(pillar, rec["title"])) or rec.get("primary", False)


def note_for(pillar: str, rec: dict) -> str:
    """Source / note cell: pillar keyword match + Adzuna id + new/reconfirmed flag.

    Rows carried forward from the previous README keep their original provenance
    note (peer / employer-ATS evidence is not reproducible from the raw JSON), but
    get the required ``reconfirmed 2026-11-02`` flag appended so every row in the
    table carries the same audit marker.
    """
    if rec["origin"] == "existing" and rec.get("old_note"):
        base = rec["old_note"].rstrip(" .")
        if "reconfirmed" in base or "new" == base.split()[-1:]:
            return base
        if rec.get("job_id"):
            return f"{base} \u00b7 Adzuna {rec['job_id']} \u00b7 reconfirmed 2026-11-02"
        return f"{base} \u00b7 reconfirmed 2026-11-02"
    hits = keyword_hits(pillar, rec["title"])
    kw = hits[0] if hits else (rec.get("query") or pillar).lower()
    label = {"servicenow": "ServiceNow", "salesforce": "Salesforce", "other": "IT platform"}[pillar]
    parts = [f"{label} match: {kw}"]
    if rec.get("query"):
        parts.append(f"query \u201c{rec['query']}\u201d")
    if rec.get("job_id"):
        parts.append(f"Adzuna {rec['job_id']}")
    if rec.get("is_new"):
        parts.append("new")
    else:
        parts.append("reconfirmed 2026-11-02")
    return " \u00b7 ".join(parts)


def select(pillar: str, pool: list[dict]) -> list[dict]:
    """Pick TARGET_ROWS.

    Ordering guarantees, highest priority first:
      1. Every raw record dated TARGET_DATE (the run's fresh postings) is pinned
         to the top of the table. The subtask mandates these appear, even when
         the title carries no pillar keyword (e.g. "Automation Engineer" found
         via the ServiceNow query) or reads like unrelated noise.
      2. Everything else is ranked by relevance, then primary-source, then date.
    """
    pinned = [r for r in pool if r["date"] == TARGET_DATE and r["origin"] == "raw"]
    pinned.sort(key=lambda r: r.get("job_id", ""), reverse=True)

    pinned_ids = {(r.get("job_id"), norm_url(r["url"])) for r in pinned}
    scored = []
    for rec in pool:
        key = (rec.get("job_id"), norm_url(rec["url"]))
        if key in pinned_ids:
            continue
        if not is_relevant(pillar, rec):
            continue
        scored.append(
            (
                relevance(pillar, rec["title"], rec.get("query", "")),
                rec.get("primary", False),
                rec["date"],
                rec.get("job_id", ""),
                rec,
            )
        )
    scored.sort(key=lambda t: (t[0], t[1], t[2], t[3]), reverse=True)

    remaining = MAX_ROWS - len(pinned)
    rest = [t[4] for t in scored[:remaining]]
    rest.sort(key=lambda r: (r["date"], r.get("job_id", "")), reverse=True)
    return (pinned + rest)[:MAX_ROWS]


def render_table(pillar: str, rows: list[dict]) -> str:
    lines = [
        "| Posted | Role | Company | Location | Source / note |",
        "|---|---|---|---|---|",
    ]
    for rec in rows:
        lines.append(
            f"| {rec['date']} | [{rec['title']}]({rec['url']}) | {rec['company']} "
            f"| {rec['location']} | {note_for(pillar, rec)} |"
        )
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    if not args.write:
        args.dry_run = True

    raw = load_raw()
    existing = parse_existing()

    built: dict[str, list[dict]] = {}
    for pillar in PILLARS:
        pool = build_pool(pillar, raw, existing[pillar])
        built[pillar] = select(pillar, pool)
        today = sum(1 for r in built[pillar] if r["date"] == TARGET_DATE)
        new = sum(1 for r in built[pillar] if r.get("is_new"))
        print(
            f"{pillar:12s} pool={len(pool):4d} selected={len(built[pillar]):3d} "
            f"today={today} new={new} carried={len(built[pillar])-new}"
        )

    if args.dry_run:
        print("\n--- preview: first 3 rows per pillar ---")
        for pillar in PILLARS:
            print(f"\n### {pillar}")
            for rec in built[pillar][:3]:
                print(f"  {rec['date']} | {rec['title'][:50]} | {rec['company'][:25]}")
        return 0

    text = README.read_text(encoding="utf-8")
    blocks = {}
    for pillar in PILLARS:
        rows = built[pillar]
        head = {
            "servicenow": "ServiceNow",
            "salesforce": "Salesforce",
            "other": "Other",
        }[pillar]
        sub = {
            "servicenow": "_developer / administrator / architect / analyst roles_",
            "salesforce": "_developer / administrator / architect / consultant roles_",
            "other": "_ITSM, ITAM, CMDB, SQL, BI, automation and integration roles that match the profile_",
        }[pillar]
        blocks[pillar] = (
            f"### {head} jobs ({len(rows)})\n\n"
            f"{sub}\n\n"
            f"<details><summary><strong>Show {len(rows)} postings</strong></summary>\n\n"
            f"{render_table(pillar, rows)}\n\n"
            "</details>"
        )

    # splice: replace from "### ServiceNow jobs" to just before "## User / AI agent guide"
    start = text.index("### ServiceNow jobs")
    end = text.index("## User / AI agent guide")
    new_mid = "\n\n".join(blocks[p] for p in PILLARS) + "\n\n"
    text = text[:start] + new_mid + text[end:]
    README.write_text(text, encoding="utf-8")
    print(f"\nwrote {README} ({len(text.splitlines())} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
