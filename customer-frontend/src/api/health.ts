import axios from 'axios';
import { apiClient } from './client';

export interface HealthCheckResult {
  isOnline: boolean;
  statusText: string;
  statusCode?: number;
  environment?: string;
  apiReachable: boolean;
}

export const checkBackendHealth = async (): Promise<HealthCheckResult> => {
  const backendBase = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';
  
  let systemOnline = false;
  let statusCode: number | undefined;
  let statusText = 'Offline';
  let apiReachable = false;
  let environment = 'dev';

  // 1. Check Root Health Endpoint: GET http://localhost:8000/health
  try {
    const rootRes = await axios.get(`${backendBase}/health`, { timeout: 3000 });
    if (rootRes.status === 200) {
      systemOnline = true;
      statusCode = 200;
      statusText = 'Online';
      environment = rootRes.data?.environment || 'dev';
    }
  } catch (err: any) {
    if (err.response) {
      statusCode = err.response.status;
      if (err.response.status === 401 || err.response.status === 403) {
        systemOnline = true;
        statusText = 'Reachable (Auth Required)';
      } else if (err.response.status === 404) {
        systemOnline = true;
        statusText = 'Server Online (Route 404)';
      } else if (err.response.status >= 500) {
        systemOnline = true;
        statusText = `Server Error (${err.response.status})`;
      }
    } else {
      statusText = 'Offline (Connection Failed)';
    }
  }

  // 2. Check Customer API Endpoint: GET /customer/catalog/categories
  try {
    const apiRes = await apiClient.get('/customer/catalog/categories', { timeout: 3000 });
    if (apiRes.status === 200) {
      apiReachable = true;
      if (!systemOnline) {
        systemOnline = true;
        statusText = 'Online';
      }
    }
  } catch (err: any) {
    if (err.response && (err.response.status === 200 || err.response.status === 401 || err.response.status === 403)) {
      apiReachable = true;
    }
  }

  return {
    isOnline: systemOnline,
    statusText,
    statusCode,
    environment,
    apiReachable
  };
};
