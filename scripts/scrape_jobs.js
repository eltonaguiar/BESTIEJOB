import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { scrapeIndeedJobs, scrapeIndeedMultiKeyword } from "../scrapers/indeed_scraper.js";
import { scrapeLinkedInJobs, scrapeLinkedInMultiKeyword } from "../scrapers/linkedin_scraper.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.join(__dirname, "..");

// Default tech keywords to search for
const DEFAULT_KEYWORDS = [
  "ServiceNow developer",
  "ServiceNow",
  "VBA developer",
  "VBA",
  "Alteryx developer",
  "Alteryx",
  "full stack developer",
  "full stack",
  "software engineer",
  "data analyst",
  "DevOps engineer",
  "cloud architect",
  "AWS engineer",
  "Python developer",
  "JavaScript developer",
  "React developer",
  "Node.js developer",
  "Java developer",
  ".NET developer",
  "SQL developer",
  "Power BI",
  "Tableau",
  "machine learning",
  "data scientist"
];

function normalizeText(value) {
  return (value ?? "").toString().trim();
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (next && !next.startsWith("--")) {
      args[key] = next;
      i += 1;
    } else {
      args[key] = true;
    }
  }
  return args;
}

function parseDateFilter(value) {
  // Convert various inputs to standard date filter
  if (!value) return "week";
  const v = value.toLowerCase();
  if (v === "24h" || v === "day" || v === "1d" || v === "1") return "24h";
  if (v === "3d" || v === "3") return "3d";
  if (v === "7d" || v === "week" || v === "7") return "week";
  if (v === "14d" || v === "14") return "14d";
  if (v === "30d" || v === "month" || v === "30") return "month";
  if (v === "any" || v === "all") return "any";
  return "week";
}

function parseSinceFilter({ sinceMinutes, sinceHours, sinceDays, sinceIso }) {
  const minutes = Number(sinceMinutes ?? "");
  const hours = Number(sinceHours ?? "");
  const days = Number(sinceDays ?? "");
  const iso = normalizeText(sinceIso);

  if (iso) {
    const d = new Date(iso);
    return Number.isNaN(d.getTime()) ? null : d;
  }

  const totalMinutes =
    (Number.isFinite(minutes) ? minutes : 0) +
    (Number.isFinite(hours) ? hours * 60 : 0) +
    (Number.isFinite(days) ? days * 24 * 60 : 0);

  if (!totalMinutes) return null;
  return new Date(Date.now() - totalMinutes * 60 * 1000);
}

function filterBySince(jobs, sinceDate) {
  if (!sinceDate) return jobs;
  return jobs.filter((job) => {
    if (!job.postedDate) return true; // Keep jobs without date (benefit of doubt)
    const posted = new Date(job.postedDate);
    return !Number.isNaN(posted.getTime()) && posted >= sinceDate;
  });
}

function mergeUnique(jobs) {
  const seen = new Set();
  return jobs.filter((job) => {
    const key = job.url || job.id || job.title;
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

async function scrapeAll({ keyword, keywords, location, dateFilter, jobType, multiKeyword }) {
  const results = [];
  const sourceErrors = [];
  
  if (multiKeyword) {
    // Multi-keyword mode: search for many keywords
    const keywordList = keywords || DEFAULT_KEYWORDS;
    console.log(`\n🔍 Multi-keyword scrape mode: ${keywordList.length} keywords`);
    console.log(`📍 Location: ${location}`);
    console.log(`📅 Date filter: ${dateFilter}`);
    console.log(`💼 Job type: ${jobType || "any"}\n`);
    
    // Indeed multi-keyword
    try {
      console.log("--- Indeed Multi-Keyword Scrape ---");
      const indeedJobs = await scrapeIndeedMultiKeyword({
        keywords: keywordList,
        location,
        dateFilter,
        jobType
      });
      results.push(...indeedJobs);
      console.log(`✅ Indeed: ${indeedJobs.length} total jobs\n`);
    } catch (error) {
      console.error("❌ Indeed multi-keyword failed:", error.message);
      sourceErrors.push({ source: "indeed", error: error.message });
    }
    
    // LinkedIn multi-keyword
    try {
      console.log("--- LinkedIn Multi-Keyword Scrape ---");
      const linkedinJobs = await scrapeLinkedInMultiKeyword({
        keywords: keywordList,
        location,
        dateFilter,
        jobType
      });
      results.push(...linkedinJobs);
      console.log(`✅ LinkedIn: ${linkedinJobs.length} total jobs\n`);
    } catch (error) {
      console.error("❌ LinkedIn multi-keyword failed:", error.message);
      sourceErrors.push({ source: "linkedin", error: error.message });
    }
  } else {
    // Single keyword mode
    console.log(`\n🔍 Single keyword scrape: "${keyword}"`);
    console.log(`📍 Location: ${location}`);
    console.log(`📅 Date filter: ${dateFilter}\n`);
    
    const sources = [
      { 
        name: "indeed", 
        run: () => scrapeIndeedJobs({ keyword, location, dateFilter, jobType }) 
      },
      { 
        name: "linkedin", 
        run: () => scrapeLinkedInJobs({ keyword, location, dateFilter, jobType }) 
      }
    ];

    const settled = await Promise.allSettled(sources.map((s) => s.run()));
    
    settled.forEach((result, idx) => {
      if (result.status === "fulfilled") {
        results.push(...result.value);
        console.log(`✅ ${sources[idx].name}: ${result.value.length} jobs`);
      } else {
        sourceErrors.push({ 
          source: sources[idx].name, 
          error: String(result.reason?.message || result.reason) 
        });
        console.error(`❌ ${sources[idx].name} failed:`, result.reason?.message);
      }
    });
  }

  return { jobs: mergeUnique(results), sourceErrors };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  
  // Parse keywords (can be comma-separated list)
  const keywordsArg = args.keywords || process.env.SCRAPE_KEYWORDS || "";
  const keywords = keywordsArg.includes(",") 
    ? keywordsArg.split(",").map(k => k.trim()).filter(Boolean)
    : null;
  const keyword = normalizeText(keywordsArg.split(",")[0] || "ServiceNow developer");
  
  // Other options
  const location = normalizeText(args.location || process.env.SCRAPE_LOCATION || "Toronto, ON");
  const output = args.output || process.env.SCRAPE_OUTPUT || path.join(ROOT_DIR, "jobs.json");
  const dateFilter = parseDateFilter(args.dateFilter || args.date || process.env.DATE_FILTER);
  const jobType = args.jobType || args.type || process.env.JOB_TYPE || null;
  const multiKeyword = args.multi || args.multiKeyword || process.env.MULTI_KEYWORD === "true";

  // Legacy since filter (also supported)
  const sinceDate = parseSinceFilter({
    sinceMinutes: args.sinceMinutes || process.env.SINCE_MINUTES,
    sinceHours: args.sinceHours || process.env.SINCE_HOURS,
    sinceDays: args.sinceDays || process.env.SINCE_DAYS,
    sinceIso: args.sinceIso || process.env.SINCE_ISO
  });

  console.log("╔══════════════════════════════════════════╗");
  console.log("║       BESTIEJOB - Job Scraper v2.0       ║");
  console.log("╚══════════════════════════════════════════╝");
  
  const { jobs, sourceErrors } = await scrapeAll({ 
    keyword,
    keywords: keywords || (multiKeyword ? DEFAULT_KEYWORDS : null),
    location, 
    dateFilter,
    jobType,
    multiKeyword: multiKeyword || (keywords && keywords.length > 1)
  });
  
  // Apply post-filter if sinceDate specified
  const filtered = filterBySince(jobs, sinceDate);

  const payload = {
    meta: {
      keyword: multiKeyword ? "multi" : keyword,
      keywords: multiKeyword ? (keywords || DEFAULT_KEYWORDS) : [keyword],
      location,
      dateFilter,
      jobType,
      sinceDate: sinceDate ? sinceDate.toISOString() : null,
      sourceErrors,
      totalFetched: jobs.length,
      totalMatched: filtered.length,
      scrapedAt: new Date().toISOString()
    },
    jobs: filtered
  };

  // Write to output file
  fs.writeFileSync(output, JSON.stringify(payload, null, 2));
  
  // Also copy to public directories
  const publicOutputs = [
    path.join(ROOT_DIR, "public", "jobs.json"),
    path.join(ROOT_DIR, "public", "findjobs", "jobs.json")
  ];
  
  for (const publicOutput of publicOutputs) {
    try {
      fs.writeFileSync(publicOutput, JSON.stringify(payload, null, 2));
    } catch (e) {
      console.warn(`Could not write to ${publicOutput}: ${e.message}`);
    }
  }
  
  console.log("\n╔══════════════════════════════════════════╗");
  console.log(`║ ✅ Saved ${filtered.length} jobs to ${path.basename(output)}`);
  console.log("╚══════════════════════════════════════════╝");
  
  if (sourceErrors.length > 0) {
    console.log("\n⚠️  Source errors:");
    sourceErrors.forEach(e => console.log(`   - ${e.source}: ${e.error}`));
  }
}

main().catch((error) => {
  console.error("Scrape failed:", error);
  process.exit(1);
});
