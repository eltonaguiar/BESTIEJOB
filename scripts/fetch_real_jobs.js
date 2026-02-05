// Test script for scraping real jobs - expanded sources
import fs from 'fs';

// Greenhouse boards - verified working tokens
const GREENHOUSE_BOARDS = [
  { company: 'Klick', token: 'klick' },
  { company: 'Wave', token: 'wave' },
  { company: 'Wealthsimple', token: 'wealthsimple' }
];

// Try Workday boards
const WORKDAY_BOARDS = [
  { company: 'RBC', token: 'rbc' },
  { company: 'TD', token: 'td' }
];

// RSS Feeds that might work
const RSS_FEEDS = [
  { name: 'StackOverflow', url: 'https://stackoverflow.com/jobs/feed' }
];

async function fetchGreenhouseJobs() {
  const results = [];
  for (const b of GREENHOUSE_BOARDS) {
    try {
      // Try different endpoint formats
      const urls = [
        `https://boards-api.greenhouse.io/v1/boards/${b.token}/jobs`,
        `https://api.greenhouse.io/v1/boards/${b.token}/jobs`,
        `https://${b.token}.greenhouse.io/boards/${b.token}/jobs.json`
      ];
      
      for (const url of urls) {
        try {
          const res = await fetch(url, { 
            headers: { 'Accept': 'application/json' },
            signal: AbortSignal.timeout(10000)
          });
          if (!res.ok) continue;
          const data = await res.json();
          const jobs = Array.isArray(data?.jobs) ? data.jobs : [];
          console.log(`${b.company}: ${jobs.length} jobs from ${url}`);
          if (jobs.length > 0) {
            results.push(...jobs.map(j => ({
              id: `greenhouse:${b.token}:${j.id}`,
              source: 'greenhouse',
              company: b.company,
              title: j.title,
              location: j.location?.name || 'Toronto, ON',
              url: j.absolute_url || j.hosted_url || `https://boards.greenhouse.io/${b.token}/jobs/${j.id}`,
              employmentType: 'full-time',
              salary: null,
              postedDate: new Date().toISOString(),
              excerpt: j.title
            })));
            break;
          }
        } catch (e) {}
      }
    } catch (e) { console.log(`${b.company}: ERROR ${e.message}`); }
  }
  return results;
}

async function fetchWorkdayJobs() {
  const results = [];
  for (const b of WORKDAY_BOARDS) {
    try {
      const url = `https://${b.token}.wd101.myworkdayjobs.com/en-US/${b.token}/jobs`;
      const res = await fetch(url, { 
        headers: { 'Accept': 'application/json', 'user-agent': 'BESTIEJOB/0.1' },
        signal: AbortSignal.timeout(10000)
      });
      console.log(`${b.company}: HTTP ${res.status}`);
    } catch (e) { console.log(`${b.company}: ERROR ${e.message}`); }
  }
  return results;
}

async function fetchGithubJobs() {
  try {
    const res = await fetch('https://api.github.com/repos/awesome-jobs/jobs/issues');
    if (!res.ok) return [];
    const issues = await res.json();
    const jobs = issues.filter(i => i.title.toLowerCase().includes('toronto') || i.title.toLowerCase().includes('canada'));
    console.log(`GitHub Issues: ${jobs.length} jobs`);
    return jobs.map(j => ({
      id: `github:${j.number}`,
      source: 'github',
      company: 'Various',
      title: j.title,
      location: 'Toronto, ON',
      url: j.html_url,
      employmentType: 'full-time',
      salary: null,
      postedDate: j.created_at,
      excerpt: j.body?.substring(0, 240) || j.title
    }));
  } catch (e) {
    console.log(`GitHub: ERROR ${e.message}`);
    return [];
  }
}

async function main() {
  console.log('Fetching REAL jobs...\n');
  const greenhouseJobs = await fetchGreenhouseJobs();
  const workdayJobs = await fetchWorkdayJobs();
  const githubJobs = await fetchGithubJobs();
  const allJobs = [...greenhouseJobs, ...workdayJobs, ...githubJobs];
  console.log(`\nTOTAL REAL JOBS: ${allJobs.length}`);
  if (allJobs.length > 0) {
    fs.writeFileSync('jobs.json', JSON.stringify({
      meta: {
        scrapedAt: new Date().toISOString(),
        totalFetched: allJobs.length,
        sources: ['greenhouse', 'github']
      },
      jobs: allJobs
    }, null, 2));
    console.log('Saved to jobs.json');
  } else {
    console.log('No real jobs found. Will try web scraping approach...');
  }
}

main();
