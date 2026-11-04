#!/usr/bin/env python3
"""semantic_dedupe.py — catch the same posting listed under two URLs.

The merger dedupes on normalized URL, so one requisition that reaches the board
twice survives as two rows. The two real shapes of that duplicate:

    Take-Two Interactive / "ServiceNow ITOM Lead"   (aggregator URL)
    take2games           / "ServiceNow ITOM Lead"   (jobs.ashbyhq.com URL)

    Lightspeed Commerce  / "ServiceNow Developer"   (aggregator URL)
    lightspeedhq         / "ServiceNow Developer"   (jobs.ashbyhq.com URL)

Neither is a rewording: the titles are identical and the *employer label* is
what differs, because an ATS handle is not a company name. Matching therefore
lives in `tools/crossurl.py` and requires all of company, title, level and city
to agree -- see that module's docstring for why each guard exists.

Optional embeddings (`--embeddings`) rescue near-titles: "ServiceNow Platform
Engineer" and "Engineer, ServiceNow Platform" score below the token threshold
but are one job. Without a Mixedbread key the pass is simply skipped.

Report by default. `--apply` removes the redundant copy of each cluster from
README's tables and writes what it removed to a timestamped archive, so nothing
is lost.

Usage:
    python3 scripts/semantic_dedupe.py                 # report only
    python3 scripts/semantic_dedupe.py --apply
    python3 scripts/semantic_dedupe.py --embeddings
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from crossurl import (city, company_key, same_posting,            # noqa: E402
                     title_sim, TITLE_SIM)

README = ROOT / "README.md"
KEYS = Path.home() / "dbpasses.txt"
MODEL = "mixedbread-ai/mxbai-embed-large-v1"
ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*\[([^\]]+)\]\((https?://[^)\s]+)[^)]*\)\s*\|\s*([^|]*)\|\s*([^|]*)\|")

# Hosts that merely resell someone else's requisition. When two copies of one
# posting survive, keep the employer's own URL: it is the one that still works
# after the aggregator's listing expires.
AGGREGATOR = re.compile(
    r"linkedin\.com|indeed\.|adzuna|jobbank\.gc\.ca|glassdoor|ziprecruiter|"
    r"simplyhired|talent\.com|jooble|careerjet|dice\.com|monster\.com|"
    r"eluta|workopolis|jobillico|neuvoo|builtin\.com|jobrapido|trabajo|whatjobs", re.I)


def mixedbread_key() -> str | None:
    if not KEYS.exists():
        return None
    lines = KEYS.read_text(encoding="utf-8", errors="replace").splitlines()
    for i, line in enumerate(lines):
        if "mixedbread" in line.lower():
            for cand in [line.split(":", 1)[1] if ":" in line else ""] + \
                        [l.strip() for l in lines[i + 1:i + 6]]:
                c = cand.strip()
                if c and " " not in c and len(c) >= 20 and not c.endswith(":"):
                    return c
    return None


def norm_title(t: str) -> str:
    t = t.lower()
    t = re.sub(r"[^a-z0-9+#/ ]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def read_rows(text: str) -> list[dict]:
    rows = []
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if not m:
            continue
        posted, title, url, company, loc = m.groups()
        rows.append({"posted": posted, "title": title.strip(), "url": url,
                     "company": company.strip(), "location": loc.strip(), "line": line})
    return rows


def embed(texts: list[str], key: str) -> list[list[float]]:
    out: list[list[float]] = []
    for i in range(0, len(texts), 64):
        chunk = texts[i:i + 64]
        req = urllib.request.Request(
            "https://api.mixedbread.com/v1/embeddings",
            data=json.dumps({"model": MODEL, "input": chunk}).encode(),
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                     "User-Agent": "bestiejob-dedupe/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())
        out.extend(item["embedding"] for item in sorted(data["data"], key=lambda d: d["index"]))
    return out


def cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0


def is_direct(url: str) -> bool:
    return not AGGREGATOR.search(url or "")


def find_clusters(rows: list[dict], *, use_embeddings: bool,
                  threshold: float = 0.93) -> list[list[int]]:
    """Group row indices that describe one posting under different URLs.

    Bucketing by the first 4 chars of the company key keeps this O(n) in practice
    while still letting `company_match` accept an abbreviated label; the pairing
    test itself is always the full four-part check in crossurl.
    """
    buckets: dict[str, list[int]] = {}
    for i, r in enumerate(rows):
        k = company_key(r["company"])
        buckets.setdefault(k[:4] if len(k) >= 4 else k, []).append(i)

    vecs: dict[int, list[float]] = {}
    if use_embeddings and mixedbread_key():
        try:
            idx = list(range(min(len(rows), 1200)))
            out = embed([f"{norm_title(rows[i]['title'])}" for i in idx], mixedbread_key())
            vecs = dict(zip(idx, out))
            print(f"[embeddings] {len(vecs)} rows embedded via Mixedbread")
        except Exception as exc:                     # noqa: BLE001
            print(f"[embeddings] skipped: {type(exc).__name__} {str(exc)[:90]}")

    clusters: list[list[int]] = []
    for members in buckets.values():
        if len(members) < 2:
            continue
        for pos, ia in enumerate(members):
            for ib in members[pos + 1:]:
                a, b = rows[ia], rows[ib]
                if a["url"] == b["url"]:
                    continue          # merge-time URL dedupe already covers this
                if same_posting(a, b):
                    clusters.append([ia, ib])
                    continue
                # near-titles: same company + city, embeddings say one job
                if ia in vecs and ib in vecs and city(a["location"]) == city(b["location"]):
                    if (same_posting(a, b, title_sim_min=0.5)
                            and cosine(vecs[ia], vecs[ib]) >= threshold):
                        clusters.append([ia, ib])

    # collapse overlapping pairs into transitive clusters
    parent = list(range(len(rows)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for ia, ib in clusters:
        ra, rb = find(ia), find(ib)
        if ra != rb:
            parent[rb] = ra
    groups: dict[int, list[int]] = {}
    for pair in clusters:
        for i in pair:
            groups.setdefault(find(i), []).append(i)
    return [sorted(set(v)) for v in groups.values() if len(set(v)) > 1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=float, default=0.93,
                    help="cosine floor for the optional embedding rescue")
    ap.add_argument("--embeddings", action="store_true",
                    help="use Mixedbread to rescue near-titles (needs a key)")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max", type=int, default=1200, help="cap rows embedded")
    args = ap.parse_args()

    text = README.read_text(encoding="utf-8")
    rows = read_rows(text)
    if len(rows) < 2:
        print("no rows to dedupe")
        return 0

    unique = find_clusters(rows, use_embeddings=args.embeddings,
                           threshold=args.threshold)

    drop: set[int] = set()
    for c in unique:
        # Keep the FRESHEST copy, then the employer's own URL over an
        # aggregator's. Keeping the earliest (the old rule) threw away a role
        # reposted today in favour of its week-old duplicate, so the board
        # quietly lost exactly the rows a job seeker wants.
        keep = sorted(c, key=lambda i: (rows[i]["posted"] or "",
                                        is_direct(rows[i]["url"]),
                                        len(rows[i]["title"])), reverse=True)[0]
        for i in c:
            if i != keep:
                drop.add(i)

    direct_pairs = sum(1 for c in unique
                       if any(is_direct(rows[i]["url"]) for i in c)
                       and not all(rows[i]["url"].startswith("http") and is_direct(rows[i]["url"])
                                   for i in c))
    print(f"[rows] {len(rows)} · [clusters] {len(unique)} · [extra copies] {len(drop)}"
          f" · [resolve to an employer URL] {direct_pairs}")
    for c in unique[:15]:
        print("  cluster:")
        for i in c:
            mark = "DROP" if i in drop else "keep"
            tag = "ats" if is_direct(rows[i]["url"]) else "agg"
            print(f"    {mark:<4} {tag} {rows[i]['posted']} {rows[i]['title'][:44]:<44} | "
                  f"{rows[i]['company'][:22]:<22} | {rows[i]['location'][:16]}")

    (ROOT / "raw").mkdir(exist_ok=True)
    (ROOT / "raw" / "semantic_dupes.json").write_text(json.dumps(
        {"generated_at": datetime.now(timezone.utc).isoformat(),
         "rows": len(rows), "clusters": len(unique), "drop": len(drop),
         "pairs": [[{k: rows[i][k] for k in ("posted", "title", "company", "url")} for i in c]
                   for c in unique]}, indent=2), encoding="utf-8")

    if not args.apply or not drop:
        return 0

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    archive = ROOT / f"README.DEDUPE_{stamp}.md"
    archive.write_text("# Removed by semantic_dedupe " + stamp + "\n\n"
                       + "\n".join(rows[i]["line"] for i in sorted(drop)) + "\n", encoding="utf-8")
    keep_lines = [ln for ln in text.splitlines() if not any(ln == rows[i]["line"] for i in drop)]
    README.write_text("\n".join(keep_lines) + "\n", encoding="utf-8")
    print(f"[applied] removed {len(drop)} rows -> {archive.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
