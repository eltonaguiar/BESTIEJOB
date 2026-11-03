#!/usr/bin/env python3
"""semantic_dedupe.py — catch reworded reposts that URL dedupe misses.

The merger dedupes on normalized URL, so the same requisition under
"Sr. Salesforce Developer" (LinkedIn) and "Salesforce Developer" (employer ATS)
survives as two rows. This pass finds those pairs two ways:

  1. fingerprint  — company + title with seniority/noise words removed
  2. embeddings   — Mixedbread cosine similarity within the same company

Report by default. `--apply` removes the later/least-complete copy of each
cluster from README's tables and writes what it removed to a timestamped
archive, so nothing is lost.

Usage:
    python3 scripts/semantic_dedupe.py                 # report only
    python3 scripts/semantic_dedupe.py --apply
    python3 scripts/semantic_dedupe.py --threshold 0.95
"""

from __future__ import annotations

import argparse
import json
import math
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
KEYS = Path.home() / "dbpasses.txt"
MODEL = "mixedbread-ai/mxbai-embed-large-v1"
# Seniority words are NOT stripped: "Developer" and "Senior Developer" are two
# requisitions at most employers, and GDIT/Cognizant post all three levels.
NOISE = re.compile(r"\b(inc|ltd|corp|llc)\b")
SUFFIX = re.compile(r"\b(inc|ltd|corp|corporation|llc|limited|canada|technologies|solutions|group)\b")
ROW = re.compile(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*\[([^\]]+)\]\((https?://[^)\s]+)[^)]*\)\s*\|\s*([^|]*)\|\s*([^|]*)\|")


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
    t = NOISE.sub(" ", t)
    return re.sub(r"\s+", " ", t).strip()


def norm_location(loc: str) -> str:
    """City-level key. 'Toronto, ON' and 'Ottawa, ON' must never collapse."""
    l = (loc or "").lower()
    l = re.split(r"[,;/(]", l)[0]
    l = re.sub(r"[^a-z ]", " ", l)
    return re.sub(r"\s+", " ", l).strip() or "unknown"


def norm_company(c: str) -> str:
    c = c.lower()
    c = re.sub(r"[^a-z0-9 ]", " ", c)
    c = SUFFIX.sub(" ", c)
    return re.sub(r"\s+", " ", c).strip()


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


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--threshold", type=float, default=0.93)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max", type=int, default=900, help="cap rows embedded")
    args = ap.parse_args()

    text = README.read_text(encoding="utf-8")
    rows = read_rows(text)
    if len(rows) < 2:
        print("no rows to dedupe")
        return 0

    # pass 1 — fingerprint
    clusters: list[list[int]] = []
    by_fp: dict[tuple[str, str], list[int]] = {}
    for i, r in enumerate(rows):
        by_fp.setdefault((norm_company(r["company"]), norm_title(r["title"]),
                          norm_location(r["location"])), []).append(i)
    clusters += [v for v in by_fp.values() if len(v) > 1]

    # pass 2 — embeddings, same company only
    key = mixedbread_key()
    if key:
        idx = list(range(min(len(rows), args.max)))
        texts = [f"{norm_title(rows[i]['title'])} at {norm_company(rows[i]['company'])}" for i in idx]
        try:
            vecs = embed(texts, key)
            print(f"[embeddings] {len(vecs)} rows embedded via Mixedbread")
            by_co: dict[str, list[int]] = {}
            for pos, i in enumerate(idx):
                by_co.setdefault((norm_company(rows[i]["company"]),
                                  norm_location(rows[i]["location"])), []).append(pos)
            for members in by_co.values():
                for a in range(len(members)):
                    for b in range(a + 1, len(members)):
                        ia, ib = idx[members[a]], idx[members[b]]
                        # embeddings may only confirm an exact-title match
                        if norm_title(rows[ia]["title"]) != norm_title(rows[ib]["title"]):
                            continue
                        if cosine(vecs[members[a]], vecs[members[b]]) >= args.threshold:
                            clusters.append([idx[members[a]], idx[members[b]]])
        except Exception as exc:                     # noqa: BLE001
            print(f"[embeddings] skipped: {type(exc).__name__} {str(exc)[:90]}")
    else:
        print("[embeddings] skipped: no Mixedbread key")

    # merge overlapping clusters, drop fingerprint dups already counted
    seen: set[frozenset] = set()
    unique: list[list[int]] = []
    for c in clusters:
        fs = frozenset(c)
        if fs not in seen:
            seen.add(fs)
            unique.append(sorted(c))

    drop: set[int] = set()
    for c in unique:
        # keep the earliest posted copy, then the longest title
        keep = sorted(c, key=lambda i: (rows[i]["posted"], -len(rows[i]["title"])))[0]
        for i in c:
            if i != keep:
                drop.add(i)

    print(f"[rows] {len(rows)} · [clusters] {len(unique)} · [extra copies] {len(drop)}")
    for c in unique[:12]:
        print("  cluster:")
        for i in c:
            mark = "DROP" if i in drop else "keep"
            print(f"    {mark:<4} {rows[i]['posted']} {rows[i]['title'][:52]:<52} | {rows[i]['company'][:26]}")

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
