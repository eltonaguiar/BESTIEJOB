#!/usr/bin/env python3
"""Round-3b scan: employer ATS APIs discovered by fingerprinting (2026-11-02).

Channels verified reachable from this host:
  * TD Bank            -> Workday  td.wd3 / TD_Bank_Careers  (/wday/cxs JSON)
  * Metrolinx          -> Oracle Recruiting Cloud ehtc.fa.ca2 / CX_1 (hcmRestApi)
  * RBC / Bell / BMO   -> Phenom career sites (api/apply/v2 probe)
  * Job Bank Canada    -> HTML search results

Writes bestiejob/raw/round3b_ats_2026-11-02.json and prints per-source status.
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    from curl_cffi import requests as cr
except ImportError:
    sys.exit("FATAL: curl_cffi not installed")

RAW = Path(__file__).resolve().parent.parent / "raw"
RAW.mkdir(exist_ok=True)
OUT = RAW / "round3b_ats_2026-11-02.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

RELEVANT = re.compile(
    r"servicenow|salesforce|itsm|itam|cmdb|itom|\bsnow\b|apex|mulesoft|"
    r"integration hub|service catalog|grc|now assist", re.I)
EXCLUDE = re.compile(
    r"sales\s+(representative|associate|manager|consultant|lead|agent)|"
    r"account executive|retail|store manager|cashier|teller|barista", re.I)

KEYWORDS = ["ServiceNow", "Salesforce"]


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def relevant(title):
    return bool(RELEVANT.search(title)) and not EXCLUDE.search(title)


# ---------------------------------------------------------------- Workday
def workday(tenant, host, site):
    out, status = [], None
    for kw in KEYWORDS + ["ITSM", "CMDB"]:
        url = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
        body = {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": kw}
        try:
            r = cr.post(url, json=body, impersonate="chrome124", timeout=30,
                        headers={"User-Agent": UA, "Accept": "application/json",
                                 "Content-Type": "application/json"})
        except Exception as e:
            status = str(e)[:70]
            continue
        if r.status_code != 200:
            status = f"HTTP {r.status_code}"
            continue
        status = "ok"
        try:
            data = r.json()
        except Exception:
            status = "non-JSON"
            continue
        for p in data.get("jobPostings", []):
            title = clean(p.get("title", ""))
            if not relevant(title):
                continue
            path = p.get("externalPath", "")
            out.append({
                "title": title,
                "company": tenant.upper(),
                "location": clean(p.get("locationsText", "")),
                "url": f"https://{host}/en-US/{site}{path}",
                "posted": None,
                "posted_rel": p.get("postedOn", ""),
                "source": "workday",
            })
    return out, status


def workday_date(url):
    try:
        r = cr.get(url, impersonate="chrome124", timeout=30, headers={"User-Agent": UA})
    except Exception:
        return None
    if r.status_code != 200:
        return None
    m = re.search(r'"datePosted"\s*:\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})', r.text)
    return m.group(1) if m else None


# ---------------------------------------------------------------- Oracle
def oracle(host, site, employer):
    out, status = [], None
    for kw in KEYWORDS:
        url = (f"https://{host}/hcmRestApi/resources/latest/recruitingCEJobRequisitions"
               "?onlyData=true&expand=requisitionList.secondaryLocations"
               f"&finder=findReqs;siteNumber={site},keyword={kw},"
               "limit=25,offset=0,sortBy=POSTING_DATES_DESC")
        try:
            r = cr.get(url, impersonate="chrome124", timeout=30,
                       headers={"User-Agent": UA, "Accept": "application/json"})
        except Exception as e:
            status = str(e)[:70]
            continue
        if r.status_code != 200:
            status = f"HTTP {r.status_code}"
            continue
        status = "ok"
        try:
            data = r.json()
        except Exception:
            status = "non-JSON"
            continue
        items = data.get("items") or []
        for it in items:
            for req in it.get("requisitionList", []):
                title = clean(req.get("Title", ""))
                if not relevant(title):
                    continue
                out.append({
                    "title": title,
                    "company": employer,
                    "location": clean(req.get("PrimaryLocation", "")),
                    "url": (f"https://{host}/hcmUI/CandidateExperience/en/sites/{site}"
                            f"/job/{req.get('Id', '')}"),
                    "posted": (req.get("PostedDate") or "")[:10] or None,
                    "source": "oracle",
                })
    return out, status


# ---------------------------------------------------------------- Phenom
def phenom(site_url, domain, employer):
    out, status = [], None
    for kw in KEYWORDS:
        url = (f"{site_url}/api/apply/v2/jobs?domain={domain}&start=0&num=20"
               f"&exact_phrase={kw}&sort_by=relevance")
        try:
            r = cr.get(url, impersonate="chrome124", timeout=30,
                       headers={"User-Agent": UA, "Accept": "application/json"})
        except Exception as e:
            status = str(e)[:70]
            continue
        if r.status_code != 200:
            status = f"HTTP {r.status_code}"
            continue
        status = "ok"
        try:
            data = r.json()
        except Exception:
            status = "non-JSON"
            continue
        for p in data.get("positions", []):
            title = clean(p.get("name", ""))
            if not relevant(title):
                continue
            loc = p.get("location") or ""
            if isinstance(loc, dict):
                loc = loc.get("city") or ""
            out.append({
                "title": title,
                "company": employer,
                "location": clean(str(loc)),
                "url": p.get("canonicalPositionUrl") or p.get("jobUrl") or "",
                "posted": (p.get("t_create") or "")[:10] or None,
                "source": "phenom",
            })
    return out, status


# ---------------------------------------------------------------- Job Bank
def jobbank(kw):
    out, status = [], None
    url = ("https://www.jobbank.gc.ca/jobsearch/jobsearch"
           f"?searchstring={kw.replace(' ', '+')}&locationstring=Toronto&sort=M&fdate=1")
    try:
        r = cr.get(url, impersonate="chrome124", timeout=30, headers={"User-Agent": UA})
    except Exception as e:
        return out, str(e)[:70]
    if r.status_code != 200:
        return out, f"HTTP {r.status_code}"
    status = "ok"
    for m in re.finditer(r'<a href="(/jobsearch/jobposting/\d+[^"]*)"[^>]*>(.*?)</a>',
                         r.text, re.S):
        title = clean(m.group(2))
        if not relevant(title):
            continue
        out.append({"title": title, "company": "Job Bank", "location": "Toronto, ON",
                    "url": "https://www.jobbank.gc.ca" + m.group(1),
                    "posted": None, "source": "jobbank"})
    return out, status


def main():
    res = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "sources": {}, "jobs": []}

    def add(name, jobs, status):
        res["sources"][name] = f"{status} ({len(jobs)} relevant)"
        res["jobs"].extend(jobs)
        print(f"{name:26s} {status:22s} {len(jobs)} relevant", flush=True)

    jobs, st = workday("td", "td.wd3.myworkdayjobs.com", "TD_Bank_Careers")
    for j in jobs:
        j["posted"] = workday_date(j["url"])
    add("TD (Workday)", jobs, st)

    jobs, st = oracle("ehtc.fa.ca2.oraclecloud.com", "CX_1", "Metrolinx")
    add("Metrolinx (Oracle)", jobs, st)

    jobs, st = phenom("https://jobs.rbc.com", "rbc.com", "RBC")
    add("RBC (Phenom)", jobs, st)

    jobs, st = phenom("https://jobs.bell.ca", "bell.ca", "Bell")
    add("Bell (Phenom)", jobs, st)

    jobs, st = phenom("https://jobs.bmo.com", "bmo.com", "BMO")
    add("BMO (Phenom)", jobs, st)

    for kw in KEYWORDS:
        jobs, st = jobbank(kw)
        add(f"Job Bank [{kw}]", jobs, st)

    # dedupe on url
    seen, uniq = set(), []
    for j in res["jobs"]:
        key = (j.get("url") or "").split("?")[0].rstrip("/") or j["title"]
        if key in seen:
            continue
        seen.add(key)
        uniq.append(j)
    res["jobs"] = uniq
    OUT.write_text(json.dumps(res, indent=1), encoding="utf-8")
    print(f"\nunique: {len(uniq)} -> {OUT}")


if __name__ == "__main__":
    main()
