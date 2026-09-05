import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Users, 
  Search, 
  LayoutGrid, 
  List, 
  ShieldCheck, 
  Clock, 
  Star, 
  Award, 
  Loader2, 
  ChevronRight
} from 'lucide-react';
import { getProvidersList } from '../../../api/providers';
import type { ProviderItem } from '../../../api/providers';

export const ProviderListView: React.FC = () => {
  const navigate = useNavigate();
  const [providers, setProviders] = useState<ProviderItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [verificationFilter, setVerificationFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const fetchProviders = async () => {
    setLoading(true);
    try {
      const data = await getProvidersList();
      setProviders(data);
    } catch (err: any) {
      console.error('Failed to load provider directory.', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProviders();
  }, []);

  const filteredProviders = useMemo(() => {
    return providers.filter((p) => {
      const matchesSearch = 
        p.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.id.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesVerification = !verificationFilter ||
        (verificationFilter === 'verified' && p.is_verified) ||
        (verificationFilter === 'pending' && !p.is_verified && p.documents.some((d) => d.verification_status === 'Pending')) ||
        (verificationFilter === 'rejected' && !p.is_verified && p.documents.some((d) => d.verification_status === 'Rejected'));

      const matchesStatus = !statusFilter ||
        (statusFilter === 'active' && p.is_active) ||
        (statusFilter === 'suspended' && !p.is_active);

      const matchesCategory = !categoryFilter || p.category.toLowerCase().includes(categoryFilter.toLowerCase());

      return matchesSearch && matchesVerification && matchesStatus && matchesCategory;
    });
  }, [providers, searchTerm, verificationFilter, statusFilter, categoryFilter]);

  const verifiedCount = providers.filter((p) => p.is_verified).length;
  const pendingCount = providers.filter((p) => !p.is_verified && p.documents.some((d) => d.verification_status === 'Pending')).length;

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-slate-600">Loading SmartServe Provider Directory...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-slate-800">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight">Provider Directory</h1>
            <span className="text-xs font-bold text-[#2F5233] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              {providers.length} Registered Providers
            </span>
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            Manage provider verification documents, AI OCR signals, performance rankings, and account access
          </p>
        </div>

        <div className="flex items-center gap-3 bg-[#FAF7F0] border border-[#E5DEC9] px-4 py-2.5 rounded-2xl text-xs font-semibold">
          <div className="flex items-center gap-1.5 text-emerald-700">
            <ShieldCheck className="w-4 h-4 text-emerald-500" />
            <span>{verifiedCount} Verified</span>
          </div>
          <div className="h-4 w-px bg-slate-200" />
          <div className="flex items-center gap-1.5 text-amber-700">
            <Clock className="w-4 h-4 text-amber-500" />
            <span>{pendingCount} Pending</span>
          </div>
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
            placeholder="Search provider name, email, or ID..."
            className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] font-medium"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto justify-end">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          >
            <option value="">All Categories</option>
            <option value="Beauty">Beauty, Salon & Spa</option>
            <option value="Domestic Help">Domestic Help & Cooking</option>
            <option value="Electrician">Electrician & Home Repairs</option>
            <option value="Painting">Painting & Home Improvement</option>
            <option value="Appliance">AC & Appliance Repair</option>
            <option value="Cleaning">Cleaning & Home Cleaning</option>
          </select>
          <select
            value={verificationFilter}
            onChange={(e) => setVerificationFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          >
            <option value="">All Verifications</option>
            <option value="verified">Verified Only</option>
            <option value="pending">Pending Review</option>
            <option value="rejected">Rejected</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          >
            <option value="">All Statuses</option>
            <option value="active">Active Only</option>
            <option value="suspended">Suspended</option>
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
      {filteredProviders.length === 0 ? (
        <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
          <Users className="w-8 h-8 text-slate-400 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No providers match the selected filters.</h3>
          <p className="text-sm text-slate-500 font-medium">Try clearing your search or filter keywords.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProviders.map((provider) => (
            <div
              key={provider.id}
              onClick={() => navigate(`/admin/providers/${provider.id}`)}
              className="group bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col justify-between space-y-5"
            >
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-2xl bg-[#F2EDE1] text-[#2F5233] font-bold text-lg flex items-center justify-center border border-[#E5DEC9]">
                      {provider.full_name.charAt(0)}
                    </div>
                    <div>
                      <h3 className="text-base md:text-lg font-bold font-serif text-[#1F2A1E] group-hover:text-[#2F5233] transition-colors">
                        {provider.full_name}
                      </h3>
                      <p className="text-xs text-slate-500 font-semibold">{provider.email}</p>
                    </div>
                  </div>

                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${
                    provider.is_active
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : 'bg-rose-50 text-rose-700 border-rose-200'
                  }`}>
                    {provider.is_active ? 'Active' : 'Suspended'}
                  </span>
                </div>

                <div className="flex items-center justify-between text-xs pt-1">
                  <span className="font-semibold text-slate-600">{provider.category}</span>
                  <span className="font-mono text-slate-500">Exp: {provider.experience_years} yrs</span>
                </div>

                <div className="grid grid-cols-2 gap-2 p-3 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9]/80 text-xs">
                  <div>
                    <span className="text-[10px] text-slate-400 font-semibold uppercase">Rating</span>
                    <p className="font-bold text-slate-900 flex items-center gap-1">
                      <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                      <span>{provider.rating}</span>
                      <span className="text-slate-400 font-normal">({provider.completed_bookings})</span>
                    </p>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 font-semibold uppercase">Rank Score</span>
                    <p className="font-bold text-[#2F5233] flex items-center gap-1">
                      <Award className="w-3.5 h-3.5" />
                      <span>{provider.composite_rank_score}</span>
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-[#E5DEC9]/60 flex items-center justify-between text-xs">
                <span className={`inline-flex items-center gap-1 px-2.5 py-1 rounded-xl font-bold border ${
                  provider.is_verified
                    ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    : 'bg-amber-50 text-amber-700 border-amber-200'
                }`}>
                  {provider.is_verified ? <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" /> : <Clock className="w-3.5 h-3.5 text-amber-500" />}
                  <span>{provider.is_verified ? 'Verified Provider' : 'Pending Review'}</span>
                </span>

                <span className="font-bold text-[#2F5233] group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                  <span>View Profile</span>
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
                  <th className="py-3.5 px-6">Provider</th>
                  <th className="py-3.5 px-4">Category</th>
                  <th className="py-3.5 px-4">Rating & Bookings</th>
                  <th className="py-3.5 px-4">Verification</th>
                  <th className="py-3.5 px-4">Account Status</th>
                  <th className="py-3.5 px-4">Rank Score</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredProviders.map((provider) => (
                  <tr
                    key={provider.id}
                    onClick={() => navigate(`/admin/providers/${provider.id}`)}
                    className="hover:bg-[#FAF7F0]/80 transition-colors cursor-pointer"
                  >
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-[#F2EDE1] text-[#2F5233] font-bold text-base flex items-center justify-center border border-[#E5DEC9] flex-shrink-0">
                          {provider.full_name.charAt(0)}
                        </div>
                        <div>
                          <p className="font-bold text-slate-900 text-sm">{provider.full_name}</p>
                          <p className="text-xs text-slate-500 font-semibold">{provider.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-4 font-semibold text-slate-700">
                      {provider.category}
                    </td>
                    <td className="py-4 px-4">
                      <div className="flex items-center gap-1 font-bold text-slate-900">
                        <Star className="w-3.5 h-3.5 fill-amber-400 text-amber-400" />
                        <span>{provider.rating}</span>
                        <span className="text-xs text-slate-400 font-normal">({provider.completed_bookings} jobs)</span>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full font-bold text-[11px] ${
                        provider.is_verified ? 'bg-emerald-50 text-emerald-700' : 'bg-amber-50 text-amber-700'
                      }`}>
                        {provider.is_verified ? <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" /> : <Clock className="w-3.5 h-3.5 text-amber-500" />}
                        <span>{provider.is_verified ? 'Verified' : 'Pending'}</span>
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-bold ${
                        provider.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                      }`}>
                        {provider.is_active ? 'Active' : 'Suspended'}
                      </span>
                    </td>
                    <td className="py-4 px-4 font-mono font-bold text-[#2F5233]">
                      {provider.composite_rank_score}
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/admin/providers/${provider.id}`);
                        }}
                        className="px-3.5 py-1.5 bg-[#F2EDE1] hover:bg-[#2F5233] hover:text-white text-slate-700 font-bold rounded-xl transition-colors text-xs"
                      >
                        View Profile
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
