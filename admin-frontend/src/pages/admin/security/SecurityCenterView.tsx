import React, { useEffect, useState, useMemo } from 'react';
import { 
  ShieldAlert, 
  Search, 
  Lock, 
  Key, 
  Smartphone, 
  AlertTriangle, 
  CheckCircle2, 
  Loader2, 
  X, 
  FileText, 
  Monitor, 
  Sparkles, 
  ShieldCheck,
  Ban
} from 'lucide-react';
import { 
  getSecuritySummary, 
  getAuditLogs, 
  getFailedLoginAttempts, 
  getSuspiciousActivities, 
  setupAdmin2FA, 
  verifyAdmin2FA, 
  getActiveSessions, 
  revokeActiveSession 
} from '../../../api/security';
import type { 
  SecuritySummary, 
  AuditLogItem, 
  FailedLoginItem, 
  SuspiciousActivityItem, 
  ActiveSessionItem 
} from '../../../api/security';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';

export const SecurityCenterView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'audit' | 'suspicious' | 'failed' | 'sessions'>('audit');

  const [summary, setSummary] = useState<SecuritySummary | null>(null);
  const [auditLogs, setAuditLogs] = useState<AuditLogItem[]>([]);
  const [failedLogins, setFailedLogins] = useState<FailedLoginItem[]>([]);
  const [suspiciousList, setSuspiciousList] = useState<SuspiciousActivityItem[]>([]);
  const [sessions, setSessions] = useState<ActiveSessionItem[]>([]);

  const [loading, setLoading] = useState<boolean>(true);

  // Filters & Search for Audit Log
  const [auditSearch, setAuditSearch] = useState<string>('');
  const [riskFilter, setRiskFilter] = useState<string>('');

  // 2FA Setup & Verification Modal State
  const [totpModalOpen, setTotpModalOpen] = useState<boolean>(false);
  const [totpUri, setTotpUri] = useState<string | null>(null);
  const [totpCode, setTotpCode] = useState<string>('');
  const [totpLoading, setTotpLoading] = useState<boolean>(false);
  const [totpVerified, setTotpVerified] = useState<boolean>(false);

  // Revoke Session Modal State
  const [revokeModalOpen, setRevokeModalOpen] = useState<boolean>(false);
  const [selectedSessionId, setSelectedSessionId] = useState<string | null>(null);
  const [revokeLoading, setRevokeLoading] = useState<boolean>(false);

  // Toast State
  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setToast({ text, type });
    setTimeout(() => setToast(null), 4000);
  };

  const fetchSecurityData = async () => {
    setLoading(true);
    try {
      const summaryData = await getSecuritySummary();
      setSummary(summaryData);
      const auditData = await getAuditLogs();
      setAuditLogs(auditData);
      const failedData = await getFailedLoginAttempts();
      setFailedLogins(failedData);
      const suspData = await getSuspiciousActivities();
      setSuspiciousList(suspData);
      const sessionData = await getActiveSessions();
      setSessions(sessionData);
    } catch (err: any) {
      console.error('Failed to load security center data.', err);
    } finally {
      setLoading(false);
    }
  };

  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  const canManageSecurity =
    !adminSession ||
    adminSession.role === 'super_admin' ||
    adminSession.role_name === 'super_admin' ||
    adminSession.permissions.includes('security:manage');

  useEffect(() => {
    getAuthenticatedAdmin()
      .then((s) => {
        setAdminSession(s);
        if (s.role === 'super_admin' || s.role_name === 'super_admin') {
          fetchSecurityData();
        } else {
          setLoading(false);
        }
      })
      .catch(() => {
        setLoading(false);
      });
  }, []);

  // Filtered Audit Logs
  const filteredAuditLogs = useMemo(() => {
    return auditLogs.filter((l) => {
      const matchesSearch =
        l.actor_email.toLowerCase().includes(auditSearch.toLowerCase()) ||
        l.action.toLowerCase().includes(auditSearch.toLowerCase()) ||
        (l.target_resource && l.target_resource.toLowerCase().includes(auditSearch.toLowerCase()));

      const matchesRisk = !riskFilter || l.risk_level.toLowerCase() === riskFilter.toLowerCase();

      return matchesSearch && matchesRisk;
    });
  }, [auditLogs, auditSearch, riskFilter]);

  // Handle 2FA Setup
  const handleInitiate2FASetup = async () => {
    setTotpLoading(true);
    try {
      const res = await setupAdmin2FA();
      setTotpUri(res.provisioning_uri);
      setTotpModalOpen(true);
      setTotpVerified(false);
    } catch (err: any) {
      showToast('Failed to initiate 2FA setup.', 'error');
    } finally {
      setTotpLoading(false);
    }
  };

  // Handle 2FA Verification
  const handleVerify2FA = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!totpCode || totpCode.length < 6) return;
    setTotpLoading(true);
    try {
      await verifyAdmin2FA(totpCode);
      showToast('Admin 2FA Verification Successful!', 'success');
      setTotpVerified(true);
      setTimeout(() => {
        setTotpModalOpen(false);
        fetchSecurityData();
      }, 1500);
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Invalid TOTP 2FA code.', 'error');
    } finally {
      setTotpLoading(false);
    }
  };

  // Handle Revoke Session Submit
  const handleRevokeConfirm = async () => {
    if (!selectedSessionId) return;
    setRevokeLoading(true);
    try {
      await revokeActiveSession(selectedSessionId);
      showToast('Session revoked successfully.', 'success');
      setRevokeModalOpen(false);
      fetchSecurityData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to revoke session.', 'error');
    } finally {
      setRevokeLoading(false);
    }
  };

  const getRiskBadgeStyle = (risk: string) => {
    switch (risk.toLowerCase()) {
      case 'critical':
        return 'bg-rose-50 text-rose-700 border-rose-200 font-extrabold';
      case 'warning':
      case 'high':
        return 'bg-amber-50 text-amber-700 border-amber-200 font-bold';
      default:
        return 'bg-[#F2EDE1] text-[#2F5233] border-[#E5DEC9] font-semibold';
    }
  };

  const isSuperAdmin =
    adminSession?.role === 'super_admin' ||
    adminSession?.role_name === 'super_admin';

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-slate-600">Loading Security & Risk Control Center...</p>
      </div>
    );
  }

  if (adminSession && !isSuperAdmin) {
    return (
      <div className="p-6 md:p-8 space-y-6 max-w-7xl mx-auto animate-in fade-in">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight flex items-center gap-2">
              <ShieldAlert className="w-7 h-7 text-rose-600" />
              <span>Security & Audit Logs Center</span>
            </h1>
            <p className="text-sm text-slate-500 font-semibold mt-1">
              System Audit Logs & Security Administration
            </p>
          </div>
        </div>

        {/* Restricted Notice Card */}
        <div className="bg-white p-8 md:p-12 rounded-3xl border border-[#E5DEC9] shadow-sm text-center max-w-2xl mx-auto space-y-6 my-12">
          <div className="w-16 h-16 bg-rose-50 text-rose-600 rounded-2xl border border-rose-200 flex items-center justify-center mx-auto shadow-sm">
            <Lock className="w-8 h-8 text-rose-600" />
          </div>
          <div className="space-y-2">
            <h2 className="text-2xl font-extrabold font-serif text-[#1F2A1E] tracking-tight">
              Security Audit Logs Restricted
            </h2>
            <p className="text-slate-600 text-sm font-medium leading-relaxed">
              Viewing security audit logs, system session controls, and login risk activity metrics is strictly restricted to <strong>Super Admin</strong> accounts (`admin@smartserve.com`).
            </p>
          </div>
          <div className="bg-[#FAF7F0] p-4 rounded-2xl border border-[#E5DEC9] text-xs text-slate-500 font-semibold flex items-center justify-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-500 flex-shrink-0" />
            <span>Current Session: <strong>{adminSession.email}</strong> ({adminSession.role_name || adminSession.role})</span>
          </div>
          <div className="pt-2">
            <a
              href="/admin/dashboard"
              className="inline-flex items-center gap-2 px-6 py-3 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-2xl text-xs transition-colors shadow-sm"
            >
              Back to Dashboard
            </a>
          </div>
        </div>
      </div>
    );
  }

  if (!summary) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-slate-600">Loading Security & Risk Control Center...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-slate-800">
      {/* Toast Notification */}
      {toast && (
        <div className="fixed top-20 right-8 z-50 flex items-center gap-3 px-5 py-3.5 bg-slate-900 text-white rounded-2xl shadow-xl border border-slate-700 text-xs font-semibold animate-in fade-in">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{toast.text}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight">Security & Risk Center</h1>
            <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-1 rounded-full border border-emerald-200 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              <span>System Guard Active</span>
            </span>
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            Immutable audit ledger, authentication monitoring, suspicious activity detection, TOTP 2FA management, and session control
          </p>
        </div>

        {/* 2FA Quick Control */}
        <div className="flex items-center gap-3">
          <button
            onClick={handleInitiate2FASetup}
            disabled={totpLoading}
            className="px-5 py-2.5 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-2xl text-xs flex items-center gap-2 shadow-xs transition-colors"
          >
            {totpLoading ? <Loader2 className="w-4 h-4 animate-spin text-[#2F5233]" /> : <Smartphone className="w-4 h-4 text-[#2F5233]" />}
            <span>Configure 2FA Authenticator</span>
          </button>
        </div>
      </div>

      {/* KPI Overview Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <div className="bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
          <span className="text-[10px] font-bold text-slate-400 uppercase block">Audit Log Entries</span>
          <span className="text-xl md:text-2xl font-extrabold text-slate-900 mt-1 block">{summary.total_audit_events}</span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
          <span className="text-[10px] font-bold text-slate-400 uppercase block">Active Sessions</span>
          <span className="text-xl md:text-2xl font-extrabold text-[#2F5233] mt-1 block">{summary.active_sessions}</span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
          <span className="text-[10px] font-bold text-slate-400 uppercase block">Failed Logins</span>
          <span className="text-xl md:text-2xl font-extrabold text-amber-600 mt-1 block">{summary.failed_logins}</span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
          <span className="text-[10px] font-bold text-slate-400 uppercase block">Suspicious Events</span>
          <span className="text-xl md:text-2xl font-extrabold text-rose-600 mt-1 block">{summary.suspicious_activities}</span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
          <span className="text-[10px] font-bold text-slate-400 uppercase block">Critical Events</span>
          <span className="text-xl md:text-2xl font-extrabold text-rose-700 mt-1 block">{summary.critical_events}</span>
        </div>

        <div className="bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
          <span className="text-[10px] font-bold text-slate-400 uppercase block">Admin 2FA Status</span>
          <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2 py-1 rounded-lg border border-emerald-200 mt-2.5 inline-block">
            {summary.is_totp_enabled ? '2FA Enabled' : 'Not Enabled'}
          </span>
        </div>
      </div>

      {/* Module Navigation Tabs */}
      <div className="bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm flex items-center gap-2 overflow-x-auto">
        <button
          onClick={() => setActiveTab('audit')}
          className={`px-5 py-2.5 rounded-xl font-bold text-xs md:text-sm transition-all flex items-center gap-2 ${
            activeTab === 'audit'
              ? 'bg-[#2F5233] text-white shadow-xs'
              : 'text-slate-600 hover:bg-[#F2EDE1]'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Immutable Audit Logs ({auditLogs.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('suspicious')}
          className={`px-5 py-2.5 rounded-xl font-bold text-xs md:text-sm transition-all flex items-center gap-2 ${
            activeTab === 'suspicious'
              ? 'bg-[#2F5233] text-white shadow-xs'
              : 'text-slate-600 hover:bg-[#F2EDE1]'
          }`}
        >
          <ShieldAlert className="w-4 h-4" />
          <span>Suspicious Activity & AI Signals ({suspiciousList.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('failed')}
          className={`px-5 py-2.5 rounded-xl font-bold text-xs md:text-sm transition-all flex items-center gap-2 ${
            activeTab === 'failed'
              ? 'bg-[#2F5233] text-white shadow-xs'
              : 'text-slate-600 hover:bg-[#F2EDE1]'
          }`}
        >
          <Key className="w-4 h-4" />
          <span>Failed Login Monitor ({failedLogins.length})</span>
        </button>

        <button
          onClick={() => setActiveTab('sessions')}
          className={`px-5 py-2.5 rounded-xl font-bold text-xs md:text-sm transition-all flex items-center gap-2 ${
            activeTab === 'sessions'
              ? 'bg-[#2F5233] text-white shadow-xs'
              : 'text-slate-600 hover:bg-[#F2EDE1]'
          }`}
        >
          <Monitor className="w-4 h-4" />
          <span>Active Sessions ({sessions.length})</span>
        </button>
      </div>

      {/* TAB 1: IMMUTABLE AUDIT LOG LEDGER (READ-ONLY) */}
      {activeTab === 'audit' && (
        <div className="space-y-6">
          {/* Search & Risk Filters */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
            <div className="relative flex-1 w-full max-w-md">
              <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                value={auditSearch}
                onChange={(e) => setAuditSearch(e.target.value)}
                placeholder="Search actor email, action, target resource..."
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] font-medium"
              />
            </div>

            <div className="flex items-center gap-3">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
                <Lock className="w-3.5 h-3.5 text-slate-400" /> Read-Only Ledger
              </span>

              <select
                value={riskFilter}
                onChange={(e) => setRiskFilter(e.target.value)}
                className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
              >
                <option value="">All Risk Levels</option>
                <option value="info">Info</option>
                <option value="warning">Warning</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
            </div>
          </div>

          {/* Audit Log Table */}
          {filteredAuditLogs.length === 0 ? (
            <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
              <FileText className="w-8 h-8 text-slate-400 mx-auto" />
              <h3 className="text-base font-bold text-slate-800">No recent security events found.</h3>
              <p className="text-xs text-slate-500 font-medium">Try clearing your risk level filter or search term.</p>
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#FAF7F0] text-slate-600 font-bold uppercase text-[10px] border-b border-[#E5DEC9]">
                    <tr>
                      <th className="py-3.5 px-6">Timestamp</th>
                      <th className="py-3.5 px-4">Actor / Email</th>
                      <th className="py-3.5 px-4">Role</th>
                      <th className="py-3.5 px-6">Action / Event</th>
                      <th className="py-3.5 px-4">Target Resource</th>
                      <th className="py-3.5 px-4">Risk Level</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-medium">
                    {filteredAuditLogs.map((log) => (
                      <tr key={log.id} className="hover:bg-[#FAF7F0] transition-colors">
                        <td className="py-4 px-6 text-slate-500 whitespace-nowrap font-mono text-[11px]">
                          {log.created_at ? new Date(log.created_at).toLocaleString('en-IN') : 'N/A'}
                        </td>
                        <td className="py-4 px-4 font-bold text-slate-900">{log.actor_email}</td>
                        <td className="py-4 px-4 font-mono text-[11px] text-slate-600">{log.actor_role}</td>
                        <td className="py-4 px-6 font-bold text-slate-800 max-w-xs truncate">{log.action}</td>
                        <td className="py-4 px-4 font-mono text-[11px] text-slate-500">{log.target_resource || 'N/A'}</td>
                        <td className="py-4 px-4">
                          <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] border ${getRiskBadgeStyle(log.risk_level)}`}>
                            {log.risk_level}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 2: SUSPICIOUS ACTIVITY & AI SIGNALS */}
      {activeTab === 'suspicious' && (
        <div className="space-y-6">
          {suspiciousList.length === 0 ? (
            <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
              <ShieldCheck className="w-8 h-8 text-emerald-500 mx-auto" />
              <h3 className="text-base font-bold text-slate-800">No suspicious activity detected.</h3>
              <p className="text-xs text-slate-500 font-medium">System anomaly monitoring reports zero active risk flags.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {suspiciousList.map((act) => (
                <div
                  key={act.id}
                  className="bg-white p-6 rounded-3xl border border-rose-200 shadow-sm space-y-4 bg-gradient-to-b from-rose-50/30 to-white"
                >
                  <div className="flex items-center justify-between border-b border-rose-100 pb-3">
                    <span className="font-bold text-slate-900 flex items-center gap-2 text-sm">
                      <AlertTriangle className="w-4 h-4 text-rose-600" />
                      <span>{act.anomaly_type}</span>
                    </span>

                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-rose-50 text-rose-700 border border-rose-200">
                      Risk Score: {Math.round(act.risk_score * 100)}%
                    </span>
                  </div>

                  {act.details_json && (
                    <div className="space-y-2 text-xs">
                      <p className="font-semibold text-slate-800">{act.details_json.detection_reason}</p>

                      {act.details_json.ai_signal && (
                        <div className="p-2.5 bg-indigo-50 text-indigo-900 rounded-xl border border-indigo-200 font-bold flex items-center gap-1.5 text-[11px]">
                          <Sparkles className="w-4 h-4 text-indigo-600" />
                          <span>{act.details_json.ai_signal}</span>
                        </div>
                      )}

                      <div className="pt-2 flex items-center justify-between text-[11px] text-slate-500 font-medium border-t border-[#E5DEC9]/60">
                        <span>IP: {act.details_json.ip_address || '185.220.101.4'}</span>
                        <span>Location: {act.details_json.geo_location || 'Remote Host'}</span>
                      </div>
                    </div>
                  )}

                  <div className="pt-2 text-right text-[10px] text-slate-400 font-mono">
                    Detected: {act.created_at ? new Date(act.created_at).toLocaleString('en-IN') : 'N/A'}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB 3: FAILED LOGIN MONITOR */}
      {activeTab === 'failed' && (
        <div className="space-y-6">
          {failedLogins.length === 0 ? (
            <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
              <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto" />
              <h3 className="text-base font-bold text-slate-800">No failed login activity.</h3>
              <p className="text-xs text-slate-500 font-medium">All authentication attempts have passed security verification.</p>
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#FAF7F0] text-slate-600 font-bold uppercase text-[10px] border-b border-[#E5DEC9]">
                    <tr>
                      <th className="py-3.5 px-6">Target Account Email</th>
                      <th className="py-3.5 px-4">Origin IP Address</th>
                      <th className="py-3.5 px-4">Failed Attempt Count</th>
                      <th className="py-3.5 px-4">Lock Status</th>
                      <th className="py-3.5 px-6 text-right">Last Attempt Time</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {failedLogins.map((fl) => (
                      <tr key={fl.id} className="hover:bg-[#FAF7F0] transition-colors">
                        <td className="py-4 px-6 font-bold text-slate-900">{fl.email}</td>
                        <td className="py-4 px-4 font-mono text-[11px] text-slate-600">{fl.ip_address || 'Unknown'}</td>
                        <td className="py-4 px-4 font-bold text-rose-600">{fl.attempt_count} attempts</td>
                        <td className="py-4 px-4">
                          {fl.locked_until ? (
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-rose-50 text-rose-700 border border-rose-200">
                              Locked Out
                            </span>
                          ) : (
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-50 text-amber-700 border border-amber-200">
                              Flagged Threshold
                            </span>
                          )}
                        </td>
                        <td className="py-4 px-6 text-right font-medium text-slate-500">
                          {fl.last_attempt ? new Date(fl.last_attempt).toLocaleString('en-IN') : 'N/A'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TAB 4: ACTIVE SESSIONS */}
      {activeTab === 'sessions' && (
        <div className="space-y-6">
          {sessions.length === 0 ? (
            <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
              <Monitor className="w-8 h-8 text-slate-400 mx-auto" />
              <h3 className="text-base font-bold text-slate-800">No active sessions.</h3>
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#FAF7F0] text-slate-600 font-bold uppercase text-[10px] border-b border-[#E5DEC9]">
                    <tr>
                      <th className="py-3.5 px-6">Session ID / Token JTI</th>
                      <th className="py-3.5 px-4">Device / User Agent</th>
                      <th className="py-3.5 px-4">IP Address</th>
                      <th className="py-3.5 px-4">Session Status</th>
                      <th className="py-3.5 px-6 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {sessions.map((s) => (
                      <tr key={s.id} className="hover:bg-[#FAF7F0] transition-colors">
                        <td className="py-4 px-6 font-mono font-bold text-slate-900 text-[11px]">{s.token_jti}</td>
                        <td className="py-4 px-4 text-slate-700 truncate max-w-xs">{s.user_agent || 'Chrome / Windows 11'}</td>
                        <td className="py-4 px-4 font-mono text-[11px] text-slate-600">{s.ip_address || '127.0.0.1'}</td>
                        <td className="py-4 px-4">
                          {s.is_revoked ? (
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#F2EDE1] text-slate-600 border border-[#E5DEC9]">
                              Revoked
                            </span>
                          ) : (
                            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                              Active
                            </span>
                          )}
                        </td>
                        <td className="py-4 px-6 text-right">
                          {!s.is_revoked && (
                            canManageSecurity ? (
                              <button
                                onClick={() => {
                                  setSelectedSessionId(s.id);
                                  setRevokeModalOpen(true);
                                }}
                                className="px-3 py-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 font-bold rounded-xl border border-rose-200 transition-colors text-xs inline-flex items-center gap-1"
                              >
                                <Ban className="w-3.5 h-3.5 text-rose-600" />
                                <span>Revoke Session</span>
                              </button>
                            ) : (
                              <button
                                disabled
                                title="Revoking active sessions requires 'security:manage' or Super Admin permission."
                                className="px-3 py-1.5 bg-[#F2EDE1] text-slate-400 font-bold rounded-xl border border-[#E5DEC9] text-xs inline-flex items-center gap-1 cursor-not-allowed opacity-60"
                              >
                                <Ban className="w-3.5 h-3.5 text-slate-400" />
                                <span>Revoke (Disabled)</span>
                              </button>
                            )
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      )}

      {/* TOTP 2FA Setup & Verification Modal */}
      {totpModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
                <Smartphone className="w-5 h-5 text-[#2F5233]" />
                <span>Configure Admin TOTP 2FA</span>
              </h3>
              <button type="button" onClick={() => setTotpModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            {totpVerified ? (
              <div className="p-6 text-center space-y-2 bg-emerald-50 rounded-2xl border border-emerald-200 text-emerald-800">
                <CheckCircle2 className="w-10 h-10 text-emerald-600 mx-auto" />
                <h4 className="text-base font-bold">2FA Verification Successful!</h4>
                <p className="text-xs text-emerald-700">Admin account 2FA protection has been confirmed.</p>
              </div>
            ) : (
              <form onSubmit={handleVerify2FA} className="space-y-4">
                <p className="text-xs text-slate-600 font-semibold leading-relaxed">
                  Scan the provisioning QR URI in your Google Authenticator or 1Password app, then enter the 6-digit verification code below:
                </p>

                {totpUri && (
                  <div className="p-3 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9] text-center font-mono text-[11px] text-slate-700 truncate">
                    {totpUri}
                  </div>
                )}

                <div>
                  <label className="block text-xs font-bold text-slate-700 mb-1">6-Digit TOTP Verification Code *</label>
                  <input
                    type="text"
                    value={totpCode}
                    onChange={(e) => setTotpCode(e.target.value.replace(/\D/g, '').substring(0, 6))}
                    placeholder="e.g. 123456"
                    className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-center text-lg font-mono font-bold text-slate-900 tracking-widest focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                    maxLength={6}
                    required
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setTotpModalOpen(false)}
                    className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={totpLoading || totpCode.length < 6}
                    className="px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
                  >
                    {totpLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Verify 2FA Code'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {/* Revoke Session Confirmation Modal */}
      {revokeModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Revoke Active JWT Session?</h3>
              <button type="button" onClick={() => setRevokeModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-semibold">
              Are you sure you want to revoke session <strong>#{selectedSessionId?.substring(0, 8)}</strong>? The user will be immediately logged out.
            </p>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setRevokeModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleRevokeConfirm}
                disabled={revokeLoading}
                className="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {revokeLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm Revocation'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
