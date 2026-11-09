# Round 2 — 20 Brand-New Search Styles (not used in Round 1)

Round 1 reused the existing scanners. Round 2 deliberately changes the *method*:
instead of querying boards for keywords, it finds postings by adjacency,
registry, geography and infrastructure.

## A. Vendor-ecosystem routes (find the employer via the platform, not the board)
1. **ServiceNow Partner Finder → partner career pages.** Scrape the ServiceNow
   partner directory (Elite/Diamond/Gold tiers, Canada filter), then discover each
   partner's ATS (Workday/Greenhouse/Lever/Ashby) and query it. Partners hire SN
   staff far more often than end users.
2. **Salesforce AppExchange consulting partners → careers.** Same inversion for
   Salesforce: filter AppExchange consulting partners by Canada, harvest their
   career domains, fingerprint their ATS.
3. **Credly / badging issuer directories.** Search public badge directories for
   people holding CSA/CAD/CIS or Salesforce PD I/II in Toronto; their employers
   are proven buyers of the platform. Cross-reference employer names to job boards.
4. **ServiceNow "Customer Stories" / Salesforce "Customer Success" case studies.**
   Every named customer in a Canadian case study is an end-user employer with an
   internal platform team. Harvest company names → career page → ATS.

## B. Institutional boards the aggregators under-index
5. **College & university HR boards.** Sheridan, Seneca, Humber, George Brown,
   Centennial, Fanshawe, Conestoga, Mohawk, UofT, TMU, York, McMaster, Waterloo,
   Western, Queen's, Carleton, uOttawa, Concordia, UdeM, UCalgary, UBC, SFU.
   (Sheridan already produced a ServiceNow Admin & Developer role.)
6. **Hospital / health-authority boards.** UHN, SickKids, Sinai, Unity Health,
   Sunnybrook, Trillium, Scarborough Health, Hamilton Health Sciences, Ontario
   Health, Ornge, Cancer Care Ontario, Public Health Ontario.
7. **Municipal & regional government boards.** City of Toronto, Peel, York, Durham,
   Halton, Hamilton, Mississauga, Brampton, Vaughan, Markham, Ottawa, Waterloo
   Region — plus their ATS (usually SuccessFactors / Taleo / Workday).
8. **Crown corporations, agencies & regulators.** OPG, Hydro One, Toronto Hydro,
   Metrolinx, TTC, Metrolinx subsidiaries, OLG, LCBO, WSIB, FSRA, OSC, OEB, IESO,
   Ontario Treasury Board, Infrastructure Ontario.
9. **School boards (K-12).** TDSB, TCDSB, Peel DSB, York Region DSB, Durham DSB,
   Halton DSB — ITSM/CRM roles sit in their IT departments and never reach Adzuna.

## C. Aggregators and feeds not yet queried
10. **Talent.com / Jooble / Careerjet / Neuvoo CA.** Different crawler sets from
    Adzuna; each surfaces a distinct slice of the same employers.
11. **Eluta.ca RSS + Jobillico + Québec emploi.** French-language Quebec postings
    are systematically absent from the English board sources.
12. **Workopolis legacy archive + jobs.ca + Jobboom.** Old-domain indexes still
    serve live requisitions for banks and telcos.
13. **Common Crawl index queries.** Query the CC index for `*.myworkdayjobs.com/*`,
    `jobs.*.com/job/*`, `boards.greenhouse.io/*` under Canadian paths to discover
    ATS tenants no human has catalogued yet.

## D. Search-engine dorking at scale
14. **`site:` dorks across ATS domains.** e.g.
    `site:myworkdayjobs.com "ServiceNow" ("Toronto" OR "Ontario")`,
    `site:jobs.lever.co "Salesforce" Canada`,
    `site:boards.greenhouse.io "ServiceNow"`, capped per-engine.
15. **`inurl:` requisition-shape dorks.** `inurl:/job/ "ServiceNow" Canada`,
    `inurl:requisition "Salesforce" Toronto`.
16. **Time-restricted query operators.** Where the engine honours them, combine
    `&tbs=qdr:d` (past 24h) / `qdr:w` with platform keywords so only fresh
    requisitions return.

## E. Differential / longitudinal detection
17. **Sitemap diffing.** Snapshot every employer's `sitemap.xml` daily and diff the
    job-URL set. A URL that appears today is a new requisition *by construction* —
    this is the only method that yields a guaranteed "posted today" signal without
    trusting an aggregator's date field.
18. **Requisition-ID gap analysis.** Employers allocate monotonic req IDs. A jump
    in the highest visible ID between snapshots reveals postings whose titles match
    no keyword (the "not obviously labelled" problem).

## F. Community and human-signal routes
19. **Reddit / Discord / Slack community feeds.** r/torontojobs, r/cscareerquestionsCAD,
    r/servicenow, r/salesforce, plus Canadian tech Slack/Discord job channels —
    recruiters post there before the boards index them.
20. **Recruiter-agency ATS (Bullhorn).** Agencies running Bullhorn expose public
    job boards with dated postings; enumerate Canadian SN/SF agencies
    (Randstad, Robert Half, TEKsystems, Procom, S.i. Systems, Artech, Altis,
    Insight Global, US Tech, ICONMA, Modis, Eagle, Brainhunter) and query them.

---
Status: defined. Execution follows Round 1 completion.
