#!/usr/bin/env node
/**
 * Alternative Indeed Scraper - Using aggregators and alternative sources
 */

import axios from "axios";
import * as cheerio from "cheerio";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const HEADERS = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
};

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
// APPROACH 1: Jooble API (Free aggregator)
// ============================================
async function scrapeJooble(keyword, location) {
  log(`[Jooble] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  
  try {
    await sleep(randomDelay(1000, 2000));
    
    // Jooble has a public endpoint
    const response = await axios.post(
      "https://jooble.org/api/",
      {
        keywords: keyword,
        location: location,
        page: 1
      },
      {
        headers: {
          ...HEADERS,
          "content-type": "application/json"
        },
        timeout: 15000
      }
    );
    
    const data = response.data;
    if (data.jobs && Array.isArray(data.jobs)) {
      data.jobs.forEach(j => {
        jobs.push({
          title: normalizeText(j.title),
          company: normalizeText(j.company),
          location: normalizeText(j.location) || location,
          url: j.link,
          source: "jooble",
          id: `jooble:${j.id || j.link}`,
          postedDate: j.updated ? new Date(j.updated).toISOString() : null,
          excerpt: j.snippet?.substring(0, 240),
          scrapedAt: new Date().toISOString()
        });
      });
    }
    
    log(`[Jooble] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[Jooble] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// APPROACH 2: SimplyHired (Indeed sister site)
// ============================================
async function scrapeSimplyHired(keyword, location) {
  log(`[SimplyHired] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const params = new URLSearchParams({
    q: keyword,
    l: location,
    pn: "1"
  });
  
  const url = `https://www.simplyhired.ca/search?${params}`;
  
  try {
    await sleep(randomDelay(2000, 4000));
    
    const response = await axios.get(url, {
      headers: HEADERS,
      timeout: 30000
    });
    
    const $ = cheerio.load(response.data);
    
    $(".SerpJob, .jobposting, [data-jobkey]").each((_, el) => {
      const $el = $(el);
      const title = normalizeText($el.find("h2, .jobposting-title, [data-testid='job-title']").text());
      let link = $el.find("a").attr("href");
      
      if (title && link) {
        if (!link.startsWith("http")) {
          link = `https://www.simplyhired.ca${link}`;
        }
        
        jobs.push({
          title,
          company: normalizeText($el.find(".jobposting-company, [data-testid='company']").text()),
          location: normalizeText($el.find(".jobposting-location, [data-testid='location']").text()) || location,
          url: link,
          source: "simplyhired",
          id: `simplyhired:${link}`,
          scrapedAt: new Date().toISOString()
        });
      }
    });
    
    log(`[SimplyHired] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[SimplyHired] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// APPROACH 3: Talent.com (formerly Neuvoo)
// ============================================
async function scrapeTalent(keyword, location) {
  log(`[Talent.com] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const params = new URLSearchParams({
    k: keyword,
    l: location
  });
  
  const url = `https://www.talent.com/jobs?${params}`;
  
  try {
    await sleep(randomDelay(2000, 4000));
    
    const response = await axios.get(url, {
      headers: HEADERS,
      timeout: 30000
    });
    
    const $ = cheerio.load(response.data);
    
    $(".card--job, .job-card, [data-cy='job-card']").each((_, el) => {
      const $el = $(el);
      const title = normalizeText($el.find("h2, .card__job-title, [data-cy='job-title']").text());
      let link = $el.find("a").attr("href");
      
      if (title && link) {
        if (!link.startsWith("http")) {
          link = `https://www.talent.com${link}`;
        }
        
        jobs.push({
          title,
          company: normalizeText($el.find(".card__job-empname, [data-cy='company-name']").text()),
          location: normalizeText($el.find(".card__job-location, [data-cy='location']").text()) || location,
          url: link,
          source: "talent",
          id: `talent:${link}`,
          scrapedAt: new Date().toISOString()
        });
      }
    });
    
    log(`[Talent.com] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[Talent.com] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// APPROACH 4: CareerBuilder
// ============================================
async function scrapeCareerBuilder(keyword, location) {
  log(`[CareerBuilder] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const params = new URLSearchParams({
    keywords: keyword,
    location: location
  });
  
  const url = `https://www.careerbuilder.ca/jobs?${params}`;
  
  try {
    await sleep(randomDelay(2000, 4000));
    
    const response = await axios.get(url, {
      headers: HEADERS,
      timeout: 30000
    });
    
    const $ = cheerio.load(response.data);
    
    $(".data-results-content, .job-listing-item").each((_, el) => {
      const $el = $(el);
      const title = normalizeText($el.find("h2, .data-results-title").text());
      let link = $el.find("a").attr("href");
      
      if (title && link) {
        if (!link.startsWith("http")) {
          link = `https://www.careerbuilder.ca${link}`;
        }
        
        jobs.push({
          title,
          company: normalizeText($el.find(".data-details, .company-name").text()),
          location: normalizeText($el.find(".data-results-location").text()) || location,
          url: link,
          source: "careerbuilder",
          id: `careerbuilder:${link}`,
          scrapedAt: new Date().toISOString()
        });
      }
    });
    
    log(`[CareerBuilder] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[CareerBuilder] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// APPROACH 5: ZipRecruiter
// ============================================
async function scrapeZipRecruiter(keyword, location) {
  log(`[ZipRecruiter] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const params = new URLSearchParams({
    search: keyword,
    location: location
  });
  
  const url = `https://www.ziprecruiter.com/jobs-search?${params}`;
  
  try {
    await sleep(randomDelay(2000, 4000));
    
    const response = await axios.get(url, {
      headers: {
        ...HEADERS,
        "referer": "https://www.google.com/"
      },
      timeout: 30000
    });
    
    const $ = cheerio.load(response.data);
    
    $(".job_result, .job-listing, [data-testid='job-listing']").each((_, el) => {
      const $el = $(el);
      const title = normalizeText($el.find("h2, .job_title, .job-title").text());
      let link = $el.find("a").attr("href");
      
      if (title && link) {
        if (!link.startsWith("http")) {
          link = `https://www.ziprecruiter.com${link}`;
        }
        
        jobs.push({
          title,
          company: normalizeText($el.find(".t_org_link, .company-name").text()),
          location: normalizeText($el.find(".location, .job-location").text()) || location,
          url: link,
          source: "ziprecruiter",
          id: `ziprecruiter:${link}`,
          scrapedAt: new Date().toISOString()
        });
      }
    });
    
    log(`[ZipRecruiter] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[ZipRecruiter] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// APPROACH 6: Indeed via mobile site (different protection)
// ============================================
async function scrapeIndeedMobile(keyword, location) {
  log(`[Indeed Mobile] Trying: "${keyword}" in ${location}`);
  
  const jobs = [];
  const params = new URLSearchParams({
    q: keyword,
    l: location,
    fromage: "7"
  });
  
  const url = `https://m.indeed.com/jobs?${params}`;
  
  try {
    await sleep(randomDelay(3000, 5000));
    
    const response = await axios.get(url, {
      headers: {
        ...HEADERS,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
      },
      timeout: 30000
    });
    
    // Check if blocked
    if (response.data.includes("unusual traffic") || response.data.includes("captcha")) {
      log(`[Indeed Mobile] Blocked`);
      return [];
    }
    
    const $ = cheerio.load(response.data);
    
    $(".tapItem, .jobsearch-SerpJobCard, [data-jk]").each((_, el) => {
      const $el = $(el);
      const title = normalizeText($el.find("h2, .jobTitle").text());
      let link = $el.attr("href") || $el.find("a").attr("href");
      
      if (title && link) {
        if (!link.startsWith("http")) {
          link = `https://m.indeed.com${link}`;
        }
        
        jobs.push({
          title,
          company: normalizeText($el.find(".companyName").text()),
          location: normalizeText($el.find(".companyLocation").text()) || location,
          url: link,
          source: "indeed",
          id: `indeed:${link}`,
          scrapedAt: new Date().toISOString()
        });
      }
    });
    
    log(`[Indeed Mobile] Found ${jobs.length} jobs`);
    return jobs;
  } catch (error) {
    log(`[Indeed Mobile] Failed: ${error.message}`);
    return [];
  }
}

// ============================================
// MAIN
// ============================================
async function main() {
  console.log("╔══════════════════════════════════════════════════════════╗");
  console.log("║  ALTERNATIVE JOB SCRAPER - Aggregators & Other Sources   ║");
  console.log("╚══════════════════════════════════════════════════════════╝\n");
  
  const keywords = [
    "ServiceNow developer",
    "VBA developer",
    "Alteryx",
    "full stack developer",
    "software engineer",
    "data analyst",
    "DevOps engineer",
    "Python developer"
  ];
  
  const location = "Toronto, ON";
  const allJobs = [];
  const seenUrls = new Set();
  
  function addJobs(newJobs) {
    for (const job of newJobs) {
      const key = job.url || job.title + job.company;
      if (key && !seenUrls.has(key)) {
        seenUrls.add(key);
        allJobs.push(job);
      }
    }
  }
  
  for (const keyword of keywords) {
    log(`\n=== Keyword: ${keyword} ===`);
    
    // Try each source
    const sources = [
      () => scrapeJooble(keyword, location),
      () => scrapeSimplyHired(keyword, location),
      () => scrapeTalent(keyword, location),
      () => scrapeCareerBuilder(keyword, location),
      () => scrapeZipRecruiter(keyword, location),
      () => scrapeIndeedMobile(keyword, location)
    ];
    
    for (const scraper of sources) {
      try {
        const jobs = await scraper();
        addJobs(jobs);
      } catch (error) {
        log(`Error: ${error.message}`);
      }
      
      await sleep(randomDelay(2000, 4000));
    }
    
    log(`Total unique jobs: ${allJobs.length}`);
  }
  
  console.log("\n" + "═".repeat(60));
  console.log(`SCRAPE COMPLETE: ${allJobs.length} total jobs`);
  console.log("═".repeat(60));
  
  // Count by source
  const bySrc = {};
  allJobs.forEach(j => { bySrc[j.source] = (bySrc[j.source] || 0) + 1; });
  console.log("\nBy source:");
  Object.entries(bySrc).sort((a,b) => b[1] - a[1]).forEach(([s, c]) => {
    console.log(`  ${s}: ${c}`);
  });
  
  if (allJobs.length > 0) {
    // Merge with existing
    const existingPath = path.join(__dirname, "..", "jobs.json");
    let existingData = { meta: {}, jobs: [] };
    try {
      existingData = JSON.parse(fs.readFileSync(existingPath, "utf-8"));
    } catch {}
    
    const existingIds = new Set(existingData.jobs.map(j => j.id));
    const newJobs = allJobs.filter(j => !existingIds.has(j.id));
    
    console.log(`\nNew jobs to add: ${newJobs.length}`);
    
    if (newJobs.length > 0) {
      existingData.jobs.push(...newJobs);
      existingData.meta = {
        ...existingData.meta,
        lastAlternativeScrape: new Date().toISOString(),
        totalJobs: existingData.jobs.length
      };
      
      fs.writeFileSync(existingPath, JSON.stringify(existingData, null, 2));
      log(`Saved ${existingData.jobs.length} total jobs`);
      
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
    }
    
    // Sample jobs
    console.log("\n--- Sample Jobs ---");
    allJobs.slice(0, 5).forEach((j, i) => {
      console.log(`${i + 1}. [${j.source}] ${j.title}`);
      console.log(`   ${j.company || "N/A"} - ${j.location}`);
    });
  }
}

main().catch(console.error);
