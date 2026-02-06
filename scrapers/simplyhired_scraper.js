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
 * Scrape SimplyHired jobs (HTML-based, scraper-friendly)
 * URL pattern: https://www.simplyhired.ca/search?q=developer&l=Toronto
 */
export async function fetchSimplyHiredJobs(keywords = ["developer"], location = "Toronto", maxPages = 3) {
  const jobs = [];
  const searchQuery = keywords.join("+");
  const loc = encodeURIComponent(location);
  
  for (let page = 1; page <= maxPages; page++) {
    try {
      const pn = page > 1 ? `&pn=${page}` : "";
      const url = `https://www.simplyhired.ca/search?q=${searchQuery}&l=${loc}${pn}`;
      
      console.log(`[SimplyHired] Fetching page ${page}: ${url}`);
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUserAgent(),
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Language": "en-CA,en;q=0.9",
          "Accept-Encoding": "gzip, deflate, br",
          "DNT": "1",
          "Connection": "keep-alive"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // SimplyHired uses article[data-testid="jobTitle"] or .job-card
      $("article[data-testid='jobTitle'], .job-card, .SerpJob-card").each((_, el) => {
        const titleEl = $(el).find("h2 a, [data-testid='jobTitle'] a, .job-title").first();
        const title = titleEl.text().trim();
        const link = titleEl.attr("href") || "";
        
        const companyEl = $(el).find("[data-testid='companyName'], .company-name, .SerpJob-company").first();
        const company = companyEl.text().trim();
        
        const locationEl = $(el).find("[data-testid='jobLocation'], .job-location, .SerpJob-location").first();
        const jobLocation = locationEl.text().trim() || location;
        
        const salaryEl = $(el).find("[data-testid='jobSalary'], .job-salary, .SerpJob-salary").first();
        const salary = salaryEl.text().trim() || null;
        
        const excerptEl = $(el).find("[data-testid='jobDescription'], .job-description, p").first();
        const excerpt = excerptEl.text().trim().substring(0, 200);
        
        if (title && company) {
          jobs.push({
            id: `simplyhired:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
            source: "simplyhired",
            title,
            company,
            location: jobLocation,
            url: link.startsWith("http") ? link : `https://www.simplyhired.ca${link}`,
            employmentType: "full-time",
            salary: salary,
            postedDate: new Date().toISOString(),
            excerpt: excerpt || title
          });
        }
      });
      
      // Alternative selectors if no jobs found
      if (jobs.length === 0 && page === 1) {
        $("[data-testid='searchSerpJob'], .SearchSerpJob, .job-listing").each((_, el) => {
          const titleEl = $(el).find("h2 a, .job-title a").first();
          const title = titleEl.text().trim();
          const link = titleEl.attr("href") || "";
          
          const companyEl = $(el).find(".company, .CompanyName").first();
          const company = companyEl.text().trim();
          
          if (title && company) {
            jobs.push({
              id: `simplyhired:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
              source: "simplyhired",
              title,
              company,
              location: location,
              url: link.startsWith("http") ? link : `https://www.simplyhired.ca${link}`,
              employmentType: "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: title
            });
          }
        });
      }
      
      await sleep(1500 + Math.random() * 1000);
      
    } catch (err) {
      console.error(`[SimplyHired] Page ${page} failed: ${err.message}`);
    }
  }
  
  console.log(`[SimplyHired] Total jobs found: ${jobs.length}`);
  return jobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchSimplyHiredJobs(["software developer"], "Toronto", 2)
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 3));
    })
    .catch(console.error);
}
