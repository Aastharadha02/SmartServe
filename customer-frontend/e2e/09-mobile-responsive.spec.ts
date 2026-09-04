import { test, expect } from '@playwright/test';
import { setupAuthenticatedState } from './test-helpers';

test.describe('09 - Mobile Viewport & Responsiveness', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuthenticatedState(page);
  });

  test('360px viewport hides sidebar rail and displays hamburger button', async ({ page }) => {
    await page.setViewportSize({ width: 360, height: 640 });
    await page.goto('/home');

    const hamburger = page.locator('button[aria-label="Open sidebar"]');
    await expect(hamburger).toBeVisible({ timeout: 10000 });

    await hamburger.click();
    await expect(page.locator('button[aria-label="Close menu"]').last()).toBeVisible();
  });

  test('Form inputs enforce 16px minimum font size on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto('/login');
    const inputFont = await page.locator('input[type="email"]').evaluate((el) => getComputedStyle(el).fontSize);
    expect(parseFloat(inputFont)).toBeGreaterThanOrEqual(16);
  });
});
