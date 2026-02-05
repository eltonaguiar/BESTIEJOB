# BESTIEJOB

Toronto-focused job posting consolidator for creative / technology manager roles with a salary minimum filter.

## Filters

- Location: Toronto (and GTA text matches)
- Role keywords: creative / technology / manager / management
- Employment: full-time (best-effort detection)
- Salary: minimum salary slider (default $100K, preset $110K)

## Simplify applications source

This project can pull your Simplify Applications list (requires an authenticated cookie).

- Set `SIMPLIFY_COOKIE` in the environment **or** pass `simplifyCookie` as a query param to `/api/jobs`.
- Use `timelineDays` to limit results to the last N days (defaults to 30).

Example:

```
/api/jobs?keywords=product%20manager&timelineDays=14
```

## Running locally

```bash
npm install
npm run dev
```

Then open:

- http://localhost:3000
