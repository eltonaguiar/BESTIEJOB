import axios from "axios";
import * as cheerio from "cheerio";
import Parser from "rss-parser";

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

/**
 * Scrape jobs specifically AT HR platform companies
 * Dayforce, Ceridian, Workday, ADP, SAP, UKG, etc.
 */

// HR Platform Companies - Jobs available at these companies
const HR_PLATFORM_COMPANIES = [
  "Ceridian", "Dayforce", "Workday", "ADP", "Paychex", "Ultimate Software", "UKG",
  "SAP SuccessFactors", "SAP", "Oracle HCM", "Oracle", "Cornerstone OnDemand",
  "Workforce Software", "Kronos", "Infor", "BambooHR", "Gusto", "Zenefits",
  "Namely", "Paylocity", "Rippling", "Deel", "Remote", "Personio", "HiBob",
  "Lattice", "15Five", "Culture Amp", "Qualtrics", "Glint", "Peakon",
  "Saba", "SumTotal", "TalentSoft", "Lumesse", "SilkRoad", "Taleo",
  "iCIMS", "Greenhouse", "Lever", "SmartRecruiters", "JazzHR", "Jobvite",
  "Bullhorn", "Avionté", "TempWorks", "Paycom", "Paycor", "PrimePay",
  "Justworks", "TriNet", "Insperity", "ADP TotalSource", "Safeguard",
  "Alight", "Willis Towers Watson", "Mercer", "Aon Hewitt", "Conduent",
  // Add more HR tech companies
  "Workato", "BetterCloud", "Hibob", "ChartHop", "Goco", "Factorial",
  "Humaans", "Kenjo", "Lano", "Oyster", "Papaya Global", "Remote First",
  "Sanders", "Sequoia", "Sora", "Verv", "Visier", "WorkBoard", "Xoxoday"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobsByCompany(company, location = "Toronto", page = 1) {
  try {
    // Search by company name in Adzuna
    const url = `http://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=100&company=${encodeURIComponent(company)}&where=${encodeURIComponent(location)}&content-type=application/json`;
    
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
      company: job.company?.display_name || company,
      title: job.title,
      location: job.location?.display_name || `${location}, Canada`,
      url: job.redirect_url,
      employmentType: "full-time",
      salary: job.salary_min && job.salary_max ? { min: Math.round(job.salary_min), max: Math.round(job.salary_max) } : null,
      postedDate: job.created_at || new Date().toISOString(),
      excerpt: job.description?.substring(0, 240) || job.title,
      category: "HR Technology"
    })).filter(job => 
      job.title.toLowerCase().includes(company.toLowerCase()) ||
      job.company.toLowerCase().includes(company.toLowerCase())
    );
  } catch (error) {
    return [];
  }
}

// Try to scrape Dayforce careers directly
async function scrapeDayforceCareers() {
  const jobs = [];
  try {
    console.log("[Dayforce Careers] Trying to scrape...");
    
    const urls = [
      "https://careers.ceridian.com/us/en",
      "https://www.dayforce.com/careers",
      "https://jobs.dayforce.com"
    ];
    
    for (const url of urls) {
      try {
        const res = await axios.get(url, {
          timeout: 15000,
          headers: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
          }
        });
        
        const $ = cheerio.load(res.data);
        
        // Look for job listings
        $("[data-job-id], .job-listing, .job-card, tr[data-id], .job-item").each((_, el) => {
          const title = $(el).find("h2, h3, .job-title, .title, td:nth-child(1)").text().trim();
          const location = $(el).find(".location, .job-location, .city, td:nth-child(2)").text().trim();
          const link = $(el).find("a").attr("href") || "";
          
          if (title && (title.toLowerCase().includes("developer") || 
                       title.toLowerCase().includes("engineer") || 
                       title.toLowerCase().includes("manager") ||
                       title.toLowerCase().includes("analyst"))) {
            jobs.push({
              id: `dayforce:${link || Math.random().toString(36).substr(2, 9)}`,
              source: "dayforce",
              company: "Dayforce/Ceridian",
              title,
              location: location || "Toronto, ON",
              url: link.startsWith("http") ? link : `https://careers.ceridian.com${link}`,
              employmentType: "full-time",
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: `${title} at Dayforce/Ceridian - HR Technology Platform`
            });
          }
        });
        
        if (jobs.length > 0) break;
      } catch (e) {
        console.log(`  ${url} failed: ${e.message}`);
      }
    }
    
    console.log(`[Dayforce Careers] Found ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Dayforce Careers] Error: ${e.message}`);
  }
  return jobs;
}

// Try Workday careers
async function scrapeWorkdayCareers() {
  const jobs = [];
  try {
    console.log("[Workday Careers] Trying to scrape...");
    
    const res = await axios.get("https://www.workday.com/en-us/company/careers.html", {
      timeout: 15000,
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      }
    });
    
    const $ = cheerio.load(res.data);
    
    $(".job-listing, .career-item, [data-role='job']").each((_, el) => {
      const title = $(el).find("h3, .job-title").text().trim();
      const location = $(el).find(".location").text().trim();
      const link = $(el).find("a").attr("href") || "";
      
      if (title) {
        jobs.push({
          id: `workday:${link || Math.random().toString(36).substr(2, 9)}`,
          source: "workday",
          company: "Workday",
          title,
          location: location || "Remote",
          url: link.startsWith("http") ? link : `https://www.workday.com${link}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: `${title} at Workday - Enterprise HR Platform`
        });
      }
    });
    
    console.log(`[Workday Careers] Found ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Workday Careers] Error: ${e.message}`);
  }
  return jobs;
}

// Main function to fetch HR platform jobs
export async function fetchHRPlatformJobs() {
  console.log("\n🚀 FETCHING HR PLATFORM COMPANY JOBS\n");
  console.log("Companies:", HR_PLATFORM_COMPANIES.slice(0, 10).join(", ") + "...\n");
  
  const allJobs = [];
  
  // Method 1: Try direct career page scraping
  const dayforceJobs = await scrapeDayforceCareers();
  allJobs.push(...dayforceJobs);
  
  const workdayJobs = await scrapeWorkdayCareers();
  allJobs.push(...workdayJobs);
  
  // Method 2: Search Adzuna by company name
  console.log("Searching Adzuna for HR platform company jobs...\n");
  
  for (let i = 0; i < Math.min(20, HR_PLATFORM_COMPANIES.length); i++) {
    const company = HR_PLATFORM_COMPANIES[i];
    const locations = ["Toronto", "Vancouver", "Montreal", "Calgary", "Remote"];
    const location = locations[i % locations.length];
    
    const jobs = await fetchAdzunaJobsByCompany(company, location, 1);
    
    if (jobs.length > 0) {
      console.log(`[${i + 1}/20] ${company}: ${jobs.length} jobs`);
      allJobs.push(...jobs);
    }
    
    await sleep(200);
  }
  
  console.log(`\n========================================`);
  console.log(`HR PLATFORM JOBS COMPLETE`);
  console.log(`Total jobs: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  return allJobs;
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchHRPlatformJobs().catch(console.error);
}
