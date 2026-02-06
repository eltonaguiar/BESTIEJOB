#!/usr/bin/env node
/**
 * Test script to verify LinkedIn and Indeed scrapers are working
 */

import { scrapeLinkedInJobs } from "../scrapers/linkedin_scraper.js";
import { scrapeIndeedJobs } from "../scrapers/indeed_scraper.js";

const TEST_KEYWORDS = ["ServiceNow developer", "VBA", "Alteryx"];
const TEST_LOCATION = "Toronto, ON";

function log(msg) {
  console.log(`[${new Date().toLocaleTimeString()}] ${msg}`);
}

async function testLinkedIn() {
  log("=== Testing LinkedIn Scraper ===");
  
  for (const keyword of TEST_KEYWORDS) {
    try {
      log(`\nSearching LinkedIn for: "${keyword}"`);
      const jobs = await scrapeLinkedInJobs({
        keyword,
        location: TEST_LOCATION,
        dateFilter: "week",
        maxPages: 1,
        useFallbackApi: true
      });
      
      log(`✅ LinkedIn "${keyword}": Found ${jobs.length} jobs`);
      
      if (jobs.length > 0) {
        const sample = jobs[0];
        log(`   Sample: ${sample.title} at ${sample.company}`);
        log(`   URL: ${sample.url}`);
        log(`   Posted: ${sample.postedDate || "N/A"}`);
      }
    } catch (error) {
      log(`❌ LinkedIn "${keyword}" failed: ${error.message}`);
    }
    
    // Delay between searches
    await new Promise(r => setTimeout(r, 3000));
  }
}

async function testIndeed() {
  log("\n=== Testing Indeed Scraper ===");
  
  for (const keyword of TEST_KEYWORDS) {
    try {
      log(`\nSearching Indeed for: "${keyword}"`);
      const jobs = await scrapeIndeedJobs({
        keyword,
        location: TEST_LOCATION,
        dateFilter: "week",
        maxPages: 1,
        useFallbackApi: true
      });
      
      log(`✅ Indeed "${keyword}": Found ${jobs.length} jobs`);
      
      if (jobs.length > 0) {
        const sample = jobs[0];
        log(`   Sample: ${sample.title} at ${sample.company}`);
        log(`   URL: ${sample.url}`);
        log(`   Posted: ${sample.postedDate || "N/A"}`);
      }
    } catch (error) {
      log(`❌ Indeed "${keyword}" failed: ${error.message}`);
    }
    
    // Delay between searches
    await new Promise(r => setTimeout(r, 5000));
  }
}

async function main() {
  log("╔══════════════════════════════════════════╗");
  log("║     BESTIEJOB - Scraper Test Suite       ║");
  log("╚══════════════════════════════════════════╝");
  log(`Location: ${TEST_LOCATION}`);
  log(`Keywords: ${TEST_KEYWORDS.join(", ")}`);
  
  try {
    await testLinkedIn();
    await testIndeed();
    
    log("\n╔══════════════════════════════════════════╗");
    log("║         Test Suite Complete              ║");
    log("╚══════════════════════════════════════════╝");
  } catch (error) {
    log(`\n❌ Test suite failed: ${error.message}`);
    console.error(error);
    process.exit(1);
  }
}

main();
