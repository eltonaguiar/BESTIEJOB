#!/usr/bin/env python3
"""Scan ServiceNow World Forum Toronto sponsors' own ATS boards for SN/SF roles.

The sponsor list from servicenow.com/events/world-forum/toronto.html is a set of
*hypotheses* about employers, not a set of boards.  Every sponsor name is turned
into slug candidates and each candidate is checked against the public board
APIs; a name that resolves to no board is reported as unreachable rather than
guessed at.

Nothing here infers a date.  A row only carries `posted` when the employer's own
board published one.

Usage:
    python3 scripts/partner_sponsor_scan.py            # probe + write inbox
    python3 scripts/partner_sponsor_scan.py --dry-run  # probe, print only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from parallel_fanout_scan import probe  # noqa: E402
from today_feeds_scan import EXCL, GEO, KW, TECH_TITLE  # noqa: E402

NOW = datetime.now(timezone.utc)
INBOX = ROOT / "inbox"
RAW = ROOT / "raw" / "partners"

PLATFORMS = ("greenhouse", "lever", "ashby", "smartrecruiters", "workable",
             "recruitee", "bamboohr", "pinpoint")

# ServiceNow World Forum Toronto sponsors, by tier, plus ServiceNow's Canadian
# partner ecosystem.  Some are product vendors rather than consultancies; they
# can still carry ServiceNow-integration roles, so they are probed too.
SPONSORS: list[tuple[str, str]] = [
    # Diamond
    ("Ateko", "diamond"), ("Deloitte Canada", "diamond"),
    ("Ernst & Young", "diamond"), ("KPMG", "diamond"),
    # Platinum
    ("Carahsoft", "platinum"), ("Cognizant", "platinum"),
    ("Crossfuze", "platinum"), ("Fujitsu", "platinum"),
    ("Ondaro", "platinum"), ("Tanium", "platinum"),
    ("TeamViewer", "platinum"), ("xtype", "platinum"),
    # Gold
    ("BDO Canada", "gold"), ("Blue Mantis", "gold"), ("Brightfin", "gold"),
    ("CDW", "gold"), ("Compugen", "gold"), ("Dynatrace", "gold"),
    ("Everforth GlideFast", "gold"), ("GlideFast", "gold"),
    ("Flexxible", "gold"), ("IBM", "gold"), ("NewRocket", "gold"),
    ("NewRocket Ltd", "gold"), ("Pentio", "gold"), ("RapDev", "gold"),
    ("SageX Transformations", "gold"), ("ScreenMeet", "gold"),
    ("TELUS", "gold"), ("Traversal", "gold"), ("Wind River", "gold"),
    # Bronze
    ("Tech Mahindra", "bronze"),
    # ServiceNow's Canadian partner ecosystem, named in the same breath
    ("OpenText", "associate"), ("Hitachi Solutions", "associate"),
    ("Unisys", "associate"), ("DXC Technology", "associate"),
    ("CGI", "associate"), ("Long View Systems", "associate"),
    ("Calgary Technologies", "associate"), ("ThinkOn", "associate"),
]

# Workday tenants cannot be guessed reliably from a display name, so the ones
# worth trying are listed explicitly.  A wrong triple simply returns nothing.
WORKDAY: list[tuple[str, str, str, str]] = [
    ("opentext", "wd3", "OpenText", "OpenText"),
    ("cgi", "wd3", "CGI_Careers", "CGI"),
    ("ibm", "wd1", "External", "IBM"),
    ("deloitte", "wd3", "Deloitte_Careers", "Deloitte"),
    ("kpmgca", "wd3", "KPMGCanada", "KPMG Canada"),
    ("ey", "wd3", "EYCareers", "EY"),
    ("cdw", "wd1", "cdw", "CDW"),
    ("telus", "wd3", "TELUS_Careers", "TELUS"),
    ("cognizant", "wd1", "Cognizant", "Cognizant"),
    ("techmahindra", "wd3", "Tech_Mahindra", "Tech Mahindra"),
    ("fujitsu", "wd3", "Fujitsu", "Fujitsu"),
    ("bdo", "wd3", "BDO", "BDO Canada"),
    ("unisys", "wd1", "Unisys", "Unisys"),
    ("dxc", "wd3", "DXC", "DXC Technology"),
]

NOISE = re.compile(r"\b(inc|llc|ltd|corp|corporation|limited|llp|plc|group|"
                   r"canada|the|technologies|technology|solutions|services|"
                   r"systems|business|transformations|\.io)\b", re.I)


def slug_candidates(name: str) -> list[str]:
    """Board-token guesses for a company name, most likely first."""
    base = NOISE.sub(" ", name)
    words = [w for w in re.split(r"[^A-Za-z0-9]+", base) if w]
    if not words:
        return []
    joined = "".join(words).lower()
    hyphen = "-".join(w.lower() for w in words)
    first = words[0].lower()
    out = [joined, hyphen, first]
    if len(words) > 1:
        out.append("".join(w[0] for w in words).lower())
    seen, uniq = set(), []
    for s in out:
        if len(s) >= 3 and s not in seen:
            seen.add(s)
            uniq.append(s)
    return uniq


def relevant(j: dict) -> bool:
    title = j.get("title") or ""
    if EXCL.search(title):
        return False
    if not KW.search(title):
        return False
    loc = j.get("location") or ""
    # A board may post Canada roles with a blank location; keep those only when
    # the title itself is unambiguous about the platform.
    return bool(GEO.search(loc)) or loc == ""


def scan(dry_run: bool = False) -> tuple[list[dict], dict]:
    rows: list[dict] = []
    report: dict[str, str] = {}
    seen_urls: set[str] = set()

    def take(jobs: list[dict], label: str) -> int:
        kept = 0
        for j in jobs:
            url = (j.get("url") or "").split("?")[0]
            if not url or url in seen_urls:
                continue
            if not relevant(j):
                continue
            seen_urls.add(url)
            j["company"] = j.get("company") or label
            j["sponsor"] = label
            rows.append(j)
            kept += 1
        return kept

    for name, tier in SPONSORS:
        tried = hit = 0
        found = False
        for platform in PLATFORMS:
            for slug in slug_candidates(name)[:3]:
                tried += 1
                jobs = probe(platform, slug)
                if jobs:
                    hit += 1
                    take(jobs, name)
                    found = True
                    break  # this platform resolved; skip its other slugs
            if found:
                break  # one board per employer is enough for a first pass
        report[name] = (f"{tier}: {tried} slugs probed, {hit} live board(s)"
                        if hit else f"{tier}: no public board found")

    for tenant, wd, site, label in WORKDAY:
        jobs = probe("workday", f"{tenant}|{wd}|{site}")
        if jobs:
            report[label] = f"workday: live board ({tenant})"
            take(jobs, label)

    rows.sort(key=lambda r: (r.get("posted") or "", r.get("company") or ""),
              reverse=True)
    return rows, report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows, report = scan(args.dry_run)

    live = [k for k, v in report.items() if "no public board" not in v]
    print(f"sponsors checked : {len(report)}")
    print(f"boards resolved  : {len(live)}")
    print(f"relevant rows    : {len(rows)}")
    dated = sum(1 for r in rows if r.get("posted"))
    recent = sum(1 for r in rows if (r.get("posted") or "") >= "2026-10-27")
    print(f"dated            : {dated} ({recent} within 7 days)")

    if not args.dry_run:
        print()
        for name, status in report.items():
            print(f"  {name:28s} {status}")

    if not rows:
        print("\nNo relevant postings found.")
        return 0

    print()
    for r in rows[:40]:
        print("  %-11s %-24s %s" % (r.get("posted") or "undated",
                                    (r["company"] or "")[:24],
                                    (r.get("title") or "")[:58]))

    if args.dry_run:
        return 0

    INBOX.mkdir(exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    stamp = NOW.strftime("%Y-%m-%dT%H%M%SZ")
    (RAW / f"sponsor-scan-{stamp}.json").write_text(
        json.dumps({"scanned_at": stamp, "report": report, "rows": rows},
                   indent=1, ensure_ascii=False))

    day = NOW.strftime("%Y-%m-%d")
    out = INBOX / f"partner-sponsors--{day}.md"
    body = [
        "---",
        "model: partner-sponsors",
        f"scanned_at: {stamp}",
        "task: servicenow-world-forum-toronto-sponsors",
        "---",
        "",
        f"# ServiceNow World Forum Toronto sponsors — {day}",
        "",
        f"{len(report)} sponsors and associates probed against their own public "
        f"ATS APIs; {len(live)} resolved to a live board. {len(rows)} relevant "
        f"postings ({dated} carrying a date from the employer's own board).",
        "",
        "| Posted | Role | Company | Location | Source |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        t = (r.get("title") or "").replace("|", "/")
        body.append(f"| {r.get('posted') or '—'} | [{t}]({r['url']}) | "
                    f"{r['company']} | {(r.get('location') or '').strip()} | "
                    f"via {r.get('source')} |")
    out.write_text("\n".join(body) + "\n")
    print(f"\nwrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
