import axios from "axios";
import * as cheerio from "cheerio";

/**
 * Direct Company Career Pages Scraper
 * Scrapes job listings directly from major company career websites
 */

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

function getRandomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

// ==================== MAJOR CANADIAN BANKS ====================

// RBC Jobs API
export async function scrapeRBCJobs(keywords = []) {
  const jobs = [];
  const searchTerms = keywords.length > 0 ? keywords : ["developer", "engineer", "analyst", "data", "software"];
  
  console.log("[RBC] Starting scrape...");
  
  for (const term of searchTerms) {
    try {
      // RBC uses Workday - API endpoint
      const url = `https://jobs.rbc.com/ca/en/search-results?keywords=${encodeURIComponent(term)}&location=Toronto%2C%20Ontario%2C%20Canada&locationId=&locationRadius=50`;
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html,application/xhtml+xml,application/xml",
          "Accept-Language": "en-US,en;q=0.9"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // Try to extract jobs from JSON-LD or script data
      $('script[type="application/ld+json"]').each((_, el) => {
        try {
          const data = JSON.parse($(el).text());
          if (data["@type"] === "JobPosting" || (Array.isArray(data) && data[0]?.["@type"] === "JobPosting")) {
            const jobData = Array.isArray(data) ? data : [data];
            for (const job of jobData) {
              jobs.push({
                id: `rbc:${job.identifier?.value || Date.now()}`,
                source: "RBC",
                company: "Royal Bank of Canada",
                title: job.title,
                location: job.jobLocation?.address?.addressLocality || "Toronto, ON",
                url: job.url || url,
                employmentType: job.employmentType || "full-time",
                salary: job.baseSalary?.value?.value ? `$${job.baseSalary.value.value}` : null,
                postedDate: job.datePosted || new Date().toISOString(),
                excerpt: job.description?.substring(0, 200) || job.title
              });
            }
          }
        } catch (e) {}
      });
      
      // Also try HTML parsing
      $('.job-tile, .job-card, [data-job-id]').each((_, el) => {
        const title = $(el).find('.job-title, h2, h3').first().text().trim();
        const location = $(el).find('.job-location, .location').first().text().trim();
        const link = $(el).find('a').first().attr('href');
        
        if (title && !jobs.find(j => j.title === title)) {
          jobs.push({
            id: `rbc:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}`,
            source: "RBC",
            company: "Royal Bank of Canada",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://jobs.rbc.com${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: title
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[RBC] Error for "${term}": ${err.message}`);
    }
  }
  
  console.log(`[RBC] Found ${jobs.length} jobs`);
  return jobs;
}

// TD Bank Jobs
export async function scrapeTDJobs(keywords = []) {
  const jobs = [];
  const searchTerms = keywords.length > 0 ? keywords : ["developer", "engineer", "analyst", "data"];
  
  console.log("[TD] Starting scrape...");
  
  for (const term of searchTerms) {
    try {
      // TD uses their own job portal
      const url = `https://jobs.td.com/en-CA/jobs/?q=${encodeURIComponent(term)}&location=Toronto%2C+ON%2C+Canada`;
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // Extract job listings
      $('article, .job-item, .job-listing, [data-job]').each((_, el) => {
        const title = $(el).find('.job-title, h2, h3, a').first().text().trim();
        const location = $(el).find('.location, .job-location').first().text().trim();
        const link = $(el).find('a').first().attr('href');
        
        if (title && title.length > 3) {
          jobs.push({
            id: `td:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}`,
            source: "TD",
            company: "TD Bank",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://jobs.td.com${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: title
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[TD] Error for "${term}": ${err.message}`);
    }
  }
  
  console.log(`[TD] Found ${jobs.length} jobs`);
  return jobs;
}

// Scotiabank Jobs (uses Taleo)
export async function scrapeScotiabankJobs(keywords = []) {
  const jobs = [];
  console.log("[Scotiabank] Starting scrape...");
  
  try {
    const url = `https://jobs.scotiabank.com/search/?q=&locationsearch=Toronto&searchbylocname=Toronto%2C+ON%2C+CA`;
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    // Try JSON in page
    const scriptContent = $('script:contains("phApp")').text();
    if (scriptContent) {
      const match = scriptContent.match(/phApp\.d498\.searchResults\s*=\s*(\[[\s\S]*?\]);/);
      if (match) {
        try {
          const jobData = JSON.parse(match[1]);
          for (const job of jobData) {
            jobs.push({
              id: `scotiabank:${job.jobId || job.id}`,
              source: "Scotiabank",
              company: "Scotiabank",
              title: job.title || job.jobTitle,
              location: job.location || "Toronto, ON",
              url: job.applyUrl || `https://jobs.scotiabank.com/job/${job.jobId}`,
              employmentType: "full-time",
              salary: null,
              postedDate: job.postedDate || new Date().toISOString(),
              excerpt: job.title
            });
          }
        } catch (e) {}
      }
    }
    
    // HTML fallback
    $('tr.data-row, .searchResultsRow, .job-listing').each((_, el) => {
      const title = $(el).find('.jobTitle, .job-title, a').first().text().trim();
      const location = $(el).find('.jobLocation, .location').first().text().trim();
      const link = $(el).find('a').first().attr('href');
      
      if (title && !jobs.find(j => j.title === title)) {
        jobs.push({
          id: `scotiabank:${title.replace(/\s+/g, '-').toLowerCase()}`,
          source: "Scotiabank",
          company: "Scotiabank",
          title,
          location: location || "Toronto, ON",
          url: link?.startsWith('http') ? link : `https://jobs.scotiabank.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
  } catch (err) {
    console.error(`[Scotiabank] Error: ${err.message}`);
  }
  
  console.log(`[Scotiabank] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== TECH COMPANIES ====================

// Shopify Jobs (Greenhouse)
export async function scrapeShopifyJobs() {
  const jobs = [];
  console.log("[Shopify] Starting scrape...");
  
  try {
    const url = "https://api.greenhouse.io/v1/boards/shopify/jobs?content=true";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "application/json"
      }
    });
    
    const jobList = res.data?.jobs || [];
    
    for (const job of jobList) {
      const locations = job.location?.name || "Remote";
      
      // Include Canadian and remote positions
      if (locations.toLowerCase().includes("canada") || 
          locations.toLowerCase().includes("toronto") ||
          locations.toLowerCase().includes("ottawa") ||
          locations.toLowerCase().includes("remote") ||
          locations.toLowerCase().includes("americas")) {
        
        jobs.push({
          id: `shopify:${job.id}`,
          source: "Shopify",
          company: "Shopify",
          title: job.title,
          location: locations,
          url: job.absolute_url || job.url,
          employmentType: "full-time",
          salary: null,
          postedDate: job.updated_at || new Date().toISOString(),
          excerpt: job.content?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
        });
      }
    }
    
  } catch (err) {
    console.error(`[Shopify] Error: ${err.message}`);
  }
  
  console.log(`[Shopify] Found ${jobs.length} jobs`);
  return jobs;
}

// Wealthsimple Jobs (Greenhouse)
export async function scrapeWealthsimpleJobs() {
  const jobs = [];
  console.log("[Wealthsimple] Starting scrape...");
  
  try {
    const url = "https://api.greenhouse.io/v1/boards/wealthsimple/jobs?content=true";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "application/json"
      }
    });
    
    const jobList = res.data?.jobs || [];
    
    for (const job of jobList) {
      jobs.push({
        id: `wealthsimple:${job.id}`,
        source: "Wealthsimple",
        company: "Wealthsimple",
        title: job.title,
        location: job.location?.name || "Toronto, Canada",
        url: job.absolute_url || job.url,
        employmentType: "full-time",
        salary: null,
        postedDate: job.updated_at || new Date().toISOString(),
        excerpt: job.content?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
      });
    }
    
  } catch (err) {
    console.error(`[Wealthsimple] Error: ${err.message}`);
  }
  
  console.log(`[Wealthsimple] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== TELECOM COMPANIES ====================

// Rogers Jobs
export async function scrapeRogersJobs(keywords = []) {
  const jobs = [];
  const searchTerms = keywords.length > 0 ? keywords : ["developer", "engineer", "analyst"];
  
  console.log("[Rogers] Starting scrape...");
  
  for (const term of searchTerms) {
    try {
      const url = `https://jobs.rogers.com/search/?q=${encodeURIComponent(term)}&location=Toronto`;
      
      const res = await axios.get(url, {
        timeout: 15000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      $('tr.data-row, .job-listing, [data-job-id]').each((_, el) => {
        const title = $(el).find('.jobTitle, .job-title, a').first().text().trim();
        const location = $(el).find('.location, .jobLocation').first().text().trim();
        const link = $(el).find('a').first().attr('href');
        
        if (title && !jobs.find(j => j.title === title)) {
          jobs.push({
            id: `rogers:${title.replace(/\s+/g, '-').toLowerCase()}`,
            source: "Rogers",
            company: "Rogers Communications",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://jobs.rogers.com${link}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date().toISOString(),
            excerpt: title
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[Rogers] Error: ${err.message}`);
    }
  }
  
  console.log(`[Rogers] Found ${jobs.length} jobs`);
  return jobs;
}

// Bell Canada Jobs
export async function scrapeBellJobs(keywords = []) {
  const jobs = [];
  console.log("[Bell] Starting scrape...");
  
  try {
    const url = "https://jobs.bell.ca/search/?q=&locationsearch=Toronto";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $('tr.data-row, .job-listing, article').each((_, el) => {
      const title = $(el).find('.jobTitle, .job-title, h2, h3, a').first().text().trim();
      const location = $(el).find('.location, .jobLocation').first().text().trim();
      const link = $(el).find('a').first().attr('href');
      
      if (title && !jobs.find(j => j.title === title)) {
        jobs.push({
          id: `bell:${title.replace(/\s+/g, '-').toLowerCase()}`,
          source: "Bell",
          company: "Bell Canada",
          title,
          location: location || "Toronto, ON",
          url: link?.startsWith('http') ? link : `https://jobs.bell.ca${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
  } catch (err) {
    console.error(`[Bell] Error: ${err.message}`);
  }
  
  console.log(`[Bell] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== INSURANCE COMPANIES ====================

// Manulife Jobs
export async function scrapeManulifeJobs(keywords = []) {
  const jobs = [];
  console.log("[Manulife] Starting scrape...");
  
  try {
    const url = "https://careers.manulife.com/global/en/search-results?keywords=&location=Toronto%2C%20ON%2C%20Canada";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    // Try JSON-LD first
    $('script[type="application/ld+json"]').each((_, el) => {
      try {
        const data = JSON.parse($(el).text());
        if (Array.isArray(data)) {
          for (const item of data) {
            if (item["@type"] === "JobPosting") {
              jobs.push({
                id: `manulife:${item.identifier?.value || Date.now()}`,
                source: "Manulife",
                company: "Manulife Financial",
                title: item.title,
                location: item.jobLocation?.address?.addressLocality || "Toronto, ON",
                url: item.url,
                employmentType: item.employmentType || "full-time",
                salary: null,
                postedDate: item.datePosted || new Date().toISOString(),
                excerpt: item.title
              });
            }
          }
        }
      } catch (e) {}
    });
    
    // HTML fallback
    $('.job-tile, .search-result, article').each((_, el) => {
      const title = $(el).find('.job-title, h2, h3').first().text().trim();
      const location = $(el).find('.location').first().text().trim();
      const link = $(el).find('a').first().attr('href');
      
      if (title && !jobs.find(j => j.title === title)) {
        jobs.push({
          id: `manulife:${title.replace(/\s+/g, '-').toLowerCase()}`,
          source: "Manulife",
          company: "Manulife Financial",
          title,
          location: location || "Toronto, ON",
          url: link?.startsWith('http') ? link : `https://careers.manulife.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
  } catch (err) {
    console.error(`[Manulife] Error: ${err.message}`);
  }
  
  console.log(`[Manulife] Found ${jobs.length} jobs`);
  return jobs;
}

// Sun Life Jobs
export async function scrapeSunLifeJobs(keywords = []) {
  const jobs = [];
  console.log("[SunLife] Starting scrape...");
  
  try {
    const url = "https://www.sunlife.com/en/careers/";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    // Sun Life often uses iframe or redirects to Workday
    // Try to extract any job links from the page
    $('a[href*="job"], a[href*="career"]').each((_, el) => {
      const href = $(el).attr('href');
      const title = $(el).text().trim();
      
      if (title && title.length > 5 && title.length < 100 && !jobs.find(j => j.title === title)) {
        jobs.push({
          id: `sunlife:${title.replace(/\s+/g, '-').toLowerCase()}`,
          source: "SunLife",
          company: "Sun Life Financial",
          title,
          location: "Toronto, ON",
          url: href?.startsWith('http') ? href : `https://www.sunlife.com${href}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
  } catch (err) {
    console.error(`[SunLife] Error: ${err.message}`);
  }
  
  console.log(`[SunLife] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== CONSULTING FIRMS ====================

// Deloitte Canada Jobs
export async function scrapeDeloitteJobs() {
  const jobs = [];
  console.log("[Deloitte] Starting scrape...");
  
  try {
    // Deloitte Canada career API
    const url = "https://jobs2.deloitte.com/ca/en/search-results?keywords=&location=Toronto%2C%20Ontario%2C%20Canada";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $('script[type="application/ld+json"]').each((_, el) => {
      try {
        const data = JSON.parse($(el).text());
        const jobList = Array.isArray(data) ? data : [data];
        
        for (const job of jobList) {
          if (job["@type"] === "JobPosting") {
            jobs.push({
              id: `deloitte:${job.identifier?.value || Date.now()}`,
              source: "Deloitte",
              company: "Deloitte Canada",
              title: job.title,
              location: job.jobLocation?.address?.addressLocality || "Toronto, ON",
              url: job.url,
              employmentType: job.employmentType || "full-time",
              salary: null,
              postedDate: job.datePosted || new Date().toISOString(),
              excerpt: job.title
            });
          }
        }
      } catch (e) {}
    });
    
  } catch (err) {
    console.error(`[Deloitte] Error: ${err.message}`);
  }
  
  console.log(`[Deloitte] Found ${jobs.length} jobs`);
  return jobs;
}

// KPMG Canada Jobs
export async function scrapeKPMGJobs() {
  const jobs = [];
  console.log("[KPMG] Starting scrape...");
  
  try {
    const url = "https://careers.kpmg.ca/jobs?location=Toronto%2C%20ON";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $('article, .job-card, .job-listing').each((_, el) => {
      const title = $(el).find('h2, h3, .job-title').first().text().trim();
      const location = $(el).find('.location').first().text().trim();
      const link = $(el).find('a').first().attr('href');
      
      if (title && !jobs.find(j => j.title === title)) {
        jobs.push({
          id: `kpmg:${title.replace(/\s+/g, '-').toLowerCase()}`,
          source: "KPMG",
          company: "KPMG Canada",
          title,
          location: location || "Toronto, ON",
          url: link?.startsWith('http') ? link : `https://careers.kpmg.ca${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
  } catch (err) {
    console.error(`[KPMG] Error: ${err.message}`);
  }
  
  console.log(`[KPMG] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== RETAIL / CONSUMER ====================

// Loblaw Jobs
export async function scrapeLoblawJobs() {
  const jobs = [];
  console.log("[Loblaw] Starting scrape...");
  
  try {
    const url = "https://jobs.loblaw.ca/search/?q=&locationsearch=Toronto";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $('tr.data-row, .job-listing').each((_, el) => {
      const title = $(el).find('.jobTitle, a').first().text().trim();
      const location = $(el).find('.location').first().text().trim();
      const link = $(el).find('a').first().attr('href');
      
      if (title && !jobs.find(j => j.title === title)) {
        jobs.push({
          id: `loblaw:${title.replace(/\s+/g, '-').toLowerCase()}`,
          source: "Loblaw",
          company: "Loblaw Companies",
          title,
          location: location || "Toronto, ON",
          url: link?.startsWith('http') ? link : `https://jobs.loblaw.ca${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
  } catch (err) {
    console.error(`[Loblaw] Error: ${err.message}`);
  }
  
  console.log(`[Loblaw] Found ${jobs.length} jobs`);
  return jobs;
}

// Canadian Tire Jobs
export async function scrapeCanadianTireJobs() {
  const jobs = [];
  console.log("[Canadian Tire] Starting scrape...");
  
  try {
    const url = "https://corp.canadiantire.ca/English/Careers/Pages/Search-Jobs.aspx";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $('article, .job-item, .job-listing').each((_, el) => {
      const title = $(el).find('h2, h3, .job-title').first().text().trim();
      const location = $(el).find('.location').first().text().trim();
      const link = $(el).find('a').first().attr('href');
      
      if (title && !jobs.find(j => j.title === title)) {
        jobs.push({
          id: `canadiantire:${title.replace(/\s+/g, '-').toLowerCase()}`,
          source: "CanadianTire",
          company: "Canadian Tire",
          title,
          location: location || "Toronto, ON",
          url: link?.startsWith('http') ? link : `https://corp.canadiantire.ca${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    
  } catch (err) {
    console.error(`[Canadian Tire] Error: ${err.message}`);
  }
  
  console.log(`[Canadian Tire] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== TECH STARTUPS (VERIFIED) ====================

// Ada Support (AI company - Toronto)
export async function scrapeAdaSupportJobs() {
  const jobs = [];
  console.log("[Ada] Starting scrape...");
  
  try {
    // Ada uses Greenhouse
    const url = "https://api.greenhouse.io/v1/boards/ada-support/jobs?content=true";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "application/json"
      }
    });
    
    const jobList = res.data?.jobs || [];
    
    for (const job of jobList) {
      jobs.push({
        id: `ada:${job.id}`,
        source: "Ada",
        company: "Ada Support",
        title: job.title,
        location: job.location?.name || "Toronto, Canada",
        url: job.absolute_url || job.url,
        employmentType: "full-time",
        salary: null,
        postedDate: job.updated_at || new Date().toISOString(),
        excerpt: job.content?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
      });
    }
    
  } catch (err) {
    console.error(`[Ada] Error: ${err.message}`);
  }
  
  console.log(`[Ada] Found ${jobs.length} jobs`);
  return jobs;
}

// 1Password Jobs (Toronto)
export async function scrape1PasswordJobs() {
  const jobs = [];
  console.log("[1Password] Starting scrape...");
  
  try {
    // 1Password uses Greenhouse
    const url = "https://api.greenhouse.io/v1/boards/1password/jobs?content=true";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "application/json"
      }
    });
    
    const jobList = res.data?.jobs || [];
    
    for (const job of jobList) {
      const locations = job.location?.name || "Remote";
      
      if (locations.toLowerCase().includes("canada") || 
          locations.toLowerCase().includes("toronto") ||
          locations.toLowerCase().includes("remote")) {
        jobs.push({
          id: `1password:${job.id}`,
          source: "1Password",
          company: "1Password",
          title: job.title,
          location: locations,
          url: job.absolute_url || job.url,
          employmentType: "full-time",
          salary: null,
          postedDate: job.updated_at || new Date().toISOString(),
          excerpt: job.content?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
        });
      }
    }
    
  } catch (err) {
    console.error(`[1Password] Error: ${err.message}`);
  }
  
  console.log(`[1Password] Found ${jobs.length} jobs`);
  return jobs;
}

// Lightspeed Commerce (Montreal/Toronto)
export async function scrapeLightspeedJobs() {
  const jobs = [];
  console.log("[Lightspeed] Starting scrape...");
  
  try {
    // Lightspeed uses Greenhouse
    const url = "https://api.greenhouse.io/v1/boards/lightspeedcommerce/jobs?content=true";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "application/json"
      }
    });
    
    const jobList = res.data?.jobs || [];
    
    for (const job of jobList) {
      const locations = job.location?.name || "Remote";
      
      if (locations.toLowerCase().includes("canada") || 
          locations.toLowerCase().includes("toronto") ||
          locations.toLowerCase().includes("montreal") ||
          locations.toLowerCase().includes("remote")) {
        jobs.push({
          id: `lightspeed:${job.id}`,
          source: "Lightspeed",
          company: "Lightspeed Commerce",
          title: job.title,
          location: locations,
          url: job.absolute_url || job.url,
          employmentType: "full-time",
          salary: null,
          postedDate: job.updated_at || new Date().toISOString(),
          excerpt: job.content?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
        });
      }
    }
    
  } catch (err) {
    console.error(`[Lightspeed] Error: ${err.message}`);
  }
  
  console.log(`[Lightspeed] Found ${jobs.length} jobs`);
  return jobs;
}

// Hootsuite (Vancouver)
export async function scrapeHootsuiteJobs() {
  const jobs = [];
  console.log("[Hootsuite] Starting scrape...");
  
  try {
    // Hootsuite uses Greenhouse
    const url = "https://api.greenhouse.io/v1/boards/hootsuite/jobs?content=true";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "application/json"
      }
    });
    
    const jobList = res.data?.jobs || [];
    
    for (const job of jobList) {
      const locations = job.location?.name || "Remote";
      
      if (locations.toLowerCase().includes("canada") || 
          locations.toLowerCase().includes("vancouver") ||
          locations.toLowerCase().includes("remote")) {
        jobs.push({
          id: `hootsuite:${job.id}`,
          source: "Hootsuite",
          company: "Hootsuite",
          title: job.title,
          location: locations,
          url: job.absolute_url || job.url,
          employmentType: "full-time",
          salary: null,
          postedDate: job.updated_at || new Date().toISOString(),
          excerpt: job.content?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
        });
      }
    }
    
  } catch (err) {
    console.error(`[Hootsuite] Error: ${err.message}`);
  }
  
  console.log(`[Hootsuite] Found ${jobs.length} jobs`);
  return jobs;
}

// Clio (Legal tech - Vancouver/Toronto)
export async function scrapeClioJobs() {
  const jobs = [];
  console.log("[Clio] Starting scrape...");
  
  try {
    // Clio uses Greenhouse
    const url = "https://api.greenhouse.io/v1/boards/clio/jobs?content=true";
    
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "application/json"
      }
    });
    
    const jobList = res.data?.jobs || [];
    
    for (const job of jobList) {
      const locations = job.location?.name || "Remote";
      
      if (locations.toLowerCase().includes("canada") || 
          locations.toLowerCase().includes("vancouver") ||
          locations.toLowerCase().includes("toronto") ||
          locations.toLowerCase().includes("calgary") ||
          locations.toLowerCase().includes("remote")) {
        jobs.push({
          id: `clio:${job.id}`,
          source: "Clio",
          company: "Clio",
          title: job.title,
          location: locations,
          url: job.absolute_url || job.url,
          employmentType: "full-time",
          salary: null,
          postedDate: job.updated_at || new Date().toISOString(),
          excerpt: job.content?.replace(/<[^>]*>/g, '').substring(0, 200) || job.title
        });
      }
    }
    
  } catch (err) {
    console.error(`[Clio] Error: ${err.message}`);
  }
  
  console.log(`[Clio] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== MASTER FETCH FUNCTION ====================

export async function scrapeAllCompanyCareers() {
  console.log("\n╔══════════════════════════════════════════╗");
  console.log("║   COMPANY CAREER PAGES SCRAPER           ║");
  console.log("╚══════════════════════════════════════════╝\n");
  
  const allJobs = [];
  
  // Canadian Banks
  const rbcJobs = await scrapeRBCJobs();
  allJobs.push(...rbcJobs);
  await sleep(500);
  
  const tdJobs = await scrapeTDJobs();
  allJobs.push(...tdJobs);
  await sleep(500);
  
  const scotiabankJobs = await scrapeScotiabankJobs();
  allJobs.push(...scotiabankJobs);
  await sleep(500);
  
  // Tech Companies
  const shopifyJobs = await scrapeShopifyJobs();
  allJobs.push(...shopifyJobs);
  await sleep(500);
  
  const wealthsimpleJobs = await scrapeWealthsimpleJobs();
  allJobs.push(...wealthsimpleJobs);
  await sleep(500);
  
  // Telecom
  const rogersJobs = await scrapeRogersJobs();
  allJobs.push(...rogersJobs);
  await sleep(500);
  
  const bellJobs = await scrapeBellJobs();
  allJobs.push(...bellJobs);
  await sleep(500);
  
  // Insurance
  const manulifeJobs = await scrapeManulifeJobs();
  allJobs.push(...manulifeJobs);
  await sleep(500);
  
  const sunlifeJobs = await scrapeSunLifeJobs();
  allJobs.push(...sunlifeJobs);
  await sleep(500);
  
  // Consulting
  const deloitteJobs = await scrapeDeloitteJobs();
  allJobs.push(...deloitteJobs);
  await sleep(500);
  
  const kpmgJobs = await scrapeKPMGJobs();
  allJobs.push(...kpmgJobs);
  await sleep(500);
  
  // Retail
  const loblawJobs = await scrapeLoblawJobs();
  allJobs.push(...loblawJobs);
  await sleep(500);
  
  const ctJobs = await scrapeCanadianTireJobs();
  allJobs.push(...ctJobs);
  await sleep(500);
  
  // Tech Startups
  const adaJobs = await scrapeAdaSupportJobs();
  allJobs.push(...adaJobs);
  await sleep(500);
  
  const onepassJobs = await scrape1PasswordJobs();
  allJobs.push(...onepassJobs);
  await sleep(500);
  
  const lightspeedJobs = await scrapeLightspeedJobs();
  allJobs.push(...lightspeedJobs);
  await sleep(500);
  
  const hootsuiteJobs = await scrapeHootsuiteJobs();
  allJobs.push(...hootsuiteJobs);
  await sleep(500);
  
  const clioJobs = await scrapeClioJobs();
  allJobs.push(...clioJobs);
  
  console.log("\n========================================");
  console.log(`COMPANY CAREERS SCRAPE COMPLETE`);
  console.log(`Total jobs from company sites: ${allJobs.length}`);
  console.log("========================================\n");
  
  return allJobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  scrapeAllCompanyCareers()
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 10));
    })
    .catch(console.error);
}
