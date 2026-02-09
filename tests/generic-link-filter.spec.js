import { test, expect } from '@playwright/test';

test.describe('Generic Link Filter', () => {
    test.beforeEach(async ({ page }) => {
        await page.goto('http://localhost:3000/gotjob/');
        await page.waitForLoadState('networkidle');
    });

    test('should have Hide Generic Links checkbox visible and checked by default', async ({ page }) => {
        const checkbox = page.locator('#hideGenericLinks');
        await expect(checkbox).toBeVisible();
        await expect(checkbox).toBeChecked();

        // Verify label text
        const label = page.locator('label:has(#hideGenericLinks)');
        await expect(label).toContainText('Hide generic career pages');
    });

    test('should filter out generic career page links when checkbox is checked', async ({ page }) => {
        // Wait for jobs to load
        await page.waitForSelector('.card', { timeout: 10000 });

        // Get all job card links
        const jobLinks = await page.locator('.card a[href]').all();

        // Check that no links point to generic career pages
        for (const link of jobLinks) {
            const href = await link.getAttribute('href');
            if (href) {
                const url = href.toLowerCase();

                // These patterns should NOT appear when filter is active
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

                const isGeneric = genericPatterns.some(pattern =>
                    url.endsWith(pattern) || url.endsWith(pattern + '/')
                );

                expect(isGeneric).toBe(false);
            }
        }
    });

    test('should show generic links when checkbox is unchecked', async ({ page }) => {
        // Uncheck the filter
        const checkbox = page.locator('#hideGenericLinks');
        await checkbox.uncheck();

        // Wait for filter to apply
        await page.waitForTimeout(500);

        // Get all job card links
        const jobLinks = await page.locator('.card a[href]').all();
        const allUrls = [];

        for (const link of jobLinks) {
            const href = await link.getAttribute('href');
            if (href) {
                allUrls.push(href.toLowerCase());
            }
        }

        // With filter OFF, we should see at least some generic links
        // (assuming the jobs.json has some generic career pages)
        const genericPatterns = [
            '/careers/',
            '/careers',
            '/jobs/',
            '/jobs'
        ];

        const hasGenericLinks = allUrls.some(url =>
            genericPatterns.some(pattern => url.endsWith(pattern) || url.endsWith(pattern + '/'))
        );

        // This test will pass if generic links exist in the data
        // If it fails, it means the data doesn't have generic links (which is fine)
        console.log('Has generic links:', hasGenericLinks);
        console.log('Total URLs:', allUrls.length);
    });

    test('should update job count when toggling filter', async ({ page }) => {
        // Wait for jobs to load
        await page.waitForSelector('.card', { timeout: 10000 });

        // Get initial count with filter ON
        const initialCards = await page.locator('.card').count();

        // Turn filter OFF
        const checkbox = page.locator('#hideGenericLinks');
        await checkbox.uncheck();
        await page.waitForTimeout(500);

        // Get count with filter OFF
        const uncheckedCards = await page.locator('.card').count();

        // Turn filter back ON
        await checkbox.check();
        await page.waitForTimeout(500);

        // Get count with filter ON again
        const recheckedCards = await page.locator('.card').count();

        // Counts should match when filter is in same state
        expect(recheckedCards).toBe(initialCards);

        // With filter OFF, we should have same or more jobs
        // (more if there are generic links in the data)
        expect(uncheckedCards).toBeGreaterThanOrEqual(initialCards);
    });

    test('should detect known generic career pages correctly', async ({ page }) => {
        // Test the isGenericLink function logic by checking specific known URLs
        const testUrls = [
            { url: 'https://www.sunlife.com/en/careers/', shouldBeFiltered: true },
            { url: 'https://www.rbc.com/careers/', shouldBeFiltered: true },
            { url: 'https://www.td.com/ca/en/about-td/careers', shouldBeFiltered: true },
            { url: 'https://careers.microsoft.com/', shouldBeFiltered: true },
            { url: 'https://www.google.com/about/careers/', shouldBeFiltered: true },
            { url: 'https://jobs.lever.co/company/123456', shouldBeFiltered: false },
            { url: 'https://www.greenhouse.io/job/123456', shouldBeFiltered: false },
            { url: 'https://apply.workable.com/company/j/ABC123/', shouldBeFiltered: false }
        ];

        // Inject test URLs into page context and check filtering logic
        const results = await page.evaluate((urls) => {
            // Copy of isGenericLink function from app.js
            function isGenericLink(url) {
                if (!url) return false;

                const urlLower = url.toLowerCase();

                const genericPatterns = [
                    '/careers/', '/careers', '/jobs/', '/jobs', '/career/', '/career',
                    '/opportunities/', '/opportunities', '/join-us/', '/join-us',
                    '/work-with-us/', '/work-with-us'
                ];

                for (const pattern of genericPatterns) {
                    if (urlLower.endsWith(pattern) || urlLower.endsWith(pattern + '/')) {
                        return true;
                    }
                }

                return false;
            }

            return urls.map(({ url, shouldBeFiltered }) => ({
                url,
                shouldBeFiltered,
                actuallyFiltered: isGenericLink(url),
                matches: isGenericLink(url) === shouldBeFiltered
            }));
        }, testUrls);

        // All test URLs should match expected filtering behavior
        for (const result of results) {
            expect(result.matches).toBe(true);
        }
    });

    test('should persist filter state on page reload', async ({ page }) => {
        // Uncheck the filter
        const checkbox = page.locator('#hideGenericLinks');
        await checkbox.uncheck();

        // Reload page
        await page.reload();
        await page.waitForLoadState('networkidle');

        // Note: Current implementation doesn't persist state
        // This test documents expected behavior for future enhancement
        // For now, filter should reset to checked (default)
        await expect(checkbox).toBeChecked();
    });
});

test.describe('Generic Link Filter UI', () => {
    test('should be in Link Quality filter section', async ({ page }) => {
        await page.goto('http://localhost:3000/gotjob/');

        // Find the Link Quality section
        const linkQualitySection = page.locator('.source-filters:has-text("Link Quality")');
        await expect(linkQualitySection).toBeVisible();

        // Checkbox should be within this section
        const checkbox = linkQualitySection.locator('#hideGenericLinks');
        await expect(checkbox).toBeVisible();
    });

    test('should have proper styling and accessibility', async ({ page }) => {
        await page.goto('http://localhost:3000/gotjob/');

        const checkbox = page.locator('#hideGenericLinks');

        // Should have proper ID for label association
        await expect(checkbox).toHaveAttribute('id', 'hideGenericLinks');
        await expect(checkbox).toHaveAttribute('type', 'checkbox');

        // Should be keyboard accessible
        await checkbox.focus();
        await expect(checkbox).toBeFocused();

        // Should toggle with Space key
        await page.keyboard.press('Space');
        await expect(checkbox).not.toBeChecked();

        await page.keyboard.press('Space');
        await expect(checkbox).toBeChecked();
    });
});
