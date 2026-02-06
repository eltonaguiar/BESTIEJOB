import { fetchGlassdoorJobsStealth } from '../scrapers/backup_scrapers/glassdoor_stealth.js';
import { fetchWorkopolisJobsStealth } from '../scrapers/backup_scrapers/workopolis_stealth.js';
import { fetchWellfoundJobsStealth } from '../scrapers/backup_scrapers/wellfound_stealth.js';
import { fetchMonsterJobsStealth } from '../scrapers/backup_scrapers/monster_stealth.js';
import fs from 'fs';

async function testStealthScrapers() {
  console.log('🥷 TESTING STEALTH-ENHANCED BACKUP SCRAPERS\n');
  
  const results = {};
  const allJobs = [];
  
  // Test Glassdoor Stealth
  try {
    console.log('Testing Glassdoor Stealth...');
    const glassdoorJobs = await fetchGlassdoorJobsStealth(['software'], 'Toronto, ON', 1);
    results.glassdoor = glassdoorJobs.length;
    allJobs.push(...glassdoorJobs);
    console.log(`✅ Glassdoor Stealth: ${glassdoorJobs.length} jobs`);
  } catch (e) {
    console.log(`❌ Glassdoor Stealth failed: ${e.message}`);
    results.glassdoor = 0;
  }
  
  // Test Workopolis Stealth
  try {
    console.log('\nTesting Workopolis Stealth...');
    const workopolisJobs = await fetchWorkopolisJobsStealth(['developer'], 'Toronto, ON', 1);
    results.workopolis = workopolisJobs.length;
    allJobs.push(...workopolisJobs);
    console.log(`✅ Workopolis Stealth: ${workopolisJobs.length} jobs`);
  } catch (e) {
    console.log(`❌ Workopolis Stealth failed: ${e.message}`);
    results.workopolis = 0;
  }
  
  // Test Wellfound Stealth
  try {
    console.log('\nTesting Wellfound Stealth...');
    const wellfoundJobs = await fetchWellfoundJobsStealth(['engineer'], 'Toronto, ON', 1);
    results.wellfound = wellfoundJobs.length;
    allJobs.push(...wellfoundJobs);
    console.log(`✅ Wellfound Stealth: ${wellfoundJobs.length} jobs`);
  } catch (e) {
    console.log(`❌ Wellfound Stealth failed: ${e.message}`);
    results.wellfound = 0;
  }
  
  // Test Monster Stealth
  try {
    console.log('\nTesting Monster Stealth...');
    const monsterJobs = await fetchMonsterJobsStealth(['manager'], 'Toronto, ON', 1);
    results.monster = monsterJobs.length;
    allJobs.push(...monsterJobs);
    console.log(`✅ Monster Stealth: ${monsterJobs.length} jobs`);
  } catch (e) {
    console.log(`❌ Monster Stealth failed: ${e.message}`);
    results.monster = 0;
  }
  
  console.log('\n========================================');
  console.log('STEALTH SCRAPER TEST RESULTS');
  console.log('========================================');
  for (const [source, count] of Object.entries(results)) {
    const status = count > 0 ? '✅' : '❌';
    console.log(`${status} ${source}: ${count} jobs`);
  }
  console.log(`\nTotal jobs from stealth scrapers: ${allJobs.length}`);
  console.log('========================================\n');
  
  // Save test results
  fs.writeFileSync('stealth_test_results.json', JSON.stringify({
    timestamp: new Date().toISOString(),
    results,
    totalJobs: allJobs.length,
    sampleJobs: allJobs.slice(0, 10)
  }, null, 2));
  
  console.log('✅ Results saved to stealth_test_results.json');
  
  return { results, jobs: allJobs };
}

testStealthScrapers().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
