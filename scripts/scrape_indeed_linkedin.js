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

async function fetchHtml(url, retries = 2) {
  for (let i = 0; i < retries; i++) {
    try {
      await sleep(2000 + Math.random() * 2000);
      const response = await axios.get(url, {
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Language": "en-US,en;q=0.5",
          "Accept-Encoding": "gzip, deflate, br",
          "Referer": "https://www.google.com/"
        },
        timeout: 15000,
        maxRedirects: 5
      });
      return response.data;
    } catch (error) {
      if (i === retries - 1) {
        console.warn(`Fetch failed for ${url}: ${error.message}`);
        return null;
      }
      await sleep(3000);
    }
  }
  return null;
}

// Indeed via mobile/nocookie endpoint (less aggressive blocking)
async function scrapeIndeedMobile(keyword, location) {
  const jobs = [];
  try {
    const searchTerm = encodeURIComponent(keyword);
    const loc = encodeURIComponent(location);
    // Try alternative Indeed endpoints
    const urls = [
      `https://ca.indeed.com/jobs?q=${searchTerm}&l=${loc}&fromage=7`,
      `https://www.indeed.com/jobs?q=${searchTerm}&l=${loc}&fromage=7`
    ];
    
    for (const url of urls) {
      const html = await fetchHtml(url);
      if (!html) continue;
      
      const $ = cheerio.load(html);
      
      // Look for job data in script tags (Indeed embeds JSON)
      $("script").each((_, el) => {
        const text = $(el).html() || "";
        if (text.includes("jobModel") || text.includes("mosaic-provider")) {
          try {
            // Extract job data from embedded JSON
            const matches = text.match(/"jobTitle":"([^"]+)"/g);
            const companyMatches = text.match(/"companyName":"([^"]+)"/g);
            const locationMatches = text.match(/"jobLocation":"([^"]+)"/g);
            
            if (matches && matches.length > 0) {
              for (let i = 0; i < matches.length; i++) {
                const title = matches[i].replace(/"jobTitle":"/, "").replace(/"$/, "");
                const company = companyMatches?.[i]?.replace(/"companyName":"/, "").replace(/"$/, "") || "Unknown";
                const jobLoc = locationMatches?.[i]?.replace(/"jobLocation":"/, "").replace(/"$/, "") || location;
                
                if (title) {
                  jobs.push({
                    id: `indeed:${title.toLowerCase().replace(/\s+/g, "-")}-${i}`,
                    source: "indeed",
                    company,
                    title,
                    location: jobLoc,
                    url: `https://ca.indeed.com/jobs?q=${searchTerm}&l=${loc}`,
                    employmentType: "full-time",
                    salary: null,
                    postedDate: new Date().toISOString(),
                    excerpt: `${title} at ${company} in ${jobLoc}`
                  });
                }
              }
            }
          } catch (e) {}
        }
      });
      
      // Also try standard selectors as fallback
      $("[data-jk], .slider_item, .job_seen_beacon").each((_, el) => {
        const $el = $(el);
        const title = $el.find("h2 a, .jobTitle span, [data-testid='job-title']").first().text().trim();
        const company = $el.find(".companyName, [data-testid='company-name']").first().text().trim();
        const jobLoc = $el.find("[data-testid='job-location'], .companyLocation").first().text().trim() || location;
        const link = $el.find("h2 a, a[data-jk]").first().attr("href");
        
        if (title) {
          const jobId = link ? link.match(/jk=([^&]+)/)?.[1] : Math.random().toString(36).substr(2, 9);
          jobs.push({
            id: `indeed:${jobId || title.toLowerCase().replace(/\s+/g, "-")}`,
            source: "indeed",
            company: company || "Unknown",
            title,
            location: jobLoc,
            url: link ? (link.startsWith("http") ? link : `https://ca.indeed.com${link}`) : `https://ca.indeed.com/jobs?q=${searchTerm}&l=${loc}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: `${title} at ${company || "Unknown"} in ${jobLoc}`
          });
        }
      });
      
      if (jobs.length > 0) {
        console.log(`[Indeed] Found ${jobs.length} jobs from ${url}`);
        break;
      }
    }
  } catch (e) {
    console.warn("[Indeed] Error:", e.message);
  }
  return jobs;
}

// LinkedIn via public job search
async function scrapeLinkedIn(keyword, location) {
  const jobs = [];
  try {
    const searchTerm = encodeURIComponent(keyword);
    const loc = encodeURIComponent(location);
    const url = `https://www.linkedin.com/jobs/search?keywords=${searchTerm}&location=${loc}&trk=public_jobs_jobs-search-bar_search-submit`;
    
    const html = await fetchHtml(url);
    if (!html) return jobs;
    
    const $ = cheerio.load(html);
    
    // LinkedIn job cards
    $(".job-search-card, .base-card, .jobs-search__results-list > li").each((_, el) => {
      const $el = $(el);
      const title = $el.find(".base-search-card__title, h3").text().trim();
      const company = $el.find(".base-search-card__subtitle, h4").text().trim();
      const jobLoc = $el.find(".job-search-card__location").text().trim() || location;
      const link = $el.find("a.base-card__full-link, a[href*='/jobs/view/']").attr("href");
      
      if (title) {
        jobs.push({
          id: `linkedin:${link?.split("/").pop()?.split("?")[0] || Math.random().toString(36).substr(2, 9)}`,
          source: "linkedin",
          company: company || "Unknown",
          title,
          location: jobLoc,
          url: link ? (link.startsWith("http") ? link : `https://www.linkedin.com${link}`) : `https://www.linkedin.com/jobs/search?keywords=${searchTerm}&location=${loc}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at ${company || "Unknown"} in ${jobLoc}`
        });
      }
    });
    
    console.log(`[LinkedIn] Found ${jobs.length} jobs`);
  } catch (e) {
    console.warn("[LinkedIn] Error:", e.message);
  }
  return jobs;
}

// Keywords to search
const KEYWORDS = [
  "software developer", "software engineer", "web developer",
  "data analyst", "business analyst", "project manager", "product manager"
];

async function main() {
  console.log("Scraping jobs from Indeed and LinkedIn...\n");
  
  const allJobs = [];
  const seen = new Set();
  
  // Scrape Indeed
  console.log("=== Indeed ===");
  for (const keyword of KEYWORDS.slice(0, 3)) {
    const jobs = await scrapeIndeedMobile(keyword, "Toronto, ON");
    for (const job of jobs) {
      if (!seen.has(job.id)) {
        seen.add(job.id);
        allJobs.push(job);
      }
    }
    await sleep(2000);
  }
  
  // Scrape LinkedIn
  console.log("\n=== LinkedIn ===");
  for (const keyword of KEYWORDS.slice(0, 2)) {
    const jobs = await scrapeLinkedIn(keyword, "Toronto, Ontario, Canada");
    for (const job of jobs) {
      if (!seen.has(job.id)) {
        seen.add(job.id);
        allJobs.push(job);
      }
    }
    await sleep(3000);
  }
  
  console.log(`\n========================================`);
  console.log(`TOTAL: ${allJobs.length} jobs from Indeed/LinkedIn`);
  console.log(`========================================\n`);
  
  // Load existing JobBank jobs
  let existingJobs = [];
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    console.log(`Loaded ${existingJobs.length} existing JobBank jobs`);
  } catch (e) {
    console.log("No existing jobs.json found");
  }
  
  // Merge and dedupe
  const merged = [...existingJobs, ...allJobs];
  const finalSeen = new Set();
  const finalJobs = merged.filter(j => {
    if (finalSeen.has(j.id)) return false;
    finalSeen.add(j.id);
    return true;
  });
  
  console.log(`\nFinal total: ${finalJobs.length} jobs (JobBank + Indeed + LinkedIn)`);
  
  // Count by source
  const bySource = {};
  for (const j of finalJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
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
  
  console.log("\n✅ Saved to jobs.json");
}

main();
