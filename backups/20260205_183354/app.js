let allJobs = [];

function formatMoney(n) {
  try {
    return new Intl.NumberFormat("en-CA", {
      style: "currency",
      currency: "CAD",
      maximumFractionDigits: 0
    }).format(n);
  } catch {
    return `$${Math.round(n).toLocaleString()}`;
  }
}

function el(id) {
  return document.getElementById(id);
}

function setLoading(loading) {
  el("search").disabled = loading;
  el("search").textContent = loading ? "Loading..." : "Find jobs";
}

function normalizeText(value) {
  return (value ?? "").toString().toLowerCase().trim();
}

function includesAny(haystack, needles) {
  const h = normalizeText(haystack);
  return needles.some((n) => h.includes(n.toLowerCase()));
}

function inToronto(locationText) {
  const l = normalizeText(locationText);
  return l.includes("toronto") || l.includes("gta") || l.includes("greater toronto");
}

function looksFullTime(text) {
  const t = normalizeText(text);
  return t.includes("full-time") || t.includes("full time") || t.includes("permanent");
}

async function fetchJobs() {
  const res = await fetch('jobs.json');
  if (!res.ok) throw new Error("Failed to load jobs");
  const data = await res.json();
  allJobs = Array.isArray(data.jobs) ? data.jobs : (Array.isArray(data) ? data : []);
  return filterJobs();
}

function filterJobs() {
  const location = el("location").value;
  const keywordsRaw = el("keywords").value;
  const minSalary = Number(el("minSalary").value);
  const fullTimeOnly = el("fullTimeOnly").checked;
  
  // Source filters
  const sources = [];
  if (el("sourceAdzuna").checked) sources.push("adzuna");
  if (el("sourceJobbank").checked) sources.push("jobbank");
  if (el("sourceLinkedin").checked) sources.push("linkedin");
  if (el("sourceRemoteok").checked) sources.push("remoteok");
  
  const keywords = keywordsRaw.split(",").map(s => s.trim()).filter(Boolean);
  
  const filtered = allJobs
    .filter(j => sources.length === 0 || sources.includes(j.source))
    .filter(j => inToronto(j.location || location))
    .filter(j => includesAny(j.title, keywords))
    .filter(j => !fullTimeOnly || j.employmentType === "full-time" || looksFullTime(j.title))
    .sort((a, b) => (b.salary?.max ?? 0) - (a.salary?.max ?? 0));
  
  return {
    meta: {
      minSalary, fullTimeOnly, location, keywords, sources,
      totalFetched: allJobs.length, totalMatched: filtered.length
    },
    jobs: filtered
  };
}

function render(data) {
  const meta = data?.meta;
  const jobs = Array.isArray(data?.jobs) ? data.jobs : [];
  el("meta").textContent = meta
    ? `Loaded ${meta.totalFetched} jobs, matched ${meta.totalMatched}. Min salary: ${formatMoney(meta.minSalary)}.`
    : "";
  const list = el("list");
  list.innerHTML = "";
  if (!jobs.length) {
    const empty = document.createElement("div");
    empty.className = "card";
    empty.textContent = "No matches found. Try different keywords.";
    list.appendChild(empty);
    return;
  }
  for (const j of jobs) {
    const card = document.createElement("div");
    card.className = "card";
    const titleRow = document.createElement("div");
    titleRow.className = "titleRow";
    const a = document.createElement("a");
    a.href = j.url;
    a.target = "_blank";
    a.rel = "noreferrer";
    a.textContent = j.title;
    const salary = document.createElement("div");
    const sMin = j.salary?.min;
    const sMax = j.salary?.max;
    salary.textContent = sMin && sMax ? `${formatMoney(sMin)} - ${formatMoney(sMax)}` : "";
    salary.style.color = "rgba(255,255,255,0.78)";
    salary.style.fontVariantNumeric = "tabular-nums";
    titleRow.appendChild(a);
    titleRow.appendChild(salary);
    const tags = document.createElement("div");
    tags.className = "tagRow";
    const addTag = (v) => {
      if (!v) return;
      const t = document.createElement("div");
      t.className = "tag";
      t.textContent = v;
      tags.appendChild(t);
    };
    addTag(j.company);
    addTag(j.location);
    addTag(j.source);
    if (j.employmentType && j.employmentType !== "unknown") addTag(j.employmentType);
    const excerpt = document.createElement("div");
    excerpt.className = "excerpt";
    excerpt.textContent = j.excerpt || "";
    card.appendChild(titleRow);
    card.appendChild(tags);
    card.appendChild(excerpt);
    list.appendChild(card);
  }
}

function bind() {
  const minSalary = el("minSalary");
  const minSalaryValue = el("minSalaryValue");
  const syncSalaryLabel = () => {
    minSalaryValue.textContent = formatMoney(Number(minSalary.value));
  };
  minSalary.addEventListener("input", syncSalaryLabel);
  syncSalaryLabel();
  el("preset110").addEventListener("click", () => {
    minSalary.value = "110000";
    syncSalaryLabel();
    loadAndRender();
  });
  el("search").addEventListener("click", loadAndRender);
  
  // Source filter listeners
  el("sourceAdzuna").addEventListener("change", () => render(filterJobs()));
  el("sourceJobbank").addEventListener("change", () => render(filterJobs()));
  el("sourceLinkedin").addEventListener("change", () => render(filterJobs()));
  el("sourceRemoteok").addEventListener("change", () => render(filterJobs()));
}

async function loadAndRender() {
  setLoading(true);
  try {
    if (allJobs.length === 0) await fetchJobs();
    else render(filterJobs());
  } catch (e) {
    el("meta").textContent = "Error: " + String(e?.message || e);
    el("list").innerHTML = "";
  } finally {
    setLoading(false);
  }
}

loadAndRender();
bind();
