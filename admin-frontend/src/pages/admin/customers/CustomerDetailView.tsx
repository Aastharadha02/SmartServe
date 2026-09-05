import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  Users, 
  ShieldAlert, 
  CalendarCheck, 
  Loader2, 
  ArrowLeft, 
  CheckCircle2, 
  ChevronRight,
  Phone,
  Mail,
  X,
  Flag
} from 'lucide-react';
import { 
  getCustomerDetail, 
  updateCustomerAccountStatus, 
  flagCustomerAccount 
} from '../../../api/customers';
import type { CustomerItem } from '../../../api/customers';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';

export const CustomerDetailView: React.FC = () => {
  const { customerId } = useParams<{ customerId: string }>();
  const navigate = useNavigate();

  const [customer, setCustomer] = useState<CustomerItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  // Modals & Action States
  const [flagModalOpen, setFlagModalOpen] = useState<boolean>(false);
  const [flagType, setFlagType] = useState<string>('Fraud Risk — Chargeback Abuse');
  const [flagReason, setFlagReason] = useState<string>('');
  const [flagLoading, setFlagLoading] = useState<boolean>(false);

  const [statusModalOpen, setStatusModalOpen] = useState<boolean>(false);
  const [statusActionType, setStatusActionType] = useState<boolean>(false); // true = reactivate, false = suspend
  const [statusReason, setStatusReason] = useState<string>('');
  const [statusLoading, setStatusLoading] = useState<boolean>(false);

  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

  const canManageCustomers = hasPermission(adminSession, 'customers:manage');

  const showToast = (text: string, type: 'success' | 'warning' | 'error' = 'success') => {
    setToastMessage({ text, type });
    setTimeout(() => setToastMessage(null), 5000);
  };

  const fetchCustomerData = async () => {
    if (!customerId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getCustomerDetail(customerId);
      setCustomer(data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load customer profile from backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomerData();
    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});
  }, [customerId]);

  const handleFlagSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customer) return;
    setFlagLoading(true);
    try {
      await flagCustomerAccount(customer.id, flagType, flagReason);
      showToast(`Customer account flagged for ${flagType}.`, 'warning');
      setFlagModalOpen(false);
      setFlagReason('');
      fetchCustomerData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Fraud flagging failed.', 'error');
    } finally {
      setFlagLoading(false);
    }
  };

  const handleStatusSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customer) return;
    setStatusLoading(true);
    try {
      await updateCustomerAccountStatus(customer.id, statusActionType, statusReason);
      const actStr = statusActionType ? 'reactivated' : 'suspended';
      showToast(`Customer account successfully ${actStr}.`, 'success');
      setStatusModalOpen(false);
      setStatusReason('');
      fetchCustomerData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Account status action failed.', 'error');
    } finally {
      setStatusLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-slate-600">Loading Customer Profile & Booking History...</p>
      </div>
    );
  }

  if (error || !customer) {
    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white border border-rose-200 rounded-3xl text-center space-y-4 shadow-sm">
        <ShieldAlert className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold font-serif text-[#1F2A1E]">Customer Not Found</h3>
        <p className="text-xs text-slate-600">{error || 'Unable to retrieve requested customer account.'}</p>
        <button
          onClick={() => navigate('/admin/customers')}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#2F5233] text-white rounded-2xl text-xs font-bold"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Customer Directory</span>
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
        <Link to="/admin/customers" className="hover:text-[#2F5233] flex items-center gap-1 transition-colors">
          <Users className="w-3.5 h-3.5" />
          <span>People</span>
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <Link to="/admin/customers" className="hover:text-[#2F5233] transition-colors">
          Customers
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <span className="text-slate-900 font-bold">{customer.full_name}</span>
      </nav>

      {/* Profile Header Banner */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-start md:items-center gap-5">
          <button
            onClick={() => navigate('/admin/customers')}
            className="p-2.5 rounded-2xl bg-[#F2EDE1] hover:bg-[#E5DEC9] text-slate-600 transition-colors"
            title="Back to Directory"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>

          <div className="w-16 h-16 rounded-2xl bg-[#F2EDE1] text-[#2F5233] font-extrabold text-2xl flex items-center justify-center border border-[#E5DEC9] shadow-xs flex-shrink-0">
            {customer.full_name.charAt(0)}
          </div>

          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight">
                {customer.full_name}
              </h1>
              <span className={`px-3 py-1 rounded-full text-xs font-bold border ${
                customer.is_active
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-rose-50 text-rose-700 border-rose-200'
              }`}>
                {customer.is_active ? 'Account Active' : 'Account Suspended'}
              </span>
              {customer.is_flagged && (
                <span className="px-3 py-1 bg-rose-50 text-rose-700 rounded-full text-xs font-bold border border-rose-200 flex items-center gap-1">
                  <ShieldAlert className="w-3.5 h-3.5 text-rose-500" />
                  <span>Fraud / Risk Flagged</span>
                </span>
              )}
            </div>

            <p className="text-sm text-slate-500 font-semibold mt-1 flex items-center gap-4 flex-wrap">
              <span className="flex items-center gap-1.5"><Mail className="w-4 h-4 text-slate-400" /> {customer.email}</span>
              <span className="flex items-center gap-1.5"><Phone className="w-4 h-4 text-slate-400" /> {customer.phone || 'N/A'}</span>
            </p>
          </div>
        </div>

        {/* Header Quick Admin Actions */}
        <div className="flex items-center gap-2.5 flex-wrap justify-end">
          {canManageCustomers ? (
            <>
              <button
                onClick={() => setFlagModalOpen(true)}
                className="px-4 py-2 bg-rose-50 hover:bg-rose-100 text-rose-700 font-bold rounded-2xl border border-rose-200 text-xs transition-colors flex items-center gap-1.5"
              >
                <Flag className="w-3.5 h-3.5" />
                <span>Flag Customer</span>
              </button>

              {customer.is_active ? (
                <button
                  onClick={() => {
                    setStatusActionType(false);
                    setStatusModalOpen(true);
                  }}
                  className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-2xl shadow-xs text-xs transition-colors"
                >
                  Suspend Customer
                </button>
              ) : (
                <button
                  onClick={() => {
                    setStatusActionType(true);
                    setStatusModalOpen(true);
                  }}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-2xl shadow-xs text-xs transition-colors"
                >
                  Reactivate Account
                </button>
              )}
            </>
          ) : (
            <button
              disabled
              title="Customer account suspension and fraud flagging requires 'customers:manage' permission."
              className="px-4 py-2 bg-[#F2EDE1] text-slate-400 font-bold rounded-2xl border border-[#E5DEC9] text-xs cursor-not-allowed opacity-70"
            >
              🔒 Actions Restricted (View Only)
            </button>
          )}
        </div>
      </div>

      {/* Grid Layout of Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Profile & Activity Metrics */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <Users className="w-5 h-5 text-[#2F5233]" />
              <span>Profile Information</span>
            </h3>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-400 font-semibold block">Customer ID (UUID)</span>
                <p className="font-mono font-bold text-slate-800 text-xs bg-[#FAF7F0] p-2 rounded-xl border border-[#E5DEC9] mt-1 select-all">
                  {customer.id}
                </p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Email Address</span>
                <p className="font-semibold text-slate-900 mt-0.5">{customer.email}</p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Phone Number</span>
                <p className="font-mono font-semibold text-slate-900 mt-0.5">{customer.phone || 'N/A'}</p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Member Since</span>
                <p className="font-medium text-slate-700 mt-0.5">
                  {customer.created_at ? new Date(customer.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : 'N/A'}
                </p>
              </div>
            </div>
          </div>

          {/* Activity Breakdown */}
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <CalendarCheck className="w-5 h-5 text-[#2F5233]" />
              <span>Activity Metrics</span>
            </h3>

            <div className="grid grid-cols-3 gap-2 text-center text-xs">
              <div className="p-3 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9]">
                <span className="text-[10px] text-slate-400 font-bold uppercase block">Total</span>
                <p className="text-base font-extrabold text-slate-900 mt-0.5">{customer.bookings_count}</p>
              </div>
              <div className="p-3 bg-emerald-50 rounded-2xl border border-emerald-100">
                <span className="text-[10px] text-emerald-700 font-bold uppercase block">Completed</span>
                <p className="text-base font-extrabold text-emerald-900 mt-0.5">{customer.completed_bookings_count}</p>
              </div>
              <div className="p-3 bg-rose-50 rounded-2xl border border-rose-100">
                <span className="text-[10px] text-rose-700 font-bold uppercase block">Cancelled</span>
                <p className="text-base font-extrabold text-rose-900 mt-0.5">{customer.cancelled_bookings_count}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Booking History & Fraud Risk Flags */}
        <div className="lg:col-span-2 space-y-6">
          {/* Risk & Fraud Flag Context */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-5">
            <h3 className="text-lg font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-rose-500" />
              <span>Risk Signals & Fraud Flags</span>
            </h3>

            {customer.flags.length === 0 ? (
              <div className="p-4 bg-[#FAF7F0] rounded-2xl text-center text-xs font-semibold text-slate-500">
                No risk flags recorded.
              </div>
            ) : (
              <div className="space-y-3">
                {customer.flags.map((flag) => (
                  <div key={flag.id} className="p-4 bg-rose-50/70 rounded-2xl border border-rose-200 space-y-1 text-xs">
                    <div className="flex items-center justify-between font-bold text-rose-900">
                      <span className="flex items-center gap-1.5">
                        <Flag className="w-3.5 h-3.5 text-rose-600" />
                        <span>Backend Risk Signal: {flag.flag_type}</span>
                      </span>
                      <span className="text-[10px] text-rose-600 font-mono">
                        {flag.created_at ? new Date(flag.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : ''}
                      </span>
                    </div>
                    <p className="text-rose-800 font-medium">{flag.reason}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Booking History */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-5">
            <h3 className="text-lg font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <CalendarCheck className="w-5 h-5 text-[#2F5233]" />
              <span>Booking History</span>
            </h3>

            {!customer.bookings || customer.bookings.length === 0 ? (
              <div className="p-6 bg-[#FAF7F0] rounded-2xl text-center text-xs font-semibold text-slate-500">
                No booking history available.
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#FAF7F0] text-slate-600 font-bold uppercase text-[10px] border-b border-[#E5DEC9]">
                    <tr>
                      <th className="py-3 px-4">Service</th>
                      <th className="py-3 px-4">Scheduled Date</th>
                      <th className="py-3 px-4">Assigned Provider</th>
                      <th className="py-3 px-4">Status</th>
                      <th className="py-3 px-4 text-right">Amount (₹)</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {customer.bookings.map((booking) => (
                      <tr key={booking.id} className="hover:bg-[#FAF7F0]/80 transition-colors">
                        <td className="py-3.5 px-4 font-bold text-slate-900">
                          {booking.service_name}
                        </td>
                        <td className="py-3.5 px-4 text-slate-600 font-medium">
                          {booking.scheduled_time ? new Date(booking.scheduled_time).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : 'N/A'}
                        </td>
                        <td className="py-3.5 px-4 text-slate-700 font-semibold">
                          {booking.provider_name}
                        </td>
                        <td className="py-3.5 px-4">
                          <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                            booking.status.toUpperCase() === 'COMPLETED' || booking.status.toUpperCase() === 'PAID'
                              ? 'bg-emerald-50 text-emerald-700'
                              : booking.status.toUpperCase() === 'CANCELLED'
                              ? 'bg-rose-50 text-rose-700'
                              : 'bg-amber-50 text-amber-700'
                          }`}>
                            {booking.status}
                          </span>
                        </td>
                        <td className="py-3.5 px-4 text-right font-mono font-bold text-slate-900">
                          ₹{booking.total_price.toFixed(2)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Fraud Flagging Modal */}
      {flagModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleFlagSubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Flag Customer Account</h3>
              <button type="button" onClick={() => setFlagModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-medium">
              Flag <strong>{customer.full_name}</strong> for risk or fraudulent activity. This will be recorded in backend audit logs.
            </p>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Flag Type *</label>
              <select
                value={flagType}
                onChange={(e) => setFlagType(e.target.value)}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-rose-400"
              >
                <option value="Fraud Risk — Chargeback Abuse">Fraud Risk — Chargeback Abuse</option>
                <option value="Frequent Cancellation Pattern">Frequent Cancellation Pattern</option>
                <option value="Suspicious Booking Pattern">Suspicious Booking Pattern</option>
                <option value="Payment Fraud">Payment Fraud</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Reason / Notes *</label>
              <textarea
                value={flagReason}
                onChange={(e) => setFlagReason(e.target.value)}
                placeholder="Detail the suspicious activity or pattern observed..."
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-xs focus:outline-none focus:ring-2 focus:ring-rose-400"
                rows={3}
                required
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setFlagModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={flagLoading}
                className="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {flagLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm Risk Flag'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Account Status Suspend/Reactivate Modal */}
      {statusModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleStatusSubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">
                {statusActionType ? 'Reactivate' : 'Suspend'} Customer Account
              </h3>
              <button type="button" onClick={() => setStatusModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-medium">
              Are you sure you want to {statusActionType ? 'reactivate' : 'suspend'} customer <strong>{customer.full_name}</strong>? {statusActionType ? 'They will regain access to booking services.' : 'They will be temporarily blocked from booking new services. Existing records will not be deleted.'}
            </p>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Reason / Notes (Optional)</label>
              <textarea
                value={statusReason}
                onChange={(e) => setStatusReason(e.target.value)}
                placeholder="Internal administrative note..."
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                rows={2}
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setStatusModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={statusLoading}
                className={`px-5 py-2 text-white font-bold rounded-xl text-xs shadow-sm ${
                  statusActionType ? 'bg-emerald-600 hover:bg-emerald-700' : 'bg-rose-600 hover:bg-rose-700'
                }`}
              >
                {statusLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : `Confirm ${statusActionType ? 'Reactivation' : 'Suspension'}`}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
