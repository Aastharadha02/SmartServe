import { apiClient } from './client';

export interface CustomerRegisterPayload {
  full_name: string;
  email: string;
  phone?: string;
  password: string;
  preferences?: string[];
}

export interface CustomerLoginPayload {
  email: string;
  password: string;
}

export interface CustomerTokenResponse {
  access_token: string;
  token_type: string;
  expires_in_minutes: number;
  customer_id: string;
  user_id: string;
  email: string;
  full_name: string;
  phone?: string;
}

export interface CustomerSessionResponse {
  customer_id: string;
  user_id: string;
  email: string;
  full_name: string;
  phone?: string;
  is_active: boolean;
  preferences?: string[];
}

export const registerCustomer = async (payload: CustomerRegisterPayload): Promise<CustomerTokenResponse> => {
  const res = await apiClient.post<CustomerTokenResponse>('/customer/auth/register', payload);
  return res.data;
};

export const loginCustomer = async (payload: CustomerLoginPayload): Promise<CustomerTokenResponse> => {
  const res = await apiClient.post<CustomerTokenResponse>('/customer/auth/login', payload);
  return res.data;
};

export const getCurrentCustomer = async (): Promise<CustomerSessionResponse> => {
  const res = await apiClient.get<CustomerSessionResponse>('/customer/auth/me');
  return res.data;
};

export const logoutCustomer = async (): Promise<void> => {
  try {
    await apiClient.post('/customer/auth/logout');
  } catch {
    // best-effort logout
  }
};

export const forgotPassword = async (email: string): Promise<{ status: string }> => {
  try {
    const res = await apiClient.post<{ status: string }>('/customer/auth/forgot-password', { email });
    return res.data;
  } catch {
    return { status: 'ok' };
  }
};

export const resetPassword = async (token: string, new_password: string): Promise<{ status: string }> => {
  const res = await apiClient.post<{ status: string }>('/customer/auth/reset-password', { token, new_password });
  return res.data;
};
