import { apiClient } from './client';

export interface MessageItem {
  id: string;
  sender_role: string;
  sender_name: string;
  message_text: string;
  created_at: string;
}

export interface SupportTicketDetail {
  id: string;
  subject: string;
  category: string;
  priority: string;
  status: string;
  created_at: string;
  description?: string;
  messages: MessageItem[];
}

export interface CreateTicketPayload {
  subject: string;
  category: string;
  priority?: string;
  description: string;
  booking_id?: string;
}

export const createSupportTicket = async (payload: CreateTicketPayload): Promise<SupportTicketDetail> => {
  const res = await apiClient.post<SupportTicketDetail>('/customer/support/tickets', payload);
  return res.data;
};

export const getCustomerTickets = async (): Promise<SupportTicketDetail[]> => {
  const res = await apiClient.get<SupportTicketDetail[]>('/customer/support/tickets');
  return res.data;
};

export const getTicketDetail = async (ticketId: string): Promise<SupportTicketDetail> => {
  const res = await apiClient.get<SupportTicketDetail>(`/customer/support/tickets/${ticketId}`);
  return res.data;
};

export const addTicketMessage = async (ticketId: string, message_text: string): Promise<MessageItem> => {
  const res = await apiClient.post<MessageItem>(`/customer/support/tickets/${ticketId}/messages`, { message_text });
  return res.data;
};
