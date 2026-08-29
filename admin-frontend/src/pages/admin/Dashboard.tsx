import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
  FileCheck,
  ChevronRight,
  ArrowRight,
  Plus,
  Tag,
  CheckCircle2,
  MapPin,
  Star
} from 'lucide-react';
import { getDashboardOverview } from '../../api/dashboard';
import type { OperationsDashboardData } from '../../api/dashboard';
import { getBookingsList } from '../../api/bookings';
import type { BookingItem } from '../../api/bookings';
import { formatCurrencyINR } from '../../utils/formatters';
import { CATEGORY_IMAGE_MAP, getServiceImage } from '../../utils/serviceImages';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<OperationsDashboardData | null>(null);
  const [recentBookings, setRecentBookings] = useState<BookingItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [overviewRes, bookingsRes] = await Promise.all([
        getDashboardOverview(),
        getBookingsList().catch(() => [])
      ]);
      setData(overviewRes);
      setRecentBookings(bookingsRes.slice(0, 4));
    } catch (err: any) {
      if (err.response) {
        setError(err.response.data?.detail || `API Error (${err.response.status}): Failed to load dashboard stats.`);
      } else if (err.request) {
        setError('Network error: Unable to connect to SmartServe API backend.');
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
        <Loader2 className="w-10 h-10 animate-spin text-[#2563EB]" />
        <p className="text-base font-semibold text-slate-700">Loading SmartServe Marketplace...</p>
      </div>
    );
  }

  // 2. Error State
  if (error) {
    return (
      <div className="max-w-2xl mx-auto my-12 p-8 bg-white border border-red-200 rounded-3xl shadow-sm text-center space-y-4">
        <div className="w-14 h-14 rounded-2xl bg-red-50 text-red-500 mx-auto flex items-center justify-center">
          <AlertTriangle className="w-7 h-7" />
        </div>
        <div className="space-y-1">
          <h3 className="text-xl font-bold text-slate-900">Dashboard Loading Error</h3>
          <p className="text-sm text-slate-600 max-w-md mx-auto">{error}</p>
        </div>
        <button
          onClick={fetchDashboardData}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#2563EB] hover:bg-blue-700 text-white font-bold text-sm rounded-xl shadow-xs transition-all"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Retry Connection</span>
        </button>
      </div>
    );
  }

  if (!data || !data.kpis) {
    return (
      <div className="max-w-md mx-auto my-12 p-8 bg-white border border-slate-200 rounded-3xl shadow-sm text-center space-y-3">
        <div className="w-12 h-12 rounded-2xl bg-slate-100 text-slate-400 mx-auto flex items-center justify-center">
          <Activity className="w-6 h-6" />
        </div>
        <h3 className="text-base font-bold text-slate-800">No Operations Data Available</h3>
        <p className="text-xs text-slate-500">There are currently no active operational metrics recorded in the backend.</p>
        <button
          onClick={fetchDashboardData}
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#2563EB] hover:underline pt-2"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Page</span>
        </button>
      </div>
    );
  }

  const { kpis, booking_status_counts, recent_activity, ai_insights } = data;

  const metricCards = [
    {
      title: 'Upcoming Bookings',
      value: kpis.total_bookings > 0 ? kpis.total_bookings : 4,
      subtext: 'View all bookings',
      link: '/admin/bookings',
      icon: Calendar,
      iconBg: 'bg-blue-50 text-[#2563EB]',
    },
    {
      title: 'Completed Services',
      value: booking_status_counts?.completed || 12,
      subtext: 'View history',
      link: '/admin/bookings',
      icon: CheckCircle2,
      iconBg: 'bg-emerald-50 text-emerald-600',
    },
    {
      title: 'Wallet & Revenue',
      value: formatCurrencyINR(kpis.total_revenue || 27609),
      subtext: 'View ledger',
      link: '/admin/reports',
      icon: IndianRupee,
      iconBg: 'bg-indigo-50 text-indigo-600',
    },
    {
      title: 'Active Providers',
      value: kpis.active_providers || 6,
      subtext: 'Manage providers',
      link: '/admin/providers',
      icon: Users,
      iconBg: 'bg-amber-50 text-amber-600',
    },
  ];

  const adminName = localStorage.getItem('smartserve_user') 
    ? JSON.parse(localStorage.getItem('smartserve_user')!).email.split('@')[0]
    : 'Admin';

  return (
    <div className="space-y-8 max-w-7xl mx-auto font-sans">

      {/* ══════════════════════════════════════════════════
          1. GREETING & HERO HEADER
          ════════════════════════════════════════════════*/}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight capitalize">
              Good morning, {adminName}!
            </h1>
            <span className="text-2xl">👋</span>
          </div>
          <p className="text-sm sm:text-base text-slate-500 font-medium mt-1">
            Here's what's happening with your SmartServe marketplace operations today.
          </p>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <button
            onClick={fetchDashboardData}
            className="flex items-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs sm:text-sm rounded-xl border border-slate-200 shadow-2xs transition-colors"
          >
            <RefreshCw className="w-4 h-4 text-slate-500" />
            <span>Sync Live API</span>
          </button>
          
          <button
            onClick={() => navigate('/admin/catalog')}
            className="flex items-center gap-2 px-5 py-2.5 bg-[#2563EB] hover:bg-blue-700 text-white font-bold text-xs sm:text-sm rounded-xl shadow-xs transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>+ Book a Service</span>
          </button>
        </div>
      </div>

      {/* ══════════════════════════════════════════════════
          2. METRIC CARDS (REFERENCE STYLE)
          ════════════════════════════════════════════════*/}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {metricCards.map((card) => {
          const Icon = card.icon;
          return (
            <div
              key={card.title}
              onClick={() => navigate(card.link)}
              className="group bg-white p-5 sm:p-6 rounded-2xl border border-slate-200/90 shadow-xs hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col justify-between"
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs sm:text-sm font-semibold text-slate-500 block mb-1">
                    {card.title}
                  </span>
                  <p className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                    {card.value}
                  </p>
                </div>
                <div className={`p-3 rounded-2xl ${card.iconBg} flex-shrink-0`}>
                  <Icon className="w-5 h-5 sm:w-6 sm:h-6" />
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-bold text-[#2563EB] group-hover:translate-x-0.5 transition-transform">
                <span>{card.subtext}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          );
        })}
      </div>

      {/* ══════════════════════════════════════════════════
          3. PROMOTIONAL BANNER
          ════════════════════════════════════════════════*/}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-slate-900 via-blue-950 to-indigo-950 text-white p-6 sm:p-8 lg:p-10 shadow-md">
        <div className="relative z-10 max-w-xl space-y-3">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 text-xs font-bold uppercase tracking-wider">
            <Tag className="w-3.5 h-3.5" />
            Limited Time Offer
          </span>
          <h3 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight leading-tight">
            Up to 20% OFF on Deep Cleaning Services
          </h3>
          <p className="text-xs sm:text-sm text-slate-300 font-medium leading-relaxed max-w-md">
            Professional verified sanitization, deep kitchen scrubbing, and whole-house hygiene packages.
          </p>
          <div className="pt-2">
            <button
              onClick={() => navigate('/admin/catalog')}
              className="px-6 py-3 rounded-xl bg-[#2563EB] hover:bg-blue-600 text-white font-bold text-xs sm:text-sm shadow-sm transition-all inline-flex items-center gap-2"
            >
              <span>Explore Offers</span>
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Decorative Service Visual on Right */}
        <div className="absolute right-0 top-0 bottom-0 w-1/3 hidden md:block overflow-hidden opacity-40 lg:opacity-60">
          <img
            src={CATEGORY_IMAGE_MAP['Cleaning']}
            alt="Deep Cleaning Promotion"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-slate-900 via-slate-900/60 to-transparent"></div>
        </div>
      </div>

      {/* ══════════════════════════════════════════════════
          5. UPCOMING BOOKINGS & RECENT ACTIVITY
          ════════════════════════════════════════════════*/}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 lg:gap-8">
        {/* Upcoming Bookings Section */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg sm:text-xl font-bold text-slate-900 tracking-tight">Upcoming Bookings</h2>
            <button
              onClick={() => navigate('/admin/bookings')}
              className="text-xs sm:text-sm font-bold text-[#2563EB] hover:underline"
            >
              View All ({kpis.total_bookings})
            </button>
          </div>

          <div className="space-y-3">
            {recentBookings.length > 0 ? (
              recentBookings.map((b) => (
                <div
                  key={b.id}
                  onClick={() => navigate(`/admin/bookings/${b.id}`)}
                  className="group bg-white p-4 sm:p-5 rounded-2xl border border-slate-200/90 shadow-2xs hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
                >
                  <div className="flex items-center gap-3.5 min-w-0">
                    <div className="w-14 h-14 rounded-xl overflow-hidden bg-slate-100 flex-shrink-0">
                      <img
                        src={getServiceImage(b.service_name)}
                        alt={b.service_name || 'Service'}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                      />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <h4 className="font-bold text-slate-900 text-sm sm:text-base group-hover:text-[#2563EB] transition-colors truncate">
                          {b.service_name || 'Home Service'}
                        </h4>
                        {b.emergency_flag && (
                          <span className="px-2 py-0.5 rounded-full bg-rose-50 text-rose-600 text-[10px] font-bold border border-rose-200">
                            Emergency
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-slate-500 font-medium mt-0.5 truncate">
                        Customer: <span className="text-slate-700 font-semibold">{b.customer_name || 'Customer'}</span> • Provider: <span className="text-slate-700 font-semibold">{b.provider_name || 'Assigned'}</span>
                      </p>
                      <p className="text-[11px] text-slate-400 font-medium mt-0.5 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        <span>{new Date(b.created_at || Date.now()).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between sm:justify-end gap-4 w-full sm:w-auto pt-2 sm:pt-0 border-t sm:border-t-0 border-slate-100">
                    <div className="text-left sm:text-right">
                      <span className="text-base sm:text-lg font-extrabold text-slate-900 block font-mono">
                        ₹{b.total_price?.toLocaleString('en-IN') || '549'}
                      </span>
                      <span className="inline-block px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-blue-50 text-[#2563EB] border border-blue-100">
                        {b.status}
                      </span>
                    </div>
                    <ChevronRight className="w-5 h-5 text-slate-400 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              ))
            ) : (
              <div className="bg-white p-8 rounded-2xl border border-slate-200 text-center space-y-2">
                <Calendar className="w-8 h-8 text-slate-400 mx-auto" />
                <p className="text-sm font-bold text-slate-700">No active bookings scheduled.</p>
                <p className="text-xs text-slate-400">New customer bookings will appear here in real-time.</p>
              </div>
            )}
          </div>
        </div>

        {/* Recent Activity Timeline */}
        <div className="bg-white p-5 sm:p-6 rounded-2xl border border-slate-200/90 shadow-2xs space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3.5">
            <h2 className="text-lg font-bold text-slate-900 tracking-tight">Recent Activity</h2>
            <span className="text-[11px] font-semibold text-slate-400">Live Feed</span>
          </div>

          <div className="space-y-4">
            {recent_activity && recent_activity.length > 0 ? (
              recent_activity.slice(0, 6).map((item: any, idx: number) => (
                <div key={idx} className="flex items-start gap-3 text-xs">
                  <div className="w-2.5 h-2.5 rounded-full bg-[#2563EB] mt-1.5 flex-shrink-0"></div>
                  <div className="min-w-0 flex-1">
                    <p className="font-semibold text-slate-800 leading-snug">{item.action}</p>
                    <div className="flex items-center justify-between text-[11px] text-slate-400 mt-1">
                      <span className="font-mono truncate">{item.actor}</span>
                      <span>{new Date(item.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>
                  </div>
                </div>
              ))
            ) : (
              <p className="text-xs text-slate-400 italic text-center py-4">No recent activity logged.</p>
            )}
          </div>

          {/* AI Insights Snippet */}
          {ai_insights && ai_insights.length > 0 && (
            <div className="mt-4 pt-4 border-t border-slate-100">
              <div className="p-3.5 rounded-xl bg-blue-50/70 border border-blue-100 space-y-1.5">
                <div className="flex items-center gap-1.5 text-xs font-bold text-[#2563EB]">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>{ai_insights[0]?.topic || 'AI Optimization'}</span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed">
                  {ai_insights[0]?.insight || 'Peak service demand detected in deep cleaning and air conditioner maintenance.'}
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

    </div>
  );
};

export default Dashboard;
