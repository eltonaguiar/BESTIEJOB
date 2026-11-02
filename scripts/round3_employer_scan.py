#!/usr/bin/env python3
"""Round-3 job scan (2026-11-02) — employer ATS + boards, data collection only.

Channels
  1. Workday tenants (RBC, TD, BMO, CIBC, Scotiabank, Manulife, Telus, Rogers,
     Metrolinx, Ontario Health, ...) via the public /wday/cxs JSON endpoint.
     Site slug is discovered from the tenant root redirect, not hardcoded.
  2. LinkedIn guest job-search fragment endpoint.
  3. Indeed Canada RSS.
  4. Ontario Public Service (gojobs.gov.on.ca).

Writes raw output to bestiejob/raw/ and prints a compact per-source summary.
Never prints credentials.
"""
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from curl_cffi import requests as cr
except ImportError:
    sys.exit("FATAL: curl_cffi not installed")

RAW = Path(__file__).resolve().parent.parent / "raw"
RAW.mkdir(exist_ok=True)
OUT = RAW / "round3_employer_2026-11-02.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

KEYWORDS = ["ServiceNow", "Salesforce"]
RELEVANT = re.compile(
    r"servicenow|salesforce|itsm|itam|cmdb|itom|snow\b|apex|mulesoft|"
    r"integration hub|service catalog|workday|grc|now assist|sap\s*s/4",
    re.I,
)
NOT_RELEVANT = re.compile(
    r"sales\s+(representative|associate|manager|consultant|lead)|account executive|"
    r"retail|store manager|cashier|teller|customer service representative", re.I
)

TENANTS = [
    "rbc", "td", "bmo", "cibc", "scotiabank", "manulife", "sunlife",
    "telus", "rogers", "metrolinx", "ontariohealth", "hydroone",
    "cppib", "otpp", "loblaw", "opg", "torontohydro", "desjardins",
]
WD_HOSTS = ["wd3", "wd1", "wd5", "wd10", "wd2"]


def log(*a):
    print(*a, flush=True)


# --------------------------------------------------------------- workday
def discover_site(tenant):
    """Root redirects to /en-US/<SITE>; returns (host, site) or None."""
    for h in WD_HOSTS:
        host = f"{tenant}.{h}.myworkdayjobs.com"
        try:
            r = cr.get(f"https://{host}", impersonate="chrome124",
                       timeout=25, allow_redirects=True, headers={"User-Agent": UA})
        except Exception:
            continue
        if r.status_code >= 400:
            continue
        m = re.search(r"/(?:[a-z]{2}-[A-Z]{2}/)?([A-Za-z0-9_\-]+)/?$", r.url or "")
        if not m:
            continue
        site = m.group(1)
        if site.lower() in {"myworkdayjobs", "en-us"}:
            continue
        return host, site
    return None


def wd_search(host, tenant, site, text, limit=20):
    url = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
    body = {"appliedFacets": {}, "limit": limit, "offset": 0, "searchText": text}
    try:
        r = cr.post(url, json=body, impersonate="chrome124", timeout=30,
                    headers={"User-Agent": UA, "Content-Type": "application/json",
                             "Accept": "application/json"})
    except Exception as e:
        return None, str(e)[:80]
    if r.status_code != 200:
        return None, f"HTTP {r.status_code}"
    try:
        return r.json(), None
    except Exception:
        return None, "non-JSON"


def wd_detail_date(host, tenant, site, external_path):
    """Exact datePosted from the posting's JSON-LD."""
    url = f"https://{host}/en-US/{site}{external_path}"
    try:
        r = cr.get(url, impersonate="chrome124", timeout=30, headers={"User-Agent": UA})
    except Exception:
        return None, None
    if r.status_code != 200:
        return None, None
    txt = r.text
    m = re.search(r'"datePosted"\s*:\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})', txt)
    loc = re.search(r'"addressLocality"\s*:\s*"([^"]+)"', txt)
    return (m.group(1) if m else None), (loc.group(1) if loc else None)


def scan_workday():
    found, report = [], {}
    for tenant in TENANTS:
        disc = discover_site(tenant)
        if not disc:
            report[tenant] = "no workday tenant"
            continue
        host, site = disc
        hits, err = [], None
        for kw in KEYWORDS:
            data, err = wd_search(host, tenant, site, kw)
            if not data:
                break
            for p in data.get("jobPostings", []):
                title = p.get("title", "")
                if not RELEVANT.search(title) or NOT_RELEVANT.search(title):
                    continue
                hits.append({
                    "tenant": tenant, "host": host, "site": site,
                    "title": title,
                    "location": p.get("locationsText", ""),
                    "posted_rel": p.get("postedOn", ""),
                    "path": p.get("externalPath", ""),
                })
        if err:
            report[tenant] = f"{host}/{site} -> {err}"
            continue
        # dedupe by path, resolve exact dates
        seen, uniq = set(), []
        for h in hits:
            if h["path"] in seen:
                continue
            seen.add(h["path"])
            d, loc = wd_detail_date(host, tenant, site, h["path"])
            h["posted"] = d
            if loc:
                h["location"] = loc
            uniq.append(h)
        found.extend(uniq)
        report[tenant] = f"{host}/{site} -> {len(uniq)} relevant"
    return found, report


# --------------------------------------------------------------- linkedin
def scan_linkedin():
    out, report = [], {}
    locs = ["Toronto%2C%20Ontario%2C%20Canada", "Canada"]
    for kw in ["ServiceNow", "Salesforce"]:
        n = 0
        for loc in locs:
            url = ("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
                   f"?keywords={kw}&location={loc}&f_TPR=r259200&start=0")
            try:
                r = cr.get(url, impersonate="chrome124", timeout=30,
                           headers={"User-Agent": UA})
            except Exception as e:
                report[f"{kw}/{loc[:12]}"] = str(e)[:60]
                continue
            if r.status_code != 200:
                report[f"{kw}/{loc[:12]}"] = f"HTTP {r.status_code}"
                continue
            html = r.text
            cards = re.findall(r"<li>(.*?)</li>", html, re.S)
            for c in cards:
                t = re.search(r'class="base-search-card__title"[^>]*>\s*(.*?)\s*<', c, re.S)
                comp = re.search(r'class="hidden-nested-link"[^>]*>\s*(.*?)\s*<', c, re.S)
                link = re.search(r'href="(https://[a-z]{2}\.linkedin\.com/jobs/view/[^"?]+)', c)
                dt = re.search(r'datetime="([0-9]{4}-[0-9]{2}-[0-9]{2})"', c)
                where = re.search(r'class="job-search-card__location"[^>]*>\s*(.*?)\s*<', c, re.S)
                if not (t and link):
                    continue
                title = re.sub(r"\s+", " ", t.group(1))[:200]
                if not RELEVANT.search(title) or NOT_RELEVANT.search(title):
                    continue
                out.append({
                    "title": title,
                    "company": re.sub(r"\s+", " ", comp.group(1))[:120] if comp else "",
                    "location": re.sub(r"\s+", " ", where.group(1))[:120] if where else "",
                    "url": link.group(1),
                    "posted": dt.group(1) if dt else None,
                    "source": "linkedin-guest",
                })
                n += 1
        report[kw] = f"{n} relevant cards"
    return out, report


# --------------------------------------------------------------- indeed
def scan_indeed():
    out, report = [], {}
    for kw in ["ServiceNow", "Salesforce"]:
        url = f"https://ca.indeed.com/rss?q={kw}&l=Toronto%2C+ON&fromage=3"
        try:
            r = cr.get(url, impersonate="chrome124", timeout=30,
                       headers={"User-Agent": UA})
        except Exception as e:
            report[kw] = str(e)[:60]
            continue
        if r.status_code != 200 or "<rss" not in r.text[:400].lower():
            report[kw] = f"HTTP {r.status_code} ({len(r.text)} bytes)"
            continue
        items = re.findall(r"<item>(.*?)</item>", r.text, re.S)
        for it in items:
            t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", it, re.S)
            l = re.search(r"<link>(.*?)</link>", it, re.S)
            d = re.search(r"<pubDate>(.*?)</pubDate>", it, re.S)
            if not (t and l):
                continue
            title = re.sub(r"\s+", " ", t.group(1)).strip()
            if not RELEVANT.search(title) or NOT_RELEVANT.search(title):
                continue
            posted = None
            if d:
                try:
                    from email.utils import parsedate_to_datetime
                    posted = parsedate_to_datetime(d.group(1)).date().isoformat()
                except Exception:
                    pass
            out.append({"title": title, "company": "", "location": "Toronto, ON",
                        "url": l.group(1).strip(), "posted": posted, "source": "indeed-rss"})
        report[kw] = f"{len(items)} rss items"
    return out, report


# --------------------------------------------------------------- ontario gov
def scan_gojobs():
    out, report = [], {}
    for kw in ["ServiceNow", "Salesforce"]:
        url = ("https://www.gojobs.gov.on.ca/SearchResults.aspx"
               f"?search={kw}&lang=en")
        try:
            r = cr.get(url, impersonate="chrome124", timeout=30, headers={"User-Agent": UA})
        except Exception as e:
            report[kw] = str(e)[:60]
            continue
        report[kw] = f"HTTP {r.status_code} ({len(r.text)}b)"
        for m in re.finditer(r'href="(JobDetails\.aspx\?JobID=(\d+)[^"]*)"[^>]*>(.*?)</a>', r.text, re.S):
            title = re.sub(r"<[^>]+>", " ", m.group(3))
            title = re.sub(r"\s+", " ", title).strip()
            if not title or not RELEVANT.search(title):
                continue
            out.append({"title": title, "company": "Ontario Public Service",
                        "location": "Ontario", "url": "https://www.gojobs.gov.on.ca/" + m.group(1),
                        "posted": None, "source": "gojobs"})
    return out, report


def main():
    result = {"fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "sources": {}}
    wd, wd_rep = scan_workday()
    result["workday"] = wd
    result["sources"]["workday"] = wd_rep
    log("WORKDAY:", json.dumps(wd_rep, indent=1))

    li, li_rep = scan_linkedin()
    result["linkedin"] = li
    result["sources"]["linkedin"] = li_rep
    log("LINKEDIN:", li_rep)

    ind, ind_rep = scan_indeed()
    result["indeed"] = ind
    result["sources"]["indeed"] = ind_rep
    log("INDEED:", ind_rep)

    gov, gov_rep = scan_gojobs()
    result["gojobs"] = gov
    result["sources"]["gojobs"] = gov_rep
    log("GOJOBS:", gov_rep)

    OUT.write_text(json.dumps(result, indent=1), encoding="utf-8")
    total = len(wd) + len(li) + len(ind) + len(gov)
    log(f"\nTOTAL candidates: {total} -> {OUT}")


if __name__ == "__main__":
    main()
