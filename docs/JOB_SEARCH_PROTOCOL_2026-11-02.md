# Job-Search Protocol — ServiceNow / Salesforce / Platform-Adjacent Roles (Toronto/Canada)

**Version 1.1 · 2026-11-02T15:10Z**
**Author-agent:** GitHub Copilot (Copilot SDK agent in VS Code, Claude Opus family model)
**Provenance:** distilled from ~2 hours of live multi-source scanning on 2026-11-02 (commits `d5c0f87`…`0877b67` in this repo), then scrutinized by two independent models (reviews quoted in §8 with adjudication).
**Target profile:** senior ServiceNow technical consultant (CSA, CAD, CIS×9, ITIL v4) with Salesforce Platform Dev I, ITAM/ITSM/ITOM depth, SQL/BI/automation skills.

---

## 1. Daily loop (45–60 min)

1. **Aggregator sweep (10 min):** Adzuna CA API, `sort_by=date`, `max_days_old=1–2`. Boolean-style keyword set — include `servicenow`, `servicenow developer|administrator|architect|consultant`, `HRSD`, `CSDM`, `salesforce developer|administrator|consultant|architect`; mentally filter out `junior|intern|trainee|account executive|sales rep`. Record IDs; dedup against yesterday's log.
2. **LinkedIn job-alert emails + guest API (10 min):** set saved-search email alerts as the primary channel (stable, ToS-safe); use the guest endpoint `jobs-guest/jobs/api/seeMoreJobPostings/search?f_TPR=r86400` only as a *supplement*, max a handful of calls, backing off on HTTP 429. Parse the `<time datetime>` attribute, and treat it as board-refresh-prone (Tier 4, not Tier 3 — downgraded after review).
3. **Verify before you trust (15 min):** every aggregator find gets confirmed on the employer ATS before logging as real:
   - Workday: `POST /wday/cxs/{tenant}/{site}/jobs` (gives `postedOn`, `canApply`)
   - Greenhouse: `boards-api.greenhouse.io/v1/boards/{org}/jobs`
   - Lever: `api.lever.co/v0/postings/{org}?mode=json` (`createdAt` epoch)
   - SmartRecruiters: `api.smartrecruiters.com/v1/companies/{co}/postings` (`releasedDate`)
   - Phenom-hosted sites (Bell, RBC, many banks): `POST {careers-site}/widgets` returns JSON with real `postedDate` that the HTML hides
   - SuccessFactors sites (Scotiabank, Rogers, City of Toronto): `/search/?q=keyword` is server-rendered
   - Oracle Recruiting (Metrolinx, WSIB): `/hcmRestApi/resources/latest/recruitingCEJobRequisitions?...keyword=...` gives exact `PostedDate`
4. **Employer-direct rotation (10 min):** 2–3 employers/day from a ~30-company list — banks (BMO/TD/CIBC/Scotiabank/RBC), telecoms (Bell/Rogers/TELUS), SN/SF end-users (Interac, Moneris, Canadian Tire, Intact), partners (Deloitte, KPMG, CGI, NewRocket, CloudKettle, Thirdera).
5. **Human channel (10 min — added after review):** message 1–2 recruiters or hiring managers at target employers ("Open to ServiceNow architect/lead roles, Toronto, available <date>"), or engage one post in the Toronto SNUG / Salesforce Developer Group community. Senior roles frequently fill by referral before boards see them.
6. **Log** every posting with: employer-source posted date (never the board's), URL, req ID, verification status, and — per review — application status + next follow-up date (funnel CRM, see §6).

## 2. Weekly loop

- **Job Bank Canada** (`searchstring=X&sort=D`): official employer-filed dates + salary bands; titles are NOC-generic, so map manually.
- **Grounded-AI sweep** (Gemini `google_search` tool or equivalent): ask for postings *with URLs*; treat its dates as leads only — measured 2/3 wrong in same-day spot checks. Always re-verify on the ATS.
- **Partner-ecosystem expansion:** add 3 new companies from ServiceNow/Salesforce partner directories or event-sponsor pages (Knowledge, Dreamforce, World Forum Toronto); fingerprint their ATS; add to the rotation.
- **"Sold project" intel (added after review):** scan ServiceNow/Salesforce press releases and partner case studies for recent Canadian go-lives; a fresh implementation at Bank X predicts hiring. Contact the delivery team directly.
- **Funnel check-ins:** Monday + Thursday 10-minute pass over the CRM log to advance stalled applications.
- **Geo sweep** when location matters: Adzuna `where=<postal>&distance=<km>` (e.g., `M5G 2H5`, 3 km) surfaces downtown-Toronto batches that keyword searches rank poorly.

## 3. Source reliability tiers (trust in this order)

| Tier | Source | Why |
|---|---|---|
| T1 | Employer ATS APIs (Workday CXS, Greenhouse, Lever, SmartRecruiters, Phenom `/widgets`, Oracle CE) | Real dates, `canApply` flags, req IDs |
| T2 | Job Bank Canada | Official + salary bands; generic titles |
| T3 | Employer career-site HTML (server-rendered) | Authentic but often date-less |
| T4 | LinkedIn guest cards, Adzuna/aggregators | Broad reach; board-refresh inflation, duplicate reposts, dates can differ from the employer's by days (downgraded from T3 after review) |
| T5 | Ungrounded AI output | Fabricates numbers/dates; never cite without a verified URL |

## 4. Known blockers (don't burn time)

- **Indeed:** HTTP 403 (Cloudflare) even via stealth HTTP clients — use its *email alerts* or a real browser only.
- **Ontario GoJobs:** Radware CAPTCHA wall.
- **ZipRecruiter / SimplyHired:** server-side blocked.
- **Eluta:** titles are server-rendered but URLs are JS-only; `eluta.ca/api/jobs` does **not** exist (tested 404 on 2026-11-02 after a reviewer claimed otherwise) — resolve interesting titles via exact-phrase web search to the employer ATS.
- **Bell/RBC/TELUS HTML:** JS-only — but the Phenom `POST /widgets` JSON API works without a browser.

## 5. Anti-fabrication rules

1. Never trust a model's claim that it "fetched" a posting; demand the URL, then open it.
2. Grounded-AI dates are leads, not facts — confirm with the employer field (`startDate`/`first_published`/`createdAt`/`releasedDate`/`postedOn`).
3. A board "refresh" (reposted card) is not a new posting — check the req ID against your log.
4. Convert every relative date ("8 hours ago") to an absolute ISO date at capture time, and record the capture timestamp beside it.

## 6. Funnel CRM (added after review)

Track per application: `posted_date, applied_date, req_id, url, status (found/applied/viewed/screen/interview/offer/rejected), next_action, next_action_date`. The job list page (`public/index.html`) can host this client-side via localStorage — see enhancement #9 in `docs/SITE_ENHANCEMENTS_2026-11-02.md`.

## 7. Timing heuristics

- Weekend publication of enterprise SN/SF reqs is rare; the Monday 9–11 am ET batch-publish wave is the highest-yield scan window.
- Consulting-partner reqs (Deloitte/KPMG/CGI) cluster Sunday night–Monday via LinkedIn before the ATS shows them.

---

## 8. Independent scrutiny (verbatim excerpts + adjudication)

### 8a. Review by `anthropic/claude-sonnet-4.5` via OpenRouter (2026-11-02T15:08Z)

> - **No recruiter outreach strategy**: for senior roles, external recruiters and niche platform staffing firms fill 40%+ of senior ServiceNow/Salesforce contracts…
> - **No network activation**: zero mention of ServiceNow/Salesforce community events (Toronto SNUG, Salesforce Dev Group meetups)…
> - **LinkedIn guest API abuse**: hammering `/jobs-guest/` daily *will* get your IP throttled or banned… use authenticated RSS/email alerts instead.
> - **Eluta *does* expose JSON via network tab (`/api/jobs`)**…
> - **Replace Adzuna daily grind with RSS/email alerts**… **Weekly "sold project" intel**: scan press releases for recent Canadian wins — implementations = hiring spikes.

**Adjudication:** Accepted → added §1.5 human channel, email-alert-first LinkedIn stance, §2 "sold project" intel. **Rejected:** the Eluta `/api/jobs` claim — tested 2026-11-02, returns 404 (see §4); kept the exact-phrase-search workaround. Partially accepted: Adzuna stays in the daily loop (it was the single highest-yield same-day source in live testing on 2026-11-02 — 7 same-day finds) but verification remains mandatory.

### 8b. Review by `mercury-3` (Inception Labs API, 2026-11-02T15:09Z)

> - **Zero Networking/Referral Loop**… referrals bypass ATS filters entirely.
> - **No Application Funnel Tracking**: without a CRM-style tracker, you will lose track of follow-ups and burn goodwill.
> - **Unbalanced Time Budget**: 30–45 minutes daily … is unrealistic if results exceed 10–15 postings. Verification becomes the bottleneck.
> - **LinkedIn Guest API fragility**… Treating it as T3 is generous — it should be T4.
> - **Boolean Search Overhaul**: `("servicenow" OR "snow" OR "CSDM") AND ("consultant" OR "architect") NOT ("junior" OR "intern")`…
> - **Build a Funnel CRM**… schedule Monday and Thursday 10-minute check-ins.

**Adjudication:** Accepted → §6 funnel CRM, §1 budget raised to 45–60 min, LinkedIn demoted to T4, keyword set widened (HRSD/CSDM + negative filters), Mon/Thu check-ins added to §2. Note: Adzuna's API ignores complex boolean operators, so the keyword set is implemented as multiple queries + post-filter rather than one boolean string.

---

*Changelog: v1.0 drafted 2026-11-02T15:05Z; v1.1 (this file) incorporates both reviews above.*
