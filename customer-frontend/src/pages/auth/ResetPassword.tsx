import React, { useState } from 'react';
import { useSearchParams, useNavigate, Link } from 'react-router-dom';
import { Lock, Eye, EyeOff, Loader2, AlertCircle, CheckCircle2, ArrowLeft } from 'lucide-react';
import { resetPassword } from '../../api/auth';
import { useToast } from '../../hooks/useToast';

export const ResetPassword: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { showToast } = useToast();

  const token = searchParams.get('token') || '';

  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);

    if (!token.trim()) {
      setErrorMessage('Missing password reset token. Please request a new reset link.');
      return;
    }

    if (password.length < 8) {
      setErrorMessage('Password must be at least 8 characters long.');
      return;
    }

    if (password !== confirmPassword) {
      setErrorMessage('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await resetPassword(token.trim(), password);
      setSuccess(true);
      showToast('Password changed successfully! You can now sign in.', 'success');
      setTimeout(() => {
        navigate('/login', { replace: true });
      }, 2000);
    } catch (err: any) {
      const detail = err.response?.data?.detail || 'Password reset token is invalid or has expired.';
      setErrorMessage(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#FAF7F0] font-sans text-[#1F2A1E] flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-white border border-[#E5DEC9] rounded-2xl p-8 shadow-sm">
        
        {/* Brand Header */}
        <div className="flex items-center gap-3 mb-6 justify-center">
          <div className="w-10 h-10 rounded-xl border border-[#E5DEC9] bg-[#FAF7F0] flex items-center justify-center p-1">
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
          <div className="flex items-baseline font-serif">
            <span className="text-xl font-bold text-[#2F5233] tracking-tight">Smart</span>
            <span className="text-xl font-bold text-[#C9A15A] tracking-tight ml-0.5">Serve</span>
          </div>
        </div>

        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-[#1F2A1E] tracking-tight mb-1.5">
            Create New Password
          </h1>
          <p className="text-xs text-[#1F2A1E]/60 font-medium">
            Enter your new secure password below to regain access to your account.
          </p>
        </div>

        {/* Error notification */}
        {errorMessage && (
          <div className="mb-5 flex items-start gap-3 p-3.5 bg-red-50 border border-red-200/80 rounded-xl text-red-800 text-xs font-medium animate-in fade-in">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-600 mt-0.5" />
            <span className="flex-1">{errorMessage}</span>
          </div>
        )}

        {/* Success notification */}
        {success ? (
          <div className="py-6 text-center space-y-4">
            <CheckCircle2 className="w-12 h-12 text-emerald-600 mx-auto" />
            <h2 className="text-lg font-bold text-[#1F2A1E]">Password Reset Successful!</h2>
            <p className="text-xs text-[#1F2A1E]/70">
              Your password has been securely updated and previous sessions have been revoked. Redirecting you to login...
            </p>
            <div className="pt-3">
              <Link
                to="/login"
                className="w-full inline-flex items-center justify-center gap-2 h-11 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-sm transition-all"
              >
                Sign In Now
              </Link>
            </div>
          </div>
        ) : !token ? (
          <div className="py-6 text-center space-y-4">
            <div className="w-12 h-12 bg-amber-50 border border-amber-200 rounded-full flex items-center justify-center mx-auto text-amber-700">
              <AlertCircle className="w-6 h-6" />
            </div>
            <h2 className="text-base font-bold text-[#1F2A1E]">Invalid or Missing Reset Link</h2>
            <p className="text-xs text-[#1F2A1E]/70">
              This password reset link is invalid or incomplete. Please request a new reset link from the login screen.
            </p>
            <div className="pt-2">
              <Link
                to="/login"
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#2F5233] hover:text-[#3D6B42] hover:underline"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                Return to Login
              </Link>
            </div>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {/* New Password */}
            <div>
              <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">
                New Password
              </label>
              <div className="relative">
                <Lock className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 8 characters"
                  className="w-full h-11 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-11 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                  required
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/35 hover:text-[#1F2A1E]/70 focus:outline-none p-0.5 cursor-pointer"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Confirm Password */}
            <div>
              <label className="block text-[11px] font-bold text-[#1F2A1E]/70 uppercase tracking-wider mb-1.5">
                Confirm New Password
              </label>
              <div className="relative">
                <Lock className="w-[18px] h-[18px] absolute left-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/30" />
                <input
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Re-enter password"
                  className="w-full h-11 bg-white border border-[#E5DEC9] rounded-xl pl-11 pr-11 text-sm font-medium text-[#1F2A1E] placeholder-[#1F2A1E]/30 focus:outline-none focus:ring-2 focus:ring-[#2F5233]/20 focus:border-[#2F5233] transition-all"
                  required
                  disabled={loading}
                />
                <button
                  type="button"
                  onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#1F2A1E]/35 hover:text-[#1F2A1E]/70 focus:outline-none p-0.5 cursor-pointer"
                >
                  {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={loading}
                className="w-full h-11 flex items-center justify-center gap-2 bg-[#2F5233] hover:bg-[#3D6B42] active:bg-[#244227] text-white font-bold rounded-xl text-sm shadow-xs hover:shadow transition-all disabled:opacity-70 disabled:cursor-not-allowed cursor-pointer"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Updating Password...</span>
                  </>
                ) : (
                  <span>Reset & Save Password</span>
                )}
              </button>
            </div>

            <div className="text-center pt-2">
              <Link
                to="/login"
                className="inline-flex items-center gap-1.5 text-xs font-semibold text-[#1F2A1E]/60 hover:text-[#1F2A1E] transition-colors"
              >
                <ArrowLeft className="w-3.5 h-3.5" />
                Back to Sign In
              </Link>
            </div>
          </form>
        )}

      </div>
    </div>
  );
};

export default ResetPassword;
