#!/usr/bin/env python3
"""
Build the GitHub Pages site from README.md's three curated tables.

Writes:
  public/jobs-data.json   machine-readable rows (includes derived `source`)
  public/index.html       self-contained page (inline data, no build step, no CDN)

Filters on the page:
  * one date window per family (Today / This week / This month / All), set
    independently for ServiceNow, Salesforce and Other
  * source filter (LinkedIn, Adzuna, Workday ATS, employer sites, ...)
  * free-text search across title, company and location
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from jobs_consolidate import README, extract_rows  # noqa: E402

PUBLIC = ROOT / "public"
FAMILY_LABEL = {
    "servicenow": "ServiceNow",
    "salesforce": "Salesforce",
    "other": "Other",
}

# host substring -> display label (first match wins)
SOURCE_RULES = [
    ("linkedin.com", "LinkedIn"),
    ("adzuna.", "Adzuna"),
    ("jobbank.gc.ca", "Job Bank"),
    ("myworkdayjobs.com", "Workday ATS"),
    ("greenhouse.io", "Greenhouse"),
    ("lever.co", "Lever"),
    ("smartrecruiters", "SmartRecruiters"),
    ("ashbyhq", "Ashby"),
    ("workable", "Workable"),
    ("indeed.", "Indeed"),
    ("jooble", "Jooble"),
    ("talent.com", "Talent.com"),
    ("eluta", "Eluta"),
    ("simplify.jobs", "Aggregator"),
    ("tealhq", "Aggregator"),
    ("glassdoor", "Glassdoor"),
]


def source_of(url: str) -> str:
    low = (url or "").lower()
    for needle, label in SOURCE_RULES:
        if needle in low:
            return label
    host = urlparse(url or "").netloc.replace("www.", "")
    return host or "unknown"


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
                "source": source_of(r["url"]),
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
  .controls { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:16px 0 6px; }
  .chips { display:flex; gap:8px; flex-wrap:wrap; }
  button { font:inherit; color:var(--text); background:var(--card); border:1px solid var(--edge); padding:6px 12px; border-radius:999px; cursor:pointer; }
  button:hover { border-color:var(--accent); }
  button.active { background:var(--accent); border-color:var(--accent); color:#fff; }
  input[type=search] { flex:1 1 220px; min-width:180px; background:var(--card); border:1px solid var(--edge); color:var(--text); padding:8px 12px; border-radius:8px; font:inherit; }
  .meta { color:var(--muted); font-size:13px; margin:10px 0 18px; }
  .meta b { color:var(--text); }
  section.fam { border-top:1px solid var(--edge); padding:18px 0 6px; }
  section.fam h2 { margin:0 0 4px; font-size:17px; }
  section.fam .hint { color:var(--muted); font-size:12.5px; margin-bottom:10px; }
  section.fam .chips { margin-bottom:12px; }
  .grid { display:grid; gap:10px; }
  .job { background:var(--card); border:1px solid var(--edge); border-radius:12px; padding:13px 15px; }
  .job h3 { margin:0 0 4px; font-size:15.5px; font-weight:600; }
  .job a { color:var(--text); text-decoration:none; }
  .job a:hover { color:var(--accent); }
  .job .row { color:var(--muted); font-size:13px; display:flex; gap:10px; flex-wrap:wrap; align-items:center; }
  .tag { font-size:11px; text-transform:uppercase; letter-spacing:.4px; padding:2px 7px; border-radius:999px; border:1px solid var(--edge); color:var(--muted); }
  .tag.servicenow { color:#7fc8a0; border-color:#2c5c45; }
  .tag.salesforce { color:#8fb4ff; border-color:#2f4a7d; }
  .tag.other { color:#d3b3ff; border-color:#4d3a6b; }
  .tag.today { color:var(--ok); border-color:#245c44; }
  .empty { color:var(--muted); padding:14px 0 18px; font-size:13.5px; }
  footer { color:var(--muted); font-size:12px; border-top:1px solid var(--edge); padding:18px 20px; }
  code { background:#0b0d11; border:1px solid var(--edge); padding:1px 5px; border-radius:5px; font-size:12px; }
</style>
</head>
<body>
<header>
  <h1>BESTIEJOB</h1>
  <div class="sub">ServiceNow · Salesforce · IT platform roles, Toronto-first. Each family has its own date window.</div>
</header>
<main>
  <div class="controls">
    <input type="search" id="q" placeholder="Search title, company or location…">
  </div>
  <div class="controls">
    <span class="sub">Source</span>
    <div class="chips" id="srcs"></div>
  </div>
  <div class="meta" id="meta"></div>
  <section class="fam" data-fam="servicenow">
    <h2>ServiceNow <span class="sub" id="count-servicenow"></span></h2>
    <div class="hint">developer / administrator / architect / analyst roles</div>
    <div class="chips" data-when="servicenow"></div>
    <div class="grid" id="list-servicenow"></div>
  </section>
  <section class="fam" data-fam="salesforce">
    <h2>Salesforce <span class="sub" id="count-salesforce"></span></h2>
    <div class="hint">developer / admin / architect / consultant roles</div>
    <div class="chips" data-when="salesforce"></div>
    <div class="grid" id="list-salesforce"></div>
  </section>
  <section class="fam" data-fam="other">
    <h2>Other <span class="sub" id="count-other"></span></h2>
    <div class="hint">ITSM / ITAM / CMDB / integration / BI and adjacent roles</div>
    <div class="chips" data-when="other"></div>
    <div class="grid" id="list-other"></div>
  </section>
</main>
<footer>
  Dates are the source posting dates, not relative “days ago” labels. Aggregator mirrors can expire —
  open the posting before applying. Data: <code>public/jobs-data.json</code> · built from README.md.
</footer>
<script>
const JOBS = __DATA__;
const TZ = "America/Toronto";
const FAMILIES = ["servicenow", "salesforce", "other"];
const WINDOWS = [["today","Today"],["week","This week"],["month","This month"],["all","All"]];
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
const state = { when: { servicenow:"all", salesforce:"all", other:"all" }, src:"all", q:"" };
const $ = (s) => document.querySelector(s);
const fmt = (s) => new Date(s + "T12:00:00Z").toLocaleDateString("en-CA", { weekday:"short", month:"short", day:"numeric", year:"numeric" });
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

// source chips, most common first
const srcCounts = {};
JOBS.forEach(j => { srcCounts[j.source] = (srcCounts[j.source] || 0) + 1; });
const srcList = Object.keys(srcCounts).sort((a,b) => srcCounts[b] - srcCounts[a]).slice(0, 10);
$("#srcs").innerHTML =
  `<button data-src="all" class="active">All sources</button>` +
  srcList.map(s => `<button data-src="${esc(s)}">${esc(s)} <span class="sub">${srcCounts[s]}</span></button>`).join("");

FAMILIES.forEach(f => {
  document.querySelector(`.chips[data-when="${f}"]`).innerHTML =
    WINDOWS.map(([k, label]) => `<button data-when-kind="${k}" class="${state.when[f] === k ? "active" : ""}">${label}</button>`).join("");
});

function matches(j, needle) {
  return !needle || (j.title + " " + j.company + " " + j.location).toLowerCase().includes(needle);
}

function render() {
  const needle = state.q.trim().toLowerCase();
  let shown = 0;
  const totals = { servicenow:0, salesforce:0, other:0 };
  FAMILIES.forEach(f => {
    const from = windowStart(state.when[f]);
    const list = JOBS.filter(j => j.family === f
      && (state.when[f] === "all" || j.posted >= from)
      && (state.src === "all" || j.source === state.src)
      && matches(j, needle));
    totals[f] = list.length;
    shown += list.length;
    $(`#count-${f}`).textContent = `${list.length} shown`;
    const host = $(`#list-${f}`);
    if (!list.length) {
      const why = state.when[f] === "today" ? `nothing dated ${TODAY}` : "no postings match these filters";
      host.innerHTML = `<div class="empty">${why}` +
        (state.when[f] === "today" ? ` — newest ${f} row is ${fmt(newest)}.` : "") + `</div>`;
      return;
    }
    host.innerHTML = list.map(j => `
      <article class="job">
        <h3><a href="${esc(j.url)}" target="_blank" rel="noopener">${esc(j.title)}</a></h3>
        <div class="row">
          <span class="tag ${j.family}">${esc(j.familyLabel)}</span>
          <span class="tag ${j.posted === TODAY ? "today" : ""}">${esc(j.posted)}</span>
          <span>${esc(j.company || "—")}</span>
          <span>${esc(j.location || "")}</span>
          <span class="tag">${esc(j.source)}</span>
        </div>
      </article>`).join("");
  });
  $("#meta").innerHTML =
    `<b>${shown}</b> of ${JOBS.length} postings shown · ServiceNow <b>${totals.servicenow}</b> · ` +
    `Salesforce <b>${totals.salesforce}</b> · Other <b>${totals.other}</b> · today is ${fmt(TODAY)} (America/Toronto)`;
}

document.querySelectorAll(".chips[data-when]").forEach(box => {
  box.addEventListener("click", (e) => {
    const b = e.target.closest("button"); if (!b) return;
    const fam = box.dataset.when;
    state.when[fam] = b.dataset.whenKind;
    [...box.children].forEach(x => x.classList.toggle("active", x === b));
    render();
  });
});
$("#srcs").addEventListener("click", (e) => {
  const b = e.target.closest("button"); if (!b) return;
  state.src = b.dataset.src;
  [...$("#srcs").children].forEach(x => x.classList.toggle("active", x === b));
  render();
});
$("#q").addEventListener("input", (e) => { state.q = e.target.value; render(); });
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
                "sources": sorted({d["source"] for d in data}),
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
    src = {}
    for d in data:
        src[d["source"]] = src.get(d["source"], 0) + 1
    top = sorted(src.items(), key=lambda kv: -kv[1])[:6]
    newest = max((d["posted"] for d in data), default="—")
    print(f"site: {len(data)} jobs {fam}, newest {newest} -> public/index.html")
    print(f"sources: {top}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
