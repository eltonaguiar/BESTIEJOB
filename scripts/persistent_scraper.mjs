#!/usr/bin/env node
/**
 * Persistent Job Scraper - Multiple approaches to get LinkedIn/Indeed jobs
 * Tries various methods until one works
 */

import axios from "axios";
import * as cheerio from "cheerio";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Stealth headers
const STEALTH_HEADERS = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
  "accept-encoding": "gzip, deflate, br",
  "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
  "cache-control": "no-cache",
  "pragma": "no-cache",
  "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": '"Windows"',
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "none",
  "sec-fetch-user": "?1",
  "upgrade-insecure-requests": "1",
  "dnt": "1"
};

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

function getRandomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function randomDelay(min, max) {
  return Math.floor(Math.random() * (max - min) + min);
}

function log(msg) {
  console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
}

function normalizeText(value) {
  return (value ?? "").toString().replace(/\s+/g, " ").trim();
}

// ============================================
// APPROACH 1: LinkedIn Guest Jobs API (Public)
// ============================================
async function scrapeLinkedInGuest(keyword, location) {
  log(`[LinkedIn Guest] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const params = new URLSearchParams({
    keywords: keyword,
    location: location,
    f_TPR: "r604800", // Past week
    sortBy: "DD",
    start: "0"
  });
  
  const url = `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?${params}`;
  
  try {
    await sleep(randomDelay(2000, 4000));
    
    const response = await axios.get(url, {
      headers: {
        ...STEALTH_HEADERS,
        "user-agent": getRandomUA(),
        "referer": "https://www.google.com/",
        "origin": "https://www.linkedin.com"
      },
      timeout: 30000
    });
    
    const $ = cheerio.load(response.data);
    
    $(".job-search-card, .base-card, .jobs-search__results-list li").each((_, el) => {
      const title = normalizeText($(el).find(".base-search-card__title, h3").text());
      const company = normalizeText($(el).find(".base-search-card__subtitle, h4").text());
      const loc = normalizeText($(el).find(".job-search-card__location").text());
      const link = $(el).find("a.base-card__full-link").attr("href");
      
      if (title && link) {
        jobs.push({
          title,
          company,
          location: loc || location,
          url: link.split("?")[0],
          source: "linkedin",
          id: `linkedin:${link.split("?")[0]}`,
          scrapedAt: new Date().toISOString()
        });
      }
    });
    
    log(`[LinkedIn Guest] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[LinkedIn Guest] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// APPROACH 2: LinkedIn Jobs Search Page (HTML)
// ============================================
async function scrapeLinkedInSearch(keyword, location) {
  log(`[LinkedIn Search] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const params = new URLSearchParams({
    keywords: keyword,
    location: location,
    f_TPR: "r604800",
    sortBy: "DD"
  });
  
  const url = `https://www.linkedin.com/jobs/search/?${params}`;
  
  try {
    await sleep(randomDelay(3000, 5000));
    
    const response = await axios.get(url, {
      headers: {
        ...STEALTH_HEADERS,
        "user-agent": getRandomUA(),
        "referer": "https://www.google.com/"
      },
      timeout: 30000,
      maxRedirects: 5
    });
    
    const $ = cheerio.load(response.data);
    
    // Try multiple selectors
    const selectors = [
      ".jobs-search__results-list li",
      ".job-search-card",
      "[data-entity-urn*='jobPosting']",
      ".base-card"
    ];
    
    for (const selector of selectors) {
      $(selector).each((_, el) => {
        const title = normalizeText($(el).find("h3, .base-search-card__title").text());
        const company = normalizeText($(el).find("h4, .base-search-card__subtitle").text());
        const link = $(el).find("a").attr("href");
        
        if (title && link && link.includes("linkedin")) {
          jobs.push({
            title,
            company,
            location,
            url: link.split("?")[0],
            source: "linkedin",
            id: `linkedin:${link}`,
            scrapedAt: new Date().toISOString()
          });
        }
      });
      
      if (jobs.length > 0) break;
    }
    
    // Try embedded JSON data
    $("script[type='application/ld+json']").each((_, el) => {
      try {
        const data = JSON.parse($(el).html());
        if (data["@type"] === "JobPosting") {
          jobs.push({
            title: data.title,
            company: data.hiringOrganization?.name || "",
            location: data.jobLocation?.address?.addressLocality || location,
            url: data.url,
            source: "linkedin",
            id: `linkedin:${data.identifier?.value || data.url}`,
            postedDate: data.datePosted,
            scrapedAt: new Date().toISOString()
          });
        }
      } catch {}
    });
    
    log(`[LinkedIn Search] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[LinkedIn Search] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// APPROACH 3: Google Jobs (indexes LinkedIn/Indeed)
// ============================================
async function scrapeGoogleJobs(keyword, location) {
  log(`[Google Jobs] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const query = encodeURIComponent(`${keyword} jobs ${location}`);
  const url = `https://www.google.com/search?q=${query}&ibp=htl;jobs`;
  
  try {
    await sleep(randomDelay(2000, 4000));
    
    const response = await axios.get(url, {
      headers: {
        ...STEALTH_HEADERS,
        "user-agent": getRandomUA(),
        "referer": "https://www.google.com/"
      },
      timeout: 30000
    });
    
    const $ = cheerio.load(response.data);
    
    // Google Jobs embeds data in script tags
    $("script").each((_, el) => {
      const text = $(el).html() || "";
      if (text.includes("JobPosting") || text.includes("htititle")) {
        try {
          // Extract job data from Google's embedded JSON
          const matches = text.match(/"htititle":"([^"]+)"/g) || [];
          matches.forEach(match => {
            const title = match.replace(/"htititle":"/, "").replace(/"$/, "");
            if (title) {
              jobs.push({
                title: normalizeText(title),
                company: "",
                location,
                url: `https://www.google.com/search?q=${encodeURIComponent(title + " " + location)}&ibp=htl;jobs`,
                source: "google_jobs",
                id: `google:${title}`,
                scrapedAt: new Date().toISOString()
              });
            }
          });
        } catch {}
      }
    });
    
    log(`[Google Jobs] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[Google Jobs] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// APPROACH 4: Indeed RSS Feeds (Multiple domains)
// ============================================
async function scrapeIndeedRSS(keyword, location) {
  log(`[Indeed RSS] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const q = encodeURIComponent(keyword);
  const l = encodeURIComponent(location);
  
  const feeds = [
    `https://ca.indeed.com/rss?q=${q}&l=${l}&sort=date&fromage=7`,
    `https://www.indeed.com/rss?q=${q}&l=${l}&sort=date&fromage=7`,
    `https://ca.indeed.com/rss?q=${q}&l=${l}`,
    `https://rss.indeed.com/rss?q=${q}&l=${l}`
  ];
  
  for (const feedUrl of feeds) {
    try {
      await sleep(randomDelay(1000, 2000));
      
      const response = await axios.get(feedUrl, {
        headers: {
          "user-agent": "Mozilla/5.0 (compatible; RSS Reader)",
          "accept": "application/rss+xml, application/xml, text/xml"
        },
        timeout: 15000
      });
      
      const $ = cheerio.load(response.data, { xmlMode: true });
      
      $("item").each((_, el) => {
        const title = normalizeText($(el).find("title").text());
        const link = normalizeText($(el).find("link").text());
        const pubDate = $(el).find("pubDate").text();
        const description = $(el).find("description").text();
        
        if (title && link) {
          jobs.push({
            title: title.replace(/ - job post$/, ""),
            company: "",
            location,
            url: link,
            source: "indeed",
            id: `indeed:${link}`,
            postedDate: pubDate ? new Date(pubDate).toISOString() : null,
            excerpt: description?.substring(0, 240),
            scrapedAt: new Date().toISOString()
          });
        }
      });
      
      if (jobs.length > 0) {
        log(`[Indeed RSS] Found ${jobs.length} jobs from ${feedUrl}`);
        return jobs;
      }
    } catch (error) {
      log(`[Indeed RSS] ${feedUrl.split("/")[2]} failed: ${error.message}`);
    }
  }
  
  return jobs;
}

// ============================================
// APPROACH 5: Indeed HTML Scrape with rotation
// ============================================
async function scrapeIndeedHTML(keyword, location) {
  log(`[Indeed HTML] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const domains = ["ca.indeed.com", "www.indeed.com"];
  
  for (const domain of domains) {
    const params = new URLSearchParams({
      q: keyword,
      l: location,
      fromage: "7",
      sort: "date"
    });
    
    const url = `https://${domain}/jobs?${params}`;
    
    try {
      await sleep(randomDelay(3000, 6000));
      
      const response = await axios.get(url, {
        headers: {
          ...STEALTH_HEADERS,
          "user-agent": getRandomUA(),
          "referer": "https://www.google.com/"
        },
        timeout: 30000
      });
      
      // Check if blocked
      if (response.data.includes("unusual traffic") || 
          response.data.includes("captcha") ||
          response.data.length < 5000) {
        log(`[Indeed HTML] ${domain} blocked`);
        continue;
      }
      
      const $ = cheerio.load(response.data);
      
      // Multiple selectors for Indeed's changing structure
      const selectors = [
        "a[data-jk]",
        ".jobsearch-ResultsList li",
        ".job_seen_beacon",
        "[data-testid='jobListing']"
      ];
      
      for (const selector of selectors) {
        $(selector).each((_, el) => {
          const $el = $(el);
          const title = normalizeText(
            $el.find("h2.jobTitle span, .jobTitle span, [data-testid='job-title']").text() ||
            $el.find("a").attr("title") ||
            $el.find("h2").text()
          );
          
          let link = $el.attr("href") || $el.find("a").first().attr("href");
          if (link && !link.startsWith("http")) {
            link = `https://${domain}${link}`;
          }
          
          if (title && link) {
            const company = normalizeText($el.find(".companyName, [data-testid='company-name']").text());
            const loc = normalizeText($el.find(".companyLocation, [data-testid='job-location']").text());
            
            jobs.push({
              title,
              company,
              location: loc || location,
              url: link,
              source: "indeed",
              id: `indeed:${link}`,
              scrapedAt: new Date().toISOString()
            });
          }
        });
        
        if (jobs.length > 0) break;
      }
      
      // Try embedded JSON
      $("script").each((_, el) => {
        const text = $(el).html() || "";
        if (text.includes("window._initialData") || text.includes("mosaic-provider")) {
          try {
            const match = text.match(/window\._initialData\s*=\s*({.+?});/);
            if (match) {
              const data = JSON.parse(match[1]);
              const results = data?.jobSearch?.results || [];
              results.forEach(j => {
                if (j.title) {
                  jobs.push({
                    title: j.title,
                    company: j.company?.name || "",
                    location: j.formattedLocation || location,
                    url: `https://${domain}/viewjob?jk=${j.jobkey}`,
                    source: "indeed",
                    id: `indeed:${j.jobkey}`,
                    scrapedAt: new Date().toISOString()
                  });
                }
              });
            }
          } catch {}
        }
      });
      
      if (jobs.length > 0) {
        log(`[Indeed HTML] Found ${jobs.length} jobs from ${domain}`);
        return jobs;
      }
    } catch (error) {
      log(`[Indeed HTML] ${domain} failed: ${error.message}`);
    }
  }
  
  return jobs;
}

// ============================================
// APPROACH 6: Use Playwright for JS-rendered pages
// ============================================
async function scrapeWithBrowser(keyword, location, source = "linkedin") {
  log(`[Browser] Trying ${source}: "${keyword}"`);
  
  const jobs = [];
  
  try {
    const { chromium } = await import("playwright");
    
    const browser = await chromium.launch({
      headless: true,
      args: ["--no-sandbox", "--disable-setuid-sandbox"]
    });
    
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: getRandomUA()
    });
    
    // Bypass webdriver detection
    await context.addInitScript(() => {
      Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    });
    
    const page = await context.newPage();
    
    let url;
    if (source === "linkedin") {
      const params = new URLSearchParams({
        keywords: keyword,
        location: location,
        f_TPR: "r604800"
      });
      url = `https://www.linkedin.com/jobs/search/?${params}`;
    } else {
      const params = new URLSearchParams({
        q: keyword,
        l: location,
        fromage: "7"
      });
      url = `https://ca.indeed.com/jobs?${params}`;
    }
    
    await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
    await sleep(randomDelay(3000, 5000));
    
    // Scroll to trigger lazy loading
    await page.evaluate(() => window.scrollBy(0, 500));
    await sleep(1000);
    
    const content = await page.content();
    const $ = cheerio.load(content);
    
    if (source === "linkedin") {
      $(".job-search-card, .base-card").each((_, el) => {
        const title = normalizeText($(el).find(".base-search-card__title, h3").text());
        const company = normalizeText($(el).find(".base-search-card__subtitle, h4").text());
        const link = $(el).find("a").attr("href");
        
        if (title && link) {
          jobs.push({
            title,
            company,
            location,
            url: link.split("?")[0],
            source: "linkedin",
            id: `linkedin:${link}`,
            scrapedAt: new Date().toISOString()
          });
        }
      });
    } else {
      $("a[data-jk], .jobsearch-ResultsList li").each((_, el) => {
        const title = normalizeText($(el).find(".jobTitle span, h2 span").text());
        let link = $(el).attr("href") || $(el).find("a").attr("href");
        
        if (title && link) {
          if (!link.startsWith("http")) link = `https://ca.indeed.com${link}`;
          jobs.push({
            title,
            company: normalizeText($(el).find(".companyName").text()),
            location,
            url: link,
            source: "indeed",
            id: `indeed:${link}`,
            scrapedAt: new Date().toISOString()
          });
        }
      });
    }
    
    await browser.close();
    log(`[Browser] Found ${jobs.length} ${source} jobs`);
    return jobs;
  } catch (error) {
    log(`[Browser] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// MAIN: Try all approaches
// ============================================
async function scrapeAllApproaches(keywords, location) {
  const allJobs = [];
  const seenUrls = new Set();
  
  function addJobs(newJobs) {
    for (const job of newJobs) {
      const key = job.url || job.title;
      if (key && !seenUrls.has(key)) {
        seenUrls.add(key);
        allJobs.push(job);
      }
    }
  }
  
  for (const keyword of keywords) {
    log(`\n${"=".repeat(50)}`);
    log(`KEYWORD: ${keyword}`);
    log(`${"=".repeat(50)}`);
    
    // LinkedIn approaches
    let linkedinJobs = await scrapeLinkedInGuest(keyword, location);
    if (linkedinJobs.length === 0) {
      linkedinJobs = await scrapeLinkedInSearch(keyword, location);
    }
    if (linkedinJobs.length === 0) {
      linkedinJobs = await scrapeWithBrowser(keyword, location, "linkedin");
    }
    addJobs(linkedinJobs);
    
    await sleep(randomDelay(2000, 4000));
    
    // Indeed approaches
    let indeedJobs = await scrapeIndeedRSS(keyword, location);
    if (indeedJobs.length === 0) {
      indeedJobs = await scrapeIndeedHTML(keyword, location);
    }
    if (indeedJobs.length === 0) {
      indeedJobs = await scrapeWithBrowser(keyword, location, "indeed");
    }
    addJobs(indeedJobs);
    
    await sleep(randomDelay(2000, 4000));
    
    // Google Jobs (catches both)
    const googleJobs = await scrapeGoogleJobs(keyword, location);
    addJobs(googleJobs);
    
    log(`\nTotal unique jobs so far: ${allJobs.length}`);
    
    // Longer delay between keywords to avoid rate limiting
    await sleep(randomDelay(5000, 10000));
  }
  
  return allJobs;
}

// ============================================
// RUN
// ============================================
async function main() {
  console.log("╔══════════════════════════════════════════════════════════╗");
  console.log("║     PERSISTENT JOB SCRAPER - LinkedIn & Indeed           ║");
  console.log("╚══════════════════════════════════════════════════════════╝\n");
  
  const keywords = [
    "ServiceNow developer",
    "VBA developer",
    "Alteryx",
    "full stack developer",
    "software engineer"
  ];
  
  const location = "Toronto, ON";
  
  log(`Starting scrape for ${keywords.length} keywords in ${location}\n`);
  
  const jobs = await scrapeAllApproaches(keywords, location);
  
  console.log("\n" + "═".repeat(60));
  console.log(`SCRAPE COMPLETE: ${jobs.length} total unique jobs`);
  console.log("═".repeat(60));
  
  // Count by source
  const bySrc = {};
  jobs.forEach(j => { bySrc[j.source] = (bySrc[j.source] || 0) + 1; });
  console.log("\nBy source:");
  Object.entries(bySrc).sort((a,b) => b[1] - a[1]).forEach(([s, c]) => {
    console.log(`  ${s}: ${c}`);
  });
  
  // Merge with existing jobs
  const existingPath = path.join(__dirname, "..", "jobs.json");
  let existingData = { jobs: [] };
  try {
    existingData = JSON.parse(fs.readFileSync(existingPath, "utf-8"));
  } catch {}
  
  const existingIds = new Set(existingData.jobs.map(j => j.id));
  const newJobs = jobs.filter(j => !existingIds.has(j.id));
  
  console.log(`\nNew jobs to add: ${newJobs.length}`);
  
  if (newJobs.length > 0) {
    existingData.jobs.push(...newJobs);
    existingData.meta = {
      ...existingData.meta,
      lastScrape: new Date().toISOString(),
      totalJobs: existingData.jobs.length
    };
    
    fs.writeFileSync(existingPath, JSON.stringify(existingData, null, 2));
    log(`Saved ${existingData.jobs.length} total jobs to jobs.json`);
    
    // Copy to public folders
    const publicPaths = [
      path.join(__dirname, "..", "public", "jobs.json"),
      path.join(__dirname, "..", "public", "findjobs", "jobs.json"),
      path.join(__dirname, "..", "public", "gotjob", "jobs.json")
    ];
    
    for (const p of publicPaths) {
      try {
        fs.writeFileSync(p, JSON.stringify(existingData, null, 2));
      } catch {}
    }
    
    log("Copied to public folders");
  }
  
  // Show sample jobs
  if (jobs.length > 0) {
    console.log("\n--- Sample Jobs Found ---");
    jobs.slice(0, 5).forEach((j, i) => {
      console.log(`${i + 1}. [${j.source}] ${j.title}`);
      console.log(`   ${j.company || "No company"} - ${j.location}`);
      console.log(`   ${j.url?.substring(0, 60)}...`);
    });
  }
}

main().catch(console.error);
