#!/usr/bin/env node
/**
 * Sort README job tables newest-Posted-first.
 *
 * For every contiguous markdown table whose header contains a "Posted" column,
 * dated rows are sorted descending by date and undated rows are kept after them
 * (stable, so the previous order of undated rows is preserved).
 *
 * Usage: node scripts/sort_readme_tables.mjs [path]
 */

import fs from "fs";
import path from "path";

const file = process.argv[2] || path.join(process.cwd(), "README.md");
const lines = fs.readFileSync(file, "utf8").split("\n");
const DATE_RE = /(\d{4}-\d{2}-\d{2})/;

const out = [];
let i = 0;
let tablesSorted = 0;
let rowsMoved = 0;

while (i < lines.length) {
  if (!lines[i].trim().startsWith("|")) {
    out.push(lines[i]);
    i++;
    continue;
  }

  // Collect the whole table block.
  const start = i;
  const block = [];
  while (i < lines.length && lines[i].trim().startsWith("|")) {
    block.push(lines[i]);
    i++;
  }

  const headerCells = block[0].split("|").slice(1, -1).map((c) => c.trim());
  const postedIndex = headerCells.findIndex((c) => /^posted/i.test(c));
  const isSeparator = (line) => line.split("|").slice(1, -1).every((c) => /^:?-{3,}:?$/.test(c.trim()));

  if (postedIndex < 0 || block.length < 3 || !isSeparator(block[1])) {
    out.push(...block);
    continue;
  }

  const head = block.slice(0, 2);
  const rows = block.slice(2).map((text) => {
    const cells = text.split("|").slice(1, -1);
    const cell = (cells[postedIndex] || "").trim();
    const match = cell.match(DATE_RE);
    return { text, date: match ? match[1] : null };
  });

  const dated = rows.filter((r) => r.date);
  const undated = rows.filter((r) => !r.date);
  const before = rows.map((r) => r.date || "-").join(",");

  dated.sort((a, b) => (a.date < b.date ? 1 : a.date > b.date ? -1 : 0));

  const sorted = [...dated, ...undated];
  const after = sorted.map((r) => r.date || "-").join(",");
  if (before !== after) {
    tablesSorted++;
    rowsMoved += sorted.filter((r, idx) => r !== rows[idx]).length;
  }

  out.push(...head, ...sorted.map((r) => r.text));
}

fs.writeFileSync(file, out.join("\n"));
console.log(`Sorted ${tablesSorted} table(s); ${rowsMoved} row position(s) changed (${file})`);
