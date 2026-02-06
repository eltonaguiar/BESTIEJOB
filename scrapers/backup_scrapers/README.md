# Backup Scrapers for BESTIEJOB

This folder contains backup scraper functions for additional job sources. These are designed to be leveraged by your main scrapers or used as fallbacks.

## Available Scrapers

### Basic Scrapers (HTTP/Axios)
- `glassdoor_scraper.js` - Basic Glassdoor scraper
- `workopolis_scraper.js` - Basic Workopolis scraper  
- `wellfound_scraper.js` - Basic Wellfound (AngelList) scraper
- `monster_scraper.js` - Basic Monster scraper

### Stealth-Enhanced Scrapers
- `glassdoor_stealth.js` - Enhanced with headers, delays, multiple selectors
- `workopolis_stealth.js` - Enhanced with anti-bot evasion
- `wellfound_stealth.js` - Enhanced with stealth techniques
- `monster_stealth.js` - Enhanced with stealth techniques

### Playwright Fallback
- `playwright_fallback.js` - Browser automation for blocked sites

## Test Results (Feb 5, 2026)

### Status: All Basic + Stealth Scrapers Blocked ❌

| Source | Basic | Stealth | Playwright | Status |
|--------|-------|---------|------------|--------|
| Glassdoor | 0 | 0 | ? | Strong anti-bot |
| Workopolis | 0 | 0 | ? | 403 Forbidden |
| Wellfound | 0 | 0 | ? | 403 + Captcha |
| Monster | 0 | 0 | ? | Structure changed |

**Recommendation**: Use Playwright fallback for these sites, or focus on APIs that work:
- ✅ Adzuna API (9,000+ jobs)
- ✅ JobBank (500+ jobs)
- ✅ RemoteOK API (100+ jobs)
- ✅ Jobicy API (20+ jobs)
- ✅ EURemote RSS (15+ jobs)

## Usage

### Basic/Stealth (HTTP-based)
```js
import { fetchGlassdoorJobsStealth } from './backup_scrapers/glassdoor_stealth.js';
const jobs = await fetchGlassdoorJobsStealth(["manager"], "Toronto, ON", 1);
```

### Playwright (Browser-based)
```js
import { fetchGlassdoorJobsPlaywright } from './backup_scrapers/playwright_fallback.js';
const jobs = await fetchGlassdoorJobsPlaywright(["manager"], "Toronto, ON", 1);
```

## Job Object Format

```js
{
  id: string,           // Unique ID with source prefix
  source: string,       // glassdoor|workopolis|wellfound|monster
  title: string,
  company: string,
  location: string,
  url: string,
  salary: string|null,
  employmentType: string,
  postedDate: string,
  excerpt: string
}
```

## Integration Example

```js
// Try stealth first, fall back to Playwright
async function fetchWithFallback(source, keywords, location) {
  let jobs = [];
  
  // Try stealth HTTP
  if (source === 'glassdoor') {
    jobs = await fetchGlassdoorJobsStealth(keywords, location, 1);
  }
  
  // Fall back to Playwright if no results
  if (jobs.length === 0) {
    console.log(`[${source}] Stealth failed, trying Playwright...`);
    jobs = await fetchGlassdoorJobsPlaywright(keywords, location, 1);
  }
  
  return jobs;
}
```

## Notes
- All basic scrapers blocked by anti-bot measures (403 errors)
- Stealth scrapers include: rotating UA, headers, delays, multi-selectors
- Playwright fallback uses real browser automation (slower but more reliable)
- For production, consider using APIs instead of scraping these sources
- JobBank, Adzuna, and RemoteOK APIs are recommended alternatives

---

Last updated: 2026-02-05
