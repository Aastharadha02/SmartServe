import apiClient from './client';

export interface LoginResponse {
  access_token: string;
  token_type: string;
  expires_in_minutes: number;
  user_id: string;
  email: string;
  role: string;
  role_name?: string;
  permissions?: string[];
}

export interface UserSession {
  user_id: string;
  email: string;
  role: string;
  role_name?: string;
  permissions?: string[];
  is_active: boolean;
}

export const authApi = {
  login: async (email: string, password: string): Promise<LoginResponse> => {
    const res = await apiClient.post<LoginResponse>('/auth/login', {
      email,
      password,
    });
    return res.data;
  },

  getCurrentSession: async (): Promise<UserSession> => {
    const res = await apiClient.get<UserSession>('/auth/me');
    return res.data;
  },
};
