import { apiClient } from './client';

export interface AdminActivityItem {
  id: string;
  action: string;
  created_at: string;
}

export interface AdminItem {
  id: string;
  email: string;
  role: string;
  role_name: string;
  permissions: string[];
  is_active: boolean;
  is_2fa_enabled: boolean;
  created_at: string;
  recent_activity?: AdminActivityItem[];
}

export interface PermissionMatrixItem {
  module: string;
  actions: string[];
}

export const getAdminsList = async (params?: {
  search?: string;
  role_name?: string;
  is_active?: boolean;
  is_2fa_enabled?: boolean;
}): Promise<AdminItem[]> => {
  const query = new URLSearchParams();
  if (params?.search) query.append('search', params.search);
  if (params?.role_name) query.append('role_name', params.role_name);
  if (params?.is_active !== undefined) query.append('is_active', String(params.is_active));
  if (params?.is_2fa_enabled !== undefined) query.append('is_2fa_enabled', String(params.is_2fa_enabled));

  const response = await apiClient.get<AdminItem[]>(`/admin/admins/?${query.toString()}`);
  return response.data;
};

export const getAdminDetail = async (adminId: string): Promise<AdminItem> => {
  const response = await apiClient.get<AdminItem>(`/admin/admins/${adminId}`);
  return response.data;
};

export const createAdminAccount = async (data: {
  email: string;
  password: string;
  role_name: string;
  permissions?: string[];
}): Promise<{ status: string; user_id: string; email: string; role_name: string }> => {
  const response = await apiClient.post('/admin/admins/', data);
  return response.data;
};

export const updateAdminRole = async (
  adminId: string,
  roleName: string,
  permissions?: string[]
): Promise<{ status: string; role_name: string; permissions: string[]; message: string }> => {
  const response = await apiClient.post(`/admin/admins/${adminId}/role`, {
    role_name: roleName,
    permissions,
  });
  return response.data;
};

export const updateAdminAccountStatus = async (
  adminId: string,
  isActive: boolean,
  reason?: string
): Promise<{ status: string; is_active: boolean; message: string }> => {
  const response = await apiClient.post(`/admin/admins/${adminId}/status`, {
    is_active: isActive,
    reason,
  });
  return response.data;
};

export const getPermissionsMatrix = async (): Promise<PermissionMatrixItem[]> => {
  const response = await apiClient.get<PermissionMatrixItem[]>('/admin/admins/permissions-matrix');
  return response.data;
};

export const changeAdminPassword = async (data: {
  current_password: string;
  new_password: string;
  confirm_password: string;
}): Promise<{ status: string; message: string }> => {
  const response = await apiClient.post('/auth/change-password', data);
  return response.data;
};

export const disableAdmin2FA = async (): Promise<{ status: string; message: string }> => {
  const response = await apiClient.post('/admin/security/2fa/disable');
  return response.data;
};

export interface SessionAdminInfo {
  user_id: string;
  email: string;
  role: string;
  role_name: string;
  permissions: string[];
  is_active: boolean;
}

export const getAuthenticatedAdmin = async (): Promise<SessionAdminInfo> => {
  const response = await apiClient.get<SessionAdminInfo>('/auth/me');
  return response.data;
};
