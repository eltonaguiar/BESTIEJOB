import * as cheerio from "cheerio";
import Parser from "rss-parser";
import { stealthFetch, scrapeWithBrowser, isBlocked, gaussianDelay } from "./utils/stealth_browser.js";

const rssParser = new Parser({
  headers: {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
  },
  timeout: 30000
});

function normalizeText(value) {
  return (value ?? "").toString().replace(/\s+/g, " ").trim();
}

function parseRelativeDate(text) {
  const t = normalizeText(text).toLowerCase();
  if (!t) return null;
  if (t.includes("just posted") || t.includes("today") || t.includes("just now")) return new Date();

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

  // Try parsing "Posted X days ago" format
  const agoMatch = t.match(/(\d+)\s*(day|week|month|hour)s?\s*ago/);
  if (agoMatch) {
    const num = Number(agoMatch[1]);
    const unit = agoMatch[2];
    const multipliers = { hour: 60 * 60 * 1000, day: 24 * 60 * 60 * 1000, week: 7 * 24 * 60 * 60 * 1000, month: 30 * 24 * 60 * 60 * 1000 };
    return new Date(Date.now() - num * (multipliers[unit] || multipliers.day));
  }

  return null;
}

// Indeed date filter values (fromage parameter in days)
const DATE_FILTERS = {
  "24h": "1",
  "day": "1",
  "3d": "3",
  "week": "7",
  "7d": "7",
  "14d": "14",
  "month": "30",
  "30d": "30",
  "any": ""
};

// Job type filters (jt parameter)
const JOB_TYPE_FILTERS = {
  "full-time": "fulltime",
  "part-time": "parttime",
  contract: "contract",
  temporary: "temporary",
  internship: "internship",
  permanent: "permanent"
};

// Experience level (explvl parameter)
const EXPERIENCE_FILTERS = {
  entry: "entry_level",
  mid: "mid_level",
  senior: "senior_level"
};

// Default keywords for tech job searches
const DEFAULT_KEYWORDS = [
  "ServiceNow developer",
  "VBA developer",
  "Alteryx",
  "full stack developer",
  "software engineer",
  "data analyst",
  "DevOps engineer",
  "cloud architect",
  "Python developer",
  "JavaScript developer",
  "React developer",
  "AWS engineer"
];

const DOMAINS = [
  "ca.indeed.com",
  "www.indeed.com",
  "uk.indeed.com"
];

let domainRotationIndex = 0;

function getNextDomain() {
  const domain = DOMAINS[domainRotationIndex % DOMAINS.length];
  domainRotationIndex++;
  return domain;
}

function toIndeedSearchUrl({ keyword, location, start = 0, domain = null, dateFilter = "week", jobType = null, salary = null }) {
  const params = new URLSearchParams({
    q: keyword,
    l: location,
    start: String(start),
    sort: "date" // Sort by date posted
  });
  
  // Add date filter (fromage = days ago)
  const fromage = DATE_FILTERS[dateFilter];
  if (fromage) {
    params.set("fromage", fromage);
  }
  
  // Add job type filter
  if (jobType && JOB_TYPE_FILTERS[jobType]) {
    params.set("jt", JOB_TYPE_FILTERS[jobType]);
  }
  
  // Add minimum salary filter (if supported)
  if (salary && Number.isFinite(salary)) {
    params.set("salary", String(salary));
  }
  
  const targetDomain = domain || getNextDomain();
  return `https://${targetDomain}/jobs?${params.toString()}`;
}

function mapJob(job) {
  return {
    ...job,
    source: "indeed",
    id: job.id || `indeed:${job.url || job.title}`,
    scrapedAt: new Date().toISOString(),
    employmentType: job.employmentType || "unknown"
  };
}

function mergeUnique(jobs) {
  const seen = new Set();
  return jobs.filter((job) => {
    const key = job.url || job.id || job.title;
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

async function scrapeIndeedHtml({ keyword, location, start = 0, domainIndex = 0, dateFilter = "week", jobType = null }) {
  const domain = DOMAINS[domainIndex % DOMAINS.length];
  const url = toIndeedSearchUrl({ keyword, location, start, domain, dateFilter, jobType });
  
  console.log(`[Indeed] Fetching: ${url}`);
  
  try {
    const response = await stealthFetch(url, { 
      maxRetries: 3,
      headers: {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate"
      }
    });
    
    if (isBlocked(response.data)) {
      throw new Error("Blocked by anti-bot");
    }
    
    const jobs = extractJobsFromHtml(response.data);
    console.log(`[Indeed] HTML scrape found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    console.log(`[Indeed] Domain ${domain} failed: ${error.message}`);
    
    // Try browser fallback only if Playwright is available
    try {
      console.log("[Indeed] Attempting browser fallback...");
      await gaussianDelay(3000, 6000);
      const html = await scrapeWithBrowser(url);
      if (!isBlocked(html)) {
        const jobs = extractJobsFromHtml(html);
        console.log(`[Indeed] Browser scrape found ${jobs.length} jobs`);
        return jobs;
      }
    } catch (browserError) {
      console.warn(`[Indeed] Browser fallback failed: ${browserError.message}`);
    }
    
    return [];
  }
}

function extractJobsFromHtml(html) {
  const $ = cheerio.load(html);
  const jobs = [];

  $("a[data-jk], .jobTitle, .slider_container .slider_item").each((_, element) => {
    const $el = $(element);
    const title = normalizeText(
      $el.find("h2.jobTitle span, .jobTitle span, [data-testid='job-title']").first().text() ||
      $el.find("a").attr("title")
    );
    if (!title) return;

    let urlPath = $el.attr("href") || $el.closest("a").attr("href");
    if (!urlPath && $el.find("a").length > 0) {
      urlPath = $el.find("a").first().attr("href");
    }
    const url = urlPath ? (urlPath.startsWith("http") ? urlPath : `https://ca.indeed.com${urlPath}`) : "";
    if (!url) return;

    const company = normalizeText($el.find("span.companyName, [data-testid='company-name']").first().text());
    const locationText = normalizeText($el.find("div.companyLocation, [data-testid='job-location']").first().text());
    const snippet = normalizeText($el.find("div.job-snippet, [data-testid='job-summary']").first().text());
    const dateText = normalizeText($el.find("span.date, [data-testid='job-date']").first().text());
    const postedDate = parseRelativeDate(dateText);

    jobs.push(mapJob({
      title, company, location: locationText, url,
      postedDate: postedDate ? postedDate.toISOString() : null, excerpt: snippet
    }));
  });

  // Look for embedded JSON
  $("script").each((_, el) => {
    const text = $(el).html() || "";
    if (text.includes("_initialData") || text.includes("jobmap")) {
      try {
        const match = text.match(/window\._initialData\s*=\s*({.+?});/) || text.match(/jobmap\s*=\s*(\[.+?\]);/);
        if (match) {
          const data = JSON.parse(match[1]);
          const jobResults = data?.jobSearch?.jobSearchResults?.results || data || [];
          jobResults.forEach((j) => {
            const id = j.jobkey || j.key;
            if (!jobs.find(existing => existing.id === id)) {
              jobs.push(mapJob({
                id, title: j.title || j.jobTitle,
                company: j.company?.name || j.companyName,
                location: j.formattedLocation || j.loc,
                url: j.url || `https://ca.indeed.com/viewjob?jk=${id}`,
                postedDate: j.date || j.postedDate,
                excerpt: j.snippet || j.description?.text?.substring(0, 240)
              }));
            }
          });
        }
      } catch {}
    }
  });

  return jobs;
}

async function scrapeIndeedRss({ keyword, location, dateFilter = "week" }) {
  const q = encodeURIComponent(keyword);
  const l = encodeURIComponent(location);
  const fromage = DATE_FILTERS[dateFilter] || "7";
  
  const endpoints = [
    `https://ca.indeed.com/rss?q=${q}&l=${l}&sort=date&fromage=${fromage}`,
    `https://rss.indeed.com/rss?q=${q}&l=${l}&sort=date&fromage=${fromage}`,
    `https://www.indeed.com/rss?q=${q}&l=${l}&sort=date`
  ];
  
  console.log(`[Indeed] Trying RSS feeds for "${keyword}"...`);
  
  for (const url of endpoints) {
    try {
      await gaussianDelay(1000, 2000);
      const feed = await rssParser.parseURL(url);
      const items = Array.isArray(feed?.items) ? feed.items : [];
      if (items.length > 0) {
        console.log(`[Indeed] RSS: ${items.length} jobs from ${url}`);
        return items.map((it) => mapJob({
          title: normalizeText(it.title?.replace(/ - job post$/, "").replace(/ - .+$/, "")),
          company: normalizeText(it.creator || it.author || ""),
          location: location,
          url: normalizeText(it.link),
          postedDate: it.pubDate ? new Date(it.pubDate).toISOString() : null,
          excerpt: (it.contentSnippet || it.content || "").slice(0, 240).replace(/<[^>]*>/g, "")
        }));
      }
    } catch (error) {
      console.warn(`[Indeed] RSS ${url} failed: ${error.message}`);
    }
  }
  return [];
}

async function fallbackApiScrape({ keyword, location }) {
  const apiEndpoints = [
    {
      name: "jsearch",
      url: `https://jsearch.p.rapidapi.com/search?query=${encodeURIComponent(keyword + " in " + location)}&page=1&num_pages=1`,
      headers: { "X-RapidAPI-Key": process.env.RAPIDAPI_KEY }
    },
    {
      name: "serpapi",
      url: `https://serpapi.com/search.json?engine=google_jobs&q=${encodeURIComponent(keyword + " " + location)}&api_key=${process.env.SERPAPI_KEY}`,
      headers: {}
    }
  ];

  for (const endpoint of apiEndpoints) {
    if (!process.env.RAPIDAPI_KEY && endpoint.name === "jsearch") continue;
    if (!process.env.SERPAPI_KEY && endpoint.name === "serpapi") continue;

    try {
      await gaussianDelay(1000, 2000);
      const response = await stealthFetch(endpoint.url, { 
        maxRetries: 1,
        headers: endpoint.headers 
      });
      
      const data = response.data;
      let jobs = [];
      
      if (endpoint.name === "jsearch" && data.data) {
        jobs = data.data.map(j => mapJob({
          id: j.job_id,
          title: j.job_title,
          company: j.employer_name,
          location: j.job_city || location,
          url: j.job_apply_link || j.job_google_link,
          postedDate: j.job_posted_at_datetime_utc,
          excerpt: j.job_description?.substring(0, 240) || ""
        }));
      } else if (endpoint.name === "serpapi" && data.jobs_results) {
        jobs = data.jobs_results.map(j => mapJob({
          id: j.job_id,
          title: j.title,
          company: j.company_name,
          location: j.location || location,
          url: j.share_link,
          postedDate: j.date_posted,
          excerpt: j.description?.substring(0, 240) || ""
        }));
      }
      
      if (jobs.length > 0) {
        console.log(`[Indeed] API fallback ${endpoint.name}: ${jobs.length} jobs`);
        return jobs;
      }
    } catch (e) {
      console.warn(`[Indeed] API ${endpoint.name} failed:`, e.message);
    }
  }
  
  return [];
}

/**
 * Scrape Indeed jobs with advanced filtering
 * @param {Object} options - Search options
 */
export async function scrapeIndeedJobs(options = {}) {
  const {
    keyword = "software engineer",
    location = "Toronto, ON",
    start = 0,
    maxPages = 3,
    useFallbackApi = true,
    dateFilter = "week",  // 24h, 3d, week, 14d, month, any
    jobType = null        // full-time, part-time, contract, etc.
  } = options;
  
  console.log(`[Indeed] Starting scrape for "${keyword}" in "${location}" (date: ${dateFilter})`);
  
  const results = [];

  // Try RSS feed first (most reliable when available)
  try {
    const rssJobs = await scrapeIndeedRss({ keyword, location, dateFilter });
    results.push(...rssJobs);
    if (rssJobs.length > 0) {
      console.log(`[Indeed] RSS feed returned ${rssJobs.length} jobs`);
    }
  } catch (e) { 
    console.error("[Indeed] RSS failed:", e.message); 
  }

  // Try HTML scraping if RSS didn't return enough
  if (results.length < 10) {
    for (let i = 0; i < maxPages; i++) {
      const offset = start + i * 10;
      try {
        if (i > 0) await gaussianDelay(4000, 8000); // Longer delays to avoid detection
        const htmlJobs = await scrapeIndeedHtml({ 
          keyword, 
          location, 
          start: offset, 
          domainIndex: i,
          dateFilter,
          jobType
        });
        results.push(...htmlJobs);
        
        // Stop if we got some results and have enough
        if (htmlJobs.length > 0 && results.length >= 20) {
          console.log(`[Indeed] Got ${results.length} total jobs, stopping pagination`);
          break;
        }
      } catch (e) { 
        console.error(`[Indeed] Page ${i} failed:`, e.message); 
      }
    }
  }

  const uniqueJobs = mergeUnique(results);
  console.log(`[Indeed] Total unique jobs: ${uniqueJobs.length}`);
  
  // Try fallback APIs if no results
  if (useFallbackApi && uniqueJobs.length === 0) {
    console.log("[Indeed] All scraping methods failed, trying fallback APIs...");
    const apiJobs = await fallbackApiScrape({ keyword, location });
    uniqueJobs.push(...apiJobs);
  }

  return uniqueJobs;
}

/**
 * Scrape Indeed for multiple keywords at once
 * @param {Object} options - Search options
 */
export async function scrapeIndeedMultiKeyword(options = {}) {
  const {
    keywords = DEFAULT_KEYWORDS,
    location = "Toronto, ON",
    dateFilter = "week",
    jobType = "full-time",
    maxJobsPerKeyword = 20
  } = options;
  
  console.log(`[Indeed] Multi-keyword scrape: ${keywords.length} keywords`);
  
  const allJobs = [];
  
  for (const keyword of keywords) {
    try {
      await gaussianDelay(5000, 10000); // Longer delay between keyword searches
      const jobs = await scrapeIndeedJobs({
        keyword,
        location,
        dateFilter,
        jobType,
        maxPages: 1, // Single page per keyword
        useFallbackApi: false
      });
      
      const limited = jobs.slice(0, maxJobsPerKeyword);
      allJobs.push(...limited);
      console.log(`[Indeed] "${keyword}": ${limited.length} jobs`);
    } catch (error) {
      console.error(`[Indeed] Keyword "${keyword}" failed:`, error.message);
    }
  }
  
  return mergeUnique(allJobs);
}

// Export filter constants for use by other modules
export { DATE_FILTERS, JOB_TYPE_FILTERS, EXPERIENCE_FILTERS, DEFAULT_KEYWORDS };

export default {
  scrapeIndeedJobs,
  scrapeIndeedMultiKeyword,
  DATE_FILTERS,
  DEFAULT_KEYWORDS
};