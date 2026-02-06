import * as cheerio from "cheerio";
import { fetchWithRetry, strategicDelay } from "./utils/scraping_infrastructure.js";

function normalizeText(value) {
  return (value ?? "").toString().replace(/\s+/g, " ").trim();
}

function parseLinkedInRelativeDate(text) {
  const t = normalizeText(text).toLowerCase();
  if (!t) return null;
  if (t.includes("today") || t.includes("just now") || t.includes("just posted")) {
    return new Date();
  }

  const hourMatch = t.match(/(\d+)\s*h/);
  if (hourMatch) {
    const hours = Number(hourMatch[1]);
    return Number.isFinite(hours) ? new Date(Date.now() - hours * 60 * 60 * 1000) : null;
  }

  const dayMatch = t.match(/(\d+)\s*d/);
  if (dayMatch) {
    const days = Number(dayMatch[1]);
    return Number.isFinite(days) ? new Date(Date.now() - days * 24 * 60 * 60 * 1000) : null;
  }

  const weekMatch = t.match(/(\d+)\s*w/);
  if (weekMatch) {
    const weeks = Number(weekMatch[1]);
    return Number.isFinite(weeks) ? new Date(Date.now() - weeks * 7 * 24 * 60 * 60 * 1000) : null;
  }

  const monthMatch = t.match(/(\d+)\s*mo/);
  if (monthMatch) {
    const months = Number(monthMatch[1]);
    return Number.isFinite(months) ? new Date(Date.now() - months * 30 * 24 * 60 * 60 * 1000) : null;
  }

  return null;
}

// LinkedIn date filter codes (f_TPR parameter)
// r86400 = past 24 hours, r604800 = past week, r2592000 = past month
const DATE_FILTERS = {
  "24h": "r86400",
  "day": "r86400",
  "week": "r604800",
  "7d": "r604800",
  "month": "r2592000",
  "30d": "r2592000",
  "any": ""
};

// Experience level filters (f_E parameter)
const EXPERIENCE_FILTERS = {
  internship: "1",
  entry: "2",
  associate: "3",
  mid: "4",
  senior: "4",
  director: "5",
  executive: "6"
};

// Job type filters (f_JT parameter)
const JOB_TYPE_FILTERS = {
  "full-time": "F",
  "part-time": "P",
  contract: "C",
  temporary: "T",
  internship: "I",
  volunteer: "V",
  other: "O"
};

// Default keywords for tech job searches
const DEFAULT_KEYWORDS = [
  "ServiceNow developer",
  "VBA",
  "Alteryx",
  "full stack developer",
  "software engineer",
  "data analyst",
  "DevOps",
  "cloud architect",
  "Python developer",
  "JavaScript developer"
];

const LINKEDIN_ENDPOINTS = [
  { domain: "www.linkedin.com", type: "main" },
  { domain: "www.linkedin.com", type: "guest" },
  { domain: "linkedin.com", type: "lite" }
];

function buildSearchUrl({ keyword, location, start = 0, endpoint = null, dateFilter = "week", jobType = null, experienceLevel = null }) {
  const target = endpoint || LINKEDIN_ENDPOINTS[0];
  const params = new URLSearchParams({
    keywords: keyword,
    location,
    start: String(start),
    sortBy: "DD" // Sort by date (most recent first)
  });
  
  // Add date filter (f_TPR)
  const timeFilter = DATE_FILTERS[dateFilter] || DATE_FILTERS.week;
  if (timeFilter) {
    params.set("f_TPR", timeFilter);
  }
  
  // Add job type filter (f_JT)
  if (jobType && JOB_TYPE_FILTERS[jobType]) {
    params.set("f_JT", JOB_TYPE_FILTERS[jobType]);
  }
  
  // Add experience level filter (f_E)
  if (experienceLevel && EXPERIENCE_FILTERS[experienceLevel]) {
    params.set("f_E", EXPERIENCE_FILTERS[experienceLevel]);
  }
  
  if (target.type === "guest") {
    return `https://${target.domain}/jobs-guest/jobs/api/seeMoreJobPostings/search?${params.toString()}`;
  }
  return `https://${target.domain}/jobs/search/?${params.toString()}`;
}

function buildGuestSearchUrl({ keyword, location, start = 0, domain = "www.linkedin.com", dateFilter = "week", jobType = null }) {
  const params = new URLSearchParams({
    keywords: keyword,
    location,
    start: String(start),
    sortBy: "DD"
  });
  
  // Add date filter
  const timeFilter = DATE_FILTERS[dateFilter] || DATE_FILTERS.week;
  if (timeFilter) {
    params.set("f_TPR", timeFilter);
  }
  
  // Add job type filter
  if (jobType && JOB_TYPE_FILTERS[jobType]) {
    params.set("f_JT", JOB_TYPE_FILTERS[jobType]);
  }
  
  return `https://${domain}/jobs-guest/jobs/api/seeMoreJobPostings/search?${params.toString()}`;
}

function mapJob({ title, url, company, location, postedDate, excerpt, jobType = null }) {
  return {
    title,
    url,
    company: normalizeText(company),
    location: normalizeText(location),
    postedDate: postedDate instanceof Date ? postedDate.toISOString() : postedDate,
    excerpt: normalizeText(excerpt || ""),
    source: "linkedin",
    id: `linkedin:${url || title}`,
    employmentType: jobType || "unknown",
    scrapedAt: new Date().toISOString()
  };
}

function mergeUnique(jobs) {
  const seen = new Set();
  return jobs.filter((job) => {
    const key = job.url || job.title;
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

function extractJobsFromHtml(html) {
  const $ = cheerio.load(html);
  const jobs = [];

  $(".job-search-card, .base-card, .jobs-search__results-list li").each((_, element) => {
    const title = normalizeText($(element).find(".base-search-card__title").text());
    const company = normalizeText($(element).find(".base-search-card__subtitle").text());
    const location = normalizeText($(element).find(".job-search-card__location").text());
    const url = $(element).find("a.base-card__full-link").attr("href");
    const dateText = normalizeText($(element).find("time").text());
    const postedDate = parseLinkedInRelativeDate(dateText);

    if (title && url) {
      jobs.push(
        mapJob({
          title,
          url: url.split("?")[0],
          company,
          location,
          postedDate,
          excerpt: `${title} at ${company}`
        })
      );
    }
  });

  return jobs;
}

async function scrapeLinkedInHtml({ keyword, location, start = 0, endpointIndex = 0, dateFilter = "week", jobType = null }) {
  const endpoint = LINKEDIN_ENDPOINTS[endpointIndex % LINKEDIN_ENDPOINTS.length];
  const url = buildSearchUrl({ keyword, location, start, endpoint, dateFilter, jobType });
  
  console.log(`[LinkedIn] Fetching: ${url}`);
  
  try {
    const response = await fetchWithRetry(url, {
      maxRetries: 3,
      baseDelay: 3000,
      strategicDelay: 2000,
      useProxy: true,
      fallbackProxies: true,
      headers: {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none"
      }
    });
    const jobs = extractJobsFromHtml(response.data);
    console.log(`[LinkedIn] HTML scrape found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    console.warn(`[LinkedIn] Endpoint ${endpoint.domain}/${endpoint.type} failed:`, error.message);
    throw error;
  }
}

async function scrapeLinkedInGuest({ keyword, location, start = 0, domainIndex = 0, dateFilter = "week", jobType = null }) {
  const domains = ["www.linkedin.com", "linkedin.com"];
  const domain = domains[domainIndex % domains.length];
  const url = buildGuestSearchUrl({ keyword, location, start, domain, dateFilter, jobType });
  
  console.log(`[LinkedIn] Guest API: ${url}`);
  
  try {
    const response = await fetchWithRetry(url, {
      maxRetries: 3,
      baseDelay: 3000,
      strategicDelay: 1500,
      useProxy: true,
      fallbackProxies: true,
      headers: {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
        "x-restli-protocol-version": "2.0.0"
      }
    });
    const jobs = extractJobsFromHtml(response.data);
    console.log(`[LinkedIn] Guest API found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    console.warn(`[LinkedIn] Guest endpoint ${domain} failed:`, error.message);
    throw error;
  }
}

async function fallbackLinkedInApi({ keyword, location }) {
  if (!process.env.RAPIDAPI_KEY && !process.env.SERPAPI_KEY) return [];
  
  const endpoints = [
    {
      name: "jsearch-linkedin",
      enabled: !!process.env.RAPIDAPI_KEY,
      url: `https://jsearch.p.rapidapi.com/search?query=${encodeURIComponent(keyword + " " + location + " linkedin")}&page=1`,
      headers: { "X-RapidAPI-Key": process.env.RAPIDAPI_KEY }
    },
    {
      name: "serpapi-linkedin",
      enabled: !!process.env.SERPAPI_KEY,
      url: `https://serpapi.com/search.json?engine=google_jobs&q=${encodeURIComponent(keyword + " " + location)}&api_key=${process.env.SERPAPI_KEY}`,
      headers: {}
    }
  ].filter(e => e.enabled);
  
  for (const endpoint of endpoints) {
    try {
      await strategicDelay(2000, 4000);
      const response = await fetchWithRetry(endpoint.url, {
        maxRetries: 1,
        baseDelay: 1000,
        headers: endpoint.headers
      });
      
      const data = response.data;
      let jobs = [];
      
      if (endpoint.name === "jsearch-linkedin" && data.data) {
        jobs = data.data
          .filter(j => j.job_apply_link?.includes("linkedin") || j.job_publisher?.includes("LinkedIn"))
          .map(j => mapJob({
            title: j.job_title,
            url: j.job_apply_link,
            company: j.employer_name,
            location: j.job_city || location,
            postedDate: j.job_posted_at_datetime_utc ? new Date(j.job_posted_at_datetime_utc).toISOString() : null,
            excerpt: j.job_description?.substring(0, 240) || ""
          }));
      } else if (endpoint.name === "serpapi-linkedin" && data.jobs_results) {
        jobs = data.jobs_results
          .filter(j => j.share_link?.includes("linkedin"))
          .map(j => mapJob({
            title: j.title,
            url: j.share_link,
            company: j.company_name,
            location: j.location || location,
            postedDate: j.date_posted,
            excerpt: j.description?.substring(0, 240) || ""
          }));
      }
      
      if (jobs.length > 0) {
        console.log(`[LinkedIn] API fallback ${endpoint.name}: ${jobs.length} jobs`);
        return jobs;
      }
    } catch (e) {
      console.warn(`[LinkedIn] API ${endpoint.name} failed:`, e.message);
    }
  }
  return [];
}

/**
 * Scrape LinkedIn jobs with advanced filtering
 * @param {string|Object} keywordOrOptions - Either keyword string or options object
 * @param {string} location - Location to search (if using positional args)
 * @param {number} start - Starting offset (if using positional args)
 * @param {number} maxPages - Max pages to scrape (if using positional args)
 * @param {boolean} useFallbackApi - Whether to use fallback APIs (if using positional args)
 */
export async function scrapeLinkedInJobs(keywordOrOptions, location, start = 0, maxPages = 3, useFallbackApi = true) {
  // Support both positional and options-based calling
  let options;
  if (typeof keywordOrOptions === "object") {
    options = keywordOrOptions;
  } else {
    options = { keyword: keywordOrOptions, location, start, maxPages, useFallbackApi };
  }
  
  const {
    keyword = "software engineer",
    location: loc = "Toronto, ON",
    start: offset = 0,
    maxPages: pages = 3,
    useFallbackApi: fallback = true,
    dateFilter = "week",    // 24h, week, month, any
    jobType = null,         // full-time, part-time, contract, etc.
    experienceLevel = null  // entry, mid, senior, director, executive
  } = options;
  
  console.log(`[LinkedIn] Starting scrape for "${keyword}" in "${loc}" (date: ${dateFilter})`);
  
  const results = [];
  const pageCount = Number.isFinite(pages) && pages > 0 ? pages : 1;

  for (let pageIndex = 0; pageIndex < pageCount; pageIndex += 1) {
    const currentOffset = offset + pageIndex * 25;
    
    // Try HTML scraping first
    try {
      await strategicDelay(1500, 3500);
      const htmlJobs = await scrapeLinkedInHtml({ 
        keyword, 
        location: loc, 
        start: currentOffset, 
        endpointIndex: pageIndex,
        dateFilter,
        jobType
      });
      results.push(...htmlJobs);
    } catch (error) {
      console.error("LinkedIn HTML scrape failed:", error?.message || error);
    }

    // Try guest API
    try {
      await strategicDelay(2500, 5000);
      const guestJobs = await scrapeLinkedInGuest({ 
        keyword, 
        location: loc, 
        start: currentOffset, 
        domainIndex: pageIndex,
        dateFilter,
        jobType
      });
      results.push(...guestJobs);
    } catch (error) {
      console.error("LinkedIn guest scrape failed:", error?.message || error);
    }
    
    // Stop if we have enough results
    if (results.length >= 50) {
      console.log(`[LinkedIn] Got ${results.length} jobs, stopping pagination`);
      break;
    }
  }
  
  const uniqueResults = mergeUnique(results);
  console.log(`[LinkedIn] Total unique jobs after scraping: ${uniqueResults.length}`);
  
  // Try fallback APIs if no results
  if (fallback && uniqueResults.length === 0) {
    console.log("[LinkedIn] All scraping methods failed, trying fallback APIs...");
    const apiJobs = await fallbackLinkedInApi({ keyword, location: loc });
    uniqueResults.push(...apiJobs);
  }

  return uniqueResults;
}

/**
 * Scrape LinkedIn for multiple keywords at once
 * @param {Object} options - Search options
 */
export async function scrapeLinkedInMultiKeyword(options = {}) {
  const {
    keywords = DEFAULT_KEYWORDS,
    location = "Toronto, ON",
    dateFilter = "week",
    jobType = "full-time",
    maxJobsPerKeyword = 25
  } = options;
  
  console.log(`[LinkedIn] Multi-keyword scrape: ${keywords.length} keywords`);
  
  const allJobs = [];
  
  for (const keyword of keywords) {
    try {
      await strategicDelay(3000, 6000); // Longer delay between keyword searches
      const jobs = await scrapeLinkedInJobs({
        keyword,
        location,
        dateFilter,
        jobType,
        maxPages: 1, // Single page per keyword to avoid rate limiting
        useFallbackApi: false
      });
      
      const limited = jobs.slice(0, maxJobsPerKeyword);
      allJobs.push(...limited);
      console.log(`[LinkedIn] "${keyword}": ${limited.length} jobs`);
    } catch (error) {
      console.error(`[LinkedIn] Keyword "${keyword}" failed:`, error.message);
    }
  }
  
  return mergeUnique(allJobs);
}

// Export filter constants for use by other modules
export { DATE_FILTERS, JOB_TYPE_FILTERS, EXPERIENCE_FILTERS, DEFAULT_KEYWORDS };