import axios from "axios";
import * as cheerio from "cheerio";

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

/**
 * Scrape Working Nomads remote jobs (HTML-based, curated tech listings)
 * URL: https://www.workingnomads.com/jobs
 */
export async function fetchWorkingNomadsJobs(maxPages = 3) {
  const jobs = [];
  const categories = ["software-development", "devops-sysadmin", "design", "marketing", "product"];
  
  for (const category of categories.slice(0, maxPages)) {
    try {
      const url = `https://www.workingnomads.com/jobs?category=${category}`;
      
      console.log(`[WorkingNomads] Fetching ${category}...`);
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUserAgent(),
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Language": "en-CA,en;q=0.9"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      $(".job-item, .job-listing, .job-card, [data-job-id]").each((_, el) => {
        const titleEl = $(el).find("h2 a, .job-title a, .title a, a[href*='jobs']").first();
        const title = titleEl.text().trim();
        const link = titleEl.attr("href") || "";
        
        const companyEl = $(el).find(".company, .company-name, .employer").first();
        const company = companyEl.text().trim() || "Unknown";
        
        const tagsEl = $(el).find(".tags, .categories, .job-tags");
        const tags = tagsEl.text().trim();
        
        const dateEl = $(el).find(".date, .posted-date, time");
        const postedDate = dateEl.attr("datetime") || new Date().toISOString();
        
        if (title) {
          jobs.push({
            id: `workingnomads:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
            source: "workingnomads",
            company,
            title,
            location: "Remote",
            url: link.startsWith("http") ? link : `https://www.workingnomads.com${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate,
            excerpt: `${title} - ${tags || category} (Remote work opportunity via Working Nomads)}`
          });
        }
      });
      
      // Alternative selectors
      if (jobs.length === 0) {
        $("article, .job").each((_, el) => {
          const titleEl = $(el).find("h3 a, h2 a, .job-title").first();
          const title = titleEl.text().trim();
          const link = titleEl.attr("href") || $(el).find("a").first().attr("href") || "";
          
          const companyEl = $(el).find(".company, strong, b").first();
          const company = companyEl.text().trim() || "Unknown";
          
          if (title && link) {
            jobs.push({
              id: `workingnomads:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
              source: "workingnomads",
              company,
              title,
              location: "Remote",
              url: link.startsWith("http") ? link : `https://www.workingnomads.com${link}`,
              employmentType: "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: title
            });
          }
        });
      }
      
      await sleep(1000 + Math.random() * 500);
      
    } catch (err) {
      console.error(`[WorkingNomads] ${category} failed: ${err.message}`);
    }
  }
  
  console.log(`[WorkingNomads] Total jobs found: ${jobs.length}`);
  return jobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchWorkingNomadsJobs(2)
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 3));
    })
    .catch(console.error);
}
