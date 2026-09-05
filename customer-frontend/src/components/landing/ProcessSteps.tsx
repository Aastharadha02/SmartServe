import { FC } from 'react';
import { ScrollReveal } from './ScrollReveal';

const steps = [
  {
    num: '01',
    title: 'Tell us what you need',
    body: 'Browse our services and pick what fits — whether it\'s a one-off deep clean or a regular electrician on call.',
  },
  {
    num: '02',
    title: 'We find your fit',
    body: 'We match you with a vetted, local professional. You see their profile, rating, and price upfront — no surprises.',
  },
  {
    num: '03',
    title: 'Feel the difference',
    body: 'Your pro arrives on time and does the job right. If anything\'s off, we make it right. That\'s our promise.',
  },
];

export const ProcessSteps: FC = () => {
  return (
    <section
      aria-label="How SmartServe works"
      className="lp-section lp-section-alt"
    >
      <div style={{ maxWidth: 1280, margin: '0 auto' }}>
        {/* Header */}
        <ScrollReveal>
          <div style={{ marginBottom: 'clamp(2.5rem, 5vw, 4.5rem)', textAlign: 'center' }}>
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
              How it works
            </p>
            <h2
              className="lp-display"
              style={{
                fontSize: 'clamp(2rem, 4vw, 3.25rem)',
                color: 'var(--lp-ink)',
                maxWidth: '18ch',
                margin: '0 auto',
                lineHeight: 1.15,
              }}
            >
              Three steps to a home that feels looked after.
            </h2>
          </div>
        </ScrollReveal>

        {/* Steps */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 260px), 1fr))',
            gap: 'clamp(1.5rem, 4vw, 3rem)',
            position: 'relative',
          }}
        >
          {/* Connector line — desktop only */}
          <div
            aria-hidden="true"
            style={{
              position: 'absolute',
              top: '2.5rem',
              left: '10%',
              right: '10%',
              height: 1,
              background:
                'linear-gradient(90deg, transparent, var(--lp-sage) 20%, var(--lp-sage) 80%, transparent)',
              opacity: 0.3,
              pointerEvents: 'none',
            }}
          />

          {steps.map((step, i) => (
            <ScrollReveal key={step.num} delay={i * 110}>
              <article
                style={{
                  position: 'relative',
                  padding: 'clamp(1.5rem, 3vw, 2.25rem)',
                  background: 'var(--lp-ivory)',
                  borderRadius: '1.5rem',
                  border: '1px solid rgba(31, 42, 30, 0.07)',
                }}
              >
                {/* Step number */}
                <div
                  aria-hidden="true"
                  style={{
                    fontFamily: 'var(--lp-font-display)',
                    fontSize: 'clamp(2.5rem, 4vw, 3.5rem)',
                    color: 'var(--lp-gold)',
                    lineHeight: 1,
                    marginBottom: '1rem',
                    opacity: 0.85,
                  }}
                >
                  {step.num}
                </div>

                <h3
                  style={{
                    fontFamily: 'var(--lp-font-body)',
                    fontWeight: 700,
                    fontSize: '1.1rem',
                    color: 'var(--lp-forest)',
                    marginBottom: '0.65rem',
                  }}
                >
                  {step.title}
                </h3>

                <p
                  style={{
                    fontFamily: 'var(--lp-font-body)',
                    fontSize: '0.9rem',
                    lineHeight: 1.7,
                    color: 'rgba(31, 42, 30, 0.65)',
                  }}
                >
                  {step.body}
                </p>
              </article>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
};
