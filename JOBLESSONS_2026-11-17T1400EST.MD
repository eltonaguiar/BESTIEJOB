# JOBLESSONS_2026-11-17T1400EST

## Run
14:00 EST hourly scan for fresh Toronto ServiceNow / Salesforce jobs against github.com/eltonaguiar/BESTIEJOB (main).

## Fresh, verified, merged (1)
- Acronym Solutions Inc. (formerly Hydro One Telecom Inc.) — ServiceNow Developer (Contract), Toronto, ON (hybrid, 5 months), posted 2026-11-16. URL: https://hydroone.talentnet.community/jobs/272e8208-a275-4f85-af68-a443053ed133. Requires CSA/CAD certs; mentions TSOM/CSM/FSM/Sales CRM/HAM/ITSM, ServiceNow Studio, MID servers, REST/SOAP APIs. Source: talentnet. Added to jobs.json, liveness-gated (HTTP 200), rebuilt, pushed to main (ca70729); GitHub Pages redeployed via manual pages.yml dispatch (run 44155585686 success, live generatedAt 2026-11-17T19:09:57Z, live count 5986, Hydro One confirmed on live page).

## Dedupe — nothing added (already on board)
- Altus Group — Salesforce Platform Developer (LinkedIn 4483476940) — already tracked.
- Gap-scan Adzuna hits (Astra-North Infoteck x5, Cognizant, Pacer Group Salesforce FSC Developer, Bank N.A. ServiceNow CMDB Administrator) — all already on board.
- City of Toronto SYSTEMS INTEGRATOR 1 (ServiceNow Developer) and Senior Systems Integrator Technology Services ServiceNow — already tracked.
- Bell — Salesforce Developer roles already tracked; jobs.bell.ca shows zero ServiceNow reqs.

## Searched, no platform-role add
- ServiceNow-the-company Toronto hits (Staff Systems Engineer JB0073788 posted Nov 06, Senior SRE Canada Protected B Nov 05, Manager Systems Engineering 18h ago, Senior Staff Cloud Security Engineer 3h ago) are senior SRE/security/engineering or management roles that do not mention the ServiceNow platform or CSA/CAD certs — excluded per board rule (no platform-adjacent adds).
- Salesforce Platform Administrator / Platform Developer I: Altus Group already tracked; Finning Platform Administrator is Calgary (out of Toronto scope); no fresh Toronto entry-level Platform Admin/Dev I surfaced.
- Rogers careers (jobs.rogers.com): Phenom board reportedly unreachable via curl; check weekly, not hourly. site:jobs.rogers.com returned no indexed SN/SF postings.
- Canadian government: City of Toronto SN roles already tracked; no fresh federal GC SN/SF Platform roles surfaced this run.

## Pipeline notes
- verify_links.py --days 2: probed 126 rows, live=31, dead=0, unknown=95, nothing dropped.
- build_site.py: 5986 jobs (servicenow 966, salesforce 1020, other 4000), 975 duplicate mirrors collapsed, built 19:08 UTC.
- Push to main rejected once (non-fast-forward; remote f397071 ahead of local base 7dd57a9). Rebased onto origin/main; remote jobs.json (2844 rows) did NOT contain Hydro One, so re-added it (2845), re-gated, rebuilt, pushed ca70729.
- pages.yml push trigger is suppressed by [skip ci] (data-only pushes never trigger it); triggered pages.yml manually via workflow_dispatch — deploy run 44155585686 success; live page now shows Hydro One. Otherwise page refreshes at the :35 UTC cron.
- Browser sandbox has no DNS (browser_exec cannot resolve); web_extract ddgs backend is search-only (cannot fetch arbitrary URLs). Direct Python urllib works for live HTTP probes (used to verify the Hydro One URL).
- Market shape this cycle: fresh Toronto platform work is scarce; most fresh SN hits are ServiceNow-the-company senior engineering/security roles (excluded), not Platform Admin/Dev I.
