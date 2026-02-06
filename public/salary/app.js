let allJobs = [];
let salaryData = null;

function formatMoney(n) {
  if (!n || isNaN(n)) return '-';
  return new Intl.NumberFormat("en-CA", {
    style: "currency",
    currency: "CAD",
    maximumFractionDigits: 0
  }).format(n);
}

function formatMoneyK(n) {
  if (!n || isNaN(n)) return '-';
  return `$${Math.round(n / 1000)}K`;
}

async function loadJobs() {
  try {
    const res = await fetch('../findjobs/jobs.json?t=' + Date.now());
    if (!res.ok) throw new Error('Failed to load jobs');
    const data = await res.json();
    allJobs = Array.isArray(data.jobs) ? data.jobs : (Array.isArray(data) ? data : []);
    analyzeSalaries();
  } catch (e) {
    console.error('Error loading jobs:', e);
    document.getElementById('roleChart').innerHTML = '<div class="error">Failed to load salary data</div>';
  }
}

function analyzeSalaries() {
  // Filter jobs with salary data
  const jobsWithSalary = allJobs.filter(j => j.salary && (j.salary.min || j.salary.max));
  
  if (jobsWithSalary.length === 0) {
    document.getElementById('roleChart').innerHTML = '<div class="empty">No salary data available yet</div>';
    return;
  }

  // Extract salary values
  const salaries = jobsWithSalary.map(j => j.salary.max || j.salary.min || 0).filter(s => s > 0);
  
  // Update overview stats
  const avg = salaries.reduce((a, b) => a + b, 0) / salaries.length;
  const sorted = [...salaries].sort((a, b) => a - b);
  const median = sorted[Math.floor(sorted.length / 2)];
  const top10 = sorted[Math.floor(sorted.length * 0.9)];
  
  document.getElementById('avgSalary').textContent = formatMoneyK(avg);
  document.getElementById('medianSalary').textContent = formatMoneyK(median);
  document.getElementById('highSalary').textContent = formatMoneyK(top10);
  document.getElementById('salaryJobs').textContent = jobsWithSalary.length.toLocaleString();

  // Analyze by role
  const roleData = {};
  jobsWithSalary.forEach(job => {
    const role = categorizeRole(job.title);
    if (!roleData[role]) {
      roleData[role] = [];
    }
    roleData[role].push(job.salary.max || job.salary.min || 0);
  });

  // Calculate stats per role
  salaryData = {};
  Object.entries(roleData).forEach(([role, values]) => {
    if (values.length >= 3) { // Only include roles with enough data
      const sorted = values.sort((a, b) => a - b);
      salaryData[role] = {
        count: values.length,
        median: sorted[Math.floor(sorted.length / 2)],
        avg: values.reduce((a, b) => a + b, 0) / values.length,
        min: sorted[0],
        max: sorted[sorted.length - 1]
      };
    }
  });

  renderRoleChart();
  renderCompanyList(jobsWithSalary);
}

function categorizeRole(title) {
  const t = title.toLowerCase();
  if (t.includes('manager') || t.includes('director') || t.includes('head')) return 'Manager/Director';
  if (t.includes('senior') || t.includes('sr.') || t.includes('staff')) return 'Senior Engineer';
  if (t.includes('devops') || t.includes('sre') || t.includes('platform')) return 'DevOps/SRE';
  if (t.includes('full stack') || t.includes('full-stack')) return 'Full Stack';
  if (t.includes('frontend') || t.includes('front-end') || t.includes('ui')) return 'Frontend';
  if (t.includes('backend') || t.includes('back-end') || t.includes('api')) return 'Backend';
  if (t.includes('data') && t.includes('engineer')) return 'Data Engineer';
  if (t.includes('data') && (t.includes('scientist') || t.includes('science'))) return 'Data Scientist';
  if (t.includes('machine learning') || t.includes('ml ') || t.includes('ai ')) return 'ML/AI';
  if (t.includes('product') && t.includes('manager')) return 'Product Manager';
  if (t.includes('project') && t.includes('manager')) return 'Project Manager';
  if (t.includes('qa') || t.includes('test')) return 'QA/Testing';
  if (t.includes('mobile') || t.includes('ios') || t.includes('android')) return 'Mobile';
  if (t.includes('security') || t.includes('cyber')) return 'Security';
  if (t.includes('cloud') || t.includes('aws') || t.includes('azure')) return 'Cloud Engineer';
  if (t.includes('developer') || t.includes('engineer')) return 'Software Engineer';
  return 'Other';
}

function renderRoleChart() {
  const container = document.getElementById('roleChart');
  const roles = Object.entries(salaryData)
    .sort((a, b) => b[1].median - a[1].median)
    .slice(0, 10);

  if (roles.length === 0) {
    container.innerHTML = '<div class="empty">Not enough data to show role comparisons</div>';
    return;
  }

  const maxSalary = Math.max(...roles.map(r => r[1].max));
  
  let html = '<div class="role-chart">';
  roles.forEach(([role, data]) => {
    const medianPct = (data.median / maxSalary) * 100;
    const rangePct = ((data.max - data.min) / maxSalary) * 100;
    const leftPct = ((data.min / maxSalary) * 100);
    
    html += `
      <div class="role-bar">
        <div class="role-name">${role}</div>
        <div class="role-viz">
          <div class="salary-bar" style="left: ${leftPct}%; width: ${rangePct}%;"></div>
          <div class="salary-median" style="left: ${medianPct}%;"></div>
        </div>
        <div class="role-stats">
          <span class="median">${formatMoneyK(data.median)}</span>
          <span class="count">${data.count} jobs</span>
        </div>
      </div>
    `;
  });
  html += '</div>';
  
  html += `
    <div class="chart-legend">
      <span><span class="legend-bar"></span> Salary range</span>
      <span><span class="legend-median"></span> Median</span>
    </div>
  `;
  
  container.innerHTML = html;
}

function renderCompanyList(jobsWithSalary) {
  const container = document.getElementById('companyList');
  const companyData = {};
  
  jobsWithSalary.forEach(job => {
    if (!job.company) return;
    if (!companyData[job.company]) {
      companyData[job.company] = [];
    }
    companyData[job.company].push(job.salary.max || job.salary.min || 0);
  });

  const companies = Object.entries(companyData)
    .map(([name, salaries]) => ({
      name,
      median: salaries.sort((a, b) => a - b)[Math.floor(salaries.length / 2)],
      count: salaries.length,
      avg: salaries.reduce((a, b) => a + b, 0) / salaries.length
    }))
    .filter(c => c.count >= 2)
    .sort((a, b) => b.median - a.median)
    .slice(0, 15);

  if (companies.length === 0) {
    container.innerHTML = '<div class="empty">Not enough company data yet</div>';
    return;
  }

  let html = '<div class="company-grid">';
  companies.forEach(c => {
    html += `
      <div class="company-card">
        <div class="company-name">${c.name}</div>
        <div class="company-salary">${formatMoneyK(c.median)}</div>
        <div class="company-meta">${c.count} job${c.count > 1 ? 's' : ''}</div>
      </div>
    `;
  });
  html += '</div>';
  
  container.innerHTML = html;
}

function calculateSalary() {
  const role = document.getElementById('calcRole').value.toLowerCase().trim();
  const experience = document.getElementById('calcExperience').value;
  
  if (!role) {
    alert('Please enter a job title');
    return;
  }

  // Find matching jobs
  const matching = allJobs.filter(j => {
    const matchesRole = j.title.toLowerCase().includes(role) ||
                       (j.excerpt || '').toLowerCase().includes(role);
    const hasSalary = j.salary && (j.salary.min || j.salary.max);
    return matchesRole && hasSalary;
  });

  if (matching.length < 3) {
    document.getElementById('calcResult').innerHTML = `
      <div class="calc-error">
        <p>Not enough data for "${role}"</p>
        <p class="calc-hint">Try broader terms like "engineer", "developer", or "manager"</p>
      </div>
    `;
    document.getElementById('calcResult').style.display = 'block';
    return;
  }

  // Apply experience multiplier
  const multipliers = {
    entry: 0.75,
    mid: 1.0,
    senior: 1.3,
    lead: 1.6,
    manager: 1.8
  };
  const multiplier = multipliers[experience] || 1.0;

  const salaries = matching.map(j => (j.salary.max || j.salary.min) * multiplier).sort((a, b) => a - b);
  
  const p25 = salaries[Math.floor(salaries.length * 0.25)];
  const p50 = salaries[Math.floor(salaries.length * 0.5)];
  const p75 = salaries[Math.floor(salaries.length * 0.75)];

  document.getElementById('range25').textContent = formatMoney(p25);
  document.getElementById('range50').textContent = formatMoney(p50);
  document.getElementById('range75').textContent = formatMoney(p75);
  document.getElementById('calcSample').textContent = matching.length;
  
  document.getElementById('calcResult').style.display = 'block';
}

// Initialize
document.getElementById('calculateBtn')?.addEventListener('click', calculateSalary);
loadJobs();