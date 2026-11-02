#!/usr/bin/env node
/**
 * Check that every job table in README.md is sorted newest-Posted-first.
 * Undated rows are allowed only after all dated rows within the same table.
 *
 * Usage: node scripts/check_readme_sort.mjs [path]
 * Exit code 1 when a table is out of order.
 */

import fs from "fs";
import path from "path";

const file = process.argv[2] || path.join(process.cwd(), "README.md");
const lines = fs.readFileSync(file, "utf8").split("\n");

const DATE_RE = /(\d{4}-\d{2}-\d{2})/;
let heading = "(top)";
let table = null;
const violations = [];
let tablesChecked = 0;

function flush() {
  if (!table) return;
  const { heading: h, rows } = table;
  tablesChecked++;
  let last = null;
  let undatedSeen = false;
  rows.forEach((row, i) => {
    const match = row.text.match(DATE_RE);
    if (!match) {
      undatedSeen = true;
      return;
    }
    const value = match[1];
    if (undatedSeen) {
      violations.push({ heading: h, line: row.line, why: "dated row after an undated row", value });
    }
    if (last && value > last.value) {
      violations.push({
        heading: h,
        line: row.line,
        why: `newer than previous row (${last.value} -> ${value})`,
        value,
      });
    }
    last = { value, line: row.line };
  });
  table = null;
}

lines.forEach((line, index) => {
  const trimmed = line.trim();
  if (trimmed.startsWith("|")) {
    const cells = trimmed.split("|").slice(1, -1).map((c) => c.trim());
    const isHeader = !table;
    if (isHeader) {
      if (cells.some((c) => /^posted/i.test(c))) {
        table = { heading, rows: [] };
      }
      return;
    }
    if (cells.every((c) => /^:?-{3,}:?$/.test(c))) return;
    if (table) table.rows.push({ line: index + 1, text: trimmed });
    return;
  }
  flush();
  if (trimmed.startsWith("#")) heading = trimmed.replace(/^#+\s*/, "");
});

flush();

if (violations.length === 0) {
  console.log(`OK: ${tablesChecked} Posted-column tables are newest-first (${file})`);
  process.exit(0);
}

console.log(`FAIL: ${violations.length} ordering problem(s) in ${tablesChecked} tables`);
for (const v of violations.slice(0, 60)) {
  console.log(`  line ${v.line} [${v.heading}] ${v.why}`);
}
process.exit(1);
