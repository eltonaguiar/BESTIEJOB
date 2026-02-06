#!/usr/bin/env node
/**
 * Fix Job Dates Script
 * Re-processes existing jobs to mark those with uncertain dates
 * Jobs scraped with incorrect postedDate will be marked appropriately
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.join(__dirname, "..");

function loadJobs() {
  const jobsPath = path.join(PROJECT_ROOT, "jobs.json");
  try {
    const data = fs.readFileSync(jobsPath, "utf8");
    const parsed = JSON.parse(data);
    return Array.isArray(parsed) ? parsed : (parsed.jobs || []);
  } catch (e) {
    console.error("Could not load jobs:", e.message);
    return [];
  }
}

function saveJobs(jobs) {
  const jobsPath = path.join(PROJECT_ROOT, "jobs.json");
  fs.writeFileSync(jobsPath, JSON.stringify(jobs, null, 2));
  
  // Also copy to public directories
  const publicDirs = [
    path.join(PROJECT_ROOT, "public", "findjobs", "jobs.json"),
    path.join(PROJECT_ROOT, "public", "gotjob", "jobs.json")
  ];
  
  for (const dest of publicDirs) {
    try {
      fs.writeFileSync(dest, JSON.stringify(jobs, null, 2));
      console.log(`✓ Saved to ${dest}`);
    } catch (e) {
      console.log(`Could not save to ${dest}`);
    }
  }
}

function main() {
  console.log("╔══════════════════════════════════════════════════════╗");
  console.log("║      FIX JOB DATES SCRIPT                            ║");
  console.log("╚══════════════════════════════════════════════════════╝\n");
  
  const jobs = loadJobs();
  console.log(`📂 Loaded ${jobs.length} jobs\n`);
  
  let fixedCount = 0;
  let uncertainCount = 0;
  let validCount = 0;
  
  const now = new Date();
  
  for (const job of jobs) {
    // Check if job has a postedDate
    if (job.postedDate) {
      const posted = new Date(job.postedDate);
      const scraped = job.scrapedAt ? new Date(job.scrapedAt) : now;
      
      // Check if postedDate is valid
      if (isNaN(posted.getTime())) {
        job.dateSource = "invalid";
        job.postedDate = null;
        fixedCount++;
        continue;
      }
      
      // Check if postedDate is suspiciously close to scrapedAt
      // (indicates it was just set to current time during scraping)
      const diffMs = Math.abs(posted - scraped);
      const diffMinutes = diffMs / (1000 * 60);
      
      if (diffMinutes < 5) {
        // Posted date is within 5 minutes of scrape time - likely fake
        job.dateSource = "scraped";
        uncertainCount++;
      } else if (job.dateSource === "parsed") {
        validCount++;
      } else if (!job.dateSource) {
        // No dateSource set - check if it looks legitimate
        // If the date is in the future, it's invalid
        if (posted > now) {
          job.dateSource = "invalid";
          job.postedDate = job.scrapedAt || now.toISOString();
          fixedCount++;
        } else {
          // Assume it's from scraping (uncertain)
          job.dateSource = "scraped";
          uncertainCount++;
        }
      }
    } else {
      // No postedDate - mark as unknown
      job.dateSource = "unknown";
      uncertainCount++;
    }
  }
  
  // Save fixed jobs
  saveJobs(jobs);
  
  console.log("════════════════════════════════════════════════════════");
  console.log("DATE FIX COMPLETE");
  console.log("════════════════════════════════════════════════════════\n");
  
  console.log(`📊 Results:
   • Jobs with valid parsed dates: ${validCount}
   • Jobs with uncertain dates: ${uncertainCount}
   • Jobs with fixed/invalid dates: ${fixedCount}
   • Total jobs: ${jobs.length}
`);
  
  // Show date source breakdown
  const bySource = {};
  for (const job of jobs) {
    const src = job.dateSource || "unknown";
    bySource[src] = (bySource[src] || 0) + 1;
  }
  console.log("📈 Date Source Breakdown:");
  for (const [src, count] of Object.entries(bySource).sort((a, b) => b[1] - a[1])) {
    const pct = ((count / jobs.length) * 100).toFixed(1);
    console.log(`   ${src}: ${count} (${pct}%)`);
  }
}

main();
