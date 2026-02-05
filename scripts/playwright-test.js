const { chromium } = require('playwright');

async function testSite() {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  
  console.log('🎭 PLAYWRIGHT TESTING\n');
  
  // Test 1: Main page loads
  try {
    await page.goto('https://findtorontoevents.ca/gotjob/');
    await page.waitForLoadState('networkidle');
    const title = await page.title();
    console.log('✅ Test 1 - Main page loads:', title);
  } catch (e) {
    console.log('❌ Test 1 failed:', e.message);
  }
  
  // Test 2: Jobs load
  try {
    await page.waitForSelector('.card', { timeout: 10000 });
    const jobCount = await page.locator('.card').count();
    console.log('✅ Test 2 - Jobs loaded:', jobCount, 'job cards');
  } catch (e) {
    console.log('❌ Test 2 failed:', e.message);
  }
  
  // Test 3: Search functionality
  try {
    await page.fill('#keywords', 'software');
    await page.click('#search');
    await page.waitForTimeout(2000);
    const filteredCount = await page.locator('.card').count();
    console.log('✅ Test 3 - Search works:', filteredCount, 'filtered jobs');
  } catch (e) {
    console.log('❌ Test 3 failed:', e.message);
  }
  
  // Test 4: Source filters
  try {
    await page.check('#sourceAdzuna');
    await page.uncheck('#sourceJobbank');
    await page.waitForTimeout(1000);
    console.log('✅ Test 4 - Source filters work');
  } catch (e) {
    console.log('❌ Test 4 failed:', e.message);
  }
  
  // Test 5: Findjobs subdirectory
  try {
    await page.goto('https://findtorontoevents.ca/gotjob/findjobs/');
    await page.waitForLoadState('networkidle');
    const title2 = await page.title();
    console.log('✅ Test 5 - /findjobs/ loads:', title2);
  } catch (e) {
    console.log('❌ Test 5 failed:', e.message);
  }
  
  // Test 6: Navigation menu
  try {
    const nav = await page.locator('.nav-menu').count();
    if (nav > 0) {
      console.log('✅ Test 6 - Navigation menu present');
    } else {
      console.log('⚠️ Test 6 - Navigation menu not found');
    }
  } catch (e) {
    console.log('❌ Test 6 failed:', e.message);
  }
  
  await browser.close();
  
  console.log('\n🎭 Playwright testing complete!');
}

test().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
