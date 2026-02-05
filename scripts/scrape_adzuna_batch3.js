import axios from "axios";
import fs from "fs";

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

// More diverse keywords
const KEYWORDS = [
  "manager", "supervisor", "coordinator", "specialist", "analyst",
  "engineer", "technician", "developer", "designer", "consultant",
  "assistant", "associate", "representative", "agent", "officer",
  "director", "lead", "principal", "senior", "junior",
  "executive", "administrator", "controller", "planner", "strategist",
  "advisor", "coordinator", "facilitator", "moderator", "evaluator",
  "inspector", "investigator", "examiner", "auditor", "assessor",
  "negotiator", "mediator", "arbitrator", "conciliator", "ombudsman",
  "archivist", "curator", "librarian", "registrar", "records manager",
  "scheduler", "dispatcher", "coordinator", "logistician", "expeditor",
  "estimator", "surveyor", "appraiser", "assessor", "valuer",
  "buyer", "purchaser", "procurement", "sourcing", "vendor",
  "merchandiser", "allocator", "distributor", "wholesaler", "retailer",
  "cashier", "teller", "clerk", "attendant", "aide",
  "helper", "porter", "mover", "packer", "picker",
  "packager", "shipper", "receiver", "stocker", "inventory",
  "forklift", "operator", "driver", "courier", "messenger",
  "installer", "repairer", "fixer", "maintainer", "servicer",
  "calibrator", "tester", "checker", "verifier", "validator"
];

const LOCATIONS = [
  "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Winnipeg"
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
      category: job.category?.label || "General"
    }));
  } catch (error) {
    return [];
  }
}

async function main() {
  console.log("🚀 ADZUNA BATCH 3 - Final push to 10K\n");
  
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs`);
  } catch (e) {}
  
  const allJobs = [...existingJobs];
  let newCount = 0;
  
  for (let i = 0; i < KEYWORDS.length && allJobs.length < 10000; i++) {
    const keyword = KEYWORDS[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    // Get 3 pages per keyword
    for (let page = 1; page <= 3 && allJobs.length < 10000; page++) {
      const jobs = await fetchAdzunaJobs(keyword, location, page, 100);
      
      for (const job of jobs) {
        if (!existingIds.has(job.id)) {
          existingIds.add(job.id);
          allJobs.push(job);
          newCount++;
        }
      }
      
      if (jobs.length < 100) break; // No more results
      await sleep(200);
    }
    
    if ((i + 1) % 20 === 0) {
      console.log(`[${i + 1}/${KEYWORDS.length}] ${keyword}: +${newCount} new, ${allJobs.length} total`);
    }
    
    await sleep(100);
  }
  
  console.log(`\n========================================`);
  console.log(`BATCH 3 COMPLETE`);
  console.log(`New jobs: ${newCount}`);
  console.log(`TOTAL: ${allJobs.length} jobs`);
  console.log(`========================================\n`);
  
  const bySource = {};
  for (const j of allJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  console.log("By source:", bySource);
  
  fs.writeFileSync("jobs.json", JSON.stringify({
    meta: {
      scrapedAt: new Date().toISOString(),
      totalFetched: allJobs.length,
      sources: Object.keys(bySource)
    },
    jobs: allJobs
  }, null, 2));
  
  console.log(`\n✅ Saved to jobs.json`);
  
  if (allJobs.length >= 10000) {
    console.log(`\n🎉🎉🎉 REACHED 10,000 JOBS! 🎉🎉🎉`);
  } else {
    console.log(`\n📊 Progress: ${allJobs.length}/10,000 (${((allJobs.length/10000)*100).toFixed(1)}%)`);
    console.log(`📊 Need ${10000 - allJobs.length} more jobs`);
  }
}

main();
