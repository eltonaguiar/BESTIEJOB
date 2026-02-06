import Parser from "rss-parser";
import fs from "fs";

const rssParser = new Parser({
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
  }
});

// RSS Feed URLs for job sources
const RSS_FEEDS = [
  { name: "weworkremotely", url: "https://weworkremotely.com/remote-jobs.rss", type: "remote" },
  { name: "remotive", url: "https://remotive.com/api/remote-jobs", type: "api" },
  { name: "euremote", url: "https://europeremotely.com/feed.xml", type: "rss" },
  { name: "jobicy", url: "https://jobicy.com/api/v2/remote-jobs", type: "api" }
];

/**
 * Fetch jobs from RSS feeds - lightweight and respectful
 */
export async function fetchRSSJobs() {
  console.log("\n📡 FETCHING FROM RSS FEEDS\n");
  
  const allJobs = [];
  
  for (const feed of RSS_FEEDS) {
    try {
      console.log(`[RSS] Fetching ${feed.name}...`);
      
      if (feed.type === "api") {
        // Handle API endpoints (already covered in other scrapers)
        continue;
      }
      
      const parsed = await rssParser.parseURL(feed.url);
      
      for (const item of parsed.items || []) {
        // Extract company from title (usually "Company: Title" format)
        let company = "Unknown";
        let title = item.title || "";
        
        if (title.includes(":")) {
          const parts = title.split(":");
          company = parts[0].trim();
          title = parts.slice(1).join(":").trim();
        }
        
        allJobs.push({
          id: `${feed.name}:${Buffer.from(item.title || '').toString('base64').substring(0, 20)}`,
          source: feed.name,
          company,
          title,
          location: "Remote",
          url: item.link,
          employmentType: "remote",
          salary: null,
          postedDate: item.pubDate || item.isoDate || new Date().toISOString(),
          excerpt: (item.contentSnippet || item.description || title).substring(0, 200)
        });
      }
      
      console.log(`[RSS] ${feed.name}: ${parsed.items?.length || 0} jobs`);
      
    } catch (err) {
      console.error(`[RSS] ${feed.name} failed: ${err.message}`);
    }
  }
  
  console.log(`\n[RSS] Total jobs from feeds: ${allJobs.length}`);
  return allJobs;
}

/**
 * Incremental update - only fetch jobs newer than last check
 */
export async function fetchIncrementalRSS(lastCheckDate = null) {
  const allJobs = await fetchRSSJobs();
  
  if (!lastCheckDate) {
    return allJobs;
  }
  
  const cutoff = new Date(lastCheckDate);
  const newJobs = allJobs.filter(job => {
    const jobDate = new Date(job.postedDate);
    return jobDate > cutoff;
  });
  
  console.log(`[RSS] Incremental: ${newJobs.length} new jobs since ${lastCheckDate}`);
  return newJobs;
}

// Test if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  fetchRSSJobs()
    .then(jobs => {
      console.log("\nSample RSS jobs:");
      console.log(jobs.slice(0, 3));
    })
    .catch(console.error);
}
