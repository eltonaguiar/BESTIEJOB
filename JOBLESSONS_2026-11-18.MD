# JOBLESSONS_2026-11-18 — BESTIEJOB hourly cron scan (01:00 EST)

## Scan scope
- Target: fresh Toronto / Canada ServiceNow and Salesforce postings (Platform Admin / Platform Developer I emphasis for Salesforce; ServiceNow platform, CSA/CAD/CIS certs for SN).
- Freshness window: posted today / yesterday preferred (`f_TPR=r86400` equivalent where supported); hourly ATS sweep carries sub-daily freshness.
- Sources scanned: public ATS feeds — SmartRecruiters, Workday (CXS), Greenhouse, Lever, Ashby, LinkedIn (guest), remote boards, Adzuna — plus partner/employer career pages.

## Result
- Fresh Canada SN/SF postings surfaced this hour: 40 (21 ServiceNow, 19 Salesforce), posted 2026-11-16 through 2026-11-18.
- New to the board from this scan: 0 — all 40 were already present (dedupe against jobs.json + README.md held). Staged as `inbox/hermes-cron--2026-11-18--v1.md`; `check_inbox.py` OK (40 dated rows); merger reported `+0 new, 40 duplicate`.
- Board net change this run: +2 rows (from concurrent `fresh-ca--2026-11-18--v1.md` IG Wealth HRSD row and `ats-sweep--2026-11-18--v1.md` TD nCino/Salesforce row). README counts: ServiceNow 1154→1155, Salesforce 1477→1478.
- `tools/build_site.py`: OK — 5006 jobs indexed (SN 808 · SF 934 · Other 3264), 863 duplicate mirrors collapsed, 35 applied hidden, newest 2026-11-18. `public/jobs-data.json` + `public/index.html` rebuilt.

## Partner / employer look (Rogers, Bell, Canadian government, Elite/SN-SF partners)
- Rogers: `jobs.rogers.com` Phenom board unreachable (HTTP 404, 9-byte body to curl; error page in browser). Check weekly, not hourly.
- Bell: `jobs.bell.ca` renders an empty shell / shows (0) for both `servicenow` and `salesforce` in a browser — zero reqs, not a scrape failure. Re-check weekly.
- Canadian government: `gojobs.gov.on.ca` (Ontario) and `jobs.gc.ca` are Radware-walled (captcha) — do not retry. Use Job Bank as proxy; trust only postings whose TITLE names the platform (Job Bank full-text search is noise: "searchstring=servicenow" returns shipping coordinators, agronomy engineers).
- Salesforce-the-company: Toronto/Canada careers page exists, but per market shape Salesforce posts nothing below 4 days old and no Platform Admin/Dev I in Toronto — nothing fresh to add this hour.
- ServiceNow-the-company: Toronto postings are sales/SRE/security only — no platform roles this hour.
- Fresh platform work this hour came from banks (BMO/TD/CIBC Workday), DXC, and GRC/IRM consultancies (PwC ServiceNow IRM practice). Accenture Workday has 1,600+ SN reqs but effectively none Canadian on page 1.

## Source / API notes (reusable next hour)
- Workday CXS IS reachable from this host — use the `wdN` host and `curl --compressed` (without `--compressed` the gzipped body decodes as nothing). Known 200 Canadian pairs: `bmo.wd3/External`, `td.wd3/TD_Bank_Careers`, `cibc.wd3/search`, `manulife.wd3/MFCJH_Jobs`, `interac.wd3/interac`, `accenture.wd103/AccentureCareers`, `salesforce.wd12/External_Career_Site`. Dead ends this cycle: `canadalife/telus/desjardins/loblaw/kpmg/deloitte/cgi` (.wd3 → 422), `sunlife/rbc.wd3` (→ 404), `dxctechnology.wd1/dxcjobs` and `cognizant.wd1` (→ 521). Workday `postedOn: "Posted Today"` is NOT a Canada signal — read the `/job/<City>/…` slug and country before counting a hit.
- LinkedIn guest `seeMoreJobPostings` 429s after ~4 rapid queries. Use `new_tab` on the guest search URL, then same-origin `fetch('/jobs-guest/...')` from that page (no CORS, HTTP 200, full card HTML with absolute `datetime`). Always test length + md5 digest distinctness, not just HTTP 200 (authwall returns 200 with a stale 337 KB body). Sleep ~25 s between batches of four; `f_TPR=r3600` is near-empty pre-dawn EST — use `r86400`.
- Adzuna 503s after ~4 rapid queries — space calls ≥3 s. Adzuna recycles IDs: use the detail page's JSON-LD (`datePosted`/`validThrough`), not the API `created` date. Dedupe by fuzzy company (strip Inc/Ltd/Corp/Limited, compare 10-char prefix) + title tokens — plain URL/company matching misses `MLSE` vs `Maple Leaf Sports & Entertainment Partnership`.
- Dedupe rules: normalize URL (strip query string + trailing slash); LinkedIn job-id equality is a hard dedupe signal even when titles differ; vendor twins (different staffing firms advertising the same client req under the same title) are DISTINCT postings — keep both, dedupe on URL only.
- `jobs.rogers.com` / `jobs.scotiabank.com` Phenom boards unreachable this cycle. `jobs.bell.ca` = zero reqs. Gov portals Radware-walled.

## What did not change
- `jobs.json` untouched (scan rows go to README via the inbox merger; `build_site.py` unions jobs.json + README, so the page reflects both).
- `inbox/hermes-cron--2026-11-18--v1.md` left untracked (merger run without `--bump-inbox`; all 40 rows were duplicates).
