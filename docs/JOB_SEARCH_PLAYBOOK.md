# Job-search playbook & site review

**Prepared by:** Buffy (Freebuff agent, DeepSeek V4.1 Flash)
**Timestamp:** 2026-11-02 15:10 UTC (10:10 America/Toronto)
**Scope:** ServiceNow / Salesforce / adjacent IT-platform roles, Toronto-first
**Data as of:** 2026-11-02 · 833 rows in `README.md` · 830 live cards on the site

---

## 1. Design review of https://eltonaguiar.github.io/BESTIEJOB/

### What is already right
- Tabbed interface: **ServiceNow / Salesforce / Other / ★ Best match**, each tab carrying its own date window (Today, This week, This month, All).
- A **resume-fit score (0–100)** with the reasons printed on every card, so "Other" is no longer a dumping ground.
- Every card has an explicit **Open posting ↗** link plus a clickable title.
- Source filter derived from the posting host, so aggregator mirrors can be hidden.
- Search understands synonyms and accents: `snow dev`, `sf admin`, `montreal`, `gta`, `cmdb` all resolve.
- A build timestamp ("Last updated … UTC") in the header.

### Suggested enhancements (ranked)

| # | Enhancement | Why | Effort |
|---|---|---|---|
| 1 | **Deadline field + "closing soon" tab** | Postings carry end dates (BMO 11/06, TD 11/09, Cognizant 11/15) but the site ignores them; sorting by deadline is the single most useful view for a job-seeker | M |
| 2 | **Applied / archived state** (`APPLIED.md` + a "Hide applied" toggle) | Prevents re-reading roles already applied to; a peer agent already matched ~76 Gmail confirmations | M |
| 3 | **Freshness badge & staleness rule** | Rows >14 days old on an aggregator are often dead; dim or filter them | S |
| 4 | **Duplicate clustering (title+company)** | The same req appears as Adzuna + LinkedIn + jobs.ca; the site dedupes URL only, not identity | M |
| 5 | **Remote/hybrid/in-person flag parsed from the note** | A Toronto-based searcher wants remote-Canada roles too; the location bonus currently rewards only Toronto | S |
| 6 | **Company pages / filter by employer** | Banks, consultancies and partners are the three real segments; a filter beats scrolling | M |
| 7 | **Saved searches as URL state** (`?tab=snow&when=week&src=LinkedIn`) | Shareable/reloadable views, no JS state loss | S |
| 8 | **"New since your last visit" marker** (localStorage) | Daily checking is the actual workflow | S |
| 9 | **Posting-health check** (HTTP status + Apply-button probe, batch nightly) | Kills phantom rows automatically rather than by hand | L |
| 10 | **Salary extraction** | Many postings state a band; it is currently buried in the note | M |
| 11 | **ICS/calendar export of deadlines** | Turns the list into a schedule | S |
| 12 | **Per-card "why this fits" expander** (module-by-module) | Already scored; making it explicit helps tailor the resume | S |
| 13 | **Cert-gate flag** (CSA/CAD/PD1/Admin required vs preferred) | The biggest screening filter in this market | M |
| 14 | **RSS/JSON feed of new rows** | Lets a scheduler or a human's reader subscribe | S |
| 15 | **Mobile card layout tightening** | Long titles wrap awkwardly at <400 px | S |

---

## 2. The protocol a human can actually follow

### Daily (15 minutes)
1. Open the site, **Today** tab per family. If Today is empty (common — Nov 1 was a Sunday), drop to **This week**.
2. Anything scoring **≥ 70** in *Best match*: open the posting, confirm **Apply is enabled** and the posting date. Do not apply from an aggregator mirror alone.
3. Record the application (company, req #, date, deadline) in `APPLIED.md`.
4. Sort the rest by deadline, not by score.

### Weekly (45 minutes)
5. Check the employer boards that actually answer: TD, CIBC, BMO (Phenom), RBC (Phenom), Bell (Phenom), Metrolinx (Oracle), Walmart Canada, Canadian Tire, Home Depot, Accenture, Desjardins — via `scripts/ats_fingerprint_scan.py`.
6. Check the **agency lane**, which the automated sweep does *not* cover: Randstad, Robert Half, TEKsystems, Procom, S.i. Systems, Artech, Altis, Insight Global, US Tech Solutions, ICONMA. A large share of Toronto contract ServiceNow/Salesforce work is posted only there.
7. Re-check partner firms (GlideFast, NewRocket, Crossfuze, Lane Four, CloudKettle, Coastal Cloud) — thin yield, but the roles are pure-platform.

### Rules that save time
8. **Never trust a relative date** ("2 days ago", "New!") — quarantine it until you see an absolute one on the employer's page.
9. **A posting with no Apply button, or an end date in the past, is dead** regardless of what the aggregator says.
10. **Deduplicate by title + company**, not just URL: `careers.company.com` and `jobs.company.com` are the same req.
11. **If the same role appears at 3+ staffing firms**, the client is probably also hiring direct — search the client's own board first.
12. **Nothing older than 30 days** without a fresh confirmation.

### Verification checklist before spending an hour on an application
- Employer domain, not an aggregator redirect.
- Req/ID visible and searchable on that board.
- Posted date within 30 days; end date in the future.
- Location and work model stated (not "Canada" with no city).
- Certification gate read carefully: *required* vs *asset*.

---

## 3. External review of this protocol

Two models answered; the OpenRouter key in `dbpasses.txt` is dead for every free slug (`404 … unavailable for free`), so it produced nothing.

### Inception Labs · `mercury-2` (the `mercury-3` and `mercury-coder-small` slugs refused: empty response / 403 legacy-account gate)
- Absolute-date-only **discards real listings** where the ATS only exposes "posted X days ago". → *Accepted: added a quarantine bucket (rule 8) rather than dropping the row.*
- A 1–3 day aggregator window **misses batch-uploaded bank reqs**. → *Accepted: the weekly employer-board pass exists precisely for that; the doc now says so explicitly.*
- Fingerprinting is **fragile** — custom front-ends hide the ATS. → *Accepted: the scanner records unsearchable employers so nobody re-tries them daily.*
- `datePosted` in JSON-LD is **sometimes static/stale**. → *Partially accepted: cross-check against the ATS listing date when both exist.*
- Scoring ignores **remote-first** postings. → *Accepted and listed as enhancement #5.*

### DeepSeek · `deepseek-chat`
- **Aggregators are the lowest-signal source** for this profile; ATS + niche boards dominate. → *Partially rejected: Adzuna is the only channel with a usable Canadian index in this environment, and it is what surfaces the staffing-firm reqs. Kept, but demoted in priority.*
- **No agency/vendor lane.** → *Accepted: it is now step 6 of the weekly routine and enhancement #2 in importance.*
- **Fingerprint daily is wasteful; precompute a static map.** → *Accepted: `updates/2026-11-02-employer-ats-inventory.md` is that map.*
- **Missing date handling.** → *Accepted: quarantine rule.*
- **Banks gate contractor reqs behind vendors.** → *Accepted: matches observed reality (BMO/TD reqs surfaced only via aggregators).*

**Net change to the protocol:** a quarantine bucket for undated rows, an explicit agency lane, a static ATS map instead of daily fingerprinting, and duplicate clustering by title+company rather than URL alone.

---

## 4. Channels that are dead ends (do not retry)

| Channel | Status |
|---|---|
| OpenRouter free models | 404 — every free slug retired; paid credit required |
| Brave Search API | 422 `SUBSCRIPTION_TOKEN_INVALID` |
| xAI Grok live search | 410 — retired upstream |
| Indeed (CA) | RSS 404, HTML blocked |
| Jooble | Cloudflare 403 |
| Talent.com | JS-only cards, no `JobPosting` JSON-LD |
| Ontario gojobs | JS-rendered search, no parseable rows |
| Job Bank search endpoint | HTTP 500 |
| SuccessFactors boards (Rogers, Deloitte, City of Toronto) | session-gated, no public search |
| Dayforce HCM board | 561 KB JS shell; cards render only in a browser |

---

## 5. Running the tooling

```bash
python3 scripts/ats_fingerprint_scan.py            # 64 employers -> ATS -> inbox submission
python3 scripts/employer_sitemap_scan.py           # RBC / Bell / BMO via sitemap + JSON-LD
python3 scripts/linkedin_guest_scan.py --days 3    # LinkedIn guest endpoint
python3 tools/migrate_peer_branches.py             # every unmerged branch -> inbox
python3 tools/jobs_merge_inbox.py --dry-run        # preview, then run without --dry-run
python3 tools/build_site.py                        # regenerate public/ for Pages
```

---

*Reviewed 2026-11-02 by Buffy (DeepSeek V4.1 Flash) with second opinions from Inception `mercury-2` and DeepSeek `deepseek-chat`. Sun Life, Canada Life, Scotiabank, Manulife and Dayforce boards remain unsearchable without a browser session — the largest remaining gap.*
