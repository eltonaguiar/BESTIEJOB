#!/usr/bin/env python3
"""Deep ServiceNow/Salesforce sweep across World Forum Toronto sponsors.

The shallow sweep only reached boards whose URL slug could be guessed, which
meant none of the large consultancies.  Their Workday tenants cannot be derived
from a company name, but they *can* be discovered from search results and then
queried through the CXS API, which returns `postedOn` per posting -- a real date
from the employer rather than a snippet.

Two correctness rules this file enforces:

  * "Posted 30+ Days Ago" is NOT a date.  It means "at least 30 days", so the
    row is left undated instead of being back-dated to exactly 30 days.
  * A posting is Canadian only if its location says so.  "Remote - USA" and
    bare "Remote" are not Canadian; matching the word "remote" alone put US
    roles on a Canadian board.

Usage:
    python3 scripts/sponsor_deep_scan.py --discover      # find ATS tenants
    python3 scripts/sponsor_deep_scan.py --dry-run       # sweep, print only
    python3 scripts/sponsor_deep_scan.py                 # sweep + write inbox
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from parallel_fanout_scan import probe  # noqa: E402
from partner_sponsor_scan_verified import identify  # noqa: E402
from today_feeds_scan import EXCL, KW, fetch_json  # noqa: E402

NOW = datetime.now(timezone.utc)
INBOX = ROOT / "inbox"
RAW = ROOT / "raw" / "partners"
STATE = ROOT / "raw" / "partners" / "workday_tenants.json"

PLATFORMS = ("greenhouse", "lever", "ashby", "smartrecruiters", "workable",
             "recruitee", "bamboohr", "pinpoint")

# Sponsors by tier, then the partner/associate ecosystem around them.  A vendor
# that merely integrates with ServiceNow still hires platform engineers.
COMPANIES: list[tuple[str, str]] = [
    ("Ateko", "diamond"), ("Deloitte Canada", "diamond"),
    ("Ernst & Young", "diamond"), ("KPMG", "diamond"),
    ("Carahsoft", "platinum"), ("Cognizant", "platinum"),
    ("Crossfuze", "platinum"), ("Fujitsu", "platinum"),
    ("Ondaro", "platinum"), ("Tanium", "platinum"),
    ("TeamViewer", "platinum"), ("xtype", "platinum"),
    ("BDO Canada", "gold"), ("Blue Mantis", "gold"), ("Brightfin", "gold"),
    ("CDW", "gold"), ("Compugen", "gold"), ("Dynatrace", "gold"),
    ("Everforth GlideFast", "gold"), ("GlideFast", "gold"),
    ("Flexxible", "gold"), ("IBM", "gold"), ("NewRocket", "gold"),
    ("Pentio", "gold"), ("RapDev", "gold"),
    ("SageX Transformations", "gold"), ("ScreenMeet", "gold"),
    ("TELUS", "gold"), ("Traversal", "gold"), ("Wind River", "gold"),
    ("Tech Mahindra", "bronze"),
    # associates / competing partners named alongside the sponsors
    ("OpenText", "associate"), ("CGI", "associate"), ("Unisys", "associate"),
    ("DXC Technology", "associate"), ("Hitachi Solutions", "associate"),
    ("Long View Systems", "associate"), ("Avanade", "associate"),
    ("Procom", "associate"), ("Robert Half", "associate"),
    ("TEKsystems", "associate"), ("Accenture", "associate"),
    ("Capgemini", "associate"), ("Atos", "associate"),
    ("NTT Data", "associate"), ("Wipro", "associate"),
    ("Infosys", "associate"), ("HCL Technologies", "associate"),
    ("Persistent Systems", "associate"), ("Glidefast Consulting", "associate"),
    ("CloudKettle", "associate"), ("Cask", "associate"),
    ("VividCharts", "associate"), ("Acorio", "associate"),
    # ServiceNow itself hires platform staff and runs its own public board
    ("ServiceNow", "vendor"),
]

WD_RE = re.compile(r"https?://([a-z0-9-]+)\.(wd\d+)\.myworkdayjobs\.com/"
                   r"(?:[a-z]{2}-[A-Z]{2}/)?([A-Za-z0-9_-]+)")
BOARD_RE = [
    ("greenhouse", re.compile(r"(?:job-boards|boards)\.greenhouse\.io/(?:embed/job_board\?for=)?([a-z0-9_-]+)")),
    ("lever", re.compile(r"jobs\.(?:eu\.)?lever\.co/([a-z0-9_-]+)")),
    ("ashby", re.compile(r"jobs\.ashbyhq\.com/([a-z0-9_.-]+)")),
    ("smartrecruiters", re.compile(r"(?:jobs|careers)\.smartrecruiters\.com/([A-Za-z0-9_-]+)")),
]

NOISE = re.compile(r"\b(inc|llc|ltd|corp|corporation|limited|llp|plc|group|"
                   r"canada|the|technologies|technology|solutions|services|"
                   r"systems|business|transformations|consulting|labs)\b", re.I)

# Place names are safe case-insensitively; two-letter province codes are not.
# An earlier `n\.?s\.?\b` matched the "ns" inside "Locations", so every
# multi-location requisition counted as Canadian — the same short-token-in-a-
# long-string failure as matching "rc" inside "salesforce".
CA_FULL = re.compile(r"canada|toronto|ontario|mississauga|markham|brampton|"
                     r"vaughan|etobicoke|scarborough|north york|richmond hill|"
                     r"oakville|burlington|waterloo|kitchener|guelph|ottawa|"
                     r"montr[ée]al|quebec|laval|qu[ée]bec|calgary|edmonton|"
                     r"winnipeg|regina|saskatoon|vancouver|victoria|kelowna|"
                     r"halifax|moncton|fredericton|newfoundland|nunavut|yukon",
                     re.I)
CA_CODE = re.compile(r"\b(?:ON|QC|BC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b")
MULTI = re.compile(r"^\s*\d+\s+locations?\s*$", re.I)
US = re.compile(r"united states|\busa\b|\bu\.s\.\b|\bus\b|america|alabama|alaska|"
                r"arizona|arkansas|california|colorado|connecticut|delaware|"
                r"florida|georgia|hawaii|idaho|illinois|indiana|iowa|kansas|"
                r"kentucky|louisiana|maine|maryland|massachusetts|michigan|"
                r"minnesota|mississippi|missouri|montana|nebraska|nevada|"
                r"new hampshire|new jersey|new mexico|new york|north carolina|"
                r"north dakota|ohio|oklahoma|oregon|pennsylvania|rhode island|"
                r"south carolina|south dakota|tennessee|texas|utah|vermont|"
                r"virginia|washington|west virginia|wisconsin|wyoming", re.I)


def flat(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def tokens(name: str) -> list[str]:
    toks = [w.lower() for w in re.split(r"[^A-Za-z0-9]+", NOISE.sub(" ", name))
            if len(w) >= 3]
    return [flat(name)] + toks


def honest_day(posted_on: str | None) -> str | None:
    """Employer's own wording -> ISO date, or None when it is not a date.

    "30+ Days Ago" is an open-ended bucket, not a day.  Treating it as exactly
    30 days back would understate the posting's age and invent precision.
    """
    if not posted_on:
        return None
    s = posted_on.lower()
    if "30+" in s:
        return None
    if "today" in s:
        return NOW.date().isoformat()
    if "yesterday" in s:
        from datetime import timedelta
        return (NOW.date() - timedelta(days=1)).isoformat()
    m = re.search(r"(\d+)\s*days?\s*ago", s)
    if m:
        from datetime import timedelta
        return (NOW.date() - timedelta(days=int(m.group(1)))).isoformat()
    m = re.search(r"(\d+)\s*hours?\s*ago", s)
    if m:
        return NOW.date().isoformat()
    return None


def is_canadian(loc: str) -> bool:
    """True only when the location actually names a Canadian place."""
    if not loc or MULTI.match(loc):
        return False          # "9 Locations" says nothing about where
    if not (CA_FULL.search(loc) or CA_CODE.search(loc)):
        return False
    if US.search(loc) and not re.search(r"canada", loc, re.I):
        return False
    return True


def workday_jobs(tenant: str, wd: str, site: str, term: str,
                 cap: int = 400) -> list[dict]:
    """Paginate the CXS jobs endpoint; it is the only source with real dates."""
    out, offset, total = [], 0, None
    while offset < (total or cap) and offset < cap:
        try:
            data = fetch_json(
                f"https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/"
                f"{tenant}/{site}/jobs", method="POST",
                body=json.dumps({"appliedFacets": {}, "limit": 20,
                                 "offset": offset, "searchText": term}).encode(),
                headers={"content-type": "application/json"})
        except Exception:
            break
        if total is None:
            total = int(data.get("total") or 0)
        posts = data.get("jobPostings") or []
        if not posts:
            break
        for p in posts:
            out.append({
                "title": p.get("title") or "",
                "company": tenant,
                "location": p.get("locationsText") or "",
                "url": f"https://{tenant}.{wd}.myworkdayjobs.com/en-US/{site}"
                       f"{p.get('externalPath') or ''}",
                "posted": honest_day(p.get("postedOn")),
                "source": "workday",
            })
        offset += 20
    return out


def discover(search) -> dict[str, set]:
    """Find ATS endpoints by asking search where each employer hosts jobs."""
    found: dict[str, set] = {}
    for name, _tier in COMPANIES:
        toks = tokens(name)
        triples, boards = set(), set()
        for q in (f'site:myworkdayjobs.com "{name}" ServiceNow',
                  f'site:myworkdayjobs.com "{name}"',
                  f'"{name}" careers ServiceNow Canada'):
            try:
                hits = search(q, 10)
            except Exception:
                continue
            for h in hits:
                url = h.get("url") or ""
                m = WD_RE.search(url)
                if m:
                    tenant = m.group(1).lower()
                    if any(len(t) >= 4 and (t in tenant or tenant.startswith(t[:4]))
                           for t in toks[:1]) or flat(tenant) == flat(name)[:len(tenant)]:
                        triples.add((m.group(1), m.group(2), m.group(3)))
                for plat, rx in BOARD_RE:
                    m2 = rx.search(url)
                    if m2:
                        boards.add((plat, m2.group(1)))
            if triples or boards:
                break
        if triples or boards:
            found[name] = {"workday": sorted(triples), "boards": sorted(boards)}
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--discover", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--cap", type=int, default=400)
    args = ap.parse_args()

    from web_search_scan import search_tavily

    if args.discover or not STATE.exists():
        found = discover(search_tavily)
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(found, indent=1))
        print(f"discovered ATS endpoints for {len(found)} of {len(COMPANIES)} companies")
        for k, v in found.items():
            print(f"  {k:24s} workday={v['workday']} boards={v['boards']}")
        if args.discover:
            return 0

    found = json.loads(STATE.read_text())
    rows: dict[str, dict] = {}
    seen_post: set[tuple] = set()
    stats = []

    def add(j, label):
        url = (j.get("url") or "").split("?")[0]
        if not url or url in rows:
            return
        title = j.get("title") or ""
        if EXCL.search(title) or not KW.search(title):
            return
        # One vacancy can be mirrored across several Workday sites (Robert Half
        # publishes the same req on its staffing and Protiviti boards).
        k = (label, title.strip().lower(), j.get("posted"),
             (j.get("location") or "").strip().lower())
        if k in seen_post:
            return
        seen_post.add(k)
        j["company"] = label
        rows[url] = j

    for name, kinds in found.items():
        before = len(rows)
        for tenant, wd, site in kinds.get("workday", []):
            for term in ("servicenow", "salesforce"):
                for j in workday_jobs(tenant, wd, site, term, args.cap):
                    if is_canadian(j["location"]):
                        add(j, name)
        for plat, slug in kinds.get("boards", []):
            # A slug is not an employer: TeamViewer/CloudKettle/Acorio all
            # resolve to smartrecruiters:ServiceNow, ServiceNow's own board.
            if not identify(plat, slug, name)[0]:
                continue
            for j in probe(plat, slug):
                if is_canadian(j.get("location") or ""):
                    add(j, name)
        if len(rows) > before:
            stats.append((name, len(rows) - before))

    dated = [r for r in rows.values() if r.get("posted")]
    print(f"\ncompanies swept  : {len(found)}")
    print(f"Canadian rows    : {len(rows)} ({len(dated)} with a real date)")
    for name, n in sorted(stats, key=lambda x: -x[1]):
        print(f"  {name:24s} +{n}")
    for r in sorted(dated, key=lambda r: r["posted"], reverse=True):
        print("  %-11s %-22s %-44s %s" % (r["posted"], r["company"][:22],
                                          (r["title"] or "")[:44],
                                          (r["location"] or "")[:26]))

    if args.dry_run or not dated:
        return 0

    INBOX.mkdir(exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    stamp = NOW.strftime("%Y-%m-%dT%H%M%SZ")
    (RAW / f"sponsor-deep-{stamp}.json").write_text(
        json.dumps(sorted(dated, key=lambda r: r["posted"], reverse=True),
                   indent=1, ensure_ascii=False))
    day = NOW.strftime("%Y-%m-%d")
    path = INBOX / f"sponsor-deep--{day}--v1.md"
    body = ["---", "model: sponsor-deep", f"scanned_at: {stamp}",
            "task: servicenow-world-forum-sponsors-deep", "---", "",
            f"# Sponsor deep sweep — {day}", "",
            f"{len(found)} sponsors and associates, queried through their own "
            f"Workday CXS endpoints and public boards. {len(dated)} Canadian "
            f"postings carrying a date from the employer.", "",
            "| Posted | Role | Company | Location | Source |", "|---|---|---|---|---|"]
    for r in sorted(dated, key=lambda r: r["posted"], reverse=True):
        t = (r["title"] or "").replace("|", "/")
        body.append(f"| {r['posted']} | [{t}]({r['url']}) | {r['company']} | "
                    f"{(r['location'] or '').strip()} | via {r['source']} |")
    path.write_text("\n".join(body) + "\n")
    print(f"\nwrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
