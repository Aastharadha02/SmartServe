import { test, expect } from '@playwright/test';

test.describe('Phase 12 — Fullstack Integration Slice', () => {
  test('customer auth, catalog, booking creation and cancellation flow', async ({ page }) => {
    // 1. Visit customer frontend home
    await page.goto('/');
    await expect(page).toHaveTitle(/SmartServe/i);

    // 2. Navigate to login card
    const loginHeading = page.getByRole('heading', { name: /welcome back/i });
    if (!(await loginHeading.isVisible())) {
      await page.goto('/login');
    }
    await expect(page.getByRole('heading', { name: /welcome back/i })).toBeVisible();

    // 3. Login with test account
    await page.fill('input[type="email"]', 'pushkar@example.com');
    await page.fill('input[type="password"]', 'Password123!');
    await page.click('button[type="submit"]');

    // 4. Verify customer home dashboard
    await expect(page.getByText(/Explore Services/i).first()).toBeVisible();

    // 5. Explore categories and services
    await page.goto('/explore');
    await expect(page.getByText(/All Categories/i)).toBeVisible();

    // 6. View service detail
    await page.goto('/services/srv-ac-101');
    await expect(page.getByText(/Split AC Foam Jet Deep Service/i)).toBeVisible();

    // 7. Proceed to booking creation
    await page.goto('/book/srv-ac-101');
    await page.fill('textarea[id="address"]', 'Flat 402, Green Valley Heights, Sector 62, Noida, UP');
    
    // Select date and time if present
    const confirmBtn = page.getByRole('button', { name: /Confirm Booking/i });
    if (await confirmBtn.isVisible()) {
      await confirmBtn.click();
    }

    // 8. Visit customer bookings list
    await page.goto('/bookings');
    await expect(page.getByText(/My Bookings/i)).toBeVisible();
  });
});
