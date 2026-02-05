import axios from "axios";
import Parser from "rss-parser";
import fs from "fs";

const rssParser = new Parser({ timeout: 10000 });

// ==================== 1. JOBICY (Free API) ====================
async function scrapeJobicy() {
  const jobs = [];
  try {
    const url = "https://jobicy.com/api/v2/remote-jobs?count=100&geo=canada";
    const response = await axios.get(url, { timeout: 15000 });
    const data = response.data?.jobs || [];
    
    for (const job of data) {
      jobs.push({
        id: `jobicy:${job.id}`,
        source: "jobicy",
        company: job.companyName,
        title: job.jobTitle,
        location: job.jobGeo || "Remote",
        url: job.url,
        employmentType: job.jobType || "full-time",
        salary: job.salaryMin ? { min: job.salaryMin, max: job.salaryMax } : null,
        postedDate: job.pubDate,
        excerpt: job.jobExcerpt || job.jobDescription?.substring(0, 240)
      });
    }
    console.log(`[Jobicy] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Jobicy] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 2. REMOTEOK (Free API) ====================
async function scrapeRemoteOK() {
  const jobs = [];
  try {
    const url = "https://remoteok.com/api";
    const response = await axios.get(url, { timeout: 15000 });
    const data = Array.isArray(response.data) ? response.data.slice(1) : [];
    
    for (const job of data.slice(0, 100)) {
      if (job.position) {
        jobs.push({
          id: `remoteok:${job.id || Math.random()}`,
          source: "remoteok",
          company: job.company,
          title: job.position,
          location: "Remote",
          url: job.apply_url || job.url,
          employmentType: "full-time",
          salary: job.salary ? { min: parseInt(job.salary) * 1000, max: parseInt(job.salary) * 1000 } : null,
          postedDate: new Date().toISOString(),
          excerpt: job.description?.substring(0, 240)
        });
      }
    }
    console.log(`[RemoteOK] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[RemoteOK] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 3. WE WORK REMOTELY (RSS) ====================
async function scrapeWeWorkRemotely() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://weworkremotely.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `weworkremotely:${item.guid || Math.random()}`,
        source: "weworkremotely",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[WeWorkRemotely] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[WeWorkRemotely] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 4. WORKING NOMADS (RSS) ====================
async function scrapeWorkingNomads() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://www.workingnomads.com/jobs.rss");
    for (const item of feed.items || []) {
      jobs.push({
        id: `workingnomads:${item.guid || Math.random()}`,
        source: "workingnomads",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[WorkingNomads] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[WorkingNomads] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 5. REMOTE CO (RSS) ====================
async function scrapeRemoteCo() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://remote.co/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `remoteco:${item.guid || Math.random()}`,
        source: "remoteco",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[RemoteCo] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[RemoteCo] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 6. ANGELLIST/STARTUP JOBS (RSS) ====================
async function scrapeAngelList() {
  const jobs = [];
  try {
    // Wellfound/AngelList job RSS
    const feed = await rssParser.parseURL("https://wellfound.com/jobs.rss");
    for (const item of feed.items || []) {
      jobs.push({
        id: `angellist:${item.guid || Math.random()}`,
        source: "angellist",
        company: item.company || "Unknown",
        title: item.title,
        location: item.location || "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[AngelList] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[AngelList] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 7. HN WHO IS HIRING ====================
async function scrapeHackerNews() {
  const jobs = [];
  try {
    // Get latest "Who is hiring?" post
    const searchUrl = "https://hn.algolia.com/api/v1/search?query=who+is+hiring&tags=story&hitsPerPage=1";
    const searchResponse = await axios.get(searchUrl, { timeout: 15000 });
    const objectID = searchResponse.data?.hits?.[0]?.objectID;
    
    if (objectID) {
      const commentsUrl = `https://hn.algolia.com/api/v1/search?tags=comment,story_${objectID}&hitsPerPage=100`;
      const commentsResponse = await axios.get(commentsUrl, { timeout: 15000 });
      const hits = commentsResponse.data?.hits || [];
      
      for (const hit of hits) {
        const text = hit.text || "";
        if (text.toLowerCase().includes("remote") || text.toLowerCase().includes("canada")) {
          jobs.push({
            id: `hackernews:${hit.objectID}`,
            source: "hackernews",
            company: "See posting",
            title: text.split("\n")[0]?.replace(/<[^>]+>/g, "").substring(0, 100) || "Tech Position",
            location: "Remote",
            url: `https://news.ycombinator.com/item?id=${hit.objectID}`,
            employmentType: "full-time",
            salary: null,
            postedDate: new Date(hit.created_at).toISOString(),
            excerpt: text.replace(/<[^>]+>/g, "").substring(0, 240)
          });
        }
      }
    }
    console.log(`[HackerNews] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[HackerNews] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 8. GITHUB JOBS (Positions API) ====================
async function scrapeGitHubJobs() {
  const jobs = [];
  try {
    const response = await axios.get("https://jobs.github.com/positions.json?search=developer", { timeout: 15000 });
    for (const job of response.data || []) {
      jobs.push({
        id: `github:${job.id}`,
        source: "github",
        company: job.company,
        title: job.title,
        location: job.location,
        url: job.url,
        employmentType: job.type || "full-time",
        salary: null,
        postedDate: job.created_at,
        excerpt: job.description?.substring(0, 240)
      });
    }
    console.log(`[GitHub] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[GitHub] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 9. CANADA.CA JOBS (Government) ====================
async function scrapeCanadaCa() {
  const jobs = [];
  try {
    // Canada.ca jobs API endpoint
    const url = "https://www.canada.ca/en/services/jobs/opportunities.html";
    // This requires parsing HTML, skip for now
    console.log(`[CanadaCa] Requires HTML parsing`);
  } catch (e) {
    console.log(`[CanadaCa] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 10. FLEXJOBS (Limited free) ====================
async function scrapeFlexJobs() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://www.flexjobs.com/rss");
    for (const item of feed.items || []) {
      jobs.push({
        id: `flexjobs:${item.guid || Math.random()}`,
        source: "flexjobs",
        company: item.company || "Unknown",
        title: item.title,
        location: item.location || "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[FlexJobs] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[FlexJobs] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 11. JUSTREMOTE ====================
async function scrapeJustRemote() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://justremote.co/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `justremote:${item.guid || Math.random()}`,
        source: "justremote",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[JustRemote] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[JustRemote] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 12. SKIP THE DRIVE ====================
async function scrapeSkipTheDrive() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://www.skipthedrive.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `skipthedrive:${item.guid || Math.random()}`,
        source: "skipthedrive",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[SkipTheDrive] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[SkipTheDrive] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 13. VIRTUAL VOCATIONS ====================
async function scrapeVirtualVocations() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://www.virtualvocations.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `virtualvocations:${item.guid || Math.random()}`,
        source: "virtualvocations",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[VirtualVocations] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[VirtualVocations] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 14. REMOTE LEAF ====================
async function scrapeRemoteLeaf() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://remoteleaf.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `remoteleaf:${item.guid || Math.random()}`,
        source: "remoteleaf",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[RemoteLeaf] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[RemoteLeaf] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 15. DYNAMITE JOBS ====================
async function scrapeDynamiteJobs() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://dynamitejobs.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `dynamitejobs:${item.guid || Math.random()}`,
        source: "dynamitejobs",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[DynamiteJobs] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[DynamiteJobs] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 16. REMOTE QUEUE ====================
async function scrapeRemoteQueue() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://remotequeue.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `remotequeue:${item.guid || Math.random()}`,
        source: "remotequeue",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[RemoteQueue] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[RemoteQueue] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 17. OUTSOURCELY ====================
async function scrapeOutsourcely() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://www.outsourcely.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `outsourcely:${item.guid || Math.random()}`,
        source: "outsourcely",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[Outsourcely] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Outsourcely] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 18. REMOTE4ME ====================
async function scrapeRemote4Me() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://remote4me.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `remote4me:${item.guid || Math.random()}`,
        source: "remote4me",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[Remote4Me] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Remote4Me] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 19. EUROPEAN JOBS (EU Remote Jobs) ====================
async function scrapeEURemote() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://euremotejobs.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `euremote:${item.guid || Math.random()}`,
        source: "euremote",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote (EU)",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[EURemote] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[EURemote] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 20. AUSTRALIAN JOBS (AU Remote Jobs) ====================
async function scrapeAURemote() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://auremotejobs.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `auremote:${item.guid || Math.random()}`,
        source: "auremote",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote (AU)",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[AURemote] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[AURemote] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 21. REMOTE HUNT ====================
async function scrapeRemoteHunt() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://remotehunt.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `remotehunt:${item.guid || Math.random()}`,
        source: "remotehunt",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[RemoteHunt] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[RemoteHunt] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 22. PANGIAN ====================
async function scrapePangian() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://pangian.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `pangian:${item.guid || Math.random()}`,
        source: "pangian",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[Pangian] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Pangian] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 23. REMOTIVE ====================
async function scrapeRemotive() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://remotive.com/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `remotive:${item.guid || Math.random()}`,
        source: "remotive",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[Remotive] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Remotive] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== 24. HIMALAYAS (Remote Jobs) ====================
async function scrapeHimalayas() {
  const jobs = [];
  try {
    const feed = await rssParser.parseURL("https://himalayas.app/feed");
    for (const item of feed.items || []) {
      jobs.push({
        id: `himalayas:${item.guid || Math.random()}`,
        source: "himalayas",
        company: item.company || "Unknown",
        title: item.title,
        location: "Remote",
        url: item.link,
        employmentType: "full-time",
        salary: null,
        postedDate: item.pubDate ? new Date(item.pubDate).toISOString() : new Date().toISOString(),
        excerpt: item.contentSnippet?.substring(0, 240)
      });
    }
    console.log(`[Himalayas] ${jobs.length} jobs`);
  } catch (e) {
    console.log(`[Himalayas] Error: ${e.message}`);
  }
  return jobs;
}

// ==================== MAIN ====================
async function main() {
  console.log("🚀 PROOF OF CONCEPT - 24 Free Job Sources\n");
  
  const allJobs = [];
  const seen = new Set();
  const results = {};
  
  // Test all 24 sources
  const scrapers = [
    { name: "Jobicy", fn: scrapeJobicy },
    { name: "RemoteOK", fn: scrapeRemoteOK },
    { name: "WeWorkRemotely", fn: scrapeWeWorkRemotely },
    { name: "WorkingNomads", fn: scrapeWorkingNomads },
    { name: "RemoteCo", fn: scrapeRemoteCo },
    { name: "AngelList", fn: scrapeAngelList },
    { name: "HackerNews", fn: scrapeHackerNews },
    { name: "GitHubJobs", fn: scrapeGitHubJobs },
    { name: "FlexJobs", fn: scrapeFlexJobs },
    { name: "JustRemote", fn: scrapeJustRemote },
    { name: "SkipTheDrive", fn: scrapeSkipTheDrive },
    { name: "VirtualVocations", fn: scrapeVirtualVocations },
    { name: "RemoteLeaf", fn: scrapeRemoteLeaf },
    { name: "DynamiteJobs", fn: scrapeDynamiteJobs },
    { name: "RemoteQueue", fn: scrapeRemoteQueue },
    { name: "Outsourcely", fn: scrapeOutsourcely },
    { name: "Remote4Me", fn: scrapeRemote4Me },
    { name: "EURemote", fn: scrapeEURemote },
    { name: "AURemote", fn: scrapeAURemote },
    { name: "RemoteHunt", fn: scrapeRemoteHunt },
    { name: "Pangian", fn: scrapePangian },
    { name: "Remotive", fn: scrapeRemotive },
    { name: "Himalayas", fn: scrapeHimalayas }
  ];
  
  for (const { name, fn } of scrapers) {
    const jobs = await fn();
    results[name] = jobs.length;
    for (const job of jobs) {
      if (!seen.has(job.id)) {
        seen.add(job.id);
        allJobs.push(job);
      }
    }
  }
  
  console.log(`\n========================================`);
  console.log(`PROOF OF CONCEPT COMPLETE`);
  console.log(`========================================`);
  console.log("Results by source:");
  for (const [name, count] of Object.entries(results)) {
    console.log(`  ${name}: ${count} jobs`);
  }
  console.log(`\nTOTAL UNIQUE JOBS: ${allJobs.length}`);
  console.log(`========================================\n`);
  
  // Save results
  fs.writeFileSync("poc_results.json", JSON.stringify({
    timestamp: new Date().toISOString(),
    totalJobs: allJobs.length,
    bySource: results,
    jobs: allJobs.slice(0, 100) // Save first 100 for inspection
  }, null, 2));
  
  console.log("✅ Results saved to poc_results.json");
}

main().catch(e => {
  console.error("Fatal error:", e);
  process.exit(1);
});
