# Search + AI pass over the live board — 2026-11-04

Two questions: can our search APIs and the free model pool find postings the scanners miss, and
what do the 1,571 postings already on the board say about where the gaps are.

## 1. Search APIs

`scripts/web_search_scan.py` with all 12 built-in queries:

| Provider | State | Result |
|---|---|---|
| Tavily | HTTP 432 — plan quota exhausted | blocked |
| Exa | HTTP 402 — credits exhausted | blocked |
| Firecrawl | working, then HTTP 429 at req/min 11 | 80 results over 8 queries → **1 undated row, 0 dated** |

Firecrawl is the only live key, and its output is mostly aggregator pages — the same shape the new
`is_listing_url()` guard rejects. With `--max-fetch 40` only one page produced a row and it had no
date, so the search-API channel added no postings this round. Exa/Tavily need a top-up before they
can contribute again.

## 2. AI pool

`python3 tools/ai_panel.py ping` → **15/21 peers answered** (vllm, ollama, litellm, kilocode,
pollinations, llm7, groq, huggingface, cohere, mistral, publicai, cloudflare, zai, openrouter, nous).
Failing: gemini (429), deepinfra (40x), sambanova (401), aimlapi (403), ovh (403), siliconflow (no key).

`ai_panel.py queries --count 12` produced 12 keyword variants not on the existing lists:
`servicenow itom, cmdb specialist, itam consultant, servicenow gsd, salesforce pardot, salesforce wave,
servicenow sysdev, salesforce apex, servicenow release, salesforce ahc, servicenow table, salesforce flow`
(saved to `raw/ai_queries_60d.json`). These are worth feeding to the Adzuna pass — the LinkedIn guest
path is the natural home but it was rate-limited (HTTP 999) straight after the 60-day sweep and only
recovered after a cooldown.

## 3. What the board itself shows (`jobs.json`, 1,571 rows)

- **Everything is dated** (1,571/1,571), median age **4 days**, 1,193 ≤7 days, 1,548 ≤30 days.
- Family tags: salesforce 627, servicenow 548, other 257, devops 64, consulting 53, data 42.
- Sources: readme harvest 678, adzuna 370, linkedin 218, workday 27, jobs.ca 22, greenhouse 19,
  smartrecruiters 15 — the ATS routes contribute little volume against Adzuna/LinkedIn.
- Employer concentration: Epsilon Solutions 39, Deloitte 31, ServiceNow 29, CGI 29, KPMG 25,
  Cognizant 24, Salesforce 22, NeuraFlash 20, TD 19, TCS 18 — i.e. staffing/consultancy firms, not
  end employers.
- **133 duplicate company+title clusters covering 347 rows** (22% of the board) — staffing firms
  repost the same requisition repeatedly.
- Title mix: architect 183, cloud 159, engineer 151, consultant 144, business analyst 127,
  administrator 88, specialist 64.
- Data-quality weak spots: **salary on 66/1,571 (4%)**, `workArrangement` unknown on 1,180/1,571 (75%).

## 4. Cross-model read

The same aggregates were fanned to six peers (huggingface, cohere, mistral, publicai, cloudflare,
zai). Consensus on the two questions:

- **Net-new channels:** Indeed, Glassdoor/Google Jobs, and government or university portals
  (Ontario Public Service, UofT/TMU) — the last is notable because the board is 78% consultancy
  postings and has almost no public-sector employers.
- **Cheapest fixes:** dedupe the 133 company+title clusters, then infer `workArrangement` and salary
  from the excerpt instead of leaving 75%/96% empty.

## Recommended next moves

1. Re-key Exa or Tavily before relying on `web_search_scan.py`; Firecrawl alone is thin and rate-capped.
2. Feed the 12 AI keyword variants into `gap_scan.mjs`'s `what` list (Adzuna gives real dates) once
   LinkedIn's guest endpoint has cooled down.
3. Add Ontario Public Service / city-of-Toronto career boards — the only channel family the models
   agreed the board is structurally missing.
4. Dedupe the 133 clusters and backfill `workArrangement`/salary from `excerpt`; that touches 22% and
   75% of rows respectively and needs no new source.
