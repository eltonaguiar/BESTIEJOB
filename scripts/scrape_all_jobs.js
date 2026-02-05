import * as cheerio from "cheerio";
import axios from "axios";
import fs from "fs";

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

function getRandomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchHtml(url) {
  try {
    await sleep(1000 + Math.random() * 2000);
    const response = await axios.get(url, {
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
      },
      timeout: 15000,
      maxRedirects: 5
    });
    return response.data;
  } catch (error) {
    console.warn(`Fetch failed: ${error.message}`);
    return null;
  }
}

async function scrapeJobBank(keyword) {
  const jobs = [];
  try {
    const searchTerm = encodeURIComponent(keyword);
    const url = `https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=${searchTerm}&locationstring=Toronto%2C+ON`;
    const html = await fetchHtml(url);
    if (!html) return jobs;
    
    const $ = cheerio.load(html);
    $("a.resultJobItem").each((_, el) => {
      const title = $(el).find("span.noctitle").text().trim();
      const company = $(el).find("span.business").text().trim();
      const location = $(el).find("span.location").text().trim();
      const urlPath = $(el).attr("href");
      
      if (title && urlPath) {
        const jobId = urlPath.split("/").pop()?.split(";")[0] || Math.random().toString(36);
        jobs.push({
          id: `jobbank:${jobId}`,
          source: "jobbank",
          company: company || "Government of Canada",
          title,
          location: location || "Toronto, ON",
          url: urlPath.startsWith("http") ? urlPath : `https://www.jobbank.gc.ca${urlPath}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    console.log(`[JobBank] "${keyword}": ${jobs.length} jobs`);
  } catch (e) {
    console.warn(`[JobBank] Error:`, e.message);
  }
  return jobs;
}

async function scrapeTorontoJobs() {
  const jobs = [];
  try {
    const url = "https://www.toronto.ca/city-government/jobs-opportunities/current-job-postings/";
    const html = await fetchHtml(url);
    if (!html) return jobs;
    
    const $ = cheerio.load(html);
    $(".job-posting, .job-item, .position-item").each((_, el) => {
      const title = $(el).find("h3, .job-title, a").text().trim();
      const urlPath = $(el).find("a").attr("href");
      
      if (title && urlPath) {
        jobs.push({
          id: `toronto:${urlPath.split("/").pop() || Math.random().toString(36)}`,
          source: "toronto",
          company: "City of Toronto",
          title,
          location: "Toronto, ON",
          url: urlPath.startsWith("http") ? urlPath : `https://www.toronto.ca${urlPath}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    console.log(`[Toronto.ca] Found ${jobs.length} jobs`);
  } catch (e) {
    console.warn(`[Toronto.ca] Error:`, e.message);
  }
  return jobs;
}

// Keywords to search
const KEYWORDS = [
  "software developer",
  "software engineer", 
  "web developer",
  "programmer",
  "data analyst",
  "business analyst",
  "project manager",
  "product manager",
  "UX designer",
  "QA tester",
  "devops engineer",
  "systems administrator",
  "network administrator",
  "database administrator",
  "IT support",
  "help desk",
  "technical support",
  "customer service",
  "sales representative",
  "marketing coordinator",
  "account manager",
  "financial analyst",
  "accountant",
  "human resources",
  "administrative assistant",
  "executive assistant",
  "office manager",
  "operations manager"
];

async function main() {
  console.log("Scraping REAL jobs from Canadian sources...\n");
  
  const allJobs = [];
  const seen = new Set();
  
  // Scrape JobBank with multiple keywords
  for (const keyword of KEYWORDS) {
    const jobs = await scrapeJobBank(keyword);
    for (const job of jobs) {
      if (!seen.has(job.id)) {
        seen.add(job.id);
        allJobs.push(job);
      }
    }
    await sleep(500); // Be nice to the server
  }
  
  // Also try Toronto city jobs
  const torontoJobs = await scrapeTorontoJobs();
  for (const job of torontoJobs) {
    if (!seen.has(job.id)) {
      seen.add(job.id);
      allJobs.push(job);
    }
  }
  
  console.log(`\n========================================`);
  console.log(`TOTAL REAL JOBS: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  if (allJobs.length > 0) {
    console.log("Sample jobs:");
    allJobs.slice(0, 10).forEach(j => {
      console.log(`- ${j.title} @ ${j.company}`);
    });
    
    // Save to jobs.json
    fs.writeFileSync("jobs.json", JSON.stringify({
      meta: {
        scrapedAt: new Date().toISOString(),
        totalFetched: allJobs.length,
        sources: ["jobbank", "toronto"]
      },
      jobs: allJobs
    }, null, 2));
    
    console.log(`\n✅ Saved ${allJobs.length} REAL jobs to jobs.json`);
  } else {
    console.log("❌ No jobs found");
    process.exit(1);
  }
}

main();
