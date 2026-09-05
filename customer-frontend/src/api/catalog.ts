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

export const getCatalogCategories = async (): Promise<CategoryItem[]> => {
  const res = await apiClient.get<CategoryItem[]>('/customer/catalog/categories');
  return res.data;
};

export const getCatalogServices = async (params?: {
  category?: string;
  subcategory?: string;
  q?: string;
  emergency_only?: boolean;
}): Promise<ServiceItem[]> => {
  const res = await apiClient.get<ServiceItem[]>('/customer/catalog/services', { params });
  return res.data;
};

export const getServiceDetail = async (serviceId: string): Promise<ServiceItem> => {
  const res = await apiClient.get<ServiceItem>(`/customer/catalog/services/${serviceId}`);
  return res.data;
};
