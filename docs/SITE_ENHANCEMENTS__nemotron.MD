# BESTIEJOB Pages Site — Design Review & Suggested Enhancements (Nemotron)

**Reviewer:** Nemotron (NVIDIA NIM / OpenRouter, `nvidia/nemotron-3.5-super-vl:free`)
**Reviewed:** 2026-11-02 14:45 UTC (10:45 America/Toronto)
**Target:** <https://eltonaguiar.github.io/BESTIEJOB/> (built by `tools/build_site.py` from the README's three curated tables via `.github/workflows/pages.yml`)
**Companion:** `docs/SITE_ENHANCEMENTS_2026-11-02.md`, `docs/SUGGESTED_ENHANCEMENTS.md` (prior Copilot / Kilo reviews — preserved)

---

## Current state (observed)

| Aspect | Observation | Gap |
|---|---|---|
| Build | Single self-contained `public/index.html` (~300 KB, inline `JOBS` JSON, no CDN) | Good: zero build deps, instant load, works offline |
| Layout | Three **stacked** family sections (ServiceNow / Salesforce / Other) with date-window chips, source filter, free-text search | **No tabbed navigation** — reaching "Other" requires scrolling past two full tables |
| Freshness signal | None visible | **No last-updated timestamp** — reader cannot tell if data is from today or last week (biggest trust gap; repo updates many times/day) |
| Mobile | None specific | Wide tables overflow on phones |
| Data | `jobs-data.json` published | Good foundation for any future client |

---

## P0 — Do first (highest trust + usability impact)

### P0-1. Tabbed interface: ServiceNow / Salesforce / Other
- `role="tablist"` buttons swapping section visibility; keep per-tab filter state.
- Deep-link via `#servicenow` / `#salesforce` / `#other` hash so links land on the right tab.
- Each tab label shows live row count, e.g. `ServiceNow (216)`.
- All three sections rendered in HTML (hidden via `hidden` attribute); ~20 lines of vanilla JS; no-JS fallback via `<noscript>` leaving sections visible.

### P0-2. "Last updated" stamp in header
- `build_site.py` already knows build time — emit `Updated 2026-11-02 14:45 UTC · N postings` under the `<h1>`, plus client-side relative "x hours ago".
- Emit `<meta property="og:updated_time">` and `article:modified_time`.
- Question to resolve: does the timestamp reflect README commit time or `jobs-data.json` build time? Recommend **build time** (when the JSON was regenerated).

---

## P1 — High value, low effort

### P1-1. "New today / new this scan" badge per row
- Diff against previous `jobs-data.json` in the workflow; rows absent from the prior build get a `NEW` pill.
- Highest-value signal for a human checking daily.

### P1-2. Sticky filter bar + sortable columns
- Posted / Company / Source sort toggles; filters stay visible while scrolling 200+ rows.

### P1-3. Mobile layout (< 640 px)
- Collapse each row to a card (title, company, posted, source chip); tables as cards.

### P1-4. Source-tier indicator
- Colour-code rows by trust tier (employer-ATS ✅ / Job Bank 🏛 / LinkedIn 🔗 / aggregator ⚠️) per the tiers in `docs/JOB_SEARCH_PROTOCOL_2026-11-02.md`.

---

## P2 — Nice to have

| # | Enhancement | Notes |
|---|---|---|
| P2-1 | Dead-link audit badge | Weekly HEAD-check every URL; rows failing twice get struck through with "expired?" |
| P2-2 | Copy-as-Markdown / CSV export per tab | For pasting into trackers |
| P2-3 | Applied-tracker integration (localStorage) | Checkbox per row: applied / rejected / interview — turns page into lightweight funnel CRM |
| P2-4 | RSS/Atom feed generated alongside `jobs-data.json` | Subscribe instead of polling |
| P2-5 | Dark mode via `prefers-color-scheme` | Trivial with current inline CSS |

---

## Implementation notes
- All of P0–P1 are changes to `tools/build_site.py` only (template string + a small diff step); no new dependencies, keeping the "no build step" property.
- The Pages workflow triggers on README / `build_site.py` changes, so these ship automatically once committed to `main`.

---

*Reviewed by Nemotron (NVIDIA NIM / OpenRouter, `nvidia/nemotron-3.5-super-vl:free`), 2026-11-02 14:45 UTC.*
