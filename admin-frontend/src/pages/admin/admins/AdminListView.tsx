import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  ShieldCheck, 
  Search, 
  LayoutGrid, 
  List, 
  UserPlus, 
  Loader2, 
  ChevronRight,
  Eye,
  EyeOff,
  KeyRound,
  X,
  Users,
  Shield
} from 'lucide-react';
import { 
  getAdminsList, 
  createAdminAccount, 
  getPermissionsMatrix,
  getAuthenticatedAdmin 
} from '../../../api/admins';
import type { AdminItem, PermissionMatrixItem, SessionAdminInfo } from '../../../api/admins';

export const AdminListView: React.FC = () => {
  const navigate = useNavigate();
  const [admins, setAdmins] = useState<AdminItem[]>([]);
  const [matrix, setMatrix] = useState<PermissionMatrixItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [roleFilter, setRoleFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [twoFaFilter, setTwoFaFilter] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  // Create Admin Modal State
  const [createModalOpen, setCreateModalOpen] = useState<boolean>(false);
  const [newEmail, setNewEmail] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [newRole, setNewRole] = useState<string>('operations_admin');
  const [createLoading, setCreateLoading] = useState<boolean>(false);

  // Permission Matrix Modal State
  const [matrixModalOpen, setMatrixModalOpen] = useState<boolean>(false);

  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

  const showToast = (text: string, type: 'success' | 'warning' | 'error' = 'success') => {
    setToastMessage({ text, type });
    setTimeout(() => setToastMessage(null), 5000);
  };

  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  const canManageAdmins =
    !adminSession ||
    adminSession.role === 'super_admin' ||
    adminSession.role_name === 'super_admin' ||
    adminSession.permissions.includes('admins:manage');

  const fetchAdmins = async () => {
    setLoading(true);
    try {
      const data = await getAdminsList();
      setAdmins(data);
      const matrixData = await getPermissionsMatrix();
      setMatrix(matrixData);
    } catch (err: any) {
      console.error('Failed to load admin directory.', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAdmins();
    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});
  }, []);

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setCreateLoading(true);
    try {
      await createAdminAccount({
        email: newEmail,
        password: newPassword,
        role_name: newRole,
      });
      showToast(`Admin account ${newEmail} created successfully.`, 'success');
      setCreateModalOpen(false);
      setNewEmail('');
      setNewPassword('');
      fetchAdmins();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Admin creation failed.', 'error');
    } finally {
      setCreateLoading(false);
    }
  };

  const filteredAdmins = useMemo(() => {
    return admins.filter((a) => {
      const matchesSearch = 
        a.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        a.id.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesRole = !roleFilter || a.role_name.toLowerCase() === roleFilter.toLowerCase();

      const matchesStatus = !statusFilter ||
        (statusFilter === 'active' && a.is_active) ||
        (statusFilter === 'suspended' && !a.is_active);

      const matchesTwoFa = !twoFaFilter ||
        (twoFaFilter === 'enabled' && a.is_2fa_enabled) ||
        (twoFaFilter === 'disabled' && !a.is_2fa_enabled);

      return matchesSearch && matchesRole && matchesStatus && matchesTwoFa;
    });
  }, [admins, searchTerm, roleFilter, statusFilter, twoFaFilter]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-slate-600">Loading Admin Directory & RBAC Matrix...</p>
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

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight">Admins & RBAC Roles</h1>
            <span className="text-xs font-bold text-[#2F5233] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              {admins.length} Administrators
            </span>
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            Manage administrator accounts, RBAC role assignments, system permission matrix, and 2FA status
          </p>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          <button
            onClick={() => setMatrixModalOpen(true)}
            className="px-4 py-2.5 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-slate-700 font-bold rounded-2xl border border-[#E5DEC9] text-xs transition-colors flex items-center gap-2"
          >
            <Shield className="w-4 h-4 text-[#2F5233]" />
            <span>Permission Matrix</span>
          </button>

          {canManageAdmins ? (
            <button
              onClick={() => setCreateModalOpen(true)}
              className="px-5 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-2xl shadow-sm text-xs transition-colors flex items-center gap-2"
            >
              <UserPlus className="w-4 h-4" />
              <span>Add Admin</span>
            </button>
          ) : (
            <button
              disabled
              title="Creating or modifying admin accounts requires 'admins:manage' or Super Admin permission."
              className="px-5 py-2.5 bg-slate-200 text-slate-500 font-bold rounded-2xl text-xs flex items-center gap-2 cursor-not-allowed opacity-70"
            >
              <UserPlus className="w-4 h-4" />
              <span>Add Admin (Disabled)</span>
            </button>
          )}
        </div>
      </div>

      {/* Search & Filter Controls */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
        <div className="relative flex-1 w-full max-w-md">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search admin email or ID..."
            className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] font-medium"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto justify-end">
          <select
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          >
            <option value="">All Roles</option>
            <option value="super_admin">Super Admin</option>
            <option value="operations_admin">Operations Admin</option>
            <option value="support_admin">Support Admin</option>
            <option value="catalog_admin">Catalog Admin</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          >
            <option value="">All Statuses</option>
            <option value="active">Active Only</option>
            <option value="suspended">Suspended Only</option>
          </select>

          <select
            value={twoFaFilter}
            onChange={(e) => setTwoFaFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          >
            <option value="">All 2FA Statuses</option>
            <option value="enabled">2FA Enabled</option>
            <option value="disabled">2FA Not Enabled</option>
          </select>

          {/* Grid / List View Toggle */}
          <div className="flex items-center bg-[#F2EDE1] p-1 rounded-xl border border-[#E5DEC9]">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-white text-[#2F5233] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'list' ? 'bg-white text-[#2F5233] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="List View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Directory Render */}
      {filteredAdmins.length === 0 ? (
        <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
          <Users className="w-8 h-8 text-slate-400 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No administrators found.</h3>
          <p className="text-xs text-slate-500 font-medium">Try changing your search terms or filter settings.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredAdmins.map((adminItem) => (
            <div
              key={adminItem.id}
              onClick={() => navigate(`/admin/admins/${adminItem.id}`)}
              className="group bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col justify-between space-y-5"
            >
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3 overflow-hidden">
                    <div className="w-12 h-12 rounded-2xl bg-indigo-50 text-indigo-600 font-extrabold text-lg flex items-center justify-center border border-indigo-100 flex-shrink-0">
                      {adminItem.email.charAt(0).toUpperCase()}
                    </div>
                    <div className="overflow-hidden">
                      <h3 className="text-base md:text-lg font-bold font-serif text-[#1F2A1E] group-hover:text-[#2F5233] transition-colors truncate">
                        {adminItem.email.split('@')[0]}
                      </h3>
                      <p className="text-xs text-slate-500 font-semibold truncate">{adminItem.email}</p>
                    </div>
                  </div>

                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border flex-shrink-0 ${
                    adminItem.is_active
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : 'bg-rose-50 text-rose-700 border-rose-200'
                  }`}>
                    {adminItem.is_active ? 'Active' : 'Suspended'}
                  </span>
                </div>

                <div className="flex items-center justify-between gap-2 pt-1 text-xs">
                  <span className="px-3 py-1 rounded-xl bg-[#F2EDE1] text-[#2F5233] font-bold border border-[#E5DEC9] capitalize">
                    {adminItem.role_name.replace('_', ' ')}
                  </span>
                  <span className={`flex items-center gap-1 font-bold text-xs ${
                    adminItem.is_2fa_enabled ? 'text-emerald-600' : 'text-slate-400'
                  }`}>
                    <KeyRound className="w-3.5 h-3.5" />
                    <span>{adminItem.is_2fa_enabled ? '2FA Enabled' : '2FA Off'}</span>
                  </span>
                </div>
              </div>

              <div className="pt-3 border-t border-[#E5DEC9]/60 flex items-center justify-between text-xs">
                <span className="text-slate-400 font-medium">
                  Created: {adminItem.created_at ? new Date(adminItem.created_at).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' }) : 'N/A'}
                </span>

                <span className="font-bold text-[#2F5233] group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                  <span>View & Edit</span>
                  <ChevronRight className="w-4 h-4" />
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#FAF7F0] text-slate-600 font-bold uppercase text-[10px] border-b border-[#E5DEC9]">
                <tr>
                  <th className="py-3.5 px-6">Admin Account</th>
                  <th className="py-3.5 px-4">RBAC Role</th>
                  <th className="py-3.5 px-4">Status</th>
                  <th className="py-3.5 px-4">2FA Status</th>
                  <th className="py-3.5 px-4">Created Date</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredAdmins.map((adminItem) => (
                  <tr
                    key={adminItem.id}
                    onClick={() => navigate(`/admin/admins/${adminItem.id}`)}
                    className="hover:bg-[#FAF7F0]/80 transition-colors cursor-pointer"
                  >
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 font-extrabold text-base flex items-center justify-center border border-indigo-100 flex-shrink-0">
                          {adminItem.email.charAt(0).toUpperCase()}
                        </div>
                        <div>
                          <p className="font-bold text-slate-900 text-sm">{adminItem.email}</p>
                          <p className="text-xs text-slate-400 font-mono">ID: {adminItem.id.substring(0, 8)}...</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-4 font-bold text-[#2F5233] capitalize">
                      {adminItem.role_name.replace('_', ' ')}
                    </td>
                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                        adminItem.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                      }`}>
                        {adminItem.is_active ? 'Active' : 'Suspended'}
                      </span>
                    </td>
                    <td className="py-4 px-4 font-semibold">
                      <span className={`inline-flex items-center gap-1 text-[11px] ${
                        adminItem.is_2fa_enabled ? 'text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full font-bold' : 'text-slate-500'
                      }`}>
                        <KeyRound className="w-3.5 h-3.5" />
                        <span>{adminItem.is_2fa_enabled ? 'Enabled' : 'Not Enabled'}</span>
                      </span>
                    </td>
                    <td className="py-4 px-4 font-medium text-slate-500">
                      {adminItem.created_at ? new Date(adminItem.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : 'N/A'}
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/admin/admins/${adminItem.id}`);
                        }}
                        className="px-3.5 py-1.5 bg-[#F2EDE1] hover:bg-[#2F5233] hover:text-white text-slate-700 font-bold rounded-xl transition-colors text-xs"
                      >
                        View & Edit
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Create Admin Modal */}
      {createModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleCreateSubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Add New Administrator</h3>
              <button type="button" onClick={() => setCreateModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Email Address *</label>
              <input
                type="email"
                value={newEmail}
                onChange={(e) => setNewEmail(e.target.value)}
                placeholder="newadmin@smartserve.com"
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Initial Password *</label>
              <div className="relative">
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  placeholder="Minimum 8 characters..."
                  className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 pr-10 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">RBAC Role *</label>
              <select
                value={newRole}
                onChange={(e) => setNewRole(e.target.value)}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
              >
                <option value="super_admin">Super Admin (Full Control)</option>
                <option value="operations_admin">Operations Admin</option>
                <option value="support_admin">Support Admin</option>
                <option value="catalog_admin">Catalog Admin</option>
              </select>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setCreateModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={createLoading}
                className="px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {createLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Create Account'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Permission Matrix Modal */}
      {matrixModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-2xl rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in max-h-[85vh] flex flex-col">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3 flex-shrink-0">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
                <Shield className="w-5 h-5 text-[#2F5233]" />
                <span>SmartServe RBAC System Permission Matrix</span>
              </h3>
              <button type="button" onClick={() => setMatrixModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="overflow-y-auto flex-1 pr-1 space-y-4 text-xs">
              <p className="text-slate-500 font-medium">
                Authoritative module permissions mapped to system RBAC roles. Backend authorization enforces these rules on all incoming requests.
              </p>

              <div className="border border-[#E5DEC9] rounded-2xl overflow-hidden">
                <table className="w-full text-left">
                  <thead className="bg-[#FAF7F0] text-slate-600 font-bold uppercase text-[10px] border-b border-[#E5DEC9]">
                    <tr>
                      <th className="py-3 px-4">Module</th>
                      <th className="py-3 px-4">Supported Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {matrix.map((row) => (
                      <tr key={row.module} className="hover:bg-[#FAF7F0]/60">
                        <td className="py-3 px-4 font-bold text-slate-900">{row.module}</td>
                        <td className="py-3 px-4 flex flex-wrap gap-1.5">
                          {row.actions.map((act) => (
                            <span key={act} className="px-2 py-0.5 bg-[#F2EDE1] text-[#2F5233] font-semibold rounded-lg text-[11px] border border-[#E5DEC9]">
                              {act}
                            </span>
                          ))}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="flex items-center justify-end pt-2 border-t border-[#E5DEC9]/60 flex-shrink-0">
              <button
                type="button"
                onClick={() => setMatrixModalOpen(false)}
                className="px-5 py-2 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-slate-800 font-bold rounded-xl text-xs"
              >
                Close Matrix
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
