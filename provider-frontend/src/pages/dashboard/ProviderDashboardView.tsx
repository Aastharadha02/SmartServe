import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Clock,
  ShieldCheck,
  Briefcase,
  FileCheck,
  Calendar,
  MapPin,
  User,
  RefreshCw,
  Play,
  CheckCircle2,
  AlertCircle,
  IndianRupee,
  Zap,
  ChevronRight,
  Bell,
  Star,
  Award,
  ArrowRight,
  LifeBuoy,
  X,
  XCircle,
  Radio,
  Compass,
  Navigation,
  KeyRound,
  Camera,
  Upload,
  FileText,
  Eye,
  Banknote,
} from 'lucide-react';
import { apiClient } from '../../api/client';
import { subscribeToRealtime } from '../../utils/realtime';

interface DashboardStats {
  today_bookings_count: number;
  active_jobs_count: number;
  completed_jobs_count: number;
  pending_requests_count: number;
  total_earnings: string;
  pipeline_count: number;
  urgent_alerts_count: number;
  recent_activity: {
    booking_id: string;
    reference: string;
    service_name: string;
    status: string;
    customer_name: string;
    amount: number;
    timestamp: string;
    is_emergency: boolean;
  }[];
}

interface ProfileTrust {
  full_name: string;
  email: string;
  phone?: string;
  photo_url?: string;
  category?: string;
  skills?: string;
  experience_years: number;
  service_area?: string;
  is_verified: boolean;
  reliability_score: string;
  acceptance_rate: string;
  cancellation_rate: string;
  on_time_rate: string;
  response_time_score: string;
  completed_jobs_count: number;
  certificates_count: number;
}

const STATUS_STYLES: Record<string, string> = {
  Requested: 'bg-amber-50 text-amber-800 border-amber-300',
  Assigned: 'bg-[#F2EDE1] text-[#2F5233] border-[#E5DEC9]',
  Accepted: 'bg-indigo-50 text-indigo-700 border-indigo-200',
  'On The Way': 'bg-sky-50 text-sky-700 border-sky-200',
  Arrived: 'bg-teal-50 text-teal-700 border-teal-200',
  Started: 'bg-purple-50 text-purple-700 border-purple-200',
  Completed: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  Cancelled: 'bg-slate-100 text-slate-500 border-slate-200',
  Rejected: 'bg-rose-50 text-rose-700 border-rose-200',
};

const resolvePhotoUrl = (url?: string | null) => {
  if (!url) return 'https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=400&q=80';
  if (url.startsWith('data:image')) return url;
  if (url.startsWith('http://') || url.startsWith('https://')) return url;
  const apiBase = (import.meta.env.VITE_API_URL || 'https://smartserve-api-de3f.onrender.com')
    .replace(/\/+$/, '')
    .replace(/\/api\/v1\/?$/, '');
  return `${apiBase}/${url.replace(/^\/+/, '')}`;
};

export const ProviderDashboardView: React.FC = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();

  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [trust, setTrust] = useState<ProfileTrust | null>(null);
  const [bookings, setBookings] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'all' | 'pending' | 'active' | 'completed'>('all');
  const [rejectingBooking, setRejectingBooking] = useState<any | null>(null);
  const [rejectionReason, setRejectionReason] = useState<string>('Schedule conflict with another job');

  // Photo Upload & Preview State
  const [photoUploadingBookingId, setPhotoUploadingBookingId] = useState<string | null>(null);
  const [previewPhotoUrl, setPreviewPhotoUrl] = useState<string | null>(null);

  // Service Start OTP state
  const [startingBooking, setStartingBooking] = useState<any | null>(null);
  const [startOtp, setStartOtp] = useState<string>('');
  const [startOtpError, setStartOtpError] = useState<string | null>(null);

  // Service Completion OTP state
  const [completingBooking, setCompletingBooking] = useState<any | null>(null);
  const [completeOtp, setCompleteOtp] = useState<string>('');
  const [completeOtpError, setCompleteOtpError] = useState<string | null>(null);

  // Cash Collection Reporting state
  const [cashCollectionBooking, setCashCollectionBooking] = useState<any | null>(null);
  const [collectedAmount, setCollectedAmount] = useState<string>('');
  const [collectionNotes, setCollectionNotes] = useState<string>('');
  const [collectionLoading, setCollectionLoading] = useState<boolean>(false);
  const [collectionError, setCollectionError] = useState<string | null>(null);
  const [collectionSuccess, setCollectionSuccess] = useState<string | null>(null);

  // Real Geolocation Tracking state
  const [locationPermission, setLocationPermission] = useState<'prompt' | 'granted' | 'denied' | 'unsupported'>('prompt');
  const [gpsCoordinates, setGpsCoordinates] = useState<{
    latitude: number;
    longitude: number;
    accuracy?: number;
    heading?: number;
    speed?: number;
  } | null>(null);
  const [lastGpsSync, setLastGpsSync] = useState<string | null>(null);
  const [isBroadcastingGps, setIsBroadcastingGps] = useState<boolean>(false);

  const compressImage = (file: File, maxWidth = 800, quality = 0.65): Promise<string> => {
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        const fallbackReader = new FileReader();
        fallbackReader.onload = () => resolve((fallbackReader.result as string) || '');
        fallbackReader.onerror = () => resolve('');
        fallbackReader.readAsDataURL(file);
      }, 2500);

      const reader = new FileReader();
      reader.onload = (event) => {
        const rawData = event.target?.result as string;
        if (!rawData) {
          clearTimeout(timer);
          resolve('');
          return;
        }
        const img = new Image();
        img.onload = () => {
          clearTimeout(timer);
          try {
            const canvas = document.createElement('canvas');
            let width = img.width || 800;
            let height = img.height || 600;
            if (width > maxWidth) {
              height = Math.round((height * maxWidth) / width);
              width = maxWidth;
            }
            canvas.width = width;
            canvas.height = height;
            const ctx = canvas.getContext('2d');
            if (!ctx) {
              resolve(rawData);
              return;
            }
            ctx.drawImage(img, 0, 0, width, height);
            resolve(canvas.toDataURL('image/jpeg', quality));
          } catch {
            resolve(rawData);
          }
        };
        img.onerror = () => {
          clearTimeout(timer);
          resolve(rawData);
        };
        img.src = rawData;
      };
      reader.onerror = () => {
        clearTimeout(timer);
        resolve('');
      };
      reader.readAsDataURL(file);
    });
  };


  const handlePhotoUpload = async (bookingId: string, type: 'before' | 'after', file: File) => {
    setPhotoUploadingBookingId(bookingId);
    setActionError(null);
    try {
      const base64Data = await compressImage(file, 800, 0.65);
      if (!base64Data) {
        setActionError('Could not process photo file.');
        setPhotoUploadingBookingId(null);
        return;
      }
      const res = await apiClient.post(`/providers/me/bookings/${bookingId}/photos/${type}`, {
        photo_url: base64Data,
      });
      const uploadedUrl = res.data?.photo_url || base64Data;
      // Immediately reflect uploaded photo in local state
      setBookings((prev) =>
        prev.map((b) => {
          if (b.id !== bookingId) return b;
          if (type === 'before') {
            const list = b.before_photos || [];
            return { ...b, before_photos: [...list, uploadedUrl] };
          } else {
            const list = b.after_photos || [];
            return { ...b, after_photos: [...list, uploadedUrl] };
          }
        })
      );
      // Background reload without blocking the photo completion UI
      fetchAll().catch(() => {});
    } catch (err: any) {
      console.error(`Failed to upload ${type} photo`, err);
      setActionError(err.response?.data?.detail || `Failed to upload ${type} photo. Please verify connection and retry.`);
    } finally {
      setPhotoUploadingBookingId(null);
    }
  };


  const fetchAll = async () => {
    try {
      const [statsRes, trustRes, bookingsRes] = await Promise.all([
        apiClient.get('/providers/me/dashboard-stats'),
        apiClient.get('/providers/me/profile-trust'),
        apiClient.get('/providers/me/bookings'),
      ]);
      setStats(statsRes.data);
      setTrust(trustRes.data);
      setBookings(bookingsRes.data);
    } catch (err) {
      console.error('Dashboard load error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Active booking detection
  const isStatusActive = (st: string) => {
    const s = (st || '').toLowerCase().replace(/_/g, ' ').trim();
    return ['accepted', 'on the way', 'arrived', 'started'].includes(s);
  };
  const activeBooking = bookings.find((b) => isStatusActive(b.status));

  // Send real GPS coordinates to backend with throttling
  const lastLocationSentRef = useRef<{ lat: number; lng: number; time: number } | null>(null);
  const [devSimulatingBookingId, setDevSimulatingBookingId] = useState<string | null>(null);
  const devSimIntervalRef = useRef<any>(null);

  const handleDevSimulateRoute = async (booking: any) => {
    if (devSimulatingBookingId === booking.id) {
      if (devSimIntervalRef.current) clearInterval(devSimIntervalRef.current);
      setDevSimulatingBookingId(null);
      return;
    }

    const pLat = gpsCoordinates?.latitude || 28.6280;
    const pLng = gpsCoordinates?.longitude || 77.3649;
    const cLat = 28.6360;
    const cLng = 77.3750;

    setDevSimulatingBookingId(booking.id);

    try {
      const url = `https://router.project-osrm.org/route/v1/driving/${pLng},${pLat};${cLng},${cLat}?overview=full&geometries=geojson`;
      const res = await fetch(url);
      const data = await res.json();
      let coords: [number, number][] = [];
      if (data.routes && data.routes.length > 0) {
        coords = data.routes[0].geometry.coordinates.map((c: [number, number]) => [c[1], c[0]]);
      } else {
        coords = [[pLat, pLng], [cLat, cLng]];
      }

      let step = 0;
      devSimIntervalRef.current = setInterval(async () => {
        step++;
        if (step >= coords.length) {
          clearInterval(devSimIntervalRef.current);
          setDevSimulatingBookingId(null);
          return;
        }
        const pt = coords[step];
        const prevPt = coords[step - 1];
        if (!pt || !prevPt) return;

        const dLon = ((pt[1] - prevPt[1]) * Math.PI) / 180;
        const y = Math.sin(dLon) * Math.cos((pt[0] * Math.PI) / 180);
        const x =
          Math.cos((prevPt[0] * Math.PI) / 180) * Math.sin((pt[0] * Math.PI) / 180) -
          Math.sin((prevPt[0] * Math.PI) / 180) * Math.cos((pt[0] * Math.PI) / 180) * Math.cos(dLon);
        const heading = ((Math.atan2(y, x) * 180) / Math.PI + 360) % 360;

        await sendLocation(booking.id, {
          latitude: pt[0],
          longitude: pt[1],
          heading,
          speed: 8.5,
          accuracy: 4.0,
        } as any, true);
      }, 1200);
    } catch (err) {
      console.warn('DEV Route simulation error:', err);
      setDevSimulatingBookingId(null);
    }
  };

  const sendLocation = async (bookingId: string, coords: GeolocationCoordinates, force = false) => {
    const now = Date.now();
    const last = lastLocationSentRef.current;
    if (!force && last) {
      const timeDiff = (now - last.time) / 1000;
      const distKm = Math.sqrt(
        Math.pow((coords.latitude - last.lat) * 111, 2) +
        Math.pow((coords.longitude - last.lng) * 111 * Math.cos((coords.latitude * Math.PI) / 180), 2)
      );
      // Skip if less than 3 meters and less than 4 seconds
      if (distKm < 0.003 && timeDiff < 4) {
        return;
      }
    }

    try {
      await apiClient.post('/providers/me/location', {
        booking_id: bookingId,
        latitude: coords.latitude,
        longitude: coords.longitude,
        heading: coords.heading || null,
        speed: coords.speed || null,
        accuracy: coords.accuracy || null,
        timestamp: new Date().toISOString(),
      });
      lastLocationSentRef.current = { lat: coords.latitude, lng: coords.longitude, time: now };
      setGpsCoordinates({
        latitude: coords.latitude,
        longitude: coords.longitude,
        accuracy: coords.accuracy,
        heading: coords.heading || undefined,
        speed: coords.speed || undefined,
      });
      setLocationPermission('granted');
      setLastGpsSync(new Date().toLocaleTimeString());
      setIsBroadcastingGps(true);
    } catch (err) {
      console.warn('GPS location post error:', err);
    }
  };

  // Trigger GPS read from browser (non-blocking, never halts booking pipeline)
  const triggerCurrentGps = (bookingId: string, force = true) => {
    try {
      if (!('geolocation' in navigator)) {
        setLocationPermission('unsupported');
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          sendLocation(bookingId, pos.coords, force).catch(() => {});
        },
        (err) => {
          if (err.code === err.PERMISSION_DENIED) {
            setLocationPermission('denied');
          }
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      );
    } catch (e) {
      console.warn('GPS trigger error ignored:', e);
    }
  };

  // Geolocation watch lifecycle while active booking exists
  useEffect(() => {
    if (!activeBooking) {
      setIsBroadcastingGps(false);
      return;
    }

    if (!('geolocation' in navigator)) {
      setLocationPermission('unsupported');
      return;
    }

    // Immediate initial sync
    triggerCurrentGps(activeBooking.id, true);

    // Watch position as device moves
    const watchId = navigator.geolocation.watchPosition(
      (pos) => {
        sendLocation(activeBooking.id, pos.coords);
      },
      (err) => {
        if (err.code === err.PERMISSION_DENIED) {
          setLocationPermission('denied');
        }
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 3000 }
    );

    // Regular interval sync every 6 seconds
    const interval = setInterval(() => {
      triggerCurrentGps(activeBooking.id, false);
    }, 6000);

    return () => {
      navigator.geolocation.clearWatch(watchId);
      clearInterval(interval);
    };
  }, [activeBooking?.id, activeBooking?.status]);

  useEffect(() => {
    fetchAll();

    let providerId = '';
    try {
      const rawUser = localStorage.getItem('smartserve_provider_user');
      if (rawUser) {
        const parsed = JSON.parse(rawUser);
        providerId = parsed.user_id || '';
      }
    } catch (e) {}

    const channels: string[] = [];
    if (providerId) {
      channels.push(`provider_${providerId}`, `user_${providerId}`);
    }

    const handleCustomBookingReceived = () => {
      fetchAll();
    };
    window.addEventListener('smartserve:booking_received', handleCustomBookingReceived);

    // Real-Time WebSocket Subscription (No Polling Required)
    const unsubscribeWs = subscribeToRealtime(channels, (payload) => {
      const type = payload.type || payload.event_type || payload.event;
      if (
        type === 'BOOKING_CREATED' ||
        type === 'BOOKING_ASSIGNED' ||
        type === 'BOOKING_ACCEPTED' ||
        type === 'BOOKING_REJECTED' ||
        type === 'BOOKING_STATUS_UPDATED' ||
        type === 'BOOKING_STARTED' ||
        type === 'BOOKING_COMPLETED' ||
        type === 'booking.created' ||
        type === 'booking.assigned' ||
        type === 'booking.accepted' ||
        type === 'booking.rejected' ||
        type === 'booking.updated' ||
        type === 'booking.started' ||
        type === 'booking.completed'
      ) {
        const targetId = String(payload.booking_id || payload.booking?.id || '');
        const newStatus = payload.status || payload.booking?.status;
        if (targetId && newStatus) {
          setBookings((prev) =>
            prev.map((b) => (String(b.id) === targetId ? { ...b, status: newStatus } : b))
          );
        }
        fetchAll();
      }
    });

    return () => {
      unsubscribeWs();
      window.removeEventListener('smartserve:booking_received', handleCustomBookingReceived);
    };
  }, []);

  const handleBookingAction = async (
    bookingId: string,
    action: 'accept' | 'reject' | 'start' | 'complete' | 'on_the_way' | 'arrived',
    customReason?: string,
    otpCode?: string
  ) => {
    setActionLoading(bookingId);
    setActionError(null);
    try {
      if (action === 'accept') {
        await apiClient.post(`/providers/me/bookings/${bookingId}/accept`);
        try { triggerCurrentGps(bookingId, true); } catch (e) {}
      } else if (action === 'reject') {
        const reasonToSend = (customReason || rejectionReason || 'Schedule conflict with another job').trim();
        await apiClient.post(`/providers/me/bookings/${bookingId}/reject`, {
          reason: reasonToSend,
        });
        setRejectingBooking(null);
      } else if (action === 'on_the_way') {
        await apiClient.patch(`/providers/me/bookings/${bookingId}/status`, {
          status: 'On The Way',
        });
        try { triggerCurrentGps(bookingId, true); } catch (e) {}
      } else if (action === 'arrived') {
        await apiClient.patch(`/providers/me/bookings/${bookingId}/status`, {
          status: 'Arrived',
        });
        try { triggerCurrentGps(bookingId, true); } catch (e) {}
      } else if (action === 'start') {
        try {
          await apiClient.post(`/providers/me/bookings/${bookingId}/start`, {
            otp_code: otpCode ? otpCode.trim() : undefined,
          });
          try { triggerCurrentGps(bookingId, true); } catch (e) {}
          setStartingBooking(null);
          setStartOtp('');
          setStartOtpError(null);
        } catch (err: any) {
          const detail = err.response?.data?.detail || 'Invalid service start OTP verification code.';
          setStartOtpError(detail);
          throw err;
        }
      } else if (action === 'complete') {
        try {
          await apiClient.post(`/providers/me/bookings/${bookingId}/complete`, {
            otp_code: otpCode ? otpCode.trim() : undefined,
          });
          setIsBroadcastingGps(false);
          setCompletingBooking(null);
          setCompleteOtp('');
          setCompleteOtpError(null);
        } catch (err: any) {
          const detail = err.response?.data?.detail || 'Invalid service completion OTP verification code.';
          setCompleteOtpError(detail);
          throw err;
        }
      }
      await fetchAll();
    } catch (err: any) {
      setActionError(err.response?.data?.detail || `Failed to ${action} booking.`);
    } finally {
      setActionLoading(null);
    }
  };

  const handleReportCashCollection = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!cashCollectionBooking) return;
    setCollectionLoading(true);
    setCollectionError(null);
    try {
      const parsedAmount = parseFloat(collectedAmount);
      if (isNaN(parsedAmount) || parsedAmount <= 0) {
        setCollectionError('Please enter a valid cash amount collected.');
        setCollectionLoading(false);
        return;
      }
      await apiClient.post(`/providers/me/bookings/${cashCollectionBooking.id}/cash-collected`, {
        reported_amount: parsedAmount,
        notes: collectionNotes.trim() || undefined,
      });
      setCollectionSuccess(`Cash collection of ₹${parsedAmount} reported successfully! Awaiting SmartServe Admin verification.`);
      setTimeout(() => {
        setCashCollectionBooking(null);
        setCollectionSuccess(null);
        setCollectedAmount('');
        setCollectionNotes('');
      }, 1500);
      await fetchAll();
    } catch (err: any) {
      setCollectionError(err.response?.data?.detail || 'Failed to report cash collection.');
    } finally {
      setCollectionLoading(false);
    }
  };


  if (loading) {
    return (
      <div className="min-h-[60vh] flex flex-col items-center justify-center space-y-4">
        <div className="w-10 h-10 border-4 border-[#2F5233] border-t-transparent rounded-full animate-spin" />
        <p className="text-sm font-semibold text-[#1F2A1E]">Loading SmartServe Partner Workspace...</p>
      </div>
    );
  }

  const isVerified = trust?.is_verified;
  const partnerFirstName = trust?.full_name ? trust.full_name.split(' ')[0] : 'Partner';

  const filteredBookings = bookings.filter((b) => {
    if (activeTab === 'all') return true;
    const s = (b.status || '').toLowerCase().replace(/_/g, ' ').trim();
    if (activeTab === 'pending') return s === 'requested' || s === 'assigned';
    if (activeTab === 'active') return ['accepted', 'on the way', 'arrived', 'started'].includes(s);
    if (activeTab === 'completed') return s === 'completed';
    return true;
  });

  const metricCards = [
    {
      title: "Today's Bookings",
      value: stats ? stats.today_bookings_count : 0,
      subtext: 'Manage schedule',
      link: '/availability',
      icon: Calendar,
      iconBg: 'bg-[#F2EDE1] text-[#2F5233]',
    },
    {
      title: 'Active Jobs',
      value: stats ? stats.active_jobs_count : 0,
      subtext: 'View active pipeline',
      link: '/dashboard',
      icon: Zap,
      iconBg: 'bg-purple-50 text-purple-700',
    },
    {
      title: 'Completed Jobs',
      value: stats ? stats.completed_jobs_count : 0,
      subtext: 'View history & ratings',
      link: '/profile',
      icon: CheckCircle2,
      iconBg: 'bg-emerald-50 text-emerald-700',
    },
    {
      title: 'Gross Earnings',
      value: stats ? `₹${parseFloat(stats.total_earnings || '0').toLocaleString('en-IN')}` : '₹0',
      subtext: 'View earnings ledger',
      link: '/profile',
      icon: IndianRupee,
      iconBg: 'bg-[#F2EDE1] text-[#C9A15A]',
    },
  ];

  return (
    <div className="space-y-8 font-sans">
      {/* ══════════════════════════════════════════════════
          1. GREETING & HERO HEADER
          ════════════════════════════════════════════════*/}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl sm:text-3xl font-serif text-[#1F2A1E] tracking-tight capitalize">
              Good morning, {partnerFirstName}!
            </h1>
            <span className="text-2xl">👋</span>
          </div>
          <p className="text-sm sm:text-base text-[#1F2A1E]/65 font-medium mt-1">
            Here's your partner schedule, job assignments, and reliability performance today.
          </p>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <button
            onClick={fetchAll}
            className="flex items-center gap-2 px-4 py-2.5 bg-white hover:bg-[#F2EDE1] text-[#1F2A1E] font-semibold text-xs sm:text-sm rounded-xl border border-[#E5DEC9] shadow-xs transition-colors cursor-pointer"
          >
            <RefreshCw className="w-4 h-4 text-[#1F2A1E]/60" />
            <span>Sync Live Pipeline</span>
          </button>

          <button
            onClick={() => navigate('/services')}
            className="flex items-center gap-2 px-5 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs sm:text-sm rounded-xl shadow-xs transition-colors cursor-pointer"
          >
            <Briefcase className="w-4 h-4" />
            <span>Manage My Services</span>
          </button>
        </div>
      </div>

      {/* ══════════════════════════════════════════════════
          2. VERIFICATION STATUS NOTIFICATION BANNER
          ════════════════════════════════════════════════*/}
      {!isVerified ? (
        <div className="p-5 rounded-3xl bg-amber-50/90 border border-amber-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xs">
          <div className="flex items-start gap-4">
            <div className="w-11 h-11 rounded-2xl bg-amber-100 text-amber-800 flex items-center justify-center shrink-0">
              <Clock className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-amber-900 font-serif">Account Under Verification Review</h3>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-200 text-amber-900 border border-amber-300">
                  Pending Review
                </span>
              </div>
              <p className="text-xs text-amber-800/80 mt-1 max-w-xl leading-relaxed">
                Your credentials are under manual review by the administrative verification team. You will receive booking notifications once approved.
              </p>
            </div>
          </div>
          <button
            onClick={() => navigate('/application-status')}
            className="px-4 py-2 rounded-xl bg-amber-700 hover:bg-amber-800 text-white font-bold text-xs shadow-xs transition-colors shrink-0"
          >
            View Application Status →
          </button>
        </div>
      ) : (
        <div className="p-5 rounded-3xl bg-emerald-50/80 border border-emerald-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 shadow-xs">
          <div className="flex items-center gap-4">
            <div className="w-11 h-11 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-emerald-950 font-serif">Verified Partner Account</h3>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">
                  Active & Booking-Eligible
                </span>
                {stats && stats.urgent_alerts_count > 0 && (
                  <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-100 text-rose-800 border border-rose-200 flex items-center gap-1">
                    <Bell className="w-3 h-3" />
                    {stats.urgent_alerts_count} Urgent Request
                  </span>
                )}
              </div>
              <p className="text-xs text-emerald-800/80 mt-1">
                Your portfolio, availability schedule, and pricing are published in the customer marketplace.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <span className="text-xs font-semibold text-emerald-800 bg-white px-3 py-1.5 rounded-xl border border-emerald-200">
              Auto-Dispatch: Enabled
            </span>
          </div>
        </div>
      )}

      {/* 2b. LOCATION PERMISSION DENIED WARNING BANNER */}
      {locationPermission === 'denied' && (
        <div className="p-5 rounded-3xl bg-rose-50 border border-rose-200 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 text-rose-900 shadow-xs">
          <div className="flex items-start gap-3">
            <div className="w-10 h-10 rounded-2xl bg-rose-100 flex items-center justify-center text-rose-700 shrink-0 mt-0.5">
              <AlertCircle className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-sm font-bold">Location Permission Required</h4>
              <p className="text-xs text-rose-700 mt-0.5 max-w-xl">
                Browser location access was denied. Please click the site settings / lock icon in your address bar and allow location permission so customers can view real dispatch telemetry.
              </p>
            </div>
          </div>
          <button
            onClick={() => activeBooking && triggerCurrentGps(activeBooking.id)}
            className="px-4 py-2 bg-rose-700 hover:bg-rose-800 text-white font-bold text-xs rounded-xl transition-colors shrink-0"
          >
            Retry GPS Permission
          </button>
        </div>
      )}

      {/* 2c. ACTIVE DISPATCH & REAL LIVE GPS TELEMETRY CARD */}
      {activeBooking && (
        <div className="p-5 sm:p-6 rounded-3xl bg-gradient-to-r from-[#1F2A1E] via-[#2F5233] to-[#1F2A1E] text-white border border-[#3D6B42] shadow-md flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start sm:items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center text-emerald-400 shrink-0">
              <Radio className="w-6 h-6 animate-pulse text-emerald-400" />
            </div>
            <div>
              <div className="flex items-center gap-2 flex-wrap">
                <span className="font-mono text-xs font-bold text-emerald-300 bg-white/10 px-2 py-0.5 rounded-lg border border-white/20">
                  {activeBooking.booking_reference}
                </span>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase bg-emerald-400/20 text-emerald-200 border border-emerald-400/30">
                  {activeBooking.status}
                </span>
                <span className="flex items-center gap-1.5 text-[10px] font-bold text-emerald-300 bg-white/10 px-2.5 py-0.5 rounded-full border border-white/15">
                  <span className={`w-2 h-2 rounded-full ${isBroadcastingGps ? 'bg-emerald-400 animate-ping' : 'bg-amber-400'}`}></span>
                  <span>{isBroadcastingGps ? 'Broadcasting Real GPS Live' : 'Connecting GPS Stream...'}</span>
                </span>
              </div>
              <h3 className="text-base sm:text-lg font-extrabold text-white mt-1">
                {activeBooking.service_name} • {activeBooking.customer_name}
              </h3>
              <p className="text-xs text-white/70 flex items-center gap-1.5 mt-0.5">
                <MapPin className="w-3.5 h-3.5 text-emerald-300" />
                <span>{activeBooking.address || 'Customer destination on file'}</span>
              </p>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row sm:items-center gap-3">
            {gpsCoordinates ? (
              <div className="bg-white/10 px-4 py-2 rounded-2xl border border-white/15 text-left sm:text-right font-mono text-[11px]">
                <span className="text-white/60 block text-[9px] uppercase font-sans font-bold">Device GPS Coordinates</span>
                <span className="text-emerald-300 font-bold">
                  {gpsCoordinates.latitude.toFixed(4)}, {gpsCoordinates.longitude.toFixed(4)}
                </span>
                {lastGpsSync && <span className="text-white/50 block text-[9px] font-sans">Synced {lastGpsSync}</span>}
              </div>
            ) : (
              <div className="text-xs text-emerald-200/80 bg-white/10 px-3.5 py-2 rounded-2xl border border-white/15">
                Acquiring GPS fix...
              </div>
            )}
            {(() => {
              const s = (activeBooking.status || '').toLowerCase().replace(/_/g, ' ').trim();
              if (s === 'accepted') {
                return (
                  <button
                    onClick={() => handleBookingAction(activeBooking.id, 'on_the_way')}
                    disabled={actionLoading === activeBooking.id}
                    className="flex items-center justify-center gap-1.5 px-4 py-2.5 bg-sky-500 hover:bg-sky-600 text-white font-bold text-xs rounded-xl shadow-xs transition-colors shrink-0 disabled:opacity-50"
                  >
                    <Navigation className="w-4 h-4" />
                    <span>{actionLoading === activeBooking.id ? 'Updating...' : 'Start Trip (On The Way)'}</span>
                  </button>
                );
              }
              if (s === 'on the way') {
                return (
                  <button
                    onClick={() => handleBookingAction(activeBooking.id, 'arrived')}
                    disabled={actionLoading === activeBooking.id}
                    className="flex items-center justify-center gap-1.5 px-4 py-2.5 bg-teal-500 hover:bg-teal-600 text-white font-bold text-xs rounded-xl shadow-xs transition-colors shrink-0 disabled:opacity-50"
                  >
                    <MapPin className="w-4 h-4" />
                    <span>{actionLoading === activeBooking.id ? 'Updating...' : 'Mark Arrived'}</span>
                  </button>
                );
              }
              if (s === 'arrived') {
                return (
                  <button
                    onClick={() => {
                      setStartingBooking(activeBooking);
                      setStartOtp('');
                      setStartOtpError(null);
                    }}
                    disabled={actionLoading === activeBooking.id}
                    className="flex items-center justify-center gap-1.5 px-4 py-2.5 bg-purple-500 hover:bg-purple-600 text-white font-bold text-xs rounded-xl shadow-xs transition-colors shrink-0 disabled:opacity-50"
                  >
                    <Play className="w-4 h-4" />
                    <span>Start Service (Enter OTP)</span>
                  </button>
                );
              }
              if (s === 'started') {
                return (
                  <button
                    onClick={() => handleBookingAction(activeBooking.id, 'complete')}
                    disabled={actionLoading === activeBooking.id}
                    className="flex items-center justify-center gap-1.5 px-4 py-2.5 bg-emerald-500 hover:bg-emerald-600 text-white font-bold text-xs rounded-xl shadow-xs transition-colors shrink-0 disabled:opacity-50"
                  >
                    <CheckCircle2 className="w-4 h-4" />
                    <span>{actionLoading === activeBooking.id ? 'Completing...' : 'Complete Service'}</span>
                  </button>
                );
              }
              return null;
            })()}
            <button
              onClick={() => triggerCurrentGps(activeBooking.id)}
              className="flex items-center justify-center gap-1.5 px-4 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors shrink-0"
            >
              <Compass className="w-4 h-4" />
              <span>Ping GPS Now</span>
            </button>
          </div>
        </div>
      )}

      {/* ══════════════════════════════════════════════════
          3. METRIC CARDS
          ════════════════════════════════════════════════*/}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
        {metricCards.map((card) => {
          const Icon = card.icon;
          return (
            <div
              key={card.title}
              onClick={() => navigate(card.link)}
              className="group bg-white p-5 sm:p-6 rounded-3xl border border-[#E5DEC9] shadow-xs hover:shadow-md hover:border-[#2F5233]/40 transition-all cursor-pointer flex flex-col justify-between"
            >
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-[#1F2A1E]/50 block mb-1">
                    {card.title}
                  </span>
                  <p className="text-2xl sm:text-3xl font-extrabold text-[#1F2A1E] tracking-tight font-serif">
                    {card.value}
                  </p>
                </div>
                <div className={`p-3 rounded-2xl ${card.iconBg} flex-shrink-0 border border-[#E5DEC9]/40`}>
                  <Icon className="w-5 h-5 sm:w-6 sm:h-6" />
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-[#E5DEC9]/60 flex items-center justify-between text-xs font-bold text-[#2F5233] group-hover:translate-x-0.5 transition-transform">
                <span>{card.subtext}</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          );
        })}
      </div>

      {/* ══════════════════════════════════════════════════
          4. PARTNER EXCELLENCE & INCENTIVES BANNER
          ════════════════════════════════════════════════*/}
      <div className="relative rounded-3xl overflow-hidden bg-gradient-to-r from-[#1F2A1E] via-[#243523] to-[#2F5233] text-white p-6 sm:p-8 lg:p-10 shadow-sm border border-[#1F2A1E]">
        <div className="relative z-10 max-w-xl space-y-3">
          <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#C9A15A]/20 text-[#C9A15A] border border-[#C9A15A]/30 text-xs font-bold uppercase tracking-wider">
            <Award className="w-3.5 h-3.5" />
            Partner Excellence Program
          </span>
          <h3 className="text-2xl sm:text-3xl font-serif tracking-tight leading-tight">
            Tier 1 Elite Matching Guarantee
          </h3>
          <p className="text-sm text-white/80 font-medium leading-relaxed">
            Maintain a 98%+ reliability score and under-15-minute response time to receive automated top-rank job routing and 0% cancellation penalty buffers.
          </p>
          <div className="pt-2 flex items-center gap-3">
            <button
              onClick={() => navigate('/profile')}
              className="px-5 py-2.5 bg-[#C9A15A] hover:bg-[#b58f4a] text-[#1F2A1E] font-bold text-xs rounded-xl shadow-xs transition-colors cursor-pointer"
            >
              View Trust Score Breakdown
            </button>
            <span className="text-xs text-white/60">Updated hourly from verified customer ratings</span>
          </div>
        </div>
      </div>

      {/* ══════════════════════════════════════════════════
          5. MAIN WORKSPACE: BOOKINGS + SIDEBAR
          ════════════════════════════════════════════════*/}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Columns: Bookings Pipeline */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-xs overflow-hidden">
            {/* Header with Title & Action */}
            <div className="p-6 border-b border-[#E5DEC9] flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 className="text-lg font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-[#2F5233]" />
                  <span>Assigned Job Pipeline</span>
                </h3>
                <p className="text-xs text-[#1F2A1E]/60 mt-0.5">
                  Accept incoming requests, verify completion OTP codes, and monitor job progress.
                </p>
              </div>

              {/* Filter Tabs */}
              <div className="flex gap-1 bg-[#FAF7F0] p-1 rounded-2xl border border-[#E5DEC9]">
                {(['all', 'pending', 'active', 'completed'] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setActiveTab(tab)}
                    className={`px-3 py-1.5 text-xs font-bold rounded-xl capitalize transition-all ${
                      activeTab === tab
                        ? 'bg-[#2F5233] text-white shadow-xs'
                        : 'text-[#1F2A1E]/60 hover:text-[#1F2A1E]'
                    }`}
                  >
                    {tab}
                  </button>
                ))}
              </div>
            </div>

            {/* Error Notification */}
            {actionError && (
              <div className="mx-6 mt-4 p-3.5 rounded-2xl bg-red-50 border border-red-200 text-xs text-red-800 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
                <span>{actionError}</span>
              </div>
            )}

            {/* Bookings List */}
            <div className="p-6">
              {filteredBookings.length === 0 ? (
                <div className="text-center py-12 rounded-2xl bg-[#FAF7F0] border border-dashed border-[#E5DEC9] space-y-2">
                  <Calendar className="w-8 h-8 text-[#1F2A1E]/30 mx-auto" />
                  <p className="text-sm font-bold text-[#1F2A1E]">No bookings in this filter</p>
                  <p className="text-xs text-[#1F2A1E]/50 max-w-sm mx-auto">
                    New customer bookings matched to your category and schedule will automatically appear here.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {filteredBookings.map((booking) => (
                    <div
                      key={booking.id}
                      className={`p-5 rounded-2xl border transition-all ${
                        booking.emergency_flag === 'EMERGENCY'
                          ? 'bg-rose-50/40 border-rose-200 hover:border-rose-300'
                          : 'bg-[#FAF7F0] border-[#E5DEC9] hover:border-[#2F5233]/40'
                      }`}
                    >
                      {/* Booking Top Info */}
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-3">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-mono text-xs font-bold text-[#2F5233] bg-white px-2.5 py-1 rounded-lg border border-[#E5DEC9]">
                            {booking.booking_reference}
                          </span>
                          <span
                            className={`text-[11px] font-bold px-3 py-0.5 rounded-full border ${
                              STATUS_STYLES[booking.status] || 'bg-slate-50 text-slate-700 border-slate-200'
                            }`}
                          >
                            {booking.status}
                          </span>
                          <span
                            className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full border ${
                              (booking.payment_status || '').toLowerCase() === 'paid'
                                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                                : (booking.payment_status || '').toLowerCase() === 'collection reported'
                                ? 'bg-amber-50 text-amber-700 border-amber-200'
                                : (booking.payment_status || '').toLowerCase() === 'rejected'
                                ? 'bg-rose-50 text-rose-700 border-rose-200'
                                : 'bg-slate-50 text-slate-600 border-slate-200'
                            }`}
                          >
                            COD: {booking.payment_status || 'Pending'}
                          </span>
                          {booking.emergency_flag === 'EMERGENCY' && (
                            <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-800 border border-rose-200 flex items-center gap-1">
                              <Zap className="w-3 h-3 text-rose-600" />
                              Emergency Dispatch
                            </span>
                          )}
                          {(booking.customer_notes?.includes('CB-') || booking.customer_notes?.includes('Bundle')) && (
                            <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-purple-50 text-purple-800 border border-purple-200 flex items-center gap-1">
                              <span>✨</span> Multi-Service Bundle
                            </span>
                          )}
                        </div>
                        <span className="text-sm font-extrabold text-[#1F2A1E] font-serif">
                          ₹{parseFloat(booking.total_price || 0).toLocaleString('en-IN')}
                        </span>
                      </div>

                      {/* Booking Details Grid */}
                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs mb-4">
                        <div>
                          <span className="text-[#1F2A1E]/50 block font-medium">Service</span>
                          <span className="font-bold text-[#1F2A1E] block truncate">{booking.service_name}</span>
                        </div>
                        <div>
                          <span className="text-[#1F2A1E]/50 block font-medium">Customer</span>
                          <span className="font-bold text-[#1F2A1E] block truncate">{booking.customer_name}</span>
                        </div>
                        <div>
                          <span className="text-[#1F2A1E]/50 block font-medium">Scheduled Time</span>
                          <span className="font-semibold text-[#1F2A1E]">
                            {booking.scheduled_time
                              ? new Date(booking.scheduled_time).toLocaleString('en-IN', {
                                  day: '2-digit',
                                  month: 'short',
                                  hour: '2-digit',
                                  minute: '2-digit',
                                })
                              : 'TBD'}
                          </span>
                        </div>
                        <div>
                          <span className="text-[#1F2A1E]/50 block font-medium">Location</span>
                          <span className="font-semibold text-[#1F2A1E] truncate block">
                            {booking.address || 'Address on file'}
                          </span>
                        </div>
                      </div>

                      {/* Customer Notes / Access Instructions */}
                      {booking.customer_notes && (
                        <div className="mb-4 p-3 bg-amber-50/80 border border-amber-200/90 rounded-2xl text-xs space-y-1">
                          <div className="flex items-center gap-1.5 font-bold text-amber-900">
                            <FileText className="w-3.5 h-3.5 text-amber-700" />
                            <span>{t('dashboard.customer_notes_title', { defaultValue: 'Customer Notes / Access Instructions' })}</span>
                          </div>
                          <p className="text-amber-800 whitespace-pre-wrap leading-relaxed">{booking.customer_notes}</p>
                        </div>
                      )}

                      {/* Job Verification Photos Section */}
                      <div className="mb-4 p-3.5 bg-white border border-[#E5DEC9] rounded-2xl space-y-3">
                        <div className="flex items-center justify-between flex-wrap gap-2">
                          <div className="flex items-center gap-1.5 font-bold text-xs text-[#1F2A1E]">
                            <Camera className="w-3.5 h-3.5 text-[#2F5233]" />
                            <span>{t('dashboard.photos_title', { defaultValue: 'Job Verification Photos (Before & After)' })}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <label className="inline-flex items-center gap-1 px-2.5 py-1 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#2F5233] text-[11px] font-bold rounded-lg cursor-pointer transition-colors border border-[#E5DEC9]">
                              <Upload className="w-3 h-3" />
                              <span>+ {t('dashboard.upload_before', { defaultValue: 'Before Photo' })}</span>
                              <input
                                type="file"
                                accept="image/*"
                                capture="environment"
                                className="hidden"
                                disabled={photoUploadingBookingId === booking.id}
                                onChange={(e) => {
                                  const file = e.target.files?.[0];
                                  if (file) handlePhotoUpload(booking.id, 'before', file);
                                  e.target.value = '';
                                }}
                              />
                            </label>
                            <label className="inline-flex items-center gap-1 px-2.5 py-1 bg-[#2F5233] hover:bg-[#3D6B42] text-white text-[11px] font-bold rounded-lg cursor-pointer transition-colors shadow-2xs">
                              <Upload className="w-3 h-3" />
                              <span>+ {t('dashboard.upload_after', { defaultValue: 'After Photo' })}</span>
                              <input
                                type="file"
                                accept="image/*"
                                capture="environment"
                                className="hidden"
                                disabled={photoUploadingBookingId === booking.id}
                                onChange={(e) => {
                                  const file = e.target.files?.[0];
                                  if (file) handlePhotoUpload(booking.id, 'after', file);
                                  e.target.value = '';
                                }}
                              />
                            </label>
                          </div>
                        </div>

                        {photoUploadingBookingId === booking.id && (
                          <div className="flex items-center gap-2 text-xs text-[#2F5233] font-semibold">
                            <span className="w-3 h-3 border-2 border-[#2F5233] border-t-transparent rounded-full animate-spin" />
                            <span>Uploading verification proof photo...</span>
                          </div>
                        )}

                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                          {/* Before Photos Gallery */}
                          <div className="space-y-1.5">
                            <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500 flex items-center gap-1">
                              <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                              {t('dashboard.before_photos', { defaultValue: 'Before Service' })} ({booking.before_photos?.length || 0})
                            </span>
                            {booking.before_photos && booking.before_photos.length > 0 ? (
                              <div className="flex items-center gap-2 flex-wrap">
                                {booking.before_photos.map((url: string, idx: number) => {
                                  const fullUrl = resolvePhotoUrl(url);
                                  return (
                                    <button
                                      key={idx}
                                      type="button"
                                      onClick={() => setPreviewPhotoUrl(fullUrl)}
                                      className="relative w-12 h-12 rounded-xl overflow-hidden border border-amber-200 group cursor-pointer shadow-2xs hover:scale-105 transition-transform"
                                    >
                                      <img
                                        src={fullUrl}
                                        alt={`Before ${idx + 1}`}
                                        className="w-full h-full object-cover"
                                        onError={(e) => {
                                          e.currentTarget.onerror = null;
                                          e.currentTarget.src = 'https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=400&q=80';
                                        }}
                                      />
                                      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity text-white">
                                        <Eye className="w-3.5 h-3.5" />
                                      </div>
                                    </button>
                                  );
                                })}
                              </div>
                            ) : (
                              <p className="text-[10px] text-slate-400 italic">No before photos added</p>
                            )}
                          </div>

                          {/* After Photos Gallery */}
                          <div className="space-y-1.5">
                            <span className="text-[10px] font-bold uppercase tracking-wider text-emerald-700 flex items-center gap-1">
                              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                              {t('dashboard.after_photos', { defaultValue: 'After Service' })} ({booking.after_photos?.length || 0})
                            </span>
                            {booking.after_photos && booking.after_photos.length > 0 ? (
                              <div className="flex items-center gap-2 flex-wrap">
                                {booking.after_photos.map((url: string, idx: number) => {
                                  const fullUrl = resolvePhotoUrl(url);
                                  return (
                                    <button
                                      key={idx}
                                      type="button"
                                      onClick={() => setPreviewPhotoUrl(fullUrl)}
                                      className="relative w-12 h-12 rounded-xl overflow-hidden border border-emerald-200 group cursor-pointer shadow-2xs hover:scale-105 transition-transform"
                                    >
                                      <img
                                        src={fullUrl}
                                        alt={`After ${idx + 1}`}
                                        className="w-full h-full object-cover"
                                        onError={(e) => {
                                          e.currentTarget.onerror = null;
                                          e.currentTarget.src = 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=400&q=80';
                                        }}
                                      />
                                      <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity text-white">
                                        <Eye className="w-3.5 h-3.5" />
                                      </div>
                                    </button>
                                  );
                                })}
                              </div>
                            ) : (
                              <p className="text-[10px] text-slate-400 italic">No after photos added</p>
                            )}
                          </div>
                        </div>
                      </div>

                      {/* Action Buttons */}
                      <div className="flex gap-2 flex-wrap pt-2 border-t border-[#E5DEC9]/60">
                        {(() => {
                          const s = (booking.status || '').toLowerCase().replace(/_/g, ' ').trim();
                          if (s === 'requested' || s === 'assigned') {
                            return (
                              <>
                                <button
                                  onClick={() => handleBookingAction(booking.id, 'accept')}
                                  disabled={actionLoading === booking.id}
                                  className="flex items-center gap-1.5 px-4 py-2 bg-[#2F5233] text-white text-xs font-bold rounded-xl hover:bg-[#3D6B42] transition-colors disabled:opacity-50"
                                >
                                  <CheckCircle2 className="w-3.5 h-3.5" />
                                  <span>{actionLoading === booking.id ? 'Accepting...' : 'Accept Job'}</span>
                                </button>
                                <button
                                  onClick={() => setRejectingBooking(booking)}
                                  disabled={actionLoading === booking.id}
                                  className="px-4 py-2 bg-rose-50 text-rose-700 border border-rose-200 text-xs font-bold rounded-xl hover:bg-rose-100 transition-colors disabled:opacity-50"
                                >
                                  Decline
                                </button>
                              </>
                            );
                          }
                          if (s === 'accepted') {
                            return (
                              <button
                                onClick={() => handleBookingAction(booking.id, 'on_the_way')}
                                disabled={actionLoading === booking.id}
                                className="flex items-center gap-1.5 px-4 py-2 bg-sky-700 text-white text-xs font-bold rounded-xl hover:bg-sky-800 transition-colors disabled:opacity-50"
                              >
                                <Navigation className="w-3.5 h-3.5" />
                                <span>{actionLoading === booking.id ? 'Updating...' : 'Start Trip (On The Way)'}</span>
                              </button>
                            );
                          }
                          if (s === 'on the way') {
                            return (
                              <div className="flex items-center gap-2 flex-wrap">
                                {import.meta.env.DEV && (
                                  <button
                                    onClick={() => handleDevSimulateRoute(booking)}
                                    className={`flex items-center gap-1.5 px-3 py-2 text-xs font-bold rounded-xl border transition-all ${
                                      devSimulatingBookingId === booking.id
                                        ? 'bg-amber-600 text-white border-amber-700 animate-pulse'
                                        : 'bg-slate-900 text-amber-300 border-amber-500/40 hover:bg-slate-800'
                                    }`}
                                  >
                                    <Navigation className="w-3.5 h-3.5" />
                                    <span>{devSimulatingBookingId === booking.id ? 'Pause DEV Sim' : 'DEV Sim Trip'}</span>
                                  </button>
                                )}
                                <button
                                  onClick={() => handleBookingAction(booking.id, 'arrived')}
                                  disabled={actionLoading === booking.id}
                                  className="flex items-center gap-1.5 px-4 py-2 bg-teal-700 text-white text-xs font-bold rounded-xl hover:bg-teal-800 transition-colors disabled:opacity-50"
                                >
                                  <MapPin className="w-3.5 h-3.5" />
                                  <span>{actionLoading === booking.id ? 'Updating...' : 'Mark Arrived'}</span>
                                </button>
                              </div>
                            );
                          }
                          if (s === 'arrived') {
                            return (
                              <button
                                onClick={() => {
                                  setStartingBooking(booking);
                                  setStartOtp('');
                                  setStartOtpError(null);
                                }}
                                disabled={actionLoading === booking.id}
                                className="flex items-center gap-1.5 px-4 py-2 bg-purple-700 text-white text-xs font-bold rounded-xl hover:bg-purple-800 transition-colors disabled:opacity-50"
                              >
                                <Play className="w-3.5 h-3.5" />
                                <span>Start Service (Enter OTP)</span>
                              </button>
                            );
                          }
                          if (s === 'started') {
                            return (
                              <div className="flex items-center gap-2 flex-wrap">
                                <button
                                  onClick={() => {
                                    setCompletingBooking(booking);
                                    setCompleteOtp('');
                                    setCompleteOtpError(null);
                                  }}
                                  disabled={actionLoading === booking.id}
                                  className="flex items-center gap-1.5 px-4 py-2 bg-emerald-600 text-white text-xs font-bold rounded-xl hover:bg-emerald-700 transition-colors disabled:opacity-50"
                                >
                                  <CheckCircle2 className="w-3.5 h-3.5" />
                                  <span>Complete Service (Enter OTP)</span>
                                </button>
                                {booking.payment_status !== 'Paid' && booking.payment_status !== 'Collection Reported' ? (
                                  <button
                                    onClick={() => {
                                      setCashCollectionBooking(booking);
                                      setCollectedAmount(String(booking.total_price || ''));
                                      setCollectionNotes('');
                                      setCollectionError(null);
                                      setCollectionSuccess(null);
                                    }}
                                    className="flex items-center gap-1.5 px-4 py-2 bg-[#2F5233] text-white text-xs font-bold rounded-xl hover:bg-[#3D6B42] transition-colors shadow-xs"
                                  >
                                    <Banknote className="w-3.5 h-3.5" />
                                    <span>Mark Cash Collected (₹{booking.total_price || 0})</span>
                                  </button>
                                ) : booking.payment_status === 'Collection Reported' ? (
                                  <div className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 border border-amber-300 text-amber-800 rounded-xl text-xs font-semibold">
                                    <Clock className="w-3.5 h-3.5 text-amber-600" />
                                    <span>Collection Reported • Awaiting Verification</span>
                                  </div>
                                ) : booking.payment_status === 'Paid' ? (
                                  <div className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 border border-emerald-300 text-emerald-800 rounded-xl text-xs font-bold">
                                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                                    <span>Payment Verified & Settled</span>
                                  </div>
                                ) : null}
                              </div>
                            );
                          }
                          if (s === 'completed') {
                            return (
                              <div className="flex items-center gap-2 flex-wrap">
                                {booking.payment_status !== 'Paid' && booking.payment_status !== 'Collection Reported' ? (
                                  <button
                                    onClick={() => {
                                      setCashCollectionBooking(booking);
                                      setCollectedAmount(String(booking.total_price || ''));
                                      setCollectionNotes('');
                                      setCollectionError(null);
                                      setCollectionSuccess(null);
                                    }}
                                    className="flex items-center gap-1.5 px-4 py-2 bg-[#2F5233] text-white text-xs font-bold rounded-xl hover:bg-[#3D6B42] transition-colors shadow-xs"
                                  >
                                    <Banknote className="w-3.5 h-3.5" />
                                    <span>Mark Cash Collected (₹{booking.total_price || 0})</span>
                                  </button>
                                ) : booking.payment_status === 'Collection Reported' ? (
                                  <div className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 border border-amber-300 text-amber-800 rounded-xl text-xs font-semibold">
                                    <Clock className="w-3.5 h-3.5 text-amber-600" />
                                    <span>Cash Collection Reported • Awaiting Admin Verification</span>
                                  </div>
                                ) : booking.payment_status === 'Paid' ? (
                                  <div className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 border border-emerald-300 text-emerald-800 rounded-xl text-xs font-bold">
                                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                                    <span>Payment Verified & Settled</span>
                                  </div>
                                ) : null}
                              </div>
                            );
                          }
                          return null;
                        })()}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

          </div>
        </div>

        {/* Right 1 Column: Profile & Trust Card */}
        <div className="space-y-6">
          {trust && (
            <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-xs p-6 relative">
              {trust.is_verified && (
                <div className="absolute top-4 right-4 bg-[#2F5233] text-white px-3 py-1 text-[10px] font-bold uppercase rounded-full shadow-2xs flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" />
                  <span>Verified</span>
                </div>
              )}

              {/* Avatar & Bio */}
              <div className="flex flex-col items-center text-center mb-6 pt-2">
                <div className="w-20 h-20 rounded-2xl border border-[#E5DEC9] shadow-xs overflow-hidden mb-3 bg-[#FAF7F0] flex items-center justify-center text-2xl font-serif font-bold text-[#2F5233]">
                  {trust.photo_url ? (
                    <img src={trust.photo_url} alt="Profile" className="w-full h-full object-cover" />
                  ) : (
                    <span>{trust.full_name.charAt(0)}</span>
                  )}
                </div>
                <h3 className="font-bold text-[#1F2A1E] text-base font-serif">{trust.full_name}</h3>
                <p className="text-xs text-[#7A9E6E] font-semibold mt-0.5">
                  {trust.category?.replace(/^\d+\.\s*/, '') || 'Service Partner'}
                </p>
                <div className="flex items-center gap-1 mt-1 text-[11px] text-[#1F2A1E]/60">
                  <MapPin className="w-3.5 h-3.5 text-[#C9A15A]" />
                  <span>{trust.service_area || 'Bengaluru, India'}</span>
                </div>
              </div>

              {/* Trust Metrics */}
              <div className="space-y-2 text-xs border-t border-[#E5DEC9] pt-4">
                <div className="flex justify-between py-2 border-b border-slate-50">
                  <span className="text-[#1F2A1E]/70 flex items-center gap-1.5 font-medium">
                    <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                    <span>Reliability Score</span>
                  </span>
                  <span className="font-bold text-emerald-700">{trust.reliability_score}%</span>
                </div>
                <div className="flex justify-between py-2 border-b border-slate-50">
                  <span className="text-[#1F2A1E]/70 font-medium">Acceptance Rate</span>
                  <span className="font-bold text-[#1F2A1E]">{trust.acceptance_rate}%</span>
                </div>
                <div className="flex justify-between py-2 border-b border-slate-50">
                  <span className="text-[#1F2A1E]/70 font-medium">On-Time Arrival</span>
                  <span className="font-bold text-[#1F2A1E]">{trust.on_time_rate}%</span>
                </div>
                <div className="flex justify-between py-2 border-b border-slate-50">
                  <span className="text-[#1F2A1E]/70 font-medium">Cancellation Rate</span>
                  <span className="font-bold text-slate-500">{trust.cancellation_rate}%</span>
                </div>
                <div className="flex justify-between py-2 border-b border-slate-50">
                  <span className="text-[#1F2A1E]/70 flex items-center gap-1.5 font-medium">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                    <span>Completed Jobs</span>
                  </span>
                  <span className="font-bold text-[#1F2A1E]">{trust.completed_jobs_count}</span>
                </div>
                <div className="flex justify-between py-2">
                  <span className="text-[#1F2A1E]/70 flex items-center gap-1.5 font-medium">
                    <FileCheck className="w-3.5 h-3.5 text-[#2F5233]" />
                    <span>Verified Documents</span>
                  </span>
                  <span className="font-bold text-[#2F5233]">{trust.certificates_count} on file</span>
                </div>
              </div>

              {/* Action Link */}
              <div className="mt-5 pt-3 border-t border-[#E5DEC9]">
                <button
                  onClick={() => navigate('/profile')}
                  className="w-full py-2.5 rounded-xl bg-[#FAF7F0] hover:bg-[#F2EDE1] text-[#1F2A1E] font-bold text-xs border border-[#E5DEC9] transition-colors flex items-center justify-center gap-1.5"
                >
                  <span>View Complete Partner Profile</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          )}

          {/* Quick Links Card */}
          <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-xs p-5 space-y-1">
            <span className="text-[10px] font-bold text-[#1F2A1E]/40 uppercase tracking-wider block px-2 mb-2">
              Partner Utilities
            </span>
            {[
              { label: 'My Offered Services', path: '/services', icon: Briefcase },
              { label: 'Calendar & Available Hours', path: '/availability', icon: Calendar },
              { label: 'Trust & Verification Dossier', path: '/profile', icon: User },
              { label: 'Support & Help Desk', path: '/support', icon: LifeBuoy },
            ].map((item) => (
              <button
                key={item.path}
                onClick={() => navigate(item.path)}
                className="w-full flex items-center justify-between p-3 rounded-2xl text-xs font-semibold text-[#1F2A1E]/75 hover:bg-[#FAF7F0] hover:text-[#2F5233] transition-colors group text-left"
              >
                <div className="flex items-center gap-2.5">
                  <item.icon className="w-4 h-4 text-[#2F5233]" />
                  <span>{item.label}</span>
                </div>
                <ChevronRight className="w-3.5 h-3.5 text-[#1F2A1E]/30 group-hover:text-[#2F5233] group-hover:translate-x-0.5 transition-transform" />
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Mandatory Rejection Reason Modal */}
      {rejectingBooking && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 space-y-5 shadow-2xl border border-[#E5DEC9]">
            <div className="flex items-start justify-between border-b border-[#E5DEC9]/60 pb-3">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-rose-50 border border-rose-200 flex items-center justify-center text-rose-600">
                  <XCircle className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Decline Service Request</h3>
                  <p className="text-[11px] text-[#1F2A1E]/60 font-mono">
                    {rejectingBooking.reference || rejectingBooking.booking_reference || rejectingBooking.id}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => setRejectingBooking(null)}
                className="text-[#1F2A1E]/40 hover:text-[#1F2A1E] p-1 rounded-full hover:bg-black/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-3 bg-[#FAF7F0] rounded-xl border border-[#E5DEC9] text-xs space-y-1">
              <p className="font-bold text-[#1F2A1E]">{rejectingBooking.service_name}</p>
              <p className="text-[#1F2A1E]/70">Customer: <span className="font-semibold">{rejectingBooking.customer_name}</span></p>
              <p className="text-[#1F2A1E]/70">Schedule: <span className="font-semibold">{rejectingBooking.scheduled_date} at {rejectingBooking.scheduled_time}</span></p>
            </div>

            <div className="space-y-3">
              <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider">
                Rejection Reason (Required) *
              </label>

              <select
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                className="w-full text-xs font-medium bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2.5 text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
              >
                <option value="Schedule conflict with another job">Schedule conflict with another job</option>
                <option value="Outside service travel radius / transit delay">Outside service travel radius / transit delay</option>
                <option value="Required tools or equipment currently unavailable">Required tools or equipment currently unavailable</option>
                <option value="Personal emergency / urgent leave">Personal emergency / urgent leave</option>
                <option value="Custom Reason">Custom Reason...</option>
              </select>

              <textarea
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                placeholder="Enter detailed reason for declining this request..."
                rows={3}
                required
                className="w-full text-xs font-medium bg-white border border-[#E5DEC9] rounded-xl p-3 text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
              />
              <p className="text-[11px] text-[#1F2A1E]/50">
                This reason will be recorded on the booking, communicated to the customer, and visible to operations admin.
              </p>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setRejectingBooking(null)}
                className="px-4 py-2 bg-[#FAF7F0] hover:bg-[#F2EDE1] text-[#1F2A1E] font-bold text-xs rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={!rejectionReason.trim() || actionLoading === rejectingBooking.id}
                onClick={() => handleBookingAction(rejectingBooking.id, 'reject', rejectionReason.trim())}
                className="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors disabled:opacity-50 flex items-center gap-1.5"
              >
                {actionLoading === rejectingBooking.id ? 'Declining...' : 'Confirm Decline'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Service Start OTP Verification Modal */}
      {startingBooking && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 space-y-5 shadow-2xl border border-[#E5DEC9]">
            <div className="flex items-start justify-between border-b border-[#E5DEC9]/60 pb-3">
              <div className="flex items-center gap-2.5">
                <div className="w-10 h-10 rounded-2xl bg-purple-50 border border-purple-200 flex items-center justify-center text-purple-700 shadow-xs">
                  <KeyRound className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Verify Start OTP</h3>
                  <p className="text-[11px] text-[#1F2A1E]/60 font-mono">
                    {startingBooking.reference || startingBooking.booking_reference || startingBooking.id}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => {
                  setStartingBooking(null);
                  setStartOtp('');
                  setStartOtpError(null);
                }}
                className="text-[#1F2A1E]/40 hover:text-[#1F2A1E] p-1 rounded-full hover:bg-black/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-3 bg-[#FAF7F0] rounded-xl border border-[#E5DEC9] text-xs space-y-1">
              <p className="font-bold text-[#1F2A1E]">{startingBooking.service_name}</p>
              <p className="text-[#1F2A1E]/70">Customer: <span className="font-semibold">{startingBooking.customer_name}</span></p>
            </div>

            {startOtpError && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                <span>{startOtpError}</span>
              </div>
            )}

            <div className="space-y-3">
              <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider">
                Enter 4-Digit Customer Start OTP
              </label>
              <input
                data-testid="start-otp-input"
                type="text"
                maxLength={6}
                value={startOtp}
                onChange={(e) => {
                  setStartOtp(e.target.value);
                  setStartOtpError(null);
                }}
                placeholder="4-digit OTP"
                className="w-full text-center font-mono text-2xl tracking-widest bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-3 text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
              />
              <p className="text-[11px] text-[#1F2A1E]/60">
                The customer has received this code on their live tracking screen upon your arrival. You must verify this OTP before initiating the service.
              </p>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => {
                  setStartingBooking(null);
                  setStartOtp('');
                  setStartOtpError(null);
                }}
                className="px-4 py-2 bg-[#FAF7F0] hover:bg-[#F2EDE1] text-[#1F2A1E] font-bold text-xs rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                data-testid="verify-otp-btn"
                type="button"
                disabled={!startOtp.trim() || actionLoading === startingBooking.id}
                onClick={async () => {
                  try {
                    await handleBookingAction(startingBooking.id, 'start', undefined, startOtp.trim());
                  } catch (e) {
                    // Handled inside handleBookingAction with setStartOtpError
                  }
                }}
                className="px-5 py-2.5 bg-purple-700 hover:bg-purple-800 text-white font-bold text-xs rounded-xl shadow-xs transition-colors disabled:opacity-50 flex items-center gap-1.5"
              >
                {actionLoading === startingBooking.id ? (
                  <span>Verifying...</span>
                ) : (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Verify & Start Service</span>
                  </>
                )}
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
              src={resolvePhotoUrl(previewPhotoUrl)}
              alt="Service Verification Proof"
              className="max-w-full max-h-[80vh] object-contain rounded-2xl"
              onError={(e) => {
                e.currentTarget.onerror = null;
                e.currentTarget.src = 'https://images.unsplash.com/photo-1560066984-138dadb4c035?auto=format&fit=crop&w=800&q=80';
              }}
            />
          </div>
        </div>
      )}

      {/* Service Completion OTP Verification Modal */}
      {completingBooking && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 space-y-5 shadow-2xl border border-[#E5DEC9]">
            <div className="flex items-start justify-between border-b border-[#E5DEC9]/60 pb-3">
              <div className="flex items-center gap-2.5">
                <div className="w-10 h-10 rounded-2xl bg-emerald-50 border border-emerald-200 flex items-center justify-center text-emerald-700 shadow-xs">
                  <KeyRound className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Verify Completion OTP</h3>
                  <p className="text-[11px] text-[#1F2A1E]/60 font-mono">
                    {completingBooking.reference || completingBooking.booking_reference || completingBooking.id}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => {
                  setCompletingBooking(null);
                  setCompleteOtp('');
                  setCompleteOtpError(null);
                }}
                className="text-[#1F2A1E]/40 hover:text-[#1F2A1E] p-1 rounded-full hover:bg-black/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-3 bg-[#FAF7F0] rounded-xl border border-[#E5DEC9] text-xs space-y-1">
              <p className="font-bold text-[#1F2A1E]">{completingBooking.service_name}</p>
              <p className="text-[#1F2A1E]/70">Customer: <span className="font-semibold">{completingBooking.customer_name}</span></p>
            </div>

            {completeOtpError && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                <span>{completeOtpError}</span>
              </div>
            )}

            <div className="space-y-3">
              <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider">
                Enter 4-Digit Customer Completion OTP
              </label>
              <input
                data-testid="complete-otp-input"
                type="text"
                maxLength={6}
                value={completeOtp}
                onChange={(e) => {
                  setCompleteOtp(e.target.value);
                  setCompleteOtpError(null);
                }}
                placeholder="4-digit OTP"
                className="w-full text-center font-mono text-2xl tracking-widest bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-3 text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
              />
              <p className="text-[11px] text-[#1F2A1E]/60">
                Ask the customer for the completion code displayed on their screen after they inspect and approve the completed service.
              </p>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => {
                  setCompletingBooking(null);
                  setCompleteOtp('');
                  setCompleteOtpError(null);
                }}
                className="px-4 py-2 bg-[#FAF7F0] hover:bg-[#F2EDE1] text-[#1F2A1E] font-bold text-xs rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                data-testid="verify-complete-otp-btn"
                type="button"
                disabled={!completeOtp.trim() || actionLoading === completingBooking.id}
                onClick={async () => {
                  try {
                    await handleBookingAction(completingBooking.id, 'complete', undefined, completeOtp.trim());
                  } catch (e) {
                    // Handled inside handleBookingAction with setCompleteOtpError
                  }
                }}
                className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors disabled:opacity-50 flex items-center gap-1.5"
              >
                {actionLoading === completingBooking.id ? (
                  <span>Verifying...</span>
                ) : (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Verify & Complete Service</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Mark Cash Collected Modal */}
      {cashCollectionBooking && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in">
          <form onSubmit={handleReportCashCollection} className="bg-white rounded-3xl max-w-md w-full p-6 space-y-5 shadow-2xl border border-[#E5DEC9]">
            <div className="flex items-start justify-between border-b border-[#E5DEC9]/60 pb-3">
              <div className="flex items-center gap-2.5">
                <div className="w-10 h-10 rounded-2xl bg-[#2F5233]/10 border border-[#2F5233]/20 flex items-center justify-center text-[#2F5233] shadow-xs">
                  <Banknote className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Mark Cash Collected</h3>
                  <p className="text-[11px] text-[#1F2A1E]/60 font-mono">
                    {cashCollectionBooking.reference || cashCollectionBooking.booking_reference || cashCollectionBooking.id}
                  </p>
                </div>
              </div>
              <button
                type="button"
                onClick={() => {
                  setCashCollectionBooking(null);
                  setCollectionError(null);
                  setCollectionSuccess(null);
                }}
                className="text-[#1F2A1E]/40 hover:text-[#1F2A1E] p-1 rounded-full hover:bg-black/5"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-3.5 bg-[#FAF7F0] rounded-xl border border-[#E5DEC9] text-xs space-y-1.5">
              <div className="flex justify-between items-center">
                <span className="text-[#1F2A1E]/60">Service:</span>
                <span className="font-bold text-[#1F2A1E]">{cashCollectionBooking.service_name}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-[#1F2A1E]/60">Customer:</span>
                <span className="font-semibold text-[#1F2A1E]">{cashCollectionBooking.customer_name}</span>
              </div>
              <div className="flex justify-between items-center pt-1 border-t border-[#E5DEC9]">
                <span className="font-semibold text-[#1F2A1E]/70">Agreed Amount:</span>
                <span className="font-mono font-bold text-sm text-[#2F5233]">
                  ₹{parseFloat(cashCollectionBooking.total_price || 0).toLocaleString('en-IN')}
                </span>
              </div>
            </div>

            {collectionError && (
              <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
                <span>{collectionError}</span>
              </div>
            )}

            {collectionSuccess && (
              <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                <span>{collectionSuccess}</span>
              </div>
            )}

            <div className="space-y-3">
              <div>
                <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider mb-1.5">
                  Amount Collected (₹)
                </label>
                <input
                  type="number"
                  step="0.01"
                  required
                  value={collectedAmount}
                  onChange={(e) => {
                    setCollectedAmount(e.target.value);
                    setCollectionError(null);
                  }}
                  placeholder="Enter collected cash amount"
                  className="w-full font-mono text-lg font-bold bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-4 py-2.5 text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
                />
              </div>

              {/* Discrepancy Alert */}
              {collectedAmount && parseFloat(collectedAmount) !== parseFloat(cashCollectionBooking.total_price || 0) && (
                <div className="p-3 bg-amber-50 border border-amber-300 rounded-xl text-xs text-amber-900 flex items-start gap-2">
                  <AlertCircle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold block">Amount Discrepancy Detected</span>
                    <span>
                      Reported: ₹{collectedAmount} vs Agreed: ₹{cashCollectionBooking.total_price}.
                      This discrepancy of ₹{Math.abs(parseFloat(collectedAmount) - parseFloat(cashCollectionBooking.total_price || 0)).toFixed(2)} will be flagged for SmartServe Admin review.
                    </span>
                  </div>
                </div>
              )}

              <div>
                <label className="block text-xs font-bold text-[#1F2A1E] uppercase tracking-wider mb-1.5">
                  Collection Notes (Optional)
                </label>
                <textarea
                  rows={2}
                  value={collectionNotes}
                  onChange={(e) => setCollectionNotes(e.target.value)}
                  placeholder="e.g. Exact cash received, tip included, or reason for difference"
                  className="w-full text-xs bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]"
                />
              </div>

              <p className="text-[11px] text-[#1F2A1E]/60 italic">
                Note: Reporting cash collection updates the payment status to "Collection Reported". Final verification is conducted by a SmartServe Operations Admin.
              </p>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2 border-t border-[#E5DEC9]">
              <button
                type="button"
                onClick={() => {
                  setCashCollectionBooking(null);
                  setCollectionError(null);
                  setCollectionSuccess(null);
                }}
                className="px-4 py-2 bg-[#FAF7F0] hover:bg-[#F2EDE1] text-[#1F2A1E] font-bold text-xs rounded-xl transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={collectionLoading || !collectedAmount}
                className="px-5 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-xl shadow-xs transition-colors disabled:opacity-50 flex items-center gap-1.5"
              >
                {collectionLoading ? (
                  <span>Recording Report...</span>
                ) : (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Confirm Cash Report</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};

export default ProviderDashboardView;
