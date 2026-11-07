#!/usr/bin/env python3
"""ai_panel.py — free-AI second-opinion panel for the BESTIEJOB job search.

Wires the free / keyless LLM pool into the automated job scan so a scan round
can (a) propose search keywords nobody hard-coded, and (b) get an independent
reading of ambiguous listings, without paying for inference.

Three subcommands:

    ping      live health-check every provider (latency + which model answered)
    queries   ask N independent models for Adzuna `what` variants we don't use
    triage    second-opinion classify a batch of job rows (category + fit)

Keys are read from ~/dbpasses.txt (gitignored) and the environment. Keys are
NEVER printed, logged, or written to a repo file.

Every provider is best-effort: a 401/402/429/timeout marks that peer failed and
the panel moves on. Correlated failure is the normal case for free tiers, so the
panel reports an answer count rather than assuming success.

Usage:
    python3 tools/ai_panel.py ping
    python3 tools/ai_panel.py ping --only groq,kilocode,pollinations
    python3 tools/ai_panel.py queries --count 12 --out raw/ai_queries.json
    python3 tools/ai_panel.py triage --input raw/ai_triage_in.json --out-json raw/ai_triage.json
"""

from __future__ import annotations

import argparse
import concurrent.futures as futures
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parent.parent
KEYS_FILE = Path.home() / "dbpasses.txt"
DISCOVER = "@discover"
UA = "Mozilla/5.0 (compatible; bestiejob-ai-panel/1.0)"

# ---------------------------------------------------------------------------
# Key loading — label match first, then env, then key-shape scan
# ---------------------------------------------------------------------------
# dbpasses.txt is inconsistent (some labels lack the trailing colon, some keys
# sit two lines below the label after a URL/notes line), so three passes are
# used and the first hit wins. Nothing here is ever echoed.
LABELS: dict[str, list[str]] = {
    "GROQ_API_KEY": ["GROQ FREE KEY", "GROQ_API_KEY"],
    "GEMINI_API_KEY": ["GOOGLE GEMINI API KEY", "GEMINI API KEY"],
    "GEMINI_API_KEY_ALT": ["GOOGLE GEMIINI API KEY ALT", "GOOGLE GEMINI API KEY ALT"],
    "HF_API_TOKEN": ["[REDACTED]", "HUGGING_FACE_TOKEN", "HUGGING FACE TOKEN"],
    "DEEPINFRA_API_KEY": ["DEEPINFRA API KEY", "DEEPINFRA API KEY ALT"],
    "COHERE_API_KEY": ["COHERE API KEY", "COHERE TRIAL KEY"],
    "MISTRAL_API_KEY": ["MISTRAL API KEY", "MISTRAL API KEY ALT"],
    "PUBLICAI_API_KEY": ["PUBLICAI API KEY", "PUBLIC AI API KEY"],
    "OPENROUTER_API_KEY": ["OPEN ROUTER API KEY", "OPENROUTER API KEY"],
    "NOUS_API_KEY": ["NOUS API KEY (USE ONLY FREE MODELS)", "NOUS API KEY"],
    "SAMBANOVA_API_KEY": ["SAMBANOVA API KEY", "SAMBANOVA CLOUD API KEY"],
    "AIMLAPI_API_KEY": ["AIMLAPI.COM", "AIMLAPI API KEY"],
    "SILICONFLOW_API_KEY": ["SILICONFLOW API KEY", "SILICON FLOW API KEY"],
    "ZAI_API_KEY": ["ZAI API KEY", "Z.AI API KEY"],
    "KILOCODE_API_KEY": ["KILOCODE API KEY", "KILO CODE API KEY"],
    "GITHUB_MODELS_KEY": ["GITHUB MODELS API KEY"],
    "CF_ACCOUNT_ID": ["CLOUDFLARE ACCOUNT ID"],
    "CF_API_TOKEN": ["CLOUDFLARE API KEY", "CLOUDFLARE API TOKEN"],
    "LLM7_API_KEY": ["LLM7 API KEY"],
    "BRAVE_SEARCH_API_KEY": ["BRAVE SEARCH API KEY"],
    # search APIs — used by scripts/web_search_scan.py through this module
    "TAVILY_API_KEY": ["TAVILY API KEY", "TAVILY API KEY 2"],
    "EXA_API_KEY": ["EXA API KEY", "EXA AI API KEY"],
    "FIRECRAWL_API_KEY": ["FIRECRAWL API KEY", "FIRECRAWL API KEY 2"],
    "JINA_API_KEY": ["JINA READER API KEY(SEARCH)", "JINA API KEY"],
    "PARALLEL_API_KEY": ["PARALLEL AI API KEY (SEARCH)"],
    # Adzuna needs an app id + app key pair; both must be present to use it
    "ADZUNA_APP_ID": ["ADZUNA APP ID", "ADZUNA APPLICATION ID"],
    "ADZUNA_APP_KEY": ["ADZUNA APP KEY", "ADZUNA API KEY"],
}

# Label matching by regex. The key store spells the search-API labels
# inconsistently ("EXA API KEY for serach", "TAVILY AI API KEY (SEARCH)",
# "JINA READER API KEY(SEARCH)"), so an exact label never matches. These
# patterns find the label line; the value is then looked for on that line and
# in the next few lines, because several entries put prose or a URL between
# the label and the credential.
# How many lines below a label its value may sit. Exa's entry has a prose
# integration blurb and a docs block between the label and the credential.
LOOKAHEAD = {"EXA_API_KEY": 25}

LABEL_REGEX: dict[str, list[re.Pattern[str]]] = {
    "TAVILY_API_KEY_ALT": [re.compile(r"tavily.*alt", re.I)],
    "TAVILY_API_KEY": [re.compile(r"tavily(?!.*alt)", re.I)],
    "EXA_API_KEY": [re.compile(r"\bexa\b.*(key|api)", re.I)],
    "FIRECRAWL_API_KEY": [re.compile(r"firecrawl.*key", re.I)],
    "JINA_API_KEY": [re.compile(r"jina.*key", re.I)],
    "PARALLEL_API_KEY": [re.compile(r"parallel.*key", re.I)],
    "BRAVE_SEARCH_API_KEY": [re.compile(r"brave.*key", re.I)],
}

# Key-shape fallback: the label was wrong/redacted but the value is recognisable.
KEY_SHAPES: list[tuple[str, re.Pattern[str]]] = [
    ("GROQ_API_KEY", re.compile(r"^gsk_[A-Za-z0-9]{20,}$")),
    ("OPENROUTER_API_KEY", re.compile(r"^sk-or-v1-[A-Za-z0-9]{20,}$")),
    ("PUBLICAI_API_KEY", re.compile(r"^zpka_[A-Za-z0-9_]{20,}$")),
    ("HF_API_TOKEN", re.compile(r"^hf_[A-Za-z0-9]{20,}$")),
    ("GEMINI_API_KEY", re.compile(r"^AIza[A-Za-z0-9_\-]{30,}$")),
    ("COHERE_API_KEY", re.compile(r"^cohere_[A-Za-z0-9]{20,}$")),
    ("GITHUB_MODELS_KEY", re.compile(r"^(github_pat_|ghp_)[A-Za-z0-9_]{20,}$")),
]

_cache: dict[str, str] = {}


def _is_value(line: str) -> bool:
    s = line.strip()
    return bool(s) and not s.endswith(":") and " " not in s and len(s) >= 12


def load_keys() -> dict[str, str]:
    """Env first (explicit override), dbpasses.txt as the canonical fallback."""
    global _cache
    if _cache:
        return _cache

    lines: list[str] = []
    if KEYS_FILE.exists():
        try:
            lines = KEYS_FILE.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            lines = []

    norm = [re.sub(r"[^a-z0-9]", "", ln.lower()) for ln in lines]

    # pass 0: regex label match with a wide lookahead (search APIs)
    for env_name, patterns in LABEL_REGEX.items():
        for i, raw in enumerate(lines):
            line = raw.strip()
            if not line or len(line) > 160:
                continue
            if not any(p.search(line) for p in patterns):
                continue
            tail = line.split(":", 1)[1].strip() if ":" in line else ""
            ahead = LOOKAHEAD.get(env_name, 8)
            for cand in [tail] + [ln.strip() for ln in lines[i + 1: i + 1 + ahead]]:
                if _is_value(cand) and len(cand) >= 20:
                    _cache[env_name] = cand
                    break
            if env_name in _cache:
                break

    for env_name, labels in LABELS.items():
        # pass 1: label match, value on one of the next 3 lines
        for label in labels:
            needle = re.sub(r"[^a-z0-9]", "", label.lower())
            for i, n in enumerate(norm):
                if n == needle or n.startswith(needle):
                    for j in range(i + 1, min(i + 4, len(lines))):
                        if _is_value(lines[j]):
                            _cache[env_name] = lines[j].strip()
                            break
                    break
            if env_name in _cache:
                break

    # pass 2: key shape, for labels the file got wrong
    for env_name, pattern in KEY_SHAPES:
        if env_name in _cache:
            continue
        for ln in lines:
            v = ln.strip()
            if pattern.match(v):
                _cache[env_name] = v
                break

    # pass 3: env overrides / fills gaps
    for env_name in LABELS:
        v = os.environ.get(env_name)
        if v and v.strip():
            _cache[env_name] = v.strip()

    return _cache


def get_key(name: str) -> Optional[str]:
    return load_keys().get(name)


# ---------------------------------------------------------------------------
# Provider registry
# ---------------------------------------------------------------------------
# key_env: list of alternative env names, or None for a keyless endpoint.
# {account} in base is substituted from the Cloudflare account id.
PROVIDERS: list[dict[str, Any]] = [
    # --- keyless: no account, no key, no quota to speak of ------------------
    {"name": "kilocode", "base": "https://api.kilo.ai/api/gateway/v1",
     "key_env": ["KILOCODE_API_KEY"], "models": ["cohere/north-mini-code:free"],
     "tier": "keyless", "note": "key raises rate limit; works anonymously too"},
    {"name": "pollinations", "base": "https://text.pollinations.ai/openai",
     "key_env": None, "models": ["openai-fast", "openai"], "tier": "keyless"},
    {"name": "llm7", "base": "https://api.llm7.io/v1",
     "key_env": ["LLM7_API_KEY"], "models": ["codestral-latest", "gpt-oss:20b"],
     "tier": "keyless", "note": "keyless token 'unused' works; space calls 1-2s"},
    {"name": "ovh", "base": "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1",
     "key_env": None, "models": ["Meta-Llama-3_3-70B-Instruct", "Qwen3.5-9B"],
     "tier": "keyless", "note": "~1-2 req/min/model; rotate model ids"},

    # --- local: unlimited, private, zero cost -------------------------------
    {"name": "vllm", "base": "http://localhost:8000/v1", "key_env": None,
     "models": [DISCOVER], "tier": "local"},
    {"name": "ollama", "base": "http://localhost:11434/v1", "key_env": None,
     "models": [DISCOVER], "tier": "local"},
    {"name": "litellm", "base": "http://localhost:4000/v1", "key_env": None,
     "models": [DISCOVER], "tier": "local"},

    # --- keyed free tiers ---------------------------------------------------
    {"name": "groq", "base": "https://api.groq.com/openai/v1",
     "key_env": ["GROQ_API_KEY"],
     "models": ["openai/gpt-oss-120b", "llama-3.3-70b-versatile"], "tier": "free"},
    {"name": "gemini", "base": "https://generativelanguage.googleapis.com/v1beta/openai",
     "key_env": ["GEMINI_API_KEY", "GEMINI_API_KEY_ALT"],
     "models": ["gemini-2.5-flash-lite", "gemini-2.5-flash"], "tier": "free"},
    {"name": "huggingface", "base": "https://router.huggingface.co/v1",
     "key_env": ["HF_API_TOKEN"],
     "models": ["meta-llama/Llama-3.1-8B-Instruct:novita", "openai/gpt-oss-20b"],
     "tier": "free"},
    {"name": "deepinfra", "base": "https://api.deepinfra.com/v1/openai",
     "key_env": ["DEEPINFRA_API_KEY"],
     "models": ["meta-llama/Meta-Llama-3.1-8B-Instruct"], "tier": "free"},
    {"name": "cohere", "base": "https://api.cohere.ai/compatibility/v1",
     "key_env": ["COHERE_API_KEY"],
     "models": ["command-r7b-12-2024", "command-a-03-2025"], "tier": "free"},
    {"name": "mistral", "base": "https://api.mistral.ai/v1",
     "key_env": ["MISTRAL_API_KEY"],
     "models": ["ministral-8b-2512", "mistral-small-latest"], "tier": "free"},
    {"name": "publicai", "base": "https://api.publicai.co/v1",
     "key_env": ["PUBLICAI_API_KEY"],
     "models": ["swiss-ai/apertus-8b-instruct"], "tier": "free"},
    {"name": "cloudflare",
     "base": "https://api.cloudflare.com/client/v4/accounts/{account}/ai/v1",
     "key_env": ["CF_API_TOKEN"], "account_env": "CF_ACCOUNT_ID",
     "models": ["@cf/meta/llama-3.3-70b-instruct-fp8-fast"], "tier": "free"},
    {"name": "siliconflow", "base": "https://api.siliconflow.com/v1",
     "key_env": ["SILICONFLOW_API_KEY"],
     "models": ["Qwen/Qwen3-8B", "zai-org/GLM-5.3-Flash"], "tier": "free"},
    {"name": "zai", "base": "https://open.bigmodel.cn/api/paas/v4",
     "key_env": ["ZAI_API_KEY"], "models": ["glm-4.5-flash", "glm-4.7-flash"],
     "tier": "free"},
    {"name": "openrouter", "base": "https://openrouter.ai/api/v1",
     "key_env": ["OPENROUTER_API_KEY"],
     "models": ["nvidia/nemotron-3.5-lightning:free",
                "meta-llama/llama-3.3-70b-instruct:free"], "tier": "free"},
    {"name": "nous", "base": "https://inference-api.nousresearch.com/v1",
     "key_env": ["NOUS_API_KEY"],
     "models": ["reflection/beam-1.0-501b-a23b:free"], "tier": "free"},
    {"name": "sambanova", "base": "https://api.sambanova.ai/v1",
     "key_env": ["SAMBANOVA_API_KEY"],
     "models": ["Meta-Llama-3.3-70B-Instruct", "gpt-oss-120b"], "tier": "free"},
    {"name": "aimlapi", "base": "https://api.aimlapi.com/v1",
     "key_env": ["AIMLAPI_API_KEY"], "models": ["gpt-4o-mini"], "tier": "free"},
]

BY_NAME = {p["name"]: p for p in PROVIDERS}

# Local + keyless first: they cannot 429 our account or bill us.
TIER_ORDER = {"local": 0, "keyless": 1, "free": 2}


def _headers(key: Optional[str]) -> dict[str, str]:
    h = {"Content-Type": "application/json", "User-Agent": UA}
    if key:
        h["Authorization"] = f"Bearer {key}"
    # OpenRouter asks for attribution headers; harmless elsewhere.
    h["HTTP-Referer"] = "https://eltonaguiar.github.io/BESTIEJOB/"
    h["X-Title"] = "BESTIEJOB job scan"
    return h


def _base_for(provider: dict[str, Any]) -> Optional[str]:
    base = provider["base"]
    if "{account}" in base:
        acct = get_key(provider.get("account_env", "CF_ACCOUNT_ID"))
        if not acct:
            return None
        base = base.replace("{account}", acct)
    return base


def _discover(base: str, key: Optional[str]) -> list[str]:
    try:
        req = urllib.request.Request(f"{base}/models", headers=_headers(key))
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
    except Exception:
        return []
    items = data.get("data", data if isinstance(data, list) else [])
    ids = [m.get("id") for m in items if isinstance(m, dict) and m.get("id")]
    return [i for i in ids if not re.search(r"embed|rerank|whisper|tts", i, re.I)]


def _call(provider: dict[str, Any], model: str, prompt: str, system: str,
          max_tokens: int = 900, timeout: int = 60) -> str:
    base = _base_for(provider)
    if not base:
        raise RuntimeError("missing account id")
    key = None
    for env_name in provider.get("key_env") or []:
        key = get_key(env_name)
        if key:
            break
    if provider.get("key_env") and not key and not provider.get("keyless_token"):
        # keyless providers (kilocode/llm7) still work without one
        if provider["tier"] != "keyless":
            raise RuntimeError(f"{provider['key_env'][0]} not configured")

    body = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": prompt}],
        "temperature": 0.4,
        "max_tokens": max_tokens,
    }
    req = urllib.request.Request(f"{base}/chat/completions",
                                 data=json.dumps(body).encode(),
                                 headers=_headers(key or ("unused" if provider["tier"] == "keyless" else None)))
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read())
    content = (data["choices"][0]["message"].get("content") or "").strip()
    if not content:
        raise RuntimeError(f"{model}: empty content (raise max_tokens)")
    return content


def ask_one(provider: dict[str, Any], prompt: str, system: str,
            model_override: Optional[str] = None,
            max_tokens: int = 900) -> dict[str, Any]:
    """Try the provider's models in order; 400/404 advances, 429/402 stops."""
    started = time.time()
    models = [model_override] if model_override else list(provider["models"])
    if models == [DISCOVER]:
        base = _base_for(provider)
        key = next((get_key(e) for e in (provider.get("key_env") or []) if get_key(e)), None)
        models = _discover(base, key)[:2] if base else []
        if not models:
            return _fail(provider, "endpoint unreachable or advertises no chat models", started)
    last = ""
    for model in models:
        try:
            text = _call(provider, model, prompt, system, max_tokens)
            return {"provider": provider["name"], "tier": provider["tier"],
                    "model": model, "text": text,
                    "latency_s": round(time.time() - started, 2)}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:140].replace("\n", " ")
            last = f"{model}: HTTP {exc.code} {detail}"
            if exc.code in (400, 404):      # wrong model id for this account
                continue
            break
        except Exception as exc:            # noqa: BLE001 - one bad peer must not sink the run
            last = f"{model}: {type(exc).__name__} {str(exc)[:110]}"
            break
    return _fail(provider, last, started)


def _fail(provider: dict[str, Any], error: str, started: float) -> dict[str, Any]:
    return {"provider": provider["name"], "tier": provider["tier"],
            "error": error, "latency_s": round(time.time() - started, 2)}


def fan_out(prompt: str, system: str, only: Optional[set[str]] = None,
            limit: Optional[int] = None, workers: int = 4) -> list[dict[str, Any]]:
    pool = [p for p in PROVIDERS if only is None or p["name"] in only]
    pool.sort(key=lambda p: TIER_ORDER.get(p["tier"], 9))
    if limit:
        pool = pool[:limit]
    with futures.ThreadPoolExecutor(max_workers=max(1, min(workers, len(pool) or 1))) as ex:
        return list(ex.map(lambda p: ask_one(p, prompt, system), pool))


# ---------------------------------------------------------------------------
# Prompting
# ---------------------------------------------------------------------------
RECRUITER_SYSTEM = (
    "You are a blunt technical recruiter in Toronto who has read thousands of "
    "ServiceNow and Salesforce postings. Answer exactly what is asked, in the "
    "format asked for. No preamble, no praise, no hedging."
)

QUERY_PROMPT = """We run a daily job scan for {city}. These Adzuna `what` keywords are already used:

{existing}

Propose {count} ADDITIONAL `what` keyword phrases that would surface Toronto/GTA/Canada
ServiceNow, Salesforce, ITAM/ITSM/CMDB, or adjacent employer roles that those existing
keywords miss. Requirements:
- 2 to 4 words each, lowercase, no site: operators, no company names, no city names.
- Real job-title or module vocabulary a recruiter would type (e.g. product names,
  certifications, module names, delivery roles). Not marketing slogans.
- No duplicates of the existing list and no near-duplicates of each other.

Reply with ONLY a JSON array of strings, e.g. ["servicenow hrsd", "salesforce cpq"]."""

TRIAGE_SYSTEM = (
    "You classify job postings for a Toronto-focused ServiceNow/Salesforce job board. "
    "Judge only from the text given; if the text is too thin to judge, say low "
    "confidence. Output strict JSON only."
)


def build_existing_keywords() -> list[str]:
    """Existing Adzuna variants, read out of gap_scan.mjs so the lists cannot drift."""
    src = ROOT / "scripts" / "gap_scan.mjs"
    try:
        text = src.read_text(encoding="utf-8")
    except OSError:
        return []
    block = re.search(r"const ADZUNA_VARIANTS = \[(.*?)\];", text, re.S)
    if not block:
        return []
    return re.findall(r'what:\s*"([^"]+)"', block.group(1))


def parse_string_array(text: str) -> list[str]:
    """Pull a JSON array of strings out of a model reply, fenced or not."""
    for candidate in (text, re.sub(r"```(?:json)?|```", "", text)):
        try:
            data = json.loads(candidate.strip())
            if isinstance(data, list):
                return [str(x).strip() for x in data if isinstance(x, (str, int))]
        except json.JSONDecodeError:
            pass
    return [m.strip() for m in re.findall(r'"([^"\n]{3,60})"', text)]


BAD_KEYWORD = re.compile(
    r"site:|http|@|\.com|^\W|\b(toronto|canada|ontario|remote|jobs?)\b|"
    r"(salary|resume|apply|hiring now)", re.I)


def clean_keywords(raw: list[str], existing: list[str], limit: int) -> tuple[list[str], list[str]]:
    """Keep only keyword-shaped phrases; report what was dropped and why."""
    existing_lc = {e.lower() for e in existing}
    seen: set[str] = set()
    keep: list[str] = []
    dropped: list[str] = []
    for item in raw:
        kw = re.sub(r"\s+", " ", str(item)).strip().strip(".,;:'\"").lower()
        words = kw.split()
        if not (1 < len(words) <= 4) or len(kw) > 48:
            dropped.append(f"{kw} (length)")
            continue
        if BAD_KEYWORD.search(kw) or not re.match(r"^[a-z0-9][a-z0-9 .+#/-]*$", kw):
            dropped.append(f"{kw} (shape)")
            continue
        if kw in existing_lc or kw in seen:
            dropped.append(f"{kw} (duplicate)")
            continue
        seen.add(kw)
        keep.append(kw)
        if len(keep) >= limit:
            break
    return keep, dropped


# ---------------------------------------------------------------------------
# Subcommands
# ---------------------------------------------------------------------------
def cmd_ping(args) -> int:
    only = {s.strip() for s in args.only.split(",")} if args.only else None
    results = fan_out("Reply with exactly: PONG", "You are a health check.", only, args.limit)
    ok = 0
    print(f"{'provider':<13}{'tier':<9}{'status':<10}{'lat':>6}  model / error")
    print("-" * 88)
    for r in results:
        if "text" in r:
            ok += 1
            print(f"{r['provider']:<13}{r['tier']:<9}{'OK':<10}{r['latency_s']:>5}s  {r['model']}")
        else:
            print(f"{r['provider']:<13}{r['tier']:<9}{'FAIL':<10}{r['latency_s']:>5}s  {r['error'][:46]}")
    print(f"\n{ok}/{len(results)} peers answered")
    if args.json:
        print(json.dumps(results, indent=1))
    return 0 if ok else 1


def cmd_queries(args) -> int:
    existing = build_existing_keywords()
    prompt = QUERY_PROMPT.format(city=args.city, existing="\n".join(f"- {e}" for e in existing),
                                 count=args.count)
    if getattr(args, "focus", None):
        prompt += f"\n\nFocus especially on: {args.focus}"
    results = fan_out(prompt, RECRUITER_SYSTEM, _only(args), args.peers, workers=args.workers)
    answered = [r for r in results if "text" in r]
    if not answered:
        print("no peer answered — query generation skipped", file=sys.stderr)
        return 1

    proposals: dict[str, list[str]] = {}
    raw: list[str] = []
    for r in answered:
        items = parse_string_array(r["text"])
        proposals[f"{r['provider']}/{r['model']}"] = items
        raw.extend(items)

    keep, dropped = clean_keywords(raw, existing, args.count)
    payload = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "city": args.city,
        "peers_answered": len(answered),
        "peers_failed": len(results) - len(answered),
        "keywords": keep,
        "per_peer": proposals,
        "dropped": dropped[:40],
    }
    out = Path(args.out) if args.out else ROOT / "raw" / "ai_queries.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = out.with_suffix(".md")
    md.write_text(
        f"# AI panel keyword proposals — {payload['generated_at']}\n\n"
        f"{len(answered)}/{len(results)} peers answered · {len(keep)} keywords kept, "
        f"{len(dropped)} dropped\n\n"
        + "\n".join(f"- `{k}`" for k in keep)
        + ("\n\n## Dropped\n\n" + "\n".join(f"- {d}" for d in dropped[:40]) if dropped else "")
        + "\n", encoding="utf-8")

    print(f"# {len(answered)}/{len(results)} peers answered")
    for k in keep:
        print(f"  + {k}")
    if dropped:
        print(f"  ({len(dropped)} proposals dropped as duplicates/not keyword-shaped)")
    print(f"  -> {out}")
    return 0 if keep else 1


def cmd_triage(args) -> int:
    path = Path(args.input)
    if not path.exists():
        print(f"input not found: {path}", file=sys.stderr)
        return 2
    rows = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(rows, dict):
        rows = rows.get("jobs", [])
    rows = rows[: args.limit]
    if not rows:
        print("nothing to triage", file=sys.stderr)
        return 0

    out, answered = run_triage(rows, args)

    dest = Path(args.out_json) if args.out_json else ROOT / "raw" / "ai_triage.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    reviewed = sum(1 for o in out if o["ai_verdict"] != "unreviewed")
    print(f"reviewed {reviewed}/{len(rows)} rows by {answered} peers -> {dest}")
    return 0


def run_triage(rows: list[dict[str, Any]], args) -> tuple[list[dict[str, Any]], int]:
    """Ask the panel to classify rows; return (verdicts, peers_that_answered)."""
    compact = [
        {"i": i, "title": (r.get("title") or "")[:120],
         "company": (r.get("company") or "")[:60],
         "location": (r.get("location") or "")[:60],
         "excerpt": (r.get("excerpt") or r.get("note") or "")[:260]}
        for i, r in enumerate(rows)
    ]
    prompt = (
        "For each posting below, decide whether it is a genuine ServiceNow / Salesforce / "
        "platform-IT role a Toronto candidate should see (staffing-agency reposts count, "
        "pure sales/pre-sales roles do not).\n\n"
        f"POSTINGS:\n{json.dumps(compact, ensure_ascii=False)}\n\n"
        'Reply with ONLY a JSON array of objects: '
        '[{"i":0,"category":"servicenow|salesforce|other|reject","confidence":0.0-1.0,'
        '"reason":"<=12 words"}]. One object per posting.'
    )
    results = fan_out(prompt, TRIAGE_SYSTEM, _only(args), args.peers, workers=args.workers)
    answered = len([r for r in results if "text" in r])
    votes: dict[int, list[dict[str, Any]]] = {}
    for r in results:
        if "text" not in r:
            continue
        for item in _parse_object_array(r["text"]):
            try:
                idx = int(item.get("i"))
            except (TypeError, ValueError):
                continue
            item["provider"] = r["provider"]
            votes.setdefault(idx, []).append(item)

    out: list[dict[str, Any]] = []
    for i, row in enumerate(rows):
        tally: dict[str, int] = {}
        reasons: list[str] = []
        for v in votes.get(i, []):
            cat = str(v.get("category", "?"))
            tally[cat] = tally.get(cat, 0) + 1
            reason = str(v.get("reason") or "").strip()[:60]
            if reason:
                reasons.append(f"{v['provider']}: {reason}")
        verdict = max(tally, key=tally.get) if tally else "unreviewed"
        out.append({"url": row.get("url"), "title": row.get("title"),
                    "origin": row.get("origin"), "posted": row.get("posted"),
                    "ai_verdict": verdict, "ai_votes": tally,
                    "ai_voters": len(votes.get(i, [])), "ai_reasons": reasons[:3]})
    return out, answered


# --- undated inbox rows ----------------------------------------------------
INBOX_NAME_RE = re.compile(
    r"^(?P<slug>[a-z0-9._-]+)--(?P<date>\d{4}-\d{2}-\d{2})--v(?P<ver>\d+)\.md$", re.I)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
BARE_URL_RE = re.compile(r"https?://[^\s|)]+")
UNDATED_MARKERS = {"", "—", "–", "-", "?", "n/a", "na", "unknown", "tbd", "none"}
SEP_RE = re.compile(r"^:?-{2,}:?$")


def collect_inbox_rows(undated_only: bool = True) -> list[dict[str, Any]]:
    """Rows from inbox/*.md. Mirrors check_inbox.py's parsing, never invents a date."""
    inbox = ROOT / "inbox"
    rows: list[dict[str, Any]] = []
    if not inbox.exists():
        return rows
    for path in sorted(inbox.glob("*.md")):
        if path.name.startswith(("_", "TEMPLATE", "README")):
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line.strip().startswith("|"):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 5 or all(SEP_RE.fullmatch(c) for c in cells if c):
                continue
            posted = cells[0]
            if posted.lower() not in UNDATED_MARKERS and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", posted):
                continue                       # relative date — check_inbox's problem, not ours
            if undated_only and re.fullmatch(r"\d{4}-\d{2}-\d{2}", posted):
                continue
            link = MD_LINK_RE.search(line)
            if link:
                title, url = link.group(1), link.group(2)
            else:
                bare = BARE_URL_RE.search(line)
                if not bare:
                    continue
                url, title = bare.group(0), cells[1]
            note = cells[4] if "http" not in cells[4] else ""
            rows.append({"posted": posted, "title": title.strip(), "url": url.strip(),
                         "company": cells[2], "location": cells[3],
                         "note": note, "origin": path.name})
    return rows


def cmd_triage_inbox(args) -> int:
    """Second opinion on undated inbox rows before a human reads them.

    Writes a review report into inbox/ with a leading underscore, so both
    jobs_merge_inbox.py and check_inbox.py ignore it — the report must never
    become a submission and never gains a posting date of its own.
    """
    rows = collect_inbox_rows(undated_only=not args.dated_too)
    if args.limit:
        rows = rows[: args.limit]
    if not rows:
        print("no undated inbox rows to triage")
        return 0

    out, answered = run_triage(rows, args)
    stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    iso = stamp[:10]

    dest = Path(args.out_json) if args.out_json else ROOT / "raw" / "ai_triage.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps({"generated_at": stamp, "rows": out}, indent=2), encoding="utf-8")

    inbox = ROOT / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    ver = 1
    while (inbox / f"_ai-triage--{iso}--v{ver}.md").exists():
        ver += 1
    report = inbox / f"_ai-triage--{iso}--v{ver}.md"

    counts: dict[str, int] = {}
    for o in out:
        counts[o["ai_verdict"]] = counts.get(o["ai_verdict"], 0) + 1
    lines = [
        "---",
        "model: ai-panel",
        f"generated_at: {stamp}",
        "task: inbox-triage",
        "note: review report only — not a job submission; ignored by the merger",
        "---",
        "",
        f"# AI second opinion — {len(rows)} inbox rows ({answered} peers answered)",
        "",
        "Undated rows are legal: the merger skips them on purpose. This report only says",
        "whether each one is worth a human re-check, never what date it should carry.",
        "",
        "| verdict | votes | posted | role | source file | url |",
        "|---|---|---|---|---|---|",
    ]
    order = {"reject": 0, "unreviewed": 1, "other": 2, "salesforce": 3, "servicenow": 4}
    for o in sorted(out, key=lambda x: (order.get(x["ai_verdict"], 9), -x["ai_voters"])):
        votes = ", ".join(f"{k}:{v}" for k, v in sorted(o["ai_votes"].items())) or "—"
        lines.append(
            f"| {o['ai_verdict']} | {votes} | {o.get('posted') or '—'} | "
            f"{str(o.get('title') or '')[:70].replace('|', '/')} | "
            f"{o.get('origin') or ''} | {o.get('url') or ''} |"
        )
    rejected = [o for o in out if o["ai_verdict"] == "reject"]
    if rejected:
        lines += ["", "## Why the rejections were rejected", ""]
        for o in rejected[:15]:
            reason = "; ".join(o.get("ai_reasons") or []) or "no reason given"
            lines.append(f"- **{str(o.get('title') or '')[:70]}** — {reason}")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    summary = ", ".join(f"{k}={v}" for k, v in sorted(counts.items()))
    print(f"triaged {len(out)} inbox rows with {answered} peers ({summary})")
    print(f"  -> {report.relative_to(ROOT)}  (review report, not a submission)")
    return 0 if answered else 1


def _parse_object_array(text: str) -> list[dict[str, Any]]:
    for candidate in (text, re.sub(r"```(?:json)?|```", "", text)):
        start, end = candidate.find("["), candidate.rfind("]")
        if start == -1 or end <= start:
            continue
        try:
            data = json.loads(candidate[start:end + 1])
        except json.JSONDecodeError:
            continue
        if isinstance(data, list):
            return [d for d in data if isinstance(d, dict)]
    return []


def _only(args) -> Optional[set[str]]:
    return {s.strip() for s in args.only.split(",")} if getattr(args, "only", None) else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--only", help="comma-separated provider names")
        p.add_argument("--peers", type=int, default=6, help="max peers (default 6)")
        p.add_argument("--workers", type=int, default=4, help="parallel calls (default 4)")
        p.add_argument("--json", action="store_true")

    p_ping = sub.add_parser("ping", help="health-check every provider")
    p_ping.add_argument("--only")
    p_ping.add_argument("--limit", type=int, default=None)
    p_ping.add_argument("--json", action="store_true")
    p_ping.set_defaults(func=cmd_ping)

    p_q = sub.add_parser("queries", help="propose new search keywords")
    common(p_q)
    p_q.add_argument("--count", type=int, default=12)
    p_q.add_argument("--city", default="Toronto / GTA / Canada")
    p_q.add_argument("--focus", default=None,
                     help="extra steering, e.g. 'CSA/CAD and Platform Developer I certifications'")
    p_q.add_argument("--out", default=None)
    p_q.set_defaults(func=cmd_queries)

    p_t = sub.add_parser("triage", help="second-opinion classify job rows")
    common(p_t)
    p_t.add_argument("--input", required=True)
    p_t.add_argument("--out-json", default=None)
    p_t.add_argument("--limit", type=int, default=25)
    p_t.set_defaults(func=cmd_triage)

    p_ti = sub.add_parser("triage-inbox", help="second opinion on undated inbox rows")
    common(p_ti)
    p_ti.add_argument("--limit", type=int, default=25)
    p_ti.add_argument("--dated-too", action="store_true",
                      help="also review rows that already carry a posted date")
    p_ti.add_argument("--out-json", default=None)
    p_ti.set_defaults(func=cmd_triage_inbox)

    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
