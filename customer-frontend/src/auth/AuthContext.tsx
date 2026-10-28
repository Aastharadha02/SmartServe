import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { CustomerLoginPayload, CustomerSessionResponse, CustomerTokenResponse, CustomerLocationPayload, loginCustomer, getCurrentCustomer, logoutCustomer } from '../api/auth';

interface AuthContextType {
  user: CustomerSessionResponse | null;
  token: string | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (credentials: CustomerLoginPayload) => Promise<void>;
  setSessionFromTokenResponse: (data: CustomerTokenResponse) => void;
  setUserLocation: (loc: CustomerLocationPayload) => void;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<CustomerSessionResponse | null>(() => {
    try {
      const saved = localStorage.getItem('smartserve_customer_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [token, setToken] = useState<string | null>(localStorage.getItem('smartserve_customer_token'));
  const [loading, setLoading] = useState<boolean>(!localStorage.getItem('smartserve_customer_user'));

  const fetchSession = async () => {
    const existingToken = localStorage.getItem('smartserve_customer_token');
    if (!existingToken) {
      // Keep cached user if guest or clean if expired
      setLoading(false);
      return;
    }

    try {
      const data = await getCurrentCustomer();
      setUser(data);
      localStorage.setItem('smartserve_customer_user', JSON.stringify(data));
    } catch {
      localStorage.removeItem('smartserve_customer_token');
      localStorage.removeItem('smartserve_customer_user');
      setUser(null);
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSession();
  }, []);

  const login = async (credentials: CustomerLoginPayload) => {
    const data = await loginCustomer(credentials);
    localStorage.setItem('smartserve_customer_token', data.access_token);
    setToken(data.access_token);

    const userObj: CustomerSessionResponse = {
      customer_id: data.customer_id,
      user_id: data.user_id,
      email: data.email,
      full_name: data.full_name,
      phone: data.phone,
      is_active: true,
      is_profile_complete: data.is_profile_complete !== false,
      missing_profile_fields: data.missing_profile_fields || [],
      location: data.location,
    };
    setUser(userObj);
    localStorage.setItem('smartserve_customer_user', JSON.stringify(userObj));
  };

  const setSessionFromTokenResponse = (data: CustomerTokenResponse) => {
    localStorage.setItem('smartserve_customer_token', data.access_token);
    setToken(data.access_token);

    const userObj: CustomerSessionResponse = {
      customer_id: data.customer_id,
      user_id: data.user_id,
      email: data.email,
      full_name: data.full_name,
      phone: data.phone,
      is_active: true,
      is_profile_complete: data.is_profile_complete !== false,
      missing_profile_fields: data.missing_profile_fields || [],
      location: data.location,
    };
    setUser(userObj);
    localStorage.setItem('smartserve_customer_user', JSON.stringify(userObj));
  };

  const setUserLocation = (loc: CustomerLocationPayload) => {
    setUser((prev) => {
      if (!prev) return null;
      const updated = { ...prev, location: loc };
      localStorage.setItem('smartserve_customer_user', JSON.stringify(updated));
      return updated;
    });
  };

  const logout = async () => {
    await logoutCustomer();
    localStorage.removeItem('smartserve_customer_token');
    localStorage.removeItem('smartserve_customer_user');
    setUser(null);
    setToken(null);
  };

  const refreshUser = async () => {
    await fetchSession();
  };

  return (
    <AuthContext.Provider value={{ user, token, isAuthenticated: !!user, loading, login, setSessionFromTokenResponse, setUserLocation, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
