# Design: Enhanced Referral Hunt for BESTIEJOB

**Date:** 2026-11-07
**Status:** Approved (design), pending implementation plan
**Approach chosen:** A — Tiered fetcher + per-ATS API adapters

## 1. Problem

`jobs.json` holds 3,256 postings across 258 distinct hosts. The user wants, for **every** posting:

1. A **direct link to an employee referral form or contact** (referral URL, referral portal, referral email/contact, or an explicit referral-program page).
2. Continued job-hunting coverage, using anti-bot bypass where needed.
3. The ability to "search those sources" — i.e. follow up on discovered referral sources.

### Why the existing script is insufficient

[`scripts/referral_hunt.py`](bestiejob/scripts/referral_hunt.py) already scans for referral indicators, but:

| Gap | Detail |
|---|---|
| **Capped at 80** | `MAX_JOBS = int(os.environ.get("MAX_JOBS", "80"))` — scans ~2.5% of the corpus |
| **Skips Adzuna entirely** | `if not url or "adzuna" in url: continue` — that is 847 postings (26% of corpus) |
| **Weak anti-bot** | Plain `requests` + UA rotation only; no TLS fingerprint, no JS rendering |
| **No ATS APIs** | Ignores the structured JSON already available from Greenhouse/Lever/Ashby/Workday/SmartRecruiters |
| **No follow-through** | Finds hints but never resolves where a referral link actually goes |
| **No persistence into `jobs.json`** | Writes only to `raw/` and `inbox/` |

### Host distribution (the actual target surface)

```
847  www.adzuna.ca                (aggregator, redirect wrappers)
593  job-boards.greenhouse.io     (ATS — has API)
528  ca.linkedin.com              (aggressive bot defence)
174  www.coinbase.com             (direct company career page)
103  jobs.ashbyhq.com             (ATS — has API)
 84  www.jobs.ca                  (aggregator)
 70  app.careerpuck.com           (aggregator)
 63  www.eluta.ca                 (aggregator)
 59  jobs.lever.co                (ATS — has API)
 57  boards.greenhouse.io         (ATS — has API)
 32  careers.airbnb.com           (direct)
 27  jobs.smartrecruiters.com     (ATS — has API)
 27  careers.datadoghq.com        (direct)
 23  www.asana.com                (direct)
 22  builtin.com                  (aggregator)
... 190 further hosts with <= 2 jobs each
```

Roughly **870 postings (27%)** are on ATS platforms with public JSON APIs. Another **~250** are direct company career pages. The remaining **~1,000** are aggregators of varying hostility.

## 2. Verified environment capabilities

Confirmed present on this machine:

| Library | Version | Purpose |
|---|---|---|
| `curl_cffi` | 0.16.3 | Chrome TLS/JA3 fingerprint impersonation — defeats most TLS-fingerprint-based bot checks |
| `playwright` | installed (python + node) | Real headless Chromium for JS challenges |
| `httpx` | 0.28.1 | HTTP/2 client, async capable |
| `bs4` | 4.14.3 | DOM parsing fallback |
| `lxml` | 6.1.1 | Fast HTML parsing |

Confirmed absent: `cloudscraper`, `selenium`, `tls_client`.

No API keys are assumed or required — this design is fully free to operate.

## 3. Architecture

```
                    ┌──────────────────────────────┐
                    │  jobs.json (3,256 postings)  │
                    └──────────────┬───────────────┘
                                   │
                          ┌────────▼─────────┐
                          │  Source Router   │  classify by host + source field
                          └────────┬─────────┘
              ┌────────────────────┼────────────────────┐
              │                    │                    │
      ┌───────▼────────┐  ┌────────▼────────┐  ┌────────▼─────────┐
      │ ATS Adapters   │  │ Tiered Fetcher  │  │ Aggregator       │
      │ (Tier 0)       │  │ (Tier 1-3)      │  │ Resolvers        │
      │                │  │                 │  │                  │
      │ greenhouse     │  │ 1. curl_cffi    │  │ adzuna redirect  │
      │ lever          │  │ 2. playwright   │  │ linkedin guest   │
      │ ashby          │  │ 3. httpx/reqs   │  │ careerpuck, etc. │
      │ workday        │  │                 │  │                  │
      │ smartrecruiters│  │                 │  │                  │
      └───────┬────────┘  └────────┬────────┘  └────────┬─────────┘
              └────────────────────┼────────────────────┘
                                   │  (HTML string | JSON dict)
                          ┌────────▼─────────┐
                          │ Referral         │  regex + DOM + JSON walk
                          │ Extractor        │
                          └────────┬─────────┘
                                   │
                          ┌────────▼─────────┐
                          │ Link Resolver    │  one-hop HEAD/GET on each
                          │ (optional, 1 hop)│  discovered referral URL
                          └────────┬─────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                    │
      ┌───────▼────────┐  ┌────────▼────────┐  ┌────────▼─────────┐
      │ raw/referral_  │  │ inbox/referral-  │  │ jobs.json        │
      │ hunt_<date>.   │  │ hunt--<date>.md  │  │ referral_info    │
      │ json           │  │                  │  │ field (additive) │
      └────────────────┘  └──────────────────┘  └──────────────────┘
```

### 3.1 Components

#### `scripts/referral/source_router.py`
Pure function `classify(job) -> SourceKind`. No I/O, fully unit-testable.

```python
class SourceKind(Enum):
    ATS_GREENHOUSE = "ats_greenhouse"
    ATS_LEVER      = "ats_lever"
    ATS_ASHBY      = "ats_ashby"
    ATS_WORKDAY    = "ats_workday"
    ATS_SR         = "ats_smartrecruiters"
    AGGREGATOR_ADZUNA = "aggregator_adzuna"
    AGGREGATOR_LINKEDIN = "aggregator_linkedin"
    AGGREGATOR_OTHER = "aggregator_other"
    COMPANY_DIRECT = "company_direct"
```

Rules: match on `urlsplit(url).netloc` first, then fall back to the `source` field prefix. Unknown host → `COMPANY_DIRECT`.

#### `scripts/referral/ats_adapters.py`
Wraps the API logic already proven in [`scripts/ats_board_sweep.py`](bestiejob/scripts/ats_board_sweep.py).

| Adapter | Endpoint | Referral payload available |
|---|---|---|
| greenhouse | `https://boards-api.greenhouse.io/v1/boards/<token>/jobs/<id>` | `content` (HTML body) — often contains "referral" text; no referral link field |
| lever | `https://api.lever.co/v0/postings/<site>/<id>` | `additional`, `lists`, `content` — body text |
| ashby | `https://api.ashbyhq.com/posting-api/job-board/<board>` | `descriptionHtml` |
| workday | `POST /wday/cxs/<tenant>/<site>/job/<path>` | `jobPostingInfo.jobDescription` |
| smartrecruiters | `https://api.smartrecruiters.com/v1/companies/<id>/postings/<postingId>` | `jobAd.sections` |

**Important finding:** ATS APIs expose the *job description body*, not a referral-form link. The referral value of this tier is:
- Structured body text → far cheaper and more reliable regex extraction than scraping the rendered page.
- The ATS **board host itself** yields the canonical referral entry point (e.g. Greenhouse hosts `/refer?token=...` for some employers).

So the ATS tier returns `(description_html, board_meta)` and the extractor treats both.

#### `scripts/referral/tiered_fetcher.py`
Ordered fallback with per-tier timeout budget and a circuit breaker.

```python
def fetch(url, *, kind: SourceKind) -> FetchResult:
    """Returns FetchResult(html|json, tier, status, elapsed)."""
```

Tier order (stop at first success where success = HTTP 2xx **and** body ≥ 500 bytes):

1. **Tier 1 — `curl_cffi`**: `impersonate="chrome124"`, `timeout=15`. Handles the large majority of company sites and Adzuna.
2. **Tier 2 — `playwright`** (headless Chromium): `timeout=30`, `wait_until="domcontentloaded"`, block images/fonts/media via route interception to cut time and bandwidth.
3. **Tier 3 — `httpx`**: final cheap attempt with browser-like headers.

A **host circuit breaker** records consecutive failures per netloc. After 3 consecutive hard failures (403/429/Cloudflare challenge detected on both Tier 1 and Tier 2), the host is quarantined for the remainder of the run and its jobs are recorded with `status: "blocked"` rather than burning 30s each.

Cloudflare challenge detection: response contains `cf-chl`, `Just a moment`, or `Attention Required` and HTTP in `{403, 503}`.

Anti-bot measures applied across tiers:
- 4 rotating desktop UA strings (existing list, extended with Chrome 131 / Edge 131).
- `Accept-Language: en-CA,en;q=0.9`, `Sec-Fetch-*` header set matching a real navigation.
- Randomised inter-request delay: `uniform(1.5, 3.5)`s, jittered per host so a single host never receives back-to-back hits faster than ~4s.
- `curl_cffi` session reuse per host to preserve cookies.

#### `scripts/referral/extractor.py`
Pure functions, no I/O — the most heavily tested module.

```python
def extract_from_html(html: str, base_url: str) -> list[ReferralHit]
def extract_from_json(payload: dict, base_url: str) -> list[ReferralHit]
```

`ReferralHit` shape:

```python
@dataclass
class ReferralHit:
    kind: str        # "url" | "email" | "form_field" | "text"
    value: str       # the URL, address, field name, or snippet
    pattern: str     # which rule fired
    confidence: float  # 0.0-1.0
    anchor_text: str | None
```

Extraction rules, ordered by confidence:

| Rule | Pattern (abridged) | Confidence |
|---|---|---|
| Referral URL in href/src | `href=["']([^"']*(?:refer\|referral\|refer-a\|employee-refer)[^"']*)` | 0.95 |
| Known referral portal hosts | `greenhouse.io/refer`, `lever.co/refer`, `ashbyhq.com/refer`, `myworkdayjobs.com/.*refer`, `jobs.smartrecruiters.com/.*refer` | 0.95 |
| Referral email | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}` within 200 chars of "referr" | 0.85 |
| Referral form field | `<input\|select\|textarea ... name\|id\|placeholder=[^>]*referr` | 0.80 |
| Explicit referral program text | `(?:employee\s+)?referr(?:al)?\s+(?:program\|bonus\|policy\|scheme)` | 0.60 |
| Generic referral mention | `referr(?:ed\|al\|er)` bare | 0.30 |

Dedup by normalised value; keep highest confidence. Cap at 15 hits per posting.

**Negative rules** (must suppress — these are not referral links):
- `refer` inside `preference`, `preferred`, `reference`, `referee`, `referendum`, `different`, `difference`.
- `referral` inside a privacy-policy or cookie-banner context.
- Job aggregator self-links pointing back to the aggregator's own referral-of-a-friend marketing.

These negative rules must be applied as word-boundary-aware exclusions, not naive substrings.

#### `scripts/referral/link_resolver.py`
For each `ReferralHit` with `kind == "url"`, issue exactly **one** hop: `HEAD` via `curl_cffi`, falling back to `GET` if `HEAD` returns 405/403. Record final URL, status, and whether it looks like a form (`<form` in a small body, or the word "refer" in the title). Strict cap: max 3 resolved links per posting so a single bad page cannot explode the run.

This satisfies the user's "search those sources" — the recorded `resolved_url` is where the referral form actually lives.

#### `scripts/enhanced_referral_hunt.py`
Orchestrator (the new entry point; the old `referral_hunt.py` stays untouched for audit history).

CLI:

```
python3 scripts/enhanced_referral_hunt.py \
    --jobs jobs.json \
    --out-dir raw \
    --limit 0                 # 0 = all
    --sources all             # or servicenow,salesforce
    --tiers curl,playwright,httpx
    --resolve-links           # enable one-hop resolution
    --concurrency 1           # keep at 1 for politeness; 4 max
    --resume                  # skip URLs already present in today's output
```

`--resume` matters: a full 3,256-posting sweep at 2–4s per posting is 2–4 hours. Resumability lets the run be interrupted and continued without re-fetching.

## 4. Data flow

1. Load and validate `jobs.json`; assert `jobs` is a list and each entry has a `url`.
2. Classify every posting (`source_router`).
3. Sort by priority: ServiceNow/Salesforce primary tags first, then ATS before aggregators, then newest `postedDate`.
4. For each posting: dispatch to adapter/fetcher → extract → optionally resolve links → append a record.
5. Every 50 postings, flush partial results to disk (crash safety) and print a progress line with counters.
6. On completion, write the final `raw/referral_hunt_<date>.json`, the `inbox/` markdown summary, and (unless `--no-write-jobs`) merge `referral_info` back into `jobs.json`.

### Output record

```json
{
  "id": "greenhouse:job-boards.greenhouse.io/neuraflash/jobs/6225939004",
  "title": "Forward Deployed Engineer, AI & Agentforce",
  "company": "NeuraFlash, Part of Accenture",
  "source": "greenhouse",
  "url": "https://job-boards.greenhouse.io/neuraflash/jobs/6225939004",
  "fetch": { "tier": "ats_api", "status": 200, "elapsed_ms": 412 },
  "referral_hits": [
    { "kind": "url", "value": "https://job-boards.greenhouse.io/neuraflash/refer?token=6225939004",
      "pattern": "known_referral_portal", "confidence": 0.95,
      "resolved": { "final_url": "https://job-boards.greenhouse.io/neuraflash/refer?token=6225939004",
                    "status": 200, "is_form": true } }
  ],
  "best_confidence": 0.95,
  "scanned_at": "2026-11-07T02:10:00Z"
}
```

### `jobs.json` schema change (additive only)

Add one optional key per job object:

```json
"referral_info": {
  "best_url": "https://...",
  "best_kind": "url",
  "confidence": 0.95,
  "hits": 1,
  "scanned_at": "2026-11-07T02:10:00Z"
}
```

Rules:
- **Never** overwrite any existing field.
- Only added when at least one hit has `confidence >= 0.6`.
- Postings with no hit get no key (keeps the file small; absence is meaningful).
- `tools/build_site.py` and `tools/jobs_consolidate.py` must be checked for tolerance of an unknown key before this ships. If they strictly validate keys, the site build step must be updated in the same change.

## 5. Error handling

| Failure | Handling |
|---|---|
| DNS / connection error | Log, mark `status: "error"`, continue |
| HTTP 404/410 | Mark `status: "gone"`; do not retry |
| HTTP 403/429 | Attempt next tier; if all fail → `status: "blocked"`, engage circuit breaker |
| Cloudflare challenge detected | Skip remaining tiers for that host, `status: "challenge"` |
| Body < 500 bytes with 2xx | Treat as soft failure, try next tier |
| Malformed JSON from ATS | Log raw snippet (truncated), `status: "bad_payload"` |
| `playwright` browser crash | Catch, mark `status: "browser_error"`, continue; do not restart the whole run |
| Disk write failure | Abort with a clear message — never silently lose collected results |
| Any single-posting exception | Caught per-iteration; one bad posting must never kill the sweep |

Per-posting try/except is mandatory. The run must always reach the final write.

## 6. Testing strategy

Unit tests (no network):
- `test_source_router.py` — every SourceKind and the unknown-host fallback, driven by real hosts from the corpus.
- `test_extractor.py` — the highest-value suite. Fixtures for: Greenhouse refer link, Lever refer link, Ashby refer link, Workday refer path, plain-text referral mention, referral email, form field, and **each negative rule** (preference/preferred/reference/different must produce zero hits).
- `test_link_resolver.py` — mocked transport; assert exactly one hop, and that 3-per-posting cap holds.

Integration tests (network, opt-in via env flag `REFERRAL_HUNT_LIVE=1`):
- One real posting per ATS adapter.
- One Adzuna posting (redirect resolution).
- One known-blocking host, asserting the circuit breaker trips and the run still completes.

Determinism: every test that touches the network is skipped unless the flag is set, so CI stays green and free.

Acceptance criteria for the implementation:
1. A full run over 3,256 postings completes without crashing and writes all three outputs.
2. `referral_info` appears on `jobs.json` only for postings with confidence ≥ 0.6.
3. Measured coverage: report the count of postings that produced a ≥0.6-confidence hit, per source kind and per tier, so the user can see which sources actually yielded referral links.
4. `python3 tools/build_site.py` and `python3 scripts/check_site_links.py` both still pass after the `jobs.json` change.

## 7. Explicit non-goals

- Not auto-submitting or auto-requesting referrals.
- Not scraping personal LinkedIn profiles for individual employees to contact. (That is a privacy and ToS line this design does not cross; LinkedIn is fetched only as guest-visible public job pages.)
- Not bypassing authenticated paywalls or logging into any service.
- Not introducing paid API dependencies.

## 8. Risks

| Risk | Mitigation |
|---|---|
| Run takes hours and gets killed | `--resume`, flush every 50, run in background with `nohup` |
| Adzuna/LinkedIn block at scale | Circuit breaker; report blocked count honestly rather than fabricating |
| `referral_info` breaks the site build | Verify builder tolerance before writing; acceptance criterion 4 |
| False positives pollute `jobs.json` | Confidence threshold 0.6 + comprehensive negative-rule test suite |
| Rate-limit / IP ban | Serial by default, 4s per-host floor, delays, session reuse |

## 9. Chosen-for-later (not in this implementation)

- Playwright-only rendering for JS-heavy company career pages that block both Tier 1 and Tier 3 — deferred until measured need, since it is ~30s per page.
- Following referral links two hops or deeper.
- Per-ATS referral-portal URL templates mined from a larger sample.
