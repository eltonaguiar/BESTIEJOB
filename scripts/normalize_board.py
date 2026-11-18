#!/usr/bin/env python3
"""Remove rows that break the board's published rules — in all three places they live.

Why
---
`board_invariants` ratchets six kinds. Four of them are rows that should never
have been published, not heuristics needing a judgement call:

  non-canada       location is explicitly outside Canada
  outside-window   posted before the 30-day window the dated tables promise
  vendor-sales     sales/exec role at the product vendor (ServiceNow/Salesforce)
  split-row        a link leaked into the Company/Location cell — unreadable row
  placeholder-cell Company/Role cell holds scraper bookkeeping

(`location-ambiguous` and `identity-date-conflict` are handled elsewhere: the
first is a bug in the gate's own pattern, the second is a heuristic, not a
promise. Neither is a data purge.)

Deleting a README row alone does nothing: `hourly-scan` re-merges `inbox/` into
the board every hour and rebuilds `jobs.json` from it, so the row comes back
within 60 minutes. This script therefore removes each row from

  README.md          the published dated tables
  jobs.json          the machine-readable board
  inbox/*.md         the source rows the merge re-reads

and then rewrites the "**N live postings**" header so the count promise holds.

Usage
-----
    python3 scripts/normalize_board.py                 # dry run, prints the plan
    python3 scripts/normalize_board.py --apply         # rewrite the three places
    python3 scripts/normalize_board.py --apply --only non-canada,outside-window

Exit: 0 = nothing to do or applied cleanly; 1 = dry run found work (useful in CI
as a "the board has debt" signal); 2 = refused (safety check failed).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import board_invariants as B  # noqa: E402  (the gate's own parser, by design)

# Kinds this script is allowed to purge. Deliberately excludes the two
# judgement kinds so a purge can never quietly decide them.
PURGEABLE = ("non-canada", "outside-window", "vendor-sales", "split-row", "placeholder-cell")


def readme_paths() -> tuple[Path, Path, Path]:
    return ROOT / "README.md", ROOT / "jobs.json", ROOT / "inbox"


def plan(only: tuple[str, ...]) -> dict:
    readme, jobs_json, inbox = readme_paths()
    rows, claimed = B.parse_readme(readme)
    findings = B.audit_readme(rows, claimed, date.today())

    doomed: dict[str, list[dict]] = defaultdict(list)
    for f in findings:
        if f["kind"] in only:
            doomed[f["kind"]].append(f)

    # A row can break several rules; drop it once.
    by_line: dict[int, dict] = {}
    for kind, fs in doomed.items():
        for f in fs:
            if f.get("line"):
                by_line.setdefault(int(f["line"]), f)
    urls = {B.normalise_url(f["url"]) for fs in doomed.values() for f in fs if f.get("url")}

    # How much of this debt is re-creatable: a pruned README row that still sits
    # in inbox/ returns on the next hourly merge, which is why the inbox is pruned too.
    in_inbox = Counter()
    inbox_files: list[Path] = []
    if inbox.is_dir():
        for p in sorted(inbox.glob("*.md")):
            text = p.read_text(encoding="utf-8", errors="replace")
            hits = sum(1 for link in B.LINK_RE.findall(text)
                       if B.normalise_url(link[1]) in urls)
            if hits:
                in_inbox[p.name] = hits
                inbox_files.append(p)

    return {
        "readme_rows": len(rows),
        "claimed": claimed,
        "findings": Counter(f["kind"] for f in findings),
        "doomed": doomed,
        "rows": list(by_line.values()),
        "lines": sorted(by_line),
        "urls": urls,
        "inbox_hits": in_inbox,
        "inbox_files": inbox_files,
    }


def _strip_readme(lines: list[str], drop: set[int]) -> list[str]:
    return [ln for i, ln in enumerate(lines, start=1) if i not in drop]


def _sync_count() -> None:
    """Rewrite the header claim with the script that already owns that job."""
    import subprocess

    subprocess.run([sys.executable, str(ROOT / "scripts" / "sync_readme_counts.py")],
                   check=True, capture_output=True, text=True)


def _prune_jobs_json(urls: set[str]) -> tuple[int, int]:
    readme, jobs_json, _ = readme_paths()
    data = json.loads(jobs_json.read_text(encoding="utf-8"))
    rows = data if isinstance(data, list) else data.get("jobs") or data.get("postings") or []
    kept = [r for r in rows if not (isinstance(r, dict) and B.normalise_url(str(r.get("url", ""))) in urls)]
    removed = len(rows) - len(kept)
    if removed:
        if isinstance(data, list):
            payload = kept
        else:
            key = "jobs" if data.get("jobs") is not None else "postings"
            data[key] = kept
            payload = data
        # indent=2 / ensure_ascii=False / no trailing newline is the format this
        # file already used; matching it keeps the diff to the rows removed.
        jobs_json.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return len(rows), removed


def _is_dated_row(line: str) -> bool:
    if not line.startswith("|") or line.count("|") < 5:
        return False
    return bool(B.DATE_RE.match(line.split("|")[1].strip()))


def _prune_inbox(urls: set[str], files: list[Path]) -> int:
    """Remove matching rows from the inbox files the hourly merge re-reads."""
    removed = 0
    for p in files:
        out: list[str] = []
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True):
            if _is_dated_row(line):
                links = B.LINK_RE.findall(line)
                if links and B.normalise_url(links[0][1]) in urls:
                    removed += 1
                    continue
            out.append(line)
        p.write_text("".join(out), encoding="utf-8")
    return removed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="rewrite README.md, jobs.json and inbox/ (default: dry run)")
    ap.add_argument("--only", default=",".join(PURGEABLE),
                    help=f"comma-separated kinds (default all purgeable: {','.join(PURGEABLE)})")
    ap.add_argument("--json", action="store_true", help="machine-readable plan/summary")
    ns = ap.parse_args(argv)

    only = tuple(k.strip() for k in ns.only.split(",") if k.strip())
    unknown = [k for k in only if k not in PURGEABLE]
    if unknown:
        print(f"refusing: {unknown} is not purgeable by this script (see PURGEABLE)", file=sys.stderr)
        return 2

    p = plan(only)
    summary = {
        "before": dict(p["findings"]),
        "readme_rows": p["readme_rows"],
        "claimed": p["claimed"],
        "rows_to_drop": len(p["rows"]),
        "per_kind": {k: len(v) for k, v in p["doomed"].items()},
        "inbox_files_with_matches": dict(p["inbox_hits"]),
        "applied": bool(ns.apply),
    }

    if ns.json:
        print(json.dumps({**summary, "sample": p["rows"][:5]}, indent=2, default=str))
    else:
        print(f"README rows: {p['readme_rows']} (header claims {p['claimed']})")
        print(f"rows to drop: {len(p['rows'])}")
        for k in sorted(p["doomed"]):
            print(f"  {k:20} {len(p['doomed'][k]):5} finding(s)")
        if p["inbox_hits"]:
            n = sum(p["inbox_hits"].values())
            print(f"inbox rows that would re-create them: {n} across {len(p['inbox_hits'])} file(s) "
                  f"(e.g. {', '.join(list(p['inbox_hits'])[:3])})")
        else:
            print("inbox: no source rows matched (nothing would come back next hour)")
        for r in p["rows"][:5]:
            print(f"  drop L{r['line']}: {r['posted']} | {r['title'][:52]} | {r['location'][:34]} | {r['kind'] if 'kind' in r else ''}")

    if not ns.apply:
        if p["rows"]:
            if not ns.json:
                print("\ndry run — re-run with --apply to rewrite README.md, jobs.json and inbox/")
            return 1
        print("nothing to do")
        return 0

    readme, _, _ = readme_paths()
    lines = readme.read_text(encoding="utf-8").splitlines()
    new_lines = _strip_readme(lines, set(p["lines"]))
    readme.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
    _sync_count()
    after = len(B.parse_readme(readme)[0])
    j_before, j_removed = _prune_jobs_json(p["urls"])
    i_removed = _prune_inbox(p["urls"], p["inbox_files"])

    if not ns.json:
        print(f"normalize: removed={p['readme_rows'] - after} rows")  # parsed by hourly-scan
        print(f"\napplied: README {p['readme_rows']} -> {after} rows")
        print(f"         jobs.json {j_before} -> {j_before - j_removed} rows")
        print(f"         inbox {i_removed} row(s) removed from {len(p['inbox_files'])} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
