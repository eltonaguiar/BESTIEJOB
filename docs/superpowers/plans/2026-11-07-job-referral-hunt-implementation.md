# Enhanced Referral Hunt Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a tiered referral-hunt system that scans 3,256 postings for referral links/contacts, using ATS APIs and anti-bot fetching.

**Architecture:**
- **Orchestrator:** `scripts/referral/enhanced_referral_hunt.py`
- **Source Router:** `scripts/referral/source_router.py`
- **ATS Adapters:** `scripts/referral/ats_adapters.py`
- **Tiered Fetcher:** `scripts/referral/tiered_fetcher.py`
- **Extractor:** `scripts/referral/extractor.py`
- **Link Resolver:** `scripts/referral/link_resolver.py`

**Tech Stack:** Python 3.11, `curl_cffi`, `playwright`, `httpx`, `bs4`, `lxml`.

---

### Task 1: Setup Package Structure

**Files:**
- Create: `bestiejob/scripts/referral/__init__.py`
- Create: `bestiejob/scripts/referral/source_router.py`

- [ ] **Step 1: Create package**
```bash
mkdir -p bestiejob/scripts/referral
touch bestiejob/scripts/referral/__init__.py
```

- [ ] **Step 2: Implement SourceRouter**
```python
from enum import Enum
from urllib.parse import urlsplit

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

def classify(job: dict) -> SourceKind:
    url = job.get("url", "").lower()
    netloc = urlsplit(url).netloc
    if "greenhouse.io" in netloc: return SourceKind.ATS_GREENHOUSE
    if "lever.co" in netloc: return SourceKind.ATS_LEVER
    if "ashbyhq.com" in netloc: return SourceKind.ATS_ASHBY
    if "myworkdayjobs.com" in netloc: return SourceKind.ATS_WORKDAY
    if "smartrecruiters.com" in netloc: return SourceKind.ATS_SR
    if "adzuna.ca" in netloc: return SourceKind.AGGREGATOR_ADZUNA
    if "linkedin.com" in netloc: return SourceKind.AGGREGATOR_LINKEDIN
    return SourceKind.COMPANY_DIRECT
```

- [ ] **Step 3: Commit**
```bash
git add bestiejob/scripts/referral/
git commit -m "feat(referral): setup package and source router"
```

### Task 2: Implement ATS Adapters

**Files:**
- Create: `bestiejob/scripts/referral/ats_adapters.py`

- [ ] **Step 1: Implement ATS Adapters**
(Reusing logic from `ats_board_sweep.py`)

```python
import httpx
from .source_router import SourceKind

class ATSAdapter:
    def fetch_description(self, job: dict) -> str | None:
        raise NotImplementedError

class GreenhouseAdapter(ATSAdapter):
    def fetch_description(self, job: dict) -> str | None:
        # Logic from ats_board_sweep.py: greenhouse_employer
        pass
# ... implement others
```

- [ ] **Step 2: Commit**
```bash
git add bestiejob/scripts/referral/ats_adapters.py
git commit -m "feat(referral): implement ATS adapters"
```

### Task 3: Implement Tiered Fetcher

**Files:**
- Create: `bestiejob/scripts/referral/tiered_fetcher.py`

- [ ] **Step 1: Implement TieredFetcher**
```python
from curl_cffi import requests as curl_requests
from playwright.sync_api import sync_playwright
import httpx

class TieredFetcher:
    def fetch(self, url: str, kind: SourceKind) -> str | None:
        # Tier 1: curl_cffi
        # Tier 2: playwright
        # Tier 3: httpx
        pass
```

- [ ] **Step 2: Commit**
```bash
git add bestiejob/scripts/referral/tiered_fetcher.py
git commit -m "feat(referral): implement tiered fetcher"
```

### Task 4: Implement Referral Extractor

**Files:**
- Create: `bestiejob/scripts/referral/extractor.py`

- [ ] **Step 1: Implement Extractor**
```python
import re
from dataclasses import dataclass

@dataclass
class ReferralHit:
    kind: str
    value: str
    pattern: str
    confidence: float

def extract(html: str) -> list[ReferralHit]:
    # Regex + DOM parsing
    pass
```

- [ ] **Step 2: Commit**
```bash
git add bestiejob/scripts/referral/extractor.py
git commit -m "feat(referral): implement extractor"
```

### Task 5: Implement Orchestrator

**Files:**
- Create: `bestiejob/scripts/referral/enhanced_referral_hunt.py`

- [ ] **Step 1: Implement Orchestrator**
```python
import json
from .source_router import classify
from .ats_adapters import ...
from .tiered_fetcher import ...
from .extractor import ...

def main():
    # Load jobs, loop, fetch, extract, save
    pass
```

- [ ] **Step 2: Commit**
```bash
git add bestiejob/scripts/referral/enhanced_referral_hunt.py
git commit -m "feat(referral): implement orchestrator"
```

### Task 6: Integration Tests

**Files:**
- Create: `bestiejob/tests/test_referral_hunt.py`

- [ ] **Step 1: Write tests**
- [ ] **Step 2: Run tests**
- [ ] **Step 3: Commit**

### Task 7: Final Verification

- [ ] **Step 1: Run full sweep**
- [ ] **Step 2: Verify output**
- [ ] **Step 3: Commit**
