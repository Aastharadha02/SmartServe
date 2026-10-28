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
  totp_code?: string;
  recovery_code?: string;
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
  requires_profile_completion?: boolean;
  is_profile_complete?: boolean;
  missing_profile_fields?: string[];
  is_new_user?: boolean;
  location?: CustomerLocationPayload;
}

export interface CustomerLocationPayload {
  address?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  latitude?: number;
  longitude?: number;
  source?: string;
}

export interface CompleteProfilePayload {
  full_name: string;
  phone: string;
  preferences?: string[];
  location?: CustomerLocationPayload;
}

export interface SkipProfilePayload {
  full_name?: string;
  phone?: string;
  preferences?: string[];
  location?: CustomerLocationPayload;
}

export interface CustomerSessionResponse {
  customer_id: string;
  user_id: string;
  email: string;
  full_name: string;
  phone?: string;
  is_active: boolean;
  preferences?: string[];
  is_profile_complete?: boolean;
  missing_profile_fields?: string[];
  location?: CustomerLocationPayload;
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

export const completeCustomerProfile = async (payload: CompleteProfilePayload): Promise<CustomerTokenResponse> => {
  const res = await apiClient.post<CustomerTokenResponse>('/customer/auth/complete-profile', payload);
  return res.data;
};

export const skipCustomerProfile = async (payload: SkipProfilePayload): Promise<CustomerTokenResponse> => {
  const res = await apiClient.post<CustomerTokenResponse>('/customer/auth/skip-profile', payload);
  return res.data;
};

export const updateCustomerLocation = async (payload: CustomerLocationPayload): Promise<{ status: string; location: CustomerLocationPayload }> => {
  const res = await apiClient.post<{ status: string; location: CustomerLocationPayload }>('/customer/profile/location', payload);
  return res.data;
};

export interface OAuthProvidersResponse {
  google: { configured: boolean; name: string };
  apple: { configured: boolean; name: string };
  github: { configured: boolean; name: string };
}

export interface OAuthAuthorizeResponse {
  provider: string;
  authorization_url: string;
  state: string;
}

export const getOAuthProviders = async (): Promise<OAuthProvidersResponse> => {
  const res = await apiClient.get<OAuthProvidersResponse>('/customer/auth/oauth/providers');
  return res.data;
};

export const initiateOAuth = async (provider: 'google' | 'apple' | 'github', redirect_uri?: string): Promise<OAuthAuthorizeResponse> => {
  const res = await apiClient.get<OAuthAuthorizeResponse>(`/customer/auth/oauth/${provider}/authorize`, {
    params: redirect_uri ? { redirect_uri } : undefined
  });
  return res.data;
};

export const submitOAuthCallback = async (
  provider: string,
  code: string,
  state: string,
  redirect_uri?: string
): Promise<CustomerTokenResponse> => {
  const res = await apiClient.post<CustomerTokenResponse>(`/customer/auth/oauth/${provider}/callback`, {
    code,
    state,
    redirect_uri,
  });
  return res.data;
};
