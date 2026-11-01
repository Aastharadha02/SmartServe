import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  Layers,
  Trash2,
  Plus,
  Calendar,
  MapPin,
  Clipboard,
  FileText,
  Upload,
  ShieldCheck,
  Sparkles,
  ArrowRight,
  AlertCircle,
  Loader2,
  CheckCircle,
  Tag,
} from 'lucide-react';
import {
  getBundleItems,
  removeBundleItem,
  clearBundle,
  BundleServiceItem,
} from '../utils/bundleCart';
import {
  getCombinedEstimate,
  createCombinedBooking,
  CombinedEstimateResponse,
  CombinedBookingCreatePayload,
} from '../api/bookings';
import { useAuth } from '../auth/useAuth';
import { useToast } from '../hooks/useToast';
import { formatCurrencyINR } from '../utils/formatters';
import { apiClient } from '../api/client';
import { getLocalizedServiceName, getLocalizedCategory } from '../utils/localizedNames';

export const CustomerCombinedBooking: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { showToast } = useToast();

  const [bundleItems, setBundleItems] = useState<BundleServiceItem[]>([]);
  const [estimate, setEstimate] = useState<CombinedEstimateResponse | null>(null);
  const [estimateLoading, setEstimateLoading] = useState(false);

  // Form State
  const [scheduledDate, setScheduledDate] = useState(() => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().slice(0, 10);
  });
  const [scheduledTime, setScheduledTime] = useState('10:00 AM');
  const [addressLine1, setAddressLine1] = useState('Flat 402, Sunshine Apartments, Sector 62');
  const [city, setCity] = useState('Noida');
  const [pincode, setPincode] = useState('201301');

  // Phone Notes State
  const [notesTab, setNotesTab] = useState<'type' | 'clipboard' | 'file'>('type');
  const [customerNotes, setCustomerNotes] = useState('');
  const [submitting, setSubmitting] = useState(false);

  // Coupon State
  const [couponCodeInput, setCouponCodeInput] = useState<string>('');
  const [appliedCoupon, setAppliedCoupon] = useState<{ code: string; discount: number } | null>(null);
  const [validatingCoupon, setValidatingCoupon] = useState<boolean>(false);

  const handleApplyCoupon = async () => {
    if (!couponCodeInput.trim()) return;
    setValidatingCoupon(true);
    try {
      const netSubtotal = (estimate?.subtotal ?? 0) - (estimate?.discount_applied ?? 0);
      const res = await apiClient.post('/coupons/validate', {
        code: couponCodeInput.trim(),
        subtotal: netSubtotal,
        service_ids: bundleItems.map((i) => i.id),
      });
      if (res.data?.is_valid) {
        setAppliedCoupon({
          code: res.data.code,
          discount: Number(res.data.discount_amount),
        });
        showToast(res.data.message || 'Coupon applied successfully!', 'success');
      } else {
        showToast(res.data?.message || 'Invalid coupon code', 'error');
      }
    } catch (err: any) {
      showToast(err.response?.data?.detail || 'Failed to validate coupon', 'error');
    } finally {
      setValidatingCoupon(false);
    }
  };

  const handleRemoveCoupon = () => {
    setAppliedCoupon(null);
    setCouponCodeInput('');
  };

  // Load bundle items from storage
  useEffect(() => {
    const items = getBundleItems();
    setBundleItems(items);
  }, []);

  // Fetch estimate when items change
  useEffect(() => {
    if (bundleItems.length < 2) {
      setEstimate(null);
      return;
    }

    const sIds = bundleItems.map((x) => x.id);
    setEstimateLoading(true);
    getCombinedEstimate(sIds)
      .then((data) => setEstimate(data))
      .catch((err) => {
        console.warn('Failed to calculate combined estimate:', err);
      })
      .finally(() => setEstimateLoading(false));
  }, [bundleItems]);

  const handleRemove = (id: string) => {
    const updated = removeBundleItem(id);
    setBundleItems(updated);
  };

  const handleClearAll = () => {
    clearBundle();
    setBundleItems([]);
  };

  // Clipboard Paste handler
  const handlePasteClipboard = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (!text.trim()) {
        showToast(t('bundle.toast_clipboard_empty', { defaultValue: 'Clipboard is empty.' }), 'error');
        return;
      }
      setCustomerNotes((prev) => (prev ? `${prev}\n${text.trim()}` : text.trim()));
      showToast(t('bundle.toast_pasted_instructions', { defaultValue: 'Pasted instructions from clipboard ✓' }), 'success');
    } catch {
      showToast(t('bundle.toast_clipboard_denied', { defaultValue: 'Clipboard access was denied. Please paste manually.' }), 'error');
    }
  };

  // File Import handler
  const handleFileImport = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      const content = event.target?.result as string;
      if (content) {
        setCustomerNotes((prev) => (prev ? `${prev}\n${content.trim()}` : content.trim()));
        showToast(t('bundle.toast_imported_notes', { fileName: file.name, defaultValue: `Imported notes from ${file.name} ✓` }), 'success');
      }
    };
    reader.readAsText(file);
  };

  // Submit Combined Booking
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) {
      showToast(t('errors.login_required', { defaultValue: 'Please log in to confirm booking.' }), 'error');
      navigate('/login');
      return;
    }

    if (bundleItems.length < 2) {
      showToast(t('bundle.toast_min_services', { defaultValue: 'A combined booking requires at least 2 services. Please add more from the catalog.' }), 'error');
      return;
    }

    if (!addressLine1.trim() || addressLine1.length < 5) {
      showToast(t('bundle.toast_valid_address', { defaultValue: 'Please enter a valid service address.' }), 'error');
      return;
    }

    setSubmitting(true);
    const dateStr: string = scheduledDate ? String(scheduledDate).trim() : new Date().toISOString().slice(0, 10);

    const payload: CombinedBookingCreatePayload = {
      service_ids: bundleItems.map((x) => x.id),
      scheduled_date: dateStr,
      scheduled_time: scheduledTime,
      address_line1: addressLine1.trim(),
      city: city.trim(),
      pincode: pincode.trim(),
      customer_notes: customerNotes.trim() ? customerNotes.trim() : null,
      payment_method: 'COD',
      coupon_code: appliedCoupon?.code || undefined,
    };

    try {
      await createCombinedBooking(payload);
      clearBundle();
      showToast(t('booking.booking_success', { defaultValue: 'Combined booking confirmed successfully!' }), 'success');
      navigate(`/bookings`);
    } catch (err: any) {
      const msg = err.response?.data?.detail || 'Failed to create combined booking. Please try again.';
      showToast(msg, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const timeSlots = [
    '09:00 AM',
    '10:00 AM',
    '11:30 AM',
    '01:00 PM',
    '02:30 PM',
    '04:00 PM',
    '05:30 PM',
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 font-sans">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 text-xs font-bold text-[#C9A15A] uppercase tracking-wider mb-1">
          <Sparkles className="w-4 h-4 text-[#C9A15A]" />
          <span>{t('bundle.advantage', { defaultValue: 'SmartServe Bundle Advantage' })}</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-[#1F2A1E]">
          {t('bundle.title', { defaultValue: 'Combined Multi-Service Booking' })}
        </h1>
        <p className="text-sm text-[#1F2A1E]/70 mt-1">
          {t('bundle.subtitle', {
            defaultValue:
              'Schedule multiple home services in a single visit with automatic bundle discounts and unified scheduling.',
          })}
        </p>
      </div>

      {bundleItems.length === 0 ? (
        /* Empty Bundle State */
        <div className="bg-[#FAF7F0] border-2 border-dashed border-[#E5DEC9] rounded-3xl p-12 text-center max-w-xl mx-auto shadow-xs">
          <div className="w-16 h-16 rounded-2xl bg-[#F2EDE1] text-[#2F5233] flex items-center justify-center mx-auto mb-4">
            <Layers className="w-8 h-8" />
          </div>
          <h3 className="text-lg font-bold text-[#1F2A1E] mb-2">{t('bundle.empty_title', { defaultValue: 'Your Bundle Is Empty' })}</h3>
          <p className="text-xs text-[#1F2A1E]/60 mb-6 leading-relaxed">
            {t('bundle.empty_cart', {
              defaultValue:
                'Explore our catalog and add 2 or more services to unlock automatic 5% to 10% bundle discounts.',
            })}
          </p>
          <Link
            to="/catalog"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#2F5233] text-white font-bold text-xs shadow-xs hover:bg-[#3D6B42] transition-colors"
          >
            <span>{t('bundle.explore_services', { defaultValue: 'Explore Services' })}</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      ) : (
        /* Main Two-Column Layout */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left Column: Form & Services Review */}
          <div className="lg:col-span-7 space-y-6">
            {/* 1. Services in Bundle Card */}
            <div className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-3xl p-6 shadow-2xs space-y-4">
              <div className="flex items-center justify-between border-b border-[#E5DEC9] pb-3">
                <div className="flex items-center gap-2">
                  <Layers className="w-5 h-5 text-[#2F5233]" />
                  <h3 className="font-bold text-sm text-[#1F2A1E]">
                    {t('bundle.services_in_bundle_count', { count: bundleItems.length, defaultValue: `Selected Services (${bundleItems.length})` })}
                  </h3>
                </div>
                <div className="flex items-center gap-3">
                  <Link
                    to="/catalog"
                    className="text-xs font-bold text-[#2F5233] hover:underline flex items-center gap-1"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>{t('bundle.add_more', { defaultValue: 'Add More' })}</span>
                  </Link>
                  <button
                    onClick={handleClearAll}
                    className="text-xs font-bold text-rose-600 hover:underline flex items-center gap-1 cursor-pointer"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                    <span>{t('bundle.clear_bundle', { defaultValue: 'Clear' })}</span>
                  </button>
                </div>
              </div>

              <div className="divide-y divide-[#E5DEC9]/60">
                {bundleItems.map((item) => (
                  <div key={item.id} className="py-3.5 flex items-center justify-between gap-4">
                    <div>
                      <h4 className="font-bold text-xs text-[#1F2A1E]">{getLocalizedServiceName(item.name)}</h4>
                      <span className="text-[10px] text-[#1F2A1E]/50 uppercase tracking-wider font-semibold">
                        {getLocalizedCategory(item.category)}
                      </span>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="font-bold text-xs text-[#2F5233] font-mono">
                        {formatCurrencyINR(item.base_price)}
                      </span>
                      <button
                        onClick={() => handleRemove(item.id)}
                        className="p-1.5 text-[#1F2A1E]/40 hover:text-rose-600 hover:bg-rose-50 rounded-lg cursor-pointer transition-colors"
                        title={t('bundle.remove_service', { defaultValue: 'Remove service' })}
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              {bundleItems.length < 2 && (
                <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl flex items-center gap-2 text-xs text-amber-800">
                  <AlertCircle className="w-4 h-4 text-amber-600 flex-shrink-0" />
                  <span>{t('bundle.add_min_2', { defaultValue: 'Add at least 1 more service to qualify for combined bundle discounts.' })}</span>
                </div>
              )}
            </div>

            {/* 2. Unified Scheduling Card */}
            <div className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-3xl p-6 shadow-2xs space-y-4">
              <div className="flex items-center gap-2 border-b border-[#E5DEC9] pb-3">
                <Calendar className="w-5 h-5 text-[#2F5233]" />
                <h3 className="font-bold text-sm text-[#1F2A1E]">
                  {t('bundle.schedule_all', { defaultValue: 'Date & Time for Visit' })}
                </h3>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-[#1F2A1E] mb-1.5">
                    {t('booking.select_date', { defaultValue: 'Appointment Date' })}
                  </label>
                  <input
                    type="date"
                    value={scheduledDate}
                    min={new Date().toISOString().split('T')[0]}
                    onChange={(e) => setScheduledDate(e.target.value)}
                    className="w-full bg-white border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-[#1F2A1E] mb-1.5">
                    {t('booking.select_time', { defaultValue: 'Preferred Start Slot' })}
                  </label>
                  <select
                    value={scheduledTime}
                    onChange={(e) => setScheduledTime(e.target.value)}
                    className="w-full bg-white border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                  >
                    {timeSlots.map((slot) => (
                      <option key={slot} value={slot}>
                        {slot}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* 3. Service Address Card */}
            <div className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-3xl p-6 shadow-2xs space-y-4">
              <div className="flex items-center gap-2 border-b border-[#E5DEC9] pb-3">
                <MapPin className="w-5 h-5 text-[#2F5233]" />
                <h3 className="font-bold text-sm text-[#1F2A1E]">
                  {t('booking.your_address', { defaultValue: 'Service Location Address' })}
                </h3>
              </div>

              <div className="space-y-3">
                <div>
                  <label className="block text-xs font-bold text-[#1F2A1E] mb-1">
                    {t('bundle.address_label', { defaultValue: 'Street Address & Flat / House No. *' })}
                  </label>
                  <input
                    type="text"
                    value={addressLine1}
                    onChange={(e) => setAddressLine1(e.target.value)}
                    placeholder={t('bundle.address_placeholder', { defaultValue: 'Flat / House No., Building Name, Street...' })}
                    required
                    className="w-full bg-white border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-xs font-bold text-[#1F2A1E] mb-1">
                      {t('booking.city', { defaultValue: 'City' })}
                    </label>
                    <input
                      type="text"
                      value={city}
                      onChange={(e) => setCity(e.target.value)}
                      className="w-full bg-white border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-[#1F2A1E] mb-1">
                      {t('booking.pincode', { defaultValue: 'PIN Code' })}
                    </label>
                    <input
                      type="text"
                      value={pincode}
                      onChange={(e) => setPincode(e.target.value)}
                      className="w-full bg-white border border-[#E5DEC9] rounded-xl p-2.5 text-xs font-medium text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* 4. Phone Notes / In-App Instructions Card */}
            <div className="bg-[#FAF7F0] border border-[#E5DEC9] rounded-3xl p-6 shadow-2xs space-y-4">
              <div className="flex items-center justify-between border-b border-[#E5DEC9] pb-3">
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-[#2F5233]" />
                  <h3 className="font-bold text-sm text-[#1F2A1E]">
                    {t('bundle.notes_title', { defaultValue: 'Phone Notes & Special Instructions' })}
                  </h3>
                </div>
              </div>

              {/* Consent & Privacy Notice */}
              <div className="p-3.5 bg-emerald-50/70 border border-emerald-200/80 rounded-2xl flex items-start gap-3">
                <ShieldCheck className="w-4 h-4 text-emerald-700 flex-shrink-0 mt-0.5" />
                <p className="text-[11px] text-emerald-900 leading-relaxed font-medium">
                  {t('bundle.consent_disclaimer', {
                    defaultValue:
                      'Your instructions and notes will be shared exclusively with the assigned service professionals for this booking.',
                  })}
                </p>
              </div>

              {/* Note Import Method Tabs */}
              <div className="flex items-center gap-2 border-b border-[#E5DEC9] pb-2">
                <button
                  type="button"
                  onClick={() => setNotesTab('type')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                    notesTab === 'type'
                      ? 'bg-[#2F5233] text-white shadow-2xs'
                      : 'text-[#1F2A1E]/70 hover:bg-[#F2EDE1]'
                  }`}
                >
                  {t('bundle.tab_type', { defaultValue: 'Type Instructions' })}
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setNotesTab('clipboard');
                    handlePasteClipboard();
                  }}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                    notesTab === 'clipboard'
                      ? 'bg-[#2F5233] text-white shadow-2xs'
                      : 'text-[#1F2A1E]/70 hover:bg-[#F2EDE1]'
                  }`}
                >
                  <Clipboard className="w-3.5 h-3.5" />
                  <span>{t('bundle.tab_clipboard', { defaultValue: 'Paste from Clipboard' })}</span>
                </button>
                <button
                  type="button"
                  onClick={() => setNotesTab('file')}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                    notesTab === 'file'
                      ? 'bg-[#2F5233] text-white shadow-2xs'
                      : 'text-[#1F2A1E]/70 hover:bg-[#F2EDE1]'
                  }`}
                >
                  <Upload className="w-3.5 h-3.5" />
                  <span>{t('bundle.tab_file', { defaultValue: 'Import File' })}</span>
                </button>
              </div>

              {/* File Upload Trigger */}
              {notesTab === 'file' && (
                <div className="p-4 bg-white border border-[#E5DEC9] rounded-2xl flex flex-col items-center justify-center text-center space-y-2">
                  <Upload className="w-6 h-6 text-[#2F5233]" />
                  <p className="text-xs font-semibold text-[#1F2A1E]">
                    {t('bundle.attach_notes_desc', { defaultValue: "Attach notes exported from your phone's Notes app (.txt or .md)" })}
                  </p>
                  <label className="px-4 py-2 bg-[#2F5233] text-white rounded-xl text-xs font-bold cursor-pointer hover:bg-[#3D6B42] transition-colors">
                    {t('bundle.import_file_btn', { defaultValue: 'Choose File' })}
                    <input
                      type="file"
                      accept=".txt,.md,text/plain"
                      onChange={handleFileImport}
                      className="hidden"
                    />
                  </label>
                </div>
              )}

              {/* Text Area */}
              <div>
                <textarea
                  value={customerNotes}
                  onChange={(e) => setCustomerNotes(e.target.value)}
                  placeholder={t('bundle.type_placeholder', {
                    defaultValue:
                      'e.g. Master valve is under kitchen sink, turn off main electrical breaker first, call on mobile upon gate arrival...',
                  })}
                  rows={4}
                  className="w-full bg-white border border-[#E5DEC9] rounded-xl p-3 text-xs text-[#1F2A1E] focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233]"
                />
                <span className="text-[10px] text-[#1F2A1E]/40 block text-right mt-1">
                  {t('bundle.characters_count', { count: customerNotes.length, defaultValue: `${customerNotes.length} characters` })}
                </span>
              </div>
            </div>
          </div>

          {/* Right Column: Price Breakdown & Confirmation */}
          <div className="lg:col-span-5 sticky top-24 space-y-5">
            <div className="bg-[#FAF7F0] border-2 border-[#C9A15A]/40 rounded-3xl p-6 shadow-md space-y-5">
              <div className="flex items-center justify-between border-b border-[#E5DEC9] pb-3">
                <div className="flex items-center gap-2">
                  <h3 className="font-extrabold text-sm text-[#1F2A1E]">
                    {t('bundle.price_estimates_title', { defaultValue: 'Price Estimate & Discounts' })}
                  </h3>
                  {estimateLoading && (
                    <span className="w-3.5 h-3.5 border-2 border-[#2F5233] border-t-transparent rounded-full animate-spin" />
                  )}
                </div>
                {estimate && estimate.discount_rate > 0 && (
                  <span className="px-2.5 py-1 rounded-full text-[10px] font-black uppercase bg-[#C9A15A] text-white shadow-2xs">
                    {(estimate.discount_rate * 100).toFixed(0)}% {t('bundle.bundle_off', { defaultValue: 'Bundle Off' })}
                  </span>
                )}
              </div>

              {/* Itemized Line Items */}
              <div className="space-y-2.5 text-xs divide-y divide-[#E5DEC9]/40">
                {bundleItems.map((item) => (
                  <div key={item.id} className="pt-2 flex items-center justify-between">
                    <span className="text-[#1F2A1E]/80">{getLocalizedServiceName(item.name)}</span>
                    <span className="font-mono font-bold text-[#1F2A1E]">
                      {formatCurrencyINR(item.base_price)}
                    </span>
                  </div>
                ))}
              </div>

              {/* Promo Coupon Box */}
              <div className="pt-2">
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <Tag className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#1F2A1E]/40" />
                    <input
                      type="text"
                      value={couponCodeInput}
                      onChange={(e) => setCouponCodeInput(e.target.value.toUpperCase())}
                      placeholder={t('bundle.coupon_placeholder', { defaultValue: 'Enter coupon (e.g. WELCOME50)' })}
                      disabled={validatingCoupon || !!appliedCoupon}
                      className="w-full bg-white border border-[#E5DEC9] rounded-xl pl-8 pr-3 py-2 text-xs font-mono uppercase text-[#1F2A1E] focus:outline-none focus:border-[#2F5233]"
                    />
                  </div>
                  {appliedCoupon ? (
                    <button
                      type="button"
                      onClick={handleRemoveCoupon}
                      className="px-3 py-2 bg-rose-50 border border-rose-200 text-rose-700 rounded-xl text-xs font-bold hover:bg-rose-100 cursor-pointer"
                    >
                      {t('common.remove', { defaultValue: 'Remove' })}
                    </button>
                  ) : (
                    <button
                      type="button"
                      onClick={handleApplyCoupon}
                      disabled={validatingCoupon || !couponCodeInput.trim()}
                      className="px-3 py-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white rounded-xl text-xs font-bold transition-all disabled:opacity-50 cursor-pointer"
                    >
                      {validatingCoupon ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : t('common.apply', { defaultValue: 'Apply' })}
                    </button>
                  )}
                </div>
                {appliedCoupon && (
                  <p className="text-[11px] text-emerald-700 font-medium mt-1 flex items-center gap-1">
                    <CheckCircle className="w-3 h-3" />
                    {t('bundle.coupon_active', { code: appliedCoupon.code, defaultValue: `Coupon '${appliedCoupon.code}' applied!` })}
                  </p>
                )}
              </div>

              {/* Calculation Summary */}
              <div className="pt-3 border-t border-[#E5DEC9] space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-[#1F2A1E]/70">
                    {t('bundle.subtotal', { defaultValue: 'Standard Subtotal' })}
                  </span>
                  <span className="font-mono font-bold text-[#1F2A1E]">
                    {formatCurrencyINR(
                      estimate?.subtotal ??
                        bundleItems.reduce((acc, curr) => acc + curr.base_price, 0)
                    )}
                  </span>
                </div>

                {estimate && estimate.discount_applied > 0 && (
                  <div className="flex items-center justify-between text-emerald-800 font-bold bg-emerald-50 px-2.5 py-1.5 rounded-xl border border-emerald-200">
                    <div className="flex items-center gap-1.5">
                      <Tag className="w-3.5 h-3.5" />
                      <span>{t('bundle.bundle_discount', { defaultValue: 'Bundle Discount' })}</span>
                    </div>
                    <span className="font-mono">
                      -{formatCurrencyINR(estimate.discount_applied)}
                    </span>
                  </div>
                )}

                {appliedCoupon && appliedCoupon.discount > 0 && (
                  <div className="flex items-center justify-between text-emerald-800 font-bold bg-emerald-50 px-2.5 py-1.5 rounded-xl border border-emerald-200">
                    <div className="flex items-center gap-1.5">
                      <Tag className="w-3.5 h-3.5" />
                      <span>{t('bundle.coupon_discount', { defaultValue: 'Coupon Discount' })} ({appliedCoupon.code})</span>
                    </div>
                    <span className="font-mono">
                      -{formatCurrencyINR(appliedCoupon.discount)}
                    </span>
                  </div>
                )}

                <div className="flex items-center justify-between pt-3 border-t border-[#E5DEC9] text-base font-extrabold text-[#1F2A1E]">
                  <span>{t('bundle.final_total', { defaultValue: 'Estimated Total' })}</span>
                  <span className="font-mono text-[#2F5233] text-xl">
                    {formatCurrencyINR(
                      Math.max(
                        0,
                        (estimate?.final_price ?? bundleItems.reduce((acc, curr) => acc + curr.base_price, 0)) -
                          (appliedCoupon?.discount ?? 0)
                      )
                    )}
                  </span>
                </div>
              </div>

              {/* Payment Mode */}
              <div className="p-3 bg-white border border-[#E5DEC9] rounded-2xl flex items-center justify-between">
                <div>
                  <span className="text-[10px] text-[#1F2A1E]/50 uppercase font-bold block">
                    {t('bundle.payment_method_label', { defaultValue: 'Payment Method' })}
                  </span>
                  <span className="text-xs font-bold text-[#1F2A1E]">
                    {t('booking.cod', { defaultValue: 'Cash on Delivery (COD)' })}
                  </span>
                </div>
                <CheckCircle className="w-4 h-4 text-emerald-600" />
              </div>

              {/* Guarantee Strip */}
              <div className="flex items-center gap-2.5 text-[11px] text-[#1F2A1E]/70 bg-[#F2EDE1]/60 p-3 rounded-2xl">
                <ShieldCheck className="w-4 h-4 text-[#2F5233] flex-shrink-0" />
                <span>
                  {t('bundle.warranty_included', { defaultValue: 'All services in this request include our 7-Day Service Warranty.' })}
                </span>
              </div>

              {/* Submit Button */}
              <button
                type="button"
                onClick={handleSubmit}
                disabled={submitting || bundleItems.length < 2}
                className="w-full py-3.5 px-6 rounded-2xl bg-[#2F5233] hover:bg-[#3D6B42] text-white font-extrabold text-sm shadow-md transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>{t('bundle.scheduling_progress', { defaultValue: 'Scheduling Booking...' })}</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-[#C9A15A]" />
                    <span>{t('bundle.confirm_combined', { defaultValue: 'Confirm Combined Booking' })}</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomerCombinedBooking;
