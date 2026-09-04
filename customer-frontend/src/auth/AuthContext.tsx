import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { CustomerLoginPayload, CustomerSessionResponse, loginCustomer, getCurrentCustomer, logoutCustomer } from '../api/auth';

interface AuthContextType {
  user: CustomerSessionResponse | null;
  token: string | null;
  loading: boolean;
  login: (credentials: CustomerLoginPayload) => Promise<void>;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<CustomerSessionResponse | null>(null);
  const [token, setToken] = useState<string | null>(localStorage.getItem('smartserve_customer_token'));
  const [loading, setLoading] = useState<boolean>(true);

  const fetchSession = async () => {
    const existingToken = localStorage.getItem('smartserve_customer_token');
    if (!existingToken) {
      setUser(null);
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
    };
    setUser(userObj);
    localStorage.setItem('smartserve_customer_user', JSON.stringify(userObj));
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
    <AuthContext.Provider value={{ user, token, loading, login, logout, refreshUser }}>
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
