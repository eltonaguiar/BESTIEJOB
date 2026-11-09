#!/usr/bin/env python3
"""Drop dead postings from jobs.json (and the three public copies) before the page build.

Quality gate for the hourly scan. A posting URL that returns 404/410 is gone: the
employer closed it, the aggregator removed it, or the board rotated it. Those must not
render on the site — a job-seeker who clicks a dead link loses trust in the whole board
(e.g. the jobs.ca Brookfield "ServiceNow Developer (Contract)" link was removed from
jobs.ca and still sat at the top of the ServiceNow table, 2026-11-09).

What counts as dead: HTTP 404, 410, and 451 only. A 403 / 429 / 999 / 5xx is NOT dead —
LinkedIn, Indeed, Workday and most ATS boards bot-wall a headless prober while the
posting is perfectly live for a browser, so treating those as dead would delete real
jobs. A transport error (timeout, DNS) is also NOT dead: it is unknown, and an unknown
posting is kept (worst case it is one stale row; deleting a live job is worse).

Verification scope: only rows posted within the last `--days` (default 2) so an hourly
run probes tens of links, not thousands. `--all` checks every row. Rows that a prior run
already verified live within `--recheck-hours` are skipped (a `verifiedAt` stamp), so the
same fresh rows are not re-probed every hour.

Usage:
    python3 tools/verify_links.py                 # last 2 days, drop 404/410/451
    python3 tools/verify_links.py --days 4
    python3 tools/verify_links.py --all --workers 24
    python3 tools/verify_links.py --dry-run       # report only, write nothing
    python3 tools/verify_links.py --blocklist dead_urls.txt   # also append dead urls
"""
from __future__ import annotations

import argparse
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [
    ROOT / "jobs.json",
    ROOT / "public" / "jobs.json",
    ROOT / "public" / "gotjob" / "jobs.json",
    ROOT / "public" / "findjobs" / "jobs.json",
]

DEAD_CODES = {404, 410, 451}
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
# Hosts that bot-wall a plain HTTP probe while the posting is live for a browser.
# Never mark these dead on a status code — only a transport failure, and even then keep.
BOT_WALL_OK = re.compile(
    r"(^|\.)(linkedin\.com|indeed\.[a-z.]+|glassdoor\.[a-z.]+|ziprecruiter\.com|"
    r"wellfound\.com|workday\.com|myworkdayjobs\.com|greenhouse\.io|lever\.co|"
    r"smartrecruiters\.com|ashbyhq\.com|icims\.com|taleo\.net|successfactors\.com|"
    r"dice\.com|monster\.com|careerbuilder\.com|jobs\.ca|eluta\.ca|workopolis\.com|"
    r"talent\.com|jooble\.org|whatjobs\.com|careerbeacon\.com|builtin\.com)$",
    re.I,
)


def _ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _host(url: str) -> str:
    m = re.match(r"https?://([^/?#]+)", url or "")
    return (m.group(1).lower().removeprefix("www.") if m else "")


def _probe(url: str, timeout: float) -> tuple[str, str]:
    """Return (verdict, detail) where verdict is 'live' | 'dead' | 'unknown'."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": UA, "Accept": "text/html,*/*",
                "Accept-Language": "en-CA,en;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as resp:
                return "live", f"{resp.status}"
        except urllib.error.HTTPError as e:
            code = e.code
            if code in DEAD_CODES:
                return "dead", f"{code}"
            # Redirect chains ending in a bot-wall/401 etc. are live-enough.
            if code in (301, 302, 303, 307, 308):
                continue
            return "unknown", f"{code}"
        except urllib.error.URLError as e:
            # TLS cert problems and DNS are unknown, not dead.
            if "CERTIFICATE" in str(e).upper() or "SSL" in str(e).upper():
                return "unknown", "tls"
            return "unknown", f"urlerr:{type(e.reason).__name__ if hasattr(e,'reason') else e}"
        except Exception:
            return "unknown", "exc"
    return "unknown", "redirect"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2, help="only verify rows posted within N days")
    ap.add_argument("--all", action="store_true", help="verify every row")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--timeout", type=float, default=12.0)
    ap.add_argument("--recheck-hours", type=float, default=6.0,
                    help="skip rows verified live within N hours")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--blocklist", default=None, help="append dead urls to this path")
    ap.add_argument("--report-json", default=None)
    args = ap.parse_args()

    jobs_path = TARGETS[0]
    if not jobs_path.exists():
        print("verify: jobs.json missing", file=sys.stderr)
        return 1
    payload = json.loads(jobs_path.read_text(encoding="utf-8"))
    jobs = payload.get("jobs", []) if isinstance(payload, dict) else payload

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=args.days)
    fresh_cutoff = now - timedelta(hours=args.recheck_hours)

    to_check: list[dict] = []
    for j in jobs:
        url = (j.get("url") or "").strip()
        if not url.startswith("http"):
            continue
        if not args.all:
            posted = (j.get("postedDate") or "")[:19]
            try:
                posted_dt = datetime.fromisoformat(posted.replace("Z", "+00:00"))
            except ValueError:
                posted_dt = None
            if posted_dt is not None:
                if posted_dt.tzinfo is None:
                    posted_dt = posted_dt.replace(tzinfo=timezone.utc)
                if posted_dt < cutoff:
                    continue
        va = j.get("verifiedAt")
        if va:
            try:
                if datetime.fromisoformat(va.replace("Z", "+00:00")) > fresh_cutoff:
                    continue
            except ValueError:
                pass
        # Browser-bot-wall hosts: skip unless we have no verdict at all.
        to_check.append(j)

    print(f"verify: probing {len(to_check)} of {len(jobs)} rows "
          f"(days={args.days}, workers={args.workers})")

    results: dict[str, str] = {}  # url -> verdict
    details: dict[str, str] = {}
    verified_at: dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futs = {pool.submit(_probe, (j.get("url") or "").strip(), args.timeout): j for j in to_check}
        done = 0
        for fut in as_completed(futs):
            job = futs[fut]
            url = (job.get("url") or "").strip()
            try:
                verdict, detail = fut.result()
            except Exception:
                verdict, detail = "unknown", "exc"
            done += 1
            results[url] = verdict
            details[url] = detail
            verified_at[url] = now.isoformat()
            if done % 25 == 0:
                print(f"  ...{done}/{len(to_check)}")

    dead = [u for u, v in results.items() if v == "dead"]
    live = [u for u, v in results.items() if v == "live"]
    unknown = [u for u, v in results.items() if v == "unknown"]
    print(f"verify: live={len(live)} dead={len(dead)} unknown={len(unknown)}")

    if args.report_json:
        Path(args.report_json).write_text(json.dumps({
            "checked": len(results), "live": live, "dead": dead,
            "unknown": unknown, "details": details,
        }, indent=1), encoding="utf-8")

    if not dead:
        print("verify: no dead postings — nothing to drop")
        return 0

    dead_set = set(dead)
    kept = []
    dropped = []
    for j in jobs:
        url = (j.get("url") or "").strip()
        if url in dead_set:
            j["_verify"] = f"dead:{details.get(url,'')}"
            dropped.append(j)
            continue
        # Stamp live/unknown verdicts so the next hourly run skips a re-probe.
        if url in verified_at and url in results and results[url] in ("live", "unknown"):
            j["verifiedAt"] = verified_at[url]
            j["verifyState"] = results[url]
        kept.append(j)

    print(f"verify: dropping {len(dropped)} dead rows, keeping {len(kept)}")
    for d in dropped[:20]:
        print(f"  - {d.get('company')} | {d.get('title')} | {d.get('url')}")

    if args.blocklist:
        bp = Path(args.blocklist)
        existing = set()
        if bp.exists():
            existing = {ln.strip() for ln in bp.read_text(encoding="utf-8").splitlines() if ln.strip()}
        with bp.open("a", encoding="utf-8") as fh:
            for u in dead:
                if u not in existing:
                    fh.write(u + "\n")
        print(f"verify: appended {len(dead)} dead urls to {bp}")

    if args.dry_run:
        print("verify: dry-run — no files written")
        return 0

    next_payload = payload
    if isinstance(payload, dict):
        next_payload = dict(payload)
        next_payload["jobs"] = kept
        meta = dict(next_payload.get("meta", {}))
        meta["total"] = len(kept)
        next_payload["meta"] = meta
    json_text = json.dumps(next_payload, indent=2, ensure_ascii=False)
    for t in TARGETS:
        t.parent.mkdir(parents=True, exist_ok=True)
        t.write_text(json_text, encoding="utf-8")
        print(f"verify: wrote {t.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
