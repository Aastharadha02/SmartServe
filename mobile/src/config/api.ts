import { Platform } from 'react-native';

/**
 * SmartServe Mobile API Configuration
 * 
 * Android Emulator uses 10.0.2.2 to access host machine's 127.0.0.1
 * Real devices / LAN testing use configurable EXPO_PUBLIC_API_URL or host IP
 */
export const getApiBaseUrl = (): string => {
  // 1. Check custom environment variable
  if (process.env.EXPO_PUBLIC_API_URL) {
    return process.env.EXPO_PUBLIC_API_URL;
  }

  // 2. Default to production Render API URL
  return 'https://smartserve-backend-tr3p.onrender.com/api/v1';
};

export const API_BASE_URL = getApiBaseUrl();
