import * as cheerio from "cheerio";
import axios from "axios";

const USER_AGENTS = [
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
];

function getRandomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchHtml(url) {
  try {
    await sleep(2000 + Math.random() * 3000);
    const response = await axios.get(url, {
      headers: {
        "User-Agent": getRandomUA(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5"
      },
      timeout: 15000,
      maxRedirects: 5
    });
    return response.data;
  } catch (error) {
    console.warn(`Fetch failed for ${url}:`, error.message);
    return null;
  }
}

// We Work Remotely - popular remote job board
export async function scrapeWeWorkRemotely() {
  const jobs = [];
  try {
    const html = await fetchHtml("https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&search=developer");
    if (!html) return jobs;
    
    const $ = cheerio.load(html);
    $("li.new-listing-container").each((_, el) => {
      const title = $(el).find("h4.new-listing__title").text().trim();
      const company = $(el).find("p.new-listing__company-name").text().trim();
      const url = $(el).find("a").attr("href");
      const location = $(el).find("span.new-listing__company-headquarters").text().trim();
      
      if (title && url) {
        jobs.push({
          id: `weworkremotely:${url.split("/").pop()}`,
          source: "weworkremotely",
          company: company || "Various",
          title,
          location: location || "Remote",
          url: url.startsWith("http") ? url : `https://weworkremotely.com${url}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    console.log(`[We Work Remotely] Found ${jobs.length} jobs`);
  } catch (e) {
    console.warn("[We Work Remotely] Error:", e.message);
  }
  return jobs;
}

// RemoteOK - another popular remote job board
export async function scrapeRemoteOK() {
  const jobs = [];
  try {
    const html = await fetchHtml("https://remoteok.com/remote-developer-jobs");
    if (!html) return jobs;
    
    const $ = cheerio.load(html);
    $("tr.job").each((_, el) => {
      const title = $(el).find("h2[itemprop='title']").text().trim();
      const company = $(el).find("h3[itemprop='name']").text().trim();
      const url = $(el).find("a[itemprop='url']").attr("href");
      
      if (title && url) {
        jobs.push({
          id: `remoteok:${url.split("/").pop()}`,
          source: "remoteok",
          company: company || "Various",
          title,
          location: "Remote",
          url: url.startsWith("http") ? url : `https://remoteok.com${url}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    console.log(`[RemoteOK] Found ${jobs.length} jobs`);
  } catch (e) {
    console.warn("[RemoteOK] Error:", e.message);
  }
  return jobs;
}

// JobBank Canada - Government jobs
export async function scrapeJobBank() {
  const jobs = [];
  try {
    const searchTerm = encodeURIComponent("software developer");
    const html = await fetchHtml(`https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=${searchTerm}&locationstring=Toronto%2C+ON`);
    if (!html) return jobs;
    
    const $ = cheerio.load(html);
    $("a.resultJobItem").each((_, el) => {
      const title = $(el).find("span.noctitle").text().trim();
      const company = $(el).find("span.business").text().trim();
      const location = $(el).find("span.location").text().trim();
      const url = $(el).attr("href");
      
      if (title && url) {
        jobs.push({
          id: `jobbank:${url.split("/").pop()}`,
          source: "jobbank",
          company: company || "Government of Canada",
          title,
          location: location || "Toronto, ON",
          url: url.startsWith("http") ? url : `https://www.jobbank.gc.ca${url}`,
          employmentType: "full-time",
          salary: null,
          postedDate: new Date().toISOString(),
          excerpt: title
        });
      }
    });
    console.log(`[JobBank] Found ${jobs.length} jobs`);
  } catch (e) {
    console.warn("[JobBank] Error:", e.message);
  }
  return jobs;
}

// All alternative sources combined
export async function scrapeAlternativeJobs() {
  console.log("\n[Alternative Sources] Starting...");
  
  const [wework, remoteok, jobbank] = await Promise.allSettled([
    scrapeWeWorkRemotely(),
    scrapeRemoteOK(),
    scrapeJobBank()
  ]);
  
  const jobs = [
    ...(wework.status === "fulfilled" ? wework.value : []),
    ...(remoteok.status === "fulfilled" ? remoteok.value : []),
    ...(jobbank.status === "fulfilled" ? jobbank.value : [])
  ];
  
  console.log(`[Alternative Sources] Total: ${jobs.length} jobs`);
  return jobs;
}

export default {
  scrapeWeWorkRemotely,
  scrapeRemoteOK,
  scrapeJobBank,
  scrapeAlternativeJobs
};
