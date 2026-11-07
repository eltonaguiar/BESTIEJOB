#!/usr/bin/env python3
"""Referral-field hunter for BESTIEJOB. Scans job posting pages for referral
indicators and extracts referrer/contact/source hints, then writes results
to raw/referral_hunt_<date>.json and inbox/ for merge."""
import json, os, re, sys, time, random, hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse, urljoin

try:
    import requests
except ImportError:
    print("requests not installed"); sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
JOBS = ROOT / "jobs.json"
RAW = ROOT / "raw"
INBOX = ROOT / "inbox"
RAW.mkdir(exist_ok=True); INBOX.mkdir(exist_ok=True)

# Anti-bot: rotate UAs, add delays, use session, try multiple strategies
UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
]

REFERRAL_PATTERNS = [
    r"referred?\s+by", r"referr(al|er)", r"employee\s+referr",
    r"how\s+did\s+you\s+hear", r"source\s*[:\-]", r"recruiter\s*[:\-]",
    r"hiring\s+manager", r"contact\s*[:\-]", r"apply\s+with\s+referr",
    r'referral[_\-]?code', r'referral[_\-]?id', r'\bref[_\-]?code\b',
    r'name="ref', r'id="ref', r'referrer', r'internal\s+candidate',
]

def fetch(url, session, timeout=20):
    headers = {
        "User-Agent": random.choice(UAS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-CA,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }
    try:
        r = session.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        if r.status_code == 200:
            return r.text, "ok"
        return None, f"http_{r.status_code}"
    except Exception as e:
        return None, str(e)[:80]

def extract_referral_hints(html, url):
    if not html: return []
    hints = []
    low = html.lower()
    for pat in REFERRAL_PATTERNS:
        for m in re.finditer(pat, low[:500000]):
            start = max(0, m.start()-80)
            end = min(len(html), m.end()+120)
            snippet = re.sub(r'\s+', ' ', html[start:end]).strip()
            snippet = re.sub(r'<[^>]+>', ' ', snippet)
            snippet = re.sub(r'\s+', ' ', snippet).strip()[:200]
            hints.append({"pattern": pat, "snippet": snippet})
    # Look for referral fields in forms
    for m in re.finditer(r'<(input|select|textarea)[^>]*(?:name|id|placeholder)=["\'][^"\']*referr[^"\']*["\'][^>]*>', low):
        hints.append({"pattern": "form_field", "snippet": m.group(0)[:200]})
    # LinkedIn/referral links
    for m in re.finditer(r'https?://[^\s"\'>]+referr[^\s"\'>]*', html):
        hints.append({"pattern": "referral_url", "snippet": m.group(0)[:200]})
    # Dedup by snippet
    seen = set(); out = []
    for h in hints:
        k = h["snippet"][:60]
        if k not in seen: seen.add(k); out.append(h)
    return out[:10]

def main():
    max_jobs = int(os.environ.get("MAX_JOBS", "80"))
    sources_filter = os.environ.get("SOURCES", "")  # comma sep
    data = json.load(open(JOBS))
    jobs = data.get("jobs", data) if isinstance(data, dict) else data
    # Prioritize SN/SF, then recent
    def score(j):
        t = (j.get("title","")+" "+j.get("source","")).lower()
        s = 0
        if "servicenow" in t or "itsm" in t or "itam" in t or "cmdb" in t: s += 10
        if "salesforce" in t or "apex" in t or "lwc" in t: s += 8
        src = j.get("source","")
        if src in ("workday","greenhouse","lever","ashby","smartrecruiters"): s += 3
        return -s
    jobs = sorted(jobs, key=score)[:max_jobs]
    if sources_filter:
        sf = set(sources_filter.split(","))
        jobs = [j for j in jobs if j.get("source") in sf]

    session = requests.Session()
    results = []
    stats = {"checked":0,"ok":0,"has_referral_hints":0,"errors":0}
    for i, j in enumerate(jobs):
        url = j.get("url","")
        if not url or "adzuna" in url:  # adzuna are redirect pages, skip
            continue
        stats["checked"] += 1
        html, status = fetch(url, session)
        if html:
            stats["ok"] += 1
            hints = extract_referral_hints(html, url)
            if hints:
                stats["has_referral_hints"] += 1
                results.append({
                    "title": j.get("title"), "company": j.get("company"),
                    "url": url, "source": j.get("source"),
                    "referral_hints": hints, "status": status,
                })
                print(f"[+] {j.get('title','')[:50]} -> {len(hints)} hints")
            else:
                print(f"[-] {j.get('title','')[:50]} (no referral field)")
        else:
            stats["errors"] += 1
            print(f"[!] {j.get('title','')[:50]} -> {status}")
        time.sleep(random.uniform(1.5, 3.5))  # anti-bot delay

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out = RAW / f"referral_hunt_{ts}.json"
    out.write_text(json.dumps({"scanned_at": ts, "stats": stats, "results": results}, indent=2))
    print(f"\nStats: {stats}\nWrote {out} ({len(results)} postings with referral hints)")

    # Also write a summary inbox note
    if results:
        lines = ["---","type: referral-hunt","date: "+ts,"---","","# Referral Hunt Results","",
                 f"Checked {stats['checked']} postings; {stats['has_referral_hints']} had referral indicators.","",
                 "| Role | Company | Source | Hints | URL |","|---|---|---|---|---|"]
        for r in results[:60]:
            hints = "; ".join(set(h["pattern"] for h in r["referral_hints"]))[:60]
            lines.append(f"| {r['title']} | {r.get('company','')} | {r['source']} | {hints} | [link]({r['url']}) |")
        (INBOX / f"referral-hunt--{ts}--v1.md").write_text("\n".join(lines))
        print(f"Wrote inbox/referral-hunt--{ts}--v1.md")

if __name__ == "__main__":
    main()
