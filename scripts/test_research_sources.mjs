import { fetchAllResearchSources } from '../scrapers/research_sources_scraper.js';
import fs from 'fs';

async function testResearchSources() {
  console.log('🚀 TESTING RESEARCH-BACKED JOB SOURCES\n');
  console.log('Sources: Jooble, USAJobs, AuthenticJobs, AngelList\n');
  
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
  
  // Fetch research sources
  const newJobs = await fetchAllResearchSources(process.env.USAJOBS_API_KEY);
  
  // Filter and merge
  let added = 0;
  for (const job of newJobs) {
    if (!existingIds.has(job.id)) {
      existingIds.add(job.id);
      existingJobs.push(job);
      added++;
    }
  }
  
  console.log(`\n========================================`);
  console.log('RESEARCH SOURCES MERGE COMPLETE');
  console.log(`Found: ${newJobs.length} jobs`);
  console.log(`New: ${added} jobs`);
  console.log(`TOTAL: ${existingJobs.length} jobs`);
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

testResearchSources().catch(console.error);
