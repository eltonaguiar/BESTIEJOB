import Parser from "rss-parser";
import fs from "fs";

const rssParser = new Parser({
  headers: {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml,application/xml;q=0.9,*/*;q=0.8"
  },
  timeout: 15000
});

const KEYWORDS = ["software", "developer", "engineer", "manager", "analyst"];

async function scrapeIndeedRSS() {
  const jobs = [];
  const seen = new Set();
  
  for (const keyword of KEYWORDS) {
    try {
      const q = encodeURIComponent(keyword);
      const l = encodeURIComponent("Toronto, ON");
      
      // Try multiple RSS endpoints
      const endpoints = [
        `https://rss.indeed.com/rss?q=${q}&l=${l}`,
        `https://ca.indeed.com/rss?q=${q}&l=${l}&sort=date&fromage=7`,
        `https://www.indeed.com/rss?q=${q}&l=${l}`
      ];
      
      for (const url of endpoints) {
        try {
          console.log(`[Indeed RSS] Trying: ${url}`);
          const feed = await rssParser.parseURL(url);
          const items = Array.isArray(feed?.items) ? feed.items : [];
          
          console.log(`[Indeed RSS] Got ${items.length} items`);
          
          for (const it of items) {
            const title = it.title?.replace(/ - job post$/, "").trim();
            const company = it.creator || it.author || "Unknown";
            const link = it.link;
            
            if (title && !seen.has(link)) {
              seen.add(link);
              jobs.push({
                id: `indeed:${link?.split("jk=").pop()?.split("&")[0] || Math.random().toString(36).substr(2, 9)}`,
                source: "indeed",
                company,
                title,
                location: "Toronto, ON",
                url: link,
                employmentType: "full-time",
                salary: null,
                postedDate: it.pubDate ? new Date(it.pubDate).toISOString() : new Date().toISOString(),
                excerpt: it.contentSnippet?.substring(0, 240) || title
              });
            }
          }
          
          if (jobs.length > 0) break; // If we got jobs, stop trying other endpoints
        } catch (e) {
          console.log(`[Indeed RSS] Failed: ${e.message}`);
        }
      }
      
      // Delay between keywords
      await new Promise(r => setTimeout(r, 2000));
    } catch (e) {
      console.warn(`[Indeed RSS] Keyword "${keyword}" error:`, e.message);
    }
  }
  
  console.log(`\n[Indeed RSS] Total unique jobs: ${jobs.length}`);
  return jobs;
}

async function main() {
  console.log("Trying Indeed RSS feeds...\n");
  
  const indeedJobs = await scrapeIndeedRSS();
  
  if (indeedJobs.length > 0) {
    // Load existing jobs
    let existingJobs = [];
    try {
      const data = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
      existingJobs = data.jobs || [];
    } catch (e) {}
    
    // Filter out existing Indeed jobs
    const nonIndeed = existingJobs.filter(j => j.source !== "indeed");
    
    // Merge
    const merged = [...nonIndeed, ...indeedJobs];
    
    // Count by source
    const bySource = {};
    for (const j of merged) {
      bySource[j.source] = (bySource[j.source] || 0) + 1;
    }
    
    console.log(`\nFinal: ${merged.length} jobs`);
    console.log("By source:", bySource);
    
    // Save
    fs.writeFileSync("jobs.json", JSON.stringify({
      meta: {
        scrapedAt: new Date().toISOString(),
        totalFetched: merged.length,
        sources: Object.keys(bySource)
      },
      jobs: merged
    }, null, 2));
    
    console.log("✅ Saved to jobs.json");
  } else {
    console.log("❌ No Indeed jobs found via RSS");
  }
}

main();
