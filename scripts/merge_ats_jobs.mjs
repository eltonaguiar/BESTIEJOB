import { fetchAllATSJobs } from '../scrapers/ats_api_scraper.js';
import fs from 'fs';

async function mergeATSJobs() {
  console.log('🚀 MERGING ATS API JOBS INTO DATABASE\n');
  
  // Load existing jobs
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync('jobs.json', 'utf-8'));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs`);
  } catch (e) {
    console.log('Creating new jobs.json');
  }
  
  // Fetch ATS jobs
  console.log('\nFetching ATS API jobs...');
  const atsJobs = await fetchAllATSJobs();
  
  // Filter duplicates and merge
  let added = 0;
  for (const job of atsJobs) {
    if (!existingIds.has(job.id)) {
      existingIds.add(job.id);
      existingJobs.push(job);
      added++;
    }
  }
  
  console.log(`\n========================================`);
  console.log(`MERGE COMPLETE`);
  console.log(`ATS jobs found: ${atsJobs.length}`);
  console.log(`New jobs added: ${added}`);
  console.log(`TOTAL DATABASE: ${existingJobs.length} jobs`);
  console.log(`========================================\n`);
  
  // Count by source
  const bySource = {};
  for (const j of existingJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  console.log('By source:', bySource);
  
  // Save
  fs.writeFileSync('jobs.json', JSON.stringify({
    meta: {
      scrapedAt: new Date().toISOString(),
      totalFetched: existingJobs.length,
      sources: Object.keys(bySource)
    },
    jobs: existingJobs
  }, null, 2));
  
  console.log('\n✅ Saved to jobs.json');
  return existingJobs;
}

mergeATSJobs().catch(console.error);
