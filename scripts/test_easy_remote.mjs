import { fetchAllEasyRemoteJobs } from '../scrapers/easy_remote_scrapers.js';
import fs from 'fs';

async function testEasyRemoteScrapers() {
  console.log('🚀 TESTING EASY-TO-SCRAPE REMOTE SOURCES\n');
  
  // Load existing jobs
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync('jobs.json', 'utf-8'));
    data.jobs?.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingIds.size} existing job IDs\n`);
  } catch (e) {
    console.log('No existing jobs.json\n');
  }
  
  // Fetch from easy remote sources
  const jobs = await fetchAllEasyRemoteJobs();
  
  // Filter new jobs
  const newJobs = jobs.filter(j => !existingIds.has(j.id));
  
  console.log(`========================================`);
  console.log('EASY REMOTE SCRAPERS TEST RESULTS');
  console.log(`========================================`);
  console.log(`Found: ${jobs.length} jobs`);
  console.log(`New: ${newJobs.length} jobs`);
  console.log(`========================================\n`);
  
  return newJobs;
}

testEasyRemoteScrapers()
  .then(jobs => {
    if (jobs.length > 0) {
      console.log('Sample new jobs:');
      console.log(jobs.slice(0, 3));
    }
  })
  .catch(console.error);
