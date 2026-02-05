import axios from "axios";
import fs from "fs";

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

const LOCATIONS = [
  "Toronto, ON", "Mississauga, ON", "Brampton, ON", "Markham, ON",
  "Vaughan, ON", "Oakville, ON", "Burlington, ON", "Hamilton, ON",
  "Guelph, ON", "Kitchener, ON", "Waterloo, ON", "London, ON",
  "Oshawa, ON", "Whitby, ON", "Ajax, ON", "Pickering, ON",
  "North York, ON", "Scarborough, ON", "Etobicoke, ON", "Richmond Hill, ON",
  "Newmarket, ON", "Aurora, ON", "Barrie, ON", "Ottawa, ON"
];

const KEYWORDS = [
  "software", "developer", "engineer", "programmer", "analyst",
  "manager", "consultant", "coordinator", "specialist", "technician",
  "administrator", "architect", "designer", "tester", "support",
  "lead", "director", "officer", "assistant", "representative",
  "supervisor", "operator", "technologist", "advisor", "strategist",
  "planner", "researcher", "scientist", "developer", "programmer",
  "web", "data", "cloud", "security", "network", "systems",
  "database", "application", "frontend", "backend", "full stack",
  "DevOps", "QA", "IT", "digital", "technology", "technical",
  "product", "project", "business", "solution", "infrastructure"
];

async function scrapeJobBank(keyword, location, page = 1) {
  const jobs = [];
  try {
    const url = `https://www.jobbank.gc.ca/jobsearch/api/jobsearch?searchstring=${encodeURIComponent(keyword)}&locationstring=${encodeURIComponent(location)}&sort=M&page=${page}&pagesize=100`;
    const response = await axios.get(url, {
      headers: { 
        "User-Agent": USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)],
        "Accept": "application/json",
        "Referer": "https://www.jobbank.gc.ca/"
      },
      timeout: 15000
    });
    
    const data = response.data;
    const results = data?.results || [];
    
    for (const job of results) {
      const id = `jobbank:${job.id || job.jobId || Math.random().toString(36).substr(2, 9)}`;
      const salaryMin = job.salary?.min ? parseInt(job.salary.min) : null;
      const salaryMax = job.salary?.max ? parseInt(job.salary.max) : null;
      
      jobs.push({
        id,
        source: "jobbank",
        company: job.employerName || job.company || "Government of Canada",
        title: job.title || job.jobTitle || "Position",
        location: job.location?.city || location,
        url: job.url || `https://www.jobbank.gc.ca/jobsearch/jobposting/${job.id}`,
        employmentType: job.type || job.employmentType || "full-time",
        salary: salaryMin && salaryMax ? { min: salaryMin, max: salaryMax } : null,
        postedDate: job.datePosted || new Date().toISOString(),
        excerpt: (job.description || job.title || "Position available").substring(0, 240)
      });
    }
    
    return jobs;
  } catch (e) {
    console.log(`[JobBank] ${keyword} in ${location} page ${page}: ${e.message}`);
    return [];
  }
}

async function main() {
  console.log("🚀 MASSIVE JOBBANK SCRAPER - Target: 10,000 jobs\n");
  console.log(`Keywords: ${KEYWORDS.length}`);
  console.log(`Locations: ${LOCATIONS.length}`);
  console.log(`Estimated searches: ${KEYWORDS.length * LOCATIONS.length}\n`);
  
  const allJobs = [];
  const seen = new Set();
  let searchCount = 0;
  let successCount = 0;
  
  // Scrape with all keyword/location combinations
  for (const keyword of KEYWORDS) {
    for (const location of LOCATIONS) {
      searchCount++;
      
      // Page 1
      const jobs = await scrapeJobBank(keyword, location, 1);
      if (jobs.length > 0) {
        successCount++;
        for (const job of jobs) {
          if (!seen.has(job.id)) {
            seen.add(job.id);
            allJobs.push(job);
          }
        }
      }
      
      // Page 2 (if first page had results)
      if (jobs.length >= 50) {
        await sleep(500);
        const jobs2 = await scrapeJobBank(keyword, location, 2);
        for (const job of jobs2) {
          if (!seen.has(job.id)) {
            seen.add(job.id);
            allJobs.push(job);
          }
        }
      }
      
      // Progress every 50 searches
      if (searchCount % 50 === 0) {
        console.log(`Progress: ${searchCount}/${KEYWORDS.length * LOCATIONS.length} searches, ${allJobs.length} jobs found`);
      }
      
      // Small delay to be nice to the API
      await sleep(300);
      
      // Early exit if we hit 10K
      if (allJobs.length >= 10000) {
        console.log("\n🎉 Reached 10,000 jobs! Stopping...");
        break;
      }
    }
    
    if (allJobs.length >= 10000) break;
  }
  
  console.log(`\n========================================`);
  console.log(`Searches: ${searchCount}`);
  console.log(`Successful: ${successCount}`);
  console.log(`UNIQUE JOBS: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  // Load existing LinkedIn/RemoteOK jobs
  let existingJobs = [];
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = (data.jobs || []).filter(j => j.source !== "jobbank");
    console.log(`Loaded ${existingJobs.length} non-JobBank jobs`);
  } catch (e) {}
  
  // Merge
  const merged = [...existingJobs, ...allJobs];
  const finalSeen = new Set();
  const finalJobs = merged.filter(j => {
    if (finalSeen.has(j.id)) return false;
    finalSeen.add(j.id);
    return true;
  });
  
  // Count by source
  const bySource = {};
  for (const j of finalJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  
  console.log(`\n🎯 FINAL: ${finalJobs.length} total jobs`);
  console.log("By source:", bySource);
  
  // Save
  fs.writeFileSync("jobs.json", JSON.stringify({
    meta: {
      scrapedAt: new Date().toISOString(),
      totalFetched: finalJobs.length,
      sources: Object.keys(bySource),
      searchCount
    },
    jobs: finalJobs
  }, null, 2));
  
  console.log(`\n✅ Saved to jobs.json`);
  
  // Progress
  const percent = ((finalJobs.length / 10000) * 100).toFixed(1);
  console.log(`\n📊 Progress: ${finalJobs.length}/10,000 (${percent}%)`);
  
  if (finalJobs.length < 10000) {
    console.log(`📊 Need ${10000 - finalJobs.length} more jobs`);
  } else {
    console.log(`\n🎉🎉🎉 REACHED 10,000 JOBS! 🎉🎉🎉`);
  }
}

main();
