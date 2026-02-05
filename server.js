


import fs from "fs";
import path, { dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const JOBS_PATH = path.join(__dirname, "jobs.json");

function saveJobsToCache(jobs) {
  fs.writeFileSync(JOBS_PATH, JSON.stringify(jobs, null, 2));
}

function loadJobsFromCache() {
  try {
    const data = JSON.parse(fs.readFileSync(JOBS_PATH, "utf-8"));
    // Handle both formats: { meta: {...}, jobs: [...] } or [...]
    if (data && Array.isArray(data.jobs)) {
      return data.jobs;
    }
    if (Array.isArray(data)) {
      return data;
    }
    return [];
  } catch {
    return [];
  }
}

import express from "express";
import { scrapeIndeedJobs } from "./scrapers/indeed_scraper.js";
import { scrapeSimplifyApplications } from "./scrapers/simplify_scraper.js";
let scrapeLinkedInJobs;
import("./scrapers/linkedin_scraper.js").then(mod => {
  scrapeLinkedInJobs = mod.scrapeLinkedInJobs;
});

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

function normalizeText(value) {
  return (value ?? "").toString().trim();
}

function includesAny(haystack, needles) {
  const h = haystack.toLowerCase();
  return needles.some((n) => h.includes(n.toLowerCase()));
}

function parseSalaryFromText(text) {
  const t = normalizeText(text);
  if (!t) return null;

  const cleaned = t
    .replaceAll("\u00a0", " ")
    .replace(/\s+/g, " ")
    .replace(/,/g, "");

  const money = (n) => {
    const num = Number(n);
    return Number.isFinite(num) ? num : null;
  };

  const annualRange = cleaned.match(
    /\$\s*(\d{2,3}(?:\.\d+)?)\s*[kK]\s*(?:-|to)\s*\$\s*(\d{2,3}(?:\.\d+)?)\s*[kK]\s*(?:CAD|USD)?\s*(?:per\s*year|\/\s*year|ann?u?a?l|yr)?/i
  );
  if (annualRange) {
    const min = money(annualRange[1]);
    const max = money(annualRange[2]);
    if (min != null && max != null) return { min: min * 1000, max: max * 1000, currency: "CAD" };
  }

  const annualSingleK = cleaned.match(
    /\$\s*(\d{2,3}(?:\.\d+)?)\s*[kK]\s*(?:CAD|USD)?\s*(?:per\s*year|\/\s*year|ann?u?a?l|yr)/i
  );
  if (annualSingleK) {
    const v = money(annualSingleK[1]);
    if (v != null) return { min: v * 1000, max: v * 1000, currency: "CAD" };
  }

  const annualRangeFull = cleaned.match(
    /\$\s*(\d{5,6})\s*(?:-|to)\s*\$\s*(\d{5,6})\s*(?:CAD|USD)?\s*(?:per\s*year|\/\s*year|ann?u?a?l|yr)/i
  );
  if (annualRangeFull) {
    const min = money(annualRangeFull[1]);
    const max = money(annualRangeFull[2]);
    if (min != null && max != null) return { min, max, currency: "CAD" };
  }

  const annualSingleFull = cleaned.match(
    /\$\s*(\d{5,6})\s*(?:CAD|USD)?\s*(?:per\s*year|\/\s*year|ann?u?a?l|yr)/i
  );
  if (annualSingleFull) {
    const v = money(annualSingleFull[1]);
    if (v != null) return { min: v, max: v, currency: "CAD" };
  }

  return null;
}

function looksFullTime(text) {
  const t = normalizeText(text).toLowerCase();
  if (!t) return false;
  return t.includes("full-time") || t.includes("full time") || t.includes("permanent");
}

function inToronto(locationText) {
  const l = normalizeText(locationText).toLowerCase();
  return l.includes("toronto") || l.includes("gta") || l.includes("greater toronto");
}

function parseSinceFilter(query) {
  const minutes = Number(query.sinceMinutes ?? "");
  const hours = Number(query.sinceHours ?? "");
  const days = Number(query.sinceDays ?? "");
  const iso = normalizeText(query.sinceIso);

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

function parseTimelineFilter(timelineValue) {
  const t = normalizeText(timelineValue).toLowerCase();
  if (!t) return null;
  if (t === "today" || t === "24h" || t === "1d") {
    return new Date(Date.now() - 24 * 60 * 60 * 1000);
  }
  if (t === "7d" || t === "week") {
    return new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
  }
  if (t === "30d" || t === "month") {
    return new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
  }

  const dayMatch = t.match(/^(\d+)d$/);
  if (dayMatch) {
    const days = Number(dayMatch[1]);
    if (Number.isFinite(days) && days > 0) {
      return new Date(Date.now() - days * 24 * 60 * 60 * 1000);
    }
  }

  const hourMatch = t.match(/^(\d+)h$/);
  if (hourMatch) {
    const hours = Number(hourMatch[1]);
    if (Number.isFinite(hours) && hours > 0) {
      return new Date(Date.now() - hours * 60 * 60 * 1000);
    }
  }

  return null;
}

const GREENHOUSE_BOARDS = [
  // Add/adjust boards over time. Not all will have Toronto roles at all times.
  { company: "Klick", token: "klick" },
  { company: "Wave", token: "wave" },
  { company: "Wealthsimple", token: "wealthsimple" }
];

async function fetchLinkedInJobs({ query, location }) {
  // LinkedIn doesn't have a public RSS feed, so we'll use their search API
  // This is a simplified approach that scrapes LinkedIn's public job search
  const baseUrl = "https://www.linkedin.com/jobs-search";
  
  try {
    const searchParams = new URLSearchParams({
      keywords: query,
      location: location,
      distance: "25",
      sortBy: "R"
    });
    
    const url = `${baseUrl}?${searchParams.toString()}`;
    
    const res = await fetch(url, {
      headers: {
        "user-agent": "BESTIEJOB/0.1"
      }
    });
    
    if (!res.ok) return [];
    
    const html = await res.text();
    
    // Parse jobs from HTML - this is a simplified parser
    // In a production environment, you'd want to use a proper HTML parser
    const jobElements = html.match(/data-entity-urn="urn:li:fsd_jobPosting:(\d+)"/g);
    
    if (!jobElements) return [];
    
    const jobs = [];
    
    // Extract job details from the HTML
    const jobMatches = html.matchAll(/data-entity-urn="urn:li:fsd_jobPosting:(\d+)".*?data-job-id="(\d+)".*?data-base-url="([^"]+)".*?data-job-title="([^"]+)".*?data-company-name="([^"]+)".*?data-job-location-name="([^"]+)".*?data-job-posted-date="([^"]+)".*?data-job-salary="([^"]+)"/gs);
    
    for (const match of jobMatches) {
      const [, jobId, jobPostingId, baseUrl, title, company, location, postedDate, salary] = match;
      
      const jobUrl = `${baseUrl}/jobs/${jobPostingId}`;
      
      // Parse salary if available
      const salaryObj = parseSalaryFromText(salary);
      
      jobs.push({
        id: `linkedin:${jobId}`,
        source: "linkedin",
        company: normalizeText(company),
        title: normalizeText(title),
        location: normalizeText(location),
        url: jobUrl,
        employmentType: looksFullTime(title) ? "full-time" : "unknown",
        salary: salaryObj,
        postedDate: postedDate,
        excerpt: `Posted on ${postedDate}. ${company} is looking for a ${title} in ${location}.`
      });
    }
    
    return jobs;
  } catch (error) {
    console.error("Error fetching LinkedIn jobs:", error);
    return [];
  }
}

async function fetchGreenhouseJobs() {
  const results = [];

  await Promise.all(
    GREENHOUSE_BOARDS.map(async (b) => {
      const url = `https://boards-api.greenhouse.io/v1/boards/${encodeURIComponent(
        b.token
      )}/jobs?content=true`;

      const res = await fetch(url, {
        headers: {
          "user-agent": "BESTIEJOB/0.1"
        }
      });
      if (!res.ok) return;

      const data = await res.json();
      const jobs = Array.isArray(data?.jobs) ? data.jobs : [];

      for (const j of jobs) {
        const title = normalizeText(j.title);
        const absoluteUrl = normalizeText(j.absolute_url);
        const location = normalizeText(j.location?.name);
        const content = normalizeText(j.content);
        const salary = parseSalaryFromText(content);

        results.push({
          id: `greenhouse:${b.token}:${j.id}`,
          source: "greenhouse",
          company: b.company,
          title,
          location,
          url: absoluteUrl,
          employmentType: looksFullTime(content) ? "full-time" : "unknown",
          salary,
          excerpt: content.replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim().slice(0, 240)
        });
      }
    })
  );

  return results;
}

function createJobSources({ keywords, location, simplifyCookie, timelineDays, maxPages }) {
  return [
    // 1. Greenhouse - API based, always works, fastest
    { name: "greenhouse", run: () => fetchGreenhouseJobs() },
    
    // 2. Indeed - RSS first (fast), then HTML with fallbacks
    {
      name: "indeed",
      run: () =>
        scrapeIndeedJobs({
          keyword: keywords.join(" "),
          location,
          maxPages,
          useFallbackApi: true // Enable third-party API fallback
        })
    },
    
    // 3. LinkedIn - Slower, often blocked, but good data
    {
      name: "linkedin",
      run: async () => {
        if (!scrapeLinkedInJobs) {
          const mod = await import("./scrapers/linkedin_scraper.js");
          scrapeLinkedInJobs = mod.scrapeLinkedInJobs;
        }
        const jobs = await scrapeLinkedInJobs(keywords.join(" "), location, 0, maxPages);
        return (jobs || []).map((j) => ({
          id: `linkedin:${j.url}`,
          source: "linkedin",
          company: normalizeText(j.company),
          title: j.title,
          location: normalizeText(j.location || location),
          url: j.url,
          employmentType: looksFullTime(j.title) ? "full-time" : "unknown",
          salary: null,
          postedDate: j.postedDate,
          excerpt: j.excerpt || j.title
        }));
      }
    },
    
    // 4. Simplify - Last, requires cookie authentication
    {
      name: "simplify",
      run: () =>
        scrapeSimplifyApplications({
          keyword: keywords.join(" "),
          timelineDays: Number.isFinite(timelineDays) && timelineDays > 0 ? timelineDays : 30,
          cookie: simplifyCookie
        })
    }
  ];
}

app.get("/api/jobs", async (req, res) => {
  try {
    const minSalary = Number(req.query.minSalary ?? 100000);
    const fullTimeOnly = (req.query.fullTimeOnly ?? "true") === "true";
    const location = normalizeText(req.query.location ?? "Toronto, ON");
    const sinceDate = parseSinceFilter(req.query);
    const timeline = normalizeText(req.query.timeline ?? "");
    const simplifyCookie = normalizeText(req.query.simplifyCookie || process.env.SIMPLIFY_COOKIE);
    const timelineDays = Number(req.query.timelineDays ?? "");
    const maxPages = Number(req.query.maxPages ?? 3);

    const keywordsRaw = normalizeText(
      req.query.keywords ?? "creative, technology, manager, management"
    );
    const keywords = keywordsRaw
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);


    const sources = createJobSources({
      keywords,
      location,
      simplifyCookie,
      timelineDays,
      maxPages
    });

    const settled = await Promise.allSettled(sources.map((s) => s.run()));
    let jobs = settled.flatMap((r) => (r.status === "fulfilled" ? r.value : []));
    
    // Fall back to cached data if scraping returned no results
    if (jobs.length === 0) {
      console.log("Live scraping returned no jobs, falling back to cache...");
      const cachedJobs = loadJobsFromCache();
      if (cachedJobs && cachedJobs.length > 0) {
        jobs = cachedJobs;
      }
    } else {
      // Save successful scrape to cache
      saveJobsToCache(jobs);
    }
    
    const sourceErrors = settled
      .map((r, idx) => ({ r, s: sources[idx] }))
      .filter(({ r }) => r.status === "rejected")
      .map(({ r, s }) => ({ source: s.name, error: String(r.reason?.message || r.reason) }));

    // Debug: log jobs fetched from each source
    console.log('Fetched jobs:', jobs.map(j => ({title: j.title, company: j.company, salary: j.salary, source: j.source})));

    // Relaxed filter: show all jobs, even those without salary
    const effectiveSinceDate = sinceDate || parseTimelineFilter(timeline);
    const filtered = jobs
      .filter((j) => inToronto(j.location || location))
      .filter((j) => includesAny(j.title, keywords))
      .filter((j) => !fullTimeOnly || j.employmentType === "full-time" || looksFullTime(j.title))
      .filter((j) => {
        if (!effectiveSinceDate) return true;
        if (!j.postedDate) return false;
        const posted = new Date(j.postedDate);
        return !Number.isNaN(posted.getTime()) && posted >= effectiveSinceDate;
      })
      // .filter((j) => {
      //   if (!j.salary) return false;
      //   return j.salary.min >= minSalary || j.salary.max >= minSalary;
      // })
      .sort((a, b) => (b.salary?.max ?? 0) - (a.salary?.max ?? 0));

    res.json({
      meta: {
        minSalary,
        fullTimeOnly,
        location,
        keywords,
        timeline,
        sinceDate: effectiveSinceDate ? effectiveSinceDate.toISOString() : null,
        sourceErrors,
        totalFetched: jobs.length,
        totalMatched: filtered.length
      },
      jobs: filtered
    });
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch jobs", details: String(err?.message || err) });
  }
});

// Endpoint to refresh jobs and update cache
app.post("/api/refresh", async (req, res) => {
  try {
    // Use default params for refresh
    const location = "Toronto, ON";
    const keywords = ["creative", "technology", "manager", "management"];
    const minSalary = 100000;
    const fullTimeOnly = true;
    const maxPages = 2;

    const sources = createJobSources({
      keywords,
      location,
      simplifyCookie: "",
      timelineDays: 30,
      maxPages
    });
    const settled = await Promise.allSettled(sources.map((s) => s.run()));
    let jobs = settled.flatMap((r) => (r.status === "fulfilled" ? r.value : []));
    
    // Fall back to cached data if scraping returned no results
    if (jobs.length === 0) {
      console.log("Refresh returned no jobs, keeping existing cache...");
      const cachedJobs = loadJobsFromCache();
      if (cachedJobs && cachedJobs.length > 0) {
        jobs = cachedJobs;
      }
    } else {
      saveJobsToCache(jobs);
    }
    
    res.json({ ok: true, total: jobs.length });
  } catch (err) {
    res.status(500).json({ error: "Failed to refresh jobs", details: String(err?.message || err) });
  }
});

app.get("/api/jobs/cached", (req, res) => {
  const jobs = loadJobsFromCache();
  res.json({ jobs });
});

// Admin endpoints
app.get("/admin", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "admin", "index.html"));
});

app.get("/api/admin/scrape", async (req, res) => {
  try {
    const location = normalizeText(req.query.location ?? "Toronto, ON");
    const keywordsRaw = normalizeText(req.query.keywords ?? "vba");
    const keywords = keywordsRaw.split(",").map(s => s.trim()).filter(Boolean);
    const sourcesParam = normalizeText(req.query.sources ?? "indeed,linkedin");
    const selectedSources = sourcesParam.split(",").map(s => s.trim()).filter(Boolean);
    
    const sinceDate = parseSinceFilter(req.query);
    const simplifyCookie = normalizeText(req.query.simplifyCookie || process.env.SIMPLIFY_COOKIE);
    const maxPages = Number(req.query.maxPages ?? 2);
    
    const allSources = createJobSources({
      keywords,
      location,
      simplifyCookie,
      timelineDays: 30,
      maxPages
    });
    
    const filteredSources = allSources.filter(s => selectedSources.includes(s.name));
    
    if (filteredSources.length === 0) {
      return res.status(400).json({ error: "No valid sources selected" });
    }
    
    const settled = await Promise.allSettled(filteredSources.map((s) => s.run()));
    let jobs = settled.flatMap((r) => (r.status === "fulfilled" ? r.value : []));
    
    // Filter by date if specified
    if (sinceDate) {
      jobs = jobs.filter(j => {
        if (!j.postedDate) return false;
        const posted = new Date(j.postedDate);
        return !Number.isNaN(posted.getTime()) && posted >= sinceDate;
      });
    }
    
    const sourceErrors = settled
      .map((r, idx) => ({ r, s: filteredSources[idx] }))
      .filter(({ r }) => r.status === "rejected")
      .map(({ r, s }) => ({ source: s.name, error: String(r.reason?.message || r.reason) }));
    
    // Merge with existing cache
    const existingJobs = loadJobsFromCache();
    const merged = [...existingJobs, ...jobs];
    
    // Deduplicate by URL
    const seen = new Set();
    const deduped = merged.filter(j => {
      const key = j.url || j.id;
      if (!key || seen.has(key)) return false;
      seen.add(key);
      return true;
    });
    
    saveJobsToCache(deduped);
    
    res.json({
      ok: true,
      totalFetched: jobs.length,
      total: deduped.length,
      sources: selectedSources,
      sinceDate: sinceDate ? sinceDate.toISOString() : null,
      sourceErrors
    });
  } catch (err) {
    res.status(500).json({ error: "Scrape failed", details: String(err?.message || err) });
  }
});

app.post("/api/admin/clear", (req, res) => {
  try {
    saveJobsToCache([]);
    res.json({ ok: true, message: "Cache cleared successfully" });
  } catch (err) {
    res.status(500).json({ error: "Failed to clear cache", details: String(err?.message || err) });
  }
});

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});

function listenWithFallback(startPort, maxAttempts = 10) {
  let attempt = 0;

  const tryListen = (p) => {
    const server = app.listen(p, () => {
      // Intentionally no console noise besides a single line.
      console.log(`BESTIEJOB running on http://localhost:${p}`);
    });

    server.on("error", (err) => {
      if (err?.code === "EADDRINUSE" && attempt < maxAttempts) {
        attempt += 1;
        server.close(() => tryListen(p + 1));
        return;
      }
      throw err;
    });
  };

  tryListen(startPort);
}

listenWithFallback(Number(port));
