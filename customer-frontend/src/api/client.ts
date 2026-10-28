import axios from 'axios';

export function getApiBaseUrl(): string {
  // 1. First use VITE_API_BASE_URL when configured
  const configuredUrl = import.meta.env.VITE_API_BASE_URL;
  if (configuredUrl && typeof configuredUrl === 'string' && configuredUrl.trim() !== '') {
    return configuredUrl.trim().replace(/\/$/, '');
  }

  // 2. Production fallback
  if (import.meta.env.PROD || (typeof window !== 'undefined' && window.location && window.location.hostname.includes('vercel.app'))) {
    return 'https://smartserve-api-de3f.onrender.com/api/v1';
  }

  return 'http://127.0.0.1:8000/api/v1';
}

export const baseURL = getApiBaseUrl();

export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
});

// Request interceptor: attach bearer token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('smartserve_customer_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor: handle automatic retry on network/cold-start errors & 401 unauthenticated
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config as any;
    if (config && (!error.response || [502, 503, 504].includes(error.response?.status))) {
      config.__retryCount = config.__retryCount || 0;
      if (config.__retryCount < 3) {
        config.__retryCount += 1;
        const delay = Math.min(1000 * Math.pow(2, config.__retryCount - 1), 3000);
        await new Promise((resolve) => setTimeout(resolve, delay));
        return apiClient(config);
      }
    }

    if (error.response && error.response.status === 401) {
      localStorage.removeItem('smartserve_customer_token');
      localStorage.removeItem('smartserve_customer_user');
      // Only forcibly redirect to login if the user is attempting to access a strictly protected route
      const isProtectedRoute = ['/bookings', '/profile'].some((p) => window.location.pathname.startsWith(p));
      if (isProtectedRoute) {
        window.location.assign('/login');
      }
    }
    return Promise.reject(error);
  }
);

