#!/usr/bin/env python3
"""import_fresh_rows.py — repair the README tables and promote freshly-scanned rows.

Two jobs, both surgical:

  repair   The 2026-11-03 merge collapsed the ServiceNow and Salesforce tables into
           one block: 813 rows under a single "### ServiceNow jobs" heading, with the
           "### Salesforce jobs" heading gone. The site builds one table from that
           block, so the Salesforce section had no heading to render. This splits the
           rows back by classify() and rewrites both sections with correct counts.

  import   Rows live in two stores: the scanners write FRESH_JOBS.md / raw/*.json,
           the site builds from README.md. A fresh posting could sit in one and never
           reach the other. This inserts the dated ServiceNow/Salesforce rows from
           those files into the matching table, newest first.

Nothing else in README.md is rewritten. It never uses jobs_merge_inbox.py's full
re-render, which caps tables at --max-per-table and would archive existing rows.

Usage
    python3 tools/import_fresh_rows.py --dry-run
    python3 tools/import_fresh_rows.py --days 7
    python3 tools/import_fresh_rows.py --no-repair        # import only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from jobs_consolidate import classify, normalise_url  # noqa: E402

README = ROOT / "README.md"
APPLIED = ROOT / "APPLIED.md"
ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|")
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")

HEAD = {
    "servicenow": "### ServiceNow jobs ({n})\n\n"
                  "_developer / administrator / architect / analyst roles_\n\n"
                  "<details><summary><strong>Show {n} postings</strong></summary>\n",
    "salesforce": "### Salesforce jobs ({n})\n\n"
                  "_developer / administrator / architect / analyst roles_\n\n"
                  "<details><summary><strong>Show {n} postings</strong></summary>\n",
}
TABLE = "| Posted | Role | Company | Location | Source / note |\n|---|---|---|---|---|\n"
FOOT = "\n\n</details>\n\n"


def cell(text: str) -> str:
    return (text or "").replace("|", "/").replace("\n", " ").replace("\xa0", " ").strip()


def parse_row(line: str) -> dict | None:
    if not ROW.match(line):
        return None
    link = LINK.search(line)
    if not link:
        return None
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 4:
        return None
    note = cells[4] if len(cells) > 4 and "http" not in cells[4] else ""
    return {"posted": cells[0], "title": link.group(1), "url": link.group(2),
            "company": cells[2], "location": cells[3], "note": note, "line": line}


def render(row: dict) -> str:
    return (f"| {row['posted']} | [{cell(row['title'])}]({row['url']}) | "
            f"{cell(row['company'])} | {cell(row['location']) or 'Not specified'} | "
            f"{cell(row['note']) or 'via fresh scan'} |")


def block_rows(text: str, heading: str, stop: str) -> list[dict]:
    start = text.find(heading)
    if start < 0:
        return []
    end = text.find(stop, start)
    if end < 0:
        end = len(text)
    out = []
    for line in text[start:end].splitlines():
        row = parse_row(line)
        if row:
            out.append(row)
    return out


def load_fresh(days: int) -> list[dict]:
    cutoff = (datetime.now(timezone.utc).date() - timedelta(days=days)).isoformat()
    upper = (datetime.now(timezone.utc).date() + timedelta(days=1)).isoformat()
    rows: list[dict] = []
    for path in [ROOT / "FRESH_JOBS.md"]:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            row = parse_row(line)
            if row and cutoff <= row["posted"] <= upper:
                rows.append(row)
    for path in sorted((ROOT / "raw").glob("*.json")):
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        bucket = data.get("dated") if isinstance(data, dict) else None
        if not isinstance(bucket, list):
            raw_rows = data.get("rows") if isinstance(data, dict) else None
            bucket = raw_rows if isinstance(raw_rows, list) else []
        for r in bucket:
            if not isinstance(r, dict) or not r.get("url") or not r.get("posted"):
                continue
            if not (cutoff <= r["posted"] <= upper):
                continue
            rows.append({"posted": r["posted"], "title": r.get("title", ""),
                         "url": r["url"], "company": r.get("company", ""),
                         "location": r.get("location", "") or "",
                         "note": f"via {r.get('source', 'scan')}", "line": ""})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-repair", action="store_true")
    args = ap.parse_args()

    text = README.read_text(encoding="utf-8")

    known = {normalise_url(u) for u in re.findall(r"https?://[^\s)|]+", text)}
    if APPLIED.exists():
        known |= {normalise_url(u) for u in
                  re.findall(r"https?://[^\s)|]+", APPLIED.read_text(errors="replace"))}

    middle = block_rows(text, "### ServiceNow jobs", "### Other jobs")
    print(f"rows in the ServiceNow/Salesforce block: {len(middle)}")

    fresh = load_fresh(args.days)
    print(f"fresh rows in the last {args.days} days across scan output: {len(fresh)}")

    # Rows already in the README always survive. A fresh row for the same canonical
    # URL does not duplicate it — it updates the posting date, because the employer
    # re-listed the role and the newer date is the honest one.
    by_key: dict[str, dict] = {}
    for row in middle:
        row["family"] = classify(row["title"], row["url"], row["location"])
        by_key.setdefault(normalise_url(row["url"]), row)
    refreshed = added = 0
    for row in fresh:
        key = normalise_url(row["url"])
        family = classify(row["title"], row["url"], row["location"])
        if key in by_key:
            if row["posted"] > by_key[key]["posted"]:
                by_key[key]["posted"] = row["posted"]
                refreshed += 1
            continue
        if key in known:          # APPLIED.md: never re-add a role already applied to
            continue
        row["family"] = family
        by_key[key] = row
        added += 1
    print(f"date refreshed on existing rows: {refreshed}; genuinely new: {added}")

    families: dict[str, list[dict]] = {"servicenow": [], "salesforce": [], "other": []}
    for row in by_key.values():
        families[row["family"]].append(row)

    for fam in families:
        families[fam].sort(key=lambda r: r["posted"], reverse=True)
    print("split:", {k: len(v) for k, v in families.items()})
    for r in families["servicenow"][:5]:
        print(f"  SN {r['posted']} {r['title'][:55]} — {cell(r['company'])[:28]}")
    for r in families["salesforce"][:5]:
        print(f"  SF {r['posted']} {r['title'][:55]} — {cell(r['company'])[:28]}")

    if args.dry_run:
        print("\n(dry run — README not written)")
        return 0

    n_sn, n_sf = len(families["servicenow"]), len(families["salesforce"])
    rebuilt = (HEAD["servicenow"].format(n=n_sn) + TABLE
               + "\n".join(render(r) for r in families["servicenow"]) + FOOT
               + HEAD["salesforce"].format(n=n_sf) + TABLE
               + "\n".join(render(r) for r in families["salesforce"]) + FOOT)

    start = text.find("### ServiceNow jobs")
    end = text.find("### Other jobs")
    if start < 0 or end < 0:
        print("!! could not locate table block — aborting")
        return 1

    # The Other table is edited BEFORE the middle block is replaced: splicing the
    # middle block first shifts every later offset, which previously truncated the
    # Other table to a single row.
    if families["other"]:
        other_next = next((m.start() for m in re.finditer(r"^##\s+", text[end:], re.M)), None)
        other_end = end + other_next if other_next else len(text)
        oblock = text[end:other_end]
        sep = oblock.find("|---")
        if sep > 0:
            eol = oblock.find("\n", sep)
            head_lines = oblock[:eol].splitlines()
            existing = [l for l in oblock[eol:].splitlines() if ROW.match(l)]
            merged = sorted(existing + [render(r) for r in families["other"]],
                            key=lambda l: l.split("|")[1].strip(), reverse=True)
            tail = [l for l in oblock[eol:].splitlines() if not ROW.match(l)]
            oblock = "\n".join(head_lines + merged + tail)
            total = len(merged)
            oblock = re.sub(r"(#{3,4}\s+Other jobs) \(\d+\)", rf"\1 ({total})", oblock, count=1)
            oblock = re.sub(r"<strong>Show \d+ postings</strong>",
                            f"<strong>Show {total} postings</strong>", oblock, count=1)
            text = text[:end] + oblock + text[other_end:]
            end = text.find("### Other jobs")

    text = text[:start] + rebuilt + text[end:]

    for label, n in (("ServiceNow", n_sn), ("Salesforce", n_sf)):
        text = re.sub(rf"^- \[{label} jobs \(\d+\)\]\(#{label.lower()}-jobs-\d+\)$",
                      f"- [{label} jobs ({n})](#{label.lower()}-jobs-{n})", text,
                      count=1, flags=re.M)

    README.write_text(text, encoding="utf-8")
    print(f"\nwrote README.md — ServiceNow {n_sn}, Salesforce {n_sf}, other {len(families['other'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
