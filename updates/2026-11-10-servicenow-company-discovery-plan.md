# Plan: stop discovering ServiceNow employers one at a time

Date: 2026-11-10. Status: proposed, nothing built yet.
Input: repo measurements below + a multi-model consult (Groq/Qwen-3.8, Gemini-3.5-Flash,
Cloudflare/Llama-3.3-70B; the rest of the panel failed, see §8).

## 1. The problem, stated in numbers

Every round so far found employers by accident of a search query. Meanwhile the
board already knows 336 company names that posted a ServiceNow-titled role:

| Slice of `jobs.json` (1,933 records) | Rows | Distinct company strings |
|---|---|---|
| "servicenow" in the **title** | 721 | 336 |
| "servicenow" only in body text | 105 | 46 |

Those 336 are a latent employer registry we never mined: nobody has checked how
many of them are already in the 455-board registry, and nobody has used the
other 46 (Hays, TMX Group, Scotiabank, Salvation Army, Mastercard, CIBC,
Enbridge, RBC, EDC, Compugen, Zurich, Equitable, Genesys, KPMG, CGI, NTT DATA …)
as leads. Names are un-normalised and include the vendor itself and staffing
agencies, so the useful number is lower — but the channel is free and already
paid for.

## 2. Channels, ranked by (yield × Canadian relevance) / effort

**C1 — Mine our own corpus, then resolve each name to a board.** *Highest
priority, zero network cost.* Read `jobs.json` + `inbox/*.md`, take every row
whose title or body matches the ServiceNow vocabulary (ServiceNow, ITSM, ITOM,
CMDB/Discovery, HRSD, CSM, IRM/GRC, SPM, FSM, HAM/SAM, CSA/CAD), emit distinct
company names, subtract the 455 known tenants, and run `ats_discover.py` on the
remainder. Cannot tell you: whether the employer still uses ServiceNow (the
posting is evidence of adoption at posting time, which is exactly the evidence
grade we want), and it inherits the corpus's own coverage bias.

**C2 — Public procurement.** *Best date-free-but-authoritative evidence, strong
Canadian weight.*
- CanadaBuys / open.canada.ca proactive-disclosure contract datasets: searchable
  for ServiceNow licence and implementation awards → federal departments and
  agencies (CRA, SSC, DND, IRCC …), all of which run their own ATS or use GC Jobs.
- Ontario Tenders Portal / MERX: provincial ministries, hospitals, universities.
- USASpending.gov API (`/api/v2/search/spending_by_award/`, free, no key) for
  AFRL-type US buyers if we ever want them.
Cannot tell you: private-sector adoption, and awards are lumpy (a 2019 award may
be a lapsed deployment).

**C3 — Vendor and partner customer proof.** Public, curated, and names real
customers rather than partners.
- `servicenow.com/customers.html` and the individual customer-story pages.
  **Measured today: curl times out (0 bytes) — needs the headless-Chrome path**,
  so budget for that rather than a plain fetch.
- Knowledge conference session catalog (customer speakers are named), and the
  Innovation-of-the-Year / Customer Award winners.
Cannot tell you: recency (stories age badly) and it is a marketing selection, not
a census.

**C4 — Partner ecosystem, split into two buckets.** The user asked specifically
about known partners; the useful answer is that a partner is two different things
and conflating them wastes the round.
- *Bucket P1 — partners as employers.* Consultancies hire ServiceNow people
  constantly and are legitimate board targets: CGI, DXC, Kyndryl, IBM, Deloitte,
  Accenture, EY, KPMG, PwC, TCS, Infosys, Wipro, Capgemini, HCL, Atos, Unisys,
  NTT DATA, Stefanini, Fujitsu, plus ServiceNow boutiques (NewRocket, Crossfuze,
  GlideFast, Thirdera/Cognizant, Acorio/NTT, ServiceIO, Systematix, Procom,
  LeverageTek, PrecisionERP, Alldus, Hanalytica, Levio, BDO).
- *Bucket P2 — partners as customer evidence.* Only worth it when the partner's
  case study or press release **names the client**. That named client is a
  verified customer and a fresh board. Directory tiers themselves
  (`servicenow.com/partners/finder.html`) rank partner commitment, not customer
  adoption — a Registered partner may have one demo instance.
Proxy verdict: P1 => add as employers; P2 => add the *named client*, never the
partner, as a ServiceNow customer.

**C5 — Technical fingerprint on a candidate domain.** Cheapest way to test a
company we suspect but cannot prove.
- **Works:** DNS CNAME on the likely hostnames (`itsm.`, `service.`, `snow.`,
  `sn.`, `help.`, `support.`) pointing at `*.service-now.com`; and an HTTP probe
  for ServiceNow's own surface — `glide_*` / `JSESSIONID` cookies on `/login.do`,
  `X-Is-Logged-In` / `X-Transaction-ID` / `Glide-*` headers, `/navpage.do`.
- **Dead, measured today:** certificate-transparency enumeration. `crt.sh` for
  `%.service-now.com` returned 101 records and *every one* is the wildcard
  `*.service-now.com` — ServiceNow serves instances under a wildcard cert, so
  instance hostnames never enter CT logs. Do not build this.
- False-positive prone: shared/partner-hosted instances, SSO gateways that strip
  headers, and vanity domains that proxy but are not the employer's own instance.
Cannot tell you: which module they bought, or whether the instance is production.

**C6 — Search-engine dorking per ATS tenant.** `site:myworkdayjobs.com
"servicenow"`, `site:jobs.smartrecruiters.com servicenow`, and the same per ATS
domain, yields employer tenants directly — the highest-yield idea the Gemini peer
raised. Needs a search API key (Serper/Bing); our free tiers are exhausted, so
this is a "when credit exists" channel, and results still have to be resolved to
the tenant's own board before any row is published.

**C7 — Aggregator company facets.** Adzuna returns `company.display_name` for a
`what=servicenow` query, which is a ready-made company list. **Measured today:
the Adzuna credentials the scanners reference (`ADZUNA_API_KEY` / `APP_ID` /
`APP_KEY`) are not present in the key store, so this channel is currently
unavailable** — fix the key before planning around it.

## 3. Verification ladder and admission rules

| Grade | Evidence | How it is earned | Admitted to registry? |
|---|---|---|---|
| **A** | Live ServiceNow-titled requisition on the employer's own ATS | fetch the board, confirm the title, keep the posting date | yes, automatic |
| **B** | ServiceNow named in the body of a live requisition on that board | same fetch, body match | yes, automatic |
| **C** | Vendor/partner case study or a procurement award naming the org | fetch the story/award page | yes, after one A/B attempt |
| **D** | Technical fingerprint only (CNAME/headers) | DNS + HTTP probe | no — use it to decide where to look for A/B |

Two rules keep this compatible with the board's hard constraint:
1. **Discovery channels never produce rows.** They produce *employers*. A row
   still requires a board fetch that yields a title, a company and a real date.
2. **Agency rows are not customer evidence.** Hays/Procom/LanceSoft post a
   client's role, so the agency earns a board (they hire SN staff) but never a
   "this company runs ServiceNow" claim.

## 4. Build order

**Phase 1 (free, this week) — C1.** `tools/snow_company_register.py`:
read `jobs.json` + `inbox/*.md` → match the SN vocabulary → normalise company
names (strip legal suffixes, collapse variants) → drop the vendor and a
staffing-agency blocklist → diff against the registry → emit
`reports/snow_candidates_YYYY-MM-DD.json` + a shell list for `ats_discover.py`.
Acceptance: every candidate carries the row id that produced it (so the claim is
auditable), and the diff against the 455 boards is non-empty.

**Phase 2 (weekly, scheduled) — C2 + C3.** `tools/snow_procurement_scan.py`
(CanadaBuys/open.canada.ca datasets, Ontario Tenders, USASpending) and a
Chrome-backed customer-story scraper. Both write candidates only.
Acceptance: each candidate has a source URL and the extracted sentence, and the
run reports zero-yield loudly instead of silently.

**Phase 3 (nightly enrichment) — C5.** CNAME/header probe over the domains of
candidates still at grade C, to decide whether an A/B hunt is worth it.
Acceptance: probe results are stored with the raw record (CNAME target, header
set) so a false positive can be diagnosed later.

**Do not build:** CL consistency nothing (dead), Crunchbase/PitchBook (paid API,
technology fields unreliable), G2/Capterra review scraping (ToS + consultant
noise), LinkedIn company "software" sections (guest search is Cloudflare-blocked
for us).

**The failure mode to design against** (independently flagged by the Cloudflare
and Groq peers): a single-source pipeline that trusts one signal. A company
appears once, at grade D, gets added, and every subsequent round spends a fetch
on a board with no ServiceNow roles. Hence the ladder: D never admits on its own,
and every candidate keeps the evidence that produced it.

## 5. What this buys, concretely

From the current corpus alone, 336 company strings carry a ServiceNow-titled
role and 46 more mention the platform in the body. Even after removing the vendor,
agencies and name variants, that is the largest single batch of candidate
employers available to this project today, and it costs one local script run.

## 6. Peer input, and what I took from each

- **Groq / Qwen-3.8-27B** — correct on the point that matters: partners are
  vendors, not customers; only a case study naming the client converts a partner
  into evidence. Its G2/LinkedIn/Crunchbase suggestions I reject (ToS, blocking,
  paid API).
- **Gemini-3.5-Flash** (partial response, truncated at ~120 bytes by the provider)
  — its one complete idea, dorking ATS domains per board provider, is the best
  new channel in the set and became C6.
- **Cloudflare / Llama-3.3-70B** — right that Partner Finder + fingerprint is the
  cheapest first automation; some of its specific endpoints are noise (CRTC,
  Procurify) and the claim that developer.servicenow.com instance-configuration
  examples carry company names is false, so I did not use them.
- Consensus (all three): verify across at least two signals, and expect adoption
  evidence to be undated — which is why the ladder admits only boards, never rows.

## 7. Immediate next actions

1. Phase-1 script + first candidate report (no network).
2. Restore Adzuna credentials, or drop C7 from the plan.
3. Attempt `servicenow.com/customers.html` through headless Chrome once, to see
   whether C3 is viable at all before writing a scraper for it.

## 8. Consult run log (honest record)

Attempted 11 provider/model pairs; 3 answered. Failures: fan-out presets in
`tools/consult_multi.py` point at retired model IDs (5 × HTTP 404), Cerebras
returned HTTP 402 payment-required, GitHub Models host unresolvable, NVIDIA timed
out, HuggingFace returned an empty body. Working: `groq/qwen3.8-27b`,
`gemini_api/gemini-3.5-flash` (truncated), `cloudflare/@cf/meta/llama-3.3-70b-instruct-fp8-fast`.
Fixing the presets is a one-line-per-entry change and is a prerequisite for the
next consult round.
