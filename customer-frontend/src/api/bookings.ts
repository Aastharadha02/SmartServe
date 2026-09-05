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
}

export interface BookingDetail {
  id: string;
  booking_reference: string;
  service_id: string;
  service_name: string;
  category: string;
  status: string;
  payment_status?: string;
  scheduled_date: string;
  scheduled_time: string;
  address_line1?: string;
  address?: string;
  total_price: number;
  total_amount?: number;
  otp_code?: string;
  provider_name?: string;
  created_at: string;
}

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
