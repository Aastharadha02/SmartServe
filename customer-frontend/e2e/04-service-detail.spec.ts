import { test, expect } from '@playwright/test';
import { setupAuthenticatedState } from './test-helpers';

test.describe('04 - Service Detail & Price Calculation', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuthenticatedState(page);
  });

  test('Selecting add-ons recalculates running price in sticky bar', async ({ page }) => {
    await page.goto('/services/srv-ac-101');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible({ timeout: 10000 });

    await expect(page.getByText('₹699').first()).toBeVisible();

    await page.click('button:has-text("Add-ons")');
    const checkbox = page.locator('input[type="checkbox"]').first();
    await checkbox.check();

    await expect(page.getByText('₹898').first()).toBeVisible();
  });

  test('FAQ accordion opens and closes', async ({ page }) => {
    await page.goto('/services/srv-ac-101');
    await expect(page.getByRole('heading', { level: 1 })).toBeVisible({ timeout: 10000 });

    await page.click('button:has-text("FAQs")');
    await page.click('text=How long does foam jet service take?');
    await expect(page.getByText('Foam jet service typically requires 45 to 60 minutes per AC unit.')).toBeVisible();
  });
});
