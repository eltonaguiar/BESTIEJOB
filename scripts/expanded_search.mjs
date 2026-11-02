#!/usr/bin/env node
/**
 * Expanded job search using Adzuna with more targeted keywords
 * and additional sources
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

const EXPANDED_KEYWORDS = [
  // ServiceNow specific certifications
  "ServiceNow CSA",
  "ServiceNow CAD",
  "ServiceNow Certified System Administrator",
  "ServiceNow Certified Application Developer",
  "CSA ServiceNow Toronto",
  "CAD ServiceNow Toronto",
  
  // ServiceNow roles with specific modules
  "ServiceNow ITSM",
  "ServiceNow ITAM",
  "ServiceNow ITOM",
  "ServiceNow HRSD",
  "ServiceNow CSM",
  "ServiceNow FSM",
  "ServiceNow GRC",
  "ServiceNow SecOps",
  "ServiceNow CMDB",
  "ServiceNow Discovery",
  "ServiceNow Service Mapping",
  "ServiceNow Flow Designer",
  "ServiceNow Integration Hub",
  "ServiceNow Agentic AI",
  "ServiceNow Now Assist",
  "ServiceNow Virtual Agent",
  
  // Salesforce specific certifications
  "Salesforce Platform Developer I",
  "Salesforce Platform Developer 1",
  "Salesforce Platform Administrator I",
  "Salesforce Platform Administrator 1",
  "Salesforce PD1",
  "Salesforce ADM 201",
  "Salesforce DEV 401",
  "Salesforce Platform App Builder",
  
  // Salesforce specific roles
  "Salesforce CPQ",
  "Salesforce Marketing Cloud",
  "Salesforce SFMC",
  "Salesforce Experience Cloud",
  "Salesforce Service Cloud",
  "Salesforce Sales Cloud",
  "Salesforce Financial Services Cloud",
  "Salesforce Health Cloud",
  "Salesforce Revenue Cloud",
  "Salesforce Industries",
  "Salesforce Vlocity",
  "Salesforce MuleSoft",
  "Salesforce Integration",
  "Salesforce Apex",
  "Salesforce LWC",
  "Salesforce Lightning Web Components",
  "Salesforce Flow",
  "Salesforce Admin",
  
  // Related tech from resume
  "ITAM",
  "IT Asset Management",
  "CMDB",
  "ITSM",
  "ITIL",
  "ITOM",
  "ServiceNow CMDB",
  "Alteryx",
  "VBA",
  "PowerShell",
  "Tableau",
  "Power BI",
  "SQL Server",
  "JIRA",
  "Confluence",
  "GitHub Actions",
  "CI/CD",
  "Technical Consultant",
  "Data Analyst",
  "IT Risk Management",
];

const LOCATIONS = [
  "Toronto",
  "Toronto, ON",
  "Ontario",
  "Remote",
  "Canada",
  "Mississauga",
  "Brampton",
  "Markham",
  "Vaughan",
  "Richmond Hill",
  "Oakville",
  "Burlington",
  "Hamilton",
  "Kitchener",
  "Waterloo",
  "London",
  "Ottawa",
  "Montreal",
  "Vancouver",
  "Calgary",
  "Edmonton"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobs(keyword, location, page = 1, resultsPerPage = 50, maxDaysOld = 7) {
  const url = `https://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=${resultsPerPage}&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&content-type=application/json&max_days_old=${maxDaysOld}&sort_by=date`;
  
  try {
    const response = await axios.get(url, {
      timeout: 30000,
      headers: {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    return response.data;
  } catch (error) {
    return { results: [], count: 0, error: error.message };
  }
}

function classifyJob(title, excerpt, keyword) {
  const text = `${title} ${excerpt}`.toLowerCase();
  
  const isServiceNow = /servicenow|service now|csa\b|cad\b|certified system admin|certified application developer|itsm|itom|itam|hrsd|csm|fsm|grc|secops|cmdb|discovery|service mapping|flow designer|integration hub|agentic ai|now assist|virtual agent/.test(text);
  const isSalesforce = /salesforce|platform developer|platform administrator|platform admin|platform dev|certified platform|cpq|sfmc|marketing cloud|experience cloud|service cloud|sales cloud|financial services cloud|health cloud|revenue cloud|industries|vlocity|mulesoft|apex|lwc|lightning web components|flow builder/.test(text);
  
  const hasCSA = /csa\b|certified system admin/.test(text);
  const hasCAD = /cad\b|certified application developer/.test(text);
  const hasPlatformDev1 = /platform developer\s*(i|1)\b/.test(text);
  const hasPlatformAdmin1 = /platform administrator\s*(i|1)\b|platform admin\s*(i|1)\b/.test(text);
  
  return { isServiceNow, isSalesforce, hasCSA, hasCAD, hasPlatformDev1, hasPlatformAdmin1 };
}

async function main() {
  console.log("╔════════════════════════════════════════════════════════════╗");
  console.log("║  EXPANDED JOB SEARCH - Round 2                             ║");
  console.log("╚════════════════════════════════════════════════════════════╝\n");
  
  console.log(`Keywords: ${EXPANDED_KEYWORDS.length}`);
  console.log(`Locations: ${LOCATIONS.length}`);
  console.log(`Max days old: 7\n`);
  
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
  const yesterday = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
  
  for (let i = 0; i < EXPANDED_KEYWORDS.length; i++) {
    const keyword = EXPANDED_KEYWORDS[i];
    let keywordJobs = 0;
    
    for (const location of LOCATIONS) {
      const result = await fetchAdzunaJobs(keyword, location, 1, 50, 7);
      totalApiCalls++;
      
      if (result.error) {
        continue;
      }
      
      totalFound += result.count;
      
      let added = 0;
      for (const job of result.results || []) {
        const id = `adzuna:${job.id}`;
        if (!seen.has(id)) {
          const classification = classifyJob(job.title, job.description || "", keyword);
          const salaryMin = job.salary_min ? Math.round(job.salary_min) : null;
          const salaryMax = job.salary_max ? Math.round(job.salary_max) : null;
          
          const newJob = {
            id,
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
            matchedKeyword: keyword,
            classification
          };
          
          seen.add(id);
          allNewJobs.push(newJob);
          keywordJobs++;
          added++;
        }
      }
      
      if (result.count > 0 && added > 0) {
        console.log(`  [${keyword} @ ${location}] Found ${result.count}, added ${added} new`);
      }
      
      await sleep(150);
    }
    
    if (keywordJobs > 0) {
      console.log(`Keyword "${keyword}": ${keywordJobs} new jobs`);
    }
    
    // Progress every 20 keywords
    if ((i + 1) % 20 === 0) {
      console.log(`\n--- Progress: ${i + 1}/${EXPANDED_KEYWORDS.length} keywords, ${allNewJobs.length} jobs ---\n`);
    }
  }
  
  console.log("\n" + "=".repeat(60));
  console.log("EXPANDED SEARCH COMPLETE");
  console.log("=".repeat(60));
  console.log(`API Calls: ${totalApiCalls}`);
  console.log(`Total Available: ${totalFound}`);
  console.log(`New Unique Jobs: ${allNewJobs.length}`);
  
  // Classification summary
  const snJobs = allNewJobs.filter(j => j.classification.isServiceNow);
  const sfJobs = allNewJobs.filter(j => j.classification.isSalesforce);
  const csaJobs = allNewJobs.filter(j => j.classification.hasCSA);
  const cadJobs = allNewJobs.filter(j => j.classification.hasCAD);
  const pd1Jobs = allNewJobs.filter(j => j.classification.hasPlatformDev1);
  const pa1Jobs = allNewJobs.filter(j => j.classification.hasPlatformAdmin1);
  const todayJobs = allNewJobs.filter(j => j.postedDate.startsWith(today));
  const yesterdayJobs = allNewJobs.filter(j => j.postedDate.startsWith(yesterday));
  
  console.log(`\nServiceNow jobs: ${snJobs.length}`);
  console.log(`Salesforce jobs: ${sfJobs.length}`);
  console.log(`CSA mentioned: ${csaJobs.length}`);
  console.log(`CAD mentioned: ${cadJobs.length}`);
  console.log(`Platform Developer I/1: ${pd1Jobs.length}`);
  console.log(`Platform Administrator I/1: ${pa1Jobs.length}`);
  console.log(`Posted TODAY (${today}): ${todayJobs.length}`);
  console.log(`Posted YESTERDAY (${yesterday}): ${yesterdayJobs.length}`);
  
  // Show today's jobs
  if (todayJobs.length > 0) {
    console.log(`\n--- TODAY'S JOBS (${today}) ---`);
    todayJobs.forEach(j => {
      console.log(`  ${j.title} @ ${j.company} [${j.matchedKeyword}]`);
    });
  }
  
  // Merge and save
  if (allNewJobs.length > 0) {
    existingData.jobs.push(...allNewJobs);
    existingData.meta = {
      ...existingData.meta,
      lastExpandedSearch: new Date().toISOString(),
      totalJobs: existingData.jobs.length
    };
    
    fs.writeFileSync(existingPath, JSON.stringify(existingData, null, 2));
    console.log(`\nSaved ${existingData.jobs.length} total jobs to jobs.json`);
    
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
  
  return allNewJobs;
}

main().catch(console.error);