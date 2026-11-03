# Requisition-level dedupe: one card per posting (2026-11-03)

## What was broken

`tools/build_site.py` clustered duplicates on the **raw** `title|company` strings:

```python
key = f'{norm(row["title"])[:70]}|{norm(row["company"])[:40]}'
```

Agencies and aggregators write the same requisition in ways that string never matches:

| Case | Rows on the page |
|---|---|
| WSIB *Manager IT Service Management (ITSM)* | 2 cards — the company cell of the Oracle HCM row held a **location**, and the LinkedIn row used the full legal name, so the employer never matched |
| Celestica | `Celestica` and `Celestica International LP` |
| KPMG | `KPMG` and `KPMG Canada` |
| RideCo | `RideCo` and `RideCo On-Demand Transit` |
| CloudKettle / iA Financial / Capco / Charles River | legal-suffix and parenthetical variants of the same employer |
| City-mirrored requisitions | Alimentiv, Maarut, Bell, TD — the same posting listed under 2–5 cities |

The 40-character truncation also split employers whose names were cut differently
(`Macpower Digital Assets Edge Private L…`).

## What changed — `tools/build_site.py`

Clustering now happens on requisition identity, via union-find over three signals:

1. **Canonical identity** — `canon_title()` strips bracketed noise (`(ITSM)`, `(EN/FR)`,
   `(job 1209)`, `(526327)`), requisition digits, and a trailing city/vendor clause;
   `canon_company()` drops parenthetical aliases, legal suffixes (`inc/ltd/lp/llc/group/…`)
   and country noise.
2. **Employer equivalence** — `companies_related()` accepts equal canonical names,
   token-subset names (`TD` ⊂ `TD Bank Group`), and initialism pairings
   (`WSIB` ↔ `Workplace Safety and Insurance Board`, connector words ignored).
3. **Requisition numbers** — `req_ids()` pulls `job 1209`, `R00356212`, `RQ00206`,
   `(526327)` out of titles; a shared number plus related titles merges the rows.

Two guards stop over-merging, both added after the first dry run produced false merges:

- **Region guard** — `region_of()`/`locations_compatible()`: city variants merge, but
  the same title posted for Canada vs the US / India / Colombia stays separate. Without
  this, NeuraFlash's per-country `Salesforce Technical Architect` requisitions collapsed
  into one card.
- **Weak-title guard** — a canonical title of fewer than two tokens (`"Adzuna 5948024028"`,
  `"LinkedIn"`, `"Job Bank 50631252"`) carries no identity and never absorbs another row.

Mirrors are kept as links rather than deleted: each alternate now carries a
`source · city` label (`LinkedIn · Ontario`, `Adzuna · Kelowna`), deduped by URL and
capped at six. The card also takes the newest date among its mirrors, so a fresher
mirror cannot be hidden behind a stale one.

### Data fix

`README.md` — the WSIB Oracle HCM row had its columns shifted, so the company cell
contained `Toronto, ON; on-site` and the location cell `Permanent full-time`. Repaired
to `WSIB (Workplace Safety and Insurance Board) | Toronto, ON; on-site | Permanent
full-time, $116,000-$145,000 …`. No rows added or removed.

## Verification

| Check | Before | After |
|---|---|---|
| Cards | 813 | 791 |
| Cards showing collapsed mirrors | 25 | 88 |
| WSIB *Manager ITSM* | 2 cards | **1** card (`WSIB …`, alternate `LinkedIn · Ontario`) |
| Celestica SF Developer/Admin | 2 cards | **1** card (`Celestica International LP`, alternate `Adzuna · Toronto`) |
| RideCo Salesforce Administrator | 2 cards | **1** card |
| Capco DevSecOps / TD SRE Lead / iA SF Solution Architect | 2 each | **1** each |
| NeuraFlash cross-country merges | 5 (wrong) | **0** |
| `scripts/check_site_links.py` | PASS | **PASS** (791 cards, 0 rows without an absolute URL) |

`python3 tools/build_site.py` → `site: 791 jobs {'servicenow': 200, 'salesforce': 227,
'other': 364} · 88 with duplicate mirrors collapsed · 19 applied hidden`.

## Known limits / follow-ups

- Two **different client requisitions** pitched by different agencies under the same
  generic title (Futran / Epsilon / Axiom "Salesforce Consultant", Toronto) still show as
  separate cards — they share no requisition number, so merging them would hide a real
  posting.
- ATB *Salesforce DevOps Developer* (Calgary) and *Salesforce Devops Lead* (Edmonton)
  stay separate: different titles and different cities on the employer's side.
- 38 README rows still carry a junk title (`Adzuna <id>`, `LinkedIn`, `Job Bank <id>`) and
  75 carry a location or status flag in the company cell (`Toronto, Ontario`,
  `Full-time`, `Unknown / peer claim not verified`). Those rows can never merge and read
  badly on the page; they need a source-side fix in the inbox submissions that produced
  them, not a clustering rule.
- `scripts/sync_readme_to_jobs.mjs` still dedupes the JSON feed on raw title+company, so
  `/jobs.json` keeps the duplicates the page now collapses.
