let allJobs = [];
let lastFetch = 0;
let filterCounts = {}; // Cache for preview counts
let savedJobs = JSON.parse(localStorage.getItem('savedJobs') || '[]');
let currentJobIndex = -1; // For keyboard navigation
let showingSavedPanel = false;

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

function formatDate(job) {
  // Handle both old format (just dateStr) and new format (job object)
  const dateStr = typeof job === 'object' ? (job.postedDate || job.scrapedAt) : job;
  const isUncertain = typeof job === 'object' && (!job.postedDate || job.dateSource === "unknown");

  if (!dateStr) return isUncertain ? "Recently" : "";

  try {
    const d = new Date(dateStr);
    if (isNaN(d.getTime())) return isUncertain ? "Recently" : "";

    const now = new Date();
    const diffMs = now - d;
    const diffMinutes = Math.floor(diffMs / (1000 * 60));
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    // If date is uncertain, show approximate
    const prefix = isUncertain ? "~" : "";

    // Super fresh jobs - show exact time
    if (diffMinutes < 1) return prefix + "Just now";
    if (diffMinutes < 5) return prefix + `${diffMinutes}m ago`;
    if (diffMinutes < 15) return prefix + `${diffMinutes} min ago`;
    if (diffMinutes < 60) return prefix + `${diffMinutes} min ago`;

    // Hours
    if (diffHours === 1) return prefix + "1 hour ago";
    if (diffHours < 24) return prefix + `${diffHours}h ago`;

    // Days
    if (diffDays === 1) return prefix + "Yesterday";
    if (diffDays < 7) return prefix + `${diffDays} days ago`;
    if (diffDays < 14) return prefix + "1 week ago";
    if (diffDays < 30) return prefix + `${Math.floor(diffDays / 7)} weeks ago`;

    return d.toLocaleDateString("en-CA", { month: "short", day: "numeric" });
  } catch {
    return isUncertain ? "Recently" : "";
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

function decodeHtmlEntities(text) {
  if (!text) return "";
  // Create a textarea element to decode HTML entities
  const textarea = document.createElement("textarea");
  textarea.innerHTML = text;
  // Get decoded text
  let decoded = textarea.value;
  // Strip HTML tags to get plain text
  const div = document.createElement("div");
  div.innerHTML = decoded;
  return div.textContent || div.innerText || "";
}

function includesAny(haystack, needles) {
  const h = normalizeText(haystack);
  return needles.some((n) => h.includes(n.toLowerCase().trim()));
}

function inToronto(locationText, targetLocation) {
  const l = normalizeText(locationText);
  const t = normalizeText(targetLocation);

  // Check for Toronto area
  if (t.includes("toronto") || t.includes("gta")) {
    return l.includes("toronto") || l.includes("gta") || l.includes("greater toronto") ||
      l.includes("ontario") || l.includes("on, ca") || l.includes("remote") ||
      l.includes("canada") || l === "";
  }

  // Check if location contains target
  return l.includes(t) || l.includes("remote") || l === "";
}

function looksFullTime(text) {
  const t = normalizeText(text);
  return t.includes("full-time") || t.includes("full time") || t.includes("permanent");
}

// Detect if a job URL is a generic career page (not a specific job posting)
function isGenericLink(job) {
  if (!job.url) return false;

  const url = job.url.toLowerCase();

  // Generic career page patterns
  const genericPatterns = [
    '/careers/',
    '/careers',
    '/jobs/',
    '/jobs',
    '/career/',
    '/career',
    '/opportunities/',
    '/opportunities',
    '/join-us/',
    '/join-us',
    '/work-with-us/',
    '/work-with-us'
  ];

  // Check if URL ends with generic pattern (no specific job ID)
  for (const pattern of genericPatterns) {
    if (url.endsWith(pattern) || url.endsWith(pattern + '/')) {
      return true;
    }
  }

  // Check for very short URLs that are likely generic
  // e.g., "https://company.com/careers" with no additional path
  const urlObj = new URL(job.url);
  const pathParts = urlObj.pathname.split('/').filter(p => p.length > 0);

  // If path is just "careers" or "jobs" with nothing after, it's generic
  if (pathParts.length === 1 && genericPatterns.some(p => p.includes(pathParts[0]))) {
    return true;
  }

  return false;
}

function getEnabledEmploymentTypes() {
  const types = [];
  document.querySelectorAll(".emp-type:checked").forEach(cb => {
    types.push(cb.value);
  });
  return types;
}

function matchesEmploymentType(job, enabledTypes) {
  if (enabledTypes.length === 0) return true;

  const jobType = (job.employmentType || "unknown").toLowerCase();

  // Direct match
  if (enabledTypes.includes(jobType)) return true;

  // Check title and excerpt for type indicators
  const text = `${job.title} ${job.excerpt || ""}`.toLowerCase();

  for (const type of enabledTypes) {
    if (type === "full-time" && (text.includes("full-time") || text.includes("full time") || text.includes("permanent"))) return true;
    if (type === "contract" && (text.includes("contract") || text.includes("contractor") || text.includes("c2c"))) return true;
    if (type === "part-time" && (text.includes("part-time") || text.includes("part time"))) return true;
    if (type === "internship" && (text.includes("intern") || text.includes("co-op") || text.includes("coop"))) return true;
    if (type === "seasonal" && (text.includes("seasonal") || text.includes("temporary") || text.includes("temp "))) return true;
    if (type === "unknown" && jobType === "unknown") return true;
  }

  return false;
}

function formatSalary(salary) {
  if (!salary) return "";

  // If salary is already a display string
  if (typeof salary === "string") return salary;

  // If salary is an object with min/max
  if (salary.display) return salary.display;

  const min = salary.min;
  const max = salary.max;
  const type = salary.type || "annual";

  if (!min) return "";

  if (type === "hourly") {
    return max && max !== min ? `$${min}-$${max}/hr` : `$${min}/hr`;
  } else {
    const minK = Math.round(min / 1000);
    const maxK = max ? Math.round(max / 1000) : minK;
    return maxK !== minK ? `$${minK}K-$${maxK}K` : `$${minK}K`;
  }
}

function isWithinDateFilter(job, filterValue) {
  if (filterValue === "any") return true;

  // Get the best date - prefer postedDate, fall back to scrapedAt
  const dateStr = job.postedDate || job.scrapedAt;

  // If no date at all, only include in broad filters (week+)
  if (!dateStr) {
    const broadFilters = ["week", "14d", "month", "any"];
    return broadFilters.includes(filterValue);
  }

  const posted = new Date(dateStr);
  if (isNaN(posted.getTime())) {
    // Invalid date - only include in broad filters
    const broadFilters = ["week", "14d", "month", "any"];
    return broadFilters.includes(filterValue);
  }

  // If the job's date source is unknown/scraped (not actual posted date),
  // be conservative with tight time filters
  if (job.dateSource === "unknown" || (!job.postedDate && job.scrapedAt)) {
    // For very tight filters (under 1 day), exclude jobs with uncertain dates
    const tightFilters = ["15m", "30m", "1h", "2h", "4h", "8h", "12h"];
    if (tightFilters.includes(filterValue)) {
      // Only include if scraped very recently (last 30 min)
      const scrapedDate = new Date(job.scrapedAt);
      if (isNaN(scrapedDate.getTime())) return false;
      const minSinceScraped = (new Date() - scrapedDate) / (1000 * 60);
      if (minSinceScraped > 30) return false;
    }
  }

  const now = new Date();
  const diffMs = now - posted;
  const diffMinutes = diffMs / (1000 * 60);
  const diffHours = diffMs / (1000 * 60 * 60);
  const diffDays = diffMs / (1000 * 60 * 60 * 24);

  switch (filterValue) {
    // Minutes
    case "15m": return diffMinutes <= 15;
    case "30m": return diffMinutes <= 30;
    // Hours
    case "1h": return diffHours <= 1;
    case "2h": return diffHours <= 2;
    case "4h": return diffHours <= 4;
    case "8h": return diffHours <= 8;
    case "12h": return diffHours <= 12;
    case "24h": return diffHours <= 24;
    // Days
    case "2d": return diffDays <= 2;
    case "3d": return diffDays <= 3;
    case "week": return diffDays <= 7;
    case "14d": return diffDays <= 14;
    case "month": return diffDays <= 30;
    default: return true;
  }
}

// Check if job matches deadline filter
function matchesDeadlineFilter(job, filterValue) {
  if (filterValue === "any") return true;

  const hasDeadline = job.deadline || job.applicationDeadline || job.closingDate;

  // Filter for jobs with/without deadline
  if (filterValue === "hasDeadline") return !!hasDeadline;
  if (filterValue === "noDeadline") return !hasDeadline;

  // If filtering by deadline timeframe but job has no deadline
  if (!hasDeadline) return filterValue === "any";

  const deadline = new Date(hasDeadline);
  if (isNaN(deadline.getTime())) return filterValue === "noDeadline";

  const now = new Date();
  const diffMs = deadline - now; // Positive means deadline is in future
  const diffDays = diffMs / (1000 * 60 * 60 * 24);

  // Deadline already passed
  if (diffDays < 0) return false;

  switch (filterValue) {
    case "today": return diffDays < 1;
    case "3d": return diffDays <= 3;
    case "week": return diffDays <= 7;
    case "14d": return diffDays <= 14;
    case "month": return diffDays <= 30;
    default: return true;
  }
}

// Calculate counts for all filter options (for preview)
function calculateFilterCounts() {
  const counts = {
    dateFilter: {},
    deadlineFilter: {},
    employmentTypes: {},
    sources: {}
  };

  // Date filter counts
  const dateOptions = ["15m", "30m", "1h", "2h", "4h", "8h", "12h", "24h", "2d", "3d", "week", "14d", "month", "any"];
  for (const opt of dateOptions) {
    counts.dateFilter[opt] = allJobs.filter(j => isWithinDateFilter(j, opt)).length;
  }

  // Deadline filter counts
  const deadlineOptions = ["any", "today", "3d", "week", "14d", "month", "hasDeadline", "noDeadline"];
  for (const opt of deadlineOptions) {
    counts.deadlineFilter[opt] = allJobs.filter(j => matchesDeadlineFilter(j, opt)).length;
  }

  // Employment type counts
  const empTypes = ["full-time", "contract", "part-time", "internship", "seasonal", "unknown"];
  for (const type of empTypes) {
    counts.employmentTypes[type] = allJobs.filter(j => {
      const jobType = (j.employmentType || "unknown").toLowerCase();
      if (type === jobType) return true;
      const text = `${j.title} ${j.excerpt || ""}`.toLowerCase();
      if (type === "full-time" && (text.includes("full-time") || text.includes("permanent"))) return true;
      if (type === "contract" && (text.includes("contract") || text.includes("contractor"))) return true;
      return false;
    }).length;
  }

  return counts;
}

// Update dropdown options with counts
function updateFilterCountsUI() {
  if (allJobs.length === 0) return;

  const counts = calculateFilterCounts();
  filterCounts = counts;

  // Update date filter dropdown
  const dateSelect = el("dateFilter");
  if (dateSelect) {
    Array.from(dateSelect.options).forEach(opt => {
      const count = counts.dateFilter[opt.value];
      const baseText = opt.textContent.replace(/\s*\(\d+\)$/, ""); // Remove existing count
      opt.textContent = `${baseText} (${count !== undefined ? count : 0})`;
    });
  }

  // Update deadline filter dropdown
  const deadlineSelect = el("deadlineFilter");
  if (deadlineSelect) {
    Array.from(deadlineSelect.options).forEach(opt => {
      const count = counts.deadlineFilter[opt.value];
      const baseText = opt.textContent.replace(/\s*\(\d+\)$/, "");
      opt.textContent = `${baseText} (${count !== undefined ? count : 0})`;
    });
  }

  // Update employment type checkboxes
  document.querySelectorAll(".emp-type").forEach(cb => {
    const count = counts.employmentTypes[cb.value] || 0;
    const label = cb.closest("label");
    if (label) {
      const span = label.querySelector("span");
      if (span) {
        const baseText = span.textContent.replace(/\s*\(\d+\)$/, "");
        span.textContent = `${baseText} (${count})`;
      }
    }
  });

  // Update stats dashboard
  updateStatsDashboard();
}

// Stats dashboard
function updateStatsDashboard() {
  const total = allJobs.length;
  const fresh = allJobs.filter(j => {
    const d = new Date(j.postedDate || j.scrapedAt);
    return !isNaN(d) && (Date.now() - d) < 24 * 60 * 60 * 1000;
  }).length;
  const remote = allJobs.filter(j => detectWorkArrangement(j) === 'remote').length;
  const withSalary = allJobs.filter(j => j.salary?.min || j.salary?.max).length;

  // Calculate average salary
  const salaries = allJobs
    .filter(j => j.salary?.min && j.salary.type !== 'hourly')
    .map(j => j.salary.min);
  const avgSalary = salaries.length > 0
    ? Math.round(salaries.reduce((a, b) => a + b, 0) / salaries.length / 1000)
    : 0;

  el("statTotal").textContent = total.toLocaleString();
  el("statFresh").textContent = fresh.toLocaleString();
  el("statRemote").textContent = remote.toLocaleString();
  el("statWithSalary").textContent = withSalary.toLocaleString();
  el("statAvgSalary").textContent = avgSalary > 0 ? `$${avgSalary}K` : '-';
}

// Work arrangement detection
function detectWorkArrangement(job) {
  const text = `${job.title} ${job.location} ${job.excerpt || ''}`.toLowerCase();

  if (text.includes('remote') || text.includes('work from home') || text.includes('wfh') ||
    text.includes('anywhere') || text.includes('distributed')) {
    if (text.includes('hybrid') || text.includes('flexible') || text.includes('occasional')) {
      return 'hybrid';
    }
    return 'remote';
  }
  if (text.includes('hybrid') || text.includes('flexible location')) {
    return 'hybrid';
  }
  if (text.includes('onsite') || text.includes('on-site') || text.includes('in-office') ||
    text.includes('in office') || text.includes('office-based')) {
    return 'onsite';
  }
  return 'unknown';
}

function matchesWorkArrangement(job, filter) {
  if (filter === 'any') return true;
  const arrangement = detectWorkArrangement(job);
  if (filter === 'remote') return arrangement === 'remote';
  if (filter === 'hybrid') return arrangement === 'hybrid' || arrangement === 'remote';
  if (filter === 'onsite') return arrangement === 'onsite' || arrangement === 'unknown';
  return true;
}

// Experience level detection
function detectExperienceLevel(job) {
  const text = `${job.title} ${job.excerpt || ''}`.toLowerCase();

  if (text.includes('director') || text.includes('vp ') || text.includes('vice president') ||
    text.includes('head of') || text.includes('chief ')) {
    return 'manager';
  }
  if (text.includes('lead') || text.includes('principal') || text.includes('staff ') ||
    text.includes('architect')) {
    return 'lead';
  }
  if (text.includes('senior') || text.includes('sr.') || text.includes('sr ') ||
    text.includes('5+ years') || text.includes('7+ years') || text.includes('10+ years')) {
    return 'senior';
  }
  if (text.includes('junior') || text.includes('jr.') || text.includes('jr ') ||
    text.includes('entry') || text.includes('graduate') || text.includes('new grad') ||
    text.includes('0-2 years') || text.includes('1-2 years') || text.includes('intern') ||
    text.includes('co-op') || text.includes('early career')) {
    return 'entry';
  }
  if (text.includes('mid') || text.includes('intermediate') || text.includes('2-5 years') ||
    text.includes('3-5 years') || text.includes('3+ years')) {
    return 'mid';
  }
  return 'unknown';
}

function matchesExperienceLevel(job, filter) {
  if (filter === 'any') return true;
  const level = detectExperienceLevel(job);
  if (level === 'unknown') return true; // Include unknown in all filters
  return level === filter;
}

// Saved jobs functions
function isJobSaved(job) {
  return savedJobs.some(s => s.url === job.url);
}

function toggleSaveJob(job) {
  const index = savedJobs.findIndex(s => s.url === job.url);
  if (index >= 0) {
    savedJobs.splice(index, 1);
  } else {
    savedJobs.push({
      url: job.url,
      title: job.title,
      company: job.company,
      location: job.location,
      salary: job.salary,
      savedAt: new Date().toISOString()
    });
  }
  localStorage.setItem('savedJobs', JSON.stringify(savedJobs));
  updateSavedCount();
  return isJobSaved(job);
}

function updateSavedCount() {
  const count = savedJobs.length;
  el("savedCount").textContent = count;
  el("savedJobsCount").textContent = count;
}

function renderSavedJobs() {
  const list = el("savedJobsList");
  list.innerHTML = "";

  if (savedJobs.length === 0) {
    list.innerHTML = '<div class="empty-saved">No saved jobs yet. Click the bookmark icon on any job to save it.</div>';
    return;
  }

  for (const j of savedJobs) {
    const card = document.createElement("div");
    card.className = "card saved-card";
    card.innerHTML = `
      <div class="titleRow">
        <a href="${j.url}" target="_blank" rel="noreferrer">${j.title}</a>
        <button class="unsave-btn" data-url="${j.url}" title="Remove from saved">&times;</button>
      </div>
      <div class="tagRow">
        <span class="tag company">${j.company || ''}</span>
        <span class="tag location">${j.location || ''}</span>
        ${j.salary?.display ? `<span class="tag salary">${j.salary.display}</span>` : ''}
      </div>
      <div class="saved-date">Saved ${formatDate({ postedDate: j.savedAt })}</div>
    `;
    list.appendChild(card);
  }

  // Add remove handlers
  list.querySelectorAll(".unsave-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const url = btn.dataset.url;
      savedJobs = savedJobs.filter(s => s.url !== url);
      localStorage.setItem('savedJobs', JSON.stringify(savedJobs));
      updateSavedCount();
      renderSavedJobs();
      render(filterJobs()); // Update main list to reflect save status
    });
  });
}

// URL state management
function getStateFromURL() {
  const params = new URLSearchParams(window.location.search);
  return {
    keywords: params.get('q') || '',
    location: params.get('loc') || 'Toronto, ON',
    dateFilter: params.get('date') || 'week',
    minSalary: params.get('salary') || '80000',
    workArrangement: params.get('work') || 'any',
    experienceLevel: params.get('exp') || 'any',
    sortBy: params.get('sort') || 'date'
  };
}

function updateURLState() {
  const params = new URLSearchParams();
  const keywords = el("keywords").value;
  const location = el("location").value;
  const dateFilter = el("dateFilter").value;
  const minSalary = el("minSalary").value;
  const workArrangement = el("workArrangement")?.value || 'any';
  const experienceLevel = el("experienceLevel")?.value || 'any';
  const sortBy = el("sortBy")?.value || 'date';

  if (keywords) params.set('q', keywords);
  if (location !== 'Toronto, ON') params.set('loc', location);
  if (dateFilter !== 'week') params.set('date', dateFilter);
  if (minSalary !== '80000') params.set('salary', minSalary);
  if (workArrangement !== 'any') params.set('work', workArrangement);
  if (experienceLevel !== 'any') params.set('exp', experienceLevel);
  if (sortBy !== 'date') params.set('sort', sortBy);

  const newURL = params.toString() ? `?${params.toString()}` : window.location.pathname;
  history.replaceState(null, '', newURL);
}

function applyStateFromURL() {
  const state = getStateFromURL();
  el("keywords").value = state.keywords;
  el("location").value = state.location;
  el("dateFilter").value = state.dateFilter;
  el("minSalary").value = state.minSalary;
  if (el("workArrangement")) el("workArrangement").value = state.workArrangement;
  if (el("experienceLevel")) el("experienceLevel").value = state.experienceLevel;
  if (el("sortBy")) el("sortBy").value = state.sortBy;

  // Update salary label
  el("minSalaryValue").textContent = formatMoney(Number(state.minSalary));
}

function copyShareableLink() {
  updateURLState();
  navigator.clipboard.writeText(window.location.href).then(() => {
    const btn = el("shareSearch");
    const original = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => btn.textContent = original, 2000);
  });
}

async function fetchJobs(forceRefresh = false) {
  const now = Date.now();
  // Cache for 5 minutes
  if (!forceRefresh && allJobs.length > 0 && (now - lastFetch) < 300000) {
    return filterJobs();
  }

  const res = await fetch('jobs.json?t=' + now);
  if (!res.ok) throw new Error("Failed to load jobs");
  const data = await res.json();
  allJobs = Array.isArray(data.jobs) ? data.jobs : (Array.isArray(data) ? data : []);
  lastFetch = now;

  // Update filter counts in UI after loading jobs
  updateFilterCountsUI();

  return filterJobs();
}

function getEnabledSources() {
  // Collect all enabled sources from checkboxes with data-sources attribute
  const sources = new Set();

  document.querySelectorAll(".source-filters input[type='checkbox']").forEach(cb => {
    if (cb.checked) {
      const srcList = cb.dataset.sources || cb.id?.replace("source", "").toLowerCase();
      if (srcList) {
        srcList.split(",").forEach(s => sources.add(s.trim().toLowerCase()));
      }
    }
  });

  return Array.from(sources);
}

function filterJobs() {
  const location = el("location").value;
  const keywordsRaw = el("keywords").value;
  const minSalary = Number(el("minSalary").value);
  const dateFilter = el("dateFilter").value;
  const deadlineFilter = el("deadlineFilter")?.value || "any";
  const workArrangement = el("workArrangement")?.value || "any";
  const experienceLevel = el("experienceLevel")?.value || "any";
  const sortBy = el("sortBy")?.value || "date";
  const recruiterOnly = el("recruiterFilter")?.checked || false;

  // Get all enabled sources and employment types
  const sources = getEnabledSources();
  const employmentTypes = getEnabledEmploymentTypes();

  const keywords = keywordsRaw.split(",").map(s => s.trim()).filter(Boolean);

  let filtered = allJobs
    .filter(j => {
      // Recruiter filter
      if (recruiterOnly && !j.recruiter) return false;
      return true;
    })
    .filter(j => {
      if (sources.length === 0) return true;
      const jobSource = (j.source || "").toLowerCase();
      return sources.some(s => jobSource.includes(s) || s.includes(jobSource));
    })
    .filter(j => inToronto(j.location || "", location))
    .filter(j => keywords.length === 0 || includesAny(j.title + " " + (j.excerpt || "") + " " + (j.company || ""), keywords))
    .filter(j => matchesEmploymentType(j, employmentTypes))
    .filter(j => isWithinDateFilter(j, dateFilter))
    .filter(j => matchesDeadlineFilter(j, deadlineFilter))
    .filter(j => matchesWorkArrangement(j, workArrangement))
    .filter(j => matchesExperienceLevel(j, experienceLevel));

  // Filter out generic links if checkbox is checked
  const hideGeneric = el("hideGenericLinks")?.checked;
  if (hideGeneric) {
    filtered = filtered.filter(j => !isGenericLink(j));
  }

  // Sort based on user preference
  filtered = sortJobs(filtered, sortBy, keywords);

  // Update URL state
  updateURLState();

  return {
    meta: {
      minSalary, location, keywords, sources, dateFilter, employmentTypes,
      workArrangement, experienceLevel, sortBy,
      totalFetched: allJobs.length, totalMatched: filtered.length
    },
    jobs: filtered
  };
}

function sortJobs(jobs, sortBy, keywords = []) {
  return [...jobs].sort((a, b) => {
    switch (sortBy) {
      case 'salary-desc': {
        const salaryA = a.salary?.max || a.salary?.min || 0;
        const salaryB = b.salary?.max || b.salary?.min || 0;
        return salaryB - salaryA;
      }
      case 'salary-asc': {
        const salaryA = a.salary?.max || a.salary?.min || Infinity;
        const salaryB = b.salary?.max || b.salary?.min || Infinity;
        return salaryA - salaryB;
      }
      case 'company': {
        return (a.company || '').localeCompare(b.company || '');
      }
      case 'relevance': {
        // Score based on keyword matches in title
        const scoreA = keywords.reduce((s, k) =>
          s + (a.title.toLowerCase().includes(k.toLowerCase()) ? 2 : 0) +
          ((a.excerpt || '').toLowerCase().includes(k.toLowerCase()) ? 1 : 0), 0);
        const scoreB = keywords.reduce((s, k) =>
          s + (b.title.toLowerCase().includes(k.toLowerCase()) ? 2 : 0) +
          ((b.excerpt || '').toLowerCase().includes(k.toLowerCase()) ? 1 : 0), 0);
        if (scoreB !== scoreA) return scoreB - scoreA;
        // Fall through to date
      }
      case 'date':
      default: {
        const dateA = a.postedDate ? new Date(a.postedDate).getTime() : 0;
        const dateB = b.postedDate ? new Date(b.postedDate).getTime() : 0;
        return dateB - dateA;
      }
    }
  });
}

function render(data) {
  const meta = data?.meta;
  const jobs = Array.isArray(data?.jobs) ? data.jobs : [];

  // Reset keyboard navigation
  currentJobIndex = -1;

  el("meta").innerHTML = meta
    ? `<strong>${meta.totalMatched.toLocaleString()}</strong> jobs matched from <strong>${meta.totalFetched.toLocaleString()}</strong> total`
    : "";

  const list = el("list");
  list.innerHTML = "";

  if (!jobs.length) {
    const empty = document.createElement("div");
    empty.className = "card empty-card";
    empty.innerHTML = `
      <h3>No matches found</h3>
      <p>Try different keywords or expand your filters:</p>
      <ul>
        <li>Remove some keywords</li>
        <li>Extend the date range</li>
        <li>Change work arrangement to "Any"</li>
        <li>Enable more job sources</li>
      </ul>
    `;
    list.appendChild(empty);
    return;
  }

  for (let i = 0; i < jobs.length; i++) {
    const j = jobs[i];
    const isSaved = isJobSaved(j);

    const card = document.createElement("div");
    card.className = "card" + (isSaved ? " saved" : "");
    card.dataset.index = i;
    card.dataset.url = j.url;
    card.tabIndex = 0;

    const titleRow = document.createElement("div");
    titleRow.className = "titleRow";

    const titleLeft = document.createElement("div");
    titleLeft.className = "titleLeft";

    // Save button
    const saveBtn = document.createElement("button");
    saveBtn.className = "save-btn" + (isSaved ? " saved" : "");
    saveBtn.innerHTML = isSaved ? "★" : "☆";
    saveBtn.title = isSaved ? "Remove from saved" : "Save job";
    saveBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const nowSaved = toggleSaveJob(j);
      saveBtn.innerHTML = nowSaved ? "★" : "☆";
      saveBtn.className = "save-btn" + (nowSaved ? " saved" : "");
      card.className = "card" + (nowSaved ? " saved" : "");
    });

    const a = document.createElement("a");
    a.href = j.url;
    a.target = "_blank";
    a.rel = "noreferrer noopener";
    a.textContent = j.title;

    const rightInfo = document.createElement("div");
    rightInfo.className = "rightInfo";

    const dateSpan = document.createElement("span");
    dateSpan.className = "posted-date";
    dateSpan.textContent = formatDate(j); // Pass whole job for date uncertainty info

    // Format salary/rate
    const salarySpan = document.createElement("span");
    salarySpan.className = "salary";

    let salaryText = "";
    if (j.salary) {
      if (typeof j.salary === "string") {
        salaryText = j.salary;
      } else if (j.salary.display) {
        salaryText = j.salary.display;
      } else if (j.salary.min || j.salary.max) {
        const min = j.salary.min;
        const max = j.salary.max || min;
        const type = j.salary.type || "annual";

        if (type === "hourly") {
          salaryText = max !== min ? `$${min}-$${max}/hr` : `$${min}/hr`;
        } else {
          const minK = Math.round(min / 1000);
          const maxK = Math.round(max / 1000);
          salaryText = maxK !== minK ? `$${minK}K-$${maxK}K` : `$${minK}K`;
        }
      }
    }
    salarySpan.textContent = salaryText;

    // Deadline display
    const deadlineSpan = document.createElement("span");
    deadlineSpan.className = "deadline";
    const deadline = j.deadline || j.applicationDeadline || j.closingDate;
    if (deadline) {
      const deadlineDate = new Date(deadline);
      if (!isNaN(deadlineDate.getTime())) {
        const now = new Date();
        const daysLeft = Math.ceil((deadlineDate - now) / (1000 * 60 * 60 * 24));
        if (daysLeft < 0) {
          deadlineSpan.textContent = "Expired";
          deadlineSpan.classList.add("expired");
        } else if (daysLeft === 0) {
          deadlineSpan.textContent = "Due today!";
          deadlineSpan.classList.add("urgent");
        } else if (daysLeft <= 3) {
          deadlineSpan.textContent = `${daysLeft}d left`;
          deadlineSpan.classList.add("urgent");
        } else if (daysLeft <= 7) {
          deadlineSpan.textContent = `${daysLeft}d left`;
          deadlineSpan.classList.add("soon");
        } else {
          deadlineSpan.textContent = `Due: ${deadlineDate.toLocaleDateString("en-CA", { month: "short", day: "numeric" })}`;
        }
      }
    }

    rightInfo.appendChild(dateSpan);
    if (salaryText) rightInfo.appendChild(salarySpan);
    if (deadline) rightInfo.appendChild(deadlineSpan);

    // Build title row with save button
    titleLeft.appendChild(saveBtn);
    titleLeft.appendChild(a);
    titleRow.appendChild(titleLeft);
    titleRow.appendChild(rightInfo);

    const tags = document.createElement("div");
    tags.className = "tagRow";

    const addTag = (v, cls = "") => {
      if (!v) return;
      const t = document.createElement("span");
      t.className = "tag" + (cls ? " " + cls : "");
      t.textContent = v;
      tags.appendChild(t);
    };

    addTag(j.company, "company");
    addTag(j.location, "location");
    addTag(j.source, "source source-" + (j.source || "").toLowerCase().replace(/\s+/g, '-'));

    // Work arrangement tag
    const workArr = detectWorkArrangement(j);
    if (workArr === 'remote') addTag('Remote', 'remote');
    else if (workArr === 'hybrid') addTag('Hybrid', 'hybrid');

    // Experience level tag
    const expLevel = detectExperienceLevel(j);
    if (expLevel !== 'unknown') {
      const expLabels = { entry: 'Entry', mid: 'Mid', senior: 'Senior', lead: 'Lead', manager: 'Director+' };
      addTag(expLabels[expLevel] || expLevel, `exp-${expLevel}`);
    }

    // Employment type with distinct styling
    const empType = j.employmentType || "unknown";
    if (empType !== "unknown") {
      const typeClass = `type type-${empType.replace(/\s+/g, '-')}`;
      addTag(empType, typeClass);
    }

    // Show recruiter if present
    if (j.recruiter && j.recruiter !== j.company) {
      addTag(`via ${j.recruiter}`, "recruiter");
    }

    const excerpt = document.createElement("div");
    excerpt.className = "excerpt";
    excerpt.textContent = decodeHtmlEntities(j.excerpt || "").substring(0, 200);

    card.appendChild(titleRow);

    // Badges row (freshness, salary disclosure, remote)
    const badgesRow = document.createElement("div");
    badgesRow.className = "badges-row";

    // Freshness badge
    const postedDate = new Date(j.postedDate || j.scrapedAt);
    if (!isNaN(postedDate.getTime())) {
      const hoursAgo = Math.floor((Date.now() - postedDate) / (1000 * 60 * 60));
      if (hoursAgo < 24) {
        const freshBadge = document.createElement("span");
        freshBadge.className = "badge badge-fresh";
        if (hoursAgo < 1) {
          freshBadge.textContent = "Just posted";
        } else if (hoursAgo === 1) {
          freshBadge.textContent = "Posted 1h ago";
        } else {
          freshBadge.textContent = `Posted ${hoursAgo}h ago`;
        }
        badgesRow.appendChild(freshBadge);
      }
    }

    // Salary disclosed badge
    if (salaryText) {
      const salaryBadge = document.createElement("span");
      salaryBadge.className = "badge badge-salary";
      salaryBadge.textContent = "💰 Salary disclosed";
      salaryBadge.title = salaryText;
      badgesRow.appendChild(salaryBadge);
    }

    // Remote/Hybrid badge
    if (workArr === 'remote') {
      const remoteBadge = document.createElement("span");
      remoteBadge.className = "badge badge-remote";
      remoteBadge.textContent = "🏠 Remote";
      badgesRow.appendChild(remoteBadge);
    } else if (workArr === 'hybrid') {
      const hybridBadge = document.createElement("span");
      hybridBadge.className = "badge badge-hybrid";
      hybridBadge.textContent = "🔀 Hybrid";
      badgesRow.appendChild(hybridBadge);
    }

    if (badgesRow.children.length > 0) {
      card.appendChild(badgesRow);
    }

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

  // Apply URL state on load
  applyStateFromURL();

  // Update saved count
  updateSavedCount();

  // Preset buttons
  el("preset110").addEventListener("click", () => {
    minSalary.value = "110000";
    syncSalaryLabel();
    render(filterJobs());
  });

  el("clearFilters")?.addEventListener("click", () => {
    el("keywords").value = "";
    el("location").value = "Toronto, ON";
    el("dateFilter").value = "week";
    if (el("deadlineFilter")) el("deadlineFilter").value = "any";
    if (el("workArrangement")) el("workArrangement").value = "any";
    if (el("experienceLevel")) el("experienceLevel").value = "any";
    if (el("sortBy")) el("sortBy").value = "date";
    minSalary.value = "50000";
    syncSalaryLabel();
    // Reset source filters
    document.querySelectorAll(".source-filters input").forEach(cb => cb.checked = true);
    // Reset employment type filters to defaults
    document.querySelectorAll(".emp-type").forEach(cb => {
      cb.checked = cb.value === "full-time" || cb.value === "contract" || cb.value === "unknown";
    });
    // Clear URL params
    history.replaceState(null, '', window.location.pathname);
    render(filterJobs());
  });

  // Share search button
  el("shareSearch")?.addEventListener("click", copyShareableLink);

  // Saved jobs panel
  el("savedJobsNav")?.addEventListener("click", (e) => {
    e.preventDefault();
    showingSavedPanel = !showingSavedPanel;
    el("savedJobsPanel").style.display = showingSavedPanel ? "block" : "none";
    if (showingSavedPanel) renderSavedJobs();
  });

  el("closeSavedPanel")?.addEventListener("click", () => {
    showingSavedPanel = false;
    el("savedJobsPanel").style.display = "none";
  });

  el("search").addEventListener("click", () => loadAndRender(true));

  // Live filtering
  const liveFilter = () => render(filterJobs());

  el("dateFilter")?.addEventListener("change", liveFilter);
  el("deadlineFilter")?.addEventListener("change", liveFilter);
  el("workArrangement")?.addEventListener("change", liveFilter);
  el("experienceLevel")?.addEventListener("change", liveFilter);
  el("sortBy")?.addEventListener("change", liveFilter);

  // Remove old fullTimeOnly if it exists (may throw, ignore)
  try { el("fullTimeOnly")?.addEventListener("change", liveFilter); } catch { }

  document.querySelectorAll(".source-filters input").forEach(cb => {
    cb.addEventListener("change", liveFilter);
  });

  // Employment type filter change handlers
  document.querySelectorAll(".emp-type").forEach(cb => {
    cb.addEventListener("change", liveFilter);
  });

  // Recruiter filter
  el("recruiterFilter")?.addEventListener("change", liveFilter);
  el("hideGenericLinks")?.addEventListener("change", liveFilter);

  // Preset keyword buttons
  document.querySelectorAll(".preset-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      el("keywords").value = btn.dataset.keywords;
      render(filterJobs());
    });
  });

  // Enter key on inputs
  el("keywords").addEventListener("keypress", (e) => {
    if (e.key === "Enter") render(filterJobs());
  });
  el("location").addEventListener("keypress", (e) => {
    if (e.key === "Enter") render(filterJobs());
  });

  // Keyboard navigation
  document.addEventListener("keydown", handleKeyboardNav);
}

// Keyboard navigation handler
function handleKeyboardNav(e) {
  // Don't intercept if user is typing in an input
  if (e.target.tagName === 'INPUT' || e.target.tagName === 'SELECT' || e.target.tagName === 'TEXTAREA') {
    return;
  }

  const cards = document.querySelectorAll("#list .card:not(.empty-card)");
  if (cards.length === 0) return;

  switch (e.key) {
    case 'j': // Next job
      e.preventDefault();
      currentJobIndex = Math.min(currentJobIndex + 1, cards.length - 1);
      highlightCard(cards, currentJobIndex);
      break;
    case 'k': // Previous job
      e.preventDefault();
      currentJobIndex = Math.max(currentJobIndex - 1, 0);
      highlightCard(cards, currentJobIndex);
      break;
    case 's': // Save current job
      if (currentJobIndex >= 0 && currentJobIndex < cards.length) {
        e.preventDefault();
        const saveBtn = cards[currentJobIndex].querySelector('.save-btn');
        if (saveBtn) saveBtn.click();
      }
      break;
    case 'Enter': // Open current job
      if (currentJobIndex >= 0 && currentJobIndex < cards.length) {
        e.preventDefault();
        const link = cards[currentJobIndex].querySelector('a');
        if (link) window.open(link.href, '_blank');
      }
      break;
    case 'Escape':
      // Close saved panel if open
      if (showingSavedPanel) {
        showingSavedPanel = false;
        el("savedJobsPanel").style.display = "none";
      }
      // Remove highlight
      cards.forEach(c => c.classList.remove('highlighted'));
      currentJobIndex = -1;
      break;
  }
}

function highlightCard(cards, index) {
  cards.forEach(c => c.classList.remove('highlighted'));
  if (index >= 0 && index < cards.length) {
    cards[index].classList.add('highlighted');
    cards[index].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

async function loadAndRender(forceRefresh = false) {
  setLoading(true);
  try {
    const data = await fetchJobs(forceRefresh);
    render(data);
  } catch (e) {
    el("meta").textContent = "Error: " + String(e?.message || e);
    el("list").innerHTML = "";
  } finally {
    setLoading(false);
  }
}

// Initialize
loadAndRender();
bind();
