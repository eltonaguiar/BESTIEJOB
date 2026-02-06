import axios from "axios";
import fs from "fs";

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

// HR Platform Companies
const HR_COMPANIES = [
  "Ceridian", "Dayforce", "Workday", "ADP", "Paychex", "Ultimate Software", "UKG",
  "SAP SuccessFactors", "SAP", "Oracle HCM", "Oracle", "Cornerstone OnDemand",
  "Workforce Software", "Kronos", "Infor", "BambooHR", "Gusto", "Zenefits",
  "Namely", "Paylocity", "Rippling", "Deel", "Remote", "Personio", "HiBob",
  "Lattice", "15Five", "Culture Amp", "Qualtrics", "Glint", "Peakon",
  "Saba", "SumTotal", "TalentSoft", "Lumesse", "SilkRoad", "Taleo",
  "iCIMS", "Greenhouse", "Lever", "SmartRecruiters", "JazzHR", "Jobvite",
  "Bullhorn", "Avionté", "TempWorks", "Paycom", "Paycor", "PrimePay",
  "Justworks", "TriNet", "Insperity", "ADP TotalSource", "Safeguard",
  "Alight", "Willis Towers Watson", "Mercer", "Aon Hewitt", "Conduent"
];

const LOCATIONS = [
  "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Winnipeg",
  "Victoria", "Halifax", "Quebec City", "Kitchener", "Waterloo", "London",
  "Markham", "Vaughan", "Mississauga", "Brampton", "Oakville", "Burlington",
  "Richmond Hill", "Burnaby", "Surrey", "Richmond", "Coquitlam", "Langley"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobsByCompany(company, location, page = 1, resultsPerPage = 100) {
  try {
    // Search by company name
    const url = `http://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=${resultsPerPage}&company=${encodeURIComponent(company)}&where=${encodeURIComponent(location)}&content-type=application/json`;
    
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
      company: job.company?.display_name || company,
      title: job.title,
      location: job.location?.display_name || `${location}, Canada`,
      url: job.redirect_url,
      employmentType: "full-time",
      salary: job.salary_min && job.salary_max ? { min: Math.round(job.salary_min), max: Math.round(job.salary_max) } : null,
      postedDate: job.created_at || new Date().toISOString(),
      excerpt: job.description?.substring(0, 240) || job.title,
      category: job.category?.label || "HR Technology"
    }));
  } catch (error) {
    return [];
  }
}

async function main() {
  console.log("🚀 SCRAPING HR PLATFORM COMPANY JOBS\n");
  console.log("Companies:", HR_COMPANIES.join(", "), "\n");
  
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
  
  // Scrape HR platform company jobs
  for (let i = 0; i < HR_COMPANIES.length && allJobs.length < 15000; i++) {
    const company = HR_COMPANIES[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    console.log(`[${i + 1}/${HR_COMPANIES.length}] Searching ${company} in ${location}...`);
    
    const jobs = await fetchAdzunaJobsByCompany(company, location, 1, 100);
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
      console.log(`  ✅ +${added} jobs from ${company}`);
    } else {
      console.log(`  ⚠️ No new jobs from ${company}`);
    }
    
    await sleep(300);
  }
  
  console.log(`\n========================================`);
  console.log(`HR PLATFORM SCRAPING COMPLETE`);
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
