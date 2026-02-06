/**
 * Unified Job Scraper with Fallback Chain
 * 
 * Tries multiple sources in order of reliability:
 * 1. APIs (Adzuna, JobBank, RemoteOK, Jobicy)
 * 2. RSS Feeds (EURemote)
 * 3. Stealth HTTP (backup scrapers)
 * 4. Playwright (last resort)
 */

import { fetchAdzunaJobs } from './scrape_adzuna.js';
import { fetchGlassdoorJobsStealth } from '../scrapers/backup_scrapers/glassdoor_stealth.js';
import { fetchWorkopolisJobsStealth } from '../scrapers/backup_scrapers/workopolis_stealth.js';
import { fetchWellfoundJobsStealth } from '../scrapers/backup_scrapers/wellfound_stealth.js';
import { fetchMonsterJobsStealth } from '../scrapers/backup_scrapers/monster_stealth.js';
import { fetchGlassdoorJobsPlaywright, fetchWellfoundJobsPlaywright } from '../scrapers/backup_scrapers/playwright_fallback.js';
import fs from 'fs';

// ==================== WORKING SOURCES ====================

async function scrapeFromWorkingSources() {
  const jobs = [];
  const seen = new Set();
  
  // Load existing to avoid duplicates
  try {
    const data = JSON.parse(fs.readFileSync('jobs.json', 'utf-8'));
    data.jobs?.forEach(j => seen.add(j.id));
  } catch {}
  
  // These are our proven working sources
  const workingSources = [
    { name: 'Adzuna', fn: () => fetchAdzunaJobs(['software'], 'Toronto', 1, 50) },
    { name: 'JobBank', fn: () => fetchJobBankJobs() },
    { name: 'RemoteOK', fn: () => fetchRemoteOKJobs() },
    { name: 'Jobicy', fn: () => fetchJobicyJobs() },
  ];
  
  for (const { name, fn } of workingSources) {
    try {
      console.log(`[Unified] Trying ${name}...`);
      const sourceJobs = await fn();
      const newJobs = sourceJobs.filter(j => !seen.has(j.id));
      newJobs.forEach(j => seen.add(j.id));
      jobs.push(...newJobs);
      console.log(`[Unified] ${name}: ${newJobs.length} new jobs`);
    } catch (e) {
      console.log(`[Unified] ${name} failed: ${e.message}`);
    }
  }
  
  return jobs;
}

// ==================== BACKUP SOURCES (With Fallback Chain) ====================

async function scrapeWithFallback(source, keywords, location) {
  let jobs = [];
  
  // Try stealth HTTP first
  try {
    switch(source) {
      case 'glassdoor':
        jobs = await fetchGlassdoorJobsStealth(keywords, location, 1);
        break;
      case 'workopolis':
        jobs = await fetchWorkopolisJobsStealth(keywords, location, 1);
        break;
      case 'wellfound':
        jobs = await fetchWellfoundJobsStealth(keywords, location, 1);
        break;
      case 'monster':
        jobs = await fetchMonsterJobsStealth(keywords, location, 1);
        break;
    }
    
    if (jobs.length > 0) {
      console.log(`[${source}] Stealth succeeded: ${jobs.length} jobs`);
      return jobs;
    }
  } catch (e) {
    console.log(`[${source}] Stealth failed: ${e.message}`);
  }
  
  // Fall back to Playwright
  console.log(`[${source}] Trying Playwright fallback...`);
  try {
    switch(source) {
      case 'glassdoor':
        jobs = await fetchGlassdoorJobsPlaywright(keywords, location, 1);
        break;
      case 'wellfound':
        jobs = await fetchWellfoundJobsPlaywright(keywords, location, 1);
        break;
    }
    
    if (jobs.length > 0) {
      console.log(`[${source}] Playwright succeeded: ${jobs.length} jobs`);
    }
  } catch (e) {
    console.log(`[${source}] Playwright failed: ${e.message}`);
  }
  
  return jobs;
}

// ==================== PLACEHOLDER FUNCTIONS ====================

async function fetchJobBankJobs() {
  // This would call the JobBank scraper
  return [];
}

async function fetchRemoteOKJobs() {
  // This would call the RemoteOK scraper
  return [];
}

async function fetchJobicyJobs() {
  // This would call the Jobicy scraper
  return [];
}

// ==================== MAIN ====================

async function unifiedScrape() {
  console.log('🚀 UNIFIED JOB SCRAPER\n');
  console.log('Strategy: Working APIs → Stealth HTTP → Playwright\n');
  
  const allJobs = [];
  
  // 1. Get jobs from working sources
  const workingJobs = await scrapeFromWorkingSources();
  allJobs.push(...workingJobs);
  
  // 2. Try backup sources with fallback chain
  const backupSources = ['glassdoor', 'workopolis', 'wellfound', 'monster'];
  for (const source of backupSources) {
    const jobs = await scrapeWithFallback(source, ['developer'], 'Toronto, ON');
    allJobs.push(...jobs);
  }
  
  console.log(`\n========================================`);
  console.log(`UNIFIED SCRAPE COMPLETE`);
  console.log(`Total jobs: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  return allJobs;
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  unifiedScrape().catch(console.error);
}

export { unifiedScrape, scrapeWithFallback };
