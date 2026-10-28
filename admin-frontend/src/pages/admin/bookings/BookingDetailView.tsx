import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  CalendarCheck, 
  Siren, 
  Loader2, 
  ArrowLeft, 
  CheckCircle2, 
  ChevronRight,
  User,
  Phone,
  MapPin,
  IndianRupee,
  UserCheck,
  History,
  X,
  RefreshCw,
  AlertTriangle,
  Zap,
  MessageCircle,
  ShieldCheck,
  Camera,
  FileText,
  Eye,
  Banknote,
  ShieldAlert,
  Bell,
  Mail,
} from 'lucide-react';
import { getBookingConversation } from '../../../api/support';
import type { SupportTicketItem } from '../../../api/support';
import { 
  getBookingDetail, 
  updateBookingStatus, 
  reassignBookingProvider,
  getAdminBookingLocation,
  resolveAdminWarrantyClaim,
  getBookingPayments,
  verifyPaymentCollection,
  rejectPaymentCollection,
  getAdminBookingNotifications,
  retryAdminNotification,
  type BookingItem,
  type PaymentRecord,
  type AdminBookingLocationResponse,
  type AdminProviderLocation,
  type AdminNotificationItem,
} from '../../../api/bookings';
import { getProvidersList } from '../../../api/providers';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';
import { subscribeToRealtime } from '../../../utils/realtime';
import { AdminLiveTrackingCard } from '../../../components/AdminLiveTrackingCard';

export const BookingDetailView: React.FC = () => {
  const { bookingId } = useParams<{ bookingId: string }>();
  const navigate = useNavigate();

  const [bookingData, setBookingData] = useState<BookingItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);
  const [liveLocationData, setLiveLocationData] = useState<AdminBookingLocationResponse | null>(null);
  const [liveProviderLocation, setLiveProviderLocation] = useState<AdminProviderLocation | null>(null);
  const [wsConnected, setWsConnected] = useState<boolean>(true);

  // Status Transition Modal State
  const [transitionModalOpen, setTransitionModalOpen] = useState<boolean>(false);
  const [targetNextStatus, setTargetNextStatus] = useState<string>('');
  const [transitionReason, setTransitionReason] = useState<string>('');
  const [transitionLoading, setTransitionLoading] = useState<boolean>(false);

  // Provider Reassignment Modal State
  const [reassignModalOpen, setReassignModalOpen] = useState<boolean>(false);
  const [providerOptions, setProviderOptions] = useState<{ id: string; name: string }[]>([]);
  const [selectedProviderId, setSelectedProviderId] = useState<string>('');
  const [reassignReason, setReassignReason] = useState<string>('Operational optimization dispatch');
  const [reassignLoading, setReassignLoading] = useState<boolean>(false);

  // Chat Audit Modal State
  const [auditModalOpen, setAuditModalOpen] = useState<boolean>(false);
  const [auditLoading, setAuditLoading] = useState<boolean>(false);
  const [auditTicket, setAuditTicket] = useState<SupportTicketItem | null>(null);
  const [auditError, setAuditError] = useState<string | null>(null);

  // Payment Review State
  const [bookingPayments, setBookingPayments] = useState<PaymentRecord[]>([]);
  const [paymentActionLoading, setPaymentActionLoading] = useState<string | null>(null);
  const [rejectPaymentModalOpen, setRejectPaymentModalOpen] = useState<boolean>(false);
  const [targetRejectPaymentId, setTargetRejectPaymentId] = useState<string>('');
  const [rejectPaymentReason, setRejectPaymentReason] = useState<string>('');

  // Notification Monitoring State
  const [adminNotifications, setAdminNotifications] = useState<AdminNotificationItem[]>([]);
  const [retryingNotificationId, setRetryingNotificationId] = useState<string | null>(null);

  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

  // Warranty Audit & Photo Lightbox State
  const [warrantyActionLoading, setWarrantyActionLoading] = useState<boolean>(false);
  const [warrantyResolvingAction, setWarrantyResolvingAction] = useState<'Resolved' | 'Rejected' | null>(null);
  const [warrantyResolveNotes, setWarrantyResolveNotes] = useState<string>('');
  const [previewPhotoUrl, setPreviewPhotoUrl] = useState<string | null>(null);

  const canManageBookings = hasPermission(adminSession, 'bookings:manage');

  const showToast = (text: string, type: 'success' | 'warning' | 'error' = 'success') => {
    setToastMessage({ text, type });
    setTimeout(() => setToastMessage(null), 5000);
  };

  const fetchBookingProfile = async () => {
    if (!bookingId) return;
    setLoading(true);
    setError(null);
    try {
      const [data, payments] = await Promise.all([
        getBookingDetail(bookingId),
        getBookingPayments(bookingId).catch(() => []),
      ]);
      setBookingData(data);
      setBookingPayments(payments || []);
      if (data.allowed_next_statuses && data.allowed_next_statuses.length > 0) {
        setTargetNextStatus(data.allowed_next_statuses[0]);
      }
      fetchLocation();
      if (data && data.booking_reference) {
        getAdminBookingNotifications(data.booking_reference)
          .then(setAdminNotifications)
          .catch(() => []);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load booking details from backend.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyCollection = async (paymentId: string) => {
    setPaymentActionLoading(paymentId);
    try {
      await verifyPaymentCollection(paymentId);
      showToast('Cash collection verified successfully! Booking payment marked as PAID.', 'success');
      await fetchBookingProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to verify payment collection.', 'error');
    } finally {
      setPaymentActionLoading(null);
    }
  };

  const handleRejectCollection = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!targetRejectPaymentId || !rejectPaymentReason.trim()) return;
    setPaymentActionLoading(targetRejectPaymentId);
    try {
      await rejectPaymentCollection(targetRejectPaymentId, rejectPaymentReason.trim());
      showToast('Payment report rejected. Follow-up reason recorded.', 'warning');
      setRejectPaymentModalOpen(false);
      setRejectPaymentReason('');
      await fetchBookingProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to reject payment collection.', 'error');
    } finally {
      setPaymentActionLoading(null);
    }
  };

  const handleRetryNotification = async (notificationId: string) => {
    try {
      setRetryingNotificationId(notificationId);
      const updated = await retryAdminNotification(notificationId);
      setAdminNotifications((prev) => prev.map((n) => (n.id === notificationId ? updated : n)));
      showToast(`Notification retry completed. Status: ${updated.delivery_status}`, updated.delivery_status === 'Sent' ? 'success' : 'warning');
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to retry notification delivery.', 'error');
    } finally {
      setRetryingNotificationId(null);
    }
  };

  const fetchLocation = async () => {
    if (!bookingId) return;
    try {
      const loc = await getAdminBookingLocation(bookingId);
      setLiveLocationData(loc);
      if (loc.provider_location) {
        setLiveProviderLocation(loc.provider_location);
      }
    } catch (e) {
      console.warn('Failed to load admin live location:', e);
    }
  };

  useEffect(() => {
    fetchBookingProfile();

    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});

    getProvidersList().then((provs) => {
      setProviderOptions(provs.map((p) => ({ id: p.user_id, name: p.full_name })));
      if (provs.length > 0) setSelectedProviderId(provs[0].user_id);
    }).catch(() => {});

    if (!bookingId) return;

    const channels = [
      `booking_${bookingId}`,
      `admin_booking_${bookingId}`,
      `booking_chat_${bookingId}`,
      'bookings',
      'dashboard',
      'admin',
      'support_tickets',
      'support'
    ];

    const unsubscribeWs = subscribeToRealtime(
      channels,
      (payload) => {
        const type = payload.type || payload.event_type || payload.event;
        const targetBookingId = String(payload.booking_id || payload.booking?.id || payload.id || '').toLowerCase();
        const currentBookingId = String(bookingId || '').toLowerCase();

        if (targetBookingId && targetBookingId === currentBookingId) {
          if (type === 'PROVIDER_LOCATION_UPDATED' || type === 'provider.location.updated') {
            if (payload.latitude !== undefined && payload.longitude !== undefined) {
              setLiveProviderLocation({
                latitude: Number(payload.latitude),
                longitude: Number(payload.longitude),
                heading: payload.heading !== undefined ? Number(payload.heading) : null,
                speed: payload.speed !== undefined ? Number(payload.speed) : null,
                accuracy: payload.accuracy !== undefined ? Number(payload.accuracy) : null,
                updated_at: payload.updated_at || new Date().toISOString(),
              });
            }
            if (payload.status) {
              setBookingData((prev) => (prev ? { ...prev, status: payload.status } : prev));
            }
          } else if (type === 'BOOKING_ACCEPTED' || type === 'booking.accepted') {
            setBookingData((prev) => (prev ? { ...prev, status: 'Accepted' } : prev));
            fetchLocation();
          } else if (type === 'BOOKING_STATUS_UPDATED' || type === 'booking.updated' || type === 'BOOKING_STARTED' || type === 'BOOKING_COMPLETED') {
            const nextSt = payload.status || payload.booking?.status;
            if (nextSt) {
              setBookingData((prev) => (prev ? { ...prev, status: nextSt } : prev));
              if (['Completed', 'Cancelled', 'Rejected'].includes(nextSt)) {
                setLiveProviderLocation(null);
              }
            }
            fetchLocation();
          } else if (type === 'BOOKING_REJECTED' || type === 'booking.rejected') {
            const reason = payload.reason || payload.rejection_reason || payload.cancellation_reason || 'Rejected by provider';
            setBookingData((prev) =>
              prev ? { ...prev, status: 'Rejected', cancellation_reason: reason } : prev
            );
          }
          if (type !== 'PROVIDER_LOCATION_UPDATED' && type !== 'provider.location.updated') {
            fetchBookingProfile();
          }
        }

        if (type === 'NEW_SUPPORT_MESSAGE' || type === 'support.message') {
          const msg = payload.message || payload.data;
          if (msg && (!payload.booking_id || String(payload.booking_id).toLowerCase() === currentBookingId)) {
            setAuditTicket((prev) => {
              if (!prev) return prev;
              const exists = (prev.messages || []).some((m: any) => String(m.id).toLowerCase() === String(msg.id).toLowerCase());
              if (exists) return prev;
              return {
                ...prev,
                messages: [...(prev.messages || []), msg],
              };
            });
          }
        }
      },
      (status: 'connected' | 'connecting' | 'disconnected') => {
        setWsConnected(status === 'connected');
      }
    );

    const pollInterval = setInterval(() => {
      fetchLocation();
    }, 10000);

    return () => {
      clearInterval(pollInterval);
      unsubscribeWs();
    };
  }, [bookingId]);

  const handleTransitionSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!bookingData || !targetNextStatus) return;
    setTransitionLoading(true);
    try {
      const updated = await updateBookingStatus(bookingData.id, targetNextStatus, transitionReason);
      setBookingData(updated);
      showToast(`Booking status transitioned to ${targetNextStatus} successfully!`, 'success');
      setTransitionModalOpen(false);
      setTransitionReason('');
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'State transition failed.', 'error');
    } finally {
      setTransitionLoading(false);
    }
  };

  const handleResolveWarranty = async (action: 'Resolved' | 'Rejected') => {
    if (!bookingData) return;
    setWarrantyActionLoading(true);
    try {
      const updatedWarranty = await resolveAdminWarrantyClaim(
        bookingData.id,
        action,
        warrantyResolveNotes.trim() || undefined
      );
      setBookingData((prev) => (prev ? { ...prev, warranty: updatedWarranty } : prev));
      showToast(`Warranty claim successfully marked as ${action}!`, 'success');
      setWarrantyResolvingAction(null);
      setWarrantyResolveNotes('');
      fetchBookingProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to update warranty claim status.', 'error');
    } finally {
      setWarrantyActionLoading(false);
    }
  };

  const handleReassignSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!bookingData || !selectedProviderId) return;
    setReassignLoading(true);
    try {
      const res = await reassignBookingProvider(bookingData.id, selectedProviderId, reassignReason);
      showToast(res.message, 'success');
      setReassignModalOpen(false);
      fetchBookingProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Provider reassignment failed.', 'error');
    } finally {
      setReassignLoading(false);
    }
  };

  const handleOpenAuditModal = async () => {
    if (!bookingData) return;
    setAuditModalOpen(true);
    setAuditLoading(true);
    setAuditError(null);
    try {
      const data = await getBookingConversation(bookingData.id);
      setAuditTicket(data);
    } catch (err: any) {
      setAuditError(err.response?.data?.detail || 'No chat found or failed to load conversation.');
    } finally {
      setAuditLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-slate-600">Loading Operational Booking Details & Lifecycle Timeline...</p>
      </div>
    );
  }

  if (error || !bookingData) {
    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white border border-rose-200 rounded-3xl text-center space-y-4 shadow-sm">
        <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold font-serif text-[#1F2A1E]">Booking Record Not Found</h3>
        <p className="text-xs text-slate-600">{error || 'Unable to retrieve requested booking record.'}</p>
        <button
          onClick={() => navigate('/admin/bookings')}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#2F5233] text-white rounded-2xl text-xs font-bold"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Bookings Directory</span>
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-slate-800">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-3 px-5 py-3.5 bg-slate-900 text-white rounded-2xl shadow-xl border border-slate-700 text-xs font-semibold animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{toastMessage.text}</span>
        </div>
      )}

      {/* Breadcrumb Navigation */}
      <nav className="flex items-center gap-2 text-xs text-slate-500 font-medium">
        <Link to="/admin/bookings" className="hover:text-[#2F5233] flex items-center gap-1 transition-colors">
          <CalendarCheck className="w-3.5 h-3.5" />
          <span>Operations</span>
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <Link to="/admin/bookings" className="hover:text-[#2F5233] transition-colors">
          Bookings
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <span className="text-slate-900 font-bold font-mono">#{bookingData.id.substring(0, 8)}</span>
      </nav>

      {/* Operational Header Banner */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-start md:items-center gap-5">
          <button
            onClick={() => navigate('/admin/bookings')}
            className="p-2.5 rounded-2xl bg-[#F2EDE1] hover:bg-[#E5DEC9] text-slate-600 transition-colors"
            title="Back to Directory"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>

          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight font-mono">
                BK-{bookingData.id.substring(0, 8).toUpperCase()}
              </h1>
              <span className="text-[11px] font-mono text-slate-400">({bookingData.id})</span>
              <span className="px-3.5 py-1 bg-[#F2EDE1] text-[#2F5233] rounded-full text-xs font-bold border border-[#E5DEC9]">
                {bookingData.status}
              </span>
              {bookingData.emergency_flag && (
                <span className="px-3.5 py-1 bg-rose-50 text-rose-700 rounded-full text-xs font-extrabold border border-rose-200 flex items-center gap-1 animate-pulse">
                  <Siren className="w-3.5 h-3.5 text-rose-600" />
                  <span>{bookingData.emergency_flag}</span>
                </span>
              )}
            </div>

            <p className="text-sm text-slate-500 font-semibold mt-1">
              Service: <strong className="text-slate-800">{bookingData.service_name}</strong> | Scheduled:{' '}
              {bookingData.scheduled_time ? new Date(bookingData.scheduled_time).toLocaleString('en-IN') : 'N/A'}
            </p>
          </div>
        </div>

        {/* Action Controls based strictly on backend state machine */}
        <div className="flex items-center gap-2.5 flex-wrap justify-end">
          {canManageBookings ? (
            <>
              <button
                onClick={() => setReassignModalOpen(true)}
                className="px-4 py-2 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-slate-700 font-bold rounded-2xl border border-[#E5DEC9] text-xs transition-colors flex items-center gap-1.5"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                <span>Reassign Provider</span>
              </button>

              {bookingData.allowed_next_statuses && bookingData.allowed_next_statuses.length > 0 && (
                <button
                  onClick={() => {
                    setTargetNextStatus(bookingData.allowed_next_statuses[0]);
                    setTransitionModalOpen(true);
                  }}
                  className="px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-2xl shadow-sm text-xs transition-colors flex items-center gap-1.5"
                >
                  <Zap className="w-4 h-4" />
                  <span>Execute State Transition</span>
                </button>
              )}
            </>
          ) : (
            <button
              disabled
              title="Reassigning providers or executing state transitions requires 'bookings:manage' permission."
              className="px-4 py-2 bg-[#F2EDE1] text-slate-400 font-bold rounded-2xl border border-[#E5DEC9] text-xs cursor-not-allowed opacity-70"
            >
              🔒 Actions Restricted (View Only)
            </button>
          )}
        </div>
      </div>

      {/* Cancellation / Rejection Reason Banner */}
      {bookingData.cancellation_reason && (
        <div className="p-5 bg-rose-50 border border-rose-200 rounded-3xl flex items-start gap-3.5 text-rose-900 shadow-xs">
          <AlertTriangle className="w-5 h-5 text-rose-600 flex-shrink-0 mt-0.5" />
          <div className="space-y-1">
            <h4 className="text-xs font-bold uppercase tracking-wider text-rose-800">
              Booking Cancellation / Provider Rejection Reason Recorded
            </h4>
            <p className="text-sm font-semibold text-rose-950 font-serif">
              "{bookingData.cancellation_reason}"
            </p>
          </div>
        </div>
      )}

      {/* Live Provider Tracking Card (Ola / Swiggy style live monitoring) */}
      {(['Accepted', 'On The Way', 'Arrived', 'In Progress', 'Started', 'Completed'].includes(bookingData.status) || liveProviderLocation || liveLocationData?.provider_location || (bookingData.provider_id && ['Accepted', 'On The Way', 'Arrived', 'Started'].includes(bookingData.status))) && (
        <AdminLiveTrackingCard
          bookingId={bookingData.id}
          bookingStatus={bookingData.status}
          customer={{
            id: bookingData.customer_id,
            name: bookingData.customer_name || 'Customer',
            phone: bookingData.customer_phone || null,
          }}
          provider={
            bookingData.provider_id
              ? {
                  id: bookingData.provider_id,
                  full_name: bookingData.provider_name || 'Assigned Technician',
                  phone: null,
                }
              : null
          }
          serviceName={bookingData.service_name || 'Service Booking'}
          customerLocation={liveLocationData?.customer_location || null}
          providerLocation={liveProviderLocation || liveLocationData?.provider_location || null}
          wsConnected={wsConnected}
          onRefresh={fetchLocation}
        />
      )}

      {/* Grid Layout of Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Customer, Service & Provider Details */}
        <div className="space-y-6">
          {/* Customer Details */}
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <User className="w-5 h-5 text-[#2F5233]" />
              <span>Customer Details</span>
            </h3>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-400 font-semibold block">Customer Name</span>
                <p className="font-bold text-slate-900 text-sm mt-0.5">{bookingData.customer_name || 'Customer'}</p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Contact Phone</span>
                <p className="font-semibold text-slate-800 mt-0.5 flex items-center gap-1.5">
                  <Phone className="w-3.5 h-3.5 text-slate-400" />
                  <span>{bookingData.customer_phone || '+91 98765 43210'}</span>
                </p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Service Location Address</span>
                <p className="font-medium text-slate-700 mt-0.5 flex items-start gap-1.5 bg-[#FAF7F0] p-2.5 rounded-xl border border-[#E5DEC9]">
                  <MapPin className="w-4 h-4 text-rose-500 flex-shrink-0 mt-0.5" />
                  <span>{bookingData.address || 'Address not specified.'}</span>
                </p>
              </div>
            </div>
          </div>

          {/* Service & Payment Review Card */}
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center justify-between">
              <span className="flex items-center gap-2">
                <Banknote className="w-5 h-5 text-[#2F5233]" />
                <span>Payment & Cash Review</span>
              </span>
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                (bookingData.payment_status || '').toLowerCase() === 'paid'
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : (bookingData.payment_status || '').toLowerCase() === 'collection reported'
                  ? 'bg-amber-50 text-amber-700 border-amber-300 animate-pulse'
                  : (bookingData.payment_status || '').toLowerCase() === 'rejected'
                  ? 'bg-rose-50 text-rose-700 border-rose-200'
                  : 'bg-slate-100 text-slate-600 border-slate-200'
              }`}>
                {bookingData.payment_status}
              </span>
            </h3>

            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 font-semibold">Payment Method</span>
                <span className="font-bold text-slate-800 uppercase text-xs">
                  {bookingData.payment_method || 'Cash on Delivery (COD)'}
                </span>
              </div>

              <div className="flex items-center justify-between">
                <span className="text-slate-400 font-semibold">Agreed Service Price</span>
                <span className="font-extrabold text-slate-900 text-base font-mono">
                  ₹{bookingData.total_price.toLocaleString('en-IN')}
                </span>
              </div>

              {/* Reported Collection details if any */}
              {bookingPayments && bookingPayments.length > 0 && (() => {
                const latest = bookingPayments[0];
                const hasDiscrepancy = Boolean(latest.discrepancy_flag);
                return (
                  <div className="p-3 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9] space-y-2 mt-2">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-500 font-medium">Reported by Provider:</span>
                      <span className="font-mono font-bold text-slate-900">
                        {latest.reported_amount !== null && latest.reported_amount !== undefined ? `₹${latest.reported_amount}` : 'Not reported'}
                      </span>
                    </div>

                    {hasDiscrepancy && (
                      <div className="p-2 bg-rose-50 border border-rose-200 rounded-xl text-[11px] text-rose-800 flex items-start gap-1.5">
                        <AlertTriangle className="w-3.5 h-3.5 text-rose-600 shrink-0 mt-0.5" />
                        <div>
                          <strong className="block">Discrepancy Detected</strong>
                          <span>Agreed ₹{latest.agreed_amount} vs Reported ₹{latest.reported_amount} (Diff: ₹{latest.discrepancy_amount || Math.abs(latest.agreed_amount - (latest.reported_amount || 0))})</span>
                        </div>
                      </div>
                    )}

                    {latest.collected_at && (
                      <div className="flex items-center justify-between text-[11px] text-slate-500">
                        <span>Reported At:</span>
                        <span>{new Date(latest.collected_at).toLocaleString('en-IN')}</span>
                      </div>
                    )}

                    {latest.reviewed_by_name && (
                      <div className="pt-2 border-t border-[#E5DEC9] text-[11px] text-slate-600 space-y-0.5">
                        <p><strong>Audited By:</strong> {latest.reviewed_by_name}</p>
                        <p><strong>Audited At:</strong> {latest.reviewed_at ? new Date(latest.reviewed_at).toLocaleString('en-IN') : 'N/A'}</p>
                        {latest.rejection_reason && (
                          <p className="text-rose-700"><strong>Rejection Reason:</strong> {latest.rejection_reason}</p>
                        )}
                      </div>
                    )}

                    {/* Admin Action Buttons */}
                    {(latest.status === 'Collection Reported' || (bookingData.payment_status || '').toLowerCase() === 'collection reported') && (
                      <div className="flex items-center gap-2 pt-2 border-t border-[#E5DEC9]">
                        <button
                          type="button"
                          onClick={() => handleVerifyCollection(latest.id)}
                          disabled={paymentActionLoading === latest.id}
                          className="flex-1 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center justify-center gap-1.5 disabled:opacity-50"
                        >
                          <CheckCircle2 className="w-3.5 h-3.5" />
                          <span>{paymentActionLoading === latest.id ? 'Verifying...' : 'Verify Collection (Paid)'}</span>
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            setTargetRejectPaymentId(latest.id);
                            setRejectPaymentReason('');
                            setRejectPaymentModalOpen(true);
                          }}
                          disabled={paymentActionLoading === latest.id}
                          className="px-3 py-2 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 font-bold text-xs rounded-xl transition-colors disabled:opacity-50"
                        >
                          Reject
                        </button>
                      </div>
                    )}
                  </div>
                );
              })()}

              {/* Start & Completion OTP Information */}
              {(bookingData.start_otp || bookingData.otp_code) && (
                <div className="flex items-center justify-between border-t border-[#E5DEC9]/60 pt-2">
                  <span className="text-slate-400 font-semibold">Service Start OTP</span>
                  <span className="font-mono font-extrabold text-amber-800 bg-amber-50 px-2.5 py-0.5 rounded-lg border border-amber-200">
                    {bookingData.start_otp || bookingData.otp_code}
                  </span>
                </div>
              )}

              {bookingData.completion_otp && (
                <div className="flex items-center justify-between border-t border-[#E5DEC9]/60 pt-2">
                  <span className="text-slate-400 font-semibold">Service Completion OTP</span>
                  <span className="font-mono font-extrabold text-emerald-800 bg-emerald-50 px-2.5 py-0.5 rounded-lg border border-emerald-200">
                    {bookingData.completion_otp}
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Provider Info Card */}
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
                <UserCheck className="w-5 h-5 text-indigo-500" />
                <span>Assigned Provider</span>
              </h3>
              {canManageBookings ? (
                <button
                  type="button"
                  onClick={() => setReassignModalOpen(true)}
                  className="px-3 py-1 bg-indigo-50 hover:bg-indigo-100 text-indigo-600 font-bold text-xs rounded-xl border border-indigo-200 transition-colors"
                >
                  + Reassign Provider
                </button>
              ) : (
                <span className="text-[10px] font-bold text-slate-500 bg-[#F2EDE1] px-2 py-1 rounded-lg border border-[#E5DEC9]">
                  🔒 View Only Mode
                </span>
              )}
            </div>

            {bookingData.provider_name ? (
              <div className="space-y-2 text-xs">
                <div>
                  <span className="text-slate-400 font-semibold block">Provider Name</span>
                  <p className="font-bold text-slate-900 text-sm mt-0.5">{bookingData.provider_name}</p>
                </div>
                <div>
                  <span className="text-slate-400 font-semibold block">Provider User ID</span>
                  <p className="font-mono text-slate-600 text-[11px]">{bookingData.provider_id}</p>
                </div>
                {!canManageBookings && (
                  <p className="text-[11px] text-slate-500 italic pt-1 border-t border-[#E5DEC9]/60">
                    Reassignment requires Operations Admin or Super Admin permission.
                  </p>
                )}

                <button
                  type="button"
                  onClick={handleOpenAuditModal}
                  className="w-full mt-3 py-2 px-3 bg-purple-50 hover:bg-purple-100 text-purple-800 font-bold text-xs rounded-xl border border-purple-200 transition-colors flex items-center justify-center gap-1.5"
                >
                  <MessageCircle className="w-3.5 h-3.5 text-purple-600" />
                  <span>Audit Customer ↔ Provider Chat</span>
                </button>
              </div>
            ) : (
              <div className="space-y-3">
                <div className="p-4 bg-amber-50 text-amber-800 rounded-2xl border border-amber-200 text-xs font-semibold text-center">
                  Provider not assigned
                </div>
                {canManageBookings && (
                  <button
                    type="button"
                    onClick={() => setReassignModalOpen(true)}
                    className="w-full py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-2xl transition-colors shadow-xs"
                  >
                    Assign Provider Now
                  </button>
                )}
              </div>
            )}
          </div>

          {/* Customer Special Instructions / Phone Notes */}
          {bookingData.customer_notes && (
            <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
                <FileText className="w-5 h-5 text-amber-600" />
                <span>Customer Instructions & Notes</span>
              </h3>
              <div className="p-3.5 bg-amber-50/70 border border-amber-200/80 rounded-2xl text-xs text-amber-900 leading-relaxed whitespace-pre-wrap">
                {bookingData.customer_notes}
              </div>
            </div>
          )}

          {/* Service Verification Proof Photos */}
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <Camera className="w-5 h-5 text-[#2F5233]" />
              <span>Job Proof Photos</span>
            </h3>

            <div className="space-y-4 text-xs">
              {/* Before Photos */}
              <div className="space-y-2">
                <span className="font-bold text-slate-700 flex items-center gap-1.5 uppercase text-[10px] tracking-wider">
                  <span className="w-2 h-2 rounded-full bg-amber-500" />
                  Before Service ({bookingData.before_photos?.length || 0})
                </span>
                {bookingData.before_photos && bookingData.before_photos.length > 0 ? (
                  <div className="flex items-center gap-2 flex-wrap">
                    {bookingData.before_photos.map((url, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setPreviewPhotoUrl(url)}
                        className="relative w-16 h-16 rounded-2xl overflow-hidden border border-amber-200 group cursor-pointer shadow-2xs hover:scale-105 transition-transform"
                      >
                        <img src={url} alt={`Before ${idx + 1}`} className="w-full h-full object-cover" />
                        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity text-white">
                          <Eye className="w-4 h-4" />
                        </div>
                      </button>
                    ))}
                  </div>
                ) : (
                  <p className="text-[11px] text-slate-400 italic">No before photos recorded</p>
                )}
              </div>

              {/* After Photos */}
              <div className="space-y-2 border-t border-[#E5DEC9]/60 pt-3">
                <span className="font-bold text-emerald-800 flex items-center gap-1.5 uppercase text-[10px] tracking-wider">
                  <span className="w-2 h-2 rounded-full bg-emerald-500" />
                  After Service ({bookingData.after_photos?.length || 0})
                </span>
                {bookingData.after_photos && bookingData.after_photos.length > 0 ? (
                  <div className="flex items-center gap-2 flex-wrap">
                    {bookingData.after_photos.map((url, idx) => (
                      <button
                        key={idx}
                        type="button"
                        onClick={() => setPreviewPhotoUrl(url)}
                        className="relative w-16 h-16 rounded-2xl overflow-hidden border border-emerald-200 group cursor-pointer shadow-2xs hover:scale-105 transition-transform"
                      >
                        <img src={url} alt={`After ${idx + 1}`} className="w-full h-full object-cover" />
                        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity text-white">
                          <Eye className="w-4 h-4" />
                        </div>
                      </button>
                    ))}
                  </div>
                ) : (
                  <p className="text-[11px] text-slate-400 italic">No after photos recorded</p>
                )}
              </div>
            </div>
          </div>

          {/* 7-Day Digital Warranty & Claim Resolution */}
          {bookingData.warranty && (
            <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
                <h3 className="text-base font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-[#2F5233]" />
                  <span>7-Day Digital Warranty</span>
                </h3>
                <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase ${
                  bookingData.warranty.is_valid ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-500'
                }`}>
                  {bookingData.warranty.is_valid ? 'Active' : 'Expired'}
                </span>
              </div>

              <div className="space-y-3 text-xs">
                <div className="flex justify-between items-center text-slate-500">
                  <span>Issued Date:</span>
                  <span className="font-semibold text-slate-800">
                    {bookingData.warranty.issued_at ? new Date(bookingData.warranty.issued_at).toLocaleDateString() : 'N/A'}
                  </span>
                </div>
                <div className="flex justify-between items-center text-slate-500">
                  <span>Valid Until:</span>
                  <span className="font-semibold text-slate-800">
                    {bookingData.warranty.expires_at ? new Date(bookingData.warranty.expires_at).toLocaleDateString() : 'N/A'}
                  </span>
                </div>

                {/* Claim Status Details */}
                <div className="pt-2 border-t border-[#E5DEC9]/60 space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="font-bold text-slate-700">Claim Status:</span>
                    <span className={`px-2 py-0.5 rounded-full font-bold text-[10px] ${
                      bookingData.warranty.claim_status === 'Pending' ? 'bg-amber-100 text-amber-800 animate-pulse' :
                      bookingData.warranty.claim_status === 'Resolved' ? 'bg-emerald-100 text-emerald-800' :
                      bookingData.warranty.claim_status === 'Rejected' ? 'bg-rose-100 text-rose-800' :
                      'bg-slate-100 text-slate-600'
                    }`}>
                      {bookingData.warranty.claim_status}
                    </span>
                  </div>

                  {bookingData.warranty.claim_description && (
                    <div className="p-3 bg-amber-50/60 rounded-xl border border-amber-200 text-[11px] text-amber-900 space-y-1">
                      <span className="font-bold block">Customer Claim Reason:</span>
                      <p>{bookingData.warranty.claim_description}</p>
                    </div>
                  )}

                  {bookingData.warranty.claim_status === 'Pending' && canManageBookings && (
                    <div className="pt-2 space-y-2">
                      <textarea
                        value={warrantyResolveNotes}
                        onChange={(e) => setWarrantyResolveNotes(e.target.value)}
                        placeholder="Resolution / rejection remarks..."
                        rows={2}
                        className="w-full text-xs p-2.5 rounded-xl border border-[#E5DEC9] bg-[#FAF7F0] focus:outline-none focus:ring-1 focus:ring-[#2F5233]"
                      />
                      <div className="flex items-center gap-2">
                        <button
                          type="button"
                          disabled={warrantyActionLoading}
                          onClick={() => handleResolveWarranty('Resolved')}
                          className="flex-1 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-xl font-bold text-xs transition-colors shadow-2xs disabled:opacity-50 cursor-pointer"
                        >
                          {warrantyActionLoading ? 'Saving...' : '✓ Resolve Claim'}
                        </button>
                        <button
                          type="button"
                          disabled={warrantyActionLoading}
                          onClick={() => handleResolveWarranty('Rejected')}
                          className="flex-1 py-2 bg-rose-600 hover:bg-rose-700 text-white rounded-xl font-bold text-xs transition-colors shadow-2xs disabled:opacity-50 cursor-pointer"
                        >
                          {warrantyActionLoading ? 'Saving...' : '✗ Reject Claim'}
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Lifecycle Timeline & State Machine Status Control */}
        <div className="lg:col-span-2 space-y-6">
          {/* Allowed Next Transitions Banner */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-lg font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center justify-between">
              <span className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-amber-500" />
                <span>Backend State Machine Authorization</span>
              </span>
              <span className="text-xs font-semibold text-slate-400">Current: {bookingData.status}</span>
            </h3>

            {bookingData.allowed_next_statuses.length === 0 ? (
              <p className="text-xs text-slate-500 font-medium">
                🔒 Terminal lifecycle status reached ({bookingData.status}). No further state transitions allowed by backend logic.
              </p>
            ) : (
              <div className="space-y-3">
                <p className="text-xs text-slate-600 font-medium">
                  Valid transitions allowed by backend for current status <strong>{bookingData.status}</strong>:
                </p>
                <div className="flex flex-wrap gap-2">
                  {bookingData.allowed_next_statuses.map((st) => (
                    canManageBookings ? (
                      <button
                        key={st}
                        onClick={() => {
                          setTargetNextStatus(st);
                          setTransitionModalOpen(true);
                        }}
                        className="px-4 py-2 bg-[#F2EDE1] hover:bg-[#2F5233] text-[#2F5233] hover:text-white font-bold rounded-2xl border border-[#E5DEC9] text-xs transition-colors flex items-center gap-1.5"
                      >
                        <ChevronRight className="w-4 h-4" />
                        <span>Transition to {st}</span>
                      </button>
                    ) : (
                      <button
                        key={st}
                        disabled
                        title="State transition requires 'bookings:manage' permission."
                        className="px-4 py-2 bg-[#F2EDE1] text-slate-400 font-bold rounded-2xl border border-[#E5DEC9] text-xs cursor-not-allowed opacity-60 flex items-center gap-1.5"
                      >
                        <ChevronRight className="w-4 h-4 text-slate-400" />
                        <span>Transition to {st} (Disabled)</span>
                      </button>
                    )
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Booking Lifecycle Timeline */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-5">
            <h3 className="text-lg font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <History className="w-5 h-5 text-[#2F5233]" />
              <span>Booking Lifecycle History Timeline</span>
            </h3>

            {!bookingData.timeline || bookingData.timeline.length === 0 ? (
              <div className="p-6 bg-[#FAF7F0] rounded-2xl text-center text-xs font-semibold text-slate-500">
                No booking activity recorded.
              </div>
            ) : (
              <div className="relative pl-6 border-l-2 border-[#E5DEC9] space-y-6 text-xs">
                {bookingData.timeline.map((eventItem, idx) => (
                  <div key={idx} className="relative group">
                    <div className="absolute -left-[31px] top-0 w-4 h-4 rounded-full bg-white border-4 border-[#2F5233] group-hover:scale-110 transition-transform" />
                    <div className="bg-[#FAF7F0] p-4 rounded-2xl border border-[#E5DEC9] space-y-1">
                      <p className="font-bold text-slate-900 text-xs md:text-sm">{eventItem.event}</p>
                      {eventItem.reason && (
                        <p className="text-xs text-slate-600 font-medium">Reason: {eventItem.reason}</p>
                      )}
                      <p className="text-[10px] text-slate-400 font-semibold pt-1">
                        {eventItem.timestamp ? new Date(eventItem.timestamp).toLocaleString('en-IN') : ''}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Automated Notification Monitoring (Email & WhatsApp) */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-5">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-lg font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
                <Bell className="w-5 h-5 text-[#2F5233]" />
                <span>Automated Notification Monitoring</span>
              </h3>
              <span className="text-xs font-semibold text-slate-400">
                {adminNotifications.length} log entr{adminNotifications.length !== 1 ? 'ies' : 'y'}
              </span>
            </div>

            {adminNotifications.length === 0 ? (
              <div className="p-6 bg-[#FAF7F0] rounded-2xl text-center text-xs font-semibold text-slate-500">
                No notification events logged for booking reference {bookingData.booking_reference}.
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead>
                    <tr className="border-b border-[#E5DEC9] text-slate-400 uppercase text-[10px] tracking-wider font-semibold">
                      <th className="pb-2.5">Event</th>
                      <th className="pb-2.5">Channel</th>
                      <th className="pb-2.5">Recipient</th>
                      <th className="pb-2.5">Status</th>
                      <th className="pb-2.5">Retries</th>
                      <th className="pb-2.5">Last Attempt</th>
                      <th className="pb-2.5 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#E5DEC9]/50">
                    {adminNotifications.map((n) => {
                      const isEmail = n.channel === 'email';
                      const stLower = (n.delivery_status || '').toLowerCase();
                      return (
                        <tr key={n.id} className="hover:bg-slate-50/50">
                          <td className="py-3 font-bold text-slate-900 font-mono text-[11px]">
                            {n.event_type}
                          </td>
                          <td className="py-3">
                            <span className="inline-flex items-center gap-1 font-semibold text-slate-700 capitalize">
                              {isEmail ? <Mail className="w-3.5 h-3.5 text-sky-600" /> : <MessageCircle className="w-3.5 h-3.5 text-emerald-600" />}
                              <span>{n.channel}</span>
                            </span>
                          </td>
                          <td className="py-3 text-slate-600 font-mono text-[11px]">
                            {n.recipient}
                          </td>
                          <td className="py-3">
                            <span
                              className={`px-2 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                                stLower === 'sent' || stLower === 'delivered'
                                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                                  : stLower === 'pending'
                                  ? 'bg-amber-50 text-amber-700 border-amber-200'
                                  : stLower === 'unconfigured'
                                  ? 'bg-slate-100 text-slate-600 border-slate-300'
                                  : 'bg-rose-50 text-rose-700 border-rose-200'
                              }`}
                            >
                              {n.delivery_status}
                            </span>
                            {n.error_message && (
                              <p className="text-[10px] text-rose-600 font-normal mt-0.5 max-w-xs truncate" title={n.error_message}>
                                {n.error_message}
                              </p>
                            )}
                          </td>
                          <td className="py-3 font-semibold text-slate-600">
                            {n.retry_count}
                          </td>
                          <td className="py-3 text-[11px] text-slate-500">
                            {new Date(n.last_attempt_at || n.created_at).toLocaleString('en-IN')}
                          </td>
                          <td className="py-3 text-right">
                            {stLower === 'failed' && canManageBookings && (
                              <button
                                type="button"
                                onClick={() => handleRetryNotification(n.id)}
                                disabled={retryingNotificationId === n.id}
                                className="px-2.5 py-1 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 font-bold text-[10px] rounded-lg transition-colors inline-flex items-center gap-1 disabled:opacity-50"
                              >
                                {retryingNotificationId === n.id ? (
                                  <Loader2 className="w-3 h-3 animate-spin" />
                                ) : (
                                  <RefreshCw className="w-3 h-3" />
                                )}
                                <span>Retry</span>
                              </button>
                            )}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* State Machine Transition Modal */}
      {transitionModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleTransitionSubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Execute Booking State Transition</h3>
              <button type="button" onClick={() => setTransitionModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-medium">
              Current status is <strong>{bookingData.status}</strong>. Transitioning status will execute backend validation and audit logging.
            </p>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Target Next Status *</label>
              <select
                value={targetNextStatus}
                onChange={(e) => setTargetNextStatus(e.target.value)}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
              >
                {bookingData.allowed_next_statuses.map((st) => (
                  <option key={st} value={st}>{st}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Reason / Notes (Optional)</label>
              <textarea
                value={transitionReason}
                onChange={(e) => setTransitionReason(e.target.value)}
                placeholder="Operational transition note..."
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                rows={2}
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setTransitionModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={transitionLoading}
                className="px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {transitionLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm Transition'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Provider Reassignment Modal */}
      {reassignModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleReassignSubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Reassign Booking Provider</h3>
              <button type="button" onClick={() => setReassignModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-medium">
              Reassign booking <strong>#{bookingData.id.substring(0, 8)}</strong> to a new provider. Historical assignment timeline will be preserved.
            </p>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Select New Provider *</label>
              <select
                value={selectedProviderId}
                onChange={(e) => setSelectedProviderId(e.target.value)}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                required
              >
                {providerOptions.map((p) => (
                  <option key={p.id} value={p.id}>{p.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Reassignment Reason</label>
              <input
                type="text"
                value={reassignReason}
                onChange={(e) => setReassignReason(e.target.value)}
                placeholder="Reason for reassignment..."
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setReassignModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={reassignLoading}
                className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {reassignLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm Reassignment'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Customer ↔ Provider Chat Audit Modal */}
      {auditModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-2xl rounded-3xl shadow-2xl border border-[#E5DEC9] overflow-hidden flex flex-col max-h-[85vh] animate-in fade-in">
            {/* Header */}
            <div className="p-6 border-b border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-purple-100 text-purple-800 border border-purple-200">
                    Read-Only Audit Mode
                  </span>
                  <span className="text-xs text-slate-500 font-mono">#{bookingData.id.substring(0, 8)}</span>
                </div>
                <h3 className="text-lg font-bold font-serif text-[#1F2A1E] mt-1">Customer ↔ Provider Conversation</h3>
                <p className="text-xs text-slate-500 mt-0.5">
                  Customer: <strong>{bookingData.customer_name || 'Customer'}</strong> • Provider: <strong>{bookingData.provider_name || 'Provider'}</strong>
                </p>
              </div>
              <button onClick={() => setAuditModalOpen(false)} className="p-2 text-slate-400 hover:text-slate-600 rounded-xl hover:bg-slate-100">
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Conversation Body */}
            <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-slate-50/50">
              {auditLoading ? (
                <div className="flex items-center justify-center py-12 gap-3">
                  <Loader2 className="w-6 h-6 animate-spin text-[#2F5233]" />
                  <span className="text-xs font-semibold text-slate-600">Loading audit log...</span>
                </div>
              ) : auditError ? (
                <div className="p-8 text-center text-xs text-slate-500">
                  <MessageCircle className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                  <p>{auditError}</p>
                </div>
              ) : !auditTicket?.messages || auditTicket.messages.length === 0 ? (
                <div className="p-8 text-center text-xs text-slate-400">
                  <MessageCircle className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                  <p>No messages exchanged between customer and provider yet.</p>
                </div>
              ) : (
                auditTicket.messages.map((msg) => {
                  const role = (msg.sender_role || '').toLowerCase().trim();
                  const isProvider = role === 'provider';
                  const isCustomer = role === 'customer';
                  return (
                    <div
                      key={msg.id}
                      className={`flex flex-col max-w-md ${isProvider ? 'ml-auto items-end' : 'items-start'}`}
                    >
                      <div className={`flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider mb-1 px-1 ${
                        isProvider ? 'text-emerald-700 flex-row-reverse' : 'text-blue-700'
                      }`}>
                        <span>{msg.sender_name || (isProvider ? 'Provider' : isCustomer ? 'Customer' : 'User')}</span>
                        <span className="opacity-60 text-[9px]">({role})</span>
                      </div>
                      <div className={`px-4 py-3 rounded-2xl text-xs font-medium leading-relaxed shadow-2xs ${
                        isProvider
                          ? 'bg-[#2F5233] text-white rounded-tr-xs'
                          : 'bg-white text-slate-900 border border-slate-200 rounded-tl-xs'
                      }`}>
                        {msg.message_text}
                      </div>
                      <span className="text-[9px] text-slate-400 mt-1 px-1 font-medium">
                        {new Date(msg.created_at).toLocaleString('en-IN', {
                          day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit'
                        })}
                      </span>
                    </div>
                  );
                })
              )}
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-between text-xs">
              <span className="text-slate-500 font-medium">
                Audited by Super Admin: <strong>{adminSession?.email || 'Admin'}</strong>
              </span>
              <button
                onClick={() => setAuditModalOpen(false)}
                className="px-4 py-2 bg-[#2F5233] text-white font-bold rounded-xl text-xs hover:bg-[#3D6B42]"
              >
                Close Audit View
              </button>
            </div>
          </div>
        </div>
      )}
      {/* Lightbox Modal for Photo Preview */}
      {previewPhotoUrl && (
        <div
          className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4 backdrop-blur-xs"
          onClick={() => setPreviewPhotoUrl(null)}
        >
          <div
            className="relative max-w-2xl max-h-[90vh] bg-white rounded-3xl p-3 shadow-2xl overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <button
              onClick={() => setPreviewPhotoUrl(null)}
              className="absolute top-4 right-4 p-2 bg-black/60 hover:bg-black text-white rounded-full transition-colors z-10 cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>
            <img
              src={previewPhotoUrl}
              alt="Service Verification Proof"
              className="max-w-full max-h-[80vh] object-contain rounded-2xl"
            />
          </div>
        </div>
      )}

      {/* Reject Payment Report Modal */}
      {rejectPaymentModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in">
          <form onSubmit={handleRejectCollection} className="bg-white rounded-3xl max-w-md w-full p-6 space-y-4 shadow-2xl border border-[#E5DEC9]">
            <div className="flex items-start justify-between border-b border-[#E5DEC9]/60 pb-3">
              <div className="flex items-center gap-2">
                <div className="w-9 h-9 rounded-xl bg-rose-50 border border-rose-200 flex items-center justify-center text-rose-600">
                  <ShieldAlert className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Reject Cash Collection Report</h3>
                  <p className="text-[11px] font-mono text-[#1F2A1E]/60">Booking ID: {bookingData.id.substring(0, 8)}</p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setRejectPaymentModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 p-1 rounded-full hover:bg-black/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-1.5">
              <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider">
                Rejection Reason (Audit Trail Required)
              </label>
              <textarea
                required
                rows={3}
                value={rejectPaymentReason}
                onChange={(e) => setRejectPaymentReason(e.target.value)}
                placeholder="State the reason for rejecting this cash collection report..."
                className="w-full text-xs bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2 border-t border-[#E5DEC9]">
              <button
                type="button"
                onClick={() => setRejectPaymentModalOpen(false)}
                className="px-4 py-2 bg-[#FAF7F0] hover:bg-[#F2EDE1] text-[#1F2A1E] font-bold text-xs rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={!rejectPaymentReason.trim() || paymentActionLoading === targetRejectPaymentId}
                className="px-5 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors disabled:opacity-50 flex items-center gap-1.5"
              >
                {paymentActionLoading === targetRejectPaymentId ? 'Saving...' : 'Confirm Rejection'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
