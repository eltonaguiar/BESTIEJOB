#!/usr/bin/env python3
"""Canadian index sweep: Eluta.ca and Job Bank.

Both are server-rendered Canadian indexes that the ATS sweep does not touch.
They matter because they index employers whose ATS tenant we have never
discovered -- Eluta crawls corporate career sites directly and even exposes the
origin host in its "last seen" link (`enavOpenNew('cache?u=...:smartrecruiters.com')`),
so a sweep doubles as an ATS-discovery oracle.

Everything here comes from the page: title, employer, location, and a
source-shown date. Eluta shows relative dates ("today", "6 days ago") which are
converted against the run date; Job Bank shows absolute dates ("October 21,
2026"). A row with no parseable date is dropped, never invented.

    python3 scripts/canada_index_sweep.py --bucket servicenow --bucket salesforce
    python3 scripts/canada_index_sweep.py --eluta-pages 6 --jobbank-pages 4 --verify 0

Outputs
    reports/canada_index_<date>.json     machine-readable rows + source stats
    inbox/canada-index--<date>--v1.md    6-column submission table
"""
from __future__ import annotations

import argparse
import html as htmllib
import json
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INBOX = ROOT / "inbox"
OUT = ROOT / "reports"
NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y-%m-%d")
TODAY = NOW.date()

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# Title-only matching, same policy as bucket_rounds.py: a body match on
# "Salesforce" would pull in every admin job at a company that merely uses it.
KW = {
    "salesforce": re.compile(
        r"\bsalesforce\b|\bapex\b|\bsoql\b|\blwc\b|\blightning web\b|\bvisualforce\b|"
        r"\bmarketing cloud\b|\bservice cloud\b|\bsales cloud\b|\bdata cloud\b|"
        r"\bagentforce\b|\bcpq\b|\brevenue cloud\b|\bmulesoft\b|\beinstein\b|"
        r"\bcopado\b|\bfsc\b|\bfinancial services cloud\b|\bsfdc\b|\bsf\s?cc\b",
        re.I,
    ),
    "servicenow": re.compile(
        r"\bservice\s?now\b|\bcsdm\b|\bcmdb\b|\bitsm\b|\bitom\b|\bitam\b|"
        r"\bnow assist\b|\bvirtual agent\b|\bmid server\b|\bflow designer\b|"
        r"\bsecops\b|\bservice mapping\b|\bhrit\b|\bspm\b",
        re.I,
    ),
}

# Titles that mention the platform but are not platform work.
REJECT = re.compile(
    r"\b(sales|account|business development|bdr|sdr)\s+(executive|manager|director|rep|representative)\b|"
    r"\b(vp|vice president|head|director|chief)\b|"
    r"\brecruiter|\btalent acquisition\b|\bmarketing manager\b|"
    r"\bhelp ?desk\b|\bdesktop support\b|\bbusiness continuity\b|\bbim\b|"
    # "Apex" is a game, a clinic, and an Oracle product before it is Salesforce Apex.
    r"\bapex legends\b|\boracle apex\b|\bacupunctu|\bkinatex\b|"
    r"\bcustomer success manager\b|\balliance\b|"
    # Co-op, internship and trainee reqs are not senior platform work.
    r"\bstage\b|\bcoop\b|\bco-op\b|\bintern\b|\binternship\b|\bstagiaire\b|\btrainee\b|"
    # People-management reqs, English and French. Leads and architects stay.
    r"\b(senior |sr\.? )?manager\b|\bdelivery mgr\b|\bdirecteur\.?rice fonctionnel|"
    r"\bresponsable fonctionnel|\bchef d.équipe\b",
    re.I,
)

CA_MARKERS = re.compile(
    r"\b(ON|QC|BC|AB|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b|"
    r"canada|toronto|mississauga|brampton|markham|vaughan|richmond hill|"
    r"scarborough|etobicoke|north york|oakville|hamilton|ottawa|montreal|"
    r"montréal|laval|quebec|québec|gatineau|calgary|edmonton|winnipeg|"
    r"vancouver|victoria|burnaby|surrey|saskatoon|regina|halifax|"
    r"st\.? john|moncton|fredericton|charlottetown|whitehorse|yellowknife|"
    r"anywhere in canada|remote \(canada\)|canada only",
    re.I,
)
US_ONLY = re.compile(
    r"\b(alabama|alaska|arizona|arkansas|california|colorado|delaware|florida|"
    r"georgia|hawaii|idaho|illinois|indiana|iowa|kansas|kentucky|louisiana|"
    r"maine|maryland|massachusetts|michigan|minnesota|mississippi|missouri|"
    r"montana|nebraska|nevada|new hampshire|new jersey|new mexico|new york|"
    r"north carolina|north dakota|ohio|oklahoma|oregon|pennsylvania|"
    r"rhode island|south carolina|south dakota|tennessee|texas|utah|vermont|"
    r"virginia|washington|west virginia|wisconsin|wyoming)\b|"
    r"\b(united states|usa|u\.s\.)\b",
    re.I,
)


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------
def fetch(url: str, timeout: int = 30) -> str | None:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-CA,en;q=0.9",
        },
    )
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < 3:
                time.sleep(6 * (attempt + 1))
                continue
            break
        except Exception:
            # Job Bank intermittently drops the connection when a sweep hits it
            # in bursts; one empty page is not evidence that the source is dead.
            if attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            break

    # Fallback: some hosts fingerprint urllib's TLS/HTTP stack and reset the
    # connection while serving the very same URL to curl without complaint.
    try:
        out = subprocess.run(
            ["curl", "-s", "--compressed", "--max-time", str(timeout), "-A", UA,
             "-H", "Accept-Language: en-CA,en;q=0.9", url],
            capture_output=True,
            timeout=timeout + 10,
        )
        if out.returncode == 0 and len(out.stdout) > 2000:
            return out.stdout.decode("utf-8", "ignore")
    except Exception:
        pass
    return None


def text(fragment: str) -> str:
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def relative_date(phrase: str) -> str | None:
    p = phrase.strip().lower()
    if p in ("today", "just posted", "new"):
        d = TODAY
    elif p.startswith("yesterday"):
        d = TODAY - timedelta(days=1)
    else:
        m = re.search(r"(\d+)\+?\s*(day|days|hour|hours|week|weeks)\s*ago", p)
        if not m:
            return None
        n = int(m.group(1))
        unit = m.group(2)
        if unit.startswith("hour"):
            d = TODAY
        elif unit.startswith("week"):
            d = TODAY - timedelta(days=7 * n)
        else:
            d = TODAY - timedelta(days=n)
    return d.isoformat()


def canada(location: str) -> bool:
    if not location:
        return False
    if CA_MARKERS.search(location):
        return True
    if re.search(r"\bremote\b", location, re.I) and not US_ONLY.search(location):
        return True
    return False


def title_ok(title: str, bucket: str) -> bool:
    if not KW[bucket].search(title):
        return False
    if REJECT.search(title):
        return False
    return True


# ---------------------------------------------------------------------------
# Eluta.ca
# ---------------------------------------------------------------------------
ELUTA_BLOCK = re.compile(r'<div data-url="(spl/[^"]+)"\s*\n?\s*class="organic-job', re.S)
ELUTA_TITLE = re.compile(r'class="lk-job-title".*?title="([^"]+)"', re.S)
ELUTA_EMPLOYER = re.compile(r'class="employer lk-employer".*?>([^<]{1,120})</a>', re.S)
ELUTA_LOCATION = re.compile(r'<span class="location">(.*?)</span>\s*(?:<span class="description">|<a class="lk lastseen")', re.S)
ELUTA_SEEN = re.compile(r'class="lk lastseen"[^>]*>\s*([^<]{1,40}?)\s*</a>', re.S)
ELUTA_ORIGIN = re.compile(r"cache\?u=\d+:([a-z0-9.\-]+\.[a-z]{2,})", re.I)


def eluta_page(keyword: str, page: int) -> tuple[list[dict], list[str]]:
    """Return (rows, origin_domains) for one Eluta search page."""
    url = f"https://www.eluta.ca/search?q={urllib.parse.quote_plus(keyword)}&pg={page}"
    body = fetch(url)
    if not body:
        return [], []

    rows: list[dict] = []
    origins: list[str] = []
    starts = [m.start() for m in ELUTA_BLOCK.finditer(body)]
    for i, start in enumerate(starts):
        end = starts[i + 1] if i + 1 < len(starts) else start + 6000
        block = body[start:end]

        slug = ELUTA_BLOCK.match(block).group(1).split("?")[0]
        title_m = ELUTA_TITLE.search(block)
        employer_m = ELUTA_EMPLOYER.search(block)
        location_m = ELUTA_LOCATION.search(block)
        seen_m = ELUTA_SEEN.search(block)
        origin_m = ELUTA_ORIGIN.search(block)

        if not (title_m and employer_m and seen_m):
            continue
        posted = relative_date(seen_m.group(1))
        if not posted:
            continue

        location = text(location_m.group(1)) if location_m else ""
        location = re.sub(r"\s*-\s*Work Remotely\s*$", " (remote)", location).strip()

        if origin_m:
            origins.append(origin_m.group(1).lower())

        rows.append(
            {
                "source": "eluta",
                "title": text(title_m.group(1)),
                "company": text(employer_m.group(1)),
                "location": location or "Canada",
                "posted": posted,
                "url": f"https://www.eluta.ca/{slug}",
                "origin_ats": origin_m.group(1).lower() if origin_m else "",
            }
        )
    return rows, origins


# ---------------------------------------------------------------------------
# Job Bank
# ---------------------------------------------------------------------------
JB_ARTICLE = re.compile(r'<article id="article-(\d+)".*?</article>', re.S)


def jobbank_page(keyword: str, page: int) -> list[dict]:
    url = (
        "https://www.jobbank.gc.ca/jobsearch/jobsearch"
        f"?searchstring={urllib.parse.quote_plus(keyword)}&sort=D&page={page}"
    )
    body = ""
    for _ in range(3):
        body = fetch(url) or ""
        if '<article id="article-' in body:
            break
        time.sleep(4)
    if not body:
        return []

    rows: list[dict] = []
    for m in JB_ARTICLE.finditer(body):
        block = m.group(0)
        title_m = re.search(r'<span class="noctitle">(.*?)</span>', block, re.S)
        date_m = re.search(r'<li class="date">(.*?)</li>', block, re.S)
        biz_m = re.search(r'<li class="business">(.*?)</li>', block, re.S)
        loc_m = re.search(r'<li class="location">(.*?)</li>', block, re.S)
        if not (title_m and date_m and biz_m):
            continue
        try:
            posted = datetime.strptime(text(date_m.group(1)), "%B %d, %Y").date()
        except ValueError:
            continue
        if posted < (TODAY - timedelta(days=45)):
            continue

        location = text(loc_m.group(1)) if loc_m else "Canada"
        location = re.sub(r"^\s*Location\s*", "", location).strip()

        rows.append(
            {
                "source": "jobbank",
                "title": text(title_m.group(1)),
                "company": text(biz_m.group(1)),
                "location": location or "Canada",
                "posted": posted.isoformat(),
                "url": f"https://www.jobbank.gc.ca/jobsearch/jobposting/{m.group(1)}",
                "origin_ats": "jobbank.gc.ca",
            }
        )
    return rows


# ---------------------------------------------------------------------------
# Dedup baseline: README links + jobs.json urls + LinkedIn numeric ids
# ---------------------------------------------------------------------------
LEGAL_SUFFIX = re.compile(
    r"\b(llp|inc|incorporated|ltd|limited|ulc|corp|corporation|company|co|group|canada|plc|sa|gmbh|pte)\b",
    re.I,
)


def norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def identity_key(company: str, role: str) -> str:
    """Company+role fingerprint, legal suffixes ignored.

    The same requisition reaches Eluta under two slugs and reaches the board via
    a different ATS URL, so URL-only dedupe is not enough.
    """
    return f"{norm(LEGAL_SUFFIX.sub(' ', company))}|{norm(role)}"


def city_key(location: str) -> str:
    m = re.match(r"\s*([^,()]+)", location or "")
    return norm(m.group(1)) if m else ""


def same_city(board_cities: set[str], city: str) -> bool:
    """Board rows mix "Toronto", "Toronto, Ontario, ca" and "5 locations".

    Comparing normalized city strings for equality misses every one of those,
    which is how 44 already-published rows nearly got resubmitted once.
    """
    if not city:
        return True
    for board_city in board_cities:
        if not board_city or board_city in ("canada", "5 locations", "various", "multiple"):
            return True
        if board_city in city or city in board_city:
            return True
    return False


def baseline_urls() -> tuple[set[str], set[str], dict[str, set[str]]]:
    urls: set[str] = set()
    ids: set[str] = set()
    board_ids: dict[str, set[str]] = {}

    readme = ROOT / "README.md"
    if readme.exists():
        for m in re.finditer(r"\]\((https?://[^)\s]+)\)", readme.read_text(encoding="utf-8", errors="ignore")):
            urls.add(m.group(1).rstrip("/"))

    jobs = ROOT / "jobs.json"
    if jobs.exists():
        try:
            data = json.loads(jobs.read_text(encoding="utf-8"))
            for j in (data.get("jobs", data) if isinstance(data, dict) else data):
                if isinstance(j, dict) and j.get("url"):
                    urls.add(str(j["url"]).rstrip("/"))
        except Exception:
            pass

    for u in urls:
        for m in re.finditer(r"/jobs/view/(?:[^/]*?-)?(\d{6,})", u):
            ids.add(m.group(1))

    # Role/company fingerprints from the published table.
    if readme.exists():
        for line in readme.read_text(encoding="utf-8", errors="ignore").splitlines():
            if not line.startswith("| ") or line.startswith("| Posted") or line.startswith("|---"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4:
                continue
            role = re.sub(r"\]\([^)]*\)", "]", cells[1]).strip("[] ")
            if not role:
                continue
            board_ids.setdefault(identity_key(cells[2], role), set()).add(city_key(cells[3]))

    return urls, ids, board_ids


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bucket", action="append", choices=sorted(KW), default=None)
    ap.add_argument("--keywords", default="", help="extra space-separated search keywords")
    ap.add_argument("--eluta-pages", type=int, default=4)
    ap.add_argument("--jobbank-pages", type=int, default=2)
    ap.add_argument("--verify", type=int, default=1, help="1 = GET each URL, drop non-200")
    ap.add_argument("--out-inbox", default="")
    args = ap.parse_args()

    buckets = args.bucket or ["servicenow", "salesforce"]
    keywords = list(buckets) + [k for k in args.keywords.split() if k]

    seen_urls, seen_ids, board_ids = baseline_urls()
    identities: set[str] = set()
    all_rows: list[dict] = []
    origins: dict[str, int] = {}
    stats = {"eluta_pages": 0, "jobbank_pages": 0, "requests": 0}

    for kw in keywords:
        for page in range(1, args.eluta_pages + 1):
            rows, page_origins = eluta_page(kw, page)
            stats["requests"] += 1
            stats["eluta_pages"] += 1
            for o in page_origins:
                origins[o] = origins.get(o, 0) + 1
            if not rows and page > 1:
                break
            all_rows.extend(rows)
            time.sleep(1.2)
        for page in range(1, args.jobbank_pages + 1):
            rows = jobbank_page(kw, page)
            stats["requests"] += 1
            stats["jobbank_pages"] += 1
            if not rows and page > 1:
                break
            all_rows.extend(rows)
            time.sleep(1.2)

    # dedupe within the batch, then filter to title/geo/bucket rules
    kept: dict[str, dict] = {}
    dropped = {"dup_board": 0, "dup_batch": 0, "title": 0, "geo": 0, "dead": 0}
    for row in all_rows:
        url = row["url"].rstrip("/")
        if url in seen_urls or any(i in url for i in seen_ids):
            dropped["dup_board"] += 1
            continue
        key = identity_key(row["company"], row["title"])
        city = city_key(row["location"])
        if key in board_ids and same_city(board_ids[key], city):
            dropped["dup_board"] += 1
            continue
        # Eluta sometimes indexes the same requisition under two slugs; compare
        # the identity, not just the URL.
        identity = re.sub(
            r"[^a-z0-9]+", " ", f"{row['company']} {row['title']} {row['location']}".lower()
        ).strip()
        if url in kept or identity in identities:
            dropped["dup_batch"] += 1
            continue
        identities.add(identity)
        bucket = next((b for b in buckets if title_ok(row["title"], b)), None)
        if not bucket:
            dropped["title"] += 1
            continue
        if not canada(row["location"]):
            dropped["geo"] += 1
            continue
        row["bucket"] = bucket
        kept[url] = row

    if args.verify:
        for url, row in list(kept.items()):
            if not fetch(url, timeout=20):
                dropped["dead"] += 1
                kept.pop(url)
            time.sleep(0.4)

    rows = sorted(kept.values(), key=lambda r: (r["posted"], r["company"]), reverse=True)

    OUT.mkdir(exist_ok=True)
    (OUT / f"canada_index_{STAMP}.json").write_text(
        json.dumps(
            {
                "generated": NOW.isoformat(),
                "buckets": buckets,
                "keywords": keywords,
                "stats": stats,
                "origin_ats": dict(sorted(origins.items(), key=lambda kv: -kv[1])),
                "dropped": dropped,
                "rows": rows,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    INBOX.mkdir(exist_ok=True)
    inbox = Path(args.out_inbox) if args.out_inbox else INBOX / f"canada-index--{STAMP}--v1.md"
    lines = [
        f"# Eluta / Job Bank sweep — {STAMP}",
        "",
        f"Sources: eluta.ca ({stats['eluta_pages']} pages), jobbank.gc.ca "
        f"({stats['jobbank_pages']} pages). Buckets: {', '.join(buckets)}.",
        "",
        "| Posted | Role | Company | Location | URL | Note |",
        "|--------|------|---------|----------|-----|------|",
    ]
    for r in rows:
        note = f"{r['source']}; origin {r['origin_ats']}" if r["origin_ats"] else r["source"]
        safe = lambda s: str(s).replace("|", "/")
        lines.append(
            f"| {r['posted']} | {safe(r['title'])} | {safe(r['company'])} | "
            f"{safe(r['location'])} | {r['url']} | {safe(note)} |"
        )
    inbox.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"fetched {len(all_rows)} raw rows from {stats['requests']} pages")
    print(f"kept {len(rows)}  dropped {dropped}")
    print("origin ATS:", ", ".join(f"{k}={v}" for k, v in list(sorted(origins.items(), key=lambda kv: -kv[1]))[:10]))
    print("inbox:", inbox)
    for r in rows[:15]:
        print(f"  {r['posted']}  [{r['bucket']}] {r['company'][:28]:28} {r['title'][:52]:52} {r['location'][:26]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
