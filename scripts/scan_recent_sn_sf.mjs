import axios from "axios";
import fs from "fs";

const APP_ID = "54ce986e";
const APP_KEY = "db851f299e966c0a2a72af525dce6199";
const COUNTRY = "ca";

const NOW = new Date();
const TODAY = NOW.toISOString().slice(0, 10); // 2026-10-31
const YESTERDAY = new Date(NOW.getTime() - 86400000).toISOString().slice(0, 10); // 2026-10-30
const WEEK_AGO = new Date(NOW.getTime() - 7 * 86400000).toISOString().slice(0, 10); // 2026-10-24

console.log("TODAY:", TODAY, "YESTERDAY:", YESTERDAY, "WEEK_AGO:", WEEK_AGO);

const SN_KEYWORDS = [
  // Core ServiceNow roles
  "ServiceNow", "ServiceNow Administrator", "ServiceNow Developer",
  "ServiceNow CSA", "ServiceNow CAD", "ServiceNow Architect",
  // ServiceNow modules / practice areas
  "ServiceNow ITSM", "ServiceNow ITOM", "ServiceNow CSM", "ServiceNow FSM",
  "ServiceNow HRSD", "ServiceNow App Engine", "ServiceNow Flow Designer",
  // ServiceNow adjacent titles
  "ServiceNow Implementation", "ServiceNow Consultant", "ServiceNow Technical Consultant",
  "ServiceNow Business Analyst", "ServiceNow Project Manager",
  // Platform terms
  "CMDB", "IT Service Management", "GlideScript", "ServiceNow Admin"
];
const SF_KEYWORDS = [
  // Core Salesforce roles
  "Salesforce Administrator", "Salesforce Platform Administrator",
  "Salesforce Platform Developer", "Salesforce Platform Developer I",
  "Salesforce Developer", "Salesforce Consultant", "Salesforce Admin",
  // Salesforce clouds / certs
  "Salesforce CPQ", "Salesforce Revenue Cloud", "Salesforce Marketing Cloud",
  "Salesforce Service Cloud", "Salesforce Experience Cloud",
  "Salesforce Certified Platform Developer", "Salesforce Certified Platform Administrator",
  // Adjacent titles
  "Salesforce BA", "Salesforce Architect", "Salesforce Technical Consultant",
  "Apex Developer", "LWC Developer"
];

const LOCATIONS = [
  "Toronto", "Ontario", "Remote", "Canada", "Vancouver", "Montreal",
  "Calgary", "Ottawa"
];

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

function classify(text) {
  const t = text.toLowerCase();
  const isSN = /servicenow|service now|csa\b|cad\b|certified system administrator|certified application developer/.test(t);
  const isSF = /salesforce|platform administrator|platform admin|platform developer|certified technical architect|cta\b/.test(t);
  return { isSN, isSF };
}

function bucket(created) {
  if (!created) return "no_date";
  const d = created.slice(0, 10);
  if (d === TODAY) return "TODAY";
  if (d === YESTERDAY) return "YESTERDAY";
  if (d >= WEEK_AGO) return "WITHIN_7_DAYS";
  return "OLDER";
}

async function fetchPage(keyword, location, page = 1, rpp = 50) {
  const url = `http://api.adzuna.com/v1/api/jobs/${COUNTRY}/search/${page}?app_id=${APP_ID}&app_key=${APP_KEY}&results_per_page=${rpp}&what=${encodeURIComponent(keyword)}&where=${encodeURIComponent(location)}&sort_by=date&content-type=application/json`;
  const res = await axios.get(url, { timeout: 30000, headers: { Accept: "application/json" } });
  return res.data;
}

async function main() {
  const existingRaw = JSON.parse(fs.readFileSync("jobs.json", "utf-8"));
  const existingJobs = Array.isArray(existingRaw) ? existingRaw : (existingRaw.jobs || []);
  const existingIds = new Set(existingJobs.map(j => j.id));
  console.log("Loaded", existingJobs.length, "existing jobs");

  const todayJobs = [], yesterdayJobs = [], weekJobs = [], olderJobs = [];
  const seen = new Set(existingIds);
  let totalCalls = 0;
  let totalSnSfSeen = 0;

  const allKeywords = [...SN_KEYWORDS, ...SF_KEYWORDS];

  for (const kw of allKeywords) {
    for (const loc of LOCATIONS) {
      let stoppedEarly = false;
      try {
        // page 1
        const data = await fetchPage(kw, loc, 1, 50);
        totalCalls++;
        const results = data.results || [];
        for (const j of results) {
          totalSnSfSeen++;
          const id = j.id || `adzuna:${Math.random().toString(36).slice(2,9)}`;
          if (seen.has(id)) continue;
          seen.add(id);
          const text = `${j.title} ${j.description || ""} ${j.company.display_name || ""}`;
          const { isSN, isSF } = classify(text);
          if (!isSN && !isSF) continue;
          const b = bucket(j.created);
          const job = {
            id, source: "adzuna",
            company: j.company?.display_name || "Unknown",
            title: j.title,
            location: j.location?.display_name || `${loc}, Canada`,
            url: j.redirect_url,
            employmentType: "full-time",
            salary: (j.salary_min && j.salary_max) ? { min: Math.round(j.salary_min), max: Math.round(j.salary_max) } : null,
            postedDate: j.created,
            excerpt: (j.description || j.title).substring(0, 300),
            category: j.category?.label || "Technology",
            matched: isSN ? "ServiceNow" : isSF ? "Salesforce" : "Both",
            posted_bucket: b
          };
          if (b === "TODAY") todayJobs.push(job);
          else if (b === "YESTERDAY") yesterdayJobs.push(job);
          else if (b === "WITHIN_7_DAYS") weekJobs.push(job);
          else {
            olderJobs.push(job);
            // sorted by date desc; once we see OLDER, further results are older too -> break
            stoppedEarly = true;
            break;
          }
        }
        console.log(`  ${kw} @ ${loc}: ${results.length} results | T=${todayJobs.length} Y=${yesterdayJobs.length} W=${weekJobs.length} O=${olderJobs.length} ${stoppedEarly ? "(stopped early)" : ""}`);
        if (stoppedEarly) continue;
        // page 2
        await sleep(200);
        const data2 = await fetchPage(kw, loc, 2, 50);
        totalCalls++;
        const results2 = data2.results || [];
        for (const j of results2) {
          const id = j.id || `adzuna:${Math.random().toString(36).slice(2,9)}`;
          if (seen.has(id)) continue;
          seen.add(id);
          const text = `${j.title} ${j.description || ""} ${j.company.display_name || ""}`;
          const { isSN, isSF } = classify(text);
          if (!isSN && !isSF) continue;
          const b = bucket(j.created);
          const job = {
            id, source: "adzuna",
            company: j.company?.display_name || "Unknown",
            title: j.title,
            location: j.location?.display_name || `${loc}, Canada`,
            url: j.redirect_url,
            employmentType: "full-time",
            salary: (j.salary_min && j.salary_max) ? { min: Math.round(j.salary_min), max: Math.round(j.salary_max) } : null,
            postedDate: j.created,
            excerpt: (j.description || j.title).substring(0, 300),
            category: j.category?.label || "Technology",
            matched: isSN ? "ServiceNow" : isSF ? "Salesforce" : "Both",
            posted_bucket: b
          };
          if (b === "TODAY") todayJobs.push(job);
          else if (b === "YESTERDAY") yesterdayJobs.push(job);
          else if (b === "WITHIN_7_DAYS") weekJobs.push(job);
          else { olderJobs.push(job); stoppedEarly = true; break; }
        }
        console.log(`     page2: ${results2.length} results | T=${todayJobs.length} Y=${yesterdayJobs.length} W=${weekJobs.length}`);
      } catch (e) {
        console.log(`  ${kw} @ ${loc}: FAILED ${e.message}`);
      }
      await sleep(200);
    }
  }

  console.log("\n========================================");
  console.log("ADZUNA SN/SF RECENT SCAN COMPLETE");
  console.log("========================================");
  console.log("Total API calls:", totalCalls, "| SN/SF results inspected:", totalSnSfSeen);
  console.log("TODAY (Oct 31):", todayJobs.length);
  console.log("YESTERDAY (Oct 30):", yesterdayJobs.length);
  console.log("WITHIN_7_DAYS (Oct 24-31):", weekJobs.length);
  console.log("OLDER:", olderJobs.length);

  const out = {
    meta: {
      scannedAt: new Date().toISOString(),
      today: TODAY, yesterday: YESTERDAY, weekAgo: WEEK_AGO,
      counts: { today: todayJobs.length, yesterday: yesterdayJobs.length, within7: weekJobs.length, older: olderJobs.length },
      source: "adzuna",
      existingJobsLoaded: existingJobs.length
    },
    today: todayJobs,
    yesterday: yesterdayJobs,
    within7Days: weekJobs,
    older: olderJobs
  };
  fs.writeFileSync("recent_sn_sf_scan.json", JSON.stringify(out, null, 2));
  console.log("\nSaved to recent_sn_sf_scan.json");
  console.log("New unique recent jobs (not already in jobs.json):", todayJobs.length + yesterdayJobs.length + weekJobs.length);
}

main().catch(e => { console.error("Fatal:", e.message); process.exit(1); });
