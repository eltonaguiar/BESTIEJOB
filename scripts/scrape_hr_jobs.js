import axios from "axios";
import fs from "fs";

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

// HR and Payroll related job titles
const HR_JOB_TITLES = [
  "HRIS Analyst", "HRIS Specialist", "HRIS Administrator",
  "Payroll Specialist", "Payroll Administrator", "Payroll Manager",
  "Benefits Administrator", "Benefits Specialist", "Compensation Analyst",
  "HR Coordinator", "HR Generalist", "HR Business Partner",
  "Talent Acquisition Specialist", "Recruiting Coordinator",
  "Workday Consultant", "Workday Analyst", "Workday Administrator",
  "Dayforce Consultant", "Ceridian Specialist", "ADP Specialist",
  "SAP SuccessFactors Consultant", "SAP HR Consultant",
  "Time and Attendance Specialist", "Workforce Management Analyst",
  "HR Technology Analyst", "HR Systems Administrator",
  "People Operations Specialist", "Employee Relations Specialist",
  "HR Data Analyst", "HR Reporting Analyst",
  "Learning Management System Admin", "LMS Administrator",
  "Talent Management Specialist", "Performance Management Analyst",
  "Onboarding Specialist", "Offboarding Coordinator",
  "HR Compliance Specialist", "Labor Relations Specialist",
  "Diversity and Inclusion Specialist", "DEI Coordinator",
  "Employee Engagement Specialist", "Culture Specialist",
  "Total Rewards Specialist", "Rewards Analyst",
  "HR Project Manager", "HR Program Manager",
  "People Analytics Manager", "HR Metrics Analyst",
  "Applicant Tracking System Admin", "ATS Administrator",
  "Background Check Coordinator", "Verification Specialist"
];

const LOCATIONS = [
  "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Winnipeg",
  "Victoria", "Halifax", "Quebec City", "Kitchener", "Waterloo", "London"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobs(keyword, location, page = 1, resultsPerPage = 100) {
  try {
    const url = `http://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=${resultsPerPage}&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&content-type=application/json`;
    
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
  console.log("🚀 SCRAPING HR/PAYROLL JOB TITLES\n");
  console.log(`Searching ${HR_JOB_TITLES.length} HR-related job titles...\n`);
  
  // Load existing jobs
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs\n`);
  } catch (e) {
    console.log("No existing jobs.json\n");
  }
  
  const allJobs = [...existingJobs];
  let newCount = 0;
  let apiCalls = 0;
  
  // Scrape HR job titles
  for (let i = 0; i < HR_JOB_TITLES.length && allJobs.length < 15000; i++) {
    const title = HR_JOB_TITLES[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    const jobs = await fetchAdzunaJobs(title, location, 1, 100);
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
      console.log(`[${i + 1}/${HR_JOB_TITLES.length}] ${title}: +${added} jobs (total: ${allJobs.length})`);
    }
    
    await sleep(200);
  }
  
  console.log(`\n========================================`);
  console.log(`HR JOB TITLES SCRAPING COMPLETE`);
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
