import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import Parser from "rss-parser";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const port = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const rssParser = new Parser({
  headers: {
    "user-agent": "BESTIEJOB/0.1"
  }
});

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

const GREENHOUSE_BOARDS = [
  // Add/adjust boards over time. Not all will have Toronto roles at all times.
  { company: "Klick", token: "klick" },
  { company: "Wave", token: "wave" },
  { company: "Wealthsimple", token: "wealthsimple" }
];

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

async function fetchIndeedRss({ query, location }) {
  // Note: salary is usually not provided in RSS. We still include it as a discovery source.
  const q = encodeURIComponent(query);
  const l = encodeURIComponent(location);
  const url = `https://ca.indeed.com/rss?q=${q}&l=${l}`;

  try {
    const feed = await rssParser.parseURL(url);
    const items = Array.isArray(feed?.items) ? feed.items : [];

    return items.map((it) => {
      const title = normalizeText(it.title);
      const link = normalizeText(it.link);
      const content = normalizeText(it.contentSnippet || it.content || it.summary);

      return {
        id: `indeed:${link || title}`,
        source: "indeed",
        company: normalizeText(it.creator || ""),
        title,
        location: location,
        url: link,
        employmentType: looksFullTime(content) ? "full-time" : "unknown",
        salary: parseSalaryFromText(content),
        excerpt: content.slice(0, 240)
      };
    });
  } catch {
    return [];
  }
}

app.get("/api/jobs", async (req, res) => {
  try {
    const minSalary = Number(req.query.minSalary ?? 100000);
    const fullTimeOnly = (req.query.fullTimeOnly ?? "true") === "true";
    const location = normalizeText(req.query.location ?? "Toronto, ON");

    const keywordsRaw = normalizeText(
      req.query.keywords ?? "creative, technology, manager, management"
    );
    const keywords = keywordsRaw
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);

    const sources = [
      { name: "greenhouse", run: () => fetchGreenhouseJobs() },
      { name: "indeed", run: () => fetchIndeedRss({ query: keywords.join(" "), location }) }
    ];

    const settled = await Promise.allSettled(sources.map((s) => s.run()));
    const jobs = settled.flatMap((r) => (r.status === "fulfilled" ? r.value : []));
    const sourceErrors = settled
      .map((r, idx) => ({ r, s: sources[idx] }))
      .filter(({ r }) => r.status === "rejected")
      .map(({ r, s }) => ({ source: s.name, error: String(r.reason?.message || r.reason) }));

    const filtered = jobs
      .filter((j) => inToronto(j.location || location))
      .filter((j) => includesAny(j.title, keywords))
      .filter((j) => !fullTimeOnly || j.employmentType === "full-time" || looksFullTime(j.title))
      .filter((j) => {
        if (!j.salary) return false;
        return j.salary.min >= minSalary || j.salary.max >= minSalary;
      })
      .sort((a, b) => (b.salary?.max ?? 0) - (a.salary?.max ?? 0));

    res.json({
      meta: {
        minSalary,
        fullTimeOnly,
        location,
        keywords,
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
