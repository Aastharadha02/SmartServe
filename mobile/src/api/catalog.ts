import apiClient from './client';

export interface ServiceItem {
  id: string;
  name: string;
  category: string;
  subcategory: string;
  sub_subcategory?: string | null;
  base_price: number;
  final_price?: number | null;
  surge_pct?: number | null;
  discount_pct?: number | null;
  duration_minutes: number;
  description?: string;
  status: string;
  image_url?: string;
  includes?: string[];
  excludes?: string[];
  faqs?: Array<{ question: string; answer: string }>;
  features?: string[];
  warranty?: string;
}

export const catalogApi = {
  getAllServices: async (params?: { category?: string; subcategory?: string; search?: string }): Promise<ServiceItem[]> => {
    try {
      const res = await apiClient.get<{ items: ServiceItem[] }>('/services/', { params });
      if (res.data && res.data.items) {
        return res.data.items;
      }
      if (Array.isArray(res.data)) {
        return res.data;
      }
    } catch (e) {
      // Fallback
      const res = await apiClient.get<ServiceItem[]>('/admin/catalog/services', { params });
      return res.data;
    }
    return [];
  },

  getServiceById: async (id: string): Promise<ServiceItem> => {
    try {
      const res = await apiClient.get<ServiceItem>(`/services/${id}`);
      return res.data;
    } catch (e) {
      const res = await apiClient.get<ServiceItem>(`/admin/catalog/services/${id}`);
      return res.data;
    }
  },

  getCategories: async (): Promise<string[]> => {
    try {
      const res = await apiClient.get<Array<{ category: string }>>('/services/categories');
      if (Array.isArray(res.data)) {
        const names = res.data.map((c) => (typeof c === 'string' ? c : c.category)).filter(Boolean);
        return Array.from(new Set(names));
      }
    } catch (e) {
      // Fallback
    }

    // Default static full list of SmartServe categories
    return [
      '1. Beauty, Salon & Spa',
      '2. Cleaning & Home Cleaning',
      '3. Painting, Waterproofing & Home Improvement',
      '4. AC, Appliance & Electronics Repair',
      '5. Electrician, Plumber, Carpenter & Home Repairs',
      '6. Smart Home & Security',
      '7. Domestic Help & Cooking',
      '8. Education, Teachers & Coaching',
      '9. Health, Fitness & Wellness',
      '10. Events, Photography & Entertainment',
      '11. Pet Services',
      '12. Technology & Digital Services',
      '13. Professional & Business Services',
      '14. Moving, Delivery & Local Assistance',
    ];
  },
};
