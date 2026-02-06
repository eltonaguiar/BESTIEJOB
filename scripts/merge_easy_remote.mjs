import { fetchAllEasyRemoteJobs } from '../scrapers/easy_remote_scrapers.js';
import fs from 'fs';

async function mergeEasyRemoteJobs() {
  console.log('🚀 MERGING EASY REMOTE JOBS\n');
  
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
  
  // Fetch easy remote jobs
  console.log('\nFetching from easy remote sources...');
  const remoteJobs = await fetchAllEasyRemoteJobs();
  
  // Filter and merge
  let added = 0;
  for (const job of remoteJobs) {
    if (!existingIds.has(job.id)) {
      existingIds.add(job.id);
      existingJobs.push(job);
      added++;
    }
  }
  
  console.log(`\n========================================`);
  console.log(`MERGE COMPLETE`);
  console.log(`Remote jobs found: ${remoteJobs.length}`);
  console.log(`New jobs added: ${added}`);
  console.log(`TOTAL DATABASE: ${existingJobs.length} jobs`);
  console.log(`========================================\n`);
  
  // Count by source
  const bySource = {};
  for (const j of existingJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  console.log('Sources breakdown:');
  for (const [source, count] of Object.entries(bySource).sort((a, b) => b[1] - a[1])) {
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

mergeEasyRemoteJobs().catch(console.error);
