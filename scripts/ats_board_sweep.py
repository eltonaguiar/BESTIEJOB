#!/usr/bin/env python3
"""Deep ATS sweep: query every discovered employer board's *dated* public feed.

Why this exists
---------------
`today_feeds_scan.py` runs the daily delta and only queries a handful of boards
(3 Ashby, 10 Workday, 3 Lever). The repositories of employer slugs we have
already discovered are much larger: 38 Workday tenants, 20 Greenhouse boards,
14 Ashby boards, 13 Lever sites, 13 SmartRecruiters companies. Those boards hold
postings the aggregators never surface, which is exactly the "job exists only on
the company's own site" gap.

Only feeds that return an authoritative publication date are used. A posting
that a feed can't date is dropped rather than guessed -- the same rule the rest
of the pipeline follows.

    workday          POST /wday/cxs/<tenant>/<site>/jobs  -> postedOn (relative)
    greenhouse       /v1/boards/<token>/jobs              -> first_published / updated_at
    lever            /v0/postings/<site>?mode=json        -> createdAt (epoch ms)
    ashby            /posting-api/job-board/<board>       -> publishedAt (ISO)
    smartrecruiters  /v1/companies/<id>/postings          -> releasedDate
    workable         /api/accounts/<sub>?details=true      -> published_on
    jobvite          JSON-LD on the posting page           -> datePosted

Deliberately excluded: Pinpoint (its public feed has no posted date, so
NewRocket/Crossfuze/Blue Mantis roles stay undated), BambooHR and Rippling
(list endpoints carry no date at all).

Canadian detection requires a real signal -- province, Canadian city, "Canada",
or Workday's `/...-CAN` path segment. A `"9 Locations"` string is not a country
and is rejected; that bug counted every multi-location US requisition as
Canadian.

Usage
    python3 scripts/ats_board_sweep.py                    # report + inbox file
    python3 scripts/ats_board_sweep.py --days 7
    python3 scripts/ats_board_sweep.py --apply            # merge + rebuild site
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
try:
    from ai_panel import get_key
    from crossurl import same_posting
    from crossurl import company_key as board_company_key
except Exception:                                    # noqa: BLE001
    get_key = None

INBOX = ROOT / "inbox"
NOW = datetime.now(timezone.utc)

try:
    from curl_cffi import requests as cr
except ImportError:  # curl_cffi is what gets past Cloudflare on Workday
    import urllib.request

    class _Fallback:
        @staticmethod
        def get(url, **kw):
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=kw.get("timeout", 25)) as r:
                return _Resp(r.read())

        @staticmethod
        def post(url, **kw):
            body = kw.get("json") or {}
            req = urllib.request.Request(
                url, data=json.dumps(body).encode(),
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
                method="POST")
            with urllib.request.urlopen(req, timeout=kw.get("timeout", 25)) as r:
                return _Resp(r.read())

    class _Resp:
        def __init__(self, data: bytes):
            self.content = data
            self.status_code = 200
            self.text = data.decode("utf-8", "replace")

        def json(self):
            return json.loads(self.content)

    cr = _Fallback()

# --------------------------------------------------------------------------
# Relevance filters. Same semantics as today_feeds_scan.py so the two scanners
# never disagree about what counts as a ServiceNow / Salesforce role.
# --------------------------------------------------------------------------
# Every alternative here names the platform itself. "field service", "service
# cloud" and friends are NOT on the list: standalone they describe a job
# function, not a product, so "CNC Field Service Technician" would match. The
# cloud names only count when Salesforce is attached to them.
KW = re.compile(r"\bservice\s?now\b|\bsalesforce\b|\bapex\b|\bsoql\b|\blwc\b|\bitsm\b|"
                r"\bitam\b|\bcmdb\b|\bitom\b|\bnow platform\b|platform developer|"
                r"agentforce|omnistudio|revenue cloud|mulesoft|"
                r"salesforce[\s\w/-]{0,24}(service|sales|experience|commerce|marketing)"
                r"\s?cloud|\bsfdc\b|\bsfmc\b", re.I)

TECH_TITLE = re.compile(
    r"developer|administrator|analyst|engineer|architect|consultant|specialist|"
    r"programmer|systems?\b|\bIT\b|information technology|integration|"
    r"database|application|software|\bQA\b|devops|platform|technical", re.I)

EXCL = re.compile(r"\b(account executive|account manager|sales representative|sales manager|"
                  r"business development|recruiter|talent acquisition|pre-?sales|"
                  r"customer success|marketing|growth|product marketing)\b", re.I)

CA_CITY = re.compile(
    r"toronto|mississauga|markham|brampton|vaughan|etobicoke|scarborough|north york|"
    r"richmond hill|oakville|burlington|waterloo|kitchener|guelph|london, on|"
    r"ottawa|montr[eé]al|montreal|laval|qu[eé]bec city|gatineau|"
    r"calgary|edmonton|winnipeg|regina|saskatoon|vancouver|burnaby|surrey|"
    r"victoria, bc|halifax|moncton|fredericton|st\.? john'?s|charlottetown|"
    r"whitehorse|yellowknife|iqaluit", re.I)
CA_FULL = re.compile(r"\b(ontario|british columbia|alberta|manitoba|saskatchewan|"
                     r"nova scotia|new brunswick|newfoundland( and labrador)?|"
                     r"prince edward island|yukon|nunavut|northwest territories)\b", re.I)
# Province codes are two letters and appear inside longer words: "on" is in
# "London", "ns" is in "Locations". Anchor on a boundary and require a capital.
CA_CODE = re.compile(r"(?:^|[\s,(/-])(ON|BC|QC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)(?=$|[\s,)/-])")
CA_WORD = re.compile(r"\bcanada\b|\bcanadian\b|\bCAN\b", re.I)
MULTI_LOC = re.compile(r"^\s*\d+\s+locations?\s*$", re.I)
US_STATE = re.compile(r"(?:^|[\s,(/-])(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|"
                      r"KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|"
                      r"OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)(?=$|[\s,)/-])")


def is_canadian(location: str, url: str = "") -> bool:
    """True only with a real Canadian signal.

    `"9 Locations"` is a count, not a place, and `"Remote"` alone says nothing
    about eligibility -- both are rejected.
    """
    text = (location or "").strip()
    if not text or MULTI_LOC.match(text):
        return False
    hay = f"{text} {url or ''}"
    if CA_WORD.search(hay) or CA_CITY.search(text) or CA_FULL.search(text):
        return True
    if CA_CODE.search(text):
        return True
    if "/CAN" in (url or "") or "-CAN" in (url or ""):
        return True
    # A US-only location simply falls through as not Canadian; no guesswork.
    return False


def day_from_iso(value) -> str | None:
    if not value:
        return None
    s = str(value)
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return None


def day_from_epoch_ms(value) -> str | None:
    try:
        ts = int(value) / 1000
    except (TypeError, ValueError):
        return None
    return datetime.fromtimestamp(ts, tz=timezone.utc).date().isoformat()


def workday_day(posted_on: str) -> str | None:
    """Workday reports a *relative* string, never a date.

    "Posted 30+ Days Ago" is an open-ended bucket, so it cannot be turned into a
    date at all -- the only honest answer is None. Parsing it as "exactly 30 days
    ago" put the freshest possible date on the stalest postings.
    """
    s = (posted_on or "").strip().lower()
    if not s:
        return None
    if "30+" in s or "today" in s:
        if "today" in s:
            return NOW.date().isoformat()
        return None
    if "yesterday" in s:
        return (NOW.date() - timedelta(days=1)).isoformat()
    m = re.search(r"(\d+)\s*\+?\s*days?", s)
    if m:
        return (NOW.date() - timedelta(days=int(m.group(1)))).isoformat()
    return None


# --------------------------------------------------------------------------
# Board registry: everything discovered so far, not just what the daily delta
# queries. Tokens that turned out to be URL noise (`map`, `j`, `en-ca`) are gone.
# --------------------------------------------------------------------------
WORKDAY = [
    ("accenture", "wd103", "AccentureCareers", "Accenture"),
    ("agf", "wd3", "AGF_Careers", "AGF"),
    ("altusgroup", "wd3", "AltusGroup", "Altus Group"),
    ("bdo", "wd3", "BDO", "BDO Canada"),
    ("bmo", "wd3", "External", "BMO"),
    ("brookfield", "wd5", "brookfield", "Brookfield"),
    ("brookfield", "wd5", "brookfieldproperties", "Brookfield Properties"),
    ("caatpension", "wd10", "Careers", "CAAT Pension Plan"),
    ("canadiantirecorporation", "wd3", "Enterprise_External_Careers_Site",
     "Canadian Tire"),
    # ("cibc", "wd3", "Search", "CIBC"),  # EXCLUDED until ~Apr 2027
    ("cloudera", "wd5", "External_Career", "Cloudera"),
    ("danaher", "wd1", "DanaherJobs", "Danaher"),
    ("desjardins", "wd10", "Desjardins", "Desjardins"),
    ("dxctechnology", "wd1", "dxcjobs", "DXC Technology"),
    ("gdit", "wd5", "External_Career_Site", "GDIT"),
    ("harriscomputer", "wd3", "1", "Harris Computer"),
    ("huron", "wd1", "HuronCareers", "Huron"),
    ("icf", "wd5", "ICFExternal_Career_Site", "ICF"),
    ("iko", "wd3", "IKO_Careers", "IKO"),
    ("interac", "wd3", "Interac", "Interac"),
    ("irvingoil", "wd3", "IOL_Careers_Primary", "Irving Oil"),
    ("manulife", "wd3", "MFCJH_Jobs", "Manulife"),
    ("mckesson", "wd3", "External_Careers", "McKesson"),
    ("medcan", "wd10", "Medcan", "Medcan"),
    ("mlse", "wd3", "MLSE", "MLSE"),
    ("moneris", "wd3", "Moneris", "Moneris"),
    ("omers", "wd3", "OMERS_External", "OMERS"),
    ("resolvetech", "wd1", "RTS", "Resolve Tech Solutions"),
    ("rsm", "wd1", "RSMCareers", "RSM"),
    ("salesforce", "wd12", "External_Career_Site", "Salesforce"),
    ("salvationarmyca", "wd3", "TSACB", "Salvation Army Canada"),
    ("soti", "wd3", "Referral_Job_Posting_Site", "SOTI"),
    ("sunlife", "wd3", "Experienced-Jobs", "Sun Life"),
    ("td", "wd3", "TD_Bank_Careers", "TD Bank"),
    ("thomsonreuters", "wd5", "External_Career_Site", "Thomson Reuters"),
    ("tjx", "wd1", "TJX_External", "TJX"),
    ("tmx", "wd3", "TMX_Careers", "TMX Group"),
]

GREENHOUSE = [
    ("neuraflash", "NeuraFlash"), ("geotab", "Geotab"), ("varicent", "Varicent"),
    ("levio", "Levio"), ("highmetric", "Highmetric"), ("taketwo", "Take-Two"),
    ("icapitalnetwork", "iCapital"), ("movableink", "Movable Ink"),
    ("toast", "Toast"), ("okta", "Okta"), ("ncinoinc", "nCino"),
    ("lightfeatheriollc", "LightFeather"), ("9thwayinsignia", "9th Way Insignia"),
    ("accenturefederalservices", "Accenture Federal Services"),
    ("guidepointsecurity", "GuidePoint Security"), ("etelligentgroup", "Etelligent"),
    ("cclfg", "CCLFG"), ("dscout", "Dscout"), ("airbnb", "Airbnb"),
    ("spacex", "SpaceX"), ("brex", "Brex"), ("mongodb", "MongoDB"),
    ("bloomerang", "Bloomerang"), ("d2l", "D2L"),
    "capco",
    "innodatainc",
    "map",
    "nmi",
]

LEVER = [
    ("eqbank", "EQ Bank"), ("alimentiv-2", "Alimentiv"), ("versapay", "Versapay"),
    ("pointclickcare", "PointClickCare"), ("electricmind", "Electric Mind"),
    ("achievers", "Achievers"), ("sitetracker", "SiteTracker"),
    ("tali-ai", "Tali AI"), ("vo2-group", "VO2 Group"), ("sait", "SAIT"),
    ("emburse", "Emburse"), ("jobgether", "Jobgether"), ("elfbeauty", "Elf Beauty"),
    "caseware",
    "metergysolutions",
    "v2sa",
]

ASHBY = [
    ("benevity", "Benevity"), ("loopio", "Loopio"), ("moego", "MoeGo"),
    ("lightspeedhq", "Lightspeed Commerce"), ("docebo", "Docebo"),
    ("rapdev", "RapDev"), ("directive", "Directive"), ("knox-systems", "Knox Systems"),
    ("norsemanservices", "Norseman"), ("cadregs", "CAD Regs"),
    ("telus-digital", "TELUS Digital"), ("1password", "1Password"),
    ("inovalon", "Inovalon"), ("webflow", "Webflow"), ("docker", "Docker"),
    "cytora",
    "facilityos",
    "relayfi",
    "riveron",
]

SMARTRECRUITERS = [
    ("ServiceNow", "ServiceNow"), ("ensiti", "Ensiti"), ("klick1", "Klick"),
    ("leger2", "Leger"), ("motocol", "Moto"), ("satechnologiesinc4", "SA Technologies"),
    ("spruceinfotech2", "Spruce Infotech"), ("spectrumhealthcare", "Spectrum Health"),
    ("systemcanadatechnologies", "System Canada"),
    ("computechcorporation1", "Compute Tech"), ("entirehire", "Entire Hire"),
]

WORKABLE = [("jolera", "Jolera"), ("zaelab", "Zaelab"), ("flosum", "Flosum"),
            ("avacone", "Avacone"), ("crossfuze", "Crossfuze")]

# Routes added after verifying their public feed carries an authoritative date:
# Recruitee `created_at`, Breezy `published_date`, Polymer `published_at`,
# Gem `first_published_at`, Teamtailor RSS `pubDate`. Pinpoint, BambooHR and
# Rippling are still absent because their feeds never state when a job was
# posted, and a posting with no date has no business on the board.
RECRUITEE: list[tuple[str, str]] = []
BREEZY: list[tuple[str, str]] = []
POLYMER: list[tuple[str, str]] = []
GEM: list[tuple[str, str]] = []
TEAMTAILOR: list[tuple[str, str]] = []

EXTRA = ROOT / "raw" / "ats_boards_extra.json"
SLUGS_CA = ROOT / "tools" / "ats_board_slugs_ca.txt"
PREFIX = {"ashby": "ashby:", "greenhouse": "greenhouse:", "lever": "lever:",
          "workable": "workable:", "smartrecruiters": "smartrecruiters:"}
ROUTES_BY_NAME = {}


def pretty(slug: str) -> str:
    """`the-trade-desk-inc` -> `The Trade Desk Inc`. Only a display label."""
    return re.sub(r"[._]+", " ", slug).replace("-", " ").title().strip()


def load_extra() -> None:
    """Merge tokens found by ats_discover.py and the CA slug file into the route tables."""
    targets = {
        "ashby": (ASHBY, lambda t: (t, pretty(t))),
        "greenhouse": (GREENHOUSE, lambda t: (t, pretty(t))),
        "lever": (LEVER, lambda t: (t, pretty(t))),
        "workable": (WORKABLE, lambda t: (t, pretty(t))),
        "smartrecruiters": (SMARTRECRUITERS, lambda t: (t, pretty(t))),
        "recruitee": (RECRUITEE, lambda t: (t, pretty(t))),
        "breezy": (BREEZY, lambda t: (t, pretty(t))),
        "polymer": (POLYMER, lambda t: (t, pretty(t))),
        "gem": (GEM, lambda t: (t, pretty(t))),
        "teamtailor": (TEAMTAILOR, lambda t: (t, pretty(t))),
    }

    # 1. Load from the CA slug file (breadth expansion)
    if SLUGS_CA.exists():
        for line in SLUGS_CA.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(None, 1)
            if len(parts) < 2:
                continue
            code, token = parts[0].upper(), parts[1]
            route = {"G": "greenhouse", "L": "lever", "A": "ashby"}.get(code)
            if not route:
                continue
            table, make = targets[route]
            have = {row[0] if isinstance(row, tuple) else row for row in table}
            if token not in have:
                table.append(make(token))

    # 2. Load from the extra JSON (discovered tokens)
    if EXTRA.exists():
        try:
            extra = json.loads(EXTRA.read_text(encoding="utf-8"))
            if isinstance(extra, dict):
                for route, tokens in extra.items():
                    if route not in targets:
                        continue
                    table, make = targets[route]
                    have = {row[0] if isinstance(row, tuple) else row for row in table}
                    for token in tokens:
                        if token not in have:
                            table.append(make(token))
        except Exception:
            pass


def fetch_json(url: str, *, method="GET", body=None, timeout=25):
    kw = {"timeout": timeout, "impersonate": "chrome"}
    if body is not None:
        r = cr.post(url, json=body, **kw)
    else:
        r = cr.get(url, **kw)
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}")
    return r.json()


_FC_SLOT = threading.Semaphore(2)      # Firecrawl 429s above ~2 concurrent
_EMPLOYER: dict[str, str] = {}
_EMPLOYER_LOCK = threading.Lock()


def greenhouse_employer(token: str, fallback: str) -> str:
    """The employer's own name from the board endpoint.

    A Greenhouse token is a handle, not a company name: '12Jlkfsk' is Orion
    Global Solutions and 'highmetric' is NewRocket (the acquisition kept the
    token). Labelling rows with the token produced companies called '12Jlkfsk'
    and split one employer across two names -- which is what made the same
    posting survive twice under two URLs.
    """
    with _EMPLOYER_LOCK:
        if token in _EMPLOYER:
            return _EMPLOYER[token]
    name = fallback
    try:
        data = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{token}")
        candidate = (data.get("name") or "").strip()
        if candidate:
            name = candidate
    except Exception:                                   # noqa: BLE001
        pass
    with _EMPLOYER_LOCK:
        _EMPLOYER[token] = name
    return name


def firecrawl_json(url: str, timeout: int = 90):
    """Fetch a JSON endpoint through Firecrawl's egress.

    apply.workable.com bans per-IP: every path returns 429 with impersonation
    and without it, so no header tweak helps. Firecrawl reads the same URL from
    its own IP and hands back the untouched body, which still carries
    `published_on` -- the authoritative date we need.
    """
    if get_key is None:
        raise RuntimeError("no key helper")
    key = get_key("FIRECRAWL_API_KEY")
    if not key:
        raise RuntimeError("no FIRECRAWL_API_KEY")
    payload = json.dumps({"url": url, "formats": ["rawHtml"],
                          "onlyMainContent": False}).encode()
    last: Exception | None = None
    for attempt in range(3):
        with _FC_SLOT:                       # cap concurrency; 429 above ~2
            req = urllib.request.Request(
                "https://api.firecrawl.dev/v2/scrape", data=payload,
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {key}"})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    body = json.loads(resp.read())
                raw = ((body.get("data") or {}).get("rawHtml")
                       or (body.get("data") or {}).get("html") or "").strip()
                if not raw:
                    raise RuntimeError("empty scrape")
                return json.loads(raw)
            except urllib.error.HTTPError as exc:
                last = exc
                if exc.code != 429:
                    raise
        time.sleep(2 + 2 * attempt)          # 2s, 4s, 6s backoff
    raise last if last else RuntimeError("firecrawl failed")


def from_workday(board) -> list[dict]:
    if len(board)==4:
        tenant, wd, site, label = board
    elif len(board)==2:
        tenant, site = board; wd="wd5"; label=tenant.title()
    elif len(board)==3:
        tenant, wd, site = board; label=tenant.title()
    else:
        return []
    base = f"https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/{tenant}/{site}"
    out, offset = [], 0
    while offset < 200:
        try:
            data = fetch_json(base + "/jobs", method="POST",
                              body={"appliedFacets": {}, "limit": 20, "offset": offset,
                                    "searchText": "servicenow"})
        except Exception as exc:
            if offset == 0:
                print(f"  [workday:{tenant}/{site}] {type(exc).__name__} {str(exc)[:44]}")
            return out
        posts = data.get("jobPostings") or []
        for p in posts:
            path = p.get("externalPath") or ""
            out.append({"title": p.get("title") or "", "company": label,
                        "location": p.get("locationsText") or "",
                        "url": f"https://{tenant}.{wd}.myworkdayjobs.com/en-US/{site}{path}",
                        "posted": workday_day(p.get("postedOn")),
                        "posted_raw": p.get("postedOn"),
                        "source": f"workday:{tenant}"})
        if len(posts) < 20:
            break
        offset += 20
    # A second pass for Salesforce, since CXS searchText is a single string.
    offset = 0
    while offset < 200:
        try:
            data = fetch_json(base + "/jobs", method="POST",
                              body={"appliedFacets": {}, "limit": 20, "offset": offset,
                                    "searchText": "salesforce"})
        except Exception:
            return out
        posts = data.get("jobPostings") or []
        for p in posts:
            path = p.get("externalPath") or ""
            out.append({"title": p.get("title") or "", "company": label,
                        "location": p.get("locationsText") or "",
                        "url": f"https://{tenant}.{wd}.myworkdayjobs.com/en-US/{site}{path}",
                        "posted": workday_day(p.get("postedOn")),
                        "posted_raw": p.get("postedOn"),
                        "source": f"workday:{tenant}"})
        if len(posts) < 20:
            break
        offset += 20
    return out


def from_greenhouse(board) -> list[dict]:
    token, label = board if isinstance(board, tuple) else (board, pretty(board))
    out = []
    try:
        data = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs")
    except Exception as exc:
        print(f"  [greenhouse:{token}] {type(exc).__name__} {str(exc)[:44]}")
        return out
    name = greenhouse_employer(token, label)
    for j in data.get("jobs") or []:
        loc = (j.get("location") or {}).get("name") or ""
        out.append({"title": j.get("title") or "", "company": name, "location": loc,
                    "url": j.get("absolute_url") or "",
                    "posted": day_from_iso(j.get("first_published") or j.get("updated_at")),
                    "source": f"greenhouse:{token}"})
    return out


def from_lever(board) -> list[dict]:
    site, label = board if isinstance(board, tuple) else (board, pretty(board))
    out = []
    try:
        data = fetch_json(f"https://api.lever.co/v0/postings/{site}?mode=json")
    except Exception as exc:
        print(f"  [lever:{site}] {type(exc).__name__} {str(exc)[:44]}")
        return out
    for j in data if isinstance(data, list) else []:
        cats = j.get("categories") or {}
        out.append({"title": j.get("text") or "", "company": label,
                    "location": cats.get("location") or "",
                    "url": j.get("hostedUrl") or "",
                    "posted": day_from_epoch_ms(j.get("createdAt")),
                    "source": f"lever:{site}"})
    return out


def from_ashby(board) -> list[dict]:
    token, label = board if isinstance(board, tuple) else (board, pretty(board))
    out = []
    try:
        data = fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{token}"
                          "?includeCompensation=true")
    except Exception as exc:
        print(f"  [ashby:{token}] {type(exc).__name__} {str(exc)[:44]}")
        return out
    for j in data.get("jobs") or []:
        if j.get("isListed") is False:   # direct-link only, not a public posting
            continue
        out.append({"title": j.get("title") or "", "company": label,
                    "location": j.get("location") or "",
                    "url": j.get("jobUrl") or "",
                    "posted": day_from_iso(j.get("publishedAt")),
                    "source": f"ashby:{token}"})
    return out


def from_smartrecruiters(board) -> list[dict]:
    ident, label = board
    out, offset = [], 0
    while offset < 300:
        try:
            data = fetch_json("https://api.smartrecruiters.com/v1/companies/"
                              f"{ident}/postings?limit=100&offset={offset}")
        except Exception as exc:
            if offset == 0:
                print(f"  [smartrecruiters:{ident}] {type(exc).__name__} {str(exc)[:40]}")
            return out
        rows = data.get("content") or []
        for j in rows:
            loc = j.get("location") or {}
            place = ", ".join(x for x in (loc.get("city"), loc.get("region"),
                                          loc.get("country")) if x)
            out.append({"title": j.get("name") or "", "company": label, "location": place,
                        "url": f"https://jobs.smartrecruiters.com/{ident}/{j.get('id')}",
                        "posted": day_from_iso(j.get("releasedDate")),
                        "source": f"smartrecruiters:{ident}"})
        if len(rows) < 100:
            break
        offset += 100
    return out


def from_workable(board) -> list[dict]:
    sub, label = board if isinstance(board, tuple) else (board, pretty(board))
    out = []
    url = f"https://www.workable.com/api/accounts/{sub}?details=true"
    try:
        data = fetch_json(url)
    except Exception as exc:
        # apply.workable.com 429s this whole IP, so fall back to Firecrawl's
        # egress rather than losing the route entirely.
        try:
            data = firecrawl_json(url)
            print(f"  [workable:{sub}] direct {type(exc).__name__} -> firecrawl OK")
        except Exception as exc2:
            print(f"  [workable:{sub}] {type(exc).__name__} + firecrawl "
                  f"{type(exc2).__name__} {str(exc2)[:40]}")
            return out
    name = (data.get("name") or "").strip() or label   # Workable states it
    for j in data.get("jobs") or []:
        loc = j.get("location") or {}
        place = ", ".join(x for x in (loc.get("city"), loc.get("region"),
                                      loc.get("country")) if x)
        out.append({"title": j.get("title") or "", "company": name, "location": place,
                    "url": j.get("url") or j.get("shortlink") or "",
                    "posted": day_from_iso(j.get("published_on")),
                    "source": f"workable:{sub}"})
    return out


def from_recruitee(board) -> list[dict]:
    sub, label = board
    out = []
    try:
        data = fetch_json(f"https://{sub}.recruitee.com/api/offers/")
    except Exception as exc:
        print(f"  [recruitee:{sub}] {type(exc).__name__} {str(exc)[:44]}")
        return out
    for j in data.get("offers") or []:
        out.append({"title": j.get("title") or "", "company": label,
                    "location": j.get("location") or "",
                    "url": j.get("careers_apply_url") or j.get("careers_url") or "",
                    "posted": day_from_iso(j.get("created_at")),
                    "source": f"recruitee:{sub}"})
    return out


def from_breezy(board) -> list[dict]:
    sub, label = board
    out = []
    try:
        data = fetch_json(f"https://{sub}.breezy.hr/json")
    except Exception as exc:
        print(f"  [breezy:{sub}] {type(exc).__name__} {str(exc)[:44]}")
        return out
    for j in (data if isinstance(data, list) else []):
        loc = (j.get("location") or {}).get("name") or ""
        out.append({"title": j.get("name") or "", "company": label, "location": loc,
                    "url": j.get("url") or "",
                    "posted": day_from_iso(j.get("published_date")),
                    "source": f"breezy:{sub}"})
    return out


def from_polymer(board) -> list[dict]:
    sub, label = board
    out = []
    try:
        data = fetch_json(f"https://api.polymer.co/v1/hire/organizations/{sub}/jobs")
    except Exception as exc:
        print(f"  [polymer:{sub}] {type(exc).__name__} {str(exc)[:44]}")
        return out
    for j in data.get("items") or []:
        out.append({"title": j.get("title") or "", "company": label,
                    "location": j.get("display_location") or j.get("country") or "",
                    "url": j.get("job_post_url") or "",
                    "posted": day_from_iso(j.get("published_at")),
                    "source": f"polymer:{sub}"})
    return out


def from_gem(board) -> list[dict]:
    sub, label = board
    out = []
    try:
        data = fetch_json(f"https://api.gem.com/job_board/v0/{sub}/job_posts/")
    except Exception as exc:
        print(f"  [gem:{sub}] {type(exc).__name__} {str(exc)[:44]}")
        return out
    for j in (data if isinstance(data, list) else []):
        loc = j.get("location") or (j.get("offices") or [{}])[0]
        place = loc.get("name") if isinstance(loc, dict) else str(loc)
        out.append({"title": j.get("title") or "", "company": label,
                    "location": place or "",
                    "url": j.get("absolute_url") or "",
                    "posted": day_from_iso(j.get("first_published_at")),
                    "source": f"gem:{sub}"})
    return out


RSS_DATE = re.compile(r"<pubDate>([^<]+)</pubDate>")
RSS_TITLE = re.compile(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", re.S)
RSS_LINK = re.compile(r"<link>(https?://[^<]+)</link>")
RSS_LOC = re.compile(r"<tt:location>(?:<!\[CDATA\[)?([^<\]]+)")


def from_teamtailor(board) -> list[dict]:
    """Teamtailor publishes RSS only; `<pubDate>` is the posting's own date."""
    sub, label = board
    out = []
    try:
        kw = {"timeout": 25, "impersonate": "chrome"}
        r = cr.get(f"https://{sub}.teamtailor.com/jobs.rss", **kw)
        if r.status_code != 200:
            raise RuntimeError(f"HTTP {r.status_code}")
        xml = r.text
    except Exception as exc:
        print(f"  [teamtailor:{sub}] {type(exc).__name__} {str(exc)[:44]}")
        return out
    for block in re.split(r"<item>", xml)[1:]:
        t = RSS_TITLE.search(block)
        link = RSS_LINK.search(block)
        pub = RSS_DATE.search(block)
        loc = RSS_LOC.search(block)
        if not (t and link and pub):
            continue
        try:
            when = datetime.strptime(pub.group(1).strip()[:25].strip(),
                                     "%a, %d %b %Y %H:%M:%S").date().isoformat()
        except ValueError:
            when = None
        out.append({"title": t.group(1).strip(), "company": label,
                    "location": (loc.group(1).strip() if loc else ""),
                    "url": link.group(1).strip(), "posted": when,
                    "source": f"teamtailor:{sub}"})
    return out


ROUTES = [
    ("workday", WORKDAY, from_workday),
    ("greenhouse", GREENHOUSE, from_greenhouse),
    ("lever", LEVER, from_lever),
    ("ashby", ASHBY, from_ashby),
    ("smartrecruiters", SMARTRECRUITERS, from_smartrecruiters),
    ("workable", WORKABLE, from_workable),
    ("recruitee", RECRUITEE, from_recruitee),
    ("breezy", BREEZY, from_breezy),
    ("polymer", POLYMER, from_polymer),
    ("gem", GEM, from_gem),
    ("teamtailor", TEAMTAILOR, from_teamtailor),
]


def relevant(row: dict) -> bool:
    title = row.get("title") or ""
    if not title or EXCL.search(title):
        return False
    if not KW.search(title):
        return False          # a platform mention in the body is not a platform role
    return True


def board_rows() -> list[dict]:
    """Rows already on the board, as crossurl-comparable dicts.

    URL dedupe is not enough here: one requisition reaches the board from an
    aggregator under the employer's full name and from the employer's ATS under
    its ATS handle, which is two URLs and two labels for one job. Comparing
    (company, title) after a regex squash missed exactly that -- 'Lightspeed
    Commerce' and 'lightspeedhq' squash to different strings.
    """
    out: list[dict] = []
    # README is the board. jobs-data.json only holds the recent window, so
    # checking it alone lets older rows through and the merger then drops them
    # as URL duplicates -- wasted rows reported as net-new.
    try:
        lines = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
    except OSError:
        return out
    for line in lines:
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", cells[0]):
            continue
        link = re.search(r"\[([^\]]+)\]", cells[1])
        out.append({"posted": cells[0],
                    "title": link.group(1) if link else cells[1],
                    "company": cells[2],
                    "location": cells[3] if len(cells) > 3 else ""})
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=int, default=7, help="how far back to accept (default 7)")
    ap.add_argument("--apply", action="store_true", help="merge into README + rebuild site")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    load_extra()
    cutoff = NOW.date() - timedelta(days=args.days)
    print(f"deep sweep: {sum(len(b) for _, b, _ in ROUTES)} boards, "
          f"accepting {cutoff}..{NOW.date()}")

    fetched: list[dict] = []
    for name, boards, fn in ROUTES:
        with ThreadPoolExecutor(max_workers=10) as pool:
            for rows in pool.map(fn, boards):
                fetched.extend(rows)
        print(f"  {name:16} boards={len(boards):3}  rows={len(fetched)}")

    print(f"\nraw rows: {len(fetched)}")
    relevant_rows = [r for r in fetched if relevant(r)]
    print(f"keyword-relevant: {len(relevant_rows)}")

    canada = [r for r in relevant_rows if is_canadian(r.get("location"), r.get("url"))]
    print(f"Canadian: {len(canada)}")

    dated = []
    for r in canada:
        d = r.get("posted")
        if not d:
            continue
        try:
            when = date.fromisoformat(d)
        except ValueError:
            continue
        if cutoff <= when <= NOW.date():
            dated.append(r)
    print(f"dated within {args.days}d: {len(dated)}")

    known = board_rows()
    by_company: dict[str, list[dict]] = {}
    for row in known:
        k = board_company_key(row["company"])
        by_company.setdefault(k[:4] if len(k) >= 4 else k, []).append(row)

    seen, rows, already = set(), [], 0
    for r in dated:
        url_key = re.sub(r"\?.*$", "", (r.get("url") or "").rstrip("/").lower())
        if not url_key or url_key in seen:
            continue
        seen.add(url_key)
        k = board_company_key(r.get("company") or "")
        bucket = by_company.get(k[:4] if len(k) >= 4 else k, [])
        if any(same_posting(r, row) for row in bucket):
            already += 1
            continue
        rows.append(r)
    print(f"already on the board (cross-URL match): {already}")

    rows.sort(key=lambda r: (r["posted"], r["company"]), reverse=True)
    for r in rows:
        print(f"  {r['posted']}  {r['company'][:24]:24}  {r['title'][:56]:56}  "
              f"{r['location'][:26]}")

    if not rows:
        print("\nnothing new with a confirmed date.")
        return 0

    INBOX.mkdir(exist_ok=True)
    stamp = NOW.strftime("%Y-%m-%d")
    path = INBOX / f"ats-sweep--{stamp}--v1.md"
    n = 1
    while path.exists():
        n += 1
        path = INBOX / f"ats-sweep--{stamp}--v{n}.md"
    lines = [
        f"# ATS deep sweep — {stamp}",
        "",
        f"{len(rows)} dated Canadian ServiceNow/Salesforce postings pulled from",
        f"{sum(len(b) for _, b, _ in ROUTES)} employer boards. Every date comes from the",
        "employer's own ATS feed (Workday `postedOn`, Greenhouse `first_published`,",
        "Lever `createdAt`, Ashby `publishedAt`).",
        "",
        "| Posted | Role | Company | Location | URL |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        title = r["title"].replace("|", "/")
        lines.append(f"| {r['posted']} | {title} | {r['company']} | "
                     f"{r['location'].replace('|', '/')} | [{title}]({r['url']}) |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {path.relative_to(ROOT)} ({len(rows)} rows)")

    if args.apply:
        subprocess.run([sys.executable, str(ROOT / "tools" / "jobs_merge_inbox.py"),
                        "--days", "60", "--max-per-table", "10000"], cwd=ROOT, check=True)
        subprocess.run(["node", "scripts/check_readme_sort.mjs"], cwd=ROOT, check=True)
        subprocess.run([sys.executable, str(ROOT / "tools" / "build_site.py")],
                       cwd=ROOT, check=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
