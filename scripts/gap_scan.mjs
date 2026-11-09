#!/usr/bin/env node
/**
 * Gap scan — Playwright sweep of partner/employer career sites plus extra
 * Adzuna keyword variants, for ServiceNow / Salesforce roles the aggregator
 * feed misses.
 *
 * Why: Adzuna and LinkedIn guest search skipped several live roles this week
 * (Ateko/FX Innovation 526327, Cofomo, Everforth, Coaxxion), and they lag by a
 * day or more on the ones they do carry. Partner career pages are the earliest
 * source.
 *
 * Each site is loaded in headless Chromium, JobPosting JSON-LD and
 * keyword-matching anchors are collected, and undated candidates are opened
 * (capped) to read their datePosted. Dates are never invented: a posting with
 * no published date goes into an inbox/ submission (model `gap-scan`) with an
 * em dash in the Posted column and is left out of the feed. The inbox is the
 * repo's review queue — tools/jobs_merge_inbox.py merges dated rows and skips
 * undated ones, so nothing reaches README or the page without a real date.
 *
 * Output rows use the same schema as scripts/daily_job_scan.mjs and are merged
 * into jobs.json + the three public copies.
 *
 * Usage:
 *   node scripts/gap_scan.mjs                # sites + adzuna variants
 *   node scripts/gap_scan.mjs --sites        # Playwright only
 *   node scripts/gap_scan.mjs --adzuna       # Adzuna variants only
 *   node scripts/gap_scan.mjs --dry-run      # print, write nothing
 *   node scripts/gap_scan.mjs --no-inbox     # skip the inbox/ submission
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { chromium } from "playwright";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

const FLAGS = new Set(process.argv.slice(2));
const DRY = FLAGS.has("--dry-run");
const ONLY_SITES = FLAGS.has("--sites");
const ONLY_ADZUNA = FLAGS.has("--adzuna");
const NO_INBOX = FLAGS.has("--no-inbox");

const NOW = new Date();
const NOW_ISO = NOW.toISOString();
const MAX_AGE_DAYS = 31;

const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

const TARGETS = [
  "jobs.json",
  "public/jobs.json",
  "public/gotjob/jobs.json",
  "public/findjobs/jobs.json",
];

// Partner/employer career sites that carry SN/SF roles Adzuna misses.
const SITES = [
  { name: "FX Innovation / Ateko", url: "https://www.fxinnovation.com/en/jobs" },
  { name: "Cofomo", url: "https://www.cofomo.com/en/careers/" },
  { name: "Everforth", url: "https://everforth.com/careers" },
  { name: "Coaxxion", url: "https://coaxxion.com/en/careers/" },
  { name: "CloudKettle", url: "https://cloudkettle.com/careers/" },
  { name: "Lane Four", url: "https://lanefour.com/opportunities/" },
  { name: "Crossfuze", url: "https://crossfuze.pinpointhq.com/" },
];

const KW = /\bservice\s?now\b|\bsalesforce\b|\bapex\b|\blwc\b|\bsoql\b|\bvisualforce\b|\bomnistudio\b|\bagentforce\b|\brevenue cloud\b|\bdata cloud\b|\bmarketing cloud\b|\bfield service\b|\bitsm\b|\bitam\b|\bcmdb\b|\bitom\b|now platform/i;

const GEO_KEEP =
  /toronto|\bgta\b|greater toronto|ontario|canada|montreal|montr[ée]al|quebec|qu[ée]bec|vancouver|british columbia|calgary|alberta|ottawa|mississauga|brampton|markham|waterloo|kitchener|hamilton|remote|anywhere|t[ée]l[ée]travail/i;

const EXCLUDE = /\b(account executive|account manager|sales representative|sales manager|business development|recruiter|talent acquisition|pre-?sales)\b/i;

// Anchor candidates must look like a job posting, not a service/product page.
// Partner sites market "ServiceNow", "Salesforce", "ITSM" etc. on marketing
// pages that otherwise pass the keyword filter (found 2026-11-02: cofomo.com
// /en/technologies/servicenow and ateko.com/en/services/* were being collected).
const JOB_URL =
  /\/jobs?\/[^/?#]+|job[-_]?(detail|posting|opening)|\/postings?\/|\/apply\b|pinpointhq\.com|greenhouse\.io|lever\.co|ashbyhq\.com|myworkdayjobs\.com|smartrecruiters\.com|recruitee\.com|workable\.com|bamboohr\.com/i;
const NON_JOB =
  /\/(services?|insights?|technolog(y|ies)|blog|products?|solutions?|resources?|about|contact|ebooks?|events?|webinars?|news|support|pricing|careers?)\/?$/i;

// Keyword variants the hourly Adzuna pass does not ask for, scoped to today.
const ADZUNA_VARIANTS = [
  { what: "now platform", where: "Toronto" },
  { what: "servicenow discovery", where: "Toronto" },
  { what: "servicenow service mapping", where: "Toronto" },
  { what: "servicenow csdm", where: "Toronto" },
  { what: "itsm analyst", where: "Toronto" },
  { what: "servicenow service desk", where: "Toronto" },
  { what: "servicenow catalog", where: "Toronto" },
  { what: "salesforce omnistudio", where: "Toronto" },
  { what: "salesforce revenue cloud", where: "Toronto" },
  { what: "salesforce data cloud", where: "Toronto" },
  { what: "salesforce service cloud", where: "Toronto" },
  { what: "salesforce community cloud", where: "Toronto" },
  { what: "agentforce", where: "Canada" },
  { what: "servicenow developer", where: "Canada" },
  { what: "servicenow architect", where: "Canada" },
  { what: "servicenow administrator", where: "Canada" },
  { what: "salesforce developer", where: "Canada" },
  { what: "salesforce administrator", where: "Canada" },
];

// AI panel keyword proposals (tools/ai_panel.py). The panel is a proposal
// source, not an authority: anything without the shape of a job keyword is
// dropped again here, so a hallucinated phrase can never reach the API.
function loadAiVariants() {
  const flagged = process.argv.find((a) => a.startsWith("--variants-file="));
  const file = flagged ? flagged.split("=")[1] : path.join(ROOT, "raw", "ai_queries.json");
  let payload;
  try {
    payload = JSON.parse(fs.readFileSync(file, "utf8"));
  } catch {
    return [];
  }
  const raw = Array.isArray(payload) ? payload : payload.keywords || [];
  const known = new Set(ADZUNA_VARIANTS.map((v) => v.what.toLowerCase()));
  const out = [];
  for (const item of raw) {
    const what = String(item || "").trim().toLowerCase();
    if (!what || known.has(what)) continue;
    if (!/^[a-z0-9][a-z0-9 .+#/-]{2,40}$/.test(what)) continue;
    if (what.split(/\s+/).length > 4) continue;
    if (/\b(toronto|canada|ontario|remote)\b/.test(what)) continue;
    known.add(what);
    out.push({ what, where: "Canada" });
  }
  if (out.length) console.log(`[gap:adzuna] +${out.length} AI-suggested variants from ${file}`);
  return out;
}

const MAX_DETAIL_PAGES = 24;
const DETAIL_CONCURRENCY = 4;

// ---------------------------------------------------------------------------
// helpers

function cleanUrl(raw) {
  try {
    const u = new URL(raw);
    for (const k of ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]) {
      u.searchParams.delete(k);
    }
    u.hash = "";
    return u.toString();
  } catch {
    return "";
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

function toIso(value) {
  if (!value) return null;
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? null : d.toISOString();
}

function detectTags(hay) {
  const tags = [];
  if (/\bservice\s?now\b/i.test(hay)) tags.push("servicenow");
  if (/\bsalesforce\b|\bapex\b|\blwc\b|\bsoql\b|\bvisualforce\b/i.test(hay)) tags.push("salesforce");
  if (/\bitsm\b|\bitil\b|it reporting/i.test(hay)) tags.push("it-reporting");
  if (/\bitam\b|\bcmdb\b|configuration management|discovery/i.test(hay)) tags.push("itam");
  return tags;
}

function buildJob({ source, title, company, location, url, postedDate, excerpt }) {
  const t = (title || "").replace(/\s+/g, " ").trim();
  const u = cleanUrl(url);
  if (!t || !u || EXCLUDE.test(t)) return null;
  if (!KW.test(`${t} ${excerpt || ""}`)) return null;
  if (!GEO_KEEP.test(location || "")) return null;
  const posted = toIso(postedDate);
  if (!posted) return null;
  const ageDays = (NOW - new Date(posted)) / 864e5;
  if (ageDays > MAX_AGE_DAYS || ageDays < -2) return null;

  const loc = (location || "").replace(/\s+/g, " ").trim() || "Not specified";
  const ex = (excerpt || "").replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim().slice(0, 320);
  const hay = `${t} ${loc} ${ex}`;

  return {
    id: `${source}:${urlKey(u)}`,
    source,
    company: (company || "").replace(/\s+/g, " ").trim() || "Unknown",
    title: t,
    location: loc,
    url: u,
    employmentType: /contract/i.test(hay) ? "contract" : /part[- ]time/i.test(hay) ? "part-time" : "unknown",
    salary: null,
    postedDate: posted,
    scrapedAt: NOW_ISO,
    excerpt: ex,
    workArrangement: /remote|t[ée]l[ée]travail|anywhere/i.test(hay)
      ? "remote"
      : /hybrid/i.test(hay)
        ? "hybrid"
        : "unknown",
    tags: detectTags(hay),
  };
}

function fromLd(json, pageUrl, siteName) {
  const out = [];
  const nodes = [];
  const push = (v) => {
    if (!v) return;
    if (Array.isArray(v)) v.forEach(push);
    else nodes.push(v);
  };
  try {
    const data = typeof json === "string" ? JSON.parse(json) : json;
    push(data["@graph"] || data);
  } catch {
    return out;
  }
  for (const node of nodes) {
    const type = node["@type"];
    const isPosting = Array.isArray(type) ? type.includes("JobPosting") : type === "JobPosting";
    if (!isPosting) continue;
    const addr = node.jobLocation?.address || node.jobLocation?.[0]?.address || {};
    const location = [addr.addressLocality, addr.addressRegion, addr.addressCountry]
      .filter(Boolean)
      .join(", ");
    out.push({
      source: `site:${siteName.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`,
      title: node.title || node.name,
      company: node.hiringOrganization?.name || siteName,
      location: location || node.jobLocationType || "",
      url: node.url || pageUrl,
      postedDate: node.datePosted,
      excerpt: node.description || "",
    });
  }
  return out;
}

async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let i = 0;
  const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
    while (i < items.length) {
      const idx = i++;
      out[idx] = await fn(items[idx], idx);
    }
  });
  await Promise.all(workers);
  return out;
}

// ---------------------------------------------------------------------------
// Playwright pass

async function scanSites() {
  const raw = { sites: {}, undated: [] };
  const candidates = [];
  // Playwright >=1.49 defaults chromium to the "chrome-headless-shell" build,
  // which `playwright install chromium` did NOT fetch (chromium_headless_shell-1208
  // missing -> gap scan aborted every hour, 2026-11-09). Try the headless shell,
  // then the full chromium build, then a channel override rather than failing.
  let browser;
  try {
    browser = await chromium.launch({ headless: true });
  } catch (shellErr) {
    console.warn(`[gap] headless-shell launch failed (${shellErr.message}); trying full chromium`);
    try {
      browser = await chromium.launch({ headless: true, channel: "chromium" });
    } catch (chanErr) {
      console.warn(`[gap] chromium channel failed (${chanErr.message}); last try: executablePath override`);
      browser = await chromium.launch({ headless: true, executablePath: process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE || undefined });
    }
  }
  const ctx = await browser.newContext({ userAgent: UA, locale: "en-CA" });

  try {
    for (const site of SITES) {
      const page = await ctx.newPage();
      try {
        await page.goto(site.url, { waitUntil: "domcontentloaded", timeout: 30000 });
        await page.waitForLoadState("networkidle", { timeout: 15000 }).catch(() => {});
        await page.waitForTimeout(1200);
        // Client-rendered listings only populate after scroll.
        for (let i = 0; i < 5; i += 1) {
          await page.mouse.wheel(0, 1600);
          await page.waitForTimeout(300);
        }

        const ldBlocks = await page.$$eval('script[type="application/ld+json"]', (els) =>
          els.map((e) => e.textContent || "")
        );
        const anchors = await page.$$eval("a[href]", (as) =>
          as.map((a) => ({
            href: a.href,
            text: (a.textContent || "").replace(/\s+/g, " ").trim().slice(0, 140),
          }))
        );

        let fromJsonLd = 0;
        for (const block of ldBlocks) {
          for (const c of fromLd(block, site.url, site.name)) {
            candidates.push({ ...c, siteName: site.name });
            fromJsonLd += 1;
          }
        }

        let fromAnchors = 0;
        for (const a of anchors) {
          if (!/^https?:/.test(a.href)) continue;
          if (!JOB_URL.test(a.href) || NON_JOB.test(a.href)) continue;
          if (!KW.test(a.text) || a.text.length < 6) continue;
          candidates.push({
            source: `site:${site.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}`,
            title: a.text,
            company: site.name,
            location: "",
            url: a.href,
            postedDate: null,
            excerpt: "",
            siteName: site.name,
          });
          fromAnchors += 1;
        }

        raw.sites[site.name] = { url: site.url, jsonLd: fromJsonLd, anchors: fromAnchors };
        console.log(`[gap:${site.name}] jsonLd=${fromJsonLd} anchors=${fromAnchors}`);
      } catch (err) {
        raw.sites[site.name] = { url: site.url, error: String(err.message || err).slice(0, 140) };
        console.warn(`[gap:${site.name}] skipped: ${String(err.message || err).slice(0, 120)}`);
      } finally {
        await page.close();
      }
    }

    // Undated candidates: open the detail page once to read JobPosting.datePosted.
    const seen = new Set();
    const undated = [];
    for (const c of candidates) {
      const k = urlKey(c.url);
      if (!k || seen.has(k)) continue;
      seen.add(k);
      if (!c.postedDate) undated.push(c);
    }

    const toVisit = undated.slice(0, MAX_DETAIL_PAGES);
    const resolved = await mapLimit(toVisit, DETAIL_CONCURRENCY, async (c) => {
      const page = await ctx.newPage();
      try {
        await page.goto(c.url, { waitUntil: "domcontentloaded", timeout: 20000 });
        const ldBlocks = await page.$$eval('script[type="application/ld+json"]', (els) =>
          els.map((e) => e.textContent || "")
        );
        for (const block of ldBlocks) {
          const found = fromLd(block, c.url, c.siteName).find((x) => x.postedDate);
          if (found) return { ...c, ...found, postedDate: found.postedDate, excerpt: found.excerpt || c.excerpt };
        }
        const text = await page.evaluate(() => {
          const body = document.body?.innerText || "";
          return body.replace(/\s+/g, " ").slice(0, 4000);
        });
        // Only trust an explicit posting date label; a bare "date" hit picks up
        // copyright footers and event dates.
        const m = text.match(
          /(?:posted|publication date|publi[ée]e? le)\D{0,20}(\d{4}-\d{2}-\d{2}|\d{1,2}\s+\w+\s+\d{4})/i
        );
        if (m) {
          const parsed = toIso(m[1]);
          if (parsed) return { ...c, postedDate: parsed, excerpt: text.slice(0, 320) };
        }
        return { ...c, excerpt: text.slice(0, 320) };
      } catch (err) {
        return { ...c, error: String(err.message || err).slice(0, 120) };
      } finally {
        await page.close();
      }
    });

    const dated = [];
    for (const c of [...candidates.filter((x) => x.postedDate), ...resolved]) {
      const job = buildJob({
        source: c.source,
        title: c.title,
        company: c.company,
        location: c.location || (GEO_KEEP.test(c.excerpt || "") ? "Canada" : ""),
        url: c.url,
        postedDate: c.postedDate,
        excerpt: c.excerpt,
      });
      if (job) dated.push(job);
      else if (!c.postedDate)
        raw.undated.push({
          site: c.siteName,
          title: (c.title || "").replace(/\s+/g, " ").trim(),
          company: c.company || c.siteName,
          location: (c.location || "").replace(/\s+/g, " ").trim(),
          url: c.url,
          excerpt: (c.excerpt || "").replace(/\s+/g, " ").slice(0, 160),
        });
    }

    raw.dated = dated;
    console.log(
      `[gap] sites dateable=${dated.length} undated=${raw.undated.length} (detail pages opened=${toVisit.length})`
    );
    return { jobs: dated, undated: raw.undated, raw };
  } finally {
    await ctx.close();
    await browser.close();
  }
}

// ---------------------------------------------------------------------------
// Adzuna variant pass (today only)

async function scanAdzunaVariants() {
  const appId = process.env.ADZUNA_APP_ID || "54ce986e";
  const appKey = process.env.ADZUNA_API_KEY || "db851f299e966c0a2a72af525dce6199";
  const jobs = [];
  const variants = [...ADZUNA_VARIANTS, ...loadAiVariants()];
  const perQuery = await mapLimit(variants, 4, async ({ what, where }) => {
    const url =
      "https://api.adzuna.com/v1/api/jobs/ca/search/1" +
      `?app_id=${encodeURIComponent(appId)}&app_key=${encodeURIComponent(appKey)}` +
      `&results_per_page=50&what=${encodeURIComponent(what)}&where=${encodeURIComponent(where)}` +
      "&sort_by=date&max_days_old=1&content-type=application/json";
    try {
      const res = await fetch(url, { headers: { "User-Agent": UA } });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const out = [];
      for (const r of data.results || []) {
        const job = buildJob({
          source: "adzuna",
          title: r.title,
          company: r.company?.display_name,
          location: r.location?.display_name || where,
          url: r.redirect_url,
          postedDate: r.created,
          excerpt: r.description,
        });
        if (job) out.push(job);
      }
      return out;
    } catch (err) {
      console.warn(`[gap:adzuna:${what}/${where}] ${String(err.message || err).slice(0, 80)}`);
      return [];
    }
  });
  for (const list of perQuery) jobs.push(...list);
  console.log(`[gap:adzuna] variants=${variants.length} today-only matches=${jobs.length}`);
  return jobs;
}

// ---------------------------------------------------------------------------
// inbox/ submission
//
// Undated partner postings used to land only in raw/, where nothing reads them.
// They now enter the inbox/ submission queue, which is where every agent's
// finds are reviewed. The Posted cell stays an em dash on purpose:
// tools/jobs_merge_inbox.py only merges rows whose date is a real YYYY-MM-DD,
// so "unknown" can never silently become a fabricated posting date.

const INBOX = path.join(ROOT, "inbox");
const INBOX_MODEL = "gap-scan";

function mdCell(value) {
  return String(value ?? "")
    .replace(/\|/g, "/")
    .replace(/\s+/g, " ")
    .trim();
}

function todaySubmissions(iso) {
  const re = new RegExp(`^${INBOX_MODEL}--${iso}--v(\\d+)\\.md$`, "i");
  let max = 0;
  const files = [];
  try {
    for (const f of fs.readdirSync(INBOX)) {
      const m = f.match(re);
      if (!m) continue;
      files.push(f);
      max = Math.max(max, Number(m[1]));
    }
  } catch {
    /* no inbox/ yet */
  }
  return { files, max };
}

function writeInbox({ dated, undated, scannedAt }) {
  if (DRY) {
    console.log(`[gap] inbox (dry run): ${dated.length} dated, ${undated.length} undated`);
    return null;
  }
  const iso = scannedAt.slice(0, 10);
  fs.mkdirSync(INBOX, { recursive: true });

  const { files, max } = todaySubmissions(iso);
  const already = new Set();
  for (const f of files) {
    const text = fs.readFileSync(path.join(INBOX, f), "utf8");
    for (const m of text.matchAll(/https?:\/\/[^)\s|]+/g)) already.add(urlKey(m[0]));
  }

  const freshDated = dated.filter((j) => !already.has(urlKey(j.url)));
  const seen = new Set();
  const freshUndated = undated.filter((j) => {
    const k = urlKey(j.url);
    if (!k || seen.has(k) || already.has(k)) return false;
    seen.add(k);
    return true;
  });

  if (!freshDated.length && !freshUndated.length) {
    console.log(
      `[gap] inbox: nothing new (${files.length} submission(s) already cover these candidates)`
    );
    return null;
  }

  const target = path.join(INBOX, `${INBOX_MODEL}--${iso}--v${max + 1}.md`);
  const lines = [
    "---",
    `model: ${INBOX_MODEL}`,
    `scanned_at: ${scannedAt}`,
    `task: partner-gap-scan`,
    `notes: ${SITES.length} partner career pages; ${freshDated.length} dated, ${freshUndated.length} undated (page publishes no posted date).`,
    "---",
    "",
    `# Partner gap scan — ${iso}`,
    "",
    "Dated rows merge normally. Undated rows carry an em dash because the employer",
    "page publishes no posted date — they are listed for review and are skipped by",
    "the merger rather than given an invented date.",
    "",
  ];

  if (freshDated.length) {
    lines.push("## Dated", "", "| Posted | Role | Company | Location | URL | Note |", "|---|---|---|---|---|---|");
    for (const j of freshDated) {
      lines.push(
        `| ${j.postedDate.slice(0, 10)} | [${mdCell(j.title)}](${j.url}) | ${mdCell(j.company)} | ${mdCell(j.location)} | ${j.url} | via ${mdCell(j.source.replace(/^site:/, ""))} |`
      );
    }
    lines.push("");
  }
  if (freshUndated.length) {
    lines.push(
      "## Undated — needs a posted date",
      "",
      "| Posted | Role | Company | Location | URL | Note |",
      "|---|---|---|---|---|---|"
    );
    for (const j of freshUndated) {
      lines.push(
        `| — | [${mdCell(j.title)}](${j.url}) | ${mdCell(j.company)} | ${mdCell(j.location || "Canada")} | ${j.url} | undated on ${mdCell(j.site)} |`
      );
    }
    lines.push("");
  }

  fs.writeFileSync(target, lines.join("\n"), "utf8");
  console.log(
    `[gap] inbox: wrote inbox/${path.basename(target)} (+${freshDated.length} dated, ${freshUndated.length} undated)`
  );
  return target;
}

// ---------------------------------------------------------------------------
// merge + write

function mergeIntoFeed(fresh) {
  const jobsPath = path.join(ROOT, "jobs.json");
  const payload = JSON.parse(fs.readFileSync(jobsPath, "utf8"));
  const existing = Array.isArray(payload) ? payload : payload.jobs || [];

  const byUrl = new Map();
  for (const j of existing) if (j?.url) byUrl.set(urlKey(j.url), j);

  let added = 0;
  for (const job of fresh) {
    const k = urlKey(job.url);
    if (!k || byUrl.has(k)) continue;
    byUrl.set(k, job);
    added += 1;
  }

  const merged = [...byUrl.values()].sort((a, b) =>
    (a.postedDate || "") < (b.postedDate || "") ? 1 : (a.postedDate || "") > (b.postedDate || "") ? -1 : 0
  );

  if (DRY) {
    console.log(`[gap] dry run: would add ${added} of ${fresh.length} (total ${merged.length})`);
    for (const j of fresh.slice(0, 12)) console.log(`  + ${j.postedDate.slice(0, 10)} | ${j.source} | ${j.title}`);
    return added;
  }

  const next = Array.isArray(payload)
    ? merged
    : { ...payload, meta: { ...(payload.meta || {}), total: merged.length }, jobs: merged };
  const json = JSON.stringify(next, null, 2);
  for (const rel of TARGETS) {
    const target = path.join(ROOT, rel);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, json);
  }
  console.log(`[gap] wrote ${TARGETS.length} feeds (+${added} new, total ${merged.length})`);
  return added;
}

async function main() {
  console.log(`[gap] start ${NOW_ISO}${DRY ? " (dry run)" : ""}`);
  const fresh = [];
  let raw = {};

  if (!ONLY_ADZUNA) {
    const { jobs, undated, raw: siteRaw } = await scanSites();
    fresh.push(...jobs);
    raw = siteRaw;
    if (!NO_INBOX) writeInbox({ dated: jobs, undated, scannedAt: NOW_ISO });
  }
  if (!ONLY_SITES) {
    fresh.push(...(await scanAdzunaVariants()));
  }

  const iso = NOW_ISO.slice(0, 10);
  const rawPath = path.join(ROOT, "raw", `gap_scan_${iso}.json`);
  fs.mkdirSync(path.dirname(rawPath), { recursive: true });
  fs.writeFileSync(
    rawPath,
    JSON.stringify({ scannedAt: NOW_ISO, total: fresh.length, ...raw, jobs: fresh }, null, 1)
  );
  console.log(`[gap] wrote raw/gap_scan_${iso}.json`);

  mergeIntoFeed(fresh);
}

main().catch((err) => {
  console.error("[gap] fatal:", err);
  process.exit(1);
});
