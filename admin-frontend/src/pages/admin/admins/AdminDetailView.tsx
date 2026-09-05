import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  Users, 
  ShieldCheck,
  ShieldAlert, 
  Loader2, 
  ArrowLeft, 
  ChevronRight,
  Mail,
  X,
  KeyRound,
  Shield,
  History
} from 'lucide-react';
import { 
  getAdminDetail, 
  updateAdminRole, 
  updateAdminAccountStatus 
} from '../../../api/admins';
import type { AdminItem } from '../../../api/admins';

export const AdminDetailView: React.FC = () => {
  const { adminId } = useParams<{ adminId: string }>();
  const navigate = useNavigate();

  const [adminData, setAdminData] = useState<AdminItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Modals & Action States
  const [roleModalOpen, setRoleModalOpen] = useState<boolean>(false);
  const [selectedRole, setSelectedRole] = useState<string>('operations_admin');
  const [roleLoading, setRoleLoading] = useState<boolean>(false);

  const [statusModalOpen, setStatusModalOpen] = useState<boolean>(false);
  const [statusActionType, setStatusActionType] = useState<boolean>(false); // true = reactivate, false = suspend
  const [statusReason, setStatusReason] = useState<string>('');
  const [statusLoading, setStatusLoading] = useState<boolean>(false);

  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

  const showToast = (text: string, type: 'success' | 'warning' | 'error' = 'success') => {
    setToastMessage({ text, type });
    setTimeout(() => setToastMessage(null), 5000);
  };

  const fetchAdminProfile = async () => {
    if (!adminId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getAdminDetail(adminId);
      setAdminData(data);
      setSelectedRole(data.role_name);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load administrator details from backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdminProfile();
  }, [adminId]);

  const handleRoleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!adminData) return;
    setRoleLoading(true);
    try {
      await updateAdminRole(adminData.id, selectedRole);
      showToast(`Admin role updated to ${selectedRole}.`, 'success');
      setRoleModalOpen(false);
      fetchAdminProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Role update failed.', 'error');
    } finally {
      setRoleLoading(false);
    }
  };

  const handleStatusSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!adminData) return;
    setStatusLoading(true);
    try {
      await updateAdminAccountStatus(adminData.id, statusActionType, statusReason);
      const actStr = statusActionType ? 'reactivated' : 'suspended';
      showToast(`Admin account successfully ${actStr}.`, 'success');
      setStatusModalOpen(false);
      setStatusReason('');
      fetchAdminProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Account status update failed.', 'error');
    } finally {
      setStatusLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-slate-600">Loading Administrator Profile & Audit Activity...</p>
      </div>
    );
  }

  if (error || !adminData) {
    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white border border-rose-200 rounded-3xl text-center space-y-4 shadow-sm">
        <ShieldAlert className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold font-serif text-[#1F2A1E]">Admin Account Not Found</h3>
        <p className="text-xs text-slate-600">{error || 'Unable to retrieve requested admin account.'}</p>
        <button
          onClick={() => navigate('/admin/admins')}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#2F5233] text-white rounded-2xl text-xs font-bold"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Admin Directory</span>
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-slate-800">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-3 px-5 py-3.5 bg-slate-900 text-white rounded-2xl shadow-xl border border-slate-700 text-xs font-semibold animate-in fade-in">
          <ShieldCheck className="w-4 h-4 text-emerald-400" />
          <span>{toastMessage.text}</span>
        </div>
      )}

      {/* Breadcrumb Navigation */}
      <nav className="flex items-center gap-2 text-xs text-slate-500 font-medium">
        <Link to="/admin/admins" className="hover:text-[#2F5233] flex items-center gap-1 transition-colors">
          <Users className="w-3.5 h-3.5" />
          <span>People</span>
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <Link to="/admin/admins" className="hover:text-[#2F5233] transition-colors">
          Admins
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <span className="text-slate-900 font-bold">{adminData.email}</span>
      </nav>

      {/* Profile Header Banner */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-start md:items-center gap-5">
          <button
            onClick={() => navigate('/admin/admins')}
            className="p-2.5 rounded-2xl bg-[#F2EDE1] hover:bg-[#E5DEC9] text-slate-600 transition-colors"
            title="Back to Directory"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>

          <div className="w-16 h-16 rounded-2xl bg-indigo-50 text-indigo-600 font-extrabold text-2xl flex items-center justify-center border border-indigo-100 shadow-xs flex-shrink-0">
            {adminData.email.charAt(0).toUpperCase()}
          </div>

          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight">
                {adminData.email.split('@')[0]}
              </h1>
              <span className="px-3 py-1 bg-[#F2EDE1] text-[#2F5233] rounded-full text-xs font-bold border border-[#E5DEC9] capitalize">
                {adminData.role_name.replace('_', ' ')}
              </span>
              <span className={`px-3 py-1 rounded-full text-xs font-bold border ${
                adminData.is_active
                  ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                  : 'bg-rose-50 text-rose-700 border-rose-200'
              }`}>
                {adminData.is_active ? 'Account Active' : 'Account Suspended'}
              </span>
            </div>

            <p className="text-sm text-slate-500 font-semibold mt-1 flex items-center gap-4 flex-wrap">
              <span className="flex items-center gap-1.5"><Mail className="w-4 h-4 text-slate-400" /> {adminData.email}</span>
              <span className="flex items-center gap-1.5 text-xs text-slate-400">ID: {adminData.id}</span>
            </p>
          </div>
        </div>

        {/* Header Quick Admin Actions */}
        <div className="flex items-center gap-2.5 flex-wrap justify-end">
          <button
            onClick={() => setRoleModalOpen(true)}
            className="px-4 py-2 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-[#2F5233] font-bold rounded-2xl border border-[#E5DEC9] text-xs transition-colors flex items-center gap-1.5"
          >
            <Shield className="w-3.5 h-3.5" />
            <span>Change Role</span>
          </button>

          {adminData.is_active ? (
            <button
              onClick={() => {
                setStatusActionType(false);
                setStatusModalOpen(true);
              }}
              className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-2xl shadow-xs text-xs transition-colors"
            >
              Suspend Admin
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
        </div>
      </div>

      {/* Grid Layout of Details */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Account Details & 2FA Status */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <Users className="w-5 h-5 text-[#2F5233]" />
              <span>Admin Profile Details</span>
            </h3>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-400 font-semibold block">Admin ID (UUID)</span>
                <p className="font-mono font-bold text-slate-800 text-xs bg-[#FAF7F0] p-2 rounded-xl border border-[#E5DEC9] mt-1 select-all">
                  {adminData.id}
                </p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Email Address</span>
                <p className="font-semibold text-slate-900 mt-0.5">{adminData.email}</p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Assigned RBAC Role</span>
                <p className="font-bold text-[#2F5233] capitalize mt-0.5">{adminData.role_name.replace('_', ' ')}</p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Created Date</span>
                <p className="font-medium text-slate-700 mt-0.5">
                  {adminData.created_at ? new Date(adminData.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : 'N/A'}
                </p>
              </div>
            </div>
          </div>

          {/* 2FA Security Context Card */}
          <div className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
            <h3 className="text-base font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <KeyRound className="w-5 h-5 text-emerald-500" />
              <span>2FA Authentication Status</span>
            </h3>

            <div className="p-4 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9] space-y-2 text-xs">
              <div className="flex items-center justify-between font-bold">
                <span className="text-slate-700">Two-Factor Authentication</span>
                <span className={`px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                  adminData.is_2fa_enabled ? 'bg-emerald-50 text-emerald-700' : 'bg-slate-200 text-slate-600'
                }`}>
                  {adminData.is_2fa_enabled ? '2FA Enabled' : '2FA Not Enabled'}
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-medium pt-1 border-t border-[#E5DEC9]/60">
                🔒 Security Note: TOTP provisioning secrets and tokens are encrypted in hardware modules and never exposed in browser views.
              </p>
            </div>
          </div>
        </div>

        {/* Right Column: RBAC Permissions & Audit Activity */}
        <div className="lg:col-span-2 space-y-6">
          {/* Granted Permissions List */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-5">
            <h3 className="text-lg font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <Shield className="w-5 h-5 text-[#2F5233]" />
              <span>Granted Module Permissions ({adminData.permissions.length})</span>
            </h3>

            <div className="flex flex-wrap gap-2 text-xs">
              {adminData.permissions.map((perm) => (
                <span key={perm} className="px-3 py-1.5 bg-[#F2EDE1] text-[#2F5233] font-bold rounded-xl border border-[#E5DEC9] font-mono">
                  {perm}
                </span>
              ))}
            </div>
          </div>

          {/* Audit & Activity History */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-5">
            <h3 className="text-lg font-bold font-serif text-[#1F2A1E] border-b border-[#E5DEC9]/60 pb-3 flex items-center gap-2">
              <History className="w-5 h-5 text-[#2F5233]" />
              <span>Recent Administrative Activity</span>
            </h3>

            {!adminData.recent_activity || adminData.recent_activity.length === 0 ? (
              <div className="p-6 bg-[#FAF7F0] rounded-2xl text-center text-xs font-semibold text-slate-500">
                No recent administrative activity.
              </div>
            ) : (
              <div className="space-y-3 text-xs">
                {adminData.recent_activity.map((act) => (
                  <div key={act.id} className="p-4 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9] flex items-center justify-between">
                    <div>
                      <p className="font-bold text-slate-900">{act.action}</p>
                      <p className="text-[10px] text-slate-400 font-mono mt-0.5">Log ID: {act.id.substring(0, 8)}...</p>
                    </div>
                    <span className="text-[11px] text-slate-500 font-semibold bg-white px-2.5 py-1 rounded-xl border border-[#E5DEC9]">
                      {act.created_at ? new Date(act.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : ''}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Role Assignment Modal */}
      {roleModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleRoleSubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Assign RBAC Role</h3>
              <button type="button" onClick={() => setRoleModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-medium">
              Update RBAC role for <strong>{adminData.email}</strong>. Changes will update module access authorization in the backend.
            </p>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Select Role *</label>
              <select
                value={selectedRole}
                onChange={(e) => setSelectedRole(e.target.value)}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
              >
                <option value="super_admin">Super Admin (Full Access)</option>
                <option value="operations_admin">Operations Admin</option>
                <option value="support_admin">Support Admin</option>
                <option value="catalog_admin">Catalog Admin</option>
              </select>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setRoleModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={roleLoading}
                className="px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {roleLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm Role Change'}
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
                {statusActionType ? 'Reactivate' : 'Deactivate'} Administrator Account
              </h3>
              <button type="button" onClick={() => setStatusModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-medium">
              Are you sure you want to {statusActionType ? 'reactivate' : 'deactivate'} administrator <strong>{adminData.email}</strong>? {statusActionType ? 'They will regain access to administrative tools.' : 'They will lose access to administrative functions. Account data will remain saved in PostgreSQL audit logs.'}
            </p>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Reason / Notes (Optional)</label>
              <textarea
                value={statusReason}
                onChange={(e) => setStatusReason(e.target.value)}
                placeholder="Internal security audit note..."
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
                {statusLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : `Confirm ${statusActionType ? 'Reactivation' : 'Deactivation'}`}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
