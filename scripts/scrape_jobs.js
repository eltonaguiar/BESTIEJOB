import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { scrapeIndeedJobs } from "../scrapers/indeed_scraper.js";
import { scrapeLinkedInJobs } from "../scrapers/linkedin_scraper.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT_DIR = path.join(__dirname, "..");

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
    if (!job.postedDate) return false;
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

async function scrapeAll({ keyword, location }) {
  const sources = [
    { name: "indeed", run: () => scrapeIndeedJobs({ keyword, location }) },
    { name: "linkedin", run: () => scrapeLinkedInJobs(keyword, location) }
  ];

  const settled = await Promise.allSettled(sources.map((s) => s.run()));
  const jobs = settled.flatMap((r) => (r.status === "fulfilled" ? r.value : []));
  const sourceErrors = settled
    .map((r, idx) => ({ r, s: sources[idx] }))
    .filter(({ r }) => r.status === "rejected")
    .map(({ r, s }) => ({ source: s.name, error: String(r.reason?.message || r.reason) }));

  return { jobs: mergeUnique(jobs), sourceErrors };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const keyword = normalizeText(args.keywords || process.env.SCRAPE_KEYWORDS || "vba");
  const location = normalizeText(args.location || process.env.SCRAPE_LOCATION || "Toronto, ON");
  const output = args.output || process.env.SCRAPE_OUTPUT || path.join(ROOT_DIR, "jobs.json");

  const sinceDate = parseSinceFilter({
    sinceMinutes: args.sinceMinutes || process.env.SINCE_MINUTES,
    sinceHours: args.sinceHours || process.env.SINCE_HOURS,
    sinceDays: args.sinceDays || process.env.SINCE_DAYS,
    sinceIso: args.sinceIso || process.env.SINCE_ISO
  });

  const { jobs, sourceErrors } = await scrapeAll({ keyword, location });
  const filtered = filterBySince(jobs, sinceDate);

  const payload = {
    meta: {
      keyword,
      location,
      sinceDate: sinceDate ? sinceDate.toISOString() : null,
      sourceErrors,
      totalFetched: jobs.length,
      totalMatched: filtered.length
    },
    jobs: filtered
  };

  fs.writeFileSync(output, JSON.stringify(payload, null, 2));
  console.log(`Saved ${filtered.length} jobs to ${output}`);
}

main().catch((error) => {
  console.error("Scrape failed:", error);
  process.exit(1);
});
