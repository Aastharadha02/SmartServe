import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Eye, EyeOff, Lock, Mail, Loader2, AlertCircle, ShieldCheck, KeyRound, ArrowLeft, CheckCircle2 } from 'lucide-react';
import { useAuth } from '../../auth/useAuth';
import { useToast } from '../../hooks/useToast';
import { CustomerLoginVideoCarousel } from '../../components/auth/CustomerLoginVideoCarousel';
import { forgotPassword } from '../../api/auth';

export const CustomerLogin: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const { showToast } = useToast();

  const [email, setEmail] = useState('demo.customer@smartserve.com');
  const [password, setPassword] = useState('DemoCustomer123!');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [is2FaRequired, setIs2FaRequired] = useState(false);
  const [twoFactorCode, setTwoFactorCode] = useState('');
  const [isRecoveryMode, setIsRecoveryMode] = useState(false);

  // Forgot password workflow state
  const [isForgotMode, setIsForgotMode] = useState(false);
  const [forgotEmail, setForgotEmail] = useState('');
  const [forgotLoading, setForgotLoading] = useState(false);
  const [forgotSubmitted, setForgotSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!email || !password) {
      setErrorMessage('Please enter both email and password.');
      return;
    }

    if (is2FaRequired && !twoFactorCode.trim()) {
      setErrorMessage(isRecoveryMode ? 'Please enter your recovery code.' : 'Please enter your 6-digit authenticator code.');
      return;
    }

    setLoading(true);
    try {
      await login({
        email: email.trim(),
        password,
        ...(is2FaRequired && !isRecoveryMode ? { totp_code: twoFactorCode.trim() } : {}),
        ...(is2FaRequired && isRecoveryMode ? { recovery_code: twoFactorCode.trim() } : {}),
      });
      showToast('Welcome back to SmartServe!', 'success');
      navigate('/home', { replace: true });
    } catch (err: any) {
      if (err.response) {
        const is2FaHeader = err.response.headers?.['x-2fa-required'] === 'true';
        const detail = err.response.data?.detail || '';
        const is2FaDetail = typeof detail === 'string' && (detail.includes('Two-factor') || detail.includes('2FA'));

        if (err.response.status === 401 && (is2FaHeader || is2FaDetail) && !is2FaRequired) {
          setIs2FaRequired(true);
          setErrorMessage(null);
          return;
        }

        if (err.response.status === 401) {
          if (is2FaRequired) {
            setErrorMessage(detail || 'Invalid two-factor authentication code.');
          } else {
            setErrorMessage('Invalid email or password. Please try again.');
          }
        } else {
          setErrorMessage(detail || 'Authentication failed. Please check your credentials.');
        }
      } else if (err.request) {
        setErrorMessage('Unable to connect to SmartServe API. Please verify backend server availability.');
      } else {
        setErrorMessage('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!forgotEmail.trim()) {
      setErrorMessage('Please enter your email address.');
      return;
    }
    setErrorMessage(null);
    setForgotLoading(true);
    try {
      await forgotPassword(forgotEmail.trim().toLowerCase());
      setForgotSubmitted(true);
    } catch {
      // Anti-enumeration: always display positive confirmation
      setForgotSubmitted(true);
    } finally {
      setForgotLoading(false);
    }
  };

  return (
    <div className="w-screen min-h-screen lg:h-screen flex flex-col lg:flex-row bg-[#FAF7F0] font-sans text-[#1F2A1E] lg:overflow-hidden">
      
      {/* ══════════════════════════════════════════════════════════════════
          LEFT: COMPACT CINEMATIC VIDEO PANEL (Matching Admin Exactly)
          ══════════════════════════════════════════════════════════════════*/}
      <div className="w-full lg:w-[40%] xl:w-[42%] h-[240px] sm:h-[280px] lg:h-full flex-shrink-0">
        <CustomerLoginVideoCarousel />
      </div>

      {/* ══════════════════════════════════════════════════════════════════
          RIGHT: PRIMARY LOGIN PANEL (Matching Admin Design System)
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
                </div>
              </div>
            </div>

            {/* Page Title */}
            <h1 className="text-2xl sm:text-3xl font-bold text-[#1F2A1E] tracking-tight mb-1.5">
              {isForgotMode
                ? 'Forgot Password'
                : is2FaRequired
                ? 'Two-Factor Verification'
                : 'Customer Login'}
            </h1>
            <p className="text-sm text-[#1F2A1E]/60 font-medium">
              {isForgotMode
                ? 'Enter your registered email address to receive password reset instructions.'
                : is2FaRequired
                ? isRecoveryMode
                  ? 'Enter your single-use backup recovery code.'
                  : 'Enter the 6-digit code from your authenticator app.'
                : 'Sign in to book and manage your home services.'}
            </p>
          </div>

          {/* ── Error Notification ── */}
          {errorMessage && (
            <div className="mb-5 flex items-start gap-3 p-3.5 bg-red-50 border border-red-200/80 rounded-xl text-red-800 text-xs sm:text-sm font-medium animate-in fade-in">
              <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-600 mt-0.5" />
              <span className="flex-1">{errorMessage}</span>
            </div>
          )}

          {isForgotMode ? (
            /* ── Forgot Password Form ── */
            <form onSubmit={handleForgotPasswordSubmit} className="space-y-5">
              {forgotSubmitted ? (
                <div className="space-y-4 py-2">
                  <div className="p-4 bg-[#F2EDE1] border border-[#C9A15A]/30 rounded-xl text-[#1F2A1E] text-xs sm:text-sm font-medium space-y-2">
                    <div className="flex items-center gap-2 font-bold text-[#2F5233]">
                      <CheckCircle2 className="w-5 h-5 text-emerald-600 flex-shrink-0" />
                      <span>Reset Instructions Sent</span>
                    </div>
                    <p className="text-[#1F2A1E]/80">
                      If an account exists for <span className="font-semibold text-[#1F2A1E]">{forgotEmail}</span>, a secure single-use password reset link has been dispatched. Please check your inbox.
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => {
                      setIsForgotMode(false);
                      setForgotSubmitted(false);
                      setErrorMessage(null);
                    }}
                    className="w-full h-11 flex items-center justify-center gap-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-sm transition-all cursor-pointer"
                  >
                    Return to Sign In
                  </button>
                </div>
              ) : (
                <>
                  <div>
                    <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">
                      Email Address
                    </label>
                    <div className="relative">
                      <Mail className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                      <input
                        type="email"
                        value={forgotEmail}
                        onChange={(e) => setForgotEmail(e.target.value)}
                        placeholder="customer@example.com"
                        className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                        required
                        disabled={forgotLoading}
                      />
                    </div>
                  </div>

                  <div className="pt-1">
                    <button
                      type="submit"
                      disabled={forgotLoading}
                      className="w-full h-12 flex items-center justify-center gap-2 bg-[#2F5233] hover:bg-[#3D6B42] active:bg-[#244227] text-white font-bold rounded-xl text-sm shadow-xs hover:shadow transition-all disabled:opacity-70 disabled:cursor-not-allowed cursor-pointer"
                    >
                      {forgotLoading ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin" />
                          <span>Sending Instructions...</span>
                        </>
                      ) : (
                        <span>Send Reset Link</span>
                      )}
                    </button>
                  </div>

                  <div className="text-center pt-2">
                    <button
                      type="button"
                      onClick={() => {
                        setIsForgotMode(false);
                        setErrorMessage(null);
                      }}
                      className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#2F5233] hover:text-[#3D6B42] hover:underline transition-colors cursor-pointer"
                    >
                      <ArrowLeft className="w-3.5 h-3.5" />
                      Back to Sign In
                    </button>
                  </div>
                </>
              )}
            </form>
          ) : (
            /* ── Login Form ── */
            <form onSubmit={handleSubmit} className="space-y-5">
              {!is2FaRequired ? (
                <>
                  {/* Demo Credentials Helper Card */}
                  <div className="p-3 bg-amber-50/90 border border-amber-200/90 rounded-xl text-xs flex items-center justify-between gap-3 shadow-xs">
                    <div className="min-w-0">
                      <div className="font-bold flex items-center gap-1.5 text-amber-900">
                        <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                        <span>Demo Customer</span>
                      </div>
                      <div className="text-[11px] text-amber-800/90 font-mono truncate mt-0.5">
                        demo.customer@smartserve.com
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        setEmail('demo.customer@smartserve.com');
                        setPassword('DemoCustomer123!');
                        setErrorMessage(null);
                      }}
                      className="px-3 py-1.5 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-semibold rounded-lg text-xs transition-colors shrink-0 shadow-xs cursor-pointer"
                    >
                      Prefill Demo
                    </button>
                  </div>

                  {/* Email Address */}
                  <div>
                    <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">
                      Email Address
                    </label>
                    <div className="relative">
                      <Mail className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                      <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="customer@example.com"
                        className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                        required
                        disabled={loading}
                      />
                    </div>
                  </div>

                  {/* Password */}
                  <div>
                    <div className="flex items-center justify-between mb-1.5">
                      <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider">
                        Password
                      </label>
                      <button
                        type="button"
                        onClick={() => {
                          setIsForgotMode(true);
                          setForgotEmail(email);
                          setErrorMessage(null);
                          setForgotSubmitted(false);
                        }}
                        className="text-xs font-semibold text-[#2F5233] hover:text-[#3D6B42] hover:underline transition-colors cursor-pointer"
                      >
                        Forgot Password?
                      </button>
                    </div>
                    <div className="relative">
                      <Lock className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                      <input
                        type={showPassword ? 'text' : 'password'}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••••••"
                        className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-11 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                        required
                        disabled={loading}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/35 hover:text-[#1F2A1E]/70 focus:outline-none p-0.5 cursor-pointer transition-colors"
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
                        {isRecoveryMode ? 'Recovery Code' : '6-Digit TOTP Code'}
                      </label>
                      <button
                        type="button"
                        onClick={() => {
                          setIsRecoveryMode(!isRecoveryMode);
                          setTwoFactorCode('');
                          setErrorMessage(null);
                        }}
                        className="text-xs font-semibold text-[#2F5233] hover:text-[#3D6B42] hover:underline transition-colors cursor-pointer"
                      >
                        {isRecoveryMode ? 'Use Authenticator Code' : 'Use Recovery Code'}
                      </button>
                    </div>
                    <div className="relative">
                      {isRecoveryMode ? (
                        <KeyRound className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                      ) : (
                        <ShieldCheck className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                      )}
                      <input
                        type="text"
                        autoFocus
                        maxLength={isRecoveryMode ? 20 : 6}
                        value={twoFactorCode}
                        onChange={(e) => setTwoFactorCode(e.target.value)}
                        placeholder={isRecoveryMode ? 'XXXX-XXXX' : '123456'}
                        className="w-full h-12 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-4 text-base font-mono tracking-widest text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                        required
                        disabled={loading}
                      />
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <button
                      type="button"
                      onClick={() => {
                        setIs2FaRequired(false);
                        setTwoFactorCode('');
                        setErrorMessage(null);
                      }}
                      className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#1F2A1E]/60 hover:text-[#1F2A1E] transition-colors cursor-pointer"
                    >
                      <ArrowLeft className="w-3.5 h-3.5" />
                      Back to credentials
                    </button>
                  </div>
                </>
              )}

              {/* Login Button */}
              <div className="pt-1">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full h-12 flex items-center justify-center gap-2 bg-[#2F5233] hover:bg-[#3D6B42] active:bg-[#244227] text-white font-bold rounded-xl text-sm shadow-xs hover:shadow transition-all disabled:opacity-70 disabled:cursor-not-allowed cursor-pointer"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Verifying...</span>
                    </>
                  ) : (
                    <span>{is2FaRequired ? 'Verify & Sign In' : 'Login to SmartServe'}</span>
                  )}
                </button>
              </div>

              {/* Sign Up Link */}
              <div className="text-center pt-2 text-xs text-[#1F2A1E]/70 font-medium">
                Don't have an account?{' '}
                <Link to="/register" className="font-bold text-[#2F5233] hover:text-[#3D6B42] hover:underline transition-colors">
                  Sign Up
                </Link>
              </div>
            </form>
          )}

        </div>

        {/* ── Minimal Footer (Matching Admin) ── */}
        <div className="text-center pt-4 pb-1">
          <p className="text-[11px] font-medium text-[#1F2A1E]/40">
            SmartServe Marketplace · Verified Home & Urban Services
          </p>
        </div>

      </div>

    </div>
  );
};

export default CustomerLogin;
