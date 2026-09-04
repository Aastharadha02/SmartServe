import { test, expect } from '@playwright/test';

test.describe('01 - Auth & Security Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
      sessionStorage.setItem('smartserve_splash_seen', 'true');
    });
  });

  test('Login form renders validation errors on invalid inputs', async ({ page }) => {
    await page.goto('/login');
    await expect(page.getByRole('heading', { name: 'Sign in to your account' })).toBeVisible();

    await page.getByRole('button', { name: 'Sign In' }).click();
    await expect(page.getByText('Please enter a valid email address.')).toBeVisible();
  });

  test('Successful login navigates to home dashboard', async ({ page }) => {
    await page.goto('/login');
    await page.locator('input[type="email"]').fill('pushkar@example.com');
    await page.locator('input[type="password"]').fill('Password123');
    await page.getByRole('button', { name: 'Sign In' }).click();

    await expect(page).toHaveURL('/home');
    await expect(page.getByText('Explore Service Categories')).toBeVisible();
  });

  test('Register form validates matching passwords', async ({ page }) => {
    await page.goto('/register');
    await page.locator('input[type="text"]').first().fill('New User');
    await page.locator('input[type="email"]').fill('new@example.com');
    await page.locator('input[type="password"]').first().fill('Password123');
    await page.locator('input[type="password"]').nth(1).fill('Mismatch123');
    await page.getByRole('button', { name: 'Create Account' }).click();

    await expect(page.getByText('Passwords do not match.')).toBeVisible();
  });

  test('Forgot password triggers confirmation message', async ({ page }) => {
    await page.goto('/forgot-password');
    await page.locator('input[type="email"]').fill('pushkar@example.com');
    await page.getByRole('button', { name: 'Send Reset Instructions' }).click();

    await expect(page.getByText('Reset instructions sent!')).toBeVisible();
  });
});
