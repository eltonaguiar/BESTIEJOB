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
  for (const job of existing) {
    if (!job?.postedDate) {
      undated += 1;
      continue;
    }
    byUrl.set(urlKey(job.url), job);
    byIdent.set(identKey(job), job);
  }

  const added = [];
  let duplicated = 0;
  for (const row of readmeRows) {
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

  const all = [...[...byUrl.values()], ...added.filter((r) => !byUrl.has(urlKey(r.url)))];
  // byUrl already holds added rows (set above); dedupe by object identity
  const merged = [...new Set(all)].sort((a, b) =>
    a.postedDate < b.postedDate ? 1 : a.postedDate > b.postedDate ? -1 : 0
  );

  console.log(
    `[sync] readme rows=${readmeRows.length} already-in-feed=${duplicated} added=${added.length} ` +
      `undated-dropped=${undated} total=${merged.length}`
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
