import axios from "axios";
import * as cheerio from "cheerio";
import fs from "fs";

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ==================== SOURCE 1: WorkBC (British Columbia Jobs) ====================
async function scrapeWorkBC() {
  const jobs = [];
  const seen = new Set();
  const KEYWORDS = ["software", "developer", "engineer", "analyst", "manager"];
  
  for (const keyword of KEYWORDS) {
    try {
      const url = `https://api.jobbank.gc.ca/v1/jobs?searchstring=${encodeURIComponent(keyword)}&locationprovince=59&pagesize=100`;
      const response = await axios.get(url, {
        headers: { "User-Agent": USER_AGENTS[0], "Accept": "application/json" },
        timeout: 10000
      });
      
      const results = response.data?.results || [];
      for (const job of results) {
        const id = `workbc:${job.id}`;
        if (!seen.has(id)) {
          seen.add(id);
          jobs.push({
            id,
            source: "workbc",
            company: job.employerName || "BC Employer",
            title: job.title,
            location: `${job.location?.city || "Various"}, BC`,
            url: job.url || `https://www.workbc.ca/Jobs/${job.id}`,
            employmentType: job.type || "full-time",
            salary: job.salary,
            postedDate: job.datePosted,
            excerpt: job.description?.substring(0, 200)
          });
        }
      }
      console.log(`[WorkBC] "${keyword}": ${jobs.length} jobs`);
      await sleep(500);
    } catch (e) {
      console.log(`[WorkBC] ${keyword}: ${e.message}`);
    }
  }
  return jobs;
}

// ==================== SOURCE 2: Ontario Job Bank (Direct scraping) ====================
async function scrapeOntarioJobs() {
  const jobs = [];
  const seen = new Set();
  
  try {
    // Ontario has a job bank at ontario.ca
    const url = "https://www.ontario.ca/page/jobs-and-employment";
    // Skip - need different approach
    
    // Try Ontario Job Bank RSS or API
    const apiUrl = "https://www.ontario.ca/api/jobs?limit=500";
    const response = await axios.get(apiUrl, {
      headers: { "User-Agent": USER_AGENTS[0] },
      timeout: 10000
    });
    
    const data = response.data?.jobs || [];
    for (const job of data) {
      const id = `ontario:${job.id}`;
      if (!seen.has(id)) {
        seen.add(id);
        jobs.push({
          id,
          source: "ontario",
          company: job.employer || "Ontario Government",
          title: job.title,
          location: job.location || "Ontario",
          url: job.url,
          employmentType: "full-time",
          salary: job.salary,
          postedDate: job.posted,
          excerpt: job.description?.substring(0, 200)
        });
      }
    }
  } catch (e) {
    console.log(`[Ontario] error: ${e.message}`);
  }
  
  console.log(`[Ontario] Total: ${jobs.length} jobs`);
  return jobs;
}

// ==================== SOURCE 3: Eluta.ca (Canadian Job Search) ====================
async function scrapeEluta() {
  const jobs = [];
  const seen = new Set();
  const KEYWORDS = ["software", "developer", "engineer", "manager", "analyst"];
  
  for (const keyword of KEYWORDS) {
    try {
      const url = `https://www.eluta.ca/search?f=${encodeURIComponent(keyword)}&l=Toronto&s=date`;
      const response = await axios.get(url, {
        headers: { 
          "User-Agent": USER_AGENTS[0],
          "Accept": "text/html"
        },
        timeout: 10000
      });
      
      const $ = cheerio.load(response.data);
      $("[data-job-id], .job-item, article").each((_, el) => {
        const $el = $(el);
        const title = $el.find("h2, .job-title, a[title]").first().text().trim() || $el.find("a").first().attr("title");
        const company = $el.find(".company, .employer").first().text().trim();
        const link = $el.find("a[href]").first().attr("href");
        
        if (title && !seen.has(title + company)) {
          seen.add(title + company);
          jobs.push({
            id: `eluta:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
            source: "eluta",
            company: company || "Unknown",
            title,
            location: "Toronto, ON",
            url: link?.startsWith("http") ? link : `https://www.eluta.ca${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"}`
          });
        }
      });
      
      console.log(`[Eluta] "${keyword}": ${jobs.length} jobs`);
      await sleep(1000);
    } catch (e) {
      console.log(`[Eluta] ${keyword}: ${e.message}`);
    }
  }
  return jobs;
}

// ==================== SOURCE 4: Jobillico (Quebec/Canada) ====================
async function scrapeJobillico() {
  const jobs = [];
  const seen = new Set();
  
  try {
    const url = "https://www.jobillico.com/api/jobs?location=toronto&limit=500";
    const response = await axios.get(url, {
      headers: { "User-Agent": USER_AGENTS[0], "Accept": "application/json" },
      timeout: 10000
    });
    
    const data = response.data?.jobs || [];
    for (const job of data) {
      const id = `jobillico:${job.id}`;
      if (!seen.has(id)) {
        seen.add(id);
        jobs.push({
          id,
          source: "jobillico",
          company: job.company,
          title: job.title,
          location: job.location || "Toronto, ON",
          url: job.url,
          employmentType: job.type || "full-time",
          salary: job.salary,
          postedDate: job.posted,
          excerpt: job.description?.substring(0, 200)
        });
      }
    }
    console.log(`[Jobillico]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Jobillico] error: ${e.message}`);
  }
  return jobs;
}

// ==================== SOURCE 5: Talent.com (formerly Neuvoo) ====================
async function scrapeTalent() {
  const jobs = [];
  const seen = new Set();
  const KEYWORDS = ["software", "developer", "engineer"];
  
  for (const keyword of KEYWORDS) {
    try {
      const url = `https://ca.talent.com/api/jobs?k=${encodeURIComponent(keyword)}&l=Toronto&page=1`;
      const response = await axios.get(url, {
        headers: { "User-Agent": USER_AGENTS[0] },
        timeout: 10000
      });
      
      const data = response.data?.jobs || [];
      for (const job of data) {
        const id = `talent:${job.id || Math.random()}`;
        if (!seen.has(id)) {
          seen.add(id);
          jobs.push({
            id,
            source: "talent",
            company: job.company,
            title: job.title,
            location: job.location || "Toronto, ON",
            url: job.url,
            employmentType: "full-time",
            salary: job.salary,
            postedDate: new Date().toISOString(),
            excerpt: job.description?.substring(0, 200)
          });
        }
      }
      console.log(`[Talent] "${keyword}": ${jobs.length} jobs`);
      await sleep(1000);
    } catch (e) {
      console.log(`[Talent] error: ${e.message}`);
    }
  }
  return jobs;
}

// ==================== SOURCE 6: Adzuna API (if key available) ====================
async function scrapeAdzuna() {
  const jobs = [];
  
  // Check if API key is available
  const appId = process.env.ADZUNA_APP_ID;
  const apiKey = process.env.ADZUNA_API_KEY;
  
  if (!appId || !apiKey) {
    console.log("[Adzuna] No API credentials - skipping");
    return jobs;
  }
  
  try {
    const url = `https://api.adzuna.com/v1/api/jobs/ca/search/1?app_id=${appId}&app_key=${apiKey}&what=software&where=toronto&results_per_page=100`;
    const response = await axios.get(url, { timeout: 10000 });
    
    const data = response.data?.results || [];
    for (const job of data) {
      jobs.push({
        id: `adzuna:${job.id}`,
        source: "adzuna",
        company: job.company?.display_name,
        title: job.title,
        location: job.location?.display_name,
        url: job.redirect_url,
        employmentType: "full-time",
        salary: job.salary_min ? { min: job.salary_min, max: job.salary_max } : null,
        postedDate: job.created_at,
        excerpt: job.description?.substring(0, 200)
      });
    }
    console.log(`[Adzuna]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Adzuna] error: ${e.message}`);
  }
  return jobs;
}

// ==================== SOURCE 7: SerpAPI (Google Jobs) ====================
async function scrapeSerpAPI() {
  const jobs = [];
  
  const apiKey = process.env.SERPAPI_KEY;
  if (!apiKey) {
    console.log("[SerpAPI] No API key - skipping");
    return jobs;
  }
  
  const KEYWORDS = ["software developer", "data analyst", "project manager"];
  
  for (const keyword of KEYWORDS) {
    try {
      const url = `https://serpapi.com/search.json?engine=google_jobs&q=${encodeURIComponent(keyword + " Toronto")}&location=Toronto&api_key=${apiKey}`;
      const response = await axios.get(url, { timeout: 15000 });
      
      const data = response.data?.jobs_results || [];
      for (const job of data) {
        jobs.push({
          id: `serpapi:${job.job_id}`,
          source: "serpapi",
          company: job.company_name,
          title: job.title,
          location: job.location,
          url: job.apply_link || job.share_link,
          employmentType: job.detected_extensions?.schedule_type || "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: job.description?.substring(0, 200)
        });
      }
      console.log(`[SerpAPI] "${keyword}": ${jobs.length} jobs`);
      await sleep(1000);
    } catch (e) {
      console.log(`[SerpAPI] error: ${e.message}`);
    }
  }
  return jobs;
}

// ==================== SOURCE 8: JSearch API (RapidAPI) ====================
async function scrapeJSearch() {
  const jobs = [];
  
  const apiKey = process.env.RAPIDAPI_KEY || process.env.JSEARCH_API_KEY;
  if (!apiKey) {
    console.log("[JSearch] No API key - skipping");
    return jobs;
  }
  
  try {
    const url = "https://jsearch.p.rapidapi.com/search?query=software+developer+in+Toronto&page=1&num_pages=5";
    const response = await axios.get(url, {
      headers: {
        "X-RapidAPI-Key": apiKey,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
      },
      timeout: 15000
    });
    
    const data = response.data?.data || [];
    for (const job of data) {
      jobs.push({
        id: `jsearch:${job.job_id}`,
        source: "jsearch",
        company: job.employer_name,
        title: job.job_title,
        location: job.job_city || "Toronto",
        url: job.job_apply_link || job.job_google_link,
        employmentType: job.job_employment_type || "full-time",
        salary: job.job_min_salary ? { min: job.job_min_salary, max: job.job_max_salary } : null,
        postedDate: job.job_posted_at_datetime_utc,
        excerpt: job.job_description?.substring(0, 200)
      });
    }
    console.log(`[JSearch]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[JSearch] error: ${e.message}`);
  }
  return jobs;
}

// ==================== SOURCE 9: JobSpider ====================
async function scrapeJobSpider() {
  const jobs = [];
  const seen = new Set();
  
  try {
    const url = "https://www.jobspider.com/job/search?keywords=software&location=Toronto";
    const response = await axios.get(url, {
      headers: { "User-Agent": USER_AGENTS[0] },
      timeout: 10000
    });
    
    const $ = cheerio.load(response.data);
    $(".job-listing, .job-item").each((_, el) => {
      const $el = $(el);
      const title = $el.find("h3, .title, a").first().text().trim();
      const company = $el.find(".company, .employer").first().text().trim();
      const link = $el.find("a[href]").first().attr("href");
      
      if (title && !seen.has(title + company)) {
        seen.add(title + company);
        jobs.push({
          id: `jobspider:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
          source: "jobspider",
          company: company || "Unknown",
          title,
          location: "Toronto, ON",
          url: link?.startsWith("http") ? link : `https://www.jobspider.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at ${company || "Unknown"}`
        });
      }
    });
    console.log(`[JobSpider]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[JobSpider] error: ${e.message}`);
  }
  return jobs;
}

// ==================== SOURCE 10: Canada Job Directory ====================
async function scrapeCanadaJobs() {
  const jobs = [];
  const seen = new Set();
  
  try {
    const url = "https://www.canadajobs.com/jobs/search?keywords=software&location=toronto";
    const response = await axios.get(url, {
      headers: { "User-Agent": USER_AGENTS[0] },
      timeout: 10000
    });
    
    const $ = cheerio.load(response.data);
    $(".job-listing, .job-card").each((_, el) => {
      const $el = $(el);
      const title = $el.find("h2, .job-title").first().text().trim();
      const company = $el.find(".company-name").first().text().trim();
      const link = $el.find("a[href]").first().attr("href");
      
      if (title && !seen.has(title + company)) {
        seen.add(title + company);
        jobs.push({
          id: `canadajobs:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
          source: "canadajobs",
          company: company || "Unknown",
          title,
          location: "Toronto, ON",
          url: link?.startsWith("http") ? link : `https://www.canadajobs.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at ${company || "Unknown"}`
        });
      }
    });
    console.log(`[CanadaJobs]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[CanadaJobs] error: ${e.message}`);
  }
  return jobs;
}

// ==================== MAIN ====================
async function main() {
  console.log("🚀 PROVINCIAL & API JOB SCRAPER - Target: 10,000 jobs\n");
  console.log("Sources: WorkBC, Ontario, Eluta, Jobillico, Talent.com, Adzuna, SerpAPI, JSearch, JobSpider, CanadaJobs\n");
  
  const allJobs = [];
  const seen = new Set();
  
  // Run all scrapers
  const results = await Promise.allSettled([
    scrapeWorkBC(),
    scrapeOntarioJobs(),
    scrapeEluta(),
    scrapeJobillico(),
    scrapeTalent(),
    scrapeAdzuna(),
    scrapeSerpAPI(),
    scrapeJSearch(),
    scrapeJobSpider(),
    scrapeCanadaJobs()
  ]);
  
  for (const result of results) {
    if (result.status === "fulfilled") {
      for (const job of result.value) {
        if (!seen.has(job.id)) {
          seen.add(job.id);
          allJobs.push(job);
        }
      }
    }
  }
  
  console.log(`\n========================================`);
  console.log(`New jobs scraped: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  // Load existing
  let existingJobs = [];
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    console.log(`Loaded ${existingJobs.length} existing jobs`);
  } catch (e) {}
  
  // Merge
  const merged = [...existingJobs, ...allJobs];
  const finalSeen = new Set();
  const finalJobs = merged.filter(j => {
    if (finalSeen.has(j.id)) return false;
    finalSeen.add(j.id);
    return true;
  });
  
  // Count by source
  const bySource = {};
  for (const j of finalJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  
  console.log(`\n🎯 FINAL: ${finalJobs.length} total jobs`);
  console.log("By source:", bySource);
  
  // Save
  fs.writeFileSync("jobs.json", JSON.stringify({
    meta: {
      scrapedAt: new Date().toISOString(),
      totalFetched: finalJobs.length,
      sources: Object.keys(bySource)
    },
    jobs: finalJobs
  }, null, 2));
  
  console.log(`\n✅ Saved to jobs.json`);
  console.log(`\n📊 Progress: ${finalJobs.length}/10,000 (${((finalJobs.length/10000)*100).toFixed(1)}%)`);
  
  if (finalJobs.length < 10000) {
    console.log(`📊 Need ${10000 - finalJobs.length} more jobs`);
    console.log(`\n💡 TIP: Set API keys for more sources:`);
    console.log(`   - ADZUNA_APP_ID + ADZUNA_API_KEY`);
    console.log(`   - SERPAPI_KEY`);
    console.log(`   - RAPIDAPI_KEY (for JSearch)`);
  } else {
    console.log(`\n🎉🎉🎉 REACHED 10,000 JOBS! 🎉🎉🎉`);
  }
}

main();
