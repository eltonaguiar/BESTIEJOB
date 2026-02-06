import { fetchGlassdoorJobsBackup } from '../scrapers/backup_scrapers/glassdoor_scraper.js';
import { fetchWorkopolisJobsBackup } from '../scrapers/backup_scrapers/workopolis_scraper.js';
import { fetchWellfoundJobsBackup } from '../scrapers/backup_scrapers/wellfound_scraper.js';
import { fetchMonsterJobsBackup } from '../scrapers/backup_scrapers/monster_scraper.js';
import fs from 'fs';

async function testBackupScrapers() {
  console.log('🧪 TESTING BACKUP SCRAPERS\n');
  
  const results = {};
  const allJobs = [];
  
  // Test Glassdoor
  try {
    console.log('Testing Glassdoor...');
    const glassdoorJobs = await fetchGlassdoorJobsBackup(['software'], 'Toronto, ON', 1);
    results.glassdoor = glassdoorJobs.length;
    allJobs.push(...glassdoorJobs);
    console.log(`✅ Glassdoor: ${glassdoorJobs.length} jobs`);
  } catch (e) {
    console.log(`❌ Glassdoor failed: ${e.message}`);
    results.glassdoor = 0;
  }
  
  // Test Workopolis
  try {
    console.log('\nTesting Workopolis...');
    const workopolisJobs = await fetchWorkopolisJobsBackup(['developer'], 'Toronto, ON', 1);
    results.workopolis = workopolisJobs.length;
    allJobs.push(...workopolisJobs);
    console.log(`✅ Workopolis: ${workopolisJobs.length} jobs`);
  } catch (e) {
    console.log(`❌ Workopolis failed: ${e.message}`);
    results.workopolis = 0;
  }
  
  // Test Wellfound
  try {
    console.log('\nTesting Wellfound...');
    const wellfoundJobs = await fetchWellfoundJobsBackup(['engineer'], 'Toronto, ON', 1);
    results.wellfound = wellfoundJobs.length;
    allJobs.push(...wellfoundJobs);
    console.log(`✅ Wellfound: ${wellfoundJobs.length} jobs`);
  } catch (e) {
    console.log(`❌ Wellfound failed: ${e.message}`);
    results.wellfound = 0;
  }
  
  // Test Monster
  try {
    console.log('\nTesting Monster...');
    const monsterJobs = await fetchMonsterJobsBackup(['manager'], 'Toronto, ON', 1);
    results.monster = monsterJobs.length;
    allJobs.push(...monsterJobs);
    console.log(`✅ Monster: ${monsterJobs.length} jobs`);
  } catch (e) {
    console.log(`❌ Monster failed: ${e.message}`);
    results.monster = 0;
  }
  
  console.log('\n========================================');
  console.log('BACKUP SCRAPER TEST RESULTS');
  console.log('========================================');
  for (const [source, count] of Object.entries(results)) {
    const status = count > 0 ? '✅' : '❌';
    console.log(`${status} ${source}: ${count} jobs`);
  }
  console.log(`\nTotal jobs from backup scrapers: ${allJobs.length}`);
  console.log('========================================\n');
  
  // Save test results
  fs.writeFileSync('backup_test_results.json', JSON.stringify({
    timestamp: new Date().toISOString(),
    results,
    totalJobs: allJobs.length,
    sampleJobs: allJobs.slice(0, 10)
  }, null, 2));
  
  console.log('✅ Results saved to backup_test_results.json');
  
  return { results, jobs: allJobs };
}

testBackupScrapers().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
