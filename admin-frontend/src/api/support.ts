import { apiClient } from './client';

export interface SupportMetrics {
  open_tickets: number;
  in_progress: number;
  escalated: number;
  high_priority: number;
  resolved: number;
}

export interface TicketMessageItem {
  id: string;
  sender_id: string;
  sender_role: string;
  message_text: string;
  attachment_url?: string | null;
  created_at: string;
}

export interface SupportTicketItem {
  id: string;
  customer_id: string;
  customer_name?: string;
  customer_email?: string;
  customer_phone?: string;
  assigned_admin_email?: string | null;
  booking_id?: string | null;
  subject: string;
  description: string;
  priority: string;
  status: string;
  escalated_to_admin: boolean;
  image_evidence_url?: string | null;
  ai_analysis?: {
    ocr_extracted_text?: string;
    sentiment_score?: number;
    complaint_category?: string;
  } | null;
  customer_context?: {
    previous_tickets_count?: number;
    relevant_booking_id?: string;
    risk_flag?: string;
  } | null;
  created_at: string;
  updated_at?: string;
  messages: TicketMessageItem[];
}

export const getSupportDashboardMetrics = async (): Promise<SupportMetrics> => {
  const response = await apiClient.get<SupportMetrics>('/admin/support/dashboard-metrics');
  return response.data;
};

export const getSupportTicketsList = async (params?: {
  status_filter?: string;
  priority_filter?: string;
  escalated_only?: boolean;
  search?: string;
  skip?: number;
  limit?: number;
}): Promise<SupportTicketItem[]> => {
  const query = new URLSearchParams();
  if (params?.status_filter) query.append('status_filter', params.status_filter);
  if (params?.priority_filter) query.append('priority_filter', params.priority_filter);
  if (params?.escalated_only !== undefined) query.append('escalated_only', String(params.escalated_only));
  if (params?.search) query.append('search', params.search);
  if (params?.skip !== undefined) query.append('skip', String(params.skip));
  if (params?.limit !== undefined) query.append('limit', String(params.limit));

  const response = await apiClient.get<SupportTicketItem[]>(`/admin/support/tickets?${query.toString()}`);
  return response.data;
};

export const getSupportTicketDetail = async (ticketId: string): Promise<SupportTicketItem> => {
  const response = await apiClient.get<SupportTicketItem>(`/admin/support/tickets/${ticketId}`);
  return response.data;
};

export const replyToSupportTicket = async (
  ticketId: string,
  messageText: string,
  attachmentUrl?: string
): Promise<{ status: string; ticket_id: string; message_id: string; message: string }> => {
  const response = await apiClient.post(`/admin/support/tickets/${ticketId}/reply`, {
    message_text: messageText,
    attachment_url: attachmentUrl,
  });
  return response.data;
};

export const escalateSupportTicket = async (
  ticketId: string
): Promise<{ status: string; ticket_id: string; escalated_to_admin: boolean; message: string }> => {
  const response = await apiClient.post(`/admin/support/tickets/${ticketId}/escalate`);
  return response.data;
};

export const updateTicketPriorityAndStatus = async (
  ticketId: string,
  data: {
    status?: string;
    priority?: string;
    escalated_to_admin?: boolean;
  }
): Promise<{ status: string; ticket_id: string; new_status: string; new_priority: string; message: string }> => {
  const response = await apiClient.patch(`/admin/support/tickets/${ticketId}/priority-status`, data);
  return response.data;
};

export const getSignedEvidenceUrl = async (
  ticketId: string,
  filePath: string = 'evidence_photo.jpg'
): Promise<{ ticket_id: string; signed_url: string; expires_in_seconds: number }> => {
  const query = new URLSearchParams({ ticket_id: ticketId, file_path: filePath });
  const response = await apiClient.get(`/admin/support/evidence/signed-url?${query.toString()}`);
  return response.data;
};
