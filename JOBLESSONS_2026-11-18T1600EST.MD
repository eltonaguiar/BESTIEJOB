# JOBLESSONS_2026-11-18T1600EST — BESTIEJOB hourly cron scan (16:00 EST)

## Scan scope
- Target: fresh Toronto / Canada ServiceNow and Salesforce postings (Platform Admin / Platform Developer I emphasis for Salesforce; ServiceNow platform, CSA/CAD/CIS certs for SN).
- Freshness window: posted today / yesterday (2026-11-17, 2026-11-18).
- Sources scanned: Adzuna (dated API), Job Bank, Eluta, LinkedIn guest; City of Toronto SuccessFactors; Ontario Public Service (Job Bank proxy); ServiceNow World Forum Toronto sponsor ATS boards.

## Result
- Fresh Canada SN/SF postings surfaced this hour: 1 (1 ServiceNow, 0 Salesforce).
  - 2026-11-18 | ServiceNow Developer - Remote Contract | 2iSolutions Inc. | Canada | ca.linkedin.com/jobs/view/servicenow-developer-remote-contract-at-2isolutions-inc-4492201395 (fresh-ca linkedin-guest)
- New to the board from this scan: 1 — staged as `inbox/fresh-ca--2026-11-18--v1.md`; merger `+1 new` for that file (total `+5` rows including 4 rows from pre-existing unmerged websearch inbox leftovers). README counts: 6220 → 6223.
- `tools/build_site.py`: OK — 4944 jobs indexed (SN 818 · SF 882 · Other 3244), 822 duplicate mirrors collapsed, 31 applied hidden, newest 2026-11-18. `public/index.html`, `public/jobs-data.json`, `public/jobs.json` rebuilt.
- public_sector_scan: City of Toronto 13 tiles (0 undated), all already boarded; OPS gojobs.gov.on.ca Radware-walled; OPS Job Bank proxy 10 articles, 0 new → 0 new public-sector jobs.
- partner_sponsor_scan (boards-only): 1/15 Workday tenants answered; 0 board-verified SN/SF postings; 18 sponsors confirmed-but-empty → 0 new partner jobs.

## Partner / employer look (Rogers, Bell, Canadian government, Elite/SN-SF partners)
- Rogers: `jobs.rogers.com` Phenom board unreachable (HTTP 404 / 9-byte body). Re-check weekly, not hourly.
- Bell: `jobs.bell.ca` renders empty shell / (0) reqs for servicenow and salesforce. Re-check weekly.
- Canadian government: `jobs.gc.ca` / `gojobs.gov.on.ca` Radware-walled (captcha) — do not retry. Job Bank used as proxy; trust only postings whose TITLE names the platform.
- Salesforce-the-company: no Platform Admin / Developer I in Toronto under 4 days old.
- ServiceNow-the-company: Toronto postings are sales/SRE/security only — no platform roles this run.
- ServiceNow World Forum Toronto sponsors (Ateko, Deloitte Canada, EY, KPMG, Cognizant, Fujitsu, Ondaro, TELUS, OpenText, BDO Canada, CDW, Compugen, IBM, NewRocket, Pentio, TELUS, CGI, Long View, Procom, Robert Half, TEKsystems, Avanade, etc.): board slugs verified only when the board page's own title named the employer; zero carried a fresh SN/SF posting this run.

## Source / API notes (reusable next hour)
- `scripts/fresh_ca_scan.py --verify 1` times out on this host (per-URL HEAD verification with 20s timeouts + Adzuna rate limits). Ran successfully with `--verify 0` (dedup against jobs.json + README still applies at scan + merge time). Keep `--verify 0` for the hourly cadence; the merger re-gates on URL/fingerprint.
- LinkedIn guest `seeMoreJobPostings` 429s after ~4 rapid queries — this run used 16 requests spaced ~1.5s and completed. `f_TPR=r86400` is the right window; `r3600` is near-empty pre-dawn EST.
- Adzuna 503s under rapid queries — space calls ≥3 s; this run made 68 calls successfully.
- Dedupe: normalize URL (strip query + trailing slash); `title|company|city` fingerprint catches re-advertised requisitions across mirrors (30 rows already on board by URL, 1 more by title fingerprint this run).
- Workday CXS is reachable but most Canadian tenants 422/404/521 on this host; only 1 of 15 sponsor tenants answered. Known-working Canadian pairs from prior runs: bmo.wd3/External, td.wd3/TD_Bank_Careers, cibc.wd3/search.

## What did not change
- `ServiceNow_Learning_TSOM-_CSM_FSM_SalesCRM_HAM_ITSM/` (pre-existing working-tree modification, unrelated to this scan — left uncommitted).
- `inbox/` left as submitted (merger run without `--bump-inbox`; `fresh-ca--2026-11-18--v1.md` remains in inbox).
- `raw/public_sector_2026-11-18.json` and `reports/fresh_ca_2026-11-18.json` written as scan artifacts.

## Next run (17:00 EST)
- Retry `fresh_ca_scan.py --verify 0` with LinkedIn guest; re-poll Rogers/Bell/GC careers portals; re-scan ServiceNow World Forum Toronto sponsor boards; confirm the 2iSolutions role is still live before anyone applies.
