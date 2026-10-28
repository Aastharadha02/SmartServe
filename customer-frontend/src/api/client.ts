import axios from 'axios';

export function getApiBaseUrl(): string {
  // 1. First use VITE_API_BASE_URL when configured
  const configuredUrl = import.meta.env.VITE_API_BASE_URL;
  if (configuredUrl && typeof configuredUrl === 'string' && configuredUrl.trim() !== '') {
    return configuredUrl.trim().replace(/\/$/, '');
  }

  // 2. Only if VITE_API_BASE_URL is not configured, use local-development fallback
  if (typeof window !== 'undefined' && window.location && window.location.hostname) {
    const host = window.location.hostname;
    if (host !== 'localhost' && host !== '127.0.0.1') {
      return `http://${host}:8000/api/v1`;
    }
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

// Response interceptor: handle 401 unauthenticated
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
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
