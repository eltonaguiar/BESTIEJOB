import axios from "axios";
import * as cheerio from "cheerio";

/**
 * IT Recruiting Firms Scraper
 * Scrapes job postings from major IT staffing/recruiting agencies
 * Extracts salary ranges, hourly rates, and employment types
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

// Parse salary/rate from text
function parseSalaryFromText(text) {
  if (!text) return null;
  
  const t = text.toLowerCase();
  
  // Hourly rate patterns: $50/hr, $50-75/hour, $50 - $75 per hour
  const hourlyMatch = t.match(/\$?\s*(\d+(?:,\d{3})?(?:\.\d{2})?)\s*(?:-|to|–)\s*\$?\s*(\d+(?:,\d{3})?(?:\.\d{2})?)\s*(?:\/\s*h(?:ou)?r|per\s*h(?:ou)?r|hourly|ph)/i) ||
                      t.match(/\$?\s*(\d+(?:,\d{3})?(?:\.\d{2})?)\s*(?:\/\s*h(?:ou)?r|per\s*h(?:ou)?r|hourly|ph)/i);
  
  if (hourlyMatch) {
    const min = parseFloat(hourlyMatch[1].replace(/,/g, ''));
    const max = hourlyMatch[2] ? parseFloat(hourlyMatch[2].replace(/,/g, '')) : min;
    return { min, max, type: 'hourly', display: `$${min}${max !== min ? `-$${max}` : ''}/hr` };
  }
  
  // Annual salary patterns: $80,000 - $120,000, $80K-120K
  const annualMatch = t.match(/\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*[kK]?\s*(?:-|to|–)\s*\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*[kK]?(?:\s*(?:per\s*)?(?:year|annual|yr|pa))?/i) ||
                      t.match(/\$?\s*(\d+(?:,\d{3})*)\s*(?:per\s*)?(?:year|annual|yr|pa)/i);
  
  if (annualMatch) {
    let min = parseFloat(annualMatch[1].replace(/,/g, ''));
    let max = annualMatch[2] ? parseFloat(annualMatch[2].replace(/,/g, '')) : min;
    
    // Handle K notation
    if (min < 1000 && t.includes('k')) {
      min *= 1000;
      max *= 1000;
    }
    
    if (min >= 20000) { // Likely annual
      return { min, max, type: 'annual', display: `$${(min/1000).toFixed(0)}K${max !== min ? `-$${(max/1000).toFixed(0)}K` : ''}/yr` };
    }
  }
  
  // Simple dollar amounts
  const simpleMatch = t.match(/\$\s*(\d+(?:,\d{3})*)/);
  if (simpleMatch) {
    const val = parseFloat(simpleMatch[1].replace(/,/g, ''));
    if (val >= 20000) {
      return { min: val, max: val, type: 'annual', display: `$${(val/1000).toFixed(0)}K/yr` };
    } else if (val >= 15 && val <= 200) {
      return { min: val, max: val, type: 'hourly', display: `$${val}/hr` };
    }
  }
  
  return null;
}

// Determine employment type from text
function parseEmploymentType(text, title = "") {
  const t = (text + " " + title).toLowerCase();
  
  if (t.includes("contract") || t.includes("contractor") || t.includes("c2c") || t.includes("corp-to-corp")) {
    return "contract";
  }
  if (t.includes("co-op") || t.includes("coop") || t.includes("internship") || t.includes("intern ")) {
    return "internship";
  }
  if (t.includes("part-time") || t.includes("part time") || t.includes("parttime")) {
    return "part-time";
  }
  if (t.includes("seasonal") || t.includes("temporary") || t.includes("temp ")) {
    return "seasonal";
  }
  if (t.includes("full-time") || t.includes("full time") || t.includes("fulltime") || t.includes("permanent") || t.includes("perm ")) {
    return "full-time";
  }
  
  return "unknown";
}

// ==================== ROBERT HALF TECHNOLOGY ====================
export async function scrapeRobertHalf(keywords = ["developer"]) {
  const jobs = [];
  console.log("[Robert Half] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 5)) {
    try {
      // Robert Half job search URL
      const url = `https://www.roberthalf.ca/en/jobs/all/toronto-on?search=${encodeURIComponent(keyword)}`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html,application/xhtml+xml",
          "Accept-Language": "en-CA,en;q=0.9"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // Try JSON-LD first
      $('script[type="application/ld+json"]').each((_, el) => {
        try {
          const data = JSON.parse($(el).text());
          const jobList = data["@graph"] || (Array.isArray(data) ? data : [data]);
          
          for (const job of jobList) {
            if (job["@type"] === "JobPosting") {
              const salary = parseSalaryFromText(
                job.baseSalary?.value?.value?.toString() || 
                job.description || ""
              );
              
              jobs.push({
                id: `roberthalf:${job.identifier?.value || Date.now()}-${jobs.length}`,
                source: "Robert Half",
                company: job.hiringOrganization?.name || "Robert Half",
                title: job.title,
                location: job.jobLocation?.address?.addressLocality || "Toronto, ON",
                url: job.url || url,
                employmentType: parseEmploymentType(job.employmentType || job.description || "", job.title),
                salary: salary,
                postedDate: job.datePosted || new Date().toISOString(),
                excerpt: (job.description || "").substring(0, 250).replace(/<[^>]*>/g, ''),
                recruiter: "Robert Half Technology"
              });
            }
          }
        } catch (e) {}
      });
      
      // HTML fallback
      $('.job-tile, .job-listing, .search-result, [data-job-id]').each((_, el) => {
        const title = $(el).find('.job-title, h2, h3, a[href*="job"]').first().text().trim();
        const link = $(el).find('a').first().attr('href');
        const location = $(el).find('.location, .job-location').first().text().trim();
        const salaryText = $(el).find('.salary, .compensation, .pay').first().text().trim();
        const description = $(el).find('.description, .excerpt, p').first().text().trim();
        
        if (title && !jobs.find(j => j.title === title)) {
          const salary = parseSalaryFromText(salaryText || description);
          
          jobs.push({
            id: `roberthalf:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}`,
            source: "Robert Half",
            company: "Robert Half",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://www.roberthalf.ca${link}`,
            employmentType: parseEmploymentType(description, title),
            salary,
            postedDate: new Date().toISOString(),
            excerpt: description.substring(0, 250),
            recruiter: "Robert Half Technology"
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[Robert Half] Error: ${err.message}`);
    }
  }
  
  console.log(`[Robert Half] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== TEKSYSTEMS ====================
export async function scrapeTEKsystems(keywords = ["developer"]) {
  const jobs = [];
  console.log("[TEKsystems] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 5)) {
    try {
      const url = `https://www.teksystems.com/en-ca/jobs?keywords=${encodeURIComponent(keyword)}&location=Toronto%2C%20ON`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // Parse job listings
      $('article, .job-card, .job-listing, [data-job], .search-result').each((_, el) => {
        const title = $(el).find('h2, h3, .job-title, a').first().text().trim();
        const link = $(el).find('a[href*="job"]').first().attr('href');
        const location = $(el).find('.location, .job-location').first().text().trim();
        const salaryText = $(el).find('.salary, .rate, .compensation').first().text().trim();
        const typeText = $(el).find('.job-type, .employment-type').first().text().trim();
        const description = $(el).find('.description, p').first().text().trim();
        
        if (title && title.length > 5) {
          const salary = parseSalaryFromText(salaryText || description);
          
          jobs.push({
            id: `teksystems:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}-${jobs.length}`,
            source: "TEKsystems",
            company: "TEKsystems",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://www.teksystems.com${link}`,
            employmentType: parseEmploymentType(typeText || description, title),
            salary,
            postedDate: new Date().toISOString(),
            excerpt: description.substring(0, 250),
            recruiter: "TEKsystems"
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[TEKsystems] Error: ${err.message}`);
    }
  }
  
  console.log(`[TEKsystems] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== RANDSTAD DIGITAL ====================
export async function scrapeRandstad(keywords = ["developer"]) {
  const jobs = [];
  console.log("[Randstad] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 5)) {
    try {
      // Randstad Canada job search
      const url = `https://www.randstad.ca/jobs/q-${encodeURIComponent(keyword)}/l-toronto/`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // JSON-LD extraction
      $('script[type="application/ld+json"]').each((_, el) => {
        try {
          const data = JSON.parse($(el).text());
          const jobList = Array.isArray(data) ? data : [data];
          
          for (const job of jobList) {
            if (job["@type"] === "JobPosting") {
              const salaryText = job.baseSalary?.value?.value || job.description || "";
              const salary = parseSalaryFromText(salaryText.toString());
              
              jobs.push({
                id: `randstad:${job.identifier?.value || Date.now()}-${jobs.length}`,
                source: "Randstad",
                company: job.hiringOrganization?.name || "Randstad",
                title: job.title,
                location: job.jobLocation?.address?.addressLocality || "Toronto, ON",
                url: job.url,
                employmentType: parseEmploymentType(job.employmentType || "", job.title),
                salary,
                postedDate: job.datePosted || new Date().toISOString(),
                excerpt: (job.description || "").substring(0, 250).replace(/<[^>]*>/g, ''),
                recruiter: "Randstad Digital"
              });
            }
          }
        } catch (e) {}
      });
      
      // HTML fallback
      $('.job-card, .job-item, article').each((_, el) => {
        const title = $(el).find('h2, h3, .job-title').first().text().trim();
        const link = $(el).find('a').first().attr('href');
        const location = $(el).find('.location').first().text().trim();
        const salaryText = $(el).find('.salary, .rate').first().text().trim();
        
        if (title && !jobs.find(j => j.title === title)) {
          jobs.push({
            id: `randstad:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}`,
            source: "Randstad",
            company: "Randstad",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://www.randstad.ca${link}`,
            employmentType: parseEmploymentType(title, ""),
            salary: parseSalaryFromText(salaryText),
            postedDate: new Date().toISOString(),
            excerpt: title,
            recruiter: "Randstad Digital"
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[Randstad] Error: ${err.message}`);
    }
  }
  
  console.log(`[Randstad] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== HAYS IT ====================
export async function scrapeHays(keywords = ["developer"]) {
  const jobs = [];
  console.log("[Hays] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 5)) {
    try {
      const url = `https://www.hays.ca/en-CA/job-search?q=${encodeURIComponent(keyword)}&location=Toronto`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      $('script[type="application/ld+json"]').each((_, el) => {
        try {
          const data = JSON.parse($(el).text());
          if (data["@type"] === "JobPosting" || data.itemListElement) {
            const jobList = data.itemListElement || [data];
            
            for (const item of jobList) {
              const job = item.item || item;
              if (job["@type"] === "JobPosting") {
                const salary = parseSalaryFromText(job.baseSalary?.value?.toString() || job.description || "");
                
                jobs.push({
                  id: `hays:${job.identifier?.value || Date.now()}-${jobs.length}`,
                  source: "Hays",
                  company: job.hiringOrganization?.name || "Hays",
                  title: job.title,
                  location: job.jobLocation?.address?.addressLocality || "Toronto, ON",
                  url: job.url,
                  employmentType: parseEmploymentType(job.employmentType || "", job.title),
                  salary,
                  postedDate: job.datePosted || new Date().toISOString(),
                  excerpt: (job.description || "").substring(0, 250).replace(/<[^>]*>/g, ''),
                  recruiter: "Hays IT"
                });
              }
            }
          }
        } catch (e) {}
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[Hays] Error: ${err.message}`);
    }
  }
  
  console.log(`[Hays] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== PROCOM (Canadian IT Staffing) ====================
export async function scrapeProcom(keywords = ["developer"]) {
  const jobs = [];
  console.log("[Procom] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 5)) {
    try {
      const url = `https://www.procom.ca/job-search/?search=${encodeURIComponent(keyword)}&location=Toronto`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // Parse job listings
      $('.job-listing, .job-card, article, .search-result').each((_, el) => {
        const title = $(el).find('h2, h3, .job-title, a').first().text().trim();
        const link = $(el).find('a[href*="job"]').first().attr('href');
        const location = $(el).find('.location').first().text().trim();
        const salaryText = $(el).find('.salary, .rate').first().text().trim();
        const description = $(el).find('.description, p').first().text().trim();
        const typeText = $(el).find('.job-type').first().text().trim();
        
        if (title && title.length > 5) {
          const salary = parseSalaryFromText(salaryText || description);
          
          jobs.push({
            id: `procom:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}-${jobs.length}`,
            source: "Procom",
            company: "Procom",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://www.procom.ca${link}`,
            employmentType: parseEmploymentType(typeText || description, title),
            salary,
            postedDate: new Date().toISOString(),
            excerpt: description.substring(0, 250),
            recruiter: "Procom"
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[Procom] Error: ${err.message}`);
    }
  }
  
  console.log(`[Procom] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== S.I. SYSTEMS (Canadian IT Staffing) ====================
export async function scrapeSISystems(keywords = ["developer"]) {
  const jobs = [];
  console.log("[S.i. Systems] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 5)) {
    try {
      const url = `https://www.sisystems.com/it-jobs/?search=${encodeURIComponent(keyword)}&location=Toronto`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // Parse job cards
      $('.job-card, .job-listing, article, [data-job]').each((_, el) => {
        const title = $(el).find('h2, h3, .job-title, a').first().text().trim();
        const link = $(el).find('a[href*="job"]').first().attr('href');
        const location = $(el).find('.location').first().text().trim();
        const rateText = $(el).find('.rate, .salary, .compensation').first().text().trim();
        const description = $(el).find('.description, p').first().text().trim();
        
        if (title && title.length > 5) {
          const salary = parseSalaryFromText(rateText || description);
          
          jobs.push({
            id: `sisystems:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}-${jobs.length}`,
            source: "S.i. Systems",
            company: "S.i. Systems",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://www.sisystems.com${link}`,
            employmentType: parseEmploymentType(description, title),
            salary,
            postedDate: new Date().toISOString(),
            excerpt: description.substring(0, 250),
            recruiter: "S.i. Systems"
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[S.i. Systems] Error: ${err.message}`);
    }
  }
  
  console.log(`[S.i. Systems] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== ALTIS RECRUITMENT ====================
export async function scrapeAltis(keywords = ["developer"]) {
  const jobs = [];
  console.log("[Altis] Starting scrape...");
  
  try {
    const url = `https://altisrecruitment.com/job-board/?search=developer&location=Toronto`;
    
    const res = await axios.get(url, {
      timeout: 20000,
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $('.job-listing, .job-card, article').each((_, el) => {
      const title = $(el).find('h2, h3, .job-title').first().text().trim();
      const link = $(el).find('a').first().attr('href');
      const location = $(el).find('.location').first().text().trim();
      const salaryText = $(el).find('.salary, .rate').first().text().trim();
      const typeText = $(el).find('.job-type').first().text().trim();
      
      if (title && title.length > 5) {
        jobs.push({
          id: `altis:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}-${jobs.length}`,
          source: "Altis",
          company: "Altis Recruitment",
          title,
          location: location || "Toronto, ON",
          url: link?.startsWith('http') ? link : `https://altisrecruitment.com${link}`,
          employmentType: parseEmploymentType(typeText, title),
          salary: parseSalaryFromText(salaryText),
          postedDate: new Date().toISOString(),
          excerpt: title,
          recruiter: "Altis Recruitment"
        });
      }
    });
    
  } catch (err) {
    console.error(`[Altis] Error: ${err.message}`);
  }
  
  console.log(`[Altis] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== EXPERIS (ManpowerGroup) ====================
export async function scrapeExperis(keywords = ["developer"]) {
  const jobs = [];
  console.log("[Experis] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 3)) {
    try {
      const url = `https://www.experis.ca/en/find-jobs?k=${encodeURIComponent(keyword)}&l=Toronto`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // JSON-LD extraction
      $('script[type="application/ld+json"]').each((_, el) => {
        try {
          const data = JSON.parse($(el).text());
          if (data["@type"] === "JobPosting") {
            const salary = parseSalaryFromText(data.baseSalary?.value?.toString() || "");
            
            jobs.push({
              id: `experis:${data.identifier?.value || Date.now()}-${jobs.length}`,
              source: "Experis",
              company: data.hiringOrganization?.name || "Experis",
              title: data.title,
              location: data.jobLocation?.address?.addressLocality || "Toronto, ON",
              url: data.url,
              employmentType: parseEmploymentType(data.employmentType || "", data.title),
              salary,
              postedDate: data.datePosted || new Date().toISOString(),
              excerpt: (data.description || "").substring(0, 250).replace(/<[^>]*>/g, ''),
              recruiter: "Experis (ManpowerGroup)"
            });
          }
        } catch (e) {}
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[Experis] Error: ${err.message}`);
    }
  }
  
  console.log(`[Experis] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== INSIGHT GLOBAL ====================
export async function scrapeInsightGlobal(keywords = ["developer"]) {
  const jobs = [];
  console.log("[Insight Global] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 3)) {
    try {
      const url = `https://insightglobal.com/jobs/?search=${encodeURIComponent(keyword)}&location=Toronto%2C%20ON`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // Parse job listings
      $('.job-card, .job-listing, article').each((_, el) => {
        const title = $(el).find('h2, h3, .job-title, a').first().text().trim();
        const link = $(el).find('a[href*="job"]').first().attr('href');
        const location = $(el).find('.location').first().text().trim();
        const salaryText = $(el).find('.salary, .rate').first().text().trim();
        const description = $(el).find('.description, p').first().text().trim();
        
        if (title && title.length > 5 && !jobs.find(j => j.title === title)) {
          jobs.push({
            id: `insightglobal:${title.replace(/\s+/g, '-').toLowerCase()}-${Date.now()}-${jobs.length}`,
            source: "Insight Global",
            company: "Insight Global",
            title,
            location: location || "Toronto, ON",
            url: link?.startsWith('http') ? link : `https://insightglobal.com${link}`,
            employmentType: parseEmploymentType(description, title),
            salary: parseSalaryFromText(salaryText || description),
            postedDate: new Date().toISOString(),
            excerpt: description.substring(0, 250),
            recruiter: "Insight Global"
          });
        }
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[Insight Global] Error: ${err.message}`);
    }
  }
  
  console.log(`[Insight Global] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== KFORCE ====================
export async function scrapeKforce(keywords = ["developer"]) {
  const jobs = [];
  console.log("[Kforce] Starting scrape...");
  
  for (const keyword of keywords.slice(0, 3)) {
    try {
      const url = `https://www.kforce.com/find-work/search-jobs/?keywords=${encodeURIComponent(keyword)}&location=Canada`;
      
      const res = await axios.get(url, {
        timeout: 20000,
        headers: {
          "User-Agent": getRandomUA(),
          "Accept": "text/html"
        }
      });
      
      const $ = cheerio.load(res.data);
      
      // JSON-LD extraction
      $('script[type="application/ld+json"]').each((_, el) => {
        try {
          const data = JSON.parse($(el).text());
          const jobList = data["@graph"] || (Array.isArray(data) ? data : [data]);
          
          for (const job of jobList) {
            if (job["@type"] === "JobPosting") {
              const salary = parseSalaryFromText(job.baseSalary?.value?.toString() || "");
              
              jobs.push({
                id: `kforce:${job.identifier?.value || Date.now()}-${jobs.length}`,
                source: "Kforce",
                company: job.hiringOrganization?.name || "Kforce",
                title: job.title,
                location: job.jobLocation?.address?.addressLocality || "Toronto, ON",
                url: job.url,
                employmentType: parseEmploymentType(job.employmentType || "", job.title),
                salary,
                postedDate: job.datePosted || new Date().toISOString(),
                excerpt: (job.description || "").substring(0, 250).replace(/<[^>]*>/g, ''),
                recruiter: "Kforce"
              });
            }
          }
        } catch (e) {}
      });
      
      await sleep(500);
    } catch (err) {
      console.error(`[Kforce] Error: ${err.message}`);
    }
  }
  
  console.log(`[Kforce] Found ${jobs.length} jobs`);
  return jobs;
}

// ==================== MASTER SCRAPE FUNCTION ====================
export async function scrapeAllRecruitingFirms() {
  console.log("\n╔══════════════════════════════════════════════════════╗");
  console.log("║      IT RECRUITING FIRMS SCRAPER                     ║");
  console.log("╚══════════════════════════════════════════════════════╝\n");
  
  const keywords = [
    "software developer", "developer", "engineer", 
    "analyst", "DevOps", "data", "cloud"
  ];
  
  const allJobs = [];
  
  // Robert Half
  const robertHalfJobs = await scrapeRobertHalf(keywords);
  allJobs.push(...robertHalfJobs);
  await sleep(1000);
  
  // TEKsystems
  const teksystemsJobs = await scrapeTEKsystems(keywords);
  allJobs.push(...teksystemsJobs);
  await sleep(1000);
  
  // Randstad
  const randstadJobs = await scrapeRandstad(keywords);
  allJobs.push(...randstadJobs);
  await sleep(1000);
  
  // Hays
  const haysJobs = await scrapeHays(keywords);
  allJobs.push(...haysJobs);
  await sleep(1000);
  
  // Procom
  const procomJobs = await scrapeProcom(keywords);
  allJobs.push(...procomJobs);
  await sleep(1000);
  
  // S.i. Systems
  const siJobs = await scrapeSISystems(keywords);
  allJobs.push(...siJobs);
  await sleep(1000);
  
  // Altis
  const altisJobs = await scrapeAltis(keywords);
  allJobs.push(...altisJobs);
  await sleep(1000);
  
  // Experis
  const experisJobs = await scrapeExperis(keywords);
  allJobs.push(...experisJobs);
  await sleep(1000);
  
  // Insight Global
  const insightJobs = await scrapeInsightGlobal(keywords);
  allJobs.push(...insightJobs);
  await sleep(1000);
  
  // Kforce
  const kforceJobs = await scrapeKforce(keywords);
  allJobs.push(...kforceJobs);
  
  console.log("\n════════════════════════════════════════════════════════");
  console.log("RECRUITING FIRMS SCRAPE COMPLETE");
  console.log(`Total jobs: ${allJobs.length}`);
  console.log("════════════════════════════════════════════════════════\n");
  
  // Summary by firm
  const bySource = {};
  for (const job of allJobs) {
    bySource[job.source] = (bySource[job.source] || 0) + 1;
  }
  console.log("Jobs by recruiting firm:");
  for (const [src, count] of Object.entries(bySource)) {
    console.log(`  ${src}: ${count}`);
  }
  
  // Summary by employment type
  const byType = {};
  for (const job of allJobs) {
    byType[job.employmentType] = (byType[job.employmentType] || 0) + 1;
  }
  console.log("\nJobs by employment type:");
  for (const [type, count] of Object.entries(byType)) {
    console.log(`  ${type}: ${count}`);
  }
  
  return allJobs;
}

// Export helper functions for use elsewhere
export { parseSalaryFromText, parseEmploymentType };

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  scrapeAllRecruitingFirms()
    .then(jobs => {
      console.log("\nSample jobs:");
      console.log(jobs.slice(0, 5));
    })
    .catch(console.error);
}
