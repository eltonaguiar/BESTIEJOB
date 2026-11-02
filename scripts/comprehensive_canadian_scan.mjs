#!/usr/bin/env node
/**
 * Comprehensive Canadian employer job scan
 * Targets: Indeed, Job Bank, Metrolinx, Canadian Banks, Telecom, Major Employers
 */

import axios from "axios";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import * as cheerio from "cheerio";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

// Targeted keywords matching the resume
const TARGET_KEYWORDS = [
  // ServiceNow
  "ServiceNow developer", "ServiceNow administrator", "ServiceNow architect",
  "ServiceNow consultant", "ServiceNow CSA", "ServiceNow CAD",
  "ServiceNow ITSM", "ServiceNow ITAM", "ServiceNow ITOM",
  "ServiceNow CMDB", "ServiceNow Flow Designer", "ServiceNow Integration Hub",
  
  // Salesforce
  "Salesforce developer", "Salesforce administrator", "Salesforce architect",
  "Salesforce Platform Developer I", "Salesforce Platform Administrator I",
  "Salesforce CPQ", "Salesforce Marketing Cloud", "Salesforce SFMC",
  "Salesforce Financial Services Cloud", "Salesforce Apex", "Salesforce LWC",
  
  // Resume-specific tech
  "ITAM", "IT Asset Management", "CMDB", "ITSM", "ITIL",
  "Alteryx", "PowerShell", "VBA", "Tableau", "Power BI",
  "Technical Consultant", "Data Analyst", "IT Risk Management"
];

// Extended Workday boards for Canadian banks & major employers
const EXTENDED_WORKDAY_BOARDS = [
  // Existing banks
  { tenant: "bmo", wd: "wd3", site: "External", label: "BMO" },
  { tenant: "td", wd: "wd3", site: "TD_Bank_Careers", label: "TD Bank" },
  { tenant: "moneris", wd: "wd3", site: "Moneris", label: "Moneris" },
  
  // Additional Canadian banks
  { tenant: "rbc", wd: "wd5", site: "RBC_Careers", label: "RBC" },
  { tenant: "scotiabank", wd: "wd101", site: "careers", label: "Scotiabank" },
  { tenant: "cibc", wd: "wd5", site: "CIBC_External", label: "CIBC" },
  { tenant: "nbc", wd: "wd5", site: "NBC_Careers", label: "National Bank" },
  { tenant: "desjardins", wd: "wd5", site: "Desjardins_Careers", label: "Desjardins" },
  
  // Telecom
  { tenant: "telus", wd: "wd5", site: "Telus_Careers", label: "Telus" },
  { tenant: "rogers", wd: "wd5", site: "Rogers_Careers", label: "Rogers" },
  { tenant: "bell", wd: "wd5", site: "Bell_Careers", label: "Bell" },
  { tenant: "shaw", wd: "wd5", site: "Shaw_Careers", label: "Shaw" },
  { tenant: "videotron", wd: "wd5", site: "Videotron_Careers", label: "Videotron" },
  
  // Insurance & Financial Services
  { tenant: "sunlife", wd: "wd5", site: "SunLife_Careers", label: "Sun Life" },
  { tenant: "manulife", wd: "wd5", site: "Manulife_Careers", label: "Manulife" },
  { tenant: "canadalife", wd: "wd5", site: "CanadaLife_Careers", label: "Canada Life" },
  { tenant: "iafinancial", wd: "wd5", site: "IAFinancial_Careers", label: "iA Financial" },
  { tenant: "greatwestlife", wd: "wd3", site: "GWL_Careers", label: "Great-West Life" },
  
  // Major Canadian employers
  { tenant: "metrolinx", wd: "wd5", site: "Metrolinx_Careers", label: "Metrolinx" },
  { tenant: "tcc", wd: "wd5", site: "TTC_Careers", label: "TTC" },
  { tenant: "hydroone", wd: "wd5", site: "HydroOne_Careers", label: "Hydro One" },
  { tenant: "opg", wd: "wd5", site: "OPG_Careers", label: "OPG" },
  { tenant: "enbridge", wd: "wd5", site: "Enbridge_Careers", label: "Enbridge" },
  { tenant: "tmx", wd: "wd5", site: "TMX_Careers", label: "TMX Group" },
  { tenant: "shopify", wd: "wd5", site: "Shopify_Careers", label: "Shopify" },
  { tenant: "weathernetwork", wd: "wd5", site: "WeatherNetwork_Careers", label: "Weather Network" },
  
  // Consulting
  { tenant: "deloitte", wd: "wd5", site: "Deloitte_Careers", label: "Deloitte" },
  { tenant: "pwc", wd: "wd5", site: "PwC_Careers", label: "PwC" },
  { tenant: "ey", wd: "wd3", site: "EY_Careers", label: "EY" },
  { tenant: "kpmg", wd: "wd5", site: "KPMG_Careers", label: "KPMG" },
  { tenant: "accenture", wd: "wd5", site: "Accenture_Careers", label: "Accenture" },
  { tenant: "cgi", wd: "wd5", site: "CGI_Careers", label: "CGI" },
];

const JOBBANK_KEYWORDS = [
  "ServiceNow", "Salesforce", "ITSM", "ITAM", "CMDB", "ITIL",
  "Alteryx", "PowerShell", "VBA", "Tableau", "Power BI",
  "Technical Consultant", "Data Analyst", "IT Risk",
  "Platform Developer", "Platform Administrator"
];

const JOBBANK_LOCATIONS = [
  "Toronto, ON", "Ontario", "Remote", "Canada",
  "Mississauga, ON", "Ottawa, ON", "Vancouver, BC", "Montreal, QC"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobs(keyword, location, page = 1, resultsPerPage = 50, maxDaysOld = 7) {
  const url = `https://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=${resultsPerPage}&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&content-type=application/json&max_days_old=${maxDaysOld}&sort_by=date`;
  
  try {
    const response = await axios.get(url, { timeout: 30000 });
    return response.data;
  } catch (error) {
    return { results: [], count: 0, error: error.message };
  }
}

async function scrapeWorkdayBoard(board, keyword, maxPages = 2) {
  const jobs = [];
  const api = `https://${board.tenant}.${board.wd}.myworkdayjobs.com/wday/cxs/${board.tenant}/${board.site}/jobs`;
  
  for (let offset = 0; offset < maxPages * 20; offset += 20) {
    try {
      const data = await axios.post(api, {
        appliedFacets: {},
        limit: 20,
        offset,
        searchText: keyword
      }, {
        headers: { "content-type": "application/json", accept: "application/json" },
        timeout: 30000
      });
      
      const posts = Array.isArray(data.data.jobPostings) ? data.data.jobPostings : [];
      if (posts.length === 0) break;
      
      for (const p of posts) {
        const job = {
          id: `workday:${board.tenant}:${p.externalPath}`,
          source: "workday",
          title: p.title,
          company: board.label,
          location: p.locationsText || "",
          url: `https://${board.tenant}.${board.wd}.myworkdayjobs.com/en-US/${board.site}${p.externalPath}`,
          postedDate: p.postedOn,
          excerpt: (p.bulletFields || []).join(" · "),
          scrapedAt: new Date().toISOString(),
          matchedKeyword: keyword
        };
        jobs.push(job);
      }
      
      if (!data.data.total || offset + 20 >= data.data.total) break;
      await sleep(300);
    } catch (err) {
      console.log(`  [Workday:${board.label}] "${keyword}" failed: ${err.message}`);
      break;
    }
  }
  return jobs;
}

async function scrapeJobBank(keyword, location, page = 1) {
  const url = `https://www.jobbank.gc.ca/jobsearch/api/jobsearch?searchstring=${encodeURIComponent(keyword)}&locationstring=${encodeURIComponent(location)}&sort=M&page=${page}&pagesize=100`;
  
  try {
    const response = await axios.get(url, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": "https://www.jobbank.gc.ca/"
      },
      timeout: 15000
    });
    
    const data = response.data;
    const results = data?.results || [];
    
    return results.map(job => ({
      id: `jobbank:${job.id || job.jobId || Math.random().toString(36).substr(2, 9)}`,
      source: "jobbank",
      company: job.employerName || job.company || "Government of Canada",
      title: job.title || job.jobTitle || "Position",
      location: job.location?.city || location,
      url: job.url || `https://www.jobbank.gc.ca/jobsearch/jobposting/${job.id}`,
      employmentType: job.type || job.employmentType || "full-time",
      salary: job.salary?.min && job.salary?.max ? { min: parseInt(job.salary.min), max: parseInt(job.salary.max) } : null,
      postedDate: job.datePosted || new Date().toISOString(),
      excerpt: (job.description || job.title || "").substring(0, 240),
      matchedKeyword: keyword
    }));
  } catch (e) {
    return [];
  }
}

async function scrapeIndeedRSS(keyword, location, dateFilter = "7") {
  const q = encodeURIComponent(keyword);
  const l = encodeURIComponent(location);
  const url = `https://ca.indeed.com/rss?q=${q}&l=${l}&sort=date&fromage=${dateFilter}`;
  
  try {
    const response = await axios.get(url, {
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" },
      timeout: 15000
    });
    
    const $ = cheerio.load(response.data, { xmlMode: true });
    const jobs = [];
    
    $("item").each((_, item) => {
      const $item = $(item);
      const title = $item.find("title").text().replace(/ - job post$/, "").replace(/ - .+$/, "");
      const link = $item.find("link").text();
      const pubDate = $item.find("pubDate").text();
      const description = $item.find("description").text().replace(/<[^>]*>/g, "").substring(0, 240);
      
      if (title && link) {
        jobs.push({
          id: `indeed:${link.split("jk=")[1]?.split("&")[0] || Math.random().toString(36).substr(2, 9)}`,
          source: "indeed",
          company: $item.find("creator").text() || "",
          title,
          location,
          url: link,
          postedDate: pubDate ? new Date(pubDate).toISOString() : new Date().toISOString(),
          excerpt: description,
          matchedKeyword: keyword
        });
      }
    });
    
    return jobs;
  } catch (e) {
    return [];
  }
}

async function main() {
  console.log("╔══════════════════════════════════════════════════════════════╗");
  console.log("║  COMPREHENSIVE CANADIAN EMPLOYER SCAN                        ║");
  console.log("║  Indeed + JobBank + Workday (Banks/Telecom/Metrolinx)       ║");
  console.log("╚══════════════════════════════════════════════════════════════╝\n");
  
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
  
  const today = new Date().toISOString().slice(0, 10);
  
  // 1. Job Bank Canada
  console.log("\n📋 JOB BANK CANADA");
  for (const keyword of JOBBANK_KEYWORDS) {
    for (const location of JOBBANK_LOCATIONS) {
      console.log(`  [JobBank] "${keyword}" in ${location}`);
      const jobs = await scrapeJobBank(keyword, location, 1);
      totalApiCalls++;
      
      let added = 0;
      for (const job of jobs) {
        if (!seen.has(job.id)) {
          seen.add(job.id);
          allNewJobs.push(job);
          added++;
        }
      }
      if (added > 0) console.log(`    Added ${added} new jobs`);
      await sleep(200);
    }
  }
  
  // 2. Extended Workday boards
  console.log("\n🏦 EXTENDED WORKDAY BOARDS (Banks/Telecom/Metrolinx/Etc)");
  const workdayQueries = ["servicenow", "salesforce", "platform developer", "platform administrator", "itsm", "itam", "cmdb"];
  
  for (const board of EXTENDED_WORKDAY_BOARDS) {
    console.log(`  [Workday] ${board.label}`);
    for (const query of workdayQueries) {
      const jobs = await scrapeWorkdayBoard(board, query, 1);
      totalApiCalls++;
      
      let added = 0;
      for (const job of jobs) {
        if (!seen.has(job.id)) {
          seen.add(job.id);
          allNewJobs.push(job);
          added++;
        }
      }
      if (added > 0) console.log(`    "${query}": ${added} new`);
      await sleep(200);
    }
  }
  
  // 3. Indeed RSS
  console.log("\n📰 INDEED RSS");
  const indeedKeywords = [
    "ServiceNow developer", "ServiceNow administrator", "Salesforce developer",
    "Salesforce Platform Developer I", "Salesforce Platform Administrator I",
    "ITAM", "CMDB", "ITSM", "Alteryx", "PowerShell", "Technical Consultant"
  ];
  
  for (const keyword of indeedKeywords) {
    console.log(`  [Indeed] "${keyword}"`);
    const jobs = await scrapeIndeedRSS(keyword, "Toronto, ON", "7");
    totalApiCalls++;
    
    let added = 0;
    for (const job of jobs) {
      if (!seen.has(job.id)) {
        seen.add(job.id);
        allNewJobs.push(job);
        added++;
      }
    }
    if (added > 0) console.log(`    Added ${added} new jobs`);
    await sleep(500);
  }
  
  // 4. Adzuna targeted (already done, but let's do a quick refresh for today)
  console.log("\n🔍 ADZUNA TODAY REFRESH");
  const todayKeywords = ["ServiceNow", "Salesforce", "ITSM", "ITAM", "CMDB", "Alteryx"];
  for (const keyword of todayKeywords) {
    const result = await fetchAdzunaJobs(keyword, "Toronto", 1, 50, 1);
    totalApiCalls++;
    
    let added = 0;
    for (const job of result.results || []) {
      const id = `adzuna:${job.id}`;
      if (!seen.has(id)) {
        const salaryMin = job.salary_min ? Math.round(job.salary_min) : null;
        const salaryMax = job.salary_max ? Math.round(job.salary_max) : null;
        
        seen.add(id);
        allNewJobs.push({
          id,
          source: "adzuna",
          company: job.company?.display_name || "Unknown",
          title: job.title,
          location: job.location?.display_name || "Toronto, Canada",
          url: job.redirect_url,
          employmentType: job.contract_time === "full_time" ? "full-time" : job.contract_time || "full-time",
          salary: salaryMin && salaryMax ? { min: salaryMin, max: salaryMax } : null,
          postedDate: job.created ? new Date(job.created).toISOString() : new Date().toISOString(),
          excerpt: job.description?.substring(0, 240)?.replace(/<[^>]*>/g, '') || job.title,
          category: job.category?.label || "Technology",
          scrapedAt: new Date().toISOString(),
          matchedKeyword: keyword
        });
        added++;
      }
    }
    if (added > 0) console.log(`    [Adzuna] "${keyword}": ${added} new`);
    await sleep(200);
  }
  
  console.log("\n" + "=".repeat(60));
  console.log("COMPREHENSIVE SCAN COMPLETE");
  console.log("=".repeat(60));
  console.log(`API Calls: ${totalApiCalls}`);
  console.log(`New Unique Jobs: ${allNewJobs.length}`);
  
  const todayJobs = allNewJobs.filter(j => j.postedDate?.startsWith(today));
  const yesterdayJobs = allNewJobs.filter(j => j.postedDate?.startsWith(new Date(Date.now() - 86400000).toISOString().slice(0, 10)));
  
  console.log(`Posted TODAY (${today}): ${todayJobs.length}`);
  console.log(`Posted YESTERDAY: ${yesterdayJobs.length}`);
  
  if (todayJobs.length > 0) {
    console.log(`\n--- TODAY'S JOBS ---`);
    todayJobs.forEach(j => console.log(`  ${j.title} @ ${j.company} [${j.source}]`));
  }
  
  // Merge and save
  if (allNewJobs.length > 0) {
    existingData.jobs.push(...allNewJobs);
    existingData.meta = {
      ...existingData.meta,
      lastComprehensiveScan: new Date().toISOString(),
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