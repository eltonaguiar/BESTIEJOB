import * as cheerio from "cheerio";
import Parser from "rss-parser";
import { stealthFetch, scrapeWithBrowser, isBlocked, gaussianDelay } from "./utils/stealth_browser.js";

const rssParser = new Parser({
  headers: {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0.4"
  }
});

function normalizeText(value) {
  return (value ?? "").toString().replace(/\s+/g, " ").trim();
}

function parseRelativeDate(text) {
  const t = normalizeText(text).toLowerCase();
  if (!t) return null;
  if (t.includes("just posted") || t.includes("today")) return new Date();

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

const DOMAINS = [
  "ca.indeed.com",
  "www.indeed.com",
  "uk.indeed.com",
  "au.indeed.com"
];

let domainRotationIndex = 0;

function getNextDomain() {
  const domain = DOMAINS[domainRotationIndex % DOMAINS.length];
  domainRotationIndex++;
  return domain;
}

function toIndeedSearchUrl({ keyword, location, start = 0, domain = null }) {
  const params = new URLSearchParams({
    q: keyword,
    l: location,
    start: String(start),
    fromage: "7",
    sort: "date"
  });
  const targetDomain = domain || getNextDomain();
  return `https://${targetDomain}/jobs?${params.toString()}`;
}

function mapJob(job) {
  return {
    ...job,
    source: "indeed",
    id: job.id || `indeed:${job.url || job.title}`
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

async function scrapeIndeedHtml({ keyword, location, start = 0, domainIndex = 0 }) {
  const domain = DOMAINS[domainIndex % DOMAINS.length];
  const url = toIndeedSearchUrl({ keyword, location, start, domain });
  
  try {
    const response = await stealthFetch(url, { maxRetries: 2 });
    
    if (isBlocked(response.data)) {
      throw new Error("Blocked by anti-bot");
    }
    
    return extractJobsFromHtml(response.data);
  } catch (error) {
    console.log(`[Indeed] Domain ${domain} failed, trying browser: ${error.message}`);
    
    await gaussianDelay(3000, 6000);
    const html = await scrapeWithBrowser(url);
    return extractJobsFromHtml(html);
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

async function scrapeIndeedRss({ keyword, location }) {
  const q = encodeURIComponent(keyword);
  const l = encodeURIComponent(location);
  
  const endpoints = [
    `https://ca.indeed.com/rss?q=${q}&l=${l}&sort=date&fromage=7`,
    `https://rss.indeed.com/rss?q=${q}&l=${l}`,
    `https://www.indeed.com/rss?q=${q}&l=${l}`
  ];
  
  for (const url of endpoints) {
    try {
      await gaussianDelay(1000, 2000);
      const feed = await rssParser.parseURL(url);
      const items = Array.isArray(feed?.items) ? feed.items : [];
      if (items.length > 0) {
        console.log(`[Indeed] RSS: ${items.length} jobs from ${url}`);
        return items.map((it) => mapJob({
          title: normalizeText(it.title?.replace(/ - job post$/, "")),
          company: normalizeText(it.creator || it.author),
          location,
          url: normalizeText(it.link),
          postedDate: it.pubDate ? new Date(it.pubDate).toISOString() : null,
          excerpt: (it.contentSnippet || "").slice(0, 240)
        }));
      }
    } catch {}
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

export async function scrapeIndeedJobs({ keyword, location, start = 0, maxPages = 3, useFallbackApi = true }) {
  const results = [];

  try {
    const rssJobs = await scrapeIndeedRss({ keyword, location });
    results.push(...rssJobs);
  } catch (e) { console.error("[Indeed] RSS failed:", e.message); }

  for (let i = 0; i < maxPages; i++) {
    const offset = start + i * 10;
    try {
      if (i > 0) await gaussianDelay(3000, 6000);
      const htmlJobs = await scrapeIndeedHtml({ keyword, location, start: offset, domainIndex: i });
      results.push(...htmlJobs);
      if (htmlJobs.length > 0) break;
    } catch (e) { console.error(`[Indeed] Page ${i} failed:`, e.message); }
  }

  const uniqueJobs = mergeUnique(results);
  
  if (useFallbackApi && uniqueJobs.length === 0) {
    console.log("[Indeed] All scraping methods failed, trying fallback APIs...");
    const apiJobs = await fallbackApiScrape({ keyword, location });
    uniqueJobs.push(...apiJobs);
  }

  return uniqueJobs;
}

export default {
  scrapeIndeedJobs
};