import axios from "axios";
import * as cheerio from "cheerio";

function normalizeText(value) {
  return (value ?? "").toString().replace(/\s+/g, " ").trim();
}

function parseDate(value) {
  if (!value) return null;
  const date = new Date(value);
  return Number.isNaN(date.valueOf()) ? null : date;
}

function hasJobShape(obj) {
  if (!obj || typeof obj !== "object") return false;
  const keys = Object.keys(obj);
  const titleKey = keys.find((k) => /title|role|position/i.test(k));
  const companyKey = keys.find((k) => /company/i.test(k));
  return Boolean(titleKey && companyKey);
}

function extractApplications(value, results) {
  if (!value) return;
  if (Array.isArray(value)) {
    value.forEach((item) => extractApplications(item, results));
    return;
  }
  if (typeof value !== "object") return;

  if (hasJobShape(value)) {
    results.push(value);
  }

  for (const v of Object.values(value)) {
    extractApplications(v, results);
  }
}

function parseApplicationsFromHtml(html) {
  const $ = cheerio.load(html);
  const nextData = $("script#__NEXT_DATA__").html();
  if (nextData) {
    try {
      const data = JSON.parse(nextData);
      const results = [];
      extractApplications(data, results);
      return results;
    } catch (error) {
      console.error("Simplify __NEXT_DATA__ parse failed:", error?.message || error);
    }
  }

  const preloadMatch = html.match(/window\.__PRELOADED_STATE__\s*=\s*(\{.*?\});/s);
  if (preloadMatch) {
    try {
      const data = JSON.parse(preloadMatch[1]);
      const results = [];
      extractApplications(data, results);
      return results;
    } catch (error) {
      console.error("Simplify preloaded state parse failed:", error?.message || error);
    }
  }

  return [];
}

function mapApplication(app) {
  const title = normalizeText(app.title || app.role || app.position || app.jobTitle || app.job_title);
  const company = normalizeText(app.company || app.companyName || app.employer || app.company_name);
  const location = normalizeText(app.location || app.city || app.jobLocation || "");
  const url = normalizeText(app.url || app.jobUrl || app.job_url || app.link || "");
  const status = normalizeText(app.status || app.applicationStatus || "");
  const appliedAt = parseDate(app.appliedAt || app.applied_at || app.createdAt || app.created_at);
  const postedDate = appliedAt ? appliedAt.toISOString() : null;

  return {
    id: `simplify:${url || company}:${title}`,
    source: "simplify",
    company,
    title,
    location,
    url,
    employmentType: "unknown",
    salary: null,
    postedDate,
    excerpt: normalizeText(status || app.notes || app.stage || "")
  };
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

export async function scrapeSimplifyApplications({
  keyword,
  timelineDays = 30,
  cookie
}) {
  if (!cookie) {
    console.warn("Simplify cookie missing; skipping simplify scraper.");
    return [];
  }

  const response = await axios.get("https://simplify.jobs/applications", {
    headers: {
      "user-agent": "BESTIEJOB/0.1",
      cookie
    }
  });

  const rawApplications = parseApplicationsFromHtml(response.data);
  const mapped = rawApplications
    .map(mapApplication)
    .filter((job) => job.title || job.company);

  const keywordText = normalizeText(keyword).toLowerCase();
  const keywordMatch = (job) => {
    if (!keywordText) return true;
    const hay = `${job.title} ${job.company} ${job.excerpt}`.toLowerCase();
    return hay.includes(keywordText);
  };

  const cutoffMs = timelineDays ? Date.now() - timelineDays * 24 * 60 * 60 * 1000 : null;
  const withinTimeline = (job) => {
    if (!cutoffMs) return true;
    if (!job.postedDate) return false;
    const posted = new Date(job.postedDate).valueOf();
    return Number.isFinite(posted) && posted >= cutoffMs;
  };

  return mergeUnique(mapped.filter(keywordMatch).filter(withinTimeline));
}
