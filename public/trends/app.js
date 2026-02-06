let allJobs = [];

async function loadJobs() {
  try {
    const res = await fetch('../findjobs/jobs.json?t=' + Date.now());
    if (!res.ok) throw new Error('Failed to load jobs');
    const data = await res.json();
    allJobs = Array.isArray(data.jobs) ? data.jobs : (Array.isArray(data) ? data : []);
    analyzeTrends();
  } catch (e) {
    console.error('Error loading jobs:', e);
  }
}

function analyzeTrends() {
  updateOverviewStats();
  renderSkills();
  renderVolume();
  renderHiringCompanies();
  renderRoles();
  renderWorkArrangements();
  renderSeasonalInfo();
}

function updateOverviewStats() {
  const now = new Date();
  const today = allJobs.filter(j => {
    const d = new Date(j.postedDate || j.scrapedAt);
    return (now - d) < 24 * 60 * 60 * 1000;
  }).length;
  
  const thisWeek = allJobs.filter(j => {
    const d = new Date(j.postedDate || j.scrapedAt);
    return (now - d) < 7 * 24 * 60 * 60 * 1000;
  }).length;
  
  // Find top role
  const roleCounts = {};
  allJobs.forEach(j => {
    const role = categorizeRole(j.title);
    roleCounts[role] = (roleCounts[role] || 0) + 1;
  });
  const topRole = Object.entries(roleCounts)
    .sort((a, b) => b[1] - a[1])[0]?.[0] || '-';
  
  // Remote percentage
  const remoteCount = allJobs.filter(j => {
    const text = (j.title + ' ' + j.location + ' ' + (j.excerpt || '')).toLowerCase();
    return text.includes('remote') && !text.includes('hybrid');
  }).length;
  const remotePct = allJobs.length > 0 ? Math.round((remoteCount / allJobs.length) * 100) : 0;
  
  document.getElementById('jobsToday').textContent = today;
  document.getElementById('jobsThisWeek').textContent = thisWeek;
  document.getElementById('topRole').textContent = topRole;
  document.getElementById('remotePct').textContent = remotePct + '%';
}

function categorizeRole(title) {
  const t = title.toLowerCase();
  if (t.includes('manager') || t.includes('director')) return 'Manager';
  if (t.includes('senior') || t.includes('sr.')) return 'Senior';
  if (t.includes('full stack') || t.includes('full-stack')) return 'Full Stack';
  if (t.includes('frontend') || t.includes('front-end')) return 'Frontend';
  if (t.includes('backend') || t.includes('back-end')) return 'Backend';
  if (t.includes('devops') || t.includes('sre')) return 'DevOps';
  if (t.includes('data')) return 'Data';
  if (t.includes('mobile') || t.includes('ios') || t.includes('android')) return 'Mobile';
  return 'Engineer';
}

function renderSkills() {
  const container = document.getElementById('skillsContainer');
  
  const skills = {
    'React': /\breact\b/i,
    'TypeScript': /\btypescript\b|\bts\b/i,
    'Python': /\bpython\b/i,
    'Node.js': /\bnode\.?js\b/i,
    'AWS': /\baws\b|\bamazon web\b/i,
    'Docker': /\bdocker\b/i,
    'Kubernetes': /\bkubernetes\b|\bk8s\b/i,
    'SQL': /\bsql\b|\bpostgres\b|\bmysql\b/i,
    'AI/ML': /\bai\b|\bmachine learning\b|\bml\b/i,
    'Go': /\bgo\b|\bgolang\b/i,
    'Java': /\bjava\b/,
    'C#': /\bc#\b|\bdotnet\b|\b\.net\b/i,
    'GraphQL': /\bgraphql\b/i,
    'Rust': /\brust\b/i
  };
  
  const skillCounts = {};
  Object.entries(skills).forEach(([name, regex]) => {
    skillCounts[name] = allJobs.filter(j => 
      regex.test(j.title + ' ' + (j.excerpt || ''))
    ).length;
  });
  
  const sorted = Object.entries(skillCounts)
    .sort((a, b) => b[1] - a[1])
    .filter(s => s[1] >= 3);
  
  const max = Math.max(...sorted.map(s => s[1]));
  
  let html = '<div class="skills-grid">';
  sorted.forEach(([name, count]) => {
    const pct = (count / max) * 100;
    const trend = count > 10 ? 'hot' : count > 5 ? 'warm' : 'cool';
    
    html += `
      <div class="skill-item ${trend}">
        <div class="skill-info">
          <span class="skill-name">${name}</span>
          <span class="skill-count">${count} jobs</span>
        </div>
        <div class="skill-bar">
          <div class="skill-fill" style="width: ${pct}%"></div>
        </div>
      </div>
    `;
  });
  html += '</div>';
  
  container.innerHTML = html;
}

function renderVolume() {
  const days = 30;
  const dayData = [];
  
  for (let i = days - 1; i >= 0; i--) {
    const date = new Date();
    date.setDate(date.getDate() - i);
    const startOfDay = new Date(date.setHours(0, 0, 0, 0));
    const endOfDay = new Date(date.setHours(23, 59, 59, 999));
    
    const count = allJobs.filter(j => {
      const d = new Date(j.postedDate || j.scrapedAt);
      return d >= startOfDay && d <= endOfDay;
    }).length;
    
    dayData.push({ date: startOfDay, count });
  }
  
  const max = Math.max(...dayData.map(d => d.count)) || 1;
  
  // Calculate trend
  const recent = dayData.slice(-7).reduce((a, b) => a + b.count, 0) / 7;
  const previous = dayData.slice(-14, -7).reduce((a, b) => a + b.count, 0) / 7;
  const trend = recent > previous * 1.1 ? '📈 Increasing' : 
                recent < previous * 0.9 ? '📉 Decreasing' : '➡️ Stable';
  
  document.getElementById('volumeTrend').textContent = trend;
  
  let html = '';
  dayData.forEach(d => {
    const height = (d.count / max) * 100;
    const label = d.date.toLocaleDateString('en-CA', { month: 'short', day: 'numeric' });
    
    html += `
      <div class="vol-bar" title="${label}: ${d.count} jobs">
        <div class="vol-fill" style="height: ${height}%"></div>
      </div>
    `;
  });
  
  document.getElementById('volumeBars').innerHTML = html;
}

function renderHiringCompanies() {
  const container = document.getElementById('hiringList');
  const companyCounts = {};
  
  allJobs.forEach(j => {
    if (j.company) {
      companyCounts[j.company] = (companyCounts[j.company] || 0) + 1;
    }
  });
  
  const sorted = Object.entries(companyCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);
  
  let html = '';
  sorted.forEach(([name, count], i) => {
    html += `
      <div class="hiring-item">
        <span class="hiring-rank">#${i + 1}</span>
        <span class="hiring-name">${name}</span>
        <span class="hiring-count">${count} jobs</span>
      </div>
    `;
  });
  
  container.innerHTML = html;
}

function renderRoles() {
  const container = document.getElementById('rolesList');
  const roleCounts = {};
  
  allJobs.forEach(j => {
    const role = categorizeRole(j.title);
    roleCounts[role] = (roleCounts[role] || 0) + 1;
  });
  
  const sorted = Object.entries(roleCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8);
  
  const max = Math.max(...sorted.map(r => r[1]));
  
  let html = '';
  sorted.forEach(([role, count]) => {
    const pct = (count / max) * 100;
    html += `
      <div class="role-item">
        <span class="role-name">${role}</span>
        <div class="role-bar">
          <div class="role-fill" style="width: ${pct}%"></div>
        </div>
        <span class="role-count">${count}</span>
      </div>
    `;
  });
  
  container.innerHTML = html;
}

function renderWorkArrangements() {
  const total = allJobs.length;
  if (total === 0) return;
  
  let remote = 0, hybrid = 0, onsite = 0;
  
  allJobs.forEach(j => {
    const text = (j.title + ' ' + j.location + ' ' + (j.excerpt || '')).toLowerCase();
    
    if (text.includes('remote')) {
      if (text.includes('hybrid') || text.includes('flexible')) {
        hybrid++;
      } else {
        remote++;
      }
    } else if (text.includes('hybrid')) {
      hybrid++;
    } else if (text.includes('onsite') || text.includes('on-site') || text.includes('in-office')) {
      onsite++;
    } else {
      hybrid++; // Default assumption
    }
  });
  
  document.getElementById('remotePercent').textContent = Math.round((remote / total) * 100) + '%';
  document.getElementById('hybridPercent').textContent = Math.round((hybrid / total) * 100) + '%';
  document.getElementById('onsitePercent').textContent = Math.round((onsite / total) * 100) + '%';
}

function renderSeasonalInfo() {
  const month = new Date().getMonth();
  const descriptions = {
    0: 'January is peak hiring season. Companies have fresh budgets and are eager to fill roles.',
    1: 'February continues strong hiring. Good time to apply as competition is high but so are openings.',
    2: 'March is solid for job searching. Q1 hiring is in full swing.',
    3: 'April sees continued activity. Spring hiring season is active.',
    4: 'May is a good month to job search before summer slowdown.',
    5: 'June starts the summer slowdown. Fewer new postings but also less competition.',
    6: 'July is the slowest month. Use this time to prepare for fall hiring.',
    7: 'August is still slow but picks up toward the end. Start preparing applications.',
    8: 'September is the second peak hiring season. Back-to-work mentality drives postings.',
    9: 'October is excellent for job searching. Q4 push to fill roles before year-end.',
    10: 'November sees continued activity. Companies rush to fill positions.',
    11: 'December slows down significantly. Focus on networking for January.'
  };
  
  const tips = {
    0: ['Apply aggressively', 'Update your resume', 'Reach out to recruiters'],
    1: ['Follow up on applications', 'Prepare for technical interviews', 'Research target companies'],
    2: ['Attend networking events', 'Polish your portfolio', 'Practice coding problems'],
    3: ['Focus on quality applications', 'Schedule informational interviews', 'Update LinkedIn'],
    4: ['Apply before summer slowdown', 'Negotiate offers received', 'Plan for fall hiring'],
    5: ['Use time to upskill', 'Work on side projects', 'Prepare for September'],
    6: ['Take online courses', 'Contribute to open source', 'Rest and recharge'],
    7: ['Update all materials', 'Start applying for September', 'Reconnect with network'],
    8: ['Apply widely', 'Attend career fairs', 'Refresh your approach'],
    9: ['Be responsive to recruiters', 'Prepare for quick hiring processes', 'Have references ready'],
    10: ['Push for decisions', 'Consider contract roles', 'Stay flexible on start dates'],
    11: ['Network for January', 'Set job search goals for new year', 'Enjoy the holidays']
  };
  
  const icons = ['❄️', '❄️', '🌸', '🌸', '🌸', '☀️', '☀️', '☀️', '🍂', '🍂', '🍂', '🎄'];
  
  document.getElementById('seasonDesc').textContent = descriptions[month];
  document.querySelector('.season-icon').textContent = icons[month];
  
  const tipsList = document.getElementById('tipsList');
  tipsList.innerHTML = tips[month].map(t => `<li>${t}</li>`).join('');
}

loadJobs();