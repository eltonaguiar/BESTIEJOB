# jev-ultrafast — single-purpose LinkedIn harvest (design)

Status: **design only, blocked on `TYPESAFE_API_KEY`.**
Evaluated 2026-11-09; see `updates/2026-11-09-parallel-search-and-jev-query-widening.md`
for why it is not wired in yet.

Upstream: <https://github.com/browser-use/jev-ultrafast> — browser agent, one goal
per run, numbered element table, CLICK / TYPE_TEXT / SELECT / SCROLL / DONE.

## The one job it is allowed to do

> With the operator's **already signed-in** Chrome, open one LinkedIn job search,
> scroll until the N newest cards are visible, and stop.

Nothing else. No Apply / Easy Apply, no Message / InMail, no connection requests,
no profile edits, no saved-search changes, no recruiter inbox. Those are the
actions a browser agent could take and must never take unattended.

## Why jev at all

The guest endpoint (`linkedin_guest_scan.py`) already covers public search, and
Playwright covers static pages for free. The gap is **session-walled pages**: the
signed-in jobs view, "My Jobs", and cards whose description only renders inside a
logged-in session. jev's Browser Harness attaches to the operator's own Chrome, so
it inherits the session without ever handling the password. That is the only
capability worth the cost here.

It does **not** bring discovery (no search), bulk extraction (one goal per run, no
row output), or cheap volume (a TypeSafe round trip per decision). So jev drives;
a deterministic reader extracts.

## Prerequisites

| Item | Check |
|---|---|
| `TYPESAFE_API_KEY` | `env | grep -c TYPESAFE` → 1 |
| `TEXT_MODEL_API_KEY` (OpenRouter works) | key present in `~/dbpasses.txt` |
| `uv` | `uv --version` |
| Browser Harness | `uv run browser-harness --doctor` |
| Chrome | remote debugging allowed, LinkedIn signed in, **own profile** |
| Legal | operator's own account; read-only browsing; no bulk automation of actions |

Setup:

```bash
git clone https://github.com/browser-use/jev-ultrafast.git /tmp/jev-ultrafast
cd /tmp/jev-ultrafast && uv sync && cp .env.example .env   # add both keys
```

## Run shape

```python
from jev_ultrafast import Agent

GOAL = (
    "LinkedIn is already signed in. Open the job search for ServiceNow developer "
    "in Toronto, Canada posted in the past week. Scroll the results list until at "
    "least 25 job cards are visible. Do not click Apply, Easy Apply, Message, "
    "Connect, Save, or any recruiter link. Stop when 25 cards are visible."
)

with Agent("https://www.linkedin.com/jobs/search/?keywords=ServiceNow%20developer"
           "&location=Toronto%2C%20Ontario%2C%20Canada&f_TPR=r604800", GOAL) as agent:
    for state in agent.run():
        print(state["elapsed_ms"], state["status"])   # DONE -> hand off to the reader
```

Then the **deterministic reader** (Playwright, same attached Chrome) reads the
cards and emits rows:

- `title`, `company`, `location`, `href` from the card anchor
- posted date **only** from the card's `<time datetime="YYYY-MM-DD">` attribute
- if there is no `<time datetime>`, the row is dropped — "3 days ago" is never
  converted into a date

## Output contract

`inbox/linkedin-jev--YYYY-MM-DD--v1.md`, six columns, per
`docs/JOB_SUBMISSION_METHODOLOGY.md`:

```
| Posted | Role | Company | Location | URL | Note |
| 2026-11-06 | [ServiceNow Developer](https://ca.linkedin.com/jobs/view/…) | Acme | Toronto, ON | via jev session harvest |
```

Dedupe key is the numeric LinkedIn job id (`/jobs/view/…-<ID>`), so the same
posting reached through a different URL collapses.

## Guardrails

- ≤ 5 queries per run, ≤ 3 result pages each, 4–6 s between navigations
- abort on any sign-in / challenge / 429 page; report, do not retry blindly
- never persist cookies, tokens, or the profile; the run borrows the session in place
- never submit a form, never send a message, never click Apply/Save
- trace files to `raw/`, ignored unless the run produced rows

## Verification before merge

1. `python3 scripts/check_inbox.py` — every Posted cell is an absolute date
2. `python3 .github/scripts/readme_job_row_guard.py --base origin/main --head HEAD`
3. `node scripts/check_readme_sort.mjs`
4. spot-check 3 URLs in a logged-out browser: a row must resolve to the same title

## Acceptance

- ≥ 10 net-new postings inside 7 days, 0 fabricated dates, 0 duplicate ids
- no account action beyond navigation and scrolling
- wall-clock under 5 minutes and under ~50 TypeSafe decisions for 25 cards

## Failure modes

| Symptom | Response |
|---|---|
| `DONE` chosen but cards not loaded | verify count independently; do not trust the agent's own claim |
| shadow DOM / iframe cards | jev's MVP does not handle them; fall back to guest endpoint |
| 429 from LinkedIn | stop the run; next attempt ≥ 30 min later |
| TypeSafe 402/403 | key/quota issue — log and exit 0 without writing a submission |
