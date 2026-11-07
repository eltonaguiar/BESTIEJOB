#!/usr/bin/env python3
"""Referral-field hunter v2 - incremental, ATS-focused, saves progress."""
import json, os, re, sys, time, random
from datetime import datetime, timezone
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
JOBS = ROOT / "jobs.json"
RAW = ROOT / "raw"; INBOX = ROOT / "inbox"
RAW.mkdir(exist_ok=True); INBOX.mkdir(exist_ok=True)

UAS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/17.4 Safari/605.1.15",
]
REFERRAL_PATTERNS = [
    r"referred?\s+by", r"referr(al|er)\b", r"employee\s+referr",
    r"how\s+did\s+you\s+hear", r"referral[_\-]?(code|id|source|name)",
    r'\bref[_\-]?code\b', r'name=["\']referr', r'placeholder=["\'][^"\']*referr',
]

def extract_hints(html):
    if not html: return []
    hints, seen = [], set()
    low = html.lower()
    for pat in REFERRAL_PATTERNS:
        for m in re.finditer(pat, low[:300000]):
            s = max(0,m.start()-60); e = min(len(html), m.end()+100)
            snip = re.sub(r'<[^>]+>',' ', html[s:e])
            snip = re.sub(r'\s+',' ', snip).strip()[:180]
            k = snip[:50]
            if k not in seen: seen.add(k); hints.append({"pattern":pat,"snippet":snip})
    for m in re.finditer(r'<(input|select)[^>]*(?:name|id)=["\'][^"\']*referr[^"\']*["\'][^>]*>', low):
        hints.append({"pattern":"form_field","snippet":m.group(0)[:160]})
    return hints[:8]

def fetch(url, session):
    try:
        r = session.get(url, headers={"User-Agent":random.choice(UAS),"Accept":"text/html,*/*"}, timeout=15, allow_redirects=True)
        return (r.text, "ok") if r.status_code==200 else (None, f"http_{r.status_code}")
    except Exception as e:
        return None, type(e).__name__

def main():
    max_jobs = int(os.environ.get("MAX_JOBS","50"))
    ats_only = os.environ.get("ATS_ONLY","1")=="1"
    data = json.load(open(JOBS))
    jobs = data.get("jobs", data) if isinstance(data, dict) else data
    ats = {"workday","greenhouse","lever","ashby","smartrecruiters","icims"}
    def pri(j):
        t=(j.get("title","")+"").lower(); s=0
        if any(x in t for x in ["servicenow","itsm","itam","cmdb"]): s+=10
        if any(x in t for x in ["salesforce","apex","lwc"]): s+=8
        if j.get("source") in ats: s+=5
        return -s
    jobs = sorted(jobs, key=pri)
    if ats_only: jobs = [j for j in jobs if j.get("source") in ats]
    jobs = [j for j in jobs if j.get("url") and "adzuna.com" not in j["url"]][:max_jobs]

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = RAW / f"referral_hunt_{ts}.json"
    results, stats = [], {"checked":0,"ok":0,"hits":0,"errors":0}
    session = requests.Session()
    for j in jobs:
        stats["checked"]+=1
        html, st = fetch(j["url"], session)
        if html:
            stats["ok"]+=1
            hints = extract_hints(html)
            if hints:
                stats["hits"]+=1
                results.append({"title":j.get("title"),"company":j.get("company"),
                    "url":j["url"],"source":j.get("source"),"hints":hints})
                print(f"[HIT] {j.get('title','')[:55]} ({len(hints)})")
            else:
                print(f"[--] {j.get('title','')[:55]}")
        else:
            stats["errors"]+=1; print(f"[ERR] {j.get('title','')[:55]} {st}")
        # save incrementally
        out_path.write_text(json.dumps({"scanned_at":ts,"stats":stats,"results":results},indent=2))
        time.sleep(random.uniform(1.0,2.0))
    print(f"\nDone. {stats}")
    if results:
        lines=["---",f"date: {ts}","type: referral-hunt","---","","# Referral Hunt","","",
               "| Role | Company | Source | Patterns | URL |","|---|---|---|---|---|"]
        for r in results[:80]:
            pats=", ".join(sorted(set(h["pattern"] for h in r["hints"])))[:55]
            lines.append(f"| {(r['title'] or '')[:60]} | {(r.get('company') or '')[:30]} | {r['source']} | {pats} | [link]({r['url']}) |")
        (INBOX/f"referral-hunt--{ts}--v1.md").write_text("\n".join(lines))

if __name__=="__main__": main()
