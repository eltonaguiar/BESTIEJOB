import axios from "axios";
import Parser from "rss-parser";
import fs from "fs";

const rssParser = new Parser({ timeout: 10000 });

// ==================== 1. JOBICY (Free API) ====================
async function scrapeJobicy() {
  const jobs = [];
  try {
    const url = "https://jobicy.com/api/v2/remote-jobs?count=100&geo=canada";
    const response = await axios.get(url, { timeout: 15000 });
    const data = response.data?.jobs || [];
    
    for (const job of data) {
      jobs.push({
        id: `jobicy:${job.id}`,
        source: "jobicy",
        company: job.companyName || "Unknown",
        title: job.jobTitle,
        location: job.jobGeo || "Remote",
        url: job.url,
        employmentType: job.jobType || "full-time",
        salary: job.salaryMin ? { min: job.salaryMin, max: job.salaryMax } : null,
        postedDate: job.pubDate,
        excerpt: job.jobExcerpt || job.jobDescription?.substring(0, 240)
      });
    }
    console.log(`[Jobicy] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Jobicy] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 2. REMOTEOK (Free API) ====================
async function scrapeRemoteOK() {
  const jobs = [];
  try {
    const url = "https://remoteok.com/api";
    const response = await axios.get(url, { timeout: 15000 });
    const data = Array.isArray(response.data) ? response.data.slice(1) : [];
    
    for (const job of data) {
      if (job.position) {
        jobs.push({
          id: `remoteok:${job.id || Math.random().toString(36).substr(2, 9)}`,
          source: "remoteok",
          company: job.company || "Unknown",
          title: job.position,
          location: "Remote",
          url: job.apply_url || job.url,
          employmentType: "full-time",
          salary: job.salary ? { min: parseInt(job.salary) * 1000, max: parseInt(job.salary) * 1000 } : null,
          postedDate: new Date().toISOString(),
          excerpt: job.description?.substring(0, 240)
        });
      }
    }
    console.log(`[RemoteOK] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[RemoteOK] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 3. EU REMOTE JOBS (RSS) ====================
async function scrapeEURemote() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://euremotejobs.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `euremote:${item.guid || Math.random().toString(36).substr(2, 9)}`,
        source: "euremote",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote (EU)",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[EURemote] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[EURemote] Error: ${e.message}`);
  }
  return jobs;
}

async function main() {
  console.log("🚀 Scraping Working Sources from POC\n");
  
  // Load existing jobs
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs`);
  } catch (e) {
    console.log("No existing jobs.json");
  }
  
  const allJobs = [...existingJobs];
  
  // Scrape working sources
  const [jobicyJobs, remoteokJobs, euremoteJobs] = await Promise.all([
    scrapeJobicy(),
    scrapeRemoteOK(),
    scrapeEURemote()
  ]);
  
  // Add new jobs
  let newCount = 0;
  for (const job of [...jobicyJobs, ...remoteokJobs, ...euremoteJobs]) {
    if (!existingIds.has(job.id)) {
      existingIds.add(job.id);
      allJobs.push(job);
      newCount++;
    }
  }
  
  console.log(`\n========================================`);
  console.log(`New jobs added: ${newCount}`);
  console.log(`TOTAL: ${allJobs.length} jobs`);
  console.log(`========================================\n`);
  
  // Count by source
  const bySource = {};
  for (const j of allJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  console.log("By source:", bySource);
  
  // Save
  fs.writeFileSync("jobs.json", JSON.stringify({
    meta: {
      scrapedAt: new Date().toISOString(),
      totalFetched: allJobs.length,
      sources: Object.keys(bySource)
    },
    jobs: allJobs
  }, null, 2));
  
  console.log(`\n✅ Saved to jobs.json`);
}

main().catch(e => {
  console.error("Fatal error:", e);
  process.exit(1);
});
