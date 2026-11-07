#!/usr/bin/env node
/**
 * Make jobs.json a superset of the curated README tables.
 *
 * The repo has two consumers reading two different files:
 *   - public/index.html (the live page) renders public/jobs-data.json,
 *     rebuilt from README.md by tools/build_site.py
 *   - the API (/jobs.json) and the hourly scanner use jobs.json, which only
 *     ever contains postings the automated sources returned
 *
 * Curated and inbox-submitted roles therefore reached the page but never the
 * feed — e.g. Ateko / FX Innovation "ServiceNow Architect (526327)".
 *
 * This script appends every README row that is missing from jobs.json (matched
 * on normalised URL first, then title+company), and drops rows without a posted
 * date, which cannot be sorted or date-windowed.
 *
 * Usage: node scripts/sync_readme_to_jobs.mjs [--dry-run]
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const DRY = process.argv.slice(2).includes("--dry-run");
const MAX_AGE_DAYS = 31;
const NOW = new Date();
const NOW_ISO = NOW.toISOString();

const TARGETS = [
  "jobs.json",
  "public/jobs.json",
  "public/gotjob/jobs.json",
  "public/findjobs/jobs.json",
];

const SECTIONS = {
  "servicenow jobs": "servicenow",
  "salesforce jobs": "salesforce",
  "other jobs": "other",
};

function cleanUrl(raw) {
  try {
    const u = new URL(raw);
    for (const k of ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term", "gh_src"]) {
      u.searchParams.delete(k);
    }
    u.hash = "";
    return u.toString();
  } catch {
    return String(raw || "").trim();
  }
}

/**
 * Aggregator search/category pages are not postings. Exa answers "data analyst
 * toronto" with a category URL, so harvests used to land LinkedIn /jobs/<keywords>-jobs
 * and Robert Half /ca/en/jobs/<city> rows in jobs.json where the page rendered them
 * as if they were roles. Kept in sync with is_listing_url() in tools/jobs_consolidate.py.
 */
const LISTING_RULES = [
  [/(^|\.)linkedin\.com$/, /^\/jobs\/(?!view\/)[a-z0-9%-]*-jobs/],
  [/(^|\.)glassdoor\.[a-z.]+$/, /-jobs-srch_|srch_|\/job\/jobs\.htm/i],
  [/(^|\.)wellfound\.com$/, /^\/role\//],
  // Robert Half category pages; a posting is /ca/en/jobs/detail/<id>/<slug>.
  [/(^|\.)roberthalf\.[a-z.]+$/, /^\/[a-z]{2}\/[a-z]{2}\/jobs\/(?!detail\/)[a-z][a-z0-9-]*(?:\/[a-z0-9-]+)?\/?$/],
  [/(^|\.)randstad\.[a-z.]+$/, /^\/jobs\/q-/],
  [/(^|\.)eluta\.ca$/, /-jobs-in-/i],
  [/(^|\.)jobbank\.gc\.ca$/, /^\/marketreport\//],
  [/(^|\.)ziprecruiter\.com$/, /^\/Jobs\//],
  [/(^|\.)whatjobs\.com$/, /^\/jobs\/[a-z0-9-]+\/[a-z0-9-]+\/?$/],
  [/(^|\.)adzuna\.[a-z.]+$/, /^\/[a-z0-9-]+\/?$/],
  [/(^|\.)indeed\.[a-z.]+$/, /^\/q-/],
];
const LISTING_QUERY = /[?&](q|query|search|keywords?|k|ss|term|what|jobtitle)=/i;
// Slash-delimited only: "/jobsearch/jobposting/<id>" (Job Bank) and
// "/jobsearch/viewjob/<token>" (Workopolis) are postings, not searches.
const LISTING_PATH = /\/(jobs?|careers?)\/(search|results|browse)(\/|$)/i;

function isListingUrl(raw) {
  let u;
  try {
    u = new URL(raw);
  } catch {
    return false;
  }
  const host = u.hostname.toLowerCase().replace(/^www\./, "");
  if (LISTING_QUERY.test(u.search) || LISTING_PATH.test(u.pathname)) return true;
  return LISTING_RULES.some(([h, p]) => h.test(host) && p.test(u.pathname));
}

function urlKey(raw) {
  try {
    const u = new URL(raw);
    return `${u.hostname.replace(/^www\./, "")}${u.pathname}`.toLowerCase().replace(/\/$/, "");
  } catch {
    return String(raw || "").toLowerCase();
  }
}

function identKey(job) {
  return `${(job.company || "").toLowerCase().trim()}|${(job.title || "")
    .toLowerCase()
    .replace(/\s+/g, " ")
    .trim()}`;
}

/**
 * Salary stated by the posting, as {min,max,currency}. Purely extractive: only
 * numbers the text actually contains, and only annual-scale figures, so an
 * hourly rate can never masquerade as a 25-dollar salary.
 */
function inferSalary(text) {
  const t = String(text || "").replace(/\u00a0/g, " ").replace(/\s+/g, " ");
  // A bare number range ("25,000 to 30,000") is as likely to be square footage,
  // headcount or a job id, so the text must also signal money.
  if (!/\$|\bcad\b|\busd\b|salary|compensation|\bpay\b|annually|per year|per annum/i.test(t)) return null;
  const num = (s) => Number(s.replace(/,/g, ""));
  const pair = t.match(
    /\$?\s?(\d{2,3}(?:,\d{3})+|\d{5,6})(?:\.\d+)?\s*(?:-|–|—|to|and)\s*\$?\s?(\d{2,3}(?:,\d{3})+|\d{5,6})(?:\.\d+)?(?:[^\d]{0,24}(?:CAD|USD))?/i
  );
  if (pair) {
    const min = Math.min(num(pair[1]), num(pair[2]));
    const max = Math.max(num(pair[1]), num(pair[2]));
    if (min >= 20000 && max <= 400000) {
      const currency = /usd|\bus\$/i.test(t) ? "USD" : "CAD";
      return { min, max, currency };
    }
  }
  const single = t.match(
    /\$\s?(\d{2,3}(?:,\d{3})+|\d{5,6})\s?(?:CAD|USD)?\s*(?:per year|annually|annual|\/\s?year|a year|salary)/i
  );
  if (single) {
    const v = num(single[1]);
    if (v >= 20000 && v <= 400000) {
      return { min: v, max: v, currency: /usd/i.test(t) ? "USD" : "CAD" };
    }
  }
  return null;
}

/**
 * Remote / hybrid / onsite from explicit wording only. Location wins when it
 * says something, then the title, then the excerpt.
 */
function inferArrangement(title, location, excerpt) {
  const loc = String(location || "").toLowerCase();
  const hay = `${title || ""} ${excerpt || ""}`.toLowerCase();
  if (/remote|t[ée]l[ée]travail|work from home|work-from-home|telework|travail [àa] distance/.test(loc)) return "remote";
  if (/hybrid|hybride/.test(loc)) return "hybrid";
  // "fully on-site, no remote option" must not read as remote.
  const negated = /(?:not|no|non)[- ]?(?:a )?(?:fully )?(?:remote|hybrid)|remote (?:is )?not (?:available|offered|possible)/.test(hay);
  if (negated) return /on-?site|in[- ]office/.test(hay) ? "onsite" : null;
  if (/hybrid|hybride|\d\s*days? (?:a|per) week in (?:the )?office|days in office/.test(hay)) return "hybrid";
  if (/fully remote|100% remote|remote[- ]first|remote position|remote role|\bremote\b|t[ée]l[ée]travail/.test(hay)) return "remote";
  if (/on-?site|in[- ]office|in person only/.test(hay)) return "onsite";
  return null;
}

const AGGREGATOR_HOST = /(^|\.)(adzuna\.|linkedin\.|indeed\.|glassdoor\.|ziprecruiter\.|eluta\.ca|talent\.com|whatjobs\.|workopolis\.|jobbank\.gc\.ca|jobs\.ca|jobsca\.)/i;

function cityOf(location) {
  const raw = String(location || "").toLowerCase();
  if (!raw.trim()) return "";
  const first = raw.split(",")[0];
  return first.replace(/[^a-z0-9 ]/g, " ").replace(/\s+/g, " ").trim();
}

/**
 * One row per role-and-city. The feed used to carry the same requisition from
 * Adzuna + LinkedIn + the employer board as separate entries (116 company+title
 * clusters, 177 excess rows on 2026-11-04), which inflated every count and made
 * the API disagree with the page, where build_site.py already clusters them.
 * The dropped mirrors are kept on the surviving row as `alternates`, the same
 * shape the cards use, so nothing is lost.
 *
 * Multi-city reposts (one role advertised per province) are deliberately NOT
 * collapsed: different city means a different listing on the board.
 */
function dedupeRows(rows) {
  const buckets = new Map();
  for (const row of rows) {
    const key = `${(row.company || "").toLowerCase().trim()}|${(row.title || "")
      .toLowerCase()
      .replace(/\s+/g, " ")
      .trim()}|${cityOf(row.location)}`;
    const bucket = buckets.get(key);
    if (bucket) bucket.push(row);
    else buckets.set(key, [row]);
  }

  const rank = (r) => [
    AGGREGATOR_HOST.test((r.url || "").replace(/^https?:\/\/(www\.)?/, "")) ? 0 : 1,
    r.postedDate || "",
    (r.location || "").length + (r.company || "").length,
  ];
  const out = [];
  let collapsed = 0;
  for (const members of buckets.values()) {
    if (members.length === 1) {
      out.push(members[0]);
      continue;
    }
    members.sort((a, b) => {
      const ra = rank(a);
      const rb = rank(b);
      return ra[0] !== rb[0] ? rb[0] - ra[0] : ra[1] !== rb[1] ? (ra[1] < rb[1] ? 1 : -1) : rb[2] - ra[2];
    });
    const [primary, ...dups] = members;
    const seen = new Set([(primary.url || "").split("?")[0].replace(/\/$/, "").toLowerCase()]);
    primary.alternates = primary.alternates || [];
    for (const dup of dups) {
      collapsed += 1;
      const u = (dup.url || "").split("?")[0].replace(/\/$/, "").toLowerCase();
      if (!u || seen.has(u) || primary.alternates.length >= 6) continue;
      seen.add(u);
      primary.alternates.push({ source: dup.source, url: dup.url, label: dup.source });
      if ((dup.postedDate || "") > (primary.postedDate || "")) primary.postedDate = dup.postedDate;
    }
    out.push(primary);
  }
  return { rows: out, collapsed };
}

/** Fill blank salary / arrangement fields from the row's own text. */
function enrichRows(rows) {
  let salaryFilled = 0;
  let arrangementFilled = 0;
  for (const row of rows) {
    const hay = `${row.title || ""} ${row.excerpt || ""}`;
    if (!row.salary) {
      const salary = inferSalary(hay);
      if (salary) {
        row.salary = salary;
        salaryFilled += 1;
      }
    }
    if (!row.workArrangement || row.workArrangement === "unknown") {
      const arrangement = inferArrangement(row.title, row.location, row.excerpt);
      if (arrangement) {
        row.workArrangement = arrangement;
        arrangementFilled += 1;
      }
    }
  }
  return { salaryFilled, arrangementFilled };
}

function detectTags(title, excerpt) {
  const hay = `${title} ${excerpt}`;
  const tags = [];
  if (/\bservice\s?now\b/i.test(hay)) tags.push("servicenow");
  if (/\bsalesforce\b|\bapex\b|\blwc\b|\bsoql\b|\bvisualforce\b|\bforce\.com\b/i.test(hay)) tags.push("salesforce");
  if (/\bitsm\b|\bitil\b/i.test(hay)) tags.push("it-reporting");
  if (/\bitam\b|\bcmdb\b|configuration management/i.test(hay)) tags.push("itam");
  return tags;
}

/**
 * Parse the three README job tables. Rows look like:
 *   | 2026-11-02 | [ServiceNow Architect (526327)](https://host/jobs/526327) | Ateko | Canada; remote | note |
 */
function parseReadme(text) {
  const rows = [];
  let family = null;
  for (const line of text.split("\n")) {
    const heading = line.match(/^###\s+(.+?)\s*$/);
    if (heading) {
      // Section headings carry a live count, e.g. "### ServiceNow jobs (150)".
      const name = heading[1].toLowerCase().replace(/\s*\(\d+[^)]*\)\s*$/, "").trim();
      family = SECTIONS[name] || null;
      continue;
    }
    if (/^##\s/.test(line)) {
      family = null;
      continue;
    }
    if (!family || !line.startsWith("|")) continue;

    const cells = line.split("|").map((c) => c.trim());
    // split() yields an empty first/last cell for a well-formed table row
    const body = cells.slice(1, cells.length - 1);
    if (body.length < 3) continue;

    const [posted, titleCell, company = "", location = "", ...rest] = body;
    if (!/^\d{4}-\d{2}-\d{2}$/.test(posted)) continue;

    const titleMatch = titleCell.match(/^\[(.*?)\]\((https?:\/\/[^)\s]+)\)$/);
    if (!titleMatch) continue;

    const title = titleMatch[1].replace(/\\\//g, "/").trim();
    const url = cleanUrl(titleMatch[2]);
    if (!title || !url.startsWith("http")) continue;

    const note = rest.join(" | ").replace(/\\\//g, "/").slice(0, 320);
    const tags = detectTags(title, note);
    if (!tags.includes(family) && family !== "other") tags.unshift(family);

    rows.push({
      id: `readme:${urlKey(url)}`,
      source: "readme",
      company: company.replace(/\\\//g, "/").trim() || "Unknown",
      title,
      location: location.replace(/\\\//g, "/").trim() || "Not specified",
      url,
      employmentType: /contract/i.test(note) ? "contract" : "unknown",
      salary: null,
      postedDate: `${posted}T12:00:00.000Z`,
      scrapedAt: NOW_ISO,
      excerpt: note,
      workArrangement: /remote|t[ée]l[ée]travail/i.test(location)
        ? "remote"
        : /hybrid/i.test(location)
          ? "hybrid"
          : "unknown",
      tags: tags.length ? tags : [family],
    });
  }
  return rows;
}

function main() {
  const readmePath = path.join(ROOT, "README.md");
  const jobsPath = path.join(ROOT, "jobs.json");
  if (!fs.existsSync(readmePath) || !fs.existsSync(jobsPath)) {
    console.error("sync: README.md or jobs.json missing");
    process.exit(1);
  }

  const readmeRows = parseReadme(fs.readFileSync(readmePath, "utf8"));
  const payload = JSON.parse(fs.readFileSync(jobsPath, "utf8"));
  const existing = Array.isArray(payload) ? payload : payload.jobs || [];

  const byUrl = new Map();
  const byIdent = new Map();
  let undated = 0;
  let listingDropped = 0;
  for (const job of existing) {
    if (!job?.postedDate) {
      undated += 1;
      continue;
    }
    if (isListingUrl(job.url)) {
      listingDropped += 1;
      continue;
    }
    byUrl.set(urlKey(job.url), job);
    byIdent.set(identKey(job), job);
  }

  const added = [];
  let duplicated = 0;
  let listingSkipped = 0;
  for (const row of readmeRows) {
    if (isListingUrl(row.url)) {
      listingSkipped += 1;
      continue;
    }
    if (byUrl.has(urlKey(row.url)) || byIdent.has(identKey(row))) {
      duplicated += 1;
      continue;
    }
    const ageDays = (NOW - new Date(row.postedDate)) / 864e5;
    if (ageDays > MAX_AGE_DAYS) continue;
    added.push(row);
    byUrl.set(urlKey(row.url), row);
    byIdent.set(identKey(row), row);
  }

  const enriched = enrichRows([...byUrl.values()]);
  const deduped = dedupeRows([...byUrl.values()]);

  const all = [...deduped.rows, ...added.filter((r) => !byUrl.has(urlKey(r.url)))];
  // byUrl already holds added rows (set above); dedupe by object identity
  const merged = [...new Set(all)].sort((a, b) =>
    a.postedDate < b.postedDate ? 1 : a.postedDate > b.postedDate ? -1 : 0
  );

  console.log(
    `[sync] readme rows=${readmeRows.length} already-in-feed=${duplicated} added=${added.length} ` +
      `undated-dropped=${undated} listing-pages-skipped=${listingSkipped} ` +
<<<<<<< HEAD
      `listing-pages-purged=${listingDropped} salary-filled=${enriched.salaryFilled} ` +
      `arrangement-filled=${enriched.arrangementFilled} dupes-collapsed=${deduped.collapsed} total=${merged.length}`
=======
      `listing-pages-purged=${listingDropped} total=${merged.length}`
>>>>>>> 3e1b8194b482405db0e670c155744c13e74fdc05
  );

  if (DRY) {
    for (const r of added.slice(0, 15)) {
      console.log(`  + ${r.postedDate.slice(0, 10)} | ${r.tags[0]} | ${r.title} | ${r.company}`);
    }
    return;
  }

  const next = Array.isArray(payload)
    ? merged
    : { ...payload, meta: { ...(payload.meta || {}), total: merged.length }, jobs: merged };
  const json = JSON.stringify(next, null, 2);
  for (const rel of TARGETS) {
    const target = path.join(ROOT, rel);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, json);
    console.log(`[sync] wrote ${rel}`);
  }
}

main();
