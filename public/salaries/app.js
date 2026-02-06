let allJobs = [];
let salaryJobs = [];
let tableDisplayed = 50;
let currentSort = { field: 'salary', dir: 'desc' };

function el(id) { return document.getElementById(id); }

function formatK(n) {
  if (n >= 1000) return `$${Math.round(n / 1000)}K`;
  return `$${Math.round(n).toLocaleString()}`;
}

function formatFull(n) {
  return new Intl.NumberFormat('en-CA', { style: 'currency', currency: 'CAD', maximumFractionDigits: 0 }).format(n);
}

function median(arr) {
  if (!arr.length) return 0;
  const s = [...arr].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid] : (s[mid - 1] + s[mid]) / 2;
}

function detectExperienceLevel(job) {
  const text = `${job.title} ${job.excerpt || ''}`.toLowerCase();
  if (text.includes('director') || text.includes('vp ') || text.includes('vice president') ||
      text.includes('head of') || text.includes('chief ')) return 'manager';
  if (text.includes('lead') || text.includes('principal') || text.includes('staff ') ||
      text.includes('architect')) return 'lead';
  if (text.includes('senior') || text.includes('sr.') || text.includes('sr ') ||
      text.includes('5+ years') || text.includes('7+ years') || text.includes('10+ years')) return 'senior';
  if (text.includes('junior') || text.includes('jr.') || text.includes('jr ') ||
      text.includes('entry') || text.includes('graduate') || text.includes('new grad') ||
      text.includes('intern') || text.includes('co-op') || text.includes('early career')) return 'entry';
  if (text.includes('mid') || text.includes('intermediate') || text.includes('2-5 years') ||
      text.includes('3-5 years') || text.includes('3+ years')) return 'mid';
  return 'unknown';
}

function detectWorkArrangement(job) {
  const text = `${job.title} ${job.location} ${job.excerpt || ''}`.toLowerCase();
  if (text.includes('remote') || text.includes('work from home') || text.includes('wfh') || text.includes('anywhere')) {
    if (text.includes('hybrid') || text.includes('flexible')) return 'hybrid';
    return 'remote';
  }
  if (text.includes('hybrid') || text.includes('flexible location')) return 'hybrid';
  if (text.includes('onsite') || text.includes('on-site') || text.includes('in-office')) return 'onsite';
  return 'unknown';
}

function normalizeRoleTitle(title) {
  // Normalize common role patterns
  let t = title.replace(/\s*(sr\.?|senior|junior|jr\.?|lead|principal|staff|intern|co-op)\s*/gi, ' ').trim();
  t = t.replace(/\s*(I|II|III|IV|V)\s*$/i, '').trim();
  t = t.replace(/\s*[-–]\s*.*$/, '').trim(); // Remove after dash
  t = t.replace(/\s*\(.*\)/, '').trim(); // Remove parenthetical
  return t.substring(0, 50);
}

function getAnnualSalary(job) {
  if (!job.salary) return null;
  const s = job.salary;
  if (s.type === 'hourly') {
    const rate = s.max || s.min;
    return rate ? rate * 2080 : null; // Standard work hours
  }
  return s.max || s.min || null;
}

function getMinSalary(job) {
  if (!job.salary) return null;
  const s = job.salary;
  if (s.type === 'hourly') {
    return s.min ? s.min * 2080 : null;
  }
  return s.min || null;
}

async function loadJobs() {
  const res = await fetch('/gotjob/jobs.json?t=' + Date.now());
  if (!res.ok) throw new Error('Failed to load jobs');
  const data = await res.json();
  allJobs = Array.isArray(data.jobs) ? data.jobs : (Array.isArray(data) ? data : []);
  return allJobs;
}

function filterAndAnalyze() {
  const roleSearch = el('roleSearch').value.toLowerCase().trim();
  const expFilter = el('expFilter').value;
  const workFilter = el('workFilter').value;

  // Filter to jobs with valid salary data
  salaryJobs = allJobs.filter(j => {
    const salary = getAnnualSalary(j);
    if (!salary || salary < 20000 || salary > 500000) return false;

    if (roleSearch) {
      const text = `${j.title} ${j.company || ''} ${j.excerpt || ''}`.toLowerCase();
      const terms = roleSearch.split(',').map(t => t.trim()).filter(Boolean);
      if (!terms.some(t => text.includes(t))) return false;
    }

    if (expFilter !== 'all' && detectExperienceLevel(j) !== expFilter) return false;
    if (workFilter !== 'all') {
      const wa = detectWorkArrangement(j);
      if (wa !== workFilter && wa !== 'unknown') return false;
    }

    return true;
  });

  renderStats();
  renderDistribution();
  renderTopRoles();
  renderExperienceLevels();
  renderTopCompanies();
  renderTable();
}

function renderStats() {
  const salaries = salaryJobs.map(j => getAnnualSalary(j)).filter(Boolean);
  const med = median(salaries);
  const avg = salaries.length ? salaries.reduce((a, b) => a + b, 0) / salaries.length : 0;
  const min = salaries.length ? Math.min(...salaries) : 0;
  const max = salaries.length ? Math.max(...salaries) : 0;

  el('statJobsWithSalary').textContent = salaryJobs.length.toLocaleString();
  el('statMedian').textContent = formatK(med);
  el('statAvg').textContent = formatK(avg);
  el('statRange').textContent = salaries.length ? `${formatK(min)} - ${formatK(max)}` : '-';
}

function renderDistribution() {
  const chart = el('distChart');
  chart.innerHTML = '';

  const salaries = salaryJobs.map(j => getAnnualSalary(j)).filter(Boolean);
  if (!salaries.length) {
    chart.innerHTML = '<div class="loading">No salary data available for this filter</div>';
    return;
  }

  // Create buckets
  const bucketSize = 10000;
  const minBucket = Math.floor(Math.min(...salaries) / bucketSize) * bucketSize;
  const maxBucket = Math.ceil(Math.max(...salaries) / bucketSize) * bucketSize;
  const buckets = {};

  for (let b = minBucket; b <= maxBucket; b += bucketSize) {
    buckets[b] = 0;
  }

  for (const s of salaries) {
    const bucket = Math.floor(s / bucketSize) * bucketSize;
    buckets[bucket] = (buckets[bucket] || 0) + 1;
  }

  const maxCount = Math.max(...Object.values(buckets), 1);
  const entries = Object.entries(buckets).sort((a, b) => Number(a[0]) - Number(b[0]));

  // Limit to reasonable number of bars
  const displayEntries = entries.length > 20 ? entries.filter((_, i) => i % 2 === 0) : entries;

  for (const [bucket, count] of displayEntries) {
    const col = document.createElement('div');
    col.className = 'bar-col';

    const countLabel = document.createElement('div');
    countLabel.className = 'bar-count';
    countLabel.textContent = count || '';

    const bar = document.createElement('div');
    bar.className = 'bar';
    bar.style.height = `${Math.max((count / maxCount) * 100, 2)}%`;
    bar.title = `${formatK(Number(bucket))} - ${formatK(Number(bucket) + bucketSize)}: ${count} jobs`;

    const label = document.createElement('div');
    label.className = 'bar-label';
    label.textContent = formatK(Number(bucket));

    col.appendChild(countLabel);
    col.appendChild(bar);
    col.appendChild(label);
    chart.appendChild(col);
  }

  el('distSubtitle').textContent = `Annual salaries across ${salaries.length.toLocaleString()} matching jobs`;
}

function renderTopRoles() {
  const chart = el('topRolesChart');
  chart.innerHTML = '';

  // Group by normalized role
  const roleMap = {};
  for (const j of salaryJobs) {
    const role = normalizeRoleTitle(j.title);
    if (!role || role.length < 3) continue;
    if (!roleMap[role]) roleMap[role] = [];
    const salary = getAnnualSalary(j);
    if (salary) roleMap[role].push(salary);
  }

  // Get roles with at least 2 data points
  const roles = Object.entries(roleMap)
    .filter(([, arr]) => arr.length >= 2)
    .map(([role, arr]) => ({
      role,
      median: median(arr),
      count: arr.length,
      min: Math.min(...arr),
      max: Math.max(...arr)
    }))
    .sort((a, b) => b.median - a.median)
    .slice(0, 15);

  if (!roles.length) {
    chart.innerHTML = '<div class="loading">Not enough data for role comparison</div>';
    return;
  }

  const maxSalary = Math.max(...roles.map(r => r.median));

  for (const r of roles) {
    const row = document.createElement('div');
    row.className = 'h-bar-row';

    const label = document.createElement('div');
    label.className = 'h-bar-label';
    label.textContent = r.role;
    label.title = `${r.role} (${r.count} jobs, range: ${formatK(r.min)} - ${formatK(r.max)})`;

    const track = document.createElement('div');
    track.className = 'h-bar-track';

    const fill = document.createElement('div');
    fill.className = 'h-bar-fill role';
    fill.style.width = `${(r.median / maxSalary) * 100}%`;

    track.appendChild(fill);

    const value = document.createElement('div');
    value.className = 'h-bar-value';
    value.innerHTML = `${formatK(r.median)}<span class="h-bar-count">(${r.count})</span>`;

    row.appendChild(label);
    row.appendChild(track);
    row.appendChild(value);
    chart.appendChild(row);
  }
}

function renderExperienceLevels() {
  const grid = el('expGrid');
  grid.innerHTML = '';

  const levels = ['entry', 'mid', 'senior', 'lead', 'manager'];
  const levelNames = { entry: 'Entry / Junior', mid: 'Mid Level', senior: 'Senior', lead: 'Lead / Principal', manager: 'Manager / Director' };

  for (const level of levels) {
    const jobs = salaryJobs.filter(j => detectExperienceLevel(j) === level);
    const salaries = jobs.map(j => getAnnualSalary(j)).filter(Boolean);

    const card = document.createElement('div');
    card.className = `exp-card ${level}`;

    const name = document.createElement('div');
    name.className = 'level-name';
    name.textContent = levelNames[level];

    const salary = document.createElement('div');
    salary.className = 'level-salary';
    salary.textContent = salaries.length ? formatK(median(salaries)) : 'N/A';

    const range = document.createElement('div');
    range.className = 'level-range';
    range.textContent = salaries.length >= 2
      ? `${formatK(Math.min(...salaries))} - ${formatK(Math.max(...salaries))}`
      : 'Limited data';

    const count = document.createElement('div');
    count.className = 'level-count';
    count.textContent = `${salaries.length} jobs`;

    card.appendChild(name);
    card.appendChild(salary);
    card.appendChild(range);
    card.appendChild(count);
    grid.appendChild(card);
  }
}

function renderTopCompanies() {
  const chart = el('companyChart');
  chart.innerHTML = '';

  const companyMap = {};
  for (const j of salaryJobs) {
    const company = (j.company || '').trim();
    if (!company || company.length < 2) continue;
    if (!companyMap[company]) companyMap[company] = [];
    const salary = getAnnualSalary(j);
    if (salary) companyMap[company].push(salary);
  }

  const companies = Object.entries(companyMap)
    .filter(([, arr]) => arr.length >= 2)
    .map(([company, arr]) => ({
      company,
      avg: Math.round(arr.reduce((a, b) => a + b, 0) / arr.length),
      count: arr.length,
      median: median(arr)
    }))
    .sort((a, b) => b.median - a.median)
    .slice(0, 15);

  if (!companies.length) {
    chart.innerHTML = '<div class="loading">Not enough data for company comparison</div>';
    return;
  }

  const maxSalary = Math.max(...companies.map(c => c.median));

  for (const c of companies) {
    const row = document.createElement('div');
    row.className = 'h-bar-row';

    const label = document.createElement('div');
    label.className = 'h-bar-label';
    label.textContent = c.company;

    const track = document.createElement('div');
    track.className = 'h-bar-track';

    const fill = document.createElement('div');
    fill.className = 'h-bar-fill company';
    fill.style.width = `${(c.median / maxSalary) * 100}%`;

    track.appendChild(fill);

    const value = document.createElement('div');
    value.className = 'h-bar-value';
    value.innerHTML = `${formatK(c.median)}<span class="h-bar-count">(${c.count})</span>`;

    row.appendChild(label);
    row.appendChild(track);
    row.appendChild(value);
    chart.appendChild(row);
  }
}

function renderTable() {
  const tbody = el('salaryTableBody');
  tbody.innerHTML = '';

  // Sort salary jobs
  const sorted = [...salaryJobs].sort((a, b) => {
    const dir = currentSort.dir === 'desc' ? -1 : 1;
    switch (currentSort.field) {
      case 'salary': return dir * ((getAnnualSalary(a) || 0) - (getAnnualSalary(b) || 0));
      case 'title': return dir * (a.title || '').localeCompare(b.title || '');
      case 'company': return dir * (a.company || '').localeCompare(b.company || '');
      case 'level': return dir * detectExperienceLevel(a).localeCompare(detectExperienceLevel(b));
      default: return 0;
    }
  });

  const display = sorted.slice(0, tableDisplayed);

  for (const j of display) {
    const tr = document.createElement('tr');
    const level = detectExperienceLevel(j);
    const salary = getAnnualSalary(j);
    const levelNames = { entry: 'Entry', mid: 'Mid', senior: 'Senior', lead: 'Lead', manager: 'Director+', unknown: '-' };

    tr.innerHTML = `
      <td><a href="${j.url}" target="_blank" rel="noreferrer" class="role-link">${j.title}</a></td>
      <td>${j.company || '-'}</td>
      <td class="salary-cell">${salary ? formatFull(salary) : '-'}</td>
      <td><span class="level-badge ${level}">${levelNames[level]}</span></td>
      <td>${j.employmentType || '-'}</td>
    `;
    tbody.appendChild(tr);
  }

  el('tableCount').textContent = `Showing ${display.length} of ${salaryJobs.length} jobs with salary data`;
  el('loadMore').style.display = tableDisplayed < salaryJobs.length ? 'inline-block' : 'none';
}

function bindEvents() {
  el('searchBtn').addEventListener('click', () => {
    tableDisplayed = 50;
    filterAndAnalyze();
  });

  el('roleSearch').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      tableDisplayed = 50;
      filterAndAnalyze();
    }
  });

  el('expFilter').addEventListener('change', () => {
    tableDisplayed = 50;
    filterAndAnalyze();
  });

  el('workFilter').addEventListener('change', () => {
    tableDisplayed = 50;
    filterAndAnalyze();
  });

  el('loadMore').addEventListener('click', () => {
    tableDisplayed += 50;
    renderTable();
  });

  // Table sort headers
  document.querySelectorAll('.salary-table th.sortable').forEach(th => {
    th.addEventListener('click', () => {
      const field = th.dataset.sort;
      if (currentSort.field === field) {
        currentSort.dir = currentSort.dir === 'desc' ? 'asc' : 'desc';
      } else {
        currentSort = { field, dir: 'desc' };
      }
      document.querySelectorAll('.salary-table th').forEach(h => h.classList.remove('active'));
      th.classList.add('active');
      th.classList.toggle('asc', currentSort.dir === 'asc');
      renderTable();
    });
  });
}

async function init() {
  try {
    await loadJobs();
    filterAndAnalyze();
    bindEvents();
  } catch (e) {
    document.querySelector('.container').innerHTML += `<div class="panel"><div class="loading">Error loading data: ${e.message}</div></div>`;
  }
}

init();
