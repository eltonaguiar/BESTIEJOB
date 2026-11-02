#!/usr/bin/env python3
"""
Build the GitHub Pages site from README.md's three curated tables.

Writes:
  public/jobs-data.json   machine-readable rows
  public/index.html       self-contained page (inline data, no build step, no CDN)

Filters on the page: Today (America/Toronto), This week, This month, All,
plus family tabs (ServiceNow / Salesforce / Other) and free-text search.
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from jobs_consolidate import README, extract_rows  # noqa: E402

PUBLIC = ROOT / "public"
FAMILY_LABEL = {
    "servicenow": "ServiceNow",
    "salesforce": "Salesforce",
    "other": "Other",
}


def rows() -> list[dict]:
    parsed, _ = extract_rows(README.read_text(encoding="utf-8"))
    seen: set[str] = set()
    out: list[dict] = []
    for r in parsed:
        key = r["url"].split("?")[0].rstrip("/").lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(
            {
                "posted": r["posted"],
                "title": r["title"],
                "company": r["company"],
                "location": r["location"],
                "url": r["url"],
                "note": r["note"][:160],
                "family": r["family"],
                "familyLabel": FAMILY_LABEL.get(r["family"], "Other"),
            }
        )
    out.sort(key=lambda r: (r["posted"], r["title"]), reverse=True)
    return out


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BESTIEJOB — ServiceNow, Salesforce &amp; IT platform jobs</title>
<style>
  :root { --bg:#0f1115; --card:#171a21; --edge:#262b36; --text:#e8ebf0; --muted:#9aa4b2; --accent:#5b8cff; --ok:#38b27a; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--text); font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  header { padding:28px 20px 16px; border-bottom:1px solid var(--edge); }
  h1 { margin:0 0 6px; font-size:22px; letter-spacing:-.2px; }
  .sub { color:var(--muted); font-size:13px; }
  main { max-width:1080px; margin:0 auto; padding:18px 20px 60px; }
  .controls { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:18px 0 6px; }
  .chips { display:flex; gap:8px; flex-wrap:wrap; }
  button { font:inherit; color:var(--text); background:var(--card); border:1px solid var(--edge); padding:7px 13px; border-radius:999px; cursor:pointer; }
  button:hover { border-color:var(--accent); }
  button.active { background:var(--accent); border-color:var(--accent); color:#fff; }
  input[type=search] { flex:1 1 220px; min-width:180px; background:var(--card); border:1px solid var(--edge); color:var(--text); padding:8px 12px; border-radius:8px; font:inherit; }
  .meta { color:var(--muted); font-size:13px; margin:10px 0 18px; }
  .meta b { color:var(--text); }
  .grid { display:grid; gap:10px; }
  .job { background:var(--card); border:1px solid var(--edge); border-radius:12px; padding:13px 15px; }
  .job h3 { margin:0 0 4px; font-size:15.5px; font-weight:600; }
  .job a { color:var(--text); text-decoration:none; }
  .job a:hover { color:var(--accent); }
  .job .row { color:var(--muted); font-size:13px; display:flex; gap:10px; flex-wrap:wrap; }
  .tag { font-size:11px; text-transform:uppercase; letter-spacing:.4px; padding:2px 7px; border-radius:999px; border:1px solid var(--edge); color:var(--muted); }
  .tag.servicenow { color:#7fc8a0; border-color:#2c5c45; }
  .tag.salesforce { color:#8fb4ff; border-color:#2f4a7d; }
  .tag.other { color:#d3b3ff; border-color:#4d3a6b; }
  .today { color:var(--ok); border-color:#245c44; }
  .empty { color:var(--muted); padding:26px 0; }
  footer { color:var(--muted); font-size:12px; border-top:1px solid var(--edge); padding:18px 20px; }
  code { background:#0b0d11; border:1px solid var(--edge); padding:1px 5px; border-radius:5px; font-size:12px; }
</style>
</head>
<body>
<header>
  <h1>BESTIEJOB</h1>
  <div class="sub">ServiceNow · Salesforce · IT platform roles, Toronto-first. Postings from the curated README tables.</div>
</header>
<main>
  <div class="controls">
    <div class="chips" id="when">
      <button data-when="today" class="active">Today</button>
      <button data-when="week">This week</button>
      <button data-when="month">This month</button>
      <button data-when="all">All</button>
    </div>
    <input type="search" id="q" placeholder="Search title, company or location…">
  </div>
  <div class="controls">
    <div class="chips" id="fam">
      <button data-fam="all" class="active">All families</button>
      <button data-fam="servicenow">ServiceNow</button>
      <button data-fam="salesforce">Salesforce</button>
      <button data-fam="other">Other</button>
    </div>
  </div>
  <div class="meta" id="meta"></div>
  <div class="grid" id="list"></div>
</main>
<footer>
  Dates are the source posting dates, not relative “days ago” labels. Aggregator mirrors can expire —
  open the posting before applying. Data: <code>public/jobs-data.json</code> · built from README.md.
</footer>
<script>
const JOBS = __DATA__;
const TZ = "America/Toronto";
const iso = (d) => d.toISOString().slice(0,10);
function todayInTz() {
  const parts = new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year:"numeric", month:"2-digit", day:"2-digit" }).formatToParts(new Date());
  const g = (t) => parts.find(p => p.type === t).value;
  return `${g("year")}-${g("month")}-${g("day")}`;
}
const TODAY = todayInTz();
const newest = JOBS.length ? JOBS[0].posted : TODAY;
function windowStart(kind) {
  if (kind === "today") return TODAY;
  if (kind === "week") { const d = new Date(TODAY + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - 6); return iso(d); }
  if (kind === "month") { const d = new Date(TODAY + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - 29); return iso(d); }
  return "0000-00-00";
}
let when = "today", fam = "all", q = "";
const $ = (s) => document.querySelector(s);
const fmt = (s) => new Date(s + "T12:00:00Z").toLocaleDateString("en-CA", { weekday:"short", month:"short", day:"numeric", year:"numeric" });

function render() {
  const from = windowStart(when);
  const needle = q.trim().toLowerCase();
  const list = JOBS.filter(j =>
    (when === "all" || j.posted >= from) &&
    (fam === "all" || j.family === fam) &&
    (!needle || (j.title + " " + j.company + " " + j.location).toLowerCase().includes(needle))
  );
  const counts = { servicenow:0, salesforce:0, other:0 };
  list.forEach(j => counts[j.family]++);
  let label;
  if (when === "today") label = `Today — ${fmt(TODAY)} (America/Toronto)`;
  else if (when === "week") label = `Last 7 days — ${fmt(from)} → ${fmt(TODAY)}`;
  else if (when === "month") label = `Last 30 days — ${fmt(from)} → ${fmt(TODAY)}`;
  else label = `All ${JOBS.length} postings in the tables`;
  $("#meta").innerHTML = `${label} · <b>${list.length}</b> shown · ServiceNow <b>${counts.servicenow}</b> · Salesforce <b>${counts.salesforce}</b> · Other <b>${counts.other}</b>` + (when === "today" && !list.length ? ` · newest data is ${fmt(newest)}` : "");
  if (!list.length) {
    $("#list").innerHTML = `<div class="empty">No postings ${when === "today" ? `dated ${TODAY} (America/Toronto)` : "match this filter"}. ${when === "today" ? `Try <b>This week</b> — the newest row is ${fmt(newest)}.` : ""}</div>`;
    return;
  }
  $("#list").innerHTML = list.map(j => `
    <article class="job">
      <h3><a href="${j.url}" target="_blank" rel="noopener">${j.title}</a></h3>
      <div class="row">
        <span class="tag ${j.family}">${j.familyLabel}</span>
        <span class="tag ${j.posted === TODAY ? "today" : ""}">${j.posted}</span>
        <span>${j.company || "—"}</span>
        <span>${j.location || ""}</span>
      </div>
    </article>`).join("");
}
$("#when").addEventListener("click", (e) => {
  const b = e.target.closest("button"); if (!b) return;
  when = b.dataset.when;
  [...$("#when").children].forEach(x => x.classList.toggle("active", x === b));
  render();
});
$("#fam").addEventListener("click", (e) => {
  const b = e.target.closest("button"); if (!b) return;
  fam = b.dataset.fam;
  [...$("#fam").children].forEach(x => x.classList.toggle("active", x === b));
  render();
});
$("#q").addEventListener("input", (e) => { q = e.target.value; render(); });
render();
</script>
</body>
</html>
"""


def main() -> int:
    data = rows()
    PUBLIC.mkdir(exist_ok=True)
    (PUBLIC / "jobs-data.json").write_text(
        json.dumps(
            {
                "generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "timezone": "America/Toronto",
                "count": len(data),
                "jobs": data,
            },
            ensure_ascii=False,
            indent=1,
        ),
        encoding="utf-8",
    )
    (PUBLIC / "index.html").write_text(
        HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/")),
        encoding="utf-8",
    )
    fam = {k: sum(1 for d in data if d["family"] == k) for k in FAMILY_LABEL}
    newest = max((d["posted"] for d in data), default="—")
    print(f"site: {len(data)} jobs {fam}, newest {newest} -> public/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
