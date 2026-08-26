import { apiClient } from './client';

export interface CustomerFlagItem {
  id: string;
  flag_type: string;
  reason: string;
  created_at: string;
}

export interface CustomerBookingItem {
  id: string;
  service_id: string;
  service_name: string;
  provider_name: string;
  status: string;
  total_price: number;
  scheduled_time: string;
  created_at: string;
}

export interface CustomerItem {
  id: string;
  user_id?: string;
  full_name: string;
  email: string;
  phone?: string;
  is_active: boolean;
  bookings_count: number;
  completed_bookings_count: number;
  cancelled_bookings_count: number;
  is_flagged: boolean;
  flags: CustomerFlagItem[];
  bookings?: CustomerBookingItem[];
  created_at: string;
}

export const getCustomersList = async (params?: {
  search?: string;
  is_active?: boolean;
  is_flagged?: boolean;
}): Promise<CustomerItem[]> => {
  const query = new URLSearchParams();
  if (params?.search) query.append('search', params.search);
  if (params?.is_active !== undefined) query.append('is_active', String(params.is_active));
  if (params?.is_flagged !== undefined) query.append('is_flagged', String(params.is_flagged));

  const response = await apiClient.get<CustomerItem[]>(`/admin/customers/?${query.toString()}`);
  return response.data;
};

export const getCustomerDetail = async (customerId: string): Promise<CustomerItem> => {
  const response = await apiClient.get<CustomerItem>(`/admin/customers/${customerId}`);
  return response.data;
};

export const updateCustomerAccountStatus = async (
  customerId: string,
  isActive: boolean,
  reason?: string
): Promise<{ status: string; is_active: boolean; message: string }> => {
  const response = await apiClient.post(`/admin/customers/${customerId}/status`, {
    is_active: isActive,
    reason,
  });
  return response.data;
};

export const flagCustomerAccount = async (
  customerId: string,
  flagType: string,
  reason: string
): Promise<{ status: string; flag_type: string; message: string }> => {
  const response = await apiClient.post(`/admin/customers/${customerId}/flag`, {
    flag_type: flagType,
    reason,
  });
  return response.data;
};
