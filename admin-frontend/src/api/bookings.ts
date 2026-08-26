import { apiClient } from './client';

export interface TimelineItem {
  event: string;
  reason?: string;
  timestamp: string;
}

export interface BookingItem {
  id: string;
  customer_id: string;
  customer_name?: string;
  customer_phone?: string;
  provider_id?: string | null;
  provider_name?: string | null;
  service_id: string;
  service_name?: string;
  status: string;
  payment_status: string;
  scheduled_time: string;
  address: string;
  total_price: number;
  otp_code?: string | null;
  timeline: TimelineItem[];
  allowed_next_statuses: string[];
  emergency_flag?: string | null;
  created_at: string;
}

export const getBookingsList = async (params?: {
  status_filter?: string;
  emergency_only?: boolean;
  search?: string;
  skip?: number;
  limit?: number;
}): Promise<BookingItem[]> => {
  const query = new URLSearchParams();
  if (params?.status_filter) query.append('status_filter', params.status_filter);
  if (params?.emergency_only !== undefined) query.append('emergency_only', String(params.emergency_only));
  if (params?.search) query.append('search', params.search);
  if (params?.skip !== undefined) query.append('skip', String(params.skip));
  if (params?.limit !== undefined) query.append('limit', String(params.limit));

  const response = await apiClient.get<BookingItem[]>(`/admin/bookings/?${query.toString()}`);
  return response.data;
};

export const getBookingDetail = async (bookingId: string): Promise<BookingItem> => {
  const response = await apiClient.get<BookingItem>(`/admin/bookings/${bookingId}`);
  return response.data;
};

export const updateBookingStatus = async (
  bookingId: string,
  nextStatus: string,
  reason?: string
): Promise<BookingItem> => {
  const response = await apiClient.patch<BookingItem>(`/admin/bookings/${bookingId}/status`, {
    next_status: nextStatus,
    reason,
  });
  return response.data;
};

export const reassignBookingProvider = async (
  bookingId: string,
  newProviderId: string,
  reason?: string
): Promise<{ status: string; booking_id: string; new_provider_id: string; provider_name: string; message: string }> => {
  const response = await apiClient.post(`/admin/bookings/${bookingId}/reassign`, {
    new_provider_id: newProviderId,
    reason,
  });
  return response.data;
};

export const createEmergencyDispatchBooking = async (data: {
  customer_id: string;
  service_id: string;
  scheduled_time: string;
  address: string;
  total_price: number;
  provider_id?: string;
  emergency_flag?: string;
}): Promise<BookingItem> => {
  const response = await apiClient.post<BookingItem>('/admin/bookings/', data);
  return response.data;
};
