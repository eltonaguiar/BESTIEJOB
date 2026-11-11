#!/usr/bin/env python3
"""Repair posting rows whose table cells are structurally wrong.

Two shapes keep coming back from the scrapers, and both are invisible in a
rendered table — the row still looks like a row:

  * **split row** — a role title containing " / " was written unescaped, so the
    title split across two cells and the link tail was duplicated into the
    Company column: `[Staff Security Engineer \\/ Systems Engineering](url) |
    Systems Engineering](url) | ServiceNow | Toronto, ON`. 42 such rows shipped
    on 2026-11-11, all with the duplicated tail in cell 3. The repair drops the
    duplicated cell; the Role cell already carries the whole link.
  * **vendor sales row** — an Account Executive / Sales Director posting *at*
    ServiceNow or Salesforce. `config/agency_portals.json` excludes "vendor
    sales titles" and "a job at the product vendor"; nothing enforced it.

Everything else is left alone on purpose. Ambiguous locations, mirror
duplicates and the feed's scan-clock dates need a per-row decision, and
`scripts/board_invariants.py` reports them without touching the file.

Dry-run by default; `--apply` rewrites README.md.

Usage
    python3 scripts/repair_board_cells.py
    python3 scripts/repair_board_cells.py --apply
    python3 scripts/repair_board_cells.py --apply --drop-vendor-sales
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"

DATE_RE = re.compile(r"^\s*(\d{4}-\d{2}-\d{2})\s*$")
LINK_TAIL_RE = re.compile(r"\]\(https?://")
CELL_URL_RE = re.compile(r"\]\((https?://[^)\s]+)\)")

VENDOR_CO = re.compile(r"\bservice\s?now\b|\bsalesforce\b", re.I)
SALES_TITLE = re.compile(
    r"\b(account executive|account manager|sales director|sales representative|"
    r"sales executive|sales development|partner sales|pre-?sales|enterprise sales|"
    r"commercial account|sales manager|business development)\b", re.I)
# "Salesforce CPQ & Sales Cloud Developer" names a sales product, not a sales job.
ENG_TITLE = re.compile(
    r"\b(developer|engineer|architect|administrator|admin|analyst|consultant|"
    r"technical|qa|integration|implementation|specialist)\b", re.I)


# A markdown table escapes a pipe inside a cell as \| — splitting on the raw
# character turns `[Staff Security Engineer \| Enterprise Security](url)` into
# two cells whose first half has no link at all.
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")


def cells_of(line: str) -> list[str] | None:
    s = line.strip()
    if not s.startswith("|"):
        return None
    s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    cells = [c.strip() for c in CELL_SPLIT_RE.split(s)]
    return cells if len(cells) >= 3 else None


def is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c)


def rebuild(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def cell_url(cell: str) -> str:
    m = CELL_URL_RE.search(cell or "")
    return m.group(1).rstrip("/") if m else ""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--apply", action="store_true", help="rewrite README.md")
    ap.add_argument("--drop-vendor-sales", action="store_true",
                    help="also remove sales/exec rows at ServiceNow or Salesforce")
    ap.add_argument("--drop-kinds", default="",
                    help="comma list of board_invariants kinds to remove, e.g. "
                         "outside-window,vendor-sales")
    ap.add_argument("--readme", default=str(README))
    ap.add_argument("--show", type=int, default=8, help="examples printed per action")
    args = ap.parse_args()

    path = Path(args.readme)
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    repaired: list[tuple[int, str, str]] = []
    dropped: list[tuple[int, str, str]] = []
    unresolved: list[tuple[int, str]] = []

    for lineno, line in enumerate(lines, 1):
        cells = cells_of(line)
        if not cells or is_separator(cells) or not DATE_RE.match(cells[0].strip()):
            out.append(line)
            continue

        # 1. duplicated link tail from an unescaped pipe in the role title.
        #    Only drop the cell when the Role cell already carries that same link:
        #    on 2026-11-11 an unconditional drop silently stripped the only URL
        #    from 7 rows whose link lived in the trailing cell.
        if len(cells) >= 5 and LINK_TAIL_RE.search(cells[2]):
            if cell_url(cells[1]) and cell_url(cells[1]) == cell_url(cells[2]):
                fixed = [cells[0], cells[1]] + cells[3:]
                repaired.append((lineno, line, rebuild(fixed)))
                out.append(rebuild(fixed))
            else:
                unresolved.append((lineno, line))
                out.append(line)
            continue

        # 2. sales/exec role at the product vendor
        company = cells[2] if len(cells) > 2 else ""
        title_cell = cells[1]
        title = re.sub(r"^\[([^\]]*)\].*$", r"\1", title_cell)
        if (args.drop_vendor_sales and VENDOR_CO.search(company)
                and SALES_TITLE.search(title) and not ENG_TITLE.search(title)):
            dropped.append((lineno, title, company))
            continue

        out.append(line)

    for lineno, old, new in repaired[: args.show]:
        print(f"  repair line {lineno}\n    - {old[:150]}\n    + {new[:150]}")
    for lineno, title, company in dropped[: args.show]:
        print(f"  drop   line {lineno}: {title[:60]} | {company[:32]}")

    for lineno, line in unresolved[: args.show]:
        print(f"  leave  line {lineno}: {line[:160]}")

    pruned: list[tuple[str, str]] = []
    if args.drop_kinds:
        # The audit decides what violates a rule; this only applies its verdict to
        # the file, so a rule can never be enforced in one place and tolerated in
        # another. Rows leave with an archive, never silently.
        from datetime import date
        sys.path.insert(0, str(ROOT / "scripts"))
        from board_invariants import audit_readme, normalise_url, parse_readme
        kinds = {k.strip() for k in args.drop_kinds.split(",") if k.strip()}
        audited, _ = parse_readme(path)
        flagged = {normalise_url(f["url"]): f["kind"]
                   for f in audit_readme(audited, None, date.today())
                   if f["kind"] in kinds and f["url"]}
        keep: list[str] = []
        for line in out:
            m = CELL_URL_RE.search(line)
            kind = flagged.get(normalise_url(m.group(1))) if m else None
            if line.startswith("| 20") and kind:
                pruned.append((line, kind))
                continue
            keep.append(line)
        out = keep
        for line, kind in pruned[: args.show]:
            print(f"  prune  {kind}: {line[:140]}")
        if pruned:
            from datetime import datetime, timezone
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            (ROOT / f"README.PRUNED_{stamp}.md").write_text(
                "# Rows removed because board_invariants.py flagged them\n"
                f"# kinds: {', '.join(sorted(kinds))}\n\n"
                + "\n".join(line for line, _ in pruned) + "\n", encoding="utf-8")

    print(f"\nsplit rows repaired: {len(repaired)}")
    print(f"vendor sales rows dropped: {len(dropped)}")
    print(f"rows pruned by audit kind: {len(pruned)}")
    print(f"split rows left for a human: {len(unresolved)}")

    if not (repaired or dropped or pruned):
        print("nothing to repair")
        return 0

    if not args.apply:
        print("\n(dry-run — pass --apply to rewrite README.md)")
        return 0

    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"\nwrote {path} ({len(lines)} -> {len(out)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
