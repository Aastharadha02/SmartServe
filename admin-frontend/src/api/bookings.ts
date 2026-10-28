import { apiClient } from './client';

export interface TimelineItem {
  event: string;
  reason?: string;
  timestamp: string;
}

export interface BookingItem {
  id: string;
  booking_reference?: string | null;
  customer_id: string;
  customer_name?: string;
  customer_phone?: string;
  provider_id?: string | null;
  provider_name?: string | null;
  service_id: string;
  service_name?: string;
  status: string;
  payment_status: string;
  payment_method?: string;
  scheduled_time: string;
  address: string;
  total_price: number;
  otp_code?: string | null;
  start_otp?: string | null;
  completion_otp?: string | null;
  timeline: TimelineItem[];
  allowed_next_statuses: string[];
  emergency_flag?: string | null;
  cancellation_reason?: string | null;
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

export interface AdminProviderLocation {
  latitude: number;
  longitude: number;
  heading?: number | null;
  speed?: number | null;
  accuracy?: number | null;
  is_active?: boolean;
  updated_at?: string | null;
}

export interface AdminCustomerLocation {
  latitude: number;
  longitude: number;
  address: string;
  city: string;
}

export interface AdminBookingLocationResponse {
  booking_id: string;
  booking_reference: string;
  status: string;
  customer: {
    id: string;
    name: string;
    phone?: string | null;
  };
  provider?: {
    id: string;
    full_name: string;
    phone?: string | null;
    photo_url?: string;
    category?: string;
    experience_years?: number;
    rating?: number;
    is_verified?: boolean;
    service_area?: string;
  } | null;
  provider_location?: AdminProviderLocation | null;
  customer_location?: AdminCustomerLocation | null;
  service_name: string;
  total_price: number;
  scheduled_time: string;
  address: string;
  timeline: any[];
}

export const getAdminBookingLocation = async (bookingId: string): Promise<AdminBookingLocationResponse> => {
  const response = await apiClient.get<AdminBookingLocationResponse>(`/admin/bookings/${bookingId}/location`);
  return response.data;
};

export interface PaymentRecord {
  id: string;
  booking_id: string;
  booking_reference?: string;
  payment_method: string;
  agreed_amount: number;
  reported_amount?: number | null;
  status: string;
  discrepancy_flag: boolean;
  discrepancy_amount?: number | null;
  collected_at?: string | null;
  reviewed_by_id?: string | null;
  reviewed_by_name?: string | null;
  reviewed_at?: string | null;
  rejection_reason?: string | null;
  notes?: string | null;
  created_at: string;
  customer_name?: string | null;
  provider_name?: string | null;
  service_name?: string | null;
}

export const getPaymentReviewList = async (statusFilter?: string): Promise<PaymentRecord[]> => {
  const query = statusFilter ? `?status_filter=${encodeURIComponent(statusFilter)}` : '';
  const response = await apiClient.get<PaymentRecord[]>(`/admin/bookings/payments/review${query}`);
  return response.data;
};

export const getBookingPayments = async (bookingId: string): Promise<PaymentRecord[]> => {
  const response = await apiClient.get<PaymentRecord[]>(`/admin/bookings/${bookingId}/payments`);
  return response.data;
};

export const verifyPaymentCollection = async (paymentId: string, notes?: string): Promise<PaymentRecord> => {
  const response = await apiClient.post<PaymentRecord>(`/admin/bookings/payments/${paymentId}/verify`, { notes });
  return response.data;
};

export const rejectPaymentCollection = async (paymentId: string, reason: string): Promise<PaymentRecord> => {
  const response = await apiClient.post<PaymentRecord>(`/admin/bookings/payments/${paymentId}/reject`, { reason });
  return response.data;
};

export interface AdminNotificationItem {
  id: string;
  booking_id: string;
  booking_reference: string;
  customer_id?: string | null;
  event_type: string;
  channel: string;
  recipient: string;
  delivery_status: string;
  retry_count: number;
  last_attempt_at: string;
  error_message?: string | null;
  created_at: string;
}

export const getAdminBookingNotifications = async (bookingReference: string): Promise<AdminNotificationItem[]> => {
  const response = await apiClient.get<AdminNotificationItem[]>(`/admins/notifications?booking_reference=${encodeURIComponent(bookingReference)}`);
  return response.data;
};

export const retryAdminNotification = async (notificationId: string): Promise<AdminNotificationItem> => {
  const response = await apiClient.post<AdminNotificationItem>(`/admins/notifications/${notificationId}/retry`);
  return response.data;
};

