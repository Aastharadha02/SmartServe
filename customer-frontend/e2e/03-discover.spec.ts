import { test, expect } from '@playwright/test';
import { setupAuthenticatedState } from './test-helpers';

test.describe('03 - Service Discovery & Catalog', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuthenticatedState(page);
  });

  test('Home page displays category grid and emergency banner', async ({ page }) => {
    await page.goto('/home');
    await expect(page.getByRole('heading', { name: 'Popular Categories' })).toBeVisible({ timeout: 10000 });
    await expect(page.getByText('AC & Appliance Repair').first()).toBeVisible();
    await expect(page.getByText('Emergency Services Available')).toBeVisible();
  });

  test('Explore page allows filtering and view mode toggle', async ({ page }) => {
    await page.goto('/explore');
    await expect(page.getByText('Service Catalog')).toBeVisible({ timeout: 10000 });

    await page.click('button[aria-label="List view"]');
    await expect(page.getByText('Split AC Foam Jet Deep Service').first()).toBeVisible();
  });

  test('Navigating from Category -> Subcategory -> Service List -> Detail works', async ({ page }) => {
    await page.goto('/explore');
    await page.click('text=AC & Appliance Repair');
    await expect(page).toHaveURL(/\/explore|\/categories/);

    await page.click('text=Split AC Foam Jet Deep Service');
    await expect(page).toHaveURL(/\/service\/srv-ac-101|\/services\/srv-ac-101/);
  });
});
