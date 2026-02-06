// backup_scrapers/wellfound_scraper.js
// Wellfound (AngelList) backup scraper for Toronto jobs
// Usage: require/import and call fetchWellfoundJobsBackup()
// Returns array of job objects: { title, company, location, url, salary, postedDate, source }

import axios from "axios";
import * as cheerio from "cheerio";

/**
 * Fetches Toronto jobs from Wellfound (backup method).
 * @param {string[]} keywords - Array of keywords to search for.
 * @param {string} location - Location string (default: "Toronto, ON").
 * @param {number} maxPages - Max pages to scrape (default: 1).
 * @returns {Promise<Array>} Array of job objects.
 */
export async function fetchWellfoundJobsBackup(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  const search = encodeURIComponent(keywords.join(" "));
  const loc = encodeURIComponent(location);

  for (let page = 1; page <= maxPages; page++) {
    const url = `https://wellfound.com/jobs?location=${loc}&keywords=${search}&page=${page}`;
    try {
      const res = await axios.get(url, {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; BESTIEJOB/backup)"
        }
      });
      const $ = cheerio.load(res.data);
      $(".job-listing").each((_, el) => {
        const title = $(el).find(".job-title").text().trim();
        const company = $(el).find(".company-name").text().trim();
        const location = $(el).find(".location").text().trim();
        const url = $(el).find("a.job-link").attr("href") || "";
        jobs.push({
          title,
          company,
          location,
          url: url.startsWith("http") ? url : `https://wellfound.com${url}`,
          salary: null,
          postedDate: null,
          source: "wellfound"
        });
      });
    } catch (err) {
      // Log and continue
      console.error("Wellfound backup scrape failed", err);
    }
  }
  return jobs;
}

// To use: import { fetchWellfoundJobsBackup } from './backup_scrapers/wellfound_scraper.js';
// Example: fetchWellfoundJobsBackup(["manager"], "Toronto, ON", 1).then(jobs => console.log(jobs));
