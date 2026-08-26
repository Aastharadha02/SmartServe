import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  User, 
  Key, 
  ShieldCheck, 
  LogOut, 
  ExternalLink, 
  CheckCircle2, 
  Loader2, 
  Globe, 
  IndianRupee, 
  X
} from 'lucide-react';
import { 
  getAdminsList, 
  changeAdminPassword, 
  disableAdmin2FA 
} from '../../../api/admins';
import { setupAdmin2FA, verifyAdmin2FA } from '../../../api/security';
import type { AdminItem } from '../../../api/admins';

export const SettingsView: React.FC = () => {
  const navigate = useNavigate();

  const [adminProfile, setAdminProfile] = useState<AdminItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Password Form State
  const [currentPassword, setCurrentPassword] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [confirmPassword, setConfirmPassword] = useState<string>('');
  const [passwordLoading, setPasswordLoading] = useState<boolean>(false);

  // 2FA State
  const [totpModalOpen, setTotpModalOpen] = useState<boolean>(false);
  const [totpUri, setTotpUri] = useState<string | null>(null);
  const [totpCode, setTotpCode] = useState<string>('');
  const [totpLoading, setTotpLoading] = useState<boolean>(false);

  // Toast State
  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setToast({ text, type });
    setTimeout(() => setToast(null), 4000);
  };

  const fetchCurrentProfile = async () => {
    setLoading(true);
    try {
      const list = await getAdminsList();
      if (list.length > 0) {
        setAdminProfile(list[0]);
      }
    } catch (err: any) {
      console.error('Failed to load admin profile for settings.', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCurrentProfile();
  }, []);

  // Handle Password Submit
  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentPassword || !newPassword || !confirmPassword) {
      showToast('All password fields are required.', 'error');
      return;
    }
    if (newPassword !== confirmPassword) {
      showToast('New password and confirmation do not match.', 'error');
      return;
    }
    if (newPassword.length < 8) {
      showToast('New password must be at least 8 characters long.', 'error');
      return;
    }

    setPasswordLoading(true);
    try {
      const res = await changeAdminPassword({
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: confirmPassword,
      });
      showToast(res.message, 'success');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Current password verification failed.', 'error');
    } finally {
      setPasswordLoading(false);
    }
  };

  // Handle 2FA Setup
  const handleInitiate2FA = async () => {
    setTotpLoading(true);
    try {
      const res = await setupAdmin2FA();
      setTotpUri(res.provisioning_uri);
      setTotpModalOpen(true);
    } catch (err: any) {
      showToast('Failed to generate 2FA QR URI.', 'error');
    } finally {
      setTotpLoading(false);
    }
  };

  // Handle 2FA Verification
  const handleVerify2FACode = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!totpCode || totpCode.length < 6) return;
    setTotpLoading(true);
    try {
      await verifyAdmin2FA(totpCode);
      showToast('2FA Authenticator verified & activated successfully!', 'success');
      setTotpModalOpen(false);
      fetchCurrentProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Invalid 2FA code.', 'error');
    } finally {
      setTotpLoading(false);
    }
  };

  // Handle Disable 2FA
  const handleDisable2FA = async () => {
    setTotpLoading(true);
    try {
      const res = await disableAdmin2FA();
      showToast(res.message, 'success');
      fetchCurrentProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to disable 2FA.', 'error');
    } finally {
      setTotpLoading(false);
    }
  };

  // Handle Logout
  const handleLogout = () => {
    localStorage.removeItem('smartserve_token');
    showToast('Signed out successfully.', 'success');
    setTimeout(() => {
      navigate('/login', { replace: true });
    }, 500);
  };

  if (loading || !adminProfile) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#5CA8FF]" />
        <p className="text-sm font-semibold text-slate-600">Loading Settings & Configuration...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto font-sans text-slate-800">
      {/* Toast Notification */}
      {toast && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-3 px-5 py-3.5 bg-slate-900 text-white rounded-2xl shadow-xl border border-slate-700 text-xs font-semibold animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{toast.text}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">Settings & Configuration</h1>
            <span className="text-xs font-bold text-[#5CA8FF] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              Admin Workspace
            </span>
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            Admin profile overview, security credentials, 2FA management, application preferences, and session sign-out
          </p>
        </div>

        <button
          onClick={handleLogout}
          className="px-5 py-2.5 bg-rose-50 hover:bg-rose-100 text-rose-700 font-bold rounded-2xl border border-rose-200 text-xs flex items-center gap-2 transition-colors self-start md:self-auto shadow-xs"
        >
          <LogOut className="w-4 h-4 text-rose-600" />
          <span>Sign Out</span>
        </button>
      </div>

      {/* SECTION 1: ADMIN PROFILE OVERVIEW */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
        <h3 className="text-base md:text-lg font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
          <User className="w-5 h-5 text-[#5CA8FF]" />
          <span>Authenticated Administrator Profile</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 text-xs">
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1">
            <span className="text-slate-400 font-bold block uppercase text-[10px]">Email Address</span>
            <p className="font-bold text-slate-900 text-sm truncate">{adminProfile.email}</p>
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1">
            <span className="text-slate-400 font-bold block uppercase text-[10px]">Assigned Role</span>
            <p className="font-bold text-[#5CA8FF] font-mono text-sm capitalize">{adminProfile.role_name}</p>
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1">
            <span className="text-slate-400 font-bold block uppercase text-[10px]">Account Status</span>
            <span className="inline-block px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 mt-0.5">
              Active Account
            </span>
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1">
            <span className="text-slate-400 font-bold block uppercase text-[10px]">2FA Protection</span>
            <span className={`inline-block px-2.5 py-0.5 rounded-full text-[10px] font-bold border mt-0.5 ${
              adminProfile.is_2fa_enabled
                ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                : 'bg-amber-50 text-amber-700 border-amber-200'
            }`}>
              {adminProfile.is_2fa_enabled ? '2FA Enabled' : 'Not Enabled'}
            </span>
          </div>
        </div>

        <p className="text-[11px] text-slate-400 font-semibold pt-1">
          * Account role assignments and permission scopes belong to <Link to="/admin/admins" className="text-[#5CA8FF] hover:underline font-bold">Admin & RBAC Management</Link>.
        </p>
      </div>

      {/* SECTION 2: ACCOUNT SECURITY & PASSWORD */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Password Change Form */}
        <form onSubmit={handlePasswordSubmit} className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
            <Key className="w-5 h-5 text-[#5CA8FF]" />
            <span>Change Account Password</span>
          </h3>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Current Password *</label>
            <input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              placeholder="Enter current password..."
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 font-medium"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">New Password (Min 8 Chars) *</label>
            <input
              type="password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              placeholder="Enter new password..."
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 font-medium"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 mb-1">Confirm New Password *</label>
            <input
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              placeholder="Confirm new password..."
              className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-xs focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 font-medium"
              required
            />
          </div>

          <div className="pt-2 flex justify-end">
            <button
              type="submit"
              disabled={passwordLoading}
              className="px-5 py-2.5 bg-[#5CA8FF] hover:bg-blue-600 text-white font-bold rounded-2xl text-xs flex items-center gap-1.5 shadow-sm transition-colors"
            >
              {passwordLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Update Password'}
            </button>
          </div>
        </form>

        {/* 2FA & Active Sessions Control */}
        <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6 flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-emerald-600" />
              <span>Two-Factor Authentication (2FA)</span>
            </h3>

            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-700">TOTP Authenticator Protection</span>
                <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                  adminProfile.is_2fa_enabled
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : 'bg-amber-50 text-amber-700 border-amber-200'
                }`}>
                  {adminProfile.is_2fa_enabled ? 'Enabled' : 'Disabled'}
                </span>
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Requires 6-digit TOTP code verification from Google Authenticator or 1Password during login.
              </p>
            </div>

            <div className="flex items-center gap-3">
              {!adminProfile.is_2fa_enabled ? (
                <button
                  onClick={handleInitiate2FA}
                  disabled={totpLoading}
                  className="px-4 py-2 bg-[#5CA8FF] hover:bg-blue-600 text-white font-bold rounded-xl text-xs transition-colors shadow-xs"
                >
                  Configure 2FA
                </button>
              ) : (
                <button
                  onClick={handleDisable2FA}
                  disabled={totpLoading}
                  className="px-4 py-2 bg-rose-50 hover:bg-rose-100 text-rose-700 font-bold rounded-xl border border-rose-200 text-xs transition-colors"
                >
                  Disable 2FA
                </button>
              )}
            </div>
          </div>

          {/* Session Management Shortcut Link */}
          <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
            <span className="text-xs font-bold text-slate-700">Manage Active JWT Sessions</span>
            <Link
              to="/admin/security"
              className="text-xs font-bold text-[#5CA8FF] hover:underline flex items-center gap-1"
            >
              <span>Security → Active Sessions</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>
      </div>

      {/* SECTION 3: APPLICATION PREFERENCES */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
        <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
          <Globe className="w-5 h-5 text-[#5CA8FF]" />
          <span>Application & Regional Preferences</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1">
            <span className="text-slate-400 font-bold block uppercase text-[10px]">Currency Display</span>
            <p className="font-bold text-slate-900 text-sm flex items-center gap-1">
              <IndianRupee className="w-4 h-4 text-emerald-600" />
              <span>₹ INR (Indian Rupee Enforced)</span>
            </p>
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1">
            <span className="text-slate-400 font-bold block uppercase text-[10px]">Date / Time Format</span>
            <p className="font-bold text-slate-900 text-sm">DD MMM YYYY, HH:mm</p>
          </div>

          <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-1">
            <span className="text-slate-400 font-bold block uppercase text-[10px]">Notification Dispatch</span>
            <p className="font-bold text-slate-700 text-xs mt-1">Managed by system event triggers.</p>
          </div>
        </div>
      </div>

      {/* 2FA Setup Modal */}
      {totpModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleVerify2FACode} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-slate-200 p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-base font-bold text-slate-900">Setup Admin TOTP 2FA</h3>
              <button type="button" onClick={() => setTotpModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            {totpUri && (
              <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200 text-center font-mono text-[11px] text-slate-700 truncate">
                {totpUri}
              </div>
            )}

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Enter 6-Digit TOTP Verification Code *</label>
              <input
                type="text"
                value={totpCode}
                onChange={(e) => setTotpCode(e.target.value.replace(/\D/g, '').substring(0, 6))}
                placeholder="123456"
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-center text-lg font-mono font-bold text-slate-900 tracking-widest focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
                maxLength={6}
                required
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setTotpModalOpen(false)}
                className="px-4 py-2 bg-slate-100 text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={totpLoading || totpCode.length < 6}
                className="px-5 py-2 bg-[#5CA8FF] hover:bg-blue-600 text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {totpLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Verify & Enable 2FA'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
