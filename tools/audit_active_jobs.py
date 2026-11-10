#!/usr/bin/env python3
"""
Audit BESTIEJOB active job listings: live status + geo classification.
Reusable for ad-hoc or CI checks. Does not require secrets for public ATS pages.

Usage:
  python3 tools/audit_active_jobs.py --input jobs.json --out raw/job_audit.json --md raw/job_audit.md
  python3 tools/audit_active_jobs.py --scope international,us,other,unknown,remote_unknown --limit 0
  python3 tools/audit_active_jobs.py --url "https://..."  # single URL probe
"""
from __future__ import annotations
import argparse, json, re, time, random, sys
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except Exception:
    print("requests required", file=sys.stderr); sys.exit(2)

UA = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
]
DEAD_PATTERNS = [
    r"no longer (available|accepting|open)",
    r"position (has been )?(filled|closed|expired)",
    r"job (not found|expired|no longer exists|has been removed)",
    r"posting.*(removed|unavailable|has expired)",
    r"this (job|position|posting) (is|has been) (closed|filled|expired|removed)",
    r"we('re| are) no longer accepting",
    r"opportunity is no longer available",
    r"requisition (is )?closed",
]
INTL_LOC = re.compile(r"\b(australia|sydney,?\s*(nsw|australia|international)|melbourne|brisbane|perth,?\s*australia|united kingdom|\buk\b|london,?\s*(uk|england)|dublin,?\s*ireland|ireland|india|bengaluru|bangalore|hyderabad|pune|mumbai|gurugram|gurgaon|noida|chennai|delhi,?\s*india|philippines|manila|singapore|germany|france|netherlands|poland|mexico|brazil|japan|china)\b", re.I)
CA_LOC = re.compile(r"\b(canada|ontario|quebec|qu\u00e9bec|british columbia|alberta|manitoba|saskatchewan|nova scotia|new brunswick|pei|prince edward|newfoundland|labrador|yukon|nunavut|northwest territories)\b", re.I)
TORONTO = re.compile(r"\b(toronto|gta|greater toronto|mississauga|markham|scarborough|north york|etobicoke|vaughan|brampton|oakville|burlington|richmond hill|pickering|ajax|whitby)\b", re.I)
US_STATE = re.compile(r",\s*(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY|DC)\b")
US_WORDS = re.compile(r"\b(united states|\busa\b|u\.s\.a\.|u\.s\.)\b", re.I)
SYDNEY_CA = re.compile(r"\bsydney,?\s*(nova scotia|ns|cape breton)\b", re.I)

def classify_geo(job: dict, page_text: str = "") -> str:
    loc = (job.get("location") or "").strip()
    arr = (job.get("arrangement") or "").strip()
    hay = " ".join([loc, job.get("title") or "", job.get("excerpt") or "", page_text[:2000]]).lower()
    locl = loc.lower()
    # Sydney: Australia context in location/url vs Canada (Sydney, NS)
    if re.search(r"sydney", locl):
        if SYDNEY_CA.search(locl) or "cape breton" in locl:
            pass  # Canadian
        elif re.search(r"australia|nsw|international house|sussex st|/sydney", (locl + " " + (job.get("url") or "").lower())):
            return "international"
    url = (job.get("url") or "").lower()
    if re.search(r"/job/sydney[-/]|-sydney/|sydney.*australia", url):
        return "international"
    if INTL_LOC.search(locl) and not (CA_LOC.search(locl) and not re.search(r"\baustralia\b", locl)):
        # allow "Canada, Europe, USA" lists? treat as mixed/remote-eligible but flag; keep simple
        if "canada" in locl and not re.search(r"\b(india|australia|singapore|philippines|mexico|germany|france|netherlands|poland|brazil|japan|china|united kingdom|ireland)\b", locl):
            pass
        else:
            return "international"
    # mixed regions like "Brazil, Canada, Europe, USA"
    if re.search(r"brazil|europe,?\s*usa|usa,?\s*europe", locl) and "canada" in locl:
        return "international"  # not Canada-specific; flag for review
    remote = "remote" in locl or "remote" in arr.lower() or "remote" in hay[:500]
    is_ca = bool(CA_LOC.search(locl)) or ("canada" in hay[:800])
    is_tor = bool(TORONTO.search(locl))
    is_us = bool(US_WORDS.search(locl)) or (bool(US_STATE.search(loc)) and "canada" not in locl)
    if is_tor and (is_ca or remote):
        return "toronto_gta"
    if is_ca and remote and not is_tor:
        return "remote_canada"
    if is_ca and not is_us:
        return "canada_other"
    if is_us and not is_ca:
        return "us"
    if remote and not is_ca and not is_us:
        return "remote_unknown"
    if not loc or loc.lower() in ("unknown", "n/a", "unknown / peer claim not verified"):
        return "unknown"
    return "other"

def probe(job: dict, timeout: int = 18) -> dict:
    url = job.get("url") or ""
    res = {"url": url, "status": None, "live": "unknown", "dead_reason": None, "page_geo_hint": None}
    if not url:
        res["live"] = "unknown"; return res
    try:
        r = requests.get(url, headers={"User-Agent": random.choice(UA)}, timeout=timeout, allow_redirects=True)
        res["status"] = r.status_code
        if r.status_code == 404:
            res["live"] = "dead"; res["dead_reason"] = "http_404"; return res
        if r.status_code >= 400:
            res["live"] = "unknown"; return res
        txt = r.text or ""
        low = txt[:150000].lower()
        for p in DEAD_PATTERNS:
            if re.search(p, low):
                res["live"] = "dead"; res["dead_reason"] = p; return res
        res["live"] = "active"
        # page geo hints (be careful: person names; prefer structured/location blocks)
        m = re.search(r'"locationsText"\s*:\s*"([^"]{2,120})"', txt)
        if m: res["page_geo_hint"] = m.group(1)
        elif re.search(r'"country"\s*:\s*\{\s*"descriptor"\s*:\s*"([^"]+)"', txt):
            res["page_geo_hint"] = re.search(r'"country"\s*:\s*\{\s*"descriptor"\s*:\s*"([^"]+)"', txt).group(1)
        # Accenture/Workday sometimes embed location
        if re.search(r'\bsydney\b', low) and re.search(r'\baustralia\b', low):
            res["page_geo_hint"] = (res["page_geo_hint"] or "") + " [Sydney, Australia signal]"
    except Exception as e:
        res["live"] = "unknown"; res["dead_reason"] = type(e).__name__
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="jobs.json")
    ap.add_argument("--out", default="raw/job_audit.json")
    ap.add_argument("--md", default="raw/job_audit.md")
    ap.add_argument("--scope", default="all", help="comma list of geo buckets or 'all'")
    ap.add_argument("--limit", type=int, default=0, help="0=no limit")
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--probe", action="store_true", help="HTTP probe liveness (default true for scoped runs)")
    ap.add_argument("--no-probe", action="store_true")
    ap.add_argument("--url", help="probe a single URL and exit")
    args = ap.parse_args()

    if args.url:
        job={"url":args.url,"location":"","title":"","excerpt":""}
        p=probe(job); print(json.dumps(p, indent=2)); return

    path = Path(args.input)
    d = json.loads(path.read_text())
    jobs = d.get("jobs", d) if isinstance(d, dict) else d
    scope = None if args.scope == "all" else set(s.strip() for s in args.scope.split(",") if s.strip())

    rows = []
    for j in jobs:
        geo = classify_geo(j)
        if scope and geo not in scope: continue
        rows.append({"job": j, "geo": geo})
    if args.limit and args.limit > 0:
        rows = rows[:args.limit]

    do_probe = args.probe or (scope is not None) or (args.limit > 0)
    if args.no_probe: do_probe = False

    results = []
    def work(item):
        j=item["job"]
        rec = {
            "id": j.get("id"), "title": j.get("title"), "company": j.get("company"),
            "location": j.get("location"), "url": j.get("url"), "source": j.get("source"),
            "postedDate": (j.get("postedDate") or "")[:10], "geo": item["geo"],
        }
        if do_probe:
            pr = probe(j); rec.update(pr)
        else:
            rec.update({"status": None, "live": "not_probed", "dead_reason": None, "page_geo_hint": None})
        return rec

    if do_probe:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futs = [ex.submit(work, it) for it in rows]
            for i,f in enumerate(as_completed(futs),1):
                results.append(f.result())
                if i % 50 == 0: print(f"probed {i}/{len(rows)}", file=sys.stderr)
    else:
        for it in rows: results.append(work(it))

    # stable order
    results.sort(key=lambda r: (r.get("geo",""), r.get("live",""), r.get("company","") or "", r.get("title","") or ""))

    from collections import Counter
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input": str(path), "total_jobs_in_file": len(jobs), "audited": len(results),
        "probe_enabled": do_probe,
        "by_geo": dict(Counter(r["geo"] for r in results)),
        "by_live": dict(Counter(r["live"] for r in results)),
    }
    outp = Path(args.out); outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps({"summary": summary, "results": results}, indent=2))

    # md report
    lines = [f"# Active Jobs Audit", "", f"- Generated: {summary['generated_at']}", f"- Input: `{summary['input']}` ({summary['total_jobs_in_file']} jobs)", f"- Audited: {summary['audited']} | probed: {summary['probe_enabled']}", "", "## By geo bucket", ""]
    for k,v in sorted(summary['by_geo'].items(), key=lambda x:-x[1]): lines.append(f"- **{k}**: {v}")
    lines += ["", "## By liveness", ""]
    for k,v in sorted(summary['by_live'].items(), key=lambda x:-x[1]): lines.append(f"- **{k}**: {v}")
    lines += ["", "## Flagged (international / dead / unknown, probed)", "", "| Live | Geo | Posted | Company | Title | Location | URL |", "|---|---|---|---|---|---|---|"]
    for r in results:
        if r['geo'] in ('international','us','other','unknown','remote_unknown') or r.get('live') in ('dead','unknown'):
            if do_probe or r['geo']=='international':
                lines.append(f"| {r.get('live','')} | {r['geo']} | {r.get('postedDate','')} | {(r.get('company') or '')[:28]} | {(r.get('title') or '')[:50]} | {(r.get('location') or '')[:28]} | {r.get('url','')} |")
    Path(args.md).parent.mkdir(parents=True, exist_ok=True)
    Path(args.md).write_text("\n".join(lines))
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
