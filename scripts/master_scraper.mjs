import { fetchAdzunaJobs } from './scrape_adzuna.js';
import { fetchAllATSJobs } from '../scrapers/ats_api_scraper.js';
import fs from 'fs';

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

const ADZUNA_KEYWORDS = [
  "software", "developer", "engineer", "manager", "analyst", "designer",
  "product", "marketing", "sales", "data", "cloud", "devops", "qa"
];

const LOCATIONS = [
  "Toronto", "Vancouver", "Montreal", "Calgary", "Ottawa", "Edmonton",
  "Winnipeg", "Victoria", "Halifax", "Kitchener", "Waterloo"
];

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function fetchAdzunaJobsDirect(keyword, location, page = 1) {
  try {
    const url = `http://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=100&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&content-type=application/json`;
    
    const response = await axios.get(url, {
      timeout: 30000,
      headers: { "Accept": "application/json" }
    });
    
    return (response.data?.results || []).map(job => ({
      id: `adzuna:${job.id || Math.random().toString(36).substr(2, 9)}`,
      source: "adzuna",
      company: job.company?.display_name || "Unknown",
      title: job.title,
      location: job.location?.display_name || `${location}, Canada`,
      url: job.redirect_url,
      employmentType: "full-time",
      salary: job.salary_min && job.salary_max ? { min: Math.round(job.salary_min), max: Math.round(job.salary_max) } : null,
      postedDate: job.created_at || new Date().toISOString(),
      excerpt: job.description?.substring(0, 240) || job.title
    }));
  } catch (error) {
    return [];
  }
}

async function runMasterScraper() {
  console.log('🚀 MASTER SCRAPER - REFRESHING ALL SOURCES\n');
  
  // Load existing
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync('jobs.json', 'utf-8'));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs\n`);
  } catch {
    console.log('Starting fresh database\n');
  }
  
  const allJobs = [...existingJobs];
  let newCount = 0;
  
  // 1. Adzuna API (bulk fetch)
  console.log('[1/3] Fetching from Adzuna API...');
  for (let i = 0; i < Math.min(ADZUNA_KEYWORDS.length, 8); i++) {
    const keyword = ADZUNA_KEYWORDS[i];
    const location = LOCATIONS[i % LOCATIONS.length];
    
    const jobs = await fetchAdzunaJobsDirect(keyword, location, 1);
    
    for (const job of jobs) {
      if (!existingIds.has(job.id)) {
        existingIds.add(job.id);
        allJobs.push(job);
        newCount++;
      }
    }
    
    if ((i + 1) % 4 === 0) {
      console.log(`  Progress: ${i + 1}/${Math.min(ADZUNA_KEYWORDS.length, 8)} keywords, ${allJobs.length} total jobs`);
    }
    
    await sleep(200);
  }
  
  // 2. ATS APIs
  console.log('\n[2/3] Fetching from ATS APIs (Greenhouse, Ashby)...');
  const atsJobs = await fetchAllATSJobs();
  
  for (const job of atsJobs) {
    if (!existingIds.has(job.id)) {
      existingIds.add(job.id);
      allJobs.push(job);
      newCount++;
    }
  }
  
  // 3. Summary
  console.log('\n[3/3] Finalizing...');
  
  const bySource = {};
  for (const j of allJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  
  console.log('\n========================================');
  console.log('MASTER SCRAPE COMPLETE');
  console.log(`New jobs added: ${newCount}`);
  console.log(`TOTAL DATABASE: ${allJobs.length} jobs`);
  console.log('========================================\n');
  
  console.log('Sources breakdown:');
  for (const [source, count] of Object.entries(bySource).sort((a, b) => b[1] - a[1])) {
    console.log(`  ${source}: ${count}`);
  }
  
  // Save
  fs.writeFileSync('jobs.json', JSON.stringify({
    meta: {
      scrapedAt: new Date().toISOString(),
      totalFetched: allJobs.length,
      sources: Object.keys(bySource)
    },
    jobs: allJobs
  }, null, 2));
  
  console.log('\n✅ Saved to jobs.json');
  console.log('📁 Copy to public/ and deploy with: npm run deploy');
  
  return allJobs;
}

runMasterScraper().catch(console.error);
