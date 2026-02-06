import axios from "axios";
import * as cheerio from "cheerio";

// Rotating user agents
const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
];

function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function getRandomDelay(min = 2000, max = 5000) {
  return Math.floor(Math.random() * (max - min + 1)) + min;
}

/**
 * Stealth-enhanced Workopolis scraper
 */
export async function fetchWorkopolisJobsStealth(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  
  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.workopolis.com/jobsearch/find-jobs?location=${encodeURIComponent(location)}&q=${encodeURIComponent(keywords.join(" "))}&page=${page}`;
    
    try {
      await sleep(getRandomDelay());
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": getRandomUserAgent(),
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
          "Accept-Language": "en-CA,en;q=0.9",
          "Accept-Encoding": "gzip, deflate, br",
          "DNT": "1",
          "Connection": "keep-alive",
          "Upgrade-Insecure-Requests": "1",
          "Sec-Fetch-Dest": "document",
          "Sec-Fetch-Mode": "navigate",
          "Referer": "https://www.google.com/"
        }
      });

      const $ = cheerio.load(res.data);
      
      // Multiple selectors for Workopolis
      const selectors = [
        ".JobCard__Content",
        "[data-testid='job-card']",
        ".job-card",
        ".job-listing"
      ];
      
      for (const selector of selectors) {
        $(selector).each((_, el) => {
          const title = $(el).find(".JobCard__Title, h3, .title").text().trim();
          const company = $(el).find(".JobCard__CompanyName, .company").text().trim();
          const jobLoc = $(el).find(".JobCard__Location, .location").text().trim();
          const link = $(el).find("a.JobCard__Link, a[href*='/job/']").attr("href") || "";
          
          if (title && company) {
            jobs.push({
              id: `workopolis:${link || Math.random().toString(36).substr(2, 9)}`,
              source: "workopolis",
              title,
              company,
              location: jobLoc || location,
              url: link.startsWith("http") ? link : `https://www.workopolis.com${link}`,
              salary: null,
              employmentType: "full-time",
              postedDate: new Date().toISOString(),
              excerpt: `${title} at ${company}`
            });
          }
        });
        
        if (jobs.length > 0) break;
      }
    } catch (err) {
      console.error(`[Workopolis Stealth] Page ${page} failed:`, err.message);
    }
  }
  
  return jobs;
}
