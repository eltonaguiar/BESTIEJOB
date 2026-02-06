import axios from "axios";
import fs from "fs";

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

// Tech programming languages and skills
const TECH_KEYWORDS = [
  "Python", "JavaScript", "Java", "C++", "C#", "SQL", "PHP", "Ruby", "Go", "Rust",
  "Swift", "Kotlin", "TypeScript", "React", "Angular", "Vue", "Node.js", "Django",
  "Flask", "Spring", "ASP.NET", "Laravel", "Rails", "AWS", "Azure", "GCP",
  "Docker", "Kubernetes", "DevOps", "Machine Learning", "Data Science", "AI",
  "Blockchain", "Solidity", "Smart Contracts", "Cybersecurity", "Network Engineer",
  "Database Administrator", "Full Stack Developer", "Frontend Developer", "Backend Developer",
  "Mobile Developer", "iOS Developer", "Android Developer", "Game Developer",
  "Embedded Systems", "IoT", "Cloud Engineer", "Site Reliability Engineer",
  "QA Engineer", "Test Automation", "Selenium", "Jenkins", "Git", "GitHub",
  "Linux", "Windows Server", "Unix", "Bash", "PowerShell", "Tableau", "Power BI",
  "Excel", "VBA", "R", "MATLAB", "SAS", "SPSS", "Hadoop", "Spark", "Kafka",
  "Elasticsearch", "MongoDB", "PostgreSQL", "MySQL", "Oracle", "Redis",
  "GraphQL", "REST API", "SOAP", "Microservices", "Serverless", "Lambda",
  "Terraform", "Ansible", "Puppet", "Chef", "Splunk", "Datadog", "New Relic"
];

// Business and management roles
const BUSINESS_KEYWORDS = [
  "Project Manager", "Product Manager", "Program Manager", "Business Analyst",
  "Data Analyst", "Financial Analyst", "Marketing Manager", "Sales Manager",
  "Account Manager", "Customer Success Manager", "Operations Manager",
  "Supply Chain Manager", "Logistics Manager", "Procurement Manager",
  "HR Manager", "Talent Acquisition", "Recruiter", "HR Business Partner",
  "Finance Manager", "Accounting Manager", "Controller", "Treasury Manager",
  "Risk Manager", "Compliance Manager", "Legal Counsel", "Contract Manager",
  "Quality Assurance Manager", "Process Improvement", "Six Sigma", "Lean",
  "Change Management", "Strategy Consultant", "Management Consultant",
  "IT Manager", "CTO", "CIO", "VP Engineering", "Director of Engineering",
  "Engineering Manager", "Tech Lead", "Team Lead", "Scrum Master", "Agile Coach",
  "Business Development", "Partnerships Manager", "Channel Manager",
  "Enterprise Sales", "Solution Architect", "Technical Architect",
  "Systems Architect", "Infrastructure Architect", "Security Architect",
  "Data Architect", "Information Architect", "UX Manager", "Design Manager",
  "Creative Director", "Art Director", "Content Manager", "Brand Manager",
  "Communications Manager", "PR Manager", "Social Media Manager",
  "Digital Marketing Manager", "SEO Manager", "SEM Manager",
  "E-commerce Manager", "Product Owner", "Delivery Manager", "Release Manager"
];

const LOCATIONS = [
  "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton", "Winnipeg",
  "Victoria", "Halifax", "Quebec City", "Hamilton", "Kitchener", "Waterloo",
  "London", "Windsor", "Oshawa", "Guelph", "Barrie", "Kingston", "St. Catharines"
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
  console.log("🚀 SCRAPING TECH & BUSINESS JOBS\n");
  
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
  let newCount = 0;
  let apiCalls = 0;
  
  // Combine all keywords
  const allKeywords = [...TECH_KEYWORDS, ...BUSINESS_KEYWORDS];
  
  console.log(`\nScraping ${allKeywords.length} keywords across ${LOCATIONS.length} locations...\n`);
  
  // Scrape tech and business jobs
  for (let i = 0; i < allKeywords.length && allJobs.length < 15000; i++) {
    const keyword = allKeywords[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    // Page 1
    const jobs = await fetchAdzunaJobs(keyword, location, 1, 100);
    apiCalls++;
    
    for (const job of jobs) {
      if (!existingIds.has(job.id)) {
        existingIds.add(job.id);
        allJobs.push(job);
        newCount++;
      }
    }
    
    if ((i + 1) % 10 === 0) {
      console.log(`[${i + 1}/${allKeywords.length}] ${keyword} in ${location}: +${newCount} new, ${allJobs.length} total`);
    }
    
    await sleep(200);
    
    if (allJobs.length >= 15000) {
      console.log("\n🎉 Reached 15,000 jobs!");
      break;
    }
  }
  
  console.log(`\n========================================`);
  console.log(`SCRAPING COMPLETE`);
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
