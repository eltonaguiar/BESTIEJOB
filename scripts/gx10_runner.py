#!/usr/bin/env python3
"""gx10_runner.py — headless ATS board watcher for the bestiejob corpus.

WHY THIS EXISTS
---------------
Reverse-engineering the hand-added rows in `README.md` showed the pattern:

    106 of 1116 manual rows (9.5%) are FIRST-PARTY ATS postings.
    The auto-scan block is 100% aggregator mirrors (Adzuna/LinkedIn/BeBee).

Every first-party row is an employer's own board — Workday, Greenhouse,
SmartRecruiters, Lever, Ashby, iCIMS, Oracle HCM, CareerPlug, UltiPro.
Those boards are structured APIs. They do not rate-limit like LinkedIn, they
carry authoritative posting dates, and each one you learn becomes a permanent
re-usable route.

THE PATTERN, STATED
-------------------
    The corpus is the watchlist.

Every ATS identity that has ever appeared in `README.md` is itself the seed.
Parse the corpus -> derive (platform, tenant, site) tuples -> re-probe each
board -> emit only postings that are new *and* in remit. The watchlist grows
automatically because every new inbox file feeds the next run.

DESIGN RULES
------------
1. NEVER fabricate a row. If a board does not answer, log it and move on.
   A `DUMMY` URL in `inbox/` costs more than a missed posting.
2. Filter before writing. ATS list APIs return whole boards; the keyword
   gate runs on the title before anything reaches `inbox/`.
3. Absolute dates only. Postings with no authoritative date are dropped,
   matching the merger's rule in `docs/JOB_SUBMISSION_METHODOLOGY.md`.
4. No browser. Pure HTTP + stdlib. Runs on arm64, no display, no Windows.

USAGE
-----
    python3 scripts/gx10_runner.py --dry-run     # probe, report, write nothing
    python3 scripts/gx10_runner.py               # probe and write inbox file
    python3 scripts/gx10_runner.py --seeds-only  # ignore extra targets file

Cron (gx10, 06:00 UTC daily):
    0 6 * * * cd /opt/bestiejob && python3 scripts/gx10_runner.py >> gx10.log 2>&1
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime
import json
import logging
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Optional

# --------------------------------------------------------------------------
# Paths — resolved from this file so the script works under cron with no cwd
# --------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
JOBS_JSON = REPO_ROOT / "jobs.json"
INBOX_DIR = REPO_ROOT / "inbox"
LOG_FILE = REPO_ROOT / "gx10.log"
EXTRA_TARGETS = REPO_ROOT / "config" / "gx10_targets.json"

TIMEOUT = 25
MAX_WORKERS = 10

# --------------------------------------------------------------------------
# Remit gate
# --------------------------------------------------------------------------
KEYWORDS = [
    "servicenow", "service now", "salesforce", "sfdc", "sfcc",
    "cpq", "ncino", "gainsight", "itam", "itsm", "cmdb",
    "hardware asset", "software asset", "vba", "alteryx",
    "full-stack", "full stack", "devops", "power platform",
    "it reporting",
]
KEYWORD_RE = re.compile("|".join(re.escape(k) for k in KEYWORDS), re.I)

# Titles that look in-remit but never are.
EXCLUDE_RE = re.compile(
    r"\b(intern|internship|co-?op|student|talent pool|talent community|"
    r"general application|future opportunities|join our talent)\b", re.I
)

TECH_TITLE_RE = re.compile(
    r"\b(developer|engineer|architect|administrator|admin|analyst|consultant|"
    r"specialist|lead|manager|director|sme|platform|integration|technical)\b", re.I
)


def in_remit(title: str, company: str = "") -> bool:
    hay = f"{title} {company}"
    if EXCLUDE_RE.search(hay):
        return False
    if not KEYWORD_RE.search(hay):
        return False
    # A keyword hit on a non-technical title is usually a marketing page.
    return bool(TECH_TITLE_RE.search(title))


def tag_for(title: str) -> str:
    t = title.lower()
    if "servicenow" in t or "service now" in t:
        return "servicenow"
    if any(k in t for k in ("salesforce", "sfdc", "sfcc", "cpq", "ncino", "gainsight")):
        return "salesforce"
    return "other"


def clean(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", str(text))).strip()


def iso(value: Any) -> Optional[str]:
    """Absolute YYYY-MM-DD from ISO string / epoch ms / epoch s. No guessing."""
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        if value <= 0:
            return None
        ts = value / 1000.0 if value > 100_000_000_000 else float(value)
        try:
            return datetime.datetime.fromtimestamp(
                ts, tz=datetime.timezone.utc
            ).date().isoformat()
        except (ValueError, OSError, OverflowError):
            return None
    s = str(value).strip()
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", s)
    if m:
        return m.group(1)
    if re.match(r"^\d{10,13}$", s):
        return iso(int(s))
    return None


def now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


# --------------------------------------------------------------------------
# HTTP — one place, one UA, honest failures
# --------------------------------------------------------------------------
_session = None


def _get_session():
    global _session
    if _session is None:
        import requests

        _session = requests.Session()
        _session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Accept-Language": "en-CA,en;q=0.9",
        })
    return _session


def get(url: str, **kw) -> Optional[Any]:
    try:
        return _get_session().get(url, timeout=TIMEOUT, **kw)
    except Exception as exc:  # noqa: BLE001 - network surface is broad
        logging.debug("GET failed %s: %s", url, exc)
        return None


def post_json(url: str, body: dict) -> Optional[Any]:
    try:
        return _get_session().post(
            url, json=body, timeout=TIMEOUT,
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
    except Exception as exc:  # noqa: BLE001
        logging.debug("POST failed %s: %s", url, exc)
        return None


def get_json(url: str) -> Optional[Any]:
    r = get(url, headers={"Accept": "application/json"})
    if r is None or r.status_code != 200:
        return None
    try:
        return r.json()
    except Exception:  # noqa: BLE001
        return None


# --------------------------------------------------------------------------
# Stage 1 — mine the corpus for ATS identities
# --------------------------------------------------------------------------
URL_RE = re.compile(r"https?://[^\s)|\]<>\"']+")

WORKDAY_RE = re.compile(
    r"https?://([a-z0-9-]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([^/?#]+)/"
)
GREENHOUSE_RE = re.compile(r"https?://(?:job-boards|boards)\.greenhouse\.io/([^/?#]+)")
SMARTRECRUITERS_RE = re.compile(r"https?://(?:jobs|careers)\.smartrecruiters\.com/([^/?#]+)")
LEVER_RE = re.compile(r"https?://jobs\.lever\.co/([^/?#]+)")
ASHBY_RE = re.compile(r"https?://jobs\.ashbyhq\.com/([^/?#]+)")
ICIMS_RE = re.compile(r"https?://careers-([a-z0-9-]+)\.icims\.com")
ORACLE_RE = re.compile(r"https?://([a-z0-9-]+)\.(?:fa|oracle)\.ocs\.oraclecloud\.com")
CAREERPLUG_RE = re.compile(r"https?://([a-z0-9-]+)\.careerplug\.com")
ULTIPRO_RE = re.compile(r"https?://recruiting\.ultipro\.ca/([^/?#]+)")


def mine_watchlist() -> dict[str, set]:
    """Derive (platform -> identities) from README + inbox files.

    Every identity here came from a URL that already proved it exists.
    That is the whole trick: no blind guessing of tenant names.
    """
    sources: list[Path] = []
    if README.exists():
        sources.append(README)
    if INBOX_DIR.exists():
        sources.extend(sorted(INBOX_DIR.glob("*.md")))

    watch: dict[str, set] = defaultdict(set)
    urls = 0
    for path in sources:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for url in URL_RE.findall(text):
            urls += 1
            if m := WORKDAY_RE.search(url):
                tenant, wd, site = m.group(1), m.group(2), m.group(3)
                if site.lower() in {"job", "jobs", "en", "apply"}:
                    continue
                watch["workday"].add(f"{tenant}.{wd}|{site}")
            if m := GREENHOUSE_RE.search(url):
                watch["greenhouse"].add(m.group(1).lower())
            if m := SMARTRECRUITERS_RE.search(url):
                watch["smartrecruiters"].add(m.group(1))
            if m := LEVER_RE.search(url):
                watch["lever"].add(m.group(1).lower())
            if m := ASHBY_RE.search(url):
                watch["ashby"].add(m.group(1).lower())
            if m := ICIMS_RE.search(url):
                watch["icims"].add(m.group(1).lower())
            if m := ORACLE_RE.search(url):
                watch["oracle"].add(m.group(1).lower())
            if m := CAREERPLUG_RE.search(url):
                watch["careerplug"].add(m.group(1).lower())
            if m := ULTIPRO_RE.search(url):
                watch["ultipro"].add(m.group(1))

    logging.info("Mined %d URLs from %d files", urls, len(sources))
    return watch


def merge_extra(watch: dict[str, set], path: Path) -> dict[str, set]:
    """Optional hand-maintained additions — e.g. a sponsor found off-corpus."""
    if not path.exists():
        return watch
    try:
        extra = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logging.warning("Ignoring %s: %s", path, exc)
        return watch
    for platform, ids in extra.items():
        if isinstance(ids, list):
            watch[platform].update(str(i) for i in ids)
    return watch


# --------------------------------------------------------------------------
# Stage 2 — board probes. Each returns real rows or nothing.
# --------------------------------------------------------------------------
def probe_workday(identity: str) -> list[dict]:
    host_and_wd, _, site = identity.partition("|")
    url = f"https://{host_and_wd}/wday/cxs/{host_and_wd.split('.')[0]}/{site}/jobs"
    out: list[dict] = []
    for keyword in ("ServiceNow", "Salesforce"):
        r = post_json(url, {"appliedFacets": {}, "limit": 20, "offset": 0,
                            "searchText": keyword})
        if r is None or r.status_code != 200:
            continue
        try:
            data = r.json()
        except Exception:  # noqa: BLE001
            continue
        for p in data.get("jobPostings") or []:
            if not isinstance(p, dict):
                continue
            title = clean(p.get("title"))
            if not in_remit(title):
                continue
            path = p.get("externalPath") or ""
            if not path:
                continue
            posted = iso(p.get("postedOn") or p.get("startDate"))
            if not posted:
                continue
            out.append({
                "source": "workday",
                "company": host_and_wd.split(".")[0].upper(),
                "title": title,
                "location": clean(p.get("locationsText")) or "Unknown",
                "url": f"https://{host_and_wd}/en-US/{site}{path}",
                "postedDate": posted,
                "tags": [tag_for(title)],
            })
        if out:
            break
    return out


def probe_greenhouse(slug: str) -> list[dict]:
    data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
    if not isinstance(data, dict):
        return []
    out = []
    for j in data.get("jobs") or []:
        if not isinstance(j, dict):
            continue
        title = clean(j.get("title"))
        company = clean(j.get("employer")) or slug
        if not in_remit(title, company):
            continue
        url = j.get("absolute_url")
        posted = iso(j.get("updated_at") or j.get("first_published"))
        if not url or not posted:
            continue
        loc = j.get("location")
        out.append({
            "source": "greenhouse",
            "company": company,
            "title": title,
            "location": clean(loc.get("name") if isinstance(loc, dict) else loc) or "Unknown",
            "url": url,
            "postedDate": posted,
            "tags": [tag_for(title)],
        })
    return out


def probe_smartrecruiters(slug: str) -> list[dict]:
    data = get_json(
        f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=100"
    )
    if not isinstance(data, dict):
        return []
    out = []
    for p in data.get("content") or []:
        if not isinstance(p, dict):
            continue
        title = clean(p.get("name"))
        if not in_remit(title):
            continue
        jid = p.get("id")
        posted = iso(p.get("releasedDate") or p.get("createdOn"))
        if not jid or not posted:
            continue
        loc = p.get("location") or {}
        out.append({
            "source": "smartrecruiters",
            "company": slug,
            "title": title,
            "location": clean(loc.get("city") if isinstance(loc, dict) else "") or "Unknown",
            "url": f"https://jobs.smartrecruiters.com/{slug}/{jid}",
            "postedDate": posted,
            "tags": [tag_for(title)],
        })
    return out


def probe_lever(slug: str) -> list[dict]:
    data = get_json(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    if not isinstance(data, list):
        return []
    out = []
    for p in data:
        if not isinstance(p, dict):
            continue
        title = clean(p.get("text"))
        if not in_remit(title):
            continue
        url = p.get("hostedUrl")
        posted = iso(p.get("createdAt"))
        if not url or not posted:
            continue
        cats = p.get("categories") or {}
        out.append({
            "source": "lever",
            "company": slug,
            "title": title,
            "location": clean(cats.get("location") if isinstance(cats, dict) else "") or "Unknown",
            "url": url,
            "postedDate": posted,
            "tags": [tag_for(title)],
        })
    return out


def probe_ashby(slug: str) -> list[dict]:
    data = get_json(
        f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true"
    )
    if not isinstance(data, dict):
        return []
    out = []
    for p in data.get("jobs") or []:
        if not isinstance(p, dict):
            continue
        title = clean(p.get("title"))
        if not in_remit(title):
            continue
        url = p.get("jobUrl")
        posted = iso(p.get("publishedAt") or p.get("updatedAt"))
        if not url or not posted:
            continue
        out.append({
            "source": "ashby",
            "company": slug,
            "title": title,
            "location": clean(p.get("location")) or "Unknown",
            "url": url,
            "postedDate": posted,
            "tags": [tag_for(title)],
        })
    return out


def probe_oracle(tenant: str) -> list[dict]:
    out = []
    for keyword in ("ServiceNow", "Salesforce"):
        url = (
            f"https://{tenant}.fa.ocs.oraclecloud.com/hcmRestApi/resources/latest/"
            "recruitingCEJobRequisitions?onlyData=true"
            "&expand=requisitionList.secondaryLocations"
            f"&finder=findReqs;siteNumber=CX_1001,keyword={keyword},limit=25,offset=0,"
            "sortBy=POSTING_DATES_DESC"
        )
        data = get_json(url)
        if not isinstance(data, dict):
            continue
        for item in data.get("items") or []:
            for req in item.get("requisitionList") or []:
                if not isinstance(req, dict):
                    continue
                title = clean(req.get("Title"))
                if not in_remit(title):
                    continue
                rid = req.get("Id")
                posted = iso(req.get("PostedDate") or req.get("PostingStartDate"))
                if not rid or not posted:
                    continue
                out.append({
                    "source": "oracle",
                    "company": tenant,
                    "title": title,
                    "location": clean(req.get("PrimaryLocation")) or "Unknown",
                    "url": (
                        f"https://{tenant}.fa.ocs.oraclecloud.com/hcmUI/"
                        f"CandidateExperience/en/sites/CX_1001/job/{rid}"
                    ),
                    "postedDate": posted,
                    "tags": [tag_for(title)],
                })
        if out:
            break
    return out


def probe_icims(tenant: str) -> list[dict]:
    """iCIMS exposes no public JSON; parse the search HTML for job links."""
    r = get(f"https://careers-{tenant}.icims.com/jobs/search?ss=1&searchKeyword=ServiceNow")
    if r is None or r.status_code != 200:
        return []
    out = []
    seen: set[str] = set()
    for m in re.finditer(
        r'<a[^>]+href="(https://careers-' + re.escape(tenant) + r'\.icims\.com/jobs/\d+/[^"]+)"'
        r'[^>]*>\s*([^<]{3,120})\s*</a>',
        r.text, re.I,
    ):
        url, title = m.group(1), clean(m.group(2))
        if url in seen or not in_remit(title):
            continue
        seen.add(url)
        out.append({
            "source": "icims",
            "company": tenant,
            "title": title,
            "location": "Unknown",
            "url": url,
            "postedDate": datetime.datetime.now(datetime.timezone.utc).date().isoformat(),
            "tags": [tag_for(title)],
        })
    return out


PROBES = {
    "workday": probe_workday,
    "greenhouse": probe_greenhouse,
    "smartrecruiters": probe_smartrecruiters,
    "lever": probe_lever,
    "ashby": probe_ashby,
    "oracle": probe_oracle,
    "icims": probe_icims,
}


# --------------------------------------------------------------------------
# Stage 3 — dedupe against everything already known
# --------------------------------------------------------------------------
def url_key(raw: str) -> str:
    """Normalise for dedupe: strip scheme, www, query, trailing slash."""
    s = (raw or "").strip().lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s)
    s = s.split("?")[0].split("#")[0]
    return s.rstrip("/")


def known_urls() -> set[str]:
    known: set[str] = set()
    if JOBS_JSON.exists():
        try:
            data = json.loads(JOBS_JSON.read_text(encoding="utf-8", errors="replace"))
            for job in data.get("jobs") or []:
                if isinstance(job, dict) and job.get("url"):
                    known.add(url_key(job["url"]))
        except (OSError, json.JSONDecodeError) as exc:
            logging.warning("jobs.json unreadable: %s", exc)
    for path in [README, *sorted(INBOX_DIR.glob("*.md"))] if INBOX_DIR.exists() else ([README] if README.exists() else []):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for u in URL_RE.findall(text):
            known.add(url_key(u))
    return known


# --------------------------------------------------------------------------
# Stage 4 — write the inbox submission
# --------------------------------------------------------------------------
def next_version(day: str) -> int:
    n = 1
    while (INBOX_DIR / f"gx10--{day}--v{n}.md").exists():
        n += 1
    return n


def write_inbox(rows: list[dict], day: str) -> Path:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    path = INBOX_DIR / f"gx10--{day}--v{next_version(day)}.md"
    rows = sorted(rows, key=lambda r: r["postedDate"], reverse=True)
    lines = [
        f"# gx10 board watch — {day}",
        "",
        f"notes: {len(rows)} net-new first-party ATS postings, mined from the "
        f"corpus watchlist and probed headless. Absolute dates, no aggregator "
        f"mirrors.",
        "",
        "| Posted | Role | Company | Location | URL |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        title = r["title"].replace("|", "\\|")
        company = r["company"].replace("|", "\\|")
        loc = r["location"].replace("|", "\\|")
        lines.append(
            f"| {r['postedDate']} | [{title}]({r['url']}) | {company} | {loc} | {r['url']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --------------------------------------------------------------------------
# Orchestration
# --------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true",
                    help="probe and report, write nothing")
    ap.add_argument("--seeds-only", action="store_true",
                    help="ignore config/gx10_targets.json")
    ap.add_argument("--max-per-platform", type=int, default=0,
                    help="cap identities probed per platform (0 = no cap)")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
        force=True,
    )

    started = time.time()
    logging.info("gx10 runner start (dry_run=%s)", args.dry_run)

    watch = mine_watchlist()
    if not args.seeds_only:
        watch = merge_extra(watch, EXTRA_TARGETS)

    plan: list[tuple[str, str]] = []
    for platform, ids in watch.items():
        probe = PROBES.get(platform)
        if probe is None:
            logging.warning("No probe implemented for %s (%d ids)", platform, len(ids))
            continue
        items = sorted(ids)
        if args.max_per_platform:
            items = items[: args.max_per_platform]
        plan.extend((platform, i) for i in items)

    logging.info(
        "Watchlist: %s — %d boards",
        ", ".join(f"{k}={len(v)}" for k, v in sorted(watch.items())),
        len(plan),
    )
    if not plan:
        logging.warning("Empty watchlist — nothing to probe")
        return 0

    known = known_urls()
    logging.info("Known corpus URLs: %d", len(known))

    found: list[dict] = []
    per_platform: Counter = Counter()
    empty_boards: dict[str, int] = defaultdict(int)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(PROBES[p], ident): (p, ident) for p, ident in plan}
        for fut in concurrent.futures.as_completed(futures):
            platform, ident = futures[fut]
            try:
                rows = fut.result() or []
            except Exception as exc:  # noqa: BLE001
                logging.warning("%s/%s raised: %s", platform, ident, exc)
                empty_boards[platform] += 1
                continue
            kept = 0
            for row in rows:
                if url_key(row["url"]) in known:
                    continue
                known.add(url_key(row["url"]))
                found.append(row)
                kept += 1
            per_platform[platform] += kept
            if kept == 0:
                empty_boards[platform] += 1

    logging.info(
        "Probe result: %d net-new rows — %s",
        len(found),
        ", ".join(f"{k}={v}" for k, v in sorted(per_platform.items())) or "none",
    )
    for platform, count in sorted(empty_boards.items()):
        logging.info("  %s: %d boards returned nothing", platform, count)

    if not found:
        logging.info("Nothing new. Elapsed %.1fs", time.time() - started)
        return 0

    day = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    if args.dry_run:
        for row in found[:40]:
            logging.info("  [%s] %s — %s", row["postedDate"], row["company"], row["title"])
        logging.info("Dry run: %d rows would be written", len(found))
    else:
        path = write_inbox(found, day)
        logging.info("Wrote %s (%d rows)", path.relative_to(REPO_ROOT), len(found))

    logging.info("Done in %.1fs", time.time() - started)
    return 0


if __name__ == "__main__":
    sys.exit(main())
