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
  Zap
} from 'lucide-react';
import { 
  getBookingDetail, 
  updateBookingStatus, 
  reassignBookingProvider 
} from '../../../api/bookings';
import { SmartServeLoader } from '../../../components/common/SmartServeLoader';
import type { BookingItem } from '../../../api/bookings';
import { getProvidersList } from '../../../api/providers';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';

export const BookingDetailView: React.FC = () => {
  const { bookingId } = useParams<{ bookingId: string }>();
  const navigate = useNavigate();

  const [bookingData, setBookingData] = useState<BookingItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

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

  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

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
      const data = await getBookingDetail(bookingId);
      setBookingData(data);
      if (data.allowed_next_statuses && data.allowed_next_statuses.length > 0) {
        setTargetNextStatus(data.allowed_next_statuses[0]);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load booking details from backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookingProfile();

    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});

    getProvidersList().then((provs) => {
      setProviderOptions(provs.map((p) => ({ id: p.user_id, name: p.full_name })));
      if (provs.length > 0) setSelectedProviderId(provs[0].user_id);
    }).catch(() => {});
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

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <SmartServeLoader size="lg" text="Loading Operational Booking Details & Lifecycle Timeline..." />
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
                Booking #{bookingData.id.substring(0, 8)}
              </h1>
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

          {/* Service & Financial Card */}
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <IndianRupee className="w-5 h-5 text-emerald-600" />
              <span>Service & Payment Details</span>
            </h3>

            <div className="space-y-3 text-xs">
              <div className="flex items-center justify-between">
                <span className="text-slate-400 font-semibold">Total Price</span>
                <span className="font-extrabold text-slate-900 text-lg">₹{bookingData.total_price.toLocaleString('en-IN')}</span>
              </div>

              <div className="flex items-center justify-between border-t border-[#E5DEC9]/60 pt-2">
                <span className="text-slate-400 font-semibold">Payment Status</span>
                <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                  bookingData.payment_status === 'Paid' ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'
                }`}>
                  {bookingData.payment_status}
                </span>
              </div>

              {bookingData.otp_code && (
                <div className="flex items-center justify-between border-t border-[#E5DEC9]/60 pt-2">
                  <span className="text-slate-400 font-semibold">Start OTP Verification Code</span>
                  <span className="font-mono font-extrabold text-indigo-600 bg-indigo-50 px-2.5 py-0.5 rounded-lg border border-indigo-200">
                    {bookingData.otp_code}
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
    </div>
  );
};
