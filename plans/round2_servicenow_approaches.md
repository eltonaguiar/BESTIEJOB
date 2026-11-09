# Round 2 — ServiceNow: 20 Brand-New Search Styles (not used in Round 1)

Round 1 reused existing scanners. Round 2 deliberately changes the *method*:
instead of querying boards for keywords, it finds postings by adjacency,
registry, geography, and infrastructure.

## A. Vendor-ecosystem routes (find the employer via the platform, not the board)
1. **ServiceNow Partner Finder → partner career pages.** Scrape the ServiceNow
   partner directory (Elite/Diamond/Gold tiers, Canada filter), then discover each
   partner's ATS (Workday/Greenhouse/Lever/Ashby) and query it. Partners hire SN
   staff far more often than end users.
2. **Credly / badging issuer directories.** Search public badge directories for
   people holding CSA/CAD/CIS in Toronto; their employers are proven buyers
   of the platform. Cross-reference employer names to job boards.
3. **ServiceNow "Customer Stories" / case studies.** Every named customer in a
   Canadian case study is an end-user employer with an internal platform team.
   Harvest company names → career page → ATS.

## B. Institutional boards the aggregators under-index
4. **College & university HR boards.** Sheridan, Seneca, Humber, George Brown,
   Centennial, Fanshawe, Conestoga, Mohawk, UofT, TMU, York, McMaster, Waterloo,
   Western, Queen's, Carleton, uOttawa, Concordia, UdeM, UCalgary, UBC, SFU.
   (Sheridan already produced a ServiceNow Admin & Developer role.)
5. **Hospital / health-authority boards.** UHN, SickKids, Sinai, Unity Health,
   Sunnybrook, Trillium, Scarborough Health, Hamilton Health Sciences, Ontario
   Health, Ornge, Cancer Care Ontario, Public Health Ontario.
6. **Municipal & regional government boards.** City of Toronto, Peel, York, Durham,
   Halton, Hamilton, Mississauga, Brampton, Vaughan, Markham, Ottawa, Waterloo
   Region — plus their ATS (usually SuccessFactors / Taleo / Workday).
7. **Crown corporations, agencies & regulators.** OPG, Hydro One, Toronto Hydro,
   Metrolinx, TTC, Metrolinx subsidiaries, OLG, LCBO, WSIB, FSRA, OSC, OEB, IESO,
   Infrastructure Ontario.
8. **School boards (K-12).** TDSB, TCDSB, Peel DSB, York Region DSB, Durham DSB,
   Halton DSB — ITSM/CRM roles sit in their IT departments and never reach Adzuna.

## C. Aggregators and feeds not yet queried
9. **Talent.com / Jooble / Careerjet / Neuvoo CA.** Different crawler sets from
   Adzuna; each surfaces a distinct slice of the same employers.
10. **Eluta.ca RSS + Jobillico + Québec emploi.** French-language Quebec postings
    are systematically absent from the English board sources.
11. **Workday legacy archive + jobs.ca + Jobboom.** Old-domain indexes still
    serve live requisitions for banks and telcos.
12. **Common Crawl index queries.** Query the CC index for `*.myworkdayjobs.com/*`,
    `jobs.*.com/job/*`, `boards.greenhouse.io/*` under Canadian paths to discover
    ATS tenants no human has catalogued yet.

## D. Search-engine dorking at scale
13. **`site:` dorks across ATS domains.** e.g.
    `site:myworkdayjobs.com "ServiceNow" ("Toronto" OR "Ontario")`,
    `site:jobs.lever.co "ServiceNow" Canada`,
    `site:boards.greenhouse.io "ServiceNow"`, capped per-engine.
14. **`inurl:` requisition-shape dorks.** `inurl:/job/ "ServiceNow" Canada`,
    `inurl:requisition "ServiceNow" Toronto`.
15. **Time-restricted query operators.** Where the engine honours them, combine
    `&tbs=qdr:d` (past 24h) / `qdr:w` with platform keywords so only fresh
    requisitions return.

## E. Differential / longitudinal detection
16. **Sitemap diffing.** Snapshot every employer's `sitemap.xml` daily and diff the
    job-URL set. A URL that appears today is a new requisition *by construction* —
    this is the only method that yields a guaranteed "posted today" signal without
    trusting an aggregator's date field.
17. **Requisition-ID gap analysis.** Employers allocate monotonic req IDs. A jump
    in the highest visible ID between snapshots reveals postings whose titles match
    no keyword (the "not obviously labelled" problem).

## F. Community and human-signal routes
18. **Reddit / Discord / Slack community feeds.** r/torontojobs, r/cscareerquestionsCAD,
    r/servicenow, plus Canadian tech Slack/Discord job channels — recruiters post
    there before the boards index them.
19. **Recruiter-agency ATS (Bullhorn).** Agencies running Bullhorn expose public
    job boards with dated postings; enumerate Canadian SN agencies
    (Randstad, Robert Half, TEKsystems, Procom, S.i. Systems, Artech, Altis,
    Insight Global, US Tech, ICONMA, Modis, Eagle, Brainhunter) and query them.
20. **ServiceNow specific communities/forums.** Search for job postings in official
    ServiceNow community forums or developer groups.

---
Status: defined. Execution follows Round 1 completion.
