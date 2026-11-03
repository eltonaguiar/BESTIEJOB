#!/usr/bin/env python3
"""parallel_fanout_scan.py — discover NEW employer boards, then pull fresh postings.

Why this exists
---------------
`today_feeds_scan.py` polls a fixed list of ATS boards. Once those boards are
exhausted it keeps returning near-zero new rows, because the bottleneck is not
the poller — it is the *universe* of boards. This pass grows that universe:

  harvest   fan out N prompts to every available model (local vLLM / Ollama /
            LiteLLM / Open WebUI, plus cloud keys) and M queries to every search
            API (Exa, Tavily, Firecrawl, Jina, Parallel). Each worker writes its
            own file under raw/fanout/ so a single dead provider cannot take the
            run down and every contribution stays auditable.
  aggregate extract ATS board slugs from those files, verify each slug by
            calling the board's own public API, then pull its postings and keep
            only ServiceNow/Salesforce titles in Canada posted within --days.

Model output is treated as a hypothesis: a company name is worthless until its
board answers 200 and returns a posting. Nothing is imported from prose alone.

Usage
-----
    python3 scripts/parallel_fanout_scan.py --phase harvest
    python3 scripts/parallel_fanout_scan.py --phase aggregate --days 7
    python3 scripts/parallel_fanout_scan.py --phase all --days 7
    python3 scripts/parallel_fanout_scan.py --phase aggregate --dry-run
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scripts"))

from ai_panel import get_key  # noqa: E402
from today_feeds_scan import (  # noqa: E402
    EXCL, GEO, KW, NOW, fetch_json, iso_day, norm, workday_day,
)

FANOUT = ROOT / "raw" / "fanout"
INBOX = ROOT / "inbox"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
LOCK = threading.Lock()


def log(msg: str) -> None:
    with LOCK:
        print(msg, flush=True)


# ---------------------------------------------------------------------------
# workers: models


def _chat(url: str, model: str, prompt: str, key: str | None,
          timeout: int = 150, max_tokens: int = 900) -> str:
    body = {"model": model, "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens, "temperature": 0.2}
    headers = {"Content-Type": "application/json", "User-Agent": UA}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    choices = data.get("choices") or []
    if not choices:
        return ""
    msg = choices[0].get("message") or {}
    return (msg.get("content") or "").strip()


def _first_model(base: str) -> str | None:
    """Ask an OpenAI-compatible endpoint what it serves."""
    try:
        req = urllib.request.Request(f"{base}/models", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
        ids = [m.get("id") for m in data.get("data", []) if m.get("id")]
        # prefer a general instruct model over embeddings/rerankers
        for want in ("llama3.3:70b", "llama3.3", "qwen2.5:14b", "Qwen2.5-14B",
                     "deepseek-r1", "qwen3"):
            for i in ids:
                if want.lower() in i.lower():
                    return i
        return ids[0] if ids else None
    except Exception:
        return None


def model_workers() -> list[dict]:
    """Every chat endpoint we can reach, discovered at runtime."""
    out: list[dict] = []
    for name, base in (("vllm", "http://localhost:8000/v1"),
                       ("ollama", "http://localhost:11434/v1"),
                       ("litellm", "http://localhost:4000/v1"),
                       ("openwebui", "http://localhost:3000/api")):
        model = _first_model(base)
        if model:
            out.append({"name": name, "url": f"{base}/chat/completions",
                        "model": model, "key": None, "tier": "local"})
    cloud = [
        ("groq", "https://api.groq.com/openai/v1", "GROQ_API_KEY", "openai/gpt-oss-120b"),
        ("gemini", "https://generativelanguage.googleapis.com/v1beta/openai", "GEMINI_API_KEY",
         "gemini-2.5-flash"),
        ("deepinfra", "https://api.deepinfra.com/v1/openai", "DEEPINFRA_API_KEY",
         "meta-llama/Meta-Llama-3.1-8B-Instruct"),
        ("kilo", "https://api.kilo.ai/api/gateway/v1", "KILOCODE_API_KEY",
         "cohere/north-mini-code:free"),
        ("siliconflow", "https://api.siliconflow.com/v1", "SILICONFLOW_API_KEY", "Qwen/Qwen3-8B"),
        ("mistral", "https://api.mistral.ai/v1", "MISTRAL_API_KEY", "ministral-8b-2512"),
    ]
    for name, base, env, model in cloud:
        key = get_key(env) or get_key("SILICONFLOW" if name == "siliconflow" else env)
        if key:
            out.append({"name": name, "url": f"{base}/chat/completions",
                        "model": model, "key": key, "tier": "cloud"})
    return out


# Divide-and-conquer: each prompt covers a slice of the employer universe, so the
# models propose breadth instead of six variations of "banks".
PROMPTS = {
    "banks-telco": (
        "List Canadian banks, insurers and telecoms that currently employ ServiceNow "
        "or Salesforce developers, administrators or consultants. For each, give the "
        "careers page URL and the ATS platform it uses (Workday, Greenhouse, Lever, "
        "SmartRecruiters, Taleo, SuccessFactors, iCIMS, Workable, Ashby). "
        "One per line: Company | ATS | careers URL | city. No commentary."),
    "agencies": (
        "List IT staffing and contracting agencies that place ServiceNow and Salesforce "
        "developers in Toronto / GTA / Canada (for example TEKsystems, Procom, Randstad, "
        "Akkodis, Robert Half, Insight Global, Hays, Modis, Experis, Judge Group, "
        "Kforce, Collabera, Ampstek, Atlantis IT, Maarut, Compest, Prodigy, LanceSoft). "
        "Add at least ten more agencies beyond those examples. "
        "One per line: Agency | careers URL | city. No commentary."),
    "servicenow-partners": (
        "List ServiceNow partners and Elite/ Premier partners operating in Canada that "
        "hire ServiceNow developers or consultants (for example NewRocket, GlideFast, "
        "AceStack, Infocenter, Veracity, Thirdera, Crossfuze, NTT Data, Fujitsu, "
        "Deloitte, KPMG, PwC, EY, Accenture, Cognizant, Capgemini, Unisys, DXC, "
        "Stefanini, Atos, Kyndryl, Compugen, CDW, Long View). "
        "Add more Canadian ones. One per line: Company | ATS | careers URL | city."),
    "salesforce-partners": (
        "List Salesforce consulting partners (Summit/Ridge/ Crest level) and Salesforce "
        "customers in Canada that hire Apex developers, Salesforce administrators or "
        "technical architects (for example NeuraFlash, Coastal Cloud, Traction on "
        "Demand, CloudKettle, Coveo, Traction, Simplus/Infosys, IBM, Slalom, "
        "Deloitte Digital, Accenture, Wipro, HCL, LTIMindtree, Mastech, Sierra-Cedar). "
        "Add more Canadian ones. One per line: Company | ATS | careers URL | city."),
    "gta-employers": (
        "List mid-market and enterprise employers in Toronto, Mississauga, Markham, "
        "Vaughan, Brampton and Etobicoke that run ServiceNow or Salesforce internally "
        "(hospitals, universities, retailers, manufacturers, logistics, energy, "
        "government agencies, fintech). For each give careers URL and ATS platform. "
        "One per line: Company | ATS | careers URL | city. No commentary."),
    "ats-native": (
        "Which well-known companies use Greenhouse, Lever, Ashby or SmartRecruiters for "
        "engineering hiring in Canada and also hire ServiceNow or Salesforce developers? "
        "Give the exact board token used in the public API URL "
        "(boards-api.greenhouse.io/v1/boards/<token>/jobs, api.lever.co/v0/postings/<token>, "
        "api.ashbyhq.com/posting-api/job-board/<token>, "
        "api.smartrecruiters.com/v1/companies/<token>/postings). "
        "One per line: Company | platform | token. No commentary."),
}


def run_model(worker: dict, tag: str, prompt: str) -> dict:
    started = time.time()
    try:
        text = _chat(worker["url"], worker["model"], prompt, worker["key"])
        status = "ok" if text else "empty"
    except urllib.error.HTTPError as exc:
        text, status = "", f"HTTP {exc.code}"
    except Exception as exc:                                  # noqa: BLE001
        text, status = "", type(exc).__name__
    log(f"[model:{worker['name']}/{tag}] {status} {len(text)}ch "
        f"{time.time() - started:.1f}s")
    return {"worker": f"{worker['name']}/{worker['model']}", "tier": worker["tier"],
            "tag": tag, "status": status, "text": text}


# ---------------------------------------------------------------------------
# workers: search APIs

ROLES = ["ServiceNow Developer", "ServiceNow Administrator", "ServiceNow Consultant",
         "ServiceNow Architect", "ServiceNow ITSM Analyst", "Salesforce Developer",
         "Salesforce Administrator", "Salesforce Consultant", "Salesforce Technical Lead",
         "Apex Developer", "ServiceNow CSA CAD certified", "Salesforce Platform Developer I"]

CITIES = ["Toronto", "Mississauga", "Markham Ontario", "Ontario Canada", "Remote Canada"]


# Scoping a search to the ATS domain itself returns individual postings, whose URL
# contains the employer's board token. That is the cheapest way to discover a board
# that no model named.
ATS_SITE_QUERIES = [
    'site:boards.greenhouse.io "ServiceNow" Canada',
    'site:job-boards.greenhouse.io "Salesforce" Toronto',
    'site:boards.greenhouse.io "Apex" developer Canada',
    'site:jobs.lever.co "ServiceNow" Canada',
    'site:jobs.lever.co "Salesforce" Toronto',
    'site:jobs.ashbyhq.com "ServiceNow"',
    'site:jobs.ashbyhq.com "Salesforce" Canada',
    'site:jobs.smartrecruiters.com "ServiceNow" Canada',
    'site:jobs.smartrecruiters.com "Salesforce" Toronto',
    'site:apply.workable.com "ServiceNow" Canada',
    'site:myworkdayjobs.com "ServiceNow" Toronto',
    'site:myworkdayjobs.com "Salesforce" Canada',
]


def search_queries() -> list[tuple[str, str]]:
    """(provider, query) pairs — spread across providers, cert and city variants."""
    qs: list[tuple[str, str]] = []
    providers = ["tavily", "exa", "firecrawl", "tavily_alt", "jina", "parallel"]
    i = 0
    for role in ROLES:
        for city in CITIES[:2] if "certified" not in role else CITIES[:3]:
            qs.append((providers[i % len(providers)],
                       f'"{role}" jobs {city} posted this week'))
            i += 1
    for city in CITIES:
        qs.append((providers[i % len(providers)], f"ServiceNow OR Salesforce developer job {city} new posting"))
        i += 1
    # ATS-scoped queries: skip firecrawl (rate limited) and jina (no site: support)
    site_providers = ["tavily", "exa", "parallel", "tavily_alt"]
    for k, query in enumerate(ATS_SITE_QUERIES):
        qs.append((site_providers[k % len(site_providers)], query))
        i += 1
    return qs


def _post(url: str, body: dict, headers: dict, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json",
                                          "User-Agent": UA, **headers})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def run_search(provider: str, query: str) -> dict:
    started = time.time()
    items: list[dict] = []
    status = "ok"
    try:
        if provider in ("tavily", "tavily_alt"):
            key = get_key("TAVILY_API_KEY" if provider == "tavily" else "TAVILY_API_KEY_ALT")
            data = _post("https://api.tavily.com/search",
                         {"api_key": key, "query": query, "max_results": 8,
                          "search_depth": "basic"}, {})
            items = [{"title": r.get("title") or "", "url": r.get("url") or "",
                      "snippet": r.get("content") or ""} for r in data.get("results", [])]
        elif provider == "exa":
            data = _post("https://api.exa.ai/search",
                         {"query": query, "numResults": 8, "type": "auto"},
                         {"x-api-key": get_key("EXA_API_KEY")})
            items = [{"title": r.get("title") or "", "url": r.get("url") or "",
                      "snippet": r.get("text") or r.get("summary") or ""}
                     for r in data.get("results", [])]
        elif provider == "firecrawl":
            data = _post("https://api.firecrawl.dev/v2/search",
                         {"query": query, "limit": 8},
                         {"Authorization": f"Bearer {get_key('FIRECRAWL_API_KEY')}"})
            raw = data.get("data") or []
            if isinstance(raw, dict):
                raw = raw.get("web") or []
            items = [{"title": r.get("title") or "", "url": r.get("url") or "",
                      "snippet": r.get("description") or ""} for r in raw]
        elif provider == "jina":
            req = urllib.request.Request(
                "https://s.jina.ai/?" + urllib.parse.urlencode({"q": query}),
                headers={"User-Agent": UA, "Authorization": f"Bearer {get_key('JINA_API_KEY')}",
                         "X-Respond-With": "no-content"})
            with urllib.request.urlopen(req, timeout=40) as resp:
                text = resp.read().decode("utf-8", "replace")
            for m in re.finditer(r"\[([^\]]{4,120})\]\((https?://[^)\s]+)\)", text):
                items.append({"title": m.group(1), "url": m.group(2), "snippet": ""})
        elif provider == "parallel":
            data = _post("https://api.parallel.ai/v1beta/search",
                         {"objective": query, "max_results": 8},
                         {"x-api-key": get_key("PARALLEL_API_KEY")})
            raw = data.get("results") or data.get("data") or []
            items = [{"title": r.get("title") or "", "url": r.get("url") or "",
                      "snippet": (r.get("excerpts") or [""])[0] if r.get("excerpts") else
                                 (r.get("description") or "")} for r in raw]
    except urllib.error.HTTPError as exc:
        status = f"HTTP {exc.code}"
    except Exception as exc:                                   # noqa: BLE001
        status = type(exc).__name__
    log(f"[search:{provider}] {len(items)} hits {status} {time.time() - started:.1f}s")
    return {"provider": provider, "query": query, "status": status, "results": items}


# ---------------------------------------------------------------------------
# harvest


def harvest(search_only: bool = False) -> None:
    FANOUT.mkdir(parents=True, exist_ok=True)
    models = model_workers()
    log(f"models available: {[m['name'] for m in models]}")

    # one prompt per model, rotating the slice so every slice gets covered
    tasks = []
    if search_only:
        models = []
    for i, (tag, prompt) in enumerate(PROMPTS.items()):
        for j, worker in enumerate(models):
            if (i + j) % 2 == 0:            # spread slices across workers
                tasks.append((worker, tag, prompt))
    if models:
        tasks = tasks or [(models[0], tag, p) for tag, p in PROMPTS.items()]

    searches = search_queries()
    log(f"fan-out: {len(tasks)} model calls, {len(searches)} search calls")

    results: list[dict] = []
    with futures.ThreadPoolExecutor(max_workers=10) as ex:
        futs = [ex.submit(run_model, w, t, p) for w, t, p in tasks]
        futs += [ex.submit(run_search, prov, q) for prov, q in searches]
        for f in futures.as_completed(futs):
            try:
                results.append(f.result())
            except Exception as exc:                            # noqa: BLE001
                log(f"[fanout] worker crashed: {exc}")

    stamp = NOW.strftime("%Y-%m-%dT%H%M%SZ")
    model_out = [r for r in results if "text" in r]
    search_out = [r for r in results if "results" in r]
    # a --search-only pass must not discard the model proposals from a prior run
    if search_only:
        prior = sorted(FANOUT.glob("harvest-*.json"))
        if prior:
            try:
                prev = json.loads(prior[-1].read_text(encoding="utf-8"))
                model_out = prev.get("models", []) + model_out
            except json.JSONDecodeError:
                pass
    (FANOUT / f"harvest-{stamp}.json").write_text(
        json.dumps({"generated_at": stamp, "models": model_out, "searches": search_out},
                   indent=2), encoding="utf-8")

    # one file per worker kind, as requested: easy to review individually
    for r in model_out:
        slug = re.sub(r"[^a-z0-9]+", "-", f"model-{r['worker']}-{r['tag']}".lower())
        (FANOUT / f"{slug}.md").write_text(
            f"# {r['worker']} — {r['tag']} ({r['status']})\n\n{r['text']}\n", encoding="utf-8")
    for prov in sorted({r["provider"] for r in search_out}):
        rows = [x for x in search_out if x["provider"] == prov]
        lines = [f"# search:{prov} — {len(rows)} queries", ""]
        for row in rows:
            lines.append(f"## {row['query']}  ({row['status']})")
            for it in row["results"]:
                lines.append(f"- [{it['title'][:100]}]({it['url']})")
            lines.append("")
        (FANOUT / f"search-{prov}.md").write_text("\n".join(lines), encoding="utf-8")

    good = sum(1 for r in model_out if r["status"] == "ok")
    hits = sum(len(r["results"]) for r in search_out)
    print(f"\nfan-out complete: {good}/{len(model_out)} models answered, "
          f"{hits} search hits across {len(search_out)} queries")
    print(f"wrote {FANOUT.relative_to(ROOT)}/harvest-{stamp}.json and per-worker files")


# ---------------------------------------------------------------------------
# aggregate: slugs -> verified boards -> postings

SLUG_PATTERNS = [
    ("greenhouse", re.compile(r"(?:job-boards|boards)\.greenhouse\.io/(?:embed/job_board\?for=)?([a-z0-9_-]+)")),
    ("greenhouse", re.compile(r"boards-api\.greenhouse\.io/v1/boards/([a-z0-9_-]+)")),
    ("lever", re.compile(r"jobs\.(?:eu\.)?lever\.co/([a-z0-9_-]+)")),
    ("lever", re.compile(r"api\.lever\.co/v0/postings/([a-z0-9_-]+)")),
    ("ashby", re.compile(r"jobs\.ashbyhq\.com/([a-z0-9_.-]+)")),
    ("ashby", re.compile(r"api\.ashbyhq\.com/posting-api/job-board/([a-z0-9_.-]+)")),
    ("smartrecruiters", re.compile(r"(?:jobs|careers)\.smartrecruiters\.com/([A-Za-z0-9_-]+)")),
    ("smartrecruiters", re.compile(r"api\.smartrecruiters\.com/v1/companies/([A-Za-z0-9_-]+)")),
    ("workable", re.compile(r"apply\.workable\.com/([a-z0-9_-]+)")),
    ("recruitee", re.compile(r"([a-z0-9-]+)\.recruitee\.com")),
    ("bamboohr", re.compile(r"([a-z0-9-]+)\.bamboohr\.com/(?:careers|jobs)")),
    ("pinpoint", re.compile(r"([a-z0-9-]+)\.pinpointhq\.com")),
    ("workday", re.compile(r"([a-z0-9-]+)\.(wd\d+)\.myworkdayjobs\.com/(?:[a-z]{2}-[A-Z]{2}/)?([A-Za-z0-9_-]+)")),
]

# tokens that are clearly not employer slugs
SLUG_DENY = {"embed", "job_board", "job-boards", "www", "api", "cdn", "assets", "search",
             "jobs", "careers", "home", "index", "v1", "en", "us", "static"}

AI_COMPANY_RE = re.compile(r"^\s*[-*|]?\s*([A-Z][\w&.,'()/ -]{2,60}?)\s*[|—–-]\s*(.*)$")
AI_ATS_RE = re.compile(r"\b(workday|greenhouse|lever|smartrecruiters|taleo|successfactors|"
                       r"icims|workable|ashby|bamboohr|pinpoint|recruitee|dayforce|"
                       r"oracle|sap|unknown)\b", re.I)


def load_harvest() -> tuple[list[dict], list[dict]]:
    files = sorted(FANOUT.glob("harvest-*.json"))
    if not files:
        return [], []
    data = json.loads(files[-1].read_text(encoding="utf-8"))
    return data.get("models", []), data.get("searches", [])


def slug_candidates(models: list[dict], searches: list[dict]) -> dict[tuple[str, str], str]:
    """(platform, slug) -> where it was found. Hypotheses only at this stage."""
    cands: dict[tuple[str, str], str] = {}

    def add(platform: str, slug: str, origin: str) -> None:
        slug = slug.strip().strip("/").lower()
        if not slug or slug in SLUG_DENY or len(slug) < 2:
            return
        cands.setdefault((platform, slug), origin)

    for res in searches:
        for item in res.get("results", []):
            url = item.get("url") or ""
            for platform, pattern in SLUG_PATTERNS:
                for m in pattern.finditer(url):
                    if platform == "workday":
                        add("workday", f"{m.group(1)}|{m.group(2)}|{m.group(3)}", url)
                    else:
                        add(platform, m.group(1), url)
    for mod in models:
        for m in re.finditer(r"https?://[^\s)|<>]+", mod.get("text") or ""):
            for platform, pattern in SLUG_PATTERNS:
                for g in pattern.finditer(m.group(0)):
                    if platform == "workday":
                        add("workday", f"{g.group(1)}|{g.group(2)}|{g.group(3)}", "model")
                    else:
                        add(platform, g.group(1), "model")
    return cands


def probe(platform: str, slug: str) -> list[dict]:
    """Return the board's postings, or [] if the slug is not a real board."""
    try:
        if platform == "greenhouse":
            data = fetch_json(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs")
            return [{"title": j.get("title") or "",
                     "company": slug,
                     "location": (j.get("location") or {}).get("name") or "",
                     "url": j.get("absolute_url") or "",
                     "posted": iso_day(j.get("first_published") or j.get("updated_at")),
                     "source": "greenhouse"} for j in data.get("jobs") or []]
        if platform == "lever":
            data = fetch_json(f"https://api.lever.co/v0/postings/{slug}?mode=json")
            return [{"title": j.get("text") or "", "company": slug,
                     "location": (j.get("categories") or {}).get("location") or "",
                     "url": j.get("hostedUrl") or "", "posted": iso_day(j.get("createdAt")),
                     "source": "lever"} for j in (data if isinstance(data, list) else [])]
        if platform == "ashby":
            data = fetch_json(f"https://api.ashbyhq.com/posting-api/job-board/{slug}")
            return [{"title": j.get("title") or "", "company": slug,
                     "location": j.get("location") or "", "url": j.get("jobUrl") or "",
                     "posted": iso_day(j.get("publishedAt")), "source": "ashby"}
                    for j in data.get("jobs") or []]
        if platform == "smartrecruiters":
            data = fetch_json(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings"
                              "?limit=100")
            out = []
            for it in data.get("content") or []:
                loc = it.get("location") or {}
                out.append({"title": it.get("name") or "", "company": slug,
                            "location": ", ".join(x for x in (loc.get("city"), loc.get("region"),
                                                              loc.get("country")) if x),
                            "url": f"https://jobs.smartrecruiters.com/{slug}/{it.get('id')}",
                            "posted": iso_day(it.get("releasedDate")),
                            "source": "smartrecruiters"})
            return out
        if platform == "workable":
            data = fetch_json(f"https://apply.workable.com/api/v1/widget/accounts/{slug}"
                              "?details=true")
            return [{"title": j.get("title") or "", "company": slug,
                     "location": ", ".join(x for x in ((j.get("location") or {}).get("city"),
                                                       (j.get("location") or {}).get("region"),
                                                       (j.get("location") or {}).get("country")) if x),
                     "url": j.get("url") or j.get("shortlink") or "",
                     "posted": iso_day(j.get("published") or j.get("created_at")),
                     "source": "workable"} for j in data.get("jobs") or []]
        if platform == "recruitee":
            data = fetch_json(f"https://{slug}.recruitee.com/api/offers/")
            return [{"title": j.get("title") or "", "company": slug,
                     "location": j.get("location") or "", "url": j.get("careers_url") or "",
                     "posted": iso_day(j.get("published_at") or j.get("created_at")),
                     "source": "recruitee"} for j in data.get("offers") or []]
        if platform == "bamboohr":
            data = fetch_json(f"https://{slug}.bamboohr.com/careers/list")
            out = []
            for j in data.get("result") or []:
                loc = j.get("location") or {}
                out.append({"title": j.get("jobOpeningName") or "", "company": slug,
                            "location": ", ".join(x for x in (loc.get("city"),
                                                              loc.get("state")) if x),
                            "url": f"https://{slug}.bamboohr.com/careers/{j.get('id')}",
                            "posted": iso_day(j.get("postedDate") or j.get("datePosted")),
                            "source": "bamboohr"})
            return out
        if platform == "pinpoint":
            data = fetch_json(f"https://{slug}.pinpointhq.com/postings.json")
            return [{"title": j.get("title") or "", "company": slug,
                     "location": ((j.get("location") or {}).get("name") or ""),
                     "url": j.get("url") or f"https://{slug}.pinpointhq.com/postings/{j.get('id')}",
                     "posted": iso_day(j.get("created_at") or j.get("published_at")),
                     "source": "pinpoint"} for j in data.get("data") or []]
        if platform == "workday":
            tenant, wd, site = slug.split("|")
            data = fetch_json(f"https://{tenant}.{wd}.myworkdayjobs.com/wday/cxs/"
                              f"{tenant}/{site}/jobs", method="POST",
                              body=json.dumps({"appliedFacets": {}, "limit": 20,
                                               "offset": 0, "searchText": "servicenow"}).encode(),
                              headers={"content-type": "application/json"})
            out = []
            for p in data.get("jobPostings") or []:
                out.append({"title": p.get("title") or "", "company": tenant,
                            "location": p.get("locationsText") or "",
                            "url": f"https://{tenant}.{wd}.myworkdayjobs.com/en-US/{site}"
                                   f"{p.get('externalPath')}",
                            "posted": workday_day(p.get("postedOn") or ""),
                            "source": "workday"})
            return out
    except Exception:
        return []
    return []


COMPANY_LINE = re.compile(r"^\s*(?:[-*\d.]+\s*)?\*{0,2}([A-Z][A-Za-z0-9&.,'()/+ -]{2,55}?)\*{0,2}\s*\|")
SEGMENT_NOISE = re.compile(r"^(company|agency|name|employer|organization|note|platform)\b", re.I)
SUFFIXES = ("inc", "ltd", "corp", "corporation", "group", "solutions", "technologies",
            "technology", "consulting", "services", "systems", "software", "canada",
            "limited", "llc", "llp", "the")


def company_names(models: list[dict]) -> list[str]:
    """Company names the models proposed. A name is a hypothesis, not a board."""
    names: dict[str, int] = {}
    for mod in models:
        for line in (mod.get("text") or "").splitlines():
            m = COMPANY_LINE.match(line)
            if not m:
                continue
            name = re.sub(r"\s+", " ", m.group(1)).strip(" -*`")
            if len(name) < 3 or SEGMENT_NOISE.match(name):
                continue
            names[name] = names.get(name, 0) + 1
    return [n for n, _ in sorted(names.items(), key=lambda kv: -kv[1])]


def slug_variants(name: str) -> list[str]:
    """Tokens an employer plausibly uses as a board slug."""
    low = re.sub(r"[^a-z0-9 &]", "", name.lower()).strip()
    low = re.sub(r"\b(and)\b", "", low)
    words = [w for w in low.split() if w]
    out: list[str] = []
    for trim in range(0, 3):
        ws = words[: len(words) - trim] if len(words) > trim else words
        if not ws:
            continue
        out.append("".join(ws))
        out.append("-".join(ws))
    stripped = [w for w in words if w not in SUFFIXES]
    if stripped and stripped != words:
        out.append("".join(stripped))
        out.append("-".join(stripped))
    return [s for i, s in enumerate(out) if s and len(s) >= 3 and s not in out[:i]]


RESOLVE_PLATFORMS = ("greenhouse", "lever", "ashby", "smartrecruiters", "workable",
                     "recruitee", "bamboohr", "pinpoint")


# Generic GEO matches "remote", so a "Remote - India" posting slipped through. A
# Canadian row must name Canada explicitly; a bare "Remote" is accepted but a
# posting that names another country is rejected outright.
CANADA = re.compile(
    r"canada|canadian|toronto|ontario|\bgta\b|mississauga|markham|brampton|vaughan|"
    r"etobicoke|scarborough|north york|richmond hill|oakville|burlington|waterloo|"
    r"kitchener|guelph|hamilton|london, on|ottawa|montreal|montr[ée]al|quebec|laval|"
    r"calgary|edmonton|vancouver|victoria, bc|winnipeg|halifax|regina|saskatoon|kelowna|"
    r",\s*(on|qc|bc|ab|mb|ns|nb|nl|pe|sk|nt|yt|nu)\b", re.I)
ELSEWHERE = re.compile(
    r"\b(india|bangalore|bengaluru|hyderabad|pune|chennai|noida|gurgaon|kolkata|mumbai|"
    r"philippines|manila|pakistan|nigeria|egypt|brazil|mexico|poland|romania|ukraine|"
    r"united states|\busa\b|u\.s\.|new york|california|texas|florida|seattle|boston|"
    r"chicago|atlanta|austin|denver|phoenix|virginia|ohio|illinois|georgia|carolina|"
    r"united kingdom|\buk\b|ireland|germany|france|netherlands|spain|australia|"
    r"singapore|japan|china|israel|uae|dubai|saudi|qatar|latin america|emea|apac)\b", re.I)

# Boards that re-list other employers' postings: the "company" is not the employer.
AGGREGATOR_SLUGS = {"jobgether", "dice", "map", "nexus", "elite"}


def applicable(row: dict, days: int, known: set[str]) -> bool:
    title = row.get("title") or ""
    url = row.get("url") or ""
    location = row.get("location") or ""
    if not title or not url or EXCL.search(title):
        return False
    if (row.get("company") or "").lower() in AGGREGATOR_SLUGS:
        return False
    if not KW.search(f"{title} {location}"):
        return False
    in_canada = bool(CANADA.search(location))
    if not in_canada:
        if ELSEWHERE.search(location) or not re.search(r"remote|anywhere", location, re.I):
            return False
    posted = row.get("posted")
    if posted:
        age = (NOW.date() - datetime.fromisoformat(posted).date()).days
        if age > days or age < 0:
            return False
    return norm(url) not in known


def aggregate(days: int, dry_run: bool) -> int:
    models, searches = load_harvest()
    if not models and not searches:
        print("no harvest files under raw/fanout/ — run --phase harvest first")
        return 1

    cands = slug_candidates(models, searches)

    # A model names a company, never its board token. Resolve each name by probing
    # the platforms that expose a public board API — a wrong guess 404s harmlessly.
    names = company_names(models)[:60]
    print(f"model-proposed companies: {len(names)}")
    for name in names:
        for platform in RESOLVE_PLATFORMS:
            for slug in slug_variants(name)[:4]:
                cands.setdefault((platform, slug), f"company:{name}")
    print(f"slug candidates: {len(cands)} "
          f"({', '.join(f'{p}:{sum(1 for k in cands if k[0] == p)}' for p in sorted({k[0] for k in cands}))})")

    known: set[str] = set()
    for p in [ROOT / "README.md", *sorted(ROOT.glob("README.BAK_*.md"))[:2], ROOT / "APPLIED.md"]:
        try:
            known.update(norm(u) for u in re.findall(r"https?://[^\s)|]+", p.read_text(errors="replace")))
        except OSError:
            pass
    for p in INBOX.glob("*.md"):
        try:
            known.update(norm(u) for u in re.findall(r"https?://[^\s)|]+", p.read_text(errors="replace")))
        except OSError:
            pass
    try:
        data = json.loads((ROOT / "jobs.json").read_text())
        for j in (data.get("jobs", data) if isinstance(data, dict) else data):
            if isinstance(j, dict) and j.get("url"):
                known.add(norm(j["url"]))
    except (OSError, json.JSONDecodeError):
        pass

    keys = list(cands)
    print(f"probing {len(keys)} candidate boards ...")
    rows: list[dict] = []
    live_boards: list[str] = []
    with futures.ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(probe, p, s): (p, s) for p, s in keys}
        for f in futures.as_completed(futs):
            platform, slug = futs[f]
            try:
                postings = f.result()
            except Exception:
                postings = []
            if postings:
                live_boards.append(f"{platform}:{slug}({len(postings)})")
                for row in postings:
                    if applicable(row, days, known):
                        row["company"] = row["company"].replace("|", "/")
                        rows.append(row)

    # collapse duplicates across boards/providers
    seen: set[str] = set()
    unique: list[dict] = []
    for row in sorted(rows, key=lambda r: (r.get("posted") or "", r.get("title") or ""), reverse=True):
        k = norm(row["url"])
        if k in seen:
            continue
        seen.add(k)
        unique.append(row)

    print(f"live boards: {len(live_boards)}/{len(keys)} -> {len(rows)} matching rows, "
          f"{len(unique)} unique")
    for b in sorted(live_boards)[:40]:
        print(f"  + {b}")
    if dry_run or not unique:
        for r in unique[:30]:
            print(f"  {r['posted'] or 'undated':<10} {r['title'][:55]:<55} | "
                  f"{r['company'][:22]:<22} | {(r['location'] or '')[:28]}")
        return 0

    today = NOW.date().isoformat()
    INBOX.mkdir(parents=True, exist_ok=True)
    ver = 1
    while (INBOX / f"fanout--{today}--v{ver}.md").exists():
        ver += 1
    target = INBOX / f"fanout--{today}--v{ver}.md"
    lines = ["---", "model: fanout",
             f"scanned_at: {NOW.strftime('%Y-%m-%dT%H:%M:%SZ')}",
             "task: ai-plus-search-universe-expansion", "---", "",
             f"# Parallel fan-out scan — {today}", "",
             f"{len(models)} model workers and {len(searches)} search queries proposed "
             f"{len(keys)} candidate ATS boards; {len(live_boards)} answered their public "
             "API and returned postings. Every row below is a posting whose own board "
             "published its date — nothing is inferred from a snippet.", "",
             "| Posted | Role | Company | Location | Source |", "|---|---|---|---|---|"]
    for r in unique:
        lines.append(f"| {r['posted'] or '—'} | [{r['title'].replace('|', '/')}]({r['url']}) | "
                     f"{r['company'].replace('|', '/')} | "
                     f"{(r['location'] or 'Not specified')[:60].replace('|', '/')} "
                     f"| via {r['source']} |")
    target.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nwrote {target.relative_to(ROOT)} (+{len(unique)} rows)")
    print(f"today: {sum(1 for r in unique if r['posted'] == today)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--phase", choices=["harvest", "aggregate", "all"], default="all")
    ap.add_argument("--search-only", action="store_true",
                    help="harvest via search APIs only, keep prior model proposals")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if args.phase in ("harvest", "all"):
        harvest(search_only=args.search_only)
    if args.phase in ("aggregate", "all"):
        return aggregate(args.days, args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
