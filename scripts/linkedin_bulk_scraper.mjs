#!/usr/bin/env node
/**
 * LinkedIn Bulk Scraper - Using the Guest API that works
 */

import axios from "axios";
import * as cheerio from "cheerio";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Inline relative date parser (to avoid module issues)
function parseRelativeDate(dateText) {
  if (!dateText) return null;
  
  const text = dateText.toLowerCase().trim();
  const now = new Date();
  
  // ISO date format
  if (/^\d{4}-\d{2}-\d{2}/.test(text)) {
    const d = new Date(text);
    if (!isNaN(d.getTime())) return d;
  }
  
  // "Just now", "now"
  if (text === "just now" || text === "now" || text.includes("moment")) {
    return now;
  }
  
  // "X seconds ago"
  let match = text.match(/(\d+)\s*(?:seconds?|secs?|s)\s*ago/i);
  if (match) {
    return new Date(now.getTime() - parseInt(match[1], 10) * 1000);
  }
  
  // "X minutes ago"
  match = text.match(/(\d+)\s*(?:minutes?|mins?|m)\s*ago/i);
  if (match) {
    return new Date(now.getTime() - parseInt(match[1], 10) * 60 * 1000);
  }
  
  // "X hours ago"
  match = text.match(/(\d+)\s*(?:hours?|hrs?|h)\s*ago/i);
  if (match) {
    return new Date(now.getTime() - parseInt(match[1], 10) * 60 * 60 * 1000);
  }
  
  // "X days ago"
  match = text.match(/(\d+)\s*(?:days?|d)\s*ago/i);
  if (match) {
    return new Date(now.getTime() - parseInt(match[1], 10) * 24 * 60 * 60 * 1000);
  }
  
  // "X weeks ago"
  match = text.match(/(\d+)\s*(?:weeks?|wks?|w)\s*ago/i);
  if (match) {
    return new Date(now.getTime() - parseInt(match[1], 10) * 7 * 24 * 60 * 60 * 1000);
  }
  
  // "yesterday"
  if (text.includes("yesterday")) {
    return new Date(now.getTime() - 24 * 60 * 60 * 1000);
  }
  
  // "a minute/hour/day ago"
  if (/^an?\s+minute/i.test(text)) return new Date(now.getTime() - 60 * 1000);
  if (/^an?\s+hour/i.test(text)) return new Date(now.getTime() - 60 * 60 * 1000);
  if (/^an?\s+day/i.test(text)) return new Date(now.getTime() - 24 * 60 * 60 * 1000);
  if (/^an?\s+week/i.test(text)) return new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
  
  // Try regular date parsing
  const parsed = new Date(text);
  if (!isNaN(parsed.getTime())) return parsed;
  
  return null;
}

const HEADERS = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
  "cache-control": "no-cache",
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

async function scrapeLinkedInGuestAPI(keyword, location, start = 0) {
  const params = new URLSearchParams({
    keywords: keyword,
    location: location,
    f_TPR: "r604800", // Past week
    sortBy: "DD", // Sort by date
    start: String(start)
  });
  
  const url = `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?${params}`;
  
  try {
    const response = await axios.get(url, {
      headers: HEADERS,
      timeout: 30000
    });
    
    const $ = cheerio.load(response.data);
    const jobs = [];
    
    $(".job-search-card, .base-card").each((_, el) => {
      const title = normalizeText($(el).find(".base-search-card__title, h3").text());
      const company = normalizeText($(el).find(".base-search-card__subtitle, h4").text());
      const loc = normalizeText($(el).find(".job-search-card__location").text());
      const link = $(el).find("a.base-card__full-link").attr("href");
      const dateText = normalizeText($(el).find("time").attr("datetime") || $(el).find("time").text());
      
      if (title && link) {
        // Parse the date - LinkedIn often uses "9 hours ago" format
        let postedDate = null;
        if (dateText) {
          const parsed = parseRelativeDate(dateText);
          if (parsed) {
            postedDate = parsed.toISOString();
          } else {
            // Try standard parsing
            const d = new Date(dateText);
            if (!isNaN(d.getTime())) {
              postedDate = d.toISOString();
            }
          }
        }
        // If we couldn't parse, mark as unknown (don't use current time!)
        const now = new Date().toISOString();
        
        jobs.push({
          title,
          company,
          location: loc || location,
          url: link.split("?")[0],
          source: "linkedin",
          id: `linkedin:${link.split("?")[0]}`,
          postedDate: postedDate || null, // null if unknown, NOT current time
          scrapedAt: now,
          dateSource: postedDate ? "parsed" : "unknown", // Track where date came from
          excerpt: `${title} at ${company}`
        });
      }
    });
    
    return jobs;
  } catch (error) {
    log(`Error scraping "${keyword}": ${error.message}`);
    return [];
  }
}

async function main() {
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║      LINKEDIN BULK SCRAPER - Using Guest API               ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");
  
  // Comprehensive list of tech keywords
  const keywords = [
    // Original requested keywords
    "ServiceNow developer",
    "ServiceNow",
    "VBA developer",
    "VBA Excel",
    "Alteryx developer",
    "Alteryx",
    "full stack developer",
    "full stack engineer",
    
    // Popular tech roles
    "software engineer",
    "software developer",
    "backend developer",
    "frontend developer",
    "Python developer",
    "JavaScript developer",
    "React developer",
    "Node.js developer",
    "Java developer",
    ".NET developer",
    "C# developer",
    
    // Data & Analytics
    "data analyst",
    "data engineer",
    "data scientist",
    "business analyst",
    "Power BI",
    "Tableau developer",
    "SQL developer",
    "ETL developer",
    
    // Cloud & DevOps
    "DevOps engineer",
    "AWS engineer",
    "Azure developer",
    "cloud architect",
    "site reliability engineer",
    "platform engineer",
    
    // Other tech roles
    "QA engineer",
    "automation engineer",
    "machine learning engineer",
    "AI engineer",
    "product manager tech",
    "technical project manager",
    "scrum master"
  ];
  
  const locations = ["Toronto, ON", "Ontario, Canada", "Canada"];
  const allJobs = [];
  const seenUrls = new Set();
  
  let successCount = 0;
  let failCount = 0;
  
  for (const keyword of keywords) {
    for (const location of locations) {
      log(`Scraping: "${keyword}" in ${location}`);
      
      // Get first 2 pages (50 jobs max per keyword/location)
      for (let page = 0; page < 2; page++) {
        await sleep(randomDelay(2000, 4000));
        
        const jobs = await scrapeLinkedInGuestAPI(keyword, location, page * 25);
        
        if (jobs.length > 0) {
          successCount++;
          for (const job of jobs) {
            if (!seenUrls.has(job.url)) {
              seenUrls.add(job.url);
              allJobs.push(job);
            }
          }
          log(`  -> Page ${page + 1}: ${jobs.length} jobs (total unique: ${allJobs.length})`);
        } else {
          failCount++;
          if (page === 0) {
            log(`  -> No jobs found`);
          }
          break; // Don't try page 2 if page 1 failed
        }
      }
      
      // Only search first location if we found jobs
      if (allJobs.length > 0 && location === "Toronto, ON") {
        break;
      }
    }
    
    // Progress update every 10 keywords
    if ((keywords.indexOf(keyword) + 1) % 10 === 0) {
      log(`\n--- Progress: ${keywords.indexOf(keyword) + 1}/${keywords.length} keywords, ${allJobs.length} unique jobs ---\n`);
    }
  }
  
  console.log("\n" + "═".repeat(60));
  console.log(`SCRAPE COMPLETE`);
  console.log(`  Total unique jobs: ${allJobs.length}`);
  console.log(`  Successful requests: ${successCount}`);
  console.log(`  Failed requests: ${failCount}`);
  console.log("═".repeat(60));
  
  // Load existing data
  const existingPath = path.join(__dirname, "..", "jobs.json");
  let existingData = { meta: {}, jobs: [] };
  try {
    existingData = JSON.parse(fs.readFileSync(existingPath, "utf-8"));
  } catch {}
  
  // Merge new jobs
  const existingIds = new Set(existingData.jobs.map(j => j.id));
  const newJobs = allJobs.filter(j => !existingIds.has(j.id));
  
  console.log(`\nNew jobs found: ${newJobs.length}`);
  
  if (newJobs.length > 0) {
    existingData.jobs.push(...newJobs);
    existingData.meta = {
      ...existingData.meta,
      lastLinkedInScrape: new Date().toISOString(),
      totalJobs: existingData.jobs.length,
      linkedInJobs: existingData.jobs.filter(j => j.source === "linkedin").length
    };
    
    // Save
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
    log("Copied to public folders");
  }
  
  // Show sample of new jobs
  if (newJobs.length > 0) {
    console.log("\n--- Sample New Jobs ---");
    newJobs.slice(0, 10).forEach((j, i) => {
      console.log(`${i + 1}. ${j.title}`);
      console.log(`   ${j.company} - ${j.location}`);
    });
  }
  
  return allJobs;
}

main().catch(console.error);
