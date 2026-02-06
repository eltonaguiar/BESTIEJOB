import axios from "axios";
import * as cheerio from "cheerio";

/**
 * Additional Scraper-Friendly Sources from Research
 * Jooble, USAJobs, Authentic Jobs, and other recommended sources
 */

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

// ==================== JOOBLE ====================
// Jooble is an aggregator with simpler HTML structure
export async function fetchJoobleJobs(keywords = ["developer"], location = "Toronto") {
  const jobs = [];
  try {
    console.log("[Jooble] Fetching jobs...");
    
    const searchQuery = keywords.join("+");
    const url = `https://ca.jooble.org/SearchResult?ukw=${searchQuery}&rgns=${encodeURIComponent(location)}`;
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": USER_AGENTS[0],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-CA,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    // Try multiple selectors as Jooble may change structure
    $("._8J6kJ, .job-card, [data-testid='jobListing'], .job").each((_, el) => {
      const titleEl = $(el).find("._1x9ZZ, .job-title, h2 a, a[href*='/jdp/']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find("._2r5qA, .company-name, .employer, [data-testid='company']").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locationEl = $(el).find("._1tK8A, .location, .job-location").first();
      const jobLocation = locationEl.text().trim() || location;
      
      const salaryEl = $(el).find("._3fD4A, .salary, .job-salary").first();
      const salary = salaryEl.text().trim() || null;
      
      if (title && title.length > 3 && company !== "Unknown") {
        jobs.push({
          id: `jooble:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
          source: "jooble",
          company,
          title,
          location: jobLocation,
          url: link.startsWith("http") ? link : `https://ca.jooble.org${link}`,
          employmentType: "full-time",
          salary,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[Jooble] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[Jooble] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== USAJOBS API ====================
// USAJobs has a documented public API: https://developer.usajobs.gov/
export async function fetchUSAJobs(apiKey = null) {
  const jobs = [];
  
  if (!apiKey) {
    console.log("[USAJobs] ⚠️  Requires API key - get one at https://developer.usajobs.gov/");
    console.log("[USAJobs] Skipping - no API key provided\n");
    return jobs;
  }
  
  try {
    console.log("[USAJobs] Fetching jobs via API...");
    
    // Search for IT/Software jobs with remote option
    const url = `https://data.usajobs.gov/api/search?Keyword=software&PositionScheduleTypeCode=1&ResultsPerPage=100`;
    
    const res = await axios.get(url, {
      timeout: 20000,
      headers: {
        "Host": "data.usajobs.gov",
        "User-Agent": "BESTIEJOB-Scraper/1.0",
        "Authorization-Key": apiKey,
        "Accept": "application/json"
      }
    });
    
    const results = res.data?.SearchResult?.SearchResultItems || [];
    
    for (const item of results) {
      const job = item.MatchedObjectDescriptor;
      
      // Check if remote or has Canadian/US locations
      const locations = job.PositionLocation || [];
      const locationStr = locations.map(l => l.LocationName).join(", ") || "United States";
      
      // Filter for relevant jobs
      const isRemote = job.PositionLocation?.some(l => 
        l.LocationName?.toLowerCase().includes("remote") ||
        l.LocationName?.toLowerCase().includes("anywhere")
      );
      
      jobs.push({
        id: `usajobs:${item.MatchedObjectId}`,
        source: "usajobs",
        company: job.OrganizationName || "US Government",
        title: job.PositionTitle,
        location: isRemote ? "Remote (US Government)" : locationStr,
        url: job.PositionURI,
        employmentType: job.PositionSchedule?.[0]?.Name || "full-time",
        salary: job.PositionRemuneration ? {
          min: job.PositionRemuneration[0]?.MinimumRange,
          max: job.PositionRemuneration[0]?.MaximumRange,
          currency: "USD"
        } : null,
        postedDate: job.PublicationStartDate || new Date().toISOString(),
        excerpt: job.QualificationSummary?.substring(0, 200) || job.PositionTitle
      });
    }
    
    console.log(`[USAJobs] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[USAJobs] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== AUTHENTIC JOBS ====================
// Authentic Jobs focuses on tech and design roles
export async function fetchAuthenticJobs() {
  const jobs = [];
  try {
    console.log("[AuthenticJobs] Fetching jobs...");
    
    // Try RSS feed first
    const Parser = (await import("rss-parser")).default;
    const parser = new Parser();
    
    const feed = await parser.parseURL("https://authenticjobs.com/rss/");
    
    for (const item of feed.items || []) {
      // Parse company from title (usually "Company: Title")
      let company = "Unknown";
      let title = item.title || "";
      
      if (title.includes(":")) {
        const parts = title.split(":");
        company = parts[0].trim();
        title = parts.slice(1).join(":").trim();
      }
      
      // Check if remote
      const isRemote = item.contentSnippet?.toLowerCase().includes("remote") ||
                      title.toLowerCase().includes("remote") ||
                      false;
      
      jobs.push({
        id: `authenticjobs:${Buffer.from(item.title || '').toString('base64').substring(0, 20)}`,
        source: "authenticjobs",
        company,
        title,
        location: isRemote ? "Remote" : "Various",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate || item.isoDate || new Date().toISOString(),
        excerpt: (item.contentSnippet || title).substring(0, 200)
      });
    }
    
    console.log(`[AuthenticJobs] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[AuthenticJobs] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== ANGELLIST/WELLFOUND (STARTUP JOBS) ====================
// AngelList has relatively accessible startup listings
export async function fetchAngelListJobs() {
  const jobs = [];
  try {
    console.log("[AngelList] Fetching startup jobs...");
    
    // Try their jobs page
    const url = "https://angel.co/jobs";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": USER_AGENTS[0],
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $("[data-testid='startup-job'], .job-listing, .listing").each((_, el) => {
      const titleEl = $(el).find("h3 a, .title a, a[href*='/jobs/']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".startup-name, .company-name").first();
      const company = companyEl.text().trim() || "Startup";
      
      if (title && title.length > 3) {
        jobs.push({
          id: `angellist:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
          source: "angellist",
          company,
          title,
          location: "Various / Remote",
          url: link.startsWith("http") ? link : `https://angel.co${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[AngelList] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[AngelList] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== FETCH ALL RESEARCH SOURCES ====================
export async function fetchAllResearchSources(usajobsApiKey = null) {
  console.log("\n🚀 FETCHING RESEARCH-BACKED JOB SOURCES\n");
  
  const allJobs = [];
  const results = {};
  
  // 1. Jooble
  const jooble = await fetchJoobleJobs();
  allJobs.push(...jooble);
  results.jooble = jooble.length;
  
  // 2. USAJobs (if API key available)
  const usajobs = await fetchUSAJobs(usajobsApiKey);
  allJobs.push(...usajobs);
  results.usajobs = usajobs.length;
  
  // 3. Authentic Jobs
  const authentic = await fetchAuthenticJobs();
  allJobs.push(...authentic);
  results.authentic = authentic.length;
  
  // 4. AngelList
  const angellist = await fetchAngelListJobs();
  allJobs.push(...angellist);
  results.angellist = angellist.length;
  
  console.log(`\n========================================`);
  console.log(`RESEARCH SOURCES RESULTS`);
  console.log(`========================================`);
  for (const [source, count] of Object.entries(results)) {
    const icon = count > 0 ? "✅" : "❌";
    console.log(`${icon} ${source}: ${count} jobs`);
  }
  console.log(`----------------------------------------`);
  console.log(`Total: ${allJobs.length} jobs`);
  console.log(`========================================\n`);
  
  return allJobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchAllResearchSources(process.env.USAJOBS_API_KEY)
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 5));
    })
    .catch(console.error);
}
