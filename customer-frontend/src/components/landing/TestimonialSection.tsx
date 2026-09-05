import { FC } from 'react';
import { ScrollReveal } from './ScrollReveal';

const secondaryQuotes = [
  {
    id: 'q2',
    text: '"The electrician was punctual and professional. Booked at 9 am, fixed by noon."',
    name: 'Rohan S.',
    city: 'Bengaluru',
    service: 'Electrical',
  },
  {
    id: 'q3',
    text: '"Best at-home facial I\'ve had. Worth every rupee."',
    name: 'Meera K.',
    city: 'Hyderabad',
    service: 'Beauty & Wellness',
  },
];

export const TestimonialSection: FC = () => {
  return (
    <section
      aria-label="Customer testimonials"
      className="lp-section lp-section-dark"
    >
      <div style={{ maxWidth: 1280, margin: '0 auto' }}>

        {/* Primary pull quote */}
        <ScrollReveal>
          <div
            style={{
              marginBottom: 'clamp(3rem, 6vw, 5rem)',
              maxWidth: 760,
            }}
          >
            {/* Decorative quote mark */}
            <div
              aria-hidden="true"
              style={{
                fontFamily: 'var(--lp-font-display)',
                fontSize: 'clamp(5rem, 10vw, 8rem)',
                lineHeight: 0.6,
                color: 'var(--lp-gold)',
                opacity: 0.4,
                marginBottom: '1rem',
                userSelect: 'none',
              }}
            >
              "
            </div>

            <blockquote>
              <p
                className="lp-display"
                style={{
                  fontSize: 'clamp(1.5rem, 3.5vw, 2.75rem)',
                  color: '#FAF7F0',
                  lineHeight: 1.25,
                  marginBottom: '1.75rem',
                  fontStyle: 'italic',
                }}
              >
                Finally, a service that actually shows up. My house has never
                felt more looked-after.
              </p>
              <footer
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '1rem',
                }}
              >
                {/* Avatar placeholder */}
                <div
                  aria-hidden="true"
                  style={{
                    width: 48,
                    height: 48,
                    borderRadius: '50%',
                    background:
                      'linear-gradient(135deg, var(--lp-sage), var(--lp-gold))',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontFamily: 'var(--lp-font-body)',
                    fontWeight: 700,
                    fontSize: '1.1rem',
                    color: '#fff',
                    flexShrink: 0,
                  }}
                >
                  P
                </div>
                <div>
                  <cite
                    style={{
                      fontFamily: 'var(--lp-font-body)',
                      fontWeight: 700,
                      fontSize: '0.95rem',
                      color: '#FAF7F0',
                      fontStyle: 'normal',
                    }}
                  >
                    Priya M.
                  </cite>
                  <span
                    style={{
                      fontFamily: 'var(--lp-font-body)',
                      fontSize: '0.8125rem',
                      color: 'rgba(250, 247, 240, 0.55)',
                      marginLeft: '0.5rem',
                    }}
                  >
                    Mumbai · Home Cleaning
                  </span>
                </div>

                {/* Stars */}
                <div
                  aria-label="5 stars"
                  style={{ marginLeft: 'auto', display: 'flex', gap: 2 }}
                >
                  {Array.from({ length: 5 }).map((_, i) => (
                    <svg key={i} width="14" height="14" viewBox="0 0 14 14">
                      <path
                        d="M7 1l1.545 3.133L12 4.634l-2.5 2.437.59 3.441L7 8.9l-3.09 1.612.59-3.44L2 4.633l3.455-.501L7 1Z"
                        fill="#C9A15A"
                      />
                    </svg>
                  ))}
                </div>
              </footer>
            </blockquote>
          </div>
        </ScrollReveal>

        {/* Secondary quote cards */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(min(100%, 300px), 1fr))',
            gap: 'clamp(1rem, 2vw, 1.5rem)',
          }}
        >
          {secondaryQuotes.map((q, i) => (
            <ScrollReveal key={q.id} delay={i * 100}>
              <div
                style={{
                  background: 'rgba(250, 247, 240, 0.06)',
                  border: '1px solid rgba(250, 247, 240, 0.12)',
                  borderLeft: `3px solid var(--lp-gold)`,
                  borderRadius: '1.25rem',
                  padding: 'clamp(1.25rem, 2.5vw, 1.75rem)',
                }}
              >
                <p
                  style={{
                    fontFamily: 'var(--lp-font-body)',
                    fontSize: '0.9375rem',
                    lineHeight: 1.65,
                    color: 'rgba(250, 247, 240, 0.82)',
                    marginBottom: '1rem',
                    fontStyle: 'italic',
                  }}
                >
                  {q.text}
                </p>
                <div
                  style={{
                    fontFamily: 'var(--lp-font-body)',
                    fontSize: '0.8rem',
                    color: 'rgba(250, 247, 240, 0.5)',
                  }}
                >
                  <span style={{ color: '#FAF7F0', fontWeight: 600 }}>
                    {q.name}
                  </span>{' '}
                  · {q.city} · {q.service}
                </div>
              </div>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
};
