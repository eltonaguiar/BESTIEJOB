import axios from "axios";
import * as cheerio from "cheerio";
import fs from "fs";

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ==================== DAYFORCE/CERIDIAN CAREERS ====================
async function scrapeDayforceCareers() {
  const jobs = [];
  try {
    console.log("Scraping Dayforce/Ceridian careers...");
    
    // Try multiple Dayforce/Ceridian career endpoints
    const urls = [
      "https://careers.ceridian.com/jobs",
      "https://www.dayforce.com/careers.html",
      "https://jobs.dayforce.com"
    ];
    
    for (const url of urls) {
      try {
        const res = await axios.get(url, {
          timeout: 15000,
          headers: {
            "User-Agent": getRandomUserAgent(),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
          }
        });
        
        const $ = cheerio.load(res.data);
        
        // Try multiple selectors
        $("[data-job-id], .job-listing, .job-card, .career-item, tr[data-id]").each((_, el) => {
          const title = $(el).find("h2, h3, .job-title, .title, td:nth-child(1)").text().trim();
          const location = $(el).find(".location, .job-location, .city, td:nth-child(2)").text().trim();
          const link = $(el).find("a").attr("href") || "";
          
          if (title && title.toLowerCase().includes("developer" || "engineer" || "manager" || "analyst" || "consultant")) {
            jobs.push({
              id: `dayforce:${link || Math.random().toString(36).substr(2, 9)}`,
              source: "dayforce",
              company: "Dayforce/Ceridian",
              title,
              location: location || "Toronto, ON",
              url: link.startsWith("http") ? link : `https://careers.ceridian.com${link}`,
              employmentType: "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: `${title} at Dayforce/Ceridian - HR Technology Platform`
            });
          }
        });
        
        if (jobs.length > 0) break;
      } catch (e) {
        console.log(`  ${url} failed: ${e.message}`);
      }
    }
    
    console.log(`  Found ${jobs.length} Dayforce jobs`);
  } catch (e) {
    console.log(`  Dayforce error: ${e.message}`);
  }
  return jobs;
}

// ==================== WORKDAY CAREERS ====================
async function scrapeWorkdayCareers() {
  const jobs = [];
  try {
    console.log("Scraping Workday careers...");
    
    const res = await axios.get("https://www.workday.com/en-us/company/careers.html", {
      timeout: 15000,
      headers: { "User-Agent": getRandomUserAgent() }
    });
    
    const $ = cheerio.load(res.data);
    
    $(".job-listing, .career-item, [data-role='job']").each((_, el) => {
      const title = $(el).find("h3, .job-title").text().trim();
      const location = $(el).find(".location").text().trim();
      const link = $(el).find("a").attr("href") || "";
      
      if (title) {
        jobs.push({
          id: `workday:${link || Math.random().toString(36).substr(2, 9)}`,
          source: "workday",
          company: "Workday",
          title,
          location: location || "Remote",
          url: link.startsWith("http") ? link : `https://www.workday.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at Workday - Enterprise HR Platform`
        });
      }
    });
    
    console.log(`  Found ${jobs.length} Workday jobs`);
  } catch (e) {
    console.log(`  Workday error: ${e.message}`);
  }
  return jobs;
}

// ==================== ADP CAREERS ====================
async function scrapeADPCareers() {
  const jobs = [];
  try {
    console.log("Scraping ADP careers...");
    
    const res = await axios.get("https://jobs.adp.com", {
      timeout: 15000,
      headers: { "User-Agent": getRandomUserAgent() }
    });
    
    const $ = cheerio.load(res.data);
    
    $(".job-result, .job-card, [data-job-id]").each((_, el) => {
      const title = $(el).find(".job-title, h3, .title").text().trim();
      const location = $(el).find(".job-location, .location").text().trim();
      const link = $(el).find("a").attr("href") || "";
      
      if (title) {
        jobs.push({
          id: `adp:${link || Math.random().toString(36).substr(2, 9)}`,
          source: "adp",
          company: "ADP",
          title,
          location: location || "Multiple Locations",
          url: link.startsWith("http") ? link : `https://jobs.adp.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at ADP - HR/Payroll Solutions`
        });
      }
    });
    
    console.log(`  Found ${jobs.length} ADP jobs`);
  } catch (e) {
    console.log(`  ADP error: ${e.message}`);
  }
  return jobs;
}

// ==================== SAP SUCCESSFACTORS ====================
async function scrapeSAPCareers() {
  const jobs = [];
  try {
    console.log("Scraping SAP/SuccessFactors careers...");
    
    const res = await axios.get("https://jobs.sap.com", {
      timeout: 15000,
      headers: { "User-Agent": getRandomUserAgent() }
    });
    
    const $ = cheerio.load(res.data);
    
    $(".job-listing, .job-item, [data-job-id]").each((_, el) => {
      const title = $(el).find(".job-title, h3, .title").text().trim();
      const location = $(el).find(".job-location, .location").text().trim();
      const link = $(el).find("a").attr("href") || "";
      
      if (title && (title.toLowerCase().includes("successfactors") || title.toLowerCase().includes("hr") || title.toLowerCase().includes("human capital"))) {
        jobs.push({
          id: `sap:${link || Math.random().toString(36).substr(2, 9)}`,
          source: "sap",
          company: "SAP",
          title,
          location: location || "Multiple Locations",
          url: link.startsWith("http") ? link : `https://jobs.sap.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at SAP - SuccessFactors HCM Platform`
        });
      }
    });
    
    console.log(`  Found ${jobs.length} SAP HR jobs`);
  } catch (e) {
    console.log(`  SAP error: ${e.message}`);
  }
  return jobs;
}

// ==================== UKG (ULTIMATE SOFTWARE + KRONOS) ====================
async function scrapeUKGCareers() {
  const jobs = [];
  try {
    console.log("Scraping UKG careers...");
    
    const res = await axios.get("https://www.ukg.com/careers", {
      timeout: 15000,
      headers: { "User-Agent": getRandomUserAgent() }
    });
    
    const $ = cheerio.load(res.data);
    
    $(".job-listing, .career-item, .job-card").each((_, el) => {
      const title = $(el).find("h3, .job-title, .title").text().trim();
      const location = $(el).find(".location, .job-location").text().trim();
      const link = $(el).find("a").attr("href") || "";
      
      if (title) {
        jobs.push({
          id: `ukg:${link || Math.random().toString(36).substr(2, 9)}`,
          source: "ukg",
          company: "UKG (Ultimate Kronos Group)",
          title,
          location: location || "Multiple Locations",
          url: link.startsWith("http") ? link : `https://www.ukg.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at UKG - HR/Payroll/Workforce Management`
        });
      }
    });
    
    console.log(`  Found ${jobs.length} UKG jobs`);
  } catch (e) {
    console.log(`  UKG error: ${e.message}`);
  }
  return jobs;
}

// ==================== GREENHOUSE (ATS PLATFORM) ====================
async function scrapeGreenhouseBoards() {
  const jobs = [];
  try {
    console.log("Searching Greenhouse job boards for HR companies...");
    
    // Greenhouse boards for HR tech companies
    const boards = [
      { company: "Rippling", board: "rippling" },
      { company: "Deel", board: "deel" },
      { company: "Lattice", board: "lattice" },
      { company: "Gusto", board: "gusto" }
    ];
    
    for (const { company, board } of boards) {
      try {
        const res = await axios.get(`https://boards.greenhouse.io/${board}`, {
          timeout: 10000,
          headers: { "User-Agent": getRandomUserAgent() }
        });
        
        const $ = cheerio.load(res.data);
        
        $(".opening, .job-posting").each((_, el) => {
          const title = $(el).find("a, .job-title, h3").text().trim();
          const location = $(el).find(".location, .job-location").text().trim();
          const link = $(el).find("a").attr("href") || "";
          
          if (title && (location.toLowerCase().includes("toronto") || location.toLowerCase().includes("canada") || location.toLowerCase().includes("remote"))) {
            jobs.push({
              id: `greenhouse:${company}:${link || Math.random().toString(36).substr(2, 9)}`,
              source: "greenhouse",
              company,
              title,
              location,
              url: link.startsWith("http") ? link : `https://boards.greenhouse.io${link}`,
              employmentType: "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: `${title} at ${company} - HR Tech via Greenhouse`
            });
          }
        });
        
        await sleep(500);
      } catch (e) {
        console.log(`  ${company} board failed: ${e.message}`);
      }
    }
    
    console.log(`  Found ${jobs.length} Greenhouse HR jobs`);
  } catch (e) {
    console.log(`  Greenhouse error: ${e.message}`);
  }
  return jobs;
}

// ==================== MAIN ====================
async function main() {
  console.log("🚀 SCRAPING HR PLATFORM CAREER PAGES\n");
  
  // Load existing jobs
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs\n`);
  } catch (e) {
    console.log("No existing jobs.json\n");
  }
  
  const allJobs = [...existingJobs];
  let newCount = 0;
  
  // Scrape from all HR platform career pages
  const scrapers = [
    { name: "Dayforce/Ceridian", fn: scrapeDayforceCareers },
    { name: "Workday", fn: scrapeWorkdayCareers },
    { name: "ADP", fn: scrapeADPCareers },
    { name: "SAP", fn: scrapeSAPCareers },
    { name: "UKG", fn: scrapeUKGCareers },
    { name: "Greenhouse", fn: scrapeGreenhouseBoards }
  ];
  
  for (const { name, fn } of scrapers) {
    const jobs = await fn();
    
    for (const job of jobs) {
      if (!existingIds.has(job.id)) {
        existingIds.add(job.id);
        allJobs.push(job);
        newCount++;
      }
    }
    
    await sleep(1000);
  }
  
  console.log(`\n========================================`);
  console.log(`HR PLATFORM CAREER SCRAPING COMPLETE`);
  console.log(`New jobs: ${newCount}`);
  console.log(`TOTAL: ${allJobs.length} jobs`);
  console.log(`========================================\n`);
  
  // Count by source
  const bySource = {};
  for (const j of allJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  console.log("By source:", bySource);
  
  // Save
  fs.writeFileSync("jobs.json", JSON.stringify({
    meta: {
      scrapedAt: new Date().toISOString(),
      totalFetched: allJobs.length,
      sources: Object.keys(bySource)
    },
    jobs: allJobs
  }, null, 2));
  
  console.log(`\n✅ Saved to jobs.json`);
}

main().catch(e => {
  console.error("Fatal error:", e);
  process.exit(1);
});
