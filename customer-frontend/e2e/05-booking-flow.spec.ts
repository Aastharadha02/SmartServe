import { test, expect } from '@playwright/test';
import { setupAuthenticatedState } from './test-helpers';

test.describe('05 - Booking Flow & Life Cycle', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuthenticatedState(page);
  });

  test('Complete booking submission creates new booking reference', async ({ page }) => {
    await page.goto('/book/srv-ac-101');
    await expect(page.getByRole('heading', { name: 'Create Booking' })).toBeVisible();

    await page.getByPlaceholder('Enter house no, floor, building name, street, locality, landmark...').fill('Flat 402, Green Valley Heights, Sector 62, Noida');

    await page.click('button:has-text("Confirm Booking")');

    await expect(page.getByText('Booking Confirmed!')).toBeVisible();
    await expect(page.getByText('Booking Reference:')).toBeVisible();
  });

  test('Bookings list displays status tabs and opens detail view', async ({ page }) => {
    await page.goto('/bookings');
    await expect(page.getByRole('heading', { name: 'My Bookings' })).toBeVisible();

    await page.click('a:has-text("View Details") >> nth=0');
    await expect(page.getByText('Assigned Service Provider')).toBeVisible();
    await expect(page.getByText('Service Lifecycle Timeline')).toBeVisible();
  });
});
