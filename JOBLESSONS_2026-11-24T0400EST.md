# JOBLESSONS_2026-11-24T0400EST

Hourly scan notes, Toronto ServiceNow / Salesforce, 2026-11-24 04:00 EST (09:00 UTC).
Commit 56abc65 on eltonaguiar/BESTIEJOB main; GitHub Pages redeployed (run 45363460392, success).

## What was added

9 fresh postings, deduped by URL against jobs.json, README.md and APPLIED.md:

ServiceNow (6)
- Insight Global — ServiceNow Developer (Intermediate), 6-month contract, Toronto, ON. Listed ~1 day ago on LinkedIn; LinkedIn guest detail pages are walled from this host, so liveness was established via the current LinkedIn search listing (snippet shows title/employer/location/timing). Row asterisked with discovery date 2026-11-24 per board policy.
- Blue Mantis — Sr ServiceNow Business Process Consultant, Toronto ON (remote hybrid, Concord ON onsite option). Job Bank 50771689, posted 2026-11-20, CSA required, $100K-$112K CAD.
- G-FORCE IT SERVICES INC. — Information Technology Service Management Consultant, Toronto ON on-site. jobs.ca, posted 2026-11-17.
- Apptoza Inc. — Project Manager – ServiceNow, Toronto ON hybrid contract. jobs.ca, posted 2026-11-20.
- Pacer Group — ServiceNow Implementation Architect, Toronto ON hybrid. jobs.ca, posted 2026-11-12, deadline 2026-11-30, $135K-$140K, CSA + CIS-ITSM + one CIS required.
- Source Code — Specialized IT Consultant - Intermediate (ServiceNow SPM), Toronto ON on-site at 55 John St. Job Bank 50698289, posted 2026-11-08; mandatory ServiceNow CSA + CAD.

Salesforce (3)
- Konrad — Salesforce Architect (Loyalty & Data 360), Toronto ON full-time. konrad.com careers page directly browsable and current (Apex, LWC, Data 360, Loyalty Management, Marketing Cloud, CI/CD); listed ~6 days ago on LinkedIn, row asterisked with discovery date.
- CoreKloud Technologies — Salesforce Developer (FSC), Toronto ON hybrid, $90-$100/hr. Indeed/SimplyHired listing, ~9 days old.
- Harbor — Salesforce Developer, Remote Canada. Remotive/Built In listing, ~4 days old; "Remote, Canada" implies Ontario eligibility.

## What was checked and rejected

- Scotiabank ServiceNow Discovery Developer: looked fresh in LinkedIn search ("3 days ago") but jobs.ca shows Posted 2026-09-05 and CareerBeacon datePosted 2026-10-09 with validThrough 2026-11-09 — expired. Rule: trust the employer/Job Bank absolute date, never the search relative label.
- Bonafide Info Systems ServiceNow ITOM Developer (Job Bank 50740706, Nov 16) and ServiceNow CMDB Consultant (50740661, Nov 16): already on the board (dupes by URL).
- EQ Bank Senior ServiceNow Engineer (lever.co/eqbank), Scotiabank ServiceNow Developer (linkedin 4423415449), Interac Technical ServiceNow Lead (linkedin 4126302101), Konrad Salesforce Architect LinkedIn mirror (4491325080), Paralucent Salesforce Architect (careers.paralucent.com/o/salesforce-architect-senior-manager-advisory): already on the board (dupes by URL).
- Moneris Principal Salesforce Developer (Workday JR106006-2): posted 2026-10-28 / Sep 19 — too old, not fresh.
- Cognizant Salesforce Developer 00071305431: published Nov 12 2026 — already on the board from the 02:00EST scan.
- Employer-direct this cycle: Rogers jobs.rogers.com Technology — no platform roles; Bell ServiceNow System Administrator req 4476350097 considered but not fresh (prior cycles noted Bell ServiceNow reqs filled/expired, Salesforce SysAdmin expired Jul 2026); Atego/FX Innovation portal not enumerable headless (ServiceNow routes to fxinnovation.com, Salesforce to ADP Workforcenow); Government of Canada Job Bank scan surfaced only the three roles above (Blue Mantis and Source Code new; Bonafide already on board). No fresh live Government of Canada direct portal roles beyond Job Bank listings.

## Patterns / lessons for future scans

1. Job Bank (jobbank.gc.ca, incl. on.jobbank.gc.ca / mb.jobbank.gc.ca) is a strong freshness source for Toronto SN/SF and shows absolute "Posted on" dates — prioritize it; Canadian government angle covered via Job Bank postings, not direct GC careers pages (those returned September–October stale postings in prior cycles).
2. jobs.ca postings carry absolute posted dates and full descriptions — preferred source; jobs.ca company detail pages are posting pages, not listing pages (safe to index).
3. LinkedIn guest detail pages return "Page not found" from headless Chrome on this host; never treat the wall as a real 404. Verify via search-index snippets + aggregator mirrors (Glassdoor, Workopolis, SimplyHired, ZipRecruiter, Job Bank), and asterisk discovery dates.
4. Relative labels ("1 day ago", "6 days ago") must not be back-calculated into absolute dates — mark with discovery date + asterisk per board policy.
5. Known partners/sponsors with current Toronto hiring this cycle: Konrad (Salesforce, Toronto World Tour sponsor) careers page is directly browseable; CoreKloud (Salesforce partner) hiring via aggregators; Insight Global (staffing) with a ~1-day-old ServiceNow contract. ServiceNow Inc. careers Toronto roles this week were sales/systems (not platform build), except Senior Systems Engineer already on board.
6. Always re-run the dedupe check by URL before merging: 6271 URLs already on the board; several apparently-fresh hits were duplicates under different mirrors (Scotiabank, EQ Bank, Interac, Cognizant).
7. Commit without [skip ci] so the GitHub Pages deploy workflow (pages.yml, push trigger on public/** + README.md) runs immediately; the separate :35 UTC scheduled redeploy is a fallback. Watch concurrency group bestiejob-main-write: the scheduled hourly scan ran alongside this push and failed (could not rebase/push behind main advance) — expected, no data loss.

## Files touched

- README.md: new "Verified fresh additions — hourly scan 2026-11-24T04:00EST" section (9 rows)
- jobs.json: +9 jobs (total 5635), meta updated
- public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json: mirrors updated
- public/jobs-data.json, public/index.html: rebuilt via tools/build_site.py

Next scan (05:00EST): re-check Insight Global LinkedIn listing persistence, Konrad careers page date, and Rogers/Bell/Ateko/Job Bank employer-direct again.
