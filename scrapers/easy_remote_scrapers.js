import axios from "axios";
import * as cheerio from "cheerio";
import Parser from "rss-parser";

const rssParser = new Parser({
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }
});

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ==================== WE WORK REMOTELY ====================
export async function fetchWeWorkRemotelyJobs() {
  const jobs = [];
  try {
    console.log("[WeWorkRemotely] Fetching jobs...");
    
    // Try RSS feed first (cleaner data)
    try {
      const feed = await rssParser.parseURL("https://weworkremotely.com/remote-jobs.rss");
      for (const item of feed.items || []) {
        jobs.push({
          id: `weworkremotely:${Buffer.from(item.title || '').toString('base64').substring(0, 20)}`,
          source: "weworkremotely",
          company: item.title?.split(":")[0]?.trim() || "Unknown",
          title: item.title?.split(":")[1]?.trim() || item.title,
          location: "Remote",
          url: item.link,
          employmentType: "remote",
          salary: null,
          postedDate: item.pubDate || new Date().toISOString(),
          excerpt: item.contentSnippet?.substring(0, 200) || item.title
        });
      }
    } catch (rssErr) {
      // Fallback to HTML scraping
      const res = await axios.get("https://weworkremotely.com/remote-jobs", {
        timeout: 15000,
        headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
      });
      
      const $ = cheerio.load(res.data);
      $(".job, .listing, article").each((_, el) => {
        const titleEl = $(el).find("h2 a, .title a, a[href*='/remote-jobs/']").first();
        const title = titleEl.text().trim();
        const link = titleEl.attr("href") || "";
        
        const companyEl = $(el).find(".company, .company-name").first();
        const company = companyEl.text().trim() || "Unknown";
        
        if (title) {
          jobs.push({
            id: `weworkremotely:${Buffer.from(title).toString('base64').substring(0, 20)}`,
            source: "weworkremotely",
            company,
            title,
            location: "Remote",
            url: link.startsWith("http") ? link : `https://weworkremotely.com${link}`,
            employmentType: "remote",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: title
          });
        }
      });
    }
    
    console.log(`[WeWorkRemotely] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[WeWorkRemotely] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== REMOTIVE ====================
export async function fetchRemotiveJobs() {
  const jobs = [];
  try {
    console.log("[Remotive] Fetching jobs...");
    
    // Remotive has a nice JSON API!
    const res = await axios.get("https://remotive.com/api/remote-jobs", {
      timeout: 15000,
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    });
    
    const jobList = res.data?.jobs || [];
    
    for (const job of jobList) {
      jobs.push({
        id: `remotive:${job.id || Math.random().toString(36).substr(2, 9)}`,
        source: "remotive",
        company: job.company_name || "Unknown",
        title: job.title,
        location: job.candidate_required_location || "Remote",
        url: job.url || job.apply_url,
        employmentType: job.job_type || "remote",
        salary: job.salary || null,
        postedDate: job.publication_date || new Date().toISOString(),
        excerpt: job.description?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
      });
    }
    
    console.log(`[Remotive] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[Remotive] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== JOBSPRESSO ====================
export async function fetchJobspressoJobs() {
  const jobs = [];
  try {
    console.log("[Jobspresso] Fetching jobs...");
    
    const res = await axios.get("https://jobspresso.co/?search_keywords=&search_location=&search_category=", {
      timeout: 15000,
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    });
    
    const $ = cheerio.load(res.data);
    $(".job-listing, .job, article").each((_, el) => {
      const titleEl = $(el).find("h3 a, .job-title a, a[href*='/job/']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".company, .company-name, .employer").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locEl = $(el).find(".location, .job-location").first();
      const location = locEl.text().trim() || "Remote";
      
      if (title) {
        jobs.push({
          id: `jobspresso:${Buffer.from(title).toString('base64').substring(0, 20)}`,
          source: "jobspresso",
          company,
          title,
          location,
          url: link.startsWith("http") ? link : `https://jobspresso.co${link}`,
          employmentType: "remote",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[Jobspresso] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[Jobspresso] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== REMOTE.CO ====================
export async function fetchRemoteCoJobs() {
  const jobs = [];
  try {
    console.log("[Remote.co] Fetching jobs...");
    
    const res = await axios.get("https://remote.co/remote-jobs/", {
      timeout: 15000,
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    });
    
    const $ = cheerio.load(res.data);
    $(".job-card, .job-listing, .card").each((_, el) => {
      const titleEl = $(el).find("h3 a, .job-title a, a[href*='/remote-jobs/']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".company, .company-name").first();
      const company = companyEl.text().trim() || "Unknown";
      
      if (title) {
        jobs.push({
          id: `remoteco:${Buffer.from(title).toString('base64').substring(0, 20)}`,
          source: "remoteco",
          company,
          title,
          location: "Remote",
          url: link.startsWith("http") ? link : `https://remote.co${link}`,
          employmentType: "remote",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[Remote.co] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[Remote.co] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== JUSTREMOTE ====================
export async function fetchJustRemoteJobs() {
  const jobs = [];
  try {
    console.log("[JustRemote] Fetching jobs...");
    
    const res = await axios.get("https://justremote.co/remote-jobs", {
      timeout: 15000,
      headers: { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" }
    });
    
    const $ = cheerio.load(res.data);
    $("[data-job], .job-item, .job-card").each((_, el) => {
      const titleEl = $(el).find("h3 a, .job-title a").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".company, .company-name").first();
      const company = companyEl.text().trim() || "Unknown";
      
      if (title) {
        jobs.push({
          id: `justremote:${Buffer.from(title).toString('base64').substring(0, 20)}`,
          source: "justremote",
          company,
          title,
          location: "Remote",
          url: link.startsWith("http") ? link : `https://justremote.co${link}`,
          employmentType: "remote",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[JustRemote] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[JustRemote] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== FETCH ALL REMOTE SOURCES ====================
export async function fetchAllEasyRemoteJobs() {
  console.log("\n🚀 FETCHING ALL EASY-TO-SCRAPE REMOTE SOURCES\n");
  
  const allJobs = [];
  
  const wwr = await fetchWeWorkRemotelyJobs();
  allJobs.push(...wwr);
  await sleep(1000);
  
  const remotive = await fetchRemotiveJobs();
  allJobs.push(...remotive);
  await sleep(1000);
  
  const jobspresso = await fetchJobspressoJobs();
  allJobs.push(...jobspresso);
  await sleep(1000);
  
  const remoteco = await fetchRemoteCoJobs();
  allJobs.push(...remoteco);
  await sleep(1000);
  
  const justremote = await fetchJustRemoteJobs();
  allJobs.push(...justremote);
  
  console.log(`\n========================================`);
  console.log(`EASY REMOTE SOURCES COMPLETE`);
  console.log(`Total remote jobs: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  return allJobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchAllEasyRemoteJobs()
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 5));
    })
    .catch(console.error);
}
