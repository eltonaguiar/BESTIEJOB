#!/usr/bin/env python3
"""Harvest agency / job-board postings that state their own posting date.

Why this exists: the board rejects any row without an absolute YYYY-MM-DD, and
agency boards are where a lot of Toronto ServiceNow/Salesforce contract work
first appears. Every enabled source in `config/agency_boards.json` was proven by
`local_tools/detail_probe.py` to expose a real posting date on the posting
itself; the adapters below encode *how*, because the boards differ:

  jsonld    JSON-LD JobPosting with datePosted + jobLocation.address  (Procom,
            CareerBeacon)
  dice      Dice embeds `"jobLocation":{...,"displayName":"City, Region, USA"}`
            and `"postedDate":"YYYY-MM-DDTHH:MM:SSZ"` in its page payload; its
            JSON-LD carries no address at all
  page_text date is literal "Posted <date>", location is matched from the page
            (Built In Toronto)

Rows are written to `inbox/agency-board--<date>--v1.md` in the exact table shape
`tools/jobs_merge_inbox.py` parses, so the normal merge/publish path picks them
up. Nothing is written when there are no dated, Toronto-area matches.

    python3 scripts/agency_board_scan.py --dry-run
    python3 scripts/agency_board_scan.py --max-per-source 40 --workers 10
    python3 tools/jobs_merge_inbox.py --dry-run
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from curl_cffi import requests as cr

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config" / "agency_boards.json"
INBOX = ROOT / "inbox"
IMPERSONATE = "chrome"

ROLE = re.compile(r"service\s*now|salesforce|itsm|itam|mulesoft|\bcpq\b|"
                  r"now platform|servicenow", re.I)
# Vendor sales roles name the product but are not platform work, and the board
# has always excluded the sales function rather than the product word.
SALES = re.compile(r"\bsales\b|account executive|account manager|business development|"
                   r"customer success|\bcrm sales\b", re.I)
JSONLD = re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.S)
TEXT_DATE = re.compile(r'(?:posted|date posted|posting date)[^\dA-Za-z]{0,20}'
                       r'([A-Z][a-z]{2,8}\.?\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}'
                       r'|\d{4}-\d{2}-\d{2})', re.I)
# Dice's Next.js payload is backslash-escaped, so every quote may be \".
DICE_DATE = re.compile(r'\\?"postedDate\\?"\s*:\s*\\?"(\d{4}-\d{2}-\d{2})')
DICE_LOC = re.compile(r'\\?"jobLocation\\?"\s*:\s*\{[^{}]{0,300}?'
                      r'\\?"displayName\\?"\s*:\s*\\?"([^"\\]{3,80})')
PROVINCE = re.compile(r",\s*(ON|Ontario|QC|Quebec|BC|British Columbia|AB|Alberta|"
                      r"MB|Manitoba|SK|Saskatchewan|NS|Nova Scotia|NB|New Brunswick|"
                      r"NL|Newfoundland|PE|PEI|YT|Yukon|NT|NU)\b")
# Only the city name is taken from the page. The province is decided
# separately, because the text immediately after a city on these pages is often
# embedded JSON ("Toronto","addressRegion":"Ontario") rather than prose.
CITY_HINT = re.compile(
    r"\b(Toronto|Mississauga|Brampton|Markham|Vaughan|Richmond Hill|Scarborough|"
    r"Etobicoke|North York|Oakville|Burlington|Milton|Ajax|Pickering|Newmarket|"
    r"Ottawa|Kitchener|Waterloo|Hamilton|London|Windsor|Kingston|Guelph|Barrie|"
    r"Montreal|Qu[ée]bec|Laval|Gatineau|Vancouver|Victoria|Burnaby|Surrey|"
    r"Calgary|Edmonton|Winnipeg|Halifax)\b")
ONTARIO = re.compile(r"\bOntario\b|,\s*ON\b")
GTA = {"toronto", "mississauga", "brampton", "markham", "vaughan", "richmond hill",
       "scarborough", "etobicoke", "north york", "oakville", "burlington", "milton",
       "ajax", "pickering", "newmarket"}
# Cities that also exist outside Canada: a bare name is not evidence of Canada.
AMBIGUOUS = {"london", "cambridge", "richmond", "windsor", "surrey", "victoria",
             "waterloo", "hamilton", "kingston"}


def norm_url(url: str) -> str:
    parts = urlsplit(url.strip())
    return urlunsplit((parts.scheme, parts.netloc.lower(),
                       parts.path.rstrip("/"), "", ""))


def check_place(locality: str, region: str = "", country: str = "") -> str:
    """Return toronto | ontario | remote-canada | other-canada | '' (reject)."""
    locality, region, country = (locality or ""), (region or ""), (country or "")
    low = " ".join((locality, region, country)).lower()
    if "usa" in low or "united states" in low or country.strip().upper() == "US":
        return ""
    city = locality.split(",")[0].strip().lower()
    ca = ("canada" in low) or bool(PROVINCE.search(f", {region}")) or \
        region.strip().upper() in {"ON", "QC", "BC", "AB", "MB", "SK", "NS", "NB",
                                   "NL", "PE", "YT", "NT", "NU"}
    if city in GTA:
        return "toronto" if (ca or "on" in low or "ontario" in low) else ("" if country else "toronto")
    if not ca and city in AMBIGUOUS:
        return ""
    if region.strip().upper() == "ON" or "ontario" in low:
        return "ontario"
    if not ca:
        return ""
    if "remote" in low:
        return "remote-canada"
    return "other-canada"


def jsonld_facts(html: str) -> dict | None:
    for raw in JSONLD.findall(html):
        try:
            data = json.loads(raw.strip())
        except Exception:
            continue
        for node in (data if isinstance(data, list) else [data]):
            if not isinstance(node, dict) or "JobPosting" not in str(node.get("@type", "")):
                continue
            posted = str(node.get("datePosted") or "")[:10]
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", posted):
                continue
            locality = region = country = ""
            locations = node.get("jobLocation") or []
            for item in (locations if isinstance(locations, list) else [locations]):
                if not isinstance(item, dict):
                    continue
                addr = item.get("address") or {}
                if not isinstance(addr, dict):
                    continue
                locality = str(addr.get("addressLocality") or locality)
                region = str(addr.get("addressRegion") or region)
                country = str(addr.get("addressCountry") or country)
            org = node.get("hiringOrganization") or {}
            return {"title": str(node.get("title") or "").strip(), "posted": posted,
                    "locality": locality, "region": region, "country": country,
                    "company": str(org.get("name") or "") if isinstance(org, dict) else ""}
    return None


def text_facts(html: str) -> dict | None:
    m = TEXT_DATE.search(html)
    if not m:
        return None
    for fmt in ("%Y-%m-%d", "%b %d %Y", "%B %d %Y"):
        try:
            posted = dt.datetime.strptime(
                re.sub(r"(st|nd|rd|th)", "", m.group(1)).replace(",", "").strip(),
                fmt).date().isoformat()
        except ValueError:
            continue
        hint = CITY_HINT.search(html)
        return {"title": "", "posted": posted,
                "locality": hint.group(1) if hint else "",
                "region": "ON" if ONTARIO.search(html[:60000]) else "",
                "country": "Canada", "company": ""}
    return None


def dice_facts(html: str) -> dict | None:
    d = DICE_DATE.search(html)
    if not d:
        return None
    loc = DICE_LOC.search(html)
    display = loc.group(1) if loc else ""
    parts = [p.strip() for p in display.split(",")]
    locality = parts[0] if parts else ""
    region = parts[1] if len(parts) > 1 else ""
    country = parts[2] if len(parts) > 2 else ""
    return {"title": "", "posted": d.group(1), "locality": locality,
            "region": region, "country": country, "company": ""}


ADAPTERS = {"jsonld": jsonld_facts, "dice": dice_facts, "page_text": text_facts}


def gather_links(source: dict, limit: int) -> list[str]:
    pat = re.compile(source["link_re"])
    found: list[str] = []
    base = source.get("base_url", "")
    targets = ([source["sitemap_url"]] if source.get("sitemap_url")
               else source["search_urls"])
    for url in targets:
        try:
            r = cr.get(url, impersonate=IMPERSONATE, timeout=35)
        except Exception:
            continue
        if r.status_code != 200:
            continue
        text = r.text or ""
        for m in pat.finditer(text):
            u = m.group(0)
            if u.startswith("/"):
                u = base + u
            if u not in found:
                found.append(u)
        if len(found) >= limit:
            break
    return found[:limit]


def fetch_job(args) -> tuple[dict | None, str]:
    source, url = args
    try:
        r = cr.get(url, impersonate=IMPERSONATE, timeout=35)
    except Exception as exc:
        return None, f"{type(exc).__name__}"
    if r.status_code != 200:
        return None, f"http {r.status_code}"
    html = r.text or ""
    adapter = ADAPTERS[source.get("adapter", "jsonld")]
    facts = adapter(html)
    if not facts:
        return None, "no date"
    title = facts["title"]
    employer = facts["company"]
    if not title:
        m = re.search(r"<title>([^<]{6,160})</title>", html, re.I)
        raw = m.group(1) if m else ""
        raw = re.split(r"\s*\|\s*(?:Built In|Dice|CareerBeacon)", raw)[0].strip()
        # Built In titles read "<Role> - <Company>"; the company is not part of
        # the role and becomes the row's company instead of the board's name.
        if source.get("adapter") == "page_text" and " - " in raw:
            head, _, tail = raw.rpartition(" - ")
            if head and tail and len(tail) < 60:
                title, employer = head.strip(), employer or tail.strip()
        if not title:
            title = raw
    if not ROLE.search(title) or SALES.search(title):
        return None, "off-topic"
    # A job AT ServiceNow/Salesforce is not a ServiceNow/Salesforce role; if the
    # keyword only appears because it is the employer, drop it.
    if employer and ROLE.search(employer) and \
            not ROLE.search(ROLE.sub("", title)):
        return None, "employer-only"
    place = check_place(facts["locality"], facts["region"], facts["country"])
    if not place:
        return None, f"place:{facts['locality'][:24] or '-'}"
    return {"title": title, "url": url, "posted": facts["posted"], "place": place,
            "location": ", ".join(p for p in (facts["locality"], facts["region"],
                                              facts["country"]) if p) or place,
            "company": employer or source["name"], "source": source["name"]}, "ok"


def known_urls() -> set[str]:
    urls: set[str] = set()
    for name in ("jobs.json", "public/jobs.json", "public/jobs-data.json"):
        p = ROOT / name
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        rows = data if isinstance(data, list) else data.get("jobs", [])
        for row in rows:
            if isinstance(row, dict) and row.get("url"):
                urls.add(norm_url(str(row["url"])))
    return urls


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", help="comma-separated source names")
    ap.add_argument("--max-per-source", type=int, default=40)
    ap.add_argument("--workers", type=int, default=10)
    args = ap.parse_args()

    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    enabled = [s for s in cfg["sources"] if s.get("enabled")]
    if args.only:
        wanted = {n.strip().lower() for n in args.only.split(",")}
        enabled = [s for s in enabled if s["name"].lower() in wanted]
    have = known_urls()
    print(f"{len(enabled)} enabled sources; {len(have)} known URLs")

    jobs: list[tuple[dict, str]] = []
    for src in enabled:
        links = gather_links(src, args.max_per_source)
        print(f"  {src['name']:18} links={len(links):>3}")
        jobs += [(src, u) for u in links]

    rows: list[dict] = []
    seen: set[str] = set()
    reasons: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for got, why in pool.map(fetch_job, jobs):
            reasons[why] = reasons.get(why, 0) + 1
            if not got:
                continue
            key = norm_url(got["url"])
            if key in seen or key in have:
                reasons["duplicate"] = reasons.get("duplicate", 0) + 1
                continue
            seen.add(key)
            rows.append(got)

    print("  outcomes: " + ", ".join(f"{k}={v}" for k, v in
                                     sorted(reasons.items(), key=lambda kv: -kv[1])[:8]))
    rows.sort(key=lambda r: (r["posted"], r["company"]), reverse=True)
    print(f"\n{len(rows)} dated, in-scope, non-duplicate rows")
    for r in rows:
        print(f"  {r['posted']} | {r['place']:13} | {r['company'][:26]:26} | "
              f"{r['title'][:52]:52} | {r['source']}")

    if not rows:
        print("nothing to write")
        return 0
    stamp = dt.date.today().isoformat()
    out = INBOX / f"agency-board--{stamp}--v1.md"
    body = [f"# Agency boards scan — {stamp}", "",
            "| Posted | Role | Company | Location | Note |",
            "| --- | --- | --- | --- | --- |"]
    for r in rows:
        body.append(f"| {r['posted']} | [{r['title'].replace('|', '/')}]({r['url']}) | "
                    f"{r['company'].replace('|', '/')} | {r['location'].replace('|', '/')} | "
                    f"via {r['source']} |")
    if args.dry_run:
        print("\n--- dry run, would write", out.name, "---")
        print("\n".join(body[:10]))
        return 0
    INBOX.mkdir(exist_ok=True)
    out.write_text("\n".join(body) + "\n", encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
