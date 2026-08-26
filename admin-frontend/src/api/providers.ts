import { apiClient } from './client';

export interface ProviderItem {
  id: string;
  user_id: string;
  full_name: string;
  email: string;
  phone: string;
  category: string;
  experience_years: number;
  base_price: number;
  is_verified: boolean;
  is_active: boolean;
  reliability_score: number;
  acceptance_rate: number;
  on_time_rate: number;
  cancellation_rate: number;
  rating: number;
  completed_bookings: number;
  composite_rank_score: number;
  rank_tier: string;
  created_at: string;
  documents: Array<{
    id: string;
    document_url: string;
    certificate_type: string;
    document_number?: string;
    extracted_name?: string;
    is_duplicate: boolean;
    verification_status: string;
    ai_scan_signal?: any;
  }>;
}

export interface ProviderRanking {
  provider_user_id: string;
  full_name: string;
  category: string;
  reliability_score: number;
  acceptance_rate: number;
  on_time_rate: number;
  composite_rank_score: number;
  rank_tier: string;
  rank_position: number;
}

export interface ProviderEtaEstimate {
  provider_user_id: string;
  distance_km: number;
  traffic_multiplier: number;
  travel_minutes: number;
  prep_buffer_minutes: number;
  total_eta_minutes: number;
  estimated_arrival_window: string;
}

export const getProvidersList = async (params?: {
  search?: string;
  category?: string;
  verification_status?: string;
  is_active?: boolean;
}): Promise<ProviderItem[]> => {
  const query = new URLSearchParams();
  if (params?.search) query.append('search', params.search);
  if (params?.category) query.append('category', params.category);
  if (params?.verification_status) query.append('verification_status', params.verification_status);
  if (params?.is_active !== undefined) query.append('is_active', String(params.is_active));

  const response = await apiClient.get<ProviderItem[]>(`/admin/providers/?${query.toString()}`);
  return response.data;
};

export const getProviderDetail = async (providerUserId: string): Promise<ProviderItem> => {
  const response = await apiClient.get<ProviderItem>(`/admin/providers/${providerUserId}`);
  return response.data;
};

export const verifyProviderDocuments = async (
  providerUserId: string,
  verificationStatus: 'Approved' | 'Rejected',
  reason?: string
): Promise<{ status: string; verification_status: string; message: string }> => {
  const response = await apiClient.post(`/admin/providers/${providerUserId}/verify`, {
    verification_status: verificationStatus,
    reason,
  });
  return response.data;
};

export const updateProviderAccountStatus = async (
  providerUserId: string,
  isActive: boolean,
  reason?: string
): Promise<{ status: string; is_active: boolean; message: string }> => {
  const response = await apiClient.post(`/admin/providers/${providerUserId}/status`, {
    is_active: isActive,
    reason,
  });
  return response.data;
};

export const getProviderRankings = async (): Promise<ProviderRanking[]> => {
  const response = await apiClient.get<ProviderRanking[]>('/admin/providers/ranking');
  return response.data;
};

export const estimateProviderEta = async (
  providerUserId?: string,
  distanceKm: number = 5.2
): Promise<ProviderEtaEstimate> => {
  const query = new URLSearchParams();
  if (providerUserId) query.append('provider_user_id', providerUserId);
  query.append('distance_km', String(distanceKm));

  const response = await apiClient.get<ProviderEtaEstimate>(`/admin/providers/eta-estimate?${query.toString()}`);
  return response.data;
};
