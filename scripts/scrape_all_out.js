import { scrapeIndeedJobs } from "../scrapers/indeed_scraper.js";
import { scrapeLinkedInJobs } from "../scrapers/linkedin_scraper.js";
import fs from "fs";

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
  " cybersecurity analyst", "information security manager",
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
  "AI product manager", "ML product manager", "data platform manager"
];

const LOCATIONS = [
  "Toronto, ON", "Mississauga, ON", "Vancouver, BC", "Montreal, QC",
  "Calgary, AB", "Ottawa, ON", "Edmonton, AB", "Winnipeg, MB",
  "Quebec City, QC", "Hamilton, ON", "Kitchener, ON", "Waterloo, ON",
  "London, ON", "Halifax, NS", "Victoria, BC"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function main() {
  console.log("🚀 FULL-SCALE INDEED + LINKEDIN SCRAPER\n");
  console.log(`Keywords: ${KEYWORDS.length}`);
  console.log(`Locations: ${LOCATIONS.length}`);
  console.log(`Total searches: ${KEYWORDS.length * 2} (Indeed + LinkedIn)\n`);
  
  const allJobs = [];
  const seen = new Set();
  let indeedCount = 0;
  let linkedinCount = 0;
  
  // Run Indeed and LinkedIn in parallel for each keyword
  for (let i = 0; i < KEYWORDS.length; i++) {
    const keyword = KEYWORDS[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    console.log(`\n[${i + 1}/${KEYWORDS.length}] "${keyword}" in ${location}`);
    
    // Run both scrapers in parallel
    const [indeedJobs, linkedinJobs] = await Promise.allSettled([
      scrapeIndeedJobs({ keyword, location, maxPages: 2, useFallbackApi: true }),
      scrapeLinkedInJobs(keyword, location, 0, 2, true)
    ]);
    
    // Process Indeed results
    if (indeedJobs.status === "fulfilled") {
      for (const job of indeedJobs.value) {
        const id = job.id || `indeed:${job.url || job.title}`;
        if (!seen.has(id)) {
          seen.add(id);
          allJobs.push({ ...job, id, source: "indeed" });
          indeedCount++;
        }
      }
      console.log(`  Indeed: ${indeedJobs.value.length} jobs`);
    } else {
      console.log(`  Indeed: FAILED - ${indeedJobs.reason?.message || "unknown"}`);
    }
    
    // Process LinkedIn results
    if (linkedinJobs.status === "fulfilled") {
      for (const job of linkedinJobs.value) {
        const id = job.id || `linkedin:${job.url || job.title}`;
        if (!seen.has(id)) {
          seen.add(id);
          allJobs.push({ ...job, id, source: "linkedin" });
          linkedinCount++;
        }
      }
      console.log(`  LinkedIn: ${linkedinJobs.value.length} jobs`);
    } else {
      console.log(`  LinkedIn: FAILED - ${linkedinJobs.reason?.message || "unknown"}`);
    }
    
    // Progress every 10 keywords
    if ((i + 1) % 10 === 0) {
      console.log(`\n📊 PROGRESS: ${allJobs.length} total jobs (${indeedCount} Indeed, ${linkedinCount} LinkedIn)`);
    }
    
    // Delay between keywords to avoid rate limiting
    await sleep(5000 + Math.random() * 3000);
    
    // Early exit if we hit 10K
    if (allJobs.length >= 10000) {
      console.log("\n🎉 Reached 10,000 jobs! Stopping...");
      break;
    }
  }
  
  console.log(`\n========================================`);
  console.log(`SCRAPING COMPLETE`);
  console.log(`========================================`);
  console.log(`Indeed jobs: ${indeedCount}`);
  console.log(`LinkedIn jobs: ${linkedinCount}`);
  console.log(`TOTAL NEW: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  // Load existing jobs
  let existingJobs = [];
  try {
    const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
    existingJobs = data.jobs || [];
    console.log(`Loaded ${existingJobs.length} existing jobs`);
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
      sources: Object.keys(bySource)
    },
    jobs: finalJobs
  }, null, 2));
  
  console.log(`\n✅ Saved to jobs.json`);
  
  // Progress
  const percent = ((finalJobs.length / 10000) * 100).toFixed(1);
  console.log(`\n📊 Progress: ${finalJobs.length}/10,000 (${percent}%)`);
  
  if (finalJobs.length < 10000) {
    console.log(`📊 Need ${10000 - finalJobs.length} more jobs`);
    console.log(`\n💡 The job sites are heavily protected. Consider:`);
    console.log(`   1. Setting RAPIDAPI_KEY for JSearch API`);
    console.log(`   2. Setting SERPAPI_KEY for Google Jobs API`);
    console.log(`   3. Using residential proxies (PROXY_LIST env var)`);
    console.log(`   4. Installing Playwright: npm install playwright`);
  } else {
    console.log(`\n🎉🎉🎉 REACHED 10,000 JOBS! 🎉🎉🎉`);
  }
}

main().catch(e => {
  console.error("Fatal error:", e);
  process.exit(1);
});
