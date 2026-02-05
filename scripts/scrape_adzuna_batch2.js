import axios from "axios";
import fs from "fs";

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

// Different set of keywords for second batch
const KEYWORDS = [
  "accountant", "financial analyst", "controller", "bookkeeper",
  "HR manager", "recruiter", "talent acquisition", "HR generalist",
  "marketing manager", "brand manager", "social media manager", "content creator",
  "sales manager", "account executive", "business development", "sales rep",
  "customer service", "call center", "support specialist", "help desk",
  "administrative assistant", "executive assistant", "office manager", "receptionist",
  "warehouse worker", "forklift operator", "logistics coordinator", "supply chain",
  "driver", "delivery driver", "truck driver", "courier",
  "nurse", "caregiver", "personal support worker", "healthcare aide",
  "teacher", "educator", "tutor", "teaching assistant",
  "chef", "cook", "line cook", "prep cook", "kitchen staff",
  "server", "bartender", "hostess", "restaurant manager",
  "barista", "cashier", "retail associate", "store manager",
  "mechanic", "technician", "electrician", "plumber", "carpenter",
  "construction worker", "general labourer", "machine operator", "assembler",
  "cleaner", "janitor", "housekeeper", "maintenance worker",
  "security guard", "doorman", "concierge", "property manager",
  "legal assistant", "paralegal", "law clerk", "attorney",
  "researcher", "scientist", "lab technician", "research assistant",
  "pharmacist", "pharmacy technician", "dental assistant", "medical receptionist",
  "physiotherapist", "occupational therapist", "massage therapist", "chiropractor",
  "psychologist", "counselor", "social worker", "case manager",
  "architect", "draftsman", "surveyor", "project coordinator",
  "real estate agent", "property agent", "leasing consultant", "mortgage broker",
  "insurance agent", "underwriter", "claims adjuster", "risk analyst",
  "bank teller", "loan officer", "credit analyst", "investment advisor",
  "event planner", "coordinator", "wedding planner", "meeting planner",
  "travel agent", "tour guide", "flight attendant", "hotel manager",
  "fitness trainer", "gym instructor", "yoga teacher", "pilates instructor",
  "cosmetologist", "hair stylist", "esthetician", "nail technician",
  "photographer", "videographer", "editor", "producer",
  "musician", "artist", "performer", "entertainer",
  "writer", "journalist", "editor", "copy editor",
  "translator", "interpreter", "linguist", "language specialist",
  "IT technician", "computer technician", "hardware technician", "field technician",
  "audio visual technician", "broadcast technician", "sound engineer", "lighting technician"
];

const LOCATIONS = [
  "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa",
  "Edmonton", "Winnipeg", "Quebec City", "Hamilton", "Kitchener",
  "Waterloo", "London", "Halifax", "Victoria", "Mississauga",
  "Brampton", "Markham", "Vaughan", "Oakville", "Burlington",
  "Richmond", "Burnaby", "Surrey", "Langley", "Coquitlam",
  "Richmond Hill", "Aurora", "Newmarket", "Whitby", "Ajax",
  "Pickering", "Oshawa", "St. Catharines", "Niagara Falls", "Barrie",
  "Guelph", "Cambridge", "Brantford", "Peterborough", "Kingston"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobs(keyword, location, page = 1, resultsPerPage = 100) {
  const jobs = [];
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
    
    for (const job of results) {
      const salaryMin = job.salary_min ? Math.round(job.salary_min) : null;
      const salaryMax = job.salary_max ? Math.round(job.salary_max) : null;
      
      jobs.push({
        id: `adzuna:${job.id || Math.random().toString(36).substr(2, 9)}`,
        source: "adzuna",
        company: job.company?.display_name || "Unknown",
        title: job.title,
        location: job.location?.display_name || `${location}, Canada`,
        url: job.redirect_url,
        employmentType: "full-time",
        salary: salaryMin && salaryMax ? { min: salaryMin, max: salaryMax } : null,
        postedDate: job.created_at || new Date().toISOString(),
        excerpt: job.description?.substring(0, 240) || job.title,
        category: job.category?.label || "General"
      });
    }
    
    return {
      jobs,
      count: data?.count || 0
    };
  } catch (error) {
    return { jobs: [], count: 0 };
  }
}

async function main() {
  console.log("🚀 ADZUNA BATCH 2 - Getting more jobs\n");
  
  // Load existing jobs
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
  let apiCalls = 0;
  
  // Scrape
  for (let i = 0; i < KEYWORDS.length; i++) {
    const keyword = KEYWORDS[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    // Page 1
    const result1 = await fetchAdzunaJobs(keyword, location, 1, 100);
    apiCalls++;
    
    for (const job of result1.jobs) {
      if (!existingIds.has(job.id)) {
        existingIds.add(job.id);
        allJobs.push(job);
        newCount++;
      }
    }
    
    // Page 2 if more results
    if (result1.count > 100 && allJobs.length < 10000) {
      await sleep(300);
      const result2 = await fetchAdzunaJobs(keyword, location, 2, 100);
      apiCalls++;
      
      for (const job of result2.jobs) {
        if (!existingIds.has(job.id)) {
          existingIds.add(job.id);
          allJobs.push(job);
          newCount++;
        }
      }
    }
    
    if ((i + 1) % 20 === 0) {
      console.log(`[${i + 1}/${KEYWORDS.length}] ${keyword} in ${location}: +${newCount} new, ${allJobs.length} total`);
    }
    
    await sleep(200);
    
    if (allJobs.length >= 10000) {
      console.log("\n🎉 Reached 10,000 jobs!");
      break;
    }
  }
  
  console.log(`\n========================================`);
  console.log(`BATCH 2 COMPLETE`);
  console.log(`New jobs: ${newCount}`);
  console.log(`Total jobs: ${allJobs.length}`);
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
  
  const percent = ((allJobs.length / 10000) * 100).toFixed(1);
  console.log(`\n📊 Progress: ${allJobs.length}/10,000 (${percent}%)`);
  
  if (allJobs.length < 10000) {
    console.log(`📊 Need ${10000 - allJobs.length} more jobs`);
  } else {
    console.log(`\n🎉🎉🎉 REACHED 10,000 JOBS! 🎉🎉🎉`);
  }
}

main();
