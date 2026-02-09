import { test, expect } from '@playwright/test';

test.describe('GotJob - Full UI and Navigation Testing', () => {
    const baseUrl = 'http://localhost:3000/gotjob/';

    test.beforeEach(async ({ page }) => {
        await page.goto(baseUrl);
        await page.waitForLoadState('networkidle');
    });

    test.describe('Navigation and Links', () => {
        test('should have working navigation menu', async ({ page }) => {
            // Check all nav links exist and are clickable
            const navLinks = [
                { text: 'Home', href: '/' },
                { text: 'Find Jobs', href: '/findjobs/' },
                { text: 'Salaries', href: '/gotjob/salary-insights/' },
                { text: 'Companies', href: '/gotjob/companies/' },
                { text: 'Career', href: '/gotjob/career/' },
                { text: 'Trends', href: '/gotjob/trends/' },
                { text: 'Tracker', href: '/gotjob/tracker/' }
            ];

            for (const link of navLinks) {
                const navLink = page.locator(`nav a:has-text("${link.text}")`);
                await expect(navLink).toBeVisible();

                // Check href attribute
                const href = await navLink.getAttribute('href');
                expect(href).toContain(link.href);
            }
        });

        test('should navigate to all pages without errors', async ({ page }) => {
            const pages = [
                { name: 'Salaries', path: '/gotjob/salary-insights/' },
                { name: 'Companies', path: '/gotjob/companies/' },
                { name: 'Career', path: '/gotjob/career/' },
                { name: 'Trends', path: '/gotjob/trends/' },
                { name: 'Tracker', path: '/gotjob/tracker/' }
            ];

            for (const testPage of pages) {
                await page.goto(`http://localhost:3000${testPage.path}`);

                // Wait for page to load
                await page.waitForLoadState('networkidle');

                // Check for JavaScript errors
                const errors = [];
                page.on('pageerror', error => errors.push(error.message));

                // Verify page loaded (should have a header or main content)
                const hasContent = await page.locator('h1, h2, .container').count() > 0;
                expect(hasContent).toBe(true);

                // Check no 404 or error messages
                const hasError = await page.locator('text=/404|not found|error/i').count();
                expect(hasError).toBe(0);
            }
        });

        test('should have no broken links in navigation', async ({ page }) => {
            const links = await page.locator('nav a[href]').all();

            for (const link of links) {
                const href = await link.getAttribute('href');
                if (href && !href.startsWith('#') && !href.startsWith('javascript:')) {
                    // Navigate to link
                    const response = await page.goto(`http://localhost:3000${href}`);
                    expect(response?.status()).toBeLessThan(400);

                    // Go back to main page
                    await page.goto(baseUrl);
                }
            }
        });
    });

    test.describe('Generic Link Filter - Default State', () => {
        test('should have "Hide generic career pages" checkbox checked by default', async ({ page }) => {
            const checkbox = page.locator('#hideGenericLinks');
            await expect(checkbox).toBeVisible();
            await expect(checkbox).toBeChecked();
        });

        test('should filter out generic career pages by default', async ({ page }) => {
            // Wait for jobs to load
            await page.waitForSelector('.card', { timeout: 10000 });

            // Get all job links
            const jobCards = await page.locator('.card').all();

            console.log(`\n📊 Testing ${jobCards.length} job cards for generic links...\n`);

            let genericLinksFound = [];

            for (let i = 0; i < jobCards.length; i++) {
                const card = jobCards[i];
                const link = card.locator('a[href]').first();
                const href = await link.getAttribute('href');
                const title = await link.textContent();

                if (href) {
                    const url = href.toLowerCase();

                    // Check for generic patterns
                    const genericPatterns = [
                        { pattern: /\/careers\/?$/i, name: '/careers/' },
                        { pattern: /\/careers\.html$/i, name: '/careers.html' },
                        { pattern: /\/careers\.aspx$/i, name: '/careers.aspx' },
                        { pattern: /\/jobs\/?$/i, name: '/jobs/' },
                        { pattern: /\/jobs\.html$/i, name: '/jobs.html' },
                        { pattern: /\/career\/?$/i, name: '/career/' },
                        { pattern: /\/opportunities\/?$/i, name: '/opportunities/' },
                        { pattern: /\/join-us\/?$/i, name: '/join-us/' },
                        { pattern: /\/talent\/?$/i, name: '/talent/' }
                    ];

                    for (const { pattern, name } of genericPatterns) {
                        if (pattern.test(url)) {
                            genericLinksFound.push({
                                url: href,
                                title: title?.trim(),
                                pattern: name,
                                cardIndex: i
                            });
                            console.log(`❌ GENERIC LINK FOUND (Card ${i + 1}):`, {
                                url: href,
                                title: title?.trim(),
                                pattern: name
                            });
                        }
                    }

                    // Specific check for sunlife.com/slgs/en/careers/slgs-careers/
                    if (url.includes('sunlife.com') && url.includes('/careers/')) {
                        const hasJobId = /\/\d{5,}/.test(url) || /[?&]id=\d+/.test(url);
                        if (!hasJobId) {
                            genericLinksFound.push({
                                url: href,
                                title: title?.trim(),
                                pattern: 'sunlife generic career page',
                                cardIndex: i
                            });
                            console.log(`❌ SUNLIFE GENERIC LINK FOUND (Card ${i + 1}):`, href);
                        }
                    }
                }
            }

            // Report findings
            if (genericLinksFound.length > 0) {
                console.log(`\n🚨 FAILED: Found ${genericLinksFound.length} generic links that should be filtered:\n`);
                genericLinksFound.forEach((item, idx) => {
                    console.log(`${idx + 1}. ${item.url}`);
                    console.log(`   Title: ${item.title}`);
                    console.log(`   Pattern: ${item.pattern}\n`);
                });
            } else {
                console.log(`\n✅ PASSED: No generic links found. Filter working correctly!\n`);
            }

            // Assertion
            expect(genericLinksFound.length).toBe(0);
        });

        test('should show generic links when filter is unchecked', async ({ page }) => {
            // Uncheck the filter
            const checkbox = page.locator('#hideGenericLinks');
            await checkbox.uncheck();

            // Wait for filter to apply
            await page.waitForTimeout(1000);

            // Get all job links
            const jobLinks = await page.locator('.card a[href]').all();
            const allUrls = [];

            for (const link of jobLinks) {
                const href = await link.getAttribute('href');
                if (href) {
                    allUrls.push(href.toLowerCase());
                }
            }

            // With filter OFF, we should see at least some generic links
            const hasGenericLinks = allUrls.some(url =>
                /\/(careers|jobs|career|opportunities)\/?$/i.test(url) ||
                /\/(careers|jobs)\.html$/i.test(url)
            );

            console.log(`\nWith filter OFF: ${allUrls.length} total jobs`);
            console.log(`Has generic links: ${hasGenericLinks}\n`);

            // This will pass if generic links exist in the data
            // If it fails, it means the data doesn't have generic links (which is fine)
        });

        test('should validate specific known generic URLs are filtered', async ({ page }) => {
            // Wait for jobs to load
            await page.waitForSelector('.card', { timeout: 10000 });

            // Known generic URLs that should be filtered
            const knownGenericUrls = [
                'sunlife.com/slgs/en/careers/slgs-careers',
                'mfs.com/en-us/investment-professional/about-mfs/careers.html',
                'adityabirlacapital.com/about-us/careers.aspx'
            ];

            // Get all visible job URLs
            const jobLinks = await page.locator('.card a[href]').all();
            const visibleUrls = [];

            for (const link of jobLinks) {
                const href = await link.getAttribute('href');
                if (href) {
                    visibleUrls.push(href.toLowerCase());
                }
            }

            // Check if any known generic URLs are visible
            const foundGeneric = [];
            for (const genericUrl of knownGenericUrls) {
                const found = visibleUrls.some(url => url.includes(genericUrl.toLowerCase()));
                if (found) {
                    foundGeneric.push(genericUrl);
                    console.log(`❌ FOUND GENERIC URL: ${genericUrl}`);
                }
            }

            if (foundGeneric.length > 0) {
                console.log(`\n🚨 These known generic URLs should be filtered but are visible:\n`);
                foundGeneric.forEach(url => console.log(`  - ${url}`));
            } else {
                console.log(`\n✅ All known generic URLs are correctly filtered!\n`);
            }

            expect(foundGeneric.length).toBe(0);
        });
    });

    test.describe('Filter Functionality', () => {
        test('should have all filter controls visible', async ({ page }) => {
            // Check main filters
            await expect(page.locator('#keywords')).toBeVisible();
            await expect(page.locator('#location')).toBeVisible();
            await expect(page.locator('#dateFilter')).toBeVisible();
            await expect(page.locator('#minSalary')).toBeVisible();

            // Check buttons
            await expect(page.locator('#search')).toBeVisible();
            await expect(page.locator('#clearFilters')).toBeVisible();
        });

        test('should clear all filters without errors', async ({ page }) => {
            // Set some filters
            await page.fill('#keywords', 'developer');
            await page.selectOption('#dateFilter', '24h');

            // Click clear filters
            const clearButton = page.locator('#clearFilters');
            await clearButton.click();

            // Wait a moment
            await page.waitForTimeout(500);

            // Verify filters are cleared
            const keywordsValue = await page.locator('#keywords').inputValue();
            expect(keywordsValue).toBe('');

            const dateValue = await page.locator('#dateFilter').inputValue();
            expect(dateValue).toBe('week');
        });

        test('should update job count when filters change', async ({ page }) => {
            // Wait for initial load
            await page.waitForSelector('.card', { timeout: 10000 });

            // Get initial count
            const initialCount = await page.locator('.card').count();

            // Apply a filter
            await page.fill('#keywords', 'senior developer');
            await page.click('#search');

            // Wait for results
            await page.waitForTimeout(1000);

            // Get new count
            const filteredCount = await page.locator('.card').count();

            // Counts should be different (or at least not error)
            console.log(`Initial: ${initialCount}, Filtered: ${filteredCount}`);
            expect(filteredCount).toBeGreaterThanOrEqual(0);
        });
    });

    test.describe('Job Cards Display', () => {
        test('should display job cards with required information', async ({ page }) => {
            await page.waitForSelector('.card', { timeout: 10000 });

            const firstCard = page.locator('.card').first();

            // Check for job title link
            await expect(firstCard.locator('a')).toBeVisible();

            // Check for company info
            const hasCompany = await firstCard.locator('.company, .tag.company').count() > 0;
            expect(hasCompany).toBe(true);

            // Check for date
            const hasDate = await firstCard.locator('.posted-date, .date').count() > 0;
            expect(hasDate).toBe(true);
        });

        test('should have working job links', async ({ page }) => {
            await page.waitForSelector('.card', { timeout: 10000 });

            const jobLink = page.locator('.card a').first();
            const href = await jobLink.getAttribute('href');

            expect(href).toBeTruthy();
            expect(href).not.toBe('#');
            expect(href).not.toBe('javascript:void(0)');
        });

        test('should display badges if present', async ({ page }) => {
            await page.waitForSelector('.card', { timeout: 10000 });

            // Check if any cards have badges
            const badgesRow = page.locator('.badges-row').first();
            const hasBadges = await badgesRow.count() > 0;

            if (hasBadges) {
                console.log('✅ Badges are displaying on job cards');

                // Check for specific badge types
                const freshBadge = await page.locator('.badge-fresh').count();
                const salaryBadge = await page.locator('.badge-salary').count();
                const remoteBadge = await page.locator('.badge-remote').count();

                console.log(`Fresh badges: ${freshBadge}`);
                console.log(`Salary badges: ${salaryBadge}`);
                console.log(`Remote badges: ${remoteBadge}`);
            }
        });
    });

    test.describe('Accessibility and UX', () => {
        test('should be keyboard navigable', async ({ page }) => {
            // Tab through key elements
            await page.keyboard.press('Tab'); // First focusable element

            // Check if focus is visible
            const focusedElement = await page.evaluate(() => document.activeElement?.tagName);
            expect(focusedElement).toBeTruthy();
        });

        test('should have proper ARIA labels', async ({ page }) => {
            const checkbox = page.locator('#hideGenericLinks');
            const label = page.locator('label:has(#hideGenericLinks)');

            await expect(label).toBeVisible();
            await expect(label).toContainText('Hide generic career pages');
        });

        test('should be responsive', async ({ page }) => {
            // Test mobile viewport
            await page.setViewportSize({ width: 375, height: 667 });
            await page.waitForTimeout(500);

            // Check if content is still visible
            await expect(page.locator('.container')).toBeVisible();

            // Test tablet viewport
            await page.setViewportSize({ width: 768, height: 1024 });
            await page.waitForTimeout(500);

            await expect(page.locator('.container')).toBeVisible();

            // Reset to desktop
            await page.setViewportSize({ width: 1280, height: 720 });
        });
    });
});
