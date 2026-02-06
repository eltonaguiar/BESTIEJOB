// backup_scrapers/monster_scraper.js
// Monster backup scraper for Toronto jobs
// Usage: require/import and call fetchMonsterJobsBackup()
// Returns array of job objects: { title, company, location, url, salary, postedDate, source }

import axios from "axios";
import * as cheerio from "cheerio";

/**
 * Fetches Toronto jobs from Monster (backup method).
 * @param {string[]} keywords - Array of keywords to search for.
 * @param {string} location - Location string (default: "Toronto, ON").
 * @param {number} maxPages - Max pages to scrape (default: 1).
 * @returns {Promise<Array>} Array of job objects.
 */
export async function fetchMonsterJobsBackup(keywords = ["manager"], location = "Toronto, ON", maxPages = 1) {
  const jobs = [];
  const search = encodeURIComponent(keywords.join(" "));
  const loc = encodeURIComponent(location);

  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.monster.ca/jobs/search/?q=${search}&where=${loc}&page=${page}`;
    try {
      const res = await axios.get(url, {
        headers: {
          "User-Agent": "Mozilla/5.0 (compatible; BESTIEJOB/backup)"
        }
      });
      const $ = cheerio.load(res.data);
      $("section.card-content").each((_, el) => {
        const title = $(el).find("h2.title").text().trim();
        const company = $(el).find("div.company").text().trim();
        const location = $(el).find("div.location").text().trim();
        const url = $(el).find("a.card-link").attr("href") || "";
        jobs.push({
          title,
          company,
          location,
          url: url.startsWith("http") ? url : `https://www.monster.ca${url}`,
          salary: null,
          postedDate: null,
          source: "monster"
        });
      });
    } catch (err) {
      // Log and continue
      console.error("Monster backup scrape failed", err);
    }
  }
  return jobs;
}

// To use: import { fetchMonsterJobsBackup } from './backup_scrapers/monster_scraper.js';
// Example: fetchMonsterJobsBackup(["manager"], "Toronto, ON", 1).then(jobs => console.log(jobs));
