/**
 * Unified scraper test - integrates all new scraper-friendly sources
 * Tests SimplyHired, Working Nomads, ATS APIs, and Remote Boards
 */

import { fetchSimplyHiredJobs } from '../scrapers/simplyhired_scraper.js';
import { fetchWorkingNomadsJobs } from '../scrapers/workingnomads_scraper.js';
import { fetchAllATSJobs } from '../scrapers/ats_api_scraper.js';
import { fetchAllRemoteBoards } from '../scrapers/remote_boards_scraper.js';
import fs from 'fs';

async function testAllNewScrapers() {
  console.log('🚀 TESTING ALL NEW SCRAPER-FRIENDLY SOURCES\n');
  
  const results = {};
  const allJobs = [];
  
  // Load existing jobs
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync('jobs.json', 'utf-8'));
    data.jobs?.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingIds.size} existing job IDs for deduplication\n`);
  } catch (e) {
    console.log('No existing jobs.json\n');
  }
  
  // 1. Test SimplyHired
  try {
    console.log('[1/4] Testing SimplyHired...');
    const jobs = await fetchSimplyHiredJobs(['developer', 'software'], 'Toronto', 2);
    const newJobs = jobs.filter(j => !existingIds.has(j.id));
    newJobs.forEach(j => existingIds.add(j.id));
    allJobs.push(...newJobs);
    results.simplyhired = { found: jobs.length, new: newJobs.length };
    console.log(`✅ SimplyHired: ${jobs.length} found, ${newJobs.length} new\n`);
  } catch (e) {
    console.error(`❌ SimplyHired failed: ${e.message}\n`);
    results.simplyhired = { found: 0, new: 0, error: e.message };
  }
  
  // 2. Test Working Nomads
  try {
    console.log('[2/4] Testing Working Nomads...');
    const jobs = await fetchWorkingNomadsJobs(2);
    const newJobs = jobs.filter(j => !existingIds.has(j.id));
    newJobs.forEach(j => existingIds.add(j.id));
    allJobs.push(...newJobs);
    results.workingnomads = { found: jobs.length, new: newJobs.length };
    console.log(`✅ WorkingNomads: ${jobs.length} found, ${newJobs.length} new\n`);
  } catch (e) {
    console.error(`❌ WorkingNomads failed: ${e.message}\n`);
    results.workingnomads = { found: 0, new: 0, error: e.message };
  }
  
  // 3. Test ATS APIs
  try {
    console.log('[3/4] Testing ATS APIs (Greenhouse, Lever, Ashby, Workable)...');
    const jobs = await fetchAllATSJobs();
    const newJobs = jobs.filter(j => !existingIds.has(j.id));
    newJobs.forEach(j => existingIds.add(j.id));
    allJobs.push(...newJobs);
    results.ats_apis = { found: jobs.length, new: newJobs.length };
    console.log(`✅ ATS APIs: ${jobs.length} found, ${newJobs.length} new\n`);
  } catch (e) {
    console.error(`❌ ATS APIs failed: ${e.message}\n`);
    results.ats_apis = { found: 0, new: 0, error: e.message };
  }
  
  // 4. Test Remote Boards
  try {
    console.log('[4/4] Testing Remote Boards (RemoteYeah, 4DayWeek, Pangian, PowerToFly)...');
    const jobs = await fetchAllRemoteBoards();
    const newJobs = jobs.filter(j => !existingIds.has(j.id));
    newJobs.forEach(j => existingIds.add(j.id));
    allJobs.push(...newJobs);
    results.remote_boards = { found: jobs.length, new: newJobs.length };
    console.log(`✅ Remote Boards: ${jobs.length} found, ${newJobs.length} new\n`);
  } catch (e) {
    console.error(`❌ Remote Boards failed: ${e.message}\n`);
    results.remote_boards = { found: 0, new: 0, error: e.message };
  }
  
  // Summary
  console.log('========================================');
  console.log('NEW SCRAPER TEST RESULTS');
  console.log('========================================');
  
  let totalFound = 0;
  let totalNew = 0;
  
  for (const [source, data] of Object.entries(results)) {
    const icon = data.error ? '❌' : '✅';
    console.log(`${icon} ${source}: ${data.found} found, ${data.new} new`);
    totalFound += data.found || 0;
    totalNew += data.new || 0;
  }
  
  console.log('----------------------------------------');
  console.log(`TOTAL: ${totalFound} found, ${totalNew} new jobs added`);
  console.log('========================================\n');
  
  // Save results
  fs.writeFileSync('scraper_test_results.json', JSON.stringify({
    timestamp: new Date().toISOString(),
    results,
    summary: { totalFound, totalNew },
    newJobs: allJobs.slice(0, 50)
  }, null, 2));
  
  console.log('✅ Test results saved to scraper_test_results.json');
  
  return { results, jobs: allJobs };
}

testAllNewScrapers().catch(console.error);
