import { FC } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../auth/useAuth';

/**
 * OrganicHeroFallback — pure CSS animated blob shown when:
 * - Device is mobile / low-end (< 768px or hardwareConcurrency < 4)
 * - prefers-reduced-motion is set
 * - 3D bundle hasn't loaded yet (Suspense fallback)
 *
 * Zero JS animation dependencies. The morphing animation is driven by
 * the `lp-blob-morph` keyframe in index.css.
 */
export const OrganicHeroFallback: FC = () => {
  return (
    <div
      className="lp-blob"
      style={{
        width: '100%',
        height: '100%',
        minHeight: 360,
      }}
      aria-hidden="true"
    />
  );
};

// ─────────────────────────────────────────────────────────────────────────────
// LandingNav — sticky glass navigation bar for the public landing page.
// Separate from TopHeader (app shell) — stands alone with no AuthContext deps.
// ─────────────────────────────────────────────────────────────────────────────

interface LandingNavProps {
  scrolled: boolean;
}

export const LandingNav: FC<LandingNavProps> = ({ scrolled }) => {
  const { isAuthenticated } = useAuth();

  return (
    <header
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        zIndex: 50,
        transition: 'background 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease',
        background: scrolled
          ? 'rgba(250, 247, 240, 0.92)'
          : 'transparent',
        backdropFilter: scrolled ? 'blur(14px)' : 'none',
        WebkitBackdropFilter: scrolled ? 'blur(14px)' : 'none',
        borderBottom: scrolled ? '1px solid rgba(31, 42, 30, 0.08)' : '1px solid transparent',
        boxShadow: scrolled ? '0 2px 20px rgba(31, 42, 30, 0.06)' : 'none',
      }}
    >
      <div
        style={{
          maxWidth: 1280,
          margin: '0 auto',
          padding: '0 clamp(1.25rem, 5vw, 3rem)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          height: 72,
        }}
      >
        {/* Brand mark */}
        <Link
          to="/"
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            textDecoration: 'none',
          }}
          data-cursor-interactive
        >
          <span
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 40,
              height: 40,
              borderRadius: 12,
              background: 'var(--lp-forest)',
            }}
          >
            <svg width="22" height="22" viewBox="0 0 100 100" fill="none">
              <path
                d="M68 32C68 25.3726 62.6274 20 56 20H38C30.268 20 24 26.268 24 34C24 41.732 30.268 48 38 48H62C69.732 48 76 54.268 76 62C76 69.732 69.732 76 62 76H44C37.3726 76 32 70.6274 32 64"
                stroke="white"
                strokeWidth="12"
                strokeLinecap="round"
              />
            </svg>
          </span>
          <span
            style={{
              fontFamily: 'var(--lp-font-body)',
              fontWeight: 800,
              fontSize: '1.15rem',
              color: 'var(--lp-ink)',
              letterSpacing: '-0.01em',
            }}
          >
            SmartServe
          </span>
        </Link>

        {/* Right CTAs */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {isAuthenticated ? (
            <Link
              to="/home"
              className="lp-btn-primary"
              style={{ padding: '0.6rem 1.4rem', fontSize: '0.875rem' }}
              data-cursor-interactive
            >
              Go to app →
            </Link>
          ) : (
            <>
              <Link
                to="/login"
                className="lp-btn-ghost"
                style={{ padding: '0.6rem 1.25rem', fontSize: '0.875rem' }}
                data-cursor-interactive
              >
                Sign in
              </Link>
              <Link
                to="/register"
                className="lp-btn-primary"
                style={{ padding: '0.6rem 1.4rem', fontSize: '0.875rem' }}
                data-cursor-interactive
              >
                Get started
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};
