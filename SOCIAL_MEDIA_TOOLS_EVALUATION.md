# Social Media Tool Evaluation — bestiejob
**Project:** bestiejob (ServiceNow/Salesforce job scanning for Canada/Toronto)
**Evaluated:** xurl (X/Twitter CLI), LinkedIn via Jina Reader, Bluesky, Mastodon, Reddit
**Date:** 2026-11-05
**Goal:** Decide which social media sources are worth adding to the pipeline.

---

## 1. xurl / X (Twitter) — DO NOT INTEGRATE (low value, real cost)

**What xurl is:** The official CLI client for the X API (`xdevplatform/xurl`, docs.x.com/tools/xurl). It is a curl-like OAuth client for calling X API endpoints — NOT a scraper and NOT a job feed by itself. It still requires an X developer app with OAuth 2.0 credentials.

**X API pricing (current, docs.x.com/x-api/getting-started/pricing):**
- Pay-per-usage, credit-based. **No ongoing free tier.** ($20 starter credits + up to $50 first-recharge match only when you first add a payment card.)
- Read operations charged per resource returned: **Posts: Read $0.005 each**, capped at **3 million post reads / month**.
- No subscriptions; credits purchased upfront in Developer Console.

**Does X have ServiceNow/Salesforce jobs?**
- No dedicated "jobs" endpoint on the X API. You can only keyword-search posts (noisy, expensive per read).
- The main relevant account `@ServiceNow_Jobs` (Nelson Frank third-party recruiting) has only **71 posts** and visible activity dates from **2018** — effectively dormant and US-focused, not Canada.
- `@XHiring` mentioned an X job-search feature (Nov 2024) but it is not a structured feed and is not ServiceNow/Salesforce/Canada-specific.
- Some Canadian job aggregator accounts exist (e.g. `@jobsfrombdm`) but none are SN/SF-specific.

**Verdict:** Not worth integrating. Pay-to-access API, no jobs endpoint, dormant/niche job accounts, noisy signal, and zero Canada/ServiceNow/Salesforce focus. Cost and complexity outweigh any marginal lead volume.

---

## 2. LinkedIn via Jina Reader — INTEGRATE (high value)

**Current state:** bestiejob already scrapes LinkedIn directly (guest endpoint `jobs-guest/jobs/api/seeMoreJobPostings/search` + Playwright fallback) in `scrapers/linkedin_scraper.js`, `scripts/linkedin_bulk_scraper.mjs`, `scripts/linkedin_guest_scan.py`. Direct scraping is **BLOCKED** (403 / login wall, heavy anti-bot) per `JOB_SOURCES_STATUS.md` — LinkedIn yielded only ~67 jobs before restriction.

**Jina Reader (r.jina.ai) viability:** Verified working. A Jina Reader fetch of `linkedin.com/jobs/search/?keywords=ServiceNow&location=Canada` returned live job cards, e.g.:
- Senior Consultant - ServiceNow CSM — Infosys, Mississauga (3 weeks ago)
- Manager, ServiceNow Technical Lead — KPMG Canada, Toronto/Vancouver (2 weeks ago)
- Bilingual Senior Specialist, ServiceNow ITSM Developer — CMHC, Ottawa (1 day ago)
- Senior Consultant, ServiceNow (ITAM/ITOM) — KPMG Canada, Toronto

LinkedIn shows **4,000+ ServiceNow jobs in Canada** and **3,000+ ServiceNow Canada jobs** in search snippets — by far the largest single concentration of relevant postings.

**Caveats:** LinkedIn's ToS prohibits scraping; Jina Reader may eventually be blocked too (as direct scraping was). Use as a **complementary** source behind the existing Adzuna/ATS/API sources, with rate limiting and fallback. Monitor for 403s.

**Verdict:** Worth integrating via Jina Reader because direct LinkedIn scraping is blocked and LinkedIn holds the bulk of relevant Canada ServiceNow/Salesforce postings. This recovers a source the pipeline currently loses.

---

## 3. Other social platforms — DO NOT INTEGRATE (low priority)

| Platform | Assessment |
|----------|------------|
| **Reddit** (r/forhire, r/salesforce, r/servicenow) | Jina Reader fetch returned **403 Forbidden** ("network security... log in or developer token"). Reddit API now requires registration (limited free tier). No verified Canada SN/SF job volume. Not worth the access friction. |
| **Bluesky** | `bsky.app` is heavily JavaScript-dependent (hard to scrape). Profiles exist (`@servicenow.bsky.social`, `@jobsearchnow.bsky.social`) but no evidence of active Canada ServiceNow/Salesforce job postings. |
| **Mastodon** | Fully decentralized; no central job board. `joinmastodon.org/careers` is for Mastodon the org only. No evidence of ServiceNow/Salesforce Canada postings. |

---

## 4. Bonus non-social but relevant source — INTEGRATE

**ServiceNow Community Jobs Forum:** `www.servicenow.com/community/servicenow-jobs-forum` — a dedicated forum where employers post ServiceNow full-time/contract/fixed-price jobs. Highly on-topic for bestiejob's ServiceNow focus and not subject to social-platform API pricing. Worth adding as a scraper target.

---

## 5. Summary recommendation

| Tool / Source | Integrate? | Why |
|---------------|-----------|-----|
| LinkedIn via Jina Reader | **YES** | Recovers blocked LinkedIn (4,000+ ServiceNow Canada jobs); Jina Reader confirmed working. Complement to existing sources. |
| xurl / X API | **NO** | Pay-per-use (no free tier), no jobs endpoint, dormant job accounts (@ServiceNow_Jobs inactive since 2018, US-focused), noisy, Canada relevance unproven. |
| Reddit | **NO** | 403-blocked, needs dev token/login, unproven Canada SN/SF volume. |
| Bluesky | **NO** | JS-heavy/hard to scrape, no active Canada SN/SF job evidence. |
| Mastodon | **NO** | Decentralized, no central job board, no SN/SF Canada evidence. |
| ServiceNow Community Jobs Forum | **YES** (bonus) | On-topic ServiceNow job forum, no API pricing. |

**Implementation priority:**
1. Add LinkedIn via Jina Reader (highest marginal value — recovers the largest blocked source).
2. Add ServiceNow Community Jobs Forum scraper (niche, on-topic, free).
3. Defer xurl/X, Reddit, Bluesky, Mastodon indefinitely; revisit only if X launches a free jobs feed or a dedicated ServiceNow Canada job account becomes active.
