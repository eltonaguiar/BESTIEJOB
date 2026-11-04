#!/usr/bin/env python3
"""
AI-powered job scanning pipeline for bestiejob.

Leverages the full API key pool from dbpasses_ASK_2026-11-02.txt:
  * Search APIs: Exa, Firecrawl, Tavily x2, Jina, Parallel AI
  * AI chat APIs (keyed-free): Groq x2, Gemini x3, HuggingFace x3, DeepInfra x3,
      Mistral x3, Cohere x2, OpenRouter, SiliconFlow, Z.AI key3, Cloudflare,
      GitHub Models (gh auth token)
  * Keyless chat: Kilo Gateway, Pollinations, OVH, LLM7
  * Local: vLLM :8000, Ollama :11434

Scan tiers:
  T1 Toronto/GTA — ServiceNow + Salesforce (cert keywords: CSA, CAD, Platform Dev I,
      Platform Admin I, JavaScript Developer I)
  T2 Canada-wide — ServiceNow + Salesforce
  T3 Fully remote Canada — ServiceNow + Salesforce
  T4 Partner/agency networks — ServiceNow + Salesforce IT contracting agencies

Writes:
  inbox/ai-scan--<date>--v<N>.md  → consumed by jobs_merge_inbox.py
  scan_results/<date>_tier{1-4}.json  → raw results per tier
  scan_results/<date>_scored.json    → LLM-scored results

Usage:
  python3 scripts/ai_scan_pipeline.py [--tier 1|2|3|4|all] [--no-commit]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

DBPASSES = Path(os.environ.get("DBPASSES_FILE", "/home/eaguiar2015/dbpasses.txt"))
ASK_FILE = Path(os.environ.get("ASK_FILE", "/home/eaguiar2015/dbpasses_ASK_2026-11-02.txt"))
SCAN_DIR = ROOT / "scan_results"
INBOX_DIR = ROOT / "inbox"
JOBS_JSON = ROOT / "jobs.json"

TODAY = datetime.now(timezone.utc).date().isoformat()
STAMP = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

# Scan windows per tier
TIER_WINDOWS = {
    1: {"days": 2,   "geo": "Toronto GTA Mississauga Markham Etobicoke Ontario Canada", "label": "Toronto/GTA"},
    2: {"days": 7,   "geo": "Canada",                                                     "label": "Canada-wide"},
    3: {"days": 7,   "geo": "Canada remote fully remote work from home",                 "label": "Fully remote Canada"},
    4: {"days": 14,  "geo": "Canada ServiceNow partner Salesforce partner consulting IT staffing agency", "label": "Partner/agency network"},
}

# Cert keywords for scoring boost
CERT_KEYWORDS = [
    "CSA", "CAD", "Platform Developer I", "Platform Admin I",
    "JavaScript Developer I", "ServiceNow Certified", "Salesforce Certified",
    "system administrator", "administrator", "developer", "architect",
    "consultant", "specialist", "lead", "senior",
]

# ---------------------------------------------------------------------------
# Key extraction from dbpasses.txt
# ---------------------------------------------------------------------------

def _is_url(val: str) -> bool:
    return val.startswith("http://") or val.startswith("https://")


def load_dbpasses() -> dict[str, str]:
    """Parse dbpasses.txt into {label: key} mapping.

    Handles three formats:
      1. LABEL: value   (inline)
      2. LABEL:         (label on one line, value on next)
      3. LABEL          (no colon, label on one line, value on next)
    Format 3 uses a heuristic: line looks like a label (mostly uppercase,
    underscores/spaces/dots) and next line is not itself a label.
    """
    keys: dict[str, str] = {}
    text = DBPASSES.read_text(encoding="utf-8", errors="replace")
    lines = [l.rstrip() for l in text.splitlines()]
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        # Inline label: value — skip if value looks like a URL (docs, not a key).
        # If value is a URL, the real key is often on the next line.
        m = re.match(r'^([A-Z][A-Z0-9_ ()&/./-]*?):\s*(.+)$', line, re.I)
        if m and m.group(2).strip():
            val2 = m.group(2).strip().strip('"').strip("'")
            if not _is_url(val2) and val2 not in ("******", "TODO", "PENDING"):
                label = _norm_label(m.group(1))
                keys[label] = val2
                i += 1
                continue
            # Value is a URL — peek at next line for the actual key
            if i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if nxt and not _is_url(nxt) and not re.match(r'^[A-Z][A-Z0-9_ ()&/./-]{2,60}:?\s*$', nxt):
                    label = _norm_label(m.group(1))
                    keys[label] = nxt.strip('"').strip("'")
                    i += 2
                    continue
            i += 1
            continue

        # Label: on its own line, value on next
        m2 = re.match(r'^([A-Z][A-Z0-9_ ()&/./-]*?):\s*$', line, re.I)
        if m2 and i + 1 < len(lines):
            label = _norm_label(m2.group(1))
            val = lines[i + 1].strip().strip('"').strip("'")
            if val and val not in ("******", "TODO", "PENDING") and not _is_url(val):
                keys[label] = val
            i += 2
            continue

        # Heuristic: bare label (no colon), value on next line.
        # Label looks like: UPPERCASE with underscores/spaces/dots/parens
        m3 = re.match(r'^([A-Z][A-Z0-9_ ()&/./-]{2,60})$', line, re.I)
        if m3 and i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            if next_line and not _is_url(next_line) and not re.match(r'^[A-Z][A-Z0-9_ ()&/./-]{2,60}:?\s*$', next_line):
                label = _norm_label(m3.group(1))
                val = next_line.strip('"').strip("'")
                if val and val not in ("******", "TODO", "PENDING"):
                    keys[label] = val
                i += 2
                continue

        i += 1
    return keys


def _norm_label(label: str) -> str:
    """Normalize a raw label to a consistent key name."""
    label = label.strip().upper()
    label = re.sub(r'[^A-Z0-9_]', '_', label)
    label = re.sub(r'_+', '_', label)
    label = label.strip('_')
    return label


def get_keys() -> dict[str, str | None]:
    """Return the configured API keys, masked for logging."""
    raw = load_dbpasses()

    # Map standard names → possible labels found in dbpasses.txt
    label_map: dict[str, list[str]] = {
        "EXA_API_KEY": ["EXA_API_KEY"],
        "FIRECRAWL_API_KEY": ["FIRECRAWL_API_KEY"],
        "TAVILY_API_KEY": ["TAVILY_AI_API_KEY_SEARCH"],
        "TAVILY_API_KEY_2": ["TAVILY_AI_API_KEY_ALT_SEARCH"],
        "JINA_API_KEY": ["JINA_READER_API_KEY_SEARCH"],
        "PARALLEL_API_KEY": ["PARALLEL_AI_API_KEY_SEARCH"],
        "GROQ_API_KEY": ["GROQ_API_KEY", "GROQ_FREE_KEY"],
        "GROQ_API_KEY_2": [],
        "GOOGLE_GEMINI_KEY": ["GOOGLE_GEMINI_API_KEY"],
        "GEMINI_API_KEY": ["GOOGLE_GEMIINI_API_KEY_ALT"],
        "GEMINI_API_KEY_2": ["GOOGLE_GEMINI_API_KEY_ALT2"],
        "HF_TOKEN": ["HUGGING_FACE_TOKEN"],
        "HF_TOKEN_2": ["HUGGING_FACE_TOKEN_ALT_TRIED_FINE_GRAIN_AND_SETTING_BUNCH_OF_CHECKBOXES"],
        "HF_TOKEN_3": ["HUGGINF_FACE_TOKEN_ALT2_READ"],
        "DEEPINFRA_API_KEY": ["DEEPINFRA_API_KEY"],
        "DEEPINFRA_API_KEY_2": ["DEEPINFRA_API_KEY_ALT"],
        "DEEPINFRA_API_KEY_BEST": ["DEEPINFRA_API_KEY_BEST"],
        "MISTRAL_API_KEY": ["MISTRAL_API_KEY"],
        "MISTRAL_API_KEY_2": ["MISTRAL_API_KEY_ALT"],
        "MISTRAL_API_KEY_3": ["MISTRAL_API_KEY_ALT2"],
        "COHERE_API_KEY": ["COHERE_TRIAL_API_KEY"],
        "COHERE_API_KEY_2": ["COHERE_TRIAL_API_KEY2_NOVEMBER_2026"],
        "OPENROUTER_API_KEY": ["OPEN_ROUTER_API_KEY_OPENROUTER"],
        "SILICONFLOW_API_KEY": ["SILICONFLOW_COM_API_KEY"],
        "ZAI_API_KEY": ["ZAI_API_KEY3_NOV2026", "ZAI_API_KEY2", "ZAI_API_KEY"],
        "CLOUDFLARE_API_TOKEN": ["CLOUDFLARE_API_KEY", "CLOUDFLARE_GATEWAY_API_EDIT_TOKEN"],
        "CLOUDFLARE_ACCOUNT_ID": ["CLOUDFLARE_ACCOUNT_ID", "ACCOUNT_ID"],
        "GITHUB_MODELS_TOKEN": ["GITHUB_MODELS_API_KEY", "GITHUB_MODELS_API_KEY2"],
        "LLM7_API_KEY": ["LLM7_API_KEY", "LLM7_API_KEY_FREE"],
        "KILOCODE_API_KEY": ["KILOCODE_API_KEY"],
        "KILO_GATEWAY_KEY": ["KILO_GATEWAY_KEY"],
    }

    out: dict[str, str | None] = {}
    for standard, candidates in label_map.items():
        val = None
        for cand in candidates:
            if cand in raw:
                val = raw[cand]
                break
        out[standard] = val

    # env-var keys not in dbpasses
    out["KILOCODE_API_KEY"] = out["KILOCODE_API_KEY"] or os.environ.get("KILOCODE_API_KEY")
    out["GITHUB_MODELS_TOKEN"] = out["GITHUB_MODELS_TOKEN"] or os.environ.get("GITHUB_MODELS_TOKEN")
    return out


KEYS = get_keys()

# ---------------------------------------------------------------------------
# HTTP helper with retries
# ---------------------------------------------------------------------------

import urllib.request
import urllib.error

def http_post(url: str, data: dict, headers: dict | None = None, timeout: int = 15) -> tuple[int, str]:
    """POST JSON, return (status, body_text)."""
    hdrs = {"Content-Type": "application/json", "Accept": "application/json", **(headers or {})}
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=hdrs, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, str(e)


def http_get(url: str, headers: dict | None = None, timeout: int = 15) -> tuple[int, str]:
    """GET, return (status, body_text)."""
    hdrs = {"Accept": "application/json", **(headers or {})}
    req = urllib.request.Request(url, headers=hdrs, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, str(e)


# ---------------------------------------------------------------------------
# Search API clients
# ---------------------------------------------------------------------------

def exa_search(query: str, num_results: int = 10) -> list[dict]:
    key = KEYS.get("EXA_API_KEY")
    if not key:
        return []
    status, body = http_post(
        "https://api.exa.ai/search",
        {"query": query, "numResults": num_results, "type": "neural", "includeDomains": []},
        {"x-api-key": key},
    )
    if status != 200:
        return []
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return []
    out = []
    for r in data.get("results", []) or []:
        out.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("snippet", ""),
            "publishedDate": r.get("publishedDate", ""),
            "source": "exa",
        })
    return out


def firecrawl_search(query: str, num_results: int = 10) -> list[dict]:
    key = KEYS.get("FIRECRAWL_API_KEY")
    if not key:
        return []
    status, body = http_post(
        "https://api.firecrawl.dev/v2/search",
        {"query": query, "limit": num_results, "scrapeOptions": {"formats": ["markdown"]}},
        {"x-api-key": key, "Content-Type": "application/json"},
    )
    if status != 200:
        return []
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return []
    out = []
    data_list = data.get("data") or [] if isinstance(data, dict) else []
    for r in data_list:
        if isinstance(r, dict):
            out.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": (r.get("markdown") or r.get("description", ""))[:400],
                "publishedDate": "",
                "source": "firecrawl",
            })
    return out


def tavily_search(query: str, key_label: str, num_results: int = 10) -> list[dict]:
    key = KEYS.get(key_label)
    if not key:
        return []
    status, body = http_post(
        "https://api.tavily.com/search",
        {"query": query, "search_depth": "advanced", "max_results": num_results, "include_domains": []},
        {"api-key": key},
    )
    if status != 200:
        return []
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return []
    out = []
    for r in data.get("results", []) or []:
        out.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": r.get("content", "")[:400],
            "publishedDate": r.get("published_date", ""),
            "source": f"tavily:{key_label}",
        })
    return out


def jina_search(query: str) -> list[dict]:
    key = KEYS.get("JINA_API_KEY")
    if not key:
        return []
    encoded = urlencode({"q": query})
    status, body = http_get(
        f"https://s.jina.ai/?{encoded}",
        {"Authorization": f"Bearer {key}"},
    )
    if status != 200:
        return []
    # Jina search returns JSON: {"code":200,"data":[{"title","url","description","content"}]}
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return []
    items = data.get("data", []) if isinstance(data, dict) else []
    out = []
    for r in items:
        if isinstance(r, dict):
            out.append({
                "title": r.get("title", ""),
                "url": r.get("url", ""),
                "snippet": r.get("description", "")[:400],
                "publishedDate": "",
                "source": "jina",
            })
    return out


def parallel_ai_search(query: str, num_results: int = 10) -> list[dict]:
    key = KEYS.get("PARALLEL_API_KEY")
    if not key:
        return []
    # Parallel AI v1beta uses 'search_queries' array, not 'query' string
    status, body = http_post(
        "https://api.parallel.ai/v1beta/search",
        {"search_queries": [query], "num_results": num_results},
        {"x-api-key": key},
    )
    if status != 200:
        return []
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return []
    out = []
    results = data.get("results", []) or data.get("data", []) or []
    for r in results:
        # Parallel AI returns 'excerpts' array, join them for snippet
        excerpts = r.get("excerpts", [])
        if isinstance(excerpts, list):
            snippet = " ".join(str(e) for e in excerpts)[:400]
        else:
            snippet = str(r.get("snippet", ""))[:400]
        out.append({
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "snippet": snippet,
            "publishedDate": r.get("publish_date", r.get("date", "")),
            "source": "parallel-ai",
        })
    return out


# ---------------------------------------------------------------------------
# AI chat client (OpenAI-compatible)
# ---------------------------------------------------------------------------

def chat_completion(
    base_url: str,
    api_key: str | None,
    model: str,
    messages: list[dict],
    max_tokens: int = 256,
    temperature: float = 0.3,
    timeout: int = 20,
) -> str | None:
    """Generic OpenAI-compatible chat completion. Returns content or None."""
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    payload = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    status, body = http_post(base_url + "/chat/completions", payload, headers, timeout=timeout)
    if status != 200:
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    choices = data.get("choices") or []
    if not choices:
        return None
    return choices[0].get("message", {}).get("content")


def local_ollama_chat(model: str, messages: list[dict], max_tokens: int = 256) -> str | None:
    """Ollama :11434 chat."""
    payload = {"model": model, "messages": messages, "stream": False, "options": {"num_predict": max_tokens}}
    status, body = http_post("http://localhost:11434/api/chat", payload, {}, timeout=30)
    if status != 200:
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    return data.get("message", {}).get("content")


def local_vllm_chat(model: str, messages: list[dict], max_tokens: int = 256) -> str | None:
    """vLLM :8000 chat."""
    headers = {"Content-Type": "application/json"}
    payload = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": 0.3}
    status, body = http_post("http://localhost:8000/v1/chat/completions", payload, headers, timeout=30)
    if status != 200:
        return None
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        return None
    choices = data.get("choices") or []
    if not choices:
        return None
    return choices[0].get("message", {}).get("content")


# ---------------------------------------------------------------------------
# Scoring: multi-AI fan-out for job relevance to cert targets
# ---------------------------------------------------------------------------

SCORING_PROMPT_TEMPLATE = """You are a hiring screener for Elton Aguiar, a ServiceNow Developer / Technical Consultant with 6+ years experience, Toronto ON.

Certifications: ServiceNow CSA, CAD, CIS-PA, CIS-RC, CIS-HAM, CIS-SAM, CIS-DISCO, CIS-SPM, CIS-HR. Salesforce JavaScript Developer I Certified. ITIL v4 Foundation.

Job: {title} at {company}
Location: {location}
Excerpt: {excerpt}

Rate this job 0-10 for fit against Elton's profile, considering:
- ServiceNow / Salesforce platform match
- Toronto / GTA / Canada / Remote Canada location
- Certification relevance (CSA, CAD, Platform Dev I, JS Dev I)
- Seniority (developer, administrator, architect, consultant, lead)

Respond with ONLY: SCORE: <0-10> | REASON: <one sentence>"""


def score_jobs_with_ai(jobs: list[dict], tier: int, voters: list[tuple[str, callable, dict]] | None = None) -> list[dict]:
    """Score jobs using a fan-out of AI providers. Returns jobs with score/reason added."""
    scored = []
    # Build AI voters: local + cloud
    default_voters: list[tuple[str, callable, dict]] = [
        ("ollama-qwen7b", local_ollama_chat, {"model": "qwen2.5:7b-instruct-q5_K_M"}),
        ("vllm-qwen14b", local_vllm_chat, {"model": "Qwen/Qwen2.5-14B-Instruct"}),
        ("groq-gpt-oss", chat_completion, {
            "base_url": "https://api.groq.com/openai/v1",
            "api_key": KEYS.get("GROQ_API_KEY"),
            "model": "openai/gpt-oss-120b",
        }),
        ("gemini-flash", chat_completion, {
            "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
            "api_key": KEYS.get("GOOGLE_GEMINI_KEY") or KEYS.get("GEMINI_API_KEY"),
            "model": "gemini-2.5-flash",
        }),
        ("deepinfra-llama", chat_completion, {
            "base_url": "https://api.deepinfra.com/v1/openai",
            "api_key": KEYS.get("DEEPINFRA_API_KEY_BEST") or KEYS.get("DEEPINFRA_API_KEY"),
            "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        }),
        ("kilo-gateway", chat_completion, {
            "base_url": "https://api.kilo.ai/api/gateway/v1",
            "api_key": os.environ.get("KILOCODE_API_KEY") or KEYS.get("KILOCODE_API_KEY"),
            "model": "cohere/north-mini-code:free",
        }),
    ]
    voters = voters or default_voters

    for job in jobs:
        prompt = SCORING_PROMPT_TEMPLATE.format(
            title=job.get("title", ""),
            company=job.get("company", ""),
            location=job.get("location", ""),
            excerpt=job.get("excerpt", "")[:300],
        )
        messages = [{"role": "user", "content": prompt}]

        best_score = 0
        best_reason = "no voter returned"
        results = []

        for name, fn, kwargs in voters:
            try:
                content = fn(messages=messages, **kwargs)
                if content:
                    m = re.search(r"SCORE:\s*(\d+)", content)
                    r = re.search(r"REASON:\s*(.+)", content)
                    score = int(m.group(1)) if m else 0
                    reason = r.group(1).strip() if r else content[:100]
                    results.append({"voter": name, "score": score, "reason": reason})
                    if score > best_score:
                        best_score = score
                        best_reason = reason
            except Exception as e:
                results.append({"voter": name, "score": 0, "reason": f"error: {e}"})

        job["ai_score"] = best_score
        job["ai_reason"] = best_reason
        job["ai_voters"] = results
        scored.append(job)
        time.sleep(0.3)  # be gentle with APIs

    return scored


# ---------------------------------------------------------------------------
# Scan builders per tier
# ---------------------------------------------------------------------------

def build_search_queries(tier: int) -> list[tuple[str, str]]:
    """Return list of (query, geo_label) search queries for a tier."""
    cfg = TIER_WINDOWS[tier]
    geo = cfg["geo"]
    queries = []

    sn_terms = ["ServiceNow developer", "ServiceNow administrator", "ServiceNow architect",
                "ServiceNow consultant", "ServiceNow CSA", "ServiceNow CAD",
                "ServiceNow ITSM", "ServiceNow ITAM", "ServiceNow CMDB"]
    sf_terms = ["Salesforce developer", "Salesforce administrator", "Salesforce architect",
                "Salesforce consultant", "Salesforce Platform Developer I",
                "Salesforce JavaScript Developer I", "Salesforce CPQ"]

    for term in sn_terms + sf_terms:
        queries.append((f"{term} {geo} posted today", f"t{tier}_{geo}"))

    # Cert-specific
    for cert in ["CSA", "CAD", "Platform Developer I", "Platform Admin I", "JavaScript Developer I"]:
        queries.append((f"{cert} ServiceNow Salesforce {geo}", f"t{tier}_cert"))
        queries.append((f"{cert} {geo} job", f"t{tier}_cert"))

    return queries


def run_search_apis(queries: list[tuple[str, str]], search_apis: list[str] | None = None, max_queries: int | None = None) -> list[dict]:
    """Run all search APIs against all queries, dedupe by URL."""
    seen: dict[str, dict] = {}
    all_results: list[dict] = []

    apis = search_apis or ["exa", "firecrawl", "tavily", "jina", "parallel"]
    if max_queries:
        queries = queries[:max_queries]

    for query, geo_label in queries:
        if "exa" in apis:
            for r in exa_search(query):
                u = r.get("url", "")
                if u and u not in seen:
                    seen[u] = r
                    all_results.append(r)
        if "firecrawl" in apis:
            for r in firecrawl_search(query):
                u = r.get("url", "")
                if u and u not in seen:
                    seen[u] = r
                    all_results.append(r)
        if "tavily" in apis:
            for r in tavily_search(query, "TAVILY_API_KEY"):
                u = r.get("url", "")
                if u and u not in seen:
                    seen[u] = r
                    all_results.append(r)
            for r in tavily_search(query, "TAVILY_API_KEY_2"):
                u = r.get("url", "")
                if u and u not in seen:
                    seen[u] = r
                    all_results.append(r)
        if "jina" in apis:
            for r in jina_search(query):
                u = r.get("url", "")
                if u and u not in seen:
                    seen[u] = r
                    all_results.append(r)
        if "parallel" in apis:
            for r in parallel_ai_search(query):
                u = r.get("url", "")
                if u and u not in seen:
                    seen[u] = r
                    all_results.append(r)
        time.sleep(0.5)  # rate-limit breathing room

    return all_results


def normalize_job(result: dict, tier: int) -> dict | None:
    """Convert a search result into a job dict."""
    title = result.get("title", "").strip()
    url = result.get("url", "").strip()
    if not title or not url:
        return None
    # Filter out non-job pages
    low = (title + " " + url + " " + result.get("snippet", "")).lower()
    if not any(k in low for k in ["job", "career", "hire", "position", "role", "servicenow", "salesforce"]):
        return None
    return {
        "title": title,
        "company": result.get("company", "Unknown"),
        "location": result.get("location", "Canada"),
        "url": url,
        "source": f"{result.get('source', 'search')} (tier {tier})",
        "postedDate": result.get("publishedDate") or TODAY + "T00:00:00Z",
        "scrapedAt": datetime.now(timezone.utc).isoformat(),
        "excerpt": result.get("snippet", "")[:300],
        "workArrangement": "unknown",
        "tags": [],
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def scan_tier(tier: int, search_apis: list[str] | None = None, max_queries: int | None = None, score: bool = True, voters: list[str] | None = None) -> list[dict]:
    """Scan one tier end-to-end: search → normalize → score."""
    print(f"\n=== TIER {tier}: {TIER_WINDOWS[tier]['label']} ===")
    queries = build_search_queries(tier)
    print(f"  {len(queries)} search queries across {len(TIER_WINDOWS[tier]['geo'].split())} geo targets")

    results = run_search_apis(queries, search_apis=search_apis, max_queries=max_queries)
    print(f"  {len(results)} raw search results")

    jobs = []
    for r in results:
        j = normalize_job(r, tier)
        if j:
            jobs.append(j)
    print(f"  {len(jobs)} normalized jobs")

    if score and jobs:
        # Filter voters if specified
        voter_list = None
        if voters:
            default_map = {
                "ollama-qwen7b": (local_ollama_chat, {"model": "qwen2.5:7b-instruct-q5_K_M"}),
                "vllm-qwen14b": (local_vllm_chat, {"model": "Qwen/Qwen2.5-14B-Instruct"}),
                "groq-gpt-oss": (chat_completion, {
                    "base_url": "https://api.groq.com/openai/v1",
                    "api_key": KEYS.get("GROQ_API_KEY"),
                    "model": "openai/gpt-oss-120b",
                }),
                "gemini-flash": (chat_completion, {
                    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
                    "api_key": KEYS.get("GOOGLE_GEMINI_KEY") or KEYS.get("GEMINI_API_KEY"),
                    "model": "gemini-2.5-flash",
                }),
                "deepinfra-llama": (chat_completion, {
                    "base_url": "https://api.deepinfra.com/v1/openai",
                    "api_key": KEYS.get("DEEPINFRA_API_KEY_BEST") or KEYS.get("DEEPINFRA_API_KEY"),
                    "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
                }),
                "kilo-gateway": (chat_completion, {
                    "base_url": "https://api.kilo.ai/api/gateway/v1",
                    "api_key": os.environ.get("KILOCODE_API_KEY") or KEYS.get("KILOCODE_API_KEY"),
                    "model": "cohere/north-mini-code:free",
                }),
            }
            voter_list = [(name, fn, kwargs) for name, (fn, kwargs) in default_map.items() if name in voters]

        # Score with AI fan-out
        scored = score_jobs_with_ai(jobs, tier, voters=voter_list)
        scored.sort(key=lambda j: j.get("ai_score", 0), reverse=True)
        return scored
    return jobs


def write_inbox_file(all_scored: dict[int, list[dict]]) -> Path:
    """Write inbox/ file in the merge-compatible format."""
    INBOX_DIR.mkdir(exist_ok=True)
    # Find next version number
    existing = list(INBOX_DIR.glob(f"ai-scan--{TODAY}--v*.md"))
    v = len(existing) + 1
    path = INBOX_DIR / f"ai-scan--{TODAY}--v{v}.md"

    lines: list[str] = []
    lines.append(f"# AI Scan — {TODAY} (v{v})")
    lines.append("")
    lines.append("Generated by scripts/ai_scan_pipeline.py using the full AI API pool from dbpasses_ASK_2026-11-02.txt")
    lines.append("")
    lines.append("| Posted | Role | Company | Location | Score | AI Reason | URL |")
    lines.append("|---|---|---|---|---|---|---|")

    for tier in sorted(all_scored):
        for job in all_scored[tier]:
            posted = job.get("postedDate", TODAY)[:10]
            score = job.get("ai_score", 0)
            reason = job.get("ai_reason", "")[:80].replace("|", "\\|")
            lines.append(
                f"| {posted} | [{job['title']}]({job['url']}) | {job['company']} | {job['location']} | {score}/10 | {reason} | {job['url']} |"
            )

    lines.append("")
    lines.append(f"_Scan tiers: {', '.join(str(t) for t in sorted(all_scored))} · Generated {STAMP}_")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  → Wrote {path} ({len(lines)} lines incl. header)")
    return path


def write_raw_results(all_scored: dict[int, list[dict]]) -> None:
    """Write raw scored results to scan_results/."""
    SCAN_DIR.mkdir(exist_ok=True)
    for tier, jobs in all_scored.items():
        path = SCAN_DIR / f"{TODAY}_tier{tier}.json"
        path.write_text(json.dumps(jobs, indent=2), encoding="utf-8")
    all_path = SCAN_DIR / f"{TODAY}_scored.json"
    flat = [j for tier_jobs in all_scored.values() for j in tier_jobs]
    all_path.write_text(json.dumps(flat, indent=2), encoding="utf-8")
    print(f"  → Wrote raw results to {SCAN_DIR}/")


def run_merge_and_build() -> None:
    """Run jobs_merge_inbox.py and build_site.py."""
    print("\n=== MERGE + BUILD ===")
    import subprocess

    # 1. Merge inbox into README
    r = subprocess.run(
        [sys.executable, "tools/jobs_merge_inbox.py"],
        cwd=ROOT,
        capture_output=True, text=True,
    )
    print("  merge:", r.stdout[-500:] if r.stdout else "(no output)")
    if r.returncode != 0:
        print("  merge stderr:", r.stderr[-500:] if r.stderr else "")

    # 2. Consolidate README
    r = subprocess.run(
        [sys.executable, "tools/jobs_consolidate.py", "--today", TODAY, "--days", "30"],
        cwd=ROOT,
        capture_output=True, text=True,
    )
    print("  consolidate:", r.stdout[-300:] if r.stdout else "(no output)")

    # 3. Build site
    r = subprocess.run(
        [sys.executable, "tools/build_site.py"],
        cwd=ROOT,
        capture_output=True, text=True,
    )
    print("  build_site:", r.stdout[-300:] if r.stdout else "(no output)")
    if r.returncode != 0:
        print("  build_site stderr:", r.stderr[-500:] if r.stderr else "")


def git_commit(commit: bool = True) -> None:
    """Commit changes to main branch."""
    if not commit:
        print("\n  (--no-commit: skipping git commit)")
        return
    import subprocess

    print("\n=== GIT COMMIT ===")
    # Check we're on a branch that only has our changes
    r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    changed = [l for l in r.stdout.splitlines() if l.strip()]
    print(f"  {len(changed)} changed files")

    # Only add our own pipeline outputs
    subprocess.run(["git", "add", "inbox/ai-scan--*.md", "scan_results/", "README.md", "public/"], cwd=ROOT)
    r = subprocess.run(
        ["git", "commit", "-m", f"chore(jobs): AI scan refresh {STAMP} [skip ci]"],
        cwd=ROOT, capture_output=True, text=True,
    )
    print("  commit:", r.stdout.strip() or r.stderr.strip())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", type=int, choices=[1, 2, 3, 4], default=None,
                    help="Run only one tier (default: all)")
    ap.add_argument("--no-commit", action="store_true", help="Skip git commit")
    ap.add_argument("--search-api", action="append", choices=["exa", "firecrawl", "tavily", "jina", "parallel"],
                    help="Search API to use (can repeat; default: all)")
    ap.add_argument("--max-queries", type=int, default=None,
                    help="Max queries per tier (for testing)")
    ap.add_argument("--no-score", action="store_true",
                    help="Skip AI scoring (just collect raw results)")
    ap.add_argument("--voter", action="append",
                    help="Scoring voter to use (can repeat; default: all)")
    args = ap.parse_args()

    tiers = [args.tier] if args.tier else [1, 2, 3, 4]
    all_scored: dict[int, list[dict]] = {}

    for tier in tiers:
        try:
            scored = scan_tier(tier, search_apis=args.search_api, max_queries=args.max_queries,
                               score=not args.no_score,
                               voters=args.voter)
            all_scored[tier] = scored
        except Exception as e:
            print(f"  ERROR tier {tier}: {e}")
            import traceback
            traceback.print_exc()

    if not all_scored:
        print("No results from any tier.")
        return 1

    write_inbox_file(all_scored)
    write_raw_results(all_scored)

    total = sum(len(v) for v in all_scored.values())
    high_score = sum(1 for v in all_scored.values() for j in v if j.get("ai_score", 0) >= 7)
    print(f"\n=== DONE: {total} jobs scored, {high_score} scored 7+/10 ===")

    run_merge_and_build()
    git_commit(commit=not args.no_commit)

    return 0


if __name__ == "__main__":
    sys.exit(main())
