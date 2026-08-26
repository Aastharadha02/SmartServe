import React, { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  HelpCircle, 
  Search, 
  List, 
  LayoutGrid, 
  ChevronRight,
  Loader2,
  Flame
} from 'lucide-react';
import { 
  getSupportTicketsList, 
  getSupportDashboardMetrics 
} from '../../../api/support';
import type { SupportTicketItem, SupportMetrics } from '../../../api/support';

export const SupportListView: React.FC = () => {
  const navigate = useNavigate();
  const [tickets, setTickets] = useState<SupportTicketItem[]>([]);
  const [metrics, setMetrics] = useState<SupportMetrics>({
    open_tickets: 0,
    in_progress: 0,
    escalated: 0,
    high_priority: 0,
    resolved: 0,
  });
  const [loading, setLoading] = useState<boolean>(true);

  // Search & Filters
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [priorityFilter, setPriorityFilter] = useState<string>('');
  const [escalatedFilter, setEscalatedFilter] = useState<string>('');
  const [viewMode, setViewMode] = useState<'list' | 'grid'>('list');

  const fetchTicketsData = async () => {
    setLoading(true);
    try {
      const ticketsData = await getSupportTicketsList();
      setTickets(ticketsData);
      const metricsData = await getSupportDashboardMetrics();
      setMetrics(metricsData);
    } catch (err: any) {
      console.error('Failed to load support ticket directory.', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTicketsData();
  }, []);

  const filteredTickets = useMemo(() => {
    return tickets.filter((t) => {
      const matchesSearch = 
        t.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (t.customer_name && t.customer_name.toLowerCase().includes(searchTerm.toLowerCase())) ||
        t.subject.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesStatus = !statusFilter || t.status.toLowerCase() === statusFilter.toLowerCase();

      const matchesPriority = !priorityFilter || t.priority.toLowerCase() === priorityFilter.toLowerCase();

      const matchesEscalation = !escalatedFilter ||
        (escalatedFilter === 'escalated' && t.escalated_to_admin) ||
        (escalatedFilter === 'normal' && !t.escalated_to_admin);

      return matchesSearch && matchesStatus && matchesPriority && matchesEscalation;
    });
  }, [tickets, searchTerm, statusFilter, priorityFilter, escalatedFilter]);

  const getPriorityBadgeStyle = (p: string) => {
    switch (p.toLowerCase()) {
      case 'urgent':
        return 'bg-rose-50 text-rose-700 border-rose-200 font-extrabold';
      case 'high':
        return 'bg-amber-50 text-amber-700 border-amber-200 font-bold';
      case 'medium':
        return 'bg-blue-50 text-[#5CA8FF] border-blue-200 font-semibold';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200 font-medium';
    }
  };

  const getStatusBadgeStyle = (s: string) => {
    switch (s.toLowerCase()) {
      case 'open':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'in_progress':
        return 'bg-blue-50 text-[#5CA8FF] border-blue-200';
      case 'resolved':
      case 'closed':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#5CA8FF]" />
        <p className="text-sm font-semibold text-slate-600">Loading Support Directory & Ticket Escalation Queue...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto font-sans text-slate-800">
      {/* Header Banner */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold text-slate-900 tracking-tight">Support Center</h1>
            <span className="text-xs font-bold text-[#5CA8FF] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              {tickets.length} Tickets Total
            </span>
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            Customer support operations, ticket escalation management, conversation threads, and evidence access
          </p>
        </div>

        {/* Real Summary Metrics Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3">
          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
            <span className="text-[11px] font-bold text-slate-400 block uppercase">Open Tickets</span>
            <span className="text-xl md:text-2xl font-extrabold text-amber-600 mt-1 block">{metrics.open_tickets}</span>
          </div>
          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
            <span className="text-[11px] font-bold text-slate-400 block uppercase">In Progress</span>
            <span className="text-xl md:text-2xl font-extrabold text-[#5CA8FF] mt-1 block">{metrics.in_progress}</span>
          </div>
          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
            <span className="text-[11px] font-bold text-slate-400 block uppercase">Escalated</span>
            <span className="text-xl md:text-2xl font-extrabold text-rose-600 mt-1 block flex items-center gap-1">
              {metrics.escalated} <Flame className="w-4 h-4 text-rose-500 animate-pulse" />
            </span>
          </div>
          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200">
            <span className="text-[11px] font-bold text-slate-400 block uppercase">High Priority</span>
            <span className="text-xl md:text-2xl font-extrabold text-indigo-600 mt-1 block">{metrics.high_priority}</span>
          </div>
          <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200 col-span-2 sm:col-span-1">
            <span className="text-[11px] font-bold text-slate-400 block uppercase">Resolved</span>
            <span className="text-xl md:text-2xl font-extrabold text-emerald-600 mt-1 block">{metrics.resolved}</span>
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
            placeholder="Search ticket ID, customer name, subject..."
            className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 font-medium"
          />
        </div>

        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto justify-end">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          >
            <option value="">All Statuses</option>
            <option value="open">Open</option>
            <option value="in_progress">In Progress</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>

          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          >
            <option value="">All Priorities</option>
            <option value="urgent">Urgent</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <select
            value={escalatedFilter}
            onChange={(e) => setEscalatedFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
          >
            <option value="">All Escalations</option>
            <option value="escalated">Escalated Only</option>
            <option value="normal">Normal Only</option>
          </select>

          {/* List / Grid View Toggle */}
          <div className="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200">
            <button
              onClick={() => setViewMode('list')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'list' ? 'bg-white text-[#5CA8FF] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="List View (Primary)"
            >
              <List className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('grid')}
              className={`p-1.5 rounded-lg transition-colors ${viewMode === 'grid' ? 'bg-white text-[#5CA8FF] shadow-sm' : 'text-slate-500 hover:text-slate-800'}`}
              title="Grid View"
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Directory Render */}
      {filteredTickets.length === 0 ? (
        <div className="py-12 p-6 text-center bg-white rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <HelpCircle className="w-8 h-8 text-slate-400 mx-auto" />
          <h3 className="text-base font-bold text-slate-800">No support tickets found.</h3>
          <p className="text-xs text-slate-500 font-medium">Try changing your search terms or status filter settings.</p>
        </div>
      ) : viewMode === 'list' ? (
        <div className="bg-white rounded-3xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-600 font-bold uppercase text-[10px] border-b border-slate-200">
                <tr>
                  <th className="py-3.5 px-6">Ticket ID & Subject</th>
                  <th className="py-3.5 px-4">Customer</th>
                  <th className="py-3.5 px-4">Priority</th>
                  <th className="py-3.5 px-4">Status</th>
                  <th className="py-3.5 px-4">Escalation</th>
                  <th className="py-3.5 px-4">Created Time</th>
                  <th className="py-3.5 px-6 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredTickets.map((t) => (
                  <tr
                    key={t.id}
                    onClick={() => navigate(`/admin/support/${t.id}`)}
                    className="hover:bg-slate-50/80 transition-colors cursor-pointer"
                  >
                    <td className="py-4 px-6 max-w-xs">
                      <p className="font-mono font-bold text-slate-400 text-[11px]">#{t.id.substring(0, 8)}</p>
                      <h4 className="text-sm md:text-base font-bold text-slate-900 truncate mt-0.5">
                        {t.subject}
                      </h4>
                    </td>

                    <td className="py-4 px-4 font-bold text-slate-800">
                      {t.customer_name || 'Customer'}
                    </td>

                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] border ${getPriorityBadgeStyle(t.priority)}`}>
                        {t.priority}
                      </span>
                    </td>

                    <td className="py-4 px-4">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-bold border ${getStatusBadgeStyle(t.status)}`}>
                        {t.status.replace('_', ' ')}
                      </span>
                    </td>

                    <td className="py-4 px-4">
                      {t.escalated_to_admin ? (
                        <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-rose-50 text-rose-700 border border-rose-200">
                          <Flame className="w-3 h-3 text-rose-600 animate-pulse" />
                          <span>Escalated</span>
                        </span>
                      ) : (
                        <span className="text-slate-400 text-[11px] font-medium">Normal</span>
                      )}
                    </td>

                    <td className="py-4 px-4 font-medium text-slate-500">
                      {t.created_at ? new Date(t.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : 'N/A'}
                    </td>

                    <td className="py-4 px-6 text-right">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/admin/support/${t.id}`);
                        }}
                        className="px-3.5 py-1.5 bg-slate-100 hover:bg-[#5CA8FF] hover:text-white text-slate-700 font-bold rounded-xl transition-colors text-xs flex items-center gap-1 ml-auto"
                      >
                        <span>Open Thread</span>
                        <ChevronRight className="w-3.5 h-3.5" />
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
          {filteredTickets.map((t) => (
            <div
              key={t.id}
              onClick={() => navigate(`/admin/support/${t.id}`)}
              className="group bg-white p-6 rounded-3xl border border-slate-200 shadow-sm hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex flex-col justify-between space-y-4"
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <span className="text-[10px] font-mono font-bold text-slate-400">#{t.id.substring(0, 8)}</span>
                  <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold border ${getStatusBadgeStyle(t.status)}`}>
                    {t.status.replace('_', ' ')}
                  </span>
                </div>

                <h3 className="text-base font-bold text-slate-900 group-hover:text-[#5CA8FF] transition-colors line-clamp-2">
                  {t.subject}
                </h3>

                <p className="text-xs text-slate-500 font-medium line-clamp-2">
                  {t.description}
                </p>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className={`px-2.5 py-0.5 rounded-full text-[10px] border ${getPriorityBadgeStyle(t.priority)}`}>
                  {t.priority}
                </span>

                <span className="font-bold text-[#5CA8FF] group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                  <span>Open Thread</span>
                  <ChevronRight className="w-4 h-4" />
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
