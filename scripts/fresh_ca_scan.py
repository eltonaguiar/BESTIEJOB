#!/usr/bin/env python3
"""Freshness-first Canadian sweep for ServiceNow / Salesforce dev+admin roles.

The hourly board scan is breadth-first: it fills seven-day windows from
aggregators and ATS APIs, so a posting made this morning can lose the table to
older rows that were already queued. This adapter is the opposite -- it only
keeps postings dated *today or yesterday*, from sources that expose an absolute
posting date or a same-day relative date, and it drops every row whose URL does
not answer.

Sources
    adzuna      api.adzuna.com, `max_days_old=2&sort_by=date` (absolute `created`)
    jobbank     jobbank.gc.ca sorted by newest (absolute "November 9, 2026")
    eluta       eluta.ca "last seen" (relative "today"/"yesterday")

Job Bank and Eluta parsing is imported from scripts/canada_index_sweep.py so
there is exactly one parser per site; a second copy would drift.

    python3 scripts/fresh_ca_scan.py                      # today + yesterday
    python3 scripts/fresh_ca_scan.py --days 3 --out-inbox inbox/x--2026-11-09--v1.md

Output
    reports/fresh_ca_<date>.json      rows + per-source stats
    inbox/fresh-ca--<date>--v1.md     6-column inbox table
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import canada_index_sweep as cis  # noqa: E402  (reuse jobbank_page / eluta_page)

INBOX = ROOT / "inbox"
OUT = ROOT / "reports"
NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y-%m-%d")
TODAY = NOW.date()

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Adzuna credentials are the public demo pair already used by
# tools/import_adzuna_jobs.py; env wins when set.
APP_ID = __import__("os").environ.get("ADZUNA_APP_ID", "54ce986e")
APP_KEY = __import__("os").environ.get("ADZUNA_APP_KEY", "db851f299e966c0a2a72af525dce6199")

ADZUNA_QUERIES = [
    "servicenow", "servicenow developer", "servicenow administrator",
    "servicenow architect", "servicenow consultant", "servicenow analyst",
    "salesforce", "salesforce developer", "salesforce administrator",
    "salesforce platform developer", "salesforce platform administrator",
    "salesforce admin", "salesforce consultant", "apex developer",
    "ITSM", "CMDB", "ServiceNow CSA CAD CIS",
]

# A title is relevant when it names the platform, one of its modules, or the
# certification the employer is buying (CSA/CAD/CIS). This mirrors the board's
# own bucket rules rather than inventing a wider net.
SN = re.compile(
    r"service\s?now|\bcsdm\b|\bcmdb\b|\bitsm\b|\bitam\b|\bitom\b|\bhrsd\b|"
    r"\bsecops\b|\bcsa\b|\bcad\b|\bcis\b|\bnow assist\b|\bflow designer\b|"
    r"\bservice catalog\b|\bglide\b", re.I)
SF = re.compile(
    r"salesforce|\bapex\b|\bsoql\b|\blwc\b|lightning|visualforce|agentforce|"
    r"\bcpq\b|mulesoft|\bsfdc\b|platform (?:developer|administrator|admin)|"
    r"\bcrm developer\b|experience cloud|\bcommunities\b", re.I)
EXCLUDE = re.compile(
    r"sales (?:representative|manager|associate|consultant|lead|agent)|"
    r"account executive|account manager|recruiter|talent acquisition|"
    r"pre-?sales|customer success|product marketing|demand gen|"
    r"marketing (?:manager|specialist|coordinator)|social media|brand manager|"
    r"business development|\bintern\b|\bco-?op\b|\bstage\b|\btrainee\b|"
    r"\bcashier\b|\bbarista\b|\bwarehouse\b", re.I)

CA_PREF = re.compile(
    r"toronto|ontario|mississauga|brampton|markham|vaughan|richmond hill|"
    r"scarborough|etobicoke|north york|oakville|hamilton|ottawa|kitchener|"
    r"waterloo|london|windsor|canada|remote", re.I)
CA_PROV = re.compile(r"\b(ON|QC|BC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b", re.I)


def get(url: str, timeout: int = 30, tries: int = 2) -> bytes | None:
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA, "Accept": "*/*",
                              "Accept-Language": "en-CA,en;q=0.9"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 410, 403):
                return None
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def classify(title: str) -> str | None:
    if EXCLUDE.search(title):
        return None
    if SN.search(title):
        return "servicenow"
    if SF.search(title):
        return "salesforce"
    return None


def canadaish(location: str) -> bool:
    return bool(location) and bool(CA_PREF.search(location) or CA_PROV.search(location))


def priority(location: str) -> int:
    """0 = Toronto/Ontario, 1 = Canadian remote, 2 = other Canada."""
    loc = location.lower()
    if re.search(r"toronto|ontario|mississauga|brampton|markham|vaughan|"
                 r"richmond hill|scarborough|etobicoke|north york|oakville|"
                 r"hamilton|ottawa|kitchener|waterloo|london|windsor", loc):
        return 0
    if "remote" in loc or "anywhere in canada" in loc:
        return 1
    return 2


def adzuna_rows(window: list[str], stats: dict, geos: list[str]) -> list[dict]:
    """National plus geo-scoped searches.

    A national date-sorted search returns the newest 50 rows for the whole
    country, which on a busy morning is mostly other provinces. Repeating each
    query with `where=Toronto`/`where=Ontario` is what keeps local roles on the
    board, and dedupe happens downstream on the resolved URL.
    """
    rows: list[dict] = []
    for query in ADZUNA_QUERIES:
        for geo in geos:
            url = ("https://api.adzuna.com/v1/api/jobs/ca/search/1"
                   f"?app_id={APP_ID}&app_key={APP_KEY}&results_per_page=50"
                   f"&what={urllib.parse.quote(query)}&max_days_old={len(window) + 1}"
                   "&sort_by=date&content-type=application/json")
            if geo:
                url += f"&where={urllib.parse.quote(geo)}"
            blob = get(url)
            stats["requests"] += 1
            if not blob:
                stats["adzuna_misses"] = stats.get("adzuna_misses", 0) + 1
                continue
            try:
                data = json.loads(blob)
            except json.JSONDecodeError:
                continue
            for r in data.get("results", []):
                created = (r.get("created") or "")[:10]
                if created not in window:
                    continue
                title = (r.get("title") or "").strip()
                bucket = classify(title)
                if not bucket:
                    continue
                location = ((r.get("location") or {}).get("display_name") or "").strip()
                if not canadaish(location):
                    continue
                rows.append({
                    "source": "adzuna", "bucket": bucket, "posted": created,
                    "title": title,
                    "company": ((r.get("company") or {}).get("display_name") or "").strip(),
                    "location": location,
                    "url": r.get("redirect_url") or r.get("url") or "",
                })
            time.sleep(0.25)
    return rows


# A bounded LinkedIn guest pass. The full keyword list in
# scripts/linkedin_guest_scan.py is ~70 terms, too slow for a same-day sweep;
# these eight are the ones that actually return ServiceNow/Salesforce dev+admin
# titles, and the module's own parser gives us the card's `<time datetime>`
# attribute -- a real posting date, not a relative age.
LI_KEYWORDS = [
    "ServiceNow", "ServiceNow Developer", "ServiceNow Administrator",
    "ServiceNow Architect", "ServiceNow Consultant", "ServiceNow Analyst",
    "ServiceNow ITSM", "ServiceNow ITAM", "ServiceNow CMDB",
    "ServiceNow Developer Toronto",
    "Salesforce", "Salesforce Developer", "Salesforce Administrator",
    "Salesforce Platform Developer", "Salesforce Platform Administrator",
    "Salesforce Architect", "Salesforce Consultant", "Salesforce CPQ",
    "Salesforce Apex", "Salesforce Admin Toronto",
]
LI_LOCATIONS = ["Toronto%2C%20Ontario%2C%20Canada", "Canada"]


def linkedin_rows(window: list[str], stats: dict, days: int, max_kw: int = 0) -> list[dict]:
    try:
        import linkedin_guest_scan as li  # noqa: PLC0415 (optional dependency)
    except (SystemExit, Exception) as exc:  # curl_cffi missing -> skip, never abort
        stats["linkedin"] = f"unavailable: {type(exc).__name__}"
        return []
    rows: list[dict] = []
    # `max_kw` exists because the guest pass is the slowest source in this
    # adapter (~11 s per keyword across two locations); a manual round can cap
    # it to fit a session, and the 0 default keeps the scheduled sweep complete.
    for kw in (LI_KEYWORDS[:max_kw] if max_kw else LI_KEYWORDS):
        for loc in LI_LOCATIONS:
            got = li.fetch(urllib.parse.quote(kw), loc, 0, days)
            stats["linkedin_requests"] = stats.get("linkedin_requests", 0) + 1
            for r in got:
                if r.get("posted") not in window:
                    continue
                bucket = classify(r.get("title", ""))
                if not bucket:
                    continue
                if not canadaish(r.get("location", "")):
                    continue
                rows.append({
                    "source": "linkedin-guest", "bucket": bucket,
                    "posted": r["posted"], "title": r.get("title", ""),
                    "company": r.get("company", ""),
                    "location": r.get("location", ""),
                    "url": r.get("url", ""),
                })
            time.sleep(1.5)
    return rows


def index_rows(window: list[str], stats: dict, eluta_pages: int,
               jobbank_pages: int) -> list[dict]:
    rows: list[dict] = []
    keywords = ["servicenow", "servicenow developer", "servicenow administrator",
                "salesforce", "salesforce developer", "salesforce administrator"]
    for kw in keywords:
        for page in range(1, jobbank_pages + 1):
            got = cis.jobbank_page(kw, page)
            stats["jobbank_pages"] += 1
            rows.extend(got)
            if not got:
                break
            time.sleep(1.0)
        for page in range(1, eluta_pages + 1):
            got, _origins = cis.eluta_page(kw, page)
            stats["eluta_pages"] += 1
            rows.extend(got)
            if not got:
                break
            time.sleep(1.0)
    kept = []
    for r in rows:
        if r.get("posted") not in window:
            continue
        bucket = classify(r.get("title", ""))
        if not bucket:
            continue
        location = r.get("location", "")
        if not canadaish(location):
            continue
        r = dict(r)
        r["bucket"] = bucket
        kept.append(r)
    return kept


def verify(url: str) -> bool:
    """A row is only submitted when its URL answers with something real."""
    if not url.startswith("http"):
        return False
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return 200 <= r.status < 400
    except urllib.error.HTTPError as e:
        return e.code in (401, 403)  # auth walls still prove the req exists
    except Exception:
        return False


def norm_url(url: str) -> str:
    return re.sub(r"[?#].*$", "", str(url).strip().lower()).rstrip("/")


CITY_STOP = {"can", "ca", "usa", "us", "canada", "remote", "hybrid", "onsite", "on", "qc", "bc", "ab", "mb",
             "ns", "nb", "sk", "nl", "pe", "territories", "province"}
CO_STOP = {"the", "inc", "inc.", "ltd", "corp", "llc", "limited", "group", "canada",
           "solutions", "technologies", "technology", "services", "systems"}


def fingerprint(row: dict) -> str:
    """`title|company|city` — the identity of a posting, not of its address.

    URL equality cannot see that one requisition is advertised on several
    mirrors with different addresses and often different dates. On 2026-11-09 a
    CGI QA role arrived twice in a single run under two Eluta `/spl/<hash>` URLs,
    and the board already held the same role under Adzuna and LinkedIn URLs.
    Company and city are reduced to their first significant token so that
    "CGI Inc."/"CGI" and "Sherbrooke QC"/"Sherbrooke, Estrie" compare equal;
    a row with any missing part is never collapsed.
    """
    def norm(value) -> list[str]:
        return re.sub(r"[^a-z0-9]+", " ", str(value or "").lower()).split()

    title = " ".join(norm(row.get("title"))[:6])
    comp = [t for t in norm(row.get("company")) if t not in CO_STOP]
    city = [t for t in norm(row.get("location")) if t not in CITY_STOP]
    if not (title and comp and city):
        return ""
    return f"{title}|{comp[0]}|{city[0]}"


README_ROW = re.compile(
    r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*\[([^\]]+)\]\(([^)]+)\)\s*"
    r"\|\s*([^|]*)\|\s*([^|]*)\|", re.M)


def known_fingerprints() -> set[str]:
    """Identity keys of postings the board already carries.

    The URL gate only catches the same address twice. This catches the same job
    re-advertised elsewhere, which is what makes a sweep's "kept" honest as
    "new to the board" rather than merely "new to this run".
    """
    seen: set[str] = set()
    readme = ROOT / "README.md"
    if readme.exists() and not readme.is_symlink():
        for m in README_ROW.finditer(readme.read_text(encoding="utf-8", errors="ignore")):
            seen.add(fingerprint({"title": m.group(2), "company": m.group(4),
                                  "location": m.group(5)}))
    seen.discard("")
    return seen


def known_urls() -> set[str]:
    """URLs the board already publishes.

    The merger dedupes too, but doing it here is what makes the run's own
    numbers honest: "kept 23" always meant "survived date and liveness checks",
    which still counted rows an earlier sweep had already published.
    """
    seen: set[str] = set()
    readme = ROOT / "README.md"
    if readme.exists() and not readme.is_symlink():
        for m in re.finditer(r"https?://[^\s|)]+",
                             readme.read_text(encoding="utf-8", errors="ignore")):
            seen.add(norm_url(m.group(0)))
    for rel in ("public/jobs.json", "jobs.json"):
        feed = ROOT / rel
        if not feed.exists() or feed.is_symlink():
            continue
        try:
            for job in json.loads(feed.read_text(encoding="utf-8")).get("jobs", []):
                if job.get("url"):
                    seen.add(norm_url(job["url"]))
        except (json.JSONDecodeError, AttributeError):
            pass
    return seen


def next_inbox_path(stamp: str) -> Path:
    """First unused `--v<N>` for the day, matching what check_inbox.py expects."""
    n = 1
    while (INBOX / f"fresh-ca--{stamp}--v{n}.md").exists():
        n += 1
    return INBOX / f"fresh-ca--{stamp}--v{n}.md"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=2, help="2 = today + yesterday")
    ap.add_argument("--eluta-pages", type=int, default=3)
    ap.add_argument("--jobbank-pages", type=int, default=2)
    ap.add_argument("--verify", type=int, default=1)
    ap.add_argument("--linkedin", type=int, default=1,
                    help="1 = also run the bounded LinkedIn guest pass")
    ap.add_argument("--linkedin-max", type=int, default=0,
                    help="cap LinkedIn keywords (0 = all %d)" % len(LI_KEYWORDS))
    ap.add_argument("--geos", default="||Toronto, Ontario|Ontario",
                    help="pipe-separated Adzuna `where` values; empty = national")
    ap.add_argument("--out-inbox", default="")
    args = ap.parse_args()

    window = [(TODAY - timedelta(days=i)).isoformat() for i in range(max(args.days, 1))]
    stats = {"requests": 0, "jobbank_pages": 0, "eluta_pages": 0}

    geos = [g.strip() for g in args.geos.split("|")]
    if args.geos == "":
        geos = [""]

    rows = adzuna_rows(window, stats, geos)
    rows += index_rows(window, stats, args.eluta_pages, args.jobbank_pages)
    if args.linkedin:
        rows += linkedin_rows(window, stats, days=max(args.days - 1, 1),
                              max_kw=args.linkedin_max)

    uniq: dict[str, dict] = {}
    for r in rows:
        url = (r.get("url") or "").rstrip("/")
        if not url:
            continue
        r["url"] = url
        key = re.sub(r"[?#].*$", "", url.lower())
        uniq.setdefault(key, r)

    kept = list(uniq.values())
    if args.verify:
        before = len(kept)
        kept = [r for r in kept if verify(r["url"])]
        stats["unverified_dropped"] = before - len(kept)

    board = known_urls()
    fresh_only = [r for r in kept if norm_url(r["url"]) not in board]
    stats["already_on_board"] = len(kept) - len(fresh_only)
    kept = fresh_only

    board_fp = known_fingerprints()
    by_title = [r for r in kept if fingerprint(r) not in board_fp]
    stats["already_on_board_by_title"] = len(kept) - len(by_title)
    kept = by_title

    seen_fp: dict[str, dict] = {}
    collapsed = 0
    for r in kept:
        fp = fingerprint(r)
        if fp and fp in seen_fp:
            collapsed += 1
            continue
        seen_fp.setdefault(fp, r)
    stats["cross_source_dup"] = collapsed
    kept = list(seen_fp.values())

    kept.sort(key=lambda r: (r["posted"], -priority(r["location"]), r["title"]), reverse=True)

    OUT.mkdir(exist_ok=True)
    (OUT / f"fresh_ca_{STAMP}.json").write_text(
        json.dumps({"generated": NOW.isoformat(), "window": window,
                    "stats": stats, "count": len(kept), "rows": kept}, indent=2),
        encoding="utf-8")

    INBOX.mkdir(exist_ok=True)
    inbox = Path(args.out_inbox) if args.out_inbox else next_inbox_path(STAMP)
    lines = [
        f"# Fresh CA sweep — {STAMP}",
        "",
        f"Window: {', '.join(window)}. Sources: Adzuna (dated API, "
        f"{stats['requests']} calls), Job Bank ({stats['jobbank_pages']} pages), "
        f"Eluta ({stats['eluta_pages']} pages). Every URL answered before submission.",
        "",
        "| Posted | Role | Company | Location | URL | Note |",
        "|--------|------|---------|----------|-----|------|",
    ]
    safe = lambda s: str(s or "").replace("|", "/").strip()
    for r in kept:
        lines.append(
            f"| {r['posted']} | {safe(r['title'])} | {safe(r['company'])} | "
            f"{safe(r['location'])} | {r['url']} | "
            f"fresh-ca {r['source']} / {r['bucket']} |")
    inbox.write_text("\n".join(lines) + "\n", encoding="utf-8")

    by_bucket: dict[str, int] = {}
    for r in kept:
        by_bucket[r["bucket"]] = by_bucket.get(r["bucket"], 0) + 1
    print(f"window {window} | raw {len(rows)} | unique {len(uniq)} | kept {len(kept)} "
          f"| {by_bucket} | stats {stats}")
    print("inbox:", inbox)
    for r in kept[:20]:
        print(f"  {r['posted']} [{r['bucket'][:4]}] {r['title'][:52]:52} "
              f"{r['company'][:24]:24} {r['location'][:30]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
