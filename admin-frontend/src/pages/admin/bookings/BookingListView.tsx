import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  CalendarCheck, 
  Search, 
  LayoutGrid, 
  List, 
  Siren, 
  Loader2, 
  ChevronRight,
  CheckCircle2,
  X,
  MapPin
} from 'lucide-react';
import { getBookingsList, createEmergencyDispatchBooking } from '../../../api/bookings';
import type { BookingItem } from '../../../api/bookings';
import { getCustomersList } from '../../../api/customers';
import { getCatalogServices } from '../../../api/catalog';
import type { ServiceItem } from '../../../api/catalog';
import { formatCurrencyINR } from '../../../utils/formatters';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';

export const BookingListView: React.FC = () => {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState<BookingItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Search & Filter State
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [emergencyFilter, setEmergencyFilter] = useState<string>('');
  const [viewMode, setViewMode] = useState<'list' | 'grid'>('list');

  // Emergency Dispatch Modal State
  const [dispatchModalOpen, setDispatchModalOpen] = useState<boolean>(false);
  const [selectedCustomerId, setSelectedCustomerId] = useState<string>('');
  const [selectedServiceId, setSelectedServiceId] = useState<string>('');
  const [dispatchAddress, setDispatchAddress] = useState<string>('Flat 402, Sunshine Heights, Powai, Mumbai');
  const [dispatchPrice, setDispatchPrice] = useState<number>(999);
  const [dispatchFlag, setDispatchFlag] = useState<string>('Emergency — Circuit Breaker Trip');
  const [dispatchLoading, setDispatchLoading] = useState<boolean>(false);

  // Pre-loaded customers & services for modal selects
  const [customerOptions, setCustomerOptions] = useState<{ id: string; name: string }[]>([]);
  const [serviceOptions, setServiceOptions] = useState<{ id: string; name: string; price: number }[]>([]);

  // Real-Time WebSocket Emergency Alert State
  const [wsAlert, setWsAlert] = useState<{ title: string; body: string } | null>(null);
  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  const canManageBookings = hasPermission(adminSession, 'bookings:manage');

  const showToast = (text: string, type: 'success' | 'warning' | 'error' = 'success') => {
    setToastMessage({ text, type });
    setTimeout(() => setToastMessage(null), 5000);
  };

  const fetchBookingsData = async () => {
    setLoading(true);
    try {
      const data = await getBookingsList();
      setBookings(data);
    } catch (err: any) {
      console.error('Failed to load bookings directory.', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookingsData();
    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});

    // Pre-fetch option lists for Emergency Dispatch Modal
    getCustomersList().then((custs) => {
      setCustomerOptions(custs.map((c) => ({ id: c.id, name: c.full_name })));
      if (custs.length > 0) setSelectedCustomerId(custs[0].id);
    }).catch(() => {});

    getCatalogServices().then((srvs: ServiceItem[]) => {
      setServiceOptions(srvs.map((s: ServiceItem) => ({ id: s.id, name: s.name, price: s.base_price })));
      if (srvs.length > 0) {
        setSelectedServiceId(srvs[0].id);
        setDispatchPrice(srvs[0].base_price || 999);
      }
    }).catch(() => {});

    // Real-Time Emergency Alerts WebSocket Connection
    const rawApiUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
    const isHttps = rawApiUrl.startsWith('https:') || window.location.protocol === 'https:';
    const wsProtocol = isHttps ? 'wss:' : 'ws:';
    const hostDomain = rawApiUrl.replace(/^https?:\/\//, '').replace(/\/api\/v1\/?$/, '');
    const wsUrl = `${wsProtocol}//${hostDomain}/ws/emergency-alerts`;
    let ws: WebSocket | null = null;

    try {
      ws = new WebSocket(wsUrl);
      ws.onmessage = (event) => {
        try {
          const payload = JSON.parse(event.data);
          if (payload.type === 'EMERGENCY_ALERT' || payload.event === 'emergency_dispatch') {
            setWsAlert({
              title: payload.title || '🚨 Real-Time Emergency Dispatch Event',
              body: payload.message || 'New emergency service request logged in system.'
            });
            fetchBookingsData();
          }
        } catch (e) {}
      };
    } catch (err) {}

    return () => {
      if (ws) ws.close();
    };
  }, []);

  const handleDispatchSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCustomerId || !selectedServiceId) {
      showToast('Please select valid customer and service.', 'error');
      return;
    }
    setDispatchLoading(true);
    try {
      const newBooking = await createEmergencyDispatchBooking({
        customer_id: selectedCustomerId,
        service_id: selectedServiceId,
        scheduled_time: new Date().toISOString(),
        address: dispatchAddress,
        total_price: dispatchPrice,
        emergency_flag: dispatchFlag
      });
      showToast(`Emergency Dispatch #${newBooking.id.substring(0, 8)} created successfully!`, 'success');
      setDispatchModalOpen(false);
      fetchBookingsData();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Emergency dispatch creation failed.', 'error');
    } finally {
      setDispatchLoading(false);
    }
  };

  const filteredBookings = useMemo(() => {
    return bookings.filter((b) => {
      const matchesSearch = 
        b.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (b.customer_name && b.customer_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (b.provider_name && b.provider_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (b.service_name && b.service_name.toLowerCase().includes(searchTerm.toLowerCase()));

      const matchesStatus = !statusFilter || b.status.toLowerCase() === statusFilter.toLowerCase();

      const matchesEmergency = !emergencyFilter ||
        (emergencyFilter === 'emergency' && !!b.emergency_flag) ||
        (emergencyFilter === 'standard' && !b.emergency_flag);

      return matchesSearch && matchesStatus && matchesEmergency;
    });
  }, [bookings, searchTerm, statusFilter, emergencyFilter]);

  const emergencyCount = bookings.filter((b) => b.emergency_flag).length;

  const getStatusBadgeStyle = (statusStr: string) => {
    switch (statusStr.toLowerCase()) {
      case 'requested':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'assigned':
        return 'bg-[#F2EDE1] text-[#2F5233] border-[#E5DEC9]';
      case 'accepted':
        return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      case 'started':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'completed':
      case 'paid':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'cancelled':
      case 'rejected':
      case 'expired':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      default:
        return 'bg-[#F2EDE1] text-slate-700 border-[#E5DEC9]';
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
        <p className="text-sm font-semibold text-slate-600">Loading Bookings Directory & Live Dispatch Queue...</p>
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

      {/* WebSocket Real-Time Emergency Alert Banner */}
      {wsAlert && (
        <div className="bg-rose-600 text-white p-4 rounded-2xl shadow-lg flex items-center justify-between animate-bounce">
          <div className="flex items-center gap-3">
            <Siren className="w-5 h-5 animate-pulse text-amber-300" />
            <div>
              <p className="font-bold text-xs">{wsAlert.title}</p>
              <p className="text-[11px] text-rose-100">{wsAlert.body}</p>
            </div>
          </div>
          <button onClick={() => setWsAlert(null)} className="text-white/80 hover:text-white p-1">
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight">Bookings & Operations</h1>
            <span className="text-xs font-bold text-[#2F5233] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              {bookings.length} Total Bookings
            </span>
            {emergencyCount > 0 && (
              <span className="text-xs font-bold text-rose-700 bg-rose-50 px-3 py-1 rounded-full border border-rose-200 flex items-center gap-1 animate-pulse">
                <Siren className="w-3.5 h-3.5" />
                <span>{emergencyCount} Emergency</span>
              </span>
            )}
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            Live operational control tower, booking state machine transitions, emergency dispatch, and provider assignment
          </p>
        </div>

        <div className="flex items-center gap-3 flex-wrap">
          {canManageBookings ? (
            <button
              onClick={() => setDispatchModalOpen(true)}
              className="px-5 py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-2xl shadow-sm text-xs transition-colors flex items-center gap-2"
            >
              <Siren className="w-4 h-4" />
              <span>Emergency Dispatch</span>
            </button>
          ) : (
            <button
              disabled
              title="Emergency dispatch creation requires 'bookings:manage' permission."
              className="px-5 py-2.5 bg-slate-200 text-slate-500 font-bold rounded-2xl text-xs flex items-center gap-2 cursor-not-allowed opacity-70 border border-slate-300"
            >
              <Siren className="w-4 h-4 text-slate-400" />
              <span>Emergency Dispatch (Disabled)</span>
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
            placeholder="Search booking ID, customer, provider, service..."
            className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] font-medium"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto justify-end">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          >
            <option value="">All Statuses</option>
            <option value="requested">Requested</option>
            <option value="assigned">Assigned</option>
            <option value="accepted">Accepted</option>
            <option value="started">Started</option>
            <option value="completed">Completed</option>
            <option value="paid">Paid</option>
            <option value="cancelled">Cancelled</option>
          </select>

          <select
            value={emergencyFilter}
            onChange={(e) => setEmergencyFilter(e.target.value)}
            className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
          >
            <option value="">All Priority Types</option>
            <option value="emergency">Emergency Only</option>
            <option value="standard">Standard Only</option>
          </select>

          {/* List / Grid View Toggle */}
          <div className="flex items-center bg-[#F2EDE1] p-1 rounded-xl border border-[#E5DEC9]">
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'list' ? 'bg-white text-[#2F5233] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="List View (Primary)"
            >
              <List className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-white text-[#2F5233] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Directory Render */}
      {filteredBookings.length === 0 ? (
        <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
          <CalendarCheck className="w-8 h-8 text-slate-400 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No bookings found.</h3>
          <p className="text-xs text-slate-500 font-medium">Try changing your search terms or status filter settings.</p>
        </div>
      ) : viewMode === 'list' ? (
        <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#FAF7F0] text-slate-600 font-bold uppercase text-[10px] border-b border-[#E5DEC9]">
                <tr>
                  <th className="py-3.5 px-6">Booking ID & Date</th>
                  <th className="py-3.5 px-4">Customer</th>
                  <th className="py-3.5 px-4">Service</th>
                  <th className="py-3.5 px-4">Assigned Provider</th>
                  <th className="py-3.5 px-4">Amount (₹)</th>
                  <th className="py-3.5 px-4">Priority / Emergency</th>
                  <th className="py-3.5 px-4">Status</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredBookings.map((b) => (
                  <tr
                    key={b.id}
                    onClick={() => navigate(`/admin/bookings/${b.id}`)}
                    className="hover:bg-[#FAF7F0]/80 transition-colors cursor-pointer"
                  >
                    <td className="py-4 px-6">
                      <p className="font-mono font-bold text-slate-900 text-xs">#{b.id.substring(0, 8)}</p>
                      <p className="text-[11px] text-slate-400 font-medium mt-0.5">
                        {b.scheduled_time ? new Date(b.scheduled_time).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : 'N/A'}
                      </p>
                    </td>

                    <td className="py-4 px-4 font-bold text-slate-900">
                      {b.customer_name || 'Customer'}
                    </td>

                    <td className="py-4 px-4 font-semibold text-[#2F5233]">
                      {b.service_name || 'Home Service'}
                    </td>

                    <td className="py-4 px-4 font-medium text-slate-700">
                      {b.provider_name ? (
                        <span className="font-bold text-slate-800">{b.provider_name}</span>
                      ) : (
                        <span className="text-slate-400 italic text-[11px]">Provider not assigned</span>
                      )}
                    </td>

                    <td className="py-4 px-4 font-extrabold text-slate-900 text-sm">
                      {formatCurrencyINR(b.total_price)}
                    </td>

                    <td className="py-4 px-4">
                      {b.emergency_flag ? (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-rose-50 text-rose-700 border border-rose-200">
                          <Siren className="w-3 h-3 text-rose-600 animate-pulse" />
                          <span>Emergency</span>
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px] font-semibold">Standard</span>
                      )}
                    </td>

                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${getStatusBadgeStyle(b.status)}`}>
                        {b.status}
                      </span>
                    </td>

                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/admin/bookings/${b.id}`);
                        }}
                        className="px-3.5 py-1.5 bg-[#F2EDE1] hover:bg-[#2F5233] hover:text-white text-slate-700 font-bold rounded-xl transition-colors text-xs"
                      >
                        View & Control
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredBookings.map((b) => (
            <div
              key={b.id}
              onClick={() => navigate(`/admin/bookings/${b.id}`)}
              className="group bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col justify-between space-y-4"
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] font-mono font-bold text-slate-400 block">#{b.id.substring(0, 8)}</span>
                    <h3 className="text-base font-bold font-serif text-[#1F2A1E] group-hover:text-[#2F5233] transition-colors">
                      {b.service_name || 'Service Booking'}
                    </h3>
                  </div>

                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${getStatusBadgeStyle(b.status)}`}>
                    {b.status}
                  </span>
                </div>

                <div className="space-y-1.5 text-xs text-slate-600">
                  <p><strong>Customer:</strong> {b.customer_name || 'Customer'}</p>
                  <p><strong>Provider:</strong> {b.provider_name || 'Provider not assigned'}</p>
                  <p className="flex items-center gap-1 text-[11px] text-slate-400">
                    <MapPin className="w-3 h-3" /> {b.address ? `${b.address.substring(0, 32)}...` : 'Location'}
                  </p>
                </div>
              </div>

              <div className="pt-3 border-t border-[#E5DEC9]/60 flex items-center justify-between text-xs">
                <span className="text-base font-extrabold text-slate-900">₹{b.total_price.toLocaleString('en-IN')}</span>

                <span className="font-bold text-[#2F5233] group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                  <span>View Detail</span>
                  <ChevronRight className="w-4 h-4" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Emergency Dispatch Modal */}
      {dispatchModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleDispatchSubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
                <Siren className="w-5 h-5 text-rose-600 animate-pulse" />
                <span>Create Emergency Dispatch</span>
              </h3>
              <button type="button" onClick={() => setDispatchModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Select Customer *</label>
              <select
                value={selectedCustomerId}
                onChange={(e) => setSelectedCustomerId(e.target.value)}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                required
              >
                {customerOptions.map((c) => (
                  <option key={c.id} value={c.id}>{c.name}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Emergency Service *</label>
              <select
                value={selectedServiceId}
                onChange={(e) => {
                  setSelectedServiceId(e.target.value);
                  const found = serviceOptions.find((s) => s.id === e.target.value);
                  if (found) setDispatchPrice(found.price || 999);
                }}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                required
              >
                {serviceOptions.map((s) => (
                  <option key={s.id} value={s.id}>{s.name} (₹{s.price})</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Emergency Priority Flag *</label>
              <input
                type="text"
                value={dispatchFlag}
                onChange={(e) => setDispatchFlag(e.target.value)}
                placeholder="e.g. Emergency — Circuit Breaker Trip"
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-semibold text-rose-700 focus:outline-none focus:ring-2 focus:ring-rose-500/40"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Service Address *</label>
              <textarea
                value={dispatchAddress}
                onChange={(e) => setDispatchAddress(e.target.value)}
                placeholder="Full address..."
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-medium focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                rows={2}
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Amount (₹) *</label>
              <input
                type="number"
                value={dispatchPrice}
                onChange={(e) => setDispatchPrice(Number(e.target.value))}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-extrabold text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                required
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setDispatchModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={dispatchLoading}
                className="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {dispatchLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Dispatch Emergency Unit'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
