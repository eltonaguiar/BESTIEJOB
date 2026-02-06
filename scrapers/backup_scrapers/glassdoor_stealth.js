import axios from "axios";
import * as cheerio from "cheerio";
import { HttpsProxyAgent } from "https-proxy-agent";

// Rotating user agents
const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0"
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
 * Stealth-enhanced Glassdoor scraper with anti-bot evasion
 */
export async function fetchGlassdoorJobsStealth(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  const search = encodeURIComponent(keywords.join(" "));
  const loc = encodeURIComponent(location);

  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.glassdoor.ca/Job/${loc}-${search}-jobs-SRCH_IL.0,${loc.length}_KO0,${search.length}.htm?pg=${page}`;
    
    try {
      await sleep(getRandomDelay());
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": getRandomUserAgent(),
          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
          "Accept-Language": "en-US,en;q=0.9",
          "Accept-Encoding": "gzip, deflate, br",
          "DNT": "1",
          "Connection": "keep-alive",
          "Upgrade-Insecure-Requests": "1",
          "Sec-Fetch-Dest": "document",
          "Sec-Fetch-Mode": "navigate",
          "Sec-Fetch-Site": "none",
          "Cache-Control": "max-age=0",
          "Referer": "https://www.google.com/search?q=glassdoor+jobs"
        }
      });

      const $ = cheerio.load(res.data);
      
      // Try multiple selectors as Glassdoor changes frequently
      const selectors = [
        ".react-job-listing",
        "[data-test='job-listing']",
        ".jobListing",
        ".jobContainer"
      ];
      
      for (const selector of selectors) {
        $(selector).each((_, el) => {
          const title = $(el).find(".jobTitle, [data-test='job-title'], h2").text().trim();
          const company = $(el).find(".jobEmpolyerName, [data-test='employer-name'], .companyName").text().trim();
          const jobLoc = $(el).find(".jobLocation, [data-test='job-location'], .location").text().trim();
          const link = $(el).find("a.jobLink, [data-test='job-link']").attr("href") || "";
          const salary = $(el).find(".salaryEstimate, [data-test='job-salary']").text().trim();
          
          if (title && company) {
            jobs.push({
              id: `glassdoor:${link || Math.random().toString(36).substr(2, 9)}`,
              source: "glassdoor",
              title,
              company,
              location: jobLoc || location,
              url: link.startsWith("http") ? link : `https://www.glassdoor.ca${link}`,
              salary: salary || null,
              employmentType: "full-time",
              postedDate: new Date().toISOString(),
              excerpt: `${title} at ${company}`
            });
          }
        });
        
        if (jobs.length > 0) break; // Found jobs with this selector
      }
    } catch (err) {
      console.error(`[Glassdoor Stealth] Page ${page} failed:`, err.message);
    }
  }
  
  return jobs;
}
