import { apiClient } from './client';
import { CustomerSessionResponse } from './auth';

export interface ProfileUpdatePayload {
  full_name?: string;
  phone?: string;
  preferences?: string[];
}

export const getCustomerProfile = async (): Promise<CustomerSessionResponse> => {
  const res = await apiClient.get<CustomerSessionResponse>('/customer/profile');
  return res.data;
};

export const updateCustomerProfile = async (payload: ProfileUpdatePayload): Promise<CustomerSessionResponse> => {
  const res = await apiClient.patch<CustomerSessionResponse>('/customer/profile', payload);
  return res.data;
};
