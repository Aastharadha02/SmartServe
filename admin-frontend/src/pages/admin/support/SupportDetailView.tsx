import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { 
  HelpCircle, 
  Flame, 
  Loader2, 
  ArrowLeft, 
  CheckCircle2, 
  ChevronRight,
  User,
  Mail,
  Phone,
  Send,
  Lock,
  ExternalLink,
  Bot,
  AlertTriangle,
  X,
  FileText,
  Sparkles,
  Paperclip
} from 'lucide-react';
import { 
  getSupportTicketDetail, 
  replyToSupportTicket, 
  escalateSupportTicket, 
  updateTicketPriorityAndStatus, 
  getSignedEvidenceUrl 
} from '../../../api/support';
import type { SupportTicketItem } from '../../../api/support';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';

export const SupportDetailView: React.FC = () => {
  const { ticketId } = useParams<{ ticketId: string }>();
  const navigate = useNavigate();

  const [ticketData, setTicketData] = useState<SupportTicketItem | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  // Admin Reply State
  const [replyText, setReplyText] = useState<string>('');
  const [replyLoading, setReplyLoading] = useState<boolean>(false);

  // Status & Priority Modal State
  const [statusModalOpen, setStatusModalOpen] = useState<boolean>(false);
  const [selectedStatus, setSelectedStatus] = useState<string>('In_Progress');
  const [selectedPriority, setSelectedPriority] = useState<string>('High');
  const [updateLoading, setUpdateLoading] = useState<boolean>(false);

  // Escalation Modal State
  const [escalateModalOpen, setEscalateModalOpen] = useState<boolean>(false);
  const [escalateLoading, setEscalateLoading] = useState<boolean>(false);

  const canManageSupport = hasPermission(adminSession, 'support:manage');

  // 15-Minute HMAC Signed Evidence URL State
  const [signedEvidenceUrl, setSignedEvidenceUrl] = useState<string | null>(null);
  const [evidenceExpired, setEvidenceExpired] = useState<boolean>(false);
  const [evidenceLoading, setEvidenceLoading] = useState<boolean>(false);

  const [toastMessage, setToastMessage] = useState<{ text: string; type: 'success' | 'warning' | 'error' } | null>(null);

  const showToast = (text: string, type: 'success' | 'warning' | 'error' = 'success') => {
    setToastMessage({ text, type });
    setTimeout(() => setToastMessage(null), 5000);
  };

  const fetchTicketProfile = async () => {
    if (!ticketId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await getSupportTicketDetail(ticketId);
      setTicketData(data);
      setSelectedStatus(data.status);
      setSelectedPriority(data.priority);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load support ticket details from backend.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTicketProfile();
    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});
  }, [ticketId]);

  const handleReplySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticketData || !replyText.trim()) return;
    setReplyLoading(true);
    try {
      await replyToSupportTicket(ticketData.id, replyText);
      showToast('Admin reply sent successfully.', 'success');
      setReplyText('');
      fetchTicketProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to send admin reply.', 'error');
    } finally {
      setReplyLoading(false);
    }
  };

  const handleEscalateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticketData) return;
    setEscalateLoading(true);
    try {
      const res = await escalateSupportTicket(ticketData.id);
      showToast(res.message, 'success');
      setEscalateModalOpen(false);
      fetchTicketProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Escalation failed.', 'error');
    } finally {
      setEscalateLoading(false);
    }
  };

  const handleStatusPrioritySubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticketData) return;
    setUpdateLoading(true);
    try {
      const res = await updateTicketPriorityAndStatus(ticketData.id, {
        status: selectedStatus,
        priority: selectedPriority,
      });
      showToast(res.message, 'success');
      setStatusModalOpen(false);
      fetchTicketProfile();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Status/Priority update failed.', 'error');
    } finally {
      setUpdateLoading(false);
    }
  };

  const handleGenerateSignedEvidence = async () => {
    if (!ticketData) return;
    setEvidenceLoading(true);
    setEvidenceExpired(false);
    try {
      const res = await getSignedEvidenceUrl(ticketData.id);
      setSignedEvidenceUrl(res.signed_url);
      showToast('15-Minute HMAC signed evidence link generated.', 'success');

      // Auto expire timer test simulation (15 mins)
      setTimeout(() => {
        setEvidenceExpired(true);
      }, res.expires_in_seconds * 1000);
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to generate signed evidence link.', 'error');
    } finally {
      setEvidenceLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <Loader2 className="w-8 h-8 animate-spin text-[#5CA8FF]" />
        <p className="text-sm font-semibold text-slate-600">Loading Support Ticket Conversation Thread...</p>
      </div>
    );
  }

  if (error || !ticketData) {
    return (
      <div className="max-w-xl mx-auto my-12 p-8 bg-white border border-rose-200 rounded-3xl text-center space-y-4 shadow-sm">
        <AlertTriangle className="w-10 h-10 text-rose-500 mx-auto" />
        <h3 className="text-lg font-bold text-slate-900">Support Ticket Not Found</h3>
        <p className="text-xs text-slate-600">{error || 'Unable to retrieve requested ticket.'}</p>
        <button
          onClick={() => navigate('/admin/support')}
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#5CA8FF] text-white rounded-2xl text-xs font-bold"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Return to Support Directory</span>
        </button>
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

      {/* Breadcrumb Navigation */}
      <nav className="flex items-center gap-2 text-xs text-slate-500 font-medium">
        <Link to="/admin/support" className="hover:text-[#5CA8FF] flex items-center gap-1 transition-colors">
          <HelpCircle className="w-3.5 h-3.5" />
          <span>Operations</span>
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <Link to="/admin/support" className="hover:text-[#5CA8FF] transition-colors">
          Support
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-300" />
        <span className="text-slate-900 font-bold font-mono">#{ticketData.id.substring(0, 8)}</span>
      </nav>

      {/* Support Header Banner */}
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="flex items-start md:items-center gap-5">
          <button
            onClick={() => navigate('/admin/support')}
            className="p-2.5 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-600 transition-colors"
            title="Back to Directory"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>

          <div>
            <div className="flex items-center gap-3 flex-wrap">
              <span className="text-xs font-mono font-bold text-slate-400">#{ticketData.id.substring(0, 8)}</span>
              <h1 className="text-lg md:text-xl font-bold text-slate-900 tracking-tight">
                {ticketData.subject}
              </h1>
              <span className="px-3 py-1 bg-blue-50 text-[#5CA8FF] rounded-full text-xs font-bold border border-blue-200">
                {ticketData.status.replace('_', ' ')}
              </span>
              <span className="px-3 py-1 bg-slate-100 text-slate-700 rounded-full text-xs font-bold border border-slate-200">
                Priority: {ticketData.priority}
              </span>
              {ticketData.escalated_to_admin && (
                <span className="px-3 py-1 bg-rose-50 text-rose-700 rounded-full text-xs font-extrabold border border-rose-200 flex items-center gap-1 animate-pulse">
                  <Flame className="w-3.5 h-3.5 text-rose-600" />
                  <span>Escalated to Executive</span>
                </span>
              )}
            </div>

            <p className="text-xs text-slate-500 font-semibold mt-1">
              Customer: <strong className="text-slate-800">{ticketData.customer_name}</strong> | Opened:{' '}
              {ticketData.created_at ? new Date(ticketData.created_at).toLocaleString('en-IN') : 'N/A'}
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2.5 flex-wrap justify-end">
          {canManageSupport ? (
            <>
              <button
                onClick={() => setStatusModalOpen(true)}
                className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-2xl border border-slate-200 text-xs transition-colors"
              >
                Update Priority/Status
              </button>

              {!ticketData.escalated_to_admin && (
                <button
                  onClick={() => setEscalateModalOpen(true)}
                  className="px-4 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-2xl shadow-xs text-xs transition-colors flex items-center gap-1.5"
                >
                  <Flame className="w-4 h-4" />
                  <span>Escalate Ticket</span>
                </button>
              )}
            </>
          ) : (
            <button
              disabled
              title="Updating support ticket status or escalating requires 'support:manage' permission."
              className="px-4 py-2 bg-slate-100 text-slate-400 font-bold rounded-2xl border border-slate-200 text-xs cursor-not-allowed opacity-70"
            >
              🔒 Actions Restricted (View Only)
            </button>
          )}
        </div>
      </div>

      {/* Grid Layout: Main Conversation Thread (Left/Center) + Customer Context (Right) */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Conversation Thread & Admin Reply Box (Main Visual Focus) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Conversation Thread Container */}
          <div className="bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6 flex flex-col justify-between min-h-[500px]">
            <div>
              <div className="border-b border-slate-100 pb-4 mb-6 flex items-center justify-between">
                <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
                  <FileText className="w-5 h-5 text-[#5CA8FF]" />
                  <span>Conversation History Thread</span>
                </h3>
                <span className="text-xs font-semibold text-slate-400">
                  {ticketData.messages.length} Messages Logged
                </span>
              </div>

              {/* Description / Initial Post */}
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-2 mb-6">
                <span className="text-xs font-bold text-slate-700 block">Initial Issue Description</span>
                <p className="text-sm text-slate-800 font-medium leading-relaxed">{ticketData.description}</p>
              </div>

              {/* Message Thread List */}
              {ticketData.messages.length === 0 ? (
                <p className="text-xs text-slate-400 italic text-center py-6">No thread messages yet.</p>
              ) : (
                <div className="space-y-4 max-h-[350px] overflow-y-auto pr-2">
                  {ticketData.messages.map((msg, idx) => {
                    const isBot = msg.sender_role === 'AI_AGENT' || msg.sender_role === 'bot';
                    const isAdmin = msg.sender_role === 'admin' || msg.sender_role === 'SUPER_ADMIN';

                    return (
                      <div
                        key={msg.id || idx}
                        className={`flex flex-col ${isAdmin ? 'items-end' : 'items-start'}`}
                      >
                        <div
                          className={`max-w-md p-4 rounded-3xl text-xs space-y-1 ${
                            isAdmin
                              ? 'bg-[#5CA8FF] text-white rounded-br-none'
                              : isBot
                              ? 'bg-purple-50 text-purple-900 border border-purple-200 rounded-bl-none'
                              : 'bg-slate-100 text-slate-800 rounded-bl-none'
                          }`}
                        >
                          <div className="flex items-center justify-between gap-4 font-bold text-[11px]">
                            <span>{isAdmin ? 'SmartServe Support Admin' : 'Customer'}</span>
                            <span className="opacity-75">{msg.sender_role}</span>
                          </div>
                          <p className="text-xs font-medium leading-relaxed mt-1">{msg.message_text}</p>
                        </div>
                        <span className="text-[10px] text-slate-400 font-semibold mt-1 px-1">
                          {msg.created_at ? new Date(msg.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' }) : ''}
                        </span>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            {/* Admin Reply Box */}
            <form onSubmit={handleReplySubmit} className="pt-4 border-t border-slate-100 space-y-3">
              <label className="block text-xs font-bold text-slate-700">
                Admin Response {!canManageSupport && '(Read Only Mode)'}
              </label>
              <div className="relative">
                <textarea
                  value={replyText}
                  onChange={(e) => setReplyText(e.target.value)}
                  disabled={!canManageSupport}
                  placeholder={canManageSupport ? "Type official support reply to customer..." : "Replying to support tickets requires 'support:manage' permission."}
                  className="w-full bg-slate-50 border border-slate-200 rounded-2xl p-4 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 font-medium disabled:opacity-75 disabled:cursor-not-allowed"
                  rows={3}
                  required
                />
                <button
                  type="submit"
                  disabled={!canManageSupport || replyLoading || !replyText.trim()}
                  className="absolute right-3 bottom-3.5 p-2.5 bg-[#5CA8FF] hover:bg-blue-600 disabled:bg-slate-300 text-white rounded-xl shadow-xs transition-colors disabled:cursor-not-allowed"
                  title={canManageSupport ? "Send Reply" : "Replying requires 'support:manage' permission"}
                >
                  {replyLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* Right Column: Customer Context & AI Signals */}
        <div className="space-y-6">
          {/* Customer Context Panel */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <User className="w-5 h-5 text-[#5CA8FF]" />
              <span>Customer Context Panel</span>
            </h3>

            <div className="space-y-3 text-xs">
              <div>
                <span className="text-slate-400 font-semibold block">Customer Name</span>
                <p className="font-bold text-slate-900 text-sm mt-0.5">{ticketData.customer_name || 'Customer'}</p>
              </div>

              <div>
                <span className="text-slate-400 font-semibold block">Contact Details</span>
                <p className="font-semibold text-slate-800 mt-0.5 flex items-center gap-1.5">
                  <Mail className="w-3.5 h-3.5 text-slate-400" />
                  <span>{ticketData.customer_email}</span>
                </p>
                <p className="font-semibold text-slate-800 mt-1 flex items-center gap-1.5">
                  <Phone className="w-3.5 h-3.5 text-slate-400" />
                  <span>{ticketData.customer_phone}</span>
                </p>
              </div>

              {ticketData.booking_id && (
                <div className="pt-2 border-t border-slate-100">
                  <span className="text-slate-400 font-semibold block">Linked Booking</span>
                  <Link
                    to={`/admin/bookings/${ticketData.booking_id}`}
                    className="font-mono font-bold text-[#5CA8FF] hover:underline flex items-center gap-1 mt-0.5 text-xs"
                  >
                    <span>#{ticketData.booking_id.substring(0, 8)}...</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </Link>
                </div>
              )}

              {ticketData.customer_context && (
                <div className="pt-2 border-t border-slate-100 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 font-semibold">Previous Tickets</span>
                    <span className="font-bold text-slate-800">{ticketData.customer_context.previous_tickets_count || 1} tickets</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400 font-semibold">Account Risk Flag</span>
                    <span className="font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded-lg border border-rose-200 text-[10px]">
                      {ticketData.customer_context.risk_flag || 'Clean Record'}
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* AI-Assisted Analysis Panel (Only when available from backend!) */}
          {ticketData.ai_analysis && (
            <div className="bg-white p-6 rounded-3xl border border-blue-200 shadow-sm space-y-4 bg-gradient-to-b from-blue-50/50 to-white">
              <h3 className="text-base font-bold text-slate-900 border-b border-blue-100 pb-3 flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Bot className="w-5 h-5 text-[#5CA8FF]" />
                  <span>AI-assisted analysis</span>
                </span>
                <Sparkles className="w-4 h-4 text-amber-500" />
              </h3>

              <div className="space-y-3 text-xs">
                {ticketData.ai_analysis.complaint_category && (
                  <div>
                    <span className="text-slate-400 font-semibold block">Predicted Complaint Category</span>
                    <p className="font-bold text-slate-800 mt-0.5">{ticketData.ai_analysis.complaint_category}</p>
                  </div>
                )}

                {ticketData.ai_analysis.sentiment_score !== undefined && (
                  <div>
                    <span className="text-slate-400 font-semibold block">Customer Frustration / Sentiment Score</span>
                    <div className="flex items-center gap-2 mt-1">
                      <div className="flex-1 h-2 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-rose-500 rounded-full"
                          style={{ width: `${Math.round((ticketData.ai_analysis.sentiment_score || 0) * 100)}%` }}
                        />
                      </div>
                      <span className="font-mono font-bold text-slate-800 text-xs">
                        {Math.round((ticketData.ai_analysis.sentiment_score || 0) * 100)}% High Priority
                      </span>
                    </div>
                  </div>
                )}

                {ticketData.ai_analysis.ocr_extracted_text && (
                  <div className="pt-2 border-t border-blue-100">
                    <span className="text-slate-400 font-semibold block">OCR Extracted Text from Evidence</span>
                    <p className="font-mono text-slate-700 bg-white p-2.5 rounded-xl border border-slate-200 mt-1 text-[11px] leading-relaxed">
                      "{ticketData.ai_analysis.ocr_extracted_text}"
                    </p>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Image Evidence & 15-Min HMAC Signed URL Panel */}
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-slate-900 border-b border-slate-100 pb-3 flex items-center gap-2">
              <Paperclip className="w-5 h-5 text-indigo-500" />
              <span>Evidence & File Attachments</span>
            </h3>

            {!ticketData.image_evidence_url ? (
              <div className="p-4 bg-slate-50 rounded-2xl text-center text-xs font-semibold text-slate-500">
                No evidence attached.
              </div>
            ) : (
              <div className="space-y-3 text-xs">
                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Paperclip className="w-4 h-4 text-slate-400" />
                    <span className="font-bold text-slate-800 truncate">Evidence Document / Photo</span>
                  </div>

                  <button
                    onClick={handleGenerateSignedEvidence}
                    disabled={evidenceLoading}
                    className="px-3 py-1.5 bg-[#5CA8FF] hover:bg-blue-600 text-white font-bold rounded-xl text-xs flex items-center gap-1 shadow-xs"
                  >
                    {evidenceLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : 'View Evidence'}
                  </button>
                </div>

                {signedEvidenceUrl && !evidenceExpired && (
                  <div className="p-3.5 bg-emerald-50 text-emerald-800 rounded-2xl border border-emerald-200 space-y-2 text-xs">
                    <div className="flex items-center justify-between font-bold">
                      <span className="flex items-center gap-1"><Lock className="w-3.5 h-3.5 text-emerald-600" /> 15-Min HMAC Signed Link Active</span>
                      <span className="text-[10px] bg-emerald-100 px-2 py-0.5 rounded-full">Expires in 15m</span>
                    </div>
                    <a
                      href={signedEvidenceUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-mono text-emerald-700 hover:underline block truncate text-[11px]"
                    >
                      {signedEvidenceUrl}
                    </a>
                  </div>
                )}

                {evidenceExpired && (
                  <div className="p-3 bg-rose-50 text-rose-700 rounded-2xl border border-rose-200 text-xs font-semibold">
                    Evidence link expired. Generate a new link.
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Escalation Modal */}
      {escalateModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleEscalateSubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-slate-200 p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Flame className="w-5 h-5 text-rose-600 animate-pulse" />
                <span>Escalate Ticket to Executive Queue</span>
              </h3>
              <button type="button" onClick={() => setEscalateModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-medium">
              Are you sure you want to escalate support ticket <strong>#{ticketData.id.substring(0, 8)}</strong>? Priority will be updated to Urgent and logged in audit history.
            </p>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setEscalateModalOpen(false)}
                className="px-4 py-2 bg-slate-100 text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={escalateLoading}
                className="px-5 py-2 bg-rose-600 hover:bg-rose-700 text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {escalateLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm Escalation'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Priority & Status Modal */}
      {statusModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleStatusPrioritySubmit} className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-slate-200 p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-base font-bold text-slate-900">Update Ticket Priority & Status</h3>
              <button type="button" onClick={() => setStatusModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Ticket Status *</label>
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
              >
                <option value="Open">Open</option>
                <option value="In_Progress">In Progress</option>
                <option value="Resolved">Resolved</option>
                <option value="Closed">Closed</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Ticket Priority *</label>
              <select
                value={selectedPriority}
                onChange={(e) => setSelectedPriority(e.target.value)}
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40"
              >
                <option value="Low">Low</option>
                <option value="Medium">Medium</option>
                <option value="High">High</option>
                <option value="Urgent">Urgent</option>
              </select>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setStatusModalOpen(false)}
                className="px-4 py-2 bg-slate-100 text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={updateLoading}
                className="px-5 py-2 bg-[#5CA8FF] hover:bg-blue-600 text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {updateLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
};
