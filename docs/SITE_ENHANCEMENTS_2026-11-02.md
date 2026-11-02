# BESTIEJOB Pages Site — Design Review & Enhancement Backlog

**Reviewed:** 2026-11-02T15:09Z · **Agent:** GitHub Copilot (Copilot SDK, VS Code; Claude Opus family) · **Target:** <https://eltonaguiar.github.io/BESTIEJOB/> (built by `tools/build_site.py` from the README's three curated tables via `.github/workflows/pages.yml`)

## Current state (observed)

- Single self-contained `public/index.html` (~300 KB, inline `JOBS` JSON, no CDN) — good: zero build deps, instant load, works offline.
- Three **stacked** family sections (ServiceNow / Salesforce / Other) with per-family date-window chips, source filter and free-text search.
- **No tabbed navigation** — reaching "Other" requires scrolling past two full tables.
- **No visible last-updated timestamp** — a reader cannot tell if data is from today or last week (the biggest trust gap, since the repo updates many times a day).
- No mobile-specific layout; wide tables overflow on phones.
- `jobs-data.json` is published — good foundation for any future client.

## Suggested enhancements (priority order)

| # | Priority | Enhancement | Notes |
|---|---|---|---|
| 1 | P0 | **Tabbed interface** for ServiceNow / Salesforce / Other | `role="tablist"` buttons swapping section visibility; keep per-tab filter state; deep-link via `#servicenow` hash so links land on the right tab. Each tab label shows live row count, e.g. `ServiceNow (216)`. |
| 2 | P0 | **"Last updated" stamp** in the header | `build_site.py` already knows build time — emit `Updated 2026-11-02 15:09 UTC · N postings` under the `<h1>`, plus a relative "x hours ago" rendered client-side. Also emit `<meta property="og:updated_time">`. |
| 3 | P1 | **"New today / new this scan" badge** per row | Diff against previous `jobs-data.json` in the workflow; rows absent from the prior build get a `NEW` pill. Highest-value signal for a daily-checking human. |
| 4 | P1 | **Sticky filter bar + sortable columns** | Posted/Company/Source sort toggles; filters stay visible while scrolling 200+ rows. |
| 5 | P1 | **Mobile layout** | Below 640 px collapse each row to a card (title, company, posted, source chip); tables as cards. |
| 6 | P2 | **Source-tier indicator** | Colour-code rows by trust tier (employer-ATS ✅ / Job Bank 🏛 / LinkedIn 🔗 / aggregator ⚠️) per the tiers in `docs/JOB_SEARCH_PROTOCOL_2026-11-02.md`. |
| 7 | P2 | **Dead-link audit badge** | Weekly workflow HEAD-checks every URL; rows failing twice get struck through with "expired?" rather than silently rotting. |
| 8 | P2 | **Copy-as-Markdown / CSV export** button per tab | For pasting into trackers. |
| 9 | P3 | **Applied-tracker integration** | LocalStorage checkbox per row ("applied", "rejected", "interview") — turns the page into a lightweight funnel CRM, addressing the biggest gap flagged in the protocol review. |
| 10 | P3 | **RSS/Atom feed** generated alongside `jobs-data.json` | Lets a human subscribe instead of polling. |
| 11 | P3 | **Dark mode** via `prefers-color-scheme` | Trivial with current inline CSS. |

## Implementation notes

- All of #1–#3 are changes to `tools/build_site.py` only (template string + a small diff step); no new dependencies needed, keeping the "no build step" property.
- Tabs: render all three sections as today but hidden with `hidden` attribute; 20 lines of vanilla JS; preserves no-JS fallback by leaving sections visible inside `<noscript>` styling.
- The Pages workflow already triggers on README/`build_site.py` changes, so these ship automatically once committed.
