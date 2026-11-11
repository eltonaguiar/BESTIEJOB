#!/usr/bin/env python3
"""search_engines.py — find out which search engines this box can actually read.

`web_search_scan.py` already wraps the paid document-search APIs (Tavily, Exa,
Firecrawl) and the Brave API, which costs a credit per query. Job discovery only
sees what those indexes return, so the question this module answers is: which
*additional* engines can be scraped from here, at no per-query cost, and do their
results contain postings rather than listing hubs?

Two modes:

    python3 scripts/search_engines.py probe            # every engine, one query
    python3 scripts/search_engines.py probe --query "servicenow toronto"
    python3 scripts/search_engines.py scan --query "servicenow toronto" --out raw/search_rows.json

The probe reports, per engine: HTTP status, result count, how many results look
like individual postings, and how many are aggregator listing pages (the thing
that made a 2026-11-04 pass spend 100 credits for zero rows). A blocked or
JS-only engine reports that too — knowing it is blocked is the useful answer.

Engines that need a key (Brave, OpenRouter, Perplexity, Kagi) read it from the
environment or `~/dbpasses.txt`; without one they self-report as `no-key` and are
skipped, never guessed at.
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEYS = Path.home() / "dbpasses.txt"
TIMEOUT = 25
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# A result is a posting if it looks like one *and* sits on a host that hosts
# individual postings rather than a search page.
JOBISH = re.compile(
    r"\b(servicenow|service now|salesforce|sfdc|apex|lwc|itsm|itam|cmdb|itom|"
    r"hrsd|agentforce|marketing cloud)\b", re.I)
LISTING = re.compile(
    r"[?&](q|query|k|keyword|keywords|search|what|jobtitle)=|"
    r"/(jobs?|jobsearch|job-search|search|careers?|opportunities)/?$|"
    r"linkedin\.com/jobs/(search|collections)|indeed\.[a-z.]+/(q|jobs)\b|"
    r"linkedin\.com/jobs/[a-z0-9-]+-jobs-|glassdoor\.[a-z.]+/Job/.*-jobs-|"
    r"/[a-z0-9-]+-jobs-(?:in-)?[a-z]|/jobs-[a-z0-9-]+/|ziprecruiter\.[a-z.]+/Jobs/|"
    r"talent\.com/view/|jobs\.ca/(?:q-|jobs\?)|jobbank\.gc\.ca/search|"
    r"jobbank\.gc\.ca/(findajob|jobsearch)", re.I)
LOCALE = re.compile(r"/[a-z]{2}[-_][A-Za-z]{2}/")


def _secret(*names: str) -> str | None:
    for name in names:
        val = (__import__("os").environ.get(name) or "").strip()
        if val:
            return val
    if not KEYS.exists():
        return None
    lines = KEYS.read_text(encoding="utf-8", errors="replace").splitlines()
    wanted = {n.lower().replace("_", "") for n in names}
    for line in lines:
        head, sep, tail = line.partition(":")
        if not sep:
            head, sep, tail = line.partition("=")
        if not sep:
            continue
        if head.lower().replace("_", "").replace(" ", "") in wanted:
            cand = tail.strip().strip('"').strip("'")
            if cand:
                return cand
    return None


def _get(url: str, *, headers: dict | None = None, data: bytes | None = None,
         timeout: int = TIMEOUT) -> tuple[int, str]:
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-CA,en;q=0.9", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read(2_500_000).decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read(400_000).decode("utf-8", "replace")
    except Exception as exc:                              # noqa: BLE001
        return 0, f"ERR:{type(exc).__name__}:{str(exc)[:120]}"


def _text(html: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()


def _ddg_url(href: str) -> str:
    """DuckDuckGo wraps results in /l/?uddg=<encoded>."""
    if "uddg=" in href:
        q = urllib.parse.urlparse(href).query
        return urllib.parse.parse_qs(q).get("uddg", [href])[0]
    if href.startswith("//"):
        return "https:" + href
    return href


def _bing_url(href: str) -> str:
    """Bing returns /ck/a?...&u=a1<base64url of the target> instead of the URL."""
    href = href.replace("&amp;", "&")
    if "bing.com/ck/a" not in href:
        return href
    token = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("u", [""])[0]
    if not token.startswith("a1"):
        return href
    body = token[2:] + "=" * (-len(token[2:]) % 4)
    try:
        target = base64.urlsafe_b64decode(body).decode("utf-8", "replace")
    except Exception:                                     # noqa: BLE001
        return href
    return target if target.startswith("http") else href


ENGINES: dict[str, callable] = {}


def engine(name):
    def wrap(fn):
        ENGINES[name] = fn
        return fn
    return wrap


# --------------------------------------------------------------------------- #
# no-key HTML engines

_LAST_DDG = [0.0]


@engine("duckduckgo")
def duckduckgo(query: str, limit: int = 20):
    """HTML endpoint. Rate-limits hard: after ~30 queries in a few minutes it
    answers 200 with a challenge page and zero results, so calls are spaced and
    one empty answer is retried after a pause rather than read as "no jobs"."""
    import time as _time
    gap = _time.time() - _LAST_DDG[0]
    if gap < 4:
        _time.sleep(4 - gap)
    _LAST_DDG[0] = _time.time()
    body = urllib.parse.urlencode({"q": query, "kl": "ca-en"}).encode()
    status, html = _get("https://html.duckduckgo.com/html/", data=body,
                        headers={"Content-Type": "application/x-www-form-urlencoded"})
    out = []
    for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
        href, title = _ddg_url(m.group(1)), _text(m.group(2))
        if href.startswith("http") and title:
            out.append({"title": title, "url": href, "snippet": "", "engine": "duckduckgo"})
    snippets = [_text(s) for s in re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.S)]
    for row, snip in zip(out, snippets):
        row["snippet"] = snip
    if not out:
        _time.sleep(8)
        status, html = _get("https://html.duckduckgo.com/html/", data=body,
                            headers={"Content-Type": "application/x-www-form-urlencoded"})
        for m in re.finditer(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
            href, title = _ddg_url(m.group(1)), _text(m.group(2))
            if href.startswith("http") and title:
                out.append({"title": title, "url": href, "snippet": "", "engine": "duckduckgo"})
    return status, out[:limit]


@engine("bing")
def bing(query: str, limit: int = 20):
    url = ("https://www.bing.com/search?q=" + urllib.parse.quote(query)
           + f"&count={limit}&setlang=en-CA&cc=CA")
    status, html = _get(url)
    out = []
    for block in re.findall(r'<li class="b_algo".*?</li>', html, re.S):
        m = re.search(r'<h2><a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block, re.S)
        if not m:
            continue
        snip = re.search(r"<p[^>]*>(.*?)</p>", block, re.S)
        out.append({"title": _text(m.group(2)), "url": _bing_url(m.group(1)),
                    "snippet": _text(snip.group(1)) if snip else "", "engine": "bing"})
    return status, out[:limit]


@engine("mojeek")
def mojeek(query: str, limit: int = 20):
    status, html = _get("https://www.mojeek.com/search?q=" + urllib.parse.quote(query))
    out = []
    for m in re.finditer(r'<a[^>]+class="ob"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', html, re.S):
        href = m.group(1)
        if href.startswith("/url?q="):
            href = urllib.parse.parse_qs(urllib.parse.urlparse(href).query).get("q", [""])[0]
        if href.startswith("http"):
            out.append({"title": _text(m.group(2)), "url": href, "snippet": "",
                        "engine": "mojeek"})
    return status, out[:limit]


@engine("marginalia")
def marginalia(query: str, limit: int = 20):
    status, html = _get("https://search.marginalia.nu/search?query=" + urllib.parse.quote(query))
    # The front page answers with a challenge token and a link to the real search
    # host; following it is what the browser does, so do the same.
    hop = re.search(r'href="(/search\?query=[^"]+sst=[^"]+)"', html)
    if hop:
        status, html = _get("https://old-search.marginalia.nu" + hop.group(1).replace("&amp;", "&"))
    out = []
    for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]*>\s*<h2[^>]*>(.*?)</h2>', html, re.S) or \
                      re.finditer(r'<h2[^>]*>\s*<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.S):
        out.append({"title": _text(m.group(2)), "url": m.group(1), "snippet": "",
                    "engine": "marginalia"})
    return status, out[:limit]


@engine("searx")
def searx(query: str, limit: int = 20):
    status, html = _get("https://searx.be/search?q=" + urllib.parse.quote(query) + "&language=en-CA")
    out = []
    for m in re.finditer(r'<a[^>]+href="(https?://[^"]+)"[^>]+class="url_header"[^>]*>(.*?)</a>', html, re.S):
        out.append({"title": _text(m.group(2)), "url": m.group(1), "snippet": "",
                    "engine": "searx"})
    if not out:
        for m in re.finditer(r'<h3>\s*<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', html, re.S):
            out.append({"title": _text(m.group(2)), "url": m.group(1), "snippet": "",
                        "engine": "searx"})
    return status, out[:limit]


@engine("startpage")
def startpage(query: str, limit: int = 20):
    body = urllib.parse.urlencode({"query": query, "cat": "web"}).encode()
    status, html = _get("https://www.startpage.com/sp/search", data=body,
                        headers={"Content-Type": "application/x-www-form-urlencoded"})
    out = []
    for m in re.finditer(r'<a[^>]+class="w-gl__result-title"[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>',
                         html, re.S):
        out.append({"title": _text(m.group(2)), "url": m.group(1), "snippet": "",
                    "engine": "startpage"})
    return status, out[:limit]


@engine("ecosia")
def ecosia(query: str, limit: int = 20):
    status, html = _get("https://www.ecosia.org/search?q=" + urllib.parse.quote(query))
    out = []
    for m in re.finditer(r'<a[^>]+data-test-id="result-link"[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>',
                         html, re.S):
        out.append({"title": _text(m.group(2)), "url": m.group(1), "snippet": "",
                    "engine": "ecosia"})
    return status, out[:limit]


@engine("qwant")
def qwant(query: str, limit: int = 20):
    params = urllib.parse.urlencode({"q": query, "count": limit, "locale": "en_CA",
                                     "offset": 0, "device": "desktop"})
    status, body = _get("https://api.qwant.com/v3/search/web?" + params,
                        headers={"Referer": "https://www.qwant.com/"})
    out = []
    try:
        data = json.loads(body)
        items = (data.get("data", {}).get("result", {}).get("items")
                 or data.get("data", {}).get("result", {}).get("web", []))
        for it in items:
            if it.get("url"):
                out.append({"title": it.get("title") or "", "url": it["url"],
                            "snippet": it.get("desc") or "", "engine": "qwant"})
    except (json.JSONDecodeError, AttributeError):
        pass
    return status, out[:limit]


# --------------------------------------------------------------------------- #
# keyed engines

@engine("brave")
def brave(query: str, limit: int = 20):
    key = _secret("BRAVESEARCHAPIKEY", "BRAVE_SEARCH_API_KEY", "BRAVE_API_KEY")
    if not key:
        return 0, []
    status, body = _get(
        "https://api.search.brave.com/res/v1/web/search?"
        + urllib.parse.urlencode({"q": query, "count": limit, "country": "CA"}),
        headers={"X-Subscription-Token": key, "Accept": "application/json"})
    out = []
    try:
        for it in json.loads(body).get("web", {}).get("results", []):
            out.append({"title": it.get("title", ""), "url": it.get("url", ""),
                        "snippet": _text(it.get("description", "")), "engine": "brave"})
    except json.JSONDecodeError:
        pass
    return status, out[:limit]


GROUNDED_MODELS = ("perplexity/sonar", "openai/gpt-4o-mini:online", "x-ai/grok-3-mini:online")


@engine("openrouter")
def openrouter(query: str, limit: int = 20):
    """A grounded LLM read of the live web: the 'AI search' path, cited."""
    key = _secret("OPENROUTER_API_KEY", "OPENROUTER")
    if not key:
        return 0, []
    prompt = (f"List {limit} individual job postings matching this query: {query}. "
              "Only real, currently open postings on employer careers pages or job boards. "
              "Return ONLY a JSON array of objects with keys title, url, company, location, "
              "posted (YYYY-MM-DD, from the posting itself). No prose.")
    for model in GROUNDED_MODELS:
        body = json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}],
                           "max_tokens": 1500}).encode()
        status, text = _get("https://openrouter.ai/api/v1/chat/completions", data=body,
                            headers={"Authorization": f"Bearer {key}",
                                     "Content-Type": "application/json"})
        if status != 200:
            continue
        try:
            content = json.loads(text)["choices"][0]["message"]["content"]
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
        m = re.search(r"\[.*\]", content, re.S)
        if not m:
            continue
        try:
            items = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        return status, [{"title": i.get("title", ""), "url": i.get("url", ""),
                         "snippet": f"{i.get('company','')} · {i.get('location','')} · "
                                    f"{i.get('posted','')}".strip(" ·"),
                         "engine": f"openrouter:{model}"} for i in items if i.get("url")][:limit]
    return status, []


@engine("perplexity")
def perplexity(query: str, limit: int = 20):
    key = _secret("PERPLEXITY_API_KEY", "PERPLEXITY")
    if not key:
        return 0, []
    body = json.dumps({"model": "sonar", "messages": [{"role": "user", "content": query}]}).encode()
    status, text = _get("https://api.perplexity.ai/chat/completions", data=body,
                        headers={"Authorization": f"Bearer {key}",
                                 "Content-Type": "application/json"})
    out = []
    try:
        data = json.loads(text)
        for url in data.get("citations", [])[:limit]:
            out.append({"title": "", "url": url, "snippet": "", "engine": "perplexity"})
    except json.JSONDecodeError:
        pass
    return status, out


@engine("kagi")
def kagi(query: str, limit: int = 20):
    key = _secret("KAGI_API_KEY", "KAGI")
    if not key:
        return 0, []
    status, body = _get("https://kagi.com/api/v0/search?"
                        + urllib.parse.urlencode({"q": query, "limit": limit}),
                        headers={"Authorization": f"Bot {key}"})
    out = []
    try:
        for it in json.loads(body).get("data", []):
            if it.get("url"):
                out.append({"title": it.get("title", ""), "url": it["url"],
                            "snippet": _text(it.get("snippet", "")), "engine": "kagi"})
    except json.JSONDecodeError:
        pass
    return status, out[:limit]


# --------------------------------------------------------------------------- #

def classify(rows: list[dict]) -> dict:
    postings = [r for r in rows if JOBISH.search(f"{r['title']} {r['snippet']} {r['url']}")
                and not LISTING.search(r["url"])]
    listings = [r for r in rows if LISTING.search(r["url"])]
    return {"results": len(rows), "postings": len(postings), "listing_hubs": len(listings),
            "unrelated": len(rows) - len(postings) - len(listings),
            "sample": [r["url"][:96] for r in postings[:3]]}


def probe(query: str, names: list[str], workers: int = 8) -> dict:
    def run(name):
        try:
            status, rows = ENGINES[name](query)
        except Exception as exc:                          # noqa: BLE001
            return name, {"status": 0, "error": f"{type(exc).__name__}: {exc}", "results": 0,
                          "postings": 0, "listing_hubs": 0, "unrelated": 0, "sample": []}
        info = classify(rows)
        return name, {"status": status, **info}

    with ThreadPoolExecutor(max_workers=workers) as ex:
        return dict(ex.map(run, names))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=("probe", "scan"))
    ap.add_argument("--query", default="servicenow developer toronto jobs")
    ap.add_argument("--engines", default="", help="comma list; default all")
    ap.add_argument("--out", default="")
    ap.add_argument("--limit", type=int, default=20)
    args = ap.parse_args()

    names = [n.strip() for n in args.engines.split(",") if n.strip()] or list(ENGINES)
    unknown = [n for n in names if n not in ENGINES]
    if unknown:
        sys.exit(f"unknown engines: {unknown}; have {sorted(ENGINES)}")

    if args.mode == "probe":
        report = probe(args.query, names)
        print(f"query: {args.query}\n")
        print(f"{'engine':12s} {'http':>5s} {'hits':>5s} {'posts':>6s} {'hubs':>5s} {'other':>6s}")
        print("-" * 50)
        for name, info in report.items():
            print(f"{name:12s} {info['status']:5d} {info['results']:5d} "
                  f"{info['postings']:6d} {info['listing_hubs']:5d} {info['unrelated']:6d}"
                  + (f"  {info['error'][:40]}" if info.get("error") else ""))
        usable = [n for n, i in report.items() if i["postings"]]
        print(f"\nusable (returned real postings): {usable or 'none'}")
        for name in usable:
            for url in report[name]["sample"]:
                print(f"  {name:12s} {url}")
        out = Path(args.out) if args.out else ROOT / "raw" / "search_engine_probe.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"generatedAt": datetime.now(timezone.utc).isoformat(),
                                   "query": args.query, "report": report}, indent=1),
                       encoding="utf-8")
        print(f"\nreport: {out}")
        return 0

    rows: list[dict] = []
    for name in names:
        try:
            _status, got = ENGINES[name](args.query, args.limit)
        except Exception:                                 # noqa: BLE001
            continue
        rows.extend(r for r in got if not LISTING.search(r["url"]))
    seen, uniq = set(), []
    for r in rows:
        key = r["url"].split("?")[0].rstrip("/").lower()
        if key not in seen:
            seen.add(key)
            uniq.append(r)
    out = Path(args.out) if args.out else ROOT / "raw" / "search_rows.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"generatedAt": datetime.now(timezone.utc).isoformat(),
                               "query": args.query, "rows": uniq}, indent=1), encoding="utf-8")
    print(f"{len(rows)} results, {len(uniq)} unique -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
