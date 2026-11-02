#!/usr/bin/env python3
"""
Build the GitHub Pages site from README.md's curated tables.

Writes:
  public/jobs-data.json   rows + derived source, verification, match score, alternates
  public/index.html       self-contained page (inline data, no build step, no CDN)

What the page gives a job-seeker
  * tabs: ServiceNow / Salesforce / Other / Best match, each with its own date window,
    ARIA tab semantics, URL-hash deep links and localStorage memory
  * one card per role: duplicates arriving from Adzuna + LinkedIn + jobs.ca are clustered
    under an employer+title key, with the alternates listed on the card
  * an employer-board vs aggregator verification badge per card
  * a resume-fit score with the reasons printed
  * APPLIED.md rows are excluded, so an applied role cannot resurface
  * sorting (newest / best fit), source filter, synonym + accent-aware search
  * "Last updated" build stamp and a staleness warning

Guarded by scripts/check_site_links.py (per-card anchors, tabs, stamp, fit score).
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from jobs_consolidate import README, extract_rows  # noqa: E402

PUBLIC = ROOT / "public"
APPLIED = ROOT / "APPLIED.md"
FAMILY_LABEL = {"servicenow": "ServiceNow", "salesforce": "Salesforce", "other": "Other"}

AGGREGATORS = ("adzuna.", "linkedin.com", "indeed.", "jooble", "talent.com", "eluta",
               "workopolis", "monster.", "glassdoor", "jobs.ca", "whatjobs", "simplify.jobs",
               "tealhq", "careerbeacon", "builtin", "ziprecruiter", "remotive")

SOURCE_RULES = [
    ("linkedin.com", "LinkedIn"), ("adzuna.", "Adzuna"), ("jobbank.gc.ca", "Job Bank"),
    ("myworkdayjobs.com", "Workday ATS"), ("greenhouse.io", "Greenhouse"), ("lever.co", "Lever"),
    ("smartrecruiters", "SmartRecruiters"), ("ashbyhq", "Ashby"), ("workable", "Workable"),
    ("indeed.", "Indeed"), ("jooble", "Jooble"), ("talent.com", "Talent.com"), ("eluta", "Eluta"),
    ("monster.", "Monster"), ("simplify.jobs", "Aggregator"), ("tealhq", "Aggregator"),
    ("glassdoor", "Glassdoor"), ("jobs.ca", "jobs.ca"), ("workopolis", "Workopolis"),
    ("whatjobs", "WhatJobs"), ("careerbeacon", "CareerBeacon"), ("builtin", "BuiltIn"),
]

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

WEAK = re.compile(r"sales\s+(representative|associate|manager|consultant|lead|agent)|account executive|"
                  r"retail|store manager|cashier|teller|barista|warehouse|driver|nurse|teacher", re.I)
FRENCH = re.compile(r"\b(fran[cç]ais|bilingue|bilingual|d[ée]veloppeur|administrateur|conseiller)\b", re.I)


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", text) if not unicodedata.combining(c))


def norm(text: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9 ]", " ", strip_accents((text or "").lower())).split())


def source_of(url: str) -> str:
    low = (url or "").lower()
    for needle, label in SOURCE_RULES:
        if needle in low:
            return label
    return urlparse(url or "").netloc.replace("www.", "") or "unknown"


def is_aggregator(url: str) -> bool:
    low = (url or "").lower()
    return any(a in low for a in AGGREGATORS)


def applied_index() -> tuple[set[str], set[str]]:
    """URLs and (title|company) keys from APPLIED.md — a role can be re-listed under
    a different link, so identity matters as much as the URL."""
    if not APPLIED.exists():
        return set(), set()
    text = APPLIED.read_text(encoding="utf-8", errors="replace")
    urls = {u.rstrip("/.,").split("?")[0].lower()
            for u in re.findall(r'https?://[^\s\)\]\|"]+', text)}
    keys: set[str] = set()
    for line in text.splitlines():
        if not line.startswith("| 2026"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3:
            continue
        m = re.match(r"\[(.*?)\]\((https?://[^)]+)\)", cells[1])
        title = m.group(1) if m else cells[1]
        keys.add(" ".join(sorted(t for t in norm(title).split() if len(t) > 3)))
    return urls, keys


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
    if WEAK.search(title):
        score = int(score * 0.35)
        reasons.append("weak title match")
    return min(100, score), reasons[:5]


def rows() -> tuple[list[dict], int]:
    parsed, _ = extract_rows(README.read_text(encoding="utf-8"))
    skip, skip_keys = applied_index()
    seen: set[str] = set()
    raw: list[dict] = []
    dropped_applied = 0
    for r in parsed:
        url = (r.get("url") or "").strip()
        if not url.startswith("http"):
            continue
        key = url.split("?")[0].rstrip("/").lower()
        toks = set(t for t in norm(r["title"]).split() if len(t) > 3)
        applied_ident = False
        if key in skip:
            applied_ident = True
        else:
            for k in skip_keys:
                kt = set(k.split())
                if kt and len(toks & kt) / max(1, len(kt)) >= 0.8:
                    applied_ident = True
                    break
        if applied_ident:
            dropped_applied += 1
            continue
        if key in seen:
            continue
        seen.add(key)
        row = {
            "posted": r["posted"], "title": r["title"], "company": r["company"],
            "location": r["location"], "url": url, "note": r["note"][:160],
            "family": r["family"], "familyLabel": FAMILY_LABEL.get(r["family"], "Other"),
            "source": source_of(url),
        }
        row["verified"] = "Aggregator" if is_aggregator(url) else "Employer board"
        score, reasons = match_score(row)
        row["match"] = score
        row["matchReasons"] = reasons
        row["french"] = bool(FRENCH.search(r["title"] + " " + row["note"]))
        row["search"] = strip_accents(" ".join([
            row["title"], row["company"], row["location"], row["source"],
            row["familyLabel"], row["note"], " ".join(reasons)])).lower()
        raw.append(row)

    # cluster duplicates: same normalised title + company -> one card, alternates kept
    clusters: dict[str, dict] = {}
    for row in raw:
        key = f'{norm(row["title"])[:70]}|{norm(row["company"])[:40]}'
        if key not in clusters:
            row["alternates"] = []
            clusters[key] = row
            continue
        primary = clusters[key]
        # prefer the employer's own board over an aggregator mirror, then the newest
        if primary["verified"] == "Aggregator" and row["verified"] == "Employer board":
            row["alternates"] = primary["alternates"] + [{"source": primary["source"], "url": primary["url"]}]
            clusters[key] = row
        else:
            primary["alternates"].append({"source": row["source"], "url": row["url"]})
    out = list(clusters.values())
    for row in out:
        seen_src = {row["source"]}
        row["alternates"] = [a for a in row["alternates"]
                             if not (a["source"] in seen_src or seen_src.add(a["source"]))][:4]
    out.sort(key=lambda r: (r["posted"], r["match"]), reverse=True)
    return out, dropped_applied


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>BESTIEJOB — ServiceNow, Salesforce &amp; IT platform jobs</title>
<meta name="description" content="Toronto-first ServiceNow, Salesforce and IT platform job postings, deduplicated, verified and ranked against a ServiceNow/Salesforce developer profile.">
<meta property="og:title" content="BESTIEJOB — ServiceNow / Salesforce jobs">
<meta property="og:description" content="Curated, deduplicated and verified ServiceNow, Salesforce and adjacent IT roles.">
<style>
  :root { --bg:#0f1115; --card:#171a21; --edge:#262b36; --text:#e8ebf0; --muted:#9aa4b2; --accent:#5b8cff; --ok:#38b27a; --warn:#e0b252; --bad:#e06a6a; }
  * { box-sizing: border-box; }
  body { margin:0; background:var(--bg); color:var(--text); font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif; }
  header { padding:26px 20px 0; border-bottom:1px solid var(--edge); }
  h1 { margin:0 0 4px; font-size:22px; letter-spacing:-.2px; }
  .sub { color:var(--muted); font-size:13px; }
  .stale { color:var(--warn); }
  main { max-width:1080px; margin:0 auto; padding:16px 20px 60px; }
  .tabs { display:flex; gap:6px; flex-wrap:wrap; padding:14px 20px 0; max-width:1080px; margin:0 auto; position:sticky; top:0; background:var(--bg); z-index:5; }
  .tabs button { border-radius:10px 10px 0 0; border-bottom-color:transparent; }
  .tabs button[aria-selected="true"] { background:var(--card); border-color:var(--edge); color:var(--text); box-shadow:inset 0 2px 0 var(--accent); }
  .tabs button .n { color:var(--muted); font-size:12px; margin-left:5px; }
  button:focus-visible, select:focus-visible, input:focus-visible, a:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }
  .controls { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin:14px 0 8px; }
  .chips { display:flex; gap:8px; flex-wrap:wrap; }
  button { font:inherit; color:var(--text); background:var(--card); border:1px solid var(--edge); padding:6px 12px; border-radius:999px; cursor:pointer; }
  button:hover { border-color:var(--accent); }
  .chips button[aria-pressed="true"] { background:var(--accent); border-color:var(--accent); color:#fff; }
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
  .alts { margin-top:6px; font-size:12px; color:var(--muted); display:flex; gap:8px; flex-wrap:wrap; }
  .alts a { color:var(--muted); text-decoration:underline; }
  .tag { font-size:11px; text-transform:uppercase; letter-spacing:.4px; padding:2px 7px; border-radius:999px; border:1px solid var(--edge); color:var(--muted); }
  .tag.servicenow { color:#7fc8a0; border-color:#2c5c45; }
  .tag.salesforce { color:#8fb4ff; border-color:#2f4a7d; }
  .tag.other { color:#d3b3ff; border-color:#4d3a6b; }
  .tag.today { color:var(--ok); border-color:#245c44; }
  .tag.match { color:var(--warn); border-color:#5c4a24; }
  .tag.board { color:var(--ok); border-color:#245c44; }
  .tag.agg { color:var(--bad); border-color:#5c2c2c; }
  .empty { color:var(--muted); padding:18px 0; font-size:13.5px; }
  footer { color:var(--muted); font-size:12px; border-top:1px solid var(--edge); padding:18px 20px; }
  code { background:#0b0d11; border:1px solid var(--edge); padding:1px 5px; border-radius:5px; font-size:12px; }
  @media (prefers-reduced-motion: reduce) { * { transition:none !important; } }
</style>
</head>
<body>
<header>
  <h1>BESTIEJOB</h1>
  <div class="sub">ServiceNow · Salesforce · IT platform roles. <b>Other</b> is ranked by fit to the profile; <b>Best match</b> collects strong fits from every family. Duplicates are clustered; applied roles are hidden.</div>
  <div class="sub" id="updated" style="margin-top:6px"></div>
</header>
<div class="tabs" id="tabs" role="tablist" aria-label="Job families"></div>
<main>
  <div class="controls">
    <input type="search" id="q" placeholder="Search title, company, location… try “snow dev”, “sf admin”, “montreal”, “cmdb”">
    <select id="src" aria-label="Filter by source"></select>
    <select id="sort" aria-label="Sort order">
      <option value="newest">Newest first</option>
      <option value="fit">Best fit first</option>
    </select>
  </div>
  <div class="controls"><div class="chips" id="when" role="group" aria-label="Date window"></div></div>
  <div class="meta" id="meta"></div>
  <div class="grid" id="list" role="tabpanel" tabindex="0"></div>
</main>
<footer>
  Dates are source posting dates, not relative “days ago” labels. Aggregator mirrors can expire — open the
  posting before applying. <span id="counts"></span> · data: <code>public/jobs-data.json</code>
</footer>
<script>
const JOBS = __DATA__;
const DROPPED_APPLIED = __APPLIED__;
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
const saved = (() => { try { return JSON.parse(localStorage.getItem("bestiejob") || "{}"); } catch (e) { return {}; } })();
const state = {
  tab: (location.hash || "").replace("#", "") || saved.tab || "servicenow",
  when: Object.assign({ servicenow:"all", salesforce:"all", other:"all", match:"all" }, saved.when || {}),
  src: "all", sort: saved.sort || "newest", q: ""
};
if (!TABS.some(t => t[0] === state.tab)) state.tab = "servicenow";
const $ = (s) => document.querySelector(s);
const fmt = (s) => new Date(s + "T12:00:00Z").toLocaleDateString("en-CA", { weekday:"short", month:"short", day:"numeric", year:"numeric" });
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
function persist() { try { localStorage.setItem("bestiejob", JSON.stringify({ tab: state.tab, when: state.when, sort: state.sort })); } catch (e) {} }

const srcCounts = {};
JOBS.forEach(j => { srcCounts[j.source] = (srcCounts[j.source] || 0) + 1; });
$("#src").innerHTML = `<option value="all">All sources (${JOBS.length})</option>` +
  Object.keys(srcCounts).sort((a,b) => srcCounts[b] - srcCounts[a])
    .map(s => `<option value="${esc(s)}">${esc(s)} (${srcCounts[s]})</option>`).join("");
$("#sort").value = state.sort;

function renderTabs() {
  const counts = {};
  TABS.forEach(([k,,fn]) => { counts[k] = JOBS.filter(fn).length; });
  $("#tabs").innerHTML = TABS.map(([key, label]) =>
    `<button role="tab" data-tab="${key}" aria-selected="${state.tab === key}" aria-controls="list" tabindex="${state.tab === key ? 0 : -1}">${label}<span class="n">${counts[key]}</span></button>`).join("");
}
function renderWindows() {
  $("#when").innerHTML = WINDOWS.map(([k, label]) =>
    `<button data-when-kind="${k}" aria-pressed="${state.when[state.tab] === k}">${label}</button>`).join("");
}
function tokens(q) {
  return stripAccents(q.toLowerCase()).replace(/[^a-z0-9 ]/g, " ").split(/\\s+/)
    .filter(Boolean).map(t => SYN[t] || t);
}

function render() {
  const tabDef = TABS.find(t => t[0] === state.tab) || TABS[0];
  const from = windowStart(state.when[state.tab]);
  const toks = tokens(state.q);
  let list = JOBS.filter(j => tabDef[2](j)
    && (state.when[state.tab] === "all" || j.posted >= from)
    && (state.src === "all" || j.source === state.src || (j.alternates || []).some(a => a.source === state.src))
    && (toks.length === 0 || toks.every(t => (j.search || "").includes(t))));
  if (state.sort === "fit") list.sort((a, b) => (b.match - a.match) || (b.posted > a.posted ? 1 : -1));
  else list.sort((a, b) => (a.posted < b.posted ? 1 : a.posted > b.posted ? -1 : b.match - a.match));

  const win = state.when[state.tab];
  const whenLabel = win === "today" ? `Today — ${fmt(TODAY)} (America/Toronto)`
    : win === "week" ? `Last 7 days — ${fmt(from)} → ${fmt(TODAY)}`
    : win === "month" ? `Last 30 days — ${fmt(from)} → ${fmt(TODAY)}` : "All dates";
  const boardCount = list.filter(j => j.verified === "Employer board").length;
  $("#meta").innerHTML = `<b>${list.length}</b> shown · ${whenLabel}` +
    ` · employer-board ${boardCount} · aggregator ${list.length - boardCount}` +
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
        <span class="tag ${j.verified === "Employer board" ? "board" : "agg"}">${esc(j.verified)}</span>
        ${j.french ? '<span class="tag">FR</span>' : ""}
        <span>${esc(j.company || "—")}</span>
        <span>${esc(j.location || "")}</span>
      </div>
      <div class="applyrow">
        <a class="apply" href="${esc(j.url)}" target="_blank" rel="noopener noreferrer">Open posting &#8599;</a>
        <span>${esc((j.matchReasons || []).join(" · "))}</span>
      </div>
      ${(j.alternates || []).length ? `<div class="alts"><span>Also listed:</span>` +
        j.alternates.map(a => `<a href="${esc(a.url)}" target="_blank" rel="noopener noreferrer">${esc(a.source)}</a>`).join("") +
        `</div>` : ""}
    </article>`).join("");
}

$("#tabs").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-tab]"); if (!b) return;
  state.tab = b.dataset.tab;
  history.replaceState(null, "", "#" + state.tab);
  persist(); renderTabs(); renderWindows(); render();
});
$("#tabs").addEventListener("keydown", (e) => {
  if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
  const i = TABS.findIndex(t => t[0] === state.tab);
  const next = TABS[(i + (e.key === "ArrowRight" ? 1 : TABS.length - 1)) % TABS.length][0];
  state.tab = next; history.replaceState(null, "", "#" + next);
  persist(); renderTabs(); renderWindows(); render();
  document.querySelector(`#tabs button[data-tab="${next}"]`).focus();
});
$("#when").addEventListener("click", (e) => {
  const b = e.target.closest("button[data-when-kind]"); if (!b) return;
  state.when[state.tab] = b.dataset.whenKind; persist(); renderWindows(); render();
});
$("#src").addEventListener("change", (e) => { state.src = e.target.value; render(); });
$("#sort").addEventListener("change", (e) => { state.sort = e.target.value; persist(); render(); });
$("#q").addEventListener("input", (e) => { state.q = e.target.value; render(); });
window.addEventListener("hashchange", () => {
  const t = location.hash.replace("#", "");
  if (TABS.some(x => x[0] === t) && t !== state.tab) { state.tab = t; renderTabs(); renderWindows(); render(); }
});

const STALE_DAYS = (new Date(TODAY + "T12:00:00Z") - new Date(newest + "T12:00:00Z")) / 86400000;
$("#updated").innerHTML = `Data updated <b>${UPDATED}</b> · ${JOBS.length} postings · newest posting ${fmt(newest)}` +
  (STALE_DAYS > 2 ? ` · <span class="stale">data looks stale (${Math.round(STALE_DAYS)} days old)</span>` : "") +
  (DROPPED_APPLIED ? ` · ${DROPPED_APPLIED} applied role(s) hidden` : "");
$("#counts").textContent = `${JOBS.length} postings indexed · ` +
  TABS.map(([k, label]) => `${label} ${JOBS.filter(t => t[2]).length}`).join(" · ");
renderTabs(); renderWindows(); render();
</script>
</body>
</html>
"""


def main() -> int:
    data, dropped = rows()
    PUBLIC.mkdir(exist_ok=True)
    built = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    payload = {"generatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "timezone": "America/Toronto", "count": len(data),
               "appliedHidden": dropped,
               "sources": sorted({d["source"] for d in data}), "jobs": data}
    (PUBLIC / "jobs-data.json").write_text(json.dumps(payload, ensure_ascii=False, indent=1),
                                           encoding="utf-8")
    page = HTML.replace("__DATA__", json.dumps(data, ensure_ascii=False).replace("</", "<\\/"))
    page = page.replace("__APPLIED__", str(dropped)).replace("__BUILT__", built)
    (PUBLIC / "index.html").write_text(page, encoding="utf-8")
    assert 'class="apply"' in page, "per-card apply link missing"
    fam = {k: sum(1 for d in data if d["family"] == k) for k in FAMILY_LABEL}
    dups = sum(1 for d in data if d.get("alternates"))
    print(f"site: {len(data)} jobs {fam} · {dups} with duplicate mirrors collapsed · "
          f"{dropped} applied hidden · best-match {sum(1 for d in data if d['match'] >= 45)} · "
          f"newest {max((d['posted'] for d in data), default='—')} · built {built}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
