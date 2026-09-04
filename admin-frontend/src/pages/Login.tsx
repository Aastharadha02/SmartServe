import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Lock, Mail, Loader2, ShieldCheck, AlertCircle, Sparkles, CheckCircle2 } from 'lucide-react';
import { loginAdmin } from '../api/auth';
import { CATEGORY_IMAGE_MAP } from '../utils/serviceImages';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('admin@smartserve.com');
  const [password, setPassword] = useState('AdminPassword123!');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showEntrance, setShowEntrance] = useState(false);

  useEffect(() => {
    const handleTransition = () => {
      setShowEntrance(true);
    };

    window.addEventListener('smartserve:splash-transition-start', handleTransition);

    // Failsafe timer: if no transition event received, reveal normally after delay
    const failsafe = setTimeout(() => {
      setShowEntrance(true);
    }, 5500);

    return () => {
      window.removeEventListener('smartserve:splash-transition-start', handleTransition);
      clearTimeout(failsafe);
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!email || !password) {
      setErrorMessage('Please enter both email and password.');
      return;
    }

    setLoading(true);
    try {
      const data = await loginAdmin({ email, password });
      
      // Store JWT token & admin user info for the session
      localStorage.setItem('smartserve_token', data.access_token);
      localStorage.setItem(
        'smartserve_user',
        JSON.stringify({
          user_id: data.user_id,
          email: data.email,
          role: data.role,
          permissions: data.permissions,
        })
      );

      // Redirect based on user role
      if (data.role === 'customer') {
        navigate('/customer');
      } else {
        navigate('/admin/dashboard');
      }
    } catch (err: any) {
      if (err.response) {
        if (err.response.status === 401) {
          setErrorMessage('Invalid admin email or password.');
        } else if (err.response.status === 403) {
          setErrorMessage('Admin account is suspended.');
        } else {
          setErrorMessage(err.response.data?.detail || 'Authentication failed. Please check your credentials.');
        }
      } else if (err.request) {
        setErrorMessage('Unable to connect to SmartServe API. Please verify network connectivity and backend server availability.');
      } else {
        setErrorMessage('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-screen min-h-screen lg:h-screen lg:overflow-hidden flex flex-col lg:flex-row bg-white font-sans text-slate-800">
      
      {/* ══════════════════════════════════════════════════════════════════
          LEFT HALF: BRANDING & PRODUCT VISUAL (FULL HEIGHT & WIDTH 45-48%)
          ══════════════════════════════════════════════════════════════════*/}
      <div className={`w-full lg:w-[46%] xl:w-[44%] h-auto lg:h-full bg-gradient-to-br from-[#0A1128] via-[#0F1D40] to-[#0B132B] text-white p-8 sm:p-12 lg:p-14 xl:p-20 flex flex-col justify-between relative overflow-hidden flex-shrink-0 ${showEntrance ? 'animate-login-left-panel' : 'opacity-0'}`}>
        
        {/* Subtle Architectural Ambient Visual */}
        <div className="absolute inset-0 opacity-15 pointer-events-none">
          <img
            src={CATEGORY_IMAGE_MAP['Cleaning']}
            alt="SmartServe Brand"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-[#0A1128] via-[#0F1D40]/90 to-transparent"></div>
        </div>

        {/* Ambient Top Glow */}
        <div className="absolute -top-24 -left-24 w-96 h-96 bg-blue-500/20 rounded-full blur-3xl pointer-events-none"></div>

        {/* Top Logo */}
        <div className="relative z-10 flex items-center gap-3.5">
          <div className="w-11 h-11 rounded-2xl bg-[#2563EB] flex items-center justify-center text-white font-black text-2xl shadow-sm flex-shrink-0">
            S
          </div>
          <div>
            <h1 className="font-extrabold text-white text-xl tracking-tight leading-tight">SmartServe</h1>
            <span className="text-[11px] font-bold text-blue-300 uppercase tracking-wider block">
              Marketplace Operations Console
            </span>
          </div>
        </div>

        {/* Center Hero Message & Value Points */}
        <div className="relative z-10 space-y-5 my-8 lg:my-auto max-w-xl">
          <span className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/20 text-blue-300 border border-blue-400/30 text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" />
            Enterprise Control Tower
          </span>

          <h2 className="text-3xl sm:text-4xl xl:text-5xl font-extrabold text-white tracking-tight leading-[1.15]">
            Empowering On-Demand Home Services Across India.
          </h2>

          <p className="text-sm sm:text-base text-slate-300 font-normal leading-relaxed">
            Unified operations console for service catalog management, dynamic surge pricing, real-time emergency dispatch, and workforce compliance.
          </p>

          <div className="space-y-3 pt-2 text-sm text-slate-200">
            <div className="flex items-center gap-3">
              <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="font-medium">100% Verified Local Service Professionals</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="font-medium">Transparent Fixed-Scope Pricing in ₹</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center flex-shrink-0">
                <CheckCircle2 className="w-4 h-4" />
              </div>
              <span className="font-medium">Enterprise RBAC Security & Audit Trail</span>
            </div>
          </div>
        </div>

        {/* Bottom Status Footer */}
        <div className="relative z-10 pt-6 border-t border-white/10 flex items-center justify-between text-xs text-slate-400">
          <span>SmartServe Pro v1.0</span>
          <span className="font-mono text-blue-300">FastAPI & Neon Cloud Connected</span>
        </div>
      </div>

      {/* ══════════════════════════════════════════════════════════════════
          RIGHT HALF: FULL-SCREEN LOGIN FORM (NO CARD BORDERS / 52-56% WIDTH)
          ══════════════════════════════════════════════════════════════════*/}
      <div className="w-full lg:w-[54%] xl:w-[56%] h-full flex items-center justify-center p-6 sm:p-12 lg:p-16 xl:p-24 bg-white lg:bg-[#FDFDFC]">
        <div className={`w-full max-w-[500px] space-y-7 ${showEntrance ? 'animate-login-card' : 'opacity-0'}`}>
          
          {/* Brand Header on Right */}
          <div className="space-y-2.5">
            <div className={`inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-blue-50 text-[#2563EB] font-black text-2xl mb-1 shadow-2xs ${showEntrance ? 'animate-login-item-1' : 'opacity-0'}`}>
              S
            </div>
            <h2 className={`text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight ${showEntrance ? 'animate-login-item-2' : 'opacity-0'}`}>
              SmartServe Admin
            </h2>
            <p className={`text-base text-slate-500 font-medium ${showEntrance ? 'animate-login-item-3' : 'opacity-0'}`}>
              Sign in to access your administrative operations console.
            </p>
          </div>

          {/* Error Alert */}
          {errorMessage && (
            <div className="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-2xl text-red-700 text-sm font-semibold animate-in fade-in">
              <AlertCircle className="w-5 h-5 flex-shrink-0 text-red-500 mt-0.5" />
              <div className="flex-1">{errorMessage}</div>
            </div>
          )}

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Email Field */}
            <div className={showEntrance ? 'animate-login-item-4' : 'opacity-0'}>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                Admin Email
              </label>
              <div className="relative">
                <Mail className="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="admin@smartserve.com"
                  className="w-full h-14 bg-slate-50/80 border border-slate-200/90 rounded-xl pl-12 pr-4 text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/25 focus:border-[#2563EB] focus:bg-white transition-all"
                  required
                  disabled={loading}
                />
              </div>
            </div>

            {/* Password Field */}
            <div className={showEntrance ? 'animate-login-item-5' : 'opacity-0'}>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="w-full h-14 bg-slate-50/80 border border-slate-200/90 rounded-xl pl-12 pr-12 text-base font-medium text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#2563EB]/25 focus:border-[#2563EB] focus:bg-white transition-all"
                  required
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 focus:outline-none p-1"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Submit Button */}
            <div className={showEntrance ? 'animate-login-item-6' : 'opacity-0'}>
              <button
                type="submit"
                disabled={loading}
                className="w-full h-14 flex items-center justify-center gap-2.5 bg-[#2563EB] hover:bg-blue-700 text-white font-bold rounded-xl text-base shadow-sm hover:shadow transition-all disabled:opacity-70 disabled:cursor-not-allowed mt-2"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    <span>Authenticating Session...</span>
                  </>
                ) : (
                  <>
                    <ShieldCheck className="w-5 h-5" />
                    <span>Sign In to Admin Console</span>
                  </>
                )}
              </button>
            </div>
          </form>

          {/* Security Footer Note */}
          <div className={`pt-4 border-t border-slate-100 text-center text-xs text-slate-400 font-medium ${showEntrance ? 'animate-login-item-7' : 'opacity-0'}`}>
            Protected by SmartServe RBAC Authorization & Audit Engine
          </div>

        </div>
      </div>

    </div>
  );
};

export default Login;
