import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  UserCheck, 
  Search, 
  LayoutGrid, 
  List, 
  ShieldAlert, 
  CalendarCheck, 
  Loader2, 
  ChevronRight,
  Users
} from 'lucide-react';
import { getCustomersList } from '../../../api/customers';
import type { CustomerItem } from '../../../api/customers';

export const CustomerListView: React.FC = () => {
  const navigate = useNavigate();
  const [customers, setCustomers] = useState<CustomerItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [riskFilter, setRiskFilter] = useState<string>('');
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  const fetchCustomers = async () => {
    setLoading(true);
    try {
      const data = await getCustomersList();
      setCustomers(data);
    } catch (err: any) {
      console.error('Failed to load customer directory.', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const filteredCustomers = useMemo(() => {
    return customers.filter((c) => {
      const matchesSearch = 
        c.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
        c.id.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesStatus = !statusFilter ||
        (statusFilter === 'active' && c.is_active) ||
        (statusFilter === 'suspended' && !c.is_active);

      const matchesRisk = !riskFilter ||
        (riskFilter === 'flagged' && c.is_flagged) ||
        (riskFilter === 'clean' && !c.is_flagged);

      return matchesSearch && matchesStatus && matchesRisk;
    });
  }, [customers, searchTerm, statusFilter, riskFilter]);

  const activeCount = customers.filter((c) => c.is_active).length;
  const flaggedCount = customers.filter((c) => c.is_flagged).length;

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#5CA8FF]" />
        <p className="text-sm font-semibold text-slate-600">Loading SmartServe Customer Directory...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-slate-800">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">Customer Directory</h1>
            <span className="text-xs font-bold text-[#5CA8FF] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              {customers.length} Accounts
            </span>
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            Manage customer accounts, booking history, fraud risk flags, and access control
          </p>
        </div>

        <div className="flex items-center gap-3 bg-slate-50 border border-slate-200 px-4 py-2.5 rounded-2xl text-xs font-semibold">
          <div className="flex items-center gap-1.5 text-emerald-700">
            <UserCheck className="w-4 h-4 text-emerald-500" />
            <span>{activeCount} Active</span>
          </div>
          <div className="h-4 w-px bg-slate-200" />
          <div className="flex items-center gap-1.5 text-rose-700">
            <ShieldAlert className="w-4 h-4 text-rose-500" />
            <span>{flaggedCount} Risk Flagged</span>
          </div>
        </div>
      </div>

      {/* Search & Filter Controls */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        <div className="relative flex-1 w-full max-w-md">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search customer name, email, or ID..."
            className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 font-medium"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto justify-end">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          >
            <option value="">All Account Statuses</option>
            <option value="active">Active Only</option>
            <option value="suspended">Suspended Only</option>
          </select>

          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          >
            <option value="">All Risk Levels</option>
            <option value="flagged">Flagged Only</option>
            <option value="clean">Not Flagged</option>
          </select>

          {/* Grid / List View Toggle */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-white text-[#5CA8FF] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'list' ? 'bg-white text-[#5CA8FF] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="List View"
            >
              <List className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Directory Render */}
      {filteredCustomers.length === 0 ? (
        <div className="py-12 p-6 text-center bg-white rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <Users className="w-8 h-8 text-slate-400 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No customers found.</h3>
          <p className="text-xs text-slate-500 font-medium">Try changing your search terms or filter settings.</p>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCustomers.map((customer) => (
            <div
              key={customer.id}
              onClick={() => navigate(`/admin/customers/${customer.id}`)}
              className="group bg-white p-6 rounded-3xl border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col justify-between space-y-5"
            >
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-2xl bg-blue-50 text-[#5CA8FF] font-extrabold text-lg flex items-center justify-center border border-blue-100 flex-shrink-0">
                      {customer.full_name.charAt(0)}
                    </div>
                    <div className="overflow-hidden">
                      <h3 className="text-base md:text-lg font-bold text-slate-900 group-hover:text-[#5CA8FF] transition-colors truncate">
                        {customer.full_name}
                      </h3>
                      <p className="text-xs text-slate-500 font-semibold truncate">{customer.email}</p>
                    </div>
                  </div>

                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border flex-shrink-0 ${
                    customer.is_active
                      ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                      : 'bg-rose-50 text-rose-700 border-rose-200'
                  }`}>
                    {customer.is_active ? 'Active' : 'Suspended'}
                  </span>
                </div>

                <div className="grid grid-cols-2 gap-2 p-3 bg-slate-50 rounded-2xl border border-slate-200/80 text-xs">
                  <div>
                    <span className="text-[10px] text-slate-400 font-semibold uppercase">Total Bookings</span>
                    <p className="font-bold text-slate-900 flex items-center gap-1.5 mt-0.5">
                      <CalendarCheck className="w-3.5 h-3.5 text-[#5CA8FF]" />
                      <span>{customer.bookings_count} jobs</span>
                    </p>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 font-semibold uppercase">Risk Status</span>
                    <p className={`font-bold text-xs mt-0.5 flex items-center gap-1 ${
                      customer.is_flagged ? 'text-rose-600' : 'text-slate-600'
                    }`}>
                      {customer.is_flagged ? <ShieldAlert className="w-3.5 h-3.5 text-rose-500" /> : null}
                      <span>{customer.is_flagged ? 'Flagged' : 'Clean'}</span>
                    </p>
                  </div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-400 font-medium">
                  Joined: {customer.created_at ? new Date(customer.created_at).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' }) : 'N/A'}
                </span>

                <span className="font-bold text-[#5CA8FF] group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                  <span>View Details</span>
                  <ChevronRight className="w-4 h-4" />
                </span>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-bold uppercase text-[10px] border-b border-slate-200">
                <tr>
                  <th className="py-3.5 px-6">Customer</th>
                  <th className="py-3.5 px-4">Contact</th>
                  <th className="py-3.5 px-4">Bookings</th>
                  <th className="py-3.5 px-4">Account Status</th>
                  <th className="py-3.5 px-4">Risk Flag</th>
                  <th className="py-3.5 px-4">Joined</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredCustomers.map((customer) => (
                  <tr
                    key={customer.id}
                    onClick={() => navigate(`/admin/customers/${customer.id}`)}
                    className="hover:bg-slate-50/80 transition-colors cursor-pointer"
                  >
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-blue-50 text-[#5CA8FF] font-extrabold text-base flex items-center justify-center border border-blue-100 flex-shrink-0">
                          {customer.full_name.charAt(0)}
                        </div>
                        <div>
                          <p className="font-bold text-slate-900 text-sm">{customer.full_name}</p>
                          <p className="text-xs text-slate-400 font-mono">ID: {customer.id.substring(0, 8)}...</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-4">
                      <p className="font-semibold text-slate-800">{customer.email}</p>
                      <p className="text-slate-400 font-mono">{customer.phone || 'N/A'}</p>
                    </td>
                    <td className="py-4 px-4 font-bold text-slate-900">
                      {customer.bookings_count} bookings
                    </td>
                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold ${
                        customer.is_active ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                      }`}>
                        {customer.is_active ? 'Active' : 'Suspended'}
                      </span>
                    </td>
                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-bold ${
                        customer.is_flagged ? 'bg-rose-50 text-rose-700' : 'bg-slate-100 text-slate-600'
                      }`}>
                        {customer.is_flagged ? <ShieldAlert className="w-3.5 h-3.5 text-rose-500" /> : null}
                        <span>{customer.is_flagged ? 'Flagged' : 'Clean'}</span>
                      </span>
                    </td>
                    <td className="py-4 px-4 font-medium text-slate-500">
                      {customer.created_at ? new Date(customer.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : 'N/A'}
                    </td>
                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/admin/customers/${customer.id}`);
                        }}
                        className="px-3.5 py-1.5 bg-slate-100 hover:bg-[#5CA8FF] hover:text-white text-slate-700 font-bold rounded-xl transition-colors text-xs"
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
