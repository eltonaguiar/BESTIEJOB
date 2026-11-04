---
name: bestiejob-hunt
description: Reusable job-hunting toolkit for the BESTIEJOB board — daily scan, 20-round GTA/remote/partner harvest, free-AI keyword harvesting and triage, ATS/Job Bank today-feeds, semantic dedupe, peer-branch rescue, and publish. Use when asked to find ServiceNow/Salesforce/ITSM roles in Toronto/GTA or remote Canada, refresh the board, harvest keywords, or recover unmerged peer finds.
---

# bestiejob-hunt

One board (`README.md` + `public/jobs-data.json`), one review queue (`inbox/`),
one publish path. Every job row must carry a date the source published — a
model, a snippet or a relative "2 days ago" is never allowed to become a date.

## The rule that governs everything

**Aggregator in, own-board verification out.** A posting enters `README.md`
only with (a) an absolute `YYYY-MM-DD` and (b) a URL. Undated finds go to
`inbox/` with an em dash and the merger skips them on purpose.

## Skill 1 — daily refresh

```bash
./scripts/daily_scan.sh              # full: aggregators -> ATS -> web search -> AI -> merge -> build
SCAN_AUTOCOMMIT=0 ./scripts/daily_scan.sh   # same, leave the tree dirty for review
SCAN_PUSH=1 ./scripts/daily_scan.sh         # also push (rarely wanted)
```
Order inside: `daily_job_scan.mjs` → `ai_panel.py queries` → `gap_scan.mjs`
(with AI variants) → `web_search_scan.py` → `today_feeds_scan.py` →
`ai_panel.py triage-inbox` → `jobs_merge_inbox.py` → `semantic_dedupe.py
--apply` → `sync_readme_to_jobs.mjs` → `build_site.py`.

## Skill 2 — 20-round campaign (GTA → remote → ambiguous → partners → agencies)

`/tmp/rounds_harvest.py` pattern, re-creatable in ~20 lines: iterate
`(what, where, company)` across GTA cities (Toronto, Mississauga, Markham,
Etobicoke, Brampton, Vaughan, Scarborough, North York, Richmond Hill), then
`where=Canada` + `remote`, then `company=` for partners (Accenture, Deloitte,
KPMG, CGI, Cognizant, Capgemini, IBM, Infosys, TCS, NeuraFlash, CloudKettle,
Lane Four) and agencies (TEKsystems, Procom, Randstad, Artech, Insight Global).

Adzuna gotcha: **`company=` and `what=` cannot be combined** — HTTP 400. Filter
on company alone and classify afterwards.

## Skill 3 — free-AI second opinion / keyword harvesting

```bash
python3 tools/ai_panel.py ping                      # who answers today
python3 tools/ai_panel.py queries --count 12 --focus "CSA/CAD, Platform Developer I"
python3 tools/ai_panel.py triage-inbox --limit 20   # verdicts on undated rows
```
Peers are tried local → keyless → keyed-free; expect 2-4 of 6 to answer. Treat
output as vocabulary only, never as fact.

## Skill 4 — today-only ATS + Job Bank

```bash
python3 scripts/today_feeds_scan.py --days 2
```
- Workday reports relative stamps ("Posted Today") → converted arithmetically.
- Greenhouse `updated_at` is an update, not a posting date — label it as such.
- **Job Bank's JSON API is dead (HTTP 500)** and its posting pages expose no
  `datePosted`, so it yields no dated rows. Don't invent them.
- SmartRecruiters is the best timestamp source (`releasedDate`), but vendor
  roles (ServiceNow/Salesforce internal engineering) usually don't name the
  product in the title — expect low yield for platform-dev filtering.

## Skill 5 — dedupe (URL, fingerprint, semantic)

```bash
python3 scripts/semantic_dedupe.py            # report
python3 scripts/semantic_dedupe.py --apply    # remove + archive
```
Key is **company + exact normalized title + city**. Never strip seniority
words: "Developer", "Senior Developer" and "Developer Principal" are three
requisitions. The first version of this script did strip them and silently
dropped 196 real rows — recover from `README.DEDUPE_*.md` if it recurs.

## Skill 6 — rescue a blocked peer branch

```bash
git show origin/<branch>:README.md   # extract dated rows, no history merged
# write inbox/sweep-<slug>--<date>--v1.md, then jobs_merge_inbox.py
```
Use when a branch holds good finds but must not be merged (secrets, other
authors' commits). Copy **data only**; never the branch history.

## Skill 7 — publish

```bash
python3 tools/jobs_merge_inbox.py --max-per-table 400
node scripts/sync_readme_to_jobs.mjs && python3 tools/build_site.py
git push origin main       # only after row count >= origin/main
```
Always compare `grep -c '^| 2026-' README.md` against `git show origin/main:README.md`
before pushing: regenerating from a stale inbox silently shrinks the board.

## Known traps

- `git add` with a pathspec that no longer exists (merge renames files) aborts
  the whole add silently — check the staged count.
- `jobs_merge_inbox.py` no longer touches `inbox/` unless you pass `--bump-inbox`
  (CI does). Before that change it renamed and stamped every submission each run,
  so a hand run silently rewrote other agents' files.
- CIBC is excluded (user ineligible until ~Apr 2027) — envelope rule for imports.
- Adzuna's newest record is usually yesterday; "posted today" only comes from
  Workday-style ATS feeds.
