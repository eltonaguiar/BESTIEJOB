/**
 * Which already-published feed rows survive the next rewrite of jobs.json?
 *
 * `scripts/daily_job_scan.mjs` rewrites jobs.json from scratch every hour, so
 * this decision is a deletion policy: anything it rejects leaves the board until
 * a later scrape re-finds it literally.
 *
 * Keyword tags decide what a *scrape* may add — they are the search remit. They
 * must not decide what *survives*. Every row in the feed has already been
 * accepted once, either by a keyword-scoped scan, by `jobs_merge_inbox.py` from
 * a peer's verified inbox, or by `sync_readme_to_jobs.mjs` from the curated
 * README tables (which include the "Other jobs" section: Workday, MuleSoft,
 * SQL/DBA, GRC, cloud and similar IT-platform roles).
 *
 * Re-testing those rows against the tag regexes was silently deleting them: on
 * 2026-11-04 the hourly run removed 265 rows, 230 of them in-remit IT roles
 * whose titles simply match no ServiceNow/Salesforce/partner keyword, and the
 * live page dropped 246 cards. Hence: prune on validity, not on keywords.
 *
 * Kept guard: rows without a usable date/URL/title, rows older than the window
 * (the board is a 45-day board), and generic career-homepage entries.
 */
export function carryExistingJobs(list, { now, maxAgeDays, matchTags }) {
  const jobs = [];
  const dropped = { invalid: 0, stale: 0, generic: 0 };

  for (const job of list) {
    if (!job?.postedDate || !job?.url || !job?.title) {
      dropped.invalid += 1;
      continue;
    }
    const ageDays = (now - new Date(job.postedDate)) / 864e5;
    if (!Number.isFinite(ageDays) || ageDays > maxAgeDays) {
      dropped.stale += 1;
      continue;
    }
    if (/^careers?$|^job openings$|^open positions$/i.test(String(job.title).trim())) {
      dropped.generic += 1;
      continue;
    }
    // Derive tags when they are missing so downstream `.tags.includes()`
    // callers keep working; an empty result no longer rejects the row.
    if (!Array.isArray(job.tags) || job.tags.length === 0) {
      job.tags = matchTags(job.title);
    }
    jobs.push(job);
  }

  return { jobs, dropped };
}
