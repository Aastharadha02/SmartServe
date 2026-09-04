import { test, expect } from '@playwright/test';

test.describe('08 - Design System & Token Assertions', () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      sessionStorage.setItem('smartserve_splash_seen', 'true');
    });
  });

  test('Page background color matches #F8FAFC token', async ({ page }) => {
    await page.goto('/login');
    const bodyBg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    expect(bodyBg).toBe('rgb(248, 250, 252)');
  });

  test('Primary buttons use #2563EB primary blue token', async ({ page }) => {
    await page.goto('/login');
    const button = page.getByRole('button', { name: 'Sign In' });
    const buttonBg = await button.evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(buttonBg).toBe('rgb(37, 99, 235)'); // #2563EB
  });
});
