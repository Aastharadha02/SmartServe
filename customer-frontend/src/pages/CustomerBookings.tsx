import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { getLocalizedServiceName, getLocalizedStatus } from '../utils/localizedNames';
import { useNavigate } from 'react-router-dom';
import { getCustomerBookings, BookingDetail } from '../api/bookings';
import { formatCurrencyINR } from '../utils/formatters';
import { getServiceImage } from '../utils/serviceImages';
import { Calendar, Clock, ChevronRight, Loader2, Plus, AlertCircle, RefreshCw, KeyRound } from 'lucide-react';
import { subscribeToRealtime } from '../utils/realtime';

export const CustomerBookings: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [bookings, setBookings] = useState<BookingDetail[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');

  const fetchBookings = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCustomerBookings();
      setBookings(data);
    } catch (err: any) {
      if (err.response) {
        setError(err.response.data?.detail || `API Error (${err.response.status}): Failed to fetch bookings.`);
      } else if (err.request) {
        setError('Unable to connect to SmartServe API. Please verify network connectivity and backend server availability.');
      } else {
        setError('An unexpected error occurred while loading your bookings.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();

    let customerId = '';
    let userId = '';
    try {
      const rawUser = localStorage.getItem('smartserve_customer_user');
      if (rawUser) {
        const parsed = JSON.parse(rawUser);
        customerId = parsed.customer_id || '';
        userId = parsed.user_id || '';
      }
    } catch (e) {}

    const channels = ['bookings'];
    if (customerId) channels.push(`customer_${customerId}`);
    if (userId) channels.push(`customer_${userId}`, `user_${userId}`);

    // Real-Time Kafka -> WebSocket Subscription (No Polling Required)
    const unsubscribeWs = subscribeToRealtime(channels, (payload) => {
      const type = payload.type || payload.event_type || payload.event;
      if (
        type === 'BOOKING_CREATED' ||
        type === 'BOOKING_ACCEPTED' ||
        type === 'BOOKING_REJECTED' ||
        type === 'BOOKING_STATUS_UPDATED' ||
        type === 'BOOKING_STARTED' ||
        type === 'BOOKING_COMPLETED' ||
        type === 'booking.created' ||
        type === 'booking.accepted' ||
        type === 'booking.rejected' ||
        type === 'booking.updated' ||
        type === 'booking.started' ||
        type === 'booking.completed'
      ) {
        const targetId = String(payload.booking_id || payload.booking?.id || '').toLowerCase();
        const newStatus = payload.status || payload.booking?.status;
        const newOtp = payload.otp_code || payload.booking?.otp_code;

        if (type === 'BOOKING_CREATED' || type === 'booking.created') {
          if (payload.booking) {
            const newBooking = { ...payload.booking, id: String(payload.booking_id || payload.booking?.id) };
            setBookings((prev) => {
              const exists = prev.some((b) => String(b.id).toLowerCase() === String(newBooking.id).toLowerCase());
              if (exists) return prev;
              return [newBooking, ...prev];
            });
          }
          getCustomerBookings().then((data) => setBookings(data)).catch(() => {});
        } else if (targetId && newStatus) {
          setBookings((prev) =>
            prev.map((b) =>
              String(b.id).toLowerCase() === targetId
                ? {
                    ...b,
                    status: newStatus,
                    ...(newOtp ? { otp_code: newOtp } : {}),
                    ...(payload.reason ? { cancellation_reason: payload.reason, rejection_reason: payload.reason } : {}),
                  }
                : b
            )
          );
          getCustomerBookings().then((data) => setBookings(data)).catch(() => {});
        } else {
          getCustomerBookings().then((data) => setBookings(data)).catch(() => {});
        }
      }
    });

    // Fallback polling interval to guarantee real-time sync even if WebSocket is disconnected
    const fallbackPoll = setInterval(() => {
      getCustomerBookings().then((data) => setBookings(data)).catch(() => {});
    }, 3000);

    return () => {
      unsubscribeWs();
      clearInterval(fallbackPoll);
    };
  }, []);

  const filteredBookings = bookings.filter((b) => {
    if (statusFilter === 'all') return true;
    if (statusFilter === 'bundles') return Boolean(b.customer_notes?.includes('CB-') || b.customer_notes?.includes('Bundle'));
    const st = (b.status || '').toLowerCase().replace(/_/g, ' ').trim();
    if (statusFilter === 'active') return ['requested', 'assigned', 'accepted', 'on the way', 'arrived', 'started'].includes(st);
    if (statusFilter === 'completed') return ['completed', 'paid'].includes(st);
    if (statusFilter === 'cancelled') return ['cancelled', 'rejected'].includes(st);
    return true;
  });

  const bundleCount = bookings.filter((b) => b.customer_notes?.includes('CB-') || b.customer_notes?.includes('Bundle')).length;

  return (
    <div className="space-y-8 font-sans max-w-5xl mx-auto">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">{t("nav.bookings", { defaultValue: "My Service Bookings" })}</h1>
          <p className="text-sm text-slate-500 font-medium mt-1">
            {t("booking.bookings_subtitle", { defaultValue: "Track real-time status and technician assignments for your bookings." })}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchBookings}
            className="flex items-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs rounded-xl border border-slate-200 shadow-2xs transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-400" />
            <span>{t("common.sync_live", { defaultValue: "Sync Live" })}</span>
          </button>
          
          <button
            onClick={() => navigate('/catalog')}
            className="flex items-center gap-2 px-5 py-2.5 bg-[#2563EB] hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>{t("common.book_new", { defaultValue: "+ Book New Service" })}</span>
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3 flex-wrap">
        {[
          { key: 'all', label: t('common.all_count', { count: bookings.length, defaultValue: `All (${bookings.length})` }) },
          { key: 'active', label: t('common.active', { defaultValue: 'Active & In-Progress' }) },
          { key: 'bundles', label: `✨ Bundles (${bundleCount})` },
          { key: 'completed', label: t('common.completed', { defaultValue: 'Completed' }) },
          { key: 'cancelled', label: t('common.cancelled', { defaultValue: 'Cancelled' }) },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setStatusFilter(tab.key)}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              statusFilter === tab.key
                ? 'bg-blue-50 text-[#2563EB] border border-blue-200'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Error View */}
      {error && (
        <div className="p-8 bg-white border border-red-200 rounded-3xl text-center space-y-3 shadow-sm">
          <AlertCircle className="w-10 h-10 text-rose-500 mx-auto" />
          <h3 className="text-base font-bold text-slate-900">{t('booking.failed_to_load_bookings', { defaultValue: 'Failed to Load Bookings' })}</h3>
          <p className="text-xs text-slate-600 max-w-md mx-auto">{error}</p>
          <button
            onClick={fetchBookings}
            className="px-4 py-2 bg-[#2563EB] text-white text-xs font-bold rounded-xl inline-flex items-center gap-2"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>{t('booking.retry_connection', { defaultValue: 'Retry Connection' })}</span>
          </button>
        </div>
      )}

      {/* Bookings List */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-16 space-y-3">
          <Loader2 className="w-10 h-10 animate-spin text-[#2563EB]" />
          <p className="text-sm font-semibold text-slate-600">{t("booking.fetching_bookings", { defaultValue: "Fetching your bookings from database..." })}</p>
        </div>
      ) : filteredBookings.length > 0 ? (
        <div className="space-y-4">
          {filteredBookings.map((b) => {
            const imgUrl = getServiceImage(b.category, undefined, b.service_name);
            const stLower = b.status.toLowerCase();
            return (
              <div
                key={b.id}
                onClick={() => navigate(`/bookings/${b.id}`)}
                className="group bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/90 shadow-2xs hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div className="flex items-center gap-4 min-w-0">
                  <div className="w-16 h-16 rounded-2xl overflow-hidden bg-slate-100 flex-shrink-0">
                    <img
                      src={imgUrl}
                      alt={b.service_name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                    />
                  </div>

                  <div className="min-w-0 space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="font-mono text-xs font-bold text-slate-500">{b.booking_reference}</span>
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                        stLower === 'completed' || stLower === 'paid'
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : stLower === 'cancelled' || stLower === 'rejected'
                          ? 'bg-rose-50 text-rose-700 border-rose-200'
                          : 'bg-blue-50 text-[#2563EB] border-blue-200'
                      }`}>
                        {getLocalizedStatus(b.status)}
                      </span>
                      {(b.customer_notes?.includes('CB-') || b.customer_notes?.includes('Bundle')) && (
                        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200 flex items-center gap-1">
                          <span>✨</span> Multi-Service Bundle
                        </span>
                      )}
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                        (b.payment_status || '').toLowerCase() === 'paid'
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : (b.payment_status || '').toLowerCase() === 'collection reported'
                          ? 'bg-amber-50 text-amber-700 border-amber-200'
                          : (b.payment_status || '').toLowerCase() === 'rejected'
                          ? 'bg-rose-50 text-rose-700 border-rose-200'
                          : 'bg-slate-100 text-slate-600 border-slate-200'
                      }`}>
                        COD: {b.payment_status || 'Pending'}
                      </span>
                    </div>

                    <h3 className="font-extrabold text-slate-900 text-base truncate group-hover:text-[#2563EB] transition-colors">
                      {getLocalizedServiceName(b.service_name)}
                    </h3>

                    <div className="flex items-center gap-4 text-xs text-slate-500 font-medium">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        <span>
                          {t('booking.date_at_time', {
                            date: b.scheduled_date,
                            time: b.scheduled_time,
                            defaultValue: `${b.scheduled_date} at ${b.scheduled_time}`
                          })}
                        </span>
                      </span>
                      <span>• {t("booking.provider_label", { defaultValue: "Provider" })}: <strong className="text-slate-700">{b.provider_name || t("booking.assigned_soon", { defaultValue: "Assigned Soon" })}</strong></span>
                    </div>

                    {(b.start_otp || b.otp_code) && ['requested', 'assigned', 'accepted', 'on the way', 'arrived'].includes(stLower) && (
                      <div className="flex items-center gap-1.5 px-2.5 py-1 bg-amber-50 text-amber-800 border border-amber-300 rounded-lg text-xs font-bold w-fit mt-1">
                        <KeyRound className="w-3.5 h-3.5" />
                        <span>{t("booking.start_otp_display", { otp: b.start_otp || b.otp_code, defaultValue: `Start OTP: ${b.start_otp || b.otp_code}` })}</span>
                      </div>
                    )}

                    {b.completion_otp && stLower === 'started' && (
                      <div className="flex items-center gap-1.5 px-2.5 py-1 bg-emerald-50 text-emerald-800 border border-emerald-300 rounded-lg text-xs font-bold w-fit mt-1">
                        <KeyRound className="w-3.5 h-3.5" />
                        <span>Completion OTP: {b.completion_otp}</span>
                      </div>
                    )}

                    {(b.cancellation_reason || (b as any).rejection_reason) && (
                      <div className="text-xs text-rose-700 bg-rose-50 px-2.5 py-1 rounded-lg border border-rose-200 mt-1 inline-block">
                        <strong>{t("booking.reason_label", { defaultValue: "Reason" })}:</strong> {b.cancellation_reason || (b as any).rejection_reason}
                      </div>
                    )}
                  </div>
                </div>

                <div className="flex items-center justify-between sm:justify-end gap-5 w-full sm:w-auto pt-3 sm:pt-0 border-t sm:border-t-0 border-slate-100">
                  <div className="text-left sm:text-right">
                    <span className="text-lg font-extrabold text-slate-900 font-mono block">
                      {formatCurrencyINR(b.total_price || b.total_amount || 0)}
                    </span>
                    <span className="text-[11px] font-semibold text-slate-400 block">{t("common.tap_to_view", { defaultValue: "Tap to view detail" })}</span>
                  </div>
                  <ChevronRight className="w-5 h-5 text-slate-400 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-white p-12 rounded-3xl border border-slate-200 text-center space-y-4">
          <Calendar className="w-12 h-12 text-slate-400 mx-auto" />
          <div className="space-y-1">
            <h3 className="text-base font-bold text-slate-800">{t("common.no_bookings", { defaultValue: "No Bookings Found" })}</h3>
            <p className="text-xs text-slate-500">{t("common.no_bookings_desc", { defaultValue: "You have no active or completed service bookings recorded." })}</p>
          </div>
          <button
            onClick={() => navigate('/catalog')}
            className="px-5 py-2.5 bg-[#2563EB] text-white font-bold text-xs rounded-xl inline-flex items-center gap-2 shadow-xs"
          >
            <Plus className="w-4 h-4" />
            <span>{t("common.book_first", { defaultValue: "Book Your First Service" })}</span>
          </button>
        </div>
      )}

    </div>
  );
};

export default CustomerBookings;
