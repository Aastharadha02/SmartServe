import { apiClient } from './client';

export interface EmailTemplateItem {
  id: string;
  template_key: string;
  subject: string;
  body_html: string;
  is_active: boolean;
  supported_variables: string[];
  updated_at: string;
}

export interface EmailLogItem {
  id: string;
  recipient_email: string;
  subject: string;
  template_key?: string | null;
  status: string;
  error_message?: string | null;
  sent_at: string;
}

export const getEmailTemplates = async (): Promise<EmailTemplateItem[]> => {
  const response = await apiClient.get<EmailTemplateItem[]>('/admin/emails/templates');
  return response.data;
};

export const upsertEmailTemplate = async (data: {
  template_key: string;
  subject: string;
  body_html: string;
  is_active?: boolean;
}): Promise<EmailTemplateItem> => {
  const response = await apiClient.post<EmailTemplateItem>('/admin/emails/templates', data);
  return response.data;
};

export const dispatchEmail = async (data: {
  recipient_email: string;
  subject: string;
  body_text: string;
  template_key?: string;
}): Promise<EmailLogItem> => {
  const response = await apiClient.post<EmailLogItem>('/admin/emails/send', data);
  return response.data;
};

export const getEmailLogs = async (params?: {
  search?: string;
  status_filter?: string;
  template_filter?: string;
  skip?: number;
  limit?: number;
}): Promise<EmailLogItem[]> => {
  const query = new URLSearchParams();
  if (params?.search) query.append('search', params.search);
  if (params?.status_filter) query.append('status_filter', params.status_filter);
  if (params?.template_filter) query.append('template_filter', params.template_filter);
  if (params?.skip !== undefined) query.append('skip', String(params.skip));
  if (params?.limit !== undefined) query.append('limit', String(params.limit));

  const response = await apiClient.get<EmailLogItem[]>(`/admin/emails/logs?${query.toString()}`);
  return response.data;
};
