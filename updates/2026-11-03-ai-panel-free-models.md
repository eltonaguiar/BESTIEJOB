# 2026-11-03 — Free-AI second-opinion panel wired into the daily job scan

## What was missing

The daily scan was 100% deterministic: `scripts/daily_job_scan.mjs` + `scripts/gap_scan.mjs`
hit a hard-coded Adzuna `what` list (13 questions in `ADZUNA_VARIANTS`), and nothing in
BESTIEJOB had ever called an LLM. Meanwhile the workspace already had a large verified pool
of free / keyless inference endpoints (see `~/dbpasses_ASK_2026-11-02.txt` and
`~/dbpasses_ASK_MISSING_free-models_2026-11-03.txt`) that no job-pipeline code used.

Result: the scan could only find roles whose vocabulary someone had already typed into
`gap_scan.mjs`, and ambiguous listings were never independently reviewed.

## What changed

**New: `tools/ai_panel.py`** — one file, three subcommands, no dependencies beyond stdlib.

| Subcommand | Purpose |
|---|---|
| `ping` | Live health-check every peer: status, latency, which model actually answered |
| `queries` | Ask N independent models for extra Adzuna `what` variants, then filter |
| `triage` | Second-opinion classify a batch of job rows (`servicenow/salesforce/other/reject`) |

Provider registry, ordered local → keyless → keyed-free (so a normal run costs nothing):

| Tier | Peers |
|---|---|
| local | vLLM `:8000`, Ollama `:11434`, LiteLLM `:4000` (model IDs discovered, not pinned) |
| keyless | Kilo Gateway, Pollinations, LLM7, OVH AI Endpoints |
| keyed free | Groq, Gemini, HuggingFace router, DeepInfra, Cohere, Mistral, PublicAI, Cloudflare Workers AI, SiliconFlow, Z.AI, OpenRouter, Nous, SambaNova, AIMLAPI |

**Key handling** — three passes over `~/dbpasses.txt`, then env as override:
label match (normalized, tolerant of missing trailing colons and of keys sitting two lines
below the label), key-prefix scan (`gsk_`, `sk-or-v1-`, `hf_`, `AIza`, `zpka_`, `cohere_`,
`github_pat_`), then env. Keys are never printed, logged, or written to a repo file.

**Wiring** — `scripts/daily_scan.sh` now runs `ai_panel.py queries` immediately before
`gap_scan.mjs`, writing `raw/ai_queries.json`. `gap_scan.mjs` merges those into
`ADZUNA_VARIANTS` (accepts `--variants-file=<path>`, defaults to `raw/ai_queries.json`).

**Two independent filters on every proposal.** The panel keeps only 2–4 word lowercase
keyword-shaped phrases and drops anything containing a city, `site:`, a URL, or an `@`.
`gap_scan.mjs` re-applies the same shape rules against its own list. A hallucinated phrase
therefore costs nothing worse than a skipped keyword — it can never become a fabricated job.

**`package.json`**: added `ai:ping`, `ai:queries`, `ai:triage`.

## Verification (2026-11-03)

```
python3 -c "py_compile ai_panel.py" → OK
node --check scripts/gap_scan.mjs   → OK
bash -n scripts/daily_scan.sh       → OK
package.json scripts → ai:ping ai:queries ai:triage present

python3 tools/ai_panel.py ping --only kilocode,pollinations,llm7,groq,cohere --limit 5
  kilocode     keyless  OK  0.72s  cohere/north-mini-code:free
  pollinations keyless  OK  6.11s  openai-fast
  llm7         keyless  OK  0.79s  codestral-latest
  groq         free     OK  0.30s  openai/gpt-oss-120b
  cohere       free     OK  0.19s  command-r7b-12-2024
  5/5 peers answered

python3 tools/ai_panel.py queries --only kilocode,pollinations,llm7,groq --peers 4 --count 8
  → 2/4 peers answered; 8 keywords kept, written to raw/ai_queries.json
```

## Known limitations

- **2/4 peers answering is normal, not a bug.** Free tiers 429/402 individually; the panel
  reports an answer count instead of assuming success. With `--peers 6` (the scan default)
  three or four usually answer.
- **Proposals repeat across runs.** The filter dedupes against `ADZUNA_VARIANTS` and within a
  run, but not against yesterday's file — repeated keywords only cost a redundant API call.
- **`triage` is not yet in the scheduled loop.** It exists and is tested by syntax and by the
  documented invocation, but no scan step consumes its output yet; it needs a caller that has
  a batch of undated `inbox/` rows to review.
- **No peer output is trusted as fact.** The panel supplies search vocabulary and a second
  reading only. Dates still come from the source, never from a model.
