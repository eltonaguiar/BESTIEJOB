# 2026-11-10 Active jobs audit & geo cleanup

- Added reusable audit tool: `tools/audit_active_jobs.py` (geo bucket + HTTP liveness probe, single-URL mode, JSON/MD report).
- Added skill: `.kilo/skills/job-location-audit/SKILL.md`.
- Evidence: `raw/job_audit_geo_all.json`, `raw/job_audit_probe_flagged.json/md`.

## Accenture ServiceNow HAM (Sydney) case
- Reported listing: *ServiceNow Hardware Asset Management (HAM) Consultant* — Accenture (Employer board, Canada shown elsewhere) was **not present** in `jobs.json` or public feeds.
- Found in raw fingerprints as `https://accenture.wd103.myworkdayjobs.com/en-US/AccentureCareers/job/Sydney-International-House-3-Sussex-St/ServiceNow-Hardware-Asset-Management--HAM--Consultant_14379035` (req 14379035).
- Verified live 2026-11-10 via Workday CXS: `locationsText/country = Sydney, International House, 3 Sussex St / Australia` (active, not Canada/Toronto). Not added; no feed removal needed.

## Board-wide geo/liveness audit (1933 jobs)
- Buckets (heuristic, no-probe): toronto_gta 634, canada_other 605, other 434, remote_canada 101, us 50, unknown 48, remote_unknown 40, **international 22**.
- Probed flagged scopes (`international,us,other,unknown,remote_unknown`, n=593): active 239, dead 61, unknown 293 (bot-protected/unreachable).

## Removed from feeds (verified, out-of-scope/dead)
- Dead international (8): 8 URLs removed.
- Active but international-only/non-Canada locations (6, India/Mexico/Germany/UK/India-remote roles): removed.
- Kept mixed-region Canada-eligible postings (2, infisical: Brazil/Canada/Europe/USA).

### Removed URLs

- https://careers.teamviewer.com/jobs/7740495-senior-software-engineer-servicenow
- https://jobs.lever.co/jobgether/1a5a8d32-26cb-46a5-8b81-449f520cd163
- https://jobs.lever.co/jobgether/551d08de-9723-4cf8-b288-e6f59a34b58a
- https://jobs.lever.co/jobgether/79423eaf-8b00-41e4-a028-cf2c3cb096e6
- https://jobs.lever.co/jobgether/845777f3-4a3a-4a5f-82b0-9ba85d4c0790
- https://jobs.lever.co/jobgether/8f6ecbb2-9bba-4c39-ab9f-8befeb5f9738
- https://jobs.lever.co/jobgether/bd0d5b21-c046-4e6b-82a8-fc1e8cfc6d37
- https://jobs.lever.co/jobgether/be192983-e3e6-4511-96a2-85587d6f6219
- https://jobs.lever.co/jobgether/c7c64363-d9fd-47c5-8556-71ca3bda4f0d
- https://jobs.lever.co/jobgether/c8c6ebee-f3cf-441a-9138-d4ee924b2ccd
- https://jobs.lever.co/jobgether/d580a817-89b1-4a2f-ba28-c343e87f3507
- https://jobs.smartrecruiters.com/ServiceNow/744000159378549
- https://www.okta.com/company/careers/opportunity/7727730?gh_jid=7727730
- https://www.okta.com/company/careers/opportunity/8053763?gh_jid=8053763
