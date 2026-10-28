import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Bell, X, Calendar, Clock, ArrowRight, Trash2, Sparkles } from 'lucide-react';
import { subscribeToRealtime } from '../../utils/realtime';
import { useAuth } from '../../context/AuthContext';

export interface ProviderBookingNotification {
  id: string;
  booking_id: string;
  booking_reference: string;
  service_name: string;
  scheduled_date: string;
  scheduled_time: string;
  status: string;
  timestamp: string;
  read: boolean;
}

const STORAGE_KEY = 'smartserve_provider_notifications_history';

// Synthesize pleasant, non-intrusive 2-tone notification chime via Web Audio API
function playNotificationChime() {
  try {
    const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
    if (!AudioContextClass) return;
    const ctx = new AudioContextClass();
    if (ctx.state === 'suspended') {
      ctx.resume().catch(() => {});
    }
    const now = ctx.currentTime;

    const osc1 = ctx.createOscillator();
    const gain1 = ctx.createGain();
    osc1.type = 'sine';
    osc1.frequency.setValueAtTime(523.25, now); // C5
    gain1.gain.setValueAtTime(0.18, now);
    gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.22);
    osc1.connect(gain1);
    gain1.connect(ctx.destination);
    osc1.start(now);
    osc1.stop(now + 0.22);

    const osc2 = ctx.createOscillator();
    const gain2 = ctx.createGain();
    osc2.type = 'sine';
    osc2.frequency.setValueAtTime(659.25, now + 0.1); // E5
    gain2.gain.setValueAtTime(0.2, now + 0.1);
    gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.38);
    osc2.connect(gain2);
    gain2.connect(ctx.destination);
    osc2.start(now + 0.1);
    osc2.stop(now + 0.38);
  } catch (_) {
    // Browser autoplay policy graceful silent fallback
  }
}

export const ProviderNotificationSystem: React.FC = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [notifications, setNotifications] = useState<ProviderBookingNotification[]>(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      return stored ? JSON.parse(stored) : [];
    } catch {
      return [];
    }
  });

  const [activePopup, setActivePopup] = useState<ProviderBookingNotification | null>(null);
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  // In-memory set of seen event keys to prevent duplicate popups on reconnection or multiple renders
  const seenEventKeysRef = useRef<Set<string>>(new Set());

  // Save notifications to localStorage
  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(notifications));
    } catch (_) {}
  }, [notifications]);

  // Close dropdown on outside click
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleOutsideClick);
    return () => document.removeEventListener('mousedown', handleOutsideClick);
  }, []);

  // Real-time WebSocket connection subscribed strictly to this provider's private channels
  useEffect(() => {
    if (!user || !user.user_id) return;
    const providerId = user.user_id;

    // Strict provider-specific channel list: NO admin or global channels
    const channels = [`provider_${providerId}`, `user_${providerId}`];

    const unsubscribe = subscribeToRealtime(channels, (payload) => {
      const type = (payload.type || payload.event_type || payload.event || '').toUpperCase();

      const isNewBooking =
        type === 'BOOKING_CREATED' ||
        type === 'BOOKING_ASSIGNED' ||
        type === 'BOOKING.CREATED' ||
        type === 'BOOKING.ASSIGNED';

      if (isNewBooking) {
        const b = payload.booking || payload.data || payload;
        const bookingId = String(b.booking_id || b.id || payload.booking_id || '');
        const bookingRef = b.booking_reference || payload.booking_reference || `BK-${bookingId.slice(0, 6).toUpperCase()}`;
        const serviceName = b.service_name || payload.service_name || 'Home Service';
        const schedDate = b.scheduled_date || payload.scheduled_date || 'Scheduled Date';
        const schedTime = b.scheduled_time || payload.scheduled_time || '';
        const status = b.status || payload.status || 'Requested';

        // Duplicate prevention key combining booking ID and event type
        const eventKey = `${bookingId}:${type}`;
        if (seenEventKeysRef.current.has(eventKey)) {
          return;
        }
        seenEventKeysRef.current.add(eventKey);

        const newNotif: ProviderBookingNotification = {
          id: `notif-${Date.now()}-${Math.random().toString(36).substring(2, 6)}`,
          booking_id: bookingId,
          booking_reference: bookingRef,
          service_name: serviceName,
          scheduled_date: schedDate,
          scheduled_time: schedTime,
          status,
          timestamp: new Date().toISOString(),
          read: false,
        };

        // Add to state and trigger audio chime
        setNotifications((prev) => [newNotif, ...prev.filter((n) => n.booking_id !== bookingId)]);
        setActivePopup(newNotif);
        playNotificationChime();

        // Dispatch browser custom event so ProviderDashboardView can refresh immediately
        window.dispatchEvent(
          new CustomEvent('smartserve:booking_received', {
            detail: { booking_id: bookingId, booking_reference: bookingRef },
          })
        );
      }
    });

    return () => {
      unsubscribe();
    };
  }, [user]);

  const handleOpenBooking = (bookingId: string) => {
    // Mark as read
    setNotifications((prev) =>
      prev.map((n) => (n.booking_id === bookingId ? { ...n, read: true } : n))
    );
    setActivePopup(null);
    setDropdownOpen(false);
    navigate('/dashboard');
  };

  const markAllRead = () => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
  };

  const clearAll = () => {
    setNotifications([]);
    setActivePopup(null);
  };

  const unreadCount = notifications.filter((n) => !n.read).length;

  return (
    <>
      {/* ── Top Header Bell & Dropdown ── */}
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={() => setDropdownOpen(!dropdownOpen)}
          className="relative p-2 rounded-xl border border-[#E5DEC9] bg-white hover:bg-[#F2EDE1] text-[#1F2A1E] transition-colors flex items-center justify-center shadow-2xs"
          aria-label="Provider Notifications"
          title="Booking Notifications"
        >
          <Bell className="w-4 h-4 text-[#2F5233]" />
          {unreadCount > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-rose-600 text-white font-black text-[10px] rounded-full flex items-center justify-center animate-bounce shadow-xs">
              {unreadCount > 9 ? '9+' : unreadCount}
            </span>
          )}
        </button>

        {dropdownOpen && (
          <div className="absolute right-0 mt-2 w-80 sm:w-96 bg-white rounded-3xl border border-[#E5DEC9] shadow-2xl p-4 z-50 text-xs animate-in fade-in">
            <div className="flex items-center justify-between pb-3 border-b border-[#E5DEC9]/70">
              <div className="flex items-center gap-2">
                <Bell className="w-4 h-4 text-[#2F5233]" />
                <span className="font-bold font-serif text-sm text-[#1F2A1E]">Booking Notifications</span>
                {unreadCount > 0 && (
                  <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#2F5233]/10 text-[#2F5233]">
                    {unreadCount} unread
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2">
                {unreadCount > 0 && (
                  <button
                    onClick={markAllRead}
                    className="text-[11px] font-semibold text-[#2F5233] hover:underline"
                  >
                    Mark all read
                  </button>
                )}
                {notifications.length > 0 && (
                  <button
                    onClick={clearAll}
                    className="text-[#1F2A1E]/40 hover:text-rose-600 p-1 rounded-md"
                    title="Clear history"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                )}
              </div>
            </div>

            <div className="max-h-80 overflow-y-auto divide-y divide-[#E5DEC9]/40 my-2 pr-1">
              {notifications.length === 0 ? (
                <div className="py-8 text-center text-slate-400 space-y-1">
                  <Bell className="w-6 h-6 text-slate-300 mx-auto" />
                  <p className="font-medium text-xs">No notifications yet</p>
                  <p className="text-[10px]">New job assignments will appear here in real-time</p>
                </div>
              ) : (
                notifications.map((n) => (
                  <div
                    key={n.id}
                    className={`py-3 px-2 rounded-2xl transition-colors cursor-pointer flex flex-col gap-1.5 ${
                      !n.read ? 'bg-[#FAF7F0]' : 'hover:bg-slate-50'
                    }`}
                    onClick={() => handleOpenBooking(n.booking_id)}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="space-y-0.5">
                        <div className="flex items-center gap-1.5">
                          <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" />
                          <h4 className="font-bold text-slate-900 text-xs">{n.service_name}</h4>
                        </div>
                        <p className="font-mono text-[10px] text-slate-500 font-semibold pl-3.5">
                          {n.booking_reference}
                        </p>
                      </div>
                      <span className="text-[9px] text-slate-400 shrink-0">
                        {new Date(n.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>

                    <div className="flex items-center justify-between text-[10px] text-slate-600 pl-3.5 pt-1">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-3 h-3 text-[#C9A15A]" />
                        <span>{n.scheduled_date}</span>
                        {n.scheduled_time && <span>• {n.scheduled_time}</span>}
                      </span>
                      <span className="text-[#2F5233] font-bold inline-flex items-center gap-0.5 hover:underline">
                        <span>View</span>
                        <ArrowRight className="w-3 h-3" />
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>

      {/* ── Real-Time Popup Notification Toast ── */}
      {activePopup && (
        <div className="fixed bottom-6 right-6 z-50 max-w-sm w-full animate-in slide-in-from-bottom-5 fade-in duration-300">
          <div className="bg-white rounded-3xl p-5 border-2 border-[#2F5233] shadow-2xl space-y-3.5 relative overflow-hidden backdrop-blur-md">
            {/* Top decorative accent bar */}
            <div className="absolute top-0 left-0 right-0 h-1.5 bg-gradient-to-r from-[#2F5233] via-[#C9A15A] to-[#2F5233]" />

            <div className="flex items-start justify-between gap-3 pt-1">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center shrink-0 shadow-xs relative">
                  <Sparkles className="w-5 h-5 text-emerald-700 animate-pulse" />
                  <span className="absolute -top-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-500 rounded-full border-2 border-white" />
                </div>
                <div>
                  <h3 className="font-extrabold text-sm text-[#1F2A1E] font-serif">New Booking Received!</h3>
                  <p className="text-[10px] font-semibold text-emerald-700 uppercase tracking-wider">
                    Assigned to your schedule
                  </p>
                </div>
              </div>

              <button
                onClick={() => setActivePopup(null)}
                className="p-1 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
                title="Dismiss"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Service & Booking Details */}
            <div className="bg-[#FAF7F0] p-3.5 rounded-2xl border border-[#E5DEC9] space-y-2 text-xs">
              <div className="flex items-center justify-between gap-2">
                <span className="font-bold text-slate-900 text-sm truncate">{activePopup.service_name}</span>
                <span className="font-mono font-bold text-[11px] bg-white px-2 py-0.5 rounded-md border border-[#E5DEC9] text-slate-700 shrink-0">
                  {activePopup.booking_reference}
                </span>
              </div>

              <div className="flex items-center gap-3 text-[11px] text-slate-600 font-medium pt-0.5">
                <div className="flex items-center gap-1">
                  <Calendar className="w-3.5 h-3.5 text-[#C9A15A]" />
                  <span>{activePopup.scheduled_date}</span>
                </div>
                {activePopup.scheduled_time && (
                  <div className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-[#C9A15A]" />
                    <span>{activePopup.scheduled_time}</span>
                  </div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex items-center gap-2 pt-1">
              <button
                onClick={() => setActivePopup(null)}
                className="flex-1 py-2 px-3 bg-[#FAF7F0] hover:bg-[#F2EDE1] text-slate-700 font-bold text-xs rounded-xl border border-[#E5DEC9] transition-colors"
              >
                Dismiss
              </button>
              <button
                onClick={() => handleOpenBooking(activePopup.booking_id)}
                className="flex-1 py-2 px-3 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center justify-center gap-1.5"
              >
                <span>View Booking</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
