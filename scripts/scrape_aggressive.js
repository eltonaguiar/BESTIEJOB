import axios from "axios";
import Parser from "rss-parser";
import fs from "fs";

const rssParser = new Parser({ timeout: 10000 });

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ==================== SOURCE 1: Lever.co Job Boards (Many companies use this) ====================
async function scrapeLever() {
  const jobs = [];
  // List of companies using Lever
  const companies = [
    "shopify", "stripe", "discord", "figma", "notion", "vercel",
    "linear", "raycast", "supabase", "planetscale", "railway",
    "render", "replicate", "resend", "twilio", "segment"
  ];
  
  for (const company of companies) {
    try {
      const url = `https://jobs.lever.co/${company}`;
      const response = await axios.get(url, {
        headers: {
          "User-Agent": USER_AGENTS[0],
          "Accept": "text/html"
        },
        timeout: 10000
      });
      
      const html = response.data;
      // Extract job data from embedded JSON
      const matches = html.match(/window\.leverJobsList = (\[.*?\]);/);
      if (matches && matches[1]) {
        const jobData = JSON.parse(matches[1]);
        for (const post of jobData) {
          // Look for Toronto or remote positions
          const loc = post.categories?.location || "";
          if (loc.toLowerCase().includes("toronto") || 
              loc.toLowerCase().includes("remote") || 
              loc.toLowerCase().includes("canada") ||
              loc.toLowerCase().includes("north america")) {
            jobs.push({
              id: `lever:${company}:${post.id}`,
              source: "lever",
              company: post.hiringOrganization?.name || company,
              title: post.title,
              location: loc,
              url: post.applyUrl || post.url || `https://jobs.lever.co/${company}/${post.id}`,
              employmentType: post.categories?.commitment || "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: `${post.title} at ${company} - ${loc}`
            });
          }
        }
      }
      console.log(`[Lever] ${company}: ${jobs.filter(j => j.company.toLowerCase().includes(company)).length} jobs`);
      await sleep(1000);
    } catch (e) {
      // Silent fail - many companies don't use lever or block
    }
  }
  
  console.log(`[Lever] Total: ${jobs.length} jobs`);
  return jobs;
}

// ==================== SOURCE 2: Greenhouse Job Boards ====================
async function scrapeGreenhouse() {
  const jobs = [];
  const companies = [
    "airbnb", "dropbox", "slack", "zoom", "asana", "notion",
    "figma", "vercel", "linear", "raycast", "github", "gitlab"
  ];
  
  for (const company of companies) {
    try {
      const url = `https://boards.greenhouse.io/${company}`;
      const response = await axios.get(url, {
        headers: { "User-Agent": USER_AGENTS[0] },
        timeout: 10000
      });
      
      const html = response.data;
      // Greenhouse uses embedded JSON
      const matches = html.match(/window\._initialProps = (\{.*?\});/s);
      if (matches && matches[1]) {
        const data = JSON.parse(matches[1]);
        const postings = data?.jobPosts || [];
        
        for (const post of postings) {
          const loc = post.location || "";
          if (loc.toLowerCase().includes("toronto") || 
              loc.toLowerCase().includes("remote") ||
              loc.toLowerCase().includes("canada")) {
            jobs.push({
              id: `greenhouse:${company}:${post.id}`,
              source: "greenhouse",
              company: post.hiringOrganization?.name || company,
              title: post.title,
              location: loc,
              url: `https://boards.greenhouse.io/${company}/jobs/${post.id}`,
              employmentType: "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: `${post.title} at ${company} - ${loc}`
            });
          }
        }
      }
      await sleep(1000);
    } catch (e) {}
  }
  
  console.log(`[Greenhouse] Total: ${jobs.length} jobs`);
  return jobs;
}

// ==================== SOURCE 3: Workday Job Boards ====================
async function scrapeWorkday() {
  const jobs = [];
  const companies = [
    { name: "Air Canada", url: "https://aircanada.wd101.myworkdayjobs.com/en-US/ac_careers" },
    { name: "RBC", url: "https://jobs.rbc.com/ca/en" },
    { name: "TD Bank", url: "https://td.wd102.myworkdayjobs.com/en-US/TD_Bank_Careers" },
    { name: "Scotiabank", url: "https://scotiabank.wd101.myworkdayjobs.com/en-US/careers" },
    { name: "CIBC", url: "https://cibc.wd103.myworkdayjobs.com/en-US/careers" },
    { name: "Shopify", url: "https://shopify.wd102.myworkdayjobs.com/en-US/Shopify_Careers" }
  ];
  
  for (const { name, url } of companies) {
    try {
      const response = await axios.get(url, {
        headers: { "User-Agent": USER_AGENTS[0] },
        timeout: 10000
      });
      
      const html = response.data;
      // Workday usually embeds JSON
      const matches = html.match(/window\.__INITIAL_STATE__ = (\{.*?\});/s) ||
                     html.match(/window\.__DATA__ = (\{.*?\});/s);
      
      if (matches && matches[1]) {
        try {
          const data = JSON.parse(matches[1]);
          const jobList = data?.jobList || data?.jobs || [];
          
          for (const job of jobList.slice(0, 20)) {
            jobs.push({
              id: `workday:${name}:${job.id || Math.random()}`,
              source: "workday",
              company: name,
              title: job.title || job.name,
              location: job.location || "Toronto, ON",
              url: job.url || url,
              employmentType: "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: `${job.title || job.name} at ${name}`
            });
          }
        } catch (e) {}
      }
      console.log(`[Workday] ${name}: extracted`);
      await sleep(1000);
    } catch (e) {}
  }
  
  console.log(`[Workday] Total: ${jobs.length} jobs`);
  return jobs;
}

// ==================== SOURCE 4: Stack Overflow Jobs API ====================
async function scrapeStackOverflow() {
  const jobs = [];
  try {
    // Stack Overflow Jobs RSS
    const url = "https://stackoverflow.com/jobs/feed";
    const feed = await rssParser.parseURL(url);
    
    for (const item of feed.items || []) {
      const loc = item.categories?.find(c => c.includes("loc:")) || "";
      const isToronto = loc.toLowerCase().includes("toronto") || loc.toLowerCase().includes("canada");
      const isRemote = loc.toLowerCase().includes("remote");
      
      if (isToronto || isRemote) {
        jobs.push({
          id: `stackoverflow:${item.guid || Math.random()}`,
          source: "stackoverflow",
          company: item.author || "Unknown",
          title: item.title?.replace(/at .*$/, "").trim(),
          location: isRemote ? "Remote" : "Toronto, ON",
          url: item.link,
          employmentType: "full-time",
          salary: null,
          postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
          excerpt: item.contentSnippet?.substring(0, 240) || item.title
        });
      }
    }
    console.log(`[StackOverflow] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[StackOverflow] error: ${e.message}`);
  }
  return jobs;
}

// ==================== SOURCE 5: GitHub Jobs (from various sources) ====================
async function scrapeGitHubJobs() {
  const jobs = [];
  try {
    // GitHub ReadME project job board
    const url = "https://api.github.com/repos/ReadME-Co/jobs/contents/jobs.json";
    // This won't work without auth, try alternative
    
    // Try GitHub Issues "Who's Hiring"
    const issuesUrl = "https://api.github.com/repos/whoishiring/whoishiring/issues?state=open&per_page=5";
    const response = await axios.get(issuesUrl, {
      headers: { 
        "User-Agent": USER_AGENTS[0],
        "Accept": "application/vnd.github.v3+json"
      },
      timeout: 10000
    });
    
    for (const issue of response.data || []) {
      // Extract jobs from issue body
      const body = issue.body || "";
      const lines = body.split("\n").filter(l => l.trim().startsWith("|"));
      
      for (const line of lines.slice(1)) { // Skip header
        const parts = line.split("|").filter(p => p.trim());
        if (parts.length >= 3) {
          const company = parts[0]?.trim();
          const title = parts[1]?.trim();
          const loc = parts[2]?.trim();
          
          if (title && (loc?.toLowerCase().includes("toronto") || loc?.toLowerCase().includes("remote"))) {
            jobs.push({
              id: `github:${issue.number}:${Math.random()}`,
              source: "github",
              company,
              title,
              location: loc,
              url: issue.html_url,
              employmentType: "full-time",
              salary: null,
              postedDate: issue.created_at,
              excerpt: `${title} at ${company}`
            });
          }
        }
      }
    }
    console.log(`[GitHub] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[GitHub] error: ${e.message}`);
  }
  return jobs;
}

// ==================== SOURCE 6: Canadian Tech Companies Direct ====================
async function scrapeCanadianTechCompanies() {
  const jobs = [];
  
  // List of Canadian tech companies with public job feeds
  const companies = [
    { name: "Wealthsimple", url: "https://jobs.lever.co/wealthsimple" },
    { name: "Clearco", url: "https://jobs.lever.co/clearbanc" },
    { name: "1Password", url: "https://jobs.lever.co/1password" },
    { name: "Freshbooks", url: "https://www.freshbooks.com/careers" },
    { name: "Wave", url: "https://www.waveapps.com/about-us/careers" },
    { name: "Hootsuite", url: "https://careers.hootsuite.com" },
    { name: "Slack", url: "https://slack.com/careers" },
    { name: "Shopify", url: "https://www.shopify.com/careers" },
    { name: "Kijiji", url: "https://careers.kijiji.ca" },
    { name: "VarageSale", url: "https://www.varagesale.com/careers" }
  ];
  
  for (const { name, url } of companies) {
    try {
      if (url.includes("lever.co")) {
        // Use Lever scraper logic
        const response = await axios.get(url, {
          headers: { "User-Agent": USER_AGENTS[0] },
          timeout: 8000
        });
        
        const html = response.data;
        const matches = html.match(/window\.leverJobsList = (\[.*?\]);/);
        if (matches && matches[1]) {
          const jobData = JSON.parse(matches[1]);
          for (const post of jobData.slice(0, 10)) {
            jobs.push({
              id: `canadian:${name}:${post.id}`,
              source: "canadian_tech",
              company: name,
              title: post.title,
              location: post.categories?.location || "Toronto, ON",
              url: post.applyUrl || `${url}/${post.id}`,
              employmentType: "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: `${post.title} at ${name}`
            });
          }
        }
      }
      await sleep(800);
    } catch (e) {}
  }
  
  console.log(`[Canadian Tech] Total: ${jobs.length} jobs`);
  return jobs;
}

// ==================== SOURCE 7: JobBank Canada (Expand search) ====================
async function expandJobBank() {
  const jobs = [];
  const seen = new Set();
  
  const KEYWORDS = [
    "software", "developer", "engineer", "programmer", "coder",
    "analyst", "manager", "director", "lead", "architect",
    "consultant", "specialist", "administrator", "coordinator",
    "designer", "tester", "support", "technician", "devops",
    "data", "cloud", "security", "network", "systems"
  ];
  
  for (const keyword of KEYWORDS) {
    try {
      const url = `https://www.jobbank.gc.ca/jobsearch/api/jobsearch?searchstring=${encodeURIComponent(keyword)}&locationstring=Toronto%2C+ON&sort=M&page=1&pagesize=100`;
      const response = await axios.get(url, {
        headers: { "User-Agent": USER_AGENTS[0] },
        timeout: 10000
      });
      
      const data = response.data;
      const results = data?.results || data?.jobs || [];
      
      for (const job of results.slice(0, 50)) {
        const id = `jobbank:${job.id || job.jobId}`;
        if (!seen.has(id)) {
          seen.add(id);
          jobs.push({
            id,
            source: "jobbank",
            company: job.employerName || "Government of Canada",
            title: job.title || job.jobTitle,
            location: job.location || "Toronto, ON",
            url: job.url || `https://www.jobbank.gc.ca/jobsearch/jobposting/${job.id}`,
            employmentType: job.type || "full-time",
            salary: job.salary ? { min: parseInt(job.salary) * 1000, max: parseInt(job.salary) * 1000 } : null,
            postedDate: job.datePosted || new Date().toISOString(),
            excerpt: job.description?.substring(0, 240) || `${job.title} at ${job.employerName}`
          });
        }
      }
      
      if (jobs.length % 100 === 0) {
        console.log(`[JobBank] "${keyword}": ${jobs.length} total`);
      }
      await sleep(500);
    } catch (e) {}
  }
  
  console.log(`[JobBank Expanded] Total: ${jobs.length} jobs`);
  return jobs;
}

// ==================== SOURCE 8: Toronto Municipal Jobs ====================
async function scrapeTorontoJobs() {
  const jobs = [];
  try {
    const url = "https://jobs.toronto.ca/public/en/listings";
    const response = await axios.get(url, {
      headers: { "User-Agent": USER_AGENTS[0] },
      timeout: 10000
    });
    
    const html = response.data;
    // Extract job listings
    const jobMatches = html.matchAll(/data-job-id="(\d+)"[^>]*>.*?<h[23][^>]*>(.*?)<\/h[23]>.*?<\/article>/gs);
    
    for (const match of jobMatches) {
      const id = match[1];
      const title = match[2]?.replace(/<[^>]+>/g, "").trim();
      
      if (title) {
        jobs.push({
          id: `toronto:${id}`,
          source: "toronto",
          company: "City of Toronto",
          title,
          location: "Toronto, ON",
          url: `https://jobs.toronto.ca/public/en/jobs/${id}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at City of Toronto`
        });
      }
    }
    console.log(`[Toronto Jobs]: ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Toronto Jobs] error: ${e.message}`);
  }
  return jobs;
}

// ==================== MAIN ====================
async function main() {
  console.log("🚀 AGGRESSIVE JOB SCRAPER - Target: 10,000 jobs\n");
  
  const allJobs = [];
  const seen = new Set();
  
  // Run all scrapers in parallel batches
  const batch1 = await Promise.allSettled([
    scrapeLever(),
    scrapeGreenhouse(),
    scrapeWorkday(),
    scrapeStackOverflow()
  ]);
  
  for (const result of batch1) {
    if (result.status === "fulfilled") {
      for (const job of result.value) {
        if (!seen.has(job.id)) {
          seen.add(job.id);
          allJobs.push(job);
        }
      }
    }
  }
  
  console.log(`\n📊 After batch 1: ${allJobs.length} jobs`);
  
  const batch2 = await Promise.allSettled([
    scrapeGitHubJobs(),
    scrapeCanadianTechCompanies(),
    expandJobBank(),
    scrapeTorontoJobs()
  ]);
  
  for (const result of batch2) {
    if (result.status === "fulfilled") {
      for (const job of result.value) {
        if (!seen.has(job.id)) {
          seen.add(job.id);
          allJobs.push(job);
        }
      }
    }
  }
  
  console.log(`\n📊 New jobs scraped: ${allJobs.length}`);
  
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
  const remaining = 10000 - finalJobs.length;
  if (remaining > 0) {
    console.log(`\n📊 Progress: ${finalJobs.length}/10,000 (${((finalJobs.length/10000)*100).toFixed(1)}%)`);
    console.log(`📊 Need ${remaining} more jobs`);
  } else {
    console.log(`\n🎉 REACHED 10,000 JOBS!`);
  }
}

main();
