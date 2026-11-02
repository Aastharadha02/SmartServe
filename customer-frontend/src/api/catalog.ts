import { apiClient } from './client';

export interface SubcategorySummary {
  name: string;
  service_count: number;
  active_count: number;
}

export interface CategoryItem {
  id: string;
  name: string;
  slug: string;
  display_name?: string;
  order?: number;
  image?: string;
  subcategories_count?: number;
  service_count?: number;
  active_count?: number;
  subcategories?: SubcategorySummary[];
}

export interface AddonItem {
  addon_id: string;
  name: string;
  price: number;
  description?: string;
}

export interface ServiceProcessStep {
  step_number: number;
  title: string;
  description: string;
  duration_minutes: number;
  is_key_step?: boolean;
}

export interface ServiceFeatureItem {
  title: string;
  description: string;
}

export interface ServiceMediaItem {
  id?: string;
  url: string;
  caption?: string;
  media_type?: string;
  is_cover?: boolean;
}

export interface ServiceFAQ {
  question: string;
  answer: string;
}

export interface ServiceItem {
  id: string;
  name: string;
  category: string;
  category_slug?: string;
  subcategory?: string;
  subcategory_slug?: string;
  description?: string;
  distinct_features?: string[];
  features?: string[];
  included?: string[];
  excluded?: string[];
  highlights?: string[];
  base_price: number;
  max_demand_increase?: number;
  max_discount?: number;
  duration_minutes?: number;
  rating?: number;
  review_count?: number;
  is_emergency?: boolean;
  is_emergency_eligible?: boolean;
  image_url?: string;
  suggested_addons?: AddonItem[];
  process_steps?: ServiceProcessStep[];
  service_features?: ServiceFeatureItem[];
  service_media?: ServiceMediaItem[];
  tools_materials?: string[];
  customer_setup?: string[];
  aftercare?: string[];
  expected_results?: string[];
  important_notes?: string[];
  warranty?: string;
  faqs?: ServiceFAQ[];
  tips?: string[];
  dos?: string[];
  donts?: string[];
  seo_title?: string;
  seo_description?: string;
  keywords?: string[];
  is_active?: boolean;
  created_at?: string;
  updated_at?: string;
}

export interface ProviderSlotDetail {
  slot_id: string;
  slot_date: string;
  start_time: string;
  end_time: string;
  display_time: string;
  is_available: boolean;
  available_times: string[];
}

export interface EligibleProvider {
  provider_id: string;
  full_name: string;
  category?: string;
  skills?: string;
  experience_years: number;
  reliability_score: number;
  acceptance_rate: number;
  service_area?: string;
  available_slots: string[];
  structured_slots?: ProviderSlotDetail[];
  is_available: boolean;
}

export const getCatalogCategories = async (): Promise<CategoryItem[]> => {
  const res = await apiClient.get<CategoryItem[]>('/customer/catalog/categories');
  return res.data;
};

export const getCatalogServices = async (params?: {
  category?: string;
  subcategory?: string;
  q?: string;
  emergency_only?: boolean;
  skip?: number;
  limit?: number;
}): Promise<ServiceItem[]> => {
  const res = await apiClient.get<ServiceItem[]>('/customer/catalog/services', { params });
  return res.data;
};

export const getServiceDetail = async (serviceId: string): Promise<ServiceItem> => {
  const res = await apiClient.get<ServiceItem>(`/customer/catalog/services/${serviceId}`);
  return res.data;
};

export const getServiceEligibleProviders = async (serviceId: string): Promise<EligibleProvider[]> => {
  const res = await apiClient.get<EligibleProvider[]>(`/customer/catalog/services/${serviceId}/eligible-providers`);
  return res.data;
};
