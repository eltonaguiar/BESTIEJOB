#!/usr/bin/env node
/**
 * Daily job scan — ServiceNow / Salesforce / other keywords.
 *
 * Pulls live postings from public, structured sources (no login):
 *   - SmartRecruiters public postings API (ServiceNow)
 *   - Workday CXS public search API (Salesforce + Canadian employers)
 *   - Greenhouse / Lever / Ashby public board APIs
 *   - LinkedIn guest job-search endpoint (Playwright fallback if blocked)
 *   - RemoteOK / Jobicy / Remotive remote feeds
 *
 * Writes:
 *   jobs.json, public/jobs.json, public/gotjob/jobs.json, public/findjobs/jobs.json
 *   FRESH_JOBS.md and the <!-- DAILY-SCAN --> block in README.md
 *
 * Usage:
 *   node scripts/daily_job_scan.mjs [--dry-run] [--playwright] [--no-readme]
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import * as cheerio from "cheerio";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const FLAGS = new Set(process.argv.slice(2));
const DRY = FLAGS.has("--dry-run");
const USE_PLAYWRIGHT = FLAGS.has("--playwright") || process.env.SCAN_PLAYWRIGHT === "1";
const SKIP_README = FLAGS.has("--no-readme");

const NOW = new Date();
const NOW_ISO = NOW.toISOString();
const MAX_AGE_DAYS = 45;
const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

// ---------------------------------------------------------------------------
// Keyword configuration
// ---------------------------------------------------------------------------

const PRIMARY_TAGS = [
  { tag: "servicenow", re: /\bservice\s?now\b/i },
  { tag: "salesforce", re: /\bsalesforce\b|\bapex\b|\bvisualforce\b|\bsoql\b|\bforce\.com\b/i },
];

const SECONDARY_TAGS = [
  { tag: "vba", re: /\bvba\b|\bexcel macro/i },
  { tag: "alteryx", re: /\balteryx\b/i },
  { tag: "full-stack", re: /full[\s-]?stack/i },
  { tag: "data", re: /data analyst|business intelligence|\bpower bi\b|\btableau\b/i },
  { tag: "devops", re: /devops|site reliability|cloud architect|aws engineer/i },
  { tag: "python", re: /python developer|python engineer/i },
  { tag: "it-reporting", re: /it reporting|itsm reporting|service now reporting|reporting analyst/i },
  { tag: "itam", re: /it asset management|itam|cmdb|configuration management/i },
];

const EXCLUDE_TITLES =
  /\b(account executive|account manager|sales representative|sales manager|sales engineer|business development|recruiter|talent acquisition|customer success|engagement manager|pre-?sales)\b/i;

const TAG_LABEL = {
  servicenow: "ServiceNow",
  salesforce: "Salesforce",
  vba: "VBA / Excel automation",
  alteryx: "Alteryx",
  "full-stack": "Full stack",
  data: "Data / BI",
  devops: "DevOps / Cloud",
  python: "Python",
  "it-reporting": "IT Reporting",
  itam: "IT Asset Mgmt / CMDB",
};

// Accept Toronto/GTA/Ontario/Canada/remote postings; the site is Toronto-focused.
const GEO_KEEP =
  /toronto|\bgta\b|greater toronto|ontario|\bcanada\b|montreal|quebec|vancouver|british columbia|calgary|alberta|ottawa|mississauga|brampton|markham|waterloo|kitchener|hamilton|victoria,? bc|remote|worldwide|anywhere|telecommute/i;

// ---------------------------------------------------------------------------
// Small helpers
// ---------------------------------------------------------------------------

const stripTags = (s) =>
  (s || "")
    .replace(/<[^>]*>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/\s+/g, " ")
    .trim();

async function fetchText(url, { method = "GET", body, headers = {}, timeout = 25000, retries = 1 } = {}) {
  let lastErr;
  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      const res = await fetch(url, {
        method,
        headers: {
          "user-agent": UA,
          accept: "text/html,application/json;q=0.9,*/*;q=0.8",
          "accept-language": "en-CA,en;q=0.9",
          ...headers,
        },
        body,
        signal: AbortSignal.timeout(timeout),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.text();
    } catch (err) {
      lastErr = err;
      if (attempt < retries) await new Promise((r) => setTimeout(r, 800 * (attempt + 1)));
    }
  }
  throw lastErr;
}

async function fetchJson(url, opts) {
  return JSON.parse(await fetchText(url, opts));
}

async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let cursor = 0;
  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (cursor < items.length) {
      const index = cursor++;
      out[index] = await fn(items[index], index);
    }
  });
  await Promise.all(workers);
  return out;
}

function toIso(value) {
  if (!value) return null;
  if (typeof value === "number") {
    const d = new Date(value);
    return Number.isNaN(d.getTime()) ? null : d.toISOString();
  }
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
}

function workdayPostedOn(text) {
  const t = (text || "").toLowerCase();
  if (!t) return null;
  if (t.includes("today")) return NOW_ISO;
  if (t.includes("yesterday")) return new Date(NOW.getTime() - 864e5).toISOString();
  const m = t.match(/(\d+)\+?\s*days?\s*ago/);
  if (m) return new Date(NOW.getTime() - Number(m[1]) * 864e5).toISOString();
  return null;
}

function detectArrangement(text) {
  const t = (text || "").toLowerCase();
  if (t.includes("remote") || t.includes("telecommute") || t.includes("work from home")) return "remote";
  if (t.includes("hybrid")) return "hybrid";
  if (t.includes("on-site") || t.includes("onsite") || t.includes("in-office") || t.includes("in office")) return "onsite";
  return "unknown";
}

function detectEmploymentType(text) {
  const t = (text || "").toLowerCase();
  if (/\bintern|co-?op\b/.test(t)) return "internship";
  if (/\bpart[\s-]?time\b/.test(t)) return "part-time";
  if (/\bcontract|contractor|temporary|temp\b|fixed[\s-]term/.test(t)) return "contract";
  if (/\bfull[\s-]?time\b|\bpermanent\b/.test(t)) return "full-time";
  return "unknown";
}

function matchTags(title) {
  if (!title || EXCLUDE_TITLES.test(title)) return [];
  const tags = [];
  for (const { tag, re } of PRIMARY_TAGS) if (re.test(title)) tags.push(tag);
  for (const { tag, re } of SECONDARY_TAGS) if (re.test(title)) tags.push(tag);
  return tags;
}

function cleanUrl(raw) {
  if (!raw) return null;
  try {
    const u = new URL(raw);
    u.search = "";
    u.hash = "";
    return u.toString();
  } catch {
    return null;
  }
}

function dedupeKey(job) {
  const url = cleanUrl(job.url);
  if (url) {
    const u = new URL(url);
    return `${u.hostname.replace(/^www\./, "")}${u.pathname}`.toLowerCase();
  }
  return `${job.company}|${job.title}`.toLowerCase().replace(/\s+/g, " ").trim();
}

function buildJob(raw) {
  const title = stripTags(raw.title);
  if (!title || !raw.url) return null;
  const tags = raw.forceTags?.length ? raw.forceTags : matchTags(title);
  if (tags.length === 0) return null;

  const location = stripTags(raw.location || "") || "";
  if (raw.requireGeo && !GEO_KEEP.test(location)) return null;

  const posted = toIso(raw.postedDate);
  if (posted) {
    const age = (NOW - new Date(posted)) / 864e5;
    if (age > MAX_AGE_DAYS || age < -2) {
      // Too old to be useful, or a bad/clock-skewed date.
      if (age > MAX_AGE_DAYS) return null;
    }
  }

  const company = stripTags(raw.company || "") || "Unknown";
  const url = cleanUrl(raw.url);
  if (!url) return null;

  return {
    id: `${raw.source}:${dedupeKey({ url, company, title })}`,
    source: raw.source,
    company,
    title,
    location: location || "Not specified",
    url,
    employmentType: raw.employmentType || detectEmploymentType(`${title} ${raw.excerpt || ""}`),
    salary: raw.salary || null,
    postedDate: posted,
    scrapedAt: NOW_ISO,
    excerpt: stripTags(raw.excerpt || "").slice(0, 320),
    workArrangement: detectArrangement(`${title} ${location} ${raw.excerpt || ""}`),
    tags,
  };
}

// ---------------------------------------------------------------------------
// Source: ServiceNow careers (SmartRecruiters public API)
// ---------------------------------------------------------------------------

async function scanSmartRecruiters() {
  const boards = [{ slug: "ServiceNow", label: "ServiceNow" }];
  const jobs = [];

  for (const board of boards) {
    for (let page = 0; page < 8; page++) {
      const url = `https://api.smartrecruiters.com/v1/companies/${board.slug}/postings?limit=100&offset=${page * 100}`;
      let data;
      try {
        data = await fetchJson(url);
      } catch (err) {
        console.warn(`[smartrecruiters:${board.slug}] page ${page} failed: ${err.message}`);
        break;
      }
      const items = Array.isArray(data.content) ? data.content : [];
      for (const item of items) {
        const loc = item.location || {};
        const locationText = [loc.city, loc.region, loc.country]
          .filter(Boolean)
          .join(", ");
        // Roles at ServiceNow itself rarely repeat the product name in the title;
        // keep its Canadian engineering/admin roles as ServiceNow-tagged jobs.
        const isPlatformCompany = board.slug === "ServiceNow" && /\bcanada\b|, ca\b/i.test(locationText);
        const isPlatformRole = /\b(engineer|developer|architect|administrator|admin|sre)\b/i.test(item.name || "");
        const job = buildJob({
          source: "smartrecruiters",
          title: item.name,
          company: item.company?.name || board.label,
          location: `${locationText}${loc.remote ? " · Remote" : ""}`,
          url: `https://jobs.smartrecruiters.com/${board.slug}/${item.id}`,
          postedDate: item.releasedDate,
          excerpt: item.refNumber ? `Req ${item.refNumber}` : "",
          forceTags: isPlatformCompany && isPlatformRole ? ["servicenow"] : undefined,
          requireGeo: true,
        });
        if (job) jobs.push(job);
      }
      if (items.length < 100) break;
    }
    console.log(`[smartrecruiters:${board.slug}] ${jobs.length} matching postings`);
  }
  return jobs;
}

// ---------------------------------------------------------------------------
// Source: Workday CXS search API
// ---------------------------------------------------------------------------

const WORKDAY_BOARDS = [
  { tenant: "salesforce", wd: "wd12", site: "External_Career_Site", label: "Salesforce" },
  { tenant: "bmo", wd: "wd3", site: "External", label: "BMO" },
  { tenant: "td", wd: "wd3", site: "TD_Bank_Careers", label: "TD Bank" },
  { tenant: "moneris", wd: "wd3", site: "Moneris", label: "Moneris" },
  { tenant: "bdo", wd: "wd3", site: "BDO", label: "BDO Canada" },
  { tenant: "caatpension", wd: "wd10", site: "Careers", label: "CAAT Pension Plan" },
  { tenant: "medcan", wd: "wd10", site: "medcan", label: "Medcan" },
  { tenant: "altusgroup", wd: "wd3", site: "AltusGroup", label: "Altus Group" },
  { tenant: "iko", wd: "wd3", site: "IKO_Careers", label: "IKO" },
  { tenant: "huron", wd: "wd1", site: "huroncareers", label: "Huron" },
  { tenant: "irvingoil", wd: "wd3", site: "IOL_Careers_Primary", label: "Irving Oil" },
  { tenant: "mckesson", wd: "wd3", site: "External_Careers", label: "McKesson" },
  { tenant: "brookfield", wd: "wd5", site: "brookfield", label: "Brookfield" },
  { tenant: "gdit", wd: "wd5", site: "External_Career_Site", label: "GDIT" },
  { tenant: "resolvetech", wd: "wd1", site: "RTS", label: "Resolve Tech Solutions" },
];

async function scanWorkday() {
  const queries = ["servicenow", "salesforce"];
  const jobs = [];

  const tasks = [];
  for (const board of WORKDAY_BOARDS) {
    for (const query of queries) tasks.push({ board, query });
  }

  const results = await mapLimit(tasks, 4, async ({ board, query }) => {
    const api = `https://${board.tenant}.${board.wd}.myworkdayjobs.com/wday/cxs/${board.tenant}/${board.site}/jobs`;
    const collected = [];
    for (let offset = 0; offset < 40; offset += 20) {
      let data;
      try {
        data = await fetchJson(api, {
          method: "POST",
          headers: { "content-type": "application/json", accept: "application/json" },
          body: JSON.stringify({ appliedFacets: {}, limit: 20, offset, searchText: query }),
        });
      } catch (err) {
        console.warn(`[workday:${board.tenant}] "${query}" failed: ${err.message}`);
        break;
      }
      const posts = Array.isArray(data.jobPostings) ? data.jobPostings : [];
      for (const p of posts) {
        const job = buildJob({
          source: "workday",
          title: p.title,
          company: board.label,
          location: p.locationsText || "",
          url: `https://${board.tenant}.${board.wd}.myworkdayjobs.com/en-US/${board.site}${p.externalPath}`,
          postedDate: workdayPostedOn(p.postedOn),
          excerpt: (p.bulletFields || []).join(" · "),
          requireGeo: true,
        });
        if (job) collected.push(job);
      }
      if (!data.total || offset + 20 >= data.total || posts.length === 0) break;
    }
    return collected;
  });

  for (const list of results) jobs.push(...list);
  console.log(`[workday] ${jobs.length} matching postings`);
  return jobs;
}

// ---------------------------------------------------------------------------
// Source: Greenhouse / Lever / Ashby public board APIs
// ---------------------------------------------------------------------------

// Only board slugs verified to answer on boards-api.greenhouse.io.
const GREENHOUSE_BOARDS = [
  ["lightfeatheriollc", "LightFeather"],
  ["9thwayinsignia", "9th Way Insignia"],
  ["accenturefederalservices", "Accenture Federal Services"],
  ["d2l", "D2L"],
  ["dscout", "Dscout"],
  ["icapitalnetwork", "iCapital"],
  ["bloomerang", "Bloomerang"],
  ["neuraflash", "NeuraFlash"],
  ["movableink", "Movable Ink"],
];

const LEVER_BOARDS = [
  ["eqbank", "EQ Bank"],
  ["alimentiv-2", "Alimentiv"],
  ["versapay", "Versapay"],
];

const ASHBY_BOARDS = [
  ["benevity", "Benevity"],
  ["loopio", "Loopio"],
  ["moego", "MoeGo"],
];

async function scanGreenhouse() {
  const jobs = [];
  await mapLimit(GREENHOUSE_BOARDS, 5, async ([token, label]) => {
    try {
      const data = await fetchJson(`https://boards-api.greenhouse.io/v1/boards/${token}/jobs`);
      for (const j of data.jobs || []) {
        const job = buildJob({
          source: "greenhouse",
          title: j.title,
          company: label,
          location: j.location?.name || "",
          url: j.absolute_url,
          postedDate: j.first_published || j.updated_at,
          excerpt: "",
          requireGeo: true,
        });
        if (job) jobs.push(job);
      }
    } catch (err) {
      console.warn(`[greenhouse:${token}] failed: ${err.message}`);
    }
  });
  console.log(`[greenhouse] ${jobs.length} matching postings`);
  return jobs;
}

async function scanLever() {
  const jobs = [];
  await mapLimit(LEVER_BOARDS, 4, async ([token, label]) => {
    try {
      const data = await fetchJson(`https://api.lever.co/v0/postings/${token}?mode=json`);
      for (const j of data || []) {
        const job = buildJob({
          source: "lever",
          title: j.text,
          company: label,
          location: j.categories?.location || "",
          url: j.hostedUrl,
          postedDate: j.createdAt,
          excerpt: j.descriptionPlain || "",
          employmentType: detectEmploymentType(j.categories?.commitment || ""),
          requireGeo: true,
        });
        if (job) jobs.push(job);
      }
    } catch (err) {
      console.warn(`[lever:${token}] failed: ${err.message}`);
    }
  });
  console.log(`[lever] ${jobs.length} matching postings`);
  return jobs;
}

async function scanAshby() {
  const jobs = [];
  await mapLimit(ASHBY_BOARDS, 3, async ([token, label]) => {
    try {
      const data = await fetchJson(`https://api.ashbyhq.com/posting-api/job-board/${token}`);
      for (const j of data.jobs || []) {
        const job = buildJob({
          source: "ashby",
          title: j.title,
          company: label,
          location: j.location || "",
          url: j.jobUrl,
          postedDate: j.publishedAt,
          excerpt: j.descriptionPlain || "",
          employmentType: detectEmploymentType(j.employmentType || ""),
          requireGeo: true,
        });
        if (job) jobs.push(job);
      }
    } catch (err) {
      console.warn(`[ashby:${token}] failed: ${err.message}`);
    }
  });
  console.log(`[ashby] ${jobs.length} matching postings`);
  return jobs;
}

// ---------------------------------------------------------------------------
// Source: LinkedIn guest search (HTTP, Playwright fallback)
// ---------------------------------------------------------------------------

const LINKEDIN_QUERIES = [
  "ServiceNow developer",
  "ServiceNow administrator",
  "ServiceNow architect",
  "Salesforce developer",
  "Salesforce administrator",
  "Salesforce architect",
];

// Second pass restricted to the last 24 hours, so brand-new postings are not
// outranked by older ones in the general search results.
const LINKEDIN_FRESH_QUERIES = [
  "ServiceNow developer",
  "ServiceNow administrator",
  "ServiceNow consultant",
  "Salesforce developer",
  "Salesforce administrator",
  "Salesforce consultant",
  "Salesforce CPQ",
  // Variants: postings routinely use these titles instead of "developer"
  "ServiceNow ITSM",
  "ServiceNow ITAM",
  "ServiceNow platform",
  "Salesforce technical",
  "Salesforce platform developer",
  "CRM developer",
];

function parseLinkedInCards(html) {
  const $ = cheerio.load(html);
  const out = [];
  $(".base-card").each((_, el) => {
    const link =
      $(el).find("a.base-card__full-link").attr("href") ||
      $(el).find("a.base-search-card__subtitle").attr("href") ||
      $(el).find("a").first().attr("href");
    const title = $(el).find(".base-search-card__title").text().trim();
    const company = $(el).find(".base-search-card__subtitle").text().trim();
    const location = $(el).find(".job-search-card__location").text().trim();
    const posted = $(el).find("time").attr("datetime") || "";
    if (!link || !title) return;
    out.push({ link, title, company, location, posted });
  });
  return out;
}

async function linkedinPage(url) {
  try {
    const html = await fetchText(url, { retries: 2 });
    const cards = parseLinkedInCards(html);
    if (cards.length > 0) return cards;
  } catch (err) {
    console.warn(`[linkedin] HTTP failed: ${err.message}`);
  }

  if (!USE_PLAYWRIGHT) return [];

  console.log("[linkedin] falling back to Playwright");
  try {
    const { chromium } = await import("playwright");
    const browser = await chromium.launch({ headless: true, args: ["--no-sandbox"] });
    try {
      const page = await browser.newPage({ userAgent: UA, locale: "en-CA" });
      await page.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
      await page.waitForSelector(".base-card", { timeout: 15000 }).catch(() => {});
      await page.waitForTimeout(1500);
      return parseLinkedInCards(await page.content());
    } finally {
      await browser.close();
    }
  } catch (err) {
    console.warn(`[linkedin] Playwright fallback failed: ${err.message}`);
    return [];
  }
}

async function scanLinkedIn() {
  const locations = ["Toronto, Ontario, Canada", "Canada"];
  const tasks = [];
  for (const query of LINKEDIN_QUERIES) {
    for (const location of locations) tasks.push({ query, location });
  }
  for (const query of LINKEDIN_FRESH_QUERIES) {
    for (const location of locations) tasks.push({ query, location, fresh: true });
  }

  // LinkedIn throttles the guest endpoint hard; two workers with a pause between
  // requests keeps the scan under the 429 threshold most runs.
  const results = await mapLimit(tasks, 2, async ({ query, location, fresh }) => {
    await new Promise((r) => setTimeout(r, 1800));
    const url =
      "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search" +
      `?keywords=${encodeURIComponent(query)}&location=${encodeURIComponent(location)}` +
      `${fresh ? "&f_TPR=r86400" : ""}&start=0`;
    const cards = await linkedinPage(url);
    return cards
      .map((c) =>
        buildJob({
          source: "linkedin",
          title: c.title,
          company: c.company,
          location: c.location || location,
          url: c.link,
          // The 24h pass only returns recent cards; if LinkedIn omits <time>,
          // the card is still inside the window, so stamp it with scan time.
          postedDate: c.posted || (fresh ? NOW_ISO : null),
          excerpt: `${query} · LinkedIn guest search${fresh ? " (last 24h)" : ""}`,
          requireGeo: true,
        })
      )
      .filter(Boolean);
  });

  const jobs = results.flat();
  console.log(`[linkedin] ${jobs.length} matching postings`);
  return jobs;
}

// ---------------------------------------------------------------------------
// Source: remote feeds
// ---------------------------------------------------------------------------

async function scanRemoteBoards() {
  const jobs = [];

  try {
    const data = await fetchJson("https://remoteok.com/api");
    for (const j of Array.isArray(data) ? data : []) {
      if (!j.position) continue;
      const job = buildJob({
        source: "remoteok",
        title: j.position,
        company: j.company,
        location: j.location || "Remote",
        url: j.url || j.apply_url,
        postedDate: j.date,
        excerpt: (j.tags || []).join(", "),
        salary: j.salary_min ? { min: j.salary_min, max: j.salary_max || j.salary_min, currency: "USD" } : null,
      });
      if (job) jobs.push(job);
    }
  } catch (err) {
    console.warn(`[remoteok] failed: ${err.message}`);
  }

  try {
    const data = await fetchJson("https://jobicy.com/api/v2/remote-jobs?count=50&geo=canada");
    for (const j of data.jobs || []) {
      const job = buildJob({
        source: "jobicy",
        title: j.jobTitle,
        company: j.companyName,
        location: j.jobGeo || "Remote",
        url: j.url,
        postedDate: j.pubDate,
        excerpt: j.jobExcerpt || "",
        salary: j.annualSalaryMin
          ? { min: Number(j.annualSalaryMin), max: Number(j.annualSalaryMax || j.annualSalaryMin), currency: j.salaryCurrency || "USD" }
          : null,
      });
      if (job) jobs.push(job);
    }
  } catch (err) {
    console.warn(`[jobicy] failed: ${err.message}`);
  }

  for (const term of ["servicenow", "salesforce"]) {
    try {
      const data = await fetchJson(`https://remotive.com/api/remote-jobs?search=${term}&limit=25`);
      for (const j of data.jobs || []) {
        const job = buildJob({
          source: "remotive",
          title: j.title,
          company: j.company_name,
          location: j.candidate_required_location || "Remote",
          url: j.url,
          postedDate: j.publication_date,
          excerpt: stripTags(j.description || "").slice(0, 300),
          salary: j.salary || null,
        });
        if (job) jobs.push(job);
      }
    } catch (err) {
      console.warn(`[remotive:${term}] failed: ${err.message}`);
    }
  }

  console.log(`[remote] ${jobs.length} matching postings`);
  return jobs;
}

// ---------------------------------------------------------------------------
// Source: Adzuna Canada search API (date sorted)
// ---------------------------------------------------------------------------

const ADZUNA_QUERIES = [
  // Toronto / GTA — ServiceNow (keyword + city)
  { what: "servicenow", where: "Toronto" },
  { what: "servicenow administrator", where: "Toronto" },
  { what: "servicenow architect", where: "Toronto" },
  { what: "servicenow developer", where: "Toronto" },
  { what: "servicenow consultant", where: "Toronto" },
  { what: "servicenow specialist", where: "Toronto" },
  { what: "servicenow lead", where: "Toronto" },
  { what: "servicenow ITSM", where: "Toronto" },
  { what: "servicenow ITOM", where: "Toronto" },
  // Toronto / GTA — Salesforce (keyword + city)
  { what: "salesforce", where: "Toronto" },
  { what: "salesforce developer", where: "Toronto" },
  { what: "salesforce administrator", where: "Toronto" },
  { what: "salesforce architect", where: "Toronto" },
  { what: "salesforce consultant", where: "Toronto" },
  { what: "salesforce analyst", where: "Toronto" },
  { what: "salesforce specialist", where: "Toronto" },
  { what: "salesforce lead", where: "Toronto" },
  // Canada-wide — remote-eligible ServiceNow / Salesforce (Toronto focus + fully remote Canada)
  { what: "servicenow remote", where: "Canada" },
  { what: "salesforce remote", where: "Canada" },
  // National broad (catches remote + any Canadian location)
  { what: "servicenow", where: "Canada" },
  { what: "salesforce", where: "Canada" },
  // Elton's core competencies (ITAM/ITSM reporting, CMDB)
  { what: "it reporting", where: "Toronto" },
  { what: "it asset management", where: "Toronto" },
  { what: "cmdb", where: "Toronto" },
  { what: "itsm reporting", where: "Toronto" },
  // Keyword variants — the titles these roles are actually posted under.
  // Adzuna matches on posting text, so these catch work hidden behind
  // generic titles ("platform developer", "ITSM analyst", "BSA").
  { what: "service now", where: "Toronto" },
  { what: "itsm", where: "Toronto" },
  { what: "service mapping", where: "Toronto" },
  { what: "software asset management", where: "Toronto" },
  { what: "hardware asset management", where: "Toronto" },
  { what: "platform developer", where: "Toronto" },
  { what: "crm developer", where: "Toronto" },
  { what: "business systems analyst", where: "Toronto" },
  { what: "application analyst", where: "Toronto" },
  { what: "apex", where: "Toronto" },
  { what: "salesforce cpq", where: "Toronto" },
  { what: "salesforce marketing cloud", where: "Toronto" },
  { what: "agentforce", where: "Toronto" },
  { what: "servicenow", where: "Ottawa" },
  { what: "servicenow", where: "Mississauga" },
];

async function scanAdzuna() {
  // Keys are the public demo credentials already used by scripts/scrape_adzuna.js;
  // env vars override them when a private quota is configured.
  const appId = process.env.ADZUNA_APP_ID || "54ce986e";
  const appKey = process.env.ADZUNA_API_KEY || "db851f299e966c0a2a72af525dce6199";
  const jobs = [];

  const results = await mapLimit(ADZUNA_QUERIES, 3, async ({ what, where }) => {
    const url =
      "https://api.adzuna.com/v1/api/jobs/ca/search/1" +
      `?app_id=${encodeURIComponent(appId)}&app_key=${encodeURIComponent(appKey)}` +
      `&results_per_page=50&what=${encodeURIComponent(what)}&where=${encodeURIComponent(where)}` +
      "&sort_by=date&max_days_old=14&content-type=application/json";
    try {
      const data = await fetchJson(url);
      const out = [];
      for (const r of data.results || []) {
        const salary =
          r.salary_min || r.salary_max
            ? { min: Number(r.salary_min) || Number(r.salary_max), max: Number(r.salary_max) || Number(r.salary_min), currency: "CAD" }
            : null;
        const job = buildJob({
          source: "adzuna",
          title: r.title,
          company: r.company?.display_name || "Unknown",
          location: r.location?.display_name || where,
          url: r.redirect_url,
          postedDate: r.created,
          excerpt: r.description,
          salary,
          requireGeo: true,
        });
        if (job) out.push(job);
      }
      return out;
    } catch (err) {
      console.warn(`[adzuna:${what}/${where}] failed: ${err.message}`);
      return [];
    }
  });

  for (const list of results) jobs.push(...list);
  console.log(`[adzuna] ${jobs.length} matching postings`);
  return jobs;
}

// ---------------------------------------------------------------------------
// Merge, build output, write site data + docs
// ---------------------------------------------------------------------------

function loadExistingJobs() {
  const candidates = [path.join(ROOT, "jobs.json")];
  const merged = [];
  for (const file of candidates) {
    try {
      const data = JSON.parse(fs.readFileSync(file, "utf8"));
      const list = Array.isArray(data) ? data : Array.isArray(data.jobs) ? data.jobs : [];
      for (const job of list) {
        if (!job?.postedDate || !job?.url || !job?.title) continue;
        const ageDays = (NOW - new Date(job.postedDate)) / 864e5;
        if (!Number.isFinite(ageDays) || ageDays > MAX_AGE_DAYS) continue;
        // Drop generic career-homepage entries carried over from older scrapes.
        if (/^careers?$|^job openings$|^open positions$/i.test(job.title.trim())) continue;
        if (!job.tags || job.tags.length === 0) {
          const tags = matchTags(job.title);
          if (tags.length === 0) continue;
          job.tags = tags;
        }
        merged.push(job);
      }
    } catch {
      /* no existing cache */
    }
  }
  return merged;
}

function dedupeJobs(jobs) {
  const byKey = new Map();
  for (const job of jobs) {
    const key = dedupeKey(job);
    const existing = byKey.get(key);
    if (!existing) {
      byKey.set(key, job);
      continue;
    }
    // Prefer the record with a real posted date and richer text.
    const existingScore = (existing.postedDate ? 2 : 0) + (existing.excerpt?.length > 40 ? 1 : 0);
    const newScore = (job.postedDate ? 2 : 0) + (job.excerpt?.length > 40 ? 1 : 0);
    if (newScore > existingScore) byKey.set(key, job);
  }
  return [...byKey.values()];
}

const TAG_ORDER = ["servicenow", "salesforce", "vba", "alteryx", "full-stack", "data", "devops", "python"];

function primaryTag(job) {
  return TAG_ORDER.find((t) => job.tags?.includes(t)) || "other";
}

function sortByDate(jobs) {
  return [...jobs].sort((a, b) => {
    const da = a.postedDate ? new Date(a.postedDate).getTime() : 0;
    const db = b.postedDate ? new Date(b.postedDate).getTime() : 0;
    return db - da;
  });
}

function capSecondary(jobs, perTag = 40) {
  const counts = {};
  const kept = [];
  for (const job of sortByDate(jobs)) {
    const tag = primaryTag(job);
    if (PRIMARY_TAGS.some((p) => p.tag === tag)) {
      kept.push(job);
      continue;
    }
    counts[tag] = (counts[tag] || 0) + 1;
    if (counts[tag] <= perTag) kept.push(job);
  }
  return kept;
}

function dateOnly(iso) {
  if (!iso) return "Not disclosed";
  return iso.slice(0, 10);
}

function escapeCell(value) {
  return String(value || "").replace(/\|/g, "\\|").replace(/\n/g, " ").trim();
}

function buildFreshMarkdown(jobs, stats) {
  const lines = [];
  lines.push("# Fresh job scan");
  lines.push("");
  lines.push(
    `Auto-generated by \`scripts/daily_job_scan.mjs\` on ${NOW_ISO}. ` +
      `Every row is a live posting pulled from an employer ATS or public job feed during this scan — newest first.`
  );
  lines.push("");
  lines.push(`**${jobs.length} matching postings** across ${Object.keys(stats.sources).length} sources:`);
  lines.push("");
  for (const [source, count] of Object.entries(stats.sources).sort((a, b) => b[1] - a[1])) {
    lines.push(`- ${source}: ${count}`);
  }
  lines.push("");

  for (const tag of TAG_ORDER) {
    const group = sortByDate(jobs.filter((j) => primaryTag(j) === tag));
    if (group.length === 0) continue;
    lines.push(`## ${TAG_LABEL[tag]} (${group.length})`);
    lines.push("");
    lines.push("| Posted | Role | Company | Location | Type | Source |");
    lines.push("|---|---|---|---|---|---|");
    for (const job of group) {
      lines.push(
        `| ${dateOnly(job.postedDate)} | [${escapeCell(job.title)}](${job.url}) | ${escapeCell(
          job.company
        )} | ${escapeCell(job.location)} | ${escapeCell(job.employmentType)} | ${escapeCell(job.source)} |`
      );
    }
    lines.push("");
  }

  lines.push("## Scan notes");
  lines.push("");
  lines.push("- Sources are public ATS/job-board endpoints; no logins or paid APIs are used.");
  lines.push("- `postedDate` is the employer's publication date when exposed, otherwise omitted.");
  lines.push(`- Entries older than ${MAX_AGE_DAYS} days are pruned on each scan.`);
  lines.push("- Remote eligibility is geographic where the posting says so; check each link before applying.");
  lines.push("");
  return lines.join("\n");
}

// The "newest" tables below restate rows the merger has already written into the
// main tables, and README job-row guard counts every repeat as a duplicate URL
// (growth > 5 fails the build). Show only postings that are not on the board yet.
function normalizeUrl(url) {
  return String(url || "")
    .split("#")[0]
    .split("?")[0]
    .replace(/\/+$/, "");
}

function buildReadmeBlock(jobs, stats, existingUrls = new Set()) {
  jobs = jobs.filter((j) => !existingUrls.has(normalizeUrl(j.url)));
  const nov1 = jobs.filter((j) => j.postedDate?.slice(0, 10) === "2026-11-01").length;
  const lines = [];
  lines.push("<!-- DAILY-SCAN:START -->");
  lines.push("## Latest auto-scanned jobs (newest first)");
  lines.push("");
  lines.push(
    `**Scan: ${NOW_ISO}** · ${jobs.length} live postings from ${Object.keys(stats.sources).length} public sources · ` +
      `${nov1} dated 2026-11-01 · full list in [FRESH_JOBS.md](FRESH_JOBS.md)`
  );
  lines.push("");
  for (const tag of ["servicenow", "salesforce"]) {
    const group = sortByDate(jobs.filter((j) => primaryTag(j) === tag)).slice(0, 12);
    if (group.length === 0) continue;
    lines.push(`### ${TAG_LABEL[tag]} — newest ${group.length}`);
    lines.push("");
    lines.push("| Posted | Role | Company | Location |");
    lines.push("|---|---|---|---|");
    for (const job of group) {
      lines.push(
        `| ${dateOnly(job.postedDate)} | [${escapeCell(job.title)}](${job.url}) | ${escapeCell(
          job.company
        )} | ${escapeCell(job.location)} |`
      );
    }
    lines.push("");
  }
  const other = sortByDate(jobs.filter((j) => !["servicenow", "salesforce"].includes(primaryTag(j)))).slice(0, 10);
  if (other.length > 0) {
    lines.push(`### Other keyword matches — newest ${other.length}`);
    lines.push("");
    lines.push("| Posted | Role | Company | Location | Keyword |");
    lines.push("|---|---|---|---|---|");
    for (const job of other) {
      lines.push(
        `| ${dateOnly(job.postedDate)} | [${escapeCell(job.title)}](${job.url}) | ${escapeCell(
          job.company
        )} | ${escapeCell(job.location)} | ${escapeCell(TAG_LABEL[primaryTag(job)] || primaryTag(job))} |`
      );
    }
    lines.push("");
  }
  lines.push("_Generated automatically by the daily job scan; run `npm run scan:daily` to refresh._");
  lines.push("<!-- DAILY-SCAN:END -->");
  return lines.join("\n");
}

function writeReadmeBlock(jobs, stats) {
  const readmePath = path.join(ROOT, "README.md");
  if (!fs.existsSync(readmePath)) return;
  let readme = fs.readFileSync(readmePath, "utf8");
  const start = "<!-- DAILY-SCAN:START -->";
  const end = "<!-- DAILY-SCAN:END -->";
  const blockStart = readme.indexOf(start);
  const blockEnd = readme.indexOf(end);
  const outsideBlock =
    blockStart >= 0 && blockEnd > blockStart
      ? readme.slice(0, blockStart) + readme.slice(blockEnd + end.length)
      : readme;
  const existingUrls = new Set(
    [...outsideBlock.matchAll(/\]\((https?:\/\/[^)\s]+)\)/g)].map((m) => normalizeUrl(m[1]))
  );
  const block = buildReadmeBlock(jobs, stats, existingUrls);

  const startIndex = readme.indexOf(start);
  const endIndex = readme.indexOf(end);
  if (startIndex >= 0 && endIndex > startIndex) {
    readme = readme.slice(0, startIndex) + block + readme.slice(endIndex + end.length);
  } else {
    const headingIndex = readme.indexOf("\n");
    const insertAt = headingIndex >= 0 ? headingIndex + 1 : readme.length;
    readme = readme.slice(0, insertAt) + "\n" + block + "\n" + readme.slice(insertAt);
  }
  fs.writeFileSync(readmePath, readme);
}

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  console.log(`[scan] start ${NOW_ISO}${DRY ? " (dry run)" : ""}`);

  const sourceResults = await Promise.allSettled([
    scanSmartRecruiters(),
    scanWorkday(),
    scanGreenhouse(),
    scanLever(),
    scanAshby(),
    scanLinkedIn(),
    scanRemoteBoards(),
    scanAdzuna(),
  ]);

  const fresh = [];
  const sourceCounts = {};
  sourceResults.forEach((res) => {
    if (res.status !== "fulfilled") {
      console.warn(`[scan] source failed: ${res.reason?.message || res.reason}`);
      return;
    }
    for (const job of res.value) {
      fresh.push(job);
      sourceCounts[job.source] = (sourceCounts[job.source] || 0) + 1;
    }
  });

  const existing = loadExistingJobs();
  const all = capSecondary(dedupeJobs([...fresh, ...existing]));
  const jobs = sortByDate(all);

  const stats = {
    generatedAt: NOW_ISO,
    total: jobs.length,
    newThisScan: fresh.length,
    retainedFromPrevious: Math.max(0, jobs.length - fresh.length),
    sources: sourceCounts,
    primaryCounts: {
      servicenow: jobs.filter((j) => j.tags.includes("servicenow")).length,
      salesforce: jobs.filter((j) => j.tags.includes("salesforce")).length,
    },
  };

  console.log(`[scan] fresh=${fresh.length} merged=${jobs.length}`, JSON.stringify(stats.primaryCounts));

  if (DRY) {
    const sample = sortByDate(fresh).slice(0, 15);
    for (const j of sample) console.log(`  ${dateOnly(j.postedDate)} | ${j.source} | ${j.title} | ${j.company} | ${j.location}`);
    return;
  }

  const payload = {
    meta: {
      keyword: "multi",
      keywords: [...PRIMARY_TAGS.map((t) => t.tag), ...SECONDARY_TAGS.map((t) => t.tag)],
      location: "Toronto, ON",
      dateFilter: "month",
      scrapedAt: NOW_ISO,
      ...stats,
    },
    jobs,
  };

  const json = JSON.stringify(payload, null, 2);
  const targets = [
    path.join(ROOT, "jobs.json"),
    path.join(ROOT, "public", "jobs.json"),
    path.join(ROOT, "public", "gotjob", "jobs.json"),
    path.join(ROOT, "public", "findjobs", "jobs.json"),
  ];
  for (const target of targets) {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, json);
    console.log(`[scan] wrote ${path.relative(ROOT, target)}`);
  }

  fs.writeFileSync(path.join(ROOT, "FRESH_JOBS.md"), buildFreshMarkdown(jobs, stats));
  console.log("[scan] wrote FRESH_JOBS.md");

  if (!SKIP_README) {
    writeReadmeBlock(jobs, stats);
    console.log("[scan] updated README daily-scan block");
  }
}

main().catch((err) => {
  console.error("[scan] fatal:", err);
  process.exit(1);
});
