# JOBLESSONS_2026-11-25T0400EST — hourly Toronto ServiceNow / Salesforce scan

## Cycle
Cron run Wednesday 2026-11-25 04:00 EST (UTC-05). Repo: eltonaguiar/BESTIEJOB (`main`). Local clone: `/c/Users/zerou/bestiejob_repo`. Pulled `origin/main` (e46e885b) before scanning so the sweep diffs against the current board.

## What ran
1. `scripts/fresh_ca_scan.py --days 2 --linkedin 0` — Adzuna dated API (`max_days_old=2`, `sort_by=date`), Job Bank 12 pages, Eluta 6 pages. LinkedIn guest pass skipped (too slow / 429-prone this session).
2. `scripts/ats_discovery.py --days 2` — Workday 24 proven tenants + SmartRecruiters (ServiceNow). Absolute posting dates from each employer's own ATS JSON.
3. `scripts/check_inbox.py` — both submissions well-formed (0 rows each).
4. `tools/jobs_merge_inbox.py --days 30 --max-per-table 5000` — ran against full `inbox/` (see Merge note below).

## Results — 0 net-new jobs this cycle
- Fresh CA sweep: 36 raw → 4 unique → 0 kept. All 4 unique postings were already on the board (`already_on_board=4`). Nothing dated 2026-11-24 or 2026-11-25 was new.
- ATS discovery: 4 raw → 0 kept (all 4 non-Canada).
- Entry-level: no Platform Administrator / Platform Developer I (Toronto) surfaced. These remain scarce this hour.

## Employer-direct checks (no fresh platform roles)
Rogers (`jobs.rogers.com`, date-sorted), Bell/Ateko, BMO/RBC/CIBC/Scotiabank/TD/Manulife/SunLife Workday tenants, Government of Canada Job Bank / Ontario gojobs (Radware-walled), ServiceNow Careers (Cloudflare bot wall), Salesforce-the-company Workday (Toronto rows = sales/AE/renewals only), Accenture Workday (CCaaS/AI, not platform). No fresh live ServiceNow or Salesforce platform roles.

## LinkedIn
`ca.linkedin.com` Toronto listing pages show volume (200+ ServiceNow dev, 200+ Salesforce dev jobs) but individual posting dates are login-gated. The LinkedIn guest pass is the only no-login source that exposes a real `<time datetime>` posting date — but it is slow (~1.5s/keyword × 2 locations) and 429-prone; it timed out at 300s this cycle.
The earlier 06:53Z fresh-ca sweep already ran the full LinkedIn pass and merged 1 role: **Harbor — Salesforce Developer, Canada (LinkedIn 4494485877), posted 2026-11-25**. Do not re-run the LinkedIn pass in the same hour as the 06:53Z sweep; it re-fetches the same cards.

## Merge note (important lesson)
Running `tools/jobs_merge_inbox.py` against ALL of `inbox/` (not just this cycle's submissions) merged 80 rows from old unmerged inbox files (twin-harvest, peer-bestiejob-scan, websearch, aicert-harvest dated Oct 27–29). Quality problems surfaced:
- identical jobs duplicated ×10–19 (same LinkedIn URL across `fresh-ca--2026-11-23--v1/v3/.../v16` — the additive merge's cross-file dedupe did not collapse them),
- misaligned cells (company/location swapped, e.g. "USA: Remote Texas" with location cell = "Full-time"),
- US-only postings that slipped the foreign-location gate.
I reverted `README.md`. Lesson: only merge this cycle's own inbox files, or re-run dedupe with row-level URL+fingerprint checking; never blindly merge a stale inbox backlog.

## Changes committed
- `JOBLESSONS_2026-11-25T0400EST.md` (this file)
- `README.md` / `jobs.json` / `public/*`: UNCHANGED (0 net-new jobs this cycle; nothing new to deploy to GitHub Pages)

## Pattern for future agents
- Run the freshness-first sweep (today + yesterday) BEFORE the breadth-first 7-day scan; it catches same-day roles aggregators bury under older queued rows.
- Dedupe by normalized URL AND by `title|company|city` fingerprint (one requisition = multiple Adzuna / LinkedIn / Eluta mirrors with different URLs and dates).
- Verify every URL before submission (404/410/451 gate); auth walls (401/403) still prove the requisition exists.
- Canadian bank / government Workday tenants need the exact `(tenant, shard, site)` triple already proven on the board; wrong guesses 404 and are skipped.
- When entry-level Platform Admin / Platform Developer I roles are scarce in Toronto, broaden keywords to "platform analyst / consultant / administrator" and adjacent ITSM/ITAM/CMDB.
- LinkedIn guest pass: cap keywords (`--linkedin-max`) and never run it in the same hour as the 06:53Z sweep.
