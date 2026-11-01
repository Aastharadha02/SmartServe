import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { ShieldCheck, AlertTriangle, CheckCircle, Clock, X, Loader2, XCircle, AlertCircle } from 'lucide-react';
import { apiClient } from '../../api/client';
import { useToast } from '../../hooks/useToast';
import { getLocalizedServiceName } from '../../utils/localizedNames';

export interface WarrantyData {
  id: string;
  booking_id: string;
  service_name: string;
  issued_at: string;
  expires_at: string;
  is_active: boolean;
  claim_status: string; // None, Pending, Resolved, Rejected
  claim_description?: string;
  claim_submitted_at?: string;
  claim_resolved_at?: string;
  claim_notes?: string;
  days_remaining?: number;
  duration_days?: number;
  nominal_fee?: number;
  terms?: string;
  badge_label?: string;
  is_eligible?: boolean;
}

interface WarrantyCardProps {
  bookingId: string;
  serviceName: string;
  warranty?: WarrantyData | null;
  onClaimRaised?: () => void;
}

export const WarrantyCard: React.FC<WarrantyCardProps> = ({
  bookingId,
  serviceName,
  warranty,
  onClaimRaised,
}) => {
  const { t } = useTranslation();
  const { showToast } = useToast();
  const [showClaimModal, setShowClaimModal] = useState(false);
  const [description, setDescription] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [localClaimStatus, setLocalClaimStatus] = useState<string | null>(
    warranty?.claim_status && warranty.claim_status !== 'None' ? warranty.claim_status : null
  );

  useEffect(() => {
    if (warranty?.claim_status && warranty.claim_status !== 'None') {
      setLocalClaimStatus(warranty.claim_status);
    }
  }, [warranty?.claim_status]);

  const expiresDate = warranty?.expires_at ? new Date(warranty.expires_at) : null;
  const isExpired = expiresDate ? expiresDate.getTime() < Date.now() : false;
  const daysRemaining = warranty?.days_remaining ?? (expiresDate ? Math.max(0, Math.ceil((expiresDate.getTime() - Date.now()) / (1000 * 60 * 60 * 24))) : 7);

  const handleClaimSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (description.trim().length < 5) {
      showToast(t('warranty.toast_min_chars', { defaultValue: 'Please provide a detailed description (at least 5 characters).' }), 'error');
      return;
    }

    setSubmitting(true);
    try {
      const res = await apiClient.post(`/customer/bookings/${bookingId}/warranty/claim`, {
        description: description.trim(),
      });
      showToast(res.data?.message || t('warranty.claim_success', { defaultValue: 'Warranty claim submitted successfully! Our team will inspect and assist.' }), 'success');
      setLocalClaimStatus('Pending');
      setShowClaimModal(false);
      setDescription('');
      if (onClaimRaised) onClaimRaised();
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string' && (detail.includes('already been filed') || detail.includes('already registered'))) {
        setLocalClaimStatus('Pending');
        setShowClaimModal(false);
        showToast(detail, 'info');
        if (onClaimRaised) onClaimRaised();
      } else {
        const msg = detail || t('warranty.toast_submit_failed', { defaultValue: 'Failed to submit warranty claim.' });
        showToast(msg, 'error');
      }
    } finally {
      setSubmitting(false);
    }
  };


  return (
    <div className="bg-gradient-to-br from-[#FAF7F0] to-[#F2EDE1] border-2 border-[#C9A15A]/40 rounded-2xl p-5 shadow-xs relative overflow-hidden">
      {/* Decorative Gold Crest Background */}
      <div className="absolute -right-6 -bottom-6 w-32 h-32 bg-[#C9A15A]/10 rounded-full blur-xl pointer-events-none" />

      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-start gap-3.5">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-[#2F5233] to-[#1E3621] text-[#C9A15A] flex items-center justify-center shadow-xs flex-shrink-0">
            <ShieldCheck className="w-7 h-7" />
          </div>
          <div>
            <div className="flex items-center gap-2 flex-wrap">
              <h3 className="text-sm font-bold text-[#1F2A1E]">
                {warranty?.badge_label || (warranty?.duration_days ? `${warranty.duration_days}-Day Digital Warranty` : t('warranty.title', { defaultValue: 'SmartServe Quality Guarantee' }))}
              </h3>
              <span className={`px-2 py-0.5 text-[11px] font-extrabold rounded-full ${
                localClaimStatus === 'Pending'
                  ? 'bg-amber-100 text-amber-800 border border-amber-300'
                  : localClaimStatus === 'Resolved'
                  ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                  : localClaimStatus === 'Rejected'
                  ? 'bg-rose-100 text-rose-800 border border-rose-300'
                  : isExpired
                  ? 'bg-stone-200 text-stone-700'
                  : 'bg-[#2F5233]/15 text-[#2F5233] border border-[#2F5233]/30'
              }`}>
                {localClaimStatus === 'Pending'
                  ? t('warranty.claim_pending', { defaultValue: 'Claim Pending' })
                  : localClaimStatus === 'Resolved'
                  ? t('warranty.claim_resolved', { defaultValue: 'Claim Resolved' })
                  : localClaimStatus === 'Rejected'
                  ? t('warranty.claim_rejected', { defaultValue: 'Claim Rejected' })
                  : isExpired
                  ? t('warranty.expired', { defaultValue: 'Expired' })
                  : t('warranty.badge', { defaultValue: 'Active Warranty' })}
              </span>
            </div>
            <p className="text-xs text-[#1F2A1E]/70 mt-1 max-w-xl leading-relaxed">
              {warranty?.terms || t('warranty.description', {
                defaultValue:
                  'This service is covered by our home maintenance quality guarantee. If you experience any recurring issue with this job, you can raise a warranty rework claim.',
              })}
            </p>

            {expiresDate && (
              <div className="flex items-center gap-2 mt-2 text-[11px] font-semibold text-[#1F2A1E]/60">
                <Clock className="w-3.5 h-3.5 text-[#C9A15A]" />
                <span>
                  {t('warranty.expires_summary', { date: expiresDate.toLocaleDateString(), days: daysRemaining, defaultValue: `Valid until: ${expiresDate.toLocaleDateString()} (${daysRemaining} days left)` })}
                </span>
              </div>
            )}

            {/* Claim Rejection Notice & Admin Notes */}
            {localClaimStatus === 'Rejected' && (
              <div className="mt-3 p-3 bg-rose-50/90 border border-rose-200 rounded-xl space-y-1">
                <div className="flex items-center gap-1.5 text-xs font-bold text-rose-800">
                  <AlertCircle className="w-3.5 h-3.5 text-rose-600 shrink-0" />
                  <span>{t('warranty.rejection_reason_label', { defaultValue: 'Admin Decision / Rejection Note' })}:</span>
                </div>
                <p className="text-xs text-rose-700 pl-5 leading-relaxed font-semibold">
                  {warranty?.claim_notes || t('warranty.claim_rejected_default_note', { defaultValue: 'Claim marked as Rejected by Admin' })}
                </p>
                {warranty?.claim_description && (
                  <p className="text-[11px] text-[#1F2A1E]/70 pl-5 pt-0.5">
                    <strong>{t('warranty.customer_claim', { defaultValue: 'Customer Issue' })}:</strong> "{warranty.claim_description}"
                  </p>
                )}
              </div>
            )}

            {/* Claim Resolved Notice */}
            {localClaimStatus === 'Resolved' && (
              <div className="mt-3 p-3 bg-emerald-50/90 border border-emerald-200 rounded-xl space-y-1">
                <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-800">
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                  <span>{t('warranty.resolution_note_label', { defaultValue: 'Resolution Note' })}:</span>
                </div>
                <p className="text-xs text-emerald-700 pl-5 leading-relaxed font-semibold">
                  {warranty?.claim_notes || t('warranty.claim_resolved_default_note', { defaultValue: 'Warranty claim resolved and approved for free rework inspection.' })}
                </p>
              </div>
            )}

            {/* Claim Under Review Notice */}
            {localClaimStatus === 'Pending' && warranty?.claim_description && (
              <div className="mt-3 p-3 bg-amber-50/90 border border-amber-200 rounded-xl space-y-1">
                <div className="flex items-center gap-1.5 text-xs font-bold text-amber-800">
                  <Clock className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                  <span>{t('warranty.claim_under_review', { defaultValue: 'Claim Under Review' })}:</span>
                </div>
                <p className="text-xs text-amber-700 pl-5 leading-relaxed font-semibold">
                  "{warranty.claim_description}"
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Claim Action Button */}
        <div>
          {!localClaimStatus && !isExpired && (
            <button
              onClick={() => setShowClaimModal(true)}
              className="px-4 py-2.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-xl shadow-xs transition-all flex items-center gap-2 cursor-pointer w-full sm:w-auto justify-center"
            >
              <AlertTriangle className="w-4 h-4 text-[#C9A15A]" />
              <span>{t('warranty.raise_claim', { defaultValue: 'Raise Warranty Claim' })}</span>
            </button>
          )}

          {localClaimStatus === 'Pending' && (
            <div className="flex items-center gap-1.5 text-xs font-bold text-amber-700 bg-amber-50 px-3 py-2 rounded-xl border border-amber-200">
              <Clock className="w-4 h-4" />
              <span>{t("warranty.claim_pending", { defaultValue: "Claim Under Inspection" })}</span>
            </div>
          )}

          {localClaimStatus === 'Resolved' && (
            <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-700 bg-emerald-50 px-3 py-2 rounded-xl border border-emerald-200">
              <CheckCircle className="w-4 h-4" />
              <span>{t("warranty.claim_resolved", { defaultValue: "Claim Resolved" })}</span>
            </div>
          )}

          {localClaimStatus === 'Rejected' && (
            <div className="flex items-center gap-1.5 text-xs font-bold text-rose-700 bg-rose-50 px-3 py-2 rounded-xl border border-rose-200">
              <XCircle className="w-4 h-4 text-rose-600" />
              <span>{t("warranty.claim_rejected", { defaultValue: "Claim Rejected" })}</span>
            </div>
          )}
        </div>
      </div>

      {/* Claim Modal */}
      {showClaimModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in">
          <div className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-2xl w-full max-w-lg p-6 shadow-2xl relative">
            <button
              onClick={() => setShowClaimModal(false)}
              className="absolute top-4 right-4 p-1.5 text-[#1F2A1E]/40 hover:text-[#1F2A1E] rounded-lg cursor-pointer"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-sm text-[#1F2A1E]">
                  {t('warranty.claim_modal_title', { defaultValue: 'Raise Warranty Claim' })}
                </h3>
                <p className="text-xs text-[#1F2A1E]/60">{getLocalizedServiceName(serviceName)}</p>
              </div>
            </div>

            <div className="p-3 bg-emerald-50 rounded-xl border border-emerald-200 mb-4 text-xs space-y-1">
              <p className="font-bold text-emerald-900 flex items-center gap-1.5">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                {t('warranty.free_guarantee_title', { defaultValue: '100% Free Rework Guarantee' })}
              </p>
              <p className="text-emerald-800 leading-relaxed">
                {t('warranty.claim_free_note', {
                  defaultValue: 'Under your 7-day SmartServe warranty, all follow-up inspection and rework labor is completely free with zero additional charges.',
                })}
              </p>
            </div>

            <form onSubmit={handleClaimSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-[#1F2A1E] mb-1.5">
                  {t("warranty.issue_description", { defaultValue: "Issue Description *" })}
                </label>
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder={t('warranty.claim_placeholder', {
                    defaultValue: 'Describe the recurring problem in detail...',
                  })}
                  rows={4}
                  required
                  className="w-full bg-white border border-[#E5DEC9] rounded-xl p-3 text-xs text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                />
              </div>

              <div className="flex items-center justify-end gap-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowClaimModal(false)}
                  className="px-4 py-2 border border-[#E5DEC9] rounded-xl text-xs font-bold text-[#1F2A1E]/70 hover:bg-[#F2EDE1]"
                >
                  {t('common.cancel', { defaultValue: 'Cancel' })}
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  {submitting && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                  <span>{submitting ? t('warranty.submitting', { defaultValue: 'Submitting...' }) : t('warranty.submit_claim', { defaultValue: 'Submit Warranty Claim' })}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
