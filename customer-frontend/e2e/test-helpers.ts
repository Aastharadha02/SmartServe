import { Page } from '@playwright/test';

export const setupAuthenticatedState = async (page: Page) => {
  await page.addInitScript(() => {
    sessionStorage.setItem('smartserve_splash_seen', 'true');
    localStorage.setItem('smartserve_customer_token', 'mock-jwt-token-12345');
    localStorage.setItem(
      'smartserve_customer_user',
      JSON.stringify({
        id: 'cust-mock-uuid-1001',
        email: 'pushkar@example.com',
        full_name: 'Pushkar Kanjani',
        phone: '+91 9876543210',
        is_active: true,
        is_verified: true,
      })
    );
  });
};
