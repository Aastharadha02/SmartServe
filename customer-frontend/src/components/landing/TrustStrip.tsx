import { FC } from 'react';
import { ScrollReveal } from './ScrollReveal';

const trustItems = [
  {
    id: 'rating',
    icon: '⭐',
    label: '4.8 / 5',
    sub: 'Average rating',
  },
  {
    id: 'cities',
    icon: '🏙',
    label: '12+ cities',
    sub: 'Across India',
  },
  {
    id: 'bookings',
    icon: '📅',
    label: '50,000+',
    sub: 'Happy bookings',
  },
  {
    id: 'verified',
    icon: '✓',
    label: 'Verified pros',
    sub: 'Background-checked',
  },
];

export const TrustStrip: FC = () => {
  return (
    <section
      aria-label="Trust signals"
      style={{
        background: 'var(--lp-ivory-2)',
        borderTop: '1px solid rgba(31, 42, 30, 0.07)',
        borderBottom: '1px solid rgba(31, 42, 30, 0.07)',
        padding: 'clamp(2rem, 4vw, 3rem) clamp(1.25rem, 5vw, 6rem)',
      }}
    >
      <div
        style={{
          maxWidth: 1280,
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
          gap: 'clamp(1.5rem, 3vw, 2.5rem)',
        }}
      >
        {trustItems.map((item, i) => (
          <ScrollReveal key={item.id} delay={i * 90}>
            <div
              style={{
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
                gap: '0.35rem',
              }}
            >
              <span
                style={{
                  fontSize: '1.6rem',
                  lineHeight: 1,
                  marginBottom: '0.25rem',
                }}
                aria-hidden="true"
              >
                {item.icon}
              </span>
              <span
                style={{
                  fontFamily: 'var(--lp-font-display)',
                  fontSize: 'clamp(1.3rem, 2.5vw, 1.7rem)',
                  color: 'var(--lp-forest)',
                  lineHeight: 1.15,
                }}
              >
                {item.label}
              </span>
              <span
                style={{
                  fontFamily: 'var(--lp-font-body)',
                  fontSize: '0.825rem',
                  color: 'rgba(31, 42, 30, 0.6)',
                  fontWeight: 500,
                }}
              >
                {item.sub}
              </span>
            </div>
          </ScrollReveal>
        ))}
      </div>
    </section>
  );
};
