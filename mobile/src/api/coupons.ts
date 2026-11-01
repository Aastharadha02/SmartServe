import apiClient from './client';

export interface CouponItem {
  id: string;
  code: string;
  discount_type: 'PERCENTAGE' | 'FIXED';
  discount_value: number;
  min_order_amount: number;
  max_discount_amount?: number | null;
  valid_from: string;
  valid_until: string;
  is_active: boolean;
  is_public: boolean;
  description?: string;
  category?: string | null;
}

export interface CouponValidatePayload {
  code: string;
  subtotal: number;
  category?: string;
  service_id?: string;
  service_ids?: string[];
}

export interface CouponValidateResult {
  is_valid: boolean;
  code: string;
  discount_amount: number;
  final_total: number;
  message: string;
  discount_type?: string;
  discount_value?: number;
  min_order_amount?: number;
}

export interface SpinRewardResult {
  code: string;
  discount_amount: number;
  discount_type: string;
  discount_value: number;
  min_order_amount: number;
  expires_at: string;
  message: string;
}

export const couponsApi = {
  /** GET /coupons - Fetch all active public coupons */
  getActiveCoupons: async (): Promise<CouponItem[]> => {
    try {
      const res = await apiClient.get<CouponItem[]>('/coupons');
      return Array.isArray(res.data) ? res.data : [];
    } catch {
      return [];
    }
  },

  /** POST /coupons/validate - Server-side coupon verification */
  validateCoupon: async (payload: CouponValidatePayload): Promise<CouponValidateResult> => {
    const res = await apiClient.post<CouponValidateResult>('/coupons/validate', payload);
    return res.data;
  },

  /** POST /coupons/spin-reward - Gamified spin the wheel reward */
  spinReward: async (rewardTier?: string, bookingId?: string): Promise<SpinRewardResult> => {
    const res = await apiClient.post<SpinRewardResult>('/coupons/spin-reward', {
      reward_tier: rewardTier || 'SERVE75',
      booking_id: bookingId,
    });
    return res.data;
  },
};

