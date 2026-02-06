#!/usr/bin/env node
/**
 * Comprehensive Job Scraper
 * Scrapes from all sources to build a complete job database
 * Designed to be run frequently (every 30-60 minutes) via GitHub Actions
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");

// Import scrapers
let atsApiScraper, companyCareersScraper, aggregatorScraper, remoteBoardsScraper, recruitingFirmsScraper;

try {
  atsApiScraper = await import("../scrapers/ats_api_scraper.js");
} catch (e) {
  console.log("ATS API scraper not available:", e.message);
}

try {
  companyCareersScraper = await import("../scrapers/company_careers_scraper.js");
} catch (e) {
  console.log("Company careers scraper not available:", e.message);
}

try {
  aggregatorScraper = await import("../scrapers/aggregator_scrapers.js");
} catch (e) {
  console.log("Aggregator scraper not available:", e.message);
}

try {
  remoteBoardsScraper = await import("../scrapers/remote_boards_scraper.js");
} catch (e) {
  console.log("Remote boards scraper not available:", e.message);
}

try {
  recruitingFirmsScraper = await import("../scrapers/recruiting_firms_scraper.js");
} catch (e) {
  console.log("Recruiting firms scraper not available:", e.message);
}

// Keywords for tech jobs
const TECH_KEYWORDS = [
  // Development
  "software developer", "software engineer", "full stack developer",
  "frontend developer", "backend developer", "web developer",
  "mobile developer", "iOS developer", "Android developer",
  "DevOps engineer", "cloud engineer", "platform engineer",
  // Data & AI
  "data scientist", "data analyst", "data engineer",
  "machine learning engineer", "AI engineer", "ML engineer",
  // Specific Technologies
  "ServiceNow developer", "VBA developer", "Alteryx developer",
  "Salesforce developer", "SAP developer", "Oracle developer",
  "Python developer", "Java developer", "JavaScript developer",
  "React developer", "Node.js developer", "TypeScript developer",
  ".NET developer", "C# developer", "Go developer", "Rust developer",
  // IT/Infrastructure
  "systems administrator", "network engineer", "security engineer",
  "cybersecurity analyst", "IT analyst", "database administrator",
  // Management
  "engineering manager", "technical lead", "tech lead",
  "product manager", "project manager", "scrum master"
];

const LOCATIONS = ["Toronto", "Ontario", "Canada", "Remote"];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function deduplicateJobs(jobs) {
  const seen = new Set();
  const unique = [];
  
  for (const job of jobs) {
    // Create a unique key based on title + company + location
    const key = `${job.title?.toLowerCase().trim()}-${job.company?.toLowerCase().trim()}-${job.location?.toLowerCase().trim()}`;
    
    if (!seen.has(key) && !seen.has(job.id)) {
      seen.add(key);
      seen.add(job.id);
      unique.push(job);
    }
  }
  
  return unique;
}

function loadExistingJobs() {
  const jobsPath = path.join(PROJECT_ROOT, "jobs.json");
  try {
    if (fs.existsSync(jobsPath)) {
      const data = fs.readFileSync(jobsPath, "utf8");
      const parsed = JSON.parse(data);
      // Handle both array and object with jobs property
      if (Array.isArray(parsed)) return parsed;
      if (Array.isArray(parsed.jobs)) return parsed.jobs;
      return [];
    }
  } catch (e) {
    console.log("Could not load existing jobs:", e.message);
  }
  return [];
}

function saveJobs(jobs) {
  const jobsPath = path.join(PROJECT_ROOT, "jobs.json");
  fs.writeFileSync(jobsPath, JSON.stringify(jobs, null, 2));
  
  // Also copy to public directories
  const publicDirs = [
    path.join(PROJECT_ROOT, "public", "jobs.json"),
    path.join(PROJECT_ROOT, "public", "findjobs", "jobs.json"),
    path.join(PROJECT_ROOT, "public", "gotjob", "jobs.json")
  ];
  
  for (const dest of publicDirs) {
    try {
      const destDir = path.dirname(dest);
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
      }
      fs.writeFileSync(dest, JSON.stringify(jobs, null, 2));
      console.log(`✓ Saved to ${dest}`);
    } catch (e) {
      console.log(`Could not save to ${dest}:`, e.message);
    }
  }
}

async function scrapeAggregators(keywords) {
  if (!aggregatorScraper) {
    console.log("[Aggregators] Scraper not available, skipping...");
    return [];
  }
  
  console.log("\n📦 SCRAPING JOB AGGREGATORS (Jooble, CareerJet, Talent.com)...");
  const jobs = [];
  
  try {
    // Jooble
    if (aggregatorScraper.fetchJoobleJobs) {
      const joobleJobs = await aggregatorScraper.fetchJoobleJobs(keywords.slice(0, 5), "Toronto");
      jobs.push(...joobleJobs);
      await sleep(500);
    }
    
    // CareerJet  
    if (aggregatorScraper.fetchCareerJetJobs) {
      const careerJetJobs = await aggregatorScraper.fetchCareerJetJobs(keywords.slice(0, 5), "Toronto, ON");
      jobs.push(...careerJetJobs);
      await sleep(500);
    }
    
    // Talent.com
    if (aggregatorScraper.fetchTalentJobs) {
      const talentJobs = await aggregatorScraper.fetchTalentJobs(keywords.slice(0, 5), "Toronto");
      jobs.push(...talentJobs);
    }
  } catch (e) {
    console.log("[Aggregators] Error:", e.message);
  }
  
  return jobs;
}

async function scrapeATSApis() {
  if (!atsApiScraper?.fetchAllATSJobs) {
    console.log("[ATS APIs] Scraper not available, skipping...");
    return [];
  }
  
  console.log("\n🏢 SCRAPING ATS APIs (Greenhouse, Lever, Ashby, Workable)...");
  
  try {
    const jobs = await atsApiScraper.fetchAllATSJobs();
    return jobs;
  } catch (e) {
    console.log("[ATS APIs] Error:", e.message);
    return [];
  }
}

async function scrapeCompanyCareers() {
  if (!companyCareersScraper?.scrapeAllCompanyCareers) {
    console.log("[Company Careers] Scraper not available, skipping...");
    return [];
  }
  
  console.log("\n🏛️ SCRAPING COMPANY CAREER PAGES...");
  
  try {
    const jobs = await companyCareersScraper.scrapeAllCompanyCareers();
    return jobs;
  } catch (e) {
    console.log("[Company Careers] Error:", e.message);
    return [];
  }
}

async function scrapeRemoteBoards() {
  if (!remoteBoardsScraper) {
    console.log("[Remote Boards] Scraper not available, skipping...");
    return [];
  }
  
  console.log("\n🌍 SCRAPING REMOTE JOB BOARDS...");
  const jobs = [];
  
  try {
    if (remoteBoardsScraper.fetchRemoteYeahJobs) {
      const remoteYeahJobs = await remoteBoardsScraper.fetchRemoteYeahJobs();
      jobs.push(...remoteYeahJobs);
      await sleep(500);
    }
    
    if (remoteBoardsScraper.fetch4DayWeekJobs) {
      const fourDayJobs = await remoteBoardsScraper.fetch4DayWeekJobs();
      jobs.push(...fourDayJobs);
      await sleep(500);
    }
    
    if (remoteBoardsScraper.fetchPangianJobs) {
      const pangianJobs = await remoteBoardsScraper.fetchPangianJobs();
      jobs.push(...pangianJobs);
    }
  } catch (e) {
    console.log("[Remote Boards] Error:", e.message);
  }
  
  return jobs;
}

async function scrapeRecruitingFirms() {
  if (!recruitingFirmsScraper) {
    console.log("[Recruiting Firms] Scraper not available, skipping...");
    return [];
  }
  
  console.log("\n🏢 SCRAPING IT RECRUITING FIRMS...");
  
  try {
    const jobs = await recruitingFirmsScraper.scrapeAllRecruitingFirms();
    return jobs;
  } catch (e) {
    console.log("[Recruiting Firms] Error:", e.message);
    return [];
  }
}

async function main() {
  console.log("╔══════════════════════════════════════════════════════╗");
  console.log("║      COMPREHENSIVE JOB SCRAPER                       ║");
  console.log("║      Aggregating jobs from all sources               ║");
  console.log("╚══════════════════════════════════════════════════════╝\n");
  
  const startTime = Date.now();
  
  // Load existing jobs
  const existingJobs = loadExistingJobs();
  console.log(`📂 Loaded ${existingJobs.length} existing jobs\n`);
  
  // Scrape all sources
  const allNewJobs = [];
  
  // 1. Job Aggregators (Jooble, CareerJet, Talent.com)
  const aggregatorJobs = await scrapeAggregators(TECH_KEYWORDS);
  allNewJobs.push(...aggregatorJobs);
  
  // 2. ATS APIs (Greenhouse, Lever, Ashby, Workable)
  const atsJobs = await scrapeATSApis();
  allNewJobs.push(...atsJobs);
  
  // 3. Company career pages
  const companyJobs = await scrapeCompanyCareers();
  allNewJobs.push(...companyJobs);
  
  // 4. Remote Job Boards
  const remoteJobs = await scrapeRemoteBoards();
  allNewJobs.push(...remoteJobs);
  
  // 5. IT Recruiting Firms
  const recruitingJobs = await scrapeRecruitingFirms();
  allNewJobs.push(...recruitingJobs);
  
  // Mark all new jobs with current timestamp
  const now = new Date().toISOString();
  for (const job of allNewJobs) {
    job.scrapedAt = now;
    if (!job.postedDate) {
      job.postedDate = now;
    }
  }
  
  // Combine with existing and deduplicate
  const combined = [...allNewJobs, ...existingJobs];
  const unique = deduplicateJobs(combined);
  
  // Sort by postedDate (most recent first)
  unique.sort((a, b) => {
    const dateA = new Date(a.postedDate || a.scrapedAt || 0);
    const dateB = new Date(b.postedDate || b.scrapedAt || 0);
    return dateB - dateA;
  });
  
  // Filter out jobs older than 30 days
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
  
  const fresh = unique.filter(job => {
    const jobDate = new Date(job.postedDate || job.scrapedAt || 0);
    return jobDate >= thirtyDaysAgo;
  });
  
  // Save jobs
  saveJobs(fresh);
  
  const elapsed = ((Date.now() - startTime) / 1000).toFixed(1);
  
  console.log("\n╔══════════════════════════════════════════════════════╗");
  console.log("║      SCRAPE COMPLETE                                 ║");
  console.log("╚══════════════════════════════════════════════════════╝");
  console.log(`
📊 Results Summary:
   • Aggregator jobs:     ${aggregatorJobs.length}
   • ATS API jobs:        ${atsJobs.length}
   • Company career jobs: ${companyJobs.length}
   • Remote board jobs:   ${remoteJobs.length}
   • Recruiting firms:    ${recruitingJobs.length}
   
   • Total new jobs:      ${allNewJobs.length}
   • Previously existing: ${existingJobs.length}
   • After deduplication: ${unique.length}
   • Fresh jobs (30d):    ${fresh.length}
   
⏱️  Elapsed time: ${elapsed}s
📁 Saved to jobs.json and public directories
  `);
}

main().catch(console.error);
