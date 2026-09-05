import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getBookingDetail, cancelBooking, BookingDetail } from '../api/bookings';
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
  HelpCircle
} from 'lucide-react';
import { SmartServeLoader } from '../components/common/SmartServeLoader';

export const CustomerBookingDetail: React.FC = () => {
  const { bookingId } = useParams<{ bookingId: string }>();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const [booking, setBooking] = useState<BookingDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [cancelling, setCancelling] = useState<boolean>(false);

  const fetchDetail = async () => {
    if (!bookingId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getBookingDetail(bookingId);
      setBooking(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch booking details from database.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDetail();
  }, [bookingId]);

  const handleCancelBooking = async () => {
    if (!bookingId) return;
    if (!window.confirm('Are you sure you want to cancel this service booking?')) return;

    setCancelling(true);
    try {
      await cancelBooking(bookingId, 'Cancelled by Customer');
      showToast('Booking cancelled successfully.', 'info');
      fetchDetail();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to cancel booking.', 'error');
    } finally {
      setCancelling(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <SmartServeLoader size="lg" text="Loading booking status from database..." />
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
  const canCancel = stLower === 'requested' || stLower === 'assigned' || stLower === 'confirmed';

  return (
    <div className="space-y-8 font-sans max-w-4xl mx-auto">
      
      {/* Back button */}
      <button
        onClick={() => navigate('/bookings')}
        className="inline-flex items-center gap-2 text-xs font-bold text-slate-600 hover:text-[#2563EB] transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        <span>Back to My Bookings</span>
      </button>

      {/* Main Card */}
      <div className="bg-white rounded-3xl border border-slate-200/90 shadow-md overflow-hidden space-y-6">
        
        {/* Header Ribbon */}
        <div className="bg-[#0A1128] text-white p-6 sm:p-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1">
            <div className="flex items-center gap-2">
              <span className="font-mono text-sm font-bold text-blue-300">{booking.booking_reference}</span>
              <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                stLower === 'completed' || stLower === 'paid'
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-400/30'
                  : stLower === 'cancelled'
                  ? 'bg-rose-500/20 text-rose-300 border-rose-400/30'
                  : 'bg-blue-500/20 text-blue-300 border-blue-400/30'
              }`}>
                {booking.status}
              </span>
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

        {/* Content Body */}
        <div className="p-6 sm:p-8 space-y-8">
          
          {/* OTP Code Box */}
          {booking.otp_code && stLower !== 'completed' && stLower !== 'cancelled' && (
            <div className="p-5 rounded-2xl bg-amber-50 border border-amber-200/80 flex items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-700 flex items-center justify-center flex-shrink-0">
                  <KeyRound className="w-5 h-5" />
                </div>
                <div>
                  <h4 className="font-bold text-amber-950 text-sm">Service OTP Verification Code</h4>
                  <p className="text-xs text-amber-800">Share this code with your technician upon arrival to begin service.</p>
                </div>
              </div>
              <span className="font-mono text-2xl font-black text-amber-950 tracking-widest bg-white px-4 py-2 rounded-xl border border-amber-300 shadow-2xs">
                {booking.otp_code}
              </span>
            </div>
          )}

          {/* Details Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            
            {/* Schedule */}
            <div className="space-y-3 p-5 rounded-2xl bg-slate-50 border border-slate-200/80">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <Clock className="w-4 h-4 text-blue-600" />
                <span>Scheduled Appointment</span>
              </h4>
              <p className="font-bold text-slate-900 text-base">{booking.scheduled_date}</p>
              <p className="text-xs text-slate-600">Time Slot: <strong>{booking.scheduled_time}</strong></p>
            </div>

            {/* Provider */}
            <div className="space-y-3 p-5 rounded-2xl bg-slate-50 border border-slate-200/80">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-2">
                <UserCheck className="w-4 h-4 text-emerald-600" />
                <span>Assigned Service Expert</span>
              </h4>
              <p className="font-bold text-slate-900 text-base">{booking.provider_name || 'Dispatching Verified Professional...'}</p>
              <p className="text-xs text-slate-600">SmartServe Background Checked & Insured</p>
            </div>

            {/* Address */}
            <div className="space-y-3 p-5 rounded-2xl bg-slate-50 border border-slate-200/80 md:col-span-2">
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
                onClick={handleCancelBooking}
                disabled={cancelling}
                className="px-5 py-2.5 bg-rose-50 hover:bg-rose-100 text-rose-600 font-bold text-xs rounded-xl transition-colors flex items-center gap-1.5 disabled:opacity-50"
              >
                {cancelling ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <XCircle className="w-4 h-4" />}
                <span>Cancel Booking</span>
              </button>
            )}
          </div>

        </div>

      </div>

    </div>
  );
};

export default CustomerBookingDetail;
