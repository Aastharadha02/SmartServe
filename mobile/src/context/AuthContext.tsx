import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { authApi, LoginResponse } from '../api/auth';

interface AuthContextType {
  user: LoginResponse | null;
  isLoading: boolean;
  login: (email: string, pass: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  isLoading: true,
  login: async () => {},
  logout: async () => {},
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<LoginResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    loadStoredAuth();
  }, []);

  const loadStoredAuth = async () => {
    try {
      const stored = await AsyncStorage.getItem('smartserve_user');
      if (stored) {
        setUser(JSON.parse(stored));
      }
    } catch (err) {
      console.warn('Failed to load session', err);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, pass: string) => {
    const data = await authApi.login(email, pass);
    await AsyncStorage.setItem('smartserve_token', data.access_token);
    await AsyncStorage.setItem('smartserve_user', JSON.stringify(data));
    setUser(data);
  };

  const logout = async () => {
    try {
      await AsyncStorage.removeItem('smartserve_token');
      await AsyncStorage.removeItem('smartserve_user');
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
