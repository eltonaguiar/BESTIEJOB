# Tabbed site, resume-fit scoring, full branch merge (2026-11-02)

## Cross-reference of every branch
`git ls-remote` showed 34 remote branches. `tools/migrate_peer_branches.py` converted
28 of them (the rest had no job rows) into inbox submissions — **3,661 rows** total —
then `tools/jobs_merge_inbox.py` deduped everything against README + archives.

The working README was mid-conflict (6 `<<<<<<<` markers, 311 rows). It was saved to
`/tmp/README.conflict_saved.md`, reset to `origin/main`, then rebuilt from origin +
all 28 branch submissions + every existing inbox file. 84 rows existed only in the
conflicted copy — none of them on any branch — so they were written as
`inbox/rescue-merge--2026-11-02--v1.md` and merged in. Nothing was lost.

Result: **759 unique postings** (215 ServiceNow / 230 Salesforce / 314 Other),
0 conflict markers, 3 tables, 0 rows without a URL.

## Links (the thing that made the page useless)
A link audit confirmed 759/759 rows carry a valid `http(s)` URL, but each card only
linked its title. Every card now has an explicit **"Open posting ↗"** link plus the
title link, both `target=_blank rel="noopener noreferrer"`. The browser test asserts
`openLinks === cards` per tab: 215, 230, 314, 440 — 1:1.

## Tabs
`ServiceNow` · `Salesforce` · `Other` · `★ Best match`, each with its own date window
and shared search + source filter. `Other` sorts by resume fit, not date, and
`Best match` collects score ≥ 45 across all families (440 rows).

## Resume-fit scoring
Weighted keyword model over title + location + note: ServiceNow/Salesforce heaviest,
then ITSM/ITAM/CMDB/ITOM, Flow Designer, Glide scripting, Integration Hub, GRC,
Analytics, plus questionnaire-derived terms (SAM/HAM, import sets / transform maps /
IRE, AIOps/Splunk, SPM/PPM, HRSD, controls/ACL, IT operations, consulting/BA).
Title evidence counts double; Toronto +12, Canada/remote +8, Quebec +4; weak titles
(sales rep, retail, teller) are multiplied by 0.35. Score and reasons ship in
`jobs-data.json` and render as a `fit N` chip with reasons on the card.

## Search that survives how people actually search
Accent folding (`Montréal` → `montreal`), punctuation splitting, and synonyms:
snow/sn → servicenow, sf/sfdc → salesforce, admin → administrator, dev → developer,
sr/jr, ba → analyst, gta/yyz → toronto, mtl → montreal. Every token must match (AND
across tokens, OR across synonyms). Verified: "snow dev" 83, "sf admin" 28,
"montreal" 27, "cmdb" 5, "gta servicenow" 106, "SERVICENOW ARCHITECT" 40.

## Verification
- Playwright (headless Chromium, local file): 4 tabs, per-tab counts, 1:1 card→link
  coverage, synonym searches, no JS errors; test exits 0.
- Junk audit: 14 flags, all real postings whose URL merely contains `/jobsearch` or
  `/land/ad/` (Workopolis, Adzuna redirect) — not junk rows.
