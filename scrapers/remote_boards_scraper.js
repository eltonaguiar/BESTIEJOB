import axios from "axios";
import * as cheerio from "cheerio";

/**
 * Aggregator for smaller remote job boards
 * RemoteYeah, Nixa, OkJob/4DayWeek, Pangian, PowerToFly
 */

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ==================== REMOTEAH ====================
export async function fetchRemoteYeahJobs() {
  const jobs = [];
  try {
    console.log("[RemoteYeah] Fetching jobs...");
    const res = await axios.get("https://remoteyeah.com/jobs", {
      timeout: 15000,
      headers: { "User-Agent": USER_AGENTS[0] }
    });
    
    const $ = cheerio.load(res.data);
    $("[data-job], .job-item, .job-card").each((_, el) => {
      const titleEl = $(el).find("h2 a, .job-title a, a[href*='job']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".company, .company-name").first();
      const company = companyEl.text().trim() || "Unknown";
      
      if (title) {
        jobs.push({
          id: `remoteyeah:${Buffer.from(title).toString('base64').substring(0, 15)}`,
          source: "remoteyeah",
          company,
          title,
          location: "Remote",
          url: link.startsWith("http") ? link : `https://remoteyeah.com${link}`,
          employmentType: "remote",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[RemoteYeah] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[RemoteYeah] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== 4 DAY WEEK (OkJob) ====================
export async function fetch4DayWeekJobs() {
  const jobs = [];
  try {
    console.log("[4DayWeek] Fetching jobs...");
    const res = await axios.get("https://4dayweek.io/jobs", {
      timeout: 15000,
      headers: { "User-Agent": USER_AGENTS[0] }
    });
    
    const $ = cheerio.load(res.data);
    $(".job-listing, .job-card, [data-job]").each((_, el) => {
      const titleEl = $(el).find("h3 a, h2 a, .job-title").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || $(el).find("a").first().attr("href") || "";
      
      const companyEl = $(el).find(".company, .employer").first();
      const company = companyEl.text().trim() || "Unknown";
      
      if (title) {
        jobs.push({
          id: `4dayweek:${Buffer.from(title).toString('base64').substring(0, 15)}`,
          source: "4dayweek",
          company,
          title,
          location: "Remote / 4-Day Work Week",
          url: link.startsWith("http") ? link : `https://4dayweek.io${link}`,
          employmentType: "4-day week",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} - 4 day work week opportunity`
        });
      }
    });
    
    console.log(`[4DayWeek] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[4DayWeek] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== PANGIAN ====================
export async function fetchPangianJobs() {
  const jobs = [];
  try {
    console.log("[Pangian] Fetching jobs...");
    const res = await axios.get("https://pangian.com/job-portal/", {
      timeout: 15000,
      headers: { "User-Agent": USER_AGENTS[0] }
    });
    
    const $ = cheerio.load(res.data);
    $(".job, .job-listing, article").each((_, el) => {
      const titleEl = $(el).find("h2 a, .job-title a, a[href*='job']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".company, .employer").first();
      const company = companyEl.text().trim() || "Unknown";
      
      if (title) {
        jobs.push({
          id: `pangian:${Buffer.from(title).toString('base64').substring(0, 15)}`,
          source: "pangian",
          company,
          title,
          location: "Remote (Global)",
          url: link,
          employmentType: "remote",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[Pangian] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[Pangian] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== POWERTOFLY ====================
export async function fetchPowerToFlyJobs() {
  const jobs = [];
  try {
    console.log("[PowerToFly] Fetching jobs...");
    const res = await axios.get("https://powertofly.com/jobs/", {
      timeout: 15000,
      headers: { "User-Agent": USER_AGENTS[0] }
    });
    
    const $ = cheerio.load(res.data);
    $(".job-card, .job-listing, [data-job]").each((_, el) => {
      const titleEl = $(el).find("h3 a, .job-title a").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".company-name, .employer").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locEl = $(el).find(".location, .job-location").first();
      const location = locEl.text().trim() || "Remote";
      
      if (title) {
        jobs.push({
          id: `powertofly:${Buffer.from(title).toString('base64').substring(0, 15)}`,
          source: "powertofly",
          company,
          title,
          location,
          url: link.startsWith("http") ? link : `https://powertofly.com${link}`,
          employmentType: "remote",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} - Diverse & inclusive workplace via PowerToFly`
        });
      }
    });
    
    console.log(`[PowerToFly] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[PowerToFly] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== FETCH ALL REMOTE BOARDS ====================
export async function fetchAllRemoteBoards() {
  console.log("\n🚀 FETCHING REMOTE JOB BOARDS\n");
  
  const allJobs = [];
  
  const remoteYeah = await fetchRemoteYeahJobs();
  allJobs.push(...remoteYeah);
  
  await sleep(500);
  
  const fourDayWeek = await fetch4DayWeekJobs();
  allJobs.push(...fourDayWeek);
  
  await sleep(500);
  
  const pangian = await fetchPangianJobs();
  allJobs.push(...pangian);
  
  await sleep(500);
  
  const powerToFly = await fetchPowerToFlyJobs();
  allJobs.push(...powerToFly);
  
  console.log(`\n========================================`);
  console.log(`REMOTE BOARDS FETCH COMPLETE`);
  console.log(`Total remote jobs: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  return allJobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchAllRemoteBoards()
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 5));
    })
    .catch(console.error);
}
