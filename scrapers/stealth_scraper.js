import { chromium } from 'playwright';

/**
 * Advanced Stealth Scraper using Playwright
 * Implements multiple anti-detection techniques:
 * - Stealth plugins (user agent spoofing, webdriver hiding)
 * - Human-like behavior (random mouse movements, delays)
 * - Browser fingerprint randomization
 * - Session persistence
 * - Proxy rotation support
 */

const STEALTH_PLUGINS = [
  // Hide webdriver property
  () => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  },
  // Override permissions
  () => {
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => (
      parameters.name === 'notifications' 
        ? Promise.resolve({ state: Notification.permission })
        : originalQuery(parameters)
    );
  },
  // Hide Playwright-specific properties
  () => {
    delete navigator.__proto__.webdriver;
    window.chrome = { runtime: {} };
  }
];

const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
];

const VIEWPORTS = [
  { width: 1920, height: 1080 },
  { width: 1366, height: 768 },
  { width: 1440, height: 900 },
  { width: 1536, height: 864 }
];

function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function getRandomViewport() {
  return VIEWPORTS[Math.floor(Math.random() * VIEWPORTS.length)];
}

function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

function randomDelay(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}

/**
 * Create browser context with stealth settings
 */
async function createStealthContext(proxy = null) {
  const browser = await chromium.launch({
    headless: true,
    proxy: proxy ? { server: proxy } : undefined,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-web-security',
      '--disable-features=IsolateOrigins,site-per-process',
      '--disable-site-isolation-trials'
    ]
  });

  const context = await browser.newContext({
    userAgent: getRandomUserAgent(),
    viewport: getRandomViewport(),
    locale: 'en-CA',
    timezoneId: 'America/Toronto',
    permissions: ['notifications'],
    bypassCSP: true,
    extraHTTPHeaders: {
      'Accept-Language': 'en-CA,en;q=0.9',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Accept-Encoding': 'gzip, deflate, br',
      'DNT': '1',
      'Connection': 'keep-alive',
      'Upgrade-Insecure-Requests': '1',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1'
    }
  });

  // Inject stealth scripts
  await context.addInitScript(() => {
    // Override navigator.webdriver
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    
    // Override chrome object
    window.chrome = { runtime: {} };
    
    // Override permissions API
    const originalQuery = window.navigator.permissions?.query;
    if (originalQuery) {
      window.navigator.permissions.query = (parameters) => {
        if (parameters.name === 'notifications') {
          return Promise.resolve({ state: Notification.permission });
        }
        return originalQuery(parameters);
      };
    }
    
    // Hide Playwright-specific properties
    delete navigator.__proto__.webdriver;
    
    // Add plugins length
    Object.defineProperty(navigator, 'plugins', {
      get: () => [1, 2, 3, 4, 5]
    });
    
    // Add languages
    Object.defineProperty(navigator, 'languages', {
      get: () => ['en-CA', 'en', 'fr']
    });
  });

  return { browser, context };
}

/**
 * Human-like mouse movement
 */
async function humanLikeMove(page, x, y) {
  const steps = randomDelay(5, 10);
  const startX = randomDelay(100, 300);
  const startY = randomDelay(100, 300);
  
  for (let i = 0; i <= steps; i++) {
    const progress = i / steps;
    const ease = 1 - Math.pow(1 - progress, 3); // ease-out
    const currX = Math.floor(startX + (x - startX) * ease);
    const currY = Math.floor(startY + (y - startY) * ease);
    
    await page.mouse.move(currX, currY);
    await sleep(randomDelay(10, 30));
  }
}

/**
 * Scroll like a human
 */
async function humanLikeScroll(page) {
  const scrolls = randomDelay(3, 7);
  
  for (let i = 0; i < scrolls; i++) {
    const scrollAmount = randomDelay(100, 400);
    await page.mouse.wheel(0, scrollAmount);
    await sleep(randomDelay(500, 1500));
    
    // Random pause to "read"
    if (Math.random() > 0.7) {
      await sleep(randomDelay(2000, 4000));
    }
  }
}

/**
 * Scrape jobs with stealth browser
 */
export async function scrapeWithStealthBrowser(url, selectors, extractFn, proxy = null) {
  const { browser, context } = await createStealthContext(proxy);
  
  try {
    const page = await context.newPage();
    
    // Set extra headers
    await page.setExtraHTTPHeaders({
      'Referer': 'https://www.google.com/search?q=jobs'
    });
    
    // Navigate with human-like delay
    await page.goto(url, { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    // Random initial wait
    await sleep(randomDelay(2000, 4000));
    
    // Human-like scroll
    await humanLikeScroll(page);
    
    // Wait for content
    for (const selector of selectors) {
      try {
        await page.waitForSelector(selector, { timeout: 10000 });
        break;
      } catch {}
    }
    
    // Move mouse to random element
    const elements = await page.$$('a, button, h1, h2, h3');
    if (elements.length > 0) {
      const randomEl = elements[Math.floor(Math.random() * elements.length)];
      const box = await randomEl.boundingBox();
      if (box) {
        await humanLikeMove(page, box.x + box.width / 2, box.y + box.height / 2);
      }
    }
    
    // Extract data
    const jobs = await page.evaluate(extractFn);
    
    return jobs;
    
  } finally {
    await browser.close();
  }
}

/**
 * Scrape LinkedIn jobs with stealth (requires login - ethical concerns)
 * Note: LinkedIn scraping is against their ToS. This is for educational purposes.
 */
export async function scrapeLinkedInJobs(keywords, location, proxy = null) {
  console.log('[Stealth] LinkedIn scraping disabled - violates ToS');
  return [];
}

/**
 * Scrape Indeed jobs with stealth
 */
export async function scrapeIndeedJobs(keywords, location, proxy = null) {
  const search = encodeURIComponent(keywords.join(' '));
  const loc = encodeURIComponent(location);
  const url = `https://ca.indeed.com/jobs?q=${search}&l=${loc}`;
  
  const selectors = ['[data-testid="jobTitle"]', '.jobTitle', '.slider_container .slider_item'];
  
  const extractFn = () => {
    const jobs = [];
    const listings = document.querySelectorAll('[data-testid="jobTitle"], .jobTitle, .slider_container .slider_item');
    
    listings.forEach(el => {
      const titleEl = el.querySelector('h2 a, a[href*="/rc/clk"], a[href*="/viewjob"]') || el;
      const title = titleEl.textContent?.trim();
      const link = titleEl.href || '';
      
      const companyEl = el.querySelector('[data-testid="company-name"], .companyName, [data-testid="job-location"]');
      const company = companyEl?.textContent?.trim() || 'Unknown';
      
      const locationEl = el.querySelector('[data-testid="job-location"], [data-testid="jobTitle"] + div');
      const jobLocation = locationEl?.textContent?.trim() || location;
      
      const salaryEl = el.querySelector('[data-testid="job-salary"], .estimated-salary, .salary-snippet-container');
      const salary = salaryEl?.textContent?.trim() || null;
      
      if (title && title.length > 3) {
        jobs.push({
          title,
          company,
          location: jobLocation,
          url: link.startsWith('http') ? link : `https://ca.indeed.com${link}`,
          salary,
          excerpt: title
        });
      }
    });
    
    return jobs;
  };
  
  try {
    const jobs = await scrapeWithStealthBrowser(url, selectors, extractFn, proxy);
    
    return jobs.map(j => ({
      ...j,
      id: `indeed:${Buffer.from(j.title + j.company).toString('base64').substring(0, 20)}`,
      source: 'indeed',
      employmentType: 'full-time',
      postedDate: new Date().toISOString()
    }));
  } catch (err) {
    console.error('[Stealth] Indeed failed:', err.message);
    return [];
  }
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  scrapeIndeedJobs(['developer'], 'Toronto')
    .then(jobs => {
      console.log(`\nFound ${jobs.length} Indeed jobs`);
      console.log(jobs.slice(0, 3));
    })
    .catch(console.error);
}
