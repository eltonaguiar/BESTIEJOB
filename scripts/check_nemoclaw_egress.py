#!/usr/bin/env python3
"""check_nemoclaw_egress.py — prove which job-search hosts the sandbox can reach.

The failure this diagnoses: NemoClaw runs OpenClaw inside an OpenShell sandbox
whose network policy is deny-by-default, so an unlisted host fails with a
connection error that the agent reports as "no network access" / "external
connections are blocked". This script separates the three cases:

  OPEN      any HTTP status came back      -> egress policy allows the host
  BLOCKED   DNS/connect/refused/timed out  -> no route (add a policy preset)
  CERT      TLS verification failed        -> L7 interception, not a policy deny

Run it in the place that is failing (inside the sandbox: `nemoclaw <name>
connect`), not only on the host — the host always works, which is why the
agent's failure looks mysterious.

Usage:
    python3 bestiejob/scripts/check_nemoclaw_egress.py
    python3 bestiejob/scripts/check_nemoclaw_egress.py --json
    python3 bestiejob/scripts/check_nemoclaw_egress.py --host api.adzuna.com

Exit code: 0 when every host is reachable, 1 otherwise (CI-friendly).
"""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import sys
import time
import urllib.error
import urllib.request

# Keep in sync with bestiejob/ops/nemoclaw-jobsearch-preset.yaml.
TARGETS = [
    ("brave search", "https://api.search.brave.com/res/v1/web/search?q=servicenow"),
    ("adzuna CA", "https://api.adzuna.com/v1/api/jobs/ca/search/1?what=servicenow"),
    ("linkedin guest", "https://ca.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=servicenow&location=Toronto"),
    ("indeed CA", "https://ca.indeed.com/jobs?q=servicenow+developer&l=Toronto%2C+ON"),
    ("workday TD", "https://td.wd3.myworkdayjobs.com/wday/cxs/td/TD_Bank_Careers/jobs"),
    ("workday manulife", "https://manulife.wd3.myworkdayjobs.com/wday/cxs/manulife/MFCJH_Jobs/jobs"),
    ("greenhouse", "https://boards-api.greenhouse.io/v1/boards/neuraflash/jobs"),
    ("lever", "https://api.lever.co/v0/postings/leverdemo?mode=json"),
    ("ashby", "https://api.ashbyhq.com/posting-api/job-board/ramp"),
    ("smartrecruiters", "https://api.smartrecruiters.com/v1/companies/Ubisoft/postings"),
    ("jobbank.gc.ca", "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=servicenow"),
    ("servicenow careers", "https://careers.servicenow.com/"),
    ("salesforce careers", "https://careers.salesforce.com/"),
]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


def probe(url: str, timeout: float = 10.0) -> tuple[str, str]:
    """Return (verdict, detail). Any HTTP response means the route works."""
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": UA,
                                                             "Accept": "*/*"})
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ms = int((time.monotonic() - started) * 1000)
            return "OPEN", f"HTTP {resp.status} in {ms}ms"
    except urllib.error.HTTPError as exc:
        ms = int((time.monotonic() - started) * 1000)
        # 4xx/5xx still proves the connection left the sandbox.
        return "OPEN", f"HTTP {exc.code} in {ms}ms"
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, ssl.SSLError):
            return "CERT", f"TLS: {reason}"
        if isinstance(reason, socket.gaierror):
            return "BLOCKED", "DNS: name not resolved"
        return "BLOCKED", f"{type(reason).__name__}: {reason}"
    except (socket.timeout, TimeoutError):
        return "BLOCKED", f"timeout after {timeout:g}s"
    except Exception as exc:                                  # noqa: BLE001
        return "BLOCKED", f"{type(exc).__name__}: {str(exc)[:90]}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", action="append", help="probe only this URL (repeatable)")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--timeout", type=float, default=10.0)
    args = ap.parse_args()

    targets = [(f"custom:{u}", u) for u in args.host] if args.host else TARGETS
    rows = []
    for label, url in targets:
        verdict, detail = probe(url, args.timeout)
        rows.append({"target": label, "url": url, "verdict": verdict, "detail": detail})

    blocked = [r for r in rows if r["verdict"] != "OPEN"]

    if args.json:
        print(json.dumps({"results": rows, "blocked": len(blocked)}, indent=2))
    else:
        width = max(len(r["target"]) for r in rows)
        for r in rows:
            mark = "ok  " if r["verdict"] == "OPEN" else "FAIL"
            print(f"[{mark}] {r['target']:<{width}}  {r['verdict']:<7}  {r['detail']}")
        print()
        if blocked:
            print(f"{len(blocked)}/{len(rows)} blocked. Inside a NemoClaw sandbox this is the")
            print("OpenShell policy, not the host. Fix with:")
            print("  nemoclaw <sandbox> policy add --from-file bestiejob/ops/nemoclaw-jobsearch-preset.yaml")
            print("Then confirm: nemoclaw <sandbox> policy list")
        else:
            print(f"all {len(rows)} job-search hosts reachable — egress policy is sufficient.")

    return 0 if not blocked else 1


if __name__ == "__main__":
    sys.exit(main())
