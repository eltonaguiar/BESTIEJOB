import axios from "axios";
import { HttpsProxyAgent } from "https-proxy-agent";
import { CookieJar } from "tough-cookie";
import { wrapper } from "axios-cookiejar-support";

// Playwright is optional - only imported when needed
let chromium = null;
async function getChromium() {
  if (!chromium) {
    const { chromium: playwright } = await import("playwright");
    chromium = playwright;
  }
  return chromium;
}

// Stealth headers mimicking real Chrome browser
const STEALTH_HEADERS = {
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
  "accept-encoding": "gzip, deflate, br",
  "accept-language": "en-CA,en-US;q=0.9,en;q=0.8",
  "cache-control": "max-age=0",
  "sec-ch-ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "\"Windows\"",
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "none",
  "sec-fetch-user": "?1",
  "upgrade-insecure-requests": "1",
  "dnt": "1"
};

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15"
];

function getRandomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function getProxyList() {
  const envProxies = process.env.PROXY_LIST;
  if (envProxies) {
    return envProxies.split(",").map(p => p.trim()).filter(Boolean);
  }
  return [];
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function gaussianDelay(min, max) {
  let u = 0, v = 0;
  while(u === 0) u = Math.random();
  while(v === 0) v = Math.random();
  let num = Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
  num = num / 10.0 + 0.5;
  if (num > 1 || num < 0) return gaussianDelay(min, max);
  return Math.floor(num * (max - min) + min);
}

// Stealth fetch with axios - tries proxies and rotates headers
export async function stealthFetch(url, options = {}) {
  const proxies = getProxyList();
  const maxRetries = options.maxRetries || 3;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const proxy = proxies.length > 0 ? proxies[attempt % proxies.length] : null;
      const agent = proxy ? new HttpsProxyAgent(proxy) : undefined;
      
      await sleep(gaussianDelay(1000, 3000));
      
      const jar = new CookieJar();
      const client = wrapper(axios.create({ jar }));
      
      const response = await client.get(url, {
        httpsAgent: agent,
        timeout: 30000,
        headers: {
          ...STEALTH_HEADERS,
          "user-agent": getRandomUA(),
          "referer": "https://www.google.com/",
          ...options.headers
        },
        maxRedirects: 5
      });
      
      if (response.status === 200) {
        return response;
      }
      throw new Error(`HTTP ${response.status}`);
    } catch (error) {
      if (attempt === maxRetries - 1) throw error;
      await sleep(gaussianDelay(2000, 5000));
    }
  }
  throw new Error("All retries failed");
}

// Browser-based scraping as LAST RESORT - requires playwright
export async function scrapeWithBrowser(url) {
  const browserModule = await import("playwright").catch(() => null);
  if (!browserModule) {
    throw new Error("Playwright not installed - skipping browser fallback");
  }
  
  const { chromium } = browserModule;
  const browser = await chromium.launch({ 
    headless: true,
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--disable-accelerated-2d-canvas",
      "--disable-gpu",
      "--window-size=1920,1080"
    ]
  });
  
  try {
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: getRandomUA()
    });
    
    const page = await context.newPage();
    
    // Bypass webdriver detection
    await page.addInitScript(() => {
      Object.defineProperty(navigator, "webdriver", { get: () => undefined });
      Object.defineProperty(navigator, "plugins", { get: () => [1, 2, 3, 4, 5] });
    });
    
    await page.goto(url, { waitUntil: "networkidle", timeout: 60000 });
    
    // Human-like behavior
    await page.mouse.move(Math.random() * 500, Math.random() * 500);
    await sleep(gaussianDelay(2000, 4000));
    
    const content = await page.content();
    return content;
  } finally {
    await browser.close();
  }
}

// Mobile API approach - often less protected
export async function fetchMobileApi({ keyword, location }) {
  const deviceId = "android-" + Math.random().toString(36).substring(2, 15);
  
  const response = await stealthFetch(
    "https://mobile.indeed.com/api/search",
    {
      headers: {
        "content-type": "application/json",
        "x-indeed-mobile-device-id": deviceId,
        "x-indeed-mobile-app-version": "100.0",
        "x-indeed-mobile-platform": "android",
        "accept": "application/json",
        "user-agent": "Indeed Mobile App 100.0 (Android 13; SM-G998B)"
      }
    }
  );
  
  return response.data;
}

// Check if blocked
export function isBlocked(html) {
  return (
    html.includes("unusual traffic") ||
    html.includes("verify you are human") ||
    html.includes("captcha") ||
    html.includes("Access Denied") ||
    html.length < 5000
  );
}

export { gaussianDelay, sleep, getRandomUA };
