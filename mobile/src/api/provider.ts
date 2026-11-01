import apiClient from './client';

export interface ProviderProfileResponse {
  id: string;
  user_id: string;
  full_name: string;
  email: string;
  phone?: string;
  category?: string;
  skills?: string;
  experience_years?: number;
  verification_status: string;
  rating?: number;
  completed_jobs_count?: number;
  is_active?: boolean;
}

export interface ProviderDashboardStats {
  assigned_bookings: number;
  completed_bookings: number;
  active_bookings: number;
  total_earnings: number;
  rating: number;
}

export interface ProviderBookingItem {
  id: string;
  booking_reference: string;
  service_name: string;
  category: string;
  status: string;
  scheduled_date: string;
  scheduled_time: string;
  total_amount: number;
  address_line1: string;
  landmark?: string;
  city: string;
  pincode: string;
  customer_name?: string;
  customer_phone?: string;
  start_otp_required?: boolean;
  completion_otp_required?: boolean;
  payment_method?: string;
  payment_status?: string;
  before_photo_url?: string;
  after_photo_url?: string;
  cash_collected?: number;
}

export interface AvailabilitySlot {
  id?: string;
  day_of_week: number; // 0=Sunday, 1=Monday...
  start_time: string; // HH:MM
  end_time: string; // HH:MM
  is_available: boolean;
}

export const providerApi = {
  /** GET /providers/me - Profile info */
  getMyProfile: async (): Promise<ProviderProfileResponse> => {
    const res = await apiClient.get<ProviderProfileResponse>('/providers/me');
    return res.data;
  },

  /** GET /providers/me/dashboard-stats */
  getDashboardStats: async (): Promise<ProviderDashboardStats> => {
    try {
      const res = await apiClient.get<ProviderDashboardStats>('/providers/me/dashboard-stats');
      return res.data;
    } catch {
      return {
        assigned_bookings: 0,
        completed_bookings: 0,
        active_bookings: 0,
        total_earnings: 0,
        rating: 4.8,
      };
    }
  },

  /** GET /providers/me/bookings - List assigned jobs */
  getAssignedBookings: async (): Promise<ProviderBookingItem[]> => {
    const res = await apiClient.get<ProviderBookingItem[]>('/providers/me/bookings');
    return Array.isArray(res.data) ? res.data : [];
  },

  /** GET /providers/me/bookings/{id} */
  getBookingDetail: async (bookingId: string): Promise<ProviderBookingItem> => {
    const res = await apiClient.get<ProviderBookingItem>(`/providers/me/bookings/${bookingId}`);
    return res.data;
  },

  /** POST /providers/me/bookings/{id}/on-the-way */
  markOnTheWay: async (bookingId: string): Promise<ProviderBookingItem> => {
    const res = await apiClient.post<ProviderBookingItem>(`/providers/me/bookings/${bookingId}/on-the-way`);
    return res.data;
  },

  /** POST /providers/me/bookings/{id}/arrived */
  markArrived: async (bookingId: string): Promise<ProviderBookingItem> => {
    const res = await apiClient.post<ProviderBookingItem>(`/providers/me/bookings/${bookingId}/arrived`);
    return res.data;
  },

  /** POST /providers/me/bookings/{id}/start - Start job with Start OTP */
  startJob: async (bookingId: string, otpCode: string): Promise<ProviderBookingItem> => {
    const res = await apiClient.post<ProviderBookingItem>(`/providers/me/bookings/${bookingId}/start`, {
      otp_code: otpCode,
    });
    return res.data;
  },

  /** POST /providers/me/bookings/{id}/complete - Complete job with Completion OTP */
  completeJob: async (bookingId: string, otpCode?: string, notes?: string): Promise<ProviderBookingItem> => {
    const res = await apiClient.post<ProviderBookingItem>(`/providers/me/bookings/${bookingId}/complete`, {
      otp_code: otpCode || null,
      notes: notes || 'Completed successfully',
    });
    return res.data;
  },

  /** POST /providers/me/bookings/{id}/photos/before */
  uploadBeforePhoto: async (bookingId: string, photoUri: string): Promise<{ photo_url: string }> => {
    const formData = new FormData();
    const filename = photoUri.split('/').pop() || 'before_photo.jpg';
    const match = /\.(\w+)$/.exec(filename);
    const type = match ? `image/${match[1]}` : 'image/jpeg';

    formData.append('file', {
      uri: photoUri,
      name: filename,
      type,
    } as any);

    const res = await apiClient.post(`/providers/me/bookings/${bookingId}/photos/before`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  /** POST /providers/me/bookings/{id}/photos/after */
  uploadAfterPhoto: async (bookingId: string, photoUri: string): Promise<{ photo_url: string }> => {
    const formData = new FormData();
    const filename = photoUri.split('/').pop() || 'after_photo.jpg';
    const match = /\.(\w+)$/.exec(filename);
    const type = match ? `image/${match[1]}` : 'image/jpeg';

    formData.append('file', {
      uri: photoUri,
      name: filename,
      type,
    } as any);

    const res = await apiClient.post(`/providers/me/bookings/${bookingId}/photos/after`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  /** POST /providers/me/bookings/{id}/report-cash-collected */
  reportCashCollected: async (
    bookingId: string,
    amount: number,
    notes?: string
  ): Promise<{ message: string; reported_amount: number }> => {
    const res = await apiClient.post(`/providers/me/bookings/${bookingId}/report-cash-collected`, {
      reported_amount: amount,
      notes: notes || 'Cash received by provider',
    });
    return res.data;
  },

  /** GET /providers/me/availability */
  getAvailability: async (): Promise<AvailabilitySlot[]> => {
    try {
      const res = await apiClient.get<AvailabilitySlot[]>('/providers/me/availability');
      return Array.isArray(res.data) ? res.data : [];
    } catch {
      return [];
    }
  },

  /** POST /providers/me/availability */
  updateAvailabilitySlot: async (slot: AvailabilitySlot): Promise<AvailabilitySlot> => {
    const res = await apiClient.post<AvailabilitySlot>('/providers/me/availability', slot);
    return res.data;
  },
};

