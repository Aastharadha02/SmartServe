import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCustomerBookings, BookingDetail } from '../api/bookings';
import { formatCurrencyINR } from '../utils/formatters';
import { getServiceImage } from '../utils/serviceImages';
import { Calendar, Clock, ChevronRight, Plus, AlertCircle, RefreshCw } from 'lucide-react';
import { SmartServeLoader } from '../components/common/SmartServeLoader';

export const CustomerBookings: React.FC = () => {
  const navigate = useNavigate();
  const [bookings, setBookings] = useState<BookingDetail[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('all');

  const fetchBookings = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCustomerBookings();
      setBookings(data);
    } catch (err: any) {
      if (err.response) {
        setError(err.response.data?.detail || `API Error (${err.response.status}): Failed to fetch bookings.`);
      } else if (err.request) {
        setError('Unable to connect to SmartServe API. Please verify network connectivity and backend server availability.');
      } else {
        setError('An unexpected error occurred while loading your bookings.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBookings();
  }, []);

  const filteredBookings = bookings.filter((b) => {
    if (statusFilter === 'all') return true;
    const st = b.status.toLowerCase();
    if (statusFilter === 'active') return st === 'requested' || st === 'assigned' || st === 'accepted' || st === 'started';
    if (statusFilter === 'completed') return st === 'completed' || st === 'paid';
    if (statusFilter === 'cancelled') return st === 'cancelled' || st === 'rejected';
    return true;
  });

  return (
    <div className="space-y-8 font-sans max-w-5xl mx-auto">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">My Service Bookings</h1>
          <p className="text-sm text-slate-500 font-medium mt-1">
            Track real-time status and technician assignments for your bookings.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchBookings}
            className="flex items-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs rounded-xl border border-slate-200 shadow-2xs transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-400" />
            <span>Sync Live</span>
          </button>
          
          <button
            onClick={() => navigate('/catalog')}
            className="flex items-center gap-2 px-5 py-2.5 bg-[#2563EB] hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>+ Book New Service</span>
          </button>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-3">
        {[
          { key: 'all', label: `All (${bookings.length})` },
          { key: 'active', label: 'Active & In-Progress' },
          { key: 'completed', label: 'Completed' },
          { key: 'cancelled', label: 'Cancelled' },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setStatusFilter(tab.key)}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              statusFilter === tab.key
                ? 'bg-blue-50 text-[#2563EB] border border-blue-200'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Error View */}
      {error && (
        <div className="p-8 bg-white border border-red-200 rounded-3xl text-center space-y-3 shadow-sm">
          <AlertCircle className="w-10 h-10 text-rose-500 mx-auto" />
          <h3 className="text-base font-bold text-slate-900">Failed to Load Bookings</h3>
          <p className="text-xs text-slate-600 max-w-md mx-auto">{error}</p>
          <button
            onClick={fetchBookings}
            className="px-4 py-2 bg-[#2563EB] text-white text-xs font-bold rounded-xl inline-flex items-center gap-2"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry Connection</span>
          </button>
        </div>
      )}

      {/* Bookings List */}
      {loading ? (
        <div className="flex items-center justify-center py-16">
          <SmartServeLoader size="lg" text="Fetching your bookings from database..." />
        </div>
      ) : filteredBookings.length > 0 ? (
        <div className="space-y-4">
          {filteredBookings.map((b) => {
            const imgUrl = getServiceImage(b.category, undefined, b.service_name);
            const stLower = b.status.toLowerCase();
            return (
              <div
                key={b.id}
                onClick={() => navigate(`/bookings/${b.id}`)}
                className="group bg-white p-5 sm:p-6 rounded-3xl border border-slate-200/90 shadow-2xs hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
              >
                <div className="flex items-center gap-4 min-w-0">
                  <div className="w-16 h-16 rounded-2xl overflow-hidden bg-slate-100 flex-shrink-0">
                    <img
                      src={imgUrl}
                      alt={b.service_name}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                    />
                  </div>

                  <div className="min-w-0 space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-slate-500">{b.booking_reference}</span>
                      <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                        stLower === 'completed' || stLower === 'paid'
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : stLower === 'cancelled'
                          ? 'bg-rose-50 text-rose-700 border-rose-200'
                          : 'bg-blue-50 text-[#2563EB] border-blue-200'
                      }`}>
                        {b.status}
                      </span>
                    </div>

                    <h3 className="font-extrabold text-slate-900 text-base truncate group-hover:text-[#2563EB] transition-colors">
                      {b.service_name}
                    </h3>

                    <div className="flex items-center gap-4 text-xs text-slate-500 font-medium">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        <span>{b.scheduled_date} at {b.scheduled_time}</span>
                      </span>
                      <span>• Provider: <strong className="text-slate-700">{b.provider_name || 'Assigned Soon'}</strong></span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center justify-between sm:justify-end gap-5 w-full sm:w-auto pt-3 sm:pt-0 border-t sm:border-t-0 border-slate-100">
                  <div className="text-left sm:text-right">
                    <span className="text-lg font-extrabold text-slate-900 font-mono block">
                      {formatCurrencyINR(b.total_price || b.total_amount || 0)}
                    </span>
                    <span className="text-[11px] font-semibold text-slate-400 block">Tap to view detail</span>
                  </div>
                  <ChevronRight className="w-5 h-5 text-slate-400 group-hover:translate-x-1 transition-transform" />
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-white p-12 rounded-3xl border border-slate-200 text-center space-y-4">
          <Calendar className="w-12 h-12 text-slate-400 mx-auto" />
          <div className="space-y-1">
            <h3 className="text-base font-bold text-slate-800">No Bookings Found</h3>
            <p className="text-xs text-slate-500">You have no active or completed service bookings recorded.</p>
          </div>
          <button
            onClick={() => navigate('/catalog')}
            className="px-5 py-2.5 bg-[#2563EB] text-white font-bold text-xs rounded-xl inline-flex items-center gap-2 shadow-xs"
          >
            <Plus className="w-4 h-4" />
            <span>Book Your First Service</span>
          </button>
        </div>
      )}

    </div>
  );
};

export default CustomerBookings;
