import { fetchHRPlatformJobs } from '../scrapers/hr_platform_scraper.js';
import fs from 'fs';

async function mergeHRPlatformJobs() {
  console.log('🚀 MERGING HR PLATFORM COMPANY JOBS\n');
  
  // Load existing jobs
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync('jobs.json', 'utf-8'));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs\n`);
  } catch (e) {
    console.log('Creating new jobs.json\n');
  }
  
  // Fetch HR platform jobs
  console.log('Fetching from Dayforce, Workday, and Adzuna company searches...\n');
  const hrJobs = await fetchHRPlatformJobs();
  
  // Filter duplicates and merge
  let added = 0;
  for (const job of hrJobs) {
    if (!existingIds.has(job.id)) {
      existingIds.add(job.id);
      existingJobs.push(job);
      added++;
    }
  }
  
  console.log(`\n========================================`);
  console.log(`HR PLATFORM MERGE COMPLETE`);
  console.log(`HR jobs found: ${hrJobs.length}`);
  console.log(`New jobs added: ${added}`);
  console.log(`TOTAL DATABASE: ${existingJobs.length} jobs`);
  console.log(`========================================\n`);
  
  // Count by source
  const bySource = {};
  for (const j of existingJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  console.log('Sources breakdown:');
  for (const [source, count] of Object.entries(bySource).sort((a, b) => b[1] - a[1]).slice(0, 15)) {
    console.log(`  ${source}: ${count}`);
  }
  
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

mergeHRPlatformJobs().catch(console.error);
