import React, { useEffect, useState, useRef } from 'react';
import { useParams, useSearchParams, useNavigate, Link } from 'react-router-dom';
import { Loader2, AlertCircle, ArrowLeft, CheckCircle2 } from 'lucide-react';
import { submitOAuthCallback } from '../../api/auth';
import { useAuth } from '../../auth/useAuth';
import { useToast } from '../../hooks/useToast';
import { useTranslation } from 'react-i18next';

export const OAuthCallback: React.FC = () => {
  const { provider } = useParams<{ provider: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setSessionFromTokenResponse } = useAuth();
  const { showToast } = useToast();
  const { t } = useTranslation();

  const [loading, setLoading] = useState(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const hasSubmittedRef = useRef(false);

  const providerName = provider ? provider.charAt(0).toUpperCase() + provider.slice(1) : 'Social';

  useEffect(() => {
    if (hasSubmittedRef.current) return;

    const processCallback = async () => {
      hasSubmittedRef.current = true;
      const code = searchParams.get('code');
      const state = searchParams.get('state');
      const error = searchParams.get('error');
      const errorDescription = searchParams.get('error_description');

      if (error) {
        setErrorMessage(errorDescription || `Authentication was denied or cancelled by ${provider || 'provider'}.`);
        setLoading(false);
        return;
      }

      if (!code || !state) {
        setErrorMessage('Invalid authentication response. Missing authorization code or state parameter.');
        setLoading(false);
        return;
      }

      if (!provider) {
        setErrorMessage('Unknown authentication provider.');
        setLoading(false);
        return;
      }

      try {
        const redirectUri = `${window.location.origin}/auth/callback/${provider}`;
        const tokenResponse = await submitOAuthCallback(provider, code, state, redirectUri);
        setSessionFromTokenResponse(tokenResponse);
        setSuccess(true);
        if (tokenResponse.requires_profile_completion) {
          showToast(t('auth.complete_profile_notice', { defaultValue: 'Welcome to SmartServe! Please complete your profile details.' }), 'info');
          setTimeout(() => {
            navigate('/complete-profile', { replace: true, state: { tokenResponse } });
          }, 800);
        } else {
          showToast(t('auth.oauth_toast_success', { provider: providerName, defaultValue: `Signed in successfully with ${providerName}!` }), 'success');
          setTimeout(() => {
            navigate('/home', { replace: true });
          }, 1000);
        }
      } catch (err: any) {
        const detail = err.response?.data?.detail || 'Authentication failed. Please verify your account and try again.';
        setErrorMessage(detail);
      } finally {
        setLoading(false);
      }
    };

    processCallback();
  }, [provider, searchParams, navigate, setSessionFromTokenResponse, showToast, t, providerName]);

  return (
    <div className="min-h-screen bg-[#FAF7F0] font-sans text-[#1F2A1E] flex items-center justify-center p-6">
      <div className="w-full max-w-md bg-white border border-[#E5DEC9] rounded-2xl p-8 shadow-sm text-center">
        {loading && (
          <div className="py-8 space-y-4">
            <Loader2 className="w-10 h-10 text-[#2F5233] animate-spin mx-auto" />
            <h2 className="text-xl font-bold text-[#1F2A1E]">
              {t('auth.oauth_authenticating', { provider: providerName, defaultValue: `Authenticating with ${providerName}...` })}
            </h2>
            <p className="text-sm text-[#1F2A1E]/60">
              {t('auth.oauth_verifying', { defaultValue: 'Verifying secure credentials and establishing your session.' })}
            </p>
          </div>
        )}

        {success && (
          <div className="py-8 space-y-4">
            <CheckCircle2 className="w-10 h-10 text-emerald-600 mx-auto" />
            <h2 className="text-xl font-bold text-[#1F2A1E]">
              {t('auth.oauth_success_title', { defaultValue: 'Welcome to SmartServe!' })}
            </h2>
            <p className="text-sm text-[#1F2A1E]/60">
              {t('auth.oauth_redirecting', { defaultValue: 'Redirecting to your dashboard...' })}
            </p>
          </div>
        )}

        {errorMessage && !loading && (
          <div className="py-6 space-y-5">
            <div className="w-12 h-12 bg-red-50 border border-red-200 rounded-full flex items-center justify-center mx-auto text-red-600">
              <AlertCircle className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-red-900 mb-1.5">
                {t('auth.oauth_failed_title', { provider: providerName, defaultValue: `${providerName} Authentication Failed` })}
              </h2>
              <p className="text-sm text-red-700/90 bg-red-50/70 border border-red-200/60 rounded-xl p-3 text-left">
                {errorMessage}
              </p>
            </div>
            <div className="pt-2">
              <Link
                to="/login"
                className="w-full h-11 flex items-center justify-center gap-2 bg-[#2F5233] hover:bg-[#3D6B42] text-white font-bold rounded-xl text-sm transition-colors"
              >
                <ArrowLeft className="w-4 h-4" />
                {t('auth.oauth_return_login', { defaultValue: 'Return to Customer Login' })}
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default OAuthCallback;
