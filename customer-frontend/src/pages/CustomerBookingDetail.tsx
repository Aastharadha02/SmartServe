import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  getBookingDetail, 
  cancelBooking, 
  BookingDetail, 
  getBookingLiveLocation,
  updateCustomerLocation,
  BookingLocationResponse,
  ProviderProfileInfo,
  ProviderGpsLocation,
  CustomerLocationInfo,
  getBookingNotifications,
  CustomerNotificationItem,
} from '../api/bookings';
import { getBookingChat, sendBookingChatMessage, SupportTicketDetail, MessageItem } from '../api/support';
import { formatCurrencyINR } from '../utils/formatters';
import { useToast } from '../hooks/useToast';
import { 
  ArrowLeft, 
  Clock, 
  MapPin, 
  KeyRound, 
  AlertCircle, 
  Loader2, 
  UserCheck, 
  XCircle,
  HelpCircle,
  Zap,
  MessageCircle,
  Send,
  User,
  ShieldCheck,
  Banknote,
  Bell,
  Mail,
} from 'lucide-react';
import { subscribeToRealtime } from '../utils/realtime';
import { CustomerLiveMap } from '../components/CustomerLiveMap';
import { CustomerProviderCard, BookingTimeline } from '../components/CustomerProviderCard';

export const CustomerBookingDetail: React.FC = () => {
  const { bookingId } = useParams<{ bookingId: string }>();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const [booking, setBooking] = useState<BookingDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [cancelling, setCancelling] = useState<boolean>(false);
  const [showCancelModal, setShowCancelModal] = useState<boolean>(false);
  const [selectedReason, setSelectedReason] = useState<string>('Change of plans / schedule conflict');
  const [notifications, setNotifications] = useState<CustomerNotificationItem[]>([]);

  // Live Location & Provider Profile state
  const [providerProfile, setProviderProfile] = useState<ProviderProfileInfo | null>(null);
  const [providerLocation, setProviderLocation] = useState<ProviderGpsLocation | null>(null);
  const [customerLocationFromApi, setCustomerLocationFromApi] = useState<CustomerLocationInfo | null>(null);
  const [, setCustomerGeoPermission] = useState<'prompt' | 'granted' | 'denied' | 'unsupported'>('prompt');
  const [customerCoords, setCustomerCoords] = useState<{ latitude: number; longitude: number } | null>(null);
  const [wsStatus, setWsStatus] = useState<'connecting' | 'connected' | 'disconnected'>('connecting');

  // Request actual customer browser geolocation (Requirement 8)
  useEffect(() => {
    if (!('geolocation' in navigator)) {
      setCustomerGeoPermission('unsupported');
      return;
    }
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setCustomerGeoPermission('granted');
        setCustomerCoords({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
        });
        if (bookingId) {
          updateCustomerLocation(bookingId, pos.coords.latitude, pos.coords.longitude);
        }
      },
      (err) => {
        if (err.code === err.PERMISSION_DENIED) {
          setCustomerGeoPermission('denied');
        }
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  }, [bookingId]);

  const effectiveCustomerLocation: CustomerLocationInfo | null = customerCoords
    ? {
        latitude: customerCoords.latitude,
        longitude: customerCoords.longitude,
        address: booking?.address_line1 || booking?.address || customerLocationFromApi?.address || 'Service Location',
        city: booking?.city || customerLocationFromApi?.city || '',
      }
    : (customerLocationFromApi || (booking ? {
        latitude: 28.6280,
        longitude: 77.3649,
        address: booking.address_line1 || booking.address || 'Sector 62, Noida',
        city: booking.city || 'Noida',
      } : null));

  // Chat state
  const [chatTicket, setChatTicket] = useState<SupportTicketDetail | null>(null);
  const [chatLoading, setChatLoading] = useState<boolean>(false);
  const [chatError, setChatError] = useState<string | null>(null);
  const [chatMessage, setChatMessage] = useState<string>('');
  const [sendingChat, setSendingChat] = useState<boolean>(false);
  const [showChat, setShowChat] = useState<boolean>(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const fetchDetail = async () => {
    if (!bookingId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getBookingDetail(bookingId);
      setBooking(data);
      // Fetch live location & provider details
      fetchLocationData();
      try {
        const notifs = await getBookingNotifications(bookingId);
        setNotifications(notifs);
      } catch (errNotif) {
        console.warn('Failed to load notification history:', errNotif);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch booking details from database.');
    } finally {
      setLoading(false);
    }
  };

  const fetchLocationData = async () => {
    if (!bookingId) return;
    try {
      const locData: BookingLocationResponse = await getBookingLiveLocation(bookingId);
      if (locData.provider) {
        setProviderProfile(locData.provider);
      }
      if (locData.provider_location) {
        setProviderLocation(locData.provider_location);
      }
      if (locData.customer_location) {
        setCustomerLocationFromApi(locData.customer_location);
      }
    } catch (err) {
      console.warn('Live location endpoint returned error or not yet ready:', err);
    }
  };

  useEffect(() => {
    fetchDetail();
    if (!bookingId) return;

    // Real-Time WebSocket Subscription for booking status & live GPS tracking (No Polling Required)
    const unsubscribeWs = subscribeToRealtime(
      [`booking_${bookingId}`, 'bookings', 'dashboard'],
      (payload) => {
        const targetId = String(payload.booking_id || payload.booking?.id || '').toLowerCase();
        if (targetId && targetId === String(bookingId).toLowerCase()) {
          const type = payload.type || payload.event_type || payload.event;

          if (type === 'PROVIDER_LOCATION_UPDATED' || type === 'provider.location.updated') {
            // Real-time GPS coordinate event
            if (payload.latitude !== undefined && payload.longitude !== undefined) {
              setProviderLocation({
                latitude: Number(payload.latitude),
                longitude: Number(payload.longitude),
                heading: payload.heading !== undefined ? Number(payload.heading) : null,
                speed: payload.speed !== undefined ? Number(payload.speed) : null,
                accuracy: payload.accuracy !== undefined ? Number(payload.accuracy) : null,
                updated_at: payload.updated_at || new Date().toISOString(),
              });
            }
            if (payload.status) {
              setBooking((prev) => (prev ? { ...prev, status: payload.status } : prev));
            }
          } else if (type === 'BOOKING_ACCEPTED' || type === 'booking.accepted') {
            setBooking((prev) => (prev ? { ...prev, status: 'Accepted' } : prev));
            fetchLocationData();
          } else if (type === 'BOOKING_STATUS_UPDATED' || type === 'booking.updated') {
            const nextSt = payload.status || payload.booking?.status;
            if (nextSt) {
              setBooking((prev) => (prev ? { ...prev, status: nextSt } : prev));
              if (['Completed', 'Cancelled', 'Rejected'].includes(nextSt)) {
                setProviderLocation(null);
              }
            }
            fetchLocationData();
          } else if (type === 'BOOKING_STARTED' || type === 'booking.started') {
            setBooking((prev) => (prev ? { ...prev, status: 'Started' } : prev));
            fetchLocationData();
          } else if (type === 'BOOKING_COMPLETED' || type === 'booking.completed') {
            setBooking((prev) => (prev ? { ...prev, status: 'Completed' } : prev));
            setProviderLocation(null); // Stop live tracking
          } else if (type === 'BOOKING_REJECTED' || type === 'booking.rejected') {
            const reason = payload.reason || payload.rejection_reason || payload.cancellation_reason || 'Provider unavailable';
            setBooking((prev) =>
              prev
                ? {
                    ...prev,
                    status: 'Rejected',
                    cancellation_reason: reason,
                    rejection_reason: reason,
                  } as any
                : prev
            );
            setProviderLocation(null);
          }

          // Re-sync full record silently on lifecycle changes (avoid redundant fetch on 1s GPS pings)
          if (type !== 'PROVIDER_LOCATION_UPDATED' && type !== 'provider.location.updated') {
            getBookingDetail(bookingId)
              .then((data) => setBooking(data))
              .catch(() => {});
          }
        }
      },
      (status) => setWsStatus(status)
    );

    return () => {
      unsubscribeWs();
    };
  }, [bookingId]);

  // Load chat when provider is assigned and chat is open
  const fetchChat = async () => {
    if (!bookingId) return;
    setChatLoading(true);
    setChatError(null);
    try {
      const data = await getBookingChat(bookingId);
      setChatTicket(data);
      setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 100);
    } catch (err: any) {
      const detail = err.response?.data?.detail || '';
      if (err.response?.status === 400 && detail.includes('No provider')) {
        setChatError('provider_not_assigned');
      } else {
        setChatError(err.response?.data?.detail || 'Failed to load chat.');
      }
    } finally {
      setChatLoading(false);
    }
  };

  useEffect(() => {
    if (!showChat || !bookingId) return;

    fetchChat();

    const channels = [`booking_${bookingId}`, `booking_chat_${bookingId}`, 'support', 'support_tickets'];
    if (chatTicket?.id) {
      channels.push(`ticket_${chatTicket.id}`);
    }

    // Real-Time Kafka -> WebSocket Subscription for chat messages (No Polling Required)
    const unsubscribeWs = subscribeToRealtime(channels, (payload) => {
      const type = payload.type || payload.event_type || payload.event;
      if (type === 'NEW_SUPPORT_MESSAGE' || type === 'support.message') {
        const msg = payload.message || payload.data;
        if (msg) {
          setChatTicket((prev) => {
            if (!prev) return prev;
            const exists = (prev.messages || []).some((m: any) => m.id === msg.id);
            if (exists) return prev;
            return {
              ...prev,
              messages: [...(prev.messages || []), msg],
            };
          });
          setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 50);
        }
        getBookingChat(bookingId)
          .then((data) => {
            setChatTicket(data);
            setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 50);
          })
          .catch(() => {});
      }
    });

    return () => {
      unsubscribeWs();
    };
  }, [showChat, bookingId]);

  const handleSendChatMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!bookingId || !chatMessage.trim()) return;
    setSendingChat(true);
    try {
      const newMsg = await sendBookingChatMessage(bookingId, chatMessage.trim());
      setChatMessage('');
      setChatTicket(prev => prev ? { ...prev, messages: [...prev.messages, newMsg] } : prev);
      setTimeout(() => chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }), 50);
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to send message.', 'error');
    } finally {
      setSendingChat(false);
    }
  };

  const handleConfirmCancel = async () => {
    if (!bookingId) return;

    setCancelling(true);
    try {
      await cancelBooking(bookingId, selectedReason);
      showToast('Booking cancelled successfully.', 'info');
      setShowCancelModal(false);
      fetchDetail();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to cancel booking.', 'error');
    } finally {
      setCancelling(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3 font-sans">
        <Loader2 className="w-10 h-10 animate-spin text-[#2563EB]" />
        <p className="text-sm font-semibold text-slate-600">Loading booking status from database...</p>
      </div>
    );
  }

  if (error || !booking) {
    return (
      <div className="max-w-md mx-auto my-12 p-8 bg-white border border-slate-200 rounded-3xl text-center space-y-4 shadow-sm font-sans">
        <AlertCircle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold text-slate-900">Booking Record Not Found</h3>
        <p className="text-xs text-slate-600">{error || 'The requested booking ID does not exist in the database.'}</p>
        <button
          onClick={() => navigate('/bookings')}
          className="px-5 py-2.5 bg-[#2563EB] text-white font-bold text-xs rounded-xl inline-flex items-center gap-2"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to My Bookings</span>
        </button>
      </div>
    );
  }

  const stLower = booking.status.toLowerCase();
  const canCancel = stLower === 'requested' || stLower === 'assigned';
  const showLiveTracking = ['accepted', 'on the way', 'arrived', 'started'].includes(stLower);

  const effectiveProvider: ProviderProfileInfo | null = providerProfile || booking.provider || (booking.provider_id ? {
    provider_id: booking.provider_id,
    full_name: booking.provider_name || 'Assigned Expert Partner',
    photo_url: `https://api.dicebear.com/7.x/avataaars/svg?seed=${booking.provider_name || 'Provider'}`,
    category: booking.category || 'Service Partner',
    skills: 'Certified Service Professional',
    experience_years: 5,
    reliability_score: 99,
    rating: 4.9,
    is_verified: true,
    service_area: booking.city || 'Bengaluru, India'
  } : null);

  const showProviderCard = Boolean(effectiveProvider);

  return (
    <div className="space-y-6 font-sans max-w-4xl mx-auto pb-12">
      
      {/* Back button */}
      <button
        onClick={() => navigate('/bookings')}
        className="inline-flex items-center gap-2 text-xs font-bold text-slate-600 hover:text-[#2563EB] transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to My Bookings</span>
      </button>

      {/* Reconnecting banner if WebSocket is offline or reconnecting (Requirement 9) */}
      {wsStatus !== 'connected' && (
        <div className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-semibold w-fit animate-pulse">
          <span className="w-2 h-2 rounded-full bg-amber-400"></span>
          <span>Reconnecting to live location…</span>
        </div>
      )}

      {/* Main Status & Reference Ribbon */}
      <div className="bg-[#0A1128] text-white p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-mono text-sm font-bold text-blue-300">{booking.booking_reference}</span>
            <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
              stLower === 'completed' || stLower === 'paid'
                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30'
                : stLower === 'cancelled' || stLower === 'rejected'
                ? 'bg-rose-500/20 text-rose-300 border-rose-400/30'
                : stLower === 'started'
                ? 'bg-purple-500/20 text-purple-300 border-purple-400/30'
                : 'bg-blue-500/20 text-blue-300 border-blue-400/30'
            }`}>
              Booking: {booking.status}
            </span>
            <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
              (booking.payment_status || '').toLowerCase() === 'paid'
                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30'
                : (booking.payment_status || '').toLowerCase() === 'collection reported'
                ? 'bg-amber-500/20 text-amber-300 border-amber-400/30'
                : (booking.payment_status || '').toLowerCase() === 'rejected'
                ? 'bg-rose-500/20 text-rose-300 border-rose-400/30'
                : 'bg-slate-700/60 text-slate-300 border-slate-600'
            }`}>
              Payment: {booking.payment_status || 'Pending'}
            </span>
            {showLiveTracking && (
              <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>Active Job</span>
              </span>
            )}
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">{booking.service_name}</h1>
        </div>

        <div className="text-left sm:text-right">
          <span className="text-xs text-slate-400 font-semibold block">Total Amount</span>
          <span className="text-2xl font-extrabold text-white font-mono">
            {formatCurrencyINR(booking.total_price || booking.total_amount || 0)}
          </span>
        </div>
      </div>

      {/* Emergency Alert Banner */}
      {Boolean(booking.emergency_flag) && (
        <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold flex-shrink-0">
              <Zap className="w-5 h-5 text-white animate-pulse" />
            </div>
            <div>
              <h4 className="font-bold text-amber-950 text-sm">Emergency Fast-Track Service</h4>
              <p className="text-xs text-amber-800">Priority safety dispatch auto-assigned per SmartServe safety protocols.</p>
            </div>
          </div>
          <span className="text-[11px] font-black uppercase tracking-wider px-2.5 py-1 bg-amber-500 text-white rounded-lg shadow-2xs">
            Emergency Dispatch
          </span>
        </div>
      )}

      {/* Rejection / Cancellation Reason Notification Banner */}
      {(stLower === 'rejected' || stLower === 'cancelled') && (
        <div className="p-5 rounded-2xl bg-rose-50 border border-rose-200 flex items-start gap-4 animate-in fade-in">
          <div className="w-10 h-10 rounded-xl bg-rose-100 text-rose-700 flex items-center justify-center flex-shrink-0 mt-0.5">
            <XCircle className="w-5 h-5 text-rose-600" />
          </div>
          <div className="space-y-1">
            <h4 className="font-bold text-rose-950 text-sm">
              {stLower === 'rejected' ? 'Service Request Declined by Partner' : 'Booking Cancelled'}
            </h4>
            <p className="text-xs text-rose-800 font-semibold">
              Reason: {booking.cancellation_reason || (booking as any).rejection_reason || 'Provider unavailable'}
            </p>
            <p className="text-[11px] text-rose-600 font-medium pt-1">
              You can reschedule with another time slot or choose another service from our catalog.
            </p>
          </div>
        </div>
      )}

      {/* Provider Arrived Special Notification Banner */}
      {stLower === 'arrived' && (
        <div className="p-5 rounded-3xl bg-teal-500/10 border-2 border-teal-500/40 flex items-center justify-between gap-4 shadow-sm animate-in fade-in">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-2xl bg-teal-600 text-white flex items-center justify-center shrink-0 shadow-md">
              <MapPin className="w-6 h-6 animate-bounce" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h4 className="font-extrabold text-teal-950 text-base">Your Technician Has Arrived!</h4>
                <span className="text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full bg-teal-200 text-teal-900 border border-teal-300">
                  Ready at Doorstep
                </span>
              </div>
              <p className="text-xs text-teal-800 mt-0.5">
                Please verify technician credentials and provide your 4-digit Service Start OTP to initiate the job.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Service Start OTP Code Box (Before Service Starts) */}
      {(booking.start_otp || booking.otp_code) && ['requested', 'assigned', 'accepted', 'on the way', 'arrived'].includes(stLower) && (
        <div className="p-5 rounded-3xl bg-gradient-to-r from-amber-50 via-orange-50 to-amber-50 border-2 border-amber-300 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm">
          <div className="flex items-center gap-3.5">
            <div className="w-12 h-12 rounded-2xl bg-amber-500 text-white flex items-center justify-center flex-shrink-0 shadow-md">
              <KeyRound className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h4 className="font-extrabold text-amber-950 text-base">Service Start OTP</h4>
                <span className={`text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full border ${
                  stLower === 'arrived'
                    ? 'bg-emerald-100 text-emerald-800 border-emerald-300 animate-pulse'
                    : 'bg-amber-100 text-amber-800 border-amber-300'
                }`}>
                  {stLower === 'arrived' ? 'Share With Technician Now' : 'Share Upon Arrival'}
                </span>
              </div>
              <p className="text-xs text-amber-800 mt-1 max-w-lg">
                Share this 4-digit one-time code with your service technician when they arrive at your location to authorize and start the service.
              </p>
            </div>
          </div>
          <div className="text-left sm:text-right shrink-0">
            <span className="font-mono text-3xl font-black text-amber-950 tracking-widest bg-white px-5 py-2.5 rounded-2xl border-2 border-amber-400 shadow-sm inline-block">
              {booking.start_otp || booking.otp_code}
            </span>
            <span className="text-[10px] font-bold text-amber-700 tracking-wider uppercase mt-1 block">
              Single-Use Start Code
            </span>
          </div>
        </div>
      )}

      {/* Service In Progress Banner & Service Completion OTP */}
      {stLower === 'started' && (
        <div className="space-y-4">
          <div className="p-5 rounded-3xl bg-purple-50 border-2 border-purple-200 flex items-center gap-3.5 shadow-sm">
            <div className="w-12 h-12 rounded-2xl bg-purple-600 text-white flex items-center justify-center shrink-0 shadow-md">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h4 className="font-extrabold text-purple-950 text-base">Service In Progress</h4>
                <span className="text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full bg-purple-100 text-purple-800 border border-purple-300">
                  Start OTP Verified
                </span>
              </div>
              <p className="text-xs text-purple-800 mt-0.5">
                Technician is currently performing your service. Start OTP was successfully verified.
              </p>
            </div>
          </div>

          {booking.completion_otp && (
            <div className="p-5 rounded-3xl bg-gradient-to-r from-emerald-50 via-teal-50 to-emerald-50 border-2 border-emerald-300 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-sm animate-in fade-in">
              <div className="flex items-center gap-3.5">
                <div className="w-12 h-12 rounded-2xl bg-emerald-600 text-white flex items-center justify-center flex-shrink-0 shadow-md">
                  <KeyRound className="w-6 h-6" />
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <h4 className="font-extrabold text-emerald-950 text-base">Service Completion OTP</h4>
                    <span className="text-[10px] font-bold uppercase px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300 animate-pulse">
                      Provide Only When Done
                    </span>
                  </div>
                  <p className="text-xs text-emerald-800 mt-1 max-w-lg">
                    Share this 4-digit completion code with the technician <strong>only after you have inspected the service and are fully satisfied</strong> with the work done.
                  </p>
                </div>
              </div>
              <div className="text-left sm:text-right shrink-0">
                <span className="font-mono text-3xl font-black text-emerald-950 tracking-widest bg-white px-5 py-2.5 rounded-2xl border-2 border-emerald-400 shadow-sm inline-block">
                  {booking.completion_otp}
                </span>
                <span className="text-[10px] font-bold text-emerald-700 tracking-wider uppercase mt-1 block">
                  Single-Use Completion Code
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Cash on Delivery (COD) Payment & Verification Status Card */}
      <div className="p-6 rounded-3xl bg-white border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-5">
        <div className="flex items-start sm:items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-[#2F5233]/10 text-[#2F5233] flex items-center justify-center flex-shrink-0">
            <Banknote className="w-6 h-6" />
          </div>
          <div className="space-y-1">
            <div className="flex items-center gap-2 flex-wrap">
              <h4 className="font-extrabold text-slate-900 text-base">Payment: {booking.payment_method || 'Cash on Delivery (COD)'}</h4>
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                (booking.payment_status || '').toLowerCase() === 'paid'
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : (booking.payment_status || '').toLowerCase() === 'collection reported'
                  ? 'bg-amber-50 text-amber-700 border-amber-200'
                  : (booking.payment_status || '').toLowerCase() === 'rejected'
                  ? 'bg-rose-50 text-rose-700 border-rose-200'
                  : 'bg-slate-100 text-slate-700 border-slate-200'
              }`}>
                {booking.payment_status || 'Pending'}
              </span>
            </div>
            <p className="text-xs text-slate-600">
              {(booking.payment_status || '').toLowerCase() === 'paid'
                ? 'Payment has been verified and settled by SmartServe Operations Admin.'
                : (booking.payment_status || '').toLowerCase() === 'collection reported'
                ? 'Technician has reported receiving cash payment. Awaiting SmartServe Admin verification.'
                : (booking.payment_status || '').toLowerCase() === 'rejected'
                ? 'Reported cash collection was rejected by Admin for follow-up review.'
                : 'Pay the agreed service amount in cash directly to your technician upon satisfactory service completion.'}
            </p>
          </div>
        </div>
        <div className="text-left sm:text-right shrink-0 border-t sm:border-t-0 pt-3 sm:pt-0 border-slate-100">
          <span className="text-[11px] font-semibold text-slate-400 block uppercase">Agreed Amount</span>
          <span className="text-xl font-mono font-extrabold text-slate-900">
            {formatCurrencyINR(booking.total_price || booking.total_amount || 0)}
          </span>
        </div>
      </div>

      {/* ========================================================= */}
      {/* 1. LIVE TRACKING MAP (Ola / Swiggy Style Road Tracking)   */}
      {/* ========================================================= */}
      {showLiveTracking && (
        <CustomerLiveMap
          bookingId={booking.id}
          bookingStatus={booking.status}
          provider={effectiveProvider}
          providerLocation={providerLocation}
          customerLocation={effectiveCustomerLocation}
          serviceName={booking.service_name}
        />
      )}

      {/* ========================================================= */}
      {/* 2. FULL VERIFIED PROVIDER DETAILS CARD                     */}
      {/* ========================================================= */}
      {showProviderCard && effectiveProvider && (
        <CustomerProviderCard
          provider={effectiveProvider}
          serviceName={booking.service_name}
          category={booking.category}
          scheduledDate={booking.scheduled_date}
          scheduledTime={booking.scheduled_time}
          status={booking.status}
          providerLocation={providerLocation}
        />
      )}

      {/* ========================================================= */}
      {/* 3. BOOKING LIFECYCLE PROGRESSION TIMELINE                  */}
      {/* ========================================================= */}
      <BookingTimeline status={booking.status} />

      {/* Details Grid */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-md p-6 sm:p-8 space-y-6">
        <h3 className="text-sm font-bold text-slate-900 border-b border-slate-100 pb-3">Appointment Information</h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
          {/* Schedule */}
          <div className="space-y-2 p-5 rounded-2xl bg-slate-50 border border-slate-200/80">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <Clock className="w-4 h-4 text-blue-600" />
              <span>Scheduled Appointment</span>
            </h4>
            <p className="font-bold text-slate-900 text-base">{booking.scheduled_date}</p>
            <p className="text-xs text-slate-600">Time Slot: <strong>{booking.scheduled_time}</strong></p>
          </div>

          {/* Provider */}
          <div className="space-y-2 p-5 rounded-2xl bg-slate-50 border border-slate-200/80">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <UserCheck className="w-4 h-4 text-emerald-600" />
              <span>Assigned Service Expert</span>
            </h4>
            <p className="font-bold text-slate-900 text-base">
              {providerProfile?.full_name || booking.provider_name || 'Dispatching Verified Professional...'}
            </p>
            <p className="text-xs text-slate-600">SmartServe Background Checked & Insured</p>
          </div>

          {/* Address */}
          <div className="space-y-2 p-5 rounded-2xl bg-slate-50 border border-slate-200/80 md:col-span-2">
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
              <MapPin className="w-4 h-4 text-rose-600" />
              <span>Service Location Address</span>
            </h4>
            <p className="font-medium text-slate-900 leading-relaxed">
              {booking.address_line1 || booking.address || 'Address provided at booking'}
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="pt-4 border-t border-slate-100 flex items-center justify-between gap-4">
          <button
            onClick={() => navigate('/support')}
            className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 font-bold text-slate-700 rounded-xl text-xs flex items-center gap-2 transition-colors"
          >
            <HelpCircle className="w-4 h-4" />
            <span>Need Help with this Booking?</span>
          </button>

          {canCancel && (
            <button
              onClick={() => setShowCancelModal(true)}
              disabled={cancelling}
              className="px-5 py-2.5 bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs rounded-xl transition-colors flex items-center gap-1.5 disabled:opacity-50"
            >
              {cancelling ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <XCircle className="w-4 h-4" />}
              <span>Cancel Booking</span>
            </button>
          )}
        </div>
      </div>

      {/* Automated Booking Notifications History (Email & WhatsApp) */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-md p-6 sm:p-8 space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center">
              <Bell className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-slate-900">Delivery Receipts & Notifications</h3>
              <p className="text-[11px] text-slate-500">Automated updates sent to your registered Email and WhatsApp</p>
            </div>
          </div>
          <span className="text-xs font-semibold text-slate-400">
            {notifications.length} update{notifications.length !== 1 ? 's' : ''}
          </span>
        </div>

        {notifications.length === 0 ? (
          <div className="py-6 text-center bg-slate-50 rounded-2xl border border-slate-100">
            <Bell className="w-6 h-6 text-slate-300 mx-auto mb-1.5" />
            <p className="text-xs text-slate-500 font-medium">No automated notifications logged yet for this booking.</p>
          </div>
        ) : (
          <div className="space-y-2.5">
            {notifications.map((n) => {
              const isEmail = n.channel === 'email';
              const eventTitle = n.event_type
                .split('.')
                .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
                .join(' ');
              const stLower = (n.delivery_status || '').toLowerCase();
              return (
                <div
                  key={n.id}
                  className="p-3.5 rounded-2xl bg-slate-50/70 border border-slate-200/80 flex items-center justify-between gap-3 text-xs"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={`w-8 h-8 rounded-xl flex items-center justify-center shrink-0 ${
                        isEmail ? 'bg-sky-100 text-sky-700' : 'bg-emerald-100 text-emerald-700'
                      }`}
                    >
                      {isEmail ? <Mail className="w-4 h-4" /> : <MessageCircle className="w-4 h-4" />}
                    </div>
                    <div>
                      <p className="font-bold text-slate-900 capitalize">{eventTitle}</p>
                      <p className="text-[11px] text-slate-500 capitalize">
                        Channel: <strong>{n.channel}</strong> • {new Date(n.created_at).toLocaleString()}
                      </p>
                    </div>
                  </div>

                  <span
                    className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase shrink-0 border ${
                      stLower === 'sent' || stLower === 'delivered'
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                        : stLower === 'pending'
                        ? 'bg-amber-50 text-amber-700 border-amber-200'
                        : 'bg-rose-50 text-rose-700 border-rose-200'
                    }`}
                  >
                    {n.delivery_status}
                  </span>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Provider Chat Section */}
      {(booking.provider_id || providerProfile) && (
        <div className="bg-white rounded-3xl border border-slate-200/90 shadow-md overflow-hidden">
          <button
            onClick={() => setShowChat(!showChat)}
            className="w-full flex items-center justify-between p-6 text-left group"
          >
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-emerald-50 to-emerald-100 border border-emerald-200 flex items-center justify-center">
                <MessageCircle className="w-5 h-5 text-emerald-600" />
              </div>
              <div>
                <h3 className="text-sm font-bold text-slate-900">Direct Chat with Partner</h3>
                <p className="text-xs text-slate-500">{providerProfile?.full_name || booking.provider_name || 'Your assigned service expert'}</p>
              </div>
            </div>
            <div className={`w-8 h-8 rounded-xl bg-slate-100 group-hover:bg-slate-200 flex items-center justify-center transition-all ${showChat ? 'rotate-180' : ''}`}>
              <svg className="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </button>

          {showChat && (
            <div className="border-t border-slate-100">
              {chatLoading ? (
                <div className="flex items-center justify-center py-12 gap-3">
                  <Loader2 className="w-5 h-5 animate-spin text-emerald-600" />
                  <span className="text-xs font-semibold text-slate-500">Loading conversation...</span>
                </div>
              ) : chatError === 'provider_not_assigned' ? (
                <div className="p-6 text-center">
                  <p className="text-xs text-slate-500">Provider hasn't been assigned yet. Chat will be available once a provider accepts your booking.</p>
                </div>
              ) : chatError ? (
                <div className="p-6 text-center">
                  <p className="text-xs text-rose-600">{chatError}</p>
                  <button onClick={fetchChat} className="mt-2 text-xs text-emerald-600 font-semibold hover:underline">Retry</button>
                </div>
              ) : (
                <>
                  <div className="max-h-96 overflow-y-auto p-6 space-y-4 bg-slate-50/50">
                    {(!chatTicket?.messages || chatTicket.messages.length === 0) ? (
                      <div className="text-center py-8">
                        <MessageCircle className="w-8 h-8 text-slate-300 mx-auto mb-2" />
                        <p className="text-xs text-slate-400">No messages yet. Start the conversation!</p>
                      </div>
                    ) : (
                      chatTicket.messages.map((msg: MessageItem) => {
                        const role = (msg.sender_role || '').toLowerCase().trim();
                        const isCustomer = role === 'customer';
                        const isProvider = role === 'provider';
                        return (
                          <div key={msg.id} className={`flex flex-col max-w-xs ${isCustomer ? 'ml-auto items-end' : 'items-start'}`}>
                            <div className={`flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider mb-1 px-1 ${
                              isCustomer ? 'text-slate-400 flex-row-reverse' : isProvider ? 'text-emerald-600' : 'text-blue-600'
                            }`}>
                              {isCustomer ? (
                                <><User className="w-3 h-3" /><span>You (Customer)</span></>
                              ) : isProvider ? (
                                <><ShieldCheck className="w-3 h-3" /><span>{msg.sender_name || providerProfile?.full_name || 'Provider'}</span></>
                              ) : (
                                <><ShieldCheck className="w-3 h-3" /><span>SmartServe Support</span></>
                              )}
                            </div>
                            <div className={`px-4 py-3 rounded-2xl text-xs font-medium leading-relaxed shadow-2xs ${
                              isCustomer
                                ? 'bg-[#2563EB] text-white rounded-tr-xs'
                                : 'bg-white text-slate-800 border border-slate-200 rounded-tl-xs'
                            }`}>
                              {msg.message_text}
                            </div>
                            <span className="text-[9px] text-slate-400 mt-1 px-1">
                              {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </span>
                          </div>
                        );
                      })
                    )}
                    <div ref={chatEndRef} />
                  </div>

                  <form onSubmit={handleSendChatMessage} className="p-4 border-t border-slate-100 flex gap-3 bg-white">
                    <input
                      type="text"
                      value={chatMessage}
                      onChange={(e) => setChatMessage(e.target.value)}
                      placeholder={`Message ${providerProfile?.full_name || 'your provider'}...`}
                      className="flex-1 h-10 bg-slate-50 border border-slate-200 rounded-xl px-3 text-xs font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/30 focus:border-[#2563EB]"
                      disabled={sendingChat}
                    />
                    <button
                      type="submit"
                      disabled={sendingChat || !chatMessage.trim()}
                      className="h-10 w-10 bg-[#2563EB] hover:bg-blue-700 text-white rounded-xl flex items-center justify-center transition-colors disabled:opacity-50 flex-shrink-0 shadow-xs"
                    >
                      {sendingChat ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                    </button>
                  </form>
                </>
              )}
            </div>
          )}
        </div>
      )}

      {/* Cancellation Modal */}
      {showCancelModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs">
          <div className="bg-white rounded-3xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-slate-100 space-y-6">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-2xl bg-rose-50 flex items-center justify-center text-rose-600 flex-shrink-0">
                <AlertCircle className="w-6 h-6" />
              </div>
              <div className="space-y-1">
                <h3 className="text-lg font-extrabold text-slate-900">Cancel Service Booking?</h3>
                <p className="text-xs text-slate-500">
                  Ref: <span className="font-mono font-bold text-slate-700">{booking.booking_reference}</span> • {booking.service_name}
                </p>
              </div>
            </div>

            <div className="space-y-3">
              <label className="text-xs font-bold text-slate-700 block">
                Please select a reason for cancellation:
              </label>
              <select
                value={selectedReason}
                onChange={(e) => setSelectedReason(e.target.value)}
                className="w-full text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-3 text-slate-800 focus:outline-none focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500"
              >
                <option value="Change of plans / schedule conflict">Change of plans / schedule conflict</option>
                <option value="Booked by mistake">Booked by mistake</option>
                <option value="Found an alternative provider">Found an alternative provider</option>
                <option value="Price or timeline concern">Price or timeline concern</option>
                <option value="Other reasons">Other reasons</option>
              </select>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setShowCancelModal(false)}
                disabled={cancelling}
                className="px-5 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl transition-colors"
              >
                Keep Booking
              </button>

              <button
                type="button"
                onClick={handleConfirmCancel}
                disabled={cancelling}
                className="px-5 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl transition-colors flex items-center gap-1.5 shadow-sm disabled:opacity-50"
              >
                {cancelling ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <XCircle className="w-4 h-4" />}
                <span>Yes, Cancel Booking</span>
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default CustomerBookingDetail;
