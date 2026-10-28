import React from 'react';
import { 
  CheckCircle2, 
  Sparkles, 
  KeyRound, 
  Clock, 
  Banknote, 
  ArrowDown, 
  X,
  MapPin
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { formatCurrencyINR } from '../../utils/formatters';

interface PostBookingSuccessCelebrationProps {
  bookingReference: string;
  serviceName: string;
  totalPrice: number;
  scheduledDate: string;
  scheduledTime: string;
  address: string;
  startOtp?: string;
  onDismiss: () => void;
  onScrollToRewards?: () => void;
}

export const PostBookingSuccessCelebration: React.FC<PostBookingSuccessCelebrationProps> = ({
  bookingReference,
  serviceName,
  totalPrice,
  scheduledDate,
  scheduledTime,
  address,
  startOtp,
  onDismiss,
  onScrollToRewards,
}) => {
  const { t } = useTranslation();

  return (
    <div className="bg-gradient-to-br from-emerald-900 via-[#1E3D22] to-[#122816] text-[#FAF7F0] p-6 sm:p-8 rounded-[32px] border-2 border-emerald-500/40 shadow-2xl relative overflow-hidden animate-in fade-in zoom-in-95 duration-300">
      {/* Background radial highlight */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-80 h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />

      {/* Dismiss Button */}
      <button
        onClick={onDismiss}
        className="absolute top-5 right-5 p-2 rounded-full bg-white/10 hover:bg-white/20 text-white/70 hover:text-white transition-colors"
        title="Dismiss celebration"
      >
        <X className="w-5 h-5" />
      </button>

      <div className="relative z-10 space-y-6">
        {/* Celebration Header */}
        <div className="flex flex-col sm:flex-row sm:items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500 text-white flex items-center justify-center shrink-0 shadow-lg shadow-emerald-500/30">
            <CheckCircle2 className="w-9 h-9" />
          </div>
          <div className="space-y-1">
            <div className="inline-flex items-center gap-2 px-3 py-0.5 rounded-full bg-emerald-400/20 text-emerald-300 text-[11px] font-black uppercase tracking-wider border border-emerald-400/30">
              <Sparkles className="w-3 h-3 text-amber-300" />
              <span>{t('booking.confirmed_banner_tag', { defaultValue: 'Booking Successfully Placed' })}</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight font-serif-display">
              {t('booking.confirmed_hero_title', { defaultValue: 'We’ve Received Your Service Request!' })}
            </h2>
            <p className="text-xs sm:text-sm text-white/80 font-sans max-w-xl">
              {t('booking.confirmed_hero_desc', { 
                defaultValue: 'Automated confirmation email and WhatsApp notifications have been dispatched. Your technician assignment is underway.' 
              })}
            </p>
          </div>
        </div>

        {/* Quick Booking Summary Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 pt-2">
          {/* Reference */}
          <div className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 space-y-1">
            <span className="text-[10px] uppercase font-bold text-white/60 tracking-wider block">Booking Reference</span>
            <span className="font-mono text-base font-extrabold text-white block">{bookingReference}</span>
            <span className="text-[11px] text-emerald-300 font-semibold block">{serviceName}</span>
          </div>

          {/* Schedule */}
          <div className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 space-y-1">
            <span className="text-[10px] uppercase font-bold text-white/60 tracking-wider flex items-center gap-1">
              <Clock className="w-3 h-3" />
              <span>Scheduled Slot</span>
            </span>
            <span className="text-sm font-bold text-white block">{scheduledDate}</span>
            <span className="text-xs text-white/80 block">{scheduledTime}</span>
          </div>

          {/* COD Payment */}
          <div className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 space-y-1">
            <span className="text-[10px] uppercase font-bold text-white/60 tracking-wider flex items-center gap-1">
              <Banknote className="w-3 h-3 text-amber-300" />
              <span>Payment (COD)</span>
            </span>
            <span className="font-mono text-lg font-black text-white block">{formatCurrencyINR(totalPrice)}</span>
            <span className="text-[11px] text-amber-300 font-semibold block">Pay cash after completion</span>
          </div>

          {/* Start OTP / Service Location */}
          {startOtp ? (
            <div className="p-4 rounded-2xl bg-amber-500/20 backdrop-blur-md border border-amber-400/40 space-y-1">
              <span className="text-[10px] uppercase font-bold text-amber-300 tracking-wider flex items-center gap-1">
                <KeyRound className="w-3 h-3 text-amber-300" />
                <span>Service Start OTP</span>
              </span>
              <span className="font-mono text-2xl font-black text-amber-200 tracking-widest block">{startOtp}</span>
              <span className="text-[10px] text-amber-200/80 block">Share upon technician arrival</span>
            </div>
          ) : (
            <div className="p-4 rounded-2xl bg-white/10 backdrop-blur-md border border-white/10 space-y-1">
              <span className="text-[10px] uppercase font-bold text-white/60 tracking-wider flex items-center gap-1">
                <MapPin className="w-3 h-3 text-rose-300" />
                <span>Service Address</span>
              </span>
              <span className="text-xs font-semibold text-white line-clamp-2 block">{address || 'Address on file'}</span>
            </div>
          )}
        </div>

        {/* Rewards Unlock Banner */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-amber-400/10 border border-amber-400/30">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-amber-500 text-white flex items-center justify-center shrink-0">
              <Sparkles className="w-5 h-5 animate-pulse" />
            </div>
            <div>
              <h4 className="font-bold text-sm text-white">
                {t('booking.partner_unlocked_title', { defaultValue: 'You Unlocked 1 Free Spin & Partner Vouchers!' })}
              </h4>
              <p className="text-xs text-amber-200/90">
                {t('booking.partner_unlocked_desc', { defaultValue: 'Spin the wheel below to claim coupons from Swiggy, Zomato, Blinkit, and Myntra.' })}
              </p>
            </div>
          </div>

          {onScrollToRewards && (
            <button
              onClick={onScrollToRewards}
              className="px-5 py-2.5 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-xs uppercase tracking-wider shrink-0 transition-all flex items-center justify-center gap-2 shadow-md hover:scale-[1.02]"
            >
              <span>{t('booking.claim_perks_btn', { defaultValue: 'Claim Partner Perks' })}</span>
              <ArrowDown className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
