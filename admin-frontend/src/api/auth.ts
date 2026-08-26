import { apiClient } from './client';

export interface LoginPayload {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in_minutes: number;
  user_id: string;
  email: string;
  role: string;
  permissions: string[];
}

export interface SessionResponse {
  user_id: string;
  email: string;
  role: string;
  is_active: boolean;
}

export const loginAdmin = async (credentials: LoginPayload): Promise<TokenResponse> => {
  const response = await apiClient.post<TokenResponse>('/auth/login', credentials);
  return response.data;
};

export const getAdminSession = async (): Promise<SessionResponse> => {
  const response = await apiClient.get<SessionResponse>('/auth/me');
  return response.data;
};
