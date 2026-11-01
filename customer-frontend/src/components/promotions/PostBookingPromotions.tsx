import React, { useState, useEffect, useRef } from 'react';
import { 
  Gift, 
  Sparkles, 
  Copy, 
  Check, 
  ExternalLink, 
  Tag, 
  ShoppingBag, 
  Utensils, 
  Zap, 
  HeartPulse, 
  X,
  RotateCw,
  Trophy,
  Flame
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { apiClient } from '../../api/client';

export interface PartnerPromo {
  id: string;
  brand: string;
  brandColor: string;
  category: 'food' | 'grocery' | 'fashion' | 'health' | 'home';
  title: string;
  description: string;
  code: string;
  discount: string;
  minOrder?: string;
  validDays: number;
  partnerUrl: string;
  logoText: string;
}

const PARTNER_OFFERS: PartnerPromo[] = [
  {
    id: 'swiggy-gourmet',
    brand: 'Swiggy',
    brandColor: '#FC8019',
    category: 'food',
    title: 'Flat ₹125 OFF on Food Orders',
    description: 'Craving delicious food while your home is being serviced? Enjoy discount on top restaurants.',
    code: 'SWIGGYSERVE',
    discount: '₹125 OFF',
    minOrder: 'Min order ₹299',
    validDays: 7,
    partnerUrl: 'https://www.swiggy.com',
    logoText: 'SWIGGY',
  },
  {
    id: 'zomato-dining',
    brand: 'Zomato',
    brandColor: '#E23744',
    category: 'food',
    title: '25% OFF on Zomato Dining & Delivery',
    description: 'Treat yourself to curated gourmet cafes and restaurants across your city.',
    code: 'ZOMATOSMART',
    discount: '25% OFF',
    minOrder: 'Up to ₹200 savings',
    validDays: 10,
    partnerUrl: 'https://www.zomato.com',
    logoText: 'ZOMATO',
  },
  {
    id: 'blinkit-grocery',
    brand: 'Blinkit',
    brandColor: '#F8CB46',
    category: 'grocery',
    title: 'Flat ₹100 Cashback in 10 Mins',
    description: 'Instant grocery delivery at your doorstep before your technician wraps up work.',
    code: 'BLINKSERVE',
    discount: '₹100 Cashback',
    minOrder: 'Min order ₹499',
    validDays: 5,
    partnerUrl: 'https://blinkit.com',
    logoText: 'BLINKIT',
  },
  {
    id: 'myntra-fashion',
    brand: 'Myntra',
    brandColor: '#FF3F6C',
    category: 'fashion',
    title: '₹250 OFF on Home Decor & Apparel',
    description: 'Refresh your wardrobe and living spaces with India’s top lifestyle brands.',
    code: 'MYNTRASMART',
    discount: '₹250 OFF',
    minOrder: 'Min order ₹1,199',
    validDays: 14,
    partnerUrl: 'https://www.myntra.com',
    logoText: 'MYNTRA',
  },
  {
    id: 'tata-1mg',
    brand: 'Tata 1mg',
    brandColor: '#FF6F61',
    category: 'health',
    title: 'Flat 20% OFF on Health & Wellness',
    description: 'Order health essentials and family wellness products with priority delivery.',
    code: 'TATAHEALTH20',
    discount: '20% OFF',
    minOrder: 'Valid on all medicines',
    validDays: 15,
    partnerUrl: 'https://www.1mg.com',
    logoText: 'TATA 1MG',
  },
  {
    id: 'smartserve-club',
    brand: 'SmartServe',
    brandColor: '#2F5233',
    category: 'home',
    title: '₹75 OFF Your Next Booking',
    description: 'Special loyalty reward for booking via SmartServe. Applies on any catalog category.',
    code: 'SERVE75',
    discount: '₹75 OFF',
    minOrder: 'Valid for 30 days',
    validDays: 30,
    partnerUrl: '/catalog',
    logoText: 'SMARTSERVE',
  },
];

const WHEEL_SECTORS = [
  { label: '₹125 Swiggy', color: '#FC8019', promo: PARTNER_OFFERS[0] },
  { label: '25% Zomato', color: '#E23744', promo: PARTNER_OFFERS[1] },
  { label: '₹100 Blinkit', color: '#EAB308', promo: PARTNER_OFFERS[2] },
  { label: '₹250 Myntra', color: '#EC4899', promo: PARTNER_OFFERS[3] },
  { label: '₹75 SmartServe', color: '#2F5233', promo: PARTNER_OFFERS[5] },
  { label: '20% Tata 1mg', color: '#F97316', promo: PARTNER_OFFERS[4] },
];

interface PostBookingPromotionsProps {
  bookingId?: string;
}

export const PostBookingPromotions: React.FC<PostBookingPromotionsProps> = ({
  bookingId,
}) => {
  const { t } = useTranslation();
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [isSpinning, setIsSpinning] = useState<boolean>(false);
  const [spinDeg, setSpinDeg] = useState<number>(0);
  const [wonPromo, setWonPromo] = useState<PartnerPromo | null>(null);
  const [showWonModal, setShowWonModal] = useState<boolean>(false);
  const [hasSpun, setHasSpun] = useState<boolean>(false);
  const [claimedCodes, setClaimedCodes] = useState<string[]>([]);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // Load previously claimed rewards from localStorage
  useEffect(() => {
    try {
      const stored = localStorage.getItem('smartserve_claimed_promos');
      if (stored) {
        setClaimedCodes(JSON.parse(stored));
      }
      const spunStatus = localStorage.getItem(`smartserve_spun_${bookingId || 'latest'}`);
      if (spunStatus === 'true') {
        setHasSpun(true);
      }
    } catch {
      // fallback safe
    }
  }, [bookingId]);

  // Draw the spin wheel on the HTML5 Canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = Math.min(centerX, centerY) - 8;
    const numSectors = WHEEL_SECTORS.length;
    const sectorAngle = (2 * Math.PI) / numSectors;

    ctx.clearRect(0, 0, width, height);

    WHEEL_SECTORS.forEach((sector, i) => {
      const startAngle = i * sectorAngle;
      const endAngle = startAngle + sectorAngle;

      // Draw wedge
      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, radius, startAngle, endAngle);
      ctx.closePath();
      ctx.fillStyle = sector.color;
      ctx.fill();

      // Border line
      ctx.strokeStyle = '#FAF7F0';
      ctx.lineWidth = 3;
      ctx.stroke();

      // Sector Text
      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.rotate(startAngle + sectorAngle / 2);
      ctx.textAlign = 'right';
      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 12px sans-serif';
      ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
      ctx.shadowBlur = 4;
      ctx.fillText(sector.label, radius - 20, 4);
      ctx.restore();
    });

    // Draw Center Circle Cap
    ctx.beginPath();
    ctx.arc(centerX, centerY, 24, 0, 2 * Math.PI);
    ctx.fillStyle = '#1F2A1E';
    ctx.fill();
    ctx.lineWidth = 4;
    ctx.strokeStyle = '#FAF7F0';
    ctx.stroke();

    // Center star icon
    ctx.fillStyle = '#E5DEC9';
    ctx.font = 'bold 14px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('★', centerX, centerY);
  }, []);

  const handleSpin = () => {
    if (isSpinning || hasSpun) return;
    setIsSpinning(true);

    // Pick a winning sector randomly (0 to 5)
    const winningIndex = Math.floor(Math.random() * WHEEL_SECTORS.length);
    const sectorAngle = 360 / WHEEL_SECTORS.length;
    // Calculate final rotation degrees so arrow at 270 deg (top) points to chosen sector
    const extraRounds = 5 * 360; // 5 full rotations for drama
    const targetSectorOffset = 360 - (winningIndex * sectorAngle + sectorAngle / 2) + 270;
    const totalRotation = extraRounds + targetSectorOffset;

    setSpinDeg(totalRotation);

    setTimeout(async () => {
      setIsSpinning(false);
      setHasSpun(true);
      const wonSector = WHEEL_SECTORS[winningIndex] ?? WHEEL_SECTORS[0]!;
      let won = wonSector.promo;
      if (won) {
        // Mint authentic server-backed coupon record for this customer
        try {
          const res = await apiClient.post('/coupons/spin-reward', {
            reward_tier: won.brand === 'SmartServe' ? 'SERVE75' : 'SERVE50',
            booking_id: bookingId,
          });
          if (res.data?.code) {
            won = {
              ...won,
              code: res.data.code,
              description: res.data.description || won.description,
            };
          }
        } catch (err) {
          console.error('Failed to mint server spin coupon:', err);
        }

        setWonPromo(won);
        setShowWonModal(true);

        // Save to localStorage
        try {
          localStorage.setItem(`smartserve_spun_${bookingId || 'latest'}`, 'true');
          const nextClaimed = Array.from(new Set([...claimedCodes, won.code]));
          setClaimedCodes(nextClaimed);
          localStorage.setItem('smartserve_claimed_promos', JSON.stringify(nextClaimed));
        } catch {
          // storage ignored
        }
      }
    }, 4200);
  };

  const handleCopyCode = (code: string, id: string) => {
    navigator.clipboard.writeText(code);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2500);
  };

  const filteredOffers = selectedCategory === 'all'
    ? PARTNER_OFFERS
    : PARTNER_OFFERS.filter(o => o.category === selectedCategory);

  return (
    <div className="space-y-6 animate-in fade-in duration-300">
      {/* Promotional Section Header */}
      <div className="bg-gradient-to-br from-[#2F5233] via-[#244227] to-[#172B1A] text-[#FAF7F0] p-6 sm:p-8 rounded-[28px] border border-[#3D6B42] shadow-xl relative overflow-hidden">
        {/* Subtle decorative circles */}
        <div className="absolute -top-16 -right-16 w-52 h-52 bg-white/5 rounded-full blur-2xl pointer-events-none" />
        <div className="absolute -bottom-16 -left-16 w-52 h-52 bg-[#E5DEC9]/10 rounded-full blur-2xl pointer-events-none" />

        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-2 max-w-xl">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-[#FAF7F0] text-xs font-bold uppercase tracking-wider">
              <Sparkles className="w-3.5 h-3.5 text-amber-300 animate-spin" />
              <span>{t('promotions.badge', { defaultValue: 'Post-Booking Rewards & Brand Perks' })}</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight font-serif-display text-white">
              {t('promotions.title', { defaultValue: 'Celebrate Your Booking with Partner Offers' })}
            </h2>
            <p className="text-sm text-white/80 leading-relaxed font-sans">
              {t('promotions.subtitle', { 
                defaultValue: 'While our expert is on their way, enjoy exclusive food, dining, grocery, and lifestyle discounts courtesy of our brand partners.' 
              })}
            </p>
          </div>

          <div className="shrink-0 flex items-center gap-3">
            <div className="px-4 py-3 rounded-2xl bg-white/10 backdrop-blur-md border border-white/15 text-center">
              <span className="text-xs uppercase tracking-wider text-white/70 block font-semibold">{t('promotions.vouchers_avail', { defaultValue: 'Active Offers' })}</span>
              <span className="text-2xl font-black font-mono text-white">6 Brand Deals</span>
            </div>
          </div>
        </div>
      </div>

      {/* Grid: Spin The Wheel & Partner Coupon Shelf */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* 1. Spin the Wheel Interactive Card (5 cols) */}
        <div className="lg:col-span-5 bg-white rounded-[28px] border border-[#E5DEC9] p-6 shadow-sm flex flex-col items-center text-center space-y-5">
          <div className="space-y-1">
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 text-amber-800 border border-amber-200 text-xs font-bold uppercase">
              <Trophy className="w-3.5 h-3.5 text-amber-600" />
              <span>{t('promotions.spin_and_win', { defaultValue: 'Spin & Win Reward' })}</span>
            </div>
            <h3 className="text-lg font-bold text-[#1F2A1E]">
              {hasSpun ? t('promotions.spin_completed', { defaultValue: 'Your Reward Is Unlocked!' }) : t('promotions.spin_headline', { defaultValue: 'Try Your Luck on the Partner Wheel' })}
            </h3>
            <p className="text-xs text-[#1F2A1E]/70 max-w-xs">
              {hasSpun 
                ? t('promotions.spin_used_hint', { defaultValue: 'You have claimed your free post-booking spin. Check your voucher code below!' })
                : t('promotions.spin_hint', { defaultValue: 'One free spin per booking. Win verified coupons from Swiggy, Zomato, Blinkit, & Myntra.' })
              }
            </p>
          </div>

          {/* Wheel Visual Container */}
          <div className="relative w-64 h-64 flex items-center justify-center my-2">
            {/* Top Indicator Arrow */}
            <div className="absolute -top-3 z-20 w-0 h-0 border-l-[12px] border-l-transparent border-r-[12px] border-r-transparent border-t-[20px] border-t-rose-600 drop-shadow-md" />

            <div 
              style={{
                transform: `rotate(${spinDeg}deg)`,
                transition: isSpinning ? 'transform 4.2s cubic-bezier(0.15, 0.9, 0.25, 1)' : 'none',
              }}
              className="w-60 h-60 rounded-full shadow-lg border-4 border-white"
            >
              <canvas ref={canvasRef} width={240} height={240} className="w-full h-full rounded-full" />
            </div>
          </div>

          {/* Spin Action CTA */}
          <button
            onClick={handleSpin}
            disabled={isSpinning || hasSpun}
            className={`w-full py-3.5 px-6 rounded-2xl font-bold text-sm tracking-wide uppercase transition-all shadow-md flex items-center justify-center gap-2 ${
              hasSpun
                ? 'bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed'
                : isSpinning
                ? 'bg-amber-500 text-white animate-pulse cursor-wait'
                : 'bg-[#2F5233] hover:bg-[#244227] text-white hover:scale-[1.01] active:scale-[0.99]'
            }`}
          >
            <RotateCw className={`w-4 h-4 ${isSpinning ? 'animate-spin' : ''}`} />
            <span>
              {isSpinning 
                ? t('promotions.spinning', { defaultValue: 'Spinning The Wheel…' })
                : hasSpun
                ? t('promotions.already_spun', { defaultValue: 'Reward Claimed' })
                : t('promotions.spin_now_btn', { defaultValue: 'Spin The Wheel Now' })}
            </span>
          </button>

          {/* Quick Notice */}
          <span className="text-[11px] text-slate-400 font-medium">
            {t('promotions.decoupled_notice', { defaultValue: 'Third-party promotional rewards are separate from service payment & billing.' })}
          </span>
        </div>

        {/* 2. Partner Campaigns & Coupons Shelf (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          {/* Category Filter Pills */}
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
            {[
              { id: 'all', label: 'All Deals', icon: Tag },
              { id: 'food', label: 'Food & Dining', icon: Utensils },
              { id: 'grocery', label: 'Instant Grocery', icon: Zap },
              { id: 'fashion', label: 'Fashion & Lifestyle', icon: ShoppingBag },
              { id: 'health', label: 'Health & Pharmacy', icon: HeartPulse },
            ].map(cat => {
              const Icon = cat.icon;
              const isSelected = selectedCategory === cat.id;
              return (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCategory(cat.id)}
                  className={`px-3.5 py-1.5 rounded-full text-xs font-bold transition-all flex items-center gap-1.5 shrink-0 border ${
                    isSelected
                      ? 'bg-[#2F5233] text-white border-[#2F5233] shadow-xs'
                      : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{cat.label}</span>
                </button>
              );
            })}
          </div>

          {/* Offer Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {filteredOffers.map((offer) => {
              const isCopied = copiedId === offer.id;
              const isClaimed = claimedCodes.includes(offer.code);

              return (
                <div 
                  key={offer.id}
                  className="bg-white rounded-2xl border border-[#E5DEC9] p-4 shadow-2xs hover:shadow-md transition-all flex flex-col justify-between space-y-3 relative overflow-hidden group"
                >
                  {/* Top brand header & discount badge */}
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span 
                        style={{ backgroundColor: `${offer.brandColor}15`, color: offer.brandColor, borderColor: `${offer.brandColor}40` }}
                        className="px-2.5 py-0.5 rounded-md text-[11px] font-black tracking-wider uppercase border"
                      >
                        {offer.brand}
                      </span>
                      <div className="flex items-center gap-1">
                        {isClaimed && (
                          <span className="text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full border border-amber-200">
                            Claimed
                          </span>
                        )}
                        <span className="flex items-center gap-1 text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                          <Flame className="w-3 h-3 text-emerald-600" />
                          <span>{offer.discount}</span>
                        </span>
                      </div>
                    </div>

                    <h4 className="font-bold text-sm text-[#1F2A1E] leading-snug group-hover:text-[#2F5233] transition-colors">
                      {offer.title}
                    </h4>
                    <p className="text-xs text-slate-500 mt-1 line-clamp-2 leading-relaxed">
                      {offer.description}
                    </p>
                  </div>

                  {/* Coupon Code Strip & Copy CTA */}
                  <div className="space-y-2 pt-2 border-t border-slate-100">
                    <div className="flex items-center justify-between gap-2 bg-slate-50 p-2 rounded-xl border border-slate-200/80">
                      <div className="space-y-0.5">
                        <span className="text-[10px] text-slate-400 uppercase tracking-wider font-bold block">Coupon Code</span>
                        <span className="font-mono font-bold text-xs text-slate-900 tracking-wider">
                          {offer.code}
                        </span>
                      </div>
                      <button
                        onClick={() => handleCopyCode(offer.code, offer.id)}
                        className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                          isCopied
                            ? 'bg-emerald-600 text-white'
                            : 'bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 shadow-2xs'
                        }`}
                      >
                        {isCopied ? <Check className="w-3 h-3" /> : <Copy className="w-3 h-3 text-slate-500" />}
                        <span>{isCopied ? 'Copied' : 'Copy'}</span>
                      </button>
                    </div>

                    <div className="flex items-center justify-between text-[11px] text-slate-400">
                      <span>{offer.minOrder}</span>
                      <a 
                        href={offer.partnerUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#2F5233] hover:underline font-bold inline-flex items-center gap-1"
                      >
                        <span>Redeem</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* WINNER CELEBRATION MODAL */}
      {showWonModal && wonPromo && (
        <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 animate-in fade-in">
          <div className="bg-white rounded-[32px] max-w-md w-full p-6 sm:p-8 border border-[#E5DEC9] shadow-2xl text-center space-y-5 relative overflow-hidden animate-in zoom-in-95 duration-200">
            {/* Close button */}
            <button
              onClick={() => setShowWonModal(false)}
              className="absolute top-4 right-4 p-2 rounded-full hover:bg-slate-100 text-slate-400 hover:text-slate-600 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Icon Banner */}
            <div className="w-16 h-16 rounded-2xl bg-amber-500 text-white flex items-center justify-center mx-auto shadow-lg shadow-amber-500/30 animate-bounce">
              <Gift className="w-8 h-8" />
            </div>

            <div className="space-y-1.5">
              <span className="text-xs font-extrabold uppercase tracking-widest text-amber-600">
                Congratulations!
              </span>
              <h3 className="text-2xl font-black text-[#1F2A1E] font-serif-display">
                You Won a {wonPromo.brand} Reward!
              </h3>
              <p className="text-xs text-slate-600 max-w-xs mx-auto">
                {wonPromo.title} — Valid for {wonPromo.validDays} days from today.
              </p>
            </div>

            {/* Voucher Box */}
            <div className="p-4 rounded-2xl bg-slate-50 border-2 border-dashed border-amber-400 space-y-2">
              <span className="text-[11px] text-slate-400 uppercase tracking-wider font-bold block">
                Exclusive Coupon Code
              </span>
              <span className="font-mono text-2xl font-black tracking-widest text-[#1F2A1E]">
                {wonPromo.code}
              </span>
              <p className="text-[11px] text-slate-500">
                {wonPromo.minOrder}
              </p>
            </div>

            {/* Actions */}
            <div className="space-y-2 pt-2">
              <button
                onClick={() => handleCopyCode(wonPromo.code, 'won-modal')}
                className="w-full py-3.5 bg-[#2F5233] hover:bg-[#244227] text-white font-bold text-xs uppercase tracking-wider rounded-2xl shadow-md flex items-center justify-center gap-2 transition-all"
              >
                {copiedId === 'won-modal' ? <Check className="w-4 h-4" /> : <Copy className="w-4 h-4" />}
                <span>{copiedId === 'won-modal' ? 'Copied to Clipboard!' : 'Copy Code & Save'}</span>
              </button>

              <a
                href={wonPromo.partnerUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-3 bg-white hover:bg-slate-50 text-slate-700 font-bold text-xs uppercase tracking-wider rounded-2xl border border-slate-200 inline-flex items-center justify-center gap-1.5 transition-all"
              >
                <span>Visit {wonPromo.brand}</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
