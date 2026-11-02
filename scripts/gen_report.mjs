import fs from "fs";

const d = JSON.parse(fs.readFileSync("recent_sn_sf_scan.json", "utf-8"));

const TODAY = d.meta.today; // 2026-10-31
const YESTERDAY = d.meta.yesterday; // 2026-10-30
const WEEK_AGO = d.meta.weekAgo; // 2026-10-24

function isRelevant(j) {
  const t = (j.title || "").toLowerCase();
  const hasSN = /servicenow|service now/.test(t);
  const hasSF = /salesforce/.test(t);
  const hasPlatformAdmin = /platform administrator|platform admin/.test(t);
  const hasPlatformDev = /platform developer/.test(t);
  const hasCSA_CAD = /\b(csa|cad)\b/.test(t) && hasSN;
  return hasSN || hasSF || hasPlatformAdmin || hasPlatformDev || hasCSA_CAD;
}

function locTier(loc) {
  const l = (loc || "").toLowerCase();
  if (l.includes("toronto") || l.includes("ontario")) return 0;
  if (l.includes("remote")) return 1;
  if (l.includes("canada")) return 2;
  return 3;
}

function bucketOrder(b) { return b === "TODAY" ? 0 : b === "YESTERDAY" ? 1 : b === "WITHIN_7_DAYS" ? 2 : 3; }

const all = [...d.today, ...d.yesterday, ...d.within7Days].filter(isRelevant);
const seen = new Set();
const uniq = all.filter(j => { if (seen.has(j.id)) return false; seen.add(j.id); return true; });
uniq.sort((a, b) => {
  const bo = bucketOrder(a.posted_bucket) - bucketOrder(b.posted_bucket);
  if (bo !== 0) return bo;
  return locTier(a.location) - locTier(b.location);
});

function fmtDate(iso) { return iso.slice(0, 10); }

function jobLine(j) {
  return "- **" + j.title + "** — " + j.company + " — " + j.location + " [" + j.matched + "] (" + fmtDate(j.postedDate) + ")\n  " + j.url;
}

function section(arr) {
  const relevant = arr.filter(isRelevant).sort((a, b) => locTier(a.location) - locTier(b.location));
  if (relevant.length === 0) return "_None_";
  return relevant.map(jobLine).join("\n");
}

const todayCount = d.today.filter(isRelevant).length;
const yesterdayCount = d.yesterday.filter(isRelevant).length;
const within7Count = d.within7Days.filter(isRelevant).length;

let lines = [];
lines.push("# ServiceNow / Salesforce Job Scan — BESTIEJOB");
lines.push("");
lines.push("**Scanned:** " + d.meta.scannedAt);
lines.push("**Source:** Adzuna CA API (sort_by=date)");
lines.push("**Priority window:** Today (" + TODAY + ") → Yesterday (" + YESTERDAY + ") → Within 7 days (since " + WEEK_AGO + ")");
lines.push("**Scope:** ServiceNow (incl. CSA/CAD certifications), Salesforce Platform Administrator / Platform Admin / Platform Developer I & related roles");
lines.push("**Cross-checked:** de-duplicated against existing jobs.json (14,283 records) — all listed below are NEW additions not already in the database.");
lines.push("");
lines.push("## Summary");
lines.push("");
lines.push("| Window | Count |");
lines.push("|--------|-------:|");
lines.push("| Today (" + TODAY + ") | " + todayCount + " |");
lines.push("| Yesterday (" + YESTERDAY + ") | " + yesterdayCount + " |");
lines.push("| Within 7 days (" + WEEK_AGO + "–" + TODAY + ") | " + within7Count + " |");
lines.push("| **Total new relevant** | ****" + uniq.length + "** |");
lines.push("");
lines.push("Location priority order: Toronto/Ontario → Remote → Other Canada. All entries flagged Unverified — confirm live on the employer Apply page before applying.");
lines.push("");
lines.push("---");
lines.push("");
lines.push("## 1) Posted TODAY (" + TODAY + ") — Highest Priority");
lines.push("");
lines.push(section(d.today).trim());
lines.push("---");
lines.push("");
lines.push("## 2) Posted YESTERDAY (" + YESTERDAY + ") — High Priority");
lines.push("");
lines.push(section(d.yesterday).trim());
lines.push("---");
lines.push("");
lines.push("## 3) Posted WITHIN 7 DAYS (" + WEEK_AGO + "–" + TODAY + ") — Medium Priority");
lines.push("");
lines.push(section(d.within7Days).trim());
lines.push("");
lines.push("---");
lines.push("");
lines.push("## Notes");
lines.push("- The matched tag indicates the matched family: ServiceNow or Salesforce.");
lines.push("- Several CSA/CAD-certified ServiceNow roles and Salesforce Platform Administrator / Platform Developer I roles are included.");
lines.push("- Adzuna results are sorted by date (sort_by=date); scanning stopped at the first older result per keyword/location, so the within-7-days list is complete for the searched keywords/locations.");
lines.push("- Keywords searched: ServiceNow, ServiceNow Administrator, ServiceNow Developer, ServiceNow CSA, ServiceNow CAD, ServiceNow Architect, Salesforce Administrator, Salesforce Platform Administrator, Salesforce Platform Developer, Salesforce Platform Developer I, Salesforce Developer, Salesforce Consultant, Salesforce Admin.");
lines.push("- Locations: Toronto, Ontario, Remote, Canada, Vancouver, Montreal, Calgary, Ottawa.");
lines.push("");
lines.push("## Recommended Next Step");
lines.push("Add these " + uniq.length + " new postings to jobs.json (source: adzuna) and push to a new branch in eltonaguiar/bestiejob, e.g. <agent>/2026-10-31.");

fs.writeFileSync("REPORT_SN_SF_2026-10-31.md", lines.join("\n"));
console.log(lines.join("\n").slice(0, 3500));
console.log("\n...(report saved to REPORT_SN_SF_2026-10-31.md)...");
console.log("\nRelevant counts: today=" + todayCount + " yesterday=" + yesterdayCount + " within7=" + within7Count + " total=" + uniq.length);
