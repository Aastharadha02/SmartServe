import apiClient from './client';

export interface CustomerRegisterPayload {
  full_name: string;
  email: string;
  password: string;
  phone?: string;
  preferences?: string[];
}

export interface CustomerTokenResponse {
  access_token: string;
  customer_id: string;
  user_id: string;
  email: string;
  full_name: string;
  phone?: string;
  token_type?: string;
  role?: 'customer' | 'provider';
}

export interface ProviderLoginResponse {
  access_token: string;
  token_type: string;
  expires_in_minutes: number;
  user_id: string;
  email: string;
  role: string;
  role_name: string;
  permissions: string[];
}

export const authApi = {
  /** POST /customer/auth/login */
  login: async (
    email: string,
    password: string,
    totp_code?: string,
    recovery_code?: string
  ): Promise<CustomerTokenResponse> => {
    const res = await apiClient.post<CustomerTokenResponse>('/customer/auth/login', {
      email,
      password,
      ...(totp_code ? { totp_code } : {}),
      ...(recovery_code ? { recovery_code } : {}),
    });
    return { ...res.data, role: 'customer' };
  },

  /** POST /auth/login - Provider and System Login */
  providerLogin: async (
    email: string,
    password: string,
    totp_code?: string,
    recovery_code?: string
  ): Promise<CustomerTokenResponse> => {
    const res = await apiClient.post<ProviderLoginResponse>('/auth/login', {
      email,
      password,
      ...(totp_code ? { totp_code } : {}),
      ...(recovery_code ? { recovery_code } : {}),
    });
    return {
      access_token: res.data.access_token,
      customer_id: '',
      user_id: res.data.user_id,
      email: res.data.email,
      full_name: res.data.email.split('@')[0],
      role: 'provider',
    };
  },

  /** POST /customer/auth/register */
  register: async (payload: CustomerRegisterPayload): Promise<CustomerTokenResponse> => {
    const res = await apiClient.post<CustomerTokenResponse>('/customer/auth/register', payload);
    return { ...res.data, role: 'customer' };
  },

  /** GET /customer/auth/me */
  getMe: async (): Promise<CustomerTokenResponse> => {
    const res = await apiClient.get<CustomerTokenResponse>('/customer/auth/me');
    return { ...res.data, role: 'customer' };
  },

  /** POST /customer/auth/logout */
  logout: async (): Promise<void> => {
    try {
      await apiClient.post('/customer/auth/logout');
    } catch {
      // offline fallback
    }
  },
};
