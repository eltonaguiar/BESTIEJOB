# JOBLESSONS — hourly scan 2026-11-24T14:00EST (Toronto time)

Scan window: Tuesday 2026-11-24 14:00 EST (19:00 UTC). Base: origin/main 2883036f (jobs.json 5,635 rows at start), README auto-scan block 4,489 live postings from 7 public sources. Board: github.com/eltonaguiar/bestiejob (main). GitHub Pages: eltonaguiar.github.io/BESTIEJOB/

## Result

One fresh posting verified live this cycle; merged to README.md under "Verified fresh additions — cron scan 2026-11-24T14:00EST", inserted into jobs.json + public feeds, and the site rebuilt (public/jobs-data.json + index.html: 4,982 cards, Other 3,161). Deduped by URL against jobs.json, README.md and APPLIED.md. Zero roles removed.

## What was verified live (added)

- Randstad Digital — Senior Enterprise Risk Management Analyst — Greater Toronto Area, Canada — LinkedIn guest-search card (posted 2026-11-23; "14 hours ago" at capture) and the detail page confirmed live in a real browser: business administrator for the client's enterprise GRC platform, PowerBI/SQL/Python/Alteryx reporting, configures GRC forms/workflows/reference data/user access. Staffing agency; the end client (a Canadian private mortgage insurer) and the GRC platform are not named in the public ad → filed under Other/GRC track, not ServiceNow/Salesforce.

## What was checked and yielded NOTHING net-new

- Adzuna CA + Job Bank + Eluta freshness sweep (scripts/fresh_ca_scan.py, window 2026-11-23..24; 68 Adzuna calls, 14 Job Bank pages, 6 Eluta pages): 26 raw rows → 3 unique → all 3 already on the board by URL. Zero net-new.
- LinkedIn guest sweep already run today (11:47Z, 1,506 cards): 4 fresh-by-URL cards (Insight Global Sr Salesforce Developer, LanceSoft Salesforce Integration Automation Engineer, INNOVA Salesforce Specialist, Slalom Leader Salesforce Digital) — all merged into README at 12:49Z. Zero net-new this hour.
- This morning's LinkedIn Toronto captures (raw/linkedin_sn_toronto.html, raw/linkedin_sf_toronto.html, 09:12 EST, 10 cards each): 12 of 13 platform candidates already on the board/feed (Deloitte ServiceNow Platform 4460515123, Deloitte ITOM Discovery 4460512143, Deloitte CSM 4460519030, Konrad Salesforce Loyalty 4491312520, Deloitte Salesforce Platform 4460507232, Pacer SFMC 4494026997, Konrad Data 360 4491325080, Highspring Salesforce Developer 4493661253, Cognizant Salesforce QE 4494089031, CGI FSC BA 4492043976, Manulife PM 4467185175, NLB 4494085039, Metrolinx 4494070999). Only the Randstad GRC role was new.
- Partner/sponsor scan (scripts/partner_sponsor_scan_verified.py --boards-only; 40 ServiceNow World Forum Toronto sponsors + associates): 0 relevant postings; 1/15 Workday CXS tenants answered; slug guesses for Ernst & Young, KPMG, Crossfuze, Blue Mantis, Brightfin, Tech Mahindra rejected by the board-title identity check.
- Public sector (scripts/public_sector_scan.py): City of Toronto 15 tiles, 1 new posting — SYSTEMS INTEGRATION SPECIALIST (AMANDA Developer/Administrator), posted 2026-11-10 — not a ServiceNow/Salesforce platform role (AMANDA), excluded per the board's own rule. OPS gojobs Radware-blocked; OPS Job Bank feed 14 articles, 0 OPS rows.
- Rogers (jobs.rogers.com): HTTP 200, 170 KB server-side shell, zero servicenow/salesforce strings → no platform roles.
- Bell (bell.ca/careers): HTTP 200, 338 KB, zero servicenow/salesforce strings → no platform roles.
- ServiceNow Careers and Salesforce Careers: Cloudflare bot verification (as in prior cycles) — not enumerable from this host.
- Government of Canada Job Bank / canada.ca: September–October 2026 postings only — stale.

## Patterns / lessons

1. Aggregator freshness yield has collapsed to ~0–1 net-new per hour: the only new row this cycle came from this morning's LinkedIn capture (first seen 09:12, still unboarded at 14:00). LinkedIn guest search is the reliable freshness oracle; Adzuna/Job Bank/Eluta mostly re-serve boarded rows.
2. A LinkedIn guest sweep of 40 keywords × 1 location × 2 pages takes >5 min and will hit a 300 s foreground timeout — run it with background=true + notify, or mine the day's existing raw/linkedin_guest_<date>.json and raw/linkedin_*_toronto.html captures before re-sweeping.
3. Derive posted dates from each card's <time datetime="YYYY-MM-DD"> attribute; "N hours ago" on the card is a relative clock and must never be converted into a date by arithmetic.
4. scripts/fresh_ca_scan.py (LinkedIn pass), scripts/public_sector_scan.py and scripts/partner_sponsor_scan_verified.py (Workday/search lanes) need curl_cffi on this host (`pip install curl_cffi`); without it the LinkedIn/OPS passes skip or abort with FATAL.
5. The board is readme-first: scripts/sync_readme_to_jobs.mjs only parses `### <family> jobs` tables, NOT the "Verified fresh additions" `##` log sections. A row added only to a log section reaches the page (tools/build_site.py extracts every dated row line) but never jobs.json — to keep the feed consistent, insert the row into jobs.json with the linkedin schema (id `linkedin:<host>/<path>`, postedDate `T00:00:00.000Z`) and update meta.total, or route it through tools/jobs_merge_inbox.py into a canonical table.
6. build_site.py classifies by keyword (service now|itsm|itam|cmdb|itom → ServiceNow; salesforce|apex|sfdc|... → Salesforce; else Other). A GRC platform administrator whose ad never says "ServiceNow" correctly lands in Other — do not force it into the ServiceNow table to make the feed pick it up.
7. GRC/IRM platform-admin roles are currently surfacing through staffing agencies (Randstad Digital) with the platform unnamed in the public ad — include with the agency labelled and the platform declared "not named", rather than inferring ServiceNow GRC.
8. Rogers and Bell careers remain zero-yield server-side shells, and the partner Workday CXS matrix is mostly dead (14/15 tenants no answer) — budget the hour on LinkedIn/Adzuna instead of re-probing them every cycle.

## Negative space (searched, nothing fresh)

- LinkedIn "Platform Administrator" / "Platform Developer I" Toronto: no fresh postings this hour.
- Workday Canadian bank tenants (bmo / td / cibc / manulife): no new answer beyond prior scans.
- Job Bank site search: no title-named platform postings newer than what the board already carries.

## Next cycle (2026-11-24T15:00 EST)

- Re-run the LinkedIn Toronto guest search (past 24h) in the background — card-level evidence suffices for adds with discovery dates.
- Re-check Cognizant and Deloitte Canada (consistent yield), plus the Randstad Digital / staffing GRC channel.
- Re-run Indeed CA / Adzuna date-sorted searches for ServiceNow and Salesforce.
- Skip Rogers / Bell / ServiceNow / Salesforce employer portals (repeatedly zero-yield or bot-walled).
