import { FC, useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import { MagneticButton } from './MagneticButton';
import { HeroVisual } from './HeroVisual';


/** Animated organic gradient background via CSS — fallback when Paper Shaders not available */
const OrganicGradientBg: FC = () => (
  <div
    aria-hidden="true"
    style={{
      position: 'absolute',
      inset: 0,
      zIndex: 0,
      overflow: 'hidden',
    }}
  >
    {/* Gradient base */}
    <div
      style={{
        position: 'absolute',
        inset: 0,
        background:
          'radial-gradient(ellipse 80% 70% at 60% 40%, #D6EAD0 0%, #FAF7F0 55%, #F2EDE1 100%)',
      }}
    />
    {/* Floating organic blobs */}
    <div
      style={{
        position: 'absolute',
        top: '-20%',
        right: '-10%',
        width: '65%',
        paddingBottom: '65%',
        borderRadius: '60% 40% 30% 70% / 60% 30% 70% 40%',
        background: 'radial-gradient(circle at 30% 30%, #C3DFC2 0%, transparent 70%)',
        opacity: 0.55,
        animation: 'lp-blob-morph 14s ease-in-out infinite',
        willChange: 'border-radius',
      }}
    />
    <div
      style={{
        position: 'absolute',
        bottom: '-15%',
        left: '-8%',
        width: '45%',
        paddingBottom: '45%',
        borderRadius: '30% 60% 70% 40% / 50% 60% 30% 60%',
        background: 'radial-gradient(circle at 70% 70%, #E8F3E2 0%, transparent 70%)',
        opacity: 0.6,
        animation: 'lp-blob-morph 10s ease-in-out infinite reverse',
        willChange: 'border-radius',
      }}
    />
  </div>
);

export const HeroSection: FC = () => {
  const sectionRef = useRef<HTMLElement>(null);

  // Intro fade-in for copy
  const [copyVisible, setCopyVisible] = useState(false);
  useEffect(() => {
    const t = setTimeout(() => setCopyVisible(true), 120);
    return () => clearTimeout(t);
  }, []);

  return (
    <section
      ref={sectionRef}
      aria-label="SmartServe hero"
      style={{
        position: 'relative',
        minHeight: '100dvh',
        display: 'flex',
        alignItems: 'center',
        overflow: 'hidden',
      }}
    >
      {/* Animated gradient background */}
      <OrganicGradientBg />

      {/* Layout: copy left / 3D right */}
      <div
        style={{
          position: 'relative',
          zIndex: 1,
          maxWidth: 1280,
          margin: '0 auto',
          padding: 'clamp(5rem, 10vw, 8rem) clamp(1.25rem, 5vw, 4rem) clamp(3rem, 6vw, 5rem)',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 420px), 1fr))',
          gap: 'clamp(2rem, 5vw, 4rem)',
          alignItems: 'center',
          width: '100%',
        }}
      >
        {/* ── Copy block ─────────────────────────────────────── */}
        <div
          style={{
            opacity: copyVisible ? 1 : 0,
            transform: copyVisible ? 'translateY(0)' : 'translateY(32px)',
            transition: 'opacity 0.8s cubic-bezier(0.19,1,0.22,1), transform 0.8s cubic-bezier(0.19,1,0.22,1)',
          }}
        >
          {/* Eyebrow */}
          <p
            style={{
              fontFamily: 'var(--lp-font-body)',
              fontWeight: 600,
              fontSize: 'clamp(0.8rem, 1.2vw, 0.9rem)',
              letterSpacing: '0.12em',
              textTransform: 'uppercase',
              color: 'var(--lp-sage)',
              marginBottom: '1.25rem',
            }}
          >
            Your home, well cared for.
          </p>

          {/* H1 */}
          <h1
            style={{
              fontFamily: 'var(--lp-font-display)',
              fontSize: 'clamp(2.5rem, 5.5vw, 4.5rem)',
              lineHeight: 1.08,
              letterSpacing: '-0.02em',
              color: 'var(--lp-ink)',
              marginBottom: '1.5rem',
              maxWidth: '12ch',
            }}
          >
            Services that show up.{' '}
            <em style={{ fontStyle: 'italic', color: 'var(--lp-forest)' }}>
              People who care.
            </em>
          </h1>

          {/* Sub-copy */}
          <p
            style={{
              fontFamily: 'var(--lp-font-body)',
              fontSize: 'clamp(1rem, 1.5vw, 1.15rem)',
              lineHeight: 1.7,
              color: 'rgba(31, 42, 30, 0.72)',
              marginBottom: '2.5rem',
              maxWidth: '42ch',
            }}
          >
            From deep cleans to plumbing emergencies — SmartServe connects you
            to trusted professionals in your neighbourhood.
          </p>

          {/* CTAs */}
          <div style={{ display: 'flex', gap: '0.875rem', flexWrap: 'wrap', alignItems: 'center' }}>
            <MagneticButton>
              <Link
                to="/register"
                className="lp-btn-primary"
                data-cursor-interactive
                aria-label="Book a home service"
              >
                Book a service
              </Link>
            </MagneticButton>
            <Link
              to="/explore"
              className="lp-btn-ghost"
              data-cursor-interactive
              style={{ opacity: copyVisible ? 1 : 0, transition: 'opacity 1s ease 0.2s' }}
            >
              Explore services →
            </Link>
          </div>

          {/* Social proof micro strip */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '1rem',
              marginTop: '2.5rem',
              opacity: 0.65,
            }}
          >
            <span
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontSize: '0.8125rem',
                color: 'var(--lp-ink)',
                display: 'flex',
                alignItems: 'center',
                gap: '0.35rem',
              }}
            >
              ⭐ 4.8/5
            </span>
            <span
              style={{
                width: 1,
                height: 14,
                background: 'rgba(31,42,30,0.25)',
              }}
            />
            <span
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontSize: '0.8125rem',
                color: 'var(--lp-ink)',
              }}
            >
              50,000+ bookings
            </span>
            <span
              style={{
                width: 1,
                height: 14,
                background: 'rgba(31,42,30,0.25)',
              }}
            />
            <span
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontSize: '0.8125rem',
                color: 'var(--lp-ink)',
              }}
            >
              Verified pros
            </span>
          </div>
        </div>

        {/* ── Editorial Showcase Visual ───────────────────────── */}
        <div
          style={{
            position: 'relative',
            width: '100%',
            opacity: copyVisible ? 1 : 0,
            transform: copyVisible ? 'translateY(0)' : 'translateY(28px)',
            transition: 'opacity 0.9s cubic-bezier(0.19,1,0.22,1) 0.15s, transform 0.9s cubic-bezier(0.19,1,0.22,1) 0.15s',
          }}
        >
          <HeroVisual />
        </div>
      </div>

      {/* Scroll cue */}
      <div
        aria-hidden="true"
        style={{
          position: 'absolute',
          bottom: '2rem',
          left: '50%',
          transform: 'translateX(-50%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '0.4rem',
          opacity: copyVisible ? 0.4 : 0,
          transition: 'opacity 1s ease 1.4s',
        }}
      >
        <span
          style={{
            fontFamily: 'var(--lp-font-body)',
            fontSize: '0.7rem',
            letterSpacing: '0.12em',
            textTransform: 'uppercase',
            color: 'var(--lp-ink)',
          }}
        >
          Scroll
        </span>
        <svg width="16" height="24" viewBox="0 0 16 24" fill="none">
          <rect x="1" y="1" width="14" height="22" rx="7" stroke="currentColor" strokeWidth="1.5" />
          <rect
            x="6.5"
            y="5"
            width="3"
            height="6"
            rx="1.5"
            fill="currentColor"
            style={{ animation: 'none' }}
          />
        </svg>
      </div>
    </section>
  );
};
