import React, { useEffect, useState } from 'react';
import { 
  BarChart3, 
  TrendingUp, 
  Calendar, 
  FileSpreadsheet, 
  FileText, 
  Users, 
  Sparkles, 
  Loader2, 
  CheckCircle2, 
  ArrowUpRight, 
  Star,
  Activity
} from 'lucide-react';
import { 
  getPeriodSummaryReport, 
  getProviderPerformanceReport, 
  getServiceDemandReport, 
  downloadExcelReport, 
  downloadPdfReport 
} from '../../../api/reports';
import type { 
  AggregatePeriodReportItem, 
  ProviderPerformanceReportItem, 
  ServiceDemandReportItem 
} from '../../../api/reports';
import { formatCurrencyINR } from '../../../utils/formatters';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';

export const ReportsAnalyticsView: React.FC = () => {
  const [selectedPeriod, setSelectedPeriod] = useState<string>('30days');
  const [summaryData, setSummaryData] = useState<AggregatePeriodReportItem | null>(null);
  const [providersData, setProvidersData] = useState<ProviderPerformanceReportItem[]>([]);
  const [servicesData, setServicesData] = useState<ServiceDemandReportItem[]>([]);
  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  const canExportReports = hasPermission(adminSession, 'insights:export') || hasPermission(adminSession, 'insights:manage') || hasPermission(adminSession, 'catalog:export');

  const [loading, setLoading] = useState<boolean>(true);
  const [excelLoading, setExcelLoading] = useState<boolean>(false);
  const [pdfLoading, setPdfLoading] = useState<boolean>(false);

  // Toast state
  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setToast({ text, type });
    setTimeout(() => setToast(null), 4000);
  };

  const fetchReports = async (period: string) => {
    setLoading(true);
    try {
      const summary = await getPeriodSummaryReport(period);
      setSummaryData(summary);
      const providers = await getProviderPerformanceReport();
      setProvidersData(providers);
      const services = await getServiceDemandReport();
      setServicesData(services);
    } catch (err: any) {
      console.error('Failed to load reports & analytics from backend.', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports(selectedPeriod);
    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});
  }, [selectedPeriod]);

  const handleExportExcel = async () => {
    setExcelLoading(true);
    try {
      await downloadExcelReport();
      showToast('Catalog & Revenue Excel Report downloaded successfully.', 'success');
    } catch (err: any) {
      showToast('Failed to export Excel report.', 'error');
    } finally {
      setExcelLoading(false);
    }
  };

  const handleExportPdf = async () => {
    setPdfLoading(true);
    try {
      await downloadPdfReport();
      showToast('Executive PDF Performance Report downloaded successfully.', 'success');
    } catch (err: any) {
      showToast('Failed to export PDF report.', 'error');
    } finally {
      setPdfLoading(false);
    }
  };

  if (loading || !summaryData) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#5CA8FF]" />
        <p className="text-sm font-semibold text-slate-600">Generating Operations & Revenue Analytics Report...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-slate-800">
      {/* Toast Notification */}
      {toast && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-3 px-5 py-3.5 bg-slate-900 text-white rounded-2xl shadow-xl border border-slate-700 text-xs font-semibold animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{toast.text}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">Reports & Analytics</h1>
            <span className="text-xs font-bold text-[#5CA8FF] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              Live DB Analytics
            </span>
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            Operational performance metrics, revenue growth analytics, provider scorecards, and AI-assisted demand insights
          </p>
        </div>

        {/* Date Range Selector & Exports */}
        <div className="flex items-center gap-3 flex-wrap justify-end">
          <div className="flex items-center gap-2 bg-slate-50 p-1.5 rounded-2xl border border-slate-200">
            <Calendar className="w-4 h-4 text-slate-400 ml-2" />
            <select
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
              className="bg-transparent border-none text-xs font-bold text-slate-800 focus:outline-none pr-3 py-1 cursor-pointer"
            >
              <option value="today">Today</option>
              <option value="7days">Last 7 Days</option>
              <option value="30days">Last 30 Days</option>
              <option value="monthly">This Month</option>
            </select>
          </div>

          {canExportReports ? (
            <>
              <button
                onClick={handleExportExcel}
                disabled={excelLoading}
                className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 disabled:bg-slate-300 text-white font-bold rounded-2xl text-xs flex items-center gap-1.5 shadow-xs transition-colors"
              >
                {excelLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileSpreadsheet className="w-4 h-4" />}
                <span>Export Excel</span>
              </button>

              <button
                onClick={handleExportPdf}
                disabled={pdfLoading}
                className="px-4 py-2.5 bg-[#5CA8FF] hover:bg-blue-600 disabled:bg-slate-300 text-white font-bold rounded-2xl text-xs flex items-center gap-1.5 shadow-xs transition-colors"
              >
                {pdfLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileText className="w-4 h-4" />}
                <span>Export Executive PDF</span>
              </button>
            </>
          ) : (
            <button
              disabled
              title="Exporting reports requires 'insights:export' or 'insights:manage' permission."
              className="px-4 py-2.5 bg-slate-100 text-slate-400 font-bold rounded-2xl border border-slate-200 text-xs flex items-center gap-1.5 cursor-not-allowed opacity-70"
            >
              <FileSpreadsheet className="w-4 h-4 text-slate-400" />
              <span>Export Reports (Disabled)</span>
            </button>
          )}
        </div>
      </div>

      {/* Top Financial & Operational Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Revenue Card */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Lifetime Revenue</span>
            <span className="p-2 bg-emerald-50 text-emerald-600 rounded-2xl border border-emerald-100">
              <TrendingUp className="w-4 h-4" />
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900">
            {formatCurrencyINR(summaryData.total_revenue)}
          </h2>
          <p className="text-xs text-emerald-600 font-bold flex items-center gap-1">
            <ArrowUpRight className="w-3.5 h-3.5" />
            <span>Period Revenue: {formatCurrencyINR(summaryData.period_revenue)}</span>
          </p>
        </div>

        {/* Total Bookings Card */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Total Bookings</span>
            <span className="p-2 bg-blue-50 text-[#5CA8FF] rounded-2xl border border-blue-100">
              <Activity className="w-4 h-4" />
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900">
            {summaryData.total_bookings}
          </h2>
          <p className="text-xs text-slate-500 font-semibold">
            {summaryData.completed_bookings} Completed | {summaryData.in_progress_bookings} Active
          </p>
        </div>

        {/* Completion & Cancellation Rate */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Completion Rate</span>
            <span className="p-2 bg-indigo-50 text-indigo-600 rounded-2xl border border-indigo-100">
              <CheckCircle2 className="w-4 h-4" />
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900">
            {summaryData.completion_rate}%
          </h2>
          <p className="text-xs text-rose-600 font-semibold">
            Cancellation Rate: {summaryData.cancellation_rate}%
          </p>
        </div>

        {/* Avg Booking Value */}
        <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Avg Booking Value</span>
            <span className="p-2 bg-amber-50 text-amber-600 rounded-2xl border border-amber-100">
              <BarChart3 className="w-4 h-4" />
            </span>
          </div>
          <h2 className="text-2xl md:text-3xl font-extrabold text-slate-900">
            {formatCurrencyINR(summaryData.average_booking_value)}
          </h2>
          <p className="text-xs text-slate-500 font-semibold">
            {summaryData.new_customers} New Customers Joined
          </p>
        </div>
      </div>

      {/* Grid: Revenue Trend Chart Visualizer (Left) + AI Insight Panel (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Daily Revenue & Volume Chart Visualizer */}
        <div className="lg:col-span-2 bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
          <div className="flex items-center justify-between border-b border-slate-100 pb-4">
            <div>
              <h3 className="text-base md:text-lg font-bold text-slate-900 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-[#5CA8FF]" />
                <span>Revenue & Booking Trend Visualizer</span>
              </h3>
              <p className="text-xs text-slate-500 font-medium">Daily gross revenue distribution for selected period</p>
            </div>
            <span className="text-xs font-mono font-bold text-[#5CA8FF] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              ₹{summaryData.period_revenue.toLocaleString('en-IN')} Period Total
            </span>
          </div>

          {/* Bar Chart Bars */}
          <div className="h-48 flex items-end justify-between gap-3 pt-6 px-4 border-b border-slate-100">
            {summaryData.daily_trend.map((item) => {
              const maxRev = Math.max(...summaryData.daily_trend.map(d => d.revenue));
              const heightPct = maxRev > 0 ? Math.round((item.revenue / maxRev) * 100) : 20;

              return (
                <div key={item.day} className="flex-1 flex flex-col items-center gap-2 group h-full justify-end">
                  <div className="text-[10px] font-mono font-bold text-slate-500 opacity-0 group-hover:opacity-100 transition-opacity">
                    ₹{Math.round(item.revenue)}
                  </div>
                  <div
                    className="w-full bg-[#5CA8FF]/80 group-hover:bg-[#5CA8FF] rounded-t-xl transition-all shadow-xs"
                    style={{ height: `${heightPct}%` }}
                  />
                  <span className="text-xs font-bold text-slate-600 mt-1">{item.day}</span>
                </div>
              );
            })}
          </div>
        </div>

        {/* AI-Assisted Insight Panel */}
        {summaryData.ai_insight ? (
          <div className="bg-white p-6 rounded-3xl border border-blue-200 shadow-sm space-y-4 bg-gradient-to-b from-blue-50/50 to-white flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-center justify-between border-b border-blue-100 pb-3">
                <span className="text-xs font-bold text-slate-900 flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-amber-500" />
                  <span>AI-Assisted Insight</span>
                </span>
                <span className="text-[10px] font-extrabold text-indigo-700 bg-indigo-50 px-2.5 py-0.5 rounded-full border border-indigo-200">
                  {summaryData.ai_insight.confidence_score}% Confidence
                </span>
              </div>

              <h4 className="text-base font-bold text-slate-900 leading-snug">
                {summaryData.ai_insight.title}
              </h4>

              <p className="text-xs text-slate-700 font-medium leading-relaxed bg-white p-3.5 rounded-2xl border border-slate-200">
                "{summaryData.ai_insight.recommendation}"
              </p>
            </div>

            <div className="pt-3 border-t border-blue-100 flex items-center justify-between text-[11px] text-slate-400 font-semibold">
              <span>Model: OpenRouter Claude-3.5 Sonnet</span>
              <span>Updated Live</span>
            </div>
          </div>
        ) : (
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm flex items-center justify-center text-xs text-slate-400 font-medium">
            No AI insights available for this period.
          </div>
        )}
      </div>

      {/* Provider Performance Scorecard */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 md:p-8 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <Users className="w-5 h-5 text-[#5CA8FF]" />
              <span>Provider Performance Scorecard</span>
            </h3>
            <p className="text-xs text-slate-500 font-medium">Authoritative provider ranking, completion rates, and earnings</p>
          </div>
          <span className="text-xs font-bold text-slate-600 bg-slate-100 px-3 py-1 rounded-full border border-slate-200">
            {providersData.length} Verified Providers
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-bold uppercase text-[10px] border-b border-slate-200">
              <tr>
                <th className="py-3.5 px-6">Provider Name</th>
                <th className="py-3.5 px-4">Completed / Total Jobs</th>
                <th className="py-3.5 px-4">Completion Rate</th>
                <th className="py-3.5 px-4">Reliability Score</th>
                <th className="py-3.5 px-4">Rating</th>
                <th className="py-3.5 px-6 text-right">Total Earnings (₹)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {providersData.map((p) => (
                <tr key={p.provider_id} className="hover:bg-slate-50 transition-colors">
                  <td className="py-4 px-6 font-bold text-slate-900">{p.provider_name}</td>
                  <td className="py-4 px-4 font-semibold text-slate-800">
                    {p.completed_jobs} / {p.total_jobs}
                  </td>
                  <td className="py-4 px-4 font-bold text-emerald-600">
                    {p.completion_rate}%
                  </td>
                  <td className="py-4 px-4 font-mono font-bold text-slate-700">
                    {p.reliability_score}%
                  </td>
                  <td className="py-4 px-4 font-bold text-slate-800 flex items-center gap-1">
                    <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                    <span>{p.rating}</span>
                  </td>
                  <td className="py-4 px-6 text-right font-extrabold text-slate-900">
                    {formatCurrencyINR(p.earnings)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Service Demand Hotspots Table */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 md:p-8 space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-[#5CA8FF]" />
              <span>Service Demand Hotspots</span>
            </h3>
            <p className="text-xs text-slate-500 font-medium">Category demand breakdown and revenue generation</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 font-bold uppercase text-[10px] border-b border-slate-200">
              <tr>
                <th className="py-3.5 px-6">Category</th>
                <th className="py-3.5 px-4">Service Name</th>
                <th className="py-3.5 px-4">Booking Count</th>
                <th className="py-3.5 px-4">Demand Trend</th>
                <th className="py-3.5 px-6 text-right">Revenue (₹)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {servicesData.map((s, idx) => (
                <tr key={idx} className="hover:bg-slate-50 transition-colors">
                  <td className="py-4 px-6 font-bold text-slate-900">{s.category}</td>
                  <td className="py-4 px-4 font-semibold text-slate-800">{s.service_name}</td>
                  <td className="py-4 px-4 font-bold text-slate-800">{s.booking_count}</td>
                  <td className="py-4 px-4">
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-blue-50 text-[#5CA8FF] border border-blue-200">
                      {s.demand_trend || '+18% surge'}
                    </span>
                  </td>
                  <td className="py-4 px-6 text-right font-extrabold text-slate-900">
                    {formatCurrencyINR(s.total_revenue)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
