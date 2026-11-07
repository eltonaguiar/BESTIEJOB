#!/usr/bin/env python3
"""Scan ServiceNow World Forum Toronto sponsors for ServiceNow/Salesforce roles.

Two lanes, because a sponsor name is *not* a board:

  boards   Guess ATS slugs for each sponsor, then prove the board is really
           theirs by reading the board page's own <title>.  Without that check a
           guess like "kpmg" lands on an unrelated firm in Mayfair, and the rows
           get misattributed to KPMG.

  search   The large consultancies (Deloitte, EY, KPMG, IBM, Fujitsu, Cognizant,
           CDW, TELUS, OpenText) run Workday/SuccessFactors/Taleo tenants whose
           path cannot be derived from a name.  For those, ask the search APIs
           for postings on the employer's own domain or ATS, and keep only rows
           whose text actually names the platform and a Canadian location.

Nothing infers a date: a row carries `posted` only when the employer's own board
published one.  Search-lane rows stay undated unless the board also surfaced them.

Usage:
    python3 scripts/partner_sponsor_scan.py --dry-run
    python3 scripts/partner_sponsor_scan.py
    python3 scripts/partner_sponsor_scan.py --boards-only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from parallel_fanout_scan import probe  # noqa: E402
from today_feeds_scan import EXCL, GEO, KW, workday_day  # noqa: E402

try:
    from curl_cffi import requests as cr
except ImportError:                       # curl_cffi is optional; Workday needs it
    cr = None

NOW = datetime.now(timezone.utc)
INBOX = ROOT / "inbox"
RAW = ROOT / "raw" / "partners"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

PLATFORMS = ("greenhouse", "lever", "ashby", "smartrecruiters", "workable",
             "recruitee", "bamboohr", "pinpoint")

BOARD_PAGE = {
    "greenhouse": "https://boards.greenhouse.io/{s}",
    "lever": "https://jobs.lever.co/{s}",
    "ashby": "https://jobs.ashbyhq.com/{s}",
    "smartrecruiters": "https://jobs.smartrecruiters.com/{s}",
    "workable": "https://apply.workable.com/{s}",
    "recruitee": "https://{s}.recruitee.com",
    "bamboohr": "https://{s}.bamboohr.com/careers",
    "pinpoint": "https://{s}.pinpointhq.com",
}

# ServiceNow World Forum Toronto sponsors by tier, plus the Canadian partner
# ecosystem.  Vendors that merely integrate with ServiceNow are probed too --
# they do hire platform engineers.
SPONSORS: list[tuple[str, str]] = [
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
    ("OpenText", "associate"), ("Hitachi Solutions", "associate"),
    ("Unisys", "associate"), ("DXC Technology", "associate"),
    ("CGI", "associate"), ("Long View Systems", "associate"),
    ("ThinkOn", "associate"), ("Compugen Finance", "associate"),
    ("Procom", "associate"), ("Robert Half", "associate"),
    ("TEKsystems", "associate"), ("Avanade", "associate"),
]

# A Workday triple is tenant|wdN|site.  Wrong guesses simply return nothing.
WORKDAY = [
    ("opentext", "wd3", "OpenText", "OpenText"),
    ("cgi", "wd3", "CGI_Careers", "CGI"),
    ("ibm", "wd1", "External", "IBM"),
    ("deloitte", "wd3", "Deloitte_Careers", "Deloitte Canada"),
    ("kpmgca", "wd3", "KPMGCanada", "KPMG"),
    ("ey", "wd3", "EYCareers", "Ernst & Young"),
    ("cdw", "wd1", "cdw", "CDW"),
    ("telus", "wd3", "TELUS_Careers", "TELUS"),
    ("cognizant", "wd1", "Cognizant", "Cognizant"),
    ("techmahindra", "wd3", "Tech_Mahindra", "Tech Mahindra"),
    ("fujitsu", "wd3", "Fujitsu", "Fujitsu"),
    ("bdo", "wd3", "BDO", "BDO Canada"),
    ("unisys", "wd1", "Unisys", "Unisys"),
    ("dxc", "wd3", "DXC", "DXC Technology"),
    ("avanade", "wd3", "Avanade", "Avanade"),
]

NOISE = re.compile(r"\b(inc|llc|ltd|corp|corporation|limited|llp|plc|group|"
                   r"canada|the|technologies|technology|solutions|services|"
                   r"systems|business|transformations|finance)\b", re.I)

# Aggregators are only trusted when the posting's own slug names the employer.
AGGREGATOR = re.compile(r"(linkedin\.com|indeed\.|glassdoor\.|ziprecruiter\.|"
                        r"talent\.com|jobillico\.|sercanto\.|trabajo\.org|"
                        r"jobrapido\.|neuvoo\.|eluta\.|careerjet\.|jooble\.|"
                        r"builtin\.com|simplyhired\.)", re.I)
ATS_DOMAIN = re.compile(r"(greenhouse\.io|lever\.co|ashbyhq\.com|"
                        r"smartrecruiters\.com|myworkdayjobs\.com|workable\.com|"
                        r"bamboohr\.com|recruitee\.com|pinpointhq\.com|icims\.com|"
                        r"successfactors\.|taleo\.net|jobvite\.com|workday\.com)", re.I)

# A search hit is only a posting if its title names a role.  Careers index
# pages, job alerts and company news all mention the platform without being
# vacancies.
ROLE = re.compile(r"\b(developer|consultant|engineer|architect|administrator|"
                  r"admin|analyst|specialist|lead|manager|director|programmer|"
                  r"integrator|tester|owner|coordinator)\b", re.I)
LANDING = re.compile(r"(careers?\b|job alerts|join our team|open roles|jobs at|"
                     r"search jobs|browse jobs|talent pool|why join)", re.I)
NEWS = re.compile(r"(/news/|/blog/|/press|/insights/|/article/|/community/|"
                  r"/interview/|acquires|announces|award|webinar|case study|"
                  r"hire-talent|search-candidates)", re.I)
# An individual posting, not a listing page: a job path with an identifier.
INDIVIDUAL = re.compile(r"(/job/|/jobs/view/|/jobs/\d|/postings?/\d|/careers?/.+\d{4,}|"
                        r"-\d{6,}(/|\?|$)|\d{6,}-)", re.I)
# Search mirrors.  Kept only when the employer's own board did not surface
# the same role, because a mirror can outlive the posting it copied.
MIRROR = re.compile(r"(theladders|ziprecruiter|remote\.io|expertini|prosple|"
                    r"glassdoor|roberthalf|talent\.com|jobillico|eluta|neuvoo|"
                    r"careerjet|jooble|simplyhired|linkedin\.com)", re.I)


def slug_candidates(name: str) -> list[str]:
    base = NOISE.sub(" ", name)
    words = [w for w in re.split(r"[^A-Za-z0-9]+", base) if w]
    if not words:
        return []
    out = ["".join(words).lower(), "-".join(w.lower() for w in words),
           words[0].lower()]
    if len(words) > 1:
        out.append("".join(w[0] for w in words).lower())
    seen, uniq = set(), []
    for s in out:
        if len(s) >= 3 and s not in seen:
            seen.add(s)
            uniq.append(s)
    return uniq


def name_tokens(name: str) -> list[str]:
    """Significant lower-case words identifying an employer."""
    toks = [w.lower() for w in re.split(r"[^A-Za-z0-9]+", NOISE.sub(" ", name))
            if len(w) >= 3]
    whole = re.sub(r"[^a-z0-9]", "", name.lower())
    return [whole] + toks


def board_title(platform: str, slug: str) -> str | None:
    """The public board page's <title>, used to prove the board's identity."""
    tpl = BOARD_PAGE.get(platform)
    if not tpl:
        return None
    try:
        req = urllib.request.Request(tpl.format(s=slug), headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=15) as r:
            html = r.read(6000).decode("utf8", "ignore")
    except Exception:
        return None
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else None


def identify(platform: str, slug: str, name: str) -> tuple[bool, str]:
    """True when the board page names the sponsor the slug was guessed from."""
    title = board_title(platform, slug)
    if not title:
        return False, "no board page to verify"
    # A slug guess can land on a vendor's demo/trial tenant (lever:blue-mantis
    # resolved to "Blue Mantis Trial").  Those boards carry no real postings, so
    # the name match alone is not proof of the employer's own board.
    if re.search(r"\b(trial|demo|sandbox|test|staging)\b", title, re.I):
        return False, f"{title} (demo/trial board, not the employer)"
    flat = re.sub(r"[^a-z0-9]", "", title.lower())
    for tok in name_tokens(name):
        if len(tok) >= 4 and tok in flat:
            return True, title
    return False, title


def workday_probe(tenant: str, wd: str, site: str, label: str) -> list[dict]:
    """Probe a Workday CXS endpoint with a browser TLS fingerprint.

    `parallel_fanout_scan.probe()` posts through urllib, and Workday's CXS
    endpoint rejects that handshake — every tenant except one came back empty
    even though the same tenants answer curl_cffi with HTTP 200 (proved in the
    round-4 ATS pass).  Both platform keywords are asked for, because a single
    "servicenow" search silently skips every Salesforce-only tenant.
    """
    if cr is None:
        return []
    host = f"{tenant}.{wd}.myworkdayjobs.com"
    url = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
    out: list[dict] = []
    for keyword in ("ServiceNow", "Salesforce"):
        body = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": keyword}
        try:
            r = cr.post(url, json=body, impersonate="chrome124", timeout=25,
                        headers={"User-Agent": UA, "Accept": "application/json",
                                 "Content-Type": "application/json"})
        except Exception:
            continue
        if r.status_code != 200:
            continue
        try:
            data = r.json()
        except Exception:
            continue
        for p in data.get("jobPostings") or []:
            out.append({"title": p.get("title") or "", "company": label,
                        "location": p.get("locationsText") or "",
                        "url": f"https://{host}/en-US/{site}{p.get('externalPath', '')}",
                        "posted": workday_day(p.get("postedOn") or ""),
                        "sponsor": True, "source": f"workday:{tenant}"})
    return out


def relevant(j: dict, require_title: bool = True) -> bool:
    title = j.get("title") or ""
    if EXCL.search(title):
        return False
    if require_title and not KW.search(title):
        return False
    loc = j.get("location") or ""
    return bool(GEO.search(loc)) or loc.strip() == ""


def scan_boards() -> tuple[list[dict], dict]:
    rows, report, seen = [], {}, set()

    def take(jobs, label):
        kept = 0
        for j in jobs:
            url = (j.get("url") or "").split("?")[0]
            if not url or url in seen or not relevant(j):
                continue
            seen.add(url)
            j["company"] = label
            j["sponsor"] = True
            rows.append(j)
            kept += 1
        return kept

    for name, tier in SPONSORS:
        resolved = None
        for platform in PLATFORMS:
            if resolved:
                break
            for slug in slug_candidates(name)[:3]:
                if not probe(platform, slug):
                    continue
                ok, title = identify(platform, slug, name)
                if ok:
                    resolved = (platform, slug, title)
                else:
                    report.setdefault(f"__rejected__{name}", []).append(
                        f"{platform}:{slug} -> {title or 'page unreachable'}")
                break
        if not resolved:
            report[name] = f"{tier}: no verifiable public board"
            continue
        platform, slug, title = resolved
        n = take(probe(platform, slug), name)
        report[name] = f"{tier}: {platform}:{slug} verified as '{title[:40]}' — {n} row(s)"

    answering = 0
    for tenant, wd, site, label in WORKDAY:
        jobs = workday_probe(tenant, wd, site, label)
        if jobs:
            answering += 1
            report[label] = (f"workday: tenant {tenant} answered — "
                             f"{take(jobs, label)} row(s)")
        else:
            report[label] = f"workday: tenant {tenant} — no answer or no SN/SF title"
    print(f"workday tenants answering : {answering}/{len(WORKDAY)}")
    return rows, report


def scan_search(sponsors: list[tuple[str, str]]) -> tuple[list[dict], dict]:
    from web_search_scan import search_exa, search_firecrawl, search_tavily

    # Firecrawl first. As of 2026-11-04 Tavily answers HTTP 432 (plan set-usage
    # limit exceeded) and Exa answers HTTP 402 (credits exhausted); Firecrawl is
    # the only provider returning results, so it must be tried before the dead
    # ones — `except Exception: continue` then falls through to them harmlessly.
    searchers = [("firecrawl", search_firecrawl), ("tavily", search_tavily),
                 ("exa", search_exa)]
    rows, report, seen = [], {}, set()
    for name, tier in sponsors:
        queries = [
            f'"{name}" ServiceNow developer OR administrator OR consultant '
            f'"Canada" job posting',
            f'site:myworkdayjobs.com "{name}" ServiceNow',
            f'site:myworkdayjobs.com "{name}" Salesforce',
        ]
        found = 0
        for q in queries:
            for label, fn in searchers:
                try:
                    hits = fn(q, 10)
                except Exception:
                    continue
                for h in hits:
                    url = (h.get("url") or "").split("?")[0]
                    if not url or url in seen:
                        continue
                    title = h.get("title") or ""
                    text = f"{title} {h.get('snippet') or ''}"
                    if not KW.search(text) or EXCL.search(title):
                        continue
                    if not ROLE.search(title) or LANDING.search(title):
                        continue          # careers index page, not a vacancy
                    if NEWS.search(url) or NEWS.search(title):
                        continue          # press release / blog
                    if not (GEO.search(text) or re.search(r"\bremote\b", text, re.I)):
                        continue
                    if not INDIVIDUAL.search(url):
                        continue          # a listing or landing page
                    slugflat = re.sub(r"[^a-z0-9]", "", name.lower())
                    hostpath = re.sub(r"[^a-z0-9]", "", url.lower())
                    # A Workday URL is only the employer's when its tenant names
                    # them: ou medicine and martin are different companies that
                    # merely share the myworkdayjobs.com suffix.
                    wd = re.match(r"https?://([a-z0-9-]+)\.[a-z0-9-]+\.myworkdayjobs\.com",
                                  url, re.I)
                    if wd:
                        tenant = wd.group(1).lower()
                        if not (slugflat[:4] in tenant or tenant[:4] in slugflat):
                            continue
                        owned = True
                    else:
                        owned = bool(ATS_DOMAIN.search(url)) or slugflat[:6] in hostpath
                    if not owned:
                        continue          # not the employer's own board
                    mirror = bool(MIRROR.search(url))
                    if mirror and slugflat not in hostpath:
                        continue          # mirror that does not name the employer
                    seen.add(url)
                    rows.append({"title": h.get("title") or "", "company": name,
                                 "sponsor": True, "location": "", "url": url,
                                 "posted": None, "source": f"search:{label}"})
                    found += 1
            if found:
                break
        if found:
            report[name] = f"{tier}: {found} posting(s) via search"
    return rows, report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--boards-only", action="store_true")
    args = ap.parse_args()

    rows, report = scan_boards()
    print(f"boards lane : {len(rows)} relevant postings")

    if not args.boards_only:
        srows, sreport = scan_search(SPONSORS)
        print(f"search lane : {len(srows)} relevant postings")
        have = {r["url"] for r in rows}
        for r in srows:
            if r["url"] not in have:
                rows.append(r)
                have.add(r["url"])
        report.update(sreport)

    # Prefer the employer's own posting over a search mirror of the same role:
    # mirrors outlive the vacancy they copied.
    key = lambda r: (r["company"],
                     re.sub(r"\W+", "", (r.get("title") or "").lower())[:28])
    owned = {key(r) for r in rows if not MIRROR.search(r["url"])}
    before = len(rows)
    rows = [r for r in rows if not (MIRROR.search(r["url"]) and key(r) in owned)]
    if before != len(rows):
        print(f"mirror rows dropped : {before - len(rows)}")

    rejected = {k: v for k, v in report.items() if k.startswith("__rejected__")}
    live = {k: v for k, v in report.items()
            if not k.startswith("__rejected__") and "no verifiable" not in v}
    print(f"sponsors with a confirmed posting: {len(live)}")

    for r in rows:
        print("  %-11s %-26s %-46s %s" % (r.get("posted") or "undated",
                                          (r["company"] or "")[:26],
                                          (r.get("title") or "")[:46],
                                          r.get("source")))
    if rejected:
        print("\nslug guesses rejected by identity check (wrong company):")
        for k, v in rejected.items():
            print(f"  {k.replace('__rejected__', ''):24s} {v}")

    if args.dry_run or not rows:
        return 0

    INBOX.mkdir(exist_ok=True)
    RAW.mkdir(parents=True, exist_ok=True)
    stamp = NOW.strftime("%Y-%m-%dT%H%M%SZ")
    (RAW / f"sponsor-scan-{stamp}.json").write_text(
        json.dumps({"scanned_at": stamp, "report": report, "rows": rows},
                   indent=1, ensure_ascii=False))

    day = NOW.strftime("%Y-%m-%d")
    out = INBOX / f"partner-sponsors--{day}.md"
    dated = sum(1 for r in rows if r.get("posted"))
    body = ["---", "model: partner-sponsors", f"scanned_at: {stamp}",
            "task: servicenow-world-forum-toronto-sponsors", "---", "",
            f"# ServiceNow World Forum Toronto sponsors — {day}", "",
            f"{len(SPONSORS)} sponsors and associates probed. Board slugs were "
            f"accepted only when the board page's own title named the employer; "
            f"{len(rows)} relevant postings kept ({dated} dated by the employer, "
            f"{len(rows) - dated} undated).", "",
            "| Posted | Role | Company | Location | Source |",
            "|---|---|---|---|---|"]
    for r in rows:
        t = (r.get("title") or "").replace("|", "/")
        body.append(f"| {r.get('posted') or '—'} | [{t}]({r['url']}) | "
                    f"{r['company']} | {(r.get('location') or '').strip()} | "
                    f"{r.get('source')} |")
    out.write_text("\n".join(body) + "\n")
    print(f"\nwrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
