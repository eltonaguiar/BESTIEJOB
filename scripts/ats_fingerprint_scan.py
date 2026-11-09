#!/usr/bin/env python3
"""Multi-employer ATS scan (2026-11-02).

For each candidate employer: fetch the careers page, fingerprint which ATS it
runs, then query that ATS's public endpoint for ServiceNow / Salesforce / ITSM
requisitions, resolving exact posting dates.

Supported routes
  workday        /wday/cxs/<tenant>/<site>/jobs  (POST) + detail JSON-LD
  oracle         /hcmRestApi/.../recruitingCEJobRequisitions
  phenom         /sitemap.xml -> requisition JSON-LD
  smartrecruiters api.smartrecruiters.com/v1/companies/<slug>/postings
  greenhouse     boards-api.greenhouse.io/v1/boards/<slug>/jobs
  lever          api.lever.co/v0/postings/<slug>
  successfactors / icims / taleo / avature / eightfold: no public search (recorded)

Usage
  python3 scripts/ats_fingerprint_scan.py                 # write inbox submission
  python3 scripts/ats_fingerprint_scan.py --apply         # merge + rebuild site
  python3 scripts/ats_fingerprint_scan.py --only workday  # single route
"""
from __future__ import annotations

import argparse
import glob
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from curl_cffi import requests as cr
except ImportError:
    sys.exit("FATAL: curl_cffi not installed (pip install curl_cffi)")

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
RAW = ROOT / "raw"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

CANDIDATES = {
    # ---- banks / finance
    "RBC": "https://jobs.rbc.com",
    "TD": "https://td.wd3.myworkdayjobs.com/TD_Bank_Careers",
    "BMO": "https://jobs.bmo.com",
    "CIBC": "https://www.cibc.com/en/about-cibc/careers.html",
    "Scotiabank": "https://www.scotiabank.com/careers/en/home.html",
    "National Bank": "https://www.nbc.ca/en/careers.html",
    "Desjardins": "https://www.desjardins.com/careers/index.jsp",
    "ATB Financial": "https://www.atb.com/careers/",
    "Manulife": "https://www.manulife.com/en/careers",
    "Sun Life": "https://www.sunlife.com/en/careers/",
    "Canada Life": "https://www.canadalife.com/careers.html",
    "Intact": "https://www.intactfc.com/en/careers/",
    "Co-operators": "https://www.cooperators.ca/en/about-us/careers",
    "Equitable Bank": "https://www.eqbank.ca/careers",
    "Canada Post": "https://www.canadapost-postescanada.ca/cpc/en/our-company/careers.page",
    # ---- telcos
    "Bell": "https://jobs.bell.ca",
    "Rogers": "https://jobs.rogers.com",
    "Telus": "https://www.telus.com/en/about/careers",
    "Videotron": "https://www.videotron.com/carrieres",
    "Cogeco": "https://www.cogeco.com/careers",
    "SaskTel": "https://www.sasktel.com/about-us/careers",
    # ---- retail / logistics
    "Loblaw": "https://www.loblaw.ca/en/careers.html",
    "Metro": "https://www.metro.ca/en/careers",
    "Walmart Canada": "https://careers.walmart.ca",
    "Canadian Tire": "https://corp.canadiantire.ca/English/careers/default.aspx",
    "Home Depot Canada": "https://careers.homedepot.ca",
    "Empire/Sobeys": "https://www.empireco.ca/careers/",
    "Purolator": "https://www.purolator.com/en/about-purolator/careers",
    # ---- tech / product
    "Dayforce": "https://www.dayforce.com/us/company/careers",
    "Workday": "https://www.workday.com/en-us/company/careers.html",
    "ServiceNow": "https://careers.servicenow.com",
    "Salesforce": "https://careers.salesforce.com",
    "Shopify": "https://www.shopify.com/careers",
    "OpenText": "https://careers.opentext.com",
    "Docebo": "https://www.docebo.com/company/careers/",
    "Kinaxis": "https://www.kinaxis.com/en/careers",
    "Constellation Software": "https://www.csisoftware.com/careers",
    # ---- consulting / integrators
    "CGI": "https://www.cgi.com/en/careers",
    "Deloitte": "https://careers.deloitte.ca",
    "KPMG": "https://kpmg.com/ca/en/home/careers.html",
    "PwC": "https://www.pwc.com/ca/en/careers.html",
    "EY": "https://www.ey.com/en_ca/careers",
    "Accenture": "https://www.accenture.com/ca-en/careers",
    "IBM": "https://www.ibm.com/careers",
    "Cognizant": "https://careers.cognizant.com/global/en",
    "Infosys": "https://www.infosys.com/careers/",
    "TCS": "https://www.tcs.com/careers",
    "Capgemini": "https://www.capgemini.com/careers/",
    "Slalom": "https://www.slalom.com/careers",
    "Long View Systems": "https://www.longviewsystems.com/careers/",
    "Artech": "https://www.artech.com/careers/",
    # ---- public sector / utilities / health / education
    "City of Toronto": "https://www.toronto.ca/city-government/council/jobs/",
    "TTC": "https://www.ttc.ca/careers",
    "Metrolinx": "https://www.metrolinx.com/en/careers",
    "Ontario Health": "https://www.ontariohealth.ca/careers",
    "OPG": "https://www.opg.com/careers/",
    "Hydro One": "https://www.hydroone.com/careers",
    "Toronto Hydro": "https://www.torontohydro.com/careers",
    "Enbridge": "https://www.enbridge.com/careers",
    "UHN": "https://www.uhn.ca/careers",
    "SickKids": "https://www.sickkids.ca/en/careers/",
    "University of Toronto": "https://people.utoronto.ca/careers/",
    "York University": "https://www.yorku.ca/careers/",
    "TMU": "https://www.torontomu.ca/careers/",
}

KEYWORDS = ["ServiceNow", "Salesforce", "ITSM", "CMDB"]

RELEVANT = re.compile(
    r"servicenow|salesforce|itsm|itam|cmdb|itom|\bsnow\b|apex|mulesoft|"
    r"integration hub|service catalog|grc|now assist|fusion risk|policy and compliance|vendor risk|"
    r"performance analytics|discovery|service mapping|alteryx|vba|data analyst|reporting analyst|"
    r"business systems analyst|asset management|ham|sam|itil|workflow editor|ui policies|ui actions|"
    r"scheduled jobs|javascript|html|css|rest|soap|mid server|acls|csdm|update sets|delegated development|"
    r"application scopes|git|github|agile|scrum|data integration|automation studio|email studio|ampscript|cpq", re.I)
EXCLUDE = re.compile(
    r"sales\s+(representative|associate|manager|consultant|lead|agent)|"
    r"account executive|retail|store manager|cashier|teller|barista", re.I)

CANADA = re.compile(r"toronto|ontario|mississauga|markham|montreal|montr|quebec|ottawa|"
                    r"calgary|vancouver|edmonton|waterloo|canada|brampton|scarborough|"
                    r"north york|laval|brossard|halifax|winnipeg|victoria|regina|saskatoon|"
                    r"greater toronto|remote", re.I)

TITLE = re.compile(r'"title"\s*:\s*"([^"]{4,160})"')
DATE = re.compile(r'"datePosted"\s*:\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})')
LOC = re.compile(r'"addressLocality"\s*:\s*"([^"]+)"')

# ---------------------------------------------------------------- fingerprint
WD_LINK = re.compile(
    r"https?://([a-z0-9\-]+)\.(wd\d+)\.myworkdayjobs\.com(?:/(?:[a-z]{2}-[A-Z]{2}))?/([A-Za-z0-9_\-]+)")
WDSITE_LINK = re.compile(r"myworkdaysite\.com/(?:recruiting|en-US)/([A-Za-z0-9_\-]+)/([A-Za-z0-9_\-]+)")
PHENOM = re.compile(r"cdn\.phenompeople\.com/CareerConnectResources/(?:prod|pp|pcs|[A-Z0-9]+)/([A-Z0-9]{4,})/")
ORACLE = re.compile(r"https?://([a-z0-9.\-]+\.oraclecloud\.com)/hcmUI/CandidateExperience/[a-z\-]+/sites/([A-Z0-9_]+)")
SMARTREC = re.compile(r"(?:jobs|careers)\.smartrecruiters\.com/([A-Za-z0-9\-]{2,})")
SF = re.compile(r"([a-z0-9\-]+)\.successfactors\.(?:com|eu)")
GH = re.compile(r"boards\.greenhouse\.io/([a-z0-9\-]{2,})")
LEVER = re.compile(r"jobs\.lever\.co/([a-z0-9\-]{2,})")
ICIMS = re.compile(r"([a-z0-9\-]+)\.icims\.com")
TALEO = re.compile(r"([a-z0-9\-]+)\.taleo\.net")
AVATURE = re.compile(r"([a-z0-9\-]+)\.avature\.net")
EIGHTFOLD = re.compile(r"([a-z0-9\-]+)\.eightfold\.ai")


def fetch(url, timeout=25, **kw):
    try:
        return cr.get(url, impersonate="chrome124", timeout=timeout,
                      headers={"User-Agent": UA}, **kw)
    except Exception:
        return None


def fingerprint(name: str, url: str) -> dict:
    r = fetch(url)
    if r is None:
        return {"name": name, "url": url, "status": "unreachable"}
    html = r.text
    f: dict = {"name": name, "url": url, "status": r.status_code}

    wd = WD_LINK.search(html)
    if wd:
        f["workday"] = {"tenant": wd.group(1), "host": f"{wd.group(1)}.{wd.group(2)}.myworkdayjobs.com",
                        "site": wd.group(3)}
    else:
        wds = WDSITE_LINK.search(html)
        if wds:
            f["workday"] = {"tenant": wds.group(1), "host": None, "site": wds.group(2)}
    ph = PHENOM.search(html)
    if ph:
        f["phenom"] = ph.group(1)
    orc = ORACLE.search(html)
    if orc:
        f["oracle"] = {"host": orc.group(1), "site": orc.group(2)}
    sr = SMARTREC.search(html)
    if sr:
        f["smartrecruiters"] = sr.group(1)
    gh = GH.search(html)
    if gh:
        f["greenhouse"] = gh.group(1)
    lv = LEVER.search(html)
    if lv:
        f["lever"] = lv.group(1)
    for key, pat in (("successfactors", SF), ("icims", ICIMS), ("taleo", TALEO),
                     ("avature", AVATURE), ("eightfold", EIGHTFOLD)):
        m = pat.search(html)
        if m:
            f[key] = m.group(1)
    if "workday" in html.lower() and "workday" not in f:
        f["workday_hint"] = True
    return f


# ---------------------------------------------------------------- scanners
def clean(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def relevant(title: str) -> bool:
    return bool(RELEVANT.search(title)) and not EXCLUDE.search(title)


def workday_search(wd: dict, keyword: str):
    if not wd.get("host"):
        return []
    url = f"https://{wd['host']}/wday/cxs/{wd['tenant']}/{wd['site']}/jobs"
    body = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": keyword}
    try:
        r = cr.post(url, json=body, impersonate="chrome124", timeout=25,
                    headers={"User-Agent": UA, "Accept": "application/json",
                             "Content-Type": "application/json"})
    except Exception:
        return []
    if r.status_code != 200:
        return []
    try:
        data = r.json()
    except Exception:
        return []
    out = []
    for p in data.get("jobPostings", []):
        title = clean(p.get("title", ""))
        if not relevant(title):
            continue
        out.append({"title": title, "location": clean(p.get("locationsText", "")),
                    "url": f"https://{wd['host']}/en-US/{wd['site']}{p.get('externalPath','')}",
                    "posted": None})
    return out


REGION = re.compile(r'"addressRegion"\s*:\s*"([^"]+)"')
COUNTRY = re.compile(r'"addressCountry"\s*:\s*"([^"]+)"')


def workday_detail(url: str):
    """(datePosted, location) — needed because multi-location reqs have an
    empty `locationsText` in the listing API."""
    r = fetch(url)
    if r is None or r.status_code != 200:
        return None, ""
    m, loc = DATE.search(r.text), LOC.search(r.text)
    region, country = REGION.search(r.text), COUNTRY.search(r.text)
    where = ", ".join(x for x in [loc.group(1) if loc else "",
                                  region.group(1) if region else "",
                                  country.group(1) if country else ""] if x)
    return (m.group(1) if m else None), where


def oracle_search(orc: dict):
    out = []
    for kw in ("ServiceNow", "Salesforce"):
        url = (f"https://{orc['host']}/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
               "?onlyData=true&expand=requisitionList.secondaryLocations"
               f"&finder=findReqs;siteNumber={orc['site']},keyword={kw},limit=25,offset=0,"
               "sortBy=POSTING_DATES_DESC")
        r = fetch(url, timeout=30)
        if r is None or r.status_code != 200:
            continue
        try:
            items = r.json().get("items") or []
        except Exception:
            continue
        for it in items:
            for req in it.get("requisitionList", []):
                title = clean(req.get("Title", ""))
                if not relevant(title):
                    continue
                out.append({"title": title,
                            "location": clean(req.get("PrimaryLocation", "")),
                            "url": (f"https://{orc['host']}/hcmUI/CandidateExperience/en/sites/"
                                    f"{orc['site']}/job/{req.get('Id','')}"),
                            "posted": (req.get("PostedDate") or "")[:10] or None})
    return out


def sitemap_urls(entry: str, depth: int = 0):
    if depth > 2:
        return []
    r = fetch(entry, timeout=30)
    if r is None or r.status_code != 200:
        return []
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
    if "<sitemapindex" in r.text:
        out = []
        for loc in locs:
            out.extend(sitemap_urls(loc, depth + 1))
        return out
    return locs


def phenom_search(base: str, tid: str):
    out = []
    for u in sitemap_urls(base.rstrip("/") + "/sitemap.xml"):
        if "/job/" not in u:
            continue
        if not RELEVANT.search(u.split("/job/", 1)[-1]):
            continue
        r = fetch(u)
        if r is None or r.status_code != 200:
            continue
        t, d = TITLE.search(r.text), DATE.search(r.text)
        if not (t and d):
            continue
        loc = LOC.search(r.text)
        if not relevant(t.group(1)):
            continue
        out.append({"title": clean(t.group(1)), "posted": d.group(1),
                    "location": loc.group(1) if loc else "", "url": u})
    return out


SITEMAP_PATHS = ("/sitemap.xml", "/sitemap_index.xml", "/sitemap-index.xml",
                  "/job-sitemap.xml", "/sitemaps/sitemap.xml")
JOB_PATH = re.compile(r"/job|/jobs/|/careers?/|/position|/opening", re.I)
SLUG_KW = re.compile(r"servicenow|salesforce|itsm|itom|itm|cmdb|mulesoft|servicenowdev", re.I)


def sitemap_search(base: str, cap: int = 40):
    """Generic route: career-site sitemap -> keyword slug -> detail JSON-LD.

    Keyword matching happens on the URL *path*, not the whole URL, otherwise a
    host like careers.servicenow.com matches every single entry.
    """
    urls: list[str] = []
    for p in SITEMAP_PATHS:
        urls = sitemap_urls(base.rstrip("/") + p)
        if urls:
            break
    cands: list[str] = []
    for u in urls:
        path = re.sub(r"^https?://[^/]+", "", u)
        if not JOB_PATH.search(path):
            continue
        if not SLUG_KW.search(re.sub(r"[-_/.]+", " ", path)):
            continue
        cands.append(u)
    cands = list(dict.fromkeys(cands))[:cap]

    def one(u: str):
        r = fetch(u)
        if r is None or r.status_code != 200:
            return None
        d = DATE.search(r.text)
        if not d:
            d = re.search(r'<time[^>]+datetime="([0-9]{4}-[0-9]{2}-[0-9]{2})', r.text)
        if not d:
            return None
        t = TITLE.search(r.text)
        title = clean(t.group(1)) if t else ""
        if not title:
            h = re.search(r"<h1[^>]*>(.*?)</h1>", r.text, re.S)
            title = clean(h.group(1)) if h else ""
        if not title or not relevant(title):
            return None
        loc = LOC.search(r.text)
        return {"title": title, "posted": d.group(1),
                "location": loc.group(1) if loc else "", "url": u}

    out = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        for res in ex.map(one, cands):
            if res:
                out.append(res)
    return out


def smartrecruiters_search(slug: str):
    out = []
    for kw in ("ServiceNow", "Salesforce"):
        r = fetch(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?q={kw}&limit=50")
        if r is None or r.status_code != 200:
            continue
        try:
            content = r.json().get("content") or []
        except Exception:
            continue
        for p in content:
            title = clean(p.get("name", ""))
            if not relevant(title):
                continue
            loc = (p.get("location") or {}).get("fullLocation") or \
                  (p.get("location") or {}).get("city") or ""
            out.append({"title": title, "location": clean(str(loc)),
                        "url": f"https://jobs.smartrecruiters.com/{slug}/{p.get('id','')}",
                        "posted": (p.get("releasedDate") or "")[:10] or None})
    return out


def greenhouse_search(slug: str):
    r = fetch(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
    if r is None or r.status_code != 200:
        return []
    try:
        jobs = r.json().get("jobs") or []
    except Exception:
        return []
    out = []
    for p in jobs:
        title = clean(p.get("title", ""))
        if not relevant(title):
            continue
        out.append({"title": title, "location": clean((p.get("location") or {}).get("name", "")),
                    "url": p.get("absolute_url", ""),
                    "posted": (p.get("updated_at") or "")[:10] or None})
    return out


def lever_search(slug: str):
    r = fetch(f"https://api.lever.co/v0/postings/{slug}?mode=json")
    if r is None or r.status_code != 200:
        return []
    try:
        jobs = r.json()
    except Exception:
        return []
    out = []
    for p in jobs:
        title = clean(p.get("text", ""))
        if not relevant(title):
            continue
        ts = p.get("createdAt")
        posted = datetime.fromtimestamp(ts / 1000, timezone.utc).date().isoformat() if ts else None
        out.append({"title": title, "location": clean((p.get("categories") or {}).get("location", "")),
                    "url": p.get("hostedUrl", ""), "posted": posted})
    return out


# ---------------------------------------------------------------- corpus
def existing():
    blob = ""
    for name in ["README.md"] + sorted(glob.glob(str(ROOT / "README.BAK_*.md"))):
        try:
            blob += Path(name).read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    for f in sorted(INBOX.glob("*.md")):
        blob += f.read_text(encoding="utf-8", errors="replace")
    urls = {u.rstrip("/.,") for u in re.findall(r'https?://[^\s\)\]\|"]+', blob)}
    return urls, blob.lower()


def norm(text: str) -> str:
    text = (text or "").replace("&amp;", "&").lower()
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", text).split())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=45)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--max-per-table", type=int, default=400)
    ap.add_argument("--all-locations", action="store_true")
    ap.add_argument("--only", help="limit to one route (workday/oracle/phenom/sitemap/...)")
    ap.add_argument("--sitemap-cap", type=int, default=40,
                    help="max detail pages fetched per employer on the sitemap route")
    args = ap.parse_args()

    today = datetime.now(timezone.utc).date()
    cutoff = (today - timedelta(days=args.days)).isoformat()
    known, corpus = existing()

    with ThreadPoolExecutor(max_workers=14) as ex:
        prints = list(ex.map(lambda kv: fingerprint(*kv), CANDIDATES.items()))

    routes: dict[str, list[dict]] = {}
    for f in prints:
        for key in ("workday", "phenom", "oracle", "smartrecruiters", "greenhouse", "lever"):
            if key in f:
                routes.setdefault(key, []).append(f)
    blocked = [f["name"] for f in prints if any(
        k in f for k in ("successfactors", "icims", "taleo", "avature", "eightfold"))]

    print(f"fingerprinted {len(prints)} employers")
    for key, lst in routes.items():
        print(f"  {key:15s} {len(lst):2d} -> {', '.join(x['name'] for x in lst)}")
    if blocked:
        print(f"  no public search  {', '.join(blocked)}")

    found: list[dict] = []

    if not args.only or args.only == "workday":
        def run_wd(f):
            wd = f["workday"]
            hits = []
            for kw in KEYWORDS:
                hits.extend(workday_search(wd, kw))
            seen, uniq = set(), []
            for h in hits:
                if h["url"] in seen:
                    continue
                seen.add(h["url"])
                posted, where = workday_detail(h["url"])
                h["posted"] = posted
                if where and not h.get("location"):
                    h["location"] = where
                uniq.append(h)
            return f["name"], uniq
        with ThreadPoolExecutor(max_workers=8) as ex:
            for name, hits in ex.map(run_wd, routes.get("workday", [])):
                for h in hits:
                    h["company"] = name
                    h["route"] = "workday"
                found.extend(hits)
                if hits:
                    print(f"  workday/{name}: {len(hits)}")

    for key, fn, arg in (
        ("oracle", lambda f: oracle_search(f["oracle"]), None),
        ("smartrecruiters", lambda f: smartrecruiters_search(f["smartrecruiters"]), None),
        ("greenhouse", lambda f: greenhouse_search(f["greenhouse"]), None),
        ("lever", lambda f: lever_search(f["lever"]), None),
        ("phenom", lambda f: phenom_search(f["url"], f["phenom"]), None),
    ):
        if args.only and args.only != key:
            continue
        for f in routes.get(key, []):
            try:
                hits = fn(f)
            except Exception as e:
                print(f"  {key}/{f['name']}: ERR {str(e)[:60]}")
                continue
            for h in hits:
                h["company"] = f["name"]
                h["route"] = key
            found.extend(hits)
            if hits:
                print(f"  {key}/{f['name']}: {len(hits)}")

    no_route = [f for f in prints if not any(
        k in f for k in ("workday", "phenom", "oracle", "smartrecruiters", "greenhouse", "lever"))]
    if not args.only or args.only == "sitemap":
        def run_sm(f):
            return f["name"], sitemap_search(f["url"], cap=args.sitemap_cap)
        with ThreadPoolExecutor(max_workers=6) as ex:
            for name, hits in ex.map(run_sm, no_route):
                for h in hits:
                    h["company"] = name
                    h["route"] = "sitemap"
                found.extend(hits)
                if hits:
                    print(f"  sitemap/{name}: {len(hits)}")

    fresh = []
    for h in found:
        url = (h.get("url") or "").split("?")[0].rstrip("/")
        if not url or url in known:
            continue
        if not h.get("posted") or not (cutoff <= h["posted"] <= today.isoformat()):
            continue
        if not args.all_locations and not CANADA.search(h.get("location", "")):
            continue
        if f'{norm(h["title"])[:60]}|{norm(h["company"])[:30]}' in corpus:
            continue
        known.add(url)
        fresh.append(h)

    fresh.sort(key=lambda h: h["posted"], reverse=True)
    RAW.mkdir(exist_ok=True)
    (RAW / f"ats_fingerprint_{today.isoformat()}.json").write_text(
        json.dumps({"scannedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "fingerprints": prints, "found": found, "fresh": fresh}, indent=1), encoding="utf-8")

    print(f"\nraw hits {len(found)} | new in window {len(fresh)}")
    for h in fresh:
        print(f"  {h['posted']} | {h['company'][:20]:20s} | {h['title'][:62]} | {h['location'][:24]}")

    if not fresh:
        return 0

    rows = "\n".join(
        f'| {h["posted"]} | {clean(h["title"])} | {clean(h["company"])} | {clean(h["location"])} | '
        f'{h["url"]} | {h["route"]} public feed, JSON-LD datePosted |' for h in fresh)
    INBOX.mkdir(exist_ok=True)
    n = 1
    while (INBOX / f"ats-fingerprint--{today.isoformat()}--v{n}.md").exists():
        n += 1
    target = INBOX / f"ats-fingerprint--{today.isoformat()}--v{n}.md"
    target.write_text(
        "---\nmodel: ats-fingerprint\n"
        f"scanned_at: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n"
        "task: multi-employer-ats-fingerprint\n"
        f"notes: {len(prints)} employers fingerprinted; routes "
        + ", ".join(f"{k}={len(v)}" for k, v in routes.items()) + "\n---\n\n"
        "| Posted | Role | Company | Location | URL | Note |\n|---|---|---|---|---|---|\n" + rows + "\n",
        encoding="utf-8")
    print(f"wrote {target.relative_to(ROOT)}")

    if args.apply:
        subprocess.run([sys.executable, str(ROOT / "tools" / "jobs_merge_inbox.py"),
                        "--max-per-table", str(args.max_per_table)], check=True)
        subprocess.run([sys.executable, str(ROOT / "tools" / "build_site.py")], check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
