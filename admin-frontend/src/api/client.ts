import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1';



export const apiClient = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});


// Interceptor to automatically attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('smartserve_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Interceptor to handle 401 Unauthorized & 403 Forbidden responses
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      const status = error.response.status;
      const detail = String(error.response.data?.detail || '').toLowerCase();
      if (
        status === 401 ||
        (status === 403 && (detail.includes('admin role') || detail.includes('forbidden') || detail.includes('unauthorized')))
      ) {
        localStorage.removeItem('smartserve_token');
        localStorage.removeItem('smartserve_user');
        if (window.location.pathname !== '/login' && window.location.pathname !== '/admin/login') {
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

