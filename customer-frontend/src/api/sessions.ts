import { apiClient } from './client';

export interface UserSession {
  id: string;
  device_name: string;
  browser: string;
  ip_address: string;
  last_active: string;
  is_current: boolean;
}

export const getActiveSessions = async (): Promise<UserSession[]> => {
  const res = await apiClient.get<UserSession[]>('/customer/sessions');
  return res.data;
};

export const revokeSession = async (sessionId: string): Promise<void> => {
  await apiClient.post(`/customer/sessions/${sessionId}/revoke`);
};

export const revokeAllOtherSessions = async (): Promise<void> => {
  await apiClient.post('/customer/sessions/revoke-all');
};
