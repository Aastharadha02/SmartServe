import { apiClient } from './client';

export interface SecuritySummary {
  failed_logins: number;
  suspicious_activities: number;
  active_sessions: number;
  is_totp_enabled: boolean;
  total_audit_events: number;
  critical_events: number;
}

export interface AuditLogItem {
  id: string;
  actor_email: string;
  actor_role: string;
  action: string;
  target_resource?: string | null;
  ip_address?: string | null;
  risk_level: string;
  metadata_json?: Record<string, any> | null;
  created_at: string;
}

export interface FailedLoginItem {
  id: string;
  email: string;
  ip_address?: string | null;
  attempt_count: number;
  last_attempt: string;
  locked_until?: string | null;
}

export interface SuspiciousActivityItem {
  id: string;
  user_id?: string | null;
  anomaly_type: string;
  risk_score: number;
  details_json?: {
    detection_reason?: string;
    ip_address?: string;
    geo_location?: string;
    ai_signal?: string;
  } | null;
  created_at: string;
}

export interface ActiveSessionItem {
  id: string;
  user_id: string;
  token_jti: string;
  ip_address?: string | null;
  user_agent?: string | null;
  is_revoked: boolean;
  created_at: string;
  expires_at: string;
}

export const getSecuritySummary = async (): Promise<SecuritySummary> => {
  const response = await apiClient.get<SecuritySummary>('/admin/security/summary');
  return response.data;
};

export const getAuditLogs = async (params?: {
  search?: string;
  risk_level?: string;
  skip?: number;
  limit?: number;
}): Promise<AuditLogItem[]> => {
  const query = new URLSearchParams();
  if (params?.search) query.append('search', params.search);
  if (params?.risk_level) query.append('risk_level', params.risk_level);
  if (params?.skip !== undefined) query.append('skip', String(params.skip));
  if (params?.limit !== undefined) query.append('limit', String(params.limit));

  const response = await apiClient.get<AuditLogItem[]>(`/admin/security/audit-logs?${query.toString()}`);
  return response.data;
};

export const getFailedLoginAttempts = async (): Promise<FailedLoginItem[]> => {
  const response = await apiClient.get<FailedLoginItem[]>('/admin/security/failed-logins');
  return response.data;
};

export const getSuspiciousActivities = async (): Promise<SuspiciousActivityItem[]> => {
  const response = await apiClient.get<SuspiciousActivityItem[]>('/admin/security/suspicious-activities');
  return response.data;
};

export const setupAdmin2FA = async (): Promise<{ secret: string; provisioning_uri: string }> => {
  const response = await apiClient.post<{ secret: string; provisioning_uri: string }>('/admin/security/2fa/setup');
  return response.data;
};

export const verifyAdmin2FA = async (code: string): Promise<{ status: string; message: string }> => {
  const response = await apiClient.post<{ status: string; message: string }>('/admin/security/2fa/verify', { code });
  return response.data;
};

export const getActiveSessions = async (): Promise<ActiveSessionItem[]> => {
  const response = await apiClient.get<ActiveSessionItem[]>('/admin/security/active-sessions');
  return response.data;
};

export const revokeActiveSession = async (sessionId: string): Promise<{ status: string; session_id: string; message: string }> => {
  const response = await apiClient.post(`/admin/security/revoke-session/${sessionId}`);
  return response.data;
};
