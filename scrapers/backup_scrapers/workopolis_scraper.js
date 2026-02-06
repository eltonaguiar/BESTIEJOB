// backup_scrapers/workopolis_scraper.js
// Workopolis backup scraper for Toronto jobs
// Usage: require/import and call fetchWorkopolisJobsBackup()
// Returns array of job objects: { title, company, location, url, salary, postedDate, source }

import axios from "axios";
import * as cheerio from "cheerio";

/**
 * Fetches Toronto jobs from Workopolis (backup method).
 * @param {string[]} keywords - Array of keywords to search for.
 * @param {string} location - Location string (default: "Toronto, ON").
 * @param {number} maxPages - Max pages to scrape (default: 1).
 * @returns {Promise<Array>} Array of job objects.
 */
export async function fetchWorkopolisJobsBackup(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  const search = encodeURIComponent(keywords.join(" "));
  const loc = encodeURIComponent(location);

  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.workopolis.com/jobsearch/find-jobs?location=${loc}&q=${search}&page=${page}`;
    try {
      const res = await axios.get(url, {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; BESTIEJOB/backup)"
        }
      });
      const $ = cheerio.load(res.data);
      $(".JobCard__Content").each((_, el) => {
        const title = $(el).find(".JobCard__Title").text().trim();
        const company = $(el).find(".JobCard__CompanyName").text().trim();
        const location = $(el).find(".JobCard__Location").text().trim();
        const url = $(el).find("a.JobCard__Link").attr("href") || "";
        jobs.push({
          title,
          company,
          location,
          url: url.startsWith("http") ? url : `https://www.workopolis.com${url}`,
          salary: null,
          postedDate: null,
          source: "workopolis"
        });
      });
    } catch (err) {
      // Log and continue
      console.error("Workopolis backup scrape failed", err);
    }
  }
  return jobs;
}

// To use: import { fetchWorkopolisJobsBackup } from './backup_scrapers/workopolis_scraper.js';
// Example: fetchWorkopolisJobsBackup(["manager"], "Toronto, ON", 1).then(jobs => console.log(jobs));
