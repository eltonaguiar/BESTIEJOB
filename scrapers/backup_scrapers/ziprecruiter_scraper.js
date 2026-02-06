// backup_scrapers/ziprecruiter_scraper.js
// ZipRecruiter backup scraper for Toronto jobs
// Usage: require/import and call fetchZipRecruiterJobsBackup()
// Returns array of job objects: { title, company, location, url, salary, postedDate, source }

import axios from "axios";
import cheerio from "cheerio";

/**
 * Fetches Toronto jobs from ZipRecruiter (backup method).
 * @param {string[]} keywords - Array of keywords to search for.
 * @param {string} location - Location string (default: "Toronto, ON").
 * @param {number} maxPages - Max pages to scrape (default: 1).
 * @returns {Promise<Array>} Array of job objects.
 */
export async function fetchZipRecruiterJobsBackup(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  const search = encodeURIComponent(keywords.join(" "));
  const loc = encodeURIComponent(location);

  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.ziprecruiter.com/jobs?search=${search}&location=${loc}&page=${page}`;
    try {
      const res = await axios.get(url, {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; BESTIEJOB/backup)"
        }
      });
      const $ = cheerio.load(res.data);
      $(".job_result").each((_, el) => {
        const title = $(el).find(".job_title").text().trim();
        const company = $(el).find(".company_name").text().trim();
        const location = $(el).find(".location").text().trim();
        const url = $(el).find("a.job_link").attr("href") || "";
        jobs.push({
          title,
          company,
          location,
          url: url.startsWith("http") ? url : `https://www.ziprecruiter.com${url}`,
          salary: null,
          postedDate: null,
          source: "ziprecruiter"
        });
      });
    } catch (err) {
      // Log and continue
      console.error("ZipRecruiter backup scrape failed", err);
    }
  }
  return jobs;
}

// To use: import { fetchZipRecruiterJobsBackup } from './backup_scrapers/ziprecruiter_scraper.js';
// Example: fetchZipRecruiterJobsBackup(["manager"], "Toronto, ON", 1).then(jobs => console.log(jobs));
