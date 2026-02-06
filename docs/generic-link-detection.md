# Enhanced Generic Link Detection - Implementation Notes

## Context
We're filtering **already-scraped job data**, not doing live page validation. The advanced Playwright techniques (iframe scanning, Apply button detection, client-side hydration) are valuable for the **scraping phase**, but our current task is to filter the scraped results.

## Current Approach (Client-Side Filtering)

We have access to these job object fields:
- `url` - The job posting URL
- `title` - Job title
- `excerpt` - Job description snippet
- `company` - Company name
- `location` - Job location
- `postedDate` / `scrapedAt` - Timestamps
- `deadline` - Application deadline
- `salary` - Salary information
- `source` - Where the job was scraped from

## Enhanced Detection Rules (Implemented)

### 1. Job ID Detection (Primary Signal)
```javascript
// Patterns that indicate a specific job posting:
/\/(job|jobs|apply|position|posting|vacancy|opening|career)\/([\w-]+\/)*\d+/i
/[?&](id|jobid|job_id|position|posting|req|requisition)=[\w-]+/i
/\/\d{5,}/i  // Long numeric IDs
```

**Examples:**
- ✅ `jobs.rogers.com/job/Toronto-Media.../1360702300/`
- ✅ `careers.company.com/apply?id=12345`
- ❌ `sunlife.com/en/careers/` (no ID)

### 2. Generic URL Patterns
```javascript
// URLs ending with these are likely generic:
/careers/, /careers.html, /careers.aspx, /jobs/, /talent/
```

### 3. Title Quality Check
```javascript
// Generic titles that indicate portals:
'careers', 'join us', 'job opportunities', 'life at', 'our people'
```

### 4. Job-Specific Fields Validation
```javascript
// Real jobs typically mention:
location, department, posted, employment type, full-time, remote, salary, apply
```

### 5. Structured Data Indicators
```javascript
// Check excerpt for schema.org markers:
@type.*jobposting, schema.org/jobposting, og:type.*job
```

## Decision Logic

**Flag as GENERIC if:**
1. URL ends with generic pattern AND no job ID
2. Has generic title AND no job-specific fields AND no job ID
3. Has career path but no job ID and very short path

**Flag as VALID if:**
1. Has job ID in URL (highest confidence)
2. Has structured data indicators
3. Has job-specific fields and not generic title

## Future Enhancements (For Scraping Phase)

These advanced techniques should be implemented in the **scraper**, not the client-side filter:

### 1. Iframe Detection (Workday, Greenhouse, Lever)
```javascript
// During scraping:
const frames = page.frames();
for (const frame of frames) {
  const frameHtml = await frame.content();
  // Extract job data from iframe
}
```

### 2. Apply Button Detection
```javascript
// During scraping:
const hasApplyButton = await page.$('button:has-text("Apply"), a:has-text("Apply")');
// Store this as metadata: job.hasApplyButton = true
```

### 3. Client-Side Hydration Handling
```javascript
// During scraping:
await page.waitForSelector('.job-description', { timeout: 5000 });
// Wait for SPA to hydrate before extracting data
```

### 4. Microdata Detection
```javascript
// During scraping:
const hasMicrodata = await page.$('[itemtype*="JobPosting"]');
```

## Recommendation

**For immediate improvement:**
- ✅ Current client-side filtering is good for URL/title/field validation
- ✅ Catches most generic career pages

**For long-term quality:**
- 📋 Implement iframe scanning in scraper
- 📋 Add "Apply button presence" field to job schema
- 📋 Detect and store structured data type (JSON-LD vs Microdata)
- 📋 Add "page type" classification during scraping (portal vs posting)

## Test Cases

| URL | Has Job ID | Title | Expected | Actual |
|-----|-----------|-------|----------|--------|
| `sunlife.com/slgs/en/careers/slgs-careers/` | ❌ | Generic | Generic | ✅ Generic |
| `mfs.com/careers.html` | ❌ | Generic | Generic | ✅ Generic |
| `jobs.rogers.com/job/.../1360702300/` | ✅ | Specific | Valid | ✅ Valid |
| `greenhouse.io/company/jobs/123456` | ✅ | Specific | Valid | ✅ Valid |
| `workday.com/company/job/Senior-Dev/JR12345` | ✅ | Specific | Valid | ✅ Valid |
