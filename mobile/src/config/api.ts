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

  // 2. Default platform development mappings
  if (Platform.OS === 'android') {
    // 10.0.2.2 is standard Android emulator loopback to host PC
    return 'http://10.0.2.2:8000/api/v1';
  }

  return 'http://127.0.0.1:8000/api/v1';
};

export const API_BASE_URL = getApiBaseUrl();
