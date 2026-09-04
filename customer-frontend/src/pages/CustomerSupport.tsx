import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCustomerTickets, createSupportTicket, SupportTicketDetail } from '../api/support';
import { formatDateINR } from '../utils/formatters';
import { useToast } from '../hooks/useToast';
import { HelpCircle, Plus, Clock, ChevronRight, Loader2, AlertCircle, RefreshCw, Send } from 'lucide-react';

export const CustomerSupport: React.FC = () => {
  const navigate = useNavigate();
  const { showToast } = useToast();

  const [tickets, setTickets] = useState<SupportTicketDetail[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // New Ticket Modal
  const [showModal, setShowModal] = useState<boolean>(false);
  const [subject, setSubject] = useState<string>('');
  const [category, setCategory] = useState<string>('Booking Assistance');
  const [priority, setPriority] = useState<string>('Normal');
  const [description, setDescription] = useState<string>('');
  const [submitting, setSubmitting] = useState<boolean>(false);

  const fetchTickets = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getCustomerTickets();
      setTickets(data);
    } catch (err: any) {
      if (err.response) {
        setError(err.response.data?.detail || `API Error (${err.response.status}): Failed to load support tickets.`);
      } else if (err.request) {
        setError('Unable to connect to SmartServe API. Please verify network connectivity and backend server availability.');
      } else {
        setError('An unexpected error occurred while loading your support tickets.');
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!subject.trim() || !description.trim()) {
      showToast('Please fill in both subject and description.', 'error');
      return;
    }

    setSubmitting(true);
    try {
      const newTicket = await createSupportTicket({
        subject,
        category,
        priority,
        description,
      });

      showToast('Support ticket submitted successfully!', 'success');
      setShowModal(false);
      setSubject('');
      setDescription('');
      fetchTickets();
      navigate(`/support/${newTicket.id}`);
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to submit support ticket.', 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-8 font-sans max-w-5xl mx-auto">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">Customer Support Center</h1>
          <p className="text-sm text-slate-500 font-medium mt-1">
            Submit inquiry tickets and chat with SmartServe operations support.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchTickets}
            className="flex items-center gap-2 px-4 py-2.5 bg-white hover:bg-slate-50 text-slate-700 font-semibold text-xs rounded-xl border border-slate-200 shadow-2xs transition-colors"
          >
            <RefreshCw className="w-3.5 h-3.5 text-slate-400" />
            <span>Sync Live</span>
          </button>
          
          <button
            onClick={() => setShowModal(true)}
            className="flex items-center gap-2 px-5 py-2.5 bg-[#2563EB] hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>+ Open New Ticket</span>
          </button>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="p-8 bg-white border border-red-200 rounded-3xl text-center space-y-3 shadow-sm">
          <AlertCircle className="w-10 h-10 text-rose-500 mx-auto" />
          <h3 className="text-base font-bold text-slate-900">Support Center Connection Error</h3>
          <p className="text-xs text-slate-600 max-w-md mx-auto">{error}</p>
          <button
            onClick={fetchTickets}
            className="px-4 py-2 bg-[#2563EB] text-white text-xs font-bold rounded-xl inline-flex items-center gap-2"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Retry Connection</span>
          </button>
        </div>
      )}

      {/* Ticket List */}
      {loading ? (
        <div className="flex flex-col items-center justify-center py-16 space-y-3">
          <Loader2 className="w-10 h-10 animate-spin text-[#2563EB]" />
          <p className="text-sm font-semibold text-slate-600">Loading support tickets from database...</p>
        </div>
      ) : tickets.length > 0 ? (
        <div className="space-y-4">
          {tickets.map((t) => {
            const stLower = t.status.toLowerCase();
            return (
              <div
                key={t.id}
                onClick={() => navigate(`/support/${t.id}`)}
                className="group bg-white p-6 rounded-3xl border border-slate-200/90 shadow-2xs hover:shadow-md hover:border-blue-200 transition-all cursor-pointer flex items-center justify-between gap-4"
              >
                <div className="space-y-2 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase border ${
                      stLower === 'open'
                        ? 'bg-blue-50 text-[#2563EB] border-blue-200'
                        : stLower === 'resolved' || stLower === 'closed'
                        ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                        : 'bg-amber-50 text-amber-700 border-amber-200'
                    }`}>
                      {t.status}
                    </span>
                    <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{t.category}</span>
                  </div>

                  <h3 className="font-extrabold text-slate-900 text-base truncate group-hover:text-[#2563EB] transition-colors">
                    {t.subject}
                  </h3>

                  <div className="flex items-center gap-3 text-xs text-slate-400 font-medium">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-400" />
                      <span>Opened {formatDateINR(t.created_at)}</span>
                    </span>
                    <span>• {t.messages ? t.messages.length : 1} Messages</span>
                  </div>
                </div>

                <ChevronRight className="w-5 h-5 text-slate-400 group-hover:translate-x-1 transition-transform flex-shrink-0" />
              </div>
            );
          })}
        </div>
      ) : (
        <div className="bg-white p-12 rounded-3xl border border-slate-200 text-center space-y-4">
          <HelpCircle className="w-12 h-12 text-slate-400 mx-auto" />
          <div className="space-y-1">
            <h3 className="text-base font-bold text-slate-800">No Support Tickets Opened</h3>
            <p className="text-xs text-slate-500">Need help with a service or billing? Open a ticket to connect with support.</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="px-5 py-2.5 bg-[#2563EB] text-white font-bold text-xs rounded-xl inline-flex items-center gap-2 shadow-xs"
          >
            <Plus className="w-4 h-4" />
            <span>Open New Support Ticket</span>
          </button>
        </div>
      )}

      {/* CREATE TICKET MODAL */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 space-y-6 shadow-2xl border border-slate-200 animate-in zoom-in-95">
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <h3 className="text-xl font-extrabold text-slate-900">Open Customer Support Ticket</h3>
              <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 font-bold text-sm">✕</button>
            </div>

            <form onSubmit={handleCreateTicket} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Subject</label>
                <input
                  type="text"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="e.g. Need assistance with AC Service booking"
                  className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Category</label>
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                  >
                    <option value="Booking Assistance">Booking Assistance</option>
                    <option value="Payment & Refund">Payment & Refund</option>
                    <option value="Technician Feedback">Technician Feedback</option>
                    <option value="General Query">General Query</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Priority</label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                    className="w-full h-12 bg-slate-50 border border-slate-200 rounded-xl px-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                  >
                    <option value="Normal">Normal</option>
                    <option value="High">High</option>
                    <option value="Urgent">Urgent</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-1.5">Issue Description</label>
                <textarea
                  rows={4}
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Describe your issue in detail..."
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm font-medium text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
                  required
                />
              </div>

              <div className="pt-2 flex gap-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="w-1/2 py-3.5 bg-slate-100 hover:bg-slate-200 font-bold text-slate-700 rounded-xl text-sm transition-all"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="w-1/2 py-3.5 bg-[#2563EB] hover:bg-blue-700 text-white font-bold rounded-xl text-sm shadow-sm transition-all disabled:opacity-70 flex items-center justify-center gap-2"
                >
                  {submitting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  <span>Submit Ticket</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};

export default CustomerSupport;
