#!/usr/bin/env python3
"""
Build the GitHub Pages site from README.md's curated tables.

Writes:
  public/jobs-data.json   rows + derived `source`, `match` (resume fit), reasons
  public/index.html       self-contained page (inline data, no build step, no CDN)

UI
  * tabs: ServiceNow / Salesforce / Other / Best match, each with its own date window
  * a resume-fit score (0-100) with the reasons printed on the card
  * every card carries a real anchor to the posting (title + "Open posting")
  * source filter, and search that understands synonyms and accents
  * a "Last updated" build stamp in the header

Anything that reaches this file must keep `class="apply"` and the title anchor:
they are the only reason the page is useful. tools/check_site_links.py asserts it.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from jobs_consolidate import README, extract_rows  # noqa: E402

PUBLIC = ROOT / "public"
FAMILY_LABEL = {"servicenow": "ServiceNow", "salesforce": "Salesforce", "other": "Other"}

SOURCE_RULES = [
    ("linkedin.com", "LinkedIn"), ("adzuna.", "Adzuna"), ("jobbank.gc.ca", "Job Bank"),
    ("myworkdayjobs.com", "Workday ATS"), ("greenhouse.io", "Greenhouse"),
    ("lever.co", "Lever"), ("smartrecruiters", "SmartRecruiters"), ("ashbyhq", "Ashby"),
    ("workable", "Workable"), ("indeed.", "Indeed"), ("jooble", "Jooble"),
    ("talent.com", "Talent.com"), ("eluta", "Eluta"), ("monster.", "Monster"),
    ("simplify.jobs", "Aggregator"), ("tealhq", "Aggregator"), ("glassdoor", "Glassdoor"),
    ("jobs.ca", "jobs.ca"), ("workopolis", "Workopolis"),
]

# resume fit: (pattern, weight, label)
PROFILE = [
    (r"service\s*now|servicenow|\bsnow\b", 34, "ServiceNow"),
    (r"itsm|incident|problem management|change management|service catalog|service desk|request fulfil", 13, "ITSM"),
    (r"itam|asset management|sam pro|software asset|hardware asset", 13, "ITAM"),
    (r"cmdb|csdm", 13, "CMDB"),
    (r"itom|discovery|service mapping|event management", 11, "ITOM"),
    (r"flow designer|workflow design|orchestration", 9, "Flow Designer"),
    (r"glide|script include|business rule|client script|ui policy|ui action", 9, "ServiceNow scripting"),
    (r"integration hub|mulesoft|boomi|scripted rest|rest api|soap api|integration", 9, "Integration"),
    (r"salesforce|apex|lightning|soql|visualforce|\bcpq\b|marketing cloud|sfmc", 20, "Salesforce"),
    (r"itil|service management framework", 8, "ITIL"),
    (r"grc|risk management|vulnerability|black duck|compliance report", 7, "Risk/GRC"),
    (r"javascript|typescript|node\.js|\bhtml\b|\bcss\b", 7, "JavaScript"),
    (r"sql|python|databricks|alteryx|tableau|power ?bi|qlik", 6, "Data/reporting"),
    (r"powershell|\bvba\b|automation", 5, "Automation"),
    (r"sam pro|\bham\b|\bsam\b|software asset", 10, "SAM/HAM"),
    (r"import set|transform map|mid server|identification and reconcil|\bire\b", 8, "Import sets/IRE"),
    (r"splunk|aiops|monitoring|observability", 6, "AIOps"),
    (r"spm|portfolio management|\bppm\b", 6, "SPM/PPM"),
    (r"hr service delivery|hrsd|hr case|employee center|virtual agent", 5, "HRSD / VA"),
    (r"platform analytic|performance analytic|dashboard|kpi", 6, "Analytics"),
    (r"siem|\bsox\b|audit|access control|\bacl\b", 5, "Controls/ACL"),
    (r"service delivery|it operations|support analyst|operations analyst|service desk lead", 5, "IT operations"),
    (r"technical consultant|solution consultant|platform analyst|business analyst|\bba\b", 5, "Consulting/BA"),
    (r"administrator|\badmin\b|developer|engineer|architect|consultant|analyst|lead|specialist|manager", 4, "Role fit"),
]

WEAK_OTHER = re.compile(
    r"sales\s+(representative|associate|manager|consultant|lead|agent)|account executive|"
    r"retail|store manager|cashier|teller|barista|warehouse|driver|nurse|teacher", re.I)


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def source_of(url: str) -> str:
    low = (url or "").lower()
    for needle, label in SOURCE_RULES:
        if needle in low:
            return label
    host = urlparse(url or "").netloc.replace("www.", "")
    return host or "unknown"


def match_score(row: dict) -> tuple[int, list[str]]:
    hay = strip_accents(" ".join([row["title"], row["location"], row.get("note", ""),
                                  row.get("company", "")])).lower()
    title = strip_accents(row["title"]).lower()
    score, reasons = 0, []
    for pattern, weight, label in PROFILE:
        if re.search(pattern, hay):
            score += weight * (2 if re.search(pattern, title) else 1)
            reasons.append(label)
    loc = strip_accents(row["location"]).lower()
    if re.search(r"toronto|ontario|\bgta\b|mississauga|markham|brampton|north york|scarborough", loc):
        score += 12
        reasons.append("Toronto area")
    elif re.search(r"canada|remote", loc):
        score += 8
        reasons.append("Canada / remote")
    elif re.search(r"montreal|montr|quebec|laval|brossard|drummondville|sherbrooke", loc):
        score += 4
        reasons.append("Quebec")
    if WEAK_OTHER.search(title):
        score = int(score * 0.35)
        reasons.append("weak title match")
    return min(100, score), reasons[:5]


def rows() -> list[dict]:
    parsed, _ = extract_rows(README.read_text(encoding="utf-8"))
    seen: set[str] = set()
    out: list[dict] = []
    for r in parsed:
        url = (r.get("url") or "").strip()
        if not url.startswith("http"):
            continue
        key = url.split("?")[0].rstrip("/").lower()
        if key in seen:
            continue
        seen.add(key)
        row = {
            "posted": r["posted"],
            "title": r["title"],
            "company": r["company"],
            "location": r["location"],
            "url": url,
            "note": r["note"][:160],
            "family": r["family"],
            "familyLabel": FAMILY_LABEL.get(r["family"], "Other"),
            "source": source_of(url),
        }
        score, reasons = match_score(row)
        row["match"] = score
        row["matchReasons"] = reasons
        row["search"] = strip_accents(" ".join([
            row["title"], row["company"], row["location"], row["source"],
            row["familyLabel"], row["note"], " ".join(reasons)])).lower()
        out.append(row)
    out.sort(key=lambda r: (r["posted"], r["match"]), reverse=True)
    return out


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BESTIEJOB — ServiceNow, Salesforce &amp; IT platform jobs</title>
<style>
  :root { --bg:#0f1115; --card:#171a21; --edge:#262b36; --text:#e8ebf0; --muted:#9aa4b2; --accent:#5b8cff; --ok:#38b27a; --warn:#e0b252; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--text); font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  header { padding:26px 20px 0; border-bottom:1px solid var(--edge); }
  h1 { margin:0 0 4px; font-size:22px; letter-spacing:-.2px; }
  .sub { color:var(--muted); font-size:13px; }
  main { max-width:1080px; margin:0 auto; padding:16px 20px 60px; }
  .tabs { display:flex; gap:6px; flex-wrap:wrap; padding:14px 20px 0; max-width:1080px; margin:0 auto; }
  .tabs button { border-radius:10px 10px 0 0; border-bottom-color:transparent; }
  .tabs button.active { background:var(--card); border-color:var(--edge); color:var(--text); box-shadow:inset 0 2px 0 var(--accent); }
  .tabs button .n { color:var(--muted); font-size:12px; margin-left:5px; }
  .controls { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:14px 0 8px; }
  .chips { display:flex; gap:8px; flex-wrap:wrap; }
  button { font:inherit; color:var(--text); background:var(--card); border:1px solid var(--edge); padding:6px 12px; border-radius:999px; cursor:pointer; }
  button:hover { border-color:var(--accent); }
  .chips button.active { background:var(--accent); border-color:var(--accent); color:#fff; }
  input[type=search] { flex:1 1 240px; min-width:190px; background:var(--card); border:1px solid var(--edge); color:var(--text); padding:9px 12px; border-radius:8px; font:inherit; }
  select { background:var(--card); border:1px solid var(--edge); color:var(--text); padding:8px 10px; border-radius:8px; font:inherit; }
  .meta { color:var(--muted); font-size:13px; margin:10px 0 16px; }
  .meta b { color:var(--text); }
  .grid { display:grid; gap:10px; }
  .job { background:var(--card); border:1px solid var(--edge); border-radius:12px; padding:13px 15px; }
  .job h3 { margin:0 0 5px; font-size:15.5px; font-weight:600; }
  .job a { color:var(--text); text-decoration:none; }
  .job a:hover { color:var(--accent); }
  .job .row { color:var(--muted); font-size:13px; display:flex; gap:9px; flex-wrap:wrap; align-items:center; }
  .job .applyrow { margin-top:8px; display:flex; gap:10px; flex-wrap:wrap; align-items:center; color:var(--muted); font-size:12.5px; }
  .job a.apply { color:var(--accent); font-weight:600; text-decoration:none; }
  .job a.apply:hover { text-decoration:underline; }
  .tag { font-size:11px; text-transform:uppercase; letter-spacing:.4px; padding:2px 7px; border-radius:999px; border:1px solid var(--edge); color:var(--muted); }
  .tag.servicenow { color:#7fc8a0; border-color:#2c5c45; }
  .tag.salesforce { color:#8fb4ff; border-color:#2f4a7d; }
  .tag.other { color:#d3b3ff; border-color:#4d3a6b; }
  .tag.today { color:var(--ok); border-color:#245c44; }
  .tag.match { color:var(--warn); border-color:#5c4a24; }
  .empty { color:var(--muted); padding:18px 0; font-size:13.5px; }
  footer { color:var(--muted); font-size:12px; border-top:1px solid var(--edge); padding:18px 20px; }
  code { background:#0b0d11; border:1px solid var(--edge); padding:1px 5px; border-radius:5px; font-size:12px; }
</style>
</head>
<body>
<header>
  <h1>BESTIEJOB</h1>
  <div class="sub">ServiceNow · Salesforce · IT platform roles. <b>Other</b> is ranked by fit to the profile; <b>Best match</b> collects strong fits from every family.</div>
  <div class="sub" id="updated" style="margin-top:6px"></div>
</header>
<div class="tabs" id="tabs"></div>
<main>
  <div class="controls">
    <input type="search" id="q" placeholder="Search title, company, location… try “snow dev”, “sf admin”, “montreal”, “cmdb”">
    <select id="src"></select>
  </div>
  <div class="controls"><div class="chips" id="when"></div></div>
  <div class="meta" id="meta"></div>
  <div class="grid" id="list"></div>
</main>
<footer>
  Dates are source posting dates, not relative “days ago” labels. Aggregator mirrors can expire — open the
  posting before applying. <span id="counts"></span> · data: <code>public/jobs-data.json</code>
</footer>
<script>
const JOBS = __DATA__;
const TZ = "America/Toronto";
const TABS = [
  ["servicenow", "ServiceNow", j => j.family === "servicenow"],
  ["salesforce", "Salesforce", j => j.family === "salesforce"],
  ["other", "Other", j => j.family === "other"],
  ["match", "★ Best match", j => j.match >= 45]
];
const WINDOWS = [["today","Today"],["week","This week"],["month","This month"],["all","All"]];
const SYN = { snow:"servicenow", sn:"servicenow", snadmin:"servicenow", sf:"salesforce",
  sfdc:"salesforce", sfadmin:"salesforce", admin:"administrator", dev:"developer",
  eng:"engineer", sr:"senior", jr:"junior", ba:"analyst", gta:"toronto", yyz:"toronto",
  mtl:"montreal", itsm:"itsm", itam:"itam", qa:"qa", bi:"bi" };
const iso = (d) => d.toISOString().slice(0,10);
function stripAccents(s) { return s.normalize("NFKD").replace(/[\\u0300-\\u036f]/g, ""); }
function todayInTz() {
  const parts = new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year:"numeric", month:"2-digit", day:"2-digit" }).formatToParts(new Date());
  const g = (t) => parts.find(p => p.type === t).value;
  return `${g("year")}-${g("month")}-${g("day")}`;
}
const TODAY = todayInTz();
const newest = JOBS.length ? JOBS[0].posted : TODAY;
const UPDATED = "__BUILT__";
function windowStart(kind) {
  if (kind === "today") return TODAY;
  if (kind === "week") { const d = new Date(TODAY + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - 6); return iso(d); }
  if (kind === "month") { const d = new Date(TODAY + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() - 29); return iso(d); }
  return "0000-00-00";
}
const state = { tab: "servicenow", when: { servicenow:"all", salesforce:"all", other:"all", match:"all" }, src:"all", q:"" };
const $ = (s) => document.querySelector(s);
const fmt = (s) => new Date(s + "T12:00:00Z").toLocaleDateString("en-CA", { weekday:"short", month:"short", day:"numeric", year:"numeric" });
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));

const srcCounts = {};
JOBS.forEach(j => { srcCounts[j.source] = (srcCounts[j.source] || 0) + 1; });
$("#src").innerHTML = `<option value="all">All sources (${JOBS.length})</option>` +
  Object.keys(srcCounts).sort((a,b) => srcCounts[b] - srcCounts[a])
    .map(s => `<option value="${esc(s)}">${esc(s)} (${srcCounts[s]})</option>`).join("");

function tabCounts() { const c = {}; TABS.forEach(([k,,fn]) => { c[k] = JOBS.filter(fn).length; }); return c; }
function renderTabs() {
  const c = tabCounts();
  $("#tabs").innerHTML = TABS.map(([key, label]) =>
    `<button data-tab="${key}" class="${state.tab === key ? "active" : ""}">${label}<span class="n">${c[key]}</span></button>`).join("");
}
function renderWindows() {
  $("#when").innerHTML = WINDOWS.map(([k, label]) =>
    `<button data-when-kind="${k}" class="${state.when[state.tab] === k ? "active" : ""}">${label}</button>`).join("");
}
function tokens(q) {
  return stripAccents(q.toLowerCase()).replace(/[^a-z0-9 ]/g, " ").split(/\\s+/)
    .filter(Boolean).map(t => SYN[t] || t);
}
function searchMatch(job, toks) {
  if (!toks.length) return true;
  const hay = job.search || "";
  return toks.every(t => hay.includes(t));
}

function render() {
  const tabDef = TABS.find(t => t[0] === state.tab) || TABS[0];
  const from = windowStart(state.when[state.tab]);
  const toks = tokens(state.q);
  let list = JOBS.filter(j => tabDef[2](j)
    && (state.when[state.tab] === "all" || j.posted >= from)
    && (state.src === "all" || j.source === state.src)
    && searchMatch(j, toks));
  if (state.tab === "other" || state.tab === "match") {
    list.sort((a, b) => (b.match - a.match) || (b.posted > a.posted ? 1 : -1));
  }
  const label = state.tab === "match" ? "strong resume fits (score ≥ 45)"
    : state.tab === "other" ? "adjacent roles, best fit first" : "core roles";
  const win = state.when[state.tab];
  const whenLabel = win === "today" ? `Today — ${fmt(TODAY)} (America/Toronto)`
    : win === "week" ? `Last 7 days — ${fmt(from)} → ${fmt(TODAY)}`
    : win === "month" ? `Last 30 days — ${fmt(from)} → ${fmt(TODAY)}` : "All dates";
  $("#meta").innerHTML = `${tabDef[1]} · ${label} · <b>${list.length}</b> shown · ${whenLabel}` +
    (state.src !== "all" ? ` · source <b>${esc(state.src)}</b>` : "") +
    (toks.length ? ` · search “${esc(state.q)}”` : "");
  if (!list.length) {
    $("#list").innerHTML = `<div class="empty">No postings match. ${win === "today" ? `Nothing dated ${TODAY} in this tab — newest row is ${fmt(newest)}.` : "Try another date window, source, or search term."}</div>`;
    return;
  }
  $("#list").innerHTML = list.map(j => `
    <article class="job">
      <h3><a href="${esc(j.url)}" target="_blank" rel="noopener noreferrer">${esc(j.title)}</a></h3>
      <div class="row">
        <span class="tag ${j.family}">${esc(j.familyLabel)}</span>
        <span class="tag ${j.posted === TODAY ? "today" : ""}">${esc(j.posted)}</span>
        <span class="tag match" title="${esc((j.matchReasons||[]).join(', '))}">fit ${j.match}</span>
        <span>${esc(j.company || "—")}</span>
        <span>${esc(j.location || "")}</span>
        <span class="tag">${esc(j.source)}</span>
      </div>
      <div class="applyrow">
        <a class="apply" href="${esc(j.url)}" target="_blank" rel="noopener noreferrer">Open posting &#8599;</a>
        <span>${esc((j.matchReasons || []).join(" · "))}</span>
      </div>
    </article>`).join("");
}

$("#tabs").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-tab]"); if (!b) return;
  state.tab = b.dataset.tab; renderTabs(); renderWindows(); render();
});
$("#when").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-when-kind]"); if (!b) return;
  state.when[state.tab] = b.dataset.whenKind; renderWindows(); render();
});
$("#src").addEventListener("change", (e) => { state.src = e.target.value; render(); });
$("#q").addEventListener("input", (e) => { state.q = e.target.value; render(); });

$("#updated").textContent = `Last updated ${UPDATED} · ${JOBS.length} postings indexed`;
$("#counts").textContent = `${JOBS.length} postings indexed · ` +
  TABS.map(([k, label]) => `${label} ${JOBS.filter(t => t[2]).length}`).join(" · ");
renderTabs(); renderWindows(); render();
</script>
</body>
</html>
"""


def main() -> int:
    data = rows()
    PUBLIC.mkdir(exist_ok=True)
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    (PUBLIC / "jobs-data.json").write_text(
        json.dumps({"generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "timezone": "America/Toronto", "count": len(data),
                    "sources": sorted({d["source"] for d in data}), "jobs": data},
                   ensure_ascii=False, indent=1), encoding="utf-8")
    page = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    page = page.replace("__BUILT__", built)
    (PUBLIC / "index.html").write_text(page, encoding="utf-8")
    assert 'class="apply"' in page, "per-card apply link missing"
    fam = {k: sum(1 for d in data if d["family"] == k) for k in FAMILY_LABEL}
    print(f"site: {len(data)} jobs {fam}, best-match {sum(1 for d in data if d['match'] >= 45)}, "
          f"newest {max((d['posted'] for d in data), default='—')}, built {built}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
