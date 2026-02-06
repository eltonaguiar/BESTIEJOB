// backup_scrapers/glassdoor_scraper.js
// Glassdoor backup scraper for Toronto jobs
// Usage: require/import and call fetchGlassdoorJobsBackup()
// Returns array of job objects: { title, company, location, url, salary, postedDate, source }

import axios from "axios";
import * as cheerio from "cheerio";

/**
 * Fetches Toronto jobs from Glassdoor (backup method).
 * @param {string[]} keywords - Array of keywords to search for.
 * @param {string} location - Location string (default: "Toronto, ON").
 * @param {number} maxPages - Max pages to scrape (default: 1).
 * @returns {Promise<Array>} Array of job objects.
 */
export async function fetchGlassdoorJobsBackup(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  const search = encodeURIComponent(keywords.join(" "));
  const loc = encodeURIComponent(location);

  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.glassdoor.ca/Job/${loc}-jobs-SRCH_IL.0,${loc.length}_IC2281069_KO0,${search.length}.htm?pg=${page}`;
    try {
      const res = await axios.get(url, {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; BESTIEJOB/backup)"
        }
      });
      const $ = cheerio.load(res.data);
      $(".react-job-listing").each((_, el) => {
        const title = $(el).find(".jobTitle").text().trim();
        const company = $(el).find(".jobEmpolyerName").text().trim();
        const location = $(el).find(".jobLocation").text().trim();
        const url = "https://www.glassdoor.ca" + ($(el).find("a.jobLink").attr("href") || "");
        const salary = $(el).find(".salaryEstimate").text().trim();
        jobs.push({
          title,
          company,
          location,
          url,
          salary,
          postedDate: null,
          source: "glassdoor"
        });
      });
    } catch (err) {
      // Log and continue
      console.error("Glassdoor backup scrape failed", err);
    }
  }
  return jobs;
}

// To use: import { fetchGlassdoorJobsBackup } from './backup_scrapers/glassdoor_scraper.js';
// Example: fetchGlassdoorJobsBackup(["manager"], "Toronto, ON", 1).then(jobs => console.log(jobs));
