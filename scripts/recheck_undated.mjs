#!/usr/bin/env node
/**
 * Re-check the undated postings sitting in inbox/ and promote them the moment
 * the employer starts publishing a posted date.
 *
 * Gap-scan submissions file partner postings with an em dash in the Posted
 * column because those pages published no date at all (Lane Four, Ateko,
 * Cofomo…). Some of those pages are evergreen listings that later gain a real
 * `datePosted`, and a human should not have to remember to look again.
 *
 * This script reads every undated row, re-fetches the page, and classifies it:
 *
 *   fresh   date found inside the window, within the posted_date field of the
 *           page's JobPosting JSON-LD                          → promoted
 *   stale   a date exists but is older than the window (or is obviously a
 *           page-creation artefact, e.g. a 2021 datePublished) → reported only
 *   undated still no date on the page                          → reported only
 *   error   page unreachable                                   → reported only
 *
 * Promoted rows are written to `inbox/undated-recheck--<date>--v<N>.md` as a
 * normal submission, so the usual merge step moves them into README and the
 * page. Nothing is promoted on a guess: only a date the page itself exposes
 * counts.
 *
 * Usage:
 *   node scripts/recheck_undated.mjs             # all undated rows
 *   node scripts/recheck_undated.mjs --dry-run   # report, write nothing
 *   node scripts/recheck_undated.mjs --max 50    # cap pages fetched
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const INBOX = path.join(ROOT, "inbox");

const FLAGS = new Set(process.argv.slice(2));
const DRY = FLAGS.has("--dry-run");
const MAX_ARG = process.argv.indexOf("--max");
const MAX_PAGES = MAX_ARG > -1 ? Number(process.argv[MAX_ARG + 1]) || 60 : 60;

const NOW = new Date();
const NOW_ISO = NOW.toISOString();
const ISO = NOW_ISO.slice(0, 10);
const MAX_AGE_DAYS = 31;
const MODEL = "undated-recheck";
const UA =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36";

const UNDATED_MARKERS = new Set(["", "—", "–", "-", "?", "n/a", "na", "unknown", "tbd", "none"]);

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

/** Every row in inbox/ whose Posted cell says "no date published". */
function undatedRows() {
  const rows = [];
  const seen = new Set();
  if (!fs.existsSync(INBOX)) return rows;

  const files = fs
    .readdirSync(INBOX)
    .filter((f) => f.toLowerCase().endsWith(".md") && !/^(_|template|readme)/i.test(f));

  for (const file of files) {
    const text = fs.readFileSync(path.join(INBOX, file), "utf8");
    for (const line of text.split("\n")) {
      const trimmed = line.trim();
      if (!trimmed.startsWith("|")) continue;
      const cells = trimmed.replace(/^\||\|$/g, "").split("|").map((c) => c.trim());
      if (cells.length < 5) continue;
      if (cells[0].toLowerCase() === "posted") continue;
      if (!UNDATED_MARKERS.has(cells[0].toLowerCase())) continue;

      const link = trimmed.match(/\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/);
      const bare = trimmed.match(/https?:\/\/[^\s|)\]]+/);
      const url = link ? link[2] : bare ? bare[0] : null;
      if (!url) continue;
      const key = urlKey(url);
      if (seen.has(key)) continue;
      seen.add(key);
      rows.push({
        title: (link ? link[1] : cells[1] || "").replace(/\s+/g, " ").trim(),
        company: cells[2] || "",
        location: cells[3] || "",
        url,
        origin: file,
      });
    }
  }
  return rows;
}

function dateFromLd(html) {
  const blocks = [...html.matchAll(/<script[^>]+application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi)];
  for (const [, raw] of blocks) {
    let data;
    try {
      data = JSON.parse(raw.trim());
    } catch {
      continue;
    }
    const queue = Array.isArray(data) ? data : [data];
    while (queue.length) {
      const node = queue.shift();
      if (!node || typeof node !== "object") continue;
      if (Array.isArray(node)) {
        queue.push(...node);
        continue;
      }
      if (node["@graph"]) queue.push(node["@graph"]);
      const type = node["@type"];
      const isPosting = Array.isArray(type) ? type.includes("JobPosting") : type === "JobPosting";
      if (isPosting) {
        const posted = toIso(node.datePosted || node.datePublished);
        if (posted) return posted;
      }
      for (const value of Object.values(node)) {
        if (value && typeof value === "object") queue.push(value);
      }
    }
  }
  return null;
}

function dateFromVisibleText(html) {
  const text = html
    .replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ");
  const m = text.match(
    /(?:posted|date posted|publication date|publi[ée]e? le)\D{0,20}(\d{4}-\d{2}-\d{2}|\d{1,2}\s+\w+\s+\d{4})/i
  );
  return m ? toIso(m[1]) : null;
}

async function probe(url) {
  try {
    const res = await fetch(url, {
      headers: { "User-Agent": UA, "Accept-Language": "en-CA,en;q=0.9" },
      redirect: "follow",
      signal: AbortSignal.timeout(20000),
    });
    if (!res.ok) return { status: "error", detail: `HTTP ${res.status}` };
    const html = await res.text();
    const posted = dateFromLd(html) || dateFromVisibleText(html);
    if (!posted) return { status: "undated", detail: "no JobPosting date, no visible Posted label" };
    const ageDays = (NOW - new Date(posted)) / 864e5;
    if (ageDays < -2) return { status: "stale", posted, detail: `date in the future (${posted.slice(0, 10)})` };
    if (ageDays > MAX_AGE_DAYS) {
      return { status: "stale", posted, detail: `posted ${posted.slice(0, 10)} (${Math.round(ageDays)} days ago)` };
    }
    return { status: "fresh", posted, detail: `posted ${posted.slice(0, 10)}` };
  } catch (err) {
    return { status: "error", detail: String(err.message || err).slice(0, 90) };
  }
}

async function mapLimit(items, limit, fn) {
  const out = new Array(items.length);
  let i = 0;
  await Promise.all(
    Array.from({ length: Math.min(limit, items.length) }, async () => {
      while (i < items.length) {
        const idx = i++;
        out[idx] = await fn(items[idx], idx);
      }
    })
  );
  return out;
}

function nextVersion() {
  const re = new RegExp(`^${MODEL}--${ISO}--v(\\d+)\\.md$`, "i");
  let max = 0;
  try {
    for (const f of fs.readdirSync(INBOX)) {
      const m = f.match(re);
      if (m) max = Math.max(max, Number(m[1]));
    }
  } catch {
    /* no inbox */
  }
  return max + 1;
}

function mdCell(v) {
  return String(v ?? "").replace(/\|/g, "/").replace(/\s+/g, " ").trim();
}

async function main() {
  console.log(`[recheck] start ${NOW_ISO}${DRY ? " (dry run)" : ""}`);
  const rows = undatedRows().slice(0, MAX_PAGES);
  if (!rows.length) {
    console.log("[recheck] no undated rows in inbox/ — nothing to re-check");
    return;
  }
  console.log(`[recheck] ${rows.length} undated row(s) to re-check`);

  const results = await mapLimit(rows, 4, async (row) => ({ row, ...(await probe(row.url)) }));

  const buckets = { fresh: [], stale: [], undated: [], error: [] };
  for (const r of results) buckets[r.status].push(r);

  for (const r of results) {
    const label = r.status.padEnd(7);
    console.log(`[recheck] ${label} ${r.row.title.slice(0, 54).padEnd(54)} ${r.detail}`);
  }
  console.log(
    `[recheck] fresh=${buckets.fresh.length} stale=${buckets.stale.length} ` +
      `undated=${buckets.undated.length} error=${buckets.error.length}`
  );

  if (!buckets.fresh.length) {
    console.log("[recheck] nothing gained a usable posted date — no submission written");
    return;
  }

  const lines = [
    "---",
    `model: ${MODEL}`,
    `scanned_at: ${NOW_ISO}`,
    "task: promote previously undated postings",
    `notes: ${rows.length} re-checked; ${buckets.fresh.length} now publish a posted date inside the ${MAX_AGE_DAYS}-day window.`,
    "---",
    "",
    `# Undated postings that gained a date — ${ISO}`,
    "",
    "| Posted | Role | Company | Location | URL | Note |",
    "|---|---|---|---|---|---|",
  ];
  for (const r of buckets.fresh) {
    lines.push(
      `| ${r.posted.slice(0, 10)} | [${mdCell(r.row.title)}](${r.row.url}) | ${mdCell(r.row.company)} | ${mdCell(r.row.location || "Canada")} | ${r.row.url} | was undated in ${mdCell(r.row.origin)}; page now publishes ${r.detail} |`
    );
  }

  if (DRY) {
    console.log("[recheck] dry run — would write:");
    console.log(lines.slice(8).join("\n"));
    return;
  }

  fs.mkdirSync(INBOX, { recursive: true });
  const target = path.join(INBOX, `${MODEL}--${ISO}--v${nextVersion()}.md`);
  fs.writeFileSync(target, lines.join("\n") + "\n", "utf8");
  console.log(`[recheck] wrote inbox/${path.basename(target)} (+${buckets.fresh.length} promoted)`);
}

main().catch((err) => {
  console.error("[recheck] fatal:", err);
  process.exit(1);
});
