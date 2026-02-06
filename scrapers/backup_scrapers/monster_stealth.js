import axios from "axios";
import * as cheerio from "cheerio";

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
 * Stealth-enhanced Monster.ca scraper
 */
export async function fetchMonsterJobsStealth(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  
  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.monster.ca/jobs/search/?q=${encodeURIComponent(keywords.join(" "))}&where=${encodeURIComponent(location)}&page=${page}`;
    
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
      
      // Multiple selectors for Monster
      const selectors = [
        "section.card-content",
        "[data-testid='job-card']",
        ".job-card",
        ".job-listing-card"
      ];
      
      for (const selector of selectors) {
        $(selector).each((_, el) => {
          const title = $(el).find("h2.title, .jobTitle, .title").text().trim();
          const company = $(el).find("div.company, .companyName, .employer").text().trim();
          const jobLoc = $(el).find("div.location, .jobLocation").text().trim();
          const link = $(el).find("a.card-link, a[href*='/jobs/']").attr("href") || "";
          
          if (title && company) {
            jobs.push({
              id: `monster:${link || Math.random().toString(36).substr(2, 9)}`,
              source: "monster",
              title,
              company,
              location: jobLoc || location,
              url: link.startsWith("http") ? link : `https://www.monster.ca${link}`,
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
      console.error(`[Monster Stealth] Page ${page} failed:`, err.message);
    }
  }
  
  return jobs;
}
