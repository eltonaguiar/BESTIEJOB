import axios from "axios";
import fs from "fs";

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

// Broader HR tech keywords
const HR_KEYWORDS = [
  "HRIS", "HRIS Analyst", "HRIS Specialist", "HRIS Administrator",
  "Payroll", "Payroll Specialist", "Payroll Administrator", "Payroll Manager",
  "Workday", "Workday Analyst", "Workday Consultant", "Workday Administrator",
  "Dayforce", "Ceridian", "Ceridian Specialist",
  "ADP", "ADP Specialist", "ADP Administrator",
  "SAP HR", "SAP SuccessFactors", "SAP Consultant",
  "UKG", "Ultimate Software", "Kronos",
  "Oracle HCM", "Oracle HR",
  "HR Technology", "HR Tech", "HR Systems",
  "PeopleSoft", "HR Analytics", "HR Data Analyst",
  "Talent Management", "Performance Management",
  "HR Software", "HR Platform", "HR Tools",
  "Benefits Administrator", "Compensation Analyst",
  "Workforce Management", "Time and Attendance",
  "ATS", "Applicant Tracking", "Recruiting Software",
  "Onboarding Specialist", "HR Operations",
  "People Operations", "People Ops",
  "HR Business Partner", "HRBP",
  "Total Rewards", "Rewards Analyst",
  "HR Project Manager", "HR Program Manager"
];

const LOCATIONS = [
  "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", 
  "Edmonton", "Winnipeg", "Victoria", "Halifax", "Quebec City",
  "Kitchener", "Waterloo", "London", "Hamilton", "Oshawa"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobs(keyword, location, page = 1) {
  try {
    const url = `http://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=100&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&content-type=application/json`;
    
    const response = await axios.get(url, {
      timeout: 30000,
      headers: {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
      }
    });
    
    const data = response.data;
    const results = data?.results || [];
    
    return results.map(job => ({
      id: `adzuna:${job.id || Math.random().toString(36).substr(2, 9)}`,
      source: "adzuna",
      company: job.company?.display_name || "Unknown",
      title: job.title,
      location: job.location?.display_name || `${location}, Canada`,
      url: job.redirect_url,
      employmentType: "full-time",
      salary: job.salary_min && job.salary_max ? { min: Math.round(job.salary_min), max: Math.round(job.salary_max) } : null,
      postedDate: job.created_at || new Date().toISOString(),
      excerpt: job.description?.substring(0, 240) || job.title,
      category: "HR Technology"
    }));
  } catch (error) {
    return [];
  }
}

async function main() {
  console.log("🚀 BROAD HR TECH JOB SEARCH\n");
  console.log(`Searching ${HR_KEYWORDS.length} HR-related keywords...\n`);
  
  // Load existing
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs\n`);
  } catch {
    console.log("Creating fresh database\n");
  }
  
  const allJobs = [...existingJobs];
  let newCount = 0;
  let apiCalls = 0;
  
  for (let i = 0; i < HR_KEYWORDS.length && allJobs.length < 15000; i++) {
    const keyword = HR_KEYWORDS[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    const jobs = await fetchAdzunaJobs(keyword, location, 1);
    apiCalls++;
    
    let added = 0;
    for (const job of jobs) {
      if (!existingIds.has(job.id)) {
        existingIds.add(job.id);
        allJobs.push(job);
        newCount++;
        added++;
      }
    }
    
    if (added > 0) {
      console.log(`[${i + 1}/${HR_KEYWORDS.length}] ${keyword}: +${added} jobs (total: ${allJobs.length})`);
    }
    
    await sleep(200);
  }
  
  console.log(`\n========================================`);
  console.log(`HR TECH SEARCH COMPLETE`);
  console.log(`API calls: ${apiCalls}`);
  console.log(`New jobs: ${newCount}`);
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
