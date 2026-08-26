import { apiClient } from './client';

export interface DashboardKPIs {
  total_bookings: number;
  active_providers: number;
  online_providers: number;
  total_revenue: number;
  pending_verifications: number;
  emergency_requests: number;
  open_support_tickets: number;
}

export interface BookingStatusCounts {
  requested: number;
  assigned: number;
  accepted: number;
  started: number;
  completed: number;
  paid: number;
  cancelled: number;
  rejected: number;
  expired: number;
}

export interface RecentActivityItem {
  id: string;
  action: string;
  actor: string;
  timestamp: string;
  risk_level: string;
}

export interface AiInsightItem {
  topic: string;
  insight: string;
  confidence: number;
  recommended_action: string;
}

export interface OperationsDashboardData {
  kpis: DashboardKPIs;
  booking_status_counts: BookingStatusCounts;
  recent_activity: RecentActivityItem[];
  ai_insights: AiInsightItem[];
}

export const getDashboardOverview = async (): Promise<OperationsDashboardData> => {
  const response = await apiClient.get<OperationsDashboardData>('/admin/dashboard/overview');
  return response.data;
};
