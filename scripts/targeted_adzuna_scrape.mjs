#!/usr/bin/env node
/**
 * Targeted Adzuna Scrape - For specific tech keywords
 * Adzuna aggregates jobs from many sources including Indeed
 */

import axios from "axios";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Adzuna API credentials
const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

// Specific keywords requested by user
const KEYWORDS = [
  // Primary requested keywords
  "ServiceNow developer",
  "ServiceNow",
  "VBA developer", 
  "VBA Excel",
  "VBA macro",
  "Alteryx developer",
  "Alteryx",
  "full stack developer",
  "full stack",
  
  // Additional tech keywords
  "software engineer",
  "software developer",
  "web developer",
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
  "business intelligence",
  "Power BI",
  "Tableau",
  "SQL developer",
  "ETL developer",
  
  // Cloud & DevOps
  "DevOps engineer",
  "AWS engineer",
  "Azure developer",
  "cloud architect",
  "site reliability engineer",
  "Kubernetes",
  
  // Other in-demand
  "machine learning",
  "AI engineer",
  "automation engineer",
  "QA engineer",
  "product manager",
  "project manager",
  "scrum master"
];

const LOCATIONS = [
  "Toronto",
  "Toronto, ON",
  "Ontario",
  "Vancouver",
  "Montreal",
  "Calgary"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function log(msg) {
  console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
}

async function fetchAdzunaJobs(keyword, location, page = 1, resultsPerPage = 100) {
  const url = `https://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=${resultsPerPage}&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&content-type=application/json&max_days_old=7`;
  
  try {
    const response = await axios.get(url, {
      timeout: 30000,
      headers: {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    
    const data = response.data;
    const results = data?.results || [];
    
    const jobs = results.map(job => {
      const salaryMin = job.salary_min ? Math.round(job.salary_min) : null;
      const salaryMax = job.salary_max ? Math.round(job.salary_max) : null;
      
      return {
        id: `adzuna:${job.id}`,
        source: "adzuna",
        company: job.company?.display_name || "Unknown",
        title: job.title,
        location: job.location?.display_name || `${location}, Canada`,
        url: job.redirect_url,
        employmentType: job.contract_time === "full_time" ? "full-time" : job.contract_time || "full-time",
        salary: salaryMin && salaryMax ? { min: salaryMin, max: salaryMax } : null,
        postedDate: job.created ? new Date(job.created).toISOString() : new Date().toISOString(),
        excerpt: job.description?.substring(0, 240)?.replace(/<[^>]*>/g, '') || job.title,
        category: job.category?.label || "Technology",
        scrapedAt: new Date().toISOString()
      };
    });
    
    return {
      jobs,
      count: data?.count || 0,
      totalPages: Math.ceil((data?.count || 0) / resultsPerPage)
    };
  } catch (error) {
    return { jobs: [], count: 0, totalPages: 0, error: error.message };
  }
}

async function main() {
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║    TARGETED ADZUNA SCRAPE - Tech Keywords (Last 7 Days)    ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");
  
  log(`Keywords: ${KEYWORDS.length}`);
  log(`Locations: ${LOCATIONS.length}`);
  log(`Country: Canada\n`);
  
  const allJobs = [];
  const seen = new Set();
  let totalApiCalls = 0;
  let totalAvailable = 0;
  
  for (let i = 0; i < KEYWORDS.length; i++) {
    const keyword = KEYWORDS[i];
    
    // Try each location
    for (const location of LOCATIONS) {
      log(`Searching: "${keyword}" in ${location}`);
      
      // Page 1
      const result = await fetchAdzunaJobs(keyword, location, 1, 100);
      totalApiCalls++;
      
      if (result.error) {
        log(`  Error: ${result.error}`);
        continue;
      }
      
      totalAvailable += result.count;
      
      let added = 0;
      for (const job of result.jobs) {
        if (!seen.has(job.id)) {
          seen.add(job.id);
          allJobs.push(job);
          added++;
        }
      }
      
      if (result.count > 0) {
        log(`  Found ${result.count} total, added ${added} new (unique: ${allJobs.length})`);
      }
      
      // Page 2 if more results
      if (result.count > 100) {
        await sleep(300);
        const result2 = await fetchAdzunaJobs(keyword, location, 2, 100);
        totalApiCalls++;
        
        for (const job of result2.jobs) {
          if (!seen.has(job.id)) {
            seen.add(job.id);
            allJobs.push(job);
          }
        }
      }
      
      await sleep(250);
      
      // If we found jobs in first location, move to next keyword
      if (result.count > 0) break;
    }
    
    // Progress update
    if ((i + 1) % 10 === 0) {
      log(`\n--- Progress: ${i + 1}/${KEYWORDS.length} keywords, ${allJobs.length} jobs ---\n`);
    }
  }
  
  console.log("\n" + "═".repeat(60));
  console.log("ADZUNA SCRAPE COMPLETE");
  console.log("═".repeat(60));
  console.log(`API Calls: ${totalApiCalls}`);
  console.log(`Total Available: ${totalAvailable}`);
  console.log(`Unique Jobs: ${allJobs.length}`);
  
  // Load existing data
  const existingPath = path.join(__dirname, "..", "jobs.json");
  let existingData = { meta: {}, jobs: [] };
  try {
    existingData = JSON.parse(fs.readFileSync(existingPath, "utf-8"));
    log(`Loaded ${existingData.jobs.length} existing jobs`);
  } catch {}
  
  // Merge
  const existingIds = new Set(existingData.jobs.map(j => j.id));
  const newJobs = allJobs.filter(j => !existingIds.has(j.id));
  
  console.log(`\nNew jobs to add: ${newJobs.length}`);
  
  if (newJobs.length > 0) {
    existingData.jobs.push(...newJobs);
    existingData.meta = {
      ...existingData.meta,
      lastAdzunaScrape: new Date().toISOString(),
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
    log("Copied to public folders");
  }
  
  // Show keyword breakdown
  if (allJobs.length > 0) {
    console.log("\n--- Sample Jobs by Keyword ---");
    
    // ServiceNow
    const snJobs = allJobs.filter(j => j.title.toLowerCase().includes("servicenow"));
    console.log(`\nServiceNow jobs: ${snJobs.length}`);
    snJobs.slice(0, 3).forEach(j => console.log(`  - ${j.title} @ ${j.company}`));
    
    // VBA
    const vbaJobs = allJobs.filter(j => j.title.toLowerCase().includes("vba") || j.excerpt?.toLowerCase().includes("vba"));
    console.log(`\nVBA jobs: ${vbaJobs.length}`);
    vbaJobs.slice(0, 3).forEach(j => console.log(`  - ${j.title} @ ${j.company}`));
    
    // Alteryx
    const alteryxJobs = allJobs.filter(j => j.title.toLowerCase().includes("alteryx") || j.excerpt?.toLowerCase().includes("alteryx"));
    console.log(`\nAlteryx jobs: ${alteryxJobs.length}`);
    alteryxJobs.slice(0, 3).forEach(j => console.log(`  - ${j.title} @ ${j.company}`));
    
    // Full Stack
    const fsJobs = allJobs.filter(j => j.title.toLowerCase().includes("full stack") || j.title.toLowerCase().includes("fullstack"));
    console.log(`\nFull Stack jobs: ${fsJobs.length}`);
    fsJobs.slice(0, 3).forEach(j => console.log(`  - ${j.title} @ ${j.company}`));
  }
}

main().catch(console.error);
