import axios from "axios";
import fs from "fs";

// Adzuna API credentials
const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";

// Canada country code for Adzuna
const COUNTRY = "ca";

const KEYWORDS = [
  "software developer", "software engineer", "web developer", "full stack developer",
  "backend developer", "frontend developer", "DevOps engineer", "data engineer",
  "data analyst", "business analyst", "project manager", "product manager",
  "engineering manager", "tech lead", "solutions architect", "cloud engineer",
  "machine learning engineer", "data scientist", "QA engineer", "security engineer",
  "mobile developer", "iOS developer", "Android developer", "UI UX designer",
  "database administrator", "network engineer", "systems administrator",
  "IT manager", "scrum master", "agile coach", "release manager",
  "site reliability engineer", "platform engineer", "infrastructure engineer",
  "software architect", "enterprise architect", "technical lead",
  "application developer", "web designer", "graphic designer",
  "business intelligence analyst", "data warehouse engineer",
  "cybersecurity analyst", "information security manager",
  "IT support specialist", "help desk technician", "network administrator",
  "systems analyst", "programmer analyst", "software tester",
  "automation engineer", "CI/CD engineer", "Kubernetes engineer",
  "AWS engineer", "Azure engineer", "GCP engineer", "cloud architect",
  "blockchain developer", "smart contract developer", "web3 developer",
  "AI engineer", "NLP engineer", "computer vision engineer",
  "robotics engineer", "embedded systems engineer", "firmware engineer",
  "game developer", "Unity developer", "Unreal Engine developer",
  "VR developer", "AR developer", "mixed reality developer",
  "salesforce developer", "SAP consultant", "Oracle developer",
  "PHP developer", "Python developer", "Java developer", "C++ developer",
  "C# developer", "Ruby developer", "Go developer", "Rust developer",
  "Swift developer", "Kotlin developer", "React developer", "Angular developer",
  "Vue developer", "Node.js developer", "Django developer", "Laravel developer",
  "Rails developer", "Spring Boot developer", ".NET developer",
  "Power BI developer", "Tableau developer", "ETL developer",
  "CRM developer", "ERP developer", "CMS developer",
  "ecommerce developer", "Shopify developer", "WordPress developer",
  "Magento developer", "WooCommerce developer", "BigCommerce developer",
  "digital marketing manager", "growth hacker", "SEO specialist",
  "content manager", "product owner", "program manager",
  "delivery manager", "client success manager", "technical account manager",
  "customer success manager", "operations manager", "IT operations manager",
  "service delivery manager", "change manager", "configuration manager",
  "incident manager", "problem manager", "IT asset manager",
  "vendor manager", "contract manager", "procurement manager",
  "IT finance manager", "IT auditor", "compliance manager",
  "risk manager", "business continuity manager", "disaster recovery manager",
  "IT governance manager", "PMO manager", "portfolio manager",
  "demand manager", "resource manager", "capacity manager",
  "performance manager", "service manager", "IT service manager",
  "application manager", "infrastructure manager", "network manager",
  "security manager", "data manager", "information manager",
  "knowledge manager", "document manager", "records manager",
  "content strategist", "UX researcher", "UX writer",
  "interaction designer", "visual designer", "motion designer",
  "brand designer", "marketing designer", "product designer",
  "design lead", "creative director", "art director",
  "copywriter", "technical writer", "documentation specialist",
  "API product manager", "platform product manager", "data product manager",
  "growth product manager", "technical product manager", "SaaS product manager",
  "AI product manager", "ML product manager", "data platform manager",
  "customer support engineer", "solutions engineer", "sales engineer",
  "presales engineer", "postsales engineer", "implementation engineer",
  "integration engineer", "migration engineer", "upgrade engineer",
  "deployment engineer", "release engineer", "build engineer",
  "test automation engineer", "SDET", "quality assurance manager",
  "compliance analyst", "security analyst", "threat analyst",
  "vulnerability analyst", "penetration tester", "ethical hacker",
  "security architect", "security engineer", "security consultant",
  "identity manager", "access manager", "IAM engineer",
  "cryptography engineer", "PKI engineer", "SSL engineer",
  "firewall engineer", "WAF engineer", "DDoS engineer",
  "forensics analyst", "incident response manager", "SOC analyst",
  "security operations manager", "threat hunter", "malware analyst"
];

const LOCATIONS = [
  "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa",
  "Edmonton", "Winnipeg", "Quebec City", "Hamilton", "Kitchener",
  "Waterloo", "London", "Halifax", "Victoria", "Mississauga",
  "Brampton", "Markham", "Vaughan", "Oakville", "Burlington"
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
        category: job.category?.label || "Technology"
      });
    }
    
    return {
      jobs,
      count: data?.count || 0,
      totalPages: Math.ceil((data?.count || 0) / resultsPerPage)
    };
  } catch (error) {
    console.log(`[Adzuna] ${keyword} in ${location} page ${page}: ${error.message}`);
    return { jobs: [], count: 0, totalPages: 0 };
  }
}

async function main() {
  console.log("🚀 ADZUNA API MASS SCRAPER - Target: 10,000 jobs\n");
  console.log(`App ID: ${ADZUNA_APP_ID}`);
  console.log(`Keywords: ${KEYWORDS.length}`);
  console.log(`Locations: ${LOCATIONS.length}`);
  console.log(`Country: Canada (ca)\n`);
  
  const allJobs = [];
  const seen = new Set();
  let totalApiCalls = 0;
  let totalFound = 0;
  
  // Scrape all keyword/location combinations
  for (let i = 0; i < KEYWORDS.length; i++) {
    const keyword = KEYWORDS[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    console.log(`[${i + 1}/${KEYWORDS.length}] "${keyword}" in ${location}`);
    
    // Page 1
    const result1 = await fetchAdzunaJobs(keyword, location, 1, 100);
    totalApiCalls++;
    totalFound += result1.count;
    
    for (const job of result1.jobs) {
      if (!seen.has(job.id)) {
        seen.add(job.id);
        allJobs.push(job);
      }
    }
    
    console.log(`  Page 1: ${result1.jobs.length} jobs (total available: ${result1.count})`);
    
    // Page 2 if there are more results
    if (result1.count > 100) {
      await sleep(500);
      const result2 = await fetchAdzunaJobs(keyword, location, 2, 100);
      totalApiCalls++;
      
      for (const job of result2.jobs) {
        if (!seen.has(job.id)) {
          seen.add(job.id);
          allJobs.push(job);
        }
      }
      console.log(`  Page 2: ${result2.jobs.length} jobs`);
    }
    
    // Page 3 if there are many more results
    if (result1.count > 200) {
      await sleep(500);
      const result3 = await fetchAdzunaJobs(keyword, location, 3, 100);
      totalApiCalls++;
      
      for (const job of result3.jobs) {
        if (!seen.has(job.id)) {
          seen.add(job.id);
          allJobs.push(job);
        }
      }
      console.log(`  Page 3: ${result3.jobs.length} jobs`);
    }
    
    // Progress every 10 keywords
    if ((i + 1) % 10 === 0) {
      console.log(`\n📊 PROGRESS: ${allJobs.length} jobs from ${totalApiCalls} API calls`);
      console.log(`📊 Total jobs available in API: ${totalFound}`);
    }
    
    // Small delay to be nice to the API
    await sleep(300);
    
    // Early exit if we hit 10K
    if (allJobs.length >= 10000) {
      console.log("\n🎉 Reached 10,000 jobs! Stopping...");
      break;
    }
  }
  
  console.log(`\n========================================`);
  console.log(`ADZUNA API SCRAPING COMPLETE`);
  console.log(`========================================`);
  console.log(`Total API calls: ${totalApiCalls}`);
  console.log(`Total jobs available: ${totalFound}`);
  console.log(`UNIQUE JOBS SCRAPED: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  // Load existing jobs
  let existingJobs = [];
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    console.log(`Loaded ${existingJobs.length} existing jobs`);
  } catch (e) {
    console.log("No existing jobs.json");
  }
  
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
      apiCalls: totalApiCalls,
      totalAvailable: totalFound
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

main().catch(e => {
  console.error("Fatal error:", e);
  process.exit(1);
});
