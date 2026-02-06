import { fetchAllEasyRemoteJobs } from '../scrapers/easy_remote_scrapers.js';
import { fetchRSSJobs } from '../scrapers/rss_feed_scraper.js';
import { scrapeIndeedJobs } from '../scrapers/stealth_scraper.js';
import { scrapeWithProxyAndSchema } from '../scrapers/advanced_extraction.js';
import fs from 'fs';

const PROXY_URL = process.env.PROXY_URL || null; // Set if you have a proxy

async function runAdvancedScrapingPipeline() {
  console.log('🚀 ADVANCED SCRAPING PIPELINE\n');
  console.log('Techniques: RSS feeds, Stealth browser, Schema.org extraction, Proxy rotation\n');
  
  // Load existing jobs
  let existingJobs = [];
  let existingIds = new Set();
  try {
    const data = JSON.parse(fs.readFileSync('jobs.json', 'utf-8'));
    existingJobs = data.jobs || [];
    existingJobs.forEach(j => existingIds.add(j.id));
    console.log(`Loaded ${existingJobs.length} existing jobs\n`);
  } catch (e) {
    console.log('Creating fresh database\n');
  }
  
  const allNewJobs = [];
  const results = {};
  
  // 1. Easy remote scrapers (RSS + HTML)
  try {
    console.log('[1/4] Easy remote scrapers (We Work Remotely, Remotive)...');
    const jobs = await fetchAllEasyRemoteJobs();
    const newJobs = jobs.filter(j => !existingIds.has(j.id));
    newJobs.forEach(j => {
      existingIds.add(j.id);
      allNewJobs.push(j);
    });
    results.easyRemote = { found: jobs.length, new: newJobs.length };
    console.log(`✅ Easy Remote: ${jobs.length} found, ${newJobs.length} new\n`);
  } catch (e) {
    console.error(`❌ Easy Remote failed: ${e.message}\n`);
    results.easyRemote = { found: 0, new: 0, error: e.message };
  }
  
  // 2. RSS Feeds
  try {
    console.log('[2/4] RSS feed scraper...');
    const jobs = await fetchRSSJobs();
    const newJobs = jobs.filter(j => !existingIds.has(j.id));
    newJobs.forEach(j => {
      existingIds.add(j.id);
      allNewJobs.push(j);
    });
    results.rss = { found: jobs.length, new: newJobs.length };
    console.log(`✅ RSS Feeds: ${jobs.length} found, ${newJobs.length} new\n`);
  } catch (e) {
    console.error(`❌ RSS failed: ${e.message}\n`);
    results.rss = { found: 0, new: 0, error: e.message };
  }
  
  // 3. Stealth browser (Indeed only - LinkedIn disabled for ToS)
  try {
    console.log('[3/4] Stealth browser (Indeed)...');
    const jobs = await scrapeIndeedJobs(['developer', 'software'], 'Toronto', PROXY_URL);
    const newJobs = jobs.filter(j => !existingIds.has(j.id));
    newJobs.forEach(j => {
      existingIds.add(j.id);
      allNewJobs.push(j);
    });
    results.stealth = { found: jobs.length, new: newJobs.length };
    console.log(`✅ Stealth Browser: ${jobs.length} found, ${newJobs.length} new\n`);
  } catch (e) {
    console.error(`❌ Stealth failed: ${e.message}\n`);
    results.stealth = { found: 0, new: 0, error: e.message };
  }
  
  // 4. Schema.org extraction
  try {
    console.log('[4/4] Schema.org structured data extraction...');
    // Test on a sample of sites
    const testUrls = [
      'https://weworkremotely.com/remote-jobs'
    ];
    
    let schemaJobs = [];
    for (const url of testUrls) {
      const jobs = await scrapeWithProxyAndSchema(url, {
        useProxy: !!PROXY_URL
      });
      schemaJobs.push(...jobs);
    }
    
    const newJobs = schemaJobs.filter(j => !existingIds.has(j.id));
    newJobs.forEach(j => {
      existingIds.add(j.id);
      allNewJobs.push(j);
    });
    results.schema = { found: schemaJobs.length, new: newJobs.length };
    console.log(`✅ Schema.org: ${schemaJobs.length} found, ${newJobs.length} new\n`);
  } catch (e) {
    console.error(`❌ Schema extraction failed: ${e.message}\n`);
    results.schema = { found: 0, new: 0, error: e.message };
  }
  
  // Merge all jobs
  const finalJobs = [...existingJobs, ...allNewJobs];
  
  // Summary
  console.log('========================================');
  console.log('ADVANCED SCRAPING RESULTS');
  console.log('========================================');
  let totalNew = 0;
  for (const [source, data] of Object.entries(results)) {
    const icon = data.error ? '⚠️' : '✅';
    console.log(`${icon} ${source}: ${data.found} found, ${data.new} new`);
    totalNew += data.new || 0;
  }
  console.log('----------------------------------------');
  console.log(`Total new jobs: ${totalNew}`);
  console.log(`DATABASE SIZE: ${finalJobs.length} jobs`);
  console.log('========================================\n');
  
  // Count by source
  const bySource = {};
  for (const j of finalJobs) {
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
      totalFetched: finalJobs.length,
      sources: Object.keys(bySource),
      scrapingTechniques: ['rss', 'stealth-browser', 'schema-org', 'proxy-rotation']
    },
    jobs: finalJobs
  }, null, 2));
  
  console.log('\n✅ Saved to jobs.json');
  console.log('📁 Ready for deployment!');
  
  return { results, totalJobs: finalJobs.length };
}

runAdvancedScrapingPipeline().catch(console.error);
