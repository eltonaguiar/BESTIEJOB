# Job Search Methodology — AI-Augmented, System-Driven

Purpose: run a job search like a project, not a scramble. Combines a proven 6-stage execution system with free job-search APIs and an AI second-opinion panel to score/tailor applications.

## Core principle
> Target, don't spray. Ten well-matched, well-tailored applications beat a hundred anonymous ones. Volume is input #2; targeting is input #1.

---

## Stage 1 — Direction (pick a viable target)
Don't start with the résumé. Start with a testable hypothesis: a role family + level + employer type + location where your experience and real hiring demand overlap.

**Output:** one sentence, e.g. *"Remote AI/ML Engineer at Series B–C AI startups, using Python + LLM agents/RAG, $140K–$190K."*

Then build a **target list of 20–40 companies** you'd genuinely join. Work backward from certainty: companies where you'd take an offer. Mix sizes/stages so the pipeline isn't dependent on one category. For each, bookmark the careers page directly and note which ATS they use (Greenhouse/Lever/Ashby/Workday) so you can check new roles quickly.

---

## Stage 2 — Proof (evidence over adjectives)
Employers hire on evidence, not claims. Build:
- One strong résumé (ATS-clean, tailored per role-type).
- 3–5 STAR stories with measurable outcomes.
- A portfolio / GitHub / demo you can point to.
- A LinkedIn profile showing real work, not just titles.

**Rule:** "Strategic / detail-oriented / fast learner" are weak. Replace with numbers and shipped artifacts.

---

## Stage 3 — Access (warm paths beat cold applies)
A referral gets your application read by a person. Map your network against your target list. Reach out genuinely (not "please refer me"): send your tailored résumé + the exact posting, ask for a conversation not a job.

Also cold-message recruiters on LinkedIn, set up informational interviews. Presence before need: post one thing you built/solved so people can vouch.

---

## Stage 4 — Apply (fewer, stronger, faster)
Apply within 24–48 hours of a role going live (early-window advantage). Mirror the posting's language so you clear the ATS and read as a fit. Tailor headline + top bullets per posting; skip generic cover letters unless asked.

**Cadence:** 3–5 applications/week while employed; 8–15/week while searching full-time. Never mass-apply untailored.

---

## Stage 5 — Convert (interviews → offers)
Build stories before interviews land. Research the company (Glassdoor, their blog, product). Practice answers out loud. Follow up ~1 week after applying, max twice, then move on.

---

## Stage 6 — Learn (feedback loop)
Track every opportunity in one pipeline (spreadsheet is fine): company, role, date applied, stage, next action + date. An application with no next action is a passive one. Review weekly: find the bottleneck, change one thing.

---

## The AI-augmented pipeline (this repo's tools)

### `tools/ai_second_opinion.py` — second-opinion fan-out
Fans one question to 5 free AI providers and aggregates a consensus + confidence.

Providers (all verified PONG 2026-11-03):
| Provider | Model | Key | Cost |
|---|---|---|---|
| Groq | openai/gpt-oss-120b | in `dbpasses.txt` | free |
| Gemini | gemini-2.5-flash | in `dbpasses.txt` | free |
| OpenRouter (free) | nvidia/nemotron-3.5-lightning:free | in `dbpasses.txt` | free |
| vLLM local (:8000) | Qwen2.5-14B-Instruct | none | free |
| Ollama local (:11434) | deepseek-r1:32b | none | free |

Usage:
```
python3 tools/ai_second_opinion.py "should I apply to this role?" \
    --context "RESUME: ...\nJOB: ..."
python3 tools/ai_second_opinion.py --file question.txt --context-file ctx.txt --json
```
Exit codes: 0 = lean yes, 1 = lean no, 2 = mixed/dead (scriptable).

### `tools/job_discover.py` — discover + AI-score jobs
Pulls from free, keyless job APIs, normalizes, then asks the AI panel "should I apply?" per job and ranks by yes-consensus + confidence.

Free job sources (no key, verified 2026-11-03):
| Source | Endpoint | Coverage |
|---|---|---|
| Arbeitnow | https://www.arbeitnow.com/api/job-board-api | EU + remote, visa flag |
| RemoteOK | https://remoteok.com/api | tech remote jobs |
| Remotive | https://remotive.com/api/remote-jobs | ~1,500 remote jobs |
| Freehire | https://freehire.me/api/v1/jobs | 3.3M+ ATS-sourced jobs |

Usage:
```
python3 tools/job_discover.py --query "ai engineer" --location remote \
    --limit 30 --top 10 --resume-file resume.txt --out jobs_ranked.csv
python3 tools/job_discover.py --query "python" --source arbeitnow --limit 50 --no-ai
```
Output: ranked CSV (title, company, location, AI recommendation, confidence, yes-votes, rationale, salary, URL).

---

## Weekly rhythm (sustainable)
- Monday: refresh target-list careers pages + fetch new jobs (job_discover).
- Tue–Thu: score top jobs with AI panel, tailor résumé + apply to 3–8 best-fit roles.
- Friday: network outreach (5–8 messages), follow-ups, pipeline review.
- Weekend: build proof (one project/demo), rest.

**Protect the pace.** A burned-out searcher runs a worse process, not a faster one.

---

## Files in this repo
- `tools/ai_second_opinion.py` — free AI second-opinion fan-out
- `tools/job_discover.py` — free job discovery + AI scoring
- `dbpasses_ASK_2026-11-02.txt` — verified free AI provider keys/endpoints
- `dbpasses_ASK_MISSING*_2026-11-03.txt` — additional free providers to signup for
- `dbpasses.txt` — underlying key vault (masked keys in ASK file)
