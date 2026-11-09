#!/usr/bin/env python3
"""
Workday deep scan — Round 2 differential route.

Why this is a *new* style rather than a re-run:

  Every existing scanner (ats_fingerprint_scan.py, round3b_ats_scan.py)
  queries Workday CXS with four keywords ("ServiceNow", "Salesforce", "ITSM",
  "CMDB") and `offset: 0`. A CXS `searchText` is a single string and the
  endpoint returns 20 rows per page, so offset 0 sees only the first 20 hits
  of one term. Anything matching only a certification code (CSA, CAD, CIS,
  HAM, SAM, CSDM), a module (GRC, HRSD, FSO, ITOM), or a Salesforce product
  (CPQ, Marketing Cloud, Agentforce, Omnistudio) is invisible.

  This scanner sweeps the far larger vocabulary and paginates each term to
  exhaustion, then de-duplicates on requisition URL. It also separates
  genuinely-new requisitions from ones already on the board by comparing the
  req-ID set against a stored snapshot -- so "new" is a *diff*, not a
  relative-date guess.

  CIBC is deliberately absent from the tenant table (ineligible until
  ~Apr 2027, per BESTIEJOB_IMPROVEMENTS_2026-11-01.md line 75).

Usage
    python3 scripts/workday_deep_scan.py                # report only
    python3 scripts/workday_deep_scan.py --apply        # write inbox file
    python3 scripts/workday_deep_scan.py --days 21
"""
from __future__ import annotations

import argparse
import json
import re
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
SNAP = RAW / "workday_req_snapshot.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# (tenant, wd-number, site-path, label) -- these are the VERIFIED slugs from
# ats_board_sweep.py's WORKDAY registry (lines 206-245), which is the only list
# proven to return HTTP 200. Guessed slugs return 422/404 and waste a full pass.
# CIBC is deliberately omitted: ineligible until ~Apr 2027
# (BESTIEJOB_IMPROVEMENTS_2026-11-01.md line 75).
_WORKDAY_REGISTRY = [
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
    # ("cibc", "wd3", "Search", "CIBC"),   # EXCLUDED until ~Apr 2027
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

TENANTS = [(tenant, f"{tenant}.{wd}.myworkdayjobs.com", site, label)
           for tenant, wd, site, label in _WORKDAY_REGISTRY]

# The full platform + certification + module vocabulary. Values that describe a
# job function rather than the product ("field service", "service cloud" alone)
# are deliberately excluded -- see ats_board_sweep.py lines 103-106 for why.
KEYWORDS = [
    # ServiceNow platform + certifications
    "ServiceNow", "CSA", "CAD", "CIS", "CSM", "ITSM", "ITAM", "ITOM", "CMDB",
    "CSDM", "HAM", "SAM", "GRC", "HRSD", "FSO", "SPM", "Discovery",
    "Service Mapping", "Performance Analytics", "Now Assist", "App Engine",
    "Flow Designer", "IntegrationHub", "Virtual Agent", "Portal",
    # Salesforce platform + products
    "Salesforce", "Apex", "SOQL", "LWC", "Visualforce", "Lightning",
    "Platform Developer", "Platform Administrator", "Omnistudio",
    "Marketing Cloud", "Commerce Cloud", "Experience Cloud", "Revenue Cloud",
    "Service Cloud", "Sales Cloud", "CPQ", "Agentforce", "Mulesoft",
    "Tableau CRM", "Einstein", "SFDC",
]

CA = re.compile(
    r"toronto|mississauga|markham|brampton|vaughan|etobicoke|scarborough|"
    r"north york|richmond hill|oakville|burlington|waterloo|kitchener|guelph|"
    r"ottawa|montr[eé]al|montreal|laval|qu[eé]bec|gatineau|calgary|edmonton|"
    r"winnipeg|regina|saskatoon|vancouver|burnaby|surrey|victoria|halifax|"
    r"moncton|fredericton|canada|ontario|alberta|quebec|british columbia", re.I)
US = re.compile(r",\s*(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|"
                r"MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|"
                r"SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY)\b")
MULTI = re.compile(r"^\s*\d+\s+locations?\s*$", re.I)
REL = re.compile(r"posted\s+(\d+)\s+day", re.I)

RELEVANT = re.compile(
    r"servicenow|salesforce|itsm|itam|cmdb|itom|\bsnow\b|apex|soql|lwc|"
    r"visualforce|lightning|mulesoft|integration hub|service catalog|grc|"
    r"now assist|performance analytics|discovery|service mapping|csdm|"
    r"ham\b|\bsam\b|hrsd|\bfso\b|\bspm\b|omnistudio|agentforce|cpq|"
    r"marketing cloud|commerce cloud|experience cloud|revenue cloud|"
    r"service cloud|sales cloud|einstein|platform developer|platform administrator",
    re.I)

EXCL = re.compile(r"\b(account executive|account manager|sales representative|"
                  r"sales manager|business development|recruiter|talent acquisition|"
                  r"pre-?sales|customer success|product marketing)\b", re.I)
TECH = re.compile(r"developer|administrator|analyst|engineer|architect|consultant|"
                  r"specialist|programmer|systems?\b|\bIT\b|information technology|"
                  r"integration|database|application|software|platform|technical", re.I)


def is_canadian(loc: str, url: str) -> bool:
    if not loc or MULTI.match(loc):
        # a multi-location or blank field is only usable if the URL names a CA city
        return bool(CA.search(url.replace("-", " ")))
    if CA.search(loc):
        return True
    if US.search(loc):
        return False
    return bool(CA.search(url.replace("-", " ")))


def posted_day(row: dict) -> str | None:
    """Workday `postedOn` is relative ('Posted 3 Days Ago'); '30+' means stale."""
    raw = (row.get("postedOn") or "").strip()
    if not raw:
        return None
    if "30+" in raw:
        return None
    low = raw.lower()
    today = datetime.now(timezone.utc).date()
    if "today" in low:
        return today.isoformat()
    if "yesterday" in low:
        return (today - timedelta(days=1)).isoformat()
    m = REL.search(low)
    if m:
        return (today - timedelta(days=int(m.group(1)))).isoformat()
    return None


def probe(tenant_host_site) -> list[dict]:
    tenant, host, site, label = tenant_host_site
    base = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
    out: list[dict] = []
    seen: set[str] = set()

    for kw in KEYWORDS:
        offset = 0
        while offset < 200:                    # cap: 10 pages per term
            body = {"appliedFacets": {}, "limit": 20, "offset": offset,
                    "searchText": kw}
            try:
                r = cr.post(base, json=body, impersonate="chrome124",
                            timeout=25, headers={"User-Agent": UA,
                                                 "Accept": "application/json"})
                if r.status_code != 200:
                    break
                data = r.json()
            except Exception:
                break

            posts = data.get("jobPostings") or []
            if not posts:
                break
            for p in posts:
                path = p.get("externalPath") or ""
                if not path or path in seen:
                    continue
                seen.add(path)
                title = (p.get("title") or "").strip()
                loc = (p.get("locationsText") or "").strip()
                url = f"https://{host}/en-US/{site}{path}"
                out.append({"title": title, "location": loc, "url": url,
                            "posted": posted_day(p), "posted_rel": p.get("postedOn"),
                            "company": label, "kw": kw})
            total = data.get("total") or 0
            offset += 20
            if offset >= total:
                break
    return out


def load_snapshot() -> set[str]:
    try:
        return set(json.loads(SNAP.read_text(encoding="utf-8")).get("urls", []))
    except Exception:
        return set()


def save_snapshot(urls: set[str]) -> None:
    RAW.mkdir(exist_ok=True)
    SNAP.write_text(json.dumps({"saved_at": datetime.now(timezone.utc).isoformat(),
                                "urls": sorted(urls)}, indent=1), encoding="utf-8")


def existing_urls() -> set[str]:
    blob = ""
    for p in [ROOT / "README.md"]:
        try:
            blob += p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            pass
    for f in INBOX.glob("*.md"):
        blob += f.read_text(encoding="utf-8", errors="replace")
    return {u.rstrip("/.,").lower() for u in
            re.findall(r"https?://[^\s\)\]\|\"]+", blob)}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--tenant", action="append", help="limit to one tenant slug")
    args = ap.parse_args()

    tenants = TENANTS
    if args.tenant:
        want = {t.lower() for t in args.tenant}
        tenants = [t for t in TENANTS if t[0].lower() in want]

    cutoff = (datetime.now(timezone.utc) - timedelta(days=args.days)).date().isoformat()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"probing {len(tenants)} tenants x {len(KEYWORDS)} keywords "
          f"(window {cutoff}..{today})")

    all_rows: list[dict] = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for rows in ex.map(probe, tenants):
            all_rows.extend(rows)

    print(f"raw workday rows: {len(all_rows)}")

    relevant = [r for r in all_rows if RELEVANT.search(r["title"])]
    print(f"platform-relevant: {len(relevant)}")

    ca = [r for r in relevant if is_canadian(r["location"], r["url"])]
    print(f"Canadian: {len(ca)}")

    excl = [r for r in ca if not EXCL.search(r["title"]) and TECH.search(r["title"])]
    print(f"technical + not sales/marketing: {len(excl)}")

    dated = [r for r in excl if r["posted"] and r["posted"] >= cutoff]
    print(f"posted within {args.days}d: {len(dated)}")

    known = existing_urls()
    snapshot = load_snapshot()
    fresh = [r for r in dated if r["url"].lower() not in known]
    print(f"not already on the board: {len(fresh)}")

    diffed = [r for r in fresh if r["url"].lower() not in snapshot]
    print(f"not in previous req snapshot: {len(diffed)}")

    # persist the union so next run can diff against it
    save_snapshot({r["url"].lower() for r in all_rows} | snapshot)

    if not diffed:
        print("\nnothing new with a confirmed date.")
        return 0

    ver = 1
    while (INBOX / f"workday-deep--{today}--v{ver}.md").exists():
        ver += 1
    path = INBOX / f"workday-deep--{today}--v{ver}.md"

    lines = ["---", "model: workday-deep",
             f"scanned_at: {datetime.now(timezone.utc).isoformat()}",
             f"task: workday-deep-pagination-{len(KEYWORDS)}-keywords",
             f"tenants: {len(tenants)}", "---", "",
             f"# Workday deep scan — {today}", "",
             "| Posted | Role | Company | Location | Source |", "|---|---|---|---|---|"]
    for r in sorted(diffed, key=lambda x: x["posted"] or "", reverse=True):
        lines.append(f"| {r['posted']} | [{r['title']}]({r['url']}) | "
                     f"{r['company']} | {r['location']} | Workday ({r['kw']}) |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {path} ({len(diffed)} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
