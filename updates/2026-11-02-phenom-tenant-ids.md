# Phenom tenant IDs for RBC / Bell / BMO (2026-11-02)

## The identifiers

Phenom bakes the tenant id into every CDN asset path:
`cdn.phenompeople.com/CareerConnectResources/<scope>/<TENANT>/...`

| Employer | Site | Tenant ID |
|---|---|---|
| RBC | jobs.rbc.com | **RBCAA0088** |
| Bell | jobs.bell.ca | **BECACA** |
| BMO | jobs.bmo.com | **BOMOGLOBAL** |

## What works, and what does not

| Route | Result |
|---|---|
| `GET /api/apply/v2/jobs?domain=<tid>&keywords=ServiceNow` | `200` + `{"status":"failure","errorMsg":"Tenant not identified"}` — for `RBCAA0088`, `BECACA`, `BOMOGLOBAL`, and for `rbc`, `rbc.com`, `jobs.rbc.com` |
| `GET /api/jobs?keywords=ServiceNow&domain=<tid>` | HTTP 500 (RBC, Bell), 404 (BMO) |
| `GET /en/search-results?keywords=ServiceNow` | `200` but byte-identical to the homepage — client-rendered SPA, no cards, no `JobPosting` JSON-LD |
| **`GET /sitemap.xml`** | **Works** — lists every live requisition URL (RBC is a sitemap index of `ca/en/sitemap1.xml` + `sitemap2.xml`) |
| **Requisition page itself** | **Works** — carries `JobPosting` JSON-LD with an exact `datePosted`, title and `addressLocality` |

So the tenant id alone does not unlock the JSON API without a session; the usable
programmatic route is **sitemap → keyword filter on the requisition slug → detail page JSON-LD**.

## Verified yield (this run)

- RBC: 734 job URLs (via the 2 child sitemaps), 1 ServiceNow/Salesforce slug
- Bell: 60 job URLs, 2 keyword hits
- BMO: 430 job URLs, 1 keyword hit

Detail-page dates confirmed: Bell *ServiceNow System Administrator* `2026-10-25` (already listed),
Bell *ServiceNow Senior Technical Advisor* `2026-10-16` (already listed), BMO *Manager, Banking
Salesforce Innovation & Enablement* `2026-10-30` (new), RBC *Salesforce Product Administrator*
`2026-10-23` (Minneapolis — dropped by the Canada filter).

New row submitted via `inbox/employer-sitemap--2026-11-02--v1.md`.

## Reuse

`scripts/employer_sitemap_scan.py` walks the three sitemaps, filters slugs by
ServiceNow/Salesforce/ITSM keywords, resolves exact dates from JSON-LD, drops
non-Canadian rows and anything already in README / archives / inbox, then writes a
normal inbox submission. `--all-locations` keeps US rows; `--apply` merges and rebuilds.
