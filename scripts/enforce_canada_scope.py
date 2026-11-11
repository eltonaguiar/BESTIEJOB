#!/usr/bin/env python3
"""enforce_canada_scope.py — settle what "Toronto-first" means for the board.

The board is a Canadian market board, and its rules say the location must come
from the posting rather than from the search scope. 1,137 rows named a location
that is explicitly outside Canada — `Remote, USA`, `Bengaluru`, `Remote - US`,
US states — and none of them named Canada. They arrived because a "Canada" search
returned them, which is precisely the failure the rule describes.

Policy applied here, in order (the classifier lives in `tools/locscope.py` so
this purge and `scripts/board_invariants.py` cannot disagree):

  1. A location that names Canada (country, province, or a Canadian city) is
     eligible, wherever else it also mentions.
  2. A location that names no country and no Canadian province is **kept** and
     stays `location-ambiguous`: absent evidence is not evidence of absence.
  3. A location that names a non-Canadian country, US state or US shorthand, and
     never names Canada, is **not board-eligible**.

Before removing anything the script looks for a Canadian sibling: the same
company + title already on the board in Canada. When one exists, the foreign copy
duplicates a role we keep and is dropped for that reason; otherwise the row is out
of scope. Both are counted separately.

Every removed row is archived (`README.NONCANADA_<stamp>.md` and
`raw/canada_scope_<date>.json`), and the feed loses the same URLs so the built
site cannot show them again.

Usage
    python3 scripts/enforce_canada_scope.py             # report only
    python3 scripts/enforce_canada_scope.py --apply
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
from board_invariants import parse_readme, normalise_url   # noqa: E402
from locscope import is_canadian, is_foreign, region_of    # noqa: E402


def identity(row: dict) -> str:
    squash = lambda s: " ".join(re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).split())
    return f"{squash(row['company'])}|{squash(row['title'])}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", default=str(ROOT))
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    root = Path(args.repo)

    rows, _claimed = parse_readme(root / "README.md")
    foreign = [{**r, "region": region_of(r["location"])}
               for r in rows if r["location"] and is_foreign(r["location"])]

    canadian_ids = {identity(r) for r in rows
                    if not r["location"] or is_canadian(r["location"])}
    dup_urls = {f["url"] for f in foreign if identity(f) in canadian_ids}
    out_of_scope = [f for f in foreign if f["url"] not in dup_urls]

    print(f"README rows: {len(rows)}")
    print(f"explicitly non-Canadian: {len(foreign)}")
    print(f"  dropped as a duplicate of a Canadian row: {len(dup_urls)}")
    print(f"  out of scope outright:                   {len(out_of_scope)}")
    print(f"kept with no country named (ambiguous):  "
          f"{sum(1 for r in rows if r['location'] and not region_of(r['location']))}")
    print("by region:", dict(Counter(f["region"] for f in foreign).most_common(12)))
    for f in foreign[:6]:
        print(f"  {f['posted']} | {f['location'][:32]:32} | {f['title'][:40]:40} | "
              f"{f['company'][:20]}")

    if not args.apply or not foreign:
        if not args.apply:
            print("\ndry run — pass --apply to write")
        return 0

    keys = {normalise_url(f["url"]) for f in foreign}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    archive = root / f"README.NONCANADA_{stamp}.md"
    archive.write_text(
        "# Rows removed by enforce_canada_scope.py\n"
        "# policy: the location comes from the posting, and the board is Canadian\n"
        f"# removed: {len(foreign)} rows at {datetime.now(timezone.utc).isoformat()}\n\n"
        + "\n".join(f"| {f['posted']} | [{f['title']}]({f['url']}) | {f['company']} | "
                    f"{f['location']} | {f['region']} |" for f in foreign) + "\n",
        encoding="utf-8")

    readme = root / "README.md"
    kept, dropped = [], 0
    for line in readme.read_text(encoding="utf-8").splitlines():
        m = re.search(r"\((https?://[^)\s]+)\)", line)
        if line.startswith("| 20") and m and normalise_url(m.group(1)) in keys:
            dropped += 1
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

    report = {"generatedAt": datetime.now(timezone.utc).isoformat(),
              "readmeRows": len(rows), "excluded": len(foreign),
              "duplicateOfCanadianRow": len(dup_urls), "outOfScope": len(out_of_scope),
              "byRegion": dict(Counter(f["region"] for f in foreign)),
              "readmeLinesRemoved": dropped, "feedRows": [before, len(jobs)],
              "archive": archive.name,
              "rows": [{k: f[k] for k in ("posted", "title", "company", "location",
                                          "url", "region")} for f in foreign]}
    raw = root / "raw"
    raw.mkdir(exist_ok=True)
    (raw / f"canada_scope_{datetime.now(timezone.utc).date().isoformat()}.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8")
    print(f"\nremoved: README lines {dropped} · feed rows {before} -> {len(jobs)}")
    print(f"archive: {archive.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
