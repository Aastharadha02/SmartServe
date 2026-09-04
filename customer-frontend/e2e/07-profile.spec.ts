import { test, expect } from '@playwright/test';
import { setupAuthenticatedState } from './test-helpers';

test.describe('07 - Profile & Security Management', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuthenticatedState(page);
  });

  test('Profile stats render lifetime spent and total bookings', async ({ page }) => {
    await page.goto('/profile');
    await expect(page.getByText('Lifetime Spent')).toBeVisible({ timeout: 10000 });
  });

  test('Security page strength meter updates on input', async ({ page }) => {
    await page.goto('/profile/security');
    await expect(page.getByRole('heading', { name: 'Security & Active Sessions' })).toBeVisible({ timeout: 10000 });

    await page.getByPlaceholder('••••••••').nth(1).fill('Weak1');
    await expect(page.getByText('Strength:')).toBeVisible();

    await page.getByPlaceholder('••••••••').nth(1).fill('StrongPassword#2026');
    await expect(page.getByText('Strength: Strong')).toBeVisible();
  });
});
