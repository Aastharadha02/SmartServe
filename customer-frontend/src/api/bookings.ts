import { apiClient } from './client';

export interface CreateBookingPayload {
  service_id: string;
  service_name?: string;
  category?: string;
  scheduled_date: string;
  scheduled_time: string;
  address_line1: string;
  landmark?: string;
  city?: string;
  pincode?: string;
  payment_method?: string;
  notes?: string;
  provider_id?: string;
}

export interface BookingDetail {
  id: string;
  booking_reference: string;
  service_id: string;
  service_name: string;
  category: string;
  status: string;
  payment_status?: string;
  payment_method?: string;
  start_otp?: string;
  completion_otp?: string;
  scheduled_date: string;
  scheduled_time: string;
  address_line1?: string;
  address?: string;
  landmark?: string;
  city?: string;
  pincode?: string;
  total_price: number;
  total_amount?: number;
  otp_code?: string;
  provider_id?: string;
  provider_name?: string;
  provider?: ProviderProfileInfo | null;
  emergency_flag?: string;
  cancellation_reason?: string;
  created_at: string;
}

export interface BookingPaymentItem {
  id: string;
  booking_id: string;
  payment_method: string;
  agreed_amount: number;
  reported_amount?: number | null;
  status: string;
  discrepancy_flag: boolean;
  collected_at?: string | null;
  reviewed_at?: string | null;
  rejection_reason?: string | null;
  created_at: string;
}

export const getBookingPayments = async (bookingId: string): Promise<BookingPaymentItem[]> => {
  const res = await apiClient.get<BookingPaymentItem[]>(`/customer/bookings/${bookingId}/payments`);
  return res.data;
};

export const createBooking = async (payload: CreateBookingPayload): Promise<BookingDetail> => {
  const res = await apiClient.post<BookingDetail>('/customer/bookings', payload);
  return res.data;
};

export const getCustomerBookings = async (): Promise<BookingDetail[]> => {
  const res = await apiClient.get<BookingDetail[]>('/customer/bookings');
  return res.data;
};

export const getBookingDetail = async (bookingId: string): Promise<BookingDetail> => {
  const res = await apiClient.get<BookingDetail>(`/customer/bookings/${bookingId}`);
  return res.data;
};

export const cancelBooking = async (bookingId: string, reason?: string): Promise<BookingDetail> => {
  const r = reason || 'Cancelled by Customer';
  const res = await apiClient.post<BookingDetail>(`/customer/bookings/${bookingId}/cancel`, { 
    reason: r,
    cancellation_reason: r 
  });
  return res.data;
};

export const updateCustomerLocation = async (bookingId: string, latitude: number, longitude: number): Promise<void> => {
  try {
    await apiClient.patch(`/customer/bookings/${bookingId}/location`, { latitude, longitude });
  } catch (err) {
    console.warn('Failed to sync customer location to backend:', err);
  }
};

export interface ProviderProfileInfo {
  provider_id: string;
  full_name: string;
  photo_url?: string;
  category?: string;
  skills?: string;
  experience_years?: number;
  reliability_score?: number;
  rating?: number;
  is_verified?: boolean;
  service_area?: string;
}

export interface ProviderGpsLocation {
  latitude: number;
  longitude: number;
  heading?: number | null;
  speed?: number | null;
  accuracy?: number | null;
  updated_at?: string;
}

export interface CustomerLocationInfo {
  latitude: number;
  longitude: number;
  address?: string;
  city?: string;
}

export interface BookingLocationResponse {
  booking_id: string;
  booking_reference: string;
  status: string;
  provider: ProviderProfileInfo | null;
  provider_location: ProviderGpsLocation | null;
  customer_location: CustomerLocationInfo;
  service_name: string;
  scheduled_date: string;
  scheduled_time: string;
}

export const getBookingLiveLocation = async (bookingId: string): Promise<BookingLocationResponse> => {
  const res = await apiClient.get<BookingLocationResponse>(`/customer/bookings/${bookingId}/location`);
  return res.data;
};

export interface CustomerNotificationItem {
  id: string;
  booking_id: string;
  booking_reference: string;
  event_type: string;
  channel: string;
  delivery_status: string;
  created_at: string;
  last_attempt_at?: string | null;
}

export const getBookingNotifications = async (bookingId: string): Promise<CustomerNotificationItem[]> => {
  const res = await apiClient.get<CustomerNotificationItem[]>(`/customer/bookings/${bookingId}/notifications`);
  return res.data;
};


