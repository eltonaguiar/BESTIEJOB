import axios from "axios";
import { HttpsProxyAgent } from "https-proxy-agent";

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
];

function getProxyList() {
  const envProxies = process.env.PROXY_LIST;
  if (envProxies) {
    return envProxies.split(",").map(p => p.trim()).filter(Boolean);
  }
  return [];
}

function getRandomUserAgent() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function getRandomProxy() {
  const proxies = getProxyList();
  if (proxies.length === 0) return null;
  return proxies[Math.floor(Math.random() * proxies.length)];
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function jitter(baseDelay, jitterFactor = 0.3) {
  const jitterAmount = baseDelay * jitterFactor * (Math.random() * 2 - 1);
  return Math.max(0, baseDelay + jitterAmount);
}

function calculateDelay(attempt, baseDelay = 1000, maxDelay = 30000) {
  const exponential = baseDelay * Math.pow(2, attempt);
  const withJitter = jitter(Math.min(exponential, maxDelay));
  return Math.floor(withJitter);
}

function createAxiosConfig(proxyUrl = null) {
  const config = {
    headers: {
      "User-Agent": getRandomUserAgent(),
      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Accept-Language": "en-US,en;q=0.5",
      "Accept-Encoding": "gzip, deflate, br",
      "DNT": "1",
      "Connection": "keep-alive",
      "Upgrade-Insecure-Requests": "1",
      "Sec-Fetch-Dest": "document",
      "Sec-Fetch-Mode": "navigate",
      "Sec-Fetch-Site": "none",
      "Sec-Fetch-User": "?1",
      "Cache-Control": "max-age=0"
    },
    timeout: 30000,
    maxRedirects: 5
  };

  if (proxyUrl) {
    config.httpsAgent = new HttpsProxyAgent(proxyUrl);
    config.proxy = false;
  }

  return config;
}

export async function fetchWithRetry(url, options = {}) {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    strategicDelay: stratDelay = 0,
    useProxy = true,
    fallbackProxies = true,
    headers: customHeaders = {}
  } = options;

  let lastError;
  const proxies = useProxy ? [getRandomProxy(), ...(fallbackProxies ? [getRandomProxy(), getRandomProxy()] : [])].filter(Boolean) : [null];
  const uniqueProxies = [...new Set(proxies)];

  for (let proxyIndex = 0; proxyIndex < uniqueProxies.length; proxyIndex++) {
    const currentProxy = uniqueProxies[proxyIndex];

    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        if (stratDelay > 0 && (attempt > 0 || proxyIndex > 0)) {
          const delay = stratDelay + Math.random() * 1000;
          await sleep(delay);
        }

        const config = createAxiosConfig(currentProxy);
        // Merge custom headers
        if (customHeaders && Object.keys(customHeaders).length > 0) {
          config.headers = { ...config.headers, ...customHeaders };
        }
        
        const response = await axios.get(url, config);

        if (response.status === 200) {
          return response;
        }

        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      } catch (error) {
        lastError = error;

        const isRetryable = error.code === "ECONNRESET" ||
                           error.code === "ETIMEDOUT" ||
                           error.code === "ECONNREFUSED" ||
                           error.response?.status === 429 ||
                           error.response?.status === 503 ||
                           error.response?.status === 502 ||
                           error.response?.status >= 500;

        if (!isRetryable && error.response?.status !== undefined) {
          throw error;
        }

        if (attempt < maxRetries - 1) {
          const delay = calculateDelay(attempt, baseDelay);
          console.warn(`Request failed (proxy: ${currentProxy || "none"}, attempt ${attempt + 1}/${maxRetries}): ${error.message}. Retrying in ${delay}ms...`);
          await sleep(delay);
        }
      }
    }

    if (proxyIndex < uniqueProxies.length - 1) {
      console.warn(`Switching proxy from ${currentProxy || "none"} to ${uniqueProxies[proxyIndex + 1] || "none"}`);
    }
  }

  throw lastError || new Error(`Failed to fetch ${url} after ${maxRetries} retries across ${uniqueProxies.length} proxies`);
}

export async function strategicDelay(minMs = 2000, maxMs = 5000) {
  const delay = minMs + Math.random() * (maxMs - minMs);
  await sleep(delay);
}

export function getRandomUserAgentString() {
  return getRandomUserAgent();
}

export function createHeaders() {
  return {
    "User-Agent": getRandomUserAgent(),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "DNT": "1",
    "Connection": "keep-alive"
  };
}
