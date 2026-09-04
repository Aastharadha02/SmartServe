import { FC, ReactNode } from 'react';
import { Sparkles, CheckCircle2 } from 'lucide-react';

export interface AuthLayoutProps {
  children: ReactNode;
}

export const AuthLayout: FC<AuthLayoutProps> = ({ children }) => {
  return (
    <div className="w-screen min-h-screen lg:h-screen lg:overflow-hidden flex flex-col lg:flex-row bg-white font-sans text-slate-800">
      {/* LEFT HALF: BRANDING & PRODUCT VISUAL */}
      <div className="w-full lg:w-[46%] xl:w-[44%] h-auto lg:h-full bg-gradient-to-br from-[#0A1128] via-[#0F1D40] to-[#0B132B] text-white p-8 sm:p-12 lg:p-14 xl:p-20 flex flex-col justify-between relative overflow-hidden flex-shrink-0">
        <div className="absolute -top-24 -left-24 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl pointer-events-none" />

        {/* Top Logo */}
        <div className="relative z-10 flex items-center gap-3.5">
          <div className="w-11 h-11 rounded-2xl bg-[#2563EB] flex items-center justify-center text-white font-black text-2xl shadow-sm flex-shrink-0">
            S
          </div>
          <div>
            <h1 className="font-extrabold text-white text-xl tracking-tight leading-tight">SmartServe</h1>
            <span className="text-[11px] font-bold text-blue-300 uppercase tracking-wider block">
              Customer Portal
            </span>
          </div>
        </div>

        {/* Center Hero Message & Value Points */}
        <div className="relative z-10 space-y-5 my-8 lg:my-auto max-w-xl">
          <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" />
            Verified Home Services
          </span>

          <h2 className="text-3xl sm:text-4xl xl:text-5xl font-extrabold text-white tracking-tight leading-[1.15]">
            Book Top-Rated Local Experts in Seconds.
          </h2>

          <p className="text-sm sm:text-base text-slate-300 font-normal leading-relaxed">
            Your single destination for home repairs, cleaning, appliance care, and professional wellness services across India.
          </p>

          <div className="space-y-3 pt-2 text-sm text-slate-200">
            <div className="flex items-center gap-3">
              <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="font-medium">100% Background-Verified Professionals</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="font-medium">Upfront Fixed Pricing & Service Guarantee</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="font-medium">24/7 In-App Customer Support & Tracking</span>
            </div>
          </div>
        </div>

        {/* Bottom Status Footer */}
        <div className="relative z-10 pt-6 border-t border-white/10 flex items-center justify-between text-xs text-slate-400">
          <span>SmartServe Customer v1.0</span>
          <span className="font-mono text-blue-300">Secure Cloud Connected</span>
        </div>
      </div>

      {/* RIGHT HALF: FORM CONTENT */}
      <div className="w-full lg:w-[54%] xl:w-[56%] min-h-full flex items-center justify-center p-6 sm:p-12 lg:p-16 xl:p-24 bg-white lg:bg-[#FDFDFC] overflow-y-auto">
        <div className="w-full max-w-[500px]">
          {children}
        </div>
      </div>
    </div>
  );
};

