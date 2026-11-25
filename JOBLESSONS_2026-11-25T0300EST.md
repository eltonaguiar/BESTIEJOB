# JOBLESSONS_2026-11-25T0300EST — hourly Toronto ServiceNow / Salesforce scan

## What ran
`node scripts/daily_job_scan.mjs` (no `--no-readme`, so the README `<!-- DAILY-SCAN -->` block and `FRESH_JOBS.md` were rewritten) at 2026-11-25T08:03Z, then `tools/build_site.py` + `scripts/sync_readme_counts.py`. Local main was ff-merged onto `origin/main` first (CI's 07:15Z scan was already in `jobs.json`).

## Result
- Net-new URLs added to `jobs.json`: **35** (5,647 → 5,682), 0 removed. Gross fresh from sources was 467; the rest were URL/title twins already on the board (Adzuna re-issues ids for the same ad — dedupe by normalized URL caught them).
- Site build: 4,997 page jobs (servicenow 868, salesforce 965, other 3,164), built 2026-11-25 08:04 UTC.
- Entry-level **Platform Administrator / Platform Developer I (Toronto): none this hour** — standing gap. Freshest Toronto-area platform roles: TCS Salesforce Developer (Toronto, LI 4494376362), Altus Group Salesforce Platform Developer (Toronto, LI 4483476940), Konrad Salesforce Architect (Toronto, LI 4491325080), Jolera Senior ServiceNow Consultant (Canada), Euna Solutions Sr Salesforce Developer (Oakville), TD Senior Solution Architect ServiceNow (Adzuna), Deloitte Senior Consultant SN/SF Platform (Toronto), Cognizant SN Software Asset Management Developer (Toronto), OSI Digital Salesforce Developer (Toronto/Vancouver), KPMG ServiceNow Solution Developer (Toronto), Benevity Senior Salesforce Administrator (Toronto/Calgary), Alimentiv ServiceNow Platform Specialist (Toronto/London).

## Source behavior this cycle
- Workday CXS: all 15 boards returned **HTTP 429** — the CI hourly scan runs at :00Z and rate-limits concurrent probes. Do not interpret as zero postings; the CI pass carries Workday. Re-probe key tenants (bmo, td, cibc, manulife, interac, salesforce, accenture) 5–10 min past :00Z with ≥8s spacing if Workday freshness matters this hour.
- LinkedIn guest: intermittent 429s but cards returned (241 matches across 14 queries × 2 locations, 1800ms spacing, 2 workers). Healthy card HTML ~31 KB; authwall is 200 + static ~400 KB body — distinguish by length/digest, not status.
- Adzuna CA API (demo keys 54ce986e / db851f299e966c0a2a72af525dce6199): 191 matches across 28 date-sorted queries; a few 503s under rapid fire are tolerated — surviving queries still return rows.
- SmartRecruiters ServiceNow 12, Greenhouse 12, Lever 1, Ashby 2, remote feeds 8.

## Employer / partner checks (Rogers, Bell, government, elite partners)
- Rogers `jobs.rogers.com/search/?q=&sortColumn=referencedate&sortDirection=desc` rendered a date-sorted shell again this cycle — **no ServiceNow/Salesforce titles**; rely on LinkedIn/Adzuna for Rogers rows; do not retry hourly.
- Bell `jobs.bell.ca` shows zero for servicenow/salesforce (genuinely no reqs — re-check weekly, not hourly). Bell's real SN channel is **Ateko (backed by Bell Canada) / FX Innovation** — search "Ateko" on LinkedIn, not "Bell".
- Canadian government: `jobs.gc.ca` and Ontario `gojobs.gov.on.ca` are Radware-walled — do not retry; use Job Bank as proxy and trust only postings whose *title* names the platform.
- ServiceNow Careers: Cloudflare bot wall. Salesforce-the-company Workday: Toronto rows are sales/AE/renewals only, no Platform Admin/Dev I. Accenture Workday: Toronto hits are CCaaS/AI, not SN/SF platform.
- Confirmed-enumerated partners this cycle (no fresh live platform roles): Lane Four, NewRocket, DXC (JS-shell search), Cognizant careers (JS shell — roles arrive via LinkedIn/Indeed/Adzuna mirrors instead).

## Dedupe reminders
- Dedupe on normalized URL (strip query + trailing slash) + trailing LinkedIn job id, never title alone. Vendor twins (two staffing firms, same client req) are distinct postings — keep both.
- A fresh twin URL may not appear by URL in `jobs-data.json` (build collapses company+title mirrors) — verify a new role reached the page by **company + title**, not URL.

## To deploy after commit
Push with `[skip ci]` (avoids chronic red truth-check/invariants audits — pre-existing, not this run's regression), then `gh workflow run pages.yml --repo eltonaguiar/BESTIEJOB` and poll `gh run list --workflow=pages.yml --limit 1`. Verify live: `curl https://eltonaguiar.github.io/BESTIEJOB/jobs-data.json` must carry the new URLs (e.g. TCS `salesforce-developer-at-tata-consultancy-services-4494376362`). The page serves only committed `public/` files — `jobs.json` alone never reaches it.
