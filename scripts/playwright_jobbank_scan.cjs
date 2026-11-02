const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
  });
  const page = await context.newPage();

  const results = [];

  async function scan(keyword) {
    const url = `https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=${encodeURIComponent(keyword)}&locationstring=Toronto%2C+ON`;
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
      await page.waitForTimeout(4000);
      // Try common job result selectors
      const selectors = [
        'article', '.job', '.job-result', '[data-testid="job"]', '.result',
        'li.job', '.job-card', 'article.job', '.job-search-result'
      ];
      let found = 0;
      for (const sel of selectors) {
        try {
          const count = await page.locator(sel).count();
          if (count > 0) {
            const texts = await page.locator(sel).allInnerTexts();
            for (const t of texts.slice(0, 8)) {
              const tt = t.trim().replace(/\s+/g, ' ');
              if (tt.length > 10 && tt.length < 300) {
                results.push({ source: 'jobbank', keyword, title: tt, url: url });
                found++;
              }
            }
            console.log(`[JobBank] ${keyword}: selector "${sel}" -> ${count} elements, captured ${found}`);
            break;
          }
        } catch (e) {}
      }
      if (found === 0) {
        console.log(`[JobBank] ${keyword}: no job-card selectors matched`);
      }
    } catch (e) {
      console.log(`[JobBank] ${keyword}: FAILED ${e.message}`);
    }
  }

  await scan('ServiceNow');
  await page.waitForTimeout(2000);
  await scan('Salesforce');

  await browser.close();
  console.log('\n=== PLAYWRIGHT JOBBank RESULTS ===');
  console.log(JSON.stringify(results, null, 2));
  console.log('Total captured:', results.length);
})();
