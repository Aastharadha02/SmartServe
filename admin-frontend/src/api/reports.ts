import { apiClient } from './client';

export interface DailyTrendItem {
  day: string;
  revenue: number;
  bookings: number;
}

export interface AIInsightItem {
  title: string;
  confidence_score: number;
  recommendation: string;
  timestamp: string;
}

export interface AggregatePeriodReportItem {
  period: string;
  total_revenue: number;
  period_revenue: number;
  total_bookings: number;
  completed_bookings: number;
  cancelled_bookings: number;
  in_progress_bookings: number;
  completion_rate: number;
  cancellation_rate: number;
  average_booking_value: number;
  new_customers: number;
  daily_trend: DailyTrendItem[];
  ai_insight?: AIInsightItem | null;
}

export interface ProviderPerformanceReportItem {
  provider_id: string;
  provider_name: string;
  total_jobs: number;
  completed_jobs: number;
  completion_rate: number;
  reliability_score: number;
  earnings: number;
  rating: number;
}

export interface ServiceDemandReportItem {
  category: string;
  service_name: string;
  booking_count: number;
  total_revenue: number;
  demand_trend?: string | null;
}

export const getPeriodSummaryReport = async (period: string = '30days'): Promise<AggregatePeriodReportItem> => {
  const response = await apiClient.get<AggregatePeriodReportItem>(`/admin/reports/summary?period=${period}`);
  return response.data;
};

export const getProviderPerformanceReport = async (): Promise<ProviderPerformanceReportItem[]> => {
  const response = await apiClient.get<ProviderPerformanceReportItem[]>('/admin/reports/provider-performance');
  return response.data;
};

export const getServiceDemandReport = async (): Promise<ServiceDemandReportItem[]> => {
  const response = await apiClient.get<ServiceDemandReportItem[]>('/admin/reports/service-demand');
  return response.data;
};

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

export const downloadExcelReport = async (): Promise<void> => {
  const token = localStorage.getItem('smartserve_token');
  const response = await fetch(`${API_BASE_URL}/admin/reports/export/excel`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'SmartServe_Revenue_Report.xlsx';
  document.body.appendChild(a);
  a.click();
  a.remove();
};

export const downloadPdfReport = async (): Promise<void> => {
  const token = localStorage.getItem('smartserve_token');
  const response = await fetch(`${API_BASE_URL}/admin/reports/export/pdf`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const blob = await response.blob();
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'SmartServe_Executive_Report.pdf';
  document.body.appendChild(a);
  a.click();
  a.remove();
};

