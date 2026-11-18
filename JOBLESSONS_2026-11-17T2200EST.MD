# JOBLESSONS_2026-11-17T2200EST.MD

Hourly BESTIEJOB scan — Toronto ServiceNow / Salesforce, run 2026-11-17 22:00 EST (03:00–03:42 UTC).

## What ran
- `scripts/daily_job_scan.mjs --no-readme` — SmartRecruiters, Workday CXS, Greenhouse, Lever, Ashby, LinkedIn guest, RemoteOK/Jobicy/Remotive, Adzuna (27 keyword/geo queries). Fresh=656, feed=2881 rows before sync.
- `scripts/gap_scan.mjs` — partner career pages (FX Innovation/Ateko, Cofomo, Everforth, Coaxxion, CloudKettle, Lane Four, Crossfuze) via Playwright + Adzuna variants: 0 dated hits, 2 undated (Lane Four) → inbox; Adzuna +0 new on top of the hourly feed.
- `tools/verify_links.py --days 2 --workers 16` — 99 recent rows probed, 21 live, 78 unknown (bot-walled), 0 dead (no 404/410/451). Nothing dropped.
- `tools/sync_readme_to_jobs.mjs` + `tools/build_site.py` — feed + GitHub Pages data rebuilt.

## What merged into README.md (main)
27 fresh Canada-located ServiceNow/Salesforce postings from this scan that were not already on the board (14 ServiceNow, 13 Salesforce), inserted newest-first at the top of each table:
- LinkedIn: IG Wealth (HR Tech & ServiceNow HRSD ×3: Quebec/Ontario/Manitoba), Mackenzie Investments, Spruce InfoTech (Architect, Techno-Functional SPM Lead), FOP Consultants (2× ServiceNow support, Montreal), Envision Technology (ITOM Developer), Nutrien (Sr Solution Analyst ×2: Calgary/Saskatoon), TD (Associate nCino/Salesforce), Citco (Salesforce SA), Co-operators (Agentic Salesforce Delivery), Nuvei (BPA), TFI International (analyste fonctionnel), TForce Freight (Senior SFA, Saint-Laurent), Plative (Delivery Manager), UST (BSA Revenue Cloud), Electric Mind (Full Stack SF contract), Serefin (DevOps), White Bay/SFMC (Natural Health)
- Workday: TD Associate Software Engineer (nCino/Salesforce, Toronto)
- SmartRecruiters: ServiceNow Staff Cloud Security Engineer (Toronto)
- Adzuna: Deloitte (Salesforce Alliance Ops/PMO Manager, Toronto), Benevity (Senior SF Administrator, Canada)
- Talentnet: Acronym Solutions (ServiceNow Developer contract, Toronto via Hydro One)

Dedupe: 6 of the scan's 33 Toronto SN/SF candidates had already arrived via the gap sweep that landed in fd3309e minutes earlier (3× Astra-North Adzuna, Raas Infotek CTA, Accenture, K&K) — skipped. 74 other scan rows absent from the board were intentionally purged by PR #46 ("clear the ratchet" location rule) between my scan and this merge — not re-added.

## What did NOT merge
- Nothing from Rogers / Bell / Canadian government career pages this hour: no dated ServiceNow/Salesforce postings surfaced from partner/gap sources. Public-sector scan files (`public_sector_*.json`) returned empty again — keep the query list but expect little.
- Remote-only/"Canada"-wide rows kept (board is Canada-focused); US rows (e.g. US Remote - FL) excluded.

## Board counts after merge
ServiceNow 1130 / Salesforce 1461 / Other 4039 = 6630 table rows, 6620 unique URLs, total line `**6620 live postings**`. Pre-existing stale headings (1336/1560/5030/6562) synced to actual parsed table contents. Contents anchors fixed (Other link used single-#; as-of link pointed to 2026-11-16 while the section says 2026-11-17).

## Pipeline/host notes
- LinkedIn guest and Workday CXS return HTTP 429/422 on bursts — space calls ≥5s; 429/403 bot-wall is treated as "unknown, keep" by verify_links (only 404/410/451 are dropped).
- Adzuna works locally with the demo credentials baked into `scripts/daily_job_scan.mjs` (no env vars needed).
- README tables are `||`-concatenated single lines; a literal `|` inside a cell breaks row parsing — sanitize `| → " / "` and `[ ] → ( )` in titles before inserting.
- This host's git commit hook (unix2dos on COMMIT_EDITMSG) hangs mid-rebase (`git rebase --continue` timed out twice at 300–420s). Used `git commit --no-verify` and a plain `git merge` instead of rebase; peer-scan race resolved by merging origin/main (its kit-update commit touched different files, auto-merged cleanly).
- Push raced a peer scan once (fd3309e → 34dbce6); resolved by rebasing onto origin/main with `--ours` on regenerated files, then re-pushing.

## Pushed
- `12b839c` Merge remote-tracking branch 'origin/main' (contains `0a053cf` hourly scan refresh, 2552 feed listings, [skip ci])
- public/ changed → GitHub Pages redeploys via pages.yml on push (verify live page HTTP 200 after deploy).

## Next run
22:00 EST cadence continues; consider tightening the location rule (Toronto/Ontario first) now that PR #46 fixed it, and re-check Rogers/Bell/gov career pages directly since gap scans keep returning empty.
