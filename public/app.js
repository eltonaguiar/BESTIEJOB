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
  el("search").textContent = loading ? "Searching..." : "Find jobs";
}

async function fetchJobs() {
  const location = el("location").value;
  const keywords = el("keywords").value;
  const minSalary = Number(el("minSalary").value);
  const fullTimeOnly = el("fullTimeOnly").checked;

  const params = new URLSearchParams({
    location,
    keywords,
    minSalary: String(minSalary),
    fullTimeOnly: String(fullTimeOnly)
  });

  const res = await fetch(`/api/jobs?${params.toString()}`);
  if (!res.ok) throw new Error("Failed to load jobs");
  return res.json();
}

function render(data) {
  const meta = data?.meta;
  const jobs = Array.isArray(data?.jobs) ? data.jobs : [];

  el("meta").textContent = meta
    ? `Fetched ${meta.totalFetched} postings, matched ${meta.totalMatched}. Salary min filter: ${formatMoney(
        meta.minSalary
      )}.`
    : "";

  const list = el("list");
  list.innerHTML = "";

  if (!jobs.length) {
    const empty = document.createElement("div");
    empty.className = "card";
    empty.textContent = "No matches found with salary data. Try lowering salary, changing keywords, or adding more sources.";
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
  });

  el("search").addEventListener("click", async () => {
    setLoading(true);
    try {
      const data = await fetchJobs();
      render(data);
    } catch (e) {
      el("meta").textContent = String(e?.message || e);
      el("list").innerHTML = "";
    } finally {
      setLoading(false);
    }
  });
}

bind();
