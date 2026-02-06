import axios from "axios";
import * as cheerio from "cheerio";
import Parser from "rss-parser";

const rssParser = new Parser();

/**
 * Additional Aggregator Scrapers
 * Based on research: Jooble, CareerJet, USAJobs, Talent.com, Monster, CareerBuilder, ZipRecruiter
 */

// ==================== JOOBLE ====================
// Jooble has a simple search interface and some API access
export async function fetchJoobleJobs(keywords = ["developer"], location = "Toronto") {
  const jobs = [];
  try {
    console.log("[Jooble] Fetching jobs...");
    
    // Jooble search URL pattern
    const searchQuery = keywords.join("+");
    const url = `https://ca.jooble.org/SearchResult?ukw=${searchQuery}&rgns=${encodeURIComponent(location)}`;
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $("._8J6kJ, .job-card, [data-testid='jobListing']").each((_, el) => {
      const titleEl = $(el).find("._1x9ZZ, .job-title, h2 a, a[href*='/jdp/']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find("._2r5qA, .company-name, .employer").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locationEl = $(el).find("._1tK8A, .location, .job-location").first();
      const jobLocation = locationEl.text().trim() || location;
      
      if (title && title.length > 3) {
        jobs.push({
          id: `jooble:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
          source: "jooble",
          company,
          title,
          location: jobLocation,
          url: link.startsWith("http") ? link : `https://ca.jooble.org${link}`,
          employmentType: "full-time",
          salary: null,
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

// ==================== CAREERJET ====================
// CareerJet has international coverage and simpler HTML
export async function fetchCareerJetJobs(keywords = ["developer"], location = "Toronto, ON") {
  const jobs = [];
  try {
    console.log("[CareerJet] Fetching jobs...");
    
    // CareerJet Canada URL
    const searchQuery = keywords.join("+");
    const url = `https://www.careerjet.ca/search/jobs?s=${searchQuery}&l=${encodeURIComponent(location)}`;
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $(".job, .job-display, article").each((_, el) => {
      const titleEl = $(el).find(".title a, h2 a, a[href*='/job/']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".company, .job-company").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locationEl = $(el).find(".locations, .job-location").first();
      const jobLocation = locationEl.text().trim() || location;
      
      const salaryEl = $(el).find(".salary, .job-salary").first();
      const salary = salaryEl.text().trim() || null;
      
      if (title && title.length > 3) {
        jobs.push({
          id: `careerjet:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
          source: "careerjet",
          company,
          title,
          location: jobLocation,
          url: link.startsWith("http") ? link : `https://www.careerjet.ca${link}`,
          employmentType: "full-time",
          salary,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[CareerJet] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[CareerJet] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== TALENT.COM (NEUVOO) ====================
// Talent.com has XML feeds and simple HTML
export async function fetchTalentJobs(keywords = ["developer"], location = "Toronto") {
  const jobs = [];
  try {
    console.log("[Talent.com] Fetching jobs...");
    
    const searchQuery = keywords.join("-");
    const url = `https://ca.talent.com/jobs?k=${searchQuery}&l=${encodeURIComponent(location)}&r=us-ca`;
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $("[data-job-id], .cvo, .job-card").each((_, el) => {
      const titleEl = $(el).find("h2 a, .title a, a[data-link='title']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".cvo-company-name, .company, [data-link='company']").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locationEl = $(el).find(".cvo-location, .location").first();
      const jobLocation = locationEl.text().trim() || location;
      
      if (title && title.length > 3) {
        jobs.push({
          id: `talent:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
          source: "talent",
          company,
          title,
          location: jobLocation,
          url: link.startsWith("http") ? link : `https://ca.talent.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[Talent.com] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[Talent.com] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== MONSTER ====================
// Monster has simpler structure than LinkedIn
export async function fetchMonsterJobs(keywords = ["developer"], location = "Toronto, ON") {
  const jobs = [];
  try {
    console.log("[Monster] Fetching jobs...");
    
    const searchQuery = keywords.join("-");
    const url = `https://www.monster.ca/jobs/search?q=${searchQuery}&where=${encodeURIComponent(location)}`;
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $("[data-testid='card'], .job-card, .results-card").each((_, el) => {
      const titleEl = $(el).find(".jobTitle, h3 a, a[data-testid='jobTitle']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".companyName, .job-company").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locationEl = $(el).find(".jobLocation, .location").first();
      const jobLocation = locationEl.text().trim() || location;
      
      if (title && title.length > 3) {
        jobs.push({
          id: `monster:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
          source: "monster",
          company,
          title,
          location: jobLocation,
          url: link.startsWith("http") ? link : `https://www.monster.ca${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[Monster] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[Monster] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== CAREERBUILDER ====================
export async function fetchCareerBuilderJobs(keywords = ["developer"], location = "Toronto, ON") {
  const jobs = [];
  try {
    console.log("[CareerBuilder] Fetching jobs...");
    
    const searchQuery = keywords.join("+");
    const url = `https://www.careerbuilder.com/jobs?keywords=${searchQuery}&location=${encodeURIComponent(location)}`;
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $(".job-row, .data-results-content, .job-card").each((_, el) => {
      const titleEl = $(el).find(".job-title, h2 a, .data-results-title a").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".job-text.emp-name, .company-name").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locationEl = $(el).find(".job-text.location, .job-location").first();
      const jobLocation = locationEl.text().trim() || location;
      
      if (title && title.length > 3) {
        jobs.push({
          id: `careerbuilder:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
          source: "careerbuilder",
          company,
          title,
          location: jobLocation,
          url: link.startsWith("http") ? link : `https://www.careerbuilder.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[CareerBuilder] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[CareerBuilder] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== ZIPRECRUITER ====================
export async function fetchZipRecruiterJobs(keywords = ["developer"], location = "Toronto, ON") {
  const jobs = [];
  try {
    console.log("[ZipRecruiter] Fetching jobs...");
    
    const searchQuery = keywords.join("+");
    const url = `https://www.ziprecruiter.ca/jobs-search?search=${searchQuery}&location=${encodeURIComponent(location)}`;
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $(".job_content, article, [data-testid='jobListing']").each((_, el) => {
      const titleEl = $(el).find(".job_title, h2 a, a[href*='/jobs/']").first();
      const title = titleEl.text().trim();
      const link = titleEl.attr("href") || "";
      
      const companyEl = $(el).find(".job_org, .company-name, .hiring_company").first();
      const company = companyEl.text().trim() || "Unknown";
      
      const locationEl = $(el).find(".job_location, .location").first();
      const jobLocation = locationEl.text().trim() || location;
      
      if (title && title.length > 3) {
        jobs.push({
          id: `ziprecruiter:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
          source: "ziprecruiter",
          company,
          title,
          location: jobLocation,
          url: link.startsWith("http") ? link : `https://www.ziprecruiter.ca${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
    console.log(`[ZipRecruiter] Found ${jobs.length} jobs`);
  } catch (e) {
    console.error(`[ZipRecruiter] Failed: ${e.message}`);
  }
  return jobs;
}

// ==================== USAJOBS (US GOVERNMENT API) ====================
// USAJobs has a documented public API: https://developer.usajobs.gov/
// Note: Requires API key registration
export async function fetchUSAJobs(apiKey = null) {
  const jobs = [];
  
  if (!apiKey) {
    console.log("[USAJobs] Skipped - requires API key (get one at developer.usajobs.gov)");
    return jobs;
  }
  
  try {
    console.log("[USAJobs] Fetching jobs via API...");
    
    // Search for IT/tech jobs
    const url = `https://data.usajobs.gov/api/search?Keyword=developer&LocationName=Remote&ResultsPerPage=100`;
    
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
      jobs.push({
        id: `usajobs:${item.MatchedObjectId}`,
        source: "usajobs",
        company: job.OrganizationName || "US Government",
        title: job.PositionTitle,
        location: job.PositionLocation?.map(l => l.LocationName).join(", ") || "Remote",
        url: job.PositionURI,
        employmentType: job.PositionSchedule?.[0]?.Name || "full-time",
        salary: job.PositionRemuneration ? {
          min: job.PositionRemuneration[0]?.MinimumRange,
          max: job.PositionRemuneration[0]?.MaximumRange
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

// ==================== FETCH ALL AGGREGATOR JOBS ====================
export async function fetchAllAggregatorJobs() {
  console.log("\n🚀 FETCHING ALL AGGREGATOR SOURCES\n");
  
  const allJobs = [];
  
  const jooble = await fetchJoobleJobs();
  allJobs.push(...jooble);
  
  const careerjet = await fetchCareerJetJobs();
  allJobs.push(...careerjet);
  
  const talent = await fetchTalentJobs();
  allJobs.push(...talent);
  
  const monster = await fetchMonsterJobs();
  allJobs.push(...monster);
  
  const careerbuilder = await fetchCareerBuilderJobs();
  allJobs.push(...careerbuilder);
  
  const ziprecruiter = await fetchZipRecruiterJobs();
  allJobs.push(...ziprecruiter);
  
  // USAJobs requires API key
  // const usajobs = await fetchUSAJobs(process.env.USAJOBS_API_KEY);
  // allJobs.push(...usajobs);
  
  console.log(`\n========================================`);
  console.log(`AGGREGATOR SOURCES COMPLETE`);
  console.log(`Total jobs: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  return allJobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchAllAggregatorJobs()
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 5));
    })
    .catch(console.error);
}
