import { test, expect } from '@playwright/test';
import { setupAuthenticatedState } from './test-helpers';

test.describe('02 - App Shell & Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuthenticatedState(page);
    await page.goto('/home');
  });

  test('Sidebar navigation links route properly without replaying splash', async ({ page }) => {
    await page.click('a[href="/explore"]');
    await expect(page).toHaveURL('/explore');

    await page.click('a[href="/bookings"]');
    await expect(page).toHaveURL('/bookings');

    await page.click('a[href="/support"]');
    await expect(page).toHaveURL('/support');

    await page.click('a[href="/profile"]');
    await expect(page).toHaveURL('/profile');
  });

  test('Top header profile dropdown toggles and allows logout', async ({ page }) => {
    await page.click('button:has-text("Pushkar Kanjani")');
    await expect(page.getByText('Account Settings')).toBeVisible();

    await page.click('button:has-text("Sign Out")');
    await expect(page).toHaveURL('/login');
  });
});
