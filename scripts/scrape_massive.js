import axios from "axios";
import * as cheerio from "cheerio";
import fs from "fs";

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

function getRandomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchHtml(url, retries = 2) {
  for (let i = 0; i < retries; i++) {
    try {
      await sleep(1500 + Math.random() * 2000);
      const response = await axios.get(url, {
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Language": "en-US,en;q=0.5",
          "Accept-Encoding": "gzip, deflate",
          "Referer": "https://www.google.com/"
        },
        timeout: 15000,
        maxRedirects: 5
      });
      return response.data;
    } catch (error) {
      if (i === retries - 1) {
        console.warn(`Fetch failed: ${url} - ${error.message}`);
        return null;
      }
      await sleep(2000);
    }
  }
  return null;
}

// ==================== SOURCE 1: ZipRecruiter ====================
async function scrapeZipRecruiter(keywords) {
  const jobs = [];
  const seen = new Set();
  
  for (const keyword of keywords.slice(0, 5)) {
    try {
      const url = `https://www.ziprecruiter.com/jobs-search?search=${encodeURIComponent(keyword)}&location=Toronto%2C+ON`;
      const html = await fetchHtml(url);
      if (!html) continue;
      
      const $ = cheerio.load(html);
      
      $("article.job-listing, .job-listing, [data-testid='job-listing']").each((_, el) => {
        const $el = $(el);
        const title = $el.find("h2, .job-title, [data-testid='job-title']").first().text().trim();
        const company = $el.find(".company-name, [data-testid='company-name']").first().text().trim();
        const location = $el.find(".location, [data-testid='location']").first().text().trim() || "Toronto, ON";
        const link = $el.find("a[href*='jobs']").first().attr("href");
        
        if (title && !seen.has(title + company)) {
          seen.add(title + company);
          jobs.push({
            id: `ziprecruiter:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
            source: "ziprecruiter",
            company: company || "Unknown",
            title,
            location,
            url: link?.startsWith("http") ? link : `https://www.ziprecruiter.com${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"}`
          });
        }
      });
      
      console.log(`[ZipRecruiter] "${keyword}": ${jobs.length} total`);
      await sleep(2000);
    } catch (e) {
      console.log(`[ZipRecruiter] "${keyword}" error: ${e.message}`);
    }
  }
  
  return jobs;
}

// ==================== SOURCE 2: SimplyHired ====================
async function scrapeSimplyHired(keywords) {
  const jobs = [];
  const seen = new Set();
  
  for (const keyword of keywords.slice(0, 5)) {
    try {
      const url = `https://www.simplyhired.ca/search?q=${encodeURIComponent(keyword)}&l=Toronto%2C+ON`;
      const html = await fetchHtml(url);
      if (!html) continue;
      
      const $ = cheerio.load(html);
      
      $("[data-testid='searchSerpJob'], .SerpJob, .job-card").each((_, el) => {
        const $el = $(el);
        const title = $el.find("h2, .job-title, [data-testid='jobTitle']").first().text().trim();
        const company = $el.find(".company-name, [data-testid='companyName']").first().text().trim();
        const location = $el.find(".job-location, [data-testid='jobLocation']").first().text().trim() || "Toronto, ON";
        const link = $el.find("a[href*='/job/']").first().attr("href");
        
        if (title && !seen.has(title + company)) {
          seen.add(title + company);
          jobs.push({
            id: `simplyhired:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
            source: "simplyhired",
            company: company || "Unknown",
            title,
            location,
            url: link?.startsWith("http") ? link : `https://www.simplyhired.ca${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"}`
          });
        }
      });
      
      console.log(`[SimplyHired] "${keyword}": ${jobs.length} total`);
      await sleep(2000);
    } catch (e) {
      console.log(`[SimplyHired] "${keyword}" error: ${e.message}`);
    }
  }
  
  return jobs;
}

// ==================== SOURCE 3: CareerBuilder ====================
async function scrapeCareerBuilder(keywords) {
  const jobs = [];
  const seen = new Set();
  
  for (const keyword of keywords.slice(0, 4)) {
    try {
      const url = `https://www.careerbuilder.com/jobs?keywords=${encodeURIComponent(keyword)}&location=Toronto%2C+ON`;
      const html = await fetchHtml(url);
      if (!html) continue;
      
      const $ = cheerio.load(html);
      
      $("[data-job-id], .job-row, .data-results").each((_, el) => {
        const $el = $(el);
        const title = $el.find("h2, .job-title, .data-results-title").first().text().trim();
        const company = $el.find(".company-name, .data-results-company").first().text().trim();
        const location = $el.find(".job-location, .data-results-location").first().text().trim() || "Toronto, ON";
        const link = $el.find("a[href*='/job/']").first().attr("href");
        
        if (title && !seen.has(title + company)) {
          seen.add(title + company);
          jobs.push({
            id: `careerbuilder:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
            source: "careerbuilder",
            company: company || "Unknown",
            title,
            location,
            url: link?.startsWith("http") ? link : `https://www.careerbuilder.com${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"}`
          });
        }
      });
      
      console.log(`[CareerBuilder] "${keyword}": ${jobs.length} total`);
      await sleep(2000);
    } catch (e) {
      console.log(`[CareerBuilder] "${keyword}" error: ${e.message}`);
    }
  }
  
  return jobs;
}

// ==================== SOURCE 4: Monster.ca ====================
async function scrapeMonster(keywords) {
  const jobs = [];
  const seen = new Set();
  
  for (const keyword of keywords.slice(0, 4)) {
    try {
      const url = `https://www.monster.ca/jobs/search?q=${encodeURIComponent(keyword)}&where=Toronto__2C-Ontario`;
      const html = await fetchHtml(url);
      if (!html) continue;
      
      const $ = cheerio.load(html);
      
      $("[data-testid='jobTitle'], .job-cardstyle__JobCardComponent").each((_, el) => {
        const $el = $(el);
        const title = $el.find("h3, .job-title, a[data-testid='jobTitle']").first().text().trim();
        const company = $el.find(".company-name, [data-testid='company']").first().text().trim();
        const location = $el.find(".location, [data-testid='jobDetailLocation']").first().text().trim() || "Toronto, ON";
        const link = $el.find("a[href*='/jobs/']").first().attr("href");
        
        if (title && !seen.has(title + company)) {
          seen.add(title + company);
          jobs.push({
            id: `monster:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
            source: "monster",
            company: company || "Unknown",
            title,
            location,
            url: link?.startsWith("http") ? link : `https://www.monster.ca${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"}`
          });
        }
      });
      
      console.log(`[Monster] "${keyword}": ${jobs.length} total`);
      await sleep(2000);
    } catch (e) {
      console.log(`[Monster] "${keyword}" error: ${e.message}`);
    }
  }
  
  return jobs;
}

// ==================== SOURCE 5: Workopolis (Canadian) ====================
async function scrapeWorkopolis(keywords) {
  const jobs = [];
  const seen = new Set();
  
  for (const keyword of keywords.slice(0, 4)) {
    try {
      const url = `https://www.workopolis.com/jobsearch/find-jobs?ak=${encodeURIComponent(keyword)}&l=Toronto%2C+ON`;
      const html = await fetchHtml(url);
      if (!html) continue;
      
      const $ = cheerio.load(html);
      
      $("[data-testid='job-listing'], .JobCard, article").each((_, el) => {
        const $el = $(el);
        const title = $el.find("h2, .job-title, a[title]").first().text().trim() || $el.find("a").first().attr("title");
        const company = $el.find(".company-name, [data-testid='company-name']").first().text().trim();
        const location = $el.find(".location, [data-testid='job-location']").first().text().trim() || "Toronto, ON";
        const link = $el.find("a[href*='/job/']").first().attr("href");
        
        if (title && !seen.has(title + company)) {
          seen.add(title + company);
          jobs.push({
            id: `workopolis:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
            source: "workopolis",
            company: company || "Unknown",
            title,
            location,
            url: link?.startsWith("http") ? link : `https://www.workopolis.com${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"}`
          });
        }
      });
      
      console.log(`[Workopolis] "${keyword}": ${jobs.length} total`);
      await sleep(2000);
    } catch (e) {
      console.log(`[Workopolis] "${keyword}" error: ${e.message}`);
    }
  }
  
  return jobs;
}

// ==================== SOURCE 6: Glassdoor (Public API) ====================
async function scrapeGlassdoor(keywords) {
  const jobs = [];
  const seen = new Set();
  
  for (const keyword of keywords.slice(0, 3)) {
    try {
      // Glassdoor has a public job search endpoint
      const url = `https://www.glassdoor.ca/Job/toronto-${keyword.replace(/\s+/g, "-")}-jobs-SRCH_IL.0,7_IC2286069_KO8,${8 + keyword.length}.htm`;
      const html = await fetchHtml(url);
      if (!html) continue;
      
      const $ = cheerio.load(html);
      
      $("[data-test='job-listing'], .react-job-listing, .jobContainer").each((_, el) => {
        const $el = $(el);
        const title = $el.find("a.job-title, [data-test='job-title']").first().text().trim();
        const company = $el.find(".employer-name, [data-test='employer-name']").first().text().trim();
        const location = $el.find(".location, [data-test='location']").first().text().trim() || "Toronto, ON";
        const link = $el.find("a[href*='/job/']").first().attr("href");
        
        if (title && !seen.has(title + company)) {
          seen.add(title + company);
          jobs.push({
            id: `glassdoor:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
            source: "glassdoor",
            company: company || "Unknown",
            title,
            location,
            url: link?.startsWith("http") ? link : `https://www.glassdoor.ca${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"}`
          });
        }
      });
      
      console.log(`[Glassdoor] "${keyword}": ${jobs.length} total`);
      await sleep(3000);
    } catch (e) {
      console.log(`[Glassdoor] "${keyword}" error: ${e.message}`);
    }
  }
  
  return jobs;
}

// ==================== SOURCE 7: Wellfound (AngelList) ====================
async function scrapeWellfound(keywords) {
  const jobs = [];
  const seen = new Set();
  
  for (const keyword of keywords.slice(0, 3)) {
    try {
      const url = `https://wellfound.com/role/r/${encodeURIComponent(keyword)}/toronto-canada`;
      const html = await fetchHtml(url);
      if (!html) continue;
      
      const $ = cheerio.load(html);
      
      $("[data-testid='startup-job'], .job-listing, .styles_component").each((_, el) => {
        const $el = $(el);
        const title = $el.find("h3, .title, a[data-testid='job-title']").first().text().trim();
        const company = $el.find(".company-name, [data-testid='company-name']").first().text().trim();
        const location = $el.find(".location").first().text().trim() || "Toronto, ON";
        const link = $el.find("a[href*='/jobs/']").first().attr("href");
        
        if (title && !seen.has(title + company)) {
          seen.add(title + company);
          jobs.push({
            id: `wellfound:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
            source: "wellfound",
            company: company || "Unknown",
            title,
            location,
            url: link?.startsWith("http") ? link : `https://wellfound.com${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"} (Startup)`
          });
        }
      });
      
      console.log(`[Wellfound] "${keyword}": ${jobs.length} total`);
      await sleep(2000);
    } catch (e) {
      console.log(`[Wellfound] "${keyword}" error: ${e.message}`);
    }
  }
  
  return jobs;
}

// ==================== SOURCE 8: WeWorkRemotely ====================
async function scrapeWeWorkRemotely() {
  const jobs = [];
  try {
    const url = "https://weworkremotely.com/remote-jobs/search?term=software&commit=Search";
    const html = await fetchHtml(url);
    if (!html) return jobs;
    
    const $ = cheerio.load(html);
    
    $("li.new-listing-container, .job").each((_, el) => {
      const $el = $(el);
      const title = $el.find("h4, .title, a span").first().text().trim();
      const company = $el.find(".company, .company-name").first().text().trim();
      const link = $el.find("a[href*='/remote-jobs/']").first().attr("href");
      
      if (title) {
        jobs.push({
          id: `weworkremotely:${Date.now()}-${Math.random().toString(36).substr(2, 5)}`,
          source: "weworkremotely",
          company: company || "Unknown",
          title,
          location: "Remote",
          url: link?.startsWith("http") ? link : `https://weworkremotely.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at ${company || "Unknown"} (Remote)`
        });
      }
    });
    
    console.log(`[WeWorkRemotely]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[WeWorkRemotely] error: ${e.message}`);
  }
  return jobs;
}

// ==================== SOURCE 9: RemoteOK ====================
async function scrapeRemoteOK() {
  const jobs = [];
  try {
    const url = "https://remoteok.com/api?tag=software";
    const response = await axios.get(url, {
      headers: { "User-Agent": getRandomUA() },
      timeout: 15000
    });
    
    const data = Array.isArray(response.data) ? response.data.slice(1) : [];
    
    for (const job of data.slice(0, 50)) {
      if (job.position) {
        jobs.push({
          id: `remoteok:${job.id || Date.now()}`,
          source: "remoteok",
          company: job.company || "Unknown",
          title: job.position,
          location: "Remote",
          url: job.apply_url || job.url || `https://remoteok.com`,
          employmentType: "full-time",
          salary: job.salary ? { min: parseInt(job.salary) * 1000, max: parseInt(job.salary) * 1000 } : null,
          postedDate: new Date().toISOString(),
          excerpt: job.description?.substring(0, 240) || `${job.position} at ${job.company}`
        });
      }
    }
    
    console.log(`[RemoteOK]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[RemoteOK] error: ${e.message}`);
  }
  return jobs;
}

// ==================== SOURCE 10: HackerNews WhoIsHiring ====================
async function scrapeHackerNews() {
  const jobs = [];
  try {
    // Get latest "Who is hiring?" post
    const searchUrl = "https://hn.algolia.com/api/v1/search?query=who+is+hiring&tags=story&hitsPerPage=1";
    const searchResponse = await axios.get(searchUrl, {
      headers: { "User-Agent": getRandomUA() },
      timeout: 15000
    });
    
    const objectID = searchResponse.data?.hits?.[0]?.objectID;
    if (!objectID) return jobs;
    
    // Get comments from the post
    const commentsUrl = `https://hn.algolia.com/api/v1/search?tags=comment,story_${objectID}&hitsPerPage=100`;
    const commentsResponse = await axios.get(commentsUrl, {
      headers: { "User-Agent": getRandomUA() },
      timeout: 15000
    });
    
    const hits = commentsResponse.data?.hits || [];
    
    for (const hit of hits) {
      const text = hit.text || "";
      // Look for job postings with location mentions
      if (text.toLowerCase().includes("remote") || text.toLowerCase().includes("toronto")) {
        const lines = text.split("\n").filter(l => l.trim());
        const title = lines[0]?.replace(/<[^>]+>/g, "").substring(0, 100) || "Software Position";
        
        jobs.push({
          id: `hackernews:${hit.objectID}`,
          source: "hackernews",
          company: "See posting",
          title,
          location: text.toLowerCase().includes("remote") ? "Remote" : "Various",
          url: `https://news.ycombinator.com/item?id=${hit.objectID}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date(hit.created_at).toISOString(),
          excerpt: text.replace(/<[^>]+>/g, "").substring(0, 240)
        });
      }
    }
    
    console.log(`[HackerNews]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[HackerNews] error: ${e.message}`);
  }
  return jobs;
}

// ==================== MAIN ====================
const KEYWORDS = [
  "software developer", "software engineer", "web developer", "full stack developer",
  "backend developer", "frontend developer", "devops engineer", "data engineer",
  "data analyst", "business analyst", "project manager", "product manager",
  "engineering manager", "tech lead", "solutions architect", "cloud engineer",
  "machine learning", "data scientist", "QA engineer", "security engineer",
  "mobile developer", "iOS developer", "Android developer", "UI UX designer"
];

async function main() {
  console.log("🚀 MASS JOB SCRAPER - Target: 10,000 jobs\n");
  console.log(`Keywords: ${KEYWORDS.length}`);
  console.log("Sources: ZipRecruiter, SimplyHired, CareerBuilder, Monster, Workopolis, Glassdoor, Wellfound, WeWorkRemotely, RemoteOK, HackerNews\n");
  
  const allJobs = [];
  const seen = new Set();
  
  // Scrape all sources
  const results = await Promise.allSettled([
    scrapeZipRecruiter(KEYWORDS),
    scrapeSimplyHired(KEYWORDS),
    scrapeCareerBuilder(KEYWORDS),
    scrapeMonster(KEYWORDS),
    scrapeWorkopolis(KEYWORDS),
    scrapeGlassdoor(KEYWORDS),
    scrapeWellfound(KEYWORDS),
    scrapeWeWorkRemotely(),
    scrapeRemoteOK(),
    scrapeHackerNews()
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
  console.log(`SCRAPED: ${allJobs.length} jobs from new sources`);
  console.log(`========================================\n`);
  
  // Load existing jobs
  let existingJobs = [];
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    console.log(`Loaded ${existingJobs.length} existing jobs`);
  } catch (e) {
    console.log("No existing jobs.json");
  }
  
  // Merge all
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
  
  // Progress toward 10K
  const remaining = 10000 - finalJobs.length;
  if (remaining > 0) {
    console.log(`\n📊 Progress: ${finalJobs.length}/10,000 (${((finalJobs.length/10000)*100).toFixed(1)}%)`);
    console.log(`📊 Need ${remaining} more jobs to reach 10K`);
  } else {
    console.log(`\n🎉 REACHED 10,000 JOBS!`);
  }
}

main();
