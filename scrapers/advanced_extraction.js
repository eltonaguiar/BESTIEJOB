/**
 * Proxy rotation and schema.org structured data extraction
 */

import axios from "axios";
import * as cheerio from "cheerio";

// Free proxy list (rotating - these change frequently)
const PROXY_LIST = [
  // These are example formats - in production use paid rotating proxies
  // Format: { host: 'proxy.example.com', port: 8080, auth: { username: 'user', password: 'pass' } }
];

// For production, use services like:
// - Bright Data (brightdata.com)
// - Smartproxy (smartproxy.com)
// - Oxylabs (oxylabs.io)
// - ScrapingBee (scrapingbee.com)

let currentProxyIndex = 0;

export function getNextProxy() {
  if (PROXY_LIST.length === 0) return null;
  const proxy = PROXY_LIST[currentProxyIndex];
  currentProxyIndex = (currentProxyIndex + 1) % PROXY_LIST.length;
  return proxy;
}

export function createProxyAgent(proxy) {
  if (!proxy) return null;
  
  const proxyUrl = proxy.auth 
    ? `http://${proxy.auth.username}:${proxy.auth.password}@${proxy.host}:${proxy.port}`
    : `http://${proxy.host}:${proxy.port}`;
    
  // Note: In Node.js 18+, axios uses proxy config directly
  return {
    protocol: 'http',
    host: proxy.host,
    port: proxy.port,
    auth: proxy.auth
  };
}

/**
 * Extract schema.org JobPosting structured data from HTML
 * This is more reliable than CSS selectors
 */
export function extractSchemaOrgJobs(html) {
  const jobs = [];
  const $ = cheerio.load(html);
  
  // Look for JSON-LD script tags
  $('script[type="application/ld+json"]').each((_, el) => {
    try {
      const data = JSON.parse($(el).html() || '{}');
      
      // Handle single job posting
      if (data['@type'] === 'JobPosting') {
        const job = parseJobPosting(data);
        if (job) jobs.push(job);
      }
      
      // Handle arrays of job postings
      if (Array.isArray(data)) {
        for (const item of data) {
          if (item['@type'] === 'JobPosting') {
            const job = parseJobPosting(item);
            if (job) jobs.push(job);
          }
        }
      }
      
    } catch (e) {
      // Invalid JSON, skip
    }
  });
  
  return jobs;
}

function parseJobPosting(data) {
  try {
    const company = data.hiringOrganization?.name || 
                   data.hiringOrganization?.legalName || 
                   'Unknown';
    
    const location = data.jobLocation?.address?.addressLocality || 
                    data.jobLocation?.address?.addressRegion || 
                    data.jobLocation?.address?.addressCountry || 
                    'Remote';
    
    const salary = data.baseSalary?.value?.value || 
                  data.baseSalary?.value?.minValue || 
                  null;
    
    return {
      id: `schemaorg:${Buffer.from(data.title + company).toString('base64').substring(0, 20)}`,
      source: 'schemaorg',
      title: data.title,
      company,
      location,
      url: data.url,
      employmentType: data.employmentType || 'full-time',
      salary: salary ? { min: salary, max: data.baseSalary?.value?.maxValue || salary } : null,
      postedDate: data.datePosted || new Date().toISOString(),
      excerpt: data.description?.substring(0, 200) || data.title,
      industry: data.industry,
      skills: data.skills
    };
  } catch (e) {
    return null;
  }
}

/**
 * Scrape with proxy rotation and schema.org extraction
 */
export async function scrapeWithProxyAndSchema(url, options = {}) {
  const proxy = options.useProxy ? getNextProxy() : null;
  const proxyConfig = createProxyAgent(proxy);
  
  try {
    const res = await axios.get(url, {
      timeout: 20000,
      proxy: proxyConfig,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-CA,en;q=0.9'
      }
    });
    
    // Try schema.org first
    let jobs = extractSchemaOrgJobs(res.data);
    
    // Fallback to CSS selectors if no schema.org data
    if (jobs.length === 0 && options.cssSelectors) {
      jobs = extractWithCSS(res.data, options.cssSelectors);
    }
    
    return jobs;
    
  } catch (err) {
    console.error(`[Proxy/Schema] Failed: ${err.message}`);
    return [];
  }
}

function extractWithCSS(html, selectors) {
  const $ = cheerio.load(html);
  const jobs = [];
  
  $(selectors.container).each((_, el) => {
    const title = $(el).find(selectors.title).text().trim();
    const company = $(el).find(selectors.company).text().trim() || 'Unknown';
    const location = $(el).find(selectors.location).text().trim() || 'Remote';
    const link = $(el).find(selectors.link).attr('href') || '';
    
    if (title) {
      jobs.push({
        id: `css:${Buffer.from(title + company).toString('base64').substring(0, 20)}`,
        source: 'css-extraction',
        title,
        company,
        location,
        url: link,
        employmentType: 'full-time',
        postedDate: new Date().toISOString(),
        excerpt: title
      });
    }
  });
  
  return jobs;
}

/**
 * Test schema.org extraction on a URL
 */
export async function testSchemaExtraction(url) {
  console.log(`\n[Schema Test] Testing ${url}...`);
  
  try {
    const res = await axios.get(url, {
      timeout: 15000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });
    
    const jobs = extractSchemaOrgJobs(res.data);
    
    console.log(`[Schema Test] Found ${jobs.length} jobs with schema.org markup`);
    
    if (jobs.length > 0) {
      console.log('Sample job:', jobs[0]);
    }
    
    return jobs;
  } catch (err) {
    console.error(`[Schema Test] Failed: ${err.message}`);
    return [];
  }
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  // Test on a known job board
  testSchemaExtraction('https://weworkremotely.com/remote-jobs')
    .then(() => process.exit(0))
    .catch(() => process.exit(1));
}
