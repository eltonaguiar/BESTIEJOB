# Job Bank contributed zero rows; dedupe dropped today's postings

**Date:** 2026-11-03
**Scope:** `scripts/today_feeds_scan.py`, `scripts/linkedin_guest_scan.py`, `scripts/semantic_dedupe.py`

## What was broken

### 1. Job Bank silently returned no rows on every run

`from_jobbank()` extracted the publish date with a schema.org JSON-LD regex:

```python
DATE_LD = re.compile(r'"datePosted"\s*:\s*"([^"]{8,40})"')
```

Job Bank does **not** publish JSON-LD. Its date is a microdata span containing
human text (verified live 2026-11-03):

```html
<span property="datePosted" class="date"> Posted on October 29, 2026 </span>
```

The regex never matched, every detail page hit `continue`, and the source
reported `fetched 0 kept 0` on every scan. Because the count was zero rather
than an error, the run looked healthy.

**Fix:** parse the microdata span and convert the month name to ISO
(`jobbank_day()`). Also strip the `<strong>` markup Job Bank wraps employer
names in, and take role/location from the page title
(`"servicenow developer - Toronto, ON - Job posting - Job Bank"`).

Result: `fetched 72` instead of `fetched 0`, with a real date per row.

### 2. `fdate` (Job Bank's "posted within N days" filter) is dead

`?fdate=1` and every other value return **HTTP 500**, with and without a warm
cookie jar and Referer. The freshness window therefore comes from the parsed
`datePosted` plus the existing `--days` filter, not from the server.

### 3. Unquoted Job Bank keywords match the description, not the title

An unquoted `servicenow` returned shipping clerks and marketing coordinators
because Job Bank matches any word in the body. Quoted phrases are materially
better (`"servicenow consultant"` -> 9 relevant ids). Keyword list switched to
quoted phrases. The existing keyword/geo filter still rejects off-target rows,
so the failure mode is "no rows", never a wrong row.

### 4. Workday tenant discovery cannot use the base URL

`https://{tenant}.wdN.myworkdayjobs.com/` returns **HTTP 406** for real tenants
*and* for wildcard subdomains, so "406 means the tenant exists" is a false
signal — a 42-tenant probe "found" all 42. The CXS JSON endpoint the scanner
already uses is the only reliable check. Boards are added only after CXS
returns a `total`.

Verified this run (matching SN/SF role counts): `neuraflash` 47, `brex` 4,
`mongodb` 4, `icapitalnetwork` 2, `toast` 1, `bloomerang` 1, `movableink` 1.
Greenhouse boards now poll 2,072 postings per run (was 1,104).

### 5. `semantic_dedupe.py` kept the *oldest* copy of a reposted role

```python
keep = sorted(c, key=lambda i: (rows[i]["posted"], -len(rows[i]["title"])))[0]
```

Ascending date = keep the earliest. A role reposted today was discarded in
favour of its week-old duplicate, so dedupe actively removed the freshest rows
from a newest-first board (today's count fell 51 -> 47 across one run).

**Fix:** sort descending, so the freshest copy survives and undated rows lose
rather than win.

### 6. LinkedIn sweep was unscalable

The keyword list grew to 54 and locations to 4, giving 432 sequential requests
(~3.7s each) — far past any single-run budget, and the script writes nothing
until the end, so a killed run wastes the whole sweep. Added `--locations` and
`--pages` flags so scope is a parameter, not an edit.

## Verification

```
today_feeds_scan.py --days 1
  [smartrecruiters] fetched  724  kept 0
  [workday       ] fetched   79  kept 0
  [greenhouse    ] fetched 2072  kept 0
  [lever         ] fetched  140  kept 0
  [ashby         ] fetched   40  kept 0
  [jobbank       ] fetched   55  kept 0     <- was 0 fetched before the fix

from_jobbank(120) -> 55 rows, 4 dated 2026-11-03
linkedin_guest_scan.py -> 620 cards, 0 new (source exhausted for this window)
build_site.py -> 908 jobs {servicenow: 256, salesforce: 291, other: 361}, newest 2026-11-03
```

`kept 0` is correct on this run: the rows found were genuinely off-target or
already on the board. The Job Bank bug was invisible before because it failed
the same way.
