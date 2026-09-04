import { apiClient } from './client';

export interface ServiceItem {
  id: string;
  category: string;
  subcategory: string;
  name: string;
  description?: string;
  base_price: number;
  max_demand_increase: number;
  max_discount: number;
  distinct_features?: string[];
  suggested_addons?: any[];
  is_active: boolean;
  created_at: string;
}

export interface ServiceCreatePayload {
  category: string;
  subcategory: string;
  name: string;
  description?: string;
  base_price: number;
  max_demand_increase?: number;
  max_discount?: number;
  distinct_features?: string[];
  suggested_addons?: any[];
  is_active?: boolean;
}

export interface ServiceUpdatePayload {
  category?: string;
  subcategory?: string;
  name?: string;
  description?: string;
  base_price?: number;
  max_demand_increase?: number;
  max_discount?: number;
  distinct_features?: string[];
  suggested_addons?: any[];
  is_active?: boolean;
  included?: string[];
  excluded?: string[];
  process_steps?: any[];
  aftercare?: string[];
  tools_materials?: string[];
  customer_setup?: string[];
  expected_results?: string[];
  important_notes?: string[];
  warranty?: string | null;
  faqs?: any[];
  tips?: string[];
  dos?: string[];
  donts?: string[];
  duration_minutes?: number;
}

export interface ProcessStepItem {
  step_number: number;
  title: string;
  description: string;
  duration_minutes?: number;
  is_key_step?: boolean;
}

export interface FaqItem {
  question: string;
  answer: string;
}

export interface AiMetadataResponse {
  service_name: string;
  category: string;
  subcategory?: string;
  description?: string;
  highlights?: string[];
  included?: string[];
  excluded?: string[];
  process_steps?: ProcessStepItem[];
  tools_materials?: string[];
  customer_setup?: string[];
  aftercare?: string[];
  important_notes?: string[];
  expected_results?: string[];
  warranty?: string | null;
  faqs?: FaqItem[];
  seo_keywords?: string[];
  
  // Legacy alias fields
  technician_sop?: string[];
  required_tools?: string[];
  customer_faqs?: any[];
  how_it_works?: any[];
  ai_generated_description?: string;
}

export interface ImportExcelResponse {
  status: string;
  inserted: number;
  updated: number;
  errors: string[];
}

export const formatRupee = (val: number): string => {
  return `₹${Math.round(val).toLocaleString('en-IN')}`;
};

export const getCatalogServices = async (
  category?: string,
  subcategory?: string,
  skip: number = 0,
  limit: number = 1000
): Promise<ServiceItem[]> => {
  const params: Record<string, any> = { skip, limit };
  if (category) params.category = category;
  if (subcategory) params.subcategory = subcategory;

  const response = await apiClient.get<ServiceItem[]>('/admin/catalog/services', { params });
  return response.data;
};

export const createCatalogService = async (payload: ServiceCreatePayload): Promise<ServiceItem> => {
  const response = await apiClient.post<ServiceItem>('/admin/catalog/services', payload);
  return response.data;
};

export const updateCatalogService = async (id: string, payload: ServiceUpdatePayload): Promise<ServiceItem> => {
  const response = await apiClient.put<ServiceItem>(`/admin/catalog/services/${id}`, payload);
  return response.data;
};

export const exportCatalogExcel = async (category?: string, subcategory?: string, search?: string): Promise<void> => {
  const params = new URLSearchParams();
  if (category) params.append('category', category);
  if (subcategory) params.append('subcategory', subcategory);
  if (search) params.append('search', search);

  const response = await apiClient.get(`/admin/catalog/export-excel?${params.toString()}`, {
    responseType: 'blob',
  });
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `SmartServe_Catalog_Export_${new Date().toISOString().slice(0, 10)}.xlsx`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

export const importCatalogExcel = async (file: File): Promise<ImportExcelResponse> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post<ImportExcelResponse>('/admin/catalog/import-excel', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export interface AuditLogItem {
  id: string;
  actor_email: string;
  actor_role: string;
  action: string;
  target_resource?: string;
  ip_address?: string;
  risk_level: string;
  metadata_json?: Record<string, any>;
  created_at: string;
}

export const previewImportCatalogExcel = async (file: File): Promise<any> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await apiClient.post('/admin/catalog/preview-import-excel', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const bulkUpdateServiceStatus = async (serviceIds: string[], isActive: boolean): Promise<{ status: string; updated_count: number }> => {
  const response = await apiClient.post('/admin/catalog/services/bulk-status', {
    service_ids: serviceIds,
    is_active: isActive,
  });
  return response.data;
};

export const generateAiMetadata = async (serviceId: string): Promise<AiMetadataResponse> => {
  const response = await apiClient.post<AiMetadataResponse>(`/admin/catalog/services/${serviceId}/ai-generate-metadata`);
  return response.data;
};

export const getServiceAuditLogs = async (serviceId: string): Promise<AuditLogItem[]> => {
  const response = await apiClient.get<AuditLogItem[]>(`/admin/catalog/services/${serviceId}/audit-logs`);
  return response.data;
};
