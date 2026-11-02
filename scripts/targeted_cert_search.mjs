#!/usr/bin/env node
/**
 * Targeted search for specific ServiceNow/Salesforce certifications and roles
 * - ServiceNow CSA (Certified System Administrator)
 * - ServiceNow CAD (Certified Application Developer)
 * - Salesforce Platform Developer I / 1
 * - Salesforce Platform Administrator I / 1
 * - Salesforce Platform Developer
 * - Salesforce Platform Admin
 */

import axios from "axios";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

const TARGET_KEYWORDS = [
  // ServiceNow Certifications
  "ServiceNow CSA",
  "ServiceNow CAD",
  "Certified System Administrator ServiceNow",
  "Certified Application Developer ServiceNow",
  "CSA ServiceNow",
  "CAD ServiceNow",
  
  // ServiceNow Roles
  "ServiceNow Administrator",
  "ServiceNow Developer",
  "ServiceNow Architect",
  "ServiceNow Consultant",
  "ServiceNow Technical Consultant",
  
  // Salesforce Certifications
  "Salesforce Platform Developer I",
  "Salesforce Platform Developer 1",
  "Salesforce Platform Administrator I",
  "Salesforce Platform Administrator 1",
  "Salesforce Certified Platform Developer",
  "Salesforce Certified Platform Administrator",
  
  // Salesforce Roles
  "Salesforce Platform Developer",
  "Salesforce Platform Administrator",
  "Salesforce Developer",
  "Salesforce Administrator",
  "Salesforce Consultant",
  "Salesforce Technical Consultant",
];

const LOCATIONS = [
  "Toronto",
  "Toronto, ON",
  "Ontario",
  "Remote",
  "Canada",
  "Vancouver",
  "Montreal",
  "Calgary",
  "Ottawa",
  "Mississauga",
  "Markham",
  "Brampton"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobs(keyword, location, page = 1, resultsPerPage = 100, maxDaysOld = 3) {
  const url = `https://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=${resultsPerPage}&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&content-type=application/json&max_days_old=${maxDaysOld}&sort_by=date`;
  
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
        scrapedAt: new Date().toISOString(),
        matchedKeyword: keyword
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

function classifyJob(title, excerpt, keyword) {
  const text = `${title} ${excerpt}`.toLowerCase();
  const keywordLower = keyword.toLowerCase();
  
  const isServiceNow = /servicenow|service now|csa\b|cad\b|certified system administrator|certified application developer/.test(text);
  const isSalesforce = /salesforce|platform developer|platform administrator|platform admin|platform dev|certified platform/.test(text);
  
  // Check for specific certifications
  const hasCSA = /csa\b|certified system admin/.test(text);
  const hasCAD = /cad\b|certified application developer/.test(text);
  const hasPlatformDev1 = /platform developer\s*(i|1)\b/.test(text);
  const hasPlatformAdmin1 = /platform administrator\s*(i|1)\b|platform admin\s*(i|1)\b/.test(text);
  
  return { isServiceNow, isSalesforce, hasCSA, hasCAD, hasPlatformDev1, hasPlatformAdmin1 };
}

async function main() {
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║  TARGETED CERT/ROLE SEARCH - ServiceNow & Salesforce       ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");
  
  console.log(`Keywords: ${TARGET_KEYWORDS.length}`);
  console.log(`Locations: ${LOCATIONS.length}`);
  console.log(`Max days old: 3\n`);
  
  // Load existing jobs
  const existingPath = path.join(ROOT, "jobs.json");
  let existingData = { meta: {}, jobs: [] };
  try {
    existingData = JSON.parse(fs.readFileSync(existingPath, "utf-8"));
    console.log(`Loaded ${existingData.jobs.length} existing jobs`);
  } catch {}
  
  const existingIds = new Set(existingData.jobs.map(j => j.id));
  const seen = new Set(existingIds);
  const allNewJobs = [];
  let totalApiCalls = 0;
  let totalFound = 0;
  
  const today = new Date().toISOString().slice(0, 10);
  
  for (let i = 0; i < TARGET_KEYWORDS.length; i++) {
    const keyword = TARGET_KEYWORDS[i];
    let keywordJobs = 0;
    
    for (const location of LOCATIONS) {
      const result = await fetchAdzunaJobs(keyword, location, 1, 100, 3);
      totalApiCalls++;
      
      if (result.error) {
        console.log(`  [${keyword} @ ${location}] Error: ${result.error}`);
        continue;
      }
      
      totalFound += result.count;
      
      let added = 0;
      for (const job of result.jobs) {
        if (!seen.has(job.id)) {
          const classification = classifyJob(job.title, job.excerpt, keyword);
          job.classification = classification;
          job.searchKeyword = keyword;
          
          seen.add(job.id);
          allNewJobs.push(job);
          keywordJobs++;
          added++;
        }
      }
      
      if (result.count > 0) {
        console.log(`  [${keyword} @ ${location}] Found ${result.count}, added ${added} new`);
      }
      
      // If we found jobs in first location, we can try next keyword
      // but let's check all locations for completeness
      
      await sleep(200);
    }
    
    console.log(`Keyword "${keyword}": ${keywordJobs} new jobs`);
  }
  
  console.log("\n" + "=".repeat(60));
  console.log("TARGETED SEARCH COMPLETE");
  console.log("=".repeat(60));
  console.log(`API Calls: ${totalApiCalls}`);
  console.log(`Total Available: ${totalFound}`);
  console.log(`New Unique Jobs: ${allNewJobs.length}`);
  
  // Show jobs by classification
  const snJobs = allNewJobs.filter(j => j.classification.isServiceNow);
  const sfJobs = allNewJobs.filter(j => j.classification.isSalesforce);
  const csaJobs = allNewJobs.filter(j => j.classification.hasCSA);
  const cadJobs = allNewJobs.filter(j => j.classification.hasCAD);
  const pd1Jobs = allNewJobs.filter(j => j.classification.hasPlatformDev1);
  const pa1Jobs = allNewJobs.filter(j => j.classification.hasPlatformAdmin1);
  const todayJobs = allNewJobs.filter(j => j.postedDate.startsWith(today));
  
  console.log(`\nServiceNow jobs: ${snJobs.length}`);
  console.log(`Salesforce jobs: ${sfJobs.length}`);
  console.log(`CSA mentioned: ${csaJobs.length}`);
  console.log(`CAD mentioned: ${cadJobs.length}`);
  console.log(`Platform Developer I/1: ${pd1Jobs.length}`);
  console.log(`Platform Administrator I/1: ${pa1Jobs.length}`);
  console.log(`Posted TODAY (${today}): ${todayJobs.length}`);
  
  // Show today's jobs
  if (todayJobs.length > 0) {
    console.log(`\n--- TODAY'S JOBS (${today}) ---`);
    todayJobs.forEach(j => {
      console.log(`  ${j.title} @ ${j.company} [${j.searchKeyword}]`);
    });
  }
  
  // Merge and save
  if (allNewJobs.length > 0) {
    existingData.jobs.push(...allNewJobs);
    existingData.meta = {
      ...existingData.meta,
      lastTargetedSearch: new Date().toISOString(),
      totalJobs: existingData.jobs.length
    };
    
    fs.writeFileSync(existingPath, JSON.stringify(existingData, null, 2));
    console.log(`\nSaved ${existingData.jobs.length} total jobs to jobs.json`);
    
    // Copy to public folders
    const publicPaths = [
      path.join(ROOT, "public", "jobs.json"),
      path.join(ROOT, "public", "findjobs", "jobs.json"),
      path.join(ROOT, "public", "gotjob", "jobs.json")
    ];
    
    for (const p of publicPaths) {
      try {
        fs.writeFileSync(p, JSON.stringify(existingData, null, 2));
      } catch {}
    }
    console.log("Copied to public folders");
  }
  
  // Also update the recent scan file
  const recentPath = path.join(ROOT, "recent_sn_sf_scan.json");
  const recentData = {
    meta: {
      scannedAt: new Date().toISOString(),
      today,
      yesterday: new Date(Date.now() - 86400000).toISOString().slice(0, 10),
      weekAgo: new Date(Date.now() - 7 * 86400000).toISOString().slice(0, 10),
      counts: {
        today: todayJobs.length,
        yesterday: allNewJobs.filter(j => j.postedDate.startsWith(new Date(Date.now() - 86400000).toISOString().slice(0, 10))).length,
        within7: allNewJobs.length,
        older: 0
      },
      source: "adzuna-targeted",
      existingJobsLoaded: existingData.jobs.length
    },
    today: todayJobs,
    yesterday: allNewJobs.filter(j => j.postedDate.startsWith(new Date(Date.now() - 86400000).toISOString().slice(0, 10))),
    within7Days: allNewJobs,
    older: []
  };
  fs.writeFileSync(recentPath, JSON.stringify(recentData, null, 2));
  console.log(`Saved recent scan to ${recentPath}`);
}

main().catch(console.error);