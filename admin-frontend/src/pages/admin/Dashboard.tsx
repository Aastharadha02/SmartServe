import React, { useEffect, useState } from 'react';
import { 
  Calendar, 
  Users, 
  IndianRupee, 
  ShieldCheck, 
  AlertTriangle, 
  Activity, 
  Sparkles, 
  Loader2, 
  RefreshCw, 
  Clock, 
  TrendingUp,
  FileCheck
} from 'lucide-react';
import { getDashboardOverview } from '../../api/dashboard';
import type { OperationsDashboardData } from '../../api/dashboard';
import { formatCurrencyINR } from '../../utils/formatters';

export const Dashboard: React.FC = () => {
  const [data, setData] = useState<OperationsDashboardData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await getDashboardOverview();
      setData(res);
    } catch (err: any) {
      if (err.response) {
        setError(err.response.data?.detail || `API Error (${err.response.status}): Failed to load dashboard stats.`);
      } else if (err.request) {
        setError('Network error: Unable to connect to SmartServe API. Ensure FastAPI server is running on port 8000.');
      } else {
        setError('An unexpected error occurred while loading dashboard metrics.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  // 1. Loading State
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-4">
        <Loader2 className="w-8 h-8 animate-spin text-[#5CA8FF]" />
        <p className="text-sm font-medium text-slate-600">Connecting to SmartServe API Engine...</p>
      </div>
    );
  }

  // 2. Error State
  if (error) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-6 bg-white border border-red-200 rounded-2xl shadow-sm text-center space-y-4">
        <div className="w-12 h-12 rounded-2xl bg-red-50 text-red-500 mx-auto flex items-center justify-center">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <div className="space-y-1">
          <h3 className="text-lg font-bold text-slate-900">Dashboard Loading Error</h3>
          <p className="text-sm text-slate-600 max-w-md mx-auto">{error}</p>
        </div>
        <button
          onClick={fetchDashboardData}
          className="inline-flex items-center gap-2 px-4 py-2 bg-[#5CA8FF] hover:bg-blue-600 text-white font-semibold text-sm rounded-xl shadow-sm transition-all"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Retry Connection</span>
        </button>
      </div>
    );
  }

  // 3. Empty State (No Data returned)
  if (!data || !data.kpis) {
    return (
      <div className="max-w-md mx-auto my-12 p-8 bg-white border border-slate-200 rounded-2xl shadow-sm text-center space-y-3">
        <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 mx-auto flex items-center justify-center">
          <Activity className="w-6 h-6" />
        </div>
        <h3 className="text-base font-bold text-slate-800">No Operations Data Available</h3>
        <p className="text-xs text-slate-500">There are currently no active operational metrics recorded in the backend.</p>
        <button
          onClick={fetchDashboardData}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#5CA8FF] hover:underline pt-2"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Page</span>
        </button>
      </div>
    );
  }

  // 4. Success State (Real Backend Metrics Rendering)
  const { kpis, booking_status_counts, recent_activity, ai_insights } = data;

  const kpiCards = [
    {
      title: 'Total Revenue',
      value: formatCurrencyINR(kpis.total_revenue),
      icon: IndianRupee,
      color: 'bg-emerald-50 text-emerald-600',
      border: 'border-emerald-100',
    },
    {
      title: 'Total Bookings',
      value: kpis.total_bookings,
      icon: Calendar,
      color: 'bg-blue-50 text-[#5CA8FF]',
      border: 'border-blue-100',
    },
    {
      title: 'Active Providers',
      value: kpis.active_providers,
      icon: Users,
      color: 'bg-indigo-50 text-indigo-600',
      border: 'border-indigo-100',
    },
    {
      title: 'Pending Verifications',
      value: kpis.pending_verifications,
      icon: FileCheck,
      color: 'bg-amber-50 text-amber-600',
      border: 'border-amber-100',
    },
    {
      title: 'Emergency Requests',
      value: kpis.emergency_requests,
      icon: AlertTriangle,
      color: 'bg-rose-50 text-rose-600',
      border: 'border-rose-100',
    },
    {
      title: 'Open Support Tickets',
      value: kpis.open_support_tickets,
      icon: Clock,
      color: 'bg-purple-50 text-purple-600',
      border: 'border-purple-100',
    },
  ];

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h2 className="text-xl font-bold text-slate-900 tracking-tight">Operations Intelligence Overview</h2>
          <p className="text-xs text-slate-500 font-medium mt-0.5">
            Real-time analytics and system health metrics from Neon Cloud PostgreSQL
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={fetchDashboardData}
            className="flex items-center gap-2 px-3.5 py-2 bg-slate-50 hover:bg-slate-100 text-slate-700 font-medium text-xs rounded-xl border border-slate-200 transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Sync Live API</span>
          </button>
          <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-200">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            Live Backend Connected
          </span>
        </div>
      </div>

      {/* KPI Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {kpiCards.map((kpi) => {
          const Icon = kpi.icon;
          return (
            <div
              key={kpi.title}
              className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm hover:shadow transition-shadow flex flex-col justify-between"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-500">{kpi.title}</span>
                <div className={`p-2 rounded-xl ${kpi.color}`}>
                  <Icon className="w-4 h-4" />
                </div>
              </div>
              <div className="mt-4">
                <p className="text-2xl font-bold text-slate-900 tracking-tight">{kpi.value}</p>
              </div>
            </div>
          );
        })}
      </div>

      {/* Two Column Layout: Status Breakdown & AI Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Booking Status Breakdown */}
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-5">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base">Booking Lifecycle Status Breakdown</h3>
              <p className="text-xs text-slate-500 font-medium">State machine count metrics across all 9 lifecycle states</p>
            </div>
            <span className="text-xs font-semibold text-[#5CA8FF] bg-blue-50 px-2.5 py-1 rounded-lg">
              {kpis.total_bookings} Total
            </span>
          </div>

          <div className="grid grid-cols-3 gap-4">
            {Object.entries(booking_status_counts).map(([statusKey, count]) => (
              <div key={statusKey} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between">
                <div>
                  <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">{statusKey}</p>
                  <p className="text-xl font-bold text-slate-900 mt-0.5">{count}</p>
                </div>
                <div className="w-2.5 h-2.5 rounded-full bg-[#5CA8FF]"></div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Insights Card */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-5 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2">
                <div className="p-1.5 rounded-lg bg-blue-50 text-[#5CA8FF]">
                  <Sparkles className="w-4 h-4" />
                </div>
                <h3 className="font-bold text-slate-900 text-base">AI OpenRouter Insights</h3>
              </div>
              <span className="text-[10px] font-mono font-semibold bg-slate-100 text-slate-600 px-2 py-0.5 rounded">
                LIVE MODEL
              </span>
            </div>

            {ai_insights && ai_insights.length > 0 ? (
              <div className="space-y-3">
                {ai_insights.map((item: any, idx: number) => (
                  <div key={idx} className="p-4 rounded-xl bg-blue-50/50 border border-blue-100 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-xs font-bold text-slate-900">{item.topic}</span>
                      <span className="text-[10px] font-semibold text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">
                        {Math.round(item.confidence * 100)}% Match
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">{item.insight}</p>
                    <div className="text-[11px] font-medium text-[#5CA8FF] pt-1 flex items-center gap-1">
                      <TrendingUp className="w-3 h-3" />
                      <span>{item.recommended_action}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-slate-400 italic">No AI insights generated yet.</p>
            )}
          </div>

          <div className="pt-3 border-t border-slate-100 text-[11px] text-slate-400 text-center">
            Powered by OpenRouter LLM Diagnostic Gateway
          </div>
        </div>
      </div>

      {/* Security Activity Feed */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-[#5CA8FF]" />
            <h3 className="font-bold text-slate-900 text-base">Recent Audit & Security Log Feed</h3>
          </div>
          <span className="text-xs font-semibold text-slate-500">Immutable Ledger</span>
        </div>

        {recent_activity && recent_activity.length > 0 ? (
          <div className="divide-[#100] divide-y">
            {recent_activity.map((log: any) => (
              <div key={log.id} className="py-3 flex items-center justify-between text-xs">
                <div className="flex items-center gap-3">
                  <span className={`w-2 h-2 rounded-full ${log.risk_level === 'Warning' ? 'bg-amber-500' : 'bg-emerald-500'}`}></span>
                  <div>
                    <p className="font-semibold text-slate-800">{log.action}</p>
                    <p className="text-slate-400 font-mono text-[11px]">{log.actor}</p>
                  </div>
                </div>
                <div className="text-right text-slate-400 font-mono text-[11px]">
                  {new Date(log.timestamp).toLocaleString()}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-slate-400 italic text-center py-4">No recent security audit logs recorded.</p>
        )}
      </div>
    </div>
  );
};
