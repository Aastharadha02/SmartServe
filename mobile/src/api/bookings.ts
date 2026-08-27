import apiClient from './client';

export interface BookingItem {
  id: string;
  booking_reference: string;
  customer_name: string;
  customer_phone?: string;
  customer_email?: string;
  service_name: string;
  category: string;
  subcategory?: string;
  provider_name?: string;
  status: 'pending' | 'confirmed' | 'in_progress' | 'completed' | 'cancelled';
  scheduled_date: string;
  scheduled_time: string;
  total_amount: number;
  service_address: string;
  notes?: string;
  created_at?: string;
}

export interface CreateBookingPayload {
  service_id: string;
  service_name: string;
  category: string;
  subcategory?: string;
  customer_name: string;
  customer_phone: string;
  customer_email: string;
  service_address: string;
  scheduled_date: string;
  scheduled_time: string;
  total_amount: number;
  notes?: string;
}

export const bookingsApi = {
  getAllBookings: async (): Promise<BookingItem[]> => {
    const res = await apiClient.get<BookingItem[]>('/bookings');
    return res.data;
  },

  createBooking: async (payload: CreateBookingPayload): Promise<BookingItem> => {
    const res = await apiClient.post<BookingItem>('/bookings', payload);
    return res.data;
  },

  getBookingById: async (id: string): Promise<BookingItem> => {
    const res = await apiClient.get<BookingItem>(`/bookings/${id}`);
    return res.data;
  },
};
