import apiClient from './client';

export interface WarrantyCardResponse {
  id: string;
  booking_id: string;
  customer_id: string;
  provider_id?: string | null;
  service_name: string;
  issued_at: string;
  expires_at: string;
  is_active: boolean;
  claim_status: string;
  claim_description?: string | null;
  claim_submitted_at?: string | null;
  claim_resolved_at?: string | null;
  claim_notes?: string | null;
  days_remaining: number;
  duration_days: number;
  nominal_fee: number;
  terms: string;
  badge_label: string;
  is_eligible: boolean;
}

export interface WarrantyClaimResult {
  success: boolean;
  message: string;
  claim_status: string;
  nominal_fee?: number;
  claim_submitted_at?: string;
}

export const warrantyApi = {
  /** GET /customer/bookings/{booking_id}/warranty */
  getWarrantyCard: async (bookingId: string): Promise<WarrantyCardResponse | null> => {
    try {
      const res = await apiClient.get<WarrantyCardResponse>(`/customer/bookings/${bookingId}/warranty`);
      return res.data;
    } catch {
      return null;
    }
  },

  /** POST /customer/bookings/{booking_id}/warranty/claim */
  submitWarrantyClaim: async (bookingId: string, description: string): Promise<WarrantyClaimResult> => {
    const res = await apiClient.post<WarrantyClaimResult>(`/customer/bookings/${bookingId}/warranty/claim`, {
      description,
    });
    return res.data;
  },
};

