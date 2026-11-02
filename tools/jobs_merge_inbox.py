#!/usr/bin/env python3
"""
Merge inbox/ job submissions into README.md's three tables.

Agents submit work by dropping a file in inbox/ (or a PR that only adds one), named:

    inbox/<model-slug>--<YYYY-MM-DD>--v<N>.md

If the file is submitted again — a correction, a later scan from the same model on the
same day — increment N instead of creating a second file. The merger does that
automatically: after a successful run every merged file is renamed to the next version
and stamped with what it contributed.

Usage:
  python3 tools/jobs_merge_inbox.py --dry-run
  python3 tools/jobs_merge_inbox.py
  python3 tools/jobs_merge_inbox.py --today 2026-11-02 --days 30

Merging:
  * reads every inbox/*.md except files starting with "_" or "TEMPLATE"
  * keeps rows with an absolute YYYY-MM-DD posted date and a URL
  * dedupes on normalised URL against the README and the other inbox files
  * rewrites README with the same three-table layout the consolidator produces
  * moves rows older than --days into README.BAK_<UTC timestamp>.md
"""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from jobs_consolidate import (  # noqa: E402
    README,
    classify,
    dedupe,
    extract_rows,
    extract_scan_block,
    normalise_url,
    render,
)

INBOX = ROOT / "inbox"
NAME_RE = re.compile(r"^(?P<model>[a-z0-9._-]+)--(?P<date>\d{4}-\d{2}-\d{2})--v(?P<ver>\d+)\.md$", re.I)
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BARE_URL_RE = re.compile(r"https?://[^\s|)]+")


def parse_inbox_file(path: Path) -> list[dict]:
    """Rows: | Posted | Role | Company | Location | URL | (extra columns tolerated)."""
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        posted = cells[0].strip()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", posted):
            continue
        link = LINK_RE.search(line)
        if link:
            title, url = link.group(1), link.group(2)
        else:
            bare = BARE_URL_RE.search(line)
            if not bare:
                continue
            url = bare.group(0)
            title = cells[1]
        company = cells[2] if len(cells) > 2 else ""
        location = cells[3] if len(cells) > 3 else ""
        note = (cells[4] if len(cells) > 4 and "http" not in cells[4] else "").strip()
        rows.append(
            {
                "posted": posted,
                "title": title.replace("|", "/").strip(),
                "url": url,
                "company": company.replace("|", "/").strip(),
                "location": location.replace("|", "/").strip(),
                "note": note or f"via {path.name}",
                "family": classify(title, url),
                "origin": path.name,
            }
        )
    return rows


def next_version(path: Path, ver: int) -> Path:
    m = NAME_RE.match(path.name)
    assert m
    return path.with_name(f"{m.group('model')}--{m.group('date')}--v{ver + 1}.md")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--today", default=None)
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--max-per-table", type=int, default=60)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    today = date.fromisoformat(args.today) if args.today else datetime.now(timezone.utc).date()
    cutoff = today - timedelta(days=args.days)

    if not INBOX.exists():
        print("no inbox/ directory — nothing to merge")
        return 0

    submissions = [
        p
        for p in sorted(INBOX.glob("*.md"))
        if not p.name.startswith(("_", "TEMPLATE", "README"))
    ]
    if not submissions:
        print("inbox/ is empty — nothing to merge")
        return 0

    old_readme = README.read_text(encoding="utf-8")
    readme_rows, _ = extract_rows(old_readme)
    known = {normalise_url(r["url"]) for r in readme_rows}
    incoming: list[dict] = []
    per_file: dict[str, dict[str, int]] = {}

    for path in submissions:
        if not NAME_RE.match(path.name):
            print(f"skip {path.name}: name must be <model>--<YYYY-MM-DD>--v<N>.md")
            continue
        added = dup = bad = 0
        for row in parse_inbox_file(path):
            key = normalise_url(row["url"])
            if key in known:
                dup += 1
                continue
            known.add(key)
            incoming.append(row)
            added += 1
        per_file[path.name] = {"added": added, "duplicate": dup, "bad": bad}
        print(f"{path.name}: +{added} new, {dup} duplicate")

    merged = readme_rows + incoming
    unique, dropped = dedupe(merged)
    current = [r for r in unique if r["posted"] >= cutoff.isoformat()]
    expired = [r for r in unique if r["posted"] < cutoff.isoformat()]

    kept: list[dict] = []
    for key in ("servicenow", "salesforce", "other"):
        group = sorted((r for r in current if r["family"] == key), key=lambda r: r["posted"], reverse=True)
        kept.extend(group[: args.max_per_table])
        expired.extend(group[args.max_per_table :])
    current = sorted(kept, key=lambda r: r["posted"], reverse=True)
    counts = {k: sum(1 for r in current if r["family"] == k) for k in ("servicenow", "salesforce", "other")}

    print(f"\nincoming rows    : {len(incoming)}")
    print(f"total unique     : {len(unique)} (dupes merged: {dropped})")
    print(f"in {args.days}-day window: {len(current)}  {counts}")
    print(f"archiving        : {len(expired)} rows older than {cutoff.isoformat()}")

    if args.dry_run:
        for row in incoming[:15]:
            print(f"  will add [{row['family']}] {row['posted']} {row['title'][:60]} — {row['company'][:28]}")
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    archive_name = f"README.BAK_{stamp}.md"
    archive = [f"# Archived on {today.isoformat()}", "", f"Rows older than {cutoff.isoformat()}:"]
    archive.append("")
    archive.append("| Posted | Role | Company | Location | URL |")
    archive.append("|---|---|---|---|---|")
    for row in sorted(expired, key=lambda r: r["posted"], reverse=True):
        archive.append(
            f"| {row['posted']} | {row['title']} | {row['company']} | {row['location']} | {row['url']} |"
        )
    (ROOT / archive_name).write_text("\n".join(archive) + "\n", encoding="utf-8")

    doc = render(current, today, args.days, cutoff, archive_name)
    scan_block = extract_scan_block(old_readme)
    if scan_block:
        doc += (
            "## Automated feed (rewritten daily)\n\n"
            "Raw output of `npm run scan:daily`; it may repeat rows from the tables above.\n\n"
            + scan_block
            + "\n"
        )
    doc += (
        f"\n## Archive\n\n`{archive_name}` holds the rows that aged out of the "
        f"{args.days}-day window on {today.isoformat()}.\n"
    )
    README.write_text(doc, encoding="utf-8")
    print(f"wrote README.md with {len(current)} rows; archived {len(expired)} to {archive_name}")

    for path in submissions:
        m = NAME_RE.match(path.name)
        if not m:
            continue
        stats = per_file.get(path.name, {"added": 0, "duplicate": 0})
        target = next_version(path, int(m.group("ver")))
        header = (
            f"<!-- merged {stamp}: +{stats['added']} new, "
            f"{stats['duplicate']} duplicate, version {int(m.group('ver')) + 1} -->\n"
        )
        body = path.read_text(encoding="utf-8")
        if not body.startswith("<!-- merged"):
            body = header + body
        target.write_text(body, encoding="utf-8")
        path.unlink()
        print(f"bumped {path.name} -> {target.name}")

    if scan_start not in README.read_text(encoding="utf-8"):
        print("warning: DAILY-SCAN markers were not preserved; the scanner will re-insert at the top")
    return 0


if __name__ == "__main__":
    sys.exit(main())
