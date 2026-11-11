#!/usr/bin/env python3
"""ats_date_resolve.py — read posting dates from ATS JSON endpoints.

Why this exists: ATS detail pages are client-rendered.  The page parser in
scripts/web_search_scan.py looks for ``datePosted`` / ``article:published_time``
in the HTML, and on Workday and SmartRecruiters pages that markup is assembled by
JavaScript, so genuinely fresh postings arrive undated and never reach the board.
Both vendors publish a public JSON document for the very same posting, from the
very same source, and it carries an absolute date.  Reading that document keeps
the board's rule intact — the date comes from the posting's own source.

    workday
        https://<tenant>.wd<N>.myworkdayjobs.com/[<locale>/]<site>/job/<path>
     -> https://<tenant>.wd<N>.myworkdayjobs.com/wday/cxs/<tenant>/<site>/job/<path>
        jobPostingInfo.startDate   "2026-11-09"        absolute
        jobPostingInfo.postedOn    "Posted Today"     relative, day named outright

    smartrecruiters
        https://jobs.smartrecruiters.com/<company>/<postingId>-<slug>
     -> https://api.smartrecruiters.com/v1/companies/<company>/postings/<postingId>
        releasedDate / createdOn   "2026-11-09T09:00:00.000Z"   absolute

Relative strings are refused unless they name the day ("Posted Today", "Posted
Yesterday").  "Posted 3 Days Ago" needs today's date from us to become a date,
which is exactly the inference this project forbids, so it returns None and the
row stays undated.

Usage
    python3 scripts/ats_date_resolve.py <url> [<url> ...]
    python3 scripts/ats_date_resolve.py --inbox inbox/websearch--2026-11-09--v1.md \
        --out inbox/websearch--2026-11-09--v2.md
    python3 scripts/ats_date_resolve.py --inbox inbox/x.md --json raw/ats_dates.json
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
MAX_AGE_DAYS = 45          # wider than the board's 31 so the resolver can report
TODAY = datetime.now(timezone.utc).date()


def _get_json(url: str, timeout: int = 15) -> dict | None:
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/json",
                      "Accept-Language": "en-CA,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            # Board lists are large (lever/eqbank: 198 KB) and a truncated read
            # looks like a JSON error, i.e. "no date" — read the whole body.
            return json.loads(resp.read())
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError,
            json.JSONDecodeError, OSError):
        return None


def _plausible(d: date) -> bool:
    """Reject a date the source could not mean: future, or older than the window."""
    return TODAY - timedelta(days=MAX_AGE_DAYS) <= d <= TODAY + timedelta(days=1)


def _iso(text: str) -> str | None:
    raw = (text or "").strip()
    if not raw:
        return None
    for parse in (lambda s: datetime.fromisoformat(s.replace("Z", "+00:00")).date(),
                  lambda s: datetime.strptime(s[:10], "%Y-%m-%d").date(),
                  lambda s: datetime.strptime(s, "%m/%d/%Y").date()):
        try:
            d = parse(raw)
        except (ValueError, TypeError):
            continue
        return d.isoformat() if _plausible(d) else None
    return None


# --------------------------------------------------------------------------- #
# Workday

WD_LOCALE = re.compile(r"^[a-z]{2}-[A-Za-z]{2}$")
WD_RELATIVE = {"posted today": 0, "posted yesterday": 1}


def _workday_parts(url: str) -> tuple[str, str, str, list[str]] | None:
    """(host, tenant, site, rest) for a Workday posting URL, else None."""
    u = urllib.parse.urlsplit(url)
    host = u.netloc.lower()
    if not host.endswith("myworkdayjobs.com"):
        return None
    tenant = host.split(".")[0]
    segs = [s for s in u.path.split("/") if s]
    if segs and WD_LOCALE.match(segs[0]):
        segs = segs[1:]                      # drop the locale prefix
    if len(segs) < 3 or segs[1] != "job":    # <site>/job/<location?>/<title>_<req>
        return None
    return host, tenant, urllib.parse.unquote(segs[0]), segs[1:]


def workday_date(url: str) -> str | None:
    parts = _workday_parts(url)
    if not parts:
        return None
    host, tenant, site, rest = parts
    api = (f"https://{host}/wday/cxs/{urllib.parse.quote(tenant)}/"
           f"{urllib.parse.quote(site)}/" + "/".join(rest))
    data = _get_json(api)
    if not data:
        return None
    info = data.get("jobPostingInfo") or data.get("jobRequisition") or {}
    # startDate is the absolute date Workday stores; postedOn is the label it
    # renders ("Posted Today"). Absolute wins whenever both are present.
    for key in ("startDate", "postedOn", "externalPostedDate"):
        value = info.get(key) or data.get(key)
        if not value:
            continue
        iso = _iso(str(value))
        if iso:
            return iso
        rel = WD_RELATIVE.get(str(value).strip().lower())
        if rel is not None:
            return (TODAY - timedelta(days=rel)).isoformat()
    return None


# --------------------------------------------------------------------------- #
# SmartRecruiters

SR_ID = re.compile(r"^(\d{5,})")


def smartrecruiters_date(url: str) -> str | None:
    u = urllib.parse.urlsplit(url)
    if not u.netloc.lower().endswith("smartrecruiters.com"):
        return None
    segs = [s for s in u.path.split("/") if s]
    if len(segs) < 2 or segs[0] == "company":
        return None
    company = segs[0]
    m = SR_ID.match(segs[1])
    if not m:
        return None
    api = (f"https://api.smartrecruiters.com/v1/companies/"
           f"{urllib.parse.quote(company)}/postings/{m.group(1)}")
    data = _get_json(api)
    if not data:
        return None
    for key in ("releasedDate", "createdOn", "updatedOn"):
        iso = _iso(str(data.get(key) or ""))
        if iso:
            return iso
    return None



# --------------------------------------------------------------------------- #
# Greenhouse / Lever / Ashby
#
# All three publish the posting as JSON for the very same job, exactly like
# Workday and SmartRecruiters, so the date still comes from the posting's own
# source. Their detail pages are client-rendered, which is why the HTML parser
# sees no `datePosted` on them at all -- measured 2026-11-11: 52 search
# candidates were discarded as undated before these resolvers existed.

GH_URL = re.compile(r"(?:boards|job-boards)\\.greenhouse\\.io/([^/?#]+)/jobs/(\\d+)")
LEVER_URL = re.compile(r"jobs\\.lever\\.co/([^/?#]+)/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})")
ASHBY_URL = re.compile(r"jobs\\.ashbyhq\\.com/([^/?#]+)/([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})")

# Per-job detail endpoints 404 for boards that moved hosts or archived a posting
# (measured 2026-11-11: 3 of 3 greenhouse and lever detail calls returned 404),
# so each board is read once through its list endpoint and indexed by posting id.
_BOARD: dict[tuple[str, str], dict[str, str]] = {}


def _board_index(kind: str, name: str) -> dict[str, str]:
    key = (kind, name)
    if key in _BOARD:
        return _BOARD[key]
    index: dict[str, str] = {}
    if kind == "greenhouse":
        data = _get_json(f"https://boards-api.greenhouse.io/v1/boards/{name}/jobs?content=false")
        for job in (data or {}).get("jobs") or []:
            iso = _iso(str(job.get("first_published") or ""))
            if iso and job.get("id") is not None:
                index[str(job["id"])] = iso
    elif kind == "lever":
        data = _get_json(f"https://api.lever.co/v0/postings/{name}?mode=json")
        for job in data if isinstance(data, list) else []:
            created = job.get("createdAt") or job.get("created_at") or job.get("publishedAt")
            iso = None
            if isinstance(created, (int, float)) and created > 0:
                d = datetime.fromtimestamp(created / 1000, tz=timezone.utc).date()
                iso = d.isoformat() if _plausible(d) else None
            elif isinstance(created, str):
                iso = _iso(created)
            if iso and job.get("id"):
                index[str(job["id"])] = iso
    elif kind == "ashby":
        data = _get_json(f"https://api.ashbyhq.com/posting-api/job-board/{name}")
        for job in (data or {}).get("jobs") or []:
            iso = _iso(str(job.get("publishedAt") or ""))
            if iso and job.get("id"):
                index[str(job["id"])] = iso
    _BOARD[key] = index
    return index


def greenhouse_date(url: str) -> str | None:
    m = GH_URL.search(url)
    if not m:
        return None
    board, job_id = m.groups()
    got = _board_index("greenhouse", board).get(str(job_id))
    if got:
        return got
    data = _get_json(f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs/{job_id}")
    # `updated_at` is an edit timestamp and is never used as a posting date.
    return _iso(str((data or {}).get("first_published") or ""))


def lever_date(url: str) -> str | None:
    m = LEVER_URL.search(url)
    if not m:
        return None
    company, posting_id = m.groups()
    got = _board_index("lever", company).get(str(posting_id))
    if got:
        return got
    data = _get_json(f"https://api.lever.co/v0/postings/{company}/{posting_id}")
    created = (data or {}).get("createdAt")
    if isinstance(created, (int, float)) and created > 0:
        d = datetime.fromtimestamp(created / 1000, tz=timezone.utc).date()
        return d.isoformat() if _plausible(d) else None
    return None


def ashby_date(url: str) -> str | None:
    m = ASHBY_URL.search(url)
    if not m:
        return None
    org, job_id = m.groups()
    return _board_index("ashby", org).get(str(job_id))

# --------------------------------------------------------------------------- #
# public API used by scripts/web_search_scan.py

_CACHE: dict[str, str | None] = {}
RESOLVERS = (("workday", workday_date), ("smartrecruiters", smartrecruiters_date),
             ("greenhouse", greenhouse_date), ("lever", lever_date),
             ("ashby", ashby_date))


def resolve(url: str) -> str | None:
    """ISO posting date from the posting's own ATS JSON, or None."""
    if url in _CACHE:
        return _CACHE[url]
    _CACHE[url] = None
    for _name, fn in RESOLVERS:
        try:
            got = fn(url)
        except Exception:                    # noqa: BLE001 — a resolver must never abort a scan
            got = None
        if got:
            _CACHE[url] = got
            return got
    return None


def resolve_many(urls: list[str], workers: int = 4) -> dict[str, str | None]:
    with futures.ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(zip(urls, ex.map(resolve, urls)))


# --------------------------------------------------------------------------- #
# inbox rewriting

ROW = re.compile(r"^\|\s*(?P<posted>[^|]*?)\s*\|(?P<rest>.*)$")


def rewrite_inbox(path: Path, out: Path, workers: int, only_undated: bool = True) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    targets, urls = [], []
    for i, line in enumerate(lines):
        m = ROW.match(line)
        if not m or not line.startswith("| "):
            continue
        cell = m.group("posted").strip()
        if cell in ("Posted", ":---", "--------", "---"):
            continue
        if only_undated and cell not in ("—", "-", ""):
            continue
        found = re.search(r"https?://[^\s)|]+", line)
        if not found:
            continue
        targets.append(i)
        urls.append(found.group(0).rstrip(".,"))
    dates = resolve_many(urls, workers=workers) if urls else {}
    filled = 0
    for i, url in zip(targets, urls):
        iso = dates.get(url)
        if not iso:
            continue
        m = ROW.match(lines[i])
        lines[i] = f"| {iso} |{m.group('rest')}"
        filled += 1
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"rows_scanned": len(urls), "dated": filled, "undated": len(urls) - filled,
            "out": str(out)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--inbox", help="inbox markdown table to fill in")
    ap.add_argument("--out", help="where to write the rewritten inbox")
    ap.add_argument("--json", help="write {url: date} JSON here")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()

    if args.inbox:
        src = Path(args.inbox)
        out = Path(args.out) if args.out else src.with_name(
            f"{src.stem}-dated{src.suffix}")
        summary = rewrite_inbox(src, out, args.workers)
        print(f"[ats] {summary['dated']} of {summary['rows_scanned']} undated rows resolved "
              f"-> {summary['out']}")
        return 0

    if not args.urls:
        ap.print_help()
        return 2
    dates = resolve_many(args.urls, workers=args.workers)
    for url, iso in dates.items():
        print(f"{iso or '—':12} {url}")
    if args.json:
        Path(args.json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json).write_text(json.dumps(dates, indent=2), encoding="utf-8")
    print(f"[ats] {sum(1 for v in dates.values() if v)}/{len(dates)} resolved", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
