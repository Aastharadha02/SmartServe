import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { setSecureItem, getSecureItem, removeSecureItem } from '../utils/secureStore';
import { authApi, CustomerTokenResponse } from '../api/auth';

export type UserRole = 'customer' | 'provider';

interface AuthContextType {
  user: CustomerTokenResponse | null;
  activeRole: UserRole;
  isLoading: boolean;
  login: (email: string, pass: string, role?: UserRole, totp_code?: string, recovery_code?: string) => Promise<void>;
  register: (fullName: string, email: string, pass: string, phone?: string) => Promise<void>;
  switchRole: (role: UserRole) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  activeRole: 'customer',
  isLoading: true,
  login: async () => {},
  register: async () => {},
  switchRole: async () => {},
  logout: async () => {},
});

const ROLE_STORAGE_KEY = 'smartserve_active_role';
const USER_STORAGE_KEY = 'smartserve_user';
const TOKEN_STORAGE_KEY = 'smartserve_token';

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<CustomerTokenResponse | null>(null);
  const [activeRole, setActiveRole] = useState<UserRole>('customer');
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    loadStoredAuth();
  }, []);

  const loadStoredAuth = async () => {
    try {
      const stored = await AsyncStorage.getItem(USER_STORAGE_KEY);
      const token = await getSecureItem(TOKEN_STORAGE_KEY);
      const savedRole = await AsyncStorage.getItem(ROLE_STORAGE_KEY);

      if (stored && token) {
        const parsed = JSON.parse(stored);
        setUser(parsed);
        if (savedRole === 'customer' || savedRole === 'provider') {
          setActiveRole(savedRole);
        } else if (parsed.role) {
          setActiveRole(parsed.role);
        }
      } else {
        setUser(null);
      }
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (
    email: string,
    pass: string,
    role: UserRole = 'customer',
    totp_code?: string,
    recovery_code?: string
  ) => {
    let data: CustomerTokenResponse;
    if (role === 'provider') {
      data = await authApi.providerLogin(email, pass, totp_code, recovery_code);
    } else {
      data = await authApi.login(email, pass, totp_code, recovery_code);
    }

    await setSecureItem(TOKEN_STORAGE_KEY, data.access_token);
    await AsyncStorage.setItem(USER_STORAGE_KEY, JSON.stringify(data));
    await AsyncStorage.setItem(ROLE_STORAGE_KEY, role);

    setUser(data);
    setActiveRole(role);
  };

  const register = async (fullName: string, email: string, pass: string, phone?: string) => {
    const data = await authApi.register({ full_name: fullName, email, password: pass, phone });
    await setSecureItem(TOKEN_STORAGE_KEY, data.access_token);
    await AsyncStorage.setItem(USER_STORAGE_KEY, JSON.stringify(data));
    await AsyncStorage.setItem(ROLE_STORAGE_KEY, 'customer');

    setUser(data);
    setActiveRole('customer');
  };

  const switchRole = async (targetRole: UserRole) => {
    setActiveRole(targetRole);
    await AsyncStorage.setItem(ROLE_STORAGE_KEY, targetRole);
  };

  const logout = async () => {
    try {
      await authApi.logout();
      await removeSecureItem(TOKEN_STORAGE_KEY);
      await AsyncStorage.removeItem(USER_STORAGE_KEY);
      await AsyncStorage.removeItem(ROLE_STORAGE_KEY);
    } finally {
      setUser(null);
      setActiveRole('customer');
    }
  };

  return (
    <AuthContext.Provider value={{ user, activeRole, isLoading, login, register, switchRole, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
