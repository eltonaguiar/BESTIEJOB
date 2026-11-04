# Cross-URL duplicate detection + finishing the rate-limited passes

**Date:** 2026-11-04
**Scripts:** `tools/crossurl.py` (new), `scripts/semantic_dedupe.py`, `scripts/ats_discover.py`, `scripts/ats_board_sweep.py`

## What was broken

### 1. The board listed the same posting twice, under two URLs

The merger dedupes on normalized URL. One requisition reaches the board twice
because it arrives through two channels with two different labels for the same
employer:

```
Take-Two Interactive / "ServiceNow ITOM Lead"   (aggregator URL)
take2games           / "ServiceNow ITOM Lead"   (jobs.ashbyhq.com URL)

Lightspeed Commerce  / "ServiceNow Developer"   (aggregator URL)
lightspeedhq         / "ServiceNow Developer"   (jobs.ashbyhq.com URL)
```

`semantic_dedupe.py` existed to catch this and could not. Its fingerprint pass
compared squashed `company + title + city` strings, so `lightspeedhq` and
`Lightspeed Commerce` produced different keys. Its embedding pass could only
*confirm* pairs whose normalized titles were already identical — the same pairs
the fingerprint pass had just compared — so it could never add a cluster.

Measured on the live board: **166 clusters, 225 redundant copies** out of 1,786
dated rows. The two rows that surfaced the bug during the previous round were
the tip of it, not the whole of it.

### 2. The sweep labelled rows with the ATS handle instead of the employer

`from_greenhouse` used `pretty(token)` as the company name. That is how the
board acquired rows whose company was a handle: token `12Jlkfsk` is **Orion
Global Solutions**, and token `highmetric` is **NewRocket** (the acquisition
kept the token, so the label was a company that no longer exists under that
name). Handle-as-label is the *cause* of the duplicates in §1, not just a
cosmetic wart.

### 3. Tavily's 432 was reported as a transient throttle

Discovery printed `HTTP Error 432` for all 24 queries and stopped. The previous
round recorded this as "rate-limited, retry later". 432 is Tavily's *plan limit
reached*; both keys carried separate quotas and both were exhausted, so waiting
would never have helped. 205 of the discoverable tokens was the symptom of a
provider that no longer worked, not of a quota that would refill.

### 4. Workable was written off as Cloudflare

Every `apply.workable.com` path returned 429 — with browser impersonation and
without it (17-byte body), on the API and on the HTML careers page. That is a
per-IP ban, not a bot check, so no header change could fix it. The route
contributed zero rows.

## What changed

### `tools/crossurl.py` — one shared definition of "same posting"

Four conditions, all required, because a board that collapses two genuine
requisitions is worse than one showing a duplicate:

| Guard | Rule | Why |
| --- | --- | --- |
| company | alias-aware key (`company_key`) + prefix/Jaccard fallback | ATS handles vs real names; `Take-Two` == `take2` via digit words |
| title | token Jaccard ≥ 0.75 after dropping market noise (`remote`, `canada`, `hybrid`…) | The same req is titled with and without those words per channel |
| level | seniority/level token **sets must be equal** | GDIT and Cognizant post Developer / Senior / II / III as separate requisitions |
| location | same city, or one side blank | `Toronto, ON` and `Ottawa, ON` must never collapse |

Seniority words are deliberately *not* stripped as noise: `Developer` and
`Senior Developer` are two jobs.

### `scripts/semantic_dedupe.py` — rewritten around it

- Clusters by `crossurl` instead of squashed strings.
- Pairs whose titles differ in word order or phrasing but score below the token
  threshold can be rescued by embeddings, now behind `--embeddings` (opt-in, and
  only for same-company + same-city pairs). Previously that pass re-tested
  clusters it could not change.
- When two copies survive, keep the freshest, then the **employer's own URL**
  over an aggregator's — the aggregator listing is the one that rots.
- Removed rows still go to a timestamped `README.DEDUPE_*.md` archive.

### `scripts/ats_discover.py` — provider pool

Discovery now rotates `TAVILY_API_KEY` → `TAVILY_API_KEY_ALT` → Exa →
Firecrawl, retiring a credential on 401/402/403/429/432 and continuing with the
next provider instead of ending the pass.

### `scripts/ats_board_sweep.py`

- **Firecrawl transport fallback** for Workable, capped at 2 concurrent scrapes
  with 2s/4s/6s backoff — Firecrawl 429s above that, which is what made the
  first attempt fall back on every board.
- **`greenhouse_employer()`** reads the board endpoint's own `name`, cached, so
  rows carry the real employer. Workable's payload already states `name` and is
  now used instead of the slug.
- **Pre-merge guard** now compares against board rows with `crossurl` rather
  than a company-squash regex, so a posting already on the board under an
  aggregator label is recognised instead of being re-added.

## Verification

| Check | Result |
| --- | --- |
| Matcher unit cases (9: 4 must-match, 5 must-not) | 9/9 pass |
| Dedupe first pass | 166 clusters, 225 copies removed, 1,786 → 1,561 rows |
| Dedupe to fixpoint | 2 more clusters (exposed by the NewRocket relabel) → **0 remaining** |
| Rows removed from the board | 1,788 → 1,560 |
| Placeholder/test rows purged | 1 (`Acme Corp` / `example.com/job/1`) |
| Broken markdown rows repaired | 1 (double-wrapped link on the Walmart Canada row; no parser could read it) |
| Misattributed employer labels fixed | 2 (`Highmetric` → `NewRocket`) |
| Parser coverage | 1,560 dated rows, **0 unparseable** |
| Sort guard | `OK: 7 Posted-column tables are newest-first` |
| Site rebuild | 1,413 → 1,393 jobs, `{servicenow: 313, salesforce: 380, other: 700}` |
| Future-dated / undated | 0 / 0 |
| Discovery pass | 205 → **479** board tokens (Tavily + alt exhausted, Exa delivered 24/24 queries) |
| Sweep re-run | 479 boards, 24,712 raw rows, 775 relevant, 93 Canadian, 29 dated ≤21d, **0 net-new** |

The drop from 1,413 to 1,393 site jobs is the duplicates leaving; the 225 rows
removed from README mostly sat outside the site's recent window, so the visible
count moved by 20.

## Limitations

- **Workable still costs a proxy call per board.** Firecrawl's egress works but
  the direct route is IP-banned; if that ban lifts, the fallback is dead weight.
- **Two providers, not four, did the discovery.** Both Tavily keys are
  plan-exhausted. Exa served all 24 queries; Firecrawl never had to.
- **Some routes still can't date their rows** (Pinpoint, BambooHR, Rippling,
  Jobvite) and are still excluded rather than back-dated.
- **Recruitee/Ashby/Lever/SmartRecruiters feeds expose no employer name**, so
  those rows still carry a prettified token. `crossurl` absorbs the mismatch,
  but the label is only as good as the token.
- The dedupe can still collapse two genuine requisitions posted with identical
  company, title, level and city on the same day. Removed rows are archived in
  `README.DEDUPE_*.md`, so the loss is recoverable.
- The deeper sweep bought **no new rows**. Doubling discoverable boards moved
  Canadian-relevant postings from 89 to 93; every dated one was already listed.
  The reachable ATS universe for this remit is saturated, and further gains need
  sources we don't have (agency mirrors, paid aggregator keys), not more boards.
