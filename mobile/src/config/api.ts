/**
 * SmartServe Mobile API Configuration
 * 
 * Auto-detects runtime environment:
 * 1. Explicit EXPO_PUBLIC_API_BASE_URL from .env
 * 2. Metro Bundler host IP extracted from Expo Constants (works automatically on physical devices)
 * 3. Android Emulator (10.0.2.2:8000)
 * 4. iOS Simulator (127.0.0.1:8000)
 * 5. Fallback LAN IPv4 address (172.20.10.2:8000)
 */
import { Platform } from 'react-native';
import Constants from 'expo-constants';

export const DETECTED_PC_LAN_IP = '172.20.10.2';
export const DEFAULT_BACKEND_PORT = '8000';

function resolveApiBaseUrl(): string {
  // 1. Explicit environment override
  if (process.env.EXPO_PUBLIC_API_BASE_URL) {
    return process.env.EXPO_PUBLIC_API_BASE_URL.replace(/\/+$/, '');
  }
  if (process.env.EXPO_PUBLIC_API_URL) {
    return process.env.EXPO_PUBLIC_API_URL.replace(/\/+$/, '');
  }

  // 2. Extract host from Expo constants (e.g., "172.20.10.2:8081" or "192.168.1.5:8081")
  const hostUri = Constants.expoConfig?.hostUri || (Constants as any)?.manifest2?.extra?.expoClient?.hostUri;
  if (hostUri) {
    const hostIp = hostUri.split(':')[0];
    if (hostIp && hostIp !== 'localhost' && hostIp !== '127.0.0.1') {
      return `http://${hostIp}:${DEFAULT_BACKEND_PORT}/api/v1`;
    }
  }

  // 3. Android Emulator fallback
  if (Platform.OS === 'android' && !Constants.isDevice) {
    return `http://10.0.2.2:${DEFAULT_BACKEND_PORT}/api/v1`;
  }

  // 4. Default LAN IP
  return `http://${DETECTED_PC_LAN_IP}:${DEFAULT_BACKEND_PORT}/api/v1`;
}

export const API_BASE_URL = resolveApiBaseUrl();
export const DEV_API_BASE_URL = API_BASE_URL;
export const DEV_BACKEND_ROOT_URL = API_BASE_URL.replace(/\/api\/v1\/?$/, '');

/**
 * Normalizes relative media/upload paths (e.g. /static/uploads/...) into full URLs.
 */
export function getFullMediaUrl(path?: string | null): string {
  if (!path) return '';
  if (path.startsWith('http://') || path.startsWith('https://')) {
    return path;
  }
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${DEV_BACKEND_ROOT_URL}${cleanPath}`;
}
