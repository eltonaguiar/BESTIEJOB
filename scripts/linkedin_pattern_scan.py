#!/usr/bin/env python3
"""Replicate the *manual* LinkedIn harvest — from a shell, with no Windows PC and no browser.

Why this exists
---------------
`raw/linkedin_manual_2026-11-04.json` holds 193 rows a human harvested by hand from four
LinkedIn search pages (Jina Reader, on the Windows machine). 100 of those rows were absent
from `jobs.json`: the automated pipeline was missing half of what a person found in an
afternoon. This script reverse-engineers *how* those rows were found and repeats it from
whatever machine it runs on.

The derived pattern (all of it read from the manual file, none of it hardcoded):

  * queries  — the four `<keyword> × <geography>` combinations encoded in the source
               filenames (`linkedin_search_servicenow_toronto.md` -> ServiceNow x Toronto)
  * variants — the role nouns that actually co-occur with the platform in the harvested
               titles (developer, architect, ITOM, CMDB, ...), because LinkedIn matches on
               the title text
  * employers— the companies the harvest concentrated on (consultancies, mostly), used to
               flag a hit as "manual-pattern" rather than to filter it out
  * window   — the harvested dates run back months, so no 14-day cut: recency is reported,
               not used to discard

Why the daily sweep does not cover this: `scripts/linkedin_guest_scan.py` sends
`f_TPR=r259200` (LinkedIn's server-side "last 3 days" filter) and then drops every row
without a posted date. A still-open posting listed three weeks ago cannot survive either
step, and that is exactly what the manual harvest consisted of.

Discovery uses LinkedIn's public guest fragment endpoint
(`jobs-guest/jobs/api/seeMoreJobPostings`), which needs no login, no cookies and no browser.
It rate-limits datacenter IPs with HTTP 429; every request is retried with backoff, and a
query that never succeeds is reported, never silently treated as "no jobs".

Output is a reviewable submission — `raw/linkedin_pattern_<date>.json` plus an inbox file the
merger understands. Nothing is written to jobs.json or the README.

Usage
  python3 scripts/linkedin_pattern_scan.py --derive        # print the pattern, fetch nothing
  python3 scripts/linkedin_pattern_scan.py                 # scan -> inbox submission
  python3 scripts/linkedin_pattern_scan.py --pages 3 --max-queries 16
"""
from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

try:
    from curl_cffi import requests as cr
except ImportError:
    sys.exit("FATAL: curl_cffi not installed (pip install curl_cffi)")

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
RAW = ROOT / "raw"
SEED = RAW / "linkedin_manual_2026-11-04.json"
# Committed distillation of `--derive`, so the scan survives raw/ being wiped.
PATTERN = ROOT / "data" / "manual_harvest_pattern.json"

BASE = "https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
PAGE = 10   # the guest fragment returns ten cards per request, not the 25 the UI shows

# The search pages are named `servicenow`/`salesforce`; these are the names the platform
# actually uses, and they go into the query string.
DISPLAY = {"servicenow": "ServiceNow", "salesforce": "Salesforce"}

ROLE_RE = re.compile(
    r"service\s*now|servicenow|salesforce|itsm|itam|itom|cmdb|mulesoft|apex|"
    r"platform (?:developer|engineer|analyst)|business systems analyst|"
    r"crm (?:developer|analyst|architect)", re.I)
GEO_RE = re.compile(
    r"canada|toronto|ontario|mississauga|brampton|markham|ottawa|calgary|edmonton|"
    r"vancouver|victoria|montr|qu[eé]bec|winnipeg|halifax|waterloo|london, on|remote",
    re.I)

# Generic role nouns worth trying against the platform keyword; only the ones that actually
# appear in the harvested titles get used (see derive()).
ROLE_NOUNS = ["Developer", "Administrator", "Architect", "Consultant", "Analyst",
              "Technical Lead", "Business Analyst", "ITSM", "ITAM", "CMDB", "ITOM",
              "Integration", "CSM", "GRC", "Platform", "Engineer", "Specialist"]


def load_seed() -> tuple[list[dict] | None, str]:
    """The manual harvest itself, if any copy of it survived.

    `raw/` is untracked working data and the Windows sync deletes it without warning, and the
    seed was never committed, so this looks in three places before giving up: the original
    JSON, the inbox submission made from it, then nothing at all (the caller falls back to the
    committed pattern in `data/manual_harvest_pattern.json`).
    """
    if SEED.exists():
        raw = json.loads(SEED.read_text(encoding="utf-8"))
        jobs = raw.get("jobs", raw) if isinstance(raw, dict) else raw
        return list(jobs), SEED.name
    for md in sorted(INBOX.glob("linkedin-manual--*.md")):
        rows = []
        for line in md.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.startswith("| ") or line.startswith("| Posted") or line.startswith("|---"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 5 or not cells[4].startswith("http"):
                continue
            rows.append({"posted": cells[0] if re.match(r"\d{4}-\d{2}-\d{2}$", cells[0]) else "",
                         "title": cells[1], "company": cells[2], "location": cells[3],
                         "url": cells[4], "source": ""})
        if rows:
            return rows, md.name
    return None, ""


def derive(seed: list[dict]) -> dict:
    """Read the manual harvest and describe the pattern that produced it."""
    base_queries: Counter = Counter()
    for row in seed:
        m = re.search(r"linkedin_search_(?P<kw>[a-z]+)_(?P<geo>[a-z]+)\.md", row.get("source") or "")
        if m:
            base_queries[(DISPLAY.get(m["kw"], m["kw"].capitalize()),
                          DISPLAY.get(m["geo"], m["geo"].capitalize()))] += 1

    titles = " ".join(row.get("title") or "" for row in seed).lower()
    variants = [n for n in ROLE_NOUNS if n.lower() in titles]

    employers = Counter((row.get("company") or "").strip() for row in seed)
    employers.pop("", None)

    dates = sorted(row["posted"] for row in seed if (row.get("posted") or "")[:4] == "2026")
    return {
        "seed_rows": len(seed),
        "base_queries": [{"keyword": k, "geo": g, "rows": n} for (k, g), n in base_queries.most_common()],
        "role_variants": variants,
        "employers": [{"company": c, "rows": n} for c, n in employers.most_common(20)],
        "date_range": [dates[0], dates[-1]] if dates else [],
        "undated_share": round(sum(1 for r in seed if not r.get("posted")) / max(1, len(seed)), 2),
    }


def build_queries(pattern: dict, max_queries: int) -> list[tuple[str, str]]:
    """<keyword> x <geo> from the seed, then the role variants, then stop."""
    geos = []
    for q in pattern["base_queries"]:
        geo = "Toronto, Ontario, Canada" if q["geo"].lower() == "toronto" else "Canada"
        if geo not in geos:
            geos.append(geo)
    platforms = [q["keyword"] for q in pattern["base_queries"]]

    out: list[tuple[str, str]] = []
    for platform in platforms:
        for geo in geos:                                     # the four seed combinations first
            out.append((platform, geo))
    for platform in platforms:
        for noun in pattern["role_variants"]:                 # then the harvested title variants
            out.append((f"{platform} {noun}", geos[0]))
    seen, deduped = set(), []
    for kw, geo in out:
        if (kw, geo) not in seen:
            seen.add((kw, geo))
            deduped.append((kw, geo))
    return deduped[:max_queries]


def fetch(url: str, tries: int = 5) -> tuple[str, int]:
    """Guest endpoint, retried: datacenter IPs get 429 before they get HTML."""
    last = 0
    for attempt in range(tries):
        try:
            r = cr.get(url, impersonate="chrome124", timeout=30,
                       headers={"Accept-Language": "en-CA,en;q=0.9"})
            last = r.status_code
            if r.status_code == 200 and "base-card" in r.text:
                return r.text, 200
            if r.status_code in (200, 404) and "base-card" not in r.text:
                return "", r.status_code          # genuinely no results on this page
        except Exception:
            last = -1
        time.sleep(min(20, 3 * (attempt + 1)) + random.uniform(0, 2))
    return "", last


def parse_cards(html: str) -> list[dict]:
    out = []
    for block in re.findall(r"<li>(.*?)</li>", html, re.S):
        urn = re.search(r'data-entity-urn="urn:li:jobPosting:(\d+)"', block)
        title = re.search(r'class="base-search-card__title">\s*(.*?)\s*</h3>', block, re.S)
        company = re.search(r'class="base-search-card__subtitle">.*?>\s*(.*?)\s*</a>', block, re.S)
        if not company:
            company = re.search(r'class="base-search-card__subtitle">\s*(.*?)\s*</h4>', block, re.S)
        loc = re.search(r'class="job-search-card__location">\s*(.*?)\s*</span>', block, re.S)
        posted = re.search(r'<time[^>]*datetime="(\d{4}-\d{2}-\d{2})"', block)
        if not urn or not title:
            continue
        out.append({
            "id": urn.group(1),
            "title": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title.group(1))).strip(),
            "company": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", company.group(1))).strip() if company else "",
            "location": re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", loc.group(1))).strip() if loc else "",
            "posted": posted.group(1) if posted else "",
            "url": f"https://ca.linkedin.com/jobs/view/{urn.group(1)}",
        })
    return out


# Both shapes occur in the repo: slugged (".../service-now-developer-at-kpmg-4482155163",
# which jobs.json and the older inbox files use) and bare (".../jobs/view/4482155163", which
# this scanner writes). Matching only the slugged form made every one of its own submissions
# invisible to the next run, so each run re-submitted the same rows.
LINKEDIN_ID = re.compile(r"linkedin\.com/jobs/view/(?:[^\s|)]*?-)?(\d{8,})(?=[\s|)?#]|$)")


def known_ids() -> set[str]:
    """Every LinkedIn posting id already on the board, in an inbox submission, or archived."""
    ids: set[str] = set()
    for job in json.loads((ROOT / "jobs.json").read_text(encoding="utf-8"))["jobs"]:
        url = job.get("url") or ""
        if "linkedin" in url:
            m = LINKEDIN_ID.search(url)
            if m:
                ids.add(m.group(1))
    sources = [ROOT / "README.md", ROOT / "APPLIED.md"]
    sources += list(INBOX.glob("*.md"))
    for path in sources:
        try:
            ids.update(LINKEDIN_ID.findall(path.read_text(encoding="utf-8", errors="ignore")))
        except OSError:
            continue
    return ids


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--derive", action="store_true", help="print the derived pattern and exit")
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--max-queries", type=int, default=16)
    ap.add_argument("--sleep", type=float, default=2.5)
    args = ap.parse_args()

    seed, seed_name = load_seed()
    if seed is None:
        if not PATTERN.exists():
            sys.exit("no seed harvest and no committed pattern — cannot derive a query matrix")
        blob = json.loads(PATTERN.read_text(encoding="utf-8"))
        pattern = blob["pattern"]
        seed_name = "data/manual_harvest_pattern.json (committed pattern; seed itself is gone)"
        print(f"note: manual harvest seed is absent — using the committed pattern derived from it "
              f"on {blob['provenance']['derived_on']}")

    print(f"seed: {pattern['seed_rows']} manual rows · dates {pattern['date_range']} "
          f"· {int(pattern['undated_share'] * 100)}% undated")
    print("base queries (from the manual harvest's own search pages):")
    for q in pattern["base_queries"]:
        print(f"  {q['keyword']:12s} × {q['geo']:8s}  {q['rows']:3d} rows")
    print("role variants present in the harvested titles: " + ", ".join(pattern["role_variants"]))
    print("employers: " + ", ".join(e["company"] for e in pattern["employers"][:8]) + " …")
    if args.derive:
        return

    queries = build_queries(pattern, args.max_queries)
    print(f"\nscanning {len(queries)} queries × {args.pages} page(s)")

    found: dict[str, dict] = {}
    failed: list[str] = []
    for kw, geo in queries:
        for page in range(args.pages):
            url = (f"{BASE}?keywords={kw.replace(' ', '%20')}"
                   f"&location={geo.replace(' ', '%20').replace(',', '%2C')}&start={page * PAGE}")
            html, code = fetch(url)
            if not html:
                if code != 200:
                    failed.append(f"{kw} × {geo} p{page + 1} (HTTP {code})")
                break
            cards = parse_cards(html)
            for card in cards:
                found.setdefault(card["id"], {**card, "query": f"{kw} × {geo}"})
            print(f"  {kw[:34]:34s} {geo[:10]:10s} p{page + 1}: {len(cards):2d} cards")
            time.sleep(args.sleep + random.uniform(0, 1.5))
            if not cards:
                break

    known = known_ids()
    top_employers = {e["company"].lower() for e in pattern["employers"]}
    fresh = []
    for card in found.values():
        if card["id"] in known or not ROLE_RE.search(card["title"]):
            continue
        if not GEO_RE.search(card["location"] + " " + card["query"]):
            continue
        card["pattern_employer"] = card["company"].lower() in top_employers
        fresh.append(card)

    fresh.sort(key=lambda c: (c["posted"] or "0000"), reverse=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    RAW.mkdir(exist_ok=True)
    (RAW / f"linkedin_pattern_{today}.json").write_text(json.dumps({
        "scannedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "method": "linkedin guest fragment endpoint (no login, no browser)",
        "pattern": pattern,
        "queries": [f"{k} × {g}" for k, g in queries],
        "failed_queries": failed,
        "found": len(found),
        "net_new": len(fresh),
        "jobs": fresh,
    }, indent=1), encoding="utf-8")

    if not fresh:
        # Nothing new: write the diagnostic report but no submission. Writing a header-only
        # inbox file made the workflow commit an empty submission every run.
        print(f"\n{len(found)} cards → 0 net-new: nothing to submit")
        print(f"wrote raw/linkedin_pattern_{today}.json")
        if failed:
            print(f"WARNING: {len(failed)} queries never returned HTML: {failed[:4]}")
        return

    INBOX.mkdir(exist_ok=True)
    version = 1
    while (INBOX / f"linkedin-pattern--{today}--v{version}.md").exists():
        version += 1
    lines = [
        "---",
        "model: linkedin-pattern",
        f"scanned_at: {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        f"task: replicate-manual-linkedin-harvest-{today}",
        f"notes: {len(found)} cards from {len(queries)} guest queries; {len(fresh)} net-new after "
        f"dedupe against jobs.json/README/inbox; {len(failed)} queries failed.",
        "---",
        "",
        "| Posted | Role | Company | Location | URL | Note |",
        "|---|---|---|---|---|---|",
    ]
    for card in fresh:
        note = "manual-pattern employer" if card["pattern_employer"] else card["query"]
        lines.append(f"| {card['posted'] or '—'} | {card['title']} | {card['company']} | "
                     f"{card['location']} | {card['url']} | {note} |")
    out = INBOX / f"linkedin-pattern--{today}--v{version}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"\n{len(found)} cards → {len(fresh)} net-new (deduped against jobs.json/README/inbox)")
    print(f"wrote raw/linkedin_pattern_{today}.json")
    print(f"wrote {out.relative_to(ROOT)}")
    if failed:
        print(f"WARNING: {len(failed)} queries never returned HTML: {failed[:4]}")
    for card in fresh[:10]:
        print(f"  {card['posted'] or '—':10s} {(card['title'][:46]):46s} {card['company'][:24]}")


if __name__ == "__main__":
    main()
