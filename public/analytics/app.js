let allJobs = [];

function el(id) { return document.getElementById(id); }

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

function detectExperienceLevel(job) {
  const text = `${job.title} ${job.excerpt || ''}`.toLowerCase();
  if (text.includes('director') || text.includes('vp ') || text.includes('vice president') ||
      text.includes('head of') || text.includes('chief ')) return 'manager';
  if (text.includes('lead') || text.includes('principal') || text.includes('staff ') ||
      text.includes('architect')) return 'lead';
  if (text.includes('senior') || text.includes('sr.') || text.includes('sr ')) return 'senior';
  if (text.includes('junior') || text.includes('jr.') || text.includes('jr ') ||
      text.includes('entry') || text.includes('graduate') || text.includes('intern')) return 'entry';
  if (text.includes('mid') || text.includes('intermediate')) return 'mid';
  return 'unknown';
}

function detectEmploymentType(job) {
  const type = (job.employmentType || '').toLowerCase();
  if (type && type !== 'unknown') return type;
  const text = `${job.title} ${job.excerpt || ''}`.toLowerCase();
  if (text.includes('full-time') || text.includes('full time') || text.includes('permanent')) return 'full-time';
  if (text.includes('contract') || text.includes('contractor')) return 'contract';
  if (text.includes('part-time') || text.includes('part time')) return 'part-time';
  if (text.includes('intern') || text.includes('co-op')) return 'internship';
  return 'unknown';
}

// Categorize role from title
function categorizeRole(title) {
  const t = title.toLowerCase();
  const roles = [
    { pattern: /developer|software eng|swe |full.?stack|front.?end|back.?end|web dev/i, label: 'Software Developer' },
    { pattern: /data scien|machine learn|ml eng|ai eng/i, label: 'Data Science / ML' },
    { pattern: /data analy|business analy|bi analy/i, label: 'Data / Business Analyst' },
    { pattern: /devops|sre|site reliab|platform eng|infra/i, label: 'DevOps / SRE' },
    { pattern: /product manag/i, label: 'Product Manager' },
    { pattern: /project manag|scrum|agile/i, label: 'Project Manager' },
    { pattern: /design|ux|ui |creative/i, label: 'UX / Design' },
    { pattern: /qa |quality|test eng|sdet/i, label: 'QA / Testing' },
    { pattern: /security|cyber|infosec/i, label: 'Security / Cyber' },
    { pattern: /cloud|aws|azure|gcp/i, label: 'Cloud Engineering' },
    { pattern: /manager|director|head of|vp /i, label: 'Management / Leadership' },
    { pattern: /market|seo|growth|content/i, label: 'Marketing' },
    { pattern: /sales|account exec|bdr|sdr/i, label: 'Sales' },
    { pattern: /hr |human resource|people|talent|recruit/i, label: 'HR / People Ops' },
    { pattern: /finance|account|payroll/i, label: 'Finance / Accounting' },
    { pattern: /support|helpdesk|customer|service desk/i, label: 'Support / Help Desk' },
    { pattern: /network|system admin|sysadmin/i, label: 'IT / Systems Admin' },
    { pattern: /servicenow/i, label: 'ServiceNow' },
    { pattern: /consultant|advisory/i, label: 'Consulting' },
  ];
  for (const r of roles) {
    if (r.pattern.test(t)) return r.label;
  }
  return 'Other';
}

// Extract skills from job text
function extractSkills(text) {
  const t = text.toLowerCase();
  const skillMap = {
    'Python': /python/i, 'JavaScript': /javascript|node\.?js/i, 'React': /react/i,
    'SQL': /\bsql\b/i, 'AWS': /\baws\b/i, 'Azure': /azure/i,
    'Java': /\bjava\b(?!script)/i, 'C#': /\bc#|\.net/i, 'TypeScript': /typescript/i,
    'Docker': /docker/i, 'Kubernetes': /kubernetes|k8s/i, 'Git': /\bgit\b/i,
    'Linux': /linux/i, 'Agile': /agile|scrum/i, 'REST API': /rest\s*api|restful/i,
    'Machine Learning': /machine learn|ml\b/i, 'Terraform': /terraform/i,
    'Power BI': /power\s*bi/i, 'Tableau': /tableau/i, 'Excel': /excel|vba/i,
    'ServiceNow': /servicenow/i, 'Salesforce': /salesforce/i,
    'CI/CD': /ci\/?cd|jenkins|github actions/i, 'GraphQL': /graphql/i,
    'MongoDB': /mongodb|mongo/i, 'PostgreSQL': /postgres|postgresql/i,
    'Angular': /angular/i, 'Vue.js': /vue\.?js|vuejs/i,
    'Jira': /jira/i, 'Confluence': /confluence/i,
    'SAP': /\bsap\b/i, 'Oracle': /oracle/i,
    'Go': /\bgolang\b|\bgo\b/i, 'Rust': /\brust\b/i,
    'PHP': /\bphp\b/i, 'Ruby': /\bruby\b/i,
    'Figma': /figma/i, 'Alteryx': /alteryx/i,
  };
  const found = {};
  for (const [skill, pattern] of Object.entries(skillMap)) {
    if (pattern.test(t)) found[skill] = true;
  }
  return Object.keys(found);
}

const CHART_COLORS = [
  '#7c5cff', '#10b981', '#f59e0b', '#ef4444', '#60a5fa',
  '#f472b6', '#a78bfa', '#34d399', '#fbbf24', '#fb923c',
  '#818cf8', '#4ade80', '#fcd34d', '#f87171', '#38bdf8',
  '#c084fc', '#2dd4bf', '#fb7185', '#a3e635', '#e879f9'
];

async function loadJobs() {
  const res = await fetch('/gotjob/jobs.json?t=' + Date.now());
  if (!res.ok) throw new Error('Failed to load jobs');
  const data = await res.json();
  allJobs = Array.isArray(data.jobs) ? data.jobs : (Array.isArray(data) ? data : []);
}

function renderMetrics() {
  const total = allJobs.length;
  const today = allJobs.filter(j => {
    const d = new Date(j.postedDate || j.scrapedAt);
    return !isNaN(d) && (Date.now() - d) < 24 * 60 * 60 * 1000;
  }).length;
  const companies = new Set(allJobs.map(j => (j.company || '').trim().toLowerCase()).filter(Boolean)).size;
  const remote = allJobs.filter(j => detectWorkArrangement(j) === 'remote').length;
  const withSalary = allJobs.filter(j => j.salary?.min || j.salary?.max).length;
  const sources = new Set(allJobs.map(j => (j.source || '').toLowerCase()).filter(Boolean)).size;

  el('metricTotal').textContent = total.toLocaleString();
  el('metricFresh').textContent = today.toLocaleString();
  el('metricCompanies').textContent = companies.toLocaleString();
  el('metricRemote').textContent = remote.toLocaleString();
  el('metricWithSalary').textContent = `${Math.round(withSalary / total * 100)}%`;
  el('metricSources').textContent = sources;
}

function renderTimeline() {
  const chart = el('timelineChart');
  chart.innerHTML = '';

  // Group by day for last 30 days
  const days = {};
  const now = new Date();
  for (let i = 29; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const key = d.toISOString().split('T')[0];
    days[key] = 0;
  }

  for (const j of allJobs) {
    const dateStr = j.postedDate || j.scrapedAt;
    if (!dateStr) continue;
    const key = dateStr.split('T')[0];
    if (key in days) days[key]++;
  }

  const entries = Object.entries(days);
  const maxCount = Math.max(...entries.map(e => e[1]), 1);
  const todayKey = now.toISOString().split('T')[0];

  for (const [date, count] of entries) {
    const col = document.createElement('div');
    col.className = 'timeline-bar' + (date === todayKey ? ' today' : '');

    const countLabel = document.createElement('div');
    countLabel.className = 'bar-count';
    countLabel.textContent = count || '';

    const bar = document.createElement('div');
    bar.className = 'bar';
    bar.style.height = `${Math.max((count / maxCount) * 100, 1)}%`;
    bar.title = `${date}: ${count} jobs`;

    const dateLabel = document.createElement('div');
    dateLabel.className = 'bar-date';
    const d = new Date(date + 'T12:00:00');
    dateLabel.textContent = d.toLocaleDateString('en-CA', { month: 'short', day: 'numeric' });

    col.appendChild(countLabel);
    col.appendChild(bar);
    col.appendChild(dateLabel);
    chart.appendChild(col);
  }
}

function renderSourceBreakdown() {
  const donut = el('sourceDonut');
  const legend = el('sourceLegend');

  const sourceMap = {};
  for (const j of allJobs) {
    const src = (j.source || 'unknown').toLowerCase();
    sourceMap[src] = (sourceMap[src] || 0) + 1;
  }

  const sorted = Object.entries(sourceMap).sort((a, b) => b[1] - a[1]);
  const top = sorted.slice(0, 8);
  const otherCount = sorted.slice(8).reduce((s, e) => s + e[1], 0);
  if (otherCount > 0) top.push(['other', otherCount]);

  const total = allJobs.length;
  let cumPct = 0;
  const segments = [];

  for (let i = 0; i < top.length; i++) {
    const pct = (top[i][1] / total) * 100;
    segments.push({ start: cumPct, end: cumPct + pct, color: CHART_COLORS[i] });
    cumPct += pct;
  }

  // CSS conic gradient
  const stops = segments.map(s => `${s.color} ${s.start}% ${s.end}%`).join(', ');
  donut.style.background = `conic-gradient(${stops})`;

  // Legend
  legend.innerHTML = '';
  for (let i = 0; i < top.length; i++) {
    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `
      <span class="legend-dot" style="background:${CHART_COLORS[i]}"></span>
      <span class="legend-label">${top[i][0]}</span>
      <span class="legend-value">${top[i][1].toLocaleString()} (${Math.round(top[i][1]/total*100)}%)</span>
    `;
    legend.appendChild(item);
  }
}

function renderEmploymentTypes() {
  const donut = el('empDonut');
  const legend = el('empLegend');

  const typeMap = {};
  for (const j of allJobs) {
    const type = detectEmploymentType(j);
    typeMap[type] = (typeMap[type] || 0) + 1;
  }

  const sorted = Object.entries(typeMap).sort((a, b) => b[1] - a[1]);
  const total = allJobs.length;
  let cumPct = 0;
  const segments = [];
  const typeColors = {
    'full-time': '#34d399', 'contract': '#fb923c', 'part-time': '#a78bfa',
    'internship': '#38bdf8', 'seasonal': '#f472b6', 'unknown': '#6b7280'
  };

  for (let i = 0; i < sorted.length; i++) {
    const pct = (sorted[i][1] / total) * 100;
    const color = typeColors[sorted[i][0]] || CHART_COLORS[i];
    segments.push({ start: cumPct, end: cumPct + pct, color });
    cumPct += pct;
  }

  const stops = segments.map(s => `${s.color} ${s.start}% ${s.end}%`).join(', ');
  donut.style.background = `conic-gradient(${stops})`;

  legend.innerHTML = '';
  for (let i = 0; i < sorted.length; i++) {
    const color = typeColors[sorted[i][0]] || CHART_COLORS[i];
    const item = document.createElement('div');
    item.className = 'legend-item';
    item.innerHTML = `
      <span class="legend-dot" style="background:${color}"></span>
      <span class="legend-label">${sorted[i][0]}</span>
      <span class="legend-value">${sorted[i][1].toLocaleString()} (${Math.round(sorted[i][1]/total*100)}%)</span>
    `;
    legend.appendChild(item);
  }
}

function renderDemandChart() {
  const chart = el('demandChart');
  chart.innerHTML = '';

  const roleMap = {};
  for (const j of allJobs) {
    const role = categorizeRole(j.title);
    roleMap[role] = (roleMap[role] || 0) + 1;
  }

  const sorted = Object.entries(roleMap)
    .filter(([k]) => k !== 'Other')
    .sort((a, b) => b[1] - a[1])
    .slice(0, 15);

  const maxCount = sorted.length ? sorted[0][1] : 1;

  for (const [role, count] of sorted) {
    const row = document.createElement('div');
    row.className = 'demand-row';
    row.innerHTML = `
      <div class="demand-label">${role}</div>
      <div class="demand-track">
        <div class="demand-fill" style="width:${(count / maxCount) * 100}%"></div>
      </div>
      <div class="demand-count">${count.toLocaleString()}</div>
    `;
    chart.appendChild(row);
  }
}

function renderArrangements() {
  const grid = el('arrangementGrid');
  grid.innerHTML = '';

  const arrMap = { remote: 0, hybrid: 0, onsite: 0 };
  for (const j of allJobs) {
    const wa = detectWorkArrangement(j);
    if (wa === 'remote') arrMap.remote++;
    else if (wa === 'hybrid') arrMap.hybrid++;
    else arrMap.onsite++;
  }

  const total = allJobs.length;
  const items = [
    { key: 'remote', icon: '🏠', label: 'Remote' },
    { key: 'hybrid', icon: '🔄', label: 'Hybrid' },
    { key: 'onsite', icon: '🏢', label: 'Onsite' },
  ];

  for (const item of items) {
    const count = arrMap[item.key];
    const card = document.createElement('div');
    card.className = `arrangement-card ${item.key}`;
    card.innerHTML = `
      <div class="arr-icon">${item.icon}</div>
      <div class="arr-value">${count.toLocaleString()}</div>
      <div class="arr-pct">${Math.round(count / total * 100)}% of listings</div>
      <div class="arr-label">${item.label}</div>
    `;
    grid.appendChild(card);
  }
}

function renderExpDemand() {
  const container = el('expDemand');
  container.innerHTML = '';

  const expMap = {};
  for (const j of allJobs) {
    const level = detectExperienceLevel(j);
    expMap[level] = (expMap[level] || 0) + 1;
  }

  const levels = [
    { key: 'entry', label: 'Entry / Junior' },
    { key: 'mid', label: 'Mid Level' },
    { key: 'senior', label: 'Senior' },
    { key: 'lead', label: 'Lead / Principal' },
    { key: 'manager', label: 'Manager / Director' },
  ];

  const total = allJobs.length;
  const maxCount = Math.max(...levels.map(l => expMap[l.key] || 0), 1);

  for (const level of levels) {
    const count = expMap[level.key] || 0;
    const pct = Math.round(count / total * 100);
    const row = document.createElement('div');
    row.className = 'exp-row';
    row.innerHTML = `
      <div class="exp-label">${level.label}</div>
      <div class="exp-track">
        <div class="exp-fill ${level.key}" style="width:${(count / maxCount) * 100}%">${pct}%</div>
      </div>
      <div class="exp-count">${count.toLocaleString()}</div>
    `;
    container.appendChild(row);
  }
}

function renderSkillsCloud() {
  const cloud = el('skillsCloud');
  cloud.innerHTML = '';

  const skillCounts = {};
  for (const j of allJobs) {
    const text = `${j.title} ${j.excerpt || ''}`;
    const skills = extractSkills(text);
    for (const s of skills) {
      skillCounts[s] = (skillCounts[s] || 0) + 1;
    }
  }

  const sorted = Object.entries(skillCounts).sort((a, b) => b[1] - a[1]).slice(0, 30);
  if (!sorted.length) {
    cloud.innerHTML = '<div class="loading">Not enough data</div>';
    return;
  }

  const maxCount = sorted[0][1];
  const minCount = sorted[sorted.length - 1][1];

  for (const [skill, count] of sorted) {
    const tag = document.createElement('span');
    tag.className = 'skill-tag';

    // Size based on frequency
    const ratio = (count - minCount) / (maxCount - minCount || 1);
    const fontSize = 12 + ratio * 14;
    const opacity = 0.5 + ratio * 0.5;
    const colorIndex = Math.floor(Math.random() * CHART_COLORS.length);

    tag.style.fontSize = `${fontSize}px`;
    tag.style.background = CHART_COLORS[colorIndex] + '25';
    tag.style.color = CHART_COLORS[colorIndex];
    tag.style.border = `1px solid ${CHART_COLORS[colorIndex]}40`;
    tag.style.opacity = opacity;
    tag.textContent = skill;
    tag.title = `${skill}: ${count.toLocaleString()} mentions`;

    cloud.appendChild(tag);
  }
}

async function init() {
  try {
    await loadJobs();
    renderMetrics();
    renderTimeline();
    renderSourceBreakdown();
    renderEmploymentTypes();
    renderDemandChart();
    renderArrangements();
    renderExpDemand();
    renderSkillsCloud();
  } catch (e) {
    document.querySelector('.container').innerHTML += `<div class="panel"><div class="loading">Error loading analytics: ${e.message}</div></div>`;
  }
}

init();
