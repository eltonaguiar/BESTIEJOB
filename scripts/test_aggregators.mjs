import { fetchAllAggregatorJobs } from '../scrapers/aggregator_scrapers.js';
import fs from 'fs';

async function testAndMergeAggregators() {
  console.log('🚀 TESTING AGGREGATOR SOURCES\n');
  
  // Load existing
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync('jobs.json', 'utf-8'));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs\n`);
  } catch {
    console.log('Creating fresh database\n');
  }
  
  // Fetch aggregator jobs
  console.log('Fetching from Jooble, CareerJet, Talent.com, Monster, CareerBuilder, ZipRecruiter...\n');
  const newJobs = await fetchAllAggregatorJobs();
  
  // Filter duplicates
  let added = 0;
  for (const job of newJobs) {
    if (!existingIds.has(job.id)) {
      existingIds.add(job.id);
      existingJobs.push(job);
      added++;
    }
  }
  
  console.log(`\n========================================`);
  console.log('AGGREGATOR MERGE COMPLETE');
  console.log(`Found: ${newJobs.length} jobs`);
  console.log(`New: ${added} jobs`);
  console.log(`TOTAL: ${existingJobs.length} jobs`);
  console.log(`========================================\n`);
  
  // Count by source
  const bySource = {};
  for (const j of existingJobs) {
    bySource[j.source] = (bySource[j.source] || 0) + 1;
  }
  console.log('Sources:');
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

testAndMergeAggregators().catch(console.error);
