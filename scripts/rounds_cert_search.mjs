#!/usr/bin/env node
/**
 * Rounds 1-5: Expanded Adzuna targeted cert search
 * Keywords: CSA, CAD, Platform Developer I, Platform Administrator I, JavaScript Developer I
 * Locations: Toronto, Mississauga, Markham, Etobicoke, Ottawa, Remote, Canada
 * Max days old: 14 (past 2 weeks)
 */

import axios from "axios";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, "..");

const ADZUNA_APP_ID = "54ce986e";
const ADZUNA_API_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

const ROUND_KEYWORDS = [
  // Round 1: ServiceNow CSA
  "ServiceNow CSA", "Certified System Administrator ServiceNow", "CSA ServiceNow",
  // Round 2: ServiceNow CAD
  "ServiceNow CAD", "Certified Application Developer ServiceNow", "CAD ServiceNow",
  // Round 3: Salesforce Platform Developer I
  "Salesforce Platform Developer I", "Salesforce Platform Developer 1", "Salesforce Certified Platform Developer",
  // Round 4: Salesforce Platform Administrator I
  "Salesforce Platform Administrator I", "Salesforce Platform Administrator 1", "Salesforce Certified Platform Administrator",
  // Round 5: Salesforce JavaScript Developer I
  "Salesforce JavaScript Developer I", "Salesforce JavaScript Developer 1", "Salesforce Certified JavaScript Developer",
];

const ROUND_LOCATIONS = [
  "Toronto", "Mississauga", "Markham", "Etobicoke", "Ottawa", "Remote", "Canada", "Vaughan", "Brampton"
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function fetchAdzunaJobs(keyword, location, page = 1, resultsPerPage = 50, maxDaysOld = 14) {
  const url = `https://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${ADZUNA_APP_ID}&app_key=${ADZUNA_API_KEY}&results_per_page=${resultsPerPage}&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&content-type=application/json&max_days_old=${maxDaysOld}&sort_by=date`;
  try {
    const response = await axios.get(url, { timeout: 30000, headers: { "Accept": "application/json", "User-Agent": "Mozilla/5.0" } });
    return response.data;
  } catch (e) { return { results: [], count: 0, error: e.message }; }
}

function classifyJob(title, excerpt, keyword) {
  const text = `${title} ${excerpt}`.toLowerCase();
  const isServiceNow = /servicenow|service now/.test(text);
  const isSalesforce = /salesforce/.test(text);
  const hasCSA = /csa\b|certified system admin/.test(text);
  const hasCAD = /cad\b|certified application developer/.test(text);
  const hasPD1 = /platform developer\s*(i|1)\b/.test(text);
  const hasPA1 = /platform administrator\s*(i|1)\b|platform admin\s*(i|1)\b/.test(text);
  const hasJSDev1 = /javascript developer\s*(i|1)\b/.test(text);
  return { isServiceNow, isSalesforce, hasCSA, hasCAD, hasPD1, hasPA1, hasJSDev1 };
}

async function main() {
  const existingPath = path.join(ROOT, "jobs.json");
  let existingData = { meta: {}, jobs: [] };
  try { existingData = JSON.parse(fs.readFileSync(existingPath, "utf-8")); } catch {}
  const existingIds = new Set(existingData.jobs.map(j => j.id));
  const seen = new Set(existingIds);
  const allNewJobs = [];
  let totalApiCalls = 0;

  const today = new Date().toISOString().slice(0, 10);
  const twoWeeksAgo = new Date(Date.now() - 14 * 86400000).toISOString().slice(0, 10);

  for (let r = 0; r < ROUND_KEYWORDS.length; r++) {
    const keyword = ROUND_KEYWORDS[r];
    let keywordJobs = 0;

    for (const location of ROUND_LOCATIONS) {
      const result = await fetchAdzunaJobs(keyword, location, 1, 50, 14);
      totalApiCalls++;
      if (result.error) continue;

      let added = 0;
      for (const job of result.results || []) {
        const id = `adzuna:${job.id}`;
        if (!seen.has(id)) {
          const classification = classifyJob(job.title, job.description || "", keyword);
          const salaryMin = job.salary_min ? Math.round(job.salary_min) : null;
          const salaryMax = job.salary_max ? Math.round(job.salary_max) : null;
          const newJob = {
            id, source: "adzuna",
            company: job.company?.display_name || "Unknown",
            title: job.title,
            location: job.location?.display_name || `${location}, Canada`,
            url: job.redirect_url,
            employmentType: job.contract_time === "full_time" ? "full-time" : job.contract_time || "full-time",
            salary: salaryMin && salaryMax ? { min: salaryMin, max: salaryMax } : null,
            postedDate: job.created ? new Date(job.created).toISOString() : new Date().toISOString(),
            excerpt: job.description?.substring(0, 400)?.replace(/<[^>]*>/g, '') || job.title,
            category: job.category?.label || "Technology",
            scrapedAt: new Date().toISOString(),
            matchedKeyword: keyword,
            classification,
            searchRound: `cert-round-${Math.floor(r/3) + 1}`
          };
          seen.add(id);
          allNewJobs.push(newJob);
          keywordJobs++;
          added++;
        }
      }
      if (result.count > 0 && added > 0) {
        console.log(`  [${keyword} @ ${location}] Found ${result.count}, added ${added} new`);
      }
      await sleep(150);
    }
    console.log(`Keyword "${keyword}": ${keywordJobs} new jobs`);
  }

  console.log("\n" + "=".repeat(60));
  console.log("CERT SEARCH COMPLETE");
  console.log("=".repeat(60));
  console.log(`API Calls: ${totalApiCalls}`);
  console.log(`New Unique Jobs: ${allNewJobs.length}`);

  const freshJobs = allNewJobs.filter(j => j.postedDate >= `${twoWeeksAgo}T`);
  const todayJobs = allNewJobs.filter(j => j.postedDate.startsWith(today));
  console.log(`Posted within 2 weeks: ${freshJobs.length}`);
  console.log(`Posted TODAY (${today}): ${todayJobs.length}`);

  if (todayJobs.length > 0) {
    console.log(`\n--- TODAY'S CERT JOBS ---`);
    todayJobs.forEach(j => console.log(`  ${j.title} @ ${j.company} [${j.location}] kw:${j.matchedKeyword}`));
  }

  // Save
  if (allNewJobs.length > 0) {
    existingData.jobs.push(...allNewJobs);
    existingData.meta = { ...existingData.meta, lastCertSearch: new Date().toISOString(), totalJobs: existingData.jobs.length };
    fs.writeFileSync(existingPath, JSON.stringify(existingData, null, 2));
    console.log(`\nSaved ${existingData.jobs.length} total jobs to jobs.json`);

    // Copy to public folders
    const publicPaths = [
      path.join(ROOT, "public", "jobs.json"),
      path.join(ROOT, "public", "findjobs", "jobs.json"),
      path.join(ROOT, "public", "gotjob", "jobs.json")
    ];
    for (const p of publicPaths) { try { fs.writeFileSync(p, JSON.stringify(existingData, null, 2)); } catch {} }
    console.log("Copied to public folders");
  }

  // Save fresh jobs report
  const reportPath = path.join(ROOT, `recent_cert_scan_${today}.json`);
  const reportData = {
    meta: { scannedAt: new Date().toISOString(), today, twoWeeksAgo, source: "adzuna-cert-expanded", counts: { fresh14d: freshJobs.length, today: todayJobs.length, totalNew: allNewJobs.length } },
    fresh14Days: freshJobs,
    today: todayJobs,
    allNew: allNewJobs
  };
  fs.writeFileSync(reportPath, JSON.stringify(reportData, null, 2));
  console.log(`Saved fresh cert report to ${reportPath}`);
}

main().catch(console.error);
