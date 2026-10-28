import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Lock, Mail, ArrowRight, AlertCircle, Eye, EyeOff, Loader2, ShieldCheck, KeyRound, ArrowLeft } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { ProviderLoginVideoCarousel } from '../../components/auth/ProviderLoginVideoCarousel';

export const ProviderLoginView: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [email, setEmail] = useState('demo.provider@smartserve.com');
  const [password, setPassword] = useState('DemoProvider123!');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [forgotSent, setForgotSent] = useState(false);
  const [is2FaRequired, setIs2FaRequired] = useState(false);
  const [twoFactorCode, setTwoFactorCode] = useState('');
  const [isRecoveryMode, setIsRecoveryMode] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!email || !password) {
      setError('Please enter both email and password.');
      return;
    }

    if (is2FaRequired && !twoFactorCode.trim()) {
      setError(isRecoveryMode ? 'Please enter your backup recovery code.' : 'Please enter your 6-digit authenticator code.');
      return;
    }

    setLoading(true);

    try {
      await login(
        email.trim(),
        password,
        is2FaRequired && !isRecoveryMode ? twoFactorCode.trim() : undefined,
        is2FaRequired && isRecoveryMode ? twoFactorCode.trim() : undefined
      );
      // isVerified is updated by AuthContext.login()
      const verified = localStorage.getItem('smartserve_provider_verified');
      if (verified === 'true') {
        navigate('/dashboard');
      } else {
        navigate('/application-status');
      }
    } catch (err: any) {
      const is2FaHeader = err.response?.headers?.['x-2fa-required'] === 'true';
      const detail = err.response?.data?.detail || '';
      const is2FaDetail = typeof detail === 'string' && (detail.includes('Two-factor') || detail.includes('2FA'));

      if (err.response?.status === 401 && (is2FaHeader || is2FaDetail) && !is2FaRequired) {
        setIs2FaRequired(true);
        setError(null);
        return;
      }

      const msg = detail || 'Invalid email or password. Please verify your credentials.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = () => {
    setForgotSent(true);
    setTimeout(() => setForgotSent(false), 5000);
  };

  return (
    <div className="w-screen min-h-screen lg:h-screen flex flex-col lg:flex-row bg-[#FAF7F0] font-sans text-[#1F2A1E] lg:overflow-hidden">
      {/* ══════════════════════════════════════════════════════════════════
          LEFT: COMPACT CINEMATIC VIDEO PANEL (40% Desktop)
          ══════════════════════════════════════════════════════════════════*/}
      <div className="w-full lg:w-[40%] xl:w-[42%] h-[240px] sm:h-[280px] lg:h-full flex-shrink-0">
        <ProviderLoginVideoCarousel />
      </div>

      {/* ══════════════════════════════════════════════════════════════════
          RIGHT: PRIMARY LOGIN PANEL (60% Desktop)
          ══════════════════════════════════════════════════════════════════*/}
      <div className="w-full lg:w-[60%] xl:w-[58%] h-full flex flex-col justify-between p-6 sm:p-10 lg:p-14 xl:p-20 bg-[#FAF7F0] overflow-y-auto">
        {/* Top spacer */}
        <div className="hidden lg:block h-4" />

        {/* ── Central Login Content ── */}
        <div className="w-full max-w-[400px] mx-auto my-auto py-4">
          {/* ── SmartServe Brand Identity ── */}
          <div className="mb-8">
            {/* Authentic SmartServe Logo Emblem + Wordmark */}
            <div className="flex items-center gap-3 mb-6">
              <div className="w-11 h-11 rounded-xl border border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-center shadow-xs p-1">
                <svg className="w-full h-full" viewBox="0 0 96 96" fill="none">
                  <path
                    d="M 48 6 L 72 6 A 18 18 0 0 1 90 24 L 90 72 A 18 18 0 0 1 72 90 L 24 90 A 18 18 0 0 1 6 72 L 6 24 A 18 18 0 0 1 24 6 L 48 6 Z"
                    stroke="#C9A15A"
                    strokeWidth={2.5}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    fill="none"
                  />
                  <path
                    d="M 62 30 C 62 23, 34 22, 34 38 C 34 54, 62 48, 62 64 C 62 80, 34 78, 34 70"
                    stroke="#2F5233"
                    strokeWidth={7}
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    fill="none"
                  />
                </svg>
              </div>
              <div>
                <div className="flex items-baseline font-serif">
                  <span className="text-xl font-bold text-[#2F5233] tracking-tight">Smart</span>
                  <span className="text-xl font-bold text-[#C9A15A] tracking-tight ml-0.5">Serve</span>
                  <span className="ml-2 px-2 py-0.5 rounded-full bg-[#FAF7F0] text-[#2F5233] text-[10px] font-sans font-bold border border-[#E5DEC9]">
                    PARTNER
                  </span>
                </div>
              </div>
            </div>

            {/* Page Title */}
            <h1 className="text-2xl sm:text-3xl font-bold text-[#1F2A1E] tracking-tight mb-1.5 font-serif">
              {is2FaRequired ? 'Partner Two-Factor Verification' : 'Service Partner Login'}
            </h1>
            <p className="text-sm text-[#1F2A1E]/60 font-medium">
              {is2FaRequired
                ? (isRecoveryMode
                    ? 'Enter your single-use backup recovery code.'
                    : 'Enter the 6-digit code from your authenticator app.')
                : 'Sign in to manage your bookings, catalog services, and availability.'}
            </p>
          </div>

          {/* ── Error Notification ── */}
          {error && (
            <div className="mb-5 flex items-start gap-3 p-3.5 bg-red-50 border border-red-200/80 rounded-xl text-red-800 text-xs sm:text-sm font-medium animate-in fade-in">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-600 mt-0.5" />
              <span className="flex-1">{error}</span>
            </div>
          )}

          {/* ── Forgot Password Notification ── */}
          {forgotSent && (
            <div className="mb-5 p-3.5 bg-[#F2EDE1] border border-[#C9A15A]/30 rounded-xl text-[#1F2A1E] text-xs sm:text-sm font-medium animate-in fade-in text-center">
              Password reset instructions sent to your registered partner email.
            </div>
          )}

          {/* ── Login Form ── */}
          <form onSubmit={handleSubmit} className="space-y-4">
            {!is2FaRequired ? (
              <>
                {/* Demo Credentials Helper Card */}
                <div className="p-3 bg-amber-50/90 border border-amber-200/90 rounded-xl text-xs flex items-center justify-between gap-3 shadow-xs">
                  <div className="min-w-0">
                    <div className="font-bold flex items-center gap-1.5 text-amber-900">
                      <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                      <span>Demo Partner</span>
                    </div>
                    <div className="text-[11px] text-amber-800/90 font-mono truncate mt-0.5">
                      demo.provider@smartserve.com
                    </div>
                  </div>
                  <div className="flex items-center gap-1.5 shrink-0">
                    <button
                      type="button"
                      onClick={() => {
                        setEmail('demo.provider@smartserve.com');
                        setPassword('DemoProvider123!');
                        setError(null);
                      }}
                      className="px-2.5 py-1.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-semibold rounded-lg text-xs transition-colors shadow-xs cursor-pointer"
                    >
                      Prefill Demo
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setEmail('rajesh.sharma@smartserve.com');
                        setPassword('ProviderPassword123!');
                        setError(null);
                      }}
                      className="px-2 py-1.5 bg-white border border-[#E5DEC9] hover:bg-neutral-50 text-[#1F2A1E] font-medium rounded-lg text-xs transition-colors shadow-xs cursor-pointer"
                      title="Prefill Rajesh Sharma"
                    >
                      Rajesh
                    </button>
                  </div>
                </div>

                {/* Email Address */}
                <div>
                  <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">
                    Partner Email Address
                  </label>
                  <div className="relative">
                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="e.g. rajesh.sharma@smartserve.com"
                      required
                      className="w-full bg-[#F2EDE1]/50 border border-[#E5DEC9] rounded-xl px-4 py-3 pl-10 text-sm focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all font-medium placeholder:text-[#1F2A1E]/35"
                    />
                    <Mail className="w-4 h-4 text-[#1F2A1E]/40 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                  </div>
                </div>

                {/* Password */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider">
                      Account Password
                    </label>
                    <button
                      type="button"
                      onClick={handleForgotPassword}
                      className="text-xs font-semibold text-[#2F5233] hover:underline"
                    >
                      Forgot password?
                    </button>
                  </div>
                  <div className="relative">
                    <input
                      type={showPassword ? 'text' : 'password'}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter partner password"
                      required
                      className="w-full bg-[#F2EDE1]/50 border border-[#E5DEC9] rounded-xl px-4 py-3 pl-10 pr-10 text-sm focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all font-medium placeholder:text-[#1F2A1E]/35"
                    />
                    <Lock className="w-4 h-4 text-[#1F2A1E]/40 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/40 hover:text-[#1F2A1E]/70 transition-colors p-1"
                      aria-label={showPassword ? 'Hide password' : 'Show password'}
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>
              </>
            ) : (
              <>
                {/* 2FA Input Field */}
                <div>
                  <div className="flex items-center justify-between mb-1.5">
                    <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider">
                      {isRecoveryMode ? 'Backup Recovery Code' : '6-Digit TOTP Authenticator Code'}
                    </label>
                    <button
                      type="button"
                      onClick={() => {
                        setIsRecoveryMode(!isRecoveryMode);
                        setTwoFactorCode('');
                        setError(null);
                      }}
                      className="text-xs font-semibold text-[#2F5233] hover:underline cursor-pointer"
                    >
                      {isRecoveryMode ? 'Use Authenticator Code' : 'Use Recovery Code'}
                    </button>
                  </div>
                  <div className="relative">
                    {isRecoveryMode ? (
                      <KeyRound className="w-4 h-4 text-[#1F2A1E]/40 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                    ) : (
                      <ShieldCheck className="w-4 h-4 text-[#1F2A1E]/40 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                    )}
                    <input
                      type="text"
                      autoFocus
                      maxLength={isRecoveryMode ? 20 : 6}
                      value={twoFactorCode}
                      onChange={(e) => setTwoFactorCode(e.target.value)}
                      placeholder={isRecoveryMode ? 'XXXX-XXXX' : '123456'}
                      required
                      className="w-full bg-[#F2EDE1]/50 border border-[#E5DEC9] rounded-xl px-4 py-3 pl-10 text-base font-mono tracking-widest focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all font-medium placeholder:text-[#1F2A1E]/35"
                    />
                  </div>
                </div>

                <div className="flex items-center justify-between pt-1">
                  <button
                    type="button"
                    onClick={() => {
                      setIs2FaRequired(false);
                      setTwoFactorCode('');
                      setError(null);
                    }}
                    className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#1F2A1E]/60 hover:text-[#1F2A1E] transition-colors cursor-pointer"
                  >
                    <ArrowLeft className="w-3.5 h-3.5" />
                    Back to credentials
                  </button>
                </div>
              </>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 px-4 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold text-sm rounded-xl shadow-xs transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50 mt-2"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>{is2FaRequired ? 'Verifying...' : 'Signing in to Partner Portal...'}</span>
                </>
              ) : (
                <>
                  <span>{is2FaRequired ? 'Verify & Access Partner Portal' : 'Sign In to Partner Portal'}</span>
                  <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </form>

          {/* Quick Demo Credentials Helper */}
          <div 
            onClick={() => {
              setEmail('rajesh.sharma@smartserve.com');
              setPassword('ProviderPass123!');
              setError(null);
            }}
            className="mt-6 p-3.5 bg-white hover:bg-[#FAF7F0] transition-colors rounded-2xl border border-[#E5DEC9] text-xs cursor-pointer group"
            title="Click to autofill demo credentials"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-bold text-[#1F2A1E]/70 uppercase tracking-wider text-[10px]">Verified Partner Demo Login</span>
              <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200 group-hover:bg-emerald-100 transition-colors">Click to Auto-fill</span>
            </div>
            <p className="text-[11px] text-[#1F2A1E]/60 font-mono">rajesh.sharma@smartserve.com / ProviderPass123!</p>
          </div>

          {/* Sign Up / Become a Partner Link */}
          <div className="mt-6 text-center">
            <p className="text-xs text-[#1F2A1E]/65 font-medium">
              Want to become a service partner?{' '}
              <Link to="/onboarding" className="font-bold text-[#2F5233] hover:underline">
                Send Your Documents for Approval →
              </Link>
            </p>
          </div>
        </div>

        {/* ── Footer / Copyright ── */}
        <div className="w-full max-w-[400px] mx-auto text-center pt-4">
          <p className="text-[11px] text-[#1F2A1E]/40 font-medium">
            SmartServe Partner Platform &copy; {new Date().getFullYear()}. All rights reserved.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProviderLoginView;
