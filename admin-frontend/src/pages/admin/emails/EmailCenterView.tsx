import React, { useEffect, useState, useMemo } from 'react';
import { 
  Mail, 
  Search, 
  Plus, 
  FileText, 
  Send, 
  History, 
  Eye, 
  Edit3, 
  CheckCircle2, 
  AlertTriangle, 
  Loader2, 
  X
} from 'lucide-react';
import { 
  getEmailTemplates, 
  upsertEmailTemplate, 
  dispatchEmail, 
  getEmailLogs 
} from '../../../api/emails';
import type { EmailTemplateItem, EmailLogItem } from '../../../api/emails';
import { getAuthenticatedAdmin } from '../../../api/admins';
import type { SessionAdminInfo } from '../../../api/admins';
import { hasPermission } from '../../../utils/rbac';

export const EmailCenterView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'templates' | 'compose' | 'history'>('templates');

  // Templates Data
  const [templates, setTemplates] = useState<EmailTemplateItem[]>([]);
  const [templatesLoading, setTemplatesLoading] = useState<boolean>(true);
  const [adminSession, setAdminSession] = useState<SessionAdminInfo | null>(null);

  const canManageEmails = hasPermission(adminSession, 'emails:manage');

  // History Logs Data
  const [logs, setLogs] = useState<EmailLogItem[]>([]);
  const [logsLoading, setLogsLoading] = useState<boolean>(true);

  // Search & Filter state for History
  const [historySearch, setHistorySearch] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');

  // Modals & Active Edit/Preview Item
  const [editorModalOpen, setEditorModalOpen] = useState<boolean>(false);
  const [previewModalOpen, setPreviewModalOpen] = useState<boolean>(false);
  const [confirmSendModalOpen, setConfirmSendModalOpen] = useState<boolean>(false);

  const [currentTemplate, setCurrentTemplate] = useState<Partial<EmailTemplateItem>>({
    template_key: '',
    subject: '',
    body_html: '',
    is_active: true,
  });

  // Compose State
  const [composeRecipient, setComposeRecipient] = useState<string>('ananya.rao@example.com');
  const [composeTemplateKey, setComposeTemplateKey] = useState<string>('');
  const [composeSubject, setComposeSubject] = useState<string>('SmartServe Booking Confirmation — #5716e23b');
  const [composeBody, setComposeBody] = useState<string>(
    'Dear Ananya Rao,\n\nYour booking for Hair Straightening / Smoothening (#5716e23b) has been confirmed for 27 Aug 2026 at 10:00 AM.\nTotal Amount: ₹2,639.\nStart OTP: 5829.\n\nThank you for choosing SmartServe!'
  );
  const [dispatchLoading, setDispatchLoading] = useState<boolean>(false);
  const [saveTemplateLoading, setSaveTemplateLoading] = useState<boolean>(false);

  // Toast message
  const [toast, setToast] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  const showToast = (text: string, type: 'success' | 'error' = 'success') => {
    setToast({ text, type });
    setTimeout(() => setToast(null), 4000);
  };

  const fetchTemplates = async () => {
    setTemplatesLoading(true);
    try {
      const data = await getEmailTemplates();
      setTemplates(data);
    } catch (err: any) {
      console.error('Failed to load email templates.', err);
    } finally {
      setTemplatesLoading(false);
    }
  };

  const fetchLogs = async () => {
    setLogsLoading(true);
    try {
      const data = await getEmailLogs();
      setLogs(data);
    } catch (err: any) {
      console.error('Failed to load email logs history.', err);
    } finally {
      setLogsLoading(false);
    }
  };

  useEffect(() => {
    fetchTemplates();
    fetchLogs();
    getAuthenticatedAdmin().then((s) => setAdminSession(s)).catch(() => {});
  }, []);

  // Filtered History Logs
  const filteredLogs = useMemo(() => {
    return logs.filter((l) => {
      const matchesSearch =
        l.recipient_email.toLowerCase().includes(historySearch.toLowerCase()) ||
        l.subject.toLowerCase().includes(historySearch.toLowerCase()) ||
        (l.template_key && l.template_key.toLowerCase().includes(historySearch.toLowerCase()));

      const matchesStatus = !statusFilter || l.status.toLowerCase() === statusFilter.toLowerCase();

      return matchesSearch && matchesStatus;
    });
  }, [logs, historySearch, statusFilter]);

  // Template select in Compose
  const handleComposeTemplateSelect = (key: string) => {
    setComposeTemplateKey(key);
    if (!key) return;
    const found = templates.find((t) => t.template_key === key);
    if (found) {
      setComposeSubject(found.subject.replace('{{booking_id}}', '5716e23b'));
      let textBody = found.body_html.replace(/<[^>]*>?/gm, '');
      textBody = textBody
        .replace('{{customer_name}}', 'Ananya Rao')
        .replace('{{service_name}}', 'Hair Straightening / Smoothening')
        .replace('{{booking_id}}', '5716e23b')
        .replace('{{scheduled_time}}', '27 Aug 2026 at 10:00 AM')
        .replace('{{amount}}', '2,639')
        .replace('{{otp_code}}', '5829')
        .replace('{{provider_name}}', 'Priya Patel');
      setComposeBody(textBody);
    }
  };

  // Upsert Template Submit
  const handleTemplateSave = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!currentTemplate.template_key || !currentTemplate.subject || !currentTemplate.body_html) return;
    setSaveTemplateLoading(true);
    try {
      await upsertEmailTemplate({
        template_key: currentTemplate.template_key,
        subject: currentTemplate.subject,
        body_html: currentTemplate.body_html,
        is_active: currentTemplate.is_active ?? true,
      });
      showToast('Email template saved successfully.', 'success');
      setEditorModalOpen(false);
      fetchTemplates();
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to save email template.', 'error');
    } finally {
      setSaveTemplateLoading(false);
    }
  };

  // Dispatch Email Submit
  const handleDispatchConfirm = async () => {
    setDispatchLoading(true);
    try {
      const res = await dispatchEmail({
        recipient_email: composeRecipient,
        subject: composeSubject,
        body_text: composeBody,
        template_key: composeTemplateKey || undefined,
      });
      showToast(`Email dispatched to ${res.recipient_email}!`, 'success');
      setConfirmSendModalOpen(false);
      fetchLogs();
      setActiveTab('history');
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to dispatch email.', 'error');
    } finally {
      setDispatchLoading(false);
    }
  };

  // Variable Interpolation Helper for Live Preview
  const renderLivePreviewHTML = (tmpl: Partial<EmailTemplateItem>) => {
    if (!tmpl.body_html) return '<p>No content preview available.</p>';
    return tmpl.body_html
      .replace(/{{customer_name}}/g, 'Ananya Rao')
      .replace(/{{booking_id}}/g, '5716e23b')
      .replace(/{{service_name}}/g, 'Hair Straightening / Smoothening')
      .replace(/{{provider_name}}/g, 'Priya Patel')
      .replace(/{{scheduled_time}}/g, '27 Aug 2026 at 10:00 AM')
      .replace(/{{amount}}/g, '2,639')
      .replace(/{{otp_code}}/g, '5829')
      .replace(/{{address}}/g, 'Plot #42, Jubilee Hills, Hyderabad');
  };

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
      <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-bold font-serif text-[#1F2A1E] tracking-tight">Email Center</h1>
            <span className="text-xs font-bold text-[#2F5233] bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              {templates.length} Templates Configured
            </span>
          </div>
          <p className="text-sm md:text-base text-slate-500 font-semibold mt-1">
            System notification templates, manual email dispatch, preview engine, and delivery history logs
          </p>
        </div>

        {/* Module Navigation Tabs */}
        <div className="flex items-center gap-2 border-b border-[#E5DEC9]/60 pt-2">
          <button
            onClick={() => setActiveTab('templates')}
            className={`px-5 py-3 font-bold text-xs md:text-sm transition-all border-b-2 flex items-center gap-2 ${
              activeTab === 'templates'
                ? 'border-[#2F5233] text-[#2F5233]'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <FileText className="w-4 h-4" />
            <span>Templates ({templates.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('compose')}
            className={`px-5 py-3 font-bold text-xs md:text-sm transition-all border-b-2 flex items-center gap-2 ${
              activeTab === 'compose'
                ? 'border-[#2F5233] text-[#2F5233]'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <Send className="w-4 h-4" />
            <span>Compose Email</span>
          </button>

          <button
            onClick={() => setActiveTab('history')}
            className={`px-5 py-3 font-bold text-xs md:text-sm transition-all border-b-2 flex items-center gap-2 ${
              activeTab === 'history'
                ? 'border-[#2F5233] text-[#2F5233]'
                : 'border-transparent text-slate-500 hover:text-slate-800'
            }`}
          >
            <History className="w-4 h-4" />
            <span>Email History ({logs.length})</span>
          </button>
        </div>
      </div>

      {/* TAB 1: TEMPLATES DIRECTORY */}
      {activeTab === 'templates' && (
        <div className="space-y-6">
          <div className="flex items-center justify-between bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
            <h3 className="text-sm font-bold text-slate-800">System Notification Templates</h3>

            {canManageEmails ? (
              <button
                onClick={() => {
                  setCurrentTemplate({ template_key: '', subject: '', body_html: '<p>Hi {{customer_name}},</p>\n\n<p>Your service update: {{service_name}}.</p>', is_active: true });
                  setEditorModalOpen(true);
                }}
                className="px-4 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-xs flex items-center gap-1.5 shadow-xs transition-colors"
              >
                <Plus className="w-4 h-4" />
                <span>Add Template</span>
              </button>
            ) : (
              <button
                disabled
                title="Template creation requires 'emails:manage' permission."
                className="px-4 py-2 bg-slate-200 text-slate-500 font-bold rounded-xl text-xs flex items-center gap-1.5 cursor-not-allowed opacity-70 border border-slate-300"
              >
                <Plus className="w-4 h-4 text-slate-400" />
                <span>Add Template (Disabled)</span>
              </button>
            )}
          </div>

          {templatesLoading ? (
            <div className="flex flex-col items-center justify-center py-12 space-y-3">
              <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
              <p className="text-sm font-semibold text-slate-600">Loading System Email Templates...</p>
            </div>
          ) : templates.length === 0 ? (
            <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
              <Mail className="w-8 h-8 text-slate-400 mx-auto" />
              <h3 className="text-base font-bold text-slate-800">No email templates configured.</h3>
              <p className="text-xs text-slate-500 font-medium">Click "+ New Template" above to create system notification templates.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {templates.map((tmpl) => (
                <div
                  key={tmpl.id}
                  className="bg-white p-6 rounded-3xl border border-[#E5DEC9] shadow-sm space-y-4 hover:border-blue-200 transition-all flex flex-col justify-between"
                >
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-xs font-bold text-[#2F5233] bg-[#F2EDE1] px-3 py-1 rounded-full border border-[#E5DEC9]">
                        {tmpl.template_key}
                      </span>
                      <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                        Active System Template
                      </span>
                    </div>

                    <h3 className="text-base font-bold font-serif text-[#1F2A1E] line-clamp-1">{tmpl.subject}</h3>

                    {/* Supported Variables Badges */}
                    <div>
                      <span className="text-[11px] font-bold text-slate-400 block mb-1 uppercase">Supported Variables</span>
                      <div className="flex flex-wrap gap-1">
                        {tmpl.supported_variables.map((v) => (
                          <span key={v} className="font-mono text-[10px] font-semibold text-slate-600 bg-[#F2EDE1] px-2 py-0.5 rounded-lg border border-[#E5DEC9]">
                            &#123;&#123;{v}&#125;&#125;
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="pt-4 border-t border-[#E5DEC9]/60 flex items-center justify-between gap-3 text-xs">
                    <span className="text-slate-400 font-semibold">
                      Updated: {tmpl.updated_at ? new Date(tmpl.updated_at).toLocaleDateString('en-IN') : 'N/A'}
                    </span>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => {
                          setCurrentTemplate(tmpl);
                          setPreviewModalOpen(true);
                        }}
                        className="px-3 py-1.5 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-slate-700 font-bold rounded-xl transition-colors flex items-center gap-1"
                      >
                        <Eye className="w-3.5 h-3.5 text-slate-500" />
                        <span>Preview</span>
                      </button>

                      <button
                        onClick={() => {
                          setCurrentTemplate(tmpl);
                          setEditorModalOpen(true);
                        }}
                        className="px-3 py-1.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl transition-colors flex items-center gap-1 shadow-xs"
                      >
                        <Edit3 className="w-3.5 h-3.5" />
                        <span>Edit</span>
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* TAB 2: COMPOSE EMAIL */}
      {activeTab === 'compose' && (
        <div className="bg-white p-6 md:p-8 rounded-3xl border border-[#E5DEC9] shadow-sm max-w-3xl mx-auto space-y-6">
          <div className="border-b border-[#E5DEC9]/60 pb-4">
            <h3 className="text-lg font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
              <Send className="w-5 h-5 text-[#2F5233]" />
              <span>Compose & Dispatch Manual Notification Email</span>
            </h3>
            <p className="text-xs text-slate-500 font-semibold mt-1">
              Select recipient, optionally apply template layout, preview variables, and confirm dispatch
            </p>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Recipient Email Address *</label>
              <input
                type="email"
                value={composeRecipient}
                onChange={(e) => setComposeRecipient(e.target.value)}
                placeholder="customer@example.com"
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] font-medium"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Apply Email Template (Optional)</label>
              <select
                value={composeTemplateKey}
                onChange={(e) => handleComposeTemplateSelect(e.target.value)}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-xs font-semibold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
              >
                <option value="">Custom Manual Email (No Template)</option>
                {templates.map((t) => (
                  <option key={t.template_key} value={t.template_key}>
                    {t.template_key} — {t.subject}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Email Subject Line *</label>
              <input
                type="text"
                value={composeSubject}
                onChange={(e) => setComposeSubject(e.target.value)}
                placeholder="Enter email subject..."
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] font-bold text-slate-900"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Email Body Text *</label>
              <textarea
                value={composeBody}
                onChange={(e) => setComposeBody(e.target.value)}
                rows={6}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] font-medium"
                required
              />
            </div>

            <div className="pt-4 border-t border-[#E5DEC9]/60 flex items-center justify-between">
              <button
                type="button"
                onClick={() => {
                  setCurrentTemplate({ subject: composeSubject, body_html: `<p>${composeBody.replace(/\n/g, '<br/>')}</p>` });
                  setPreviewModalOpen(true);
                }}
                className="px-4 py-2.5 bg-[#F2EDE1] hover:bg-[#E5DEC9] text-slate-700 font-bold rounded-2xl text-xs flex items-center gap-1.5 transition-colors"
              >
                <Eye className="w-4 h-4 text-slate-500" />
                <span>Preview Recipient View</span>
              </button>

              <button
                type="button"
                onClick={() => setConfirmSendModalOpen(true)}
                className="px-6 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-2xl text-xs flex items-center gap-2 shadow-sm transition-colors"
              >
                <Send className="w-4 h-4" />
                <span>Send Email...</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* TAB 3: EMAIL HISTORY LOGS */}
      {activeTab === 'history' && (
        <div className="space-y-6">
          {/* Search & Filters */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-3 bg-white p-4 rounded-2xl border border-[#E5DEC9] shadow-sm">
            <div className="relative flex-1 w-full max-w-md">
              <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="text"
                value={historySearch}
                onChange={(e) => setHistorySearch(e.target.value)}
                placeholder="Search recipient email, subject, template key..."
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl pl-10 pr-4 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] font-medium"
              />
            </div>

            <div className="flex items-center gap-3">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl px-3 py-2 text-xs font-semibold text-slate-700 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
              >
                <option value="">All Delivery Statuses</option>
                <option value="sent">Sent</option>
                <option value="failed">Failed</option>
              </select>
            </div>
          </div>

          {/* History Log Table */}
          {logsLoading ? (
            <div className="flex flex-col items-center justify-center py-12 space-y-3">
              <Loader2 className="w-8 h-8 animate-spin text-[#2F5233]" />
              <p className="text-sm font-semibold text-slate-600">Loading Outbound Email History Logs...</p>
            </div>
          ) : filteredLogs.length === 0 ? (
            <div className="py-12 p-6 text-center bg-white rounded-2xl border border-[#E5DEC9] shadow-sm space-y-2">
              <History className="w-8 h-8 text-slate-400 mx-auto" />
              <h3 className="text-base font-bold text-slate-800">No email activity recorded.</h3>
              <p className="text-xs text-slate-500 font-medium">Outbound email dispatch logs will appear here.</p>
            </div>
          ) : (
            <div className="bg-white rounded-3xl border border-[#E5DEC9] shadow-sm overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs">
                  <thead className="bg-[#FAF7F0] text-slate-600 font-bold uppercase text-[10px] border-b border-[#E5DEC9]">
                    <tr>
                      <th className="py-3.5 px-6">Recipient Email</th>
                      <th className="py-3.5 px-4">Subject Line</th>
                      <th className="py-3.5 px-4">Template Key</th>
                      <th className="py-3.5 px-4">Delivery Status</th>
                      <th className="py-3.5 px-6 text-right">Sent Time</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {filteredLogs.map((log) => (
                      <tr key={log.id} className="hover:bg-[#FAF7F0] transition-colors">
                        <td className="py-4 px-6 font-bold text-slate-900">{log.recipient_email}</td>
                        <td className="py-4 px-4 font-semibold text-slate-800">{log.subject}</td>
                        <td className="py-4 px-4 font-mono text-[11px] text-[#2F5233]">
                          {log.template_key || 'Manual Email'}
                        </td>
                        <td className="py-4 px-4">
                          {log.status === 'Sent' ? (
                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
                              <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                              <span>Sent</span>
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">
                              <AlertTriangle className="w-3 h-3 text-rose-600" />
                              <span>Failed — {log.error_message || 'SMTP 550 Recipient unroutable'}</span>
                            </span>
                          )}
                        </td>
                        <td className="py-4 px-6 text-right font-medium text-slate-500">
                          {log.sent_at ? new Date(log.sent_at).toLocaleString('en-IN') : 'N/A'}
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

      {/* Editor Modal */}
      {editorModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleTemplateSave} className="bg-white w-full max-w-2xl rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">
                {currentTemplate.id ? 'Edit System Email Template' : 'Create New Email Template'}
              </h3>
              <button type="button" onClick={() => setEditorModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Template Key (Unique Identifier) *</label>
              <input
                type="text"
                value={currentTemplate.template_key || ''}
                onChange={(e) => setCurrentTemplate({ ...currentTemplate, template_key: e.target.value.toLowerCase().replace(/\s+/g, '_') })}
                placeholder="e.g. booking_confirmation"
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-mono font-bold text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Email Subject Line *</label>
              <input
                type="text"
                value={currentTemplate.subject || ''}
                onChange={(e) => setCurrentTemplate({ ...currentTemplate, subject: e.target.value })}
                placeholder="e.g. SmartServe Booking Confirmation — #{{booking_id}}"
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-bold text-slate-900 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Supported Template Variables</label>
              <div className="flex flex-wrap gap-1.5 p-2.5 bg-[#FAF7F0] rounded-xl border border-[#E5DEC9]">
                {['customer_name', 'booking_id', 'service_name', 'provider_name', 'scheduled_time', 'amount', 'otp_code'].map((v) => (
                  <button
                    key={v}
                    type="button"
                    onClick={() => setCurrentTemplate({ ...currentTemplate, body_html: (currentTemplate.body_html || '') + ` {{${v}}}` })}
                    className="font-mono text-[10px] font-bold text-slate-700 bg-white hover:bg-[#F2EDE1] hover:text-[#2F5233] px-2 py-1 rounded-lg border border-[#E5DEC9] transition-colors"
                  >
                    + &#123;&#123;{v}&#125;&#125;
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Body HTML / Content *</label>
              <textarea
                value={currentTemplate.body_html || ''}
                onChange={(e) => setCurrentTemplate({ ...currentTemplate, body_html: e.target.value })}
                rows={7}
                className="w-full bg-[#FAF7F0] border border-[#E5DEC9] rounded-xl p-3 text-xs font-mono text-slate-800 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                required
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setEditorModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={saveTemplateLoading}
                className="px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {saveTemplateLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Save Template'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Preview Modal */}
      {previewModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-xl rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E] flex items-center gap-2">
                <Eye className="w-5 h-5 text-[#2F5233]" />
                <span>Recipient Email Preview</span>
              </h3>
              <button type="button" onClick={() => setPreviewModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-3 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9] text-xs space-y-1">
              <p><strong className="text-slate-400">Subject:</strong> <span className="font-bold text-slate-900">{currentTemplate.subject?.replace(/{{booking_id}}/g, '5716e23b')}</span></p>
              <p><strong className="text-slate-400">Recipient Preview:</strong> <span className="text-slate-700">ananya.rao@example.com</span></p>
            </div>

            <div
              className="p-5 bg-white border border-[#E5DEC9] rounded-2xl text-sm space-y-2 shadow-xs"
              dangerouslySetInnerHTML={{ __html: renderLivePreviewHTML(currentTemplate) }}
            />

            <div className="flex justify-end pt-2">
              <button
                type="button"
                onClick={() => setPreviewModalOpen(false)}
                className="px-5 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Close Preview
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Send Confirmation Modal */}
      {confirmSendModalOpen && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white w-full max-w-md rounded-3xl shadow-xl border border-[#E5DEC9] p-6 space-y-4 animate-in fade-in">
            <div className="flex items-center justify-between border-b border-[#E5DEC9]/60 pb-3">
              <h3 className="text-base font-bold font-serif text-[#1F2A1E]">Send this email?</h3>
              <button type="button" onClick={() => setConfirmSendModalOpen(false)} className="text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>

            <p className="text-xs text-slate-600 font-semibold">
              Are you sure you want to dispatch this email to <strong>{composeRecipient}</strong>?
            </p>

            <div className="p-3 bg-[#FAF7F0] rounded-2xl border border-[#E5DEC9] text-xs font-bold text-slate-800">
              Subject: {composeSubject}
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setConfirmSendModalOpen(false)}
                className="px-4 py-2 bg-[#F2EDE1] text-slate-700 font-bold rounded-xl text-xs"
              >
                Cancel
              </button>
              <button
                type="button"
                onClick={handleDispatchConfirm}
                disabled={dispatchLoading}
                className="px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-xs shadow-sm flex items-center gap-1.5"
              >
                {dispatchLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : 'Confirm & Dispatch'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
