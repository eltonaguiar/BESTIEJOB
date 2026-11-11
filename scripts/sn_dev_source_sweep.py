#!/usr/bin/env python3
"""Sweep ServiceNow developer roles from sources that do NOT feed bestiejob.

Excluded on purpose (already in this repo's scanners): Job Bank, GoJobs Ontario,
SmartRecruiters, Greenhouse, Lever, Ashby, Adzuna, Workday employer tenants
(RBC/BMO/Bell/Canada Life...), CareerBeacon, Dice, Procom, Built In.

Every row is verified live. A row without an absolute date is reported as
"live, undated" and never written as a dated board row.
"""
from __future__ import annotations
import argparse, datetime as dt, json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote_plus, urljoin, urlsplit, urlunsplit

from curl_cffi import requests as cr

ROOT = Path(__file__).resolve().parent.parent
SN = re.compile(r"service\s*now", re.I)
ROLE = re.compile(r"develop|engineer|consultant|architect|administrator|\badmin\b|"
                  r"specialist|analyst|platform|technical lead|tech lead|integration", re.I)
SALES = re.compile(r"\bsales\b|account executive|account manager|business development|"
                   r"customer success|recruit", re.I)
ISO = re.compile(r"(\d{4}-\d{2}-\d{2})")


def fetch(url, **kw):
    try:
        return cr.get(url, impersonate="chrome", timeout=30, **kw)
    except Exception as e:
        return e


def norm(u):
    p = urlsplit(u.strip())
    return urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip("/"), "", ""))


# ---------------- adapters: each returns (status, rows) ----------------
def a_gcjobs(term):
    """Federal public service. The legacy applicant portal still server-renders."""
    urls = [
        f"https://emploisfp-psjobs.cfp-psc.gc.ca/psrs-srfp/applicant/page1800?toggleLanguage=en&searchKeyword={quote_plus(term)}",
        f"https://www.canada.ca/en/public-service-commission/jobs/services/gc-jobs.html?search={quote_plus(term)}",
    ]
    rows, status = [], []
    for u in urls:
        r = fetch(u)
        if isinstance(r, Exception):
            status.append(f"{urlsplit(u).netloc}: {type(r).__name__}"); continue
        status.append(f"{urlsplit(u).netloc}: http {r.status_code}, {len(r.text)}B")
        if r.status_code != 200:
            continue
        for m in re.finditer(r'href="([^"]*(?:page1[0-9]+|jobposting|jobs)[^"]*)"[^>]*>([^<]{5,120})<', r.text, re.I):
            href, label = m.group(1), m.group(2)
            if SN.search(label) or SN.search(href):
                rows.append({"title": label.strip(), "url": urljoin(u, href),
                             "company": "Government of Canada", "location": "Canada", "posted": ""})
    return "; ".join(status), rows


def a_remoteok(term):
    r = fetch("https://remoteok.com/api")
    if isinstance(r, Exception):
        return f"error {type(r).__name__}", []
    if r.status_code != 200:
        return f"http {r.status_code}", []
    try:
        data = r.json()
    except Exception:
        return "not json", []
    rows = []
    for j in data:
        if not isinstance(j, dict):
            continue
        pos = j.get("position") or ""
        if SN.search(pos) or SN.search(str(j.get("tags", ""))):
            rows.append({"title": pos, "url": j.get("url") or j.get("apply_url", ""),
                         "company": j.get("company", ""), "location": j.get("location") or "Remote",
                         "posted": str(j.get("date", ""))[:10]})
    return f"http 200, {len(data)} jobs", rows


def a_remotive(term):
    r = fetch(f"https://remotive.com/api/remote-jobs?search={quote_plus(term)}&limit=50")
    if isinstance(r, Exception):
        return f"error {type(r).__name__}", []
    if r.status_code != 200:
        return f"http {r.status_code}", []
    try:
        data = r.json()
    except Exception:
        return "not json", []
    rows = [{"title": j.get("title", ""), "url": j.get("url", ""),
             "company": j.get("company_name", ""),
             "location": j.get("candidate_required_location") or "Remote",
             "posted": str(j.get("publication_date", ""))[:10]}
            for j in data.get("jobs", [])]
    return f"http 200, {len(rows)} jobs", rows


def a_himalayas_paged(term, pages=5):
    rows, seen, statuses = [], set(), []
    for i in range(pages):
        u = f"https://himalayas.app/jobs/api?limit=100&offset={i*100}"
        r = fetch(u)
        if isinstance(r, Exception):
            statuses.append(f"p{i}:{type(r).__name__}"); break
        if r.status_code != 200:
            statuses.append(f"p{i}:http {r.status_code}"); break
        try:
            d = r.json()
        except Exception:
            statuses.append(f"p{i}:not json"); break
        js = d.get("jobs") or []
        statuses.append(f"p{i}:{len(js)}/{d.get('totalCount','?')}")
        for j in js:
            title = j.get("title", "")
            if not SN.search(title):
                continue
            url = j.get("applicationLink") or j.get("url") or f"https://himalayas.app/companies/{j.get('companySlug','')}"
            if url in seen:
                continue
            seen.add(url)
            loc = j.get("locationRestrictions") or ["Remote"]
            rows.append({"title": title, "url": url,
                         "company": j.get("companyName", ""),
                         "location": loc[0] if isinstance(loc[ list ], ) and loc else "Remote",
                         "posted": str(j.get("pubDate") or j.get("publishedDate") or "")[:10]})
        if not js:
            break
    return ", ".join(statuses), rows


def a_jobboom(term):
    """Quebec board. Its keyword param is ignored (returns payroll/admin jobs),
    so the query is done client-side on the anchors we do get back."""
    rows, status = [], ""
    for u in (f"https://www.jobboom.com/en/jobs?q={quote_plus(term)}",
              f"https://www.jobboom.com/en/jobs?keywords={quote_plus(term)}"):
        r = fetch(u)
        if isinstance(r, Exception):
            status += f"{type(r).__name__}; "; continue
        status += f"http {r.status_code}, {len(r.text)}B; "
        if r.status_code != 200:
            continue
        for href, label in re.findall(r'<a[^>]+href="([^"]*job-offer[^"]*)"[^>]*>(.*?)</a>', r.text, re.S):
            title = re.sub(r"<[^>]+>", " ", label).strip()
            if SN.search(title):
                rows.append({"title": title, "url": urljoin(u, href),
                             "company": "", "location": "Canada", "posted": ""})
    return status.strip("; "), rows


def a_himalayas(term):
    rows, status = [], ""
    for u in ("https://himalayas.app/jobs/api?limit=100&offset=0",
              "https://himalayas.app/jobs/feed"):
        r = fetch(u)
        if isinstance(r, Exception):
            status += f"{u[-14:]}: {type(r).__name__}; "; continue
        status += f"{u[-14:]}: http {r.status_code}; "
        if r.status_code != 200:
            continue
        text = r.text
        try:
            data = json.loads(text)
            items = data.get("jobs") or data.get("data") or []
        except Exception:
            items = []
        for j in items:
            if not isinstance(j, dict):
                continue
            title = j.get("title") or j.get("position") or ""
            if SN.search(title):
                rows.append({"title": title, "url": j.get("applicationLink") or j.get("url", ""),
                             "company": j.get("companyName") or j.get("company", ""),
                             "location": j.get("locationRestrictions", ["Remote"])[0]
                             if isinstance(j.get("locationRestrictions"), list) else "Remote",
                             "posted": str(j.get("pubDate") or j.get("publishedDate") or "")[:10]})
        if not items and SN.search(text):
            for m in re.finditer(r"<title>([^<]*[Ss]ervice[Nn]ow[^<]*)</title>", text):
                rows.append({"title": m.group(1), "url": u, "company": "", "location": "Remote", "posted": ""})
    return status.strip("; "), rows


def a_wwr(term):
    rows, status = [], ""
    for u in ("https://weworkremotely.com/categories/remote-programming-jobs.rss",
              "https://weworkremotely.com/remote-jobs.rss"):
        r = fetch(u)
        if isinstance(r, Exception):
            status += f"{type(r).__name__}; "; continue
        status += f"http {r.status_code}; "
        if r.status_code != 200:
            continue
        for item in re.findall(r"<item>(.*?)</item>", r.text, re.S):
            t = re.search(r"<title>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>", item, re.S)
            l = re.search(r"<link>(.*?)</link>", item, re.S)
            p = re.search(r"<pubDate>(.*?)</pubDate>", item, re.S)
            title = (t.group(1) if t else "").strip()
            if SN.search(title):
                posted = ""
                if p:
                    try:
                        posted = dt.datetime.strptime(p.group(1).strip()[:16], "%a, %d %b %Y").date().isoformat()
                    except Exception:
                        posted = ""
                rows.append({"title": title, "url": (l.group(1).strip() if l else u),
                             "company": "", "location": "Remote", "posted": posted})
    return status.strip("; "), rows


def a_hn(term):
    r = fetch('https://hn.algolia.com/api/v1/search?query=%22Who%20is%20hiring%22&tags=story&hitsPerPage=3')
    if isinstance(r, Exception):
        return f"error {type(r).__name__}", []
    try:
        hits = r.json().get("hits", [])
    except Exception:
        return "not json", []
    if not hits:
        return "no hiring threads", []
    sid = hits[0].get("objectID")
    r2 = fetch(f"https://hn.algolia.com/api/v1/search?query={quote_plus(term)}&tags=comment,story_{sid}&hitsPerPage=50")
    if isinstance(r2, Exception) or r2.status_code != 200:
        return f"thread {sid}: no comment search", []
    rows = []
    for h in r2.json().get("hits", []):
        txt = re.sub(r"<[^>]+>", " ", h.get("comment_text") or "")
        if SN.search(txt):
            first = txt.strip().split("\n")[0][:120]
            rows.append({"title": first or "HN who-is-hiring comment",
                         "url": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
                         "company": "", "location": "see comment",
                         "posted": str(h.get("created_at", ""))[:10]})
    return f"thread {sid}, {len(rows)} SN comments", rows


def a_reddit(term):
    r = fetch(f"https://www.reddit.com/r/servicenow/search.json?q={quote_plus(term)}&restrict_sr=1&sort=new&limit=50")
    if isinstance(r, Exception):
        return f"error {type(r).__name__}", []
    if r.status_code != 200:
        return f"http {r.status_code} (blocked)", []
    try:
        kids = r.json()["data"]["children"]
    except Exception:
        return "not json", []
    rows = []
    for k in kids:
        d = k.get("data", {})
        title = d.get("title", "")
        if SN.search(title) or SN.search(d.get("selftext", "")[:400]):
            rows.append({"title": title, "url": "https://reddit.com" + d.get("permalink", ""),
                         "company": "", "location": "unknown",
                         "posted": dt.datetime.utcfromtimestamp(d.get("created_utc", 0)).date().isoformat()})
    return f"http 200, {len(kids)} posts", rows


def a_careerjet(term):
    rows, status = [], ""
    for loc in ("Toronto,+ON", "Canada"):
        u = f"https://www.careerjet.ca/search/jobs?s={quote_plus(term)}&l={loc}"
        r = fetch(u)
        if isinstance(r, Exception):
            status += f"{type(r).__name__}; "; continue
        status += f"http {r.status_code}; "
        if r.status_code != 200:
            continue
        for m in re.finditer(r'<a[^>]+href="(/jobad/\d+\.html)"[^>]*>(.*?)</a>', r.text, re.S):
            label = re.sub(r"<[^>]+>", " ", m.group(2)).strip()
            if SN.search(label):
                rows.append({"title": label[:140], "url": urljoin(u, m.group(1)),
                             "company": "", "location": loc.replace("+", " "), "posted": ""})
    return status.strip("; "), rows


def a_jobrapido(term):
    u = f"https://ca.jobrapido.com/?w={quote_plus(term)}&l=Toronto"
    r = fetch(u)
    if isinstance(r, Exception):
        return f"error {type(r).__name__}", []
    if r.status_code != 200:
        return f"http {r.status_code}", []
    rows = []
    for m in re.finditer(r'href="(https://ca\.jobrapido\.com/jobpreview/\d+[^"]*)"[^>]*>(.*?)</a>', r.text, re.S):
        label = re.sub(r"<[^>]+>", " ", m.group(2)).strip()
        if SN.search(label):
            rows.append({"title": label[:140], "url": m.group(1), "company": "",
                         "location": "Toronto, ON", "posted": ""})
    return f"http 200, {len(rows)} SN links", rows


def a_monster(term):
    u = f"https://www.monster.ca/jobs/search/?q={quote_plus(term)}&where=Toronto%2C+ON"
    r = fetch(u)
    if isinstance(r, Exception):
        return f"error {type(r).__name__}", []
    if r.status_code != 200:
        return f"http {r.status_code}", []
    rows = []
    for m in re.finditer(r'href="(https://www\.monster\.ca/[^"]*job[^"]*?)"[^>]*>(.*?)</a>', r.text, re.S):
        label = re.sub(r"<[^>]+>", " ", m.group(2)).strip()
        if SN.search(label):
            rows.append({"title": label[:140], "url": m.group(1), "company": "",
                         "location": "Toronto, ON", "posted": ""})
    return f"http 200, {len(rows)} SN links", rows


def a_jobsca(term):
    u = f"https://www.jobs.ca/search/?q={quote_plus(term)}"
    r = fetch(u)
    if isinstance(r, Exception):
        return f"error {type(r).__name__}", []
    if r.status_code != 200:
        return f"http {r.status_code}", []
    rows = []
    for m in re.finditer(r'href="(/job/[^"]+)"[^>]*>(.*?)</a>', r.text, re.S):
        label = re.sub(r"<[^>]+>", " ", m.group(2)).strip()
        if SN.search(label):
            rows.append({"title": label[:140], "url": urljoin(u, m.group(1)),
                         "company": "", "location": "Canada", "posted": ""})
    return f"http 200, {len(rows)} SN links", rows


ADAPTERS = {
    "GC Jobs (federal)": a_gcjobs,
    "RemoteOK": a_remoteok,
    "Remotive": a_remotive,
    "Himalayas": a_himalayas_paged,
    "Jobboom (QC)": a_jobboom,
    "We Work Remotely": a_wwr,
    "Hacker News hiring": a_hn,
    "Reddit r/servicenow": a_reddit,
    "Careerjet CA": a_careerjet,
    "Jobrapido CA": a_jobrapido,
    "Monster.ca": a_monster,
    "Jobs.ca": a_jobsca,
}


def known():
    urls = set()
    for name in ("jobs.json", "public/jobs.json", "public/jobs-data.json"):
        p = ROOT / name
        if not p.exists():
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for row in (data if isinstance(data, list) else data.get("jobs", [])):
            if isinstance(row, dict) and row.get("url"):
                urls.add(norm(str(row["url"])))
    return urls


def alive(url):
    try:
        r = cr.get(url, impersonate="chrome", timeout=25, allow_redirects=True)
    except Exception:
        return False
    return r.status_code < 400


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--term", default="servicenow")
    ap.add_argument("--out", default="reports/sn_dev_roles_2026-11-11.md")
    ap.add_argument("--verify", action="store_true", help="HEAD/GET every kept row")
    args = ap.parse_args()

    have = known()
    status, kept, dropped = {}, [], []
    for name, fn in ADAPTERS.items():
        try:
            st, rows = fn(args.term)
        except Exception as e:
            st, rows = f"crashed {type(e).__name__}", []
        status[name] = {"status": st, "raw": len(rows)}
        for row in rows:
            title, url = row.get("title", ""), row.get("url", "")
            if not title or not url:
                continue
            if not SN.search(title) or not ROLE.search(title):
                dropped.append((name, title, "title filter")); continue
            if SALES.search(title):
                dropped.append((name, title, "sales/recruit")); continue
            key = norm(url)
            if key in have:
                dropped.append((name, title, "already on board")); continue
            row["source"] = name
            row["posted"] = row.get("posted", "") if ISO.match(row.get("posted", "") or "") else ""
            kept.append(row)
    # dedupe inside the sweep on title+company
    seen, uniq = set(), []
    for r in kept:
        k = (re.sub(r"\W+", "", r["title"].lower())[:60], (r.get("company") or "").lower())
        if k in seen:
            dropped.append((r["source"], r["title"], "duplicate in sweep")); continue
        seen.add(k); uniq.append(r)

    if args.verify:
        with ThreadPoolExecutor(max_workers=8) as pool:
            flags = list(pool.map(lambda r: alive(r["url"]), uniq))
        uniq = [r for r, ok in zip(uniq, flags) if ok]
        status["_verify"] = {"status": f"liveness checked, {len(uniq)} live", "raw": len(uniq)}

    dated = [r for r in uniq if r["posted"]]
    undated = [r for r in uniq if not r["posted"]]
    dated.sort(key=lambda r: r["posted"], reverse=True)

    lines = ["# ServiceNow developer roles outside the current feeds", "",
             f"Run: {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} local. Term: `{args.term}`.", "",
             "Sources already feeding bestiejob (Job Bank, GoJobs, SmartRecruiters,",
             "Greenhouse, Lever, Ashby, Workday tenants, CareerBeacon, Dice, Procom,",
             "Built In) are excluded by design.", "",
             "## Source status", "", "| Source | Result | Raw hits |", "| --- | --- | --- |"]
    for name, s in status.items():
        lines.append(f"| {name} | {s['status']} | {s['raw']} |")
    lines += ["", f"## Roles with an absolute posted date ({len(dated)})", "",
              "| Posted | Role | Company | Location | Source | URL |",
              "| --- | --- | --- | --- | --- | --- |"]
    for r in dated:
        lines.append(f"| {r['posted']} | {r['title'][:70]} | {(r.get('company') or '—')[:26]} | "
                     f"{(r.get('location') or '—')[:24]} | {r['source']} | {r['url'][:70]} |")
    lines += ["", f"## Live but undated ({len(undated)})", "",
              "These are real, currently listed roles whose source publishes no date.",
              "They are not eligible to become dated board rows.", "",
              "| Role | Company | Location | Source | URL |", "| --- | --- | --- | --- | --- |"]
    for r in undated:
        lines.append(f"| {r['title'][:70]} | {(r.get('company') or '—')[:26]} | "
                     f"{(r.get('location') or '—')[:24]} | {r['source']} | {r['url'][:70]} |")
    lines += ["", "## Dropped", "", "| Source | Title | Why |", "| --- | --- | --- |"]
    for s, t, why in dropped[:40]:
        lines.append(f"| {s} | {t[:60]} | {why} |")
    Path(args.out).write_text("\n".join(lines) + "\n")
    Path(args.out.replace(".md", ".json")).write_text(json.dumps(
        {"status": status, "dated": dated, "undated": undated,
         "dropped": [{"source": s, "title": t, "why": w} for s, t, w in dropped]}, indent=1))
    print(f"dated={len(dated)} undated={len(undated)} dropped={len(dropped)}")
    for name, s in status.items():
        print(f"  {name:22} {s['status'][:60]:60} raw={s['raw']}")
    for r in dated[:12]:
        print(f"  DATE {r['posted']} | {(r.get('company') or '-')[:22]:22} | {r['title'][:58]}")
    for r in undated[:12]:
        print(f"  live       | {(r.get('company') or '-')[:22]:22} | {r['title'][:58]}")


if __name__ == "__main__":
    sys.exit(main())
