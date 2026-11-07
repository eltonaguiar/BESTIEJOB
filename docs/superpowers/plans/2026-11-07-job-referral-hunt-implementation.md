# Enhanced Referral Hunt — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
>
> **Run every command with cwd = `bestiejob/`.** Paths below are relative to that directory.

**Goal:** Scan all 3,256 postings in `jobs.json` for a direct employee-referral artifact — a referral form URL, a referral email, or an application question/field that asks who referred the candidate — using ATS JSON APIs first (cheap, bot-free), then a tiered HTTP fetcher for everything else.

**Design doc:** [`docs/superpowers/specs/2026-11-07-job-referral-hunt-design.md`](../specs/2026-11-07-job-referral-hunt-design.md)

**Tech stack (all verified installed):** Python 3.11, `curl_cffi 0.16.3`, `playwright` (chromium present), `httpx 0.28.1`, `bs4 4.14.3`, `lxml 6.1.1`, `pytest 9.0.3`.

**Verified corpus distribution (from `jobs.json`, 3,256 rows):**

| Route | Count | Plan |
|---|---|---|
| `direct_other` | 958 | Tiered fetch of posting page |
| `adzuna` | 851 | 1 redirect hop, capped; else `skipped_aggregator` |
| `greenhouse` | 650 | **Greenhouse job API + `?questions=true`** (best channel) |
| `linkedin` | 530 | `skipped_aggregator` (auth-walled) |
| `ashby` | 103 | Ashby posting-api `descriptionHtml` |
| `workday` | 78 | Tiered fetch (curl_cffi → playwright) |
| `lever` | 59 | Lever posting API description |
| `smartrecruiters` | 27 | SmartRecruiters posting detail API |

**Safety constraint already verified:** [`tools/build_site.py`](../../tools/build_site.py:327) reads only `url`, `title`, `postedDate`, `company`, `location`, `source`. Adding a new `referral_info` key to jobs rows cannot change site output.

---

## Architecture

```
scripts/referral/
├── __init__.py
├── source_router.py          # URL host -> SourceKind
├── host_gate.py              # per-host circuit breaker + politeness delay
├── tiered_fetcher.py         # curl_cffi -> playwright -> httpx
├── ats_adapters.py           # ATS JSON APIs -> structured description + questions
├── extractor.py              # HTML/text -> list[ReferralHit] (scored, FP-controlled)
├── link_resolver.py          # relative href / form action -> absolute URL
└── enhanced_referral_hunt.py # orchestrator + CLI
tests/
├── fixtures/referral_page.html
└── test_referral_hunt.py
```

**Per-job flow:**

```
job -> source_router.classify()
     ├─ ATS_*  ──> ats_adapters.fetch()  ->  {description, questions[], canonical_url}
     │                └─ if no referral hit -> tiered_fetcher.fetch(canonical_url)
     ├─ ADZUNA ──> tiered_fetcher.fetch() (1 hop, capped) 
     ├─ LINKEDIN-> status=skipped_aggregator (no network)
     └─ DIRECT ──> tiered_fetcher.fetch()
                        ↓
                  extractor.extract(html, title, company)
                        ↓
                  link_resolver.absolutize(hits, base_url)
                        ↓
                  best hit -> ReferralInfo(kind,url,email,confidence,evidence)
```

**Result record (one per job, written to `raw/referral_hunt_<date>.json`):**

```json
{
  "job_id": "greenhouse:boards.greenhouse.io/neuraflash/jobs/123",
  "company": "NeuraFlash",
  "title": "ServiceNow Developer",
  "url": "https://boards.greenhouse.io/neuraflash/jobs/123",
  "route": "ats_greenhouse",
  "status": "found",
  "tier": "ats_api",
  "referral": {
    "kind": "form",
    "url": "https://boards.greenhouse.io/neuraflash/referrals/new",
    "email": null,
    "confidence": 1.0,
    "evidence": "application question: 'Were you referred by a current NeuraFlash employee?'",
    "all_hits": []
  },
  "checked_at": "2026-11-07T02:10:00Z"
}
```

**Status vocabulary:** `found` · `no_referral` · `blocked` · `error` · `skipped_aggregator` · `unroutable`.

---

## Task 1: Package + source router

**Files**
- Create: `scripts/referral/__init__.py`
- Create: `scripts/referral/source_router.py`

- [ ] **Step 1: Create the package**

```bash
mkdir -p scripts/referral tests/fixtures
printf '"""Referral-hunt package."""\n' > scripts/referral/__init__.py
```

- [ ] **Step 2: Write `source_router.py`**

```python
"""Map a job's URL to a fetch route.

Kept separate from the fetcher so tests can assert routing without a network
call, and so the orchestrator can skip whole families (LinkedIn) cheaply.
"""
from __future__ import annotations

from enum import Enum
from urllib.parse import urlsplit


class SourceKind(Enum):
    ATS_GREENHOUSE = "ats_greenhouse"
    ATS_LEVER = "ats_lever"
    ATS_ASHBY = "ats_ashby"
    ATS_WORKDAY = "ats_workday"
    ATS_SMARTRECRUITERS = "ats_smartrecruiters"
    AGGREGATOR_ADZUNA = "aggregator_adzuna"
    AGGREGATOR_LINKEDIN = "aggregator_linkedin"
    COMPANY_DIRECT = "company_direct"
    UNROUTABLE = "unroutable"


# Order matters: `jobs.smartrecruiters.com` must not be caught by a looser rule.
_HOST_RULES: tuple[tuple[str, SourceKind], ...] = (
    ("boards.greenhouse.io", SourceKind.ATS_GREENHOUSE),
    ("boards-api.greenhouse.io", SourceKind.ATS_GREENHOUSE),
    ("job-boards.greenhouse.io", SourceKind.ATS_GREENHOUSE),
    ("greenhouse.io", SourceKind.ATS_GREENHOUSE),
    ("jobs.lever.co", SourceKind.ATS_LEVER),
    ("api.lever.co", SourceKind.ATS_LEVER),
    ("lever.co", SourceKind.ATS_LEVER),
    ("jobs.ashbyhq.com", SourceKind.ATS_ASHBY),
    ("api.ashbyhq.com", SourceKind.ATS_ASHBY),
    ("ashbyhq.com", SourceKind.ATS_ASHBY),
    ("myworkdayjobs.com", SourceKind.ATS_WORKDAY),
    ("myworkdaysite.com", SourceKind.ATS_WORKDAY),
    ("jobs.smartrecruiters.com", SourceKind.ATS_SMARTRECRUITERS),
    ("api.smartrecruiters.com", SourceKind.ATS_SMARTRECRUITERS),
    ("smartrecruiters.com", SourceKind.ATS_SMARTRECRUITERS),
    ("adzuna.ca", SourceKind.AGGREGATOR_ADZUNA),
    ("adzuna.com", SourceKind.AGGREGATOR_ADZUNA),
    ("linkedin.com", SourceKind.AGGREGATOR_LINKEDIN),
)

# Routes where fetching the human page is known not to pay off.
NO_FETCH = frozenset({SourceKind.AGGREGATOR_LINKEDIN, SourceKind.UNROUTABLE})

ATS_KINDS = frozenset({
    SourceKind.ATS_GREENHOUSE,
    SourceKind.ATS_LEVER,
    SourceKind.ATS_ASHBY,
    SourceKind.ATS_WORKDAY,
    SourceKind.ATS_SMARTRECRUITERS,
})


def classify(job: dict) -> SourceKind:
    url = (job.get("url") or "").strip()
    if not url:
        return SourceKind.UNROUTABLE
    try:
        host = urlsplit(url).netloc.lower()
    except ValueError:
        return SourceKind.UNROUTABLE
    if not host:
        return SourceKind.UNROUTABLE
    host = host.split(":")[0]
    for suffix, kind in _HOST_RULES:
        if host == suffix or host.endswith("." + suffix):
            return kind
    if urlsplit(url).scheme not in ("http", "https"):
        return SourceKind.UNROUTABLE
    return SourceKind.COMPANY_DIRECT
```

- [ ] **Step 3: Smoke-test the router against the real corpus**

```bash
python3 - <<'PY'
import json, sys
sys.path.insert(0, ".")
from collections import Counter
from scripts.referral.source_router import classify

jobs = json.load(open("jobs.json"))["jobs"]
c = Counter(classify(j).value for j in jobs)
for k, v in c.most_common():
    print(f"{k:26s} {v}")
print("total", sum(c.values()))
PY
```

Expected: the five ATS kinds + adzuna + linkedin + company_direct sum to 3256, with `company_direct` ≈ 958 and `unroutable` 0.

- [ ] **Step 4: Commit**

```bash
git add scripts/referral/__init__.py scripts/referral/source_router.py
git commit -m "feat(referral): package skeleton and URL source router"
```

---

## Task 2: Host gate (circuit breaker + politeness)

**Files**
- Create: `scripts/referral/host_gate.py`
- Create: `tests/test_host_gate.py`

Rationale: a full sweep touches 958 arbitrary employer hosts. Without a breaker, one dead host costs N timeouts; without politeness, we trip Cloudflare on the first big one.

- [ ] **Step 1: Write `host_gate.py`**

```python
"""Per-host circuit breaker and politeness delay.

A sweep over ~1,000 arbitrary employer hosts will hit dead domains, parked
pages and WAFs. Three counters per host are enough to stop burning wall-clock
on a host that has already refused us.
"""
from __future__ import annotations

import random
import threading
import time


class HostGate:
    def __init__(self, *, max_failures: int = 4, quarantine_s: float = 300.0,
                 min_interval_s: float = 1.0) -> None:
        self.max_failures = max_failures
        self.quarantine_s = quarantine_s
        self.min_interval_s = min_interval_s
        self._lock = threading.Lock()
        self._failures: dict[str, int] = {}
        self._until: dict[str, float] = {}
        self._last: dict[str, float] = {}

    def available(self, host: str) -> bool:
        with self._lock:
            until = self._until.get(host, 0.0)
            return time.monotonic() >= until

    def wait(self, host: str) -> float:
        """Sleep the remainder of the polite interval. Returns seconds slept."""
        with self._lock:
            last = self._last.get(host)
            now = time.monotonic()
            delay = 0.0
            if last is not None:
                delay = (last + self.min_interval_s) - now
            if delay > 0:
                delay += random.uniform(0, 0.35)   # jitter, not a metronome
            self._last[host] = now + max(delay, 0.0)
        if delay > 0:
            time.sleep(delay)
        return max(delay, 0.0)

    def record(self, host: str, ok: bool) -> None:
        with self._lock:
            if ok:
                self._failures.pop(host, None)
                return
            n = self._failures.get(host, 0) + 1
            self._failures[host] = n
            if n >= self.max_failures:
                self._until[host] = time.monotonic() + self.quarantine_s

    def is_quarantined(self, host: str) -> bool:
        with self._lock:
            return time.monotonic() < self._until.get(host, 0.0)

    def failures(self, host: str) -> int:
        with self._lock:
            return self._failures.get(host, 0)
```

- [ ] **Step 2: Write `tests/test_host_gate.py`** (no network, no sleeps)

```python
import time

from scripts.referral.host_gate import HostGate


def test_quarantines_after_max_failures():
    gate = HostGate(max_failures=3, quarantine_s=60, min_interval_s=0)
    for _ in range(2):
        gate.record("dead.example", ok=False)
    assert gate.available("dead.example")
    gate.record("dead.example", ok=False)
    assert not gate.available("dead.example")
    assert gate.is_quarantined("dead.example")


def test_success_resets_counter():
    gate = HostGate(max_failures=2, quarantine_s=60, min_interval_s=0)
    gate.record("flaky.example", ok=False)
    gate.record("flaky.example", ok=True)
    gate.record("flaky.example", ok=False)
    assert gate.available("flaky.example")


def test_wait_is_zero_when_interval_already_elapsed():
    gate = HostGate(min_interval_s=0.0)
    assert gate.wait("a.example") == 0.0
    assert gate.wait("a.example") == 0.0


def test_wait_enforces_interval():
    gate = HostGate(min_interval_s=0.2)
    gate.wait("b.example")
    slept = gate.wait("b.example")
    assert slept > 0.1
```

- [ ] **Step 3: Run**

```bash
python3 -m pytest tests/test_host_gate.py -q
```

Expected: 4 passed.

- [ ] **Step 4: Commit**

```bash
git add scripts/referral/host_gate.py tests/test_host_gate.py
git commit -m "feat(referral): per-host circuit breaker and politeness gate"
```

---

## Task 3: Link resolver

**Files**
- Create: `scripts/referral/link_resolver.py`
- Create: `tests/test_link_resolver.py`

- [ ] **Step 1: Write `link_resolver.py`**

```python
"""Turn a relative href / form action into an absolute, deduped URL."""
from __future__ import annotations

from urllib.parse import urljoin, urlsplit, urlunsplit, parse_qsl, urlencode

TRACKING_PREFIXES = ("utm_", "gh_src", "lever-source", "ref_", "source=")


def absolutize(href: str, base: str) -> str | None:
    """Resolve `href` against `base`. Returns None for non-http(s) results."""
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "#")):
        return None
    try:
        absolute = urljoin(base, href)
        parts = urlsplit(absolute)
    except ValueError:
        return None
    if parts.scheme not in ("http", "https") or not parts.netloc:
        return None
    return absolute


def strip_tracking(url: str) -> str:
    """Drop utm_* and ATS source params so two hops to one form dedupe."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return url
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if not any(k.lower().startswith(p) for p in ("utm_", "gh_src",
                                                         "lever-source",
                                                         "ref_", "src", "source"))]
    return urlunsplit((parts.scheme, parts.netloc, parts.path,
                       urlencode(kept), ""))


def same_target(a: str, b: str) -> bool:
    """Compare ignoring scheme, trailing slash, tracking params and fragment."""
    def norm(u: str) -> str:
        p = urlsplit(strip_tracking(u))
        return f"{p.netloc.lower().removeprefix('www.')}{p.path.rstrip('/')}".lower()
    return norm(a) == norm(b)


def dedupe(urls: list[str]) -> list[str]:
    out: list[str] = []
    for u in urls:
        if not any(same_target(u, seen) for seen in out):
            out.append(u)
    return out
```

- [ ] **Step 2: Write `tests/test_link_resolver.py`**

```python
from scripts.referral.link_resolver import absolutize, dedupe, same_target, strip_tracking


def test_relative_path_resolves_against_posting():
    got = absolutize("/referrals/new", "https://boards.greenhouse.io/acme/jobs/1")
    assert got == "https://boards.greenhouse.io/referrals/new"


def test_query_only_href_resolves():
    got = absolutize("?refer=1", "https://jobs.lever.co/acme/abc")
    assert got == "https://jobs.lever.co/acme/abc?refer=1"


def test_rejects_mailto_and_javascript():
    assert absolutize("mailto:a@b.com", "https://x.test/") is None
    assert absolutize("javascript:void(0)", "https://x.test/") is None


def test_strip_tracking_removes_utm_keeps_meaning():
    got = strip_tracking("https://x.test/refer?utm_source=li&team=abc")
    assert "utm_source" not in got
    assert "team=abc" in got


def test_same_target_ignores_www_slash_and_utm():
    a = "https://www.x.test/refer/?utm_medium=email"
    b = "https://x.test/refer"
    assert same_target(a, b)


def test_dedupe_collapses_tracking_variants():
    urls = ["https://x.test/refer?utm_source=a", "https://x.test/refer",
            "https://x.test/other"]
    assert len(dedupe(urls)) == 2
```

- [ ] **Step 3: Run**

```bash
python3 -m pytest tests/test_link_resolver.py -q
```

Expected: 6 passed.

- [ ] **Step 4: Commit**

```bash
git add scripts/referral/link_resolver.py tests/test_link_resolver.py
git commit -m "feat(referral): URL absolutiser, tracking stripper, dedupe"
```

---

## Task 4: Extractor (the false-positive-critical piece)

**Files**
- Create: `scripts/referral/extractor.py`
- Create: `tests/fixtures/referral_page.html`
- Create: `tests/test_extractor.py`

This is the task most likely to produce garbage. The single biggest hazard is the English phrase **"refer to"** ("refer to the job description", "referred to as"), which appears on thousands of legitimate postings. It must be scored to zero.

- [ ] **Step 1: Write `tests/fixtures/referral_page.html`**

```html
<!doctype html>
<html><body>
<h1>ServiceNow Developer</h1>
<p>Please refer to the job description for full requirements.</p>
<p>This role is referred to as a Platform Developer internally.</p>
<p>Our employee referral program pays $2,000. Refer a friend today.</p>
<a href="/referrals/new?job=991">Refer a friend</a>
<a href="mailto:referrals@acme.test?subject=Referral%20for%20ServiceNow%20Developer">
  Email us a referral</a>
<a href="mailto:careers@acme.test">General careers inbox</a>
<form action="/employee-referral/submit">
  <input name="referrer_name" type="text">
  <select name="how_did_you_hear"><option>Referral</option></select>
</form>
</body></html>
```

- [ ] **Step 2: Write `extractor.py`**

```python
"""Find a direct employee-referral artifact in a posting.

Scoring exists because English reuses the word "refer" for unrelated things:
"refer to the job description", "referred to as", "referral to a specialist".
Every pattern below is either an unambiguous referral artifact (a form field
named `referrer`, a `mailto:referrals@`) or is scored low enough that a single
ambiguous hit never wins.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup

KINDS = ("form", "email", "page", "question")

# --- Negative patterns: force confidence to 0 -----------------------------
# `refer to` is the classic trap. Also "referral" in clinical/legal prose.
_NEGATIVE = re.compile(
    r"\brefer(?:red|ring)?\s+to\b"          # refer to the JD / referred to as
    r"|\breferral\s+to\s+(?:a\s+)?(?:specialist|clinician|physician|program\b)"
    r"|\bplease\s+refer\b",
    re.I,
)

# --- Positive text signals, with their base confidence --------------------
_TEXT_SIGNALS: tuple[tuple[re.Pattern[str], float, str], ...] = (
    (re.compile(r"\brefer\s+a\s+friend\b", re.I), 0.95, "refer a friend"),
    (re.compile(r"\brefer\s+someone\b", re.I), 0.9, "refer someone"),
    (re.compile(r"\bemployee\s+referral\s+(?:program|scheme|bonus)\b", re.I), 0.9,
     "employee referral program"),
    (re.compile(r"\breferral\s+bonus\b", re.I), 0.85, "referral bonus"),
    (re.compile(r"\breferral\s+(?:link|code|form|portal)\b", re.I), 0.9,
     "referral link/code/form"),
    (re.compile(r"\bknow\s+someone\s+who\b", re.I), 0.7, "know someone who"),
    (re.compile(r"\bhow\s+did\s+you\s+hear\b", re.I), 0.6, "how did you hear"),
    (re.compile(r"\bwere\s+you\s+referred\b", re.I), 1.0, "were you referred"),
    (re.compile(r"\bname\s+of\s+(?:the\s+)?(?:employee|referrer)\b", re.I), 0.95,
     "name of referrer"),
    (re.compile(r"\breferral\b", re.I), 0.35, "bare 'referral'"),
)

_EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
_REFERRAL_EMAIL_LOCAL = re.compile(
    r"^(refer|referral|referrals|referafriend|refer-a-friend|employee\.?referral|"
    r"talent\.?referral|internal\.?referral)", re.I)
_REFERRAL_PATH = re.compile(
    r"(?:^|/)(?:refer|referral|referrals|refer-a-friend|employee-referral|"
    r"employee_referral|internal-referral|internal_referral|referral-program)"
    r"(?:/|$|\?)", re.I)
_REFERRAL_FIELD = re.compile(
    r"referr|referral|ref_code|refcode|referred_by|referrer_name|how_did_you_hear",
    re.I)


@dataclass
class ReferralHit:
    kind: str                      # form | email | page | question
    value: str                     # absolute URL (resolved later) or email
    pattern: str
    confidence: float
    evidence: str = ""
    attrs: dict = field(default_factory=dict)


def _snippet(text: str, start: int, end: int, radius: int = 110) -> str:
    lo = max(0, start - radius)
    hi = min(len(text), end + radius)
    return re.sub(r"\s+", " ", text[lo:hi]).strip()


def _score_text(text: str) -> tuple[float, str, str]:
    """Best text-only referral signal in a blob. Returns (conf, pattern, snippet)."""
    if not text:
        return 0.0, "", ""
    if _NEGATIVE.search(text) and not re.search(
            r"\brefer\s+a\s+friend|\bemployee\s+referral\s+program", text, re.I):
        # "refer to" only: the rest of this blob cannot be trusted for a bare
        # `referral` hit, but explicit artifacts were handled by callers.
        pass
    best = (0.0, "", "")
    for rx, conf, label in _TEXT_SIGNALS:
        m = rx.search(text)
        if not m:
            continue
        if conf < best[0]:
            continue
        window = text[max(0, m.start() - 160): m.end() + 160]
        if _NEGATIVE.search(window) and conf < 0.8:
            continue                     # ambiguous and sitting next to "refer to"
        best = (conf, label, _snippet(text, m.start(), m.end()))
    return best


def extract(html: str, *, title: str = "", company: str = "",
            structured_questions: list[str] | None = None) -> list[ReferralHit]:
    """Extract scored referral hits from a posting page or ATS payload."""
    hits: list[ReferralHit] = []
    if structured_questions:
        for q in structured_questions:
            conf, label, snip = _score_text(q or "")
            if conf >= 0.8:
                hits.append(ReferralHit("question", "", f"ats question: {label}",
                                        conf, f"application question: {q[:200]}"))

    if not html:
        return _rank(hits)

    soup = BeautifulSoup(html, "lxml")

    # 1. Anchors whose href or text looks like a referral target.
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        text = a.get_text(" ", strip=True)
        conf, label, snip = _score_text(f"{text} {href}")
        path_hit = bool(_REFERRAL_PATH.search(href))
        if path_hit:
            conf = max(conf, 0.9)
            label = label or "referral path"
        if conf >= 0.5:
            hits.append(ReferralHit("page", href, label or "anchor",
                                    min(conf, 1.0), snip or text[:160],
                                    {"href": href}))

    # 2. mailto: referral inboxes.
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if not href.lower().startswith("mailto:"):
            continue
        addr = href[7:].split("?")[0].strip()
        for m in _EMAIL_RE.finditer(addr):
            email = m.group(0)
            local = email.split("@")[0]
            if _REFERRAL_EMAIL_LOCAL.search(local) or "refer" in href.lower():
                hits.append(ReferralHit("email", email, "mailto referral inbox",
                                        1.0, f"mailto link: {href[:160]}",
                                        {"href": href}))
                break

    # 3. Form fields and form actions.
    for tag in soup.find_all(["input", "select", "textarea"]):
        name = f"{tag.get('name') or ''} {tag.get('id') or ''} " \
               f"{tag.get('placeholder') or ''}"
        if _REFERRAL_FIELD.search(name):
            form = tag.find_parent("form")
            action = (form.get("action") if form else "") or ""
            hits.append(ReferralHit(
                "form", action, "referral form field", 1.0,
                f"field {tag.name} name={name.strip()[:80]}", {"action": action}))
    for form in soup.find_all("form", action=True):
        action = form["action"].strip()
        if _REFERRAL_PATH.search(action):
            hits.append(ReferralHit("form", action, "referral form action", 0.95,
                                    f"<form action='{action[:120]}'>",
                                    {"action": action}))

    # 4. Plain-text fallback over the visible copy.
    text = soup.get_text(" ", strip=True)
    conf, label, snip = _score_text(text)
    if conf >= 0.85:
        hits.append(ReferralHit("page", "", f"page text: {label}", conf, snip))

    return _rank(hits)


def _rank(hits: list[ReferralHit]) -> list[ReferralHit]:
    kind_bonus = {"form": 0.05, "email": 0.04, "question": 0.03, "page": 0.0}
    for h in hits:
        h.confidence = round(min(1.0, h.confidence + kind_bonus.get(h.kind, 0.0)), 3)
    hits.sort(key=lambda h: (-h.confidence, h.kind, h.value))
    out, seen = [], set()
    for h in hits:
        key = (h.kind, h.value.lower(), h.pattern)
        if key in seen:
            continue
        seen.add(key)
        out.append(h)
    return out[:12]


def best(hits: list[ReferralHit], *, threshold: float = 0.75) -> ReferralHit | None:
    for h in hits:
        if h.confidence >= threshold:
            return h
    return None
```

- [ ] **Step 3: Write `tests/test_extractor.py`**

```python
from pathlib import Path

from scripts.referral.extractor import best, extract

FIXTURE = Path(__file__).parent / "fixtures" / "referral_page.html"
HTML = FIXTURE.read_text(encoding="utf-8")


def test_finds_refer_a_friend_anchor():
    hits = extract(HTML)
    anchors = [h for h in hits if h.pattern in ("refer a friend", "referral path")
               or "refer a friend" in h.evidence.lower()]
    assert anchors, [h.pattern for h in hits]
    assert any(h.kind == "page" for h in hits)


def test_finds_referral_mailto_inbox():
    emails = [h.value for h in extract(HTML) if h.kind == "email"]
    assert "referrals@acme.test" in emails
    assert "careers@acme.test" not in emails     # not a referral inbox


def test_finds_referral_form_field():
    forms = [h for h in extract(HTML) if h.kind == "form"]
    assert forms, "referrer_name field must be detected"
    assert forms[0].confidence >= 0.9


def test_refer_to_the_job_description_is_not_a_hit():
    html = "<html><body><p>Please refer to the job description for details. " \
           "This is referred to as a level 3 role.</p></body></html>"
    assert best(extract(html)) is None


def test_bare_referral_alone_below_threshold():
    html = "<html><body><p>Referral to a specialist may be required.</p></body></html>"
    assert best(extract(html)) is None


def test_ats_question_hit_is_top_confidence():
    hits = extract("", structured_questions=[
        "Were you referred by a current employee? If so, please provide their name."])
    top = best(hits)
    assert top is not None
    assert top.kind == "question"
    assert top.confidence >= 0.9


def test_generic_how_did_you_hear_is_weak_but_present():
    hits = extract("", structured_questions=["How did you hear about this role?"])
    assert any(h.pattern.endswith("how did you hear") for h in hits)
    assert best(hits) is None          # 0.6 + 0.03 bonus < 0.75 threshold


def test_empty_input_returns_empty():
    assert extract("") == []
    assert extract("", structured_questions=[]) == []
```

- [ ] **Step 4: Run**

```bash
python3 -m pytest tests/test_extractor.py -q
```

Expected: 8 passed. If `test_refer_to_the_job_description_is_not_a_hit` fails, the negative filter is too weak — fix the scorer, not the test.

- [ ] **Step 5: Commit**

```bash
git add scripts/referral/extractor.py tests/test_extractor.py tests/fixtures/referral_page.html
git commit -m "feat(referral): scored referral extractor with refer-to false-positive guard"
```

---

## Task 5: Tiered fetcher

**Files**
- Create: `scripts/referral/tiered_fetcher.py`

**Threading constraint:** Playwright's sync API is not thread-safe. All Playwright work is serialised behind a module lock; tiers 1 and 3 are thread-safe.

- [ ] **Step 1: Write `tiered_fetcher.py`**

```python
"""Escalating HTTP fetcher: curl_cffi -> playwright -> httpx.

Most employer sites answer a TLS-fingerprinted GET. The ones that don't are
usually JS-rendered, which is what the browser tier is for. httpx is the last
resort for plain hosts that dislike curl_cffi's headers.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass

from .host_gate import HostGate

UA_POOL = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
)

_PW_LOCK = threading.Lock()
_PW_BROWSER = None


@dataclass
class FetchResult:
    html: str | None
    tier: str            # curl_cffi | playwright | httpx | none
    status: int
    url: str
    detail: str = ""

    @property
    def ok(self) -> bool:
        return bool(self.html)


def _tier_curl(url: str, timeout: float, host: str, gate: HostGate) -> FetchResult:
    try:
        from curl_cffi import requests as cr
    except ImportError:
        return FetchResult(None, "curl_cffi", 0, url, "curl_cffi missing")
    try:
        r = cr.get(url, impersonate="chrome", timeout=timeout,
                   allow_redirects=True,
                   headers={"Accept-Language": "en-CA,en;q=0.9"})
    except Exception as exc:                                    # noqa: BLE001
        return FetchResult(None, "curl_cffi", 0, url, type(exc).__name__)
    if r.status_code == 200 and r.text:
        gate.record(host, True)
        return FetchResult(r.text, "curl_cffi", 200, str(r.url))
    return FetchResult(None, "curl_cffi", r.status_code, url,
                       f"HTTP {r.status_code}")


def _tier_httpx(url: str, timeout: float, host: str, gate: HostGate) -> FetchResult:
    try:
        import httpx
    except ImportError:
        return FetchResult(None, "httpx", 0, url, "httpx missing")
    try:
        with httpx.Client(http2=True, follow_redirects=True,
                          timeout=timeout,
                          headers={"User-Agent": UA_POOL[0],
                                   "Accept-Language": "en-CA,en;q=0.9"}) as client:
            r = client.get(url)
    except Exception as exc:                                    # noqa: BLE001
        return FetchResult(None, "httpx", 0, url, type(exc).__name__)
    if r.status_code == 200 and r.text:
        return FetchResult(r.text, "httpx", 200, str(r.url))
    return FetchResult(None, "httpx", r.status_code, url, f"HTTP {r.status_code}")


def _browser():
    global _PW_BROWSER
    from playwright.sync_api import sync_playwright
    if _PW_BROWSER is None:
        pw = sync_playwright().start()
        _PW_BROWSER = (pw, pw.chromium.launch(headless=True))
    return _PW_BROWSER


def _tier_playwright(url: str, timeout_ms: int) -> FetchResult:
    with _PW_LOCK:                     # sync API is not thread-safe
        try:
            _, browser = _browser()
            ctx = browser.new_context(
                user_agent=UA_POOL[0], locale="en-CA",
                viewport={"width": 1366, "height": 900})
            page = ctx.new_page()
            page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
            page.wait_for_timeout(1200)          # let client-side hydration settle
            html = page.content()
            final = page.url
            ctx.close()
        except Exception as exc:                                # noqa: BLE001
            return FetchResult(None, "playwright", 0, url, type(exc).__name__)
    if html:
        return FetchResult(html, "playwright", 200, final)
    return FetchResult(None, "playwright", 200, url, "empty document")


def fetch(url: str, *, gate: HostGate, timeout: float = 20.0,
          allow_playwright: bool = True) -> FetchResult:
    """Try each tier in order, stopping at the first non-empty document."""
    from urllib.parse import urlsplit
    host = urlsplit(url).netloc.lower()
    if gate.is_quarantined(host):
        return FetchResult(None, "none", 0, url, "host quarantined")
    gate.wait(host)

    first = _tier_curl(url, timeout, host, gate)
    if first.ok:
        return first

    if first.status in (301, 302, 303, 307, 308):
        gate.record(host, True)         # redirect handled by allow_redirects
    else:
        gate.record(host, False)

    if allow_playwright and not gate.is_quarantined(host):
        pw = _tier_playwright(url, int(timeout * 1500))
        if pw.ok:
            return pw
        last_ts = pw
    else:
        last_ts = first

    third = _tier_httpx(url, timeout, host, gate)
    if third.ok:
        return third
    return FetchResult(None, "none", third.status or last_ts.status, url,
                       f"{first.detail} | {third.detail}")
```

- [ ] **Step 2: Smoke-test the fetcher against one known-good ATS page**

```bash
python3 - <<'PY'
import sys; sys.path.insert(0, ".")
from scripts.referral.host_gate import HostGate
from scripts.referral.tiered_fetcher import fetch

r = fetch("https://boards.greenhouse.io/geotab", gate=HostGate())
print("tier:", r.tier, "status:", r.status, "len:", len(r.html or ""))
print("detail:", r.detail)
PY
```

Expected: `tier: curl_cffi  status: 200  len: >5000`. A `playwright` tier also counts as a pass.

- [ ] **Step 3: Commit**

```bash
git add scripts/referral/tiered_fetcher.py
git commit -m "feat(referral): tiered fetcher (curl_cffi -> playwright -> httpx)"
```

---

## Task 6: ATS adapters

**Files**
- Create: `scripts/referral/ats_adapters.py`
- Create: `tests/test_ats_adapters.py`

**This is the highest-yield task.** Greenhouse's job endpoint with `?questions=true` returns the actual application questions — so a posting whose form asks *"Were you referred by a current employee?"* is detectable with **zero** browser traffic. Endpoint shapes below are copied from verified working code in [`scripts/ats_board_sweep.py`](../../scripts/ats_board_sweep.py:470).

- [ ] **Step 1: Write `ats_adapters.py`**

```python
"""Pull a posting's description and application questions from its ATS API.

Every endpoint here is public, unauthenticated and returns the posting body as
a string. That makes the ATS channel both the cheapest and the most reliable
source of a referral signal: Greenhouse's `?questions=true` literally returns
the application form, so "were you referred by an employee?" is answerable
without fetching a single web page.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from .source_router import SourceKind


@dataclass
class AtsPayload:
    description_html: str = ""
    questions: list[str] = field(default_factory=list)
    canonical_url: str = ""
    detail: str = ""
    ok: bool = False


def _api_get(url: str, timeout: float = 20.0) -> dict | list | None:
    try:
        from curl_cffi import requests as cr
        r = cr.get(url, impersonate="chrome", timeout=timeout)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:                                            # noqa: BLE001
        return None


# --------------------------------------------------------------------------
# URL shapes
#   greenhouse  boards.greenhouse.io/<token>/jobs/<id>
#               job-boards.greenhouse.io/<token>/jobs/<id>
#               boards-api.greenhouse.io/v1/boards/<token>/jobs/<id>
#   lever       jobs.lever.co/<site>/<uuid>
#   ashby       jobs.ashbyhq.com/<token>/<uuid>
#   smartrec    jobs.smartrecruiters.com/<company>/<postingId>
#   workday     <tenant>.wd<N>.myworkdayjobs.com/en-US/<site>/job/<path>
# --------------------------------------------------------------------------
GH_PATH = re.compile(r"/([^/]+)/jobs/(\d+)")
GH_API_PATH = re.compile(r"/v1/boards/([^/]+)/jobs/(\d+)")
LEVER_PATH = re.compile(r"/([^/]+)/([0-9a-f-]{20,})", re.I)
ASHBY_PATH = re.compile(r"/([^/]+)/([0-9a-f-]{20,})", re.I)
SR_PATH = re.compile(r"/([^/]+)/(\d{6,})")
WD_HOST = re.compile(r"^(?P<tenant>[^.]+)\.(?P<wd>wd\d+)\.myworkdayjobs\.com$")


def _greenhouse(url: str) -> AtsPayload:
    parts = urlsplit(url)
    m = GH_API_PATH.search(parts.path) or GH_PATH.search(parts.path)
    if not m:
        return AtsPayload(detail="unparsed greenhouse url")
    token, job_id = m.group(1), m.group(2)
    data = _api_get("https://boards-api.greenhouse.io/v1/boards/"
                    f"{token}/jobs/{job_id}?questions=true")
    if not isinstance(data, dict):
        return AtsPayload(detail="greenhouse api miss")
    questions: list[str] = []
    for q in data.get("questions") or []:
        label = (q.get("label") or "").strip()
        if label:
            questions.append(label)
        for fld in q.get("fields") or []:
            if fld.get("name"):
                questions.append(f"{label} :: {fld['name']}")
    content = data.get("content") or ""
    content = content.replace("<", "<").replace(">", ">") \
                     .replace("&", "&").replace(""", '"') \
                     .replace("'", "'")
    return AtsPayload(
        description_html=content,
        questions=questions,
        canonical_url=data.get("absolute_url") or url,
        detail=f"{len(questions)} application questions",
        ok=True)


def _lever(url: str) -> AtsPayload:
    m = LEVER_PATH.search(urlsplit(url).path)
    if not m:
        return AtsPayload(detail="unparsed lever url")
    site, posting_id = m.group(1), m.group(2)
    data = _api_get(f"https://api.lever.co/v0/postings/{site}/{posting_id}")
    if not isinstance(data, dict):
        return AtsPayload(detail="lever api miss")
    body = " ".join(filter(None, [
        data.get("description") or "",
        data.get("descriptionPlain") or "",
        *(l.get("content") or "" for l in (data.get("lists") or [])),
        data.get("additional") or "",
    ]))
    return AtsPayload(description_html=body,
                      canonical_url=data.get("hostedUrl") or url,
                      detail="lever posting detail", ok=True)


def _ashby(url: str) -> AtsPayload:
    m = ASHBY_PATH.search(urlsplit(url).path)
    if not m:
        return AtsPayload(detail="unparsed ashby url")
    token = m.group(1)
    data = _api_get("https://api.ashbyhq.com/posting-api/job-board/"
                    f"{token}?includeCompensation=true")
    if not isinstance(data, dict):
        return AtsPayload(detail="ashby board miss")
    target = m.group(2).lower()
    for j in data.get("jobs") or []:
        if target in (j.get("jobUrl") or "").lower() or target == str(j.get("id") or "").lower():
            return AtsPayload(
                description_html=j.get("descriptionHtml") or "",
                questions=[],
                canonical_url=j.get("jobUrl") or url,
                detail="ashby posting", ok=True)
    return AtsPayload(detail="ashby posting not in board payload")


def _smartrecruiters(url: str) -> AtsPayload:
    m = SR_PATH.search(urlsplit(url).path)
    if not m:
        return AtsPayload(detail="unparsed smartrecruiters url")
    company, posting_id = m.group(1), m.group(2)
    data = _api_get("https://api.smartrecruiters.com/v1/companies/"
                    f"{company}/postings/{posting_id}")
    if not isinstance(data, dict):
        return AtsPayload(detail="smartrecruiters api miss")
    sections = ((data.get("jobAd") or {}).get("sections") or {})
    body = " ".join(
        (sections.get(k) or {}).get("text") or ""
        for k in ("companyDescription", "jobDescription", "qualifications",
                  "additionalInformation"))
    return AtsPayload(description_html=body,
                      canonical_url=f"https://jobs.smartrecruiters.com/{company}/{posting_id}",
                      detail="smartrecruiters posting", ok=True)


def _workday(url: str) -> AtsPayload:
    """Workday has no public per-posting JSON endpoint we can rely on.

    The CXS job-list call needs the site id and a POST body; the posting page
    itself is JS-rendered. So the adapter reports "no API" and the orchestrator
    falls through to the tiered fetcher, which handles Workday via curl_cffi.
    """
    host = urlsplit(url).netloc
    return AtsPayload(detail=f"workday unapi'd ({host})", ok=False)


_ADAPTERS = {
    SourceKind.ATS_GREENHOUSE: _greenhouse,
    SourceKind.ATS_LEVER: _lever,
    SourceKind.ATS_ASHBY: _ashby,
    SourceKind.ATS_SMARTRECRUITERS: _smartrecruiters,
    SourceKind.ATS_WORKDAY: _workday,
}


def fetch(kind: SourceKind, url: str) -> AtsPayload:
    fn = _ADAPTERS.get(kind)
    if fn is None:
        return AtsPayload(detail=f"no adapter for {kind.value}")
    return fn(url)


def has_api(kind: SourceKind) -> bool:
    return kind in _ADAPTERS and kind is not SourceKind.ATS_WORKDAY
```

- [ ] **Step 2: Write `tests/test_ats_adapters.py`** (URL parsing only — no network)

```python
from scripts.referral import ats_adapters as A
from scripts.referral.source_router import SourceKind


def test_greenhouse_url_variants_parse():
    for url in ("https://boards.greenhouse.io/geotab/jobs/4567890",
                "https://job-boards.greenhouse.io/geotab/jobs/4567890",
                "https://boards-api.greenhouse.io/v1/boards/geotab/jobs/4567890"):
        m = A.GH_API_PATH.search(url) or A.GH_PATH.search(url)
        assert m and m.group(1) == "geotab" and m.group(2) == "4567890", url


def test_lever_uuid_parses():
    m = A.LEVER_PATH.search(
        "/pointclickcare/1f2e3d4c-5b6a-7890-abcd-ef1234567890")
    assert m and m.group(1) == "pointclickcare"


def test_smartrecruiters_parses():
    m = A.SR_PATH.search("/ServiceNow/744000160277860")
    assert m and m.group(1) == "ServiceNow"


def test_workday_has_no_api():
    assert A.has_api(SourceKind.ATS_WORKDAY) is False
    assert A.has_api(SourceKind.ATS_GREENHOUSE) is True


def test_unknown_kind_returns_not_ok():
    payload = A.fetch(SourceKind.COMPANY_DIRECT, "https://example.test/job/1")
    assert payload.ok is False


def test_workday_adapter_is_not_ok():
    payload = A.fetch(SourceKind.ATS_WORKDAY,
                      "https://bmo.wd3.myworkdayjobs.com/en-US/External/job/x")
    assert payload.ok is False
```

- [ ] **Step 3: Run**

```bash
python3 -m pytest tests/test_ats_adapters.py -q
```

Expected: 6 passed.

- [ ] **Step 4: Live-check one real Greenhouse posting (the whole thesis of this task)**

```bash
python3 - <<'PY'
import json, sys; sys.path.insert(0, ".")
from scripts.referral import ats_adapters as A
from scripts.referral.source_router import SourceKind, classify

jobs = json.load(open("jobs.json"))["jobs"]
gh = [j for j in jobs if classify(j) is SourceKind.ATS_GREENHOUSE][:3]
for j in gh:
    p = A.fetch(SourceKind.ATS_GREENHOUSE, j["url"])
    print(f"{p.ok} {p.detail:32s} q={len(p.questions)} body={len(p.description_html)}")
    print("   ", j["url"][:100])
    for q in p.questions[:6]:
        print("     Q:", q[:90])
PY
```

Expected: at least one `ok=True` with a non-zero `q=`. If all three miss, the posting IDs are stale — try later rows before concluding the endpoint changed.

- [ ] **Step 5: Commit**

```bash
git add scripts/referral/ats_adapters.py tests/test_ats_adapters.py
git commit -m "feat(referral): ATS API adapters incl. Greenhouse application questions"
```

---

## Task 7: Orchestrator + CLI

**Files**
- Create: `scripts/referral/enhanced_referral_hunt.py`

Resumability matters: a 3,256-row sweep with Playwright fallbacks takes hours. The orchestrator writes a checkpoint JSON after every N rows and skips job ids already present.

- [ ] **Step 1: Write `enhanced_referral_hunt.py`**

```python
#!/usr/bin/env python3
"""Full referral sweep over jobs.json.

Usage (from bestiejob/):
    python3 scripts/referral/enhanced_referral_hunt.py --limit 25
    python3 scripts/referral/enhanced_referral_hunt.py --kinds ats_greenhouse,ats_lever
    python3 scripts/referral/enhanced_referral_hunt.py --apply
"""
from __future__ import annotations

import argparse
import json
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

REPO = Path(__file__).resolve().parent.parent.parent
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))          # `python scripts/referral/...` has no package root

from scripts.referral import ats_adapters, extractor, link_resolver, source_router
from scripts.referral.host_gate import HostGate
from scripts.referral.tiered_fetcher import fetch as tiered_fetch

JOBS = REPO / "jobs.json"
RAW = REPO / "raw"
NOW = datetime.now(timezone.utc)

_WRITE_LOCK = threading.Lock()


def load_jobs() -> list[dict]:
    data = json.loads(JOBS.read_text(encoding="utf-8"))
    return data["jobs"] if isinstance(data, dict) else data


def _evidence(hit) -> str:
    return (hit.evidence or hit.pattern or "")[:280]


def inspect_job(job: dict, *, gate: HostGate, allow_playwright: bool) -> dict:
    url = (job.get("url") or "").strip()
    kind = source_router.classify(job)
    record = {
        "job_id": job.get("id"),
        "company": job.get("company"),
        "title": job.get("title"),
        "url": url,
        "route": kind.value,
        "status": "no_referral",
        "tier": "none",
        "referral": None,
        "checked_at": NOW.isoformat().replace("+00:00", "Z"),
    }
    if kind is source_router.SourceKind.UNROUTABLE:
        record["status"] = "unroutable"
        return record
    if kind in source_router.NO_FETCH:
        record["status"] = "skipped_aggregator"
        return record

    hits = []

    # --- ATS API channel ------------------------------------------------
    if kind in source_router.ATS_KINDS and ats_adapters.has_api(kind):
        payload = ats_adapters.fetch(kind, url)
        if payload.ok:
            record["tier"] = "ats_api"
            hits = extractor.extract(payload.description_html,
                                     title=job.get("title") or "",
                                     company=job.get("company") or "",
                                     structured_questions=payload.questions)
            if payload.canonical_url:
                url = payload.canonical_url
                record["canonical_url"] = payload.canonical_url

    # --- Web channel (only if the API channel was silent) ---------------
    if not extractor.best(hits):
        if gate.is_quarantined(urlsplit(url).netloc.lower()):
            record["status"] = "blocked"
            record["detail"] = "host quarantined"
            return record
        result = tiered_fetch(url, gate=gate, allow_playwright=allow_playwright)
        if not result.ok:
            record["status"] = "blocked" if result.status in (403, 429) else "error"
            record["tier"] = result.tier
            record["detail"] = result.detail[:160]
            return record
        record["tier"] = result.tier
        script_hits = extractor.extract(result.html,
                                        title=job.get("title") or "",
                                        company=job.get("company") or "")
        base = result.url or url
        for h in script_hits:
            if h.kind in ("page", "form") and h.value:
                resolved = link_resolver.absolutize(h.value, base)
                if resolved:
                    h.value = resolved
            hits.extend([h])
        hits = extractor._rank(hits)

    top = extractor.best(hits)
    if top is None:
        record["all_hits"] = [
            {"kind": h.kind, "value": h.value, "conf": h.confidence,
             "pattern": h.pattern} for h in hits[:5]]
        return record

    record["status"] = "found"
    record["referral"] = {
        "kind": top.kind,
        "url": top.value if top.kind in ("form", "page") else None,
        "email": top.value if top.kind == "email" else None,
        "confidence": top.confidence,
        "evidence": _evidence(top),
        "all_hits": [{"kind": h.kind, "value": h.value, "conf": h.confidence,
                      "pattern": h.pattern} for h in hits[:6]],
    }
    return record


def _checkpoint(path: Path, results: list[dict]) -> None:
    with _WRITE_LOCK:
        tmp = path.with_suffix(".tmp")
        tmp.write_text(json.dumps({"generated_at": NOW.isoformat(),
                                   "results": results}, indent=1,
                                  ensure_ascii=False), encoding="utf-8")
        tmp.replace(path)


def apply_to_jobs(results: list[dict]) -> int:
    """Inject `referral_info` into matching jobs rows. Returns rows touched."""
    data = json.loads(JOBS.read_text(encoding="utf-8"))
    rows = data["jobs"] if isinstance(data, dict) else data
    by_id = {r["job_id"]: r for r in results if r.get("job_id")}
    touched = 0
    for row in rows:
        rec = by_id.get(row.get("id"))
        if not rec or rec["status"] != "found":
            continue
        row["referral_info"] = rec["referral"]
        touched += 1
    JOBS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")
    return touched


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jobs", default=str(JOBS))
    ap.add_argument("--out", default=None)
    ap.add_argument("--limit", type=int, default=0, help="0 = all")
    ap.add_argument("--kinds", default="", help="comma-separated SourceKind values")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--no-playwright", action="store_true")
    ap.add_argument("--resume", action="store_true", help="skip ids already in --out")
    ap.add_argument("--apply", action="store_true", help="write referral_info into jobs.json")
    args = ap.parse_args()

    out = Path(args.out) if args.out else RAW / f"referral_hunt_{NOW:%Y-%m-%d}.json"
    RAW.mkdir(exist_ok=True)

    jobs = load_jobs()
    if args.kinds:
        wanted = {k.strip() for k in args.kinds.split(",") if k.strip()}
        keep = [j for j in jobs
                if source_router.classify(j).value in wanted]
        # keep input order, but only the requested routes
        jobs = keep
    if args.limit:
        jobs = jobs[: args.limit]

    done: dict[str, dict] = {}
    if args.resume and out.exists():
        for r in json.loads(out.read_text(encoding="utf-8")).get("results", []):
            if r.get("job_id"):
                done[r["job_id"]] = r
        jobs = [j for j in jobs if j.get("id") not in done]

    print(f"sweeping {len(jobs)} jobs -> {out.relative_to(REPO)}  "
          f"workers={args.workers} playwright={not args.no_playwright}")

    gate = HostGate()
    results = list(done.values())
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(inspect_job, j, gate=gate,
                               allow_playwright=not args.no_playwright): j
                   for j in jobs}
        for i, fut in enumerate(as_completed(futures), 1):
            job = futures[fut]
            try:
                results.append(fut.result())
            except Exception as exc:                             # noqa: BLE001
                results.append({"job_id": job.get("id"), "status": "error",
                                "detail": f"{type(exc).__name__}: {exc}"[:160],
                                "url": job.get("url")})
            if i % 25 == 0:
                _checkpoint(out, results)
                rate = i / max(time.time() - t0, 1e-6)
                print(f"  {i}/{len(jobs)}  {rate:.1f}/s  "
                      f"found={sum(1 for r in results if r.get('status') == 'found')}")

    _checkpoint(out, results)

    from collections import Counter
    counts = Counter(r.get("status") for r in results)
    print("\nstatus:", dict(counts))
    found = [r for r in results if r.get("status") == "found"]
    print(f"referral artifacts: {len(found)}")
    for r in found[:25]:
        ref = r["referral"]
        print(f"  {ref['confidence']:.2f} {ref['kind']:8s} "
              f"{(ref.get('url') or ref.get('email') or '')[:70]}")
        print(f"        {r['company'][:26]:26} {r['title'][:52]}")

    if args.apply:
        n = apply_to_jobs(results)
        print(f"\njobs.json: added referral_info to {n} rows")

    print(f"\nwrote {out.relative_to(REPO)} ({len(results)} records)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Bounded smoke run — 15 rows, no Playwright, no apply**

```bash
python3 scripts/referral/enhanced_referral_hunt.py --limit 15 --no-playwright --out raw/referral_smoke.json
```

Expected: exits 0, prints a `status:` counter, writes `raw/referral_smoke.json` with 15 records. No tracebacks. If every record is `blocked`, the fetcher tier is the problem, not the orchestrator.

- [ ] **Step 3: Parallelism sanity check — must not deadlock on the Playwright lock**

```bash
timeout 600 python3 scripts/referral/enhanced_referral_hunt.py \
  --limit 40 --workers 6 --out raw/referral_smoke2.json
```

Expected: completes inside the timeout, `found` count ≥ 0, no `thread 'MainThread' is not the owner` Playwright errors.

- [ ] **Step 4: Commit**

```bash
git add scripts/referral/enhanced_referral_hunt.py
git commit -m "feat(referral): resumable orchestrator with checkpointing and --apply"
```

---

## Task 8: Integration tests + full-sweep gate

**Files**
- Create: `tests/test_referral_integration.py`

- [ ] **Step 1: Write `tests/test_referral_integration.py`** (offline: monkeypatch the network)

```python
"""End-to-end tests with the network stubbed out."""
import json
from pathlib import Path

import pytest

from scripts.referral import ats_adapters
from scripts.referral import enhanced_referral_hunt as hunt
from scripts.referral.host_gate import HostGate
from scripts.referral.tiered_fetcher import FetchResult

FIXTURE = (Path(__file__).parent / "fixtures" / "referral_page.html").read_text(
    encoding="utf-8")


def _job(**kw):
    base = {"id": "greenhouse:boards.greenhouse.io/acme/jobs/1",
            "company": "Acme", "title": "ServiceNow Developer",
            "url": "https://boards.greenhouse.io/acme/jobs/1"}
    base.update(kw)
    return base


def test_ats_question_hit_produces_found(monkeypatch):
    monkeypatch.setattr(
        ats_adapters, "fetch",
        lambda kind, url: ats_adapters.AtsPayload(
            description_html="<p>Great role.</p>",
            questions=["Were you referred by a current Acme employee?"],
            canonical_url=url, ok=True, detail="stub"))
    rec = hunt.inspect_job(_job(), gate=HostGate(min_interval_s=0),
                           allow_playwright=False)
    assert rec["status"] == "found"
    assert rec["referral"]["kind"] == "question"
    assert rec["referral"]["confidence"] >= 0.9
    assert rec["tier"] == "ats_api"


def test_api_miss_falls_through_to_web(monkeypatch):
    monkeypatch.setattr(ats_adapters, "fetch",
                        lambda kind, url: ats_adapters.AtsPayload(ok=False))
    monkeypatch.setattr(
        hunt, "tiered_fetch",
        lambda url, **kw: FetchResult(FIXTURE, "curl_cffi", 200, url))
    rec = hunt.inspect_job(_job(), gate=HostGate(min_interval_s=0),
                           allow_playwright=False)
    assert rec["status"] == "found"
    assert rec["tier"] == "curl_cffi"
    assert rec["referral"]["url"].startswith("https://boards.greenhouse.io/")


def test_linkedin_is_skipped_without_network(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("must not fetch LinkedIn")
    monkeypatch.setattr(hunt, "tiered_fetch", boom)
    rec = hunt.inspect_job(_job(url="https://www.linkedin.com/jobs/view/123"),
                           gate=HostGate(min_interval_s=0),
                           allow_playwright=False)
    assert rec["status"] == "skipped_aggregator"


def test_blocked_status_on_403(monkeypatch):
    monkeypatch.setattr(ats_adapters, "fetch",
                        lambda kind, url: ats_adapters.AtsPayload(ok=False))
    monkeypatch.setattr(
        hunt, "tiered_fetch",
        lambda url, **kw: FetchResult(None, "none", 403, url, "HTTP 403"))
    rec = hunt.inspect_job(_job(), gate=HostGate(min_interval_s=0),
                           allow_playwright=False)
    assert rec["status"] == "blocked"


def test_apply_writes_referral_info(monkeypatch, tmp_path):
    jobs_file = tmp_path / "jobs.json"
    jobs_file.write_text(json.dumps({"jobs": [_job()]}), encoding="utf-8")
    monkeypatch.setattr(hunt, "JOBS", jobs_file)
    results = [{"job_id": _job()["id"], "status": "found",
                "referral": {"kind": "question", "url": None, "email": None,
                             "confidence": 1.0, "evidence": "stub"}}]
    assert hunt.apply_to_jobs(results) == 1
    row = json.loads(jobs_file.read_text(encoding="utf-8"))["jobs"][0]
    assert row["referral_info"]["kind"] == "question"
```

- [ ] **Step 2: Run the whole referral suite**

```bash
python3 -m pytest tests/test_host_gate.py tests/test_link_resolver.py \
  tests/test_extractor.py tests/test_ats_adapters.py \
  tests/test_referral_integration.py -q
```

Expected: 29 passed, 0 failed, ~2s.

- [ ] **Step 3: Commit**

```bash
git add tests/test_referral_integration.py
git commit -m "test(referral): offline end-to-end integration coverage"
```

---

## Task 9: Full sweep and report

- [ ] **Step 1: Run the ATS channel across the whole corpus first** (cheapest, ~850 rows)

```bash
timeout 5400 python3 scripts/referral/enhanced_referral_hunt.py \
  --kinds ats_greenhouse,ats_lever,ats_ashby,ats_smartrecruiters \
  --workers 8 --no-playwright --resume \
  --out raw/referral_ats_2026-11-07.json
```

Expected: `found` ≥ 1. Greenhouse alone is 650 rows and is API-only, so this should finish in minutes, not hours.

- [ ] **Step 2: Run the remaining routes** (direct + workday + adzuna; LinkedIn skipped)

```bash
timeout 21600 python3 scripts/referral/enhanced_referral_hunt.py \
  --kinds workday,company_direct,aggregator_adzuna \
  --workers 6 --resume --out raw/referral_web_2026-11-07.json
```

Expected: hours for the full 1,887 rows; `--resume` makes interruption safe.

- [ ] **Step 3: Write the human report**

```bash
python3 - <<'PY'
import json, glob
rows = []
for p in sorted(glob.glob("raw/referral_*_2026-11-07.json")):
    rows += json.load(open(p))["results"]
found = [r for r in rows if r.get("status") == "found"]
found.sort(key=lambda r: -r["referral"]["confidence"])
lines = ["# Referral hunt — 2026-11-07", "",
         f"{len(found)} direct referral artifacts across {len(rows)} postings.", "",
         "| Conf | Kind | Company | Role | Referral target |",
         "| --- | --- | --- | --- | --- |"]
for r in found:
    ref = r["referral"]
    target = ref.get("url") or ref.get("email") or ref.get("evidence") or ""
    lines.append(f"| {ref['confidence']:.2f} | {ref['kind']} | "
                 f"{r['company']} | {r['title']} | {target[:120]} |")
open("inbox/referral-hunt--2026-11-07--final.md", "w").write("\n".join(lines) + "\n")
print(f"wrote inbox/referral-hunt--2026-11-07--final.md ({len(found)} rows)")
PY
```

- [ ] **Step 4: Optionally persist into the site data**

```bash
python3 scripts/referral/enhanced_referral_hunt.py \
  --kinds ats_greenhouse,ats_lever,ats_ashby,ats_smartrecruiters,company_direct \
  --resume --apply --out raw/referral_apply_2026-11-07.json
python3 -c "import json;d=json.load(open('jobs.json'));print('rows with referral_info:', sum(1 for j in d['jobs'] if 'referral_info' in j))"
python3 tools/build_site.py
git diff --stat public/
```

Expected: `rows with referral_info: N` where N > 0, and `public/` diff is empty because `build_site.py` ignores unknown keys.

- [ ] **Step 5: Commit the report (never the raw sweep dumps)**

```bash
git add inbox/referral-hunt--2026-11-07--final.md
git commit -m "docs(referral): referral-hunt findings report for 2026-11-07"
```

---

## Risks and honest limits

1. **Greenhouse `absolute_url` is not a referral URL.** It is the posting URL. The *questions array* is the real prize; a posting whose form has no referral question legitimately returns `no_referral`.
2. **"Referral form" is rare in the wild.** Expect a low `found` rate (single-digit percent of ATS rows). A sweep that returns 40 high-confidence hits is a success; one that returns 800 is a broken scorer. If `found` > 25% of rows, stop and re-audit `extractor._score_text` before trusting anything.
3. **Adzuna's 851 rows will mostly be `blocked`.** That is expected and correct — do not add retries to force them through.
4. **Playwright tier is the wall-clock cost.** The `--no-playwright` flag exists for a reason; only the web pass needs it.
5. **`referral_info` is additive.** No existing key changes, so no site regression is possible from `--apply`.

---

## Definition of done

- [ ] All 5 test files pass offline (`pytest -q`, ~2s, no network).
- [ ] ATS pass completes and writes `raw/referral_ats_2026-11-07.json`.
- [ ] Web pass completes (or is deliberately scoped) and writes `raw/referral_web_2026-11-07.json`.
- [ ] `inbox/referral-hunt--2026-11-07--final.md` lists every hit with confidence + evidence.
- [ ] If `--apply` used: `jobs.json` has `referral_info` rows and `tools/build_site.py` produces an unchanged `public/`.
