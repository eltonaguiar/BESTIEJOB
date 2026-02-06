import axios from "axios";

/**
 * ATS API Scrapers for structured job data
 * These APIs provide clean JSON without HTML parsing
 */

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ==================== GREENHOUSE API ====================
// https://api.greenhouse.io/v1/boards/{clientname}/jobs?content=true
export async function fetchGreenhouseJobs(companySlugs = []) {
  const jobs = [];
  
  // Verified working Greenhouse board slugs (tested 2026)
  const defaultSlugs = [
    // Major Tech (verified working)
    "stripe", "airbnb", "dropbox", "twilio", 
    "datadog", "elastic", "mongodb", "gitlab", "figma",
    "airtable", "asana", "cloudflare",
    // Fintech
    "affirm", "robinhood", "coinbase",
    // Canadian Companies (verified working)
    "hootsuite", "benevity", "d2l", "ecobee", "vidyard", "thinkific",
    // Enterprise/SaaS
    "intercom", "amplitude", "mixpanel", "postman", "launchdarkly",
    // AI/ML Companies (verified working)
    "anthropic",
    // Others verified working
    "gusto", "webflow", "notion", "linear", "vercel", "retool",
    "ramp", "mercury", "braintree", "square", "lyft", "instacart",
    "doordash", "grubhub", "toast", "chime", "sofi", "nubank"
  ];
  
  const slugs = companySlugs.length > 0 ? companySlugs : defaultSlugs;
  
  for (const slug of slugs) {
    try {
      const url = `https://api.greenhouse.io/v1/boards/${slug}/jobs?content=true`;
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": USER_AGENTS[0],
          "Accept": "application/json"
        }
      });
      
      const jobList = res.data?.jobs || [];
      
      for (const job of jobList) {
        const locations = job.location?.name || "Remote";
        
        // Filter for Canada/remote positions
        if (locations.toLowerCase().includes("canada") || 
            locations.toLowerCase().includes("toronto") ||
            locations.toLowerCase().includes("vancouver") ||
            locations.toLowerCase().includes("remote") ||
            locations.toLowerCase().includes("north america")) {
          
          jobs.push({
            id: `greenhouse:${slug}:${job.id}`,
            source: "greenhouse",
            company: res.data.name || slug,
            title: job.title,
            location: locations,
            url: job.absolute_url || job.url,
            employmentType: job.metadata?.find(m => m.name === "Employment Type")?.value || "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: job.content?.substring(0, 200) || job.title
          });
        }
      }
      
      await sleep(300);
      
    } catch (err) {
      console.error(`[Greenhouse] ${slug}: ${err.message}`);
    }
  }
  
  console.log(`[Greenhouse] Total jobs found: ${jobs.length}`);
  return jobs;
}

// ==================== LEVER API ====================
// https://api.lever.co/v0/postings/{clientname}?mode=json
export async function fetchLeverJobs(companySlugs = []) {
  const jobs = [];
  
  const defaultSlugs = [
    // Major Tech
    "netflix", "uber", "notion", "figma", "linear", "vercel", 
    "rippling", "deel", "remote", "gusto", "brex", "plaid",
    // Growing startups
    "superhuman", "lattice", "loom", "pitch", "rows", "ashby",
    "webflow", "substack", "cal-com", "dbt-labs", "airbyte",
    // Canadian/Remote-friendly
    "clearbit", "dutchie", "netlify", "prisma", "supabase",
    // Enterprise
    "twilio", "contentful", "miro", "lucid", "clickup"
  ];
  
  const slugs = companySlugs.length > 0 ? companySlugs : defaultSlugs;
  
  for (const slug of slugs) {
    try {
      const url = `https://api.lever.co/v0/postings/${slug}?mode=json`;
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": USER_AGENTS[0],
          "Accept": "application/json"
        }
      });
      
      const jobList = res.data || [];
      
      for (const job of jobList) {
        const locations = job.categories?.location || "Remote";
        
        // Filter for Canada/remote
        if (locations.toLowerCase().includes("canada") || 
            locations.toLowerCase().includes("toronto") ||
            locations.toLowerCase().includes("vancouver") ||
            locations.toLowerCase().includes("remote") ||
            locations.toLowerCase().includes("north america") ||
            locations.toLowerCase().includes("anywhere")) {
          
          jobs.push({
            id: `lever:${slug}:${job.id || job.text}`,
            source: "lever",
            company: job.categories?.team || slug,
            title: job.text,
            location: locations,
            url: job.applyUrl || job.hostedUrl,
            employmentType: job.categories?.commitment || "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: job.description?.substring(0, 200) || job.text
          });
        }
      }
      
      await sleep(300);
      
    } catch (err) {
      console.error(`[Lever] ${slug}: ${err.message}`);
    }
  }
  
  console.log(`[Lever] Total jobs found: ${jobs.length}`);
  return jobs;
}

// ==================== ASHBY API ====================
// https://api.ashbyhq.com/posting-api/job-board/{clientname}
export async function fetchAshbyJobs(companySlugs = []) {
  const jobs = [];
  
  // Verified working Ashby board slugs
  const defaultSlugs = [
    // AI/ML/Dev Tools (verified working)
    "mercury", "ramp", "retool", "elevenlabs", "cursor",
    "replit", "perplexity", "runway",
    // Fintech
    "moderntreasury", "column",
    // Dev/Infrastructure
    "railway", "render", "neon"
  ];
  
  const slugs = companySlugs.length > 0 ? companySlugs : defaultSlugs;
  
  for (const slug of slugs) {
    try {
      const url = `https://api.ashbyhq.com/posting-api/job-board/${slug}`;
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": USER_AGENTS[0],
          "Accept": "application/json"
        }
      });
      
      const jobList = res.data?.jobs || [];
      
      for (const job of jobList) {
        const locations = job.location || "Remote";
        
        // Filter for Canada/remote
        if (locations.toLowerCase().includes("canada") || 
            locations.toLowerCase().includes("toronto") ||
            locations.toLowerCase().includes("vancouver") ||
            locations.toLowerCase().includes("remote") ||
            locations.toLowerCase().includes("north america")) {
          
          jobs.push({
            id: `ashby:${slug}:${job.id}`,
            source: "ashby",
            company: res.data?.jobBoard?.name || slug,
            title: job.title,
            location: locations,
            url: job.jobUrl,
            employmentType: job.employmentType || "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: job.descriptionHtml?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
          });
        }
      }
      
      await sleep(300);
      
    } catch (err) {
      console.error(`[Ashby] ${slug}: ${err.message}`);
    }
  }
  
  console.log(`[Ashby] Total jobs found: ${jobs.length}`);
  return jobs;
}

// ==================== WORKABLE API ====================
// https://apply.workable.com/api/v1/widget/accounts/{clientname}?details=true
export async function fetchWorkableJobs(companySlugs = []) {
  const jobs = [];
  
  const defaultSlugs = [
    "canonical", "automattic", "invision", "trello", "atlassian"
  ];
  
  const slugs = companySlugs.length > 0 ? companySlugs : defaultSlugs;
  
  for (const slug of slugs) {
    try {
      const url = `https://apply.workable.com/api/v1/widget/accounts/${slug}`;
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": USER_AGENTS[0],
          "Accept": "application/json"
        }
      });
      
      const jobList = res.data?.jobs || [];
      
      for (const job of jobList) {
        const locations = job.location?.location_str || "Remote";
        
        // Filter for Canada/remote
        if (locations.toLowerCase().includes("canada") || 
            locations.toLowerCase().includes("toronto") ||
            locations.toLowerCase().includes("vancouver") ||
            locations.toLowerCase().includes("remote") ||
            locations.toLowerCase().includes("north america")) {
          
          jobs.push({
            id: `workable:${slug}:${job.shortcode}`,
            source: "workable",
            company: res.data?.name || slug,
            title: job.title,
            location: locations,
            url: job.application_url || job.url,
            employmentType: job.employment_type || "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: job.description?.substring(0, 200) || job.title
          });
        }
      }
      
      await sleep(300);
      
    } catch (err) {
      console.error(`[Workable] ${slug}: ${err.message}`);
    }
  }
  
  console.log(`[Workable] Total jobs found: ${jobs.length}`);
  return jobs;
}

// ==================== BATCH FETCH ALL ATS JOBS ====================
export async function fetchAllATSJobs() {
  console.log("\n🚀 FETCHING ALL ATS API JOBS\n");
  
  const allJobs = [];
  
  const greenhouseJobs = await fetchGreenhouseJobs();
  allJobs.push(...greenhouseJobs);
  
  const leverJobs = await fetchLeverJobs();
  allJobs.push(...leverJobs);
  
  const ashbyJobs = await fetchAshbyJobs();
  allJobs.push(...ashbyJobs);
  
  const workableJobs = await fetchWorkableJobs();
  allJobs.push(...workableJobs);
  
  console.log(`\n========================================`);
  console.log(`ATS API FETCH COMPLETE`);
  console.log(`Total ATS jobs: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  return allJobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchAllATSJobs()
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 5));
    })
    .catch(console.error);
}
