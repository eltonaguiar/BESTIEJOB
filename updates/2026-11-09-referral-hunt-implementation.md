# Referral Hunt Implementation - 2026-11-09

## What was broken / missing
The job hunting pipeline lacked a mechanism to identify and extract employee referral information (mailto inboxes, referral forms, referral pages) from job postings, leading to missed opportunities for direct referrals.

## What I changed
Implemented the "Enhanced Referral Hunt" feature:
1.  **Package + Source Router**: Added `bestiejob/scripts/referral/` package with URL classification logic.
2.  **Host Gate**: Implemented circuit breaking and politeness for web scraping.
3.  **Link Resolver**: Added logic to resolve and validate referral links.
4.  **Extractor**: Created a robust regex-based extractor to identify referral artifacts (forms, emails, pages) while guarding against false positives (e.g., "refer to the job description").
5.  **Orchestrator**: Added `enhanced_referral_hunt.py` to perform referral sweeps.
6.  **Integration**: Updated `jobs.json` schema to include optional `referral_info` and integrated the hunt into the pipeline.

## Verification
- **Tests**: 30 integration and unit tests pass (including regex guards for false positives).
- **Pipeline**: Ran full daily scan and verified `referral_info` is preserved in `jobs.json`.
- **Integrity**: Verified no data loss (1887 jobs maintained, 7 referral hits preserved).
