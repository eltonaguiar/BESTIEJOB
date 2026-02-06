import { test, expect } from '@playwright/test';

const BASE_URL = 'https://findtorontoevents.ca';

// All navigation paths to test
const navigationPaths = [
    { path: '/gotjob/', name: 'GotJob Main' },
    { path: '/salary-insights/', name: 'Salary Insights' },
    { path: '/career-resources/', name: 'Career Resources' },
    { path: '/companies/', name: 'Companies' },
    { path: '/resume-builder/', name: 'Resume Builder' },
    { path: '/interview-prep/', name: 'Interview Prep' },
    { path: '/my-jobs/', name: 'My Jobs' },
    { path: '/ai-match-lab/', name: 'AI Match Lab' },
    { path: '/experience-hub/', name: 'Experience Hub' },
    { path: '/market-report/', name: 'Market Report' },
    { path: '/mobile-studio/', name: 'Mobile Studio' },
    { path: '/tracker/', name: 'Tracker' },
    { path: '/trends/', name: 'Trends' },
    { path: '/analytics/', name: 'Analytics' },
    { path: '/career/', name: 'Career' },
    { path: '/salaries/', name: 'Salaries' },
    { path: '/salary/', name: 'Salary' }
];

test.describe('BESTIEJOB Navigation Tests', () => {

    test('All navigation paths should load without 404 errors', async ({ page }) => {
        const results = [];

        for (const route of navigationPaths) {
            const url = `${BASE_URL}${route.path}`;
            console.log(`Testing: ${route.name} (${url})`);

            const response = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 10000 });
            const status = response?.status() || 0;

            results.push({
                name: route.name,
                path: route.path,
                status: status,
                ok: status === 200
            });

            // Check for 404 error page
            const pageTitle = await page.title();
            const bodyText = await page.textContent('body');

            expect(status, `${route.name} should return 200 status`).toBe(200);
            expect(pageTitle, `${route.name} should not show "Object not found"`).not.toContain('Object not found');
            expect(bodyText, `${route.name} should not show 404 error`).not.toContain('404');
        }

        // Log summary
        console.log('\n=== Test Summary ===');
        results.forEach(r => {
            console.log(`${r.ok ? '✅' : '❌'} ${r.name}: ${r.status}`);
        });
    });

    test('All pages should have proper CSS loaded', async ({ page }) => {
        const cssResults = [];

        for (const route of navigationPaths) {
            const url = `${BASE_URL}${route.path}`;
            await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });

            // Check if styles are applied by looking for computed styles
            const bodyBgColor = await page.evaluate(() => {
                return window.getComputedStyle(document.body).backgroundColor;
            });

            // Check for broken CSS links (404s)
            const failedResources = [];
            page.on('response', response => {
                if (response.url().endsWith('.css') && response.status() === 404) {
                    failedResources.push(response.url());
                }
            });

            await page.waitForTimeout(1000);

            cssResults.push({
                name: route.name,
                path: route.path,
                hasStyles: bodyBgColor !== 'rgba(0, 0, 0, 0)' && bodyBgColor !== 'rgb(255, 255, 255)',
                failedCss: failedResources
            });

            expect(failedResources.length, `${route.name} should not have failed CSS requests`).toBe(0);
        }

        // Log CSS summary
        console.log('\n=== CSS Test Summary ===');
        cssResults.forEach(r => {
            console.log(`${r.hasStyles ? '✅' : '⚠️'} ${r.name}: ${r.failedCss.length} failed CSS`);
        });
    });

    test('GotJob page should display job listings', async ({ page }) => {
        await page.goto(`${BASE_URL}/gotjob/`, { waitUntil: 'networkidle' });

        // Wait for job cards to load
        await page.waitForSelector('.card', { timeout: 10000 });

        const jobCards = await page.$$('.card');
        expect(jobCards.length, 'Should have at least one job card').toBeGreaterThan(0);

        // Check that posting dates are visible
        const firstCard = jobCards[0];
        const postedDate = await firstCard.$('.posted-date');
        expect(postedDate, 'Job card should have posting date').not.toBeNull();

        // Check that date is in viewport
        const isVisible = await postedDate?.isVisible();
        expect(isVisible, 'Posting date should be visible').toBe(true);
    });

    test('Salary Insights should have working charts', async ({ page }) => {
        await page.goto(`${BASE_URL}/salary-insights/`, { waitUntil: 'networkidle' });

        // Wait for Chart.js to load
        await page.waitForTimeout(2000);

        // Check for canvas elements (charts)
        const canvases = await page.$$('canvas');
        expect(canvases.length, 'Should have chart canvases').toBeGreaterThan(0);

        // Check that stats are populated
        const avgSalary = await page.textContent('#avgSalary');
        expect(avgSalary, 'Average salary should be displayed').not.toBe('$0');
    });

    test('Navigation links should work from GotJob page', async ({ page }) => {
        await page.goto(`${BASE_URL}/gotjob/`, { waitUntil: 'domcontentloaded' });

        // Get all navigation links
        const navLinks = await page.$$('nav a, header a');
        const linkTexts = await Promise.all(
            navLinks.map(link => link.textContent())
        );

        console.log(`Found ${navLinks.length} navigation links:`, linkTexts);

        // Click each link and verify it doesn't 404
        for (let i = 0; i < Math.min(navLinks.length, 10); i++) {
            const link = navLinks[i];
            const href = await link.getAttribute('href');

            if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
                const fullUrl = href.startsWith('http') ? href : `${BASE_URL}${href}`;
                console.log(`Testing link: ${href}`);

                const response = await page.goto(fullUrl, { waitUntil: 'domcontentloaded', timeout: 10000 });
                const status = response?.status() || 0;

                expect(status, `Link ${href} should not 404`).not.toBe(404);

                // Go back to gotjob page
                await page.goto(`${BASE_URL}/gotjob/`, { waitUntil: 'domcontentloaded' });
            }
        }
    });
});
