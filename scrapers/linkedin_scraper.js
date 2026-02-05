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

  return null;
}

const LINKEDIN_ENDPOINTS = [
  { domain: "www.linkedin.com", type: "main" },
  { domain: "www.linkedin.com", type: "guest" },
  { domain: "linkedin.com", type: "lite" }
];

function buildSearchUrl({ keyword, location, start = 0, endpoint = null }) {
  const target = endpoint || LINKEDIN_ENDPOINTS[0];
  const params = new URLSearchParams({
    keywords: keyword,
    location,
    start: String(start)
  });
  
  if (target.type === "guest") {
    return `https://${target.domain}/jobs-guest/jobs/api/seeMoreJobPostings/search?${params.toString()}`;
  }
  return `https://${target.domain}/jobs/search/?${params.toString()}`;
}

function buildGuestSearchUrl({ keyword, location, start = 0, domain = "www.linkedin.com" }) {
  const params = new URLSearchParams({
    keywords: keyword,
    location,
    start: String(start)
  });
  return `https://${domain}/jobs-guest/jobs/api/seeMoreJobPostings/search?${params.toString()}`;
}

function mapJob({ title, url, company, location, postedDate, excerpt }) {
  return {
    title,
    url,
    company: normalizeText(company),
    location: normalizeText(location),
    postedDate: postedDate ? postedDate.toISOString() : null,
    excerpt: normalizeText(excerpt || "")
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

async function scrapeLinkedInHtml({ keyword, location, start = 0, endpointIndex = 0 }) {
  const endpoint = LINKEDIN_ENDPOINTS[endpointIndex % LINKEDIN_ENDPOINTS.length];
  const url = buildSearchUrl({ keyword, location, start, endpoint });
  
  try {
    const response = await fetchWithRetry(url, {
      maxRetries: 2,
      baseDelay: 3000,
      strategicDelay: 2000,
      useProxy: true,
      fallbackProxies: true
    });
    return extractJobsFromHtml(response.data);
  } catch (error) {
    console.warn(`[LinkedIn] Endpoint ${endpoint.domain}/${endpoint.type} failed:`, error.message);
    throw error;
  }
}

async function scrapeLinkedInGuest({ keyword, location, start = 0, domainIndex = 0 }) {
  const domains = ["www.linkedin.com", "linkedin.com"];
  const domain = domains[domainIndex % domains.length];
  const url = buildGuestSearchUrl({ keyword, location, start, domain });
  
  try {
    const response = await fetchWithRetry(url, {
      maxRetries: 2,
      baseDelay: 3000,
      strategicDelay: 1500,
      useProxy: true,
      fallbackProxies: true
    });
    return extractJobsFromHtml(response.data);
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

export async function scrapeLinkedInJobs(keyword, location, start = 0, maxPages = 3, useFallbackApi = true) {
  const results = [];
  const pages = Number.isFinite(maxPages) && maxPages > 0 ? maxPages : 1;

  for (let pageIndex = 0; pageIndex < pages; pageIndex += 1) {
    const offset = start + pageIndex * 25;
    
    try {
      await strategicDelay(1500, 3500);
      const htmlJobs = await scrapeLinkedInHtml({ keyword, location, start: offset, endpointIndex: pageIndex });
      results.push(...htmlJobs);
    } catch (error) {
      console.error("LinkedIn HTML scrape failed:", error?.message || error);
    }

    try {
      await strategicDelay(2500, 5000);
      const guestJobs = await scrapeLinkedInGuest({ keyword, location, start: offset, domainIndex: pageIndex });
      results.push(...guestJobs);
    } catch (error) {
      console.error("LinkedIn guest scrape failed:", error?.message || error);
    }
  }
  
  const uniqueResults = mergeUnique(results);
  
  if (useFallbackApi && uniqueResults.length === 0) {
    console.log("[LinkedIn] All scraping methods failed, trying fallback APIs...");
    const apiJobs = await fallbackLinkedInApi({ keyword, location });
    uniqueResults.push(...apiJobs);
  }

  return uniqueResults;
}