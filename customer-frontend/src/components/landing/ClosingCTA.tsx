import { FC } from 'react';
import { Link } from 'react-router-dom';
import { ScrollReveal } from './ScrollReveal';
import { MagneticButton } from './MagneticButton';

export const ClosingCTA: FC = () => {
  return (
    <>
      {/* ── Closing CTA section ───────────────────────────────── */}
      <section
        aria-label="Get started with SmartServe"
        className="lp-section"
        style={{ textAlign: 'center' }}
      >
        <div style={{ maxWidth: 680, margin: '0 auto' }}>
          <ScrollReveal>
            <p
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontWeight: 600,
                fontSize: '0.8rem',
                letterSpacing: '0.12em',
                textTransform: 'uppercase',
                color: 'var(--lp-sage)',
                marginBottom: '0.75rem',
              }}
            >
              Ready when you are
            </p>
          </ScrollReveal>

          <ScrollReveal delay={80}>
            <h2
              className="lp-display"
              style={{
                fontSize: 'clamp(2rem, 4.5vw, 3.5rem)',
                color: 'var(--lp-ink)',
                marginBottom: '1.25rem',
                lineHeight: 1.12,
              }}
            >
              Your home deserves care.{' '}
              <em style={{ fontStyle: 'italic', color: 'var(--lp-forest)' }}>
                Let's start.
              </em>
            </h2>
          </ScrollReveal>

          <ScrollReveal delay={160}>
            <p
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontSize: 'clamp(0.95rem, 1.4vw, 1.075rem)',
                lineHeight: 1.7,
                color: 'rgba(31, 42, 30, 0.65)',
                marginBottom: '2.5rem',
                maxWidth: '46ch',
                margin: '0 auto 2.5rem',
              }}
            >
              Join thousands of households across India who trust SmartServe
              for the services that matter most.
            </p>
          </ScrollReveal>

          <ScrollReveal delay={220}>
            <div
              style={{
                display: 'flex',
                gap: '0.875rem',
                justifyContent: 'center',
                flexWrap: 'wrap',
              }}
            >
              <MagneticButton>
                <Link
                  to="/register"
                  className="lp-btn-primary"
                  data-cursor-interactive
                  style={{ fontSize: '1rem', padding: '1rem 2.25rem' }}
                  aria-label="Create a free SmartServe account"
                >
                  Get started — it's free
                </Link>
              </MagneticButton>
              <Link
                to="/login"
                className="lp-btn-ghost"
                data-cursor-interactive
                style={{ fontSize: '1rem', padding: '1rem 1.75rem' }}
              >
                Already a member? Sign in
              </Link>
            </div>
          </ScrollReveal>
        </div>
      </section>

      {/* ── Footer ────────────────────────────────────────────── */}
      <footer
        style={{
          background: 'var(--lp-ivory-2)',
          borderTop: '1px solid rgba(31, 42, 30, 0.08)',
          padding: 'clamp(1.5rem, 3vw, 2.25rem) clamp(1.25rem, 5vw, 6rem)',
        }}
      >
        <div
          style={{
            maxWidth: 1280,
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '1rem',
          }}
        >
          {/* Brand */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <span
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: 32,
                height: 32,
                borderRadius: 9,
                background: 'var(--lp-forest)',
              }}
            >
              <svg width="17" height="17" viewBox="0 0 100 100" fill="none">
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
                fontWeight: 700,
                fontSize: '0.95rem',
                color: 'var(--lp-ink)',
              }}
            >
              SmartServe
            </span>
            <span
              style={{
                fontFamily: 'var(--lp-font-body)',
                fontSize: '0.8rem',
                color: 'rgba(31, 42, 30, 0.45)',
                marginLeft: '0.5rem',
              }}
            >
              © 2025
            </span>
          </div>

          {/* Footer links */}
          <nav aria-label="Footer navigation">
            <ul
              style={{
                display: 'flex',
                gap: 'clamp(1rem, 2.5vw, 2rem)',
                listStyle: 'none',
                margin: 0,
                padding: 0,
                flexWrap: 'wrap',
              }}
            >
              {['Privacy', 'Terms', 'Contact'].map((item) => (
                <li key={item}>
                  <Link
                    to={`/${item.toLowerCase()}`}
                    style={{
                      fontFamily: 'var(--lp-font-body)',
                      fontSize: '0.8375rem',
                      color: 'rgba(31, 42, 30, 0.55)',
                      textDecoration: 'none',
                      transition: 'color 0.2s ease',
                    }}
                    onMouseEnter={(e) =>
                      ((e.target as HTMLAnchorElement).style.color =
                        'var(--lp-forest)')
                    }
                    onMouseLeave={(e) =>
                      ((e.target as HTMLAnchorElement).style.color =
                        'rgba(31, 42, 30, 0.55)')
                    }
                    data-cursor-interactive
                  >
                    {item}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </div>
      </footer>
    </>
  );
};
