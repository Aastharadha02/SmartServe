import { test, expect } from '@playwright/test';
import { setupAuthenticatedState } from './test-helpers';

test.describe('06 - Support & Customer Helpdesk', () => {
  test.beforeEach(async ({ page }) => {
    await setupAuthenticatedState(page);
  });

  test('Creating support ticket redirects to conversation thread', async ({ page }) => {
    await page.goto('/support/new');
    await expect(page.getByRole('heading', { name: 'Create New Support Ticket' })).toBeVisible();

    await page.click('button:has-text("Booking issue")');
    await page.getByPlaceholder('Brief summary of the issue').fill('Technician delay inquiry');
    await page.getByPlaceholder('Please describe what happened').fill('Technician is running 20 minutes behind the scheduled afternoon slot.');

    await page.click('button:has-text("Submit Ticket")');

    await expect(page.getByText('Conversation Thread')).toBeVisible();
    await expect(page.getByText('Technician delay inquiry')).toBeVisible();
  });
});
