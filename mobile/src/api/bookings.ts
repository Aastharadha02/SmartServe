import apiClient from './client';

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

export interface BookingTimelineItem {
  event: string;
  status?: string;
  previous_status?: string;
  actor?: string;
  role?: string;
  reason?: string;
  timestamp: string;
  provider_assigned?: string;
  provider_id?: string;
}

export interface BookingItem {
  id: string;
  booking_reference: string;
  customer_id: string;
  service_id: string;
  service_name: string;
  category: string;
  subcategory?: string;
  provider_id?: string;
  provider_name?: string;
  provider?: ProviderProfileInfo | null;
  status: string;
  scheduled_date: string;
  scheduled_time: string;
  total_price: number;
  total_amount?: number;
  address_line1: string;
  landmark?: string;
  city: string;
  pincode: string;
  notes?: string;
  payment_method?: string;
  payment_status?: string;
  otp_code?: string;
  start_otp?: string;
  completion_otp?: string;
  cancellation_reason?: string;
  emergency_flag?: string;
  timeline?: BookingTimelineItem[];
  created_at?: string;
}

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
  notes?: string;
  payment_method?: string;
  provider_id?: string;
}

export const bookingsApi = {
  /** GET /customer/bookings */
  getAllBookings: async (): Promise<BookingItem[]> => {
    const res = await apiClient.get<BookingItem[]>('/customer/bookings');
    return Array.isArray(res.data) ? res.data : [];
  },

  /** GET /customer/bookings/{id} */
  getBookingById: async (id: string): Promise<BookingItem> => {
    const res = await apiClient.get<BookingItem>(`/customer/bookings/${id}`);
    return res.data;
  },

  /** POST /customer/bookings */
  createBooking: async (payload: CreateBookingPayload): Promise<BookingItem> => {
    const res = await apiClient.post<BookingItem>('/customer/bookings', payload);
    return res.data;
  },

  /** POST /customer/bookings/{id}/cancel */
  cancelBooking: async (bookingId: string, reason?: string): Promise<BookingItem> => {
    const r = reason || 'Cancelled by Customer';
    const res = await apiClient.post<BookingItem>(`/customer/bookings/${bookingId}/cancel`, {
      reason: r,
      cancellation_reason: r,
    });
    return res.data;
  },

  /** GET /customer/bookings/{booking_id}/location */
  getBookingLocation: async (bookingId: string): Promise<BookingLocationResponse | null> => {
    try {
      const res = await apiClient.get<BookingLocationResponse>(`/customer/bookings/${bookingId}/location`);
      return res.data;
    } catch {
      return null;
    }
  },

  /** PATCH /customer/bookings/{booking_id}/location */
  updateCustomerLocation: async (bookingId: string, latitude: number, longitude: number): Promise<void> => {
    try {
      await apiClient.patch(`/customer/bookings/${bookingId}/location`, { latitude, longitude });
    } catch (err) {
      console.warn('Failed to update customer location', err);
    }
  },
};
