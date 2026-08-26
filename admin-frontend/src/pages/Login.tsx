import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Eye, EyeOff, Lock, Mail, Loader2, ShieldCheck, AlertCircle } from 'lucide-react';
import { loginAdmin } from '../api/auth';

export const Login: React.FC = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('admin@smartserve.com');
  const [password, setPassword] = useState('AdminPassword123!');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

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

      // Redirect to Admin Dashboard
      navigate('/admin/dashboard');
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
        setErrorMessage('Unable to connect to SmartServe API. Please verify the backend server is running on http://127.0.0.1:8000.');
      } else {
        setErrorMessage('An unexpected error occurred. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-4 font-sans text-slate-800">
      <div className="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-sm p-8 space-y-6">
        {/* Brand Header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-blue-50 text-[#5CA8FF] font-bold text-2xl mb-2">
            S
          </div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">SmartServe Admin</h1>
          <p className="text-xs text-slate-500 font-medium">Sign in to access the Operations Console</p>
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div className="flex items-start gap-3 p-3.5 bg-red-50 border border-red-200 rounded-xl text-red-700 text-xs font-medium animate-in fade-in">
            <AlertCircle className="w-4 h-4 flex-shrink-0 text-red-500 mt-0.5" />
            <div className="flex-1">{errorMessage}</div>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Email Field */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              Admin Email
            </label>
            <div className="relative">
              <Mail className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="admin@smartserve.com"
                className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 focus:border-[#5CA8FF] focus:bg-white transition-all"
                required
                disabled={loading}
              />
            </div>
          </div>

          {/* Password Field */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••••••"
                className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-10 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#5CA8FF]/40 focus:border-[#5CA8FF] focus:bg-white transition-all"
                required
                disabled={loading}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 focus:outline-none"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-[#5CA8FF] hover:bg-blue-600 text-white font-semibold py-2.5 px-4 rounded-xl shadow-sm hover:shadow transition-all disabled:opacity-70 disabled:cursor-not-allowed mt-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Authenticating...</span>
              </>
            ) : (
              <>
                <ShieldCheck className="w-4 h-4" />
                <span>Sign In to Admin Console</span>
              </>
            )}
          </button>
        </form>

        {/* Security Footer Note */}
        <div className="pt-2 border-t border-slate-100 text-center text-[11px] text-slate-400">
          Protected by SmartServe RBAC Authorization & Audit Engine
        </div>
      </div>
    </div>
  );
};
