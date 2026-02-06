// backup_scrapers/jobboom_scraper.js
// Jobboom backup scraper for Toronto jobs
// Usage: require/import and call fetchJobboomJobsBackup()
// Returns array of job objects: { title, company, location, url, salary, postedDate, source }

import axios from "axios";
import cheerio from "cheerio";

/**
 * Fetches Toronto jobs from Jobboom (backup method).
 * @param {string[]} keywords - Array of keywords to search for.
 * @param {string} location - Location string (default: "Toronto, ON").
 * @param {number} maxPages - Max pages to scrape (default: 1).
 * @returns {Promise<Array>} Array of job objects.
 */
export async function fetchJobboomJobsBackup(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  const search = encodeURIComponent(keywords.join(" "));
  const loc = encodeURIComponent(location);

  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.jobboom.com/en/jobs/?keywords=${search}&location=${loc}&page=${page}`;
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
          url: url.startsWith("http") ? url : `https://www.jobboom.com${url}`,
          salary: null,
          postedDate: null,
          source: "jobboom"
        });
      });
    } catch (err) {
      // Log and continue
      console.error("Jobboom backup scrape failed", err);
    }
  }
  return jobs;
}

// To use: import { fetchJobboomJobsBackup } from './backup_scrapers/jobboom_scraper.js';
// Example: fetchJobboomJobsBackup(["manager"], "Toronto, ON", 1).then(jobs => console.log(jobs));
