#!/usr/bin/env python3
"""job_source_truth.py — keep fake / paywall / signup-gated job links off the board.

Job discovery scrapers ingest postings by URL from many aggregator sites. Several of
those sites (jobleads.com, theladders.com, …) are signup/paywall traps: the URL looks
like a posting but only leads to a marketing wall, never to the employer's real job
posting. Rows from those domains are not "true" postings and must not be promoted to
the site as canonical links.

This module is the single reusable source of truth for that problem:

  * domain_is_gated(url)  — True when the URL's host is a known gated/aggregator trap.
  * xref_search_links(...) — builds Google Jobs / LinkedIn / Indeed / Adzuna search
                              links for a job (title + company + location) so a human
                              can locate the employer's real posting.
  * annotate(jobs)        — adds 'gated' and 'xref' to each job dict; returns counts.
  * CLI / --check          — scan README.md, FRESH_JOBS.md, jobs.json (or any json/tsv)
                              and emit a JSON + markdown report. Exit code 1 when gated
                              rows are found in a canonical artifact (README.md).

Blocklist is data-driven: the built-in core is conservative (confirmed walls). Extra
domains can be added in config/gated_domains.txt (one host per line, ignored if absent)
or via the GATED_DOMAINS_EXTRA environment variable (comma-separated).

Usage
    python3 tools/job_source_truth.py --check                  # scan README + fresh + jobs
    python3 tools/job_source_truth.py --in jobs.json --out /tmp/truth.json
    python3 tools/job_source_truth.py --in README.md --report-md /tmp/truth.md
    python3 tools/job_source_truth.py --list-domains
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Confirmed signup/paywall aggregator traps. Keep this conservative: only add a host
# here when you have seen it gate a real posting behind a signup/paywall.
CORE_GATED_DOMAINS = {
    "jobleads.com",
    "www.jobleads.com",
    "theladders.com",
    "www.theladders.com",
}


def _extra_domains() -> set[str]:
    extra: set[str] = set()
    cfg = ROOT / "config" / "gated_domains.txt"
    if cfg.exists():
        for line in cfg.read_text(errors="replace").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                extra.add(line.lower())
    env = os.environ.get("GATED_DOMAINS_EXTRA", "").strip()
    if env:
        extra.update(h.strip().lower() for h in env.split(",") if h.strip())
    return extra


def gated_domains() -> set[str]:
    return CORE_GATED_DOMAINS | _extra_domains()


def hostname(url: str) -> str:
    m = re.match(r"https?://([^/]+)", url or "")
    return m.group(1).lower() if m else ""


def root_domain(host: str) -> str:
    """Map a host to its registrable-ish root for blocklist matching."""
    host = host.lower().strip(".")
    if not host:
        return ""
    parts = host.split(".")
    # Take the last two labels for common TLDs, else last two.
    if len(parts) >= 3 and parts[-1] in ("com", "org", "net", "ca", "io", "co", "jobs", "app", "dev", "me", "xyz", "info", "biz", "name", "tv", "work", "online", "site", "tech", "company", "careers"):
        return ".".join(parts[-2:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def domain_is_gated(url: str) -> bool:
    h = hostname(url)
    if not h:
        return False
    r = root_domain(h)
    gated = gated_domains()
    return h in gated or r in gated or r in {g.split(".")[-1] for g in gated if len(g.split(".")) >= 2}


# ---- cross-reference search links -------------------------------------------

LOC_PRIORITY = ["toronto", "mississauga", "brampton", "ottawa", "oakville", "markham",
                "vancouver", "calgary", "edmonton", "montreal", "quebec", "halifax",
                "winnipeg", "saskatoon", "regina", "victoria", "kitchener", "waterloo",
                "hamilton"]


def _short_location(location: str) -> str:
    l = (location or "").lower()
    for c in LOC_PRIORITY:
        if c in l:
            return c.title()
    if any(k in l for k in ("remote", "canada")):
        return "Canada"
    return "Canada"


def xref_search_links(title: str, company: str = "", location: str = "") -> list[tuple[str, str]]:
    comp = (company or "").strip()
    if comp.lower() in ("unknown", "jobleads") or not comp:
        comp = ""
    q = " ".join(x for x in (title, comp) if x)
    loc = _short_location(location)
    qe = urllib.parse.quote(q)
    le = urllib.parse.quote(loc)
    return [
        ("Google Jobs", f"https://www.google.com/search?q={qe}+{le}+jobs&ibp=htl;jobs"),
        ("LinkedIn", f"https://www.linkedin.com/jobs/search/?keywords={qe}&location={le}"),
        ("Indeed", f"https://ca.indeed.com/jobs?q={qe}&l={le}"),
        ("Adzuna", f"https://www.adzuna.ca/search?q={qe}&loc={le}"),
    ]


# ---- annotation / CLI --------------------------------------------------------

def annotate(jobs: list[dict]) -> dict:
    """Add 'gated' and 'xref' to each job dict in place. Returns count summary."""
    n_gated = 0
    for j in jobs:
        url = j.get("url", "") or ""
        j["gated"] = domain_is_gated(url)
        if j["gated"]:
            n_gated += 1
            j.setdefault("xref", xref_search_links(j.get("title", ""),
                                                   j.get("company", ""),
                                                   j.get("location", "")))
    return {"jobs": len(jobs), "gated": n_gated}


def load_jobs(path: Path) -> list[dict]:
    text = path.read_text(errors="replace")
    jobs: list[dict] = []
    if path.suffix.lower() == ".json":
        data = json.loads(text)
        if isinstance(data, dict):
            bucket = data.get("jobs")
            if not isinstance(bucket, list):
                bucket = data.get("dated") or data.get("rows")
            data = bucket
        if isinstance(data, list):
            for it in data:
                if isinstance(it, dict) and (it.get("url") or it.get("title")):
                    jobs.append(it)
    else:  # markdown table
        link = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
        for line in text.splitlines():
            m = link.search(line)
            if not m:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            jobs.append({
                "posted": cells[0] if cells and re.match(r"^\d{4}-\d{2}-\d{2}$", cells[0]) else "",
                "title": m.group(1),
                "url": m.group(2),
                "company": cells[2] if len(cells) > 2 else "",
                "location": cells[3] if len(cells) > 3 else "",
                "source": cells[5] if len(cells) > 5 else "",
            })
    return jobs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--in", dest="inp", help="file to scan (json or markdown table)")
    ap.add_argument("--out", help="write JSON report here")
    ap.add_argument("--report-md", help="write a human-readable markdown report here")
    ap.add_argument("--check", action="store_true",
                    help="scan canonical artifacts (README.md, FRESH_JOBS.md, jobs.json); exit 1 if gated rows are found in README")
    ap.add_argument("--list-domains", action="store_true", help="print the gated-domain blocklist")
    ap.add_argument("--fail-on-readme", action="store_true", help="with --check, also exit 1 when README holds gated rows")
    args = ap.parse_args()

    if args.list_domains:
        for d in sorted(gated_domains()):
            print(d)
        return 0

    paths: list[Path] = []
    if args.inp:
        paths.append(Path(args.inp))
    if args.check:
        paths = [ROOT / "README.md", ROOT / "FRESH_JOBS.md", ROOT / "jobs.json"]

    report: dict = {"scanned": [], "gated_rows": [], "total": 0, "gated": 0}
    for p in paths:
        if not p.exists():
            continue
        jobs = load_jobs(p)
        summ = annotate(jobs)
        report["scanned"].append({"file": str(p), **summ})
        report["total"] += summ["jobs"]
        report["gated"] += summ["gated"]
        for j in jobs:
            if j.get("gated"):
                report["gated_rows"].append({
                    "file": str(p),
                    "posted": j.get("posted", ""),
                    "title": j.get("title", ""),
                    "company": j.get("company", ""),
                    "location": j.get("location", ""),
                    "url": j.get("url", ""),
                    "xref": j.get("xref", []),
                })

    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2), encoding="utf-8")

    if args.report_md:
        lines = ["# Job Source Truth Report", "",
                 f"- Files scanned: {len(report['scanned'])}",
                 f"- Total rows: {report['total']}",
                 f"- Gated/signup-trap rows: {report['gated']}", ""]
        if report["gated_rows"]:
            lines.append("## Gated rows")
            for g in report["gated_rows"]:
                lines.append(f"- [{g['title']}]({g['url']}) — {g['company']} · {g['location']} · {g['posted']}")
                links = " · ".join(f"[{n}]({u})" for n, u in g["xref"])
                lines.append(f"    cross-ref: {links}")
        Path(args.report_md).write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"scanned={len(report['scanned'])} total={report['total']} gated={report['gated']}")
    for g in report["gated_rows"]:
        print(f"  GATED [{g['posted']}] {g['title'][:60]} — {g['company'][:24]} · {g['location'][:24]} · {g['url'][:80]}")

    # Enforcement: exit non-zero when gated rows exist in a canonical artifact.
    if args.check and args.fail_on_readme:
        readme_gated = [g for g in report["gated_rows"] if g["file"].endswith("README.md")]
        if readme_gated:
            print(f"!! {len(readme_gated)} gated row(s) present in README.md")
            return 1
    return 1 if report["gated"] and args.check else 0


if __name__ == "__main__":
    sys.exit(main())
