#!/usr/bin/env python3
"""verify_jobs.py — the live + unique gate for candidate postings.

The user's requirement is not "HTTP 200". It is:

    legit postings -> verified live -> verified unique -> posted to BESTIEJOB

So a candidate survives only if all three hold:

  1. LIVE    the URL returns 200 (after redirects) and the page body still
             contains the posting's own title. A 200 on a "this job no longer
             exists" shell page is a false pass; the title check catches it.
  2. UNIQUE  no earlier survivor is the same posting under another URL, judged
             by crossurl.same_posting() (alias-aware company + title overlap +
             seniority + city), which is the only catch for one requisition
             arriving under an employer label and an ATS handle.
  3. ON-BOARD-NOT  the posting is not already in README.md, the database.
             board_rows() reads README because jobs-data.json only holds a
             recent window.

Usage:
    python3 tools/verify_jobs.py <input.json> <output.json> [--apply]

    without --apply  -> report only, writes <output.json> with survivors
    with    --apply  -> also write survivors as an inbox markdown table
"""

from __future__ import annotations

import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from crossurl import company_key, same_posting  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
INBOX = ROOT / "inbox"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Words too common to prove a title is on the page.
WEAK = frozenset("""
the and of for a an at in on with senior junior lead principal staff
developer administrator admin engineer analyst consultant specialist
manager remote canada canadian contract
""".split())


def title_signature(title: str) -> list[str]:
    """The distinctive words of a title, longest first. Empty means 'cannot check'."""
    words = re.findall(r"[A-Za-z0-9+#]{4,}", (title or "").lower())
    keep = [w for w in words if w not in WEAK]
    # Fall back to all words when the title is nothing but weak ones.
    return sorted(keep or words, key=len, reverse=True)


def check_live(row: dict, timeout: int = 25) -> tuple[bool, str]:
    """200 AND the posting's own title is still on the page."""
    url = (row.get("url") or "").strip()
    if not url:
        return False, "no url"
    headers = {"User-Agent": UA, "Accept-Language": "en-CA,en;q=0.9"}
    try:
        r = requests.get(url, headers=headers, timeout=timeout,
                         allow_redirects=True)
    except Exception as e:                                  # noqa: BLE001
        return False, f"{type(e).__name__}"
    if r.status_code != 200:
        return False, f"http {r.status_code}"
    body = (r.text or "").lower()
    if not body:
        return False, "empty body"

    # Hard "this posting is gone" markers that some ATS still serve with 200.
    for marker in ("no longer accepting applications",
                   "position has been filled",
                   "this job is no longer available",
                   "job posting has expired",
                   "this posting is closed"):
        if marker in body:
            return False, f"gone: {marker}"

    sig = title_signature(row.get("title", ""))
    if sig and not any(w in body for w in sig):
        return False, "title absent"
    return True, "ok"


def load_candidates(path: Path) -> list[dict]:
    """Accept a flat list, or the dict-of-lists shape scanners emit."""
    data = json.loads(path.read_text(encoding="utf-8"))
    rows: list[dict] = []
    if isinstance(data, dict):
        for value in data.values():
            if isinstance(value, list):
                rows.extend(r for r in value if isinstance(r, dict))
    elif isinstance(data, list):
        rows = [r for r in data if isinstance(r, dict)]
    return rows


def board_rows() -> list[dict]:
    """Rows already on the board, parsed from README.md (the database)."""
    if not README.exists():
        return []
    link = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
    out = []
    for line in README.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.startswith("|"):
            continue
        m = link.search(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        out.append({
            "posted": cells[0],
            "title": m.group(1).strip(),
            "company": cells[2] if len(cells) > 2 else "",
            "location": cells[3] if len(cells) > 3 else "",
            "url": m.group(2).strip(),
        })
    return out


def normalise_url(u: str) -> str:
    return re.sub(r"[?#].*$", "", (u or "").strip().rstrip("/")).lower()


def dedupe(rows: list[dict], known: list[dict]) -> tuple[list[dict], list[str]]:
    """Split rows into (survivors, notes). Rejects URL repeats and same-posting."""
    known_urls = {normalise_url(r["url"]) for r in known}
    survivors: list[dict] = []
    notes: list[str] = []
    for row in rows:
        u = normalise_url(row.get("url"))
        if u in known_urls:
            notes.append(f"already on board: {row.get('title')} / {row.get('company')}")
            continue
        hit = next((r for r in known
                    if same_posting({"company": r["company"], "title": r["title"],
                                     "location": r["location"]}, row)), None)
        if hit:
            notes.append(f"already on board (cross-URL): {row.get('title')} / "
                         f"{row.get('company')} ~ {hit['title']} / {hit['company']}")
            continue
        hit = next((r for r in survivors if same_posting(r, row)), None)
        if hit:
            notes.append(f"duplicate of candidate: {row.get('title')} / "
                         f"{row.get('company')} ~ {hit.get('title')} / {hit.get('company')}")
            continue
        survivors.append(row)
    return survivors, notes


def write_inbox(rows: list[dict], day: str) -> Path:
    INBOX.mkdir(exist_ok=True)
    n = 1
    while (INBOX / f"verified--{day}--v{n}.md").exists():
        n += 1
    path = INBOX / f"verified--{day}--v{n}.md"
    lines = [
        "---",
        "model: verified",
        f"scanned_at: {datetime.now(timezone.utc).isoformat()}",
        "task: live-url-title-dedupe-gate",
        f"rows: {len(rows)}",
        "---",
        "",
        f"# Verified new postings — {day}",
        "",
        "| Posted | Role | Company | Location | URL |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r.get('posted') or r.get('date') or day} "
            f"| [{r.get('title','')}]({r.get('url','')}) "
            f"| {r.get('company','')} | {r.get('location','')} "
            f"| {r.get('url','')} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    if len(args) < 2:
        print(__doc__)
        return 2
    src, out = Path(args[0]), Path(args[1])
    if not src.exists():
        print(f"input not found: {src}")
        return 1

    cands = load_candidates(src)
    print(f"candidates: {len(cands)}")

    # URL-level pre-dedupe before spending network calls.
    seen, uniq = set(), []
    for c in cands:
        u = normalise_url(c.get("url"))
        if u and u not in seen:
            seen.add(u)
            uniq.append(c)
    print(f"unique by url: {len(uniq)}")

    print(f"checking targets: {len(uniq)} (200 + title present)")
    with ThreadPoolExecutor(max_workers=10) as pool:
        results = list(pool.map(check_live, uniq))

    live = []
    for row, (ok, why) in zip(uniq, results):
        if ok:
            live.append(row)
        else:
            print(f"  DEAD  {why:<28} {(row.get('title') or '')[:56]}")
    print(f"live: {len(live)}")

    known = board_rows()
    print(f"board rows (README): {len(known)}")
    survivors, notes = dedupe(live, known)
    for n in notes:
        print(f"  SKIP  {n}")
    print(f"NEW: {len(survivors)}")

    out.write_text(json.dumps(survivors, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    print(f"wrote {out}")

    for r in survivors:
        print(f"  {r.get('posted') or r.get('date') or '?'}  "
              f"{(r.get('company') or '')[:30]:<30}  {(r.get('title') or '')[:60]}")

    if apply:
        if survivors:
            day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            path = write_inbox(survivors, day)
            print(f"wrote {path} ({len(survivors)} rows)")
        else:
            print("nothing to write (0 survivors)")
    return 0


if __name__ == "__main__":
    sys.exit(main())