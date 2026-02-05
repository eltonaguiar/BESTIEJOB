import { scrapeAlternativeJobs } from '../scrapers/alternative_scraper.js';
import fs from 'fs';

console.log('Testing alternative job sources...\n');

const jobs = await scrapeAlternativeJobs();

console.log('\n========================================');
console.log(`TOTAL: ${jobs.length} real jobs`);
console.log('========================================\n');

if (jobs.length > 0) {
  console.log('Sample jobs:');
  jobs.slice(0, 5).forEach(j => {
    console.log(`- ${j.title} @ ${j.company} (${j.source})`);
    console.log(`  URL: ${j.url}`);
    console.log('');
  });
  
  // Save to jobs.json
  fs.writeFileSync('jobs.json', JSON.stringify({
    meta: {
      scrapedAt: new Date().toISOString(),
      totalFetched: jobs.length,
      sources: ['weworkremotely', 'remoteok', 'jobbank']
    },
    jobs: jobs
  }, null, 2));
  
  console.log('✅ Saved real jobs to jobs.json');
} else {
  console.log('❌ No jobs found from alternative sources');
  process.exit(1);
}
