#!/usr/bin/env python3
"""gap_channels_scan.py — breadth channels the BESTIEJOB board barely covers.

Coverage measured on the 2026-11-11 live feed (5,340 rows, 328 hosts):
  ca.linkedin.com 1,603 + adzuna.ca 1,357 = 55% of the board
  Workday 31 rows (12 tenants) · Job Bank 11 · Workable 0

This script sweeps the three thin channels:

  1. Workday CXS public JSON (`POST /wday/cxs/<tenant>/<site>/jobs`). Boards are
     discovered from the board's own Workday URLs, from employer careers pages,
     and from a small guess list — each candidate is validated by a real CXS
     response before use. The date is the req's own `startDate`; the relative
     `postedOn` string is never turned into a date.
  2. Job Bank Canada search (`article > span.noctitle`, `li.date`, `li.location`).
     The posting's own "November 08, 2026" line is converted to ISO.
  3. Workable public API (`created` + nested location object).
  4. Phenom People boards (`/api/apply/v2/jobs`) and Oracle Cloud Recruiting
     (`/hcmRestApi/resources/latest/recruitingCEJobRequisitions`). Both are tried
     against several query shapes because they differ per tenant; a tenant that
     answers with zero reqs is counted, never filled in.

Rules enforced here (they mirror the board's own rules):
  * no absolute date -> dropped and counted, never guessed
  * posting older than --days (default 30) -> dropped
  * location must be Canadian (US/other countries dropped, including "US Remote")
  * title first; description only as a fallback and only for strong tokens
    (servicenow / service now / itsm / itam / itom / cmdb / salesforce / apex / mulesoft)

Usage:
  python3 scripts/gap_channels_scan.py
  python3 scripts/gap_channels_scan.py --inbox inbox/gap-channels--2026-11-11--v1.md
"""
import argparse
import collections
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today()
UA = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept-Language": "en-CA,en;q=0.9",
}

# Strong platform tokens only. Deliberately excludes generic words ("discovery",
# "asset management", "lightning") that matched unrelated roles in iteration 2.
PLATFORM = re.compile(
    r"service\s*now|servicenow|\bitsm\b|\bitam\b|\bitom\b|\bcmdb\b|"
    r"salesforce|\bapex\b|\bmulesoft\b|\bagentforce\b|\bcpq\b",
    re.I,
)
CA_LOC = re.compile(
    r"Ontario|Quebec|Québec|British Columbia|Alberta|Manitoba|Saskatchewan|Nova Scotia|"
    r"New Brunswick|Newfoundland|Prince Edward|Yukon|Nunavut|Toronto|Vancouver|Montr[ée]al|"
    r"Calgary|Ottawa|Mississauga|Edmonton|Winnipeg|Halifax|Waterloo|Victoria|Regina|"
    r"Saskatoon|Gatineau|Laval|Hamilton|Brampton|Markham|Oakville|Burnaby|Surrey|"
    r"Canada|CAN|Remote|T[ée]l[ée]travail",
    re.I,
)
NON_CA_LOC = re.compile(
    r"\b(USA|U\.S\.|United States|US\s*Remote|Remote\s*-\s*US|Poland|\bPOL\b|Brazil|\bBRA\b|"
    r"India|Philippines|Australia|Ireland|Germany|Romania|Mexico|Costa Rica|Singapore|Japan|"
    r"Taiwan|South Carolina|North Carolina|Florida|Texas|California|New York|Illinois|"
    r"Washington|Massachusetts|Georgia|Virginia|Ohio|Pennsylvania|Arizona|Colorado|Michigan|"
    r"Minnesota|Missouri|New Jersey|Tennessee|Utah|Wisconsin|Maryland|Oregon|Nevada|Indiana|"
    r"Connecticut|Kentucky|Alabama|Oklahoma|Iowa|Kansas|Arkansas|Mississippi|Nebraska|"
    r"United Kingdom|\bUK\b|Spain|Portugal|France)\b",
    re.I,
)

# A bare "Remote" is not a Canadian location. Require an explicit Canadian token.
CANADA_SIGNAL = re.compile(
    r"\bcanada\b|\bcan\b|Ontario|Quebec|Québec|British Columbia|Alberta|Manitoba|"
    r"Saskatchewan|Nova Scotia|New Brunswick|Newfoundland|Prince Edward|Yukon|Nunavut|"
    r"Toronto|Vancouver|Montr[ée]al|Calgary|Ottawa|Mississauga|Edmonton|Winnipeg|Halifax|"
    r"Waterloo|Victoria|Regina|Saskatoon|Gatineau|Laval|Hamilton|Brampton|Markham|Oakville|"
    r"Burnaby|Surrey|London, ON|Kitchener|Windsor",
    re.I,
)

IT_ROLE = re.compile(r"analyst|administrator|developer|engineer|architect|consultant|"
                     r"specialist|manager|lead|engineer|administrator", re.I)
PRODUCT = re.compile(r"service\s*now|servicenow|salesforce", re.I)

COMPANY_NAMES = {
    "bmo": "BMO", "td": "TD", "cibc": "CIBC", "rbc": "RBC", "interac": "Interac",
    "mckesson": "McKesson", "rsm": "RSM", "gdit": "GDIT", "soti": "SOTI",
    "omers": "OMERS", "moneris": "Moneris", "mlse": "MLSE", "agf": "AGF",
    "tmx": "TMX", "caatpension": "CAAT Pension Plan", "brookfield": "Brookfield",
    "salvationarmyca": "Salvation Army Canada", "sunlife": "Sun Life", "manulife": "Manulife",
    "canadalife": "Canada Life", "scotiabank": "Scotiabank", "accenture": "Accenture",
    "lifeworks": "LifeWorks", "ssctech": "SS&C Technologies", "iko": "IKO",
    "resolvetech": "ResolveTech", "danaher": "Danaher", "agf": "AGF",
}
US_STATE_TAIL = re.compile(
    r"[-,]\s*(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|"
    r"NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b"
)

CAREERS_PAGES = {
    "manulife": "https://www.manulife.com/en/careers",
    "sunlife": "https://www.sunlife.com/en/careers/",
    "canadalife": "https://www.canadalife.com/careers.html",
    "loblaw": "https://careers.loblaw.ca/",
    "rogers": "https://jobs.rogers.com/",
    "bell": "https://jobs.bell.ca/",
    "telus": "https://careers.telus.com/",
    "opg": "https://www.opg.com/careers/",
    "metrolinx": "https://www.metrolinx.com/en/about-us/careers",
    "enbridge": "https://www.enbridge.com/careers",
    "aircanada": "https://careers.aircanada.com/",
    "deloitte": "https://www.deloitte.com/ca/en/careers.html",
    "pwc": "https://www.pwc.com/ca/en/careers.html",
    "kpmg": "https://careers.kpmg.ca/",
    "cgi": "https://www.cgi.com/en/careers",
    "dxc": "https://dxc.com/us/en/careers",
    "kyndryl": "https://www.kyndryl.com/careers",
    "scotiabank": "https://www.scotiabank.com/careers/en/home.html",
    "cibc": "https://www.cibc.com/en/about-cibc/careers.html",
    # sectors the board has not swept: hospitals, universities, crown corps, governments
    "uhn": "https://www.uhn.ca/careers",
    "sickkids": "https://www.sickkids.ca/en/careers/",
    "sunnybrook": "https://www.sunnybrook.ca/content/?page=careers-main",
    "utoronto": "https://people.utoronto.ca/careers/",
    "yorku": "https://www.yorku.ca/hr/careers/",
    "torontomu": "https://www.torontomu.ca/human-resources/careers/",
    "cityoftoronto": "https://www.toronto.ca/city-government/career-opportunities/",
    "ontario": "https://www.ontario.ca/page/careers-ontario-public-service",
    "hydroone": "https://www.hydroone.com/careers",
    "ieso": "https://www.ieso.ca/en/Careers",
    "canadapost": "https://www.canadapost-postescanada.ca/cpc/en/our-company/careers.page",
    "viarail": "https://www.viarail.ca/en/about-via-rail/careers",
    "cbc": "https://careers.cbc.ca/",
    "laurentianbank": "https://www.laurentianbank.ca/en/careers.html",
    "atb": "https://www.atb.com/careers/",
    "equitablebank": "https://www.equitablebank.ca/en/careers.html",
}

# Phenom People boards (RBC and others). Endpoint shape varies per tenant, so the
# sweep tries several query forms and counts an empty answer instead of failing.
PHENOM_HOSTS = ["jobs.rbc.com"]
# Oracle Cloud Recruiting (ORC). The REST finder answers without a key; hosts are
# seeded here and can be extended as tenants are discovered.
ORACLE_HOSTS = ["estm.fa.em2.oraclecloud.com"]

GUESSES = {
    "rbc": (["wd3", "wd1"], ["External", "RBC_Careers"]),
    "td": (["wd3", "wd1"], ["External", "TD_Careers"]),
    "cibc": (["wd3"], ["External", "CIBC_Careers"]),
    "scotiabank": (["wd3", "wd1"], ["External", "Scotiabank_Careers"]),
    "manulife": (["wd3", "wd1"], ["External", "Manulife_Careers"]),
    "sunlife": (["wd3", "wd1"], ["External", "SunLife_Careers"]),
    "bmo": (["wd3"], ["External_Career_Site", "External"]),
    "accenture": (["wd3", "wd103"], ["External", "AccentureCareers"]),
}

WD_URL = re.compile(
    r"https?://([a-z0-9][a-z0-9-]*)\.(wd\d+)\.myworkdayjobs\.com/"
    r"(?:[a-z]{2}-[A-Za-z]{2}/)?([A-Za-z0-9_%\-]+)"
)


def fetch(url, data=None, timeout=30):
    headers = dict(UA)
    if data is not None:
        headers["Content-Type"] = "application/json"
    try:
        resp = urllib.request.urlopen(
            urllib.request.Request(url, data=data, headers=headers), timeout=timeout
        )
        return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, b""
    except Exception:
        return 0, b""


def boards_from_board():
    out = set()
    path = Path("/tmp/board_urls.json")
    if not path.exists():
        return out
    for url in json.load(open(path)):
        match = WD_URL.match(url)
        if match:
            out.add((match.group(1), match.group(2), urllib.parse.unquote(match.group(3))))
    return out


def boards_from_careers(counters):
    found = set()
    for _tenant, url in CAREERS_PAGES.items():
        status, body = fetch(url, timeout=20)
        if status != 200:
            counters[f"careers-http-{status}"] += 1
            continue
        text = body.decode("utf-8", "replace")
        for tenant, host, site in WD_URL.findall(text):
            site = urllib.parse.unquote(site)
            if site.lower() in ("job", "jobs", "wday", "apply"):
                continue
            found.add((tenant.lower(), host, site))
    return found


def wd_search(tenant, host, site, keyword, limit=20):
    url = f"https://{tenant}.{host}.myworkdayjobs.com/wday/cxs/{tenant}/{site}/jobs"
    body = json.dumps(
        {"appliedFacets": {}, "limit": limit, "offset": 0, "searchText": keyword}
    ).encode()
    status, raw = fetch(url, body, timeout=20)
    if status != 200 or b"jobPostings" not in raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None


def wd_detail(tenant, host, site, external_path):
    url = f"https://{tenant}.{host}.myworkdayjobs.com/wday/cxs/{tenant}/{site}{external_path}"
    status, raw = fetch(url, timeout=20)
    if status != 200:
        return None
    try:
        return json.loads(raw).get("jobPostingInfo", {})
    except Exception:
        return None


def resolve_guessed(tenant, hosts, sites):
    for host in hosts:
        for site in sites:
            if wd_search(tenant, host, site, "ServiceNow") is not None:
                return (tenant, host, site)
    return None


def location_ok(text):
    """Require an explicit Canadian signal; 'Remote' alone is ambiguous."""
    if not text:
        return False
    if NON_CA_LOC.search(text):
        return False
    if US_STATE_TAIL.search(text) and "CAN" not in text.upper():
        return False
    return bool(CANADA_SIGNAL.search(text))


def workday(counters, cutoff):
    candidates = set(boards_from_board()) | boards_from_careers(counters)
    for tenant, (hosts, sites) in GUESSES.items():
        resolved = resolve_guessed(tenant, hosts, sites)
        if resolved:
            candidates.add(resolved)

    def probe(board):
        return board, wd_search(board[0], board[1], board[2], "ServiceNow") is not None

    live = []
    with ThreadPoolExecutor(max_workers=12) as pool:
        for board, ok in pool.map(probe, candidates):
            if ok:
                live.append(board)
            else:
                counters["workday-board-unreachable"] += 1
    print(f"workday: {len(candidates)} candidate boards -> {len(live)} reachable")
    for board in sorted(live):
        print("   live board:", ".".join(board))

    def sweep(board):
        tenant, host, site = board
        rows = []
        for keyword in ("ServiceNow", "Salesforce"):
            payload = wd_search(tenant, host, site, keyword)
            if not payload:
                continue
            for posting in payload.get("jobPostings", []):
                loc = posting.get("locationsText", "") or ""
                if not location_ok(loc):
                    counters["not-canada"] += 1
                    continue
                detail = wd_detail(tenant, host, site, posting.get("externalPath", ""))
                if not detail:
                    counters["workday-detail-failed"] += 1
                    continue
                posted = (detail.get("startDate") or "").strip()
                if not re.fullmatch(r"20\d\d-\d\d-\d\d", posted):
                    counters["no-absolute-date"] += 1
                    continue
                if posted < cutoff:
                    counters["older-than-window"] += 1
                    continue
                title = detail.get("title", "") or posting.get("title", "")
                if not PLATFORM.search(title):
                    # Title-only. A description mention is not evidence: Workday JDs list
                    # ServiceNow among tools for sales, procurement and data roles too.
                    counters["off-topic"] += 1
                    continue
                rows.append({
                    "channel": "workday",
                    "company": tenant,
                    "title": title,
                    "location": detail.get("location") or loc,
                    "posted": posted,
                    "url": detail.get("externalUrl") or
                           f"https://{tenant}.{host}.myworkdayjobs.com/en-US/{site}"
                           f"{posting.get('externalPath','')}",
                    "req": detail.get("jobRequisitionId", ""),
                })
        return rows

    rows = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        for part in pool.map(sweep, live):
            rows.extend(part)
    for row in rows:
        row["company"] = COMPANY_NAMES.get(row["company"], row["company"].replace("-", " ").title())
    return rows


def parse_date(text):
    text = re.sub(r"\s+", " ", text or "").strip()
    iso = re.search(r"(20\d\d)-(\d\d)-(\d\d)", text)
    if iso:
        return iso.group(0)
    for fmt in ("%B %d, %Y", "%b %d, %Y", "%d %B %Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


def strip_tags(value):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value or "")).strip()


def jobbank(counters, cutoff):
    rows = []
    for query in ("servicenow", "service+now", "salesforce", "itsm"):
        status, body = fetch(
            "https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring="
            f"{query}&sort=D&locationstring=Canada",
            timeout=35,
        )
        if status != 200:
            counters[f"jobbank-http-{status}"] += 1
            continue
        text = body.decode("utf-8", "replace")
        for article in re.findall(r'<article id="article-\d+"(.*?)</article>', text, re.S):
            link = re.search(r'href="(/jobsearch/jobposting/\d+)', article)
            title = re.search(r'class="noctitle"[^>]*>(.*?)</span>', article, re.S)
            if not (link and title):
                counters["jobbank-parse-miss"] += 1
                continue
            name = strip_tags(title.group(1))
            if not PLATFORM.search(name):
                counters["off-topic"] += 1
                continue
            day = re.search(r'<li class="date">(.*?)</li>', article, re.S)
            posted = parse_date(strip_tags(day.group(1)) if day else "")
            if not posted:
                counters["no-absolute-date"] += 1
                continue
            if posted < cutoff:
                counters["older-than-window"] += 1
                continue
            employer = re.search(r'<li class="business">(.*?)</li>', article, re.S)
            place = re.search(r'<li class="location">(.*?)</li>', article, re.S)
            rows.append({
                "channel": "jobbank",
                "company": strip_tags(employer.group(1) if employer else ""),
                "title": name,
                "location": strip_tags(place.group(1) if place else ""),
                "posted": posted,
                "url": "https://www.jobbank.gc.ca" + link.group(1),
                "req": "",
            })
    return rows


def workable(counters, cutoff):
    rows = []
    for query in ("servicenow", "service%20now", "salesforce", "itsm"):
        for place in ("Canada", "Toronto%2C%20ON", "Vancouver%2C%20BC", "Montreal%2C%20QC"):
            status, body = fetch(
                f"https://jobs.workable.com/api/v1/jobs?query={query}&location={place}",
                timeout=30,
            )
            if status != 200:
                counters[f"workable-http-{status}"] += 1
                continue
            try:
                jobs = json.loads(body).get("jobs", [])
            except Exception:
                continue
            for job in jobs:
                loc_obj = job.get("location") or {}
                loc = ", ".join(
                    x for x in (loc_obj.get("city"), loc_obj.get("subregion"),
                                loc_obj.get("countryName")) if x
                )
                if "Canada" not in loc:
                    counters["not-canada"] += 1
                    continue
                title = job.get("title", "")
                if not PLATFORM.search(title):
                    counters["off-topic"] += 1
                    continue
                posted = parse_date(job.get("created") or job.get("updated") or "")
                if not posted:
                    counters["no-absolute-date"] += 1
                    continue
                if posted < cutoff:
                    counters["older-than-window"] += 1
                    continue
                rows.append({
                    "channel": "workable",
                    "company": (job.get("company") or {}).get("title", ""),
                    "title": title,
                    "location": loc,
                    "posted": posted,
                    "url": job.get("url") or "",
                    "req": job.get("id", ""),
                })
    return rows


def iso_from(value):
    """Absolute date from an ISO string or an epoch (s/ms). Nothing is inferred."""
    if isinstance(value, (int, float)) or (isinstance(value, str) and value.isdigit()):
        try:
            ts = int(value)
            if ts > 10 ** 11:
                ts //= 1000
            return datetime.utcfromtimestamp(ts).date().isoformat()
        except Exception:
            return ""
    return parse_date(str(value or ""))


def content_key(title, company):
    t = re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()
    c = re.sub(r"[^a-z0-9]+", " ", (company or "").lower()).strip()
    return f"{t}|{c}"


def ensure_board_index(board, board_content):
    """CI has no /tmp cache: build the dedupe index from the live feed."""
    if board and board_content:
        return board, board_content
    status, body = fetch("https://eltonaguiar.github.io/BESTIEJOB/jobs.json", timeout=60)
    if status != 200:
        print(f"board index unavailable (HTTP {status}); dedupe is inbox-internal only")
        return board, board_content
    try:
        jobs = json.loads(body).get("jobs", [])
    except Exception:
        return board, board_content
    board = {normalize(j.get("url", "")) for j in jobs}
    board.discard("")
    board_content = {content_key(j.get("title"), j.get("company")) for j in jobs}
    Path("/tmp/board_urls.json").write_text(json.dumps(sorted(board)))
    Path("/tmp/board_content.json").write_text(json.dumps(sorted(board_content)))
    print(f"board index built from live feed: {len(jobs)} rows")
    return board, board_content


def phenom(counters, cutoff):
    rows = []
    for host in PHENOM_HOSTS:
        domain = re.sub(r"^jobs\.", "", host)
        jobs = []
        for keyword in ("ServiceNow", "Salesforce"):
            for url in (
                f"https://{host}/api/apply/v2/jobs?domain={domain}&query={keyword}&start=0&num=100",
                f"https://{host}/api/apply/v2/jobs?domain=https%3A%2F%2F{host}&query={keyword}&start=0&num=100",
                f"https://{host}/api/apply/v2/jobs?domain={domain}&keywords={keyword}&start=0&num=100",
            ):
                status, body = fetch(url, timeout=25)
                if status != 200:
                    counters[f"phenom-http-{status}"] += 1
                    continue
                try:
                    payload = json.loads(body)
                except Exception:
                    counters["phenom-not-json"] += 1
                    continue
                data = payload.get("data")
                found = data if isinstance(data, list) else ((data or {}).get("jobs") if isinstance(data, dict) else None)
                found = found or payload.get("jobs") or []
                if found:
                    jobs = found
                    break
            if jobs:
                break
        if not jobs:
            counters["phenom-no-postings"] += 1
            continue
        for job in jobs:
            title = job.get("title") or job.get("name") or ""
            if not PLATFORM.search(title):
                counters["off-topic"] += 1
                continue
            loc = job.get("cityStateCountry") or job.get("location") or ""
            if isinstance(job.get("locations"), list) and not loc:
                loc = ", ".join(str(x) for x in job["locations"][:2])
            if not location_ok(str(loc)):
                counters["not-canada"] += 1
                continue
            posted = iso_from(job.get("postedDate") or job.get("dateCreated") or job.get("createDate"))
            if not posted:
                counters["no-absolute-date"] += 1
                continue
            if posted < cutoff:
                counters["older-than-window"] += 1
                continue
            ident = job.get("jobId") or job.get("id") or ""
            rows.append({"channel": "phenom", "company": domain.split(".")[0].upper(),
                         "title": title, "location": str(loc), "posted": posted,
                         "url": job.get("applyUrl") or job.get("jobUrl") or job.get("url")
                                or f"https://{host}/job/{ident}",
                         "req": str(ident)})
    return rows


def oracle(counters, cutoff):
    rows = []
    for host in ORACLE_HOSTS:
        for site in ("CX_1001", "CX_1"):
            for finder in (f"findReqs;siteNumber={site},limit=50,sortBy=POSTING_DATES_DESC",
                           f"findReqs;siteNumber={site},limit=50,keyword=ServiceNow"):
                url = (f"https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
                       f"?onlyData=true&expand=requisitionList&finder="
                       + urllib.parse.quote(finder, safe=",;="))
                status, body = fetch(url, timeout=30)
                if status != 200:
                    counters[f"oracle-http-{status}"] += 1
                    continue
                try:
                    items = json.loads(body).get("items", [])
                except Exception:
                    counters["oracle-not-json"] += 1
                    continue
                reqs = (items[0].get("requisitionList") if items else []) or []
                if not reqs:
                    counters["oracle-no-requisitions"] += 1
                    continue
                for req in reqs:
                    title = req.get("Title", "")
                    if not PLATFORM.search(title):
                        counters["off-topic"] += 1
                        continue
                    loc = req.get("PrimaryLocation") or req.get("PrimaryLocationCountry") or ""
                    if not location_ok(loc):
                        counters["not-canada"] += 1
                        continue
                    posted = iso_from(req.get("PostedDate") or req.get("PostingStartDate"))
                    if not posted:
                        counters["no-absolute-date"] += 1
                        continue
                    if posted < cutoff:
                        counters["older-than-window"] += 1
                        continue
                    rid = req.get("Id") or req.get("RequisitionId") or ""
                    rows.append({"channel": "oracle",
                                 "company": req.get("Organization") or host.split(".")[0].upper(),
                                 "title": title, "location": loc, "posted": posted,
                                 "url": f"https://{host}/hcmUI/CandidateExperience/en/sites/{site}/job/{rid}",
                                 "req": str(rid)})
    return rows


def normalize(url):
    url = (url or "").split("#")[0]
    url = re.sub(
        r"(utm_[^&]+&?|refId=[^&]+&?|trackingId=[^&]+&?|position=\d+&?|pageNum=\d+&?)",
        "", url,
    )
    return url.rstrip("?&/").lower()


def write_inbox(path, rows):
    lines = [
        f"# Gap-channel harvest — {TODAY.isoformat()}",
        "",
        "notes: Workday CXS / Job Bank Canada / Workable. Every row carries an absolute "
        "date published by the source (Workday `startDate`, Job Bank `li.date`, Workable "
        "`created`); undated and out-of-window rows were dropped, not guessed.",
        "",
        "| Posted | Role | Company | Location | Source |",
        "|---|---|---|---|---|",
    ]
    for row in rows:
        title = (row["title"] or "").replace("|", "/").strip()
        company = (row["company"] or "unknown").replace("|", "/").strip()
        location = (row["location"] or "—").replace("|", "/").strip()
        lines.append(
            f"| {row['posted']} | [{title}]({row['url']}) | {company} | {location} | "
            f"via {row['channel']} |"
        )
    path = Path(path)
    path.parent.mkdir(exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", default="/tmp/gap_jobs.json")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--inbox", default="")
    args = parser.parse_args()
    cutoff = (TODAY - timedelta(days=args.days)).isoformat()

    board = set()
    if Path("/tmp/board_urls.json").exists():
        board = set(json.load(open("/tmp/board_urls.json")))
    board_content = set()
    if Path("/tmp/board_content.json").exists():
        board_content = set(json.load(open("/tmp/board_content.json")))
    board, board_content = ensure_board_index(board, board_content)
    print(f"board urls loaded: {len(board)} | title+company keys: {len(board_content)} | window: {cutoff} .. {TODAY.isoformat()}")

    counters = collections.Counter()
    rows, notes = [], {}
    for name, func in (("workday", workday), ("jobbank", jobbank), ("workable", workable),
                       ("phenom", phenom), ("oracle", oracle)):
        started = time.time()
        before = collections.Counter(counters)
        try:
            got = func(counters, cutoff)
        except Exception as exc:  # keep the other channels running
            got = []
            counters[f"{name}-error"] += 1
            print(f"{name} failed: {exc}")
        notes[name] = {
            "rows": len(got),
            "secs": round(time.time() - started, 1),
            "drops": dict(counters - before),
        }
        rows.extend(got)

    seen, unique = set(), []
    for row in rows:
        key = normalize(row["url"])
        if not key or key in seen:
            continue
        seen.add(key)
        content_key = f'{re.sub(r"[^a-z0-9]+", " ", (row["title"] or "").lower()).strip()}|' \
                      f'{re.sub(r"[^a-z0-9]+", " ", (row["company"] or "").lower()).strip()}'
        # URL dedupe alone re-adds the same role when another board already carried it
        # under a different link (RSM Architect, BMO SAM Admin both already on the board).
        row["on_board"] = key in board or content_key in board_content
        unique.append(row)
    fresh = [row for row in unique if not row["on_board"]]
    fresh.sort(key=lambda row: (row["posted"], row["company"]), reverse=True)

    report = {
        "generated": TODAY.isoformat(), "window_start": cutoff, "channels": notes,
        "counters": dict(counters), "unique": len(unique),
        "already_on_board": len(unique) - len(fresh), "new": len(fresh), "rows": fresh,
    }
    Path(args.json).write_text(json.dumps(report, indent=1), encoding="utf-8")

    print("\nper-channel rows:", json.dumps({k: v["rows"] for k, v in notes.items()}))
    print("drops:", json.dumps(dict(counters)))
    print(f"\nunique: {len(unique)} | already on board: {len(unique)-len(fresh)} | NEW: {len(fresh)}\n")
    for row in fresh:
        print(f"  {row['posted']} | {row['channel']:8s} | {row['company'][:20]:20s} | "
              f"{row['title'][:56]:56s} | {row['location'][:28]}")
    if args.inbox and fresh:
        print("\ninbox written:", write_inbox(args.inbox, fresh))


main()
