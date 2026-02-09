import { test, expect } from '@playwright/test';

test.describe('JavaScript Error Detection - All Pages', () => {
    const pages = [
        { name: 'GotJob Main', url: 'http://localhost:3000/gotjob/' },
        { name: 'Salary Insights', url: 'http://localhost:3000/gotjob/salary-insights/' },
        { name: 'Career Resources', url: 'http://localhost:3000/gotjob/career-resources/' },
        { name: 'Tracker', url: 'http://localhost:3000/gotjob/tracker/' },
        { name: 'Market Report', url: 'http://localhost:3000/gotjob/market-report/' },
        { name: 'AI Match Lab', url: 'http://localhost:3000/gotjob/ai-match-lab/' },
        { name: 'Experience Hub', url: 'http://localhost:3000/gotjob/experience-hub/' },
        { name: 'Mobile Studio', url: 'http://localhost:3000/gotjob/mobile-studio/' },
        { name: 'Companies', url: 'http://localhost:3000/gotjob/companies/' },
        { name: 'Salaries', url: 'http://localhost:3000/gotjob/salaries/' },
        { name: 'Analytics', url: 'http://localhost:3000/gotjob/analytics/' },
        { name: 'Trends', url: 'http://localhost:3000/gotjob/trends/' }
    ];

    for (const pageInfo of pages) {
        test(`${pageInfo.name} - should load without JavaScript errors`, async ({ page }) => {
            const errors = [];
            const consoleMessages = [];

            // Capture console errors
            page.on('console', msg => {
                if (msg.type() === 'error') {
                    consoleMessages.push({
                        type: 'error',
                        text: msg.text(),
                        location: msg.location()
                    });
                }
            });

            // Capture page errors
            page.on('pageerror', error => {
                errors.push({
                    message: error.message,
                    stack: error.stack
                });
            });

            // Navigate to page
            const response = await page.goto(pageInfo.url, {
                waitUntil: 'networkidle',
                timeout: 30000
            });

            // Check HTTP status
            const status = response?.status();
            console.log(`\n📄 ${pageInfo.name}: HTTP ${status}`);

            // Wait a bit for any async errors
            await page.waitForTimeout(2000);

            // Report errors
            if (errors.length > 0) {
                console.log(`\n❌ ${pageInfo.name} - Page Errors:`);
                errors.forEach((err, idx) => {
                    console.log(`\n${idx + 1}. ${err.message}`);
                    if (err.stack) {
                        console.log(`   Stack: ${err.stack.substring(0, 200)}...`);
                    }
                });
            }

            if (consoleMessages.length > 0) {
                console.log(`\n⚠️  ${pageInfo.name} - Console Errors:`);
                consoleMessages.forEach((msg, idx) => {
                    console.log(`\n${idx + 1}. ${msg.text}`);
                    if (msg.location) {
                        console.log(`   Location: ${msg.location.url}:${msg.location.lineNumber}`);
                    }
                });
            }

            if (errors.length === 0 && consoleMessages.length === 0) {
                console.log(`✅ ${pageInfo.name} - No errors detected`);
            }

            // Assertions
            expect(status).toBeLessThan(400);
            expect(errors.length).toBe(0);
            expect(consoleMessages.length).toBe(0);
        });
    }

    test('All pages - Network request failures', async ({ page }) => {
        const failedRequests = [];

        page.on('requestfailed', request => {
            failedRequests.push({
                url: request.url(),
                failure: request.failure()?.errorText
            });
        });

        for (const pageInfo of pages) {
            failedRequests.length = 0; // Reset for each page

            await page.goto(pageInfo.url, {
                waitUntil: 'networkidle',
                timeout: 30000
            });

            await page.waitForTimeout(1000);

            if (failedRequests.length > 0) {
                console.log(`\n🚨 ${pageInfo.name} - Failed Requests:`);
                failedRequests.forEach(req => {
                    console.log(`  - ${req.url}`);
                    console.log(`    Error: ${req.failure}`);
                });
            }
        }
    });

    test('GotJob Main - Specific error checks', async ({ page }) => {
        const errors = [];

        page.on('pageerror', error => {
            errors.push(error.message);
        });

        await page.goto('http://localhost:3000/gotjob/');
        await page.waitForLoadState('networkidle');

        // Try to trigger the clear filters error
        const clearButton = page.locator('#clearFilters');
        if (await clearButton.count() > 0) {
            await clearButton.click();
            await page.waitForTimeout(500);
        }

        // Try to trigger filter changes
        const hideGenericCheckbox = page.locator('#hideGenericLinks');
        if (await hideGenericCheckbox.count() > 0) {
            await hideGenericCheckbox.uncheck();
            await page.waitForTimeout(500);
            await hideGenericCheckbox.check();
            await page.waitForTimeout(500);
        }

        if (errors.length > 0) {
            console.log('\n❌ Errors during interaction:');
            errors.forEach(err => console.log(`  - ${err}`));
        }

        expect(errors.length).toBe(0);
    });
});
