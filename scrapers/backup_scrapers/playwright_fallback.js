import { chromium } from 'playwright';

/**
 * Playwright-based scraper for sites with strong anti-bot protection
 * Uses real browser automation to bypass detection
 */

export async function fetchWithPlaywright(url, selector, extractFn, timeout = 30000) {
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    await page.goto(url, { waitUntil: 'networkidle', timeout });
    
    // Wait for content to load
    await page.waitForSelector(selector, { timeout: 10000 });
    
    // Extract data
    const jobs = await page.evaluate(extractFn);
    
    return jobs;
  } finally {
    await browser.close();
  }
}

/**
 * Glassdoor scraper using Playwright
 */
export async function fetchGlassdoorJobsPlaywright(keywords = ['manager'], location = 'Toronto, ON', maxPages = 1) {
  const jobs = [];
  const search = encodeURIComponent(keywords.join('-'));
  const loc = encodeURIComponent(location.toLowerCase().replace(', ', '-').replace(' ', '-'));
  
  for (let page = 1; page <= maxPages; page++) {
    const url = `https://www.glassdoor.ca/Job/${loc}-${search}-jobs-SRCH_IL.0,${loc.length}_KO0,${search.length}.htm`;
    
    try {
      const pageJobs = await fetchWithPlaywright(
        url,
        '[data-test="job-listing"]',
        () => {
          const listings = document.querySelectorAll('[data-test="job-listing"]');
          return Array.from(listings).map(el => ({
            title: el.querySelector('[data-test="job-title"]')?.textContent?.trim() || '',
            company: el.querySelector('[data-test="employer-name"]')?.textContent?.trim() || '',
            location: el.querySelector('[data-test="job-location"]')?.textContent?.trim() || '',
            url: el.querySelector('a')?.href || '',
            salary: el.querySelector('[data-test="job-salary"]')?.textContent?.trim() || null
          })).filter(j => j.title && j.company);
        }
      );
      
      jobs.push(...pageJobs.map(j => ({
        ...j,
        id: `glassdoor:${Math.random().toString(36).substr(2, 9)}`,
        source: 'glassdoor',
        employmentType: 'full-time',
        postedDate: new Date().toISOString(),
        excerpt: `${j.title} at ${j.company}`
      })));
      
    } catch (err) {
      console.error(`[Glassdoor Playwright] Page ${page} failed:`, err.message);
    }
  }
  
  return jobs;
}

/**
 * Wellfound scraper using Playwright
 */
export async function fetchWellfoundJobsPlaywright(keywords = ['engineer'], location = 'Toronto', maxPages = 1) {
  const jobs = [];
  
  for (let page = 1; page <= maxPages; page++) {
    const url = `https://wellfound.com/jobs?location=${encodeURIComponent(location)}&keywords=${encodeURIComponent(keywords.join(' '))}`;
    
    try {
      const pageJobs = await fetchWithPlaywright(
        url,
        '.job-listing, [data-test="job-listing"]',
        () => {
          const listings = document.querySelectorAll('.job-listing, [data-test="job-listing"]');
          return Array.from(listings).map(el => ({
            title: el.querySelector('.job-title, h3')?.textContent?.trim() || '',
            company: el.querySelector('.company-name')?.textContent?.trim() || '',
            location: el.querySelector('.location')?.textContent?.trim() || 'Remote',
            url: el.querySelector('a')?.href || ''
          })).filter(j => j.title && j.company);
        }
      );
      
      jobs.push(...pageJobs.map(j => ({
        ...j,
        id: `wellfound:${Math.random().toString(36).substr(2, 9)}`,
        source: 'wellfound',
        employmentType: 'full-time',
        postedDate: new Date().toISOString(),
        excerpt: `${j.title} at ${j.company}`
      })));
      
    } catch (err) {
      console.error(`[Wellfound Playwright] Page ${page} failed:`, err.message);
    }
  }
  
  return jobs;
}
